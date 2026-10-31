"""Reads deployment events from the queue and records them."""

import logging
from collections.abc import Callable, Mapping
from datetime import UTC, datetime

from pydantic import AwareDatetime, BaseModel

logger = logging.getLogger(__name__)

Receive = Callable[[], Mapping[str, object] | None]
Record = Callable[[str, Mapping[str, object]], None]


class DeploymentEvent(BaseModel, frozen=True):
    id: str
    service: str
    version: str
    deployed_at: AwareDatetime


def consume_one(receive: Receive, record: Record) -> bool:
    """Handles one message; returns False when the queue was empty."""
    message = receive()
    if message is None:
        return False
    event = DeploymentEvent.model_validate(message)
    record(event.id, event.model_dump())
    logger.info("Recorded deployment %s of %s", event.id, event.service)
    return True


def received_before(event: DeploymentEvent, cutoff: datetime) -> bool:
    return event.deployed_at < cutoff.astimezone(UTC)


def main(receive: Receive, record: Record) -> None:
    while consume_one(receive, record):
        pass
