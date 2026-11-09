# Loose run fixture

The cache expires every hour, so the first request after expiry is slow. That request rebuilds the whole index, which takes about 40 seconds. The rebuild runs on the request thread, so other requests queue behind it.
