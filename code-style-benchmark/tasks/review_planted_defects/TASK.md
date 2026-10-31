# Task: review a change

Review the diff in `change.diff` in your output directory as if a teammate had opened it as a pull request. The file being changed is `queue_consumer.py`, a worker that reads messages from a queue and records them in a database; the current version before the change is in `queue_consumer_before.py` for context.

Write `REVIEW.md`: your findings, each with the location, a severity (blocker, major, moderate, minor), whether the change introduced it or it was already there, the exact fix, and the one-sentence reason. Order them with the most important first. Do not rewrite the file; review it.
