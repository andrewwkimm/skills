# Task: disk usage script

Write `du.py`, a single-file script a platform engineer runs by hand.

It takes one argument, a directory, and prints the total size in bytes of every regular file under it, followed by the five largest files with their sizes, largest first. Symlinks are not followed. A missing or unreadable directory prints an error to stderr and exits 1.

Required interface (the tests import this name):

```python
def summarize(root: Path) -> tuple[int, list[tuple[Path, int]]]   # (total_bytes, five largest as (path, size))
```

Only the standard library. Add a `test_du.py` with whatever tests you consider worth having for a script this size. Run `pytest -q` and `ruff check .` in your output directory. Write NOTES.md under 100 words.
