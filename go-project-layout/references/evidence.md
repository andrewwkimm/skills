## Purpose

Use this index to load only the evidence relevant to the current decision. Read [consensus.md](consensus.md) first. Do not search every repository for every review.

A question already answered by the consensus project-shape sections needs no further evidence. Use this index when a choice is disputed.

Audited revisions are pinned in each audited file. Re-audit before citing a newer revision, and record the revision with each claim.

## Decision routing

|Question|Primary evidence|Counterevidence or caution|
|---|---|---|
|Root `main.go` or `cmd/<binary>`|[Focused applications](audited-focused-applications.md)|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md)|
|Several production binaries|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md)|[Large-system controls](audited-large-system-controls.md) only for exceptional scale|
|Public library root and companion packages|[Uber repositories](audited-uber-repositories.md)|[Focused applications](audited-focused-applications.md) for applications with public APIs|
|`internal` placement|[Consensus](consensus.md)|[Uber repositories](audited-uber-repositories.md) for nested boundaries; [large-system controls](audited-large-system-controls.md) for exceptional cross-module restrictions|
|`pkg`|[Consensus](consensus.md)|[Helm in full-stack evidence](audited-full-stack-and-multi-binary.md); [large-system controls](audited-large-system-controls.md) as cautions|
|`model`|[Consensus](consensus.md)|[Uber Mock](audited-uber-repositories.md); application examples are contextual, not a general layer|
|Interfaces|[Consensus](consensus.md)|[Uber repositories](audited-uber-repositories.md), [focused applications](audited-focused-applications.md), and [SQL/workflow](audited-sql-and-workflow.md)|
|`run.go`, `store.go`, `query.go`, `execution.go`|[SQL and workflow](audited-sql-and-workflow.md)|[Focused applications](audited-focused-applications.md) for package-context counterexamples|
|SQL file placement|[SQL and workflow](audited-sql-and-workflow.md)|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md) for migration alternatives|
|Migrations|[SQL and workflow](audited-sql-and-workflow.md)|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md) for Go-authored and embedded alternatives|
|Generated code|[Uber repositories](audited-uber-repositories.md)|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md); [large-system controls](audited-large-system-controls.md) only for public generated APIs|
|HTTP service and transport ownership|[Consensus](consensus.md)|[Focused applications](audited-focused-applications.md) and [full-stack and multi-binary](audited-full-stack-and-multi-binary.md) as contextual application precedent|
|Frontend source and embedded assets|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md)|[Consensus](consensus.md) for nested `src` guidance|
|Multiple modules|[Uber repositories](audited-uber-repositories.md) for dependency isolation|[Large-system controls](audited-large-system-controls.md) for independent API publication|
|Plugins or custom binaries|[Caddy](audited-focused-applications.md) and [Helm](audited-full-stack-and-multi-binary.md)|[Kubernetes and containerd](audited-large-system-controls.md) only for established extension protocols|
|Tools, generators, and fixtures|[Uber repositories](audited-uber-repositories.md)|[Focused applications](audited-focused-applications.md) and [large-system controls](audited-large-system-controls.md)|
|Existing large monorepo review|[Full-stack and multi-binary](audited-full-stack-and-multi-binary.md)|[Large-system controls](audited-large-system-controls.md)|
|Relational runtime, sqlc selection, generated query ownership|[Relational database decisions](relational-database-decisions.md)|Project size and query count alone do not justify generation|
|Existing-repository review or migration|[Consensus](consensus.md) preservation rules and current official module behavior|Greenfield precedent does not justify relocating an established executable or public package|
|Package cohesion, discoverability, and caller-facing naming|[Consensus](consensus.md) and current official naming guidance|[Practitioner perspectives](practitioner-perspectives.md), especially Rakyll and Cheney, for review heuristics|
|Over-structuring, `internal`, `pkg`, or premature package splitting|Current official module behavior and [Consensus](consensus.md)|[Practitioner perspectives](practitioner-perspectives.md), especially Laurent, as an adversarial check|
|Process entry point and optional `run` seam|[Consensus](consensus.md)|[Practitioner perspectives](practitioner-perspectives.md), especially Mat Ryer; focused applications remain repository precedent|
|Mutable package-scoped state|Project requirements and package ownership|[Practitioner perspectives](practitioner-perspectives.md), especially Cheney; inspect real concurrency and lifecycle constraints|
|Import-cycle diagnosis and remediation|The Go specification for the prohibition and [Consensus](consensus.md) for the house procedure|[Practitioner perspectives](practitioner-perspectives.md) for provenance and alternative heuristics; ownership and the package-boundary test select the remedy|
|Export surface at a package boundary|[Consensus](consensus.md) and existing compatibility contracts|[Uber repositories](audited-uber-repositories.md) for `internal` exports|
|Persistent dependency diagrams|[Consensus](consensus.md) for the required compact graph or ordered list|[Practitioner perspectives](practitioner-perspectives.md) for meaningful spatial order; entity-count ranges remain practitioner judgment|

## Evidence sufficiency

Stop researching a disputed choice when all of these are available:

1. Applicable Go-enforced behavior or current official guidance has been checked.

2. The strongest available examples match the relevant product shape, ownership question, deployment model, compatibility surface, and toolchain constraints. One close analogue may outweigh several famous but weak analogues.

3. A credible pinned counterexample or alternative has been inspected when the choice is disputed. Repository counts are not votes.

4. The project constraint that selects among the alternatives is explicit.

5. No unresolved choice changes conceptual ownership, public compatibility, deployment, or data semantics.

Continue research or request human review when sources conflict, analogues are materially different, or the choice creates a durable compatibility boundary.

## Citation rule

Repository evidence must use permanent links pinned to the audited commit. Living official documentation and maintained style guides may use their canonical current URLs. State the evidence class and the constraint that makes each repository analogous.
