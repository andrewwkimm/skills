#!/usr/bin/env python3
"""Checks a markdown draft against the technical writing style guide.

Reports Fail violations (exit 1), Flag candidates (exit 2 until a human passes
--accept-flags), and advisory range warnings. Bans and weasels are scanned in
headings and table cells as well as prose. A coverage line names the regions the
checker excluded (code fences, blockquotes, quoted spans, BEFORE blocks) so a
human can review them by eye. Output is capped regardless of input size unless
--all is passed. Uses only the standard library.

Pass --reference for rulebooks and specifications, where short imperative rule
statements and dense headings are features of the form rather than defects.
Pass --accept-flags only after a human has confirmed or dismissed each Flag.
Pass --all to list every hard-ban hit and every Flag, so a reviewer can
dispose of each one; the default report shows a capped sample.
"""

import re
import sys
from pathlib import Path

MAX_HITS_PER_RULE = 4
SHORT_SENTENCE_WORDS = 9
LONG_SENTENCE_WORDS = 40
MAX_SUBJECT_VERB_GAP = 10
MAX_CLAUSES = 2
MIN_MEDIAN_WORDS = 14
MAX_MEDIAN_WORDS = 22
MIN_MONOSYLLABLE_PCT = 50.0
MAX_LONGWORD_PCT = 20.0
MAX_NOMINALIZATION_PCT = 4.0
MAX_WEASELS = 1
MAX_ADVERBS_PER_KWORDS = 15.0
MAX_HEADINGS_PER_500 = 3.0
MAX_PARAGRAPH_LINES = 6
MAX_COLONS_PER_KWORDS = 12.0
REPEAT_NGRAM = 4
LIST_FRAGMENT_WORDS = 5
REFERENCE_MIN_MEDIAN = 9
REFERENCE_MAX_HEADINGS_PER_500 = 8.0

BANS = [
    ("em dash", r"\u2014", "comma, colon, or two sentences"),
    ("inline double hyphen", r"(?<=\w) -- (?=\w)", "comma, colon, or two sentences"),
    ("negated parallel", r"\b(?:is|are|was|were|it's|its)\s+not\s+(?:about\s+)?\w+[,;]\s*(?:it'?s?|but|they'?re)\b|\b\w+,\s+not\s+\w+\b", "state the claim once, positively"),
    ("to be clear", r"\b(?:to|let'?s|let us)\s+be\s+clear\b", "delete"),
    ("worth noting", r"\bit(?:'s| is)\s+(?:worth\s+(?:noting|mentioning)|important\s+to\s+note)\b", "state the thing"),
    ("dead metaphor", r"\b(?:load-bearing|smoking gun|moving the needle|move the needle|north star|secret sauce|low-hanging fruit|boil(?:ing)? the ocean|silver bullet|table stakes)\b", "describe the mechanism"),
    ("vague praise", r"\b(?:robust|seamless(?:ly)?|powerful|elegant|delightful|blazing(?:ly)? fast|best-in-class|world-class|cutting-edge|state-of-the-art)\b", "a measurement, or nothing"),
    ("hype intensifier", r"\b(?:truly|genuinely|incredibly|extremely|vastly|remarkably|profoundly)\b", "delete or give the number"),
    ("minimizing simply", r"\b(?:simply|just)\s+(?:add|run|use|call|set|change|update|do|write|drop)\b", "delete the minimizer"),
    ("rhetorical question", r"(?:^|(?<=[.!?]\s))(?:So\s+)?(?:What|Why|How|Who)\b[^.!?\n]{0,70}\?\s+(?:The\s+answer|Because|It'?s|Simple|Turns out)\b|(?:^|(?<=[.!?]\s))The answer\?", "assert the answer"),
    ("emphasis fragment", r"(?:^|(?<=[.!?]\s))(?:Simple|Wrong|Exactly|Nope|Correct|Not anymore|Never)\.(?:\s|$)", "fold into adjacent sentence"),
    ("triadic fragment", r"(?:^|(?<=[.!?]\s))(?:One|No|Zero|Every)\s+\w+(?:\s+\w+)?,\s+(?:one|no|zero|every)\s+\w+(?:\s+\w+)?,\s+(?:one|no|zero|every)?\s*\w+[^.!?]{0,30}\.(?:\s|$)", "fold into the causal sentence"),
    ("closing exhortation", r"\b(?:go\s+(?:build|ship|try)\s+something|now\s+go\s+\w+|happy\s+(?:coding|hacking|building))\b", "delete"),
    ("fat word", r"\b(?:utiliz(?:e|es|ed|ing|ation)|leverag(?:e|es|ed|ing)|delv(?:e|es|ed|ing)\s+into|in\s+order\s+to|prior\s+to|subsequent\s+to|due\s+to\s+the\s+fact\s+that|in\s+the\s+event\s+that|at\s+this\s+point\s+in\s+time|has\s+the\s+ability\s+to|in\s+terms\s+of)\b", "use the lean form"),
    ("nominalized verb", r"\b(?:make|makes|made|making)\s+a\s+decision\b|\bprovid(?:e|es|ed|ing)\s+a\s+solution\b|\bperform(?:s|ed|ing)?\s+an?\s+analysis\b|\bconduct(?:s|ed|ing)?\s+an?\s+(?:review|investigation)\b|\bgive\s+consideration\s+to\b", "use the verb"),
    ("exclamation point", r"(?<=[A-Za-z0-9)])!(?=\s|$)", "delete; state it plainly"),
    ("agentless passive", r"\b(?:it\s+(?:was|is)\s+(?:decided|determined|observed|noted|found)|(?:mistakes|errors|changes)\s+were\s+made)\b(?!\s+by\b)", "name the actor"),
]

