## Contents

- [Purpose](#purpose)
- [Audit set](#audit-set)
- [Corroborated findings](#corroborated-findings)
- [Focused findings](#focused-findings)
- [Specialized findings](#specialized-findings)
- [What this category does not establish](#what-this-category-does-not-establish)
- [Required use in future recommendations](#required-use-in-future-recommendations)

## Purpose

This reference records pinned evidence from selected Uber Go repositories. It supports narrow layout and naming decisions. It does not turn Uber repository history into universal Go policy.

## Audit set

|Repository|Audited revision|Date|Product shape|Corpus role|
|---|---|---|---|---|
|[uber-go/zap](https://github.com/uber-go/zap/tree/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f)|[`5b81b37`](https://github.com/uber-go/zap/commit/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f)|2026-04-28|Public logging library with focused companion packages and purpose-specific modules|Focused precedent|
|[uber-go/goleak](https://github.com/uber-go/goleak/tree/5f791e3ef83b35d32b262466250507c2f20fea3c)|[`5f791e3`](https://github.com/uber-go/goleak/commit/5f791e3ef83b35d32b262466250507c2f20fea3c)|2026-06-02|Small public library with one narrow internal package|Focused precedent|
|[uber-go/mock](https://github.com/uber-go/mock/tree/349aac660616b1492317714bff32347e90563340)|[`349aac6`](https://github.com/uber-go/mock/commit/349aac660616b1492317714bff32347e90563340)|2025-12-17|Public runtime library plus released generator, tooling, generated fixtures, and several isolation modules|Focused precedent|
|[uber-go/fx](https://github.com/uber-go/fx/tree/d5da5b04ac906bfbad8b400baeee9b970c1be6f3)|[`d5da5b0`](https://github.com/uber-go/fx/commit/d5da5b04ac906bfbad8b400baeee9b970c1be6f3)|2025-12-27|Public dependency-injection framework with docs, E2E, and tools modules|Focused precedent; framework patterns are specialized|
|[uber-go/dig](https://github.com/uber-go/dig/tree/770912487056bfe8bc9bd5879a4e049f68989ab0)|[`7709124`](https://github.com/uber-go/dig/commit/770912487056bfe8bc9bd5879a4e049f68989ab0)|2025-05-13|Compact public dependency-injection library|Focused precedent; reflection patterns are specialized|

## Corroborated findings

These findings recur across enough of this category to serve as corroborated library precedent. They remain subordinate to official guidance and do not automatically apply to applications.

### A public library may live at the module root

`zap`, `goleak`, `fx`, and `dig` expose their main supported package directly from the module root. None creates `cmd` or `pkg` merely for symmetry.

Examples: [zap `logger.go`](https://github.com/uber-go/zap/blob/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f/logger.go), [goleak `doc.go`](https://github.com/uber-go/goleak/blob/5f791e3ef83b35d32b262466250507c2f20fea3c/doc.go), [Fx `app.go`](https://github.com/uber-go/fx/blob/d5da5b04ac906bfbad8b400baeee9b970c1be6f3/app.go), and [Dig `container.go`](https://github.com/uber-go/dig/blob/770912487056bfe8bc9bd5879a4e049f68989ab0/container.go).

Use this as evidence for public libraries, not scheduled jobs or servers.

### `internal` should express the narrowest useful boundary

The repositories use root and nested `internal` directories for cohesive helpers, algorithms, test support, and integration fixtures. `mock` is especially useful because it has narrow nested internal trees rather than a mandatory root-level `internal`: [gomock internal mock](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/gomock/internal/mock_gomock/mock_matcher.go) and [mockgen internal tests](https://github.com/uber-go/mock/tree/349aac660616b1492317714bff32347e90563340/mockgen/internal/tests).

This corroborates the rule that `internal` is a visibility mechanism whose placement must match the intended importer subtree.

### File names should expose concepts or operations within a cohesive package

Observed names include `logger.go`, `sink.go`, `provide.go`, `invoke.go`, `controller.go`, `matchers.go`, `leaks.go`, and `options.go`. These names are not universally good in isolation. They work because the package supplies the missing context.

Examples: [zap `sink.go`](https://github.com/uber-go/zap/blob/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f/sink.go), [Fx `provide.go`](https://github.com/uber-go/fx/blob/d5da5b04ac906bfbad8b400baeee9b970c1be6f3/provide.go), [mock `controller.go`](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/gomock/controller.go), and [goleak `leaks.go`](https://github.com/uber-go/goleak/blob/5f791e3ef83b35d32b262466250507c2f20fea3c/leaks.go).

Do not blacklist `run.go`, `store.go`, `query.go`, or similar names by filename alone. Inspect the owning package and file contents.

### Interfaces follow semantic ownership, not one mechanical placement rule

The category supports consumer-owned interfaces as the default, while showing legitimate exceptions:

- `goleak.TestingT` and `TestingM` sit beside their consumers in [`testmain.go`](https://github.com/uber-go/goleak/blob/5f791e3ef83b35d32b262466250507c2f20fea3c/testmain.go).

- `fxtest.TB` sits in the consuming test package in [`fxtest/tb.go`](https://github.com/uber-go/fx/blob/d5da5b04ac906bfbad8b400baeee9b970c1be6f3/fxtest/tb.go).

- Dig's graph algorithm owns the small input contract it consumes in [`internal/graph/graph.go`](https://github.com/uber-go/dig/blob/770912487056bfe8bc9bd5879a4e049f68989ab0/internal/graph/graph.go).

- Zap's public extension interfaces live with the abstraction and concrete implementations in [`zapcore/core.go`](https://github.com/uber-go/zap/blob/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f/zapcore/core.go).

The durable rule is to place an interface where its semantics and compatibility obligation are owned. Consumer placement remains the default, not an absolute law.

### Extra modules need a concrete isolation reason

The repositories use nested modules to isolate benchmark competitors, experimental APIs, docs, E2E programs, developer tools, Bazel support, or integration fixtures.

Examples: [zap benchmarks](https://github.com/uber-go/zap/blob/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f/benchmarks/go.mod), [Fx docs](https://github.com/uber-go/fx/blob/d5da5b04ac906bfbad8b400baeee9b970c1be6f3/docs/go.mod), and [mock tools](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/tools/go.mod).

Do not infer that a large repository needs multiple modules. Record the dependency, release, toolchain, or fixture-isolation reason.

### Examples and fixtures need not share one directory convention

The repositories use executable `Example...` tests, `sample`, `docs/ex`, `internal/tests`, and `testdata` according to purpose.

Examples: [zap executable examples](https://github.com/uber-go/zap/blob/5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f/example_test.go), [mock sample](https://github.com/uber-go/mock/tree/349aac660616b1492317714bff32347e90563340/sample), [Fx tutorial program](https://github.com/uber-go/fx/blob/d5da5b04ac906bfbad8b400baeee9b970c1be6f3/docs/ex/get-started/01-minimal/main.go), and [Dig golden fixtures](https://github.com/uber-go/dig/tree/770912487056bfe8bc9bd5879a4e049f68989ab0/testdata).

Choose placement from audience and build behavior: godoc example, standalone sample, documentation program, parser fixture, integration case, or golden output.

## Focused findings

### A `model` package can be cohesive

`mockgen/model` owns the generator's intermediate representation and associated behavior: packages, interfaces, methods, parameters, and types. See [`mockgen/model/model.go`](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/mockgen/model/model.go).

This is evidence against a categorical ban on `model`. It is not evidence for collecting every application struct in one package. The package is justified by one coherent representation consumed by the generator.

### `cmd` is not the only legitimate executable placement

The released `mockgen` executable lives at `mockgen/`, while a maintenance tool lives at [`tools/cmd/extract-changelog`](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/tools/cmd/extract-changelog/main.go). The released path carries compatibility history; the maintenance tool follows a local tools-module convention.

Use this as a counterexample to categorical `cmd` rules. For greenfield applications, current official module guidance and actual executable count remain stronger evidence.

### Generated code can be committed when regeneration is controlled

`mock` commits generated mocks with generated-file markers and checks regeneration drift in [`ci/test.sh`](https://github.com/uber-go/mock/blob/349aac660616b1492317714bff32347e90563340/ci/test.sh).

The general lesson is not "commit generated code." It is: decide whether consumers need generated artifacts, make ownership explicit, provide deterministic regeneration, and verify freshness in CI.

## Specialized findings

- Fx and Dig expose option interfaces, marker types, lifecycle wrappers, graph algorithms, and reflection helpers because they are dependency-injection frameworks. Do not transfer those patterns to ordinary applications without matching constraints.

- Zap's `zapcore` split and multiple isolation modules reflect a performance-sensitive public logging API, benchmarks against competitors, experimental integrations, and compatibility commitments.

- Mock's fixture density, generated names, Bazel module, and generator IR reflect source-generation requirements.

- Exported names inside an `internal` package are legitimate when needed by permitted importers; they do not create an external support commitment. See [`stack.Stack`](https://github.com/uber-go/goleak/blob/5f791e3ef83b35d32b262466250507c2f20fea3c/internal/stack/stacks.go).

## What this category does not establish

These repositories provide weak evidence for:

- Single-binary services

- Scheduled batch applications

- SQL-backed applications

- HTTP servers with embedded frontends

- Multiple production executables

- Database migrations and transactional persistence

- Deployment manifests and operational topology

Do not use this category to settle those questions. Audit matching application repositories first.

## Required use in future recommendations

When this category is relevant:

1. Cite a pinned file, not an unpinned repository homepage.

2. State whether the example is corroborated, focused, or specialized.

3. Explain the matching project constraint.

4. Include a credible counterexample when the choice is disputed.

5. Do not claim that Uber's style guide mandates a layout seen in an Uber repository.
