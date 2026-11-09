# Checker fixtures

Run from the skill root with these exact commands:

```sh
python3 scripts/style_check.py tests/bad_prose.md
python3 scripts/style_check.py tests/good_prose.md
python3 scripts/style_check.py --reference --accept-flags SKILL.md references/*.md
python3 scripts/style_check.py tests/dash_and_paragraph.md
python3 scripts/style_check.py tests/forbidden_dashes.md
python3 scripts/style_check.py tests/new_rules.md
python3 scripts/style_check.py tests/ban_in_heading.md
python3 scripts/style_check.py tests/ban_in_table.md
python3 scripts/style_check.py tests/quoted_prose.md
python3 scripts/style_check.py tests/flags_only.md
python3 scripts/style_check.py --accept-flags tests/flags_only.md
python3 scripts/style_check.py tests/weasel_offset.md
python3 scripts/style_check.py tests/list_fragments.md
python3 scripts/style_check.py tests/triad_flag.md
python3 scripts/style_check.py tests/loose_run.md
python3 scripts/style_check.py tests/exclamation.md
python3 scripts/style_check.py tests/month_may.md
python3 scripts/style_check.py tests/pronoun_subject.md
```

Expected exits are 1, 2, 0, 2, 1, 1, 1, 1, 0, 2, 0, 0, 2, 2, 2, 1, 0, and 0.

Exit semantics: 1 means a hard ban fired, 2 means Flags remain without a recorded human disposition, 0 means neither. `--accept-flags` records that a human confirmed or dismissed each Flag; the flags_only pair proves it converts exit 2 to 0. The reference-set command carries `--accept-flags` because the guide and exemplars quote flaggable shapes as teaching material, a standing human disposition.

Per fixture: `dash_and_paragraph.md` proves an en dash passes, a seven-line paragraph warns, and its Flags now exit 2. `forbidden_dashes.md` proves the em dash and inline double hyphen still fail. `new_rules.md` proves the triadic fragment and trailing negated parallels fail and the colon-density and repeated-phrase advisories fire. `ban_in_heading.md` proves a banned word in a heading fails. `ban_in_table.md` proves a banned word in a table cell fails. `quoted_prose.md` proves a quoted literal stays masked and appears in the coverage line instead of failing. `weasel_offset.md` proves a labeled gap exempts only its own sentence: its two hedges in other sentences exceed the budget of one and warn, where the old document-wide subtraction hid them. `list_fragments.md` proves a fragment such as "No changes." inside a numbered step is flagged, while bold step labels and unpunctuated source entries are skipped. `triad_flag.md` proves a verbless three-part list that does not open with One, No, Zero, or Every is flagged for review rather than failed. `loose_run.md` proves three loose sentences in a row (Strunk and White's Rule 18) raise a Flag. `exclamation.md` proves an exclamation point fails. `month_may.md` proves the month May does not count as the weasel word "may". `pronoun_subject.md` proves a long sentence that opens "I plan to" is not flagged for subject-verb distance, since the verb follows the pronoun.

Fixture nouns follow `references/maintaining.md`: generic subjects, no real identifiers.

The checker is read-only; these fixtures do not claim protected-literal rewrite enforcement.
