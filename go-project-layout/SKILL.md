---
name: go-project-layout
description: Designs and reviews Go repository layouts using current official guidance, project constraints, and pinned OSS evidence. Use for Go package boundaries, modules, cmd and main placement, internal and public APIs, interfaces, SQL and migrations, generated code, frontend assets, multiple binaries, plugins, tests, and repository refactoring.
---

Design the most sensible repository structure for the project's current responsibilities and committed near-term needs. Do not apply a stock tree.

Project layout governs module, package, executable, public compatibility, and repository boundaries, including dependency direction across modules, packages, distributions, and executables. Code style governs implementation inside accepted boundaries, including dependency relationships among functions and collaborators. When a recommendation moves code across a package or module, evaluate layout first. This skill governs one repository. Repository-count decisions such as monorepo versus polyrepo are out of scope.

## Rule strength

- **MUST** marks a deterministic house rule. Depart only when a higher-precedence Go, toolchain, compatibility, or repository constraint requires it, and say so.
- **SHOULD** marks a strong default. Depart only for a concrete reason.
- **MAY** marks an acceptable option.
- **MUST NOT** and **SHOULD NOT** carry the same force as MUST and SHOULD, applied to a prohibition.

Enforcement follows section:

- sections whose heading begins with `Required`: MUST.
- `Default decisions`, `Review standard`, and `Practices to reject`: SHOULD unless a statement is explicitly marked otherwise.
- A category MUST resolve to a heading or named list label in this skill; an unresolved category is a defect.
- A statement marked MUST, SHOULD, or MAY carries that strength wherever it appears.
- Examples, rationale, tables, and other explanatory prose are not independently enforceable.

This scheme governs this file and every reference it loads.

## Amendment standard

A proposed change to this skill MUST fall into one of three classes:

1. **Factual error.** A claim about the language, a packaging system, or a documented tool behavior that is false. Fix it and cite the primary source.
2. **Internal contradiction.** Two rules that cannot both be satisfied, or a rule that contradicts its own cited authority. Fix it.
3. **Demonstrated worse outcome.** A concrete scenario in which the current rule produces a worse result. Record the scenario with the change, and add it to an applicable benchmark when one exists.

Strictness is deliberate: these rules instruct an agent, and a granted permission gets used constantly while a denied one surfaces in review. Correctness, public compatibility, repository requirements, and configured tooling already override every house rule. A proposal to weaken a rule still needs one of the three classes above; preference alone is not sufficient.

A **house rule** is a deliberate convention adopted by this skill, not a Go requirement and not a claim that alternatives are wrong.

## Loading

Read [the consensus](references/consensus.md) before making a material layout recommendation.

For a question already answered by the consensus project-shape sections, the consensus alone is sufficient. Read [the evidence index](references/evidence.md) when a choice is disputed, and load only the audited files the index routes you to. Apply its stopping rule instead of researching every filename or directory.

Read `../code-style/references/shared-principles.md` for the depth, extraction, and effect-boundary vocabulary this skill relies on. Package-level depth and hiding findings use the same definitions as the function-level rules there.

Treat this directory together with the `code-style` skill directory as the portable unit. This skill depends on `../code-style/references/shared-principles.md` for the depth, extraction, and effect-boundary vocabulary. Distribute both directories together. Do not add further external references.

## First branch: greenfield or existing

Establish which case applies before recommending anything.

**Greenfield.** Select structure from project constraints using the required method below.

**Existing repository.** Inventory before proposing, in proportion to the decision. A narrow naming question needs only the owning package and its importers. A structural question needs the full inventory below. Record `go.mod` and any `go.work`, every `package main` location, module paths and semantic import version, public importable packages, `internal` boundaries, build and release targets, generators and generated output, build constraints and cgo, and test layout including `testdata` and integration suites. Read the repository tree to depth two, trace package imports to establish the current dependency direction, and trace one vertical slice relevant to the task. Stop once you can answer the disputed ownership question; do not scan every file. Preserve public import paths and build targets. Apply house rules to new and changed code only. Do not propose executable relocation, `internal` restructuring, or a module split as incidental cleanup during unrelated work.

**Requested migration.** Record compatibility requirements, define a deprecation path for every public import path consumers depend on, move one slice at a time, and verify builds and public imports after each step.

## Evidence routing

Load references directly from this file:

- Use [Uber repositories](references/audited-uber-repositories.md) for public libraries, generators, examples, fixtures, narrow `internal` boundaries, and purpose-specific modules.
- Use [focused applications](references/audited-focused-applications.md) for single-product CLIs, servers, executable placement, public application APIs, and contextual filenames.
- Use [SQL and workflow repositories](references/audited-sql-and-workflow.md) for SQL ownership, migrations, persistence boundaries, transactions, and run or execution terminology.
- Use [full-stack and multi-binary repositories](references/audited-full-stack-and-multi-binary.md) for multiple build targets, frontends, public SDKs, generated code, migrations, and long-lived compatibility structure.
- Use [large-system controls](references/audited-large-system-controls.md) only for independently versioned APIs, many production binaries, generated public APIs, plugins, cross-platform implementations, or system-level test infrastructure.
- Use [practitioner perspectives](references/practitioner-perspectives.md) to compare design philosophies, expose trade-offs, or challenge a tentative judgment. Never use practitioner agreement as proof of a Go rule.
- Use [relational database decisions](references/relational-database-decisions.md) for the `database/sql` runtime boundary, the sqlc selection procedure, generated-code ownership, and SQL and migration placement.

- Use [portable benchmarks](references/benchmark.md) when evaluating or changing this skill. Run them after any edit to this directory.

## Required method

1. Identify the project type, current and committed near-term deliverables, executable count, intended public Go API, non-Go components, persistence systems, and deployment model. Separate approved implementation requirements from uncommitted possibilities.

2. Separate toolchain requirements from official guidance, style-guide rules, practitioner opinion, audited repository precedent, and project judgment.

3. Start from a sensible layout that supports current work and committed requirements in the active implementation horizon. Permit an abstraction when it clarifies ownership, dependency direction, reuse, privacy, or an established boundary.

4. Add each directory only when it represents a real package, executable, generated artifact, content boundary, or tool boundary.

5. Give every Go package one sentence that describes what it owns. Reject packages whose only description is "shared code" or "common models."

6. Draft representative client expressions before accepting package names. Prefer `http.Server`-style composition over repeated names.

7. Draw the intended package dependency direction. Reject import cycles and bidirectional conceptual ownership.

8. Keep implementation private with the narrowest useful `internal` boundary when external imports are not supported.

9. Define interfaces at consuming boundaries after a concrete need identifies the required behavior. Return concrete types by default.

10. Distinguish canonical domain state from provider-native records, transport payloads, persistence rows, configuration, and presentation types. Do not centralize every struct.

11. Trace one complete vertical slice from input through transformation, orchestration, side effects, and output. Use that flow to test package ownership and dependency direction.

12. Require shared semantics before introducing a common provider interface. Similar method names do not prove equivalent records, corrections, time periods, units, or provenance.

13. For a disputed choice, define the project concept and selecting constraints first. Prefer evidence matched on product shape, ownership question, deployment model, compatibility surface, and toolchain constraints. Inspect enough pinned analogous implementations and credible alternatives to explain where each analogy fits or fails; do not count repositories as votes. Do not infer quality from a filename or directory alone; read the owning code.

14. Explain conditional choices such as `cmd`, `model`, `pkg`, `app`, `engine`, `storage`, `web`, `ui`, and `src` instead of declaring them universally good or bad.

15. Classify each material recommendation as Go-enforced, official guidance, style rule, corroborated precedent, contextual precedent, project judgment, or unresolved.

16. State what should not be created yet and the concrete trigger that would justify it later. Request human review when unresolved alternatives materially change conceptual ownership, public compatibility, deployment, or data semantics.

## Default decisions

Apply these defaults unless project constraints justify another choice:

- Start with one module when the repository has one release, dependency, and compatibility unit. Add a module only for an independently versioned or dependency-isolated unit with a demonstrated owner and workflow.

- Keep a simple library at the module root. For one executable, compare root `main.go` with `cmd/<binary>` using root importability, customization, repository tooling, command complexity, and composition needs. Executable count alone does not settle the choice.

- For multiple current or committed near-term production binaries, start by evaluating `cmd/<binary>`. Preserve another clear existing executable layout when migration would not improve ownership, builds, or navigation. Subcommands of one executable do not count as separate binaries.

- Use `internal` when the intended importer scope should be enforced by the Go toolchain. Do not use it merely as an application-code category.

- Do not create `pkg` unless the repository deliberately supports importable Go packages and the name improves navigation.

- Do not create `model` merely to collect structs. Permit it when it owns one cohesive representation with clear semantics or invariants and legitimate consumers. Behavior strengthens the boundary but is not required.

