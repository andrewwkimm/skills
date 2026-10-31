"""Turns a signed payment-provider webhook into a typed event."""

import hashlib
import hmac
import json

from pydantic import AwareDatetime, BaseModel


class SignatureError(Exception):
    """The request's signature does not match the body."""


class PaymentSucceeded(BaseModel, frozen=True):
    id: str
    created_at: AwareDatetime
    payment_id: str
    amount_cents: int
    currency: str


class PaymentFailed(BaseModel, frozen=True):
    id: str
    created_at: AwareDatetime
    payment_id: str
    reason: str


class RefundCreated(BaseModel, frozen=True):
    id: str
    created_at: AwareDatetime
    refund_id: str
    payment_id: str
    amount_cents: int


class UnknownEvent(BaseModel, frozen=True):
    """An event type the provider added after this code was written."""

    id: str
    type: str
    created_at: AwareDatetime


class _Envelope(BaseModel, frozen=True):
    id: str
    type: str
    created_at: AwareDatetime
    data: dict[str, object]
    metadata: dict[str, str] | None = None  # The provider omits it when the caller set none.


_EVENT_BY_TYPE: dict[str, type[PaymentSucceeded | PaymentFailed | RefundCreated]] = {
    "payment.succeeded": PaymentSucceeded,
    "payment.failed": PaymentFailed,
    "refund.created": RefundCreated,
}

Event = PaymentSucceeded | PaymentFailed | RefundCreated | UnknownEvent


def parse_webhook(raw_body: bytes, signature: str, *, secret: bytes) -> Event:
    """Returns the typed event in a verified webhook body.

    Raises:
        SignatureError: the signature does not match the body.
        pydantic.ValidationError: the body or a known type's data is missing or mistyped.
    """
    expected = hmac.new(secret, raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise SignatureError("Webhook signature does not match the body.")
    envelope = _Envelope.model_validate(json.loads(raw_body))
    event_type = _EVENT_BY_TYPE.get(envelope.type)
    if event_type is None:
        return UnknownEvent(id=envelope.id, type=envelope.type, created_at=envelope.created_at)
    return event_type.model_validate({"id": envelope.id, "created_at": envelope.created_at, **envelope.data})
