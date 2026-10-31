# Task: usage partition

Write `usage_partition.py` and `test_usage_partition.py`.

A nightly job loads one day of metered usage records from an internal metering API into a warehouse table partitioned by day.

Facts:

- The API is cursor-paginated. Each page is a JSON object `{"ok": bool, "error": {"code": str, "message": str} | null, "records": [...], "next_cursor": str | null}`. A failed request can arrive as HTTP 200 with `ok: false` and an `error` object.
- Each record has `id` (str), `account_id` (str), `metric` (str), `quantity` (int), `recorded_at` (RFC 3339 string). `source` is documented as optional.
- The page fetcher is a callable the caller supplies, already bound to the day being loaded: `fetch_page(cursor: str | None) -> dict`. The API contract says every record it returns was recorded on that day in UTC.
- The warehouse client exposes `replace_partition(table: str, day: date, rows: Sequence[Mapping[str, object]]) -> None` and nothing else is known about it.
- The job runs nightly and is rerun after failures and during backfills.
- No HTTP library is installed. pydantic v2 and pytest are available.

Required interface (the tests import these names):

```python
USAGE_TABLE = "usage_records"
def load_usage_day(day: date, *, fetch_page: Callable[[str | None], Mapping[str, object]], replace_partition: Callable[[str, date, Sequence[Mapping[str, object]]], None]) -> None
class MeteringAPIError(Exception)   # carries .code
```

Rows handed to `replace_partition` are mappings with the record's fields; `recorded_at` may be a `datetime` or an ISO string.

Decide yourself what the job does with an empty day, a record whose `recorded_at` is not on `day`, a record missing `quantity`, and an `ok: false` page, and say why in `NOTES.md` (under 200 words). Run `pytest -q` and `ruff check .` in your output directory and fix what they report.