- Do not create `util`, `common`, `shared`, `misc`, `types`, or `interfaces` catchalls. This is stricter than the Python layout skill, which permits a precisely scoped `types` or `interfaces` package: Go resolves the same need through consumer-defined interfaces and concrete return types, so a dedicated package adds a dependency hop without hiding a decision.

- Keep process termination in `main`. Prefer a small `main` focused on process concerns and composition when that improves testing or readability. For a small command, understandable orchestration may remain in `main`; an optional same-package `run` function can isolate arguments, streams, environment, and returned errors.

- Treat mutable package-scoped state as a design review point, not a blanket prohibition. Require explicit ownership, synchronization, lifecycle, reset behavior, and a reason that dependency injection or instance state is worse.

- Keep frontend source in its own toolchain directory such as `ui/src`; do not add a repository-level `src` for Go code.

- Name concrete adapters by what they implement or the technology they use, such as `sqlite`, when that is clearer than a premature generic layer.

- Use `internal/http`, `internal/web`, or another specific transport package only when it owns real routes, handlers, middleware, protocol payloads, or presentation behavior. Keep transport payloads distinct from canonical domain state unless they are intentionally the same representation.

- A committed near-term requirement may justify a boundary before every implementation is complete. Do not create empty placeholder packages: add the boundary with its first consumer, implementation, or working vertical slice in the same implementation phase.

- Keep provider-specific records in provider adapters until a validated canonical representation exists.

- Keep historical, scenario, schema, migration, fixture, and generated content outside Go package taxonomies when they are not Go packages.

## Required output for layout recommendations

Provide:

1. **Decision**: the recommended structure and the project assumptions behind it.

2. **Tree**: only directories justified now, each with a brief responsibility comment.

3. **Package responsibilities**: one sentence per package.

4. **Dependency direction**: a compact graph or ordered list.

5. **Contested names**: explain decisions on names such as `model`, `pkg`, `app`, or `engine` when relevant.

6. **Deferred structure**: folders or abstractions to add only after named triggers occur.

7. **Evidence basis**: cite the minimum authoritative sources needed for disputed claims.

For an existing repository, also provide:

8. **Preserved surfaces**: public import paths, build targets, and generated or embedded artifacts that must keep working.

9. **Migration steps**: ordered slices, deprecation paths, and verification after each step. Include this only when migration is requested or recommended. A greenfield design or a narrow review has none.

Do not cite a large repository as proof of universal convention. Use it only as context-specific precedent.

## Review standard

Findings marked MUST are rejections. Findings marked SHOULD require a stated reason to proceed. Report each finding with a severity of blocker, major, moderate, or minor, and state whether the change introduces it or it is pre-existing. Do not raise a pre-existing structural issue as a blocker on an unrelated change.

Reject or revise a layout when any of these are true:

- A recommendation restructures an existing repository, or breaks one of its public import paths or build targets, without a requested and justified migration (MUST).

- A directory exists only because a template contained it.

- A package name does not describe a coherent responsibility.

- An import cycle or bidirectional conceptual ownership exists (MUST). Apply the diagnosis and remedy order in [Consensus](references/consensus.md#dependency-rules) before proposing a boundary change.

- A package combines unrelated domain, HTTP, database, and configuration types.

- An interface is colocated with its implementation only by habit.

- `internal` is used without understanding its parent-subtree import rule.

- `pkg` is claimed to make code public or stable.

- `cmd` subdirectories are created for subcommands rather than separate binaries.

- Historical repository precedent is presented as current Go policy.

- A large-project structure is copied without the large project's constraints.

- The proposal creates empty speculative packages.

- A common interface erases provider-specific units, corrections, periods, identity, or provenance.

- A boundary is justified only by an uncommitted future possibility.

- A repository example is cited without a pinned revision, inspected code, analogous constraint, or stated limitation.

- A material naming or ownership choice has two credible answers but is presented as settled without human review.

- A package's exported identifiers publish the representation, storage format, wire schema, or algorithm the package exists to contain.

- A proposed package boundary crosses forwarding packages that add no contract, hidden complexity, or ownership change.

- A domain-to-adapter import contradicts the proposed ownership direction or blocks substitution, testing, or reuse that the project actually requires. Do not introduce dependency inversion solely to satisfy an architectural pattern.

Use direct, evidence-based prose. State conclusions first. Avoid ceremony, folklore, and categorical claims unsupported by Go semantics or current official guidance.
