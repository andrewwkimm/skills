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

Three rules follow from that.

Quote error messages, log lines, and code verbatim. A paraphrase that reads clean has invented precision the source did not have.

Never invent detail around a real fact. Confirming that a regression test exists licenses no claim about how long it runs. The surrounding detail feels safe because the core fact is true, which is what makes it easy to write.

Prefer an honest vague sentence to a specific invented one. "The check runs on every commit" beats "the check adds 40 milliseconds" when nobody measured it. Concreteness is the goal of this style, so this style creates constant pressure to fabricate numbers. Expect that pressure and refuse it.

## Uncertainty

Not knowing something splits four ways, and collapsing them is what produces mush.

**The fact exists somewhere, and you have not looked.** Look it up. Bernoff is harshest here, calling it laziness: writers use weasel words "to avoid the necessary research to get precise answers." His rewrite of a United Airlines letter replaces "millions of people" with "140 million trips with us last year," and he notes that the figure "took me 15 seconds to look it up." Any hedge a search would dissolve is not honesty. Run this test before labeling anything unknown.

**You hold a judgment you cannot prove.** State it flat and own it. The qualifier buys nothing, because "your readers will hold you responsible regardless of whether you said the exceptions happen 'rarely' or didn't mention them at all, so you might as well be bold." Strip `I think`, `it seems to me`, `in my experience`, and `from what I have seen` off any claim you actually hold. That advice aims at the ritual self-deprecation writers wrap around stances they hold. It says nothing about concealing a fact you lack.

Removing a hedge never licenses keeping the claim at its original size. When a sentence cannot survive flat, shrink the claim along one of three axes until it can: the subject (`the maintainers already chose` becomes `#1286 added the columns`), the timeframe (`this is settled` becomes `as of the April release`), or the source (`no metrics doc exists` becomes `I found no metrics doc in docs/ or the README`). Deleting the qualifier while keeping the claim converts a hedge defect into a factual one, which is a worse trade.

**The fact does not exist, because nobody measured it.** Write the gap as its own declarative sentence and say what would close it. "We have not measured p99 latency under retry storms. A load test against the staging gateway would settle it." That is two facts and an action, so it does not read as weaseling. A hedge attaches doubt to a claim you are still making, which weakens the claim and adds nothing.

**You think you are probably wrong.** Delete the sentence. Bernoff: "If you're afraid of generalizing—if you think there's a good chance you're wrong—then don't generalize." A claim at sixty percent confidence comes out rather than getting a label.

Where a number carries provenance the reader needs, put it in parentheses after the claim so the claim itself stays direct. Bernoff does this when he invents figures to demonstrate a rewrite: "(I made these numbers up; Pakes would have to substitute the actual data.)"

### When the quantity is not the point

A weak generalization survives when the writer reaches for a count the argument never needed. Bernoff's fix is to name the subject rather than the quantity: "Don't tell us that many people do something, tell us which people do it."

His Bernie Sanders example shows the move. "A growing number of communities do not trust the police and law enforcement officers have become disconnected from the communities they are sworn to protect" becomes "In communities where people don't trust the police, law enforcement officers lack a connection with those they are sworn to protect." He notes that the original "doesn't really quantify the problem" and that "the quantity isn't relevant anyway."

So "most interviewees cannot pass the technical screen" does not need softening. It needs a subject the evidence covers: "five of the seven recruiter-pipeline candidates last quarter failed the technical screen" (fictional count, for illustration). That names who, stays inside what the writer observed, and still makes the point about the pipeline. Widening instead to "candidates from the recruiter pipeline cannot pass" trades the hedge for a claim about the whole group that seven interviews never established, which is the worse defect. When the flat sentence overreaches, shrink the subject, the timeframe, or the source until it holds.

Comparisons still need "less" and "more," and an unstable explosive still gets called "extremely unstable," so the target was never zero qualifiers. His target is pruning "as many of them as possible," and his stated goal across all three habits is a ninety percent cut.

## Target voice

Plain, specific, and sourced. The writer knows the subject, respects the reader's time, and has no interest in sounding impressive. Judgments are stated flat and owned. Gaps in the evidence are named in their own sentence.

## Diction

