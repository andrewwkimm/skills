"""Mechanical pattern checks over Python files an agent wrote.

Each check is a function that takes a parsed module and returns findings. A
finding is a code, a location, and a one-line message. The checks are
deliberately narrow: they catch patterns the code-style skill names, and they
say nothing about anything else. A task's `rubric.json` decides which codes
count against the output; the checks themselves only report.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    """One pattern match in one file."""

    code: str
    path: str
    line: int
    message: str


def _calls(tree: ast.AST) -> list[ast.Call]:
    return [node for node in ast.walk(tree) if isinstance(node, ast.Call)]


def _attr_name(func: ast.expr) -> str:
    """Returns `a.b.c` for an attribute chain, or the bare name, or ''."""
    parts: list[str] = []
    node = func
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def point_of_use_default(tree: ast.Module, path: str) -> list[Finding]:
    """`.get(key, default)` with a non-None default, or `x or {}` / `x or []`."""
    findings = []
    for call in _calls(tree):
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "get"
            and len(call.args) == 2
            and not (isinstance(call.args[1], ast.Constant) and call.args[1].value is None)
        ):
            findings.append(
                Finding("PY_DEFAULT_AT_USE", path, call.lineno, ".get(key, default) hides the missing-key decision")
            )
    for node in ast.walk(tree):
        if not (isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or)):
            continue
        last = node.values[-1]
        empty_literal = (isinstance(last, ast.Dict) and not last.keys) or (isinstance(last, ast.List) and not last.elts)
        if empty_literal:
            findings.append(
                Finding("PY_DEFAULT_AT_USE", path, node.lineno, "`or {}` / `or []` hides the missing-value decision")
            )
    return findings


def broad_except(tree: ast.Module, path: str) -> list[Finding]:
    """`except:`, `except Exception`, or `except BaseException`."""
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if node.type is None:
            findings.append(Finding("PY_BARE_EXCEPT", path, node.lineno, "bare except"))
        elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
            findings.append(Finding("PY_BROAD_EXCEPT", path, node.lineno, f"except {node.type.id}"))
    return findings


def swallowed_except(tree: ast.Module, path: str) -> list[Finding]:
    """An except body that is only `pass`, `...`, or `return None`."""
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and len(node.body) == 1:
            stmt = node.body[0]
            silent = (
                isinstance(stmt, ast.Pass)
                or (
                    isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis
                )
                or (
                    isinstance(stmt, ast.Return)
                    and (stmt.value is None or (isinstance(stmt.value, ast.Constant) and stmt.value.value is None))
                )
            )
            if silent:
                findings.append(Finding("PY_SWALLOWED_EXCEPT", path, node.lineno, "exception caught and discarded"))
    return findings


def ignore_errors_flag(tree: ast.Module, path: str) -> list[Finding]:
    """`ignore_errors=True`, which swallows every failure, not one case."""
    findings = []
    for call in _calls(tree):
        for kw in call.keywords:
            if kw.arg == "ignore_errors" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                findings.append(
                    Finding("PY_IGNORE_ERRORS", path, call.lineno, "ignore_errors=True swallows every failure")
                )
    return findings


def check_then_act(tree: ast.Module, path: str) -> list[Finding]:
    """`if path.exists():` guarding a filesystem action that has an idempotent form."""
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test
            if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
                test = test.operand
            if isinstance(test, ast.Call) and _attr_name(test.func).endswith((".exists", ".is_dir", ".is_file")):
                findings.append(
                    Finding(
                        "PY_CHECK_THEN_ACT",
                        path,
                        node.lineno,
                        "exists() check before acting; the idempotent form does not race",
                    )
                )
    return findings


def mutable_default_arg(tree: ast.Module, path: str) -> list[Finding]:
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)) or (
                    isinstance(default, ast.Call) and _attr_name(default.func) in {"list", "dict", "set"}
                ):
                    findings.append(
                        Finding("PY_MUTABLE_DEFAULT", path, node.lineno, f"mutable default argument in {node.name}")
                    )
    return findings


def self_free_methods(tree: ast.Module, path: str) -> list[Finding]:
    """Instance methods whose body never reads `self` (dunders and decorated methods excluded)."""
    findings = []
    for cls in ast.walk(tree):
        if not isinstance(cls, ast.ClassDef):
            continue
        bases = {_attr_name(b) for b in cls.bases}
        if bases & {"Protocol", "typing.Protocol", "HTMLParser"}:
            continue
        for fn in cls.body:
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if fn.name.startswith("__") or fn.decorator_list or not fn.args.args:
                continue
            receiver = fn.args.args[0].arg
            uses_receiver = any(
                isinstance(n, ast.Name) and n.id == receiver for n in ast.walk(fn) if n is not fn.args.args[0]
            )
            if not uses_receiver:
                findings.append(
                    Finding(
                        "PY_SELF_FREE_METHOD",
                        path,
                        fn.lineno,
                        f"{cls.name}.{fn.name} reads nothing from {receiver}; it is a function",
                    )
                )
    return findings


def _default_argument_nodes(tree: ast.Module) -> set[int]:
    """Ids of every node inside a parameter default, where a clock default is injection, not a hidden read."""
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            for default in node.args.defaults + node.args.kw_defaults:
                if default is not None:
                    ids.update(id(n) for n in ast.walk(default))
    return ids


def clock_or_random_inside(tree: ast.Module, path: str) -> list[Finding]:
    """Calls that read the clock or randomness outside a parameter default."""
    findings = []
    in_default = _default_argument_nodes(tree)
    names = {
        "datetime.now",
        "datetime.utcnow",
        "date.today",
        "time.time",
        "time.monotonic",
        "random.random",
        "random.randint",
        "random.choice",
        "uuid.uuid4",
    }
    for call in _calls(tree):
        if id(call) in in_default:
            continue
        name = _attr_name(call.func)
        if name in names or name.endswith((".datetime.now", ".date.today", ".datetime.utcnow")):
            findings.append(Finding("PY_HIDDEN_INPUT", path, call.lineno, f"{name}() read inside the module"))
    return findings


def magicmock_in_tests(tree: ast.Module, path: str) -> list[Finding]:
    findings = []
    for call in _calls(tree):
        name = _attr_name(call.func)
        if name.endswith(("MagicMock", "Mock")) and "create_autospec" not in name:
            findings.append(Finding("PY_MAGICMOCK", path, call.lineno, "MagicMock has no real field names or types"))
        if name.endswith(
            ("assert_called", "assert_called_once", "assert_called_with", "assert_called_once_with", "assert_any_call")
        ):
            findings.append(
                Finding("PY_ASSERT_ON_CALL", path, call.lineno, "asserts that a call happened rather than on a result")
            )
    return findings


def broad_pytest_raises(tree: ast.Module, path: str) -> list[Finding]:
    findings = []
    for call in _calls(tree):
        if _attr_name(call.func) == "pytest.raises" and call.args:
            arg = call.args[0]
            if isinstance(arg, ast.Name) and arg.id in {"Exception", "BaseException"}:
                findings.append(
                    Finding("PY_RAISES_EXCEPTION", path, call.lineno, "pytest.raises(Exception) accepts any failure")
                )
    return findings


def fstring_logging(tree: ast.Module, path: str) -> list[Finding]:
    findings = []
    levels = {"debug", "info", "warning", "error", "exception", "critical"}
    for call in _calls(tree):
        parts = _attr_name(call.func).split(".")
        is_log_call = parts[-1] in levels and parts[0] in {"logger", "log", "logging"}
        if is_log_call and call.args and isinstance(call.args[0], ast.JoinedStr):
            findings.append(
                Finding(
                    "PY_FSTRING_LOG", path, call.lineno, "f-string in a logging call is formatted even when not emitted"
                )
            )
    return findings


def sleep_in_tests(tree: ast.Module, path: str) -> list[Finding]:
    return [
        Finding("PY_SLEEP_IN_TEST", path, call.lineno, "time.sleep in a test")
        for call in _calls(tree)
        if _attr_name(call.func) == "time.sleep"
    ]


def module_level_effects(tree: ast.Module, path: str) -> list[Finding]:
    """Module-level statements that construct clients or read the environment."""
    findings = []
    suspicious = ("Client", "Session", "connect", "create_engine", "getenv", "environ")
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.Expr)):
            for call in ast.walk(node):
                if isinstance(call, ast.Call) and _attr_name(call.func).split(".")[-1].endswith(suspicious):
                    findings.append(
                        Finding(
                            "PY_IMPORT_TIME_EFFECT", path, node.lineno, f"{_attr_name(call.func)} runs at import time"
                        )
                    )
    return findings


SOURCE_CHECKS = [
    point_of_use_default,
    broad_except,
    swallowed_except,
    ignore_errors_flag,
    check_then_act,
    mutable_default_arg,
    self_free_methods,
    clock_or_random_inside,
    fstring_logging,
    module_level_effects,
]
TEST_CHECKS = [magicmock_in_tests, broad_pytest_raises, sleep_in_tests, mutable_default_arg]


def check_file(path: Path) -> list[Finding]:
    """Runs the source checks, or the test checks for a `test_*.py` file."""
    tree = ast.parse(path.read_text(), filename=str(path))
    checks = TEST_CHECKS if path.name.startswith("test_") or path.name.endswith("_test.py") else SOURCE_CHECKS
    findings: list[Finding] = []
    for check in checks:
        findings.extend(check(tree, str(path)))
    return findings


def check_tree(root: Path) -> list[Finding]:
    """Checks every Python file under root, skipping hidden tests and caches."""
    findings: list[Finding] = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts or "hidden_tests" in path.parts or ".venv" in path.parts:
            continue
        findings.extend(check_file(path))
    return findings


def main(argv: list[str]) -> int:
    """Prints findings for the paths given; exits 1 when there are any."""
    findings: list[Finding] = []
    for arg in argv[1:] or ["."]:
        path = Path(arg)
        findings.extend(check_tree(path) if path.is_dir() else check_file(path))
    for f in findings:
        print(f"{f.path}:{f.line}: {f.code}: {f.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
