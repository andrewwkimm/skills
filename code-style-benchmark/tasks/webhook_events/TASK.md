# Task: webhook events

Write `webhook_events.py` and `test_webhook_events.py`.

A payment provider posts webhooks to our service. Each request carries a JSON body and an `X-Signature` header. Write the code that turns a raw request into a typed event the rest of the service can act on.

Facts:

- The signature is `hex(HMAC-SHA256(secret, raw_body))`. A request whose signature does not match is rejected.
- The body is a JSON object: `{"id": str, "type": str, "created_at": RFC 3339 string, "data": {...}}`. `data` depends on `type`:
  - `"payment.succeeded"`: `{"payment_id": str, "amount_cents": int, "currency": str}`
  - `"payment.failed"`: `{"payment_id": str, "reason": str}`
  - `"refund.created"`: `{"refund_id": str, "payment_id": str, "amount_cents": int}`
  - The provider documents that it may add new `type` values at any time; our service must not break when it does.
- `metadata` is an optional object on every body; when present its values are strings.

Required interface (the tests import these names):

```python
def parse_webhook(raw_body: bytes, signature: str, *, secret: bytes) -> PaymentSucceeded | PaymentFailed | RefundCreated | UnknownEvent
class SignatureError(Exception)
```

`PaymentSucceeded`, `PaymentFailed`, `RefundCreated` carry the fields listed above plus `id` and `created_at` (a timezone-aware `datetime`). `UnknownEvent` carries `id`, `type`, and `created_at`. Decide yourself what happens with a body missing a documented field, an `amount_cents` that is not an integer, or a known type whose `data` is missing a field, and say why in `NOTES.md`.

pydantic v2 and pytest are available. Run `pytest -q` and `ruff check .` in your output directory and fix what they report. Write NOTES.md under 200 words: the decisions you made and why.
