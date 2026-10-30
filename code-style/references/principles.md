# Principles

These apply in every language. The language files say how each looks in Python and Go.

## 1. Functional core, imperative shell

A pure function computes its result from its arguments and immutable values, changes nothing outside itself, and returns the same result for the same arguments. An effect is anything else: network, files, databases, the clock, randomness, environment, configuration, secrets, mutable globals, and mutating an argument.

Put decisions in pure functions (the core) and effects in a thin layer that acquires inputs, calls the core, and applies the result (the shell). The aim is the practical gains rather than purity: logic you can test with values alone, effects you can find by reading the shell, and failures you can retry. A class, a log line, or a local mutation inside the core is fine when it costs none of those. The shell owns I/O, retries, transactions, cleanup, and metrics, each at the narrowest boundary that knows the policy: retries where idempotency is known, transactions where atomicity is defined.

- Classify a function by what it may do rather than by one run. A function that takes a client is shell, even when a fake makes one test run pure.
- Test for where an effect belongs: if a test of the logic would have to mock it, move it to the shell.
- Logging may stay in the core: it feeds no decision and no test needs to fake it. If a test must assert on a log, return the event instead.
- Extract a meaningful rule out of an effectful function even when it has one caller. Do not extract a trivial expression just because it is pure.
- Two exceptions: a thin adapter may keep translation and I/O together when a pure core would only forward values, and a small transaction script may stay one function when the extracted core would have no meaning of its own.
- Pass values, or the narrowest capability, into the core: rows rather than a client, resolved settings rather than a settings object, a stream rather than a filename. A global a function reads is a hidden parameter; pass it in. Pass a function for one operation and a collaborator for several.
- Inject clocks, randomness, id generation, and external clients where behavior depends on them. Do not inject pure standard-library functions, value constructors, or stable transformations.
- When the shell must apply several changes decided by the core, have the core return a plan (a record of what to write, post, or queue) and the shell apply it in one place.

## 2. Handle failure where it starts

Bad data that passes silently surfaces later as a wrong number nobody can trace. Check data where it enters, so the run fails at the line that received it with an error that names it.

- Parse API responses, files, and configuration into typed models at the boundary. A required field has no default, so a missing one raises there.
- Decide each missing or bad case explicitly: fail with an error that names it, skip it and log the skip, or use a default declared where the setting or model is defined. A default added at the point of use (`or {}`, `.get(key, default)`, `or []`) hides that decision. When the source documents a value as optional, the model declares it.
- Treat an empty result as its own case, checked where it is returned.
- Catch only what the current layer can handle, and let everything else fail the unit of work. Make that unit safe to run again after a failure, because this rule means it will be.

## 3. Reuse existing code before writing new

Two ways to do one thing make every later reader work out which is right.

- When something close exists, extend it, for example with a parameter, and update its callers in the same change.
- When a change replaces something, delete the old version in the same change.
- Give each setting one home; derive what can be derived.
- If an existing pattern is wrong, fix it everywhere in a separate change rather than diverging in one place.
- Similar-looking code is not yet reuse. Share code when callers depend on the same concept and would change for the same reason. A function with one user can stay beside that user until a second appears.

## 4. Optimize for the reader

Code is read far more often than it is written, and working memory is small. Write so the next reader, who lacks your context, can follow it without stopping.

- **Self-documenting names.** Prefer a better name or an explanatory variable to a comment. When the name would have to be a sentence, write the comment.
- **Positive conditions.** Name flags for what is enabled (`validate` rather than `skip_validation`) and put the positive branch first. `is not None` reads as a positive.
- **Named constants** for values whose meaning is not obvious, such as limits, sizes, and conversion factors.
- **Shallow nesting.** Aim for two levels. Guard clauses, early returns, and combined conditions flatten most code; a third level is a prompt to restructure. Keep tightly coupled logic together when an extraction would hide its controlling condition.
- **No dead code.** Delete commented-out code and unused functions. When behavior changes, update or delete every comment, docstring, README line, and test name that described it.
- **Comments** say what the code cannot: a business reason, an external constraint, an invariant, a unit, a tradeoff, or why the obvious approach is wrong. They describe the code as it is; history belongs in commit messages, so no "now", "no longer", "instead of the old", "as discussed", and no phrasing borrowed from the conversation that produced the change. Do not restate a name, a signature, or the next line. Section comments may mark phases of a long, flat function.

### Depth over decomposition