BANS_BY_NAME = {name: pattern for name, pattern, _ in BANS}

WEASELS = (r"\b(?:might|possibly|potentially|arguably|somewhat|fairly|generally|very|quite|pretty\s+much|sort\s+of|kind\s+of"
           r"|typically|often|usually|perhaps|likely|tends?\s+to)\b"
           r"|\brather\s+(?!than\b)"
           r"|\b(?:seems?|appears?)\s+(?!as\b)"
           r"|\b(?-i:may|could)\b")  # lowercase only, so the month May does not count
LABELED_UNKNOWN = r"\b(?:not\s+(?:measured|verified|tested|known|confirmed)|unverified|no\s+data|unmeasured|we\s+don'?t\s+know|has\s+not\s+been\s+measured)\b"
NOMINALIZATION = r"\b\w{4,}(?:tion|tions|ment|ments|ance|ence|ity|ities|ness|sion|sions)\b"

# Concrete nouns that merely end in a nominalizing suffix. A guide about sentences
# is not Latinate because it says "sentence" often.
NOT_NOMINALIZATIONS = frozenset("""
sentence sentences evidence audience reference references science instance instances
difference differences experience experiences sequence sequences consequence
maintenance performance distance balance chance advance alliance appliance
entity entities quantity quality city cities community communities
element elements moment moments comment comments document documents environment
department equipment instrument argument segment increment component components
version versions dimension dimensions extension extensions tension mention
station stations question questions ration nation function functions option options
section sections fraction friction position positions condition conditions
edition tradition addition ambition portion caution motion notion ration
business witness illness wilderness
""".split())
STACKED_MODIFIER = r"\b\w+-(?:specific|level|based|driven|aware|oriented|related|facing)\b"
SUBORDINATOR = r"\b(?:which|that|because|although|though|while|whereas|since|unless|if|when|after|before|whether)\b"


