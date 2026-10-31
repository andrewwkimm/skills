# Code-style amendment record

## 2026-10-20: Go source review and the observability case study

**Amendment classes:** Source or version change, class 4, and demonstrated worse outcome, class 3.

The class 4 edits align the Go guide with Code Review Comments, Test Comments, Google, Uber, the Go 1.25 runtime, and `go fix`. Most edited rules now name their source, or the source they depart from, in a parenthesized tag. The guide drops two rules that `go vet` enforces, and validation keeps `go vet ./...` because `go test` runs only part of vet. The blank-import and in-band-error rules restate Code Review Comments rules the guide had omitted.

The class 3 edits come from the `observability` repository, a Go 1.26 module an agent built in one pass under this skill. Its layout matched the Go Project Layout skill except for one exported pool that an existing rule already covers, so that skill is unchanged.

| Rule | Demonstrated worse outcome under the previous guide |
| --- | --- |
| Wall-clock times | `Rules.Deadline` added an offset to local midnight. In America/Chicago the 08:35 deadline computes as 09:35 on 2026-03-08 and as 07:35 on 2026-11-01. The deadline test used 2026-09-30 and passed. |
| In-band errors | `parseDate` returned nil for an empty date and for an unparseable one, and the classifier labels a nil date `dead`. A date-format change in the QA log would label every failing table dead. |
| Doc comments match code | Four doc comments described behavior the code lacks. One called the store's read-write pool a read-only handle, and another said `Ask` withholds text that it returns. |
| Instance APIs over package state | `Store.Migrate` called `goose.SetBaseFS` and `goose.SetDialect`, which set goose's package state. goose added `NewProvider` in v3.16.0 to avoid that state, and a public pull request reports the same calls racing under `t.Parallel`. |
| Failure-path fakes | `Collector.Run` documents that a failing source does not stop the others. No fake returned an error, so that path had no test. |
| Production-size tests | The provenance check passed tests whose tool results held three to six numbers. Against a simulated 20-row result, the size of one default tool call, it accepted every integer from 1 to 100 in each of 20 trials. |
| Learned state | Attribution rules learned client names during collection, so attribution depended on which sources ran. A Dagster-only run stores runs without a client, and the upsert overwrites clients stored earlier. |

The `t.Context` rule stays, reworded. Deleting it assumed `go fix` covers the case. The `testingcontext` fixer rewrites only `context.WithCancel(context.Background())`, so the repository's four bare `context.Background()` test calls would remain.

## 2026-08-26: Exception messages and function-level imports

**Amendment class:** Demonstrated worse outcome, class 3.

The previous Python guide did not define when a one-use exception message deserved a variable or when a function-level import was acceptable. One-use `error_message` variables added indirection and produced inconsistent changed functions. Unexplained function-level imports hid runtime constraints, bypassed normal import organization, and required lint suppressions whose necessity was unclear.

The revised guide constructs one-use exception messages directly. It permits a function-level import only for a concrete runtime constraint and requires an adjacent justification, the narrowest necessary suppression, practical coverage, and explicit disclosure to the user or reviewer.

## 2026-08-26: Prefer explicit types over `Any`

**Amendment class:** Demonstrated worse outcome, class 3.

The previous Python rule allowed `Any` at a dynamic boundary without requiring a check for an available explicit type. A Stripe change cast typed SDK parameters and values to `Any` even though the SDK published `ChargeListParams` and `Charge`. The casts discarded valid contracts and silenced useful diagnostics. Google Discovery provided the contrasting case: its `Resource` type cannot express methods generated from a discovery document, so one narrow ignored diagnostic accurately marks the limitation.

The revised rule requires explicit types when available and permits a narrow, explained escape hatch when the checker cannot represent a valid boundary.

## 2026-08-11: Functional lessons for imperative code

**Source class:** Practitioner writing.

**Source:** [Jeremy Bowers, Functional Programming Lessons in Imperative Code](https://jerf.org/iri/blogbooks/functional-programming-lessons-in-imperative-code/).

**Amendment class:** Demonstrated worse outcome, class 3.

The `code-style` skill has no benchmark file, so these scenarios carry the full amendment justification. The module-level `purifiable` architecture remains outside this skill under `SKILL.md` scope. The accepted changes are limited to function-level and type-level consequences.

| Rule | Demonstrated worse outcome under the previous guide |
| --- | --- |
| Value validity | A record is constructed with a required field unset, passed to a callback that reads it, and fails because observation occurred before construction finished. The Go constructor guidance listed invalid-state prevention as an option but did not forbid an incomplete value from escaping; Python had no equivalent rule. |
| Second type over mode | One type carries a `validated` flag. Downstream functions repeatedly check it, and one missed check silently processes an invalid value. A separate validated type removes the invalid combination. |
| Bare primitive convention | The preference for precise domain types is applied mechanically to unconstrained network bytes and source strings. Wrapper types add conversions and API surface while preventing no invalid state. |
| Boundary representations | The same identifier arrives through an API and a CSV file and is normalized differently. The system creates two identities for one entity and later double-encodes one output. |
| Capability minimization | A component receives a full client to perform one unauthenticated GET. Tests must reproduce the larger client surface, and the component receives authority beyond its purpose. |
| Mutation authority | Several processors receive the same mutable record and write overlapping fields. Results depend on processor order, and no record identifies which processor made each change. |
| Purity classification | An agent classifies a function taking an injected repository as core because a fake makes one test execution observationally pure. The Python guide then forbids that same core function from performing database access, producing opposite classifications for the same function contract. |

### Practitioner claims not adopted

The guide does not add module-placement rules for `purifiable` components, blanket restrictions on `map`, `filter`, or `reduce`, inheritance-oriented interface normalization, or new global-state rules. Existing scope, extraction, control-flow, interface, and global-state rules already decide those cases.
