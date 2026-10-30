---
name: evidence-tiering
description: Separates directly observed facts, derived conclusions, and untested behavior in research, design, evaluation, and decision-making.
---
# Evidence tiering

Keep observed facts, derived conclusions, and untested behavior disjoint. Verification completeness is recorded separately from claim tier. Apply the same source-neutral tests to internal sources, external sources, and reviews from any author or system.

## Classify claims

### F1: directly observed fact

Use F1 for a specific fact directly observed in a source, repository state, structured tool output, calculation, or executed check. Record the source, version or date, and a repeatable check. A passing test is F1 only for that recorded run; it does not by itself establish broader behavior.

A statement in a message, ticket, or document is F1 for the fact that its author said it, never for the behavior it describes. "IT reported a 24-hour lockout" is F1; "the server enforces a 24-hour lockout" stays F2 or F3 until a configuration read or an executed check observes it.

Examples: a named configuration key appears at a recorded file and line; a structured response reports `state: open`; a recorded calculation produces 42; one test passed in the stated environment at the stated revision.

### F2: derived conclusion

Use F2 for a conclusion derived from named, supported premises. List the premises and the inference separately so a reviewer can challenge either one.

Absence claims are F2 only when the record includes the exact query, concrete scope, units or count, stopping rule, and observed result. Without all five, an absence claim is unsupported and MUST be researched, qualified, or omitted. It is not F3.

Example: a bounded search found no matching setting in 128 tracked configuration files after examining every file returned by the stated file query. The observed file list and search results are F1; the bounded absence conclusion is F2.

### F3: untested runtime or real-world behavior

Use F3 only for runtime or real-world behavior that requires execution, such as end-to-end interoperability, behavior under load, or an operational outcome in a target environment. State it as a hypothesis and name the execution that would settle it.

Example: the service will preserve ordering during a regional failover remains F3 until the named failover test runs. A narrow passing unit test may be F1 for that run while the broader operational claim remains F2 or F3, depending on its supported premises.

## Record verification completeness separately

Tier says what kind of claim this is. Verification completeness says whether the required source reads, queries, calculations, or executions were completed. Do not raise or lower a tier to signal incomplete work.

For each decision-critical claim, record:

| Field | Required content |
| --- | --- |
| Claim | One specific factual statement or conclusion |
| Tier | F1, F2, or F3 |
| Evidence | Direct observation, or named premises and inference |
| Source | Version, revision, date, or environment |
| Recheck | Exact repeatable query, calculation, or execution |
| Completeness | Complete, partial, blocked, or pending |

## Source selection

For every decision-critical source, record its authority for the claim, suitability to the exact question, and freshness for facts that can change. A familiar or internal source receives no automatic preference, and an external review receives the same scrutiny as any other evidence.

## Apply the rules

1. Ground recommendations in F1 observations or F2 conclusions with named premises.
2. Keep every F3 statement conditional on its named execution.
3. For an absence claim, require the exact query, scope, units or count, stopping rule, and result; otherwise research, qualify, or omit it. For code absence, inspect each complete relevant function and every relevant callee needed to establish the claim, rather than relying on filenames, symbols, snippets, or partial bodies.
4. Treat one passing test as evidence only for its recorded run. State separately what, if anything, supports broader behavior.
5. Date changeable facts and record source versions.
6. Retrieve missing sources instead of speculating. Report the exact failed URL or query when access is blocked.
7. Record conflicting evidence and resolve it through precedence, version matching, or execution.
8. Keep judgments distinct from factual premises and link each judgment to the premises it uses.
9. When an unresolved F3 could reverse a decision, gate the decision on the named execution or escalate it; do not deliver the decision as settled.
10. For an unresolved design fork, default to the option that preserves current behavior and compatibility, state the fallback if that default fails, and gate any irreversible choice on the evidence that resolves the fork.

## Delivery gate

Before delivery, identify each decision-critical claim, assign its tier, record verification completeness, and confirm that every F2 conclusion names supported premises. Review the final output claim by claim and confirm that each material claim is covered by cited evidence or is clearly identified as judgment. Confirm that each F3 claim is phrased as an untested hypothesis, and that no unsupported absence claim has been mislabeled as F3. Report unresolved conflicts rather than hiding them.
