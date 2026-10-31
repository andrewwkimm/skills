# Task: report job refactor

Refactor the module `report_job.py` in your output directory (a copy of a real module is placed there for you) and write `test_report_job.py` for it.

Context:

- `ReportJob` is constructed once by the scheduler as `ReportJob(services, fetch_metrics, publish, out_dir, threshold=...)` and `run()` is called nightly. Keep that constructor signature working and keep `run()` returning the report document; you may add keyword-only parameters with defaults to the constructor.
- The team has confirmed one bug: a metrics payload with no `counts`, or with `counts` missing `requests` or `errors`, currently produces a row with zero requests and a 0.0 error rate, which hides a broken metrics source. That case must fail instead, with an error that names the missing field. Everything else about the output for well-formed payloads must stay the same (same keys, same values, same order of rows).
- `_format_row` has no callers anywhere in the codebase.

Improve the module for maintainability under the skill you were given, and write tests that would catch a regression in the report's content. pytest is available; pydantic v2 is available if you want it. Run `pytest -q` and `ruff check .` in your output directory and fix what they report. Write NOTES.md under 200 words: what you changed, what you left, and why.
