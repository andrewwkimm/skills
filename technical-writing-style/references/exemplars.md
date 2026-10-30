# Exemplars

Paired rewrites by register. The note after each pair says what changed and why, so the reasoning transfers rather than the surface pattern.

Quoted BEFORE text is deliberately bad. The checker skips blockquote lines for that reason.

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

"Running both is normal" is a four-word verdict that carries no fact. Deleting it costs emphasis and nothing else. The rewrite folds the point into a sentence that names what each mechanism does. An earlier version of this rewrite appended "Most systems run both," which replaced the verdict with an unsourced survey claim, a worse defect than the one it fixed.

## 6. Blog opener

**Before**

> In this post, we'll take a look at retry storms. Retry storms are an interesting problem in distributed systems. But first, some background on how retries work.

**After**

A retry that fires during a partial outage adds load to a system that is already short of capacity, so the retry meant to hide one failure helps cause the next one.

The opener that announces the topic came out, along with the background deferral. The claim is now sentence one. The reader gives you fifteen seconds and this spends none of them on setup.

## 7. Same fact, three audiences

Engineer: The loader casts an all-null column to `float64`, which Parquet writes as `DOUBLE`, so the downstream reader rejects the file on a type mismatch.

PM: When a column arrives empty, the loader guesses the wrong type for it, and the next job refuses to read the file.

Executive: Five client reports stopped updating for two days. One code change altered how empty columns are typed, which broke the file format the reporting layer reads.

The facts do not change. The named machinery does. `float64` and `DOUBLE` are precise for the first reader and noise for the third. This is register calibration, and no word list detects it.

## 8. Organizational post

**Before**

> It's important to note that there may potentially be some organizational challenges. Different teams might have somewhat different incentives, which could possibly lead to friction in the prioritization process.

**After**

The platform team is measured on uptime and the product teams are measured on shipped features, so a migration that risks uptime to unblock features has no natural owner. Whoever proposes it absorbs the risk and someone else books the gain.

Five weasels became zero. Name the incentive rather than gesturing at friction. First person and plain naming, with no moralizing about how teams should behave.

## 9. Postmortem summary

**Before**

> A refactor was made to the schema logic. Unfortunately, this ended up being load-bearing in ways nobody anticipated, and it broke things downstream.

**After**

A one-line change replaced an explicit column loop with `reindex`, which changed the type of all-null columns from `object` to `float64`. Five client reports failed to load for two days.

The agentless passive, the dead metaphor, and "broke things" all came out. RCA register is one fact per sentence, each naming an actor and an action. No rhythmic emphasis and no asides.

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

> A regression test now asserts the column type on every commit, and it adds 40 milliseconds to the suite.

**After**

A regression test now asserts the column type on every commit.

The test exists and the assertion is real. The 40 milliseconds was invented, because a number reads better than its absence. That is the failure mode this style creates: concreteness is the goal, so the pressure to supply concrete detail is constant. Confirming that a test exists licenses no claim about its runtime.

## 13. Verdict sentences in a design doc

**BEFORE**

Redis becomes a hard dependency of admission. When it is unreachable, the gateway falls back to the existing in-memory bucket and logs the degradation, which restores today's behavior rather than failing closed. A gateway that rejects all traffic during a Redis blip is worse than one that briefly over-admits.

**AFTER**

Admission now depends on Redis, so when Redis is unreachable the gateway falls back to the existing in-memory bucket and logs the degradation. That restores today's behavior rather than failing closed, which means a Redis outage costs us correct limits rather than all traffic.

Sentence one announced what sentence two then demonstrated, so the announcement was a promise of a fact rather than a fact. Sentence three restated the tradeoff sentence two had already carried, converting the argument into a lesson. Folding the dependency into the working sentence and ending on what the outage actually costs leaves two sentences that each carry facts.

**BEFORE**

Sliding windows fix this and cost more per request, and the downstream writer absorbs a two-millisecond burst without trouble, so the fixed window is the right trade here.

**AFTER**

