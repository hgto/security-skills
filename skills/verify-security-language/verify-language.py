#!/usr/bin/env python3
"""verify-language.py — security writing language linter.

Usage:
    python3 verify-language.py [--json] [<file>]

Reads <file> or stdin. For each flagged term prints:
    LINE:COL [category] "term" → suggestion

With --json, prints a JSON array of {line, col, category, term, suggestion}.

Exit 1 if any hits, 0 if clean.
"""

import re
import sys
import json

# ---------------------------------------------------------------------------
# Term dictionaries — mirrors word-substitutions.md (single source of truth)
# ---------------------------------------------------------------------------

# Loaded / emotive terms → more neutral alternatives
LOADED = {
    "unauthorized access": "inappropriate access — state authN/authZ + what was accessed",
    "attacker": "external party / threat actor",
    "hacker": "threat actor / external party",
    "victim": "affected party",
    "malicious": "anomalous / unsanctioned",
    "hacked": "inappropriately accessed (detail what was accessed)",
    "backdoor": "undocumented access mechanism",
    "vulnerability": "weakness / potential weakness / finding",
    "vulnerabilities": "weaknesses / potential weaknesses",
    "weaponized": "configured to exploit / used to deliver",
    "guilty": "responsible party / actor / source",
    "culprit": "responsible party / actor / source",
    "perpetrator": "responsible party / actor / source",
    "war": "sustained activity / related set of events",
    "campaign": "sustained activity / related set of events",
    "destroyed": "rendered unavailable / deleted / encrypted",
    "wiped": "rendered unavailable / deleted / encrypted",
    "spy": "collection of information beyond approved scope",
    "espionage": "collection of information beyond approved scope",
}

# Legal terms of art
LEGAL = {
    "breach": "incident / inappropriate access",
    "stolen": "accessed / transferred",
    "exfiltrated": "observed transferring",
    "negligent": "did not align with policy",
    "compromised": "potentially affected",
    "careless": "did not align with [policy/standard]",
    "sloppy": "did not align with [policy/standard]",
}

# Hyperbole — words that over-claim severity
HYPERBOLE = {
    "catastrophic": "significant / material / [quantified]",
    "devastating": "significant / material / [quantified]",
    "massive": "significant / material / [quantified]",
    "disaster": "significant / material / [quantified]",
    "obviously": "(delete; state the evidence)",
    "clearly": "(delete; state the evidence)",
}

# Absolutes — phrases that make epistemically false guarantees
# Multi-word entries must come before single-word ones to ensure longer
# phrases are matched first.
ABSOLUTES = {
    "100% secure": "reduces the likelihood of …; mitigates …",
    "fully secure": "reduces the likelihood of …; mitigates …",
    "fully eliminated": "mitigates; reduces residual risk",
    "completely eliminated": "mitigates; reduces residual risk",
    "cannot be breached": "reduces the likelihood of …; mitigates …",
    "unhackable": "reduces the likelihood of …; mitigates …",
    "guaranteed": "reduces the likelihood of; no absolute claim — state residual risk",
    "impossible": "reduces the likelihood of; no absolute claim — state residual risk",
}

# Legal-compliance opinion terms — rendering conclusions only counsel/compliance
# may make. Multi-word phrases must come before constituent single words.
COMPLIANCE = {
    "compliance violation": "gap relative to [control]; flag for compliance",
    "in breach of": "may have implications under [framework]; recommend review by counsel",
    "non-compliant": "did not align with [control]",
    "violates": "may have implications under [framework]; recommend review by compliance",
    "violation": "did not align with [control/policy]",
    "illegal": "(state observed fact); flag for counsel",
    "unlawful": "(state observed fact); flag for counsel",
}

# Second-person blame pattern (not a dict, just one regex)
SECOND_PERSON_BLAME_PATTERN = re.compile(
    r"\byou (failed|should have|neglected|forgot)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Category ordering: longer / multi-word phrases checked before shorter ones
# so that "compliance violation" wins over bare "violation", etc.
# ---------------------------------------------------------------------------

def _sorted_by_length(d):
    """Return dict items sorted longest key first."""
    return sorted(d.items(), key=lambda kv: len(kv[0]), reverse=True)


def _compile_category(d):
    """Return list of (compiled_pattern, term, suggestion) sorted longest term first."""
    return [
        (re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE), term, suggestion)
        for term, suggestion in _sorted_by_length(d)
    ]


# Precompile all patterns once at module load.
CATEGORIES = [
    ("loaded-term",              _compile_category(LOADED)),
    ("legal-term",               _compile_category(LEGAL)),
    ("hyperbole",                _compile_category(HYPERBOLE)),
    ("absolute",                 _compile_category(ABSOLUTES)),
    ("legal-compliance-opinion", _compile_category(COMPLIANCE)),
]

# ---------------------------------------------------------------------------
# Core linting logic
# ---------------------------------------------------------------------------

def lint_lines(lines):
    """Lint a list of text lines, returning a list of hit dicts."""
    hits = []

    for lineno, raw_line in enumerate(lines, start=1):
        # Track which character spans are already claimed by a hit on this
        # line so a shorter constituent word doesn't double-report.
        claimed_spans = []

        def span_is_free(start, end):
            for cs, ce in claimed_spans:
                if start < ce and end > cs:  # overlap
                    return False
            return True

        # Process each category in order.
        for category, compiled_entries in CATEGORIES:
            for pattern, term, suggestion in compiled_entries:
                for m in pattern.finditer(raw_line):
                    start, end = m.start(), m.end()
                    if not span_is_free(start, end):
                        continue
                    claimed_spans.append((start, end))
                    hits.append({
                        "line": lineno,
                        "col": start + 1,   # 1-based
                        "category": category,
                        "term": m.group(0),
                        "suggestion": suggestion,
                    })

        # Second-person blame check
        for m in SECOND_PERSON_BLAME_PATTERN.finditer(raw_line):
            start, end = m.start(), m.end()
            if not span_is_free(start, end):
                continue
            claimed_spans.append((start, end))
            hits.append({
                "line": lineno,
                "col": start + 1,
                "category": "second-person-blame",
                "term": m.group(0),
                "suggestion": "(reframe to system/process)",
            })

    return hits


def format_hit(hit):
    return (
        f'{hit["line"]}:{hit["col"]} [{hit["category"]}] '
        f'"{hit["term"]}" → {hit["suggestion"]}'
    )


def main():
    args = sys.argv[1:]
    use_json = "--json" in args
    file_args = [a for a in args if a != "--json"]

    if file_args:
        try:
            with open(file_args[0], encoding="utf-8") as fh:
                lines = fh.readlines()
        except OSError as exc:
            print(f"verify-language: cannot open file: {exc}", file=sys.stderr)
            sys.exit(2)
    else:
        lines = sys.stdin.readlines()

    hits = lint_lines(lines)

    if use_json:
        print(json.dumps(hits))
    else:
        for hit in hits:
            print(format_hit(hit))

    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
