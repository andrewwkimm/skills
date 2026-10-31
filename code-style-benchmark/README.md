# Code-style benchmark

Measures whether a version of the `code-style` skill changes the code an agent writes, and in which direction. It lives beside the skill, is run when the skill changes, and is never loaded during an ordinary task.

## What it measures

Each task is a small, self-contained piece of backend or platform work with an exact interface. The agent sees `TASK.md` and the skill, nothing else. Three things are then scored:

1. **Hidden tests.** Behavior the agent did not see: the error body that arrives as HTTP 200, the rerun, the permission error that must surface, the record that contradicts a contract. These are the outcomes the skill's rules exist to produce, so a rule that works shows up here.
2. **Pattern checks.** An AST pass over the agent's files for patterns the skill names: `.get(key, default)` at the point of use, `except Exception`, a method that never reads `self`, `MagicMock`, `ignore_errors=True`, a clock read inside logic, a mutable default argument. Each task's `rubric.json` lists which codes count against it.
3. **A rubric**, for the review task only, graded by a person or a model: planted defects found, pre-existing noise correctly left alone, scope kept to a review.

Alongside: the agent's own tests (do they pass), source line count, and the agent's `NOTES.md`, which shows what it believed it was doing.

## Tasks

| Task | Exercises | Negative control? |
| --- | --- | --- |
| `webhook_events` | Boundary parsing, distinct outcome types, an unknown case defined as a normal result, no hidden defaults | |
| `usage_partition` | Rerun-safe replace write, fail on an error body, fail on a record that contradicts the fetcher's contract, empty day as a result | |
| `workspace_reset` | Define errors out of existence without swallowing: absent is normal, permission error still fails, safe to call twice | |
| `rollout_decision` | Pure decision, distinct outcomes with reasons, no clock or randomness inside, stable hashing, validation at construction | |
| `report_job_refactor` | Refactoring a workflow-as-class: nine planted smells, a bug to fix, behavior to keep | |
| `disk_usage_script` | A 40-line script: the rules should *not* fire (no models, no classes, no protocols) | yes |
| `review_planted_defects` | Reviewing a diff: eight planted defects, three pre-existing items that must not be blamed on the change | |

Every task with hidden tests has a `reference/` solution (or, for the refactor, the `fixture/` it starts from). `python run.py --validate` runs the hidden tests against those, so the tests are known to pass a correct answer before they judge an agent. The fixture is expected to fail exactly the three bug-fix tests and trip all nine checks.

## Running it

1. For each task and each skill variant, give a fresh agent the task:
   - Tell it which skill directory to read and that it is the only style guidance.
   - Give it `TASK.md` verbatim, and copy in any files `rubric.json` lists under `copy_into_output` (the refactor fixture; the review's diff and before-file).
   - Point it at an empty output directory: `outputs/<task>/<variant>/<run>/`.
   - Repeat for as many runs as you want to average over. Three per cell is the minimum at which a difference means anything; one run tells you what one agent did.
2. Score: `python run.py --outputs ./outputs --python <venv with pytest and pydantic>`.
3. Read `outputs/report.md`: one row per task and variant with hidden-test pass rate, own-test pass rate, violations per run and which codes, and source size; then per-run detail. Grade the review task by hand against `tasks/review_planted_defects/rubric.md`.

The script never launches agents; the runs are yours to produce however you run agents.

## Reading the results

- A rule is **doing its job** when the variant that carries it passes the hidden test for that behavior more often, or trips its check code less often, by more than the spread between runs of the same variant.
- A rule is **inert** when neither number moves across variants that differ only in that rule. That is the evidence for cutting it; nothing else is.
- The **negative control** catches over-application: a variant whose `disk_usage_script` output grows classes, models, or protocols is applying rules where their reasons do not hold.
- `NOTES.md` explains divergences the numbers cannot: two agents can both pass and still have read a contract differently.

## Adding a task

A task needs: `TASK.md` with an exact interface the hidden tests import; `hidden_tests/` that pass against a `reference/` solution and fail against the mistake they target; `rubric.json`. Keep the domain generic (billing, metering, deployments, queues) and the interface small enough that two correct solutions are easy to compare.

## Limits

Pattern checks are narrow by design and will miss a smell written another way. Hidden tests judge behavior, not readability; the rubric and `NOTES.md` are the only view of that. There is no Go suite yet; the layout mirrors what one would need (`go test` against hidden `_test.go` files, `go vet` plus a small pattern pass).