Sliding windows remove that overlap and cost more per request. The downstream writer absorbs a two-millisecond burst without falling behind, so we accept the boundary error and keep the fixed window.

The original scored its own decision. `the right trade` tells the reader the conclusion after the sentence has already given them the cost and the tolerance, which is the reasoning they needed to reach it themselves. Naming the decision plainly, "we accept the boundary error," reports what was chosen without grading it.

## 14. Uncertainty, four branches

**BEFORE**

I think most interviewees probably can't pass the technical screen, at least from what I've seen, and the p99 latency under retry storms may potentially be a problem too.

**AFTER**

Five of the seven recruiter-pipeline candidates last quarter failed the technical screen (fictional count, for illustration). We have not measured p99 latency under retry storms, and a load test against the staging gateway would settle it.

The first claim drops `I think`, `probably`, and `from what I've seen`, and shrinks the subject to the group and period the writer observed. Widening it to "candidates from the recruiter pipeline cannot pass" would trade the hedge for a claim about the whole group that seven interviews never established. The second is a gap in the evidence, which gets its own declarative sentence plus the action that would close it. Both read as owned. Neither hedges.

**BEFORE**

Our exports are used by millions of records daily, and switching formats might possibly break some of them.

**AFTER**

The nightly export writes 140 million rows. Changing the format breaks every consumer that reads positional columns, which is four of the six downstream jobs.

`millions` was reachable by looking at the job metrics, so the hedge marked laziness rather than uncertainty. `might possibly break some` became a count once the writer checked which consumers parse by position. When a search would resolve the vagueness, searching is the fix.

## 15. Triadic emphasis fragment (design proposal)

**BEFORE**

> A BackupStorage can reference that Secret directly, because its controller adopts a credential Secret only when it has no controller owner. One Secret, one writer, no copies to drift.

**AFTER**

A BackupStorage can reference that Secret directly because its controller adopts a credential Secret only when it has no controller owner. Both sides then share one Secret with no copies to drift.

The fragment repeated the preceding sentence as rhythm. Its one new fact, that sharing avoids copy drift, folded into a plain sentence with an actor.

## 16. Figurative coinage in a technical register

**BEFORE**

> Anyone running on-premise or at the edge has to stand up the storage by hand, outside the platform, and then feed the coordinates back in.

**AFTER**

Anyone running on-premise or at the edge has to stand it up by hand and enter its endpoint, bucket, and credentials into OpenEverest themselves.

`Feed the coordinates back in` is a coined metaphor no reader can verify against the system. The rewrite names the actual fields, which is also more information.

## 17. Invented qualifier next to a real term

**BEFORE**

> I screened the candidates against four requirements: compatible licensing, an operator-backed lifecycle, and declarative bucket and credential management.

**AFTER**

I screened the candidates against four requirements: a license the project can ship, an existing Kubernetes operator to run the cluster, and buckets and credentials the provider can manage as Kubernetes resources.

`Operator-backed lifecycle` and `declarative bucket management` stack real terms into compounds the source domain never uses. The rewrite says what each requirement means, so a reader who has never seen the jargon can still evaluate the screen.

## 18. Deference hedge in a design proposal

**BEFORE**

> That is my lean, but I would not commit to it untested. Whether that destination is worth its cost is a mentor decision, not mine to preempt.

**AFTER**

I recommend SeaweedFS as the first engine to validate and implement. If the MVP shows buckets and credentials need lifecycles independent of the Instance, I would propose dedicated core resources.

A proposal is evaluated on owned decisions. `My lean` and `not mine to preempt` outsource the judgment the reader came for. The rewrite states the choice and makes the open question conditional on named evidence instead of on someone else's authority.

## 19. Negated parallel in scope statements

**BEFORE**

> Testing and documentation are part of each step, not a final phase. This proposal makes object storage a backup target, not a backup source.

**AFTER**

Testing and documentation are part of each step. Backing up the object store itself is out of scope.

Each `X, not Y` pair asserts X and then spends half the sentence denying a Y nobody claimed. Stating the positive half carries the same scope in fewer words.