def strip_noise(text):
    """Returns (kept, fragments, excluded): prose lines, table-cell fragments, and excluded-line counts."""
    lines = text.split("\n")
    kept = []
    fragments = []
    excluded = {"code fence": 0, "blockquote": 0, "BEFORE block": 0}
    in_fence = False
    in_before = False
    for i, raw in enumerate(lines, 1):
        label = raw.strip().strip("*").rstrip(":").upper()
        if label == "BEFORE":
            in_before = True
            continue
        if label in {"AFTER", "WHY"} or raw.startswith("#"):
            in_before = False
        if in_before:
            excluded["BEFORE block"] += 1
            continue
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            excluded["code fence"] += 1
            continue
        if in_fence:
            excluded["code fence"] += 1
            continue
        stripped = raw.strip()
        if not stripped:
            kept.append((i, ""))
            continue
        if stripped.startswith(">"):
            excluded["blockquote"] += 1
            continue
        if re.fullmatch(r"[-=*_\s]{3,}", stripped):
            continue
        if stripped.startswith("|"):
            if not re.fullmatch(r"[|\s:\-=]+", stripped):
                for cell in stripped.strip("|").split("|"):
                    cell_text = clean_inline(cell).strip()
                    if cell_text:
                        fragments.append((i, cell_text))
            continue
        kept.append((i, clean_inline(raw)))
    return kept, fragments, excluded


def clean_inline(line):
    """Returns a line with link targets, code spans, and quoted spans masked."""
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"`[^`]{0,80}`", "CODE", line)
    line = re.sub(r"\"[^\"\n]{0,400}\"", "QUOTED", line)
    return line


def prose_only(kept):
    """Returns (prose, item_lines): lines that read as flowing prose, and the line numbers of list items.

    Each list item becomes its own block, so items never merge into one sentence,
    and a leading bold label such as "**Now.**" is dropped before the item is checked.
    """
    out = []
    item_lines = set()
    for num, line in kept:
        s = line.strip()
        if s.startswith("#"):
            continue
        if re.fullmatch(r"\*\*[^*]+\*\*:?", s):
            continue
        is_item = bool(re.match(r"^\s*(?:[-*+]|\d+\.)\s", line))
        s = re.sub(r"^[-*+]\s+", "", s)
        s = re.sub(r"^\d+\.\s+", "", s)
        if is_item:
            s = re.sub(r"^\*\*[^*]+\*\*:?\s*", "", s)
            if not s or is_list_label(s):
                continue
            out.append((num, ""))
            item_lines.add(num)
        out.append((num, s))
    return out, item_lines


def is_list_label(item):
    """Tests whether a list item is a label, such as a source name, rather than a sentence.

    An item with no terminal punctuation reads as a label. A punctuated item is a
    sentence, so fragments like "No changes." stay in scope for the deletion test.
    """
    return not item.rstrip().endswith((".", "!", "?"))


def sentences_with_lines(prose):
    """Returns (sentence, line_number) pairs split on terminal punctuation."""
    buf, start, out = "", None, []
    for num, s in prose:
        if not s:
            if buf.strip():
                out.extend((p, start) for p in split_sentences(buf))
            buf, start = "", None
            continue
        if start is None:
            start = num
        buf += " " + s
    if buf.strip():
        out.extend((p, start) for p in split_sentences(buf))
    return [(s, n) for s, n in out if s]


def split_sentences(block):
    """Returns sentence strings from a text block."""
    block = re.sub(r"\s+", " ", block).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"'`])", block)
    return [p.strip() for p in parts if p.strip()]


def word_list(text):
    """Returns alphabetic word tokens."""
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def syllables(word):
    """Returns an approximate syllable count for one word."""
    w = word.lower().strip("'-")
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    count = len(groups)
    if w.endswith("e") and count > 1 and not w.endswith(("le", "ee", "ye")):
        count -= 1
    return max(count, 1)


def is_bare_simple(sentence):
    """Tests whether a sentence has one clause and no internal punctuation."""
    if re.search(r"[,;:()]", sentence):
        return False
    return not re.search(SUBORDINATOR, sentence, re.I)


def has_concrete_referent(sentence):
    """Tests whether a short sentence names something specific."""
    if re.search(r"\d", sentence):
        return True
    if re.search(r"\bCODE\b", sentence):
        return True
    words = word_list(sentence)
    caps = [w for w in words[1:] if w[0].isupper()]
    return bool(caps)


def back_referring(sentence):
    """Tests whether the sentence opens with a pronoun pointing backward."""
    return bool(re.match(r"^(?:It|This|That|These|Those|They)\b", sentence.strip()))


