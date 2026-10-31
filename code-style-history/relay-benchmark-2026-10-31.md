# Webhook relay benchmark: no skill vs. 2026-10-29 skills vs. 2026-10-31 skills

Three agents built the same service from the same spec in three phases (core; five features; a change request plus two bug reports), each continuing its own session so phases 2 and 3 were feature work inside code it had written. Variants: no skill; the skills as installed on 2026-10-29 (code-style plus python-project-layout, including the broken `shared-principles.md` reference); the 2026-10-31 skills. Acceptance tests (55) were written from the spec before any build was read and drive the service only through its CLI and HTTP contract. Code: `none/`, `old/`, `new/`; per-phase snapshots in `snapshots/`; scorer `score.py`; reports `report-phase{1,2,3}.md`.

## Results

| | none | old (10-29) | new (10-31) |
| --- | --- | --- | --- |
| Acceptance, phases 1+2+3 | 54 / 55 | 55 / 55 | 55 / 55 |
| Own tests | 104 | 171 | 142 |
| Source lines / test lines | 1,325 / 1,339 | 1,512 / 2,238 | 1,386 / 1,717 |
| Modules | 9 | 11 | 11 |
| Data / exception / behavior classes | 11 / 4 / 4 | 21 / 2 / 2 | 17 / 3 / 1 |
| Methods on behavior classes | 19 (`Store` has 16) | 6 (HTTP handler) | 1 (HTTP handler) |
| Module-level functions | 42 | 63 | 62 |
| `try` blocks | 23 | 11 | 13 |
| Pattern findings (source) | 11 | 8 | 7 |
| Outcomes as distinct types | no (`Outcome` record with status field) | `Succeeded \| Failed` | `UnknownProvider \| BadSignature \| InvalidEvent \| Accepted`, `Succeeded \| Failed` |
| MagicMock / `raises(Exception)` in tests | 0 / 0 | 0 / 0 | 0 / 0 |

Acceptance-test corrections during the run, all on the test side: integer delivery ids passed to `subprocess`; two races with the live `serve` worker; phase-1 exact-dict assertions that phase 2 legitimately extended; a rate-limit test that depended on the worker not delivering. None of the builds was changed.

## What the one acceptance failure was

The no-skill build accepts `X-Hub-Signature-256` without the `sha256=` prefix: its `_strip_prefix` returns the value unchanged when the prefix is absent, so a bare hex digest validates. Both skilled builds reject it (old: "a malformed hub value maps to an empty digest that can never verify"; new: `presented()` returns None when the prefix is missing). Lenient acceptance of an undocumented variant at a security boundary is the pattern principle 2 exists to stop; it is also a defensible product call, which is why it is one test and not a verdict.

## Where the builds differ in shape

- **Storage.** No skill: a `Store` class with 16 methods and a `_MinuteBudget` class. Both skilled builds: module functions over a connection, with the SQL beside the queries that use it. Both are allowed under the guide's class line; the skilled shape is the one it prefers.
- **Decisions as values.** All three implemented `Retry-After` as a pure transition function over values (`_outcome`, `plan_after_attempt`, `resolve_attempt`) with the header parsed into the result by the transport. The skilled builds also made the ingest outcome a type union; the no-skill build maps status codes inline in the handler.
- **Exception surface.** 23 `try` blocks (none) against 11 and 13. The no-skill handler wraps the whole request in `except Exception` to return 500; the skilled builds keep that only on the worker loop, with the comment the skill asks for.
- **Boundary strictness.** `extra="forbid"` on config in all three; strict mode on webhook bodies in the skilled builds only.
- **Tests.** All three test through loopback HTTP servers and subprocesses, with no mocks. The old-skill build wrote the most tests (171, 2,238 lines); the new-skill build wrote fewer, shorter ones (142).
- **Self-correction.** In phase 3 the new-skill agent reported a defect in its own phase-2 rate limit (it counted deliveries, the spec counts requests) and added a regression test; the other two replaced the same table for the same reason without calling it a defect.
- **Reporting.** Both skilled agents listed what they could not verify (the wheel build) and the calls made under a default; the no-skill agent listed decisions without flagging gaps. The broken reference in the old skills was noted and worked around; it cost nothing.

