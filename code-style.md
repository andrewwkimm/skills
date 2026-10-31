# Code Style: the readable version

This is the human-readable companion to the `code-style` skill. It follows the skill's principles in the same order, says why each exists, and shows one small example per principle. The skill is the source of truth for an agent; this document is for a person who wants to understand the thinking or review a change against it. Where a rule is a deliberate house choice rather than a settled fact, the text says so, and the skill's `decisions.md` records the alternatives.

The examples are illustrative. The comments inside the "Avoid" and "Prefer" blocks are there to teach; production code would not carry them.

## What the guide is for

A codebase written by several people and several agents converges only if the defaults are shared. Most of these rules exist so that the next reader, who lacks the author's context, can follow the code without stopping, and so that a failure surfaces at the line that caused it rather than three steps downstream. None of them is a style preference for its own sake; each says why it exists, and when the reason does not apply, the rule does not either.

Precedence, highest first: correctness and safety; public compatibility; the repository's own conventions and tools; the owner's stated preferences; this guide. The guide marks a handful of rules **MUST**; the rest are defaults to depart from for a reason you can state in a sentence.

## 1. Functional core, imperative shell

Most bugs happen when code runs in a state its author did not picture. A function that computes its result from its arguments alone has no hidden state: you can read it, test it with values, and run it again. Everything else is an effect: network, files, databases, the clock, randomness, environment, configuration, secrets, globals, and mutating an argument.

The shape to aim for is a thin shell that gathers inputs, calls pure functions to decide, and applies the results. Purity is a continuum. A function that reaches less outside state is better even when it is not pure, and untangling the one function that touches everything is worth more than polishing the ones that are already nearly pure. Logging may stay inside logic: it feeds no decision and no test needs to fake it.

The lesson that transfers from functional programming is this medium-scale structure, not the micro-scale syntax. Rewriting loops as maps and folds, or chaining comprehensions, does not make code more functional; a plain loop inside a pure function already is.

Suppose a job reads the open invoices for a customer, decides which are overdue, and sends a reminder for each.

**Avoid**

```python
def send_reminders(customer_id: str, billing: BillingClient, mail: Mailer) -> None:
    today = date.today()                       # the clock, read inside the logic
    for invoice in billing.list_open(customer_id):
        if invoice.due_on < today - timedelta(days=GRACE_DAYS):
            mail.send(invoice.contact, overdue_text(invoice))
# Testing "which invoices count as overdue" requires faking the client, the
# mailer, and the clock.
```

**Prefer**

```python
def overdue_invoices(invoices: Sequence[Invoice], today: date) -> list[Invoice]:
    cutoff = today - timedelta(days=GRACE_DAYS)
    return [invoice for invoice in invoices if invoice.due_on < cutoff]


def send_reminders(customer_id: str, today: date, billing: BillingClient, mail: Mailer) -> None:
    for invoice in overdue_invoices(billing.list_open(customer_id), today):
        mail.send(invoice.contact, overdue_text(invoice))
# The rule is tested with a list and a date. The shell is three lines of effects.
```

The same principle decides the shape of code in general: a data type plus functions that take and return it. A type gets methods when they read its state and callers would naturally call them on it; a type gets mutable state only when several operations must share it. A workflow is a function, not a class. Python makes it easy to turn a workflow into a class whose private methods pass their state through `self`; that is the hidden-parameter problem again, in a different costume (see section 11).

## 2. Handle failure where it starts, and define away the failures you can

Bad data that passes silently becomes a wrong number nobody can trace. Nothing alerts on a value that is wrong but plausible, and the further it travels from its source, the harder it is to trace back. So check data where it enters: parse responses, files, and configuration into typed models at the boundary, and let a required field with no default fail there, by name.

Decide each missing or bad case on purpose: fail, skip and log the skip, or use a default declared where the setting is defined. A default added at the point of use hides that decision, and a missing client, a misspelled key, and an absent field then all look the same downstream.

**Avoid**

```python
def parse_lines(payload: dict) -> list[dict]:
    items = payload.get("data", {}).get("items") or []     # error body, missing key, empty page: all []
    return [{"id": i["id"], "cents": int(i.get("amount_cents", 0))} for i in items]
# A dropped column becomes zero revenue, and the total is simply wrong.
```

