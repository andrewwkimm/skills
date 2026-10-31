"""Decides whether an account sees a gradually rolled-out feature."""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

Reason = Literal["kill_switch", "not_started", "blocklisted", "allowlisted", "in_bucket", "out_of_bucket"]

_BUCKETS = 10_000


@dataclass(frozen=True)
class Rollout:
    """How far a feature has been rolled out and to whom."""

    percentage: int
    allowlist: frozenset[str] = field(default_factory=frozenset)
    blocklist: frozenset[str] = field(default_factory=frozenset)
    kill_switch: bool = False
    starts_at: datetime | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.percentage <= 100:
            raise ValueError(f"percentage must be between 0 and 100, got {self.percentage}.")
        object.__setattr__(self, "allowlist", frozenset(self.allowlist))
        object.__setattr__(self, "blocklist", frozenset(self.blocklist))


@dataclass(frozen=True)
class Enabled:
    reason: Reason


@dataclass(frozen=True)
class Disabled:
    reason: Reason


def decide(feature: str, account_id: str, rollout: Rollout, now: datetime) -> Enabled | Disabled:
    """Returns whether ``account_id`` sees ``feature`` at ``now``, and why."""
    if rollout.kill_switch:
        return Disabled("kill_switch")
    if rollout.starts_at is not None and now < rollout.starts_at:
        return Disabled("not_started")
    if account_id in rollout.blocklist:
        return Disabled("blocklisted")
    if account_id in rollout.allowlist:
        return Enabled("allowlisted")
    if bucket(feature, account_id) < rollout.percentage * _BUCKETS // 100:
        return Enabled("in_bucket")
    return Disabled("out_of_bucket")


def bucket(feature: str, account_id: str) -> int:
    """Returns a stable bucket in [0, 10000) for the account under the feature."""
    digest = hashlib.sha256(f"{feature}:{account_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % _BUCKETS
