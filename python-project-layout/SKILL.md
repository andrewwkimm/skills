---
name: python-project-layout
description: Designs and reviews Python repository layouts using Python packaging mechanics, project constraints, locality, dependency direction, and audited OSS evidence. Use for flat package layouts, package and module boundaries, public APIs, entry points, tests, adapters, configuration, SQL and migrations, generated files, notebooks, optional dependencies, multiple distributions, and repository refactoring.
---

Design the most sensible flat repository structure for the project's current responsibilities and committed near-term needs. Do not apply a stock tree.

Project layout governs distribution, package, module, executable, public compatibility, and repository boundaries, including dependency direction across modules, packages, distributions, and executables. Code style governs implementation inside accepted boundaries, including dependency relationships among functions and collaborators. When a recommendation moves code across a module or package, evaluate layout first. This skill governs one repository. Repository-count decisions such as monorepo versus polyrepo are out of scope.

## Rule strength

- **MUST** marks a deterministic house rule. Depart only when a higher-precedence correctness, compatibility, repository, or packaging constraint requires it, and say so.
- **SHOULD** marks a strong default. Depart only for a concrete reason.
- **MAY** marks an acceptable option.
- **MUST NOT** and **SHOULD NOT** carry the same force as MUST and SHOULD, applied to a prohibition.

Enforcement follows section:

- sections whose heading begins with `Required`, plus `Flat layout house rule`: MUST.
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

A **house rule** is a deliberate convention adopted by this skill, not a language requirement and not a claim that alternatives are wrong.

## Flat layout house rule

New Python repositories MUST use a flat layout and MUST NOT add a top-level `src` directory. Existing repositories MUST keep their current layout unless migration is explicitly requested and justified.

This convention selects flat layout for locality and consistency. It does not claim flat layout is universally superior: maintained packaging guidance presents flat and `src` layouts as alternatives with different tradeoffs. Because a flat checkout is directly importable, the compensating controls in the consensus are mandatory, not optional.

The rule applies to the Python project. A nested toolchain such as a frontend MAY use its own `src` directory.

## Loading

Read [the consensus](references/consensus.md) before making a material layout recommendation.

For a question already answered by the consensus "Project archetypes" section, the consensus alone is sufficient. Read [the evidence index](references/evidence.md) when a choice is disputed, and load [the audited repositories](references/audited-repositories.md) only when the index routes the decision there.

Use [the benchmark](references/benchmark.md) when evaluating or changing this skill. Run it after any edit to this directory.

Read `../code-style/references/shared-principles.md` for the depth, extraction, and effect-boundary vocabulary this skill relies on. Package-level depth and hiding findings use the same definitions as the function-level rules there.

Treat this directory together with the `code-style` skill directory as the portable unit. This skill depends on `../code-style/references/shared-principles.md` for the depth, extraction, and effect-boundary vocabulary. Distribute both directories together. Do not add further external references.

## First branch: greenfield or existing

Establish which case applies before recommending anything.

**Greenfield.** Select structure from project constraints using the required method below.

**Existing repository.** Inventory before proposing, in proportion to the decision. A narrow naming question needs only the owning module and its importers. A structural question needs the full inventory below. Record the current distributions, root import packages, layout style, public imports, executable and framework entry points, plugin or entry-point registrations, package-discovery configuration, test paths and import assumptions, and known downstream consumers. Preserve those surfaces. Apply house rules to new and changed code only. Do not propose a layout migration, a `src` removal, or a package move as incidental cleanup during unrelated work.

**Requested migration.** Record the compatibility requirements. Define aliases or a deprecation path for every import consumers depend on. Move one vertical slice at a time when the change is large. Inspect the built artifact and verify import origins after each step. Remove compatibility paths only after consumers migrate.

## Required method

1. Identify the project type, current and committed deliverables, import package count, executable and framework entry points, intended public API, persistence systems, optional integrations, non-Python components, deployment model, and release model.

2. Separate Python and packaging behavior from official guidance, repository precedent, and project judgment.