**Prefer**

```python
class Line(BaseModel):
    id: str
    amount_cents: int          # no default: a line without an amount is bad data


class Page(BaseModel):
    ok: bool
    error: ApiError | None
    items: list[Line]


def parse_lines(payload: dict) -> list[Line]:
    page = Page.model_validate(payload)          # a missing key or bad field fails here, by name
    if not page.ok:
        raise BillingApiError(page.error)        # an error body is an error, not an empty page
    return page.items                            # an empty page is a real result; the caller decides
```

The other half of this principle sounds like its opposite and is not. Every case an operation reports as a failure is a case each caller must handle, and callers get it wrong. Before adding one, ask whether the operation can be defined so the case is a normal result. Deleting what is already gone succeeds, because the promise is "afterwards it does not exist". Ensuring a directory exists succeeds when it already does. A query with no matches returns an empty result. Writing the same row twice is an upsert on its key.

One test keeps the two halves apart: could any caller now receive a plausible but wrong value without knowing? If not, redefine the operation. If so, it is a hidden default, and it still fails. A missing amount read as zero fails the test. An existing resource returned although its settings differ from the ones requested fails the test; the create-if-absent flag on most clients returns the existing object without comparing anything, so the code checks the settings that matter.

Redefine only the case you mean. `Path.unlink(missing_ok=True)` defines away one case; `shutil.rmtree(ignore_errors=True)` also swallows permission errors and a full disk, and leaves last run's files in place for this run to reuse.

```python
# Avoid: check-then-act races, and the broad flag hides every failure.
if path.exists():
    shutil.rmtree(path, ignore_errors=True)
path.mkdir()

# Prefer: only "already absent" and "already present" are normal; anything else raises.
with contextlib.suppress(FileNotFoundError):
    shutil.rmtree(path)
path.mkdir(parents=True, exist_ok=True)
```

## 3. Make each unit of work deterministic and safe to rerun

A batch job, a pipeline task, or a partition load is rerun constantly: after a failure, during a backfill, when the logic changes. If a rerun can double-count, depend on when it ran, or leave a half-written output, every rerun is a risk and every failure is a cleanup. This is Beauchemin's functional data engineering, reduced to what affects how a function is written.

- Given the same parameters and inputs, a unit produces the same output. Pass the run date, the partition, and the window in; nothing inside reads the clock or "the latest".
- A unit writes one output and replaces the whole thing: overwrite the partition, upsert on the key, write to a temporary location and swap. Appending is what makes a rerun double-count.
- Run every step on every run. Skipping a step because a previous run "already did it" is where partially updated outputs come from.
- Logic that changes over time is gated on the data's date inside the unit, so a backfill reproduces the rules of the period.
- A unit that reads its own previous output needs a stated reason; it serializes backfills and makes the output depend on history.

**Avoid**

```python
def load_invoice_lines(fetch_page, warehouse) -> None:
    day = date.today() - timedelta(days=1)                 # which day depends on when this runs
    warehouse.append("invoice_lines", fetch_all(fetch_page))   # a retry writes the rows twice
```

**Prefer**

```python
def load_invoice_lines(day: date, fetch_page, warehouse) -> None:
    lines = fetch_all(fetch_page)
    warehouse.replace_partition("invoice_lines", day, [line.row() for line in lines])
# Rerun it ten times for the same day and the partition holds one copy.
```

Idempotency is also what makes principle 2 affordable. "Let everything else fail the unit of work" is safe advice only because the unit can be run again.

## 4. Reuse existing code before writing new

Two ways to do one thing make every later reader work out which is right and whether the difference is intended. When something close exists, extend it and update its callers in the same change. When a change replaces something, delete the old version in the same change. If the existing pattern is wrong, fix it everywhere in a separate change rather than diverging in one place.

Similar-looking code is not yet reuse, though. Share code when callers depend on the same concept and would change for the same reason. A function with one user can stay beside that user until a second appears.

## 5. Optimize for the reader

Code is read far more often than it is written, and a reader holds only a few things in mind at once. Code that must be understood together should sit together, and nothing should make the reader stop to puzzle.

