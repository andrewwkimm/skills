# Decision log

Settled questions, with the reasoning and the option that lost. Read this before proposing a change to the skill or when a user questions a rule. An entry is reopened only with new evidence of one of three kinds: a factual error (cite the primary source), a contradiction between rules, or an observed worse outcome you can describe. A user's doubt alone is answered with the recorded reasoning; the owner may override any entry, and the override is recorded here as owner preference.

Source tiers, highest first: language docs and toolchain behavior; official or semi-official style guides (Effective Go, Code Review Comments, Test Comments, Google Go and Python guides, Uber, PEP 8); named practitioners; exemplar repositories; owner preference recorded as a house rule.

## Shape of the skill

**One skill, shared principles, per-language files.** The principles are identical across languages; only the mechanics differ. Two self-contained skills would drift. Rejected: splitting into `go-code-style` and `python-code-style`. Owner confirmed 2026-10-31.

**Rules carry reasons; no fixed word budget.** Length is cut by removing duplicates and rules that change no output, never by stripping the clause that says why. The reason is what lets an agent apply a rule to a case it does not name, and what lets it recognize when the rule does not apply. Rejected: compressing to shorthand for token count.

**Few code snippets, generic domain, ten lines or fewer.** Snippets appear only for patterns that prose alone failed to correct in practice (chained defaults, workflow-as-class, the iterator error contract). Longer examples live in the prose companion, not in the skill, because an agent copies what the skill shows, including teaching comments. Snippets never come from a conversation or a team document.

**Decision log outside the per-task load.** This file is read only when changing the skill or answering a challenge, so it costs nothing on ordinary tasks. Rejected: inlining reasoning into every rule (already done in one clause), or a log loaded every session.

**Pipelines section lives in principles.** Deterministic, rerun-safe units of work are language-neutral and shape how a function is written (parameters in, replace-write out), so they belong beside failure handling rather than in `python.md` or the layout skills. Source: Beauchemin. Owner confirmed 2026-10-31.

**What the benchmark can and cannot show, 2026-10-31.** Seventeen runs over three small tasks and a negative control, with no skill, the previous skill, and this one, all scored 100% on hidden tests with no pattern violations (one `pytest.raises(Exception)` in a no-skill test file aside), while the planted fixture scored 6 of 9 with nine violations. The benchmark separates good from bad; on tasks of that size it does not separate the skill from the model's own prior, which already parses at the boundary, replaces the partition once, and injects the clock. Consequences: a rule is not cut because the benchmark shows no difference on small tasks; the skill's value is expected on large modules, ambiguous contracts, and feature work inside smelly code, so new benchmark tasks are built there; a proposed rule still needs the benchmark to show it does no harm (the negative control) before it is added.

**Settling procedure for contested rules.** A rule is decided by the highest source tier that speaks to it; when no tier above owner preference speaks, the owner's preference is recorded as a house rule with its reason. A later session does not reverse a house rule because it finds the losing option defensible; defensible is the normal state of a contested question.

## Principles

**Fail where the data enters, and define errors out of existence, are one rule with one test.** The test: could any caller now receive a plausible but wrong value without knowing? If not, redefine the operation so the case is a normal result; if so, fail at the boundary. Ousterhout's own examples include clamping an out-of-range index, which the test rejects: the index was the caller's bug and clamping hides it. Rejected: treating the two as a conflict and choosing one.

**Inline (Carmack, Vaillant) versus extract (Cheney §3.2.2) resolves to depth.** Both sides argue from locality. The rule: extract when the piece hides real work and can be read without its caller; inline when the call teaches as much as the body. A step several places must run is made pure and called from one place. Neither "functions should be small" nor "inline everything called once" is adopted as a rule.

**Functional at the medium scale (Bowers), not the micro scale.** Comprehension chains, `map`/`filter` rewrites, and pipeline libraries for plain sequencing are not adopted and are discouraged. Purifiable components, explicit inputs, and valid-by-construction values are the rules.

**Idempotent, overwrite-not-append units of work (Beauchemin).** Adopted as principle 3. Beauchemin's warehouse-modeling material (dimension snapshots, processing-time partitioning, parameter tables) is not adopted; it is modeling, not code style. Carmack's "do the work every time, then inhibit" is adopted only in the form "run every step every run"; his power-and-thermal caveat does not apply to batch pipelines.

**Vaillant's layout rules are dropped where a formatter decides.** `gofmt` and `ruff format` settle vertical density and statement grouping. His structural rules (declare near use, inline a once-used variable whose name adds nothing, deep modules, no globals, composition) are adopted.

**Comments: minimal, not banned.** Self-documenting code first; a comment for what code cannot say. Cheney's "describe contents, not purpose" is adopted for constants and variables. "Write the comment before the function" is not adopted as a rule; the one-sentence test covers it.

## Python

**Structs plus functions by default; classes for shared mutable state, resource lifetime, or framework contract.** Sources agree: Google 2.17 (no `staticmethod`), Diederich ("two methods and one is `__init__`"), Hettinger ("you have to create an instance just to call a function"), Hynek ("a function is all you need"), Cannon. The mechanical test for a method on a shell class: reads nothing from `self`, it is a function; reads only settings, it takes them as parameters; chooses between effects, the choice is a pure function. Pure methods on a frozen data type are allowed; that is the Go shape. Rejected: forbidding behavior on data models; forbidding private pydantic models per API (they are the boundary rule working). Owner confirmed 2026-10-31.

**Name imports allowed.** PEP 8 permits `from x import Name`; Google's modules-only rule is not adopted. PEP 8 is the higher tier for a Python project. Owner preference agrees.

