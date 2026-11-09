---
name: technical writing style
description: "Writes and edits technical prose for docs, blog posts, design docs, postmortems, and chat messages in a plain, sourced, non-machine register. Use when drafting or revising any prose deliverable, or when asked for Bernoff style, no-BS style, plain language, or a style pass. Covers evidence rules, diction, sentence construction, paragraph flow, hard bans, numeric targets, and per-audience register profiles."
---

# Technical Writing Style

## Precedence

When rules conflict, the higher rule wins. Say which rule you broke and why.

1. Factual accuracy, including sourcing. An unsourced specific is a factual defect. Style does not enter into it.
2. Completeness of the content the reader needs to act.
3. Clarity for the declared audience, as declared before drafting.
4. Hard bans. Zero tolerance, requiring no judgment.
5. Rhythm findings. These are near-certain defects, though a human confirms each one.
6. Numeric ranges. These are budgets, and you may break one when you state the reason.

## Evidence

Every number, date, duration, version, error string, threshold, and named behavior traces to one of these: a linked document, a commit or pull request, a log line, a timestamped message, a test run, or the author's own direct knowledge. Anything else comes out.

The reader should be able to check a claim without trusting the writer. Link the source where the claim appears, either in parentheses or by linking the words that make the claim, or point to a methodology section with the query or script that reproduces it. Internal data with neither a link nor a reproducible method comes out of the deliverable.

Three rules follow from that.

Quote error messages, log lines, and code verbatim. A paraphrase that reads clean has invented precision the source did not have.

Never invent detail around a real fact. Confirming that a regression test exists licenses no claim about how long it runs. The surrounding detail feels safe because the core fact is true, which is what makes it easy to write.

Prefer an honest vague sentence to a specific invented one. "The check runs on every commit" beats "the check adds 40 milliseconds" when nobody measured it. Concreteness is the goal of this style, so this style creates constant pressure to fabricate numbers. Expect that pressure and refuse it.

## Uncertainty

Not knowing something splits four ways, and collapsing them is what produces mush.

**The fact exists somewhere, and you have not looked.** Look it up. Bernoff is harshest here, calling it laziness: writers use weasel words "to avoid the necessary research to get precise answers." His rewrite of a United Airlines letter replaces "millions of people" with "140 million trips with us last year," and he notes that the figure "took me 15 seconds to look it up." Any hedge a search would dissolve is not honesty. Run this test before labeling anything unknown. The same test applies to an open-questions list: answer every question the writer could close with the access already in hand, and keep only the questions that need someone else.

**You hold a judgment you cannot prove.** State it flat and own it. The qualifier buys nothing, because "your readers will hold you responsible regardless of whether you said the exceptions happen 'rarely' or didn't mention them at all, so you might as well be bold." Strip `I think`, `it seems to me`, `in my experience`, and `from what I have seen` off any claim you actually hold. That advice aims at the ritual self-deprecation writers wrap around stances they hold. It says nothing about concealing a fact you lack.

Removing a hedge never licenses keeping the claim at its original size. When a sentence cannot survive flat, shrink the claim along one of three axes until it can: the subject (`the team already decided` becomes `#412 renamed the field`), the timeframe (`this is settled` becomes `as of the April release`), or the source (`no runbook exists` becomes `I found no runbook in the wiki or the repo's docs/`). Deleting the qualifier while keeping the claim converts a hedge defect into a factual one, which is a worse trade.

**The fact does not exist, because nobody measured it.** Write the gap as its own declarative sentence and say what would close it. "We have not measured p99 latency under retry storms. A load test against the staging gateway would settle it." That is two facts and an action, so it does not read as weaseling. A hedge attaches doubt to a claim you are still making, which weakens the claim and adds nothing.

**You think you are probably wrong.** Delete the sentence. Bernoff: "If you're afraid of generalizing—if you think there's a good chance you're wrong—then don't generalize." A claim at sixty percent confidence comes out rather than getting a label.

Where a number carries provenance the reader needs, put it in parentheses after the claim so the claim itself stays direct. Bernoff does this when he invents figures to demonstrate a rewrite: "(I made these numbers up; Pakes would have to substitute the actual data.)"