ANNOUNCEMENT = re.compile(
    r"^(?:The|This|That|A|An|Our)\s+\w+(?:\s+\w+)?\s+"
    r"(?:is|are|was|were|becomes|become|remains|remain)\s+"
    r"(?:not\s+)?(?:theoretical|normal|hard|clear|simple|important|critical|"
    r"obvious|deliberate|approximate|intentional|straightforward|subtle|tricky|"
    r"key|essential|crucial|nontrivial|by\s+design|the\s+\w+)\b",
    re.I,
)

MAXIM = re.compile(
    r"^(?:A|An)\s+\w+\s+(?:that|which|who)\b.{0,140}?"
    r"\b(?:is|are)\s+(?:worse|better|more|less|cheaper|safer|the\s+\w+)\b",
    re.I,
)

VERDICT_WORDS = re.compile(
    r"\b(?:the\s+right\s+(?:trade|tradeoff|call|choice)|"
    r"the\s+correct\s+(?:choice|call|approach)|"
    r"a\s+reasonable\s+(?:trade|tradeoff|compromise)|"
    r"the\s+sensible\s+(?:choice|option))\b",
    re.I,
)

FINALITY_VERB = re.compile(
    r"\b(?:establish(?:es|ed)?|settl(?:es|ed)|specif(?:ies|ied)|chose|decided|confirm(?:s|ed))\b", re.I)
REF_MARKER = re.compile(r"#\d+")
STATUS_WORD = re.compile(
    r"\b(?:merged|closed|shipped|released|landed|open|draft|proposed|pending|stalled)\b", re.I)
# A verbless three-part list standing as its own sentence, such as "Faster builds, fewer flakes,
# smaller images." The Fail ban above catches the One/No/Every form; this general form can match
# a real sentence, so it is a Flag.
TRIAD_FRAGMENT = re.compile(
    r"^[A-Z][\w'-]*(?:\s+[\w'-]+)?,\s+[\w'-]+(?:\s+[\w'-]+)?,\s+(?:and\s+)?[\w'-]+(?:\s+[\w'-]+)?\.$")
# Strunk and White rule 18: a succession of two-clause sentences joined the same way reads as singsong.
LOOSE_JOIN = re.compile(r",\s+(?:so|which|and|but|while)\s", re.I)
LOOSE_RUN = 3
COMPLIANCE = re.compile(
    r"\b(?:matching|satisfying|fulfilling|meeting)\s+the\b[^.!?]{0,50}\b(?:outcome|requirement|criteria|ask)\b", re.I)


def is_announcement(sentence):
    """Tests whether a sentence labels its paragraph instead of reporting a fact."""
    return bool(ANNOUNCEMENT.match(sentence.strip()))


def is_maxim(sentence):
    """Tests whether a sentence restates the point as a general principle."""
    return bool(MAXIM.match(sentence.strip()))


def clause_count(sentence):
    """Returns the number of subordinators in a sentence."""
    return len(re.findall(SUBORDINATOR, sentence, re.I))


def subject_verb_gap(sentence):
    """Returns the word distance from sentence start to the first finite verb."""
    words = word_list(sentence)
    verbs = {"is", "are", "was", "were", "has", "have", "had", "does", "do", "did",
             "will", "can", "could", "should", "would", "must", "may", "might",
             "runs", "ran", "makes", "made", "means", "meant", "gets", "got",
             "becomes", "became", "needs", "needed", "takes", "took", "sits", "sat",
             "beats", "wins", "loses", "reads", "writes", "fails", "passes"}
    # A pronoun subject is followed by its verb, whatever that verb is ("I plan", "we want").
    if len(words) > 1 and words[0].lower() in {"i", "we", "you", "they", "he", "she"}:
        return 1
    for i, w in enumerate(words):
        if w.lower() in verbs or re.fullmatch(r"\w+(?:ed|es|s)", w.lower()):
            return i
    return 0


