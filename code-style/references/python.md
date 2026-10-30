# Python

Read the principles first. This file covers what is specific to Python. [PEP 8](https://peps.python.org/pep-0008/) and the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) settle anything neither file nor the repository's tools cover; where the principles and Google disagree (function length, nested functions, docstring mood), the principles and this file win, and the departure is marked.

## Modules

- Order a module: docstring, imports, constants, types and models, then functions and classes with each public entry point above the private code it calls. Framework registration, `@overload` stacks, and decorator adjacency override that order.
- Importing a module defines names and does nothing else: no network, files, clients, environment reads, or mutable module state at import time. An executable module keeps its work in `main()` behind `if __name__ == "__main__":`.
- Import names when that reads better (`from pydantic import BaseModel`), per PEP 8; Google's modules-only rule is not adopted. Use `__all__` only when a module deliberately re-exports a public API.
- Imports go at module scope by default. An import needed only for annotations that would otherwise form a cycle goes in an `if TYPE_CHECKING:` block right after the imports. A function-level import **MUST** carry a comment naming the runtime constraint that requires it (an optional dependency, a platform module, a runtime import cycle a proportionate refactor cannot break, or a measured import cost) and be reported to the reviewer.

## Names

- PEP 8 forms. Lowercase initialisms in `snake_case` (`api_url`), capitals in `CapWords` (`APIResponse`). One leading underscore for internal names. No abbreviations made by deleting letters from a word.
- Units in names when the type does not carry them: `timeout_seconds`, `size_bytes`.
- Plural collections; mappings named by relationship (`customer_by_id`).
- Verbs that say what happens: `fetch_` for remote reads, `load_` or `read_` for local ones, `parse_` for conversion, `build_` for assembly. Predicates read as questions (`is_`, `has_`, `can_`, `should_`) and return `bool`.

## Functions and classes

- Model data as frozen pydantic models or frozen dataclasses, and put behavior in module-level functions that take and return them. That is the Go and Rust shape: a struct plus functions. A method belongs on a type only when it reads the instance's state and would be called on it, or when a protocol or framework requires it.
- Use a class with mutable state only for cohesive state that must change together, a resource lifetime, or a framework contract. Never a class to namespace functions, hold dependencies that could be parameters, or create a test seam. No `@staticmethod` unless a library's API demands it; `@classmethod` only for a named constructor. (Google 2.17)
- A shell class that holds several collaborators (a client, a session factory, a poster) keeps each method a short apply step. When a method would branch two or more ways into different effects, the decision comes from a pure function that returns a plan; a single decision beside a single effect can stay inline.
- Prefer composition. Inherit only from a framework base class or to implement an abstract interface; a reader should not need the parent open to follow the child.
- Pydantic models, dataclasses, enums, and exceptions are data. Keep business behavior off them unless it enforces an invariant or belongs to the value, such as a derived property.
- Keyword-only parameters for options, booleans, and arguments easy to transpose. `**kwargs` only to forward an open parameter set or meet a framework contract.
- A default **MUST** be safe to share and evaluate at import time: never a mutable literal or a fresh container. Use `None` as the sentinel for a per-call container, or when absence means something distinct.
- Return one kind of value from every successful path.
- Properties are cheap and side-effect free; anything doing I/O is a method. A property that only reads or writes an attribute is unnecessary: make the attribute public. (Google 2.13)
- Comprehensions for one-stage transforms and filters; loops for side effects, several steps, error handling, or `break`.
- `_validate_*` returns the validated value or raises; `_check_*` verifies a precondition and raises; `is_*`, `has_*`, `can_*`, `should_*` answer a question and return `bool`.

## Types and boundaries

- Annotate public functions and stable boundaries. Prefer abstract containers in signatures (`Sequence`, `Mapping`) and concrete ones in returns.
- Parse external data into a model at the boundary. Use a pydantic model with required fields, `alias_generator=to_camel` for camelCase APIs, and frozen when the value should not change. Declare a field optional only when the source documents it as optional, with a one-line comment saying when it is absent.
- Use `Any` only for a value whose shape is unknown by nature, such as a validator's raw input or a recursive JSON tree, and narrow it immediately. Say why next to it. A cast or ignored type diagnostic needs the same reason. (Stricter than Google 3.19.)
- `Protocol` at a consumer boundary that needs several operations; a callable for one. Never a protocol only to mock one implementation.
- Distinct outcomes get distinct types and an `isinstance` check at the caller.

## Exceptions and logging

- Catch the narrowest type the layer can handle. No bare `except`, no `except BaseException`. `except Exception` is allowed in exactly one place: the outermost boundary of a unit of work that must outlive one failure, such as a worker loop or a scheduler callback, where it logs the traceback and the item's identity and then continues. It carries a comment saying so. Do not add one where the framework already isolates the unit (a Dagster op, a request handler), and never in ordinary application code. (Google 2.4's isolation point; stricter than PEP 8.)
- Keep `try` blocks narrow; use `else` for work that should not be protected.
- Translate dependency errors where their details stop being useful, and preserve the cause with `raise ... from error`. Drop the cause (`from None`) only when it would leak a secret, and say so.
- `assert` only for internal invariants, never to validate input.
- Log a failure once, where it is handled. Logging calls take a `%`-style template and arguments, never an f-string, so the message is formatted only when emitted. (Google 3.10.1; ruff `G004` catches it when enabled.)
- Custom exceptions end in `Error` and do not repeat the package name.
- Build a message inline unless it is reused, such as one message both logged and raised. Mark interpolated values so they stand out: `f"Unsupported mode: {mode!r}."`

## Docstrings

- Public modules, classes, and functions **MUST** have a docstring. Private ones need one only when their contract, effects, or failure behavior is not obvious.
- Descriptive mood: "Returns the parsed configuration." rather than "Return". A test's docstring says what its name cannot, the input and the expected outcome: "Tests that an expired offer is excluded from the active list." (House rule; departs from PEP 257's imperative and Google's no-test-docstring advice. If a repository enables ruff `D401`, follow the linter.)
- One line by default. Add Google-style `Args`, `Returns`, and `Raises` sections only for behavior a caller cannot infer: an effect, a failure, a unit, an invariant, or an external constraint. Module docstrings are one or two sentences; architecture belongs in the repository's docs.

## Async and resources

- The code that acquires a resource owns its cleanup; use `with` and `async with`.
- Use async only for asynchronous I/O, concurrency, or a framework contract.
- Every created task has an owner that awaits or cancels it.
- Put timeouts at the boundary that owns the latency budget, and keep blocking work off the event loop.

## Tests

- Order a test module: imports, constants, support classes, support functions and builders, fixtures, then tests. Helpers always come before the tests that use them.
- One behavior per test; several assertions are fine when they describe one outcome. Arrange, act, assert, separated by blank lines.
- Parametrize equivalent cases with readable ids.
- Never `pytest.raises(Exception)`; assert the specific exception.
- Prefer handwritten fakes and real implementations. When a mock is needed and the repository uses `pytest-mock`, use the `mocker` fixture rather than `unittest.mock`: `mocker.spy` when the real code should still run, `mocker.stub` for callbacks, `mocker.create_autospec` for an injected collaborator, `mocker.patch` for a dependency that cannot be injected. Patch the name where the code under test looks it up. Never use `mocker.patch` as a context manager or decorator; the fixture owns cleanup, and that usage only warns at runtime. Use `monkeypatch` for environment variables and working directories.
- Prefer function-scoped fixtures; autouse only for isolation every test needs.
- Test a private function directly only when its public caller would bury the rule in unrelated setup.
