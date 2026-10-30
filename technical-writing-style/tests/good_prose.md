# Retries Amplify Load

A retry that fires during a partial outage adds load to a system that is already
short of capacity, so the retry that was meant to hide one failure helps cause the
next one.

A service slows down, its callers time out, and
each caller sends the request again. The service now handles the original traffic
plus the retries, which pushes it further past its limit.

Layered call chains make this worse. If four services sit in a chain and each one
retries three times, one user request can turn into 81 requests at the bottom,
because each layer multiplies the layer below it.

A retry budget caps the share of a client's traffic that retries may consume. When
the client exceeds the cap, it stops retrying and returns the error, which keeps
total load bounded even when every downstream call is failing.

Jitter matters as much as the budget. Plain exponential backoff keeps retries
synchronized, so a thousand clients that failed together will retry together.
Adding random jitter to each delay spreads the load across the window.
