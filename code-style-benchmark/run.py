"""Scores agent outputs for the code-style benchmark.

Layout of the outputs directory, one leaf directory per agent run:

    <outputs>/<task>/<variant>/<run>/   e.g. outputs/webhook_events/new/run1/

For each leaf the script runs the task's hidden tests against the agent's
files, runs the agent's own tests, and runs the pattern checks. It then
aggregates by task and variant and writes `report.md` and `results.json`
into the outputs directory.

    python run.py --outputs ./outputs                 # score everything
    python run.py --outputs ./outputs --tasks webhook_events,rollout_decision
    python run.py --validate                          # hidden tests against the reference solutions

The script does not launch agents. Run each task's TASK.md through the agent
under each skill variant yourself, as many times as you want to average over,
and point this script at the results.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).parent / "checks"))
from python_checks import Finding, check_tree

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"


@dataclass
class TestCounts:
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.errors

    @property
    def pass_rate(self) -> float | None:
        return self.passed / self.total if self.total else None


@dataclass
class RunResult:
    task: str
    variant: str
    run: str
    hidden: TestCounts
    own: TestCounts
    violations: list[Finding]
    violation_codes: dict[str, int] = field(default_factory=dict)
    source_lines: int = 0
    notes: str = ""


def run_pytest(python: str, workdir: Path, target: Path) -> TestCounts:
    """Runs pytest on target with workdir on the import path and returns counts."""
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as handle:
        junit = Path(handle.name)
    try:
        subprocess.run(
            [
                python,
                "-m",
                "pytest",
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml",
                str(junit),
                "--rootdir",
                str(workdir),
                "-o",
                "pythonpath=.",
                str(target),
            ],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if not junit.exists() or junit.stat().st_size == 0:
            return TestCounts(errors=1)
        suite = ET.parse(junit).getroot()
        if suite.tag == "testsuites":
            suite = suite[0] if len(suite) else suite
        tests = int(suite.get("tests", 0))
        failures = int(suite.get("failures", 0))
        errors = int(suite.get("errors", 0))
        skipped = int(suite.get("skipped", 0))
        return TestCounts(passed=tests - failures - errors - skipped, failed=failures, errors=errors, skipped=skipped)
    finally:
        junit.unlink(missing_ok=True)


def score_run(python: str, task: str, run_dir: Path, rubric: dict) -> RunResult:
    """Scores one agent run directory for one task."""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        shutil.copytree(run_dir, work, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        hidden = TestCounts()
        if rubric.get("hidden_tests"):
            hidden_src = TASKS_DIR / task / "hidden_tests"
            hidden_dst = work / "_hidden_tests"
            shutil.copytree(hidden_src, hidden_dst)
            hidden = run_pytest(python, work, hidden_dst)
        own_tests = list(work.glob("test_*.py"))
        own = run_pytest(python, work, work) if own_tests else TestCounts()
    findings = check_tree(run_dir)
    forbidden = set(rubric.get("forbidden_codes", []))
    violations = [f for f in findings if f.code in forbidden]
    source_lines = sum(
        len(p.read_text().splitlines())
        for p in run_dir.rglob("*.py")
        if "__pycache__" not in p.parts and not p.name.startswith("test_")
    )
    notes_path = run_dir / "NOTES.md"
    return RunResult(
        task=task,
        variant=run_dir.parent.name,
        run=run_dir.name,
        hidden=hidden,
        own=own,
        violations=violations,
        violation_codes=dict(Counter(f.code for f in violations)),
        source_lines=source_lines,
        notes=notes_path.read_text() if notes_path.exists() else "",
    )


def load_rubric(task: str) -> dict:
    return json.loads((TASKS_DIR / task / "rubric.json").read_text())


def discover_runs(outputs: Path, tasks: list[str]) -> list[tuple[str, Path]]:
    runs = []
    for task in tasks:
        task_dir = outputs / task
        if not task_dir.is_dir():
            continue
        for variant_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            for run_dir in sorted(p for p in variant_dir.iterdir() if p.is_dir()):
                runs.append((task, run_dir))
    return runs


def fmt_rate(rate: float | None) -> str:
    return "n/a" if rate is None else f"{rate:.0%}"


def write_report(results: list[RunResult], outputs: Path) -> None:
    """Writes report.md (aggregated by task and variant) and results.json."""
    by_cell: dict[tuple[str, str], list[RunResult]] = defaultdict(list)
    for r in results:
        by_cell[(r.task, r.variant)].append(r)

    lines = [
        "# Code-style benchmark report",
        "",
        "| Task | Variant | Runs | Hidden tests passed | Own tests passed | Violations per run | Codes | Source lines |",  # noqa: E501
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for (task, variant), rs in sorted(by_cell.items()):
        hidden_rates = [r.hidden.pass_rate for r in rs if r.hidden.pass_rate is not None]
        own_rates = [r.own.pass_rate for r in rs if r.own.pass_rate is not None]
        codes = Counter()
        for r in rs:
            codes.update(r.violation_codes)
        code_text = ", ".join(f"{c}x{n}" for c, n in codes.most_common()) or "none"
        hidden_text = fmt_rate(mean(hidden_rates) if hidden_rates else None)
        own_text = fmt_rate(mean(own_rates) if own_rates else None)
        violations = mean(len(r.violations) for r in rs)
        source_lines = mean(r.source_lines for r in rs)
        lines.append(
            f"| {task} | {variant} | {len(rs)} | {hidden_text} | {own_text} | {violations:.1f} "
            f"| {code_text} | {source_lines:.0f} |"
        )
    lines += ["", "## Per-run detail", ""]
    for r in results:
        lines.append(f"### {r.task} / {r.variant} / {r.run}")
        lines.append(
            f"Hidden: {r.hidden.passed} passed, {r.hidden.failed} failed, {r.hidden.errors} errors. "
            f"Own: {r.own.passed} passed, {r.own.failed} failed. Violations: {len(r.violations)}."
        )
        for v in r.violations:
            lines.append(f"- `{Path(v.path).name}:{v.line}` {v.code}: {v.message}")
        lines.append("")
    manual = [
        t for t in TASKS_DIR.iterdir() if (t / "rubric.json").exists() and not load_rubric(t.name).get("hidden_tests")
    ]
    if manual:
        lines += ["## Manually graded tasks", ""]
        for t in manual:
            lines.append(
                f"- `{t.name}`: grade each run against `tasks/{t.name}/{load_rubric(t.name)['manual_rubric']}` "
                "and record the score beside this report."
            )
    (outputs / "report.md").write_text("\n".join(lines) + "\n")
    (outputs / "results.json").write_text(json.dumps([asdict(r) for r in results], indent=2, default=str) + "\n")


def validate(python: str) -> int:
    """Runs each task's hidden tests against its reference solution (or fixture)."""
    failures = 0
    for task_dir in sorted(TASKS_DIR.iterdir()):
        rubric = load_rubric(task_dir.name)
        if not rubric.get("hidden_tests"):
            continue
        source = task_dir / rubric.get("baseline", "reference")
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "work"
            shutil.copytree(source, work)
            shutil.copytree(task_dir / "hidden_tests", work / "_hidden_tests")
            counts = run_pytest(python, work, work / "_hidden_tests")
        findings = [f for f in check_tree(source) if f.code in set(rubric.get("forbidden_codes", []))]
        label = "fixture (expected to fail the bug-fix tests)" if rubric.get("baseline") == "fixture" else "reference"
        print(
            f"{task_dir.name:24} {label}: hidden {counts.passed} passed, {counts.failed} failed, "
            f"{counts.errors} errors; {len(findings)} check findings"
        )
        for f in findings:
            print(f"    {Path(f.path).name}:{f.line} {f.code}")
        if rubric.get("baseline") != "fixture" and (counts.failed or counts.errors or findings):
            failures += 1
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--outputs", type=Path, help="directory of agent outputs, <task>/<variant>/<run>/")
    parser.add_argument("--tasks", help="comma-separated task names; default all")
    parser.add_argument("--python", default=sys.executable, help="interpreter with pytest and pydantic")
    parser.add_argument(
        "--validate", action="store_true", help="check the hidden tests against the reference solutions"
    )
    args = parser.parse_args()
    args.python = os.path.abspath(
        args.python
    )  # not resolve(): a venv's python is a symlink to an interpreter without the venv's packages
    if args.validate:
        return validate(args.python)
    if args.outputs is None:
        parser.error("--outputs is required unless --validate is given")
    tasks = (
        args.tasks.split(",")
        if args.tasks
        else sorted(p.name for p in TASKS_DIR.iterdir() if (p / "rubric.json").exists())
    )
    results = []
    for task, run_dir in discover_runs(args.outputs, tasks):
        rubric = load_rubric(task)
        if not rubric.get("hidden_tests") and not rubric.get("forbidden_codes"):
            continue
        result = score_run(args.python, task, run_dir, rubric)
        results.append(result)
        print(
            f"{task}/{result.variant}/{result.run}: hidden {fmt_rate(result.hidden.pass_rate)}, "
            f"own {fmt_rate(result.own.pass_rate)}, violations {len(result.violations)}"
        )
    if not results:
        print("no runs found", file=sys.stderr)
        return 1
    write_report(results, args.outputs)
    print(f"\nwrote {args.outputs / 'report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