**Names.** Prefer a better name or an explanatory variable to a comment. Use one term per concept: before naming something, search for the word the code already uses for it, because a different word tells the reader it is a different thing. Replace words that could name anything (`data`, `info`, `item`, `handle`, `process`, `manager`) with the thing they stand for. Name the contents, not the type: `users`, not `users_map`. If a function or type cannot be described in one sentence, it does more than one thing.

**Flow.** Name flags for what is enabled (`validate`, not `skip_validation`) and put the positive branch first. Aim for two levels of nesting; guard clauses and early returns flatten most code. Declare a variable where it is first needed, not at the top. Steps that happen in order are written in order, as statements; a pipeline abstraction or a chain of callbacks earns its place only for concurrency, distribution, or stages chosen at run time.

**Depth over decomposition.** A function earns its place by hiding real complexity behind a simpler interface. A shallow helper, whose call teaches as much as its body, costs a jump, a name, and a contract to keep accurate, and buys nothing. Extract when the piece makes sense on its own: parsing, retries, a business rule, resource handling. Inline a one-caller helper that only renames a construction or a setup step. Long, flat, sequential code is fine; splitting a straight workflow into one-line helpers hides the order and makes it possible to call a step out of sequence. This is where Carmack ("inline it") and the small-functions school both have a point, and the resolution is depth: neither "functions should be small" nor "inline everything called once" is the rule.

**Comments.** A comment says what the code cannot: a business reason, an external constraint, an invariant, a unit, a tradeoff, or why the obvious approach is wrong. It describes the code as it is; history belongs in commit messages, so no "now", "no longer", or phrasing borrowed from the conversation that produced the change. Formatters settle layout; do not fight them.

**Avoid**

```python
def export(d, skip_validation=False):
    # Step 1: get the rows
    rows = fetch_rows(d)
    # Step 2: validate
    if not skip_validation:
        validate(rows)
    # Step 3: convert and sum
    out = {}
    for r in rows:
        if r["status"] != "TEST":
            if r["account"] in out:
                out[r["account"]] += r["amount_micros"] / 1000000
            else:
                out[r["account"]] = r["amount_micros"] / 1000000
    upload(f"spend/{d}.json", out)
```

**Prefer**

```python
MICROS_PER_UNIT = 1_000_000


def export_spend(report_date: date, *, validate: bool = True) -> None:
    rows = fetch_rows(report_date)
    if validate:
        validate_rows(rows)
    upload(f"spend/{report_date}.json", spend_by_account(rows))


def spend_by_account(rows: Sequence[Row]) -> dict[str, float]:
    spend = defaultdict(float)
    for row in rows:
        if row.status != "TEST":
            spend[row.account] += row.amount_micros / MICROS_PER_UNIT
    return spend
```

## 6. Test behavior through the real code

Mock only the effects principle 1 moved to the shell; run everything else for real. Test through the public interface, and test a private function directly only when its public caller would bury the rule in unrelated setup. Never widen visibility (export a name, drop an underscore) just so a test can reach something.

Fakes and fixtures copy the real responses: field names, types, nullability, nesting. A `MagicMock` has none of those, so a test built on one passes against the wrong shape. Assert on returned values and written data; assert that a call happened only when the call is the behavior, such as sending a request. Before keeping a test, ask whether it would still pass if the code were wrong.

The words matter: a fake is a working stand-in with shortcuts (an in-memory store), a stub returns canned answers, a spy records calls, a mock asserts on calls. Prefer them in that order.

**Avoid**

```python
def test_send_reminders(mocker):
    billing = mocker.MagicMock()
    billing.list_open.return_value = [mocker.MagicMock()]   # no real fields or types
    mail = mocker.MagicMock()
    send_reminders("c1", date(2026, 3, 1), billing, mail)
    mail.send.assert_called()      # passes whether or not the invoice was overdue
```

**Prefer**

```python
def test_overdue_invoices_excludes_those_inside_grace():
    today = date(2026, 3, 31)
    inside = make_invoice(due_on=today - timedelta(days=GRACE_DAYS - 1))
    outside = make_invoice(due_on=today - timedelta(days=GRACE_DAYS + 1))

    assert overdue_invoices([inside, outside], today) == [outside]
```

## 7. Test every relevant path

The happy path, then every branch. Both settings of every option the change touches. Each failure the code handles, asserting the specific error promised. Edge cases that apply, parametrized: empty, one, many, missing, null, non-ASCII, and for date logic a daylight-saving transition. A regression test with every bug fix, written to fail before the fix. And at least one test at production shape: a fixture with three rows passes checks that fail at three thousand.