Word origin predicts machine prose better than sentence length does. Orwell's rewrite of a passage from Ecclesiastes is 38 words against the original's 49, so it wins on brevity and loses on every other axis, because the short version runs 39 percent long Latinate words against the original's 6 percent.

Prefer the short Anglo-Saxon word. Zinsser's rule is to use short words that say what you mean and get rid of the Latin.

Kill nominalizations. A nominalization buries a verb inside a noun, then needs a weak verb to carry the sentence. `make a decision` becomes decide. `provide a solution` becomes solve. `perform an analysis` becomes analyze. `the implementation of` becomes we built.

Do not stack nouns. Zinsser calls it creeping nounism, stringing two or three nouns where one noun or a verb will do. Any compound noun phrase must survive a plain-clause rewrite test: if `schema-handling code` reads better as "the code that reads the file layout," rewrite it. Keep the compound when it is the shortest accurate phrasing.

Long-word share is the reliable signal, and monosyllable share is the weak one. Technical prose carries domain nouns that have no short form, so a piece about a rate limiter pays a syllable tax no rewrite can remove. Measured across book prose and technical drafts, long-word share separates jargon from plain writing by a wide margin. A deliberately bad jargon paragraph runs 60 percent long words against 5 to 13 percent for plain prose, while its monosyllable share sits close to a clean document's. Treat a low monosyllable count as a prompt to check whether the long words are domain terms or fat words, since only the second kind is a defect.

## Sentence construction

There is no minimum sentence length, only a content test.

**The deletion test.** Every sentence must carry a fact, a decision, a material uncertainty, or a reader action that disappears if you delete it. If deleting it costs only emphasis or framing, merge it into a neighbor or cut it. Length is not the signal, since an eighteen-word sentence can be pure verdict while a seven-word sentence can carry the only fact in the paragraph. When a short sentence labels a fact without stating its consequence (`Capture is done and conservative.`), the repair is a merge into the sentence that says why the fact matters, never a standalone rewrite.

Failing: "Running both is normal." "Retries multiply through layers." "The failure is not theoretical."

Passing: "The pipeline then deduplicated the results." "A configuration flag limited the change to one client."

**Verdicts.** A verdict evaluates or labels rather than reports, so it fails the deletion test at any length. Three forms, and the same fix each time: cut it and let the facts stand.

*Announcements* label the paragraph before delivering it. "The failure is not theoretical." "The counter is approximate at window boundaries." "The mechanism is simple to state." Cut the announcement and open with the fact, since the reader learns the point faster from the evidence than from a promise of evidence.

*Maxims* restate the reasoning as a general principle after the fact. "A gateway that rejects all traffic during a Redis blip is worse than one that briefly over-admits." "Running both is normal." The preceding sentence already carried the tradeoff, so the maxim converts an argument into a lesson delivered to the reader.

*Appended verdicts* score a decision the sentence already justified. "so the fixed window is the right trade here" adds nothing after the sentence has named the cost and the tolerance. Words like right trade, correct choice, and reasonable tradeoff score the decision instead of reporting it. State the cost and who absorbs it, then stop.

"The fixed window is the right trade" tells the reader your conclusion, where "the writer absorbs a two-millisecond burst" lets them reach it themselves.

**Do not chop causation.** Facts joined by cause belong in one sentence, joined by because, so, or which. Splitting them into three sentences discards the relationship the reader needed. Delete words that carry nothing; never split a sentence that carries something. A 25-word sentence with no waste beats three 8-word sentences that restate each other.

**Clustering limit.** At most one bare simple sentence under nine words per paragraph, never two consecutive.

**The opposite bound.** Longer is fine until it stops being readable in one pass. Four detectable failures: more than two subordinate clauses in one sentence, a relative clause nested inside another, more than ten words between subject and verb, and nested parentheticals.

## Paragraph flow

Make the paragraph the unit of composition, as Strunk and White put it: one idea per paragraph, and a topic sentence that says what the paragraph is for.

Put the emphatic words at the end of the sentence. Put the emphatic sentence at the end of the paragraph.