**Function-level imports need a comment naming the runtime constraint.** Observed outcome, 2026-08-26: unexplained local imports hid runtime constraints and needed unexplained lint suppressions.

**`except Exception` in exactly one place per unit of work.** Google 2.4's isolation point, made stricter than PEP 8: the outermost boundary of a unit that must outlive one failure, with a comment. Not where a framework already isolates the unit.

**Descriptive docstring mood, and docstrings on tests.** House rule, owner preference; departs from PEP 257 and Google. Earlier evidence from the owner's own repositories was circular (written under the guide) and is not the justification. A repository that enables ruff `D401` wins.

**`%`-style logging templates.** Google 3.10.1 and ruff `G004`; the message is formatted only when emitted. Earlier repository counts are not the justification.

**`Any` only for shapes unknown by nature, with a stated reason.** Observed outcome, 2026-08-26: SDK types were cast to `Any` although the SDK published them.

**Define-away flags: use the library flag for exactly the case, never an everything flag.** `missing_ok`, `exist_ok`, `not_found_ok` are adopted; `shutil.rmtree(ignore_errors=True)` is forbidden because it also swallows permission and I/O errors. A create-if-absent flag returns the existing resource without comparing settings (verified in `google-cloud-bigquery` 3.46.2 `create_dataset`), so settings that matter are checked.

## Go

**External tests by default, `foo_internal_test.go` for exceptions.** `testing` permits both; Cheney prefers internal tests, Google uses `foo_test` only for examples. Chosen because unit tests lock in the exported API (Cheney §8.1 himself), and because an agent uses any permission it is given: in-package tests reach private state whenever that is easier, and the exception then has no visible marker. A separate file makes the exception show in a diff. Rejected: internal by default. Departs from Cheney.

**Testify in new repositories, with guardrails.** Test Comments and Google forbid assertion libraries; Uber's own examples use testify; 7 of 9 surveyed large projects (tailscale, litestream, prometheus, grafana, etcd, cockroach, kubernetes) depend on it directly, golang/tools and terraform do not. Owner preference, recorded as a house rule with the guardrails: `require` versus `assert` by whether the test can continue, `cmp.Diff` for structs, no `suite`, `testifylint`. A repository tested with the standard library alone stays that way. Departs from TC and Google.

**`iter.Seq2[T, error]` for paginated or streamed remote results.** The Go team removed the value-error convention from the `iter` docs on purpose and has not issued guidance (golang/go#71901); Google's own client libraries (`All()` on every generated iterator, via `gax-go/v2/iterator.RangeAdapter`), Stripe, and go-github chose this shape with the contract "a non-nil error is the last pair; the iterator stops". Alternatives: `Scan`/`Err` (the Go team acknowledges people forget `Err`), callbacks (cannot stop early cleanly), channels (rejected by CRC). Caveat recorded honestly: a caller who ranges with one variable drops the error silently, so review checks it; the compile-time check applies only when the caller declares `err`. Contested, not endorsed; a repository with another shape wins. Reopen if the Go team publishes guidance.

**No package-internal panic/recover pattern.** Departs from Effective Go, the Go wiki, and Google. Errors returned from each level are the shape the rest of the guide (wrapping, `errors.Is`) relies on; `recover` only at a boundary that restores an invariant.

**`log.Fatal` only in `main`, at most once.** Uber. Cheney's "avoid entirely" is not adopted because a `run() error` plus one `log.Fatal` in `main` is the idiom.

**Doc comment on interface-implementing methods.** CRC and Google require a comment on every exported name; Cheney would omit it for methods that implement an interface. The higher tier wins; the fix for a contentless comment is a real one-line comment, not deletion.

**Cheney's superseded advice is not adopted.** Behavior assertions by hand-written interface (use `errors.As`), "do not export error types" (the standard library does), `first T, rest ...T` signatures (uncommon, awkward with a slice in hand), hand-rolled `done`/`stop` channels (use `context` and `errgroup`), `ioutil`.

**Wall-clock times built with `time.Date`, tested on a transition date.** Observed outcome, 2026-10-20: a deadline computed by adding an offset to local midnight was an hour off on both daylight-saving transition dates; the test used a non-transition date and passed.

**No in-band nil for "nothing happened".** Observed outcome, 2026-10-20: a parser returned nil for both an empty date and an unparseable one, and a downstream classifier treated nil as a state.

**Instance APIs over package-level library state.** Observed outcome, 2026-10-20: calls that set a migration library's package state raced under `t.Parallel`; the library had an instance API.

**Fakes carry a failure mode.** Observed outcome, 2026-10-20: a documented "one failing source does not stop the others" path had no test because no fake could fail.

## Not adopted, with reasons

- Uber's `_` prefix on unexported globals, 99-column limit, `go.uber.org/atomic`: superseded or against CRC.
- Google Python's modules-only imports: PEP 8 is the higher tier for Python.
- "Functions should be small" and "inline everything called once": both replaced by depth over decomposition.
- Bowers's ranking of one-type packages above interfaces for cycle breaking: layout, not code style; the layout skills decide.
- Hilton's "no abbreviations except id" for Go: conflicts with `ctx`, `r`, `w`, `i`.
- Hilton's habits advice and Orwell's rules: covered by the writing skill, not actionable in code.
- Cheney's channel axioms, `var` versus `:=` as a full section, TODO(user) format: language facts or repository conventions. The `var`/`:=` meaning is kept as one line.
- Repository counts from the owner's own code as tiebreakers: circular when the code was written under an earlier version of this guide. Decisions that once rested on them (testify, logging templates, test docstrings, name imports) have been re-justified above or marked as owner preference.
