Audited revisions: HTTPX 0.28.1, Datasette 1.0a23, Pydantic commit `27f95c7`, Dagster 1.13.1. Re-audit before citing a newer release.

## Contents

- [Official Python and packaging mechanics](#official-python-and-packaging-mechanics)
- [HTTPX](#httpx)
- [Datasette](#datasette)
- [Pydantic](#pydantic)
- [Dagster](#dagster)
- [Cross-repository conclusions](#cross-repository-conclusions)

## Official Python and packaging mechanics

### Observed

- A flat layout places the import package beside `pyproject.toml`. The checkout is directly importable because the working directory is on the import path.
- Direct checkout imports can conceal omitted files and undeclared dependencies.
- Distribution names and import-package names are independent.
- Installed scripts map names to importable callables through entry-point metadata.
- `__main__.py` implements `python -m package` and should delegate reusable behavior.
- Build backends differ in automatic discovery. Broad namespace discovery can include unintended directories.

### Use

- Keep one unambiguous root import package.
- Configure package inclusion explicitly when repository contents make discovery ambiguous.
- Build, inspect, install, and test the wheel from outside the checkout.
- Keep script and `__main__` adapters thin.
- Use regular packages unless independently distributed namespace portions are required.

### Limit

Official material defines mechanics, not domain architecture. Capability boundaries remain project judgment supported by repository evidence. The guidance presents flat and `src` layouts as alternatives; it does not recommend either.

Sources:

- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Python import system](https://docs.python.org/3/reference/import.html)
- [`__main__`](https://docs.python.org/3/library/__main__.html)
- [Entry points](https://packaging.python.org/en/latest/specifications/entry-points/)
- [setuptools package discovery](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)

## HTTPX

Pinned release: [0.28.1](https://github.com/encode/httpx/tree/0.28.1)

### Observed

- `httpx/` and `tests/` are root siblings.
- Most implementation modules are one level deep.
- `_transports/` is a subpackage because several transport implementations share a cohesive contract.
- `httpx/__init__.py` defines an intentional public facade.
- Optional features have named dependency groups.
- Tests organize dense behavioral areas without mechanically mirroring every private module.

### Use

- Keep a focused library shallow.
- Add a subpackage when a real implementation family and extension boundary exist.
- Test the public facade.
- Isolate optional dependencies with the capability that needs them.

### Do not copy

- `_utils.py` and broad model modules are mature accumulation, not naming guidance.
- A transport family, parallel sync and async classes, or a separately published core package requires HTTPX-like constraints.
- Dynamic re-export machinery is unnecessary without a large compatibility surface.

Key sources:

- [httpx package](https://github.com/encode/httpx/tree/0.28.1/httpx)
- [transports subpackage](https://github.com/encode/httpx/tree/0.28.1/httpx/_transports)
- [public facade](https://github.com/encode/httpx/blob/0.28.1/httpx/__init__.py)
- [pyproject.toml](https://github.com/encode/httpx/blob/0.28.1/pyproject.toml)
- [tests](https://github.com/encode/httpx/tree/0.28.1/tests)

## Datasette

Pinned release: [1.0a23](https://github.com/simonw/datasette/tree/1.0a23)

### Observed

- `datasette/` and `tests/` are root siblings.
- The application has a visible composition root while database, HTTP views, plugins, and permissions have named owners.
- The installed CLI and `python -m datasette` converge on the same command object.
- Plugin contracts and discovery have explicit modules and entry-point metadata.
- Tests are capability-oriented and exercise CLI, ASGI, database, and plugin boundaries.

### Use

- Keep one visible composition boundary.
- Give database, transport, policy, and extension behavior named owners.
- Route executable forms to one implementation.
- Create plugin architecture only for a committed extension ecosystem.

### Do not copy

- Large `app.py`, broad `cli.py`, and utility hierarchies reflect accumulated framework scope.
- Global plugin state and large shared test fixtures are not general guidance.
- The plugin system is product behavior, not baseline application structure.

Key sources:

- [pyproject.toml](https://github.com/simonw/datasette/blob/1.0a23/pyproject.toml)
- [datasette package](https://github.com/simonw/datasette/tree/1.0a23/datasette)
- [app.py](https://github.com/simonw/datasette/blob/1.0a23/datasette/app.py)
- [cli.py](https://github.com/simonw/datasette/blob/1.0a23/datasette/cli.py)
- [tests](https://github.com/simonw/datasette/tree/1.0a23/tests)

## Pydantic

Pinned commit: [`27f95c7`](https://github.com/pydantic/pydantic/tree/27f95c789b20aa23306e5ce559327db0e9a10a6e)

### Observed

- `pydantic/` and `tests/` are root siblings.
- Public capability modules live at package root.
- `_internal/`, `deprecated/`, `experimental/`, `plugin/`, and `v1/` express distinct stability and compatibility commitments.
- The public facade is explicit and tested for availability and internal leakage.
- `pydantic-core` is separately packaged because it has a language boundary, performance role, and explicit schema contract.
- Optional features and plugin installation have dedicated packaging and tests.

### Use

- Isolate substantial implementation machinery behind a tested public facade when a public library needs it.
- Give compatibility, deprecation, experimental, and plugin surfaces explicit ownership only when those commitments exist.
- Split distributions only for a genuine technical and operational boundary.

### Do not copy

- Large `main.py`, `types.py`, and `_utils.py` are not capability-naming exemplars.
- `_internal`, versioned APIs, plugins, and a second-language core are exceptional requirements.
- A focused application does not need Pydantic's compatibility structure.

Key sources:

- [pydantic package](https://github.com/pydantic/pydantic/tree/27f95c789b20aa23306e5ce559327db0e9a10a6e/pydantic)
- [public facade](https://github.com/pydantic/pydantic/blob/27f95c789b20aa23306e5ce559327db0e9a10a6e/pydantic/__init__.py)
- [export tests](https://github.com/pydantic/pydantic/blob/27f95c789b20aa23306e5ce559327db0e9a10a6e/tests/test_exports.py)
- [architecture notes](https://github.com/pydantic/pydantic/blob/27f95c789b20aa23306e5ce559327db0e9a10a6e/docs/internals/architecture.md)
- [pyproject.toml](https://github.com/pydantic/pydantic/blob/27f95c789b20aa23306e5ce559327db0e9a10a6e/pyproject.toml)

## Dagster

Pinned release: [1.13.1](https://github.com/dagster-io/dagster/tree/1.13.1)

### Observed

- Dagster is a platform monorepo with multiple Python distributions, a web UI, documentation, examples, and release automation.
- Each Python distribution has its own package root, metadata, tests, dependencies, and executable surfaces.
- Core, webserver, CLI, Pipes, and provider integrations have distinct installation roles.
- Provider distributions own provider SDK dependencies and tests.
- The core public facade is explicit.

### Use

- Separate distributions when release, installation, dependency, deployment, or ownership boundaries are real.
- Keep optional provider SDKs with provider-specific ownership.
- Partition large test suites by runtime contract when one suite becomes impractical.

### Do not copy

- `python_modules/`, dozens of distributions, deep `_core`, broad utilities, and large re-export surfaces solve platform-scale constraints.
- A focused application should not imitate Dagster's monorepo taxonomy.
- Dagster's documented `src` scaffold conflicts with this guide's flat-layout house rule. That conflict is a known cost of the house rule, not evidence against it.

Key sources:

- [python_modules](https://github.com/dagster-io/dagster/tree/1.13.1/python_modules)
- [core distribution metadata](https://github.com/dagster-io/dagster/blob/1.13.1/python_modules/dagster/setup.py)
- [provider distribution metadata](https://github.com/dagster-io/dagster/blob/1.13.1/python_modules/libraries/dagster-databricks/setup.py)
- [installation guidance](https://docs.dagster.io/getting-started/installation)

## Cross-repository conclusions

Corroborated patterns:

- A rigorous flat layout is viable with explicit packaging and installed-artifact tests.
- Focused libraries and applications benefit from one root import package and shallow capability modules.
- Subpackages are justified by cohesive implementation families, substantial internals, plugins, compatibility surfaces, or separately owned subsystems.
- Public APIs should be deliberate and tested when compatibility matters.
- Optional dependencies should remain with their capability or provider.
- Tests should follow behavior and runtime boundaries rather than mirror every private file.
- Large repository structures are evidence for their specific constraints, not targets for smaller projects.

House judgments supported by these patterns:

- Favor locality and short comprehension paths.
- Prefer capability ownership over horizontal layers.
- Permit justified abstractions but reject speculative ones.
- Avoid vague catchalls.
- Do not add a top-level Python `src` directory to a new repository.
