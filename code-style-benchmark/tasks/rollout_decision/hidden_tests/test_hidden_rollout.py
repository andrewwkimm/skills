"""Hidden tests for the rollout_decision task."""

from datetime import UTC, datetime, timedelta

import pytest
import rollout as ro

NOW = datetime(2026, 5, 1, 12, tzinfo=UTC)
ACCOUNTS = [f"acct_{i}" for i in range(400)]


def make(**kwargs) -> ro.Rollout:
    base = {"percentage": 50, "allowlist": frozenset(), "blocklist": frozenset()}
    base.update(kwargs)
    return ro.Rollout(**base)


def test_kill_switch_wins_over_allowlist() -> None:
    decision = ro.decide("f", "acct_1", make(kill_switch=True, allowlist={"acct_1"}), NOW)

    assert isinstance(decision, ro.Disabled) and decision.reason == "kill_switch"


def test_not_started_wins_over_allowlist() -> None:
    decision = ro.decide("f", "acct_1", make(allowlist={"acct_1"}, starts_at=NOW + timedelta(hours=1)), NOW)

    assert isinstance(decision, ro.Disabled) and decision.reason == "not_started"


def test_started_at_exactly_now_is_started() -> None:
    decision = ro.decide("f", "acct_1", make(allowlist={"acct_1"}, starts_at=NOW), NOW)

    assert isinstance(decision, ro.Enabled)


def test_blocklist_wins_over_allowlist() -> None:
    decision = ro.decide("f", "acct_1", make(allowlist={"acct_1"}, blocklist={"acct_1"}), NOW)

    assert isinstance(decision, ro.Disabled) and decision.reason == "blocklisted"


def test_allowlist_wins_over_bucket() -> None:
    decision = ro.decide("f", "acct_1", make(percentage=0, allowlist={"acct_1"}), NOW)

    assert isinstance(decision, ro.Enabled) and decision.reason == "allowlisted"


@pytest.mark.parametrize("percentage", [0, 100])
def test_bucket_extremes(percentage: int) -> None:
    decisions = [ro.decide("f", a, make(percentage=percentage), NOW) for a in ACCOUNTS]

    expected = ro.Enabled if percentage == 100 else ro.Disabled
    assert all(isinstance(d, expected) for d in decisions)


def test_bucket_is_stable_across_calls() -> None:
    first = [type(ro.decide("f", a, make(), NOW)) for a in ACCOUNTS]
    second = [type(ro.decide("f", a, make(), NOW)) for a in ACCOUNTS]

    assert first == second


def test_bucket_is_roughly_the_percentage() -> None:
    enabled = sum(isinstance(ro.decide("f", a, make(percentage=50), NOW), ro.Enabled) for a in ACCOUNTS)

    assert 140 <= enabled <= 260


def test_raising_percentage_keeps_everyone_already_in() -> None:
    at_20 = {a for a in ACCOUNTS if isinstance(ro.decide("f", a, make(percentage=20), NOW), ro.Enabled)}
    at_30 = {a for a in ACCOUNTS if isinstance(ro.decide("f", a, make(percentage=30), NOW), ro.Enabled)}

    assert at_20 <= at_30


def test_bucket_depends_on_feature_name() -> None:
    a = [type(ro.decide("feature_a", acct, make(), NOW)) for acct in ACCOUNTS]
    b = [type(ro.decide("feature_b", acct, make(), NOW)) for acct in ACCOUNTS]

    assert a != b


def test_decision_does_not_depend_on_wall_clock_when_no_start() -> None:
    early = ro.decide("f", "acct_7", make(), NOW - timedelta(days=400))
    late = ro.decide("f", "acct_7", make(), NOW + timedelta(days=400))

    assert type(early) is type(late)


def test_invalid_percentage_is_rejected_at_construction() -> None:
    with pytest.raises(Exception):
        make(percentage=101)
