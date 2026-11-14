# Checker fixtures

Run from the skill root:

```sh
python3 scripts/ledger_check.py tests/bad_ledger.md
python3 scripts/ledger_check.py tests/good_ledger.md
```

Expected exits are 1 and 0, with 11 problems reported for `bad_ledger.md`.

`bad_ledger.md` has nine rows. The first six carry one defect each: an unknown tier, an F2 absence claim with no scope or stopping rule, an F3 row whose Recheck is "None", an empty Claim, an empty Evidence cell, and a Completeness value outside the four allowed words. The last three test absence detection outside software and with modifier words between the negation and the noun:

- "No maintained open-source tool ..." (F2, no scope) reports one problem. Before the fix, the two modifiers hid it.
- "No published study ..." (tiered F1) reports two: wrong tier and no scope.
- "Nothing like this provision exists in the state code" (tiered F3) reports two: wrong tier and no scope.

`good_ledger.md` is the same table repaired, plus one F1 row, "The probe saw no errors in 400 requests". That row names no existence noun, so a measured zero does not trigger the absence rule.