Every sentence has one job, which is to make the reader want to read the next one. Zinsser's stronger version, that the last sentence of each paragraph should carry a surprise, suits blog posts and essays. It is wrong for a postmortem, where the reader wants the next fact and nothing else.

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
| Verbless fragment as an aside: `No change to handle_output.` `Zero downtime.` | Fail | Fold into the adjacent sentence with a verb |
| Triadic emphasis fragment: `One Secret, one writer, no copies to drift.` | Fail | Fold into the causal sentence it decorates |
| Figurative coinage in a technical register: `feed the coordinates back in`, `closing the loop`, `learned the hard way` | Manual | Describe the mechanism in the domain's own words. The dead-metaphor list is examples, never a boundary |
| Opening that restates the question | Manual | Start with the answer |
| Closing summary that repeats the body | Manual | Stop at the last substantive point |
| Closing generalization or moral | Manual | Off by default. Write one only when the author asks |
| Closing exhortation: `Go build something` | Fail | Delete |
| Rule-of-three list whose third item is filler | Manual | Keep only the items that carry facts |
| Passive voice with no agent | Fail | Name the actor. Test by appending "by zombies" |
| Announcement sentence: abstract subject plus evaluative predicate, before the facts | Flag | Cut it. Open with the fact |
| Maxim restating the point as a general principle | Flag | Cut it. The preceding sentence carried it |
| Verdict words scoring a decision: `the right trade`, `the correct choice`, `a reasonable tradeoff` | Flag | State the cost and who absorbs it |
| Finality verb applied to unmerged work: `#665 establishes`, `the specification settles` | Flag | Reserve `establishes`, `settles`, `specifies`, `chose` for merged or shipped work. Name the status (merged, open, draft) in the sentence that cites the reference |
| Absence claim without a search scope: `no metrics doc exists` | Manual | State where you looked: `I found no metrics doc in docs/ or the README` |
| Compliance narration: `matching the issue's outcome`, `satisfying the requirement` | Flag | Delete. Meeting the requirement is shown by the content, never claimed alongside it |

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
| Weasel words per document | 1 or fewer, per Bernoff. A named gap does not count |
| Adverbs ending in -ly | 15 per thousand words or fewer |
| Colon constructions | 12 per thousand words or fewer, excluding list introductions |
| Distinctive phrase repeated across sentences | 0. Vary the phrasing or delete the repeat |
| Headings per 500 words | 3 or fewer |
| Paragraph length | 6 lines or fewer |
| Cut from first draft | 20 to 50 percent |

Labeled gaps do not count against the budget. See Uncertainty below.

## Judgment rules

No regex catches these.

**Register calibration.** Write for the declared audience rather than for the most technical possible reader. `schema-handling code` is aimed at the wrong reader, which is a different problem from a banned phrase.

**Vocabulary fidelity.** Use the subject domain's own terms. Before attaching a qualifier or coining a compound (`operator-backed lifecycle`, `reference topology`, `edge users`), check that the source material uses it; if it does not, either use the domain's term or define the coinage at first use. A reader who asks "is that a real term?" has caught a defect.

**Caveat placement.** Caveats have a budget, roughly one per section. Spend it at the single point where an informed reader would otherwise stop trusting the writer. Front-loading caveats reads as hedging.

**Frontload.** The reader gives you fifteen seconds. The claim goes in the first sentence, before any setup.

**Opinions.** State them as opinions, once, without apology or repetition.

**Decision status.** Distinguish a recommendation, an open question, and a confirmed decision. Do not imply agreement or finality the evidence does not establish. An option under review stays an option even when a reviewer favors it or a partial implementation exists.

**Scope discipline.** Answer the question asked. Add adjacent context only when it changes the answer or prevents a material mistake. Raise separate concerns separately.

**Correction proportion.** State a contradiction when it affects correctness, action, or how a reader will interpret the record later. Let minor wording imprecision pass when correcting it costs more than it fixes.

**Referent clarity.** Use a pronoun when the referent is obvious. Repeat the noun when the pronoun could plausibly attach to more than one object, decision, or system in the surrounding sentences.

## Writing contract

Declare this contract before drafting. The contract chooses the document's job before sentence-level rules shape its prose.

| Field | Required declaration |
| --- | --- |
| Mode | Evidence memo, decision document, stakeholder message, or sensitive internal critique |
| Audience | The specific reader or group and their working knowledge |
| Exposure | Private, team-visible, or broadly visible |
| Reader action | Decide, align, approve, investigate, or reflect |

