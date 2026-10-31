# Rubric: review_planted_defects

Grade `REVIEW.md` by hand or with a model given this file. Score = planted defects found (one point each, half a point if found but mis-ranked by two severity levels or more) minus false positives on pre-existing lines flagged as introduced (one point each). A review that blocks on a pre-existing finding fails the task.

## Planted by the change (should be found, severity in parentheses)

1. `except Exception` around `model_validate` that logs "Skipping malformed message" and returns `False` (blocker). Swallows every failure including programmer errors, loses the message content, and `False` also means "queue empty", so `main` stops consuming on the first bad message. Fix: catch `ValidationError` only, include the message id or body in the log, and distinguish "skipped" from "empty" (a distinct return type or an exception at the unit-of-work boundary).
2. Mutable default `seen: list[str] = []` (blocker). Shared across calls and tests; grows forever; dedup state hidden in a default. Fix: an explicit owner for seen ids (a set passed in, or a store that upserts on id).
3. Deduplication by in-memory list instead of an idempotent record (major). A restart forgets `seen`; the queue redelivers; rows duplicate. Fix: make `record` an upsert on `event.id`, which also removes the `seen` parameter.
4. `datetime.now(UTC)` inside `consume_one` (major). The audit time is a hidden input; tests cannot pin it, and it differs from `deployed_at` with no stated reason. Fix: pass `now` in, or use `event.deployed_at` if the audit means the deployment time.
5. `region: str = "us-east-1"` default on a boundary model (major). A message missing `region` is recorded as us-east-1 and nothing alerts; a plausible but wrong value. Fix: required field, or `str | None` with the absence documented, decided with the producer.
6. f-string in `logger.info` (minor). Formatted even when the level is off; the module's other log call uses a `%` template.
7. Test inside the production module, built on `MagicMock` with `record.assert_called_once()` (major). Asserts a call rather than the recorded content; passes if the wrong payload is recorded; lives in the wrong file. Fix: a test file, a fake `record` that stores what it was given, assert on the stored row.
8. `Append` type alias identical to `Record` (minor). Two names for one concept; the reader assumes they differ.

## Pre-existing, must NOT be reported as introduced (and must not block)

- `import json` unused (minor, pre-existing).
- `received_before` has no callers (minor, pre-existing).
- `main` has no stop condition beyond an empty queue (design, pre-existing).

## Scope check

A review that proposes rewriting the module, adding a class, or introducing a framework scores zero for scope: the task was a review.
