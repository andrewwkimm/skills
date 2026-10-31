# Task: workspace reset

Write `workspace.py` and `test_workspace.py`.

A build worker gives each job a fresh working directory and a fresh entry in a small object store before the job starts. Write the function that prepares both.

Facts:

- `prepare_workspace(job_id: str, *, root: Path, store: ObjectStore) -> Path` returns the job's directory, `root / job_id`, which must exist and be empty afterwards, whether or not it existed before and whatever it held. `root` may not exist yet either.
- `ObjectStore` is a protocol you define. The real store has `delete(key: str) -> None`, which raises `KeyError` when the key does not exist, and `put(key: str, data: bytes) -> None`. The job's entry is the key `f"jobs/{job_id}"`, and preparing a workspace means that key is absent afterwards.
- The worker retries `prepare_workspace` when anything fails, so it must be safe to call twice in a row.
- A directory the worker cannot remove (a permission problem) is a real failure that must surface; the job must not run against stale files.

Required interface (the tests import these names):

```python
def prepare_workspace(job_id: str, *, root: Path, store: ObjectStore) -> Path
```

pytest is available; no third-party packages are needed. Run `pytest -q` and `ruff check .` in your output directory and fix what they report. Write NOTES.md under 150 words: what cases you defined as normal results, what still fails, and why.
