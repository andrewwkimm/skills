# Fixture: the bad ledger, repaired

| Claim | Tier | Evidence and source | Recheck | Completeness |
| --- | --- | --- | --- | --- |
| Library X caps requests at 5,000 per window | F1 | https://example.invalid/docs/limits, read 2026-11-13 | Open the page | Complete |
| No existing tool reads footers across providers | F2 (absence; scope: GitHub with three phrasings, PyPI, crates.io, one VLDB survey; stopping rule: first 50 results per query; examined 10 repos) | notes §4 | Repeat the queries listed in notes §4 | Partial |
| The scanner will sustain 100 footers per second | F3 | None yet | Week-3 run against 10^5 files with the concurrency probe | Pending |
| 100 footers took 3.5 s at concurrency 32 | F1 | `concurrency_probe.py` output 2026-11-13 | Run the script | Complete |
| Listing returns 1,000 keys per page | F1 | https://example.invalid/api/list | Open the API doc | Complete |
| Footer read costs 2 requests | F1 | probe output | Run the probe | Complete |
| No maintained open-source tool diffs dataset snapshots | F2 (absence; scope: GitHub with three phrasings, PyPI, crates.io; stopping rule: top 15 results per query, all examined) | notes §5 | Repeat the queries in notes §5 | Partial |
| No published study measures remote-work productivity in county governments | F2 (absence; scope: Google Scholar and SSRN with four queries listed in notes §6, plus the reference list of one 2025 review; stopping rule: first 50 results per query; examined 212 titles) | notes §6 | Repeat the queries in notes §6 | Complete |
| Nothing like this provision exists in the state code | F2 (absence; scope: full-text search of the official state code site for four phrasings, and the annotated index; stopping rule: every hit read) | notes §7 | Repeat the searches in notes §7 | Complete |
| The probe saw no errors in 400 requests | F1 | `concurrency_probe.py` output 2026-11-13 | Run the script | Complete |
