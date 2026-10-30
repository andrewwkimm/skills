## Contents

- [Purpose](#purpose)
- [1. Focused library](#1-focused-library)
- [2. CLI application](#2-cli-application)
- [3. Service with one database](#3-service-with-one-database)
- [4. Data pipeline on an orchestration framework](#4-data-pipeline-on-an-orchestration-framework)
- [5. Second provider committed](#5-second-provider-committed)
- [6. Optional dependencies](#6-optional-dependencies)
- [7. Second distribution proposed](#7-second-distribution-proposed)
- [8. Catchall proposed](#8-catchall-proposed)
- [9. Packaging verification](#9-packaging-verification)
- [10. Existing repository, unrelated task](#10-existing-repository-unrelated-task)
- [11. Requested migration](#11-requested-migration)
- [12. Negative trigger](#12-negative-trigger)
- [13. Evidence unavailable](#13-evidence-unavailable)
- [14. Competing valid choices](#14-competing-valid-choices)
- [15. No finding expected](#15-no-finding-expected)
- [16. Module that publishes its representation](#16-module-that-publishes-its-representation)
- [17. Dependency direction with no mechanism](#17-dependency-direction-with-no-mechanism)
- [Evaluation procedure](#evaluation-procedure)

## Purpose

Use these cases to regression-test the skill in any session. They are generalized and contain no company-specific assumptions. A case passes when the response reaches every required conclusion, permits the stated alternatives, avoids every forbidden claim, and names the human-review points instead of deciding them silently.

## 1. Focused library

**Requirements:** One installable library, one public API, no executable, no optional dependencies.

**Required conclusions:** One root import package beside `pyproject.toml` with a top-level `tests/`. Keep modules one level deep. Define a deliberate public API in `__init__.py` and test it. Specify explicit package discovery and installed-artifact verification.

**Forbidden claims:** A subpackage per class; an `_internal` package; a `src` directory.

## 2. CLI application

**Requirements:** One console script, one workflow, no library consumers.

**Required conclusions:** Declare the entry point in `pyproject.toml`. Route the installed script and any `__main__.py` to one callable. Keep argument parsing and output formatting separate from policy.

**Acceptable alternatives:** Omitting `__main__.py` when `python -m` is not supported.

**Forbidden claims:** A `cli/` package is required for one command; business rules belong in the entry point.

## 3. Service with one database

**Requirements:** One deployed service, one Postgres database, migrations, HTTP transport.

**Required conclusions:** Name the persistence and transport modules for what they own. Keep row types with the persistence adapter and payload types with transport. Put migrations where the migration tool expects them, with stated database ownership. Keep policy free of database and framework imports.

**Acceptable alternatives:** One capability module or a capability subpackage, selected by how much behavior each owns.

**Forbidden claims:** A `repositories/` layer is required; every model belongs in `models.py`; a `Protocol` is required before a second implementation exists.

## 4. Data pipeline on an orchestration framework

**Requirements:** Scheduled ingestion for an explicit period, one provider, framework-registered jobs, backfill support, audit records.

**Required conclusions:** Keep framework registration thin and delegate to ordinary orchestration. Make the period input explicit. Keep provider payloads with provider decoding, distinct from canonical domain values. State where the audit record is written and what identifies a run.

**Acceptable alternatives:** One workflow module rather than a workflow subpackage when the workflow is small.

**Forbidden claims:** Framework decorators determine the package tree; a `src` layout is required because the framework scaffold documents one.

## 5. Second provider committed

**Requirements:** A second provider is approved for the active implementation phase, and the two providers report overlapping but not identical metrics.

**Required conclusions:** Give each provider its own named module or subpackage owning its payloads, translation, client, and dependency imports. Require demonstrated shared semantics, including identity, units, periods, corrections, and provenance, before defining a common `Protocol`. Add the boundary with its first working slice.

**Forbidden claims:** Matching field names prove equivalent metrics; a provider package family is justified by one provider.

**Human review:** Canonical semantics when the two providers disagree after restatement.

## 6. Optional dependencies

**Requirements:** Two integrations whose SDKs should not be installed by default.

**Required conclusions:** Use optional dependency groups. Keep each SDK import inside the module that owns the integration. Do not import optional dependencies at package import time.

**Forbidden claims:** Optional dependencies require a separate distribution.

## 7. Second distribution proposed

**Requirements:** A team proposes splitting the repository into two distributions, with no independent release, installation, or dependency difference yet.

**Required conclusions:** Reject the split for now. Name the concrete trigger that would justify it: independent release cadence, dependency isolation, separate installation, distinct deployment, or separate ownership. Keep one distribution and one root import package.

**Acceptable alternatives:** Accept the split when one of those triggers is already true, with per-distribution metadata, explicit dependency direction, and per-artifact verification.

**Forbidden claims:** A monorepo layout copied from a platform-scale project is a general template.

## 8. Catchall proposed

**Requirements:** A change proposes `utils.py` for date parsing, retry logic, and Slack formatting.

**Required conclusions:** Reject the catchall. Move each behavior to the capability that owns it, or give narrowly scoped modules specific names. Distinguish this from a precisely named support module, which is acceptable.

**Forbidden claims:** Any module named `types` or `handlers` is automatically wrong.

## 9. Packaging verification

**Requirements:** CI builds a wheel, installs it, and runs `pytest` from the repository root.

**Required conclusions:** Identify the shadowing defect: the checkout is importable and can satisfy the import instead of the installed package. Require running from a temporary directory outside the checkout and asserting that the resolved package file is inside the isolated environment.

**Forbidden claims:** Installing the wheel is sufficient verification; the flat layout has no import tradeoff.

## 10. Existing repository, unrelated task

**Requirements:** A working repository already uses a `src` layout with generic layer directories. The task is to add one function to an existing module.

**Required conclusions:** Make the change inside the existing structure. Preserve the layout, public imports, and entry points. Report structural observations separately, marked pre-existing and non-blocking.

**Forbidden claims:** The `src` directory must be removed; the layer directories must be reorganized before the function can be added.

**Human review:** Any migration proposal, raised as its own task.

## 11. Requested migration

**Requirements:** Maintainers explicitly ask to move from a layer-based tree to capability packages, and other teams import current module paths.

**Required conclusions:** Inventory public imports, entry points, registrations, discovery configuration, and test assumptions first. Provide ordered slices, compatibility aliases for every import consumers use, verification of built artifacts and import origins after each step, and the condition for removing aliases.

**Forbidden claims:** Consumers can be broken because the new layout is better; the whole tree should move in one commit.

## 12. Negative trigger

**Requirements:** The request is to fix an off-by-one error inside one function, with no question about packages, modules, or directories.

**Required conclusions:** This skill does not apply. Route to code style. Do not produce a tree, a package inventory, or an evidence citation.

**Forbidden claims:** Any layout recommendation.

## 13. Evidence unavailable

**Requirements:** A disputed ownership choice has no closely analogous pinned repository available in the session.

**Required conclusions:** State that repository evidence is unavailable, rely on documented import and packaging behavior, label the rest project judgment, and request human review when ownership, compatibility, or release boundaries are affected.

**Forbidden claims:** A remembered repository structure presented as inspected evidence; an unpinned `master` link offered as evidence.

## 14. Competing valid choices

**Requirements:** A capability could reasonably live as one module or as a subpackage with three modules, and both preserve ownership and dependency direction.

**Required conclusions:** Present both, name the constraint that would select each, recommend one with its reason, and mark the choice unresolved rather than universal.

**Forbidden claims:** One option is objectively correct without a selecting constraint.

## 15. No finding expected

**Requirements:** A repository already satisfies the defaults: flat layout, one root import package, capability modules, representations near their owners, top-level `tests/`, verified wheel.

**Required conclusions:** Report no findings. Do not manufacture symmetry, layers, or speculative boundaries.

**Forbidden claims:** Any directory, protocol, or layer that no stated requirement needs.

## 16. Module that publishes its representation

**Requirements:** A capability module aggregates usage records and returns a `pandas.DataFrame`. Callers filter, group, and sum by column name. Package discovery and installed-artifact verification are correct, imports are directed, and the module has a precise one-sentence responsibility.

**Required conclusions:** Reject the public return type. The module publishes its representation as an incidental consequence of its implementation, not as a documented contract, so a column rename or a change to column semantics breaks consumers coupled to that column. Require a stable, representation-independent contract. Permit the `DataFrame` inside the module as an implementation detail.

**Acceptable alternatives:** Returning a tabular structure from a module whose declared purpose is tabular export or analysis, where the frame schema is the documented contract and is tested as such.

**Forbidden claims:** An added column forces every consumer to change; a `DataFrame` is acceptable because the project is a data pipeline; the layout is acceptable because import direction and packaging verification pass; the return type is a code-style concern outside layout scope.

## 17. Dependency direction with no mechanism

**Requirements:** A repository organized by capability states its intended import direction in documentation. A capability's policy module imports a concrete storage adapter through an intermediate formatting module. Every individual import looks locally reasonable, and review of the changed files raises nothing.

**Required conclusions:** Require an import contract in the repository CI gate: an `acyclic_siblings` contract for cycles and a separate `forbidden` contract for the policy-to-adapter arrow. State that leading underscores and narrow exports communicate intent without enforcing it, and that the indirect chain is the case review does not catch. Seed ignored imports from existing violations as a burndown so adoption does not block on pre-existing debt.

**Acceptable alternatives:** Starting with the acyclic contract plus a single forbidden contract, and deferring capability independence until a second capability exists.

**Forbidden claims:** A review question provides near-equivalent assurance to a mechanical check; a contract check is equivalent to Go's toolchain-enforced `internal`; a `layers` contract is the right starting shape for a capability-organized package; the flat layout is the reason the direction is unenforced; an adapter importing a capability-owned value type is a violation.

## Evaluation procedure

For each case:

1. Ask for a layout recommendation or review using only the stated requirements.

2. Check every required conclusion and forbidden claim.

3. Verify that the greenfield or existing-repository branch was chosen correctly.

4. Verify evidence routing through [evidence.md](evidence.md), including the cheap path for archetype questions.

5. Verify that project judgment is labeled separately from packaging behavior and official guidance.

6. Verify that credible alternatives are not flattened into categorical rules.

7. Verify that no finding is raised on a case that should produce none, and that pre-existing issues are not reported as blockers.

8. Record failures as a missing rule, bad evidence route, overgeneralization, unnecessary migration, or unresolved human decision.

Score each case pass or fail. A case fails if any required conclusion is missing, any forbidden claim appears, or a human-review point is decided silently. Run all cases after editing this directory.
