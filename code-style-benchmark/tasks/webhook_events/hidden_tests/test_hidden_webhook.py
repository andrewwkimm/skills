"""Hidden tests for the webhook_events task."""

import hashlib
import hmac
import json
from datetime import UTC, datetime

import pytest
import webhook_events as we

SECRET = b"top-secret"


def body(payload: dict) -> bytes:
    return json.dumps(payload).encode()


def sign(raw: bytes, secret: bytes = SECRET) -> str:
    return hmac.new(secret, raw, hashlib.sha256).hexdigest()


def succeeded(**overrides) -> dict:
    payload = {
        "id": "evt_1",
        "type": "payment.succeeded",
        "created_at": "2026-03-01T12:00:00Z",
        "data": {"payment_id": "pay_1", "amount_cents": 1250, "currency": "USD"},
    }
    payload.update(overrides)
    return payload


def test_payment_succeeded_is_typed() -> None:
    raw = body(succeeded())

    event = we.parse_webhook(raw, sign(raw), secret=SECRET)

    assert isinstance(event, we.PaymentSucceeded)
    assert event.id == "evt_1"
    assert event.payment_id == "pay_1"
    assert event.amount_cents == 1250
    assert event.currency == "USD"
    assert event.created_at == datetime(2026, 3, 1, 12, tzinfo=UTC)


def test_bad_signature_is_rejected_before_parsing() -> None:
    raw = body(succeeded())

    with pytest.raises(we.SignatureError):
        we.parse_webhook(raw, sign(raw, b"other"), secret=SECRET)


def test_unknown_type_is_its_own_outcome_not_an_error() -> None:
    raw = body({"id": "evt_9", "type": "dispute.opened", "created_at": "2026-03-01T12:00:00Z", "data": {"anything": 1}})

    event = we.parse_webhook(raw, sign(raw), secret=SECRET)

    assert isinstance(event, we.UnknownEvent)
    assert event.type == "dispute.opened"
    assert event.id == "evt_9"


def test_missing_amount_is_not_read_as_zero() -> None:
    raw = body(succeeded(data={"payment_id": "pay_1", "currency": "USD"}))

    with pytest.raises(Exception) as info:
        we.parse_webhook(raw, sign(raw), secret=SECRET)
    assert "amount_cents" in str(info.value)


def test_non_numeric_amount_is_rejected() -> None:
    raw = body(succeeded(data={"payment_id": "pay_1", "amount_cents": "twelve", "currency": "USD"}))

    with pytest.raises(Exception):
        we.parse_webhook(raw, sign(raw), secret=SECRET)


def test_missing_envelope_field_names_it() -> None:
    payload = succeeded()
    del payload["created_at"]
    raw = body(payload)

    with pytest.raises(Exception) as info:
        we.parse_webhook(raw, sign(raw), secret=SECRET)
    assert "created_at" in str(info.value)


def test_metadata_is_optional() -> None:
    raw = body(succeeded(metadata={"order": "o_7"}))

    event = we.parse_webhook(raw, sign(raw), secret=SECRET)

    assert isinstance(event, we.PaymentSucceeded)


def test_refund_created() -> None:
    raw = body(
        {
            "id": "evt_3",
            "type": "refund.created",
            "created_at": "2026-03-01T12:00:00+00:00",
            "data": {"refund_id": "re_1", "payment_id": "pay_1", "amount_cents": 500},
        }
    )

    event = we.parse_webhook(raw, sign(raw), secret=SECRET)

    assert isinstance(event, we.RefundCreated)
    assert (event.refund_id, event.payment_id, event.amount_cents) == ("re_1", "pay_1", 500)
