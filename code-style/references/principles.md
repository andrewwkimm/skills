# Principles

These apply in every language; the language files say how each looks in Python and Go. Each rule carries its reason so that you can apply it to a case it does not name, and so that you can tell when the reason does not hold.

## 1. Functional core, imperative shell

Most defects come from code running in a state its author did not picture. A function that computes its result from its arguments alone has no such state: it can be read, tested, and rerun in isolation. An effect is anything else: network, files, databases, the clock, randomness, environment, configuration, secrets, mutable globals, and mutating an argument.

Put decisions in pure functions (the core) and effects in a thin layer that gathers inputs, calls the core, and applies the result (the shell). Purity is a continuum: a function that reaches less outside state is better even when it is not pure, and untangling the worst state-laden code is worth more than perfecting code that is already nearly pure. The aim is the practical gains, not purity for its own sake: logic you can test with values alone, effects you can find by reading the shell, and failures you can retry.

- Classify a function by what it may do, not by one run. A function that takes a client is shell even when a fake makes one test run pure.
- Test for where an effect belongs: if a test of the logic would have to fake it, move it to the shell.
- Logging may stay in the core: it feeds no decision and no test needs to fake it. If a test must assert on a log, return the event instead.
- Pass values, or the narrowest capability, into the core: rows rather than a client, resolved settings rather than a settings object, an open stream rather than a filename. A global a function reads is a hidden parameter; pass it in. A single bag of everything (a context object, `self` carrying every collaborator) passed into logic defeats the purpose; pass the two values the logic reads.
- Inject clocks, randomness, id generation, and external clients where behavior depends on them. Do not inject pure standard-library functions, value constructors, or stable transformations.
- When the shell must apply several changes decided by the core, have the core return a plan (a record of what to write, post, or queue) and the shell apply it in one place.
- Shape code as data types plus functions that take and return them. A type gets methods when they read its state and callers would call them on it; a type gets mutable state when several operations must share it (a connection, a cache, a lifetime). A workflow is a function, not a class. The language files give the mechanics.
- Work at the medium scale. The lessons that transfer from functional programming are purifiable components, explicit inputs, and valid-by-construction values. Rewriting loops as maps and folds, or chaining comprehensions, is not one of them; a plain loop in a pure function is already functional.
- Two exceptions: a thin adapter may keep translation and I/O together when a pure core would only forward values, and a small transaction script may stay one function when the extracted core would have no meaning of its own.

## 2. Handle failure where it starts, and define away the failures you can

Bad data that passes silently surfaces later as a wrong number nobody can trace. Nothing alerts on a value that is wrong but plausible, and the further it travels from its source the harder it is to trace back. Check data where it enters, so the run fails at the line that received it with an error that names it.

- Parse API responses, files, and configuration into typed models at the boundary. A required field has no default, so a missing one fails there.
- Decide each missing or bad case explicitly: fail with an error that names it, skip it and log the skip, or use a default declared where the setting or model is defined. A default added at the point of use (`or {}`, `.get(key, default)`, a zero when the lookup misses) hides that decision, and a missing client, a misspelled key, and an absent field then look the same downstream.
- Skip and log only records the contract says are not this unit's concern. A record that contradicts an assumption the unit relies on is a failure, because it means the input is not what the code believes it is.
- Treat an empty result as its own case, checked where it is returned.
- Catch only what the current layer can handle, and let everything else fail the unit of work. Principle 3 makes that unit safe to run again, which this rule relies on.

### Define errors out of existence

Every case an operation reports as a failure is a case each caller must handle, and callers get it wrong. Before adding one, ask whether the operation can be defined so that the case is a normal result (Ousterhout, *A Philosophy of Software Design*, chapter 10).