3. For a greenfield, single-distribution repository, start with one root import package beside `pyproject.toml`. For an existing repository, start from its current root packages. For a justified multi-distribution repository, apply this per distribution. Add modules and subpackages only when they clarify a real responsibility, ownership boundary, dependency boundary, public API, optional dependency, deployment unit, or substantial subsystem.

4. For a new repository, use a flat layout and compensate for its import behavior with explicit package discovery, wheel inspection, and tests run against the installed artifact from outside the checkout. For an existing repository, preserve the current layout.

5. Give every package and module one sentence that states what it owns. Reject descriptions such as "shared code," "common models," "business services," or "helpers."

6. Trace the shortest comprehension path for one important workflow. A reader should move from its entry point to the directly called policy and effect boundaries without crossing forwarding layers.

7. Trace one complete vertical slice from input through translation, policy, orchestration, side effects, and output. Use it to test ownership and dependency direction.

8. Keep meaningful deterministic policy separate from effects. Prefer module-level functions. Do not create packages or classes only to satisfy an architectural pattern.

9. Distinguish domain values from provider payloads, transport schemas, persistence records, configuration input, runtime configuration, audit records, and presentation types. Keep each representation near its owner.

10. Draw the intended import direction. Reject import cycles, bidirectional ownership, and central modules imported by unrelated capabilities.

11. Evaluate a module split by locality, semantic cohesion, callers, dependency differences, stability, and comprehension cost. Do not split by file length or one-class-per-file habits.

12. Evaluate a package split only after a module boundary is insufficient. A directory adds an import path and navigation step, so it must own a coherent cluster rather than provide visual grouping.

13. For disputed choices, inspect Python mechanics and closely analogous pinned repositories. Explain where each analogy fits and fails. Do not count repositories as votes.

14. State what should not be created yet and the concrete trigger that would justify it later.

15. Request human review when alternatives materially change public compatibility, conceptual ownership, release boundaries, deployment, or data semantics.

## Default decisions

Apply these defaults unless project constraints justify another choice:

- Use one distribution and one root import package when the repository has one release, dependency, ownership, and deployment unit.

- Do not add a top-level `src` directory to a new repository. Do not remove one from an existing repository without a requested migration.

- Keep production Python inside the root import package. Do not place loose production modules beside `pyproject.toml`.

- Keep the import package and distribution names recognizably aligned. A hyphenated distribution may map to an underscored import package.

- Organize around product or domain capabilities, not generic technical layers.

- Reject vague catchalls named `utils`, `common`, `helpers`, `shared`, or `misc`. The defect in `services`, `managers`, `processors`, `handlers`, `types`, `interfaces`, and `models` is mixed ownership rather than the filename: reject them when they collect unrelated declarations, and permit one when its responsibility is precise and the name reads clearly at the import site.

- Permit a narrowly named support module only when its responsibility is specific, such as `json_encoding`, `retry_policy`, `path_validation`, or `slack_formatting`.

- Keep package nesting shallow. Prefer `package.module`. Add `package.capability.module` when the capability owns several cohesive modules. Treat deeper paths as a review trigger.

- Keep related policy, orchestration, value types, and narrow private helpers in the same module when that gives the clearest top-to-bottom reading path.

- Keep concrete effect adapters near the capability they serve or in a specifically named adapter module. Do not create a universal repository, client, or service layer.

- Define `Protocol` types at consuming boundaries after a real consumer identifies the required behavior. Do not create a central interfaces package. A precisely scoped `types` or `interfaces` module is permitted here under the mixed-ownership test above; the Go layout skill bans both names outright.

- Keep `__init__.py` small. Use it to define an intentional public API, not to execute application work or mirror every internal name.

- Keep `__main__.py` and installed script targets thin. They should parse process inputs, construct dependencies, invoke orchestration, and translate the final result into process behavior.

- A repository with one distribution SHOULD use one top-level `tests` directory. Independently built distributions MAY own separate suites when their installation, dependencies, release process, or runtime contracts differ. Organize tests by capability or observable behavior. Do not mirror the production tree mechanically.

