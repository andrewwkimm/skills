# Changing this skill

This skill describes one writer's style, and it has to hold in any job, field, or company. Feedback from a session is evidence about that style. The nouns of the session are not, so they stay out of the skill.

## Turn feedback into a rule

1. State the rule without any noun from the session that prompted it. If the rule cannot be stated that way, it is a note about one document, and it belongs in the reply to the requester.
2. Name two documents from unrelated fields, such as a runbook and a blog post, where the rule would catch a defect. If you cannot name them, leave the rule out.
3. Search the skill for a rule that already covers the case. Extend that rule rather than adding a sibling, and resolve any contradiction in the same change.
4. Prefer extending a register row or a judgment rule over adding a section, mode, or row. A new row needs the owner to confirm they write that kind of document more than once.

## Examples, exemplars, and fixtures

Keep the shape of the source sentence and replace every noun in it: products, teams, tools, people, clients, ticket keys, numbers, dates, and places. The structure of a sentence is the signal worth learning, and its nouns are what make an example overfit.

This repository is public. Never write a ticket key, an internal URL, an employer, a client, a colleague, an internal system name, or the date or figures of a real incident into any file. A public term that reads the same at any company, such as `connection pool` or `p99`, is fine.

An AFTER may add a fact only where the vagueness of the BEFORE stood in for a fact the writer had, and its note says so. Any other added detail is invented, which trades one defect for a worse one.

Use at most one exemplar per source document or session, and vary the field across exemplars so no domain dominates. Before adding one, scan the existing exemplars for the same field. A rule's inline example and its exemplar use different cases, so the guide never repeats one example in two places.

A fixture tests one checker behavior, so it can be narrow, but its nouns follow the same rules.

## Checker patterns

Never add an exemption, a lookahead, or a word-list entry whose only purpose is to let one document pass. Fix the pattern, or accept the warning with a stated reason.

Write each pattern for the general shape of the defect. When the general shape produces false positives, keep the precise form as a Fail and add the general form as a Flag. Every pattern change gets a fixture, and `tests/README.md` lists its expected exit.

## Documents the owner points to

The owner may share documents they wrote as examples of the target style. Learn their order, voice, and what they leave out, and copy none of their sentences, facts, or section names. Treat them as good and imperfect: a trait becomes a rule when the owner confirms it or when it appears in more than one of their documents.

## Testing a change

Before adopting a change larger than a wording fix, run a blind comparison. Give the old and new versions of the skill to separate writers, have each write the prompts in `../technical-writing-style-history/eval-prompts/`, shuffle the outputs under neutral labels for each prompt, and let the owner pick the best one without knowing which version wrote it. Adopt the change only if it wins or ties. The 2026-11-09 comparison showed that a rewrite built on sound sources can still lose to the version it replaces, so the test is worth the few minutes it costs.

## Before finishing

Search the changed files for the session's nouns, for ticket keys with `grep -nE '[A-Z]{2,}-[0-9]+'`, and for internal domains and names. Run every command in `tests/README.md` and compare the exits to the expected list. Record the change in `../technical-writing-style-history/CHANGES-YYYY-MM-DD.md` with what changed and the general reason, and describe the prompting case without its identifying details.
