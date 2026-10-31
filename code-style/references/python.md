# Python

Read the principles first. This file covers what is specific to Python. Target the interpreter the repository pins (3.12 or later is assumed). [PEP 8](https://peps.python.org/pep-0008/) and the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) settle anything neither file nor the repository's tools cover; where the principles and Google disagree (function length, nested functions, docstring mood), the principles and this file win, and the departure is marked. `ruff format` and the repository's linters settle layout; do not restate or fight them.

## Modules

- Order a module: docstring, imports, constants, types and models, then functions and classes with each public entry point above the private code it calls. Framework registration, `@overload` stacks, and decorator adjacency override that order.
- Importing a module defines names and does nothing else: no network, files, clients, environment reads, or mutable module state at import time. An executable module keeps its work in `main()` behind `if __name__ == "__main__":`.
- Import names when that reads better (`from pydantic import BaseModel`), per PEP 8; Google's modules-only rule is not adopted. Use `__all__` only when a module deliberately re-exports a public API.
- Imports go at module scope by default. An import needed only for annotations that would otherwise form a cycle goes in an `if TYPE_CHECKING:` block right after the imports. A function-level import **MUST** carry a comment naming the runtime constraint that requires it (an optional dependency, a platform module, a runtime import cycle a proportionate refactor cannot break, or a measured import cost) and be reported to the reviewer.
- Module-level state is constants and immutable lookup tables. A cache, a client, or a counter at module level is a hidden parameter to every function in the module; give it an owner (principle 9).

## Names

- PEP 8 forms. Lowercase initialisms in `snake_case` (`api_url`), capitals in `CapWords` (`APIResponse`). One leading underscore for internal names. No abbreviations made by deleting letters from a word.
- Units in names when the type does not carry them: `timeout_seconds`, `size_bytes`.
- Plural collections; mappings named by relationship (`customer_by_id`).
- Verbs that say what happens: `fetch_` for remote reads, `load_` or `read_` for local ones, `parse_` for conversion, `build_` for assembly. Predicates read as questions (`is_`, `has_`, `can_`, `should_`) and return `bool`.
- `_validate_*` returns the validated value or raises; `_check_*` verifies a precondition and raises.

## Data, functions, and classes

The default shape is the one Go and Rust force: a data type plus functions that take and return it. Python lets a class absorb a whole workflow, and the result is a function split into methods that pass their state through `self`, which is the hidden-parameter problem of principle 1 in a different costume.

- Model data as frozen dataclasses, or pydantic models where the data crosses a boundary and needs validation. Put behavior in module-level functions that take and return them.
- A method belongs on a type when it reads the instance's state and callers would naturally call it on the instance (`offer.is_active(now)`), or when a protocol, framework, or dunder requires it. A pure method on a frozen type is fine; it is the Go shape.
- Use a class with mutable state only for state that several operations must share and change together (a cache with its refresh schedule, a worker with its thread), a resource lifetime (a client holding a connection), or a framework contract. Never a class to namespace functions, to hold dependencies that could be parameters, or to create a test seam. No `@staticmethod` unless a library's API demands it; `@classmethod` only for a named constructor. (Google 2.17)
- A class that holds collaborators (a session factory, a client, a poster) is shell. Its methods are the sequence of effects, each a few lines. The test for each method: if it reads nothing from `self`, it is a module function; if it reads only settings values, it is a module function that takes those values; if it branches two or more ways into different effects, the decision is a pure function that returns a plan (a small frozen type per outcome) and the method applies it, while a single decision beside a single effect stays inline. What remains on the class is the part that genuinely needs the collaborators.
- A workflow (load, decide, write) is a function. When it needs many collaborators, pass them, or group them in a frozen dataclass that is passed in; do not turn the workflow into a class so that its steps can reach them through `self`.

  ```python
  # A method that uses none of self; it is a function in disguise.
  class ReportRunner:
      def _summarize(self, rows: Sequence[Row]) -> Summary: ...

  # The same logic as a function. It is testable with values and reusable without an instance.
  def summarize(rows: Sequence[Row]) -> Summary: ...
  ```

- Prefer composition. Inherit only from a framework base class or to implement an abstract interface; a reader should not need the parent open to follow the child.
- Pydantic models, dataclasses, enums, and exceptions are data. Keep business behavior off them unless it enforces an invariant or belongs to the value, such as a derived property.
- Keyword-only parameters for options, booleans, and arguments easy to transpose. `**kwargs` only to forward an open parameter set or meet a framework contract.
- A default **MUST** be safe to share and evaluate at import time: never a mutable literal or a fresh container. Use `None` as the sentinel for a per-call container, or when absence means something distinct.
- Return one kind of value from every successful path.
- Properties are cheap and side-effect free; anything doing I/O is a method. A property that only reads or writes an attribute is unnecessary: make the attribute public. (Google 2.13)
- Comprehensions for one-stage transforms and filters; loops for side effects, several steps, error handling, or `break`. A nested or chained comprehension is a loop that has lost its names.

## Types and boundaries

- Annotate public functions and stable boundaries. Prefer abstract containers in signatures (`Sequence`, `Mapping`) and concrete ones in returns.
- Parse external data into a model at the boundary. Use a pydantic model with required fields, `alias_generator=to_camel` for camelCase APIs, and frozen when the value should not change. Declare a field optional only when the source documents it as optional, with a one-line comment saying when it is absent.

  ```python
  # Chained defaults: an error body, a missing key, and an empty page all become [].
  rows = payload.get("data", {}).get("items") or []

  # The envelope is a model, so an error body and a missing key fail here, by name.
  page = Page.model_validate(payload)
  rows = page.data.items  # an empty list is a real result, handled by the caller
  ```

- Use `Any` only for a value whose shape is unknown by nature, such as a validator's raw input or a recursive JSON tree, and narrow it immediately. Say why next to it. A cast or ignored type diagnostic needs the same reason. (Stricter than Google 3.19.)
- `Protocol` at a consumer boundary that needs several operations; a callable for one. Never a protocol only to mock one implementation.
- Distinct outcomes get distinct types and an `isinstance` check at the caller.

## Exceptions and logging

- Catch the narrowest type the layer can handle. No bare `except`, no `except BaseException`. `except Exception` is allowed in exactly one place: the outermost boundary of a unit of work that must outlive one failure, such as a worker loop or a scheduler callback, where it logs the traceback and the item's identity and then continues. It carries a comment saying so. Do not add one where the framework already isolates the unit (an orchestrator task, a request handler), and never in ordinary application code. (Google 2.4's isolation point; stricter than PEP 8.)
- Keep `try` blocks narrow; use `else` for work that should not be protected.
- Where principle 2 lets a case be defined away, use the library's flag for exactly that case rather than a check-then-act pair or a broad `except`: `Path.unlink(missing_ok=True)`, `Path.mkdir(parents=True, exist_ok=True)`, a client's `not_found_ok`. With no such flag, use `contextlib.suppress` with the one exception. Never a flag that swallows every error, such as `shutil.rmtree(ignore_errors=True)`. A create-if-absent flag (`exists_ok=True`) usually returns the existing resource without comparing its settings, so check the settings that matter or fail.
- Translate dependency errors where their details stop being useful, and preserve the cause with `raise ... from error`. Drop the cause (`from None`) only when it would leak a secret, and say so.
- `assert` only for internal invariants, never to validate input.
- Log a failure once, where it is handled. Logging calls take a `%`-style template and arguments, never an f-string, so the message is formatted only when emitted. (Google 3.10.1; ruff `G004` catches it when enabled.)
- Custom exceptions end in `Error` and do not repeat the package name. Carry the upstream code or identifier as a field when a caller or a reader of the log will need it.
- Build a message inline unless it is reused, such as one message both logged and raised. Mark interpolated values so they stand out: `f"Unsupported mode: {mode!r}."`