### When the quantity is not the point

A weak generalization survives when the writer reaches for a count the argument never needed. Bernoff's fix is to name the subject rather than the quantity: "Don't tell us that many people do something, tell us which people do it."

His Bernie Sanders example shows the move. "A growing number of communities do not trust the police and law enforcement officers have become disconnected from the communities they are sworn to protect" becomes "In communities where people don't trust the police, law enforcement officers lack a connection with those they are sworn to protect." He notes that the original "doesn't really quantify the problem" and that "the quantity isn't relevant anyway."

So "most interviewees cannot pass the technical screen" does not need softening. It needs a subject the evidence covers: "five of the seven recruiter-pipeline candidates last quarter failed the technical screen" (fictional count, for illustration). That names who, stays inside what the writer observed, and still makes the point about the pipeline. Widening instead to "candidates from the recruiter pipeline cannot pass" trades the hedge for a claim about the whole group that seven interviews never established, which is the worse defect. When the flat sentence overreaches, shrink the subject, the timeframe, or the source until it holds.

Comparisons still need "less" and "more," and an unstable explosive still gets called "extremely unstable," so the target was never zero qualifiers. His target is pruning "as many of them as possible," and his stated goal across all three habits is a ninety percent cut.

## Target voice

The target voice is plain, specific, and sourced. The writer knows the subject, respects the reader's time, and has no interest in sounding impressive. Judgments are stated flat and owned. Gaps in the evidence are named in their own sentence.

Voice follows the document, so team proposals and plans use "we" or a neutral, business-professional voice, and analysis keeps "I" for provenance where the reader needs to know who measured what ("I timed the last 200 builds").

State a recommendation as what should happen or what you will do: "We should move the job to 4 am" or "I plan to raise the limit on Thursday." Avoid "I recommend," which puts the writer in front of the action.

A plain idiom is fine when it carries a judgment the surrounding facts support, such as "a textbook N+1 query" or "worth doing while you are in that module, though it saves under a second." The bans on dead metaphors and figurative coinage still apply, because those stand in for a mechanism instead of judging one.

## Diction

Word origin predicts machine prose better than sentence length does. Orwell's rewrite of a passage from Ecclesiastes is 38 words against the original's 49, so it wins on brevity and loses on every other axis, because the short version runs 39 percent long Latinate words against the original's 6 percent.

Prefer the short Anglo-Saxon word. Zinsser warns against the long word that is no better than the short one, and Strunk and White against the twenty-dollar word when a ten-center will do.

Kill nominalizations. A nominalization buries a verb inside a noun, then needs a weak verb to carry the sentence. `make a decision` becomes decide. `provide a solution` becomes solve. `perform an analysis` becomes analyze. `the implementation of` becomes we built.

Do not stack nouns. Zinsser calls it creeping nounism, stringing two or three nouns where one noun or a verb will do. Any compound noun phrase must survive a plain-clause rewrite test: if `schema-handling code` reads better as "the code that reads the file layout," rewrite it. Keep the compound when it is the shortest accurate phrasing.

Long-word share is the reliable signal, and monosyllable share is the weak one. Technical prose carries domain nouns that have no short form, so a piece about a rate limiter pays a syllable tax no rewrite can remove. Measured across book prose and technical drafts, long-word share separates jargon from plain writing by a wide margin. A deliberately bad jargon paragraph runs 60 percent long words against 5 to 13 percent for plain prose, while its monosyllable share sits close to a clean document's. Treat a low monosyllable count as a prompt to check whether the long words are domain terms or fat words, since only the second kind is a defect.

## Sentence construction

There is no minimum sentence length, only a content test.

**The deletion test.** Every sentence must carry a fact, a decision, a material uncertainty, or a reader action that disappears if you delete it. If deleting it costs only emphasis or framing, merge it into a neighbor or cut it. Length is not the signal, since an eighteen-word sentence can be pure verdict while a seven-word sentence can carry the only fact in the paragraph. When a short sentence labels a fact without stating its consequence (`The backfill is done and conservative.`), the repair is a merge into the sentence that says why the fact matters, never a standalone rewrite.

Failing: "Running both is normal." "Retries multiply through layers." "The failure is not theoretical."

