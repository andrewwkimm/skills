## Contents

- [Purpose](#purpose)
- [Evidence hierarchy](#evidence-hierarchy)
- [Core findings](#core-findings)
- [Flat layout](#flat-layout)
- [Architecture and locality](#architecture-and-locality)
- [Module and package boundaries](#module-and-package-boundaries)
- [Dependency direction](#dependency-direction)
- [Public and executable surfaces](#public-and-executable-surfaces)
- [Data ownership](#data-ownership)
- [Tests](#tests)
- [Non-Python content](#non-python-content)
- [Project archetypes](#project-archetypes)
- [Contested names](#contested-names)
- [Boundary tests](#boundary-tests)
- [Practices to reject](#practices-to-reject)
- [Sources](#sources)

## Purpose

Python defines imports and packaging mechanics but does not prescribe one application architecture. This guide combines those mechanics with audited repository evidence and explicit project judgment.

The target is not the smallest tree. The target is the most sensible flat structure for current responsibilities and committed near-term work. Sensible structure preserves locality, states ownership, keeps dependency direction visible, and avoids abstractions that only move the reader elsewhere.

Rule strength follows the skill: MUST is a deterministic house rule, SHOULD is a strong default, MAY is an option. The enforcement rules in the skill entry point govern this file and every other reference it loads.

## Evidence hierarchy

Use evidence in this order:

1. Python language and import behavior.
2. Python packaging interoperability specifications.
3. Maintained PyPA and build-backend guidance.
4. Repository-local requirements and supported workflows.
5. Audited, closely analogous repository code.
6. Established practitioner analysis.
7. Generic templates and framework scaffolds.

Classify claims as:

- **Python-enforced**: required by import or runtime behavior.
- **Packaging behavior**: required or implemented by build and installation tooling.
- **Official guidance**: maintained Python or PyPA recommendation.
- **Corroborated precedent**: a bounded pattern in several analogous repositories.
- **Contextual precedent**: a project-specific pattern that fits stated constraints.
- **Project judgment**: a choice selected by this project's needs.
- **Unresolved**: evidence supports materially different ownership choices.

A lower tier may fill a gap. It does not overrule higher-tier behavior. A house rule selects among alternatives that higher tiers leave open; it does not contradict them.

## Core findings

### No universal application tree exists

Python's import system defines packages and modules. Packaging standards define distributions, metadata, entry points, and build behavior. They do not define domain packages, service layers, adapters, or application boundaries.

Treat framework examples as examples. Do not treat them as language standards.

### Modules are first-class architecture

Python provides a useful boundary below a package directory. A cohesive capability may remain one module with public functions, value types, exceptions, and private helpers.

Do not create a directory when a module states ownership clearly. Do not create one file per class or function.

### Locality is a design constraint

A common workflow should be understandable through a short sequence:

```
entry point -> orchestration -> policy and effect boundaries

```

A layer that only forwards parameters increases comprehension cost. Keep related decisions and transformations together unless a split isolates policy, hides real complexity, separates dependencies, or defines a stable boundary.

### Python may permit cycles, but the design should not

Import cycles create initialization hazards and signal unclear ownership. Keep conceptual dependencies directed even when delayed imports could make a cycle run.

### Functional design is the default

Prefer module-level functions for stateless behavior and pure functions for deterministic policy. Use classes for cohesive state, resource lifetime, enforced invariants, framework contracts, or real polymorphism.

Pydantic models, dataclasses, enums, exceptions, and typed records are declarative types, not evidence that the project needs a behavioral class layer.

## Flat layout

### House rule

New repositories MUST use a flat layout and MUST NOT add a top-level `src` directory. Existing repositories MUST keep their current layout unless migration is explicitly requested and justified.

Maintained packaging guidance presents flat and `src` layouts as alternatives with different behavior, not as a recommendation for one. This rule selects flat layout for locality and consistency across repositories that adopt the skill. It is a deliberate policy, not a claim that its tradeoffs do not exist.

Use:

```
project/
├── pyproject.toml
├── project_name/
│   ├── __init__.py
│   └── ...
└── tests/

```

A nested toolchain such as a frontend MAY use its own `src` directory. The prohibition covers the Python project only.

### Known tradeoff

The repository root is normally importable during local execution because the interpreter places the working directory first on the import path. A test can therefore pass against checkout code even when the built distribution omits a package, data file, or dependency.

### Required compensating controls

These steps are mandatory under the house rule, not optional hygiene:

1. Configure package discovery explicitly when more than one top-level Python-bearing directory exists.
2. Avoid loose production modules at repository root.
3. Build the wheel in CI.
4. Inspect wheel contents or assert required files.
5. Install the wheel into an isolated environment.
6. Change to a temporary directory outside the checkout before importing.
7. Assert the import origin resolves inside the isolated environment. Import a concrete module rather than the package root and check its `__file__`, or check `importlib.util.find_spec()` and its `submodule_search_locations`. Do not read `__file__` on a package root: a namespace package has `__file__` set to `None`, so `Path(package.__file__)` raises `TypeError`.
8. Run an import smoke test and the relevant tests without the repository root first on the import path.

Installing the wheel but running tests from the checkout root is not verification. Steps 6 and 7 are what make the check meaningful.

### Distribution and import names

A distribution name and import-package name are distinct. Keep them recognizably aligned unless compatibility requires otherwise:

```
Distribution: data-products-agents
Import:       data_products_agents

```

One distribution may technically expose several import packages. Prefer one root import package unless the packages have independently meaningful consumers or compatibility surfaces.

### Package discovery

Narrow discovery to intended packages. Broad namespace discovery at repository root can package tests, examples, or documentation unexpectedly.

Use namespace packages only when separately distributed portions must share a namespace. Do not omit `__init__.py` casually.

## Architecture and locality

### Organize by capability

Prefer product language:

```
project_name/
├── remediation/
├── oncall/
├── audit/
└── github.py

```

Avoid generic horizontal layers:

```
project_name/
├── controllers/
├── services/
├── repositories/
└── models/

```

A capability may contain policy, orchestration, and specific adapters while preserving directed imports. Physical proximity does not require semantic mixing.

### Keep comprehension paths short

A normal reader should not follow:

```
handler -> service -> manager -> processor -> repository

```

Each transition must add a real contract, hide complexity, or change ownership. Remove forwarding layers.

### Name the hidden decision

For each package and material module, identify the significant implementation decisions or complexity the boundary hides, if any, and what changes elsewhere if a hidden decision leaks into its public surface. When a boundary intentionally exposes a representation, verify that the representation is its documented contract and is tested as such. Reject accidental leakage that couples unrelated consumers to implementation details. Start from the decisions most likely to change: representation, storage format, provider payload shape, wire schema, retry and transaction strategy, and algorithm choice.

A module returning a `DataFrame`, an ORM row, a provider response object, or a `dict` keyed by internal column names publishes that representation regardless of how coherent its responsibility statement reads. This is a defect when the representation is an implementation detail. When it is the documented public contract, test its schema and mutation semantics explicitly. Otherwise return domain values and keep the internal representation inside. A mutable published record leaks the same decision more slowly, because consumers may come to depend on mutating it.

### Package nesting

Prefer:

```
project_name.module
project_name.capability.module

```

Treat this as a review trigger:

```
project_name.layer.capability.component.module

```

A deeper path may be justified for a large independently coherent subsystem, generated API, plugin family, or compatibility namespace. Nesting must improve navigation rather than reflect a taxonomy.

In this skill, nesting means import-path length, short means few hops on a comprehension path, and depth means the Ousterhout sense: a boundary is deep when it hides substantially more complexity than its public surface adds. Depth is the default goal. A shallow package is one whose exported identifiers teach a reader almost everything its implementation does; that is a defect when the package exists to contain complexity, and acceptable when it is a composition root, a compatibility facade, a registration point, or an intentionally transparent adapter.

## Module and package boundaries

### Keep code in one module when

- It serves one coherent capability.
- The main workflow reads clearly from public entry point to private helpers.
- Types and functions share dependencies and change drivers.
- A split would create forwarding imports or repeated navigation.
- The file is long because the workflow is linear rather than conceptually mixed.

### Split a module when

- A coherent subset has independent callers.
- A pure policy can be separated from effectful orchestration.
- A concrete adapter has dependencies unrelated to the policy.
- Public API and implementation details need a stability boundary.
- Resource ownership, concurrency, parsing, or protocol handling forms a deep subsystem.
- Two regions have different change drivers and can be understood independently.
- Import cost or optional dependencies should remain isolated.

Do not split by line count alone.

### Create a subpackage when

- Several cohesive modules share one responsibility.
- Multiple implementations share a proven semantic contract.
- The subsystem has its own public or extension surface.
- The subsystem has substantial internal structure that a flat set of modules would obscure.
- Optional dependencies, compatibility, generated code, or plugin implementations need an explicit boundary.

Do not create a subpackage for visual grouping, one implementation, or a future possibility.

### Shared semantics before shared abstractions

Similar method names do not prove a common model or adapter interface. Verify identity, units, time periods, corrections, errors, retries, and provenance before unifying providers.

Small duplication may be safer than a false shared abstraction.

## Dependency direction

Choose and document an import direction for each project. A common focused-application direction is:

```
entry points -> orchestration -> policy and consuming protocols
                             \-> concrete effect adapters

```

Pure policy should not import concrete databases, cloud clients, transports, process state, or framework entry points.

Concrete adapters may translate external representations into domain values. Keep translation near the representation owner.

Place a `Protocol` near the consumer that needs it. Return concrete implementations by default. Do not create `interfaces.py` or a universal repository abstraction.

Use dependency inversion when it preserves a real consumer boundary, substitution need, testability need, or domain independence. Do not invert dependencies only to imitate Clean Architecture.

## Public and executable surfaces

### `__init__.py`

Use `__init__.py` to mark regular packages and, when needed, expose a small deliberate public API.

Do not:

- Execute application work.
- Construct clients.
- Read environment configuration.
- Re-export every internal declaration.
- Hide an unstable implementation behind a broad accidental facade.

Test intentional public exports when compatibility matters.

### Internal code

Python does not enforce an internal directory rule like Go. Use leading underscores, narrow exports, documentation, and package ownership to communicate internal status.

An `_internal` subpackage is justified for a mature public library with substantial implementation machinery and a tested public facade. It is usually ceremony for an application package.

### Import contracts

Leading underscores and narrow exports communicate intent. They do not stop a persistence module importing a transport module. When a dependency restriction is stable, consequential, and reliably checkable, a repository SHOULD declare an import contract and run it in its CI gate, so a reversed arrow fails a build instead of surviving until someone notices it in review.

Start with two contracts: an `acyclic_siblings` contract rooted at the import package, which is six lines and does not grow with the tree, and one `forbidden` contract asserting that capability policy modules must not import concrete effect adapters or transport entry points. Concrete adapters MAY import capability-owned value types or consuming protocols required to implement their contract; that arrow is permitted, not an exception. Add an `independence` contract between capabilities when the second capability lands. Avoid `layers`, which encodes a horizontal ordering this guide's capability layout does not produce, and avoid `exhaustive` on first adoption.

Seed `ignore_imports` from the violations an existing repository already has, and treat that list as a burndown. The gate stays green on adoption, new violations fail immediately, and the remaining debt is visible.

Record only violations you intend to remove. An import the intended direction permits belongs in the contract as a permitted arrow, not in the ignored list. Scope the adapter contract to a capability's policy modules rather than the whole capability, so neither an orchestration module wiring an adapter nor an adapter importing a domain value type needs an exception. Mixing permitted arrows into the burndown empties it of meaning.

This is the best mechanism Python offers, not parity with Go's toolchain-enforced `internal`. Contract checks are fallible and their feedback loop is longer than a compiler's. Do not present a review question as an equivalent substitute: the review question catches boundaries that are wrong by design, and the contract catches arrows that reverse by accident, including indirect chains through an intermediate module.

The contract file itself belongs to repository guidance, not to this skill.

### Installed scripts

Declare command-line entry points in `pyproject.toml`. Route every supported executable form to one callable.

Keep `cli.py` focused on argument and output behavior. Keep business policy in ordinary modules.

### `__main__.py`

Add `__main__.py` only when `python -m project_name` is supported. It should delegate to the same callable as the installed script.

### Framework entry points

Dagster definitions, web application factories, workers, scheduled jobs, plugins, and other registered entry points should translate framework inputs, construct or receive dependencies, call ordinary orchestration, and return framework outputs.

Do not let framework decorators determine the package taxonomy.

## Data ownership

Do not centralize every structured value in `models.py`.

Keep representations near their owner:

- Provider payloads with provider decoding.
- HTTP requests and responses with transport code.
- Database rows with persistence adapters.
- Raw configuration with configuration loading.
- Validated runtime configuration with the application boundary that consumes it.
- Domain values with the policy and invariants they represent.
- Audit records with audit behavior.
- Presentation values with rendering or delivery.

A `model` or `models` module is acceptable only when it owns one cohesive canonical representation with stable semantics and legitimate consumers. Use a more specific domain name whenever possible.

Do not equate Pydantic with a models layer. Pydantic describes data and validation. It does not determine ownership.

## Tests

A repository with one distribution SHOULD use one top-level `tests/` directory. Independently built distributions MAY own separate suites when their installation, dependencies, release process, or runtime contracts differ.

Organize tests by capability, stable boundary, or observable behavior. Mirror production paths only when that improves navigation.

Prefer:

```
tests/
├── test_remediation.py
├── test_policy.py
├── test_github.py
└── integration/
    └── test_postgres.py

```

Do not create a parallel directory for every private module automatically.

Keep fixtures and fakes local to a test module until several tests share the same stable concept. Then move them to a specifically named support module or a narrow `conftest.py` scope.

Avoid generic `tests/helpers.py`, broad root fixtures, and autouse behavior that obscures setup.

Separate integration, end-to-end, plugin-installation, generated-code, or type-checker suites when their environment or execution contract differs.

Test the installed wheel from outside the checkout. Checkout imports alone do not verify packaging.

## Non-Python content

Place content according to ownership and tooling rather than Python package symmetry.

### SQL and migrations

Keep SQL beside the adapter or workflow that owns it when deployment and migration tooling permit. Put migrations in the location expected by the migration system, with clear database ownership.

Do not place every query in a global `sql/` directory if ownership becomes unclear.

### Templates and static assets

Keep templates and static assets with the feature or delivery boundary that consumes them. Declare package-data inclusion explicitly and verify wheel contents.

### Generated files

Place generated code in a named package or directory that identifies its generator and owner. Mark it generated. Keep regeneration commands deterministic. Do not edit generated output manually.

### Notebooks

Keep notebooks outside the import package unless they are shipped runtime assets. Treat them as exploration, analysis, or documentation. Move reusable production behavior into normal modules.

### Fixtures and sample data

Keep test fixtures under the narrowest test boundary that owns them. Keep operational policy data with the production capability that reads it. Do not mix them.

### Frontends and other toolchains

Give each independent toolchain its own root directory such as `ui/`. A nested frontend may use its own `src/`; the prohibition applies to the Python project layout.

## Project archetypes

A question answered by this section needs no further evidence.

### Focused library

```
project/
├── pyproject.toml
├── project_name/
│   ├── __init__.py
│   ├── capability.py
│   └── errors.py
└── tests/
    ├── test_capability.py
    └── test_public_api.py

```

Add subpackages only for cohesive capability families or substantial internals.

### CLI application

```
project/
├── pyproject.toml
├── project_name/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── run.py
│   └── <capability>.py
└── tests/
    ├── test_cli.py
    └── test_<capability>.py

```

`run.py` is valid only when it owns real orchestration. Do not create it merely because this example contains it.

### Service or worker

```
project/
├── pyproject.toml
├── project_name/
│   ├── __init__.py
│   ├── config.py
│   ├── runtime.py
│   ├── <domain>.py
│   ├── http.py
│   └── postgres.py
├── migrations/
└── tests/
    ├── test_<domain>.py
    └── integration/

```

Use specific transport and technology names only when those modules own real behavior.

### Data pipeline or agent application

```
project/
├── pyproject.toml
├── project_name/
│   ├── __init__.py
│   ├── config.py
│   ├── audit.py
│   ├── <workflow>/
│   │   ├── __init__.py
│   │   ├── policy.py
│   │   ├── orchestration.py
│   │   └── <provider>.py
│   └── entrypoints/
│       └── <framework>.py
└── tests/
    ├── <workflow>/
    └── integration/

```

Do not create `entrypoints/`, `policy.py`, or `orchestration.py` mechanically. Use them only when each owns enough real behavior to justify the boundary. A focused workflow may remain one module.

### Multiple optional providers

Keep each provider's payloads, translation, client behavior, and dependency imports in a specifically named module or subpackage. Introduce a shared protocol only after consuming behavior proves shared semantics.

Use optional dependency groups for provider SDKs when installations should remain focused.

### Multiple distributions

This shape is exceptional. Use it only when release, installation, dependency, ownership, or deployment boundaries are independently meaningful. Keep release-coupled packages in one distribution unless the split solves a concrete operational problem.

```
project/
├── pyproject.toml            # workspace or build coordination only
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   ├── project_core/
│   │   └── tests/
│   └── provider_x/
│       ├── pyproject.toml
│       ├── project_provider_x/
│       └── tests/
└── integration_tests/        # cross-distribution behavior

```

Require:

1. Independent build metadata per distribution.
2. Explicit dependency direction between distributions, with no cycles.
3. Independent installation or release value, stated concretely.
4. Per-distribution artifact verification using the flat-layout controls above.

Add cross-distribution compatibility tests when consumers can install mismatched versions.

## Contested names

**core.** Use only when it denotes a stable central capability understood by the product. Reject it when it means "important code" or becomes a dependency magnet.

**app and application.** Use only for a specific composition or runtime boundary. Prefer a domain or executable name when possible.

**domain.** Use only when the package owns a coherent domain model and policy used by distinct boundaries. Do not place all business code under a ceremonial domain layer.

**services.** Usually vague. Use the capability or effect name. Permit it only when it names one precise responsibility.

**models.** Avoid as a general container. Permit only one cohesive representation with stable semantics and clear consumers. Prefer specific names.

**types and handlers.** The defect is mixed ownership, not the filename. Reject them when they collect unrelated declarations. Permit one when its responsibility is precise and the name reads clearly at the import site.

**adapters.** Use only when several concrete adapters form a real family and the extra package improves navigation. For a focused application, `github.py`, `postgres.py`, or `slack.py` is usually clearer.

**api.** Specify the protocol or responsibility when possible, such as `http`, `graphql`, `github`, or `public_api`.

**utils, common, helpers, shared, and misc.** Reject. Move behavior to the capability that owns it or give a narrow module a specific name.

## Boundary tests

Accept a package or module only when most answers are clear:

1. What capability, invariant, representation, or effect does it own?
2. Who imports it?
3. What may it import?
4. Which changes should remain inside it?
5. Does its name describe the behavior without reading its contents?
6. Does it shorten or lengthen the common comprehension path?
7. Does it avoid cycles and bidirectional ownership?
8. Does it contain real behavior or stable representation rather than a category of declarations?
9. Would removing the boundary make ownership less clear?
10. Is the boundary needed now or for committed work?

If the only argument is symmetry, file length, testing convenience, or hypothetical growth, reject it.

## Practices to reject

- A top-level `src` directory in a new repository (MUST).
- Restructuring an existing repository as incidental cleanup (MUST).
- Loose production modules at repository root.
- Generic layer trees copied from Clean Architecture, Java, Rails, or framework scaffolds.
- One file per class or function.
- Packages split by arbitrary line limits.
- Catchall utility, service, model, or interface modules.
- Import cycles hidden with local imports (MUST).
- Re-exporting an entire internal tree through `__init__.py`.
- Side-effectful package imports.
- A plugin system before external extensions exist.
- Namespace packages before independently distributed portions exist.
- Multiple distributions without independent release or installation value.
- Mirroring a large framework repository in a focused application.
- Citing popularity as proof of universal design.
- Claiming installed-artifact verification without out-of-checkout execution.

## Sources

- [Python import system](https://docs.python.org/3/reference/import.html)
- [`__main__` and `python -m`](https://docs.python.org/3/library/__main__.html)
- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Distribution package vs import package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/)
- [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/)
- [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [setuptools package discovery](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)
- [Packaging namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/)
