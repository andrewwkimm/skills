# Exemplars

Paired rewrites by register. The note after each pair says what changed and why. The reasoning is what should carry over to new documents; the nouns and the surface pattern should stay behind.

Quoted BEFORE text is deliberately bad. The checker skips blockquote lines for that reason.

Each BEFORE shows a pattern, and its wording is not a template. Match the failure to the rule it breaks, and ignore the nouns. An AFTER adds a fact only where the vagueness of the BEFORE stood in for a fact the writer had, and the note says so. Any other added detail is invented, which trades one defect for a worse one.

## 1. Reference doc entry

**Before**

> The `retry_budget` parameter is a powerful configuration option that can be utilized in order to seamlessly control the amount of retry traffic that your client is able to generate.

**After**

The `retry_budget` parameter caps the share of a client's requests that may be retries. When the client exceeds the cap, it returns the error instead of retrying.

Vague praise and two fat words came out. The rewrite adds the fact the original omitted, which is what happens when the cap is exceeded. Reference docs use present tense and active voice, and carry no personality.

## 2. How-to step

**Before**

> Now you'll want to simply go ahead and set the connection pool size, which is something that should probably be tuned based on your workload.

**After**

Set `pool_size` to the number of concurrent queries you expect. A pool smaller than that number queues requests; a larger pool holds idle connections open.

The minimizer and the hedge came out. One action per step, and the step states its result. The hedge was replaced by the actual tradeoff, which is the information the hedge was standing in for.

## 3. The Victorian failure and its fix

**Before**

> The migration, which had been planned for several weeks by a team that also owned the ingestion path, required a schema change that, because the downstream consumers read the same table that the batch loader writes, could not be applied without a coordinated deploy, although the team had considered a dual-write approach that would have avoided the coordination.

**After**

The migration needed a schema change on a table that both the batch loader and the downstream consumers use, so it could not ship without a coordinated deploy. The team considered dual writes, which would have avoided the coordination.

76 words, five clauses, and a relative clause nested inside another became 30 and 21 words. Both are still well above the chopped version. This is the bound on the other side: longer is fine until it stops reading in one pass.

## 4. The chopped failure and its fix

**Before**

> A service degrades. Latency rises past the client timeout. Each client counts a timeout as a failure and retries.

**After**

When a service slows past the client timeout, each client counts the timeout as a failure and retries, which adds load to a service that is already short of capacity.

Three sentences that split one causal chain became one sentence that states the cause. The first two failed the deletion test, since neither named an actor doing anything. Facts joined by cause belong in one sentence.

## 5. Verdict sentences

**Before**

> Budgets and breakers overlap deliberately. A budget bounds steady-state amplification; a breaker responds faster to a hard failure. Running both is normal.

**After**

Budgets and breakers overlap on purpose, because a budget bounds steady-state amplification while a breaker reacts faster to a hard failure.

"Running both is normal" is a four-word verdict that carries no fact. Deleting it costs emphasis and nothing else. The rewrite merges the point into a sentence that names what each mechanism does. An earlier version of this rewrite appended "Most systems run both," which replaced the verdict with an unsourced survey claim, a worse defect than the one it fixed.

## 6. Blog opener

**Before**

> In this post, we'll take a look at retry storms. Retry storms are an interesting problem in distributed systems. But first, some background on how retries work.

**After**

A retry that fires during a partial outage adds load to a system that is already short of capacity, so the retry meant to hide one failure helps cause the next one.

The opener that announces the topic came out, and so did the background deferral. The claim is now sentence one. Bernoff says the reader gives you tens of seconds, and this opener spends none of them on setup.

## 7. Same fact, three audiences

Engineer: The page cache key omits the locale. After a deploy, the first request fills the cache in one language, and every later request gets that copy until the entry expires an hour later.

PM: After each release, the site shows every visitor the language of whoever loaded the page first, for up to an hour.

Executive: For up to an hour after each release, some customers saw pages in the wrong language. One missing field in how pages are cached caused it.

The facts do not change. The named machinery does. `cache key` and `locale` are precise for the first reader and noise for the third. This is register calibration, and no word list detects it.

## 8. Organizational post

**Before**

> It's important to note that there may potentially be some organizational challenges. Different teams might have somewhat different incentives, which could possibly lead to friction in the prioritization process.