Passing: "The pipeline then deduplicated the results." "A configuration flag limited the change to one client."

**Verdicts.** A verdict evaluates or labels rather than reports, so it fails the deletion test at any length. Three forms, and the same fix each time: cut it and let the facts stand.

*Announcements* label the paragraph before delivering it. "The failure is not theoretical." "The counter is approximate at window boundaries." "The mechanism is simple to state." Cut the announcement and open with the fact, since the reader learns the point faster from the evidence than from a promise of evidence.

*Maxims* restate the reasoning as a general principle after the fact. "A gateway that rejects all traffic during a Redis blip is worse than one that briefly over-admits." "Running both is normal." The preceding sentence already carried the tradeoff, so the maxim converts an argument into a lesson delivered to the reader.

*Appended verdicts* score a decision the sentence already justified. "so the fixed window is the right trade here" adds nothing after the sentence has named the cost and the tolerance. Words like right trade, correct choice, and reasonable tradeoff score the decision instead of reporting it. State the cost and who absorbs it, then stop.

"The fixed window is the right trade" tells the reader your conclusion, where "the writer absorbs a two-millisecond burst" lets them reach it themselves.

**Do not chop causation.** Facts joined by cause belong in one sentence. Splitting them into three sentences discards the relationship the reader needed. Delete words that carry nothing; never split a sentence that carries something. A 25-word sentence with no waste beats three 8-word sentences that restate each other.

**Vary the sentences.** Strunk and White's Rule 18 warns against a succession of loose sentences: two clauses joined by `, so`, `, which`, `, and`, or `, while`, one after another, read as singsong. Keep a cause with its effect when the reader needs the link, and let other facts stand as their own sentences. Use a semicolon, a subordinate clause (`because`, `when`, `after`), or a plain second sentence for variety. Most sentences should be short and some long. The checker flags three loose sentences in a row.

**Fragments in lists, tables, and steps.** The deletion test and the fragment bans apply inside list items, table cells, and numbered steps. "No changes.", "Disks stay clear", and "Capacity goes to prod" read as machine output wherever they sit. Write each item as a sentence that says what happens and why, or fold it into the item it belongs to. A cell that holds a bare value, such as a number, a name, or a date, is fine.

**Clustering limit.** At most one bare simple sentence under nine words per paragraph, never two consecutive.

**The opposite bound.** Longer is fine until it stops being readable in one pass. Four detectable failures: more than two subordinate clauses in one sentence, a relative clause nested inside another, more than ten words between subject and verb, and nested parentheticals.

## Paragraph flow

Make the paragraph the unit of composition, as Strunk and White put it: one step of the argument per paragraph. Let the subject of the first sentence show the topic, and make that sentence a fact rather than a label for what follows.

Put the emphatic words at the end of the sentence. Put the emphatic sentence at the end of the paragraph.

Every sentence has one job, which is to make the reader want to read the next one. In a work document that means giving the next fact the reader needs; Zinsser's surprising last lines belong to essays.

Keep paragraphs to six lines or fewer.

## Hard bans

The table distinguishes mechanical failures, checker candidates, and manual review. **Fail** is an automatic block once the checker detects or a reviewer confirms the pattern. **Flag** is a checker candidate that requires human confirmation. **Manual** requires manual review. These statuses describe how a violation gets detected and do not imply that the checker detects every violation. Confirmed hard-ban violations remain zero-tolerance regardless of status.