- Keep test support local until several tests share the same stable concept. Avoid `tests/helpers.py` and equivalent catchalls.

- Keep SQL, migrations, templates, policy data, generated files, fixtures, and notebooks in boundaries that state their owner and execution model. Do not force non-Python artifacts into the Python package taxonomy.

- When dependency restrictions are stable, consequential, and reliably checkable, declare an import contract covering cycles and prohibited policy-to-adapter dependencies, and run it in the repository CI gate. Permit orchestration imports of concrete adapters, and adapter imports of capability-owned value types and consuming protocols. For existing violations, use ignored imports only as an explicit burndown.

- Use namespace packages only when independently distributed portions must share an import namespace.

- Create another distribution only when release cadence, dependency isolation, ownership, public compatibility, deployment, or installation requirements are independently meaningful.

- A committed near-term requirement may justify a boundary before every implementation is complete. Add the boundary with its first working vertical slice. Do not create empty placeholder packages.

## Required output

Provide:

1. **Decision**: the recommended structure and selecting project constraints.
2. **Tree**: only directories and representative files justified now, each with a short responsibility comment.
3. **Responsibilities**: one sentence for every package and material module.
4. **Dependency direction**: a compact graph or ordered list.
5. **Comprehension path**: the files a reader follows for one important workflow.
6. **Public and executable surfaces**: supported imports, script targets, `__main__`, framework registrations, or jobs.
7. **Contested names**: explain decisions involving `models`, `services`, `core`, `app`, `domain`, `adapters`, or similar broad names.
8. **Deferred structure**: abstractions or directories to add only after named triggers.
9. **Packaging verification**: package discovery, built-wheel inspection, and the installed-artifact test strategy including its out-of-checkout execution and import-origin assertion.
10. **Evidence basis**: cite the minimum authoritative sources needed for disputed claims.

For an existing repository, also provide:

11. **Preserved surfaces**: public imports, script targets, framework registrations, and test paths that must keep working.
12. **Migration steps**: ordered slices, compatibility aliases, verification after each step, and the condition for removing compatibility paths. Include this only when migration is requested or recommended. A greenfield design or a narrow review has none.

## Review standard

Findings marked MUST are rejections. Findings marked SHOULD require a stated reason to proceed. Report each finding with a severity of blocker, major, moderate, or minor, and state whether the change introduces it or it is pre-existing. Do not raise a pre-existing structural issue as a blocker on an unrelated change.

Reject or revise a layout when any of these are true:

- A new repository adds a top-level `src` directory (MUST).
- A recommendation restructures an existing repository, or removes its `src` layout, without a requested and justified migration (MUST).
- A directory exists only because a template or framework generated it.
- A package or module lacks a coherent one-sentence responsibility.
- A common workflow crosses forwarding modules that add no policy, ownership, or depth.
- The tree mirrors generic layers such as controllers, services, repositories, and models across every capability.
- A catchall accumulates unrelated declarations.
- A module contains unrelated domain, transport, persistence, and configuration concepts.
- A subpackage exists only to reduce file length or create symmetry.
- A class or package exists only to namespace functions or support mocking.
- Provider payloads, persistence rows, configuration, and canonical domain values are centralized as one model layer.
- An import cycle or bidirectional ownership exists (MUST).
- `__init__.py` performs application work or exposes internals accidentally.
- A flat layout is accepted without explicit package discovery and installed-artifact verification.
- Tests import the checkout successfully but the built wheel is not checked.
- A namespace package, plugin system, or second distribution is justified only by hypothetical growth.
- A large repository is copied without matching its release, compatibility, deployment, or ownership constraints.
- Two credible ownership choices remain but the recommendation presents one as universal.
- An existing public import, script target, or framework registration is dropped without a compatibility path (MUST).
- A package or module accidentally publishes an implementation representation through return types or exported names, causing consumers to depend on a representation that is not its documented public contract.
- A repository example is cited without a pinned revision, inspected code, analogous constraint, or stated limitation.

Use direct prose. State conclusions first. Avoid ceremony, folklore, and claims unsupported by Python mechanics or inspected evidence.