- Redefine the operation when the new result is correct for every caller under its stated contract. Deleting what is already gone succeeds, because the promise is "afterwards it does not exist". Ensuring a directory exists succeeds when it already does. A query with no matches returns an empty result, and the caller checks for empty as its own case. Writing the same row twice is an upsert on its key.
- Put the redefinition where callers read the contract: the name (`delete_if_exists`, `EnsureDir`), the doc comment, or the library's flag for exactly that case. Prefer a library operation that already has the semantics to a check-then-act pair, which also races.
- This is not the point-of-use default the rules above forbid. The test: could any caller now receive a plausible but wrong value without knowing? A missing amount read as zero, an unparseable date read as no date, an existing resource returned although its settings differ from the ones requested, an out-of-range index clamped when the index was the caller's bug: each still fails.
- Redefine only the case you mean. A flag or handler that also swallows unrelated failures (permissions, network, a full disk) hides them; narrow it to the one case.
- When several steps in a row each need the same failure check and the caller needs only all-or-nothing, keep the first failure in one place and check it once at the end. Python's exceptions already do this; `go.md` shows the Go form.

## 3. Make each unit of work deterministic and safe to rerun

A batch job, a pipeline task, or a partition load is rerun constantly: after a failure, during a backfill, when logic changes. If rerunning can double-count, depend on when it ran, or leave a half-written output, every rerun is a risk and every failure is a cleanup. (Beauchemin, *Functional Data Engineering*.)

- Given the same parameters and the same inputs, a unit produces the same output. Pass the run date, the partition, and the window in; do not read the clock or "the latest" inside the unit.
- A unit writes one output, and writes it by replacing the whole thing: overwrite the partition, upsert on the key, write to a temporary location and swap. Appending is what makes a rerun double-count.
- Keep per-run scratch state (temporary tables, work directories) keyed by the run, so two instances cannot interfere.
- Land raw inputs once and leave them unchanged; derived outputs are rebuilt from them, so a logic change is a rerun rather than a migration.
- Run every step on every run. Skipping a step because a previous run "already did it" is where partially updated outputs come from; if the step is expensive, make it cheap to redo rather than conditional.
- Logic that changes over time is gated on the data's date inside the unit, not on the deploy date, so a backfill reproduces what the period's rules were.
- A unit that reads its own previous output needs a stated reason, because it serializes backfills and makes the output depend on history.

## 4. Reuse existing code before writing new

Two ways to do one thing make every later reader work out which is right and whether the difference is intended.

- When something close exists, extend it, for example with a parameter, and update its callers in the same change.
- When a change replaces something, delete the old version in the same change.
- Give each setting one home; derive what can be derived.
- If an existing pattern is wrong, fix it everywhere in a separate change rather than diverging in one place.
- Similar-looking code is not yet reuse. Share code when callers depend on the same concept and would change for the same reason. A function with one user can stay beside that user until a second appears.

## 5. Optimize for the reader

Code is read far more often than it is written, and a reader holds only a few things in mind at once. Code that must be understood together should sit together, and nothing should make the reader stop to puzzle.