## Reading

1. **Skill versus no skill:** a real but modest difference. Same spec compliance (one boundary-leniency failure aside), fewer exception handlers, functions over repository classes, outcomes as types, stricter boundaries, more explicit reporting. The model's unaided code is good; the skill moves its shape toward the guide's.
2. **Old versus new skill:** indistinguishable on everything measured here. The new draft produced slightly less source with the same acceptance and fewer behavior classes; the old draft produced more tests. One agent's self-caught defect is one data point. At ~1,400 source lines over three phases, nothing in the 10-31 changes (reasons on principles, pipelines principle, Python shape rule, snippets, stop-and-ask) produced a measurable gain over the 10-29 text in this project.
3. **What that means for the draft:** its justified value is the decision log and benchmark (the mechanism against re-litigating), the fixed layout reference, the settled contested rules (testify, iterators, tests, class line), and honest documentation of what is and is not known. It is not justified as "writes better code than the previous version", and the change record should say so.
4. **Where a difference might still appear:** data-pipeline work, where principle 3 (idempotent units) has no analogue in the 10-29 text and this service exercised it only through "replace, never append"; a larger legacy codebase with existing smells rather than one the agent wrote itself; Go, where the 10-31 Sequences, testify, and test-package rules change the output directly.

## Follow-up: why new has fewer tests, and whether that made it worse

Own-test counts were 171 (old) and 142 (new). The difference is structural, not coverage:

| Test module | old | new |
| --- | --- | --- |
| `test_cli` | 18 | 18 |
| `test_delivery` | 51 | 50 |
| `test_webhooks` | 34 | 33 |
| `test_config` | 29 | 41 |
| `test_type_patterns` | 22 | none |
| `test_server` (HTTP handler over a socket) | 14 | none |
| `test_store_purge`, `test_runtime` | 3 | none |

Old split its type-pattern grammar into a standalone two-function module (22 parametrized cases) and kept an HTTP handler class tested over real sockets. New left pattern matching on the config model, covered by its config tests (12 more cases there), and tested HTTP through the WSGI application function inside the webhook tests. Fewer modules, fewer test files, same behavior reached through the nearest public surface. The three test modules old has that new lacks account for the gap.

Measured instead of counted (both on the same service, same operators):

- **Statement and branch coverage of each build's own tests, subprocesses included:** old 98%, new 98%, no skill 89%. Plain `coverage` showed new at 74% because its CLI and `serve` tests run as subprocesses; with a startup hook that follows them the figures are equal.
- **Mutation testing** (`mutation.py`: flip comparison and arithmetic operators, swap `and`/`or`, nudge integer constants, negate booleans, drop `not`; every site, own tests only): old killed 126 of 168 (75.0%), new 133 of 180 (73.9%), no skill 159 of 212 (75.0%). A one-mutant difference is far inside the noise of a sample this size.
- **What survives, by category, in both skilled builds:** `frozen=True` flipped to mutable, argparse `required=True`, `min_length`/`ge` bounds on config fields, and table-rendering details. These are mostly equivalent or low-value changes.
- **Real gaps, from reading the survivors.** Both builds leave the rate-limit window end (`minutes=1`) unpinned, so a two-minute window passes their tests. New additionally leaves its explicit `200 <= status < 300` untested at 300 (a 3xx would count as success), the window start (`second=0`, `microsecond=0`) unpinned, and empty webhook `id`/`type` strings untested. Old additionally leaves a few timezone and `max(0, ...)` guards unpinned. Old has no 2xx comparison to mutate because it lets `urllib` decide what is an error, so the gap is a consequence of making the rule explicit, which is the guide's preference.

Conclusion: no evidence the new build's tests are weaker. The two suites detect injected faults at the same rate and cover the same lines; new's suite is smaller because its structure has fewer seams. The three boundary gaps above are worth closing and would cost about four test cases.
