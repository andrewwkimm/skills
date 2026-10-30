## Contents

- [Purpose](#purpose)
- [1. Single command](#1-single-command)
- [2. Multi-command CLI product](#2-multi-command-cli-product)
- [3. Two production binaries](#3-two-production-binaries)
- [4. Public library with companion command](#4-public-library-with-companion-command)
- [5. Library plus generator](#5-library-plus-generator)
- [6. SQL-backed scheduled service](#6-sql-backed-scheduled-service)
- [7. Focused HTTP service](#7-focused-http-service)
- [8. Go server with embedded frontend](#8-go-server-with-embedded-frontend)
- [9. Integration-heavy ingestion application](#9-integration-heavy-ingestion-application)
- [10. Plugin-oriented server](#10-plugin-oriented-server)
- [11. Existing large repository](#11-existing-large-repository)
- [12. Disputed `model` package](#12-disputed-model-package)
- [13. Ambiguous filename](#13-ambiguous-filename)
- [14. Intentional concrete dependency](#14-intentional-concrete-dependency)
- [15. Package-scoped state](#15-package-scoped-state)
- [16. Existing repository, unrelated task](#16-existing-repository-unrelated-task)
- [17. Requested migration](#17-requested-migration)
- [18. Negative trigger](#18-negative-trigger)
- [19. Evidence unavailable](#19-evidence-unavailable)
- [20. No finding expected](#20-no-finding-expected)
- [21. Handwritten database access, small application](#21-handwritten-database-access-small-application)
- [22. Predominantly dynamic query shapes](#22-predominantly-dynamic-query-shapes)
- [23. sqlc proposed with an unmet prerequisite](#23-sqlc-proposed-with-an-unmet-prerequisite)
- [24. Hybrid transaction](#24-hybrid-transaction)
- [25. Established pgx repository](#25-established-pgx-repository)
- [26. Cohesive package with a transparent interface](#26-cohesive-package-with-a-transparent-interface)
- [27. Forwarding package](#27-forwarding-package)
- [Database case evaluation](#database-case-evaluation)

## Purpose

Use these cases to regression-test the skill in any session. They are generalized and contain no company-specific assumptions. A response passes when it reaches a required conclusion, permits stated alternatives, avoids forbidden claims, and identifies the human-review points.

## 1. Single command

**Requirements:** One private CLI, one executable, no public Go API, no non-Go toolchain.

**Required conclusions:** Compare root `main.go` and `cmd/tool` using repository shape, installation path, root importability, tooling, and command complexity. Prefer the smaller justified boundary. Subcommands do not become separate binaries.

**Forbidden claims:** `cmd` is mandatory; a hypothetical future binary justifies empty command directories.

## 2. Multi-command CLI product

**Requirements:** One shipped executable with many subcommands and substantial command behavior.

**Required conclusions:** Count one binary. Keep one entry point. Put testable command composition in a cohesive package when useful.

**Acceptable alternatives:** Root `main.go` or `cmd/product/main.go`, selected by root importability, tooling, customization, and repository shape.

## 3. Two production binaries

**Requirements:** An API server and worker are independently built, deployed, and operated in the current release.

**Required conclusions:** Separate executable boundaries are justified. `cmd/server` and `cmd/worker` are the conventional starting point, but an existing clear alternative need not be migrated without a concrete benefit. Shared behavior belongs in responsibility-owned packages, not `shared`.

**Forbidden claims:** The two binaries require two modules.

## 4. Public library with companion command

**Requirements:** A supported importable library and one CLI using it.

**Required conclusions:** Keep the public package at the root or in ordinary public subpackages; use a separate executable boundary such as `cmd/tool`; document compatibility.

**Human review:** Decide whether the command API itself is supported for custom binaries.

## 5. Library plus generator

**Requirements:** A runtime library, a released code generator, committed generated output, and deterministic regeneration.

**Required conclusions:** Separate the generator executable from runtime packages; keep the generator's intermediate representation cohesive; verify generated-code freshness in CI.

**Evidence target:** Uber Mock.

## 6. SQL-backed scheduled service

**Requirements:** One scheduled binary reads warehouse billing records for an explicit period, applies versioned rules, reconciles totals, writes summaries, and optionally notifies. Backfill is a subcommand. Retries and deterministic replay are operational requirements. A second provider is approved for the active implementation phase.

**Required conclusions:** One executable unless deployment differs. Trace source-native record through normalization, transformation, reconciliation, publication, and notification. Make the period input, idempotency strategy, transaction boundary, and durable run or audit record explicit. Backfills must be deterministic. Provider interfaces require defined common semantics. SQL follows its owning adapter. Notification failure is distinct from publication failure.

**Acceptable alternatives:** A provider interface may be introduced now because the second implementation is committed, but no empty provider package may exist without its working slice.

**Forbidden claims:** Every side effect needs its own generic interface; `cmd` is mandatory; all provider records are interchangeable costs.

**Human review:** Canonical provider semantics, transaction scope, and the operational identity of a run.

## 7. Focused HTTP service

**Requirements:** One independently deployed Go HTTP service, one production binary, one database, no frontend, no supported public Go SDK, and no plugin protocol.

**Required conclusions:** Start with one module. Choose root `main.go` or `cmd/<binary>` from repository shape rather than executable count alone. Keep routing, middleware, protocol request and response types, and HTTP presentation under clear transport ownership. State whether domain independence from concrete HTTP and database adapters is a project requirement or an architectural choice. Keep persistence rows with the concrete adapter unless they are the canonical domain representation.

**Acceptable alternatives:** `internal/http`, `internal/web`, or a product-specific transport name may be appropriate when its package responsibility is explicit.

**Forbidden claims:** `cmd` is mandatory; every service needs `handlers`, `services`, `repositories`, `controllers`, and `models` packages; HTTP payloads automatically belong in the canonical domain model.

**Human review:** Transaction boundaries and any intentionally supported public Go API.

## 8. Go server with embedded frontend

**Requirements:** One local web application, Go HTTP backend, TypeScript frontend, assets embedded into the binary.

**Required conclusions:** Keep Go HTTP code and frontend toolchain in distinct boundaries. A nested `ui/src` is acceptable. Generated frontend output must have a clear owner and build path.

**Forbidden claims:** Frontend `src` violates Go layout guidance; `web`, `ui`, or `frontend` is universally preferred.

## 9. Integration-heavy ingestion application

**Requirements:** Several external APIs with different pagination, correction, identity, and timestamp semantics feed one canonical domain process.

**Required conclusions:** Keep provider-native records in adapters until canonical semantics are defined. Test one vertical slice. Shared interfaces must preserve differences rather than erase them.

**Human review:** Canonical identity, correction, and time semantics.

## 10. Plugin-oriented server

**Requirements:** Third parties build custom binaries and register implementations through a supported extension contract.

**Required conclusions:** Public command or registration packages may be justified. Compatibility and versioning obligations must be explicit. A `plugins` package is justified only by the real protocol.

**Evidence target:** Caddy, Helm, containerd only when constraints match.

## 11. Existing large repository

**Requirements:** Long-lived monorepo with many binaries, generated public APIs, platform variants, and historical `pkg`, `util`, or layer directories.

**Required conclusions:** Review incrementally. Separate supported APIs from directory names. Do not recommend a wholesale rewrite or copy its layout into greenfield projects. Label legacy constraints.

**Evidence target:** Full-stack evidence and large-system controls.

## 12. Disputed `model` package

**Requirements:** A proposed package contains domain aggregates, HTTP payloads, SQL rows, configuration structs, and generated types.

**Required conclusions:** Reject the mixed package. Permit `model` after one coherent canonical representation, clear semantics or invariants, and legitimate consumers are demonstrated. Behavior is supporting evidence, not a prerequisite.

**Counterexample target:** Uber Mock's cohesive generator model.

## 13. Ambiguous filename

**Requirements:** A review challenges `run.go`, `store.go`, or `query.go` solely because the word is generic.

**Required conclusions:** Inspect the owning package and declarations. Accept the filename when it improves navigation for a real package concept; reject it when it hides unrelated behavior.

**Evidence target:** SQL/workflow and focused-application references.

## 14. Intentional concrete dependency

**Requirements:** A small private service has one database implementation, no substitution requirement, and a cohesive package that owns both domain behavior and its persistence code.

**Required conclusions:** Evaluate whether the concrete dependency obscures ownership or blocks a current requirement. Do not require ports, repository interfaces, or dependency inversion solely to match an architecture diagram.

**Human review:** Revisit the boundary when a second implementation, independent testing seam, public API, or separate ownership need becomes real.

## 15. Package-scoped state

**Requirements:** A package proposes a synchronized process-wide cache with explicit initialization, bounded memory, documented reset behavior, and no supported per-instance variation.

**Required conclusions:** Review ownership, concurrency, lifecycle, observability, and tests. Permit the state when those constraints make package ownership clearer than injected instance state. Reject hidden mutable registries and import-time side effects that obscure behavior.

**Forbidden claims:** All package variables are forbidden; all singleton-like resources are harmless.

## 16. Existing repository, unrelated task

**Requirements:** A working service already uses a layout this skill would not have chosen, such as an executable at an unconventional path and a broad `pkg` tree. The task is to add one handler.

**Required conclusions:** Add the handler within the existing structure. Report structural observations separately from the task, marked pre-existing and non-blocking.

**Forbidden claims:** The repository must be restructured before the handler can be added; the existing executable path is a violation.

**Human review:** Any restructuring proposal, raised as its own task.

## 17. Requested migration

**Requirements:** Maintainers ask to move from one module to two, and external consumers import current public packages.

**Required conclusions:** Inventory public import paths and build targets first. Provide ordered slices, a deprecation path for each broken import, and verification after each step. State the condition for removing compatibility shims.

**Forbidden claims:** Consumers can be broken because the new layout is better.

## 18. Negative trigger

**Requirements:** The request is to fix a nil-pointer dereference inside one function, with no question about packages, modules, or directories.

**Required conclusions:** This skill does not apply. Route to code style. Do not produce a tree, a package inventory, or an evidence citation.

**Forbidden claims:** Any layout recommendation.

## 19. Evidence unavailable

**Requirements:** A disputed ownership choice has no closely analogous pinned repository available in the session.

**Required conclusions:** State that repository evidence is unavailable, rely on toolchain behavior and official guidance, label the remainder project judgment, and request human review if ownership or compatibility is affected.

**Forbidden claims:** A remembered repository structure presented as inspected evidence.

## 20. No finding expected

**Requirements:** A small service already satisfies the defaults: one module, one binary, cohesive packages, narrow `internal`, consumer-defined interfaces, no catchalls.

**Required conclusions:** Report no findings. Do not manufacture improvements, symmetry, or speculative boundaries.

**Forbidden claims:** Any layer, interface, or directory that no stated requirement needs.

## 21. Handwritten database access, small application

**Requirements:** One service, one database, roughly a dozen static queries, handwritten `database/sql`, no prior mapping defects.

**Required conclusions:** No finding. Handwritten `database/sql` is the correct baseline. Confirm the mechanics: error check before deferred close, closure on every early-return path, `Rows.Err()` after iteration, `errors.Is` for `sql.ErrNoRows`.

**Forbidden claims:** sqlc is recommended because the query count is growing; generated code is inherently safer.

## 22. Predominantly dynamic query shapes

**Requirements:** Most reads carry optional predicates, dynamic `IN` lists, and caller-selected ordering. A handful of writes are fully static.

**Required conclusions:** Dynamic shapes weaken the case for broad generation and do not block partial adoption. Permit generating the static writes while keeping dynamic reads handwritten against the same pool. Require the coverage record naming both sets and the boundary reason.

**Forbidden claims:** Dynamic SQL blocks sqlc outright; the dynamic queries should be reshaped into generated combinatorial methods.

## 23. sqlc proposed with an unmet prerequisite

**Requirements:** A team proposes sqlc. The schema is not reproducible as generator input, and no CI step can verify generated-code freshness.

**Required conclusions:** Blocked on prerequisites. Name both failures. Do not weigh them against payoff. State what would unblock adoption.

**Forbidden claims:** Strong payoff offsets a missing prerequisite; the drift check can be added later.

## 24. Hybrid transaction

**Requirements:** One transaction combines generated static writes with one handwritten dynamic query.

**Required conclusions:** All related operations execute through the same transaction-bound connection. A shared `DBTX` parameter, a direct `*sql.Tx`, a generated `Queries.WithTx(tx)` wrapper, or an equivalent transaction-bound wrapper all satisfy this. Identify the defect if any related statement is issued through `*sql.DB`: it takes a different pooled connection and cannot observe uncommitted state. The workflow owns commit and rollback.

**Forbidden claims:** One specific API shape is required; the pool may be used for a related statement because the transaction is short.

## 25. Established pgx repository

**Requirements:** A working service already standardizes on `pgx` for all persistence. The task is to add one query to an existing store.

**Required conclusions:** Add the query using the existing `pgx` runtime. Do not introduce `database/sql` alongside it. Report the runtime difference from this skill default as pre-existing and non-blocking.

**Forbidden claims:** New code must use `database/sql` because the house rule says so; the repository should be migrated before the query is added.

**Human review:** Any runtime migration proposal.

## 26. Cohesive package with a transparent interface

**Requirements:** A package owns daily usage aggregation for one provider. It has one coherent responsibility sentence, no import cycles, an intentional `internal` boundary, and a name that combines cleanly with its exported identifiers. Its exported function returns the provider's decoded response struct.

**Required conclusions:** Reject the boundary as drawn. The package hides nothing it exists to contain: the provider payload shape is published through the return type, so a provider schema change or a field rename breaks consumers coupled to the leaked shape, and the package cannot add a second provider without changing its published contract. Require a canonical domain value as the return type and keep provider decoding inside. Name the hidden decision and the leak consequence explicitly.

**Acceptable alternatives:** Returning the provider struct from a package whose stated purpose is provider decoding, when a separate package owns canonical values and the decoding package's consumers are limited to it.

**Forbidden claims:** A second provider necessarily forces every existing consumer to change; a coherent one-sentence responsibility is sufficient to accept the boundary; the package is acceptable because it passes the other boundary-test questions; a common provider interface should be introduced before shared semantics are demonstrated.

## 27. Forwarding package

**Requirements:** A package sits between an orchestration package and a storage package. It exports the same operations with the same signatures, adds no policy, owns no invariant, and its stated justification is that it clarifies ownership.

**Required conclusions:** Reject the package. Every exported identifier forwards, so the boundary adds an import hop and publishes its neighbor's surface while hiding nothing. Let consumers import the owner directly. Ownership clarification does not by itself justify a boundary that hides no complexity.

**Acceptable alternatives:** Retaining the package when it owns a transaction boundary, a retry policy, a translation the neighbor cannot express, or a public compatibility surface consumers already depend on.

**Forbidden claims:** The boundary is acceptable because the package name describes a coherent capability; deleting it would reduce ownership clarity; forwarding is acceptable because the guide permits abstractions that clarify ownership.

## 28. Mechanical import-cycle break

**Requirements:** `billing` owns `Invoice`. A misplaced `Invoice.RenderReport` method imports `reporting`, while `reporting` imports `billing` to read invoice fields. An agent can make the code compile by adding an interface solely for the cycle, moving declarations into a generic `types` package, or tracing the exact dependency and restoring ownership.

**Required conclusions:** Trace the fields, methods, functions, and values that complete the cycle. Move report rendering to `reporting`, or move composition to a higher package when the workflow owns it. Apply the remedies in order and require every extracted or merged package to pass the package-boundary test. Treat a narrow single-type package as acceptable only when the current cycle demonstrates an independent semantic boundary. Evaluate the size of a copied fragment and the resulting merged package before choosing either fallback.

**Acceptable alternatives:** Extracting an already-shared report input with independent ownership; defining a narrow consumer-owned interface after a concrete behavioral need is clear; copying a tiny implementation when sharing creates a false dependency; merging small packages whose concepts cannot stand independently.

**Forbidden claims:** Any interface is acceptable when it makes the cycle compile; all shared declarations belong in `types`; every single-type package is invalid; predicted growth justifies a package; merge size is irrelevant; future divergence alone justifies copying.

## 29. Exported-identifier audit

**Requirements:** A new `internal` package exports a client, response type, parser, default value, and test seam. Permitted importers need only the client constructor and its fetch method. No compatibility contract, reflection, generator, or framework requires the other exports.

**Required conclusions:** Audit each exported identifier and keep only the identifiers that a permitted importer or toolchain requirement needs. Accept required exports within the `internal` tree because permitted importers still need a package API. Preserve any existing supported API during unrelated cleanup.

**Acceptable alternatives:** Retaining an export required by compatibility, reflection, code generation, or framework mechanics, with that requirement stated.

**Forbidden claims:** Every identifier under `internal` must be unexported; placement under `internal` makes every export justified; an unrelated boundary change may narrow a supported API.

## Database case evaluation

Required conclusions and forbidden claims are mandatory evaluation conditions, not guidance. A case fails if any required conclusion is missing or any forbidden claim appears.