## 8. Make invalid states hard to build

Validity checked once at construction is validity every later line can rely on; validity checked by every consumer is validity one of them forgets. One type per validity contract; validate when constructing; never let a half-built value escape. When an operation has distinct outcomes, return distinct types (a selection or a refusal) rather than one type with optional fields and a mode flag. Decode at input, encode at output, and hold the decoded value in between.

Use a domain type when it prevents an invalid combination or removes repeated validation; do not wrap a value only to label where it came from. A bare primitive says the value is unconstrained, which is sometimes exactly right.

**Avoid**

```python
@dataclass
class Resolution:
    model: str | None = None
    refused: bool = False
    reason: str = ""
# Every consumer checks `refused` and reads `model` anyway; one forgets.
```

**Prefer**

```python
@dataclass(frozen=True)
class Selection:
    model: ModelInfo


@dataclass(frozen=True)
class Refusal:
    reason: str


def resolve(request: Request, catalog: Catalog) -> Selection | Refusal: ...
# The caller must branch on the type; there is no invalid combination to construct.
```

## 9. Constrain mutation and shared state

Total immutability is the wrong goal in an imperative language; knowing what is mutated, by whom, and when is the right one. Give mutable state one owner and give collaborators the narrowest operation they need. Prefer returning new values, and offer the value-returning form (`normalized()`) before the self-mutating one. Local mutation the caller cannot see is fine; copying a large structure to avoid it is not required. Make a state change in one place at a known time: one check in one place beats the same check at twenty call sites.

## 10. Keep dependencies pointing one way

Arrange modules so dependencies form layers with no cycles. Each module is then understandable, and testable, with only the modules beneath it, and a fake for a module can be built from the fakes of the modules it uses. When a cycle appears, find the exact names involved and fix it: move the code to the module it belongs in; extract the shared piece into a lower module; add a higher module that composes both; introduce a small interface; copy, as a last resort with a stated reason. Where the repository checks this mechanically (import-linter in Python, the compiler in Go), keep the configuration current.

## 11. Python specifics

**Data, functions, and classes.** The default shape is a frozen dataclass or pydantic model plus module-level functions. A method belongs on a type when it reads the instance's state and callers would call it on the instance; a pure method on a frozen type is fine. A class with mutable state is for state several operations must share and change together (a cache with its refresh schedule, a worker with its thread), a resource lifetime, or a framework contract. A class that holds collaborators is shell, and each method is a short sequence of effects; the test for a method is simple: if it reads nothing from `self`, it is a function; if it reads only settings, it is a function that takes those values; if it chooses between effects, the choice is a pure function that returns what to do.

**Avoid**

```python
class TurnRunner:
    def __init__(self, settings, store, poster): ...

    def run(self, turn):
        case = self._load(turn)
        outcome = self._observe(self._client.stream(turn))
        self._record(case, outcome)
        if self._should_escalate(outcome):
            self._escalate(case, outcome)

    def _observe(self, messages):          # reads nothing from self
        ...
    def _should_escalate(self, outcome):   # reads one setting from self
        return outcome.stop_reason != "completed" or outcome.cost > self._settings.max_cost
```

**Prefer**

```python
def observe(messages: Iterable[Message]) -> Outcome: ...                 # pure, tested with values


def should_escalate(outcome: Outcome, max_cost: float) -> bool:          # pure, the setting is a parameter
    return outcome.stop_reason != "completed" or outcome.cost > max_cost


class TurnRunner:                                                         # shell: holds the collaborators
    def run(self, turn: Turn) -> None:
        case = load_case(self._store, turn)
        outcome = observe(self._client.stream(turn))
        record_turn(self._store, case, outcome)
        if should_escalate(outcome, self._settings.max_cost):
            escalate(self._poster, case, outcome)
```

**Exceptions.** Catch the narrowest type the layer can handle. `except Exception` lives in exactly one place: the outermost boundary of a unit of work that must outlive one failure, with a comment, and never where the framework already isolates the unit. Keep `try` blocks narrow. Preserve causes with `raise ... from error`. Log a failure once, where it is handled, with a `%`-style template so the message is formatted only when emitted.