Do not draft until these fields are clear. A technically clean document that asks the reader to do the wrong thing has failed.

The contract, the claim ledger, claim classifications, and verification records live in research notes, never in the deliverable. The reader document opens with the subject, the conclusion, and the next action in plain prose, with no metadata header. Add a header or an evidence appendix only when the reader asks for one or the document's purpose requires it. State material uncertainty in ordinary language, as in "IT needs to confirm the production lockout settings," so the reader gets the action without the classification scheme.

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

### Document shapes

Use the smallest shape that gives the reader what the mode requires.

| Mode | Shape |
| --- | --- |
| Decision document | Conclusion, evidence, scope or path mapping, implementation-impacting exceptions, owners, open questions, sources |
| Technical mapping | Object, current state, target state, owner, exception, source |
| Replacement evaluation | Conclusion, current-vs-proposed comparison that establishes the current system first, decisions, required tests. Capability claims live only in the comparison |
| Stakeholder message | Context, concrete question or proposal, next step |
| Sensitive internal critique | Observable pattern, work or client impact, systemic question. No named targets and no motive claims. |

Do not add a section merely to look complete. Add it only when it changes the reader's decision, action, or understanding of scope.

## Register profiles

Declare the audience before drafting, then follow the row.

| Register | Rules |
| --- | --- |
| Reference docs | Second person, present tense, active voice, no figurative language, no personality |
| How-to and tutorials | Second person imperative, one action per step, state the result of each step |
| Engineering blog | Claim in sentence one, few caveats, casual but not chatty, opinions allowed, concrete examples over abstraction |
| Organizational and political posts | First person, name incentives plainly, no moralizing, spend the caveat budget where the reader would push back |
| Postmortems and RCAs | Declarative and formal. One fact per sentence, each naming an actor and an action. Avoid rhythmic emphasis, short verdicts, and asides. Blameless |
| Slack proposals and RFCs | Soft framing. No `Heads up`, no `I recommend`. State the option, the tradeoff, and what you plan to do absent objection |
| Design proposals and applications | First person. Own every decision: state the choice, the reason, and the evidence. For an open fork, give one default, one fallback, and the gate that switches them. Defer to reviewers on open questions without deference language such as `not mine to preempt` or `that is my lean` |
| Chat reply to a technical peer | Dense. Assume fluency, skip scaffolding, lead with the answer. Preserve decision status, answer only what was asked, and correct only the point at issue |
| Docstrings | Google convention, non-imperative phrasing, one line where one line suffices |

## Self-audit gate

Run all thirteen before emitting. The first changes content, so it goes first.

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

The checker reports Fail, Flag, and Manual labels that match the table; a human confirms each Flag finding and performs each Manual review. It scans headings and table cells for bans and weasels, warns when a prose paragraph exceeds `MAX_PARAGRAPH_LINES`, and prints a coverage line naming the regions it excluded (code fences, blockquotes, quoted spans), which a human scans by eye. It is read-only and does not claim to rewrite or protect literals. It cannot tell whether a flagged sentence is empty, only that it fits the shape of one.

## House deviations

These rules are stricter than the sources they came from. Keep them, and know they are ours.

**The em dash ban.** En dashes are allowed for ranges and parenthetical punctuation; the checker bans only the em dash and inline double hyphen. Strunk and White permit the dash as "a mark of separation stronger than a comma, less formal than a colon, and more relaxed than parentheses," with the instruction to "use a dash only when a more common mark of punctuation seems inadequate." We ban it outright, because heavy em dash use is a strong marker of machine prose and this register rarely builds sentences complex enough to need one.

**Fat words as hard bans.** Bernoff presents his substitution list as habits to break. We enforce it mechanically.

**Rhythm limits.** Zinsser writes that there is no minimum length for a sentence that is acceptable in the eyes of God, and he defends the deliberate fragment. Our limits stand anyway. Where they conflict, the deletion test wins, since his defense assumes the short sentence carries content.

None of the three sources was trying to make prose sound less like a machine, because in 1959, 1976, and 2016 that was not a failure mode, so every rule aimed at machine tics is ours.

## References

- `references/exemplars.md` for paired rewrites by register.
- `references/source_rules.md` for the underlying rules in the authors' own words.
