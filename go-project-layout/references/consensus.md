## Contents

- [Purpose](#purpose)
- [Evidence hierarchy](#evidence-hierarchy)
- [Core findings](#core-findings)
- [Contested directory and package names](#contested-directory-and-package-names)
- [Integration-heavy batch services](#integration-heavy-batch-services)
- [Process boundaries and package state](#process-boundaries-and-package-state)
- [Project archetypes](#project-archetypes)
- [Package-boundary test](#package-boundary-test)
- [Keep import paths short](#keep-import-paths-short)
- [Dependency rules](#dependency-rules)
- [Naming rules](#naming-rules)
- [Repository precedent](#repository-precedent)
- [Source assessment](#source-assessment)
- [Practices to reject](#practices-to-reject)
- [Decision record template](#decision-record-template)

## Purpose

This reference establishes a durable decision framework for Go repository layout. It does not prescribe one tree. Go's toolchain defines package and import behavior, while repository structure follows project constraints.

This is a synthesis of Go toolchain behavior, official guidance, and audited repositories selected for analogy to common project shapes. It is not a measured survey of community practice, and agreement among the audited repositories is not proof of a Go rule.

Agreement is strongest on package cohesion, dependency direction, naming, structural restraint, and deliberate API boundaries. It is weak on universal directory names beyond the tool-enforced meaning of `internal`. The corpus does not cover embedded targets, WebAssembly, or plugin ecosystems beyond the cited examples.

## Evidence hierarchy

Use sources in this order:

1. Go language and toolchain behavior

2. Current official Go documentation

3. Official Go review and naming guidance

4. The Uber Go Style Guide

5. Established practitioner analysis

6. Repository precedent

7. Generic layout templates

A lower tier may fill a gap. It must not overrule a higher tier without a clear compatibility or age issue.

Label claims as:

- **Go-enforced**: required by the language or toolchain.

- **Official guidance**: recommended or illustrated by the Go project.

- **Style rule**: an organization's documented convention.

- **Corroborated precedent**: the same bounded pattern appears in several audited, analogous repositories.

- **Contextual precedent**: a repository-specific design that worked under stated constraints.

- **Project judgment**: a choice derived from this project's requirements rather than a general Go rule.

- **Unresolved**: evidence supports materially different choices and requires human judgment.

## Core findings

### No universal tree exists

The official Go module-layout documentation presents several layouts for simple packages, commands, multiple packages, multiple commands, and servers. It says server repositories vary widely. These are examples and recommendations, not a mandatory scaffold. [Organizing a Go module](https://go.dev/doc/modules/layout)

The `golang-standards/project-layout` repository explicitly says it is not an official standard. Russ Cox challenged its standard-like framing and its claim to represent common Go practice. Treat it as a catalog, not authority. [Repository](https://github.com/golang-standards/project-layout) and [Russ Cox's critique](https://github.com/golang-standards/project-layout/issues/117)

### Packages are the real architecture

A Go source directory is a package boundary. Adding directories changes import paths, visibility, dependencies, and ownership. Do not create directories for visual symmetry alone.

Import cycles are forbidden. Dependency direction must therefore be designed, not deferred. [Go specification](https://go.dev/ref/spec)

Package names should be short, clear, lowercase, and meaningful in client code. Avoid names that collect unrelated code. [Package names](https://go.dev/blog/package-names), [Effective Go: Names](https://go.dev/doc/effective_go#names), and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)

### Start from demonstrated needs

The official layout guide permits a simple package or command at the module root. Add packages when responsibilities, reuse, privacy, ownership, or dependency control justify them. [Organizing a Go module](https://go.dev/doc/modules/layout)

Alex Edwards reaches the same practical conclusion: structure should grow from demonstrated needs, not a prebuilt architecture. [Eleven Tips for Structuring Your Go Projects](https://www.alexedwards.net/blog/11-tips-for-structuring-your-go-projects)

### Treat committed requirements as current constraints

Structural restraint does not require the smallest possible tree. A committed executable, consumer, implementation, deployment unit, or meaningful ownership boundary in the active implementation horizon may justify an abstraction before the entire feature is complete. An uncommitted possibility may not.

Apply four tests:

1. The requirement is approved and scheduled in the current implementation plan.

2. The boundary will have a real consumer, implementation, or working vertical slice in that plan.

3. The abstraction preserves known semantic differences.

4. The repository does not contain empty placeholder packages while waiting for future work.

This is project judgment derived from incremental-design guidance. It is not a Go toolchain rule.

### `internal` has precise semantics

For an import path containing an `internal` segment, code outside the tree rooted at the parent of that `internal` directory cannot import the package. This is enforced by the Go toolchain. Placement determines the visibility boundary. [Go command documentation](https://pkg.go.dev/cmd/go#hdr-Internal_Directories)

Use `internal` when the repository does not support external imports of implementation packages. Do not treat it as an architecture or place everything beneath it without considering the intended boundary.

### `cmd` is a convention

A `cmd/<binary>` directory normally contains one `package main` for one executable. It is useful when a repository has multiple commands, mixes commands with importable packages, or needs a clear entry-point boundary. It is not required for a simple single command. [Organizing a Go module](https://go.dev/doc/modules/layout)

Subcommands of one executable do not require separate `cmd` directories. They are application behavior, often implemented beneath the main package or in an internal CLI package.

The filename `main.go` is conventional. The toolchain requires a `main` package with a `main` function, not that filename. [Organizing a Go module](https://go.dev/doc/modules/layout)

### Keep `main` explicit and testable

The Uber guide recommends calling `os.Exit` or `log.Fatal` only from `main`, avoiding mutable globals, avoiding side-effectful `init`, and giving goroutines explicit lifecycles. These rules favor a thin process boundary and explicit composition. [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)

A thin `main` does not require a generic `app` package. Put behavior in packages named for actual responsibilities.

### Interfaces belong to consumers

Go review guidance recommends defining interfaces where they are consumed and returning concrete types by default. Create an interface after a consumer demonstrates the required method set. [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)

Rob Pike's small-interface guidance supports this default but is a design principle, not a layout specification. [Go Proverbs](https://go-proverbs.github.io/)

## Contested directory and package names

### `model`

`model` is not forbidden. The official module-layout page uses `internal/model` as a neutral example. That example proves acceptability, not universal endorsement. [Organizing a Go module](https://go.dev/doc/modules/layout)

Use `model` when all of these hold:

- It owns a coherent canonical representation.

- The types share semantics, invariants, or one stable representational role. Behavior strengthens the package but is not required.

- Multiple legitimate consumers need that representation.

- Client expressions such as `model.Actor` are clear.

- It excludes HTTP payloads, database rows, file-decoding types, and unrelated structs.

Reject `model` when it means "all structs" or "objects shared by everything." Prefer ownership-based types such as `scenario.Scenario`, `sim.State`, and `sqlite.Row`.

The official package-naming article warns about broad names such as `types`, `interfaces`, `util`, `common`, and `misc`. Its test is cohesion and client readability, not a blacklist detached from context. [Package names](https://go.dev/blog/package-names)

### `pkg`

`pkg` has no toolchain semantics. It does not make packages public, stable, or supported.

Use ordinary top-level package directories for intentionally importable packages. Use `internal` for unsupported implementation. Add `pkg` only when the repository deliberately uses it as a documented navigation convention and the benefit exceeds the extra path element.

Kubernetes shows that `pkg` can work in a large repository with staging modules, generated APIs, release machinery, and historical compatibility constraints. Those constraints are not a mandate for new applications. See [large-system controls](audited-large-system-controls.md).

The `golang-standards/project-layout` repository presents `pkg` as optional, while Russ Cox disputes its prevalence. Do not scaffold it by default. Treat the [repository](https://github.com/golang-standards/project-layout) and [critique](https://github.com/golang-standards/project-layout/issues/117) as living primary-source context, not audited repository precedent.

### `app` and `application`

These names are valid only when they denote a specific orchestration boundary that callers can understand. They often become dependency-wiring or use-case catchalls.

Prefer names from the product vocabulary. For example, use `sim`, `scenario`, `experiment`, or `report` when those names describe the capability more precisely.

### `engine`

`engine` is acceptable when the product itself calls a cohesive reusable runtime an engine. It is too broad when it hides state transitions, scheduling, rendering, storage, and orchestration under one package.

Use a narrower domain term when possible. For a simulation product, `sim` or `simulation` usually states the responsibility better.

### `storage`, `database`, and technology names

Use a capability name such as `storage` only when the package exposes one coherent storage abstraction to multiple implementations or consumers.

Use a technology name such as `sqlite`, `postgres`, or `s3` when the package is a concrete adapter. Put small interfaces in consuming packages rather than a central repository-interface package.

Ben Johnson's dependency-oriented package layout is a useful example of separating domain behavior from adapters. It is one architecture, not a standard. [Standard Package Layout](https://www.gobeyond.dev/standard-package-layout/)

### `web`, `http`, and `api`

Use `http` when the package provides HTTP-specific behavior and the name reads clearly. Use `web` when it owns a broader browser-facing boundary, including routes, handlers, embedded assets, or web presentation.

The name `api` is often vague. Specify the protocol or capability where possible.

### `src`

Do not add a top-level `src` directory for ordinary Go code. Modules and packages already define the source structure, so the extra level usually communicates nothing.

A nested frontend project may use `ui/src` because `src` belongs to that toolchain's conventions, not Go's import organization. Audited mixed repositories use project-specific frontend layouts. This is precedent, not a Go rule. See [full-stack and multi-binary repositories](audited-full-stack-and-multi-binary.md).

## Integration-heavy batch services

Trace one production use case before accepting the package tree:

```text
source adapter → source-native record → normalization → domain transformation
→ reconciliation → publication → audit → optional notification

```

Use that trace to assign ownership:

- Keep vendor-native decoding and query rows in the concrete adapter.

- Introduce a canonical domain record only after defining shared semantics for identity, units, time periods, adjustments, corrections, and provenance.

- Put interfaces in consuming packages after the consumer's required behavior is known. Future vendors alone do not justify an interface.

- Keep orchestration separate from leaf adapters when the orchestration expresses a real workflow, retry boundary, or transaction boundary.

- Keep publication success distinct from optional notification success.

- Treat configuration, migrations, embedded queries, and policy data as owned inputs, not generic package categories.

- Do not create empty provider packages. Add a provider with its first end-to-end implementation and tests.

For scheduled or backfilled work, verify that the proposed boundaries can express idempotency, explicit period inputs, reconciliation, audit lineage, and deterministic replay. These concerns may justify packages only when they own implemented behavior; they do not justify speculative layers.

This follows the same package-cohesion and consumer-owned-interface principles in [Package names](https://go.dev/blog/package-names) and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments). It is an application of those principles, not a separate official layout standard.

## Process boundaries and package state

A small `main` is a style and testability pattern, not a directory rule. Keep immediate process termination in `main`. Use a same-package `run` function when passing arguments, streams, environment, or other process inputs makes behavior easier to test and errors easier to return. Do not create `run.go`, an `app` package, or another layer solely to follow this pattern.

Mutable package-scoped state deserves review because it can hide dependencies, lifecycle, synchronization, and test reset behavior. Prefer explicit instance ownership when practical. Accept package state when the package genuinely owns a process-wide registry, cache, immutable table, sentinel, or other singleton-like resource and documents its concurrency and lifecycle constraints.

These are practitioner-informed design heuristics. See [practitioner perspectives](practitioner-perspectives.md) for their sources and limits.

## Project archetypes

### Small library

Start with:

```text
project/
├── go.mod
├── package.go
└── package_test.go

```

Add subpackages only for distinct reusable capabilities. Every externally importable package creates a potential dependency surface. An explicit support policy, published API promise, or established consumer relationship creates the compatibility commitment.

### Single CLI

Start with either:

```text
project/
├── go.mod
├── main.go
└── internal/
    └── <capability>/

```

or use `cmd/<binary>` when root separation improves the repository:

```text
project/
├── cmd/
│   └── tool/
│       └── main.go
└── internal/
    └── <capability>/

```

Do not create one command directory per CLI subcommand.

### Multiple binaries

Use:

```text
project/
├── cmd/
│   ├── server/
│   │   └── main.go
│   └── worker/
│       └── main.go
└── internal/
    └── <shared application capability>/

```

Keep binaries thin where practical. Share behavior through coherent packages, not a generic `shared` package.

### Service

A reasonable starting shape is:

```text
project/
├── cmd/
│   └── service/
│       └── main.go
├── internal/
│   ├── <domain capability>/
│   ├── http/
│   └── postgres/
└── migrations/

```

Use responsibility-based packages. Do not add `handlers`, `services`, `repositories`, `models`, and `controllers` solely to resemble another framework.

### Full-stack local web application

A reasonable starting shape is:

```text
project/
├── cmd/
│   └── product/
│       └── main.go
├── internal/
│   ├── <domain capability>/
│   ├── web/
│   └── sqlite/
└── ui/
    ├── package.json
    └── src/

```

The Go HTTP package and browser project are separate toolchain boundaries. They may ship in one executable through `embed` without sharing source directories.

### Repository with a supported Go SDK

Keep supported importable packages at the module root or in ordinary subdirectories. Keep application implementation under `internal`. Consider a separate module only when release cadence, versioning, dependency weight, or audience justifies it. [Organizing a Go module](https://go.dev/doc/modules/layout)

## Package-boundary test

Accept a package only when most answers are clear:

1. What capability or invariant does it own?

2. Who imports it?

3. What may it import?

4. Which changes should remain inside it?

5. Does its name combine cleanly with exported identifiers?

6. Does it avoid import cycles?

7. Is its visibility intentional?

8. Does it own coherent behavior, semantics, invariants, or a stable representation rather than a random category of declarations?

9. Would deleting the package boundary make ownership less clear?

10. Is the package needed now?

11. What design decision does this package hide, and what changes outside it if that decision leaks?

Answer question 11 as two concrete statements: the decision, and the leak consequence. A package that owns a coherent capability can still hide nothing, which is a finding when the package exists to contain a decision and acceptable when transparency is its documented purpose. If its exported identifiers publish the representation, storage format, wire schema, or algorithm the package exists to contain, affected consumers may change when that decision changes. Question 1 answers what is inside the package. Question 11 answers what breaks when the inside changes.

State the leak consequence as concrete consumer churn: name what a schema change, a field rename, or a second implementation would force callers to rewrite. A leak consequence stated only as general coupling risk does not answer the question.

12. Does every exported identifier have a current permitted importer, compatibility requirement, or toolchain requirement?

When creating or materially changing a package boundary, audit every exported identifier (SHOULD). Keep an identifier unexported unless a permitted importer needs it, a compatibility contract requires it, or reflection, code generation, or framework mechanics require access. Exported names inside an `internal` package remain legitimate for permitted importers and create no external support commitment. Preserve an existing supported API during incidental cleanup (MUST).

If the only argument is repository symmetry, reject it.

## Keep import paths short

A normal reader should not follow:

```
handler -> service -> store -> repository -> driver

```

Each package boundary crossed must add a real contract, hide substantial complexity, or change ownership. A package that re-exports a neighbor's types and adds no behavior is a forwarding layer: delete it and let consumers import the owner directly. Preserve a forwarding boundary that carries a public compatibility surface consumers already depend on, or that visibility or dependency constraints require.

Clarifying ownership is not sufficient on its own. A forwarding package can be named for a coherent capability and still publish its neighbor's entire surface. Weigh what the boundary hides against what its exported identifiers add.

In this skill, nesting means import-path length, short means few package hops on a comprehension path, and depth means the Ousterhout sense: a boundary is deep when it hides substantially more complexity than its public surface adds. Depth is the default goal. A shallow package is one whose exported identifiers teach a reader almost everything its implementation does; that is a defect when the package exists to contain complexity, and acceptable when it is a composition root, a compatibility facade, a registration point, or an intentionally transparent adapter.

## Dependency rules

- Keep dependencies acyclic. The [Go specification](https://go.dev/ref/spec#Import_declarations) defines the language rule.

- When an import cycle appears, trace it to the smallest concrete dependency that completes it (MUST). Identify the fields, methods, functions, and values that create the dependency before choosing a remedy.

- Prefer the first ownership-valid remedy in this order (SHOULD):

  1. Move misplaced behavior or state to its actual owner.
  2. Extract a cohesive concept that both packages already need into a lower package they can import.
  3. Move the operation that composes both packages into a higher package.
  4. Define a narrow interface in the consuming package when the consumer needs only behavior from the concrete dependency.
  5. Copy a tiny implementation when sharing it would create a false dependency. Observed independent evolution strengthens this choice; predicted divergence alone does not.
  6. Merge packages whose concepts cannot stand as independent boundaries. A larger combined package strengthens the case for an earlier remedy.

- Every extracted or merged package MUST pass the package-boundary test. A cycle break supplies project-specific evidence for a narrow package, including a single-type package. Predicted growth alone remains insufficient under the active-horizon rule.

- Default (SHOULD): choose the first ownership-valid remedy. Move misplaced behavior first; extract an already-shared concept when it has independent ownership; otherwise move composition upward.

- Fallback (SHOULD): use a consumer-owned interface, copy a tiny implementation, or merge packages only when the earlier remedies fail the ownership and boundary tests.

- Gate (MUST): trace the exact dependency first and record why each earlier remedy contradicts ownership or yields a shallower boundary.

  This ordered remedy is a house review procedure synthesized from practitioner evidence: diagnose the ownership error first, preserve cohesive responsibilities, and use extraction only when it improves the dependency direction. The Go specification remains the source for the acyclic-import rule. Provenance for the synthesized rationale is retained in [practitioner perspectives](practitioner-perspectives.md).

- Make dependency direction visible in package imports and documentation.

- Keep process and transport concerns outside core domain behavior when the separation is real.

- Keep persistence representations local to persistence adapters unless they are the actual canonical domain model.

- Keep configuration decoding separate from validated runtime state when their invariants differ.

- Keep analysis and reporting from mutating execution state unless mutation is part of their responsibility.

- Avoid a central package imported by every other package merely to share declarations.

- Avoid interfaces created solely to satisfy a mocking framework.

## Naming rules

Apply official Go and Uber guidance:

- Use short, lowercase package names.

- Prefer singular, specific names.

- Avoid underscores and mixed capitalization.

- Read names with the package qualifier.

- Avoid stutter such as `http.HTTPServer`.

- Avoid unnecessary import aliases.

- Use `New` when package context makes the constructed type clear.

- Do not abbreviate unless the abbreviation is familiar and unambiguous.

Sources: [Effective Go](https://go.dev/doc/effective_go#names), [Package names](https://go.dev/blog/package-names), [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments), and [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)

## Repository precedent

Use repositories to answer narrow questions:

- [Large-system controls](audited-large-system-controls.md) show specialized multi-module, generated-API, platform, and test constraints. Do not copy Kubernetes or containerd into an ordinary project.

- [Full-stack and multi-binary repositories](audited-full-stack-and-multi-binary.md) show several legitimate executable, frontend, SDK, migration, and generated-code arrangements under explicit product constraints.

- [Focused applications](audited-focused-applications.md) show that root `main.go`, `cmd/<binary>`, public packages, and substantial command packages are all contextual choices.

- [SQL and workflow repositories](audited-sql-and-workflow.md) show that SQL, migrations, persistence interfaces, and workflow terminology follow semantic and operational ownership.

- [Uber repositories](audited-uber-repositories.md) show several valid library shapes, narrow uses of `internal`, purpose-specific modules, and contextual executable placement. They are library and generator precedents, not application templates.

When citing precedent, state the constraint that makes it relevant. Practitioner essays may frame alternatives and failure modes, but they do not outrank official behavior or closely analogous inspected code. See [practitioner perspectives](practitioner-perspectives.md).

## Source assessment

| Source | Authority | Use | Limit |
| --- | --- | --- | --- |
| [Go specification](https://go.dev/ref/spec) | Normative | Language and import-cycle rules | Does not prescribe repository architecture |
| [Organizing a Go module](https://go.dev/doc/modules/layout) | Official current guidance | Modules, commands, `internal`, example layouts | Examples are not mandatory templates |
| [Go command internal directories](https://pkg.go.dev/cmd/go#hdr-Internal_Directories) | Normative tool behavior | Exact `internal` visibility rule | Says nothing about architectural quality |
| [Package names](https://go.dev/blog/package-names) | Official design guidance | Package cohesion and client-facing naming | Published in 2015; some environment context predates modules |
| [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) | Official review guidance | Interfaces, imports, naming, review defaults | Explicitly not comprehensive |
| [Effective Go](https://go.dev/doc/effective_go) | Official but historical | Durable naming and API principles | Written for early Go and not a complete modern guide |
| [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md) | Established industry style | Package names, initialization, exits, goroutines, ordering | Does not prescribe a repository tree |
| [Audited Uber repositories](audited-uber-repositories.md) | Pinned contextual precedent | Library roots, narrow `internal`, interfaces, generators, examples, fixtures, and module isolation | Five library/framework repositories; weak evidence for application layouts |
| [Alex Edwards](https://www.alexedwards.net/blog/11-tips-for-structuring-your-go-projects) | Practitioner | Incremental structure and practical boundaries | Opinion, not policy |
| [Ben Johnson](https://www.gobeyond.dev/standard-package-layout/) | Practitioner | Dependency-oriented packaging and adapters | One architecture; predates modern module practice |
| [Rakyll](https://rakyll.org/style-packages/) | Established practitioner | Responsibility, type locality, caller-facing names, documentation, and examples | Several naming and import-path claims reflect GOPATH-era practice; guidance is explicitly non-normative |
| [Laurent Schwartz](https://laurentsv.com/blog/2024/10/19/no-nonsense-go-package-layout.html) | Practitioner counterweight | Challenges unnecessary `internal`, `cmd`, `pkg`, utility packages, and premature splitting | Useful as an over-structuring check; numerical and categorical claims are opinion, not evidence |
| [golang-standards/project-layout](https://github.com/golang-standards/project-layout) | Community pattern catalog | Vocabulary and examples | Unofficial, disputed, and easy to cargo-cult |
| [Russ Cox critique](https://github.com/golang-standards/project-layout/issues/117) | Go maintainer opinion | Corrects claims of standard status and prevalence | Critique, not a replacement layout standard |
| [Go Proverbs](https://go-proverbs.github.io/) | Rob Pike design heuristics | Simplicity, small interfaces, clear components | Proverbs are not detailed architecture rules |

## Practices to reject

Reject these without project-specific evidence:

- Generating the full `golang-standards/project-layout` tree.

- Treating `pkg` as public API enforcement.

- Treating `internal` as a generic home for all code.

- Treating the official `model` example as endorsement of a models layer.

- Using `model` for every struct.

- Creating `util`, `common`, `shared`, or `helpers` buckets.

- Creating one package per type as a mechanical organizing rule.

- Mirroring Java, Rails, or Clean Architecture directories mechanically.

- Creating interfaces before consumers exist.

- Splitting packages to satisfy arbitrary file-size limits.

- Copying Kubernetes, Grafana, or another large repository without matching its constraints.

- Calling a structure idiomatic solely because several popular repositories use it.

- Citing a proverb as if it were a toolchain rule.

## Decision record template

For each disputed structural choice, record:

```text
Decision:
Project constraint:
Alternatives considered:
Package responsibility:
Allowed dependencies:
Visibility boundary:
Why now:
Deferred trigger:
Evidence class:
Sources:

```

This makes architecture revisitable without reopening the entire Go layout debate.