| Pattern | Checker status | Action |
| --- | --- | --- |
| Em dash, and inline `--` used as a dash. En dash is allowed | Fail | A comma, a colon, or two sentences |
| Negated parallel: `it is not X, it is Y` or `X, not Y` | Fail | State the claim once, positively |
| `To be clear` / `Let's be clear` | Fail | Delete. The sentence is the clarification |
| `It is worth noting that` / `It is important to note` | Fail | Delete and state the thing |
| Dead metaphors: `load-bearing`, `smoking gun`, `moving the needle`, `north star`, `secret sauce`, `low-hanging fruit`, `boiling the ocean` | Fail | Describe the mechanism plainly |
| Vague praise: `robust`, `seamless`, `powerful`, `elegant`, `delightful`, `blazing fast` | Fail | A measurement, or nothing |
| Hype intensifiers: `truly`, `genuinely`, `incredibly`, `extremely`, `vastly` | Fail | Delete, or give the number |
| `simply` / `just` used to minimize difficulty | Fail | Delete |
| Rhetorical question followed by its answer | Fail | Assert the answer |
| One-word emphasis fragments: `Simple.` `Wrong.` `Exactly.` | Fail | Fold into the adjacent sentence |
| Verbless fragment as an aside, including inside list items, table cells, and steps: `No change to handle_output.` `Zero downtime.` `No changes.` | Fail | Fold into the adjacent sentence with a verb |
| Triadic emphasis fragment: `One lockfile, one resolver, no drift.` | Fail | Fold into the causal sentence it decorates |
| Verbless three-part list standing as a sentence: `Faster builds, fewer flakes, smaller images.` | Flag | Fold into the causal sentence it decorates |
| Figurative coinage in a technical register: `feed the coordinates back in`, `closing the loop`, `learned the hard way` | Manual | Describe the mechanism in the domain's own words. The dead-metaphor list is examples, never a boundary |
| Opening that restates the question | Manual | Start with the answer |
| Closing summary that repeats the body | Manual | Stop at the last substantive point |
| Closing generalization or moral | Manual | Off by default. Write one only when the author asks |
| Closing exhortation: `Go build something` | Fail | Delete |
| Exclamation points, emojis, cheery closings | Fail | Delete; state it plainly |
| Rule-of-three list whose third item is filler | Manual | Keep only the items that carry facts |
| Passive voice with no agent | Fail | Name the actor. Test by appending "by zombies" |
| Announcement sentence: abstract subject plus evaluative predicate, before the facts | Flag | Cut it. Open with the fact |
| Maxim restating the point as a general principle | Flag | Cut it. The preceding sentence carried it |
| Verdict words scoring a decision: `the right trade`, `the correct choice`, `a reasonable tradeoff` | Flag | State the cost and who absorbs it |
| Finality verb applied to unmerged work: `#412 establishes`, `the draft spec settles` | Flag | Reserve `establishes`, `settles`, `specifies`, `chose` for merged or shipped work. Name the status (merged, open, draft) in the sentence that cites the reference |
| Absence claim without a search scope: `no runbook exists` | Manual | State where you looked: `I found no runbook in the wiki or the repo's docs/` |
| Compliance narration: `matching the issue's outcome`, `satisfying the requirement` | Flag | Delete. Meeting the requirement is shown by the content, never claimed alongside it |
| Run of three loose sentences joined by `, so`, `, which`, `, and`, `, while`, or `, but` | Flag | Recast one or two as simple sentences or with a semicolon |

## Fat-word substitutions

| Fat | Lean |
| --- | --- |
| `utilize`, `leverage` | use |
| `delve into` | examine |
| `in order to` | to |
| `prior to` | before |
| `subsequent to` | after |
| `due to the fact that` | because |
| `in the event that` | if |
| `at this point in time` | now |
| `a number of` | some, or the count |
| `is able to`, `has the ability to` | can |
| `in terms of` | for, or delete |
| `the fact that` | that, or delete |

## Numeric targets

Budgets rather than gates. A warning may be accepted with a stated reason.

