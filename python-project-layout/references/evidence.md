## Purpose

Load only the evidence relevant to the decision. Read [consensus.md](consensus.md) first. Repository precedent answers bounded questions; it does not define a universal tree.

A question already answered by the consensus "Project archetypes" section needs no further evidence. Load this index when a choice is disputed, and [audited-repositories.md](audited-repositories.md) only when the routing table below names it.

Audited revisions: HTTPX 0.28.1, Datasette 1.0a23, Pydantic commit `27f95c7`, Dagster 1.13.1. Re-audit before citing a newer release, and record the revision with each claim.

## Decision routing

| Question | Primary evidence | Caution |
| --- | --- | --- |
| Flat layout mechanics | Python, PyPA, and setuptools sections in [audited repositories](audited-repositories.md) | Flat imports can hide packaging errors |
| Shallow library package | HTTPX | Mature private modules are not universal templates |
| Focused data application and CLI | Datasette | Do not copy its plugin scale or broad utilities |
| Public facade and substantial internals | Pydantic | Its compatibility and Rust boundaries are exceptional |
| Multiple distributions and integrations | Dagster | Use only for real release and dependency boundaries |
| Public API exports | HTTPX, Datasette, Pydantic | Do not re-export everything |
| Optional provider dependencies | HTTPX, Dagster | One provider does not justify a package family |
| Tests and installed artifact | Official mechanics, HTTPX, Pydantic | Checkout imports do not prove wheel correctness |
| Plugins | Datasette, Pydantic | Require a committed extension ecosystem |
| Deep subsystem boundary | HTTPX transports, Pydantic internals | Match the subsystem's actual complexity |
| Existing-repository review or migration | Consensus preservation rules and official packaging mechanics | Precedent from a greenfield tree does not justify moving an established package |
| Evaluating or editing this skill | [benchmark.md](benchmark.md) | A passing benchmark is not proof that an unlisted case is handled |

## Evidence sufficiency

Stop researching a disputed choice when all are available:

1. Applicable import or packaging behavior has been checked.
2. The project constraint selecting among alternatives is explicit.
3. One closely analogous pinned implementation supports the recommendation when such an analogue exists.
4. One credible alternative or counterexample has been inspected.
5. No unresolved choice changes conceptual ownership, public compatibility, release, deployment, or data semantics.

Continue research or request human review when sources conflict, analogues differ materially, or the choice creates a durable compatibility boundary.

## Evidence rules

- Prefer immutable repository links pinned to a tag or commit. A `master` or `main` link is not acceptable evidence.
- Record the audited revision and what makes it current enough to cite.
- Use canonical living URLs for Python and packaging specifications.
- Inspect owning code, packaging metadata, and tests. Do not infer quality from a filename or tree alone.
- State the constraint that makes an example analogous.
- State what should not be copied.
- Do not count repositories as votes.
- Do not use Go or C repository directory names as Python evidence. Use their locality, ownership, dependency, and simplicity principles only when Python mechanics permit them.

## Claim classes

Label material claims as:

- Python-enforced
- Packaging behavior
- Official guidance
- Corroborated precedent
- Contextual precedent
- Project judgment
- Unresolved