def is_imperative_rule(sentence):
    """Tests whether a short sentence is an imperative instruction."""
    words = word_list(sentence)
    if not words:
        return False
    starters = {"kill", "delete", "cut", "prefer", "keep", "state", "put", "write",
                "use", "avoid", "run", "name", "label", "merge", "rewrite", "declare",
                "do", "never", "always", "make", "spend", "stop", "report"}
    return words[0].lower() in starters


STOP_NGRAM_WORDS = frozenset("the a an of to in for and or is are with that this on at by".split())


def repeated_ngrams(sents):
    """Returns distinctive REPEAT_NGRAM-word phrases that appear in more than one sentence."""
    seen, first_seen = {}, {}
    for s, _ in sents:
        words = [w.lower() for w in word_list(s)]
        grams = set()
        for i in range(len(words) - REPEAT_NGRAM + 1):
            gram = tuple(words[i:i + REPEAT_NGRAM])
            if sum(1 for w in gram if w in STOP_NGRAM_WORDS) >= REPEAT_NGRAM - 1:
                continue
            grams.add(gram)
            first_seen.setdefault(gram, len(first_seen))
        for gram in grams:
            seen[gram] = seen.get(gram, 0) + 1
    hits = {g: c for g, c in seen.items() if c > 1}
    out, used = [], set()
    # Sorting by count alone leaves ties from one sentence in set order, which varies with PYTHONHASHSEED.
    for gram in sorted(hits, key=lambda g: (-hits[g], first_seen[g])):
        if used & set(gram):
            continue
        used |= set(gram)
        out.append((" ".join(gram), hits[gram]))
    return out[:MAX_HITS_PER_RULE]


