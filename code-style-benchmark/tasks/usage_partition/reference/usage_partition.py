"""Loads one day of metered usage records into a warehouse partition."""

from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, date

from pydantic import AwareDatetime, BaseModel

USAGE_TABLE = "usage_records"

FetchPage = Callable[[str | None], Mapping[str, object]]
ReplacePartition = Callable[[str, date, Sequence[Mapping[str, object]]], None]


class MeteringAPIError(Exception):
    """The metering API reported a failed request in a page body."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"Metering API error {code!r}: {message}")
        self.code = code


class RecordOffDayError(ValueError):
    """The API returned a record outside the day it promised to serve."""


class UsageRecord(BaseModel, frozen=True):
    id: str
    account_id: str
    metric: str
    quantity: int
    recorded_at: AwareDatetime
    source: str | None = None  # Absent when the meter did not report one.


class PageError(BaseModel, frozen=True):
    code: str
    message: str


class Page(BaseModel, frozen=True):
    ok: bool
    error: PageError | None
    records: list[UsageRecord]
    next_cursor: str | None


def load_usage_day(day: date, *, fetch_page: FetchPage, replace_partition: ReplacePartition) -> None:
    """Replaces the ``day`` partition of the usage table with what the API serves for it.

    Raises:
        MeteringAPIError: a page reported ``ok: false``.
        pydantic.ValidationError: a page or record did not match the documented shape.
        RecordOffDayError: a record was recorded outside ``day``, which the API promises not to return.
    """
    records = fetch_usage_records(fetch_page)
    check_recorded_on(records, day)
    replace_partition(USAGE_TABLE, day, [record.model_dump() for record in records])


def fetch_usage_records(fetch_page: FetchPage) -> list[UsageRecord]:
    """Follows cursors to the end and returns every record."""
    records: list[UsageRecord] = []
    cursor: str | None = None
    while True:
        page = Page.model_validate(fetch_page(cursor))
        if not page.ok:
            error = page.error or PageError(code="unknown", message="ok was false with no error object")
            raise MeteringAPIError(error.code, error.message)
        records.extend(page.records)
        if page.next_cursor is None:
            return records
        cursor = page.next_cursor


def check_recorded_on(records: Sequence[UsageRecord], day: date) -> None:
    """Raises when a record contradicts the fetcher's promise to serve only ``day``."""
    for record in records:
        recorded_on = record.recorded_at.astimezone(UTC).date()
        if recorded_on != day:
            raise RecordOffDayError(f"Record {record.id!r} was recorded on {recorded_on}, not {day}.")