| Measure | Target |
| --- | --- |
| Median sentence length | 14 to 22 words. Below 14 suggests chopped causation |
| p95 sentence length | 40 words or fewer |
| Sentences over 40 words | 0 |
| Subordinate clauses per sentence | 2 or fewer |
| Words between subject and verb | 10 or fewer |
| Words of three or more syllables | 20 percent or fewer. The primary diction signal |
| Monosyllable share | 50 percent or more. Weak signal, since domain nouns depress it |
| Nominalization density | 4 percent of words or fewer |
| Weasel words per document | 1 or fewer (house budget; Bernoff's own target is a 90 percent cut). A named gap does not count |
| Adverbs ending in -ly | 15 per thousand words or fewer |
| Colon constructions | 12 per thousand words or fewer, excluding list introductions |
| Distinctive phrase repeated across sentences | 0. Vary the phrasing or delete the repeat |
| Headings per 500 words | 3 or fewer |
| Paragraph length | 6 lines or fewer |
| Cut from first draft | 20 to 50 percent (Zinsser: most first drafts can lose half) |

Labeled gaps do not count against the budget. See Uncertainty below.

## Judgment rules

No regex catches these.

**Register calibration.** Write for the declared audience rather than for the most technical possible reader. `schema-handling code` is aimed at the wrong reader, which is a different problem from a banned phrase.

**Vocabulary fidelity.** Use the subject domain's own terms. Before attaching a qualifier or coining a compound (`cloud-native footprint`, `reference topology`, `tier-two consumers`), check that the source material uses it; if it does not, either use the domain's term or define the coinage at first use. A reader who asks "is that a real term?" has caught a defect. Use jargon when it is the word practitioners and the official docs use, such as `p99` or `connection pool`. Do not borrow a word that sounds technical but belongs to another field, such as `runway` for a minimum or `blackout` for a host failing. Search the domain's docs when unsure, and use plain words when the domain has no term.

**Caveat placement.** Caveats have a budget, roughly one per section. Spend it at the single point where an informed reader would otherwise stop trusting the writer. Front-loading caveats reads as hedging.

**Frontload.** Bernoff says the reader gives you tens of seconds. The claim goes in the first sentence, before any setup. An audit or investigation may open with one sentence of the symptom when the finding only makes sense against it, and the finding follows in the next sentence.

**Answer first, background last.** Order a document by what the reader needs to act. The answer and what to do come first; the reasoning, background, and history follow, and the deep detail and sources come last. A reader who stops after the first sections should still know the decision and why. Section names and counts follow the content, so no document needs a fixed set of sections.

**Time zones.** Name the zone on every clock time. Which zone to use depends on the reader and the data, so follow the requester's choice and ask when the choice changes what the reader does.

**Current state.** Describe how things work now once, where the problem is stated. Don't open every point with "Today" or "Currently."

**Tables, lists, and prose.** Use a table when three or more items share two or more attributes, such as a rollout with wave, team, job count, and start date, or a set of changes with the problem and the reason for each. Use a plain list when each item is one sentence, a numbered list for a sequence, and prose for one or two items. Chronologies are tables of time and event. Avoid tables in chat, where they render badly.

**Plain sentences by default.** Prefer ordinary sentences and paragraphs to paragraphs that open with a bolded sentence. A bold lead phrase is fine on a list item when it labels the item, but it should not be the default way to structure prose.

**State the next step plainly.** Name what happens next and by when, such as "Approval is needed by April 7 to start the first wave." Do not address the reader with formal or deferential requests such as "I ask leadership to accept" or "we ask the manager to approve."

**Opinions.** State them as opinions, once, without apology or repetition.

**Decision status.** Distinguish a recommendation, an open question, and a confirmed decision. Do not imply agreement or finality the evidence does not establish. An option under review stays an option even when a reviewer favors it or a partial implementation exists.

**Scope discipline.** Answer the question asked. Add adjacent context only when it changes the answer or prevents a material mistake. Raise separate concerns separately.

**Correction proportion.** State a contradiction when it affects correctness, action, or how a reader will interpret the record later. Let minor wording imprecision pass when correcting it costs more than it fixes.

**Referent clarity.** Use a pronoun when the referent is obvious. Repeat the noun when the pronoun could plausibly attach to more than one object, decision, or system in the surrounding sentences.

## Writing contract

Declare this contract before drafting. The contract chooses the document's job before sentence-level rules shape its prose.

| Field | Required declaration |
| --- | --- |
| Register | One row from Register profiles below |
| Audience | The specific reader or group and their working knowledge |
| Exposure | Private, team-visible, or broadly visible |
| Reader action | Decide, align, approve, investigate, or reflect |

Do not draft until these fields are clear. A technically clean document that asks the reader to do the wrong thing has failed.

The contract, the claim ledger, claim classifications, and verification records live in research notes, never in the deliverable. The reader document opens with the subject, the conclusion, and the next action in plain prose, with no metadata header. Add a header or an evidence appendix only when the reader asks for one or the document's purpose requires it. State material uncertainty in ordinary language, as in "the database team needs to confirm the backup retention period," so the reader gets the action without the classification scheme.

The same goes for process notes. What the writer checked, what could not be verified, formatting problems, and contingencies the requester ruled out go to the requester in the reply, never into the document. The deliverable carries only the final content, so a ticket states what the code does and leaves out how the writer confirmed it. Methodology that the reader needs to trust the data stays.

### Claim status

Classify every externally checkable claim before writing it.

| Status | Rule |
| --- | --- |
| Verified | Cite the source close to the claim. State it directly. |
| Source-assumed | Name the source and limit the claim to what it establishes. Do not extend an example into a pattern. |
| Unknown | State the gap, the search scope already checked when relevant, and the action or evidence that would resolve it. |

Never infer intent, competence, cause, frequency, or generality from evidence that does not establish it. A claim that cannot survive this test comes out.

### Social-risk control

For internal writing, critique observable incentives, decisions, mechanisms, and outcomes. Do not infer private motives, competence, or character.

The wider the exposure, the less a reader should be able to identify a person, team, or framework from the draft. A broadly visible critique must remain defensible to a reader who knows none of the backstory.

### Document shape

Use the smallest shape that gives the reader what the register row requires. Do not add a section merely to look complete. Add it only when it changes the reader's decision, action, or understanding of scope.

## Register profiles

Declare the audience before drafting, then follow the row.

| Register | Rules |
| --- | --- |
| Reference docs | Second person, present tense, active voice, no figurative language, no personality |
| How-to and tutorials | Second person imperative, one action per step, state the result of each step |
| Engineering blog | Claim in sentence one, few caveats, casual but not chatty, opinions allowed, concrete examples over abstraction |
| Organizational and political posts | First person, name incentives plainly, no moralizing, spend the caveat budget where the reader would push back |
| Postmortems and RCAs | Declarative and plain. One fact per sentence, each naming an actor and an action, including in the chronology (write `I merged the change` where a draft says `the change was merged`). The author owns their own defects in first person without ceremony, and the summary stays matter-of-fact rather than formal or apologetic. Describe other people's actions by role and what they did, without judging motive. The chronology is a table of time and event in one time zone. Avoid rhythmic emphasis, short verdicts, and asides |
| Audits and investigations | Open with the finding, or with one sentence of the symptom when the finding needs it. Give the method in a sentence or two, then the findings ranked by impact with their evidence, then what you plan to do and in what order. Use "I" for who measured what |
| Slack proposals and RFCs | Soft framing. No `Heads up`. State the option, the tradeoff, and what you plan to do absent objection. When you need an answer, ask one concrete question and name the next step. Write two or three short paragraphs separated by blank lines rather than one block, and link a document for anything longer |
| Sensitive internal critique | Describe the observable pattern, its effect on the work, and the question it raises for the system. Name no individual targets and make no claims about motive |
| Spikes and technical proposals | Lead with the recommendation and its reason in one or two sentences. Then give each change with the problem it fixes and why it fixes it, then the plan, then the reasoning and sources. Describe decisions and limits in prose, and leave configuration and code to the implementation ticket. Plan steps name who does what by when. Use "we" or a neutral voice |
| Jira tickets | A title that states the problem, then a few sentences a new teammate can pick up: one line of context with a link, the problem with its evidence, where it lives in the code, and the suggested approach as a sentence in the body rather than its own section. Neutral voice, though first person fits work the writer did (`I reproduced it locally with...`). Acceptance criteria are short, checkable outcomes, one per line, and only as many as the change needs |
| Design proposals and applications | Use "we" or a neutral voice, and keep "I" for the writer's own analysis. Own every decision: state the choice, the reason, and the evidence. For an open fork, give one default, one fallback, and the gate that switches them. Defer to reviewers on open questions without deference language such as `not mine to preempt` or `that is my lean` |
| Chat reply | Lead with the answer in plain words. Explain enough for the reader to build a mental model of the situation, and skip only the background they have shown they already know. Preserve decision status, answer what was asked, and correct only the point at issue |
| Docstrings | Google convention, non-imperative phrasing, one line where one line suffices |

## Self-audit gate

Run all thirteen before emitting a document. The first changes content, so it goes first. A chat reply skips the claim ledger in gate 1 and the research-notes record in gate 12, and still sources every specific.

1. Sourcing. Every specific traces to a source or to author knowledge. Delete or label the rest. When the document maintains a claim ledger, this gate means ledger coverage: every sentence carrying a number, quote, code identifier, or issue reference has an entry.
2. Frontload. Sentence one carries the claim.
3. Hard bans. Zero confirmed hard-ban hits.
4. Deletion test on every sentence, regardless of length. Cut announcements, maxims, and appended verdicts.
5. Clause bounds and subject-verb distance.
6. Diction. Long-word share and nominalization density, checking that long words are domain terms rather than fat words.
7. Weasel count, excluding named gaps. For each hedge: look it up, state it flat, name the gap, or delete.
8. Paragraph unit. One idea, six lines or fewer, emphatic word last.
9. Structural audit. Each section has one purpose, each argument appears in one section, every implementation detail supports a stated decision, and the plan summarizes scope without reopening design arguments.
10. Cut pass. Remove 20 to 50 percent of the draft.
11. Register match against the declared profile.
12. Citation check. Fetch every cited link, confirm the target exists and supports the claim it is attached to, and record the target's title and the supported claim in the research notes. A link without a record does not ship.
13. Publication re-read. After writing to an external destination, re-read the rendered artifact and walk every sentence, identifier, and link for truncation or damage. Repeat after every subsequent edit or format conversion. A clean checker run is not publication approval.

Then run `scripts/style_check.py` on the file, which fails on bans and warns on ranges. Run it again after every subsequent edit to the document, since fixes routinely introduce new violations. Treat every Flag as blocking until a human confirms or dismisses it; the checker exits 2 while Flags remain, and only a human decision justifies `--accept-flags`.

Add `--reference` when the document is a rulebook, specification, or checklist. That form is scanned rather than read, so short imperative rule statements and dense headings are features of it. Prose written to be read straight through takes the default.

The checker reports Fail, Flag, and Manual labels that match the table; a human confirms each Flag finding and performs each Manual review. It scans headings and table cells for bans and weasels, checks each list item as its own block so a fragment such as "No changes." inside a step is flagged, skips bold step labels and unpunctuated entries such as source names, warns when a prose paragraph exceeds `MAX_PARAGRAPH_LINES`, and prints a coverage line naming the regions it excluded (code fences, blockquotes, quoted spans), which a human scans by eye. It is read-only and does not claim to rewrite or protect literals. It cannot tell whether a flagged sentence is empty, only that it fits the shape of one.

## House deviations

These rules are stricter than the sources they came from. Keep them, and know they are ours.

**The em dash ban.** En dashes are allowed for ranges and parenthetical punctuation; the checker bans only the em dash and inline double hyphen. Strunk and White permit the dash as "a mark of separation stronger than a comma, less formal than a colon, and more relaxed than parentheses," with the instruction to "use a dash only when a more common mark of punctuation seems inadequate." We ban it outright, because heavy em dash use is a strong marker of machine prose and this register rarely builds sentences complex enough to need one.

**Fat words as hard bans.** Bernoff and Zinsser both tell writers to prefer the short word. The substitution list is ours, and we enforce it mechanically.

**Rhythm limits.** Strunk and White allow a fragment when its emphasis is earned (Rule 6), and Zinsser wants short sentences to predominate. Our limits on fragments stand anyway, because a machine's fragments rarely earn their emphasis. Short complete sentences that carry a fact are fine.

None of the three sources was trying to make prose sound less like a machine, because in 1959, 1976, and 2016 that was not a failure mode, so every rule aimed at machine tics is ours.

## Changing this skill

The owner may change any rule. Before you add or edit a rule, exemplar, fixture, or checker pattern, read `references/maintaining.md`. Every change must hold for documents outside the session that prompted it, and nothing that identifies an employer, client, colleague, or internal system goes into this repository.

## References

- `references/exemplars.md` for paired rewrites by register.
- `references/source_rules.md` for the underlying rules in the authors' own words.
- `references/maintaining.md` for how to change this skill without fitting it to one session.