def check(path, reference=False):
    """Returns (failures, findings, warnings, stats) for one markdown file."""
    text = Path(path).read_text(encoding="utf-8")
    kept, fragments, excluded = strip_noise(text)
    prose, item_lines = prose_only(kept)
    heading_texts = [(n, l.strip().lstrip("#").strip()) for n, l in kept
                     if l.strip().startswith("#")]
    body = " ".join(s for _, s in prose)
    sents = sentences_with_lines(prose)

    failures = []
    scannable = prose + heading_texts + fragments
    for name, pattern, fix in BANS:
        hits = []
        for num, line in scannable:
            for m in re.finditer(pattern, line, re.I):
                hits.append((num, m.group(0)[:48]))
        if hits:
            failures.append((name, fix, hits, len(hits)))

    findings = []
    prev_short = False
    loose_run = 0
    for s, num in sents:
        loose_run = loose_run + 1 if LOOSE_JOIN.search(s) else 0
        if loose_run == LOOSE_RUN:
            findings.append(("run of loose sentences", num, s[:66]))
        n = len(word_list(s))
        in_item = num in item_lines
        if in_item and not reference and n < LIST_FRAGMENT_WORDS and is_bare_simple(s):
            findings.append(("fragment in a list item", num, s[:66]))
        if not in_item and n < SHORT_SENTENCE_WORDS and is_bare_simple(s):
            if not has_concrete_referent(s) and not (reference and is_imperative_rule(s)):
                findings.append(("deletion test", num, s[:66]))
            if back_referring(s):
                findings.append(("back-referring short sentence", num, s[:66]))
            if prev_short:
                findings.append(("consecutive short sentences", num, s[:66]))
            prev_short = True
        else:
            prev_short = False
        if is_announcement(s):
            findings.append(("announcement sentence", num, s[:66]))
        if is_maxim(s):
            findings.append(("maxim restating the point", num, s[:66]))
        for m in VERDICT_WORDS.finditer(s):
            findings.append((f"verdict word: {m.group(0)}", num, s[:66]))
        if REF_MARKER.search(s) and FINALITY_VERB.search(s) and not STATUS_WORD.search(s):
            findings.append(("finality verb without reference status", num, s[:66]))
        if TRIAD_FRAGMENT.match(s.strip()) and not re.search(BANS_BY_NAME["triadic fragment"], s, re.I):
            findings.append(("three-part fragment", num, s[:66]))
        if COMPLIANCE.search(s):
            findings.append(("compliance narration", num, s[:66]))
        if clause_count(s) > MAX_CLAUSES:
            findings.append((f"{clause_count(s)} subordinate clauses", num, s[:66]))
        gap = subject_verb_gap(s)
        if gap > MAX_SUBJECT_VERB_GAP:
            findings.append((f"subject-verb gap {gap}", num, s[:66]))

    words = word_list(body)
    total = len(words) or 1
    lengths = sorted(len(word_list(s)) for s, _ in sents)
    median = lengths[len(lengths) // 2] if lengths else 0
    p95 = lengths[int(len(lengths) * 0.95)] if lengths else 0
    mono = sum(1 for w in words if syllables(w) == 1)
    longw = sum(1 for w in words if syllables(w) >= 3)
    noms = sum(1 for m in re.finditer(NOMINALIZATION, body, re.I)
               if m.group(0).lower() not in NOT_NOMINALIZATIONS)
    weasels = 0
    weasel_units = [s for s, _ in sents] + [t for _, t in fragments] + [t for _, t in heading_texts]
    for unit in weasel_units:
        if re.search(LABELED_UNKNOWN, unit, re.I):
            continue
        weasels += len(re.findall(WEASELS, unit, re.I))
    adverbs = len(re.findall(r"\b\w{4,}ly\b", body, re.I))
    headings = sum(1 for _, l in kept if l.strip().startswith("#"))
    quoted = sum(l.count("QUOTED") for _, l in kept) + sum(t.count("QUOTED") for _, t in fragments)

    stats = {
        "words": total, "sentences": len(sents), "median": median, "p95": p95,
        "mono_pct": 100.0 * mono / total, "long_pct": 100.0 * longw / total,
        "nom_pct": 100.0 * noms / total, "weasels": weasels,
        "adverbs_per_k": 1000.0 * adverbs / total,
        "headings_per_500": 500.0 * headings / total,
        "coverage": (f"{len(fragments)} table cell(s) and {len(heading_texts)} heading(s) scanned; "
                     f"excluded {excluded['blockquote']} blockquote, {excluded['code fence']} code-fence, "
                     f"{excluded['BEFORE block']} BEFORE line(s); {quoted} quoted span(s) masked"),
    }

    min_median = REFERENCE_MIN_MEDIAN if reference else MIN_MEDIAN_WORDS
    max_headings = REFERENCE_MAX_HEADINGS_PER_500 if reference else MAX_HEADINGS_PER_500

    warnings = []
    if lengths and median < min_median:
        warnings.append(f"median sentence {median}w below {min_median}: check for chopped causation")
    if median > MAX_MEDIAN_WORDS:
        warnings.append(f"median sentence {median}w above {MAX_MEDIAN_WORDS}")
    over = [(n, s[:50]) for s, n in sents if len(word_list(s)) > LONG_SENTENCE_WORDS]
    if over:
        warnings.append(f"{len(over)} sentence(s) over {LONG_SENTENCE_WORDS}w, first at line {over[0][0]}")
    if stats["mono_pct"] < MIN_MONOSYLLABLE_PCT:
        warnings.append(f"monosyllables {stats['mono_pct']:.0f}% below {MIN_MONOSYLLABLE_PCT:.0f}%: heavy Latinate diction")
    if stats["long_pct"] > MAX_LONGWORD_PCT:
        warnings.append(f"3+ syllable words {stats['long_pct']:.0f}% above {MAX_LONGWORD_PCT:.0f}%: check for nominalizations and fat words")
    if stats["nom_pct"] > MAX_NOMINALIZATION_PCT:
        warnings.append(f"nominalizations {stats['nom_pct']:.1f}% above {MAX_NOMINALIZATION_PCT:.0f}%")
    if stats["weasels"] > MAX_WEASELS:
        warnings.append(f"{stats['weasels']} weasel words, budget {MAX_WEASELS}")
    if stats["adverbs_per_k"] > MAX_ADVERBS_PER_KWORDS:
        warnings.append(f"-ly adverbs {stats['adverbs_per_k']:.0f}/1000w above {MAX_ADVERBS_PER_KWORDS:.0f}")
    if stats["headings_per_500"] > max_headings:
        warnings.append(f"headings {stats['headings_per_500']:.1f}/500w above {max_headings:.0f}")
    stacked = re.findall(STACKED_MODIFIER, body, re.I)
    if len(stacked) > MAX_CLAUSES:
        warnings.append(f"{len(stacked)} stacked modifiers, e.g. {stacked[0]}: apply the plain-clause test")
    colons = sum(1 for s, _ in sents if ":" in s)
    colons_per_k = 1000.0 * colons / total
    if colons_per_k > MAX_COLONS_PER_KWORDS:
        warnings.append(f"colon constructions {colons_per_k:.0f}/1000w above {MAX_COLONS_PER_KWORDS:.0f}: rewrite some as plain sentences")
    for phrase, count in repeated_ngrams(sents):
        warnings.append(f"phrase repeated {count}x: \"{phrase}\": vary or dedupe")
    paragraph_start = None
    paragraph_lines = 0
    for number, line in kept + [(0, "")]:
        stripped = line.strip()
        prose_line = bool(stripped and not stripped.startswith("#") and not re.match(r"^\s*(?:[-*+]|\d+\.)\s", line))
        if prose_line:
            paragraph_start = number if paragraph_start is None else paragraph_start
            paragraph_lines += 1
        else:
            if paragraph_lines > MAX_PARAGRAPH_LINES:
                warnings.append(f"paragraph at line {paragraph_start} spans {paragraph_lines} lines, above {MAX_PARAGRAPH_LINES}")
            paragraph_start, paragraph_lines = None, 0
    return failures, findings, warnings, stats


def main():
    """Prints a bounded report. Exits 1 on hard bans, 2 on unreviewed Flags, else 0."""
    args = sys.argv[1:]
    reference = "--reference" in args
    accept_flags = "--accept-flags" in args
    show_all = "--all" in args
    flag_cap = None if show_all else 8
    paths = [a for a in args if not a.startswith("--")]
    if not paths:
        print("usage: style_check.py [--reference] [--accept-flags] [--all] FILE [FILE ...]")
        return 2
    worst = 0
    flags_pending = False
    for path in paths:
        failures, findings, warnings, st = check(path, reference=reference)
        print(f"\n=== {Path(path).name} ===")
        print(f"{st['words']}w  {st['sentences']} sentences  median {st['median']}w  p95 {st['p95']}w")
        print(f"mono {st['mono_pct']:.0f}%  long {st['long_pct']:.0f}%  "
              f"nominalized {st['nom_pct']:.1f}%  weasels {st['weasels']}")
        print(f"Coverage: {st['coverage']}")
        if failures:
            print(f"\nFail {len(failures)} hard-ban rule(s):")
            for name, fix, hits, n in failures:
                hits = hits if show_all else hits[:MAX_HITS_PER_RULE]
                shown = "; ".join(f"L{ln}: {txt}" for ln, txt in hits)
                more = f" (+{n - len(hits)} more)" if n > len(hits) else ""
                print(f"  [{name}] -> {fix}\n    {shown}{more}")
            worst = 1
        else:
            print("\nFail: 0 confirmed hard-ban hits")
        if findings:
            flags_pending = True
            print(f"\nFlag {len(findings)} checker candidate(s), confirm each:")
            for name, num, txt in findings[:flag_cap]:
                print(f"  L{num} [{name}] {txt}")
            if flag_cap is not None and len(findings) > flag_cap:
                print(f"  (+{len(findings) - flag_cap} more; rerun with --all to list them)")
        else:
            print("Flag: no checker candidates")
        if warnings:
            print(f"\nAdvisory {len(warnings)} range warning(s):")
            for w in warnings:
                print(f"  {w}")
        else:
            print("Advisory: all ranges in target")
    if flags_pending and not accept_flags and worst == 0:
        worst = 2
        print("\nFlags await human review; this exit is not publication approval. "
              "Rerun with --accept-flags after a human confirms or dismisses each Flag.")
    return worst


if __name__ == "__main__":
    sys.exit(main())
