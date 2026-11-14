"""Checks evidence-ledger tables in a Markdown file.

A ledger is any Markdown table whose header contains a "Claim" column and a
"Tier" column. Each row must have a non-empty Claim, a Tier in F1/F2/F3,
non-empty Evidence and Recheck cells, and a Completeness cell that starts with
Complete, Partial, Blocked, or Pending. F3 rows need a Recheck that names an
execution (not "none" or empty). A row whose claim asserts that something does
not exist (a tool, study, dataset, rule, record, and so on) must be tiered F2
and must name scope and a stopping rule somewhere in the row; evidence-tiering
treats an absence as a bounded conclusion, never as an observation or an
untested behavior.

Exit 0 when every row passes, 1 otherwise. Usage: ledger_check.py FILE [FILE ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TIERS = {"F1", "F2", "F3"}
COMPLETENESS = ("complete", "partial", "blocked", "pending")
# Existence-style absence claims only. A measurement such as "no errors in 400
# requests" names no existence noun, so it does not match. Up to four modifier
# words may sit between the negation and the noun ("no maintained open-source tool").
ABSENCE_NOUNS = (
    r"(?:tool|system|product|library|package|implementation|project|repo\w*|service|vendor"
    r"|competitor|alternative|paper|study|studies|survey|review|report|dataset|benchmark"
    r"|standard|law|statute|rule|regulation|policy|record|source|document|precedent)s?"
)
ABSENCE_WORDS = re.compile(
    r"\bno\b(?:\s+[\w\-`'.]+){0,4}?\s+" + ABSENCE_NOUNS + r"\b"
    r"|\bnone (?:found|exists?)\b|\bnot found\b|\bnothing (?:like|found|exists|similar)\b"
    r"|\bdoes not exist\b|\bno one (?:has|does|ships|offers)\b|\bnobody (?:has|does|ships|offers)\b"
    r"|\bthere (?:is|are) no\b",
    re.IGNORECASE,
)
SCOPE_WORDS = re.compile(r"\b(scope|searched|queries|stopping rule|examined|bounded)\b", re.IGNORECASE)


def split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def find_column(header: list[str], name: str) -> int | None:
    for i, cell in enumerate(header):
        if name.lower() in cell.lower():
            return i
    return None


def check_file(path: Path) -> list[str]:
    problems: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    rows_seen = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|\s*-", lines[i + 1]):
            header = split_row(line)
            claim_col = find_column(header, "claim")
            tier_col = find_column(header, "tier")
            if claim_col is None or tier_col is None:
                i += 1
                continue
            evidence_col = find_column(header, "evidence")
            recheck_col = find_column(header, "recheck")
            completeness_col = find_column(header, "completeness")
            for col_name, col in (("Evidence", evidence_col), ("Recheck", recheck_col), ("Completeness", completeness_col)):
                if col is None:
                    problems.append(f"{path}:{i + 1}: ledger header lacks a {col_name} column")
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = split_row(lines[i])
                rows_seen += 1
                loc = f"{path}:{i + 1}"

                def cell(col: int | None) -> str:
                    return row[col] if col is not None and col < len(row) else ""

                claim = cell(claim_col)
                tier = cell(tier_col).split()[0] if cell(tier_col) else ""
                evidence = cell(evidence_col)
                recheck = cell(recheck_col)
                completeness = cell(completeness_col)
                if not claim:
                    problems.append(f"{loc}: empty Claim")
                if tier not in TIERS:
                    problems.append(f"{loc}: Tier must start with F1, F2, or F3 (got {tier!r})")
                if not evidence:
                    problems.append(f"{loc}: empty Evidence")
                if not recheck:
                    problems.append(f"{loc}: empty Recheck")
                if not completeness.lower().startswith(COMPLETENESS):
                    problems.append(f"{loc}: Completeness must start with Complete, Partial, Blocked, or Pending (got {completeness!r})")
                if tier == "F3" and (not recheck or recheck.lower().startswith("none")):
                    problems.append(f"{loc}: F3 row must name the execution that would settle it")
                if ABSENCE_WORDS.search(claim):
                    if tier in TIERS and tier != "F2":
                        problems.append(f"{loc}: absence claim tiered {tier}; an absence is F2 with scope, or it is unsupported")
                    if not SCOPE_WORDS.search(" ".join(row)):
                        problems.append(f"{loc}: absence claim lacks scope or stopping rule words")
                i += 1
            continue
        i += 1
    if rows_seen == 0:
        problems.append(f"{path}: no ledger table found (header needs Claim and Tier columns)")
    return problems


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    all_problems: list[str] = []
    for arg in argv:
        all_problems.extend(check_file(Path(arg)))
    for p in all_problems:
        print(p)
    if all_problems:
        print(f"{len(all_problems)} problem(s)")
        return 1
    print("ledger ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