- **Self-documenting names.** Prefer a better name or an explanatory variable to a comment. When the name would have to be a sentence, write the comment.
- **One term per concept.** Before naming a new type, field, parameter, or function, search for the term the code already uses for that concept and use it. A different word tells the reader it is a different thing. Give a recurring value, such as a database handle or an API client, one name in every signature. Do a rename across the codebase as its own change.
- **Specific words.** Replace a word that could name anything with the one it stands for: `data`, `info`, `item`, `obj`, `thing`, `details`, `manager`, `helper`, and the verbs `handle`, `process`, `manage`, `do`, `perform`. Keep one when it is the domain or framework term or the scope is a few lines.
- **Name the contents, not the type.** `users`, not `users_map` or `user_list`. When two values of one type share a scope, name their roles (`original`, `updated`), not `config1` and `config2`.
- **The one-sentence test.** If a function, type, or module cannot be described in one sentence, it does more than one thing or is not yet understood. Restructure it before documenting it.
- **Positive conditions.** Name flags for what is enabled (`validate` rather than `skip_validation`) and put the positive branch first. `is not None` reads as a positive.
- **Named constants** for values whose meaning is not obvious, such as limits, sizes, and conversion factors.
- **Declare near use.** Introduce a variable where it is first needed, not at the top. Inline a variable used once when its name adds nothing the expression does not already say; keep it when the name explains the expression.
- **Shallow nesting.** Aim for two levels. Guard clauses, early returns, and combined conditions flatten most code; a third level is a prompt to restructure. Keep tightly coupled logic together when an extraction would hide its controlling condition.
- **Plain sequencing.** Steps that happen in order are written in order, as statements. A pipeline abstraction, a chain of callbacks, or a step registry earns its place only for concurrency, distribution, scheduling, or stages chosen at run time (an orchestrator's task graph qualifies); used for plain sequencing inside one task it is a platform inside the program.
- **No dead code.** Delete commented-out code and unused functions. When behavior changes, update or delete every comment, docstring, README line, and test name that described it.
- **Comments** say what the code cannot: a business reason, an external constraint, an invariant, a unit, a tradeoff, or why the obvious approach is wrong. They describe the code as it is; history belongs in commit messages, so no "now", "no longer", "instead of the old", "as discussed", and no phrasing borrowed from the conversation that produced the change. Do not restate a name, a signature, or the next line. A comment on a constant says what the value is or where it comes from. Section comments may mark phases of a long, flat function.

### Depth over decomposition

A function earns its place by hiding real complexity behind a simpler interface (Ousterhout's deep module). A shallow helper, whose call teaches as much as its body, costs a jump, a name, and a contract to keep accurate, and buys nothing.

- Extract when the piece makes sense on its own and hides real work: parsing, retries, state coordination, resource handling, or a business rule. One caller is enough when that is true.
- Inline a one-caller helper that only renames a construction, an argument unpacking, a setup step, or a short guard.
- Long, flat, sequential code is fine. If steps must happen in order, let them read in order. Splitting a straight workflow into one-line helpers hides the order and makes it possible to call a step out of sequence; a step that several places must run is made pure, called from one place, and inlined nowhere.
- A good split lets someone read either function without opening the other.
- Do not extract or inline code to satisfy a slogan, including this one.

### Keep code read together close together

Place related decisions, the data they use, and the resources they hold close enough to follow without jumping. Put callers above callees when that reads better; do not reorder untouched code to satisfy an ordering rule.

## 6. Test behavior through the real code

- Mock only the effects principle 1 moved to the shell. Run everything else for real.
- Test through the public interface. Test a private function directly only when its public caller would bury the rule in unrelated setup. Never widen visibility (export a name, drop a leading underscore) only so a test can reach something.
- Make fakes and fixtures copy the real responses: field names, types, nullability, and nesting. A fake that stands in for a real service needs its own test against that service's documented behavior. When a change alters what one part hands another, test both parts together with only the external effects faked.
- Assert on returned values and written data. Assert that a call happened only when the call is the behavior, such as sending a request.
- Ask of every test whether it would still pass if the code were wrong. If it would, fix or delete it.
- Prefer, in order: the real implementation, a fake (a working stand-in with shortcuts, such as an in-memory store), a stub (canned answers), a spy (records calls), a mock (asserts on calls). Patch only what cannot be injected. The words carry the rule, so use them precisely in code and review.

## 7. Test every relevant path

- The happy path, then every branch the code can take.
- Both settings of every option, flag, or argument the change touches.
- Each failure the code handles: an error status, an empty body, a missing field, a timeout. Assert the specific error promised.
- Edge cases that apply, parametrized: empty, one, many, missing, null, non-ASCII, and for date logic a daylight-saving transition.
- A regression test with every bug fix, written to fail before the fix.
- Test at production shape. A fixture with three rows passes checks that fail at three thousand; when size, ordering, or duplicates matter, one test uses realistic data.

## 8. Make invalid states hard to build

Validity checked once at construction is validity every later line can rely on; validity checked by every consumer is validity one of them forgets.

- One type per validity contract. Validate when constructing; never let a half-built value escape. A builder may mutate locally while assembling, and a supported zero value counts as valid. A constructor assembles; it does no I/O.
- Prefer a design in which the invalid case cannot arise over a check that detects it.
- When an operation has distinct outcomes, return distinct types (a selection or a refusal) rather than one type with optional fields and a mode flag.
- Use a domain type when it prevents an invalid combination or removes repeated validation; do not wrap a value only to label where it came from. A bare primitive says the value is unconstrained.
- Decode at input and encode at output. Hold the decoded value in between. Keep a raw representation only for a contract, audit, or round-trip need, behind a name that marks it as exceptional.
- When several sources or sinks differ in detail, give them one interface and let the ones that lack an operation implement it as a documented no-op or "not applicable" result, rather than special-casing each in the callers.
- Name a type for its role, and use the domain noun alone when a suffix adds nothing: `Spec` for desired state or matching criteria, `Schema` for fields and constraints, `Config` for reusable settings, `Options` for one call's controls, `Policy` for rules that decide whether or when, `Definition` for a declaration a framework interprets, `Contract` for guarantees enforced across a boundary.

## 9. Constrain mutation and shared state

Total immutability is the wrong goal in an imperative language; knowing what is mutated, by whom, and when is the right one.

- Give mutable state one owner, and give collaborators the narrowest operation they need rather than general access.
- Prefer returning new values; offer the value-returning form (`normalized()`) before the self-mutating one. Local mutation the caller cannot see is fine, and copying a large structure to avoid it is not required.
- Make a state change in one place at a known time rather than from many call sites. One check in one place beats the same check at twenty callers.
- Keep startup configuration separate from what a run learns, and pass learned state forward as explicit values.

## 10. Keep dependencies pointing one way

Arrange modules so dependencies form layers with no cycles. Each module is then understandable, and testable, with only the modules beneath it, and a fake for a module can be built from the fakes of the modules it uses. Where the repository checks this mechanically (import-linter in Python, the compiler in Go), keep that configuration current.

When a cycle appears, find the exact names involved and fix it, preferring in order: move the code to the module it belongs in; extract the shared piece into a lower module; add a higher module that composes both; introduce a small interface. A copy is a last resort and needs a stated reason. The project-layout skills decide where moved code lives.

Import rules check static imports only. They cannot see dynamic loading, configuration keys, shared tables, globals, or whether a function took a whole client when it needed one method; review covers those.

## Sources

- Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell).
- John Carmack, [Functional Programming in C++](https://sevangelatos.com/john-carmack-on/) (2012) and [on inlined code](http://number-none.com/blow/john_carmack_on_inlined_code.html) (2007, with 2014 preface).
- Maxime Beauchemin, [Functional Data Engineering](https://maximebeauchemin.medium.com/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a).
- Jeremy Bowers, [Functional Programming Lessons in Imperative Code](https://www.jerf.org/iri/blogbooks/functional-programming-lessons-in-imperative-code/) and [Layered Design in Go](https://jerf.org/iri/post/2025/go_layered_design/).
- John Ousterhout, *A Philosophy of Software Design*.
- Loup Vaillant, [The Source of Readability](https://loup-vaillant.fr/articles/source-of-readability).
- Peter Hilton, [How to name things](https://www.slideshare.net/slideshow/how-to-name-things-the-hardest-problem-in-programming/39383508).
- Rob Pike, [Errors are values](https://go.dev/blog/errors-are-values).
- Dave Cheney, [Practical Go](https://dave.cheney.net/practical-go/presentations/gophercon-singapore-2019.html).
- Google Testing Blog, [Increase Test Fidelity by Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html).
