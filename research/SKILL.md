---
name: research
description: Independently verifies a handoff, spike, plan, thought piece, or research question and reports back with sourced evidence and a decision, in one autonomous run. Use for "verify this", "is this idea already taken", "research X and tell me if it holds", "review this spike for rigor", "find options for X and test each", or any decision memo where the author's preference might be wrong. Works for software, research literature, policy, and operational questions. Covers research mode (produce the memo) and review mode (audit someone else's memo against the same rules). Pairs with evidence-tiering and technical-writing-style.
---

# Research

Produce a decision the reader can act on, backed by evidence the reader can recheck, in one run. The reader wants to hear what the evidence says, including the parts that kill their favorite idea.

This skill sets procedure and floors. Claim tiers come from `evidence-tiering`; prose rules come from `technical-writing-style`. Load both before drafting.

## Operating rules

1. Work autonomously to the end of the task. Accuracy outranks speed; spend the time.
2. Ask questions once, at the start, only for forks that change the deliverable and have no safe default. Put everything else in an Assumptions section of the deliverable and proceed. Never pause mid-run to ask.
3. Do not spawn subagents unless the user asked for them in this task. Do the searching, fetching, and measuring yourself. One exception: when the environment exposes page fetching only through an agent built for that purpose, using it counts as a fetch. Give it the URL and the exact facts to quote, and treat its report under the summary rule in step 3.
4. Read the whole input before forming a view. Write down the author's preferred conclusion in one line so you can check later that it did not steer you.
5. Prefer running a measurement over quoting a claim about it, whenever a measurement is possible from this machine within the stated budget.
6. Never commit, push, or publish. Write files to the location the user named, or to a `scratch/` directory beside the input.

## Procedure

### 1. Contract

Record mode (research or review), audience, exposure, and reader action, per the writing contract in `technical-writing-style`. Record the time or token budget the user gave, or state the default: the task ends when every ledger row has a completeness value, however early the first answer appears.

### 2. Extract the claims

Research mode: turn the question into 5 to 15 decision-critical claims to establish or refute. Review mode: pull every externally checkable claim from the input, including the implicit ones (a plan that says "no competitor does X" claims an absence; a plan that assumes 50 GB free claims a machine fact).

Each claim becomes a ledger row (section 6) before any searching starts. A claim that is not in the ledger is not in the deliverable.

When the task is to generate candidates (ideas, alternatives, vendors, open problems) rather than to check given ones, read `references/finding-candidates.md` first. Each candidate's decisive claims then enter this ledger like any other.

### 3. Search floors

These floors exist because the common failure is stopping after one confirming hit. For each decision-critical claim:

- Run at least two differently worded searches, one phrased to confirm and one phrased to disconfirm ("X does not support Y", "alternatives to X", "X deprecated").
- Open the primary source. A search snippet, an aggregator, a search engine's generated answer, or a model's summary of a page (including a fetch tool's digest) is not a read of the page. A row supported only by one of these is Partial, never Complete.
- For a "nothing exists" claim, record the exact queries, the scope, the stopping rule, and the count examined. Search every class of source where the thing would appear if it existed, with at least two phrasings in each. Without that record the claim is unsupported and is written as "I found none in <scope>". Typical classes:

  | Subject | Source classes to search |
  | --- | --- |
  | Software, tools, products | The dominant package registry for the language, GitHub with three phrasings, one survey or academic venue, one vendor-docs site |
  | Research findings | Two indexes suited to the field (for example Google Scholar, arXiv, PubMed, SSRN), one recent survey or review, and the citations of the closest paper |
  | Laws, rules, policies | Full-text search of the official text, the issuing body's site, one annotated index or secondary tracker |
  | Facts inside a document set or codebase | The complete set, with the query and the count of files or documents examined |
  | Organizations, events, people | Primary records (filings, registries, official sites) and two independent reports |

- For a claim that a thing does or says something (a tool's behavior, a law's requirement, a paper's result), read the thing itself: the docs or source, the statute, the paper. A comparison article or a summary does not count.
- For a number (price, limit, size, count, date), cite the page that states it and the date you read it. Prices and limits expire; include the region or tier.
- When a source is unreachable (failed fetch, bot challenge, paywall, sandbox denial), record the URL and the error, then try one mirror or cached form and one alternative source of the same class, and name the substitute in the row. If nothing works, mark the row Blocked, or Partial for an absence row that lost one class, and say in the deliverable which class is missing.

### 3a. Triage when claims outrun the budget

Screening many candidates, or reviewing a long input, can produce more claims than the budget allows at full floors. Then run a kill check on every claim first: one search phrased to disconfirm, aimed at the newest evidence (a recent release, ruling, retraction, or competing result). Give the full floors only to claims that survive the kill check and remain decision-critical. A row that got only the kill check is Partial and says "triage only".

### 4. Source ranking

Use the highest tier available; a lower tier alone supports only a Partial row.

| Tier | Sources |
| --- | --- |
| 1 | Primary sources: specifications, statutes and regulations, court opinions, filings, datasets, source code, official docs, machine-readable pricing, your own measurement or calculation |
| 2 | Peer-reviewed papers and their artifacts, official reports with a stated method, maintainer-written release notes, repository metadata (commits, license, archived flag) |
| 3 | Organization or vendor blog posts, conference talks, maintainer answers in issues, named expert statements |
| 4 | Reputable secondary reporting that quotes a tier 1 or 2 source |
| Excluded as sole support | Personal blogs, listicles, marketing pages, forum answers, LLM output (including search-generated answers and tool summaries of a page), your memory |

For a repository, record license, last commit date, archived flag, and star count from the API or page; memory does not count.

Claims about what people need or will do get their own rules, because no search result settles them. A person's dated, public account of what they did or what happened to them is F1 for that account: a bug report, a complaint on file, a post that describes a workaround. Rank such evidence of a need, strongest first: someone built or paid for a workaround; someone reported a dated failure that cost them; someone asked for the thing; people reacted to a request. Count distinct people and link each one. A claim that people will adopt, buy, or keep using something stays F3, with the execution named (an interview, a trial, an offer made to the people who reported the need).

### 5. Measure where possible

If a claim is about behavior reachable from this machine (a public endpoint, a library's behavior, throughput, file counts, disk) or can be recomputed from published data (a total, a rate, a trend), write a short script, run it, keep the script and raw output next to the notes, and cite them. State the budget used (bytes, time, disk). A measurement is F1 for that run only; say so.

### 6. Ledger

Keep one table in the research notes with these columns, per `evidence-tiering`: Claim, Tier, Evidence and source, Recheck, Completeness. Add a sixth column in review mode: Author's tier (what the input implied) so the gap is visible.

Run `scripts/ledger_check.py NOTES.md` before drafting. It fails on a row with a missing field, an unknown tier or completeness value, an F3 row without a named execution, or an absence row that is not tiered F2 or lacks scope and stopping rule words. Its absence detection is a pattern match, so a clean run does not prove every absence row was caught; read the Claim column once yourself. Fix the row or demote the claim; do not delete the row.

### 7. Revisit pass

After the ledger is complete and before writing, reread the input's preferred conclusion from step 1 and answer in the notes: which rows contradict it, and did any row get a tier or completeness it did not earn because it agreed with that conclusion. Then reread every row marked Partial or Pending and attempt it once more. This pass is where early assumptions get caught; do not skip it.

### 8. Deliverable

Follow the decision-document shape in `technical-writing-style`: conclusion first, then evidence, then the plan or mapping, then open questions, then sources. Lead with the findings that contradict the author's preference; do not soften them. Mark judgment as judgment. Put the ledger in an appendix or a separate notes file, as the user asked. Run `style_check.py --all` on the deliverable, fix every Fail, and list every remaining Flag for the user.

Include an Assumptions section listing every default you took instead of asking, and a What I could not verify section listing Blocked and Partial rows in plain words.

## Review mode

Audit the input with the same ledger. For each of its claims record what the input offered as support, what tier that support earns, and what you found when you checked. The review's verdict is per claim (holds, holds with narrower scope, unsupported, wrong), then an overall judgment. A review that only comments on structure or tone has not done the work.

Do not reproduce the input's length. A review lists the claims that change the reader's decision and skips the rest.

## Floors that protect against stopping early

- A claim without a ledger row is not written.
- A row cannot be Complete on a snippet, a memory, or one source.
- A "likely", "probably", or "should" in the draft means the ledger row is missing or Partial; fix the row, then delete the hedge.
- Every absence claim names its scope and stopping rule in the sentence that makes it.
- The run ends when the ledger has no Pending rows and the revisit pass is written, or when the stated budget is exhausted, in which case the deliverable says which rows ran out of budget.

## What this skill cannot do

It enforces procedure; judgment stays with the model and the reader. A model can follow every floor and still misread a source; the recheck column exists so the reader can catch that. It cannot verify private systems or paid products behind a login, and it cannot establish that people will adopt something; those rows stay F3 with the execution named (an interview, a trial account, a company-approved test).