## Docstrings

- Public modules, classes, and functions **MUST** have a docstring. Private ones need one only when their contract, effects, or failure behavior is not obvious.
- Descriptive mood: "Returns the parsed configuration." rather than "Return". A test's docstring says what its name cannot, the input and the expected outcome. (House rule; departs from PEP 257's imperative and Google's no-test-docstring advice. If a repository enables ruff `D401`, follow the linter.)
- One line by default. Add Google-style `Args`, `Returns`, and `Raises` sections only for behavior a caller cannot infer: an effect, a failure, a unit, an invariant, or an external constraint. Module docstrings are one or two sentences; architecture belongs in the repository's docs.

## Pipelines

How principle 3 looks in an orchestrated Python pipeline, whatever the framework.

- The task function takes its partition or run window as a parameter from the framework and passes it down; nothing below reads the clock or the framework context.
- Write the output with a replace operation on the partition or key (`WRITE_TRUNCATE` on a partition decorator, a `MERGE`, a temporary table swapped in), and name the task with a verb and its output (`load_invoice_lines_partition`), not its mechanism (`sync_billing_api`).
- Resources (clients, connections) come from the framework's resource mechanism or a parameter, not from module-level construction.
- Retry policy lives on the task, where idempotency is known, and is the repository's shared policy unless a comment says why this task differs.

## Async and resources

- The code that acquires a resource owns its cleanup; use `with` and `async with`. A function that receives an open resource does not close it.
- Use async only for asynchronous I/O, concurrency, or a framework contract.
- Every created task has an owner that awaits or cancels it.
- Put timeouts at the boundary that owns the latency budget, and keep blocking work off the event loop.

## Tests

- Order a test module: imports, constants, support classes, support functions and builders, fixtures, then tests. Helpers always come before the tests that use them.
- One behavior per test; several assertions are fine when they describe one outcome. Arrange, act, assert, separated by blank lines.
- Parametrize equivalent cases with readable ids.
- Never `pytest.raises(Exception)`; assert the specific exception, and `match=` on the part of the message that carries the rule.
- When a mock is needed and the repository uses `pytest-mock`, use the `mocker` fixture rather than `unittest.mock`: `mocker.spy` when the real code should still run, `mocker.stub` for callbacks, `mocker.create_autospec` for an injected collaborator, `mocker.patch` for a dependency that cannot be injected. Patch the name where the code under test looks it up. Never use `mocker.patch` as a context manager or decorator; the fixture owns cleanup, and that usage only warns at runtime. Use `monkeypatch` for environment variables and working directories.
- A fake for an external service is a small class with the real method names and a failure mode, built once in the test module or `conftest.py`. `MagicMock` has no field names or types, so a test built on one passes against the wrong shape.
- Prefer function-scoped fixtures; autouse only for isolation every test needs.