**After**

The platform team is measured on uptime and the product teams are measured on shipped features, so a migration that risks uptime to unblock features has no natural owner. Whoever proposes it absorbs the risk and someone else books the gain.

Five weasels became zero. Name the incentive rather than gesturing at friction. First person and plain naming, with no moralizing about how teams should behave.

## 9. Postmortem summary

**Before**

> A config change was made to the connection settings. Unfortunately, this ended up being load-bearing in ways nobody anticipated, and it broke things downstream.

**After**

I raised the pool's idle timeout from 30 to 120 seconds, above the load balancer's 60-second limit, so the balancer closed connections the pool still treated as open. Checkout requests failed for 40 minutes.

The agentless passive, the dead metaphor, and "broke things" all came out. The vague "broke things" stood in for figures the author had; the rewrite states them. RCA register is one fact per sentence, each naming an actor and an action, and the author owns their own change in first person.

## 10. Slack proposal

**Before**

> Heads up — I recommend we move the nightly job to 4am. Thoughts?

**After**

The nightly job overlaps the warehouse maintenance window, which is why it retries so often. Moving it to 4am clears the overlap. I plan to change it Thursday unless someone sees a problem.

"Heads up" and "I recommend" both came out, along with the em dash. The rewrite gives the reason, the change, and the default action if nobody objects, which is what lets people ignore it safely.

## 11. Noun stacks

| Stacked | Plain |
| --- | --- |
| schema-handling code | the code that reads the file layout |
| data quality validation failure | the quality check failed |
| user authentication token refresh logic | the code that refreshes login tokens |
| pipeline execution state management | tracking which pipeline runs are still going |
| client-specific configuration flag | a flag set per client |

Each stacked form is shorter and slower. The test is whether the plain-clause version reads better for the declared audience. Sometimes it does not, and then the compound stays.

## 12. Fabricated detail

**Before**

> A regression test now checks on every commit that the pool timeout stays below the balancer's, and it adds 40 milliseconds to the suite.

**After**

A regression test now checks on every commit that the pool timeout stays below the balancer's.

The test exists and the check is real. The 40 milliseconds was invented, because a number reads better than its absence. That is the failure mode this style creates: because concreteness is the goal, the pressure to supply concrete detail never lets up. Confirming that a test exists licenses no claim about its runtime.

## 13. Verdict sentences in a design doc

**BEFORE**

Redis becomes a hard dependency of admission. When it is unreachable, the gateway falls back to the existing in-memory bucket and logs the degradation, which restores today's behavior rather than failing closed. A gateway that rejects all traffic during a Redis blip is worse than one that briefly over-admits.

**AFTER**

Admission now depends on Redis. When Redis is unreachable, the gateway falls back to the existing in-memory bucket and logs the degradation. That restores today's behavior rather than failing closed, which means a Redis outage costs us correct limits rather than all traffic.

Sentence one announced what sentence two then demonstrated; the announcement was a promise of a fact rather than a fact. Sentence three restated the tradeoff sentence two had already carried, converting the argument into a lesson. Folding the dependency into the working sentence and ending on what the outage actually costs leaves two sentences that each carry facts.

**BEFORE**

Sliding windows fix this and cost more per request, and the downstream writer absorbs a two-millisecond burst without trouble, so the fixed window is the right trade here.

**AFTER**

Sliding windows remove that overlap and cost more per request. The downstream writer absorbs a two-millisecond burst without falling behind, so we accept the boundary error and keep the fixed window.

The original scored its own decision. `the right trade` tells the reader the conclusion after the sentence has already given them the cost and the tolerance, which is the reasoning they needed to reach it themselves. Naming the decision plainly, "we accept the boundary error," reports what was chosen without grading it.

## 14. Uncertainty, four branches

**BEFORE**

I think most of our flaky tests probably come from the network mocks, at least from what I've seen, and the p99 latency under retry storms may potentially be a problem too.

**AFTER**

Eleven of the fourteen tests quarantined last month used the network mocks (fictional count, for illustration). We have not measured p99 latency under retry storms, and a load test against the staging gateway would settle it.