A function earns its place by hiding real complexity behind a simpler interface (Ousterhout's deep module). A shallow helper, whose call teaches as much as its body, costs a jump, a name, and a contract to keep accurate, and buys nothing.

- Extract when the piece makes sense on its own and hides real work: parsing, retries, state coordination, resource handling, or a business rule. One caller is enough when that is true.
- Inline a one-caller helper that only renames a construction, an argument unpacking, a setup step, or a short guard.
- Long, flat, sequential code is fine. If steps must happen in order, let them read in order. Splitting a straight workflow into one-line helpers hides the order and makes it possible to call a step out of sequence.
- A good split lets someone read either function without opening the other.
- Do not extract or inline code to satisfy a slogan.

### Keep code read together close together

Place related decisions, the data they use, and the resources they hold close enough to follow without jumping. Put callers above callees when that reads better; do not reorder untouched code to satisfy an ordering rule.

## 5. Test behavior through the real code

- Mock only the effects rule 1 moved to the shell. Run everything else for real.
- Make fakes and fixtures copy the real responses: field names, types, nullability, and nesting. A fake that stands in for a real service needs its own test against that service's documented behavior. When a change alters what one part hands another, test both parts together with only the external effects faked.
- Assert on returned values and written data. Assert that a call happened only when the call is the behavior, such as sending a request.
- Ask of every test whether it would still pass if the code were wrong. If it would, fix or delete it.
- Prefer, in order: the real implementation, a fake (a working stand-in with shortcuts, such as an in-memory store), a stub (canned answers), a spy (records calls), a mock (asserts on calls). Patch only what cannot be injected. The words carry the rule, so use them precisely in code and review.

## 6. Test every relevant path

- The happy path, then every branch the code can take.
- Both settings of every option, flag, or argument the change touches.
- Each failure the code handles: an error status, an empty body, a missing field, a timeout. Assert the specific exception promised.
- Edge cases that apply, parametrized: empty, one, many, missing, null, non-ASCII.
- A regression test with every bug fix, written to fail before the fix.

## 7. Make invalid states hard to build

- One type per validity contract. Validate when constructing; never let a half-built value escape. A builder may mutate locally while assembling, and a supported zero value counts as valid.
- Prefer a design in which the invalid case cannot arise over a check that detects it.
- When an operation has distinct outcomes, return distinct types (a selection or a refusal) rather than one type with optional fields and a mode flag.
- Use a domain type when it prevents an invalid combination or removes repeated validation; do not wrap a value only to label where it came from. A bare primitive says the value is unconstrained.
- Decode at input and encode at output. Hold the decoded value in between. Keep a raw representation only for a contract, audit, or round-trip need, behind a name that marks it as exceptional.
- Name a type for its role, and use the domain noun alone when a suffix adds nothing: `Spec` for desired state or matching criteria, `Schema` for fields and constraints, `Config` for reusable settings, `Options` for one call's controls, `Policy` for rules that decide whether or when, `Definition` for a declaration a framework interprets, `Contract` for guarantees enforced across a boundary.

## 8. Constrain mutation and shared state

- Give mutable state one owner, and give collaborators the narrowest operation they need rather than general access.
- Prefer returning new values. Local mutation the caller cannot see is fine.
- Make a state change in one place at a known time rather than from many call sites.
- Keep startup configuration separate from what a run learns, and pass learned state forward as explicit values.

## 9. Keep dependencies pointing one way

Arrange modules so dependencies form layers with no cycles. Each module should then be understandable, and testable, with only the modules beneath it. Where the repository checks this mechanically (import-linter in Python, the compiler in Go), keep that configuration current.

When a cycle appears, find the exact names involved and fix it, preferring in order: move the code to the module it belongs in; extract the shared piece into a lower module; add a higher module that composes both; introduce a small interface. A copy is a last resort and needs a stated reason. The project-layout skills decide where moved code lives.

Import rules check static imports only. They cannot see dynamic loading, configuration keys, shared tables, globals, or whether a function took a whole client when it needed one method; review covers those.

## Sources

- Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell).
- John Ousterhout, *A Philosophy of Software Design*.
- [John Carmack on inlined code](http://number-none.com/blow/john_carmack_on_inlined_code.html).
- [Loup Vaillant, The Source of Readability](https://loup-vaillant.fr/articles/source-of-readability).
- [Jeremy Bowers, Functional Programming Lessons in Imperative Code](https://www.jerf.org/iri/blogbooks/functional-programming-lessons-in-imperative-code/).
- [Jeremy Bowers, Layered Design in Go](https://jerf.org/iri/post/2025/go_layered_design/).
- [Google Testing Blog, Increase Test Fidelity by Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html).
