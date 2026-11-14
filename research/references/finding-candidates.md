# Finding candidates

Read this when the task is to generate options, such as project ideas, alternatives to a tool, vendors, or open research problems, and then test each one. When the candidates are given, skip this file.

## 1. Write the acceptance test first

Take the test from the user's request and write it in the notes before any search: what a candidate must show to survive. Do not loosen it later to fill a list. If fewer candidates survive than the user asked for, report the true count.

## 2. Source candidates where unmet need leaves dated traces

Record every sourcing query in the notes, as with any other search. Places to look, by domain:

| Domain | Where need shows up |
| --- | --- |
| Software | Issue trackers sorted by reactions; requests closed as not planned or closed by a stale bot despite many reactions; repositories or notebooks where users built their own workaround; maintainers' calls for contributors |
| Research | Limitations and future-work sections of recent surveys; papers whose artifacts are dormant; failed or partial replications; benchmark leaderboards that stopped updating |
| Policy and operations | Trackers kept by hand; public calls for reports or tips; recurring themes in comment dockets; audits that name a missing control |
| Products and markets | Shutdown or archive notices of a tool people used; migration guides away from a product; pricing changes that pushed users out |

Signals that a need is real, and the ranking to apply, are in SKILL.md under step 4 ("Claims about what people need").

## 3. Kill check every candidate

Apply step 3a of SKILL.md: one disconfirming search per candidate, aimed at the last 12 to 24 months, because the most common way an idea dies is that someone shipped it recently. Then run the full floors on the survivors only.

## 4. Report the dead

List every candidate that died and what killed it, with the source. The dead list saves the next run from repeating the search.