The first claim drops `I think`, `probably`, and `from what I've seen`, and shrinks the subject to the tests and the period the writer observed. Widening it to "the network mocks cause our flaky tests" would trade the hedge for a causal claim that fourteen tests never established. The second is a gap in the evidence, which gets its own declarative sentence plus the action that would close it. Both read as owned. Neither hedges.

**BEFORE**

Our exports are used by millions of records daily, and switching formats might possibly break some of them.

**AFTER**

The nightly export writes 140 million rows. Changing the format breaks every consumer that reads positional columns, which is four of the six downstream jobs.

Because `millions` was reachable by looking at the job metrics, the hedge marked laziness rather than uncertainty. `might possibly break some` became a count once the writer checked which consumers parse by position. When a search would resolve the vagueness, searching is the fix.

## 15. Triadic emphasis fragment

**BEFORE**

> Every build reads the same lockfile, so CI and local builds resolve the same package versions. One lockfile, one resolver, no drift.

**AFTER**

Because every build reads the same lockfile, CI and local builds resolve the same package versions and cannot drift apart.

The fragment repeated the preceding sentence as rhythm. Its one new idea, that the versions cannot drift, moved into the causal sentence it decorated.

## 16. Figurative coinage in a technical register

**BEFORE**

> Support staff have to pull the crash report out of the vendor console and then stitch it back into the ticket.

**AFTER**

Support staff have to download the crash report from the vendor console and attach it to the ticket themselves.

`Stitch it back into the ticket` is a coined metaphor that no reader can check against the system. The rewrite names the actual steps, which also tells the reader more.

## 17. Vocabulary fidelity

**BEFORE**

> I compared the queues against three requirements: permissive licensing, a cloud-native footprint, and declarative topic lifecycle.

**AFTER**

I compared the queues against three requirements: a license we can ship, a managed offering from our cloud provider, and topics we can create and delete from configuration files.

`Cloud-native footprint` and `declarative topic lifecycle` stack real terms into compounds the domain does not use. The rewrite says what each requirement means. A reader who has never seen the jargon can still judge the comparison.

**BEFORE**

> The pool keeps a runway of four idle connections, so a blackout on one host no longer stops queries.

**AFTER**

The pool keeps at least four idle connections open, and losing one host no longer stops queries.

`Runway` and `blackout` sound technical but belong to other fields, and a reader has to guess what they mean here. The rewrite uses plain words, and it would use the domain's own term, such as a minimum idle count, where one exists.

## 18. Deference hedge in a proposal

**BEFORE**

> That is my lean, but I would not commit to it untested. Whether a second region is worth its cost is a call for the platform leads, not mine to preempt.

**AFTER**

We should start with one region and measure failover time in the first month. If failover takes longer than the recovery target, I plan to propose the second region with that measurement attached.

A proposal is judged on owned decisions. `My lean` and `not mine to preempt` hand off the judgment the reader came for. The rewrite states the choice with "we should," states the follow-up with "I plan to," and makes the open question depend on named evidence instead of on someone else's authority.

## 19. Negated parallel in scope statements

**BEFORE**

> Load testing is part of each milestone, not a final phase. This change makes the cache a read path, not a write path.

**AFTER**

Load testing is part of each milestone. The cache serves reads only.

Each `X, not Y` pair asserts X and then spends half the sentence denying a Y nobody claimed. Stating the positive half carries the same scope in fewer words.

## 20. Fragment inside a plan step

**BEFORE**

> 3. **During the upgrade.** No changes. The old replica stays up, so traffic can move back by switching the DNS record.

**AFTER**

3. **During the upgrade.** Keep the old replica running, so traffic can move back by switching the DNS record.

`No changes.` is a verbless fragment, and putting it in a numbered step does not exempt it. The rewrite folds the instruction into the sentence that already carried the action and the reason. The same holds for list items and table cells.

## 21. Process notes in the deliverable

**BEFORE**

> I confirmed this on `main`. The loader deletes the staging file before the upload finishes, so a failed upload leaves the retry with nothing to read. If the vendor slips, we can fall back to manual exports.

**AFTER**

Because the loader deletes the staging file before the upload finishes, a failed upload leaves the retry with nothing to read.

How the writer checked the code and a fallback plan outside the document's scope are notes for the requester. The reader gets the problem and its consequence.