**Pipelines.** The task function takes its partition or window from the framework and passes it down; nothing below reads the clock or the framework context. Write with a replace operation on the partition or key. Retry policy lives on the task, where idempotency is known.

**Tests.** `pytest` with parametrized cases and readable ids. `pytest.raises` names the specific exception. When a mock is unavoidable and the repository uses `pytest-mock`, use the `mocker` fixture, patch where the name is looked up, and never as a context manager or decorator. A fake for an external service is a small class with the real method names and a failure mode.

## 12. Go specifics

Go has strong, shared idioms; write the code an experienced Go reviewer expects, and where a principle and an official Go rule disagree, the Go rule wins. The skill's `go.md` restates the official sources with tags; a few house choices deserve explanation here.

**Errors are values.** Return errors for ordinary failures; panic only for programmer errors. Add context as you return (`fmt.Errorf("load customer %q: %w", id, err)`), inspect with `errors.Is` and `errors.As`, never compare strings. Handle an error once: log it or return it, not both. When a run of calls would each need the same check and the caller needs only all-or-nothing, let a type keep the first error and report it once, as `bufio.Writer` does; this is the Go form of defining errors out of existence.

```go
// Avoid: four checks, and the caller cannot see the shape of the report for the plumbing.
if _, err := fmt.Fprintln(w, header); err != nil { return err }
for _, r := range rows {
	if _, err := fmt.Fprintf(w, "%s\t%d\n", r.Name, r.Count); err != nil { return err }
}

// Prefer: bufio.Writer keeps the first error; Flush reports it.
bw := bufio.NewWriter(w)
fmt.Fprintln(bw, header)
for _, r := range rows {
	fmt.Fprintf(bw, "%s\t%d\n", r.Name, r.Count)
}
if err := bw.Flush(); err != nil {
	return fmt.Errorf("write report: %w", err)
}
```

One caution: Cheney's `errWriter` returns `n, nil` from the failing write, which breaks the `io.Writer` contract. A type that implements `io.Writer` returns a non-nil error from every short write.

**Sequences.** Return a slice when the result fits in memory. Return an iterator (`iter.Seq`, `iter.Seq2`) when the sequence is large, lazy, or callers may stop early. Never return a channel to deliver a sequence: it cannot report a failure partway through, and the caller must drain it or leak the goroutine. For a paginated remote result that can fail, the house rule is `iter.Seq2[T, error]` with the contract Google's client libraries use: a non-nil error is the last pair yielded. This is a convention, not an official endorsement; the Go team deliberately left it out of the `iter` docs, and a caller who ranges with one variable drops the error silently, so review checks for it.

```go
for event, err := range auditexport.Events(ctx, client, window) {
	if err != nil {
		return fmt.Errorf("list events: %w", err)
	}
	if err := enc.Encode(event); err != nil {
		return err
	}
}
```

**Tests.** Tests go in `package foo_test` by default and exercise the exported API; a private function that needs a direct test gets `foo_internal_test.go`, so the exception is visible as its own file. New repositories use `testify` (`require` when the test cannot continue, `assert` otherwise, `cmp.Diff` for structs, no `suite`); this departs from Go's Test Comments and is an owner choice shared by most large Go projects. Table-driven tests with `t.Run`, cases named for the condition, failure messages in the form `Parse(%q) = %v, want %v`.

**Concurrency.** Prefer synchronous functions and let the caller add concurrency. Every goroutine has an owner, a way to stop, and a way to report its error; `errgroup` and `context` are the tools. Buffers of zero or one unless the protocol fixes a size.

## Further reading

- Gary Bernhardt, *Functional Core, Imperative Shell*.
- John Carmack, *Functional Programming in C++* (2012) and the inlined-code email (2007, 2014 preface).
- Maxime Beauchemin, *Functional Data Engineering*.
- Jeremy Bowers, *Functional Programming Lessons in Imperative Code* and *Layered Design in Go*.
- John Ousterhout, *A Philosophy of Software Design*.
- Rob Pike, *Errors are values*; Dave Cheney, *Practical Go*.
- Peter Hilton, *How to name things*; Loup Vaillant, *The Source of Readability*.
- Google Testing Blog, *Increase Test Fidelity by Avoiding Mocks*.
