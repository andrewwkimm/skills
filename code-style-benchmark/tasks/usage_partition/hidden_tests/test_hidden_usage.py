"""Hidden tests for the usage_partition task."""

from collections.abc import Mapping, Sequence
from datetime import date

import pytest
import usage_partition as up

DAY = date(2026, 4, 2)


def record(**overrides) -> dict:
    base = {
        "id": "r1",
        "account_id": "acct_1",
        "metric": "api_calls",
        "quantity": 10,
        "recorded_at": "2026-04-02T10:00:00Z",
    }
    base.update(overrides)
    return base


class FakeFetcher:
    """Serves pages by cursor and counts calls."""

    def __init__(self, pages: dict[str | None, dict]) -> None:
        self.pages = pages
        self.calls = 0

    def __call__(self, cursor: str | None) -> dict:
        self.calls += 1
        return self.pages[cursor]


class FakeWarehouse:
    def __init__(self) -> None:
        self.writes: list[tuple[str, date, list[dict]]] = []

    def replace_partition(self, table: str, day: date, rows: Sequence[Mapping[str, object]]) -> None:
        self.writes.append((table, day, [dict(r) for r in rows]))


def ok_page(records: list[dict], next_cursor: str | None = None) -> dict:
    return {"ok": True, "error": None, "records": records, "next_cursor": next_cursor}


def test_all_pages_land_in_one_replace() -> None:
    fetch = FakeFetcher({None: ok_page([record(id="r1")], "c2"), "c2": ok_page([record(id="r2"), record(id="r3")])})
    warehouse = FakeWarehouse()

    up.load_usage_day(DAY, fetch_page=fetch, replace_partition=warehouse.replace_partition)

    assert len(warehouse.writes) == 1
    table, day, rows = warehouse.writes[0]
    assert table == up.USAGE_TABLE
    assert day == DAY
    assert [r["id"] for r in rows] == ["r1", "r2", "r3"]
    assert rows[0]["quantity"] == 10


def test_rerun_produces_identical_write() -> None:
    pages = {None: ok_page([record(id="r1")], "c2"), "c2": ok_page([record(id="r2")])}
    first, second = FakeWarehouse(), FakeWarehouse()

    up.load_usage_day(DAY, fetch_page=FakeFetcher(pages), replace_partition=first.replace_partition)
    up.load_usage_day(DAY, fetch_page=FakeFetcher(pages), replace_partition=second.replace_partition)

    assert first.writes == second.writes


def test_empty_day_writes_an_empty_partition() -> None:
    warehouse = FakeWarehouse()

    up.load_usage_day(DAY, fetch_page=FakeFetcher({None: ok_page([])}), replace_partition=warehouse.replace_partition)

    assert warehouse.writes == [(up.USAGE_TABLE, DAY, [])]


def test_error_page_fails_with_the_api_code_and_writes_nothing() -> None:
    fetch = FakeFetcher(
        {
            None: ok_page([record()], "c2"),
            "c2": {
                "ok": False,
                "error": {"code": "rate_limited", "message": "slow down"},
                "records": [],
                "next_cursor": None,
            },
        }
    )
    warehouse = FakeWarehouse()

    with pytest.raises(up.MeteringAPIError) as info:
        up.load_usage_day(DAY, fetch_page=fetch, replace_partition=warehouse.replace_partition)

    assert info.value.code == "rate_limited"
    assert warehouse.writes == []


def test_missing_quantity_fails_and_is_not_read_as_zero() -> None:
    bad = record()
    del bad["quantity"]
    warehouse = FakeWarehouse()

    with pytest.raises(Exception) as info:
        up.load_usage_day(
            DAY, fetch_page=FakeFetcher({None: ok_page([bad])}), replace_partition=warehouse.replace_partition
        )

    assert "quantity" in str(info.value)
    assert warehouse.writes == []


def test_record_off_day_contradicts_the_fetcher_contract_and_fails() -> None:
    off_day = record(id="r_old", recorded_at="2026-04-01T23:59:00Z")
    warehouse = FakeWarehouse()

    with pytest.raises(Exception):
        up.load_usage_day(
            DAY,
            fetch_page=FakeFetcher({None: ok_page([record(), off_day])}),
            replace_partition=warehouse.replace_partition,
        )

    assert warehouse.writes == []


def test_optional_source_is_allowed_absent_and_present() -> None:
    warehouse = FakeWarehouse()
    pages = {None: ok_page([record(id="a"), record(id="b", source="sdk")])}

    up.load_usage_day(DAY, fetch_page=FakeFetcher(pages), replace_partition=warehouse.replace_partition)

    assert [r["id"] for r in warehouse.writes[0][2]] == ["a", "b"]
