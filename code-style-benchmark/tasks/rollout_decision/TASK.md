# Task: rollout decision

Write `rollout.py` and `test_rollout.py`.

A platform team rolls features out gradually. Write the code that decides whether a given account sees a feature.

Facts:

- A feature's rollout is configured as: `percentage` (0 to 100), an `allowlist` of account ids that always see it, a `blocklist` of account ids that never see it, an optional `kill_switch` flag that turns the feature off for everyone, and an optional `starts_at` (timezone-aware datetime) before which nobody sees it.
- The percentage bucket must be stable: the same account gets the same answer for the same feature every time, across processes and machines, and changing the percentage from 20 to 30 must keep every account that was in at 20. Use a hash of `f"{feature}:{account_id}"`.
- Callers need to know *why* an account is in or out, because support staff read the reason: kill switch, not yet started, blocked, allowed, in bucket, out of bucket.
- The decision will run in a request handler hundreds of times per second, and in a batch job that evaluates every account once a night.

Required interface (the tests import these names):

```python
class Rollout(...)      # the configuration above; construct with keyword arguments
def decide(feature: str, account_id: str, rollout: Rollout, now: datetime) -> Enabled | Disabled
```

`Enabled` and `Disabled` each carry a `reason` field whose value is one of the strings `"kill_switch"`, `"not_started"`, `"blocklisted"`, `"allowlisted"`, `"in_bucket"`, `"out_of_bucket"`. A kill switch wins over everything; `starts_at` wins over the lists; the blocklist wins over the allowlist; the lists win over the bucket.

pydantic v2 and pytest are available but not required. Run `pytest -q` and `ruff check .` in your output directory and fix what they report. Write NOTES.md under 150 words.
