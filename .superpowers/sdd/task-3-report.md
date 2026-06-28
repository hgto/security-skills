# Task 3 Report: `verify-language.py` Linter

## Status
COMPLETE — 13/13 tests passing, pristine output.

## Commit
- SHA: `1b8ec6f`
- Subject: `feat: add verify-language.py linter with tests`

---

## TDD Evidence

### RED Phase (Step 2)

**Command:**
```
cd skills/verify-security-language && python3 -m pytest test_verify_language.py -v
```

**Output (abbreviated):**
```
collected 13 items

test_verify_language.py::test_flags_attacker FAILED
test_verify_language.py::test_flags_absolute FAILED
...
13 failed in 0.40s
```

**Why expected:** `verify-language.py` did not yet exist. Python returned exit code 2 ("No such file or directory"), which is neither 0 nor 1, causing all assertions to fail immediately.

---

### GREEN Phase (Step 4)

**Command:**
```
cd skills/verify-security-language && python3 -m pytest test_verify_language.py -v
```

**Output:**
```
collected 13 items

test_verify_language.py::test_flags_attacker PASSED        [  7%]
test_verify_language.py::test_flags_absolute PASSED        [ 15%]
test_verify_language.py::test_flags_legal_term PASSED      [ 23%]
test_verify_language.py::test_flags_second_person_blame PASSED [ 30%]
test_verify_language.py::test_flags_compliance_opinion PASSED [ 38%]
test_verify_language.py::test_flags_violation_word PASSED  [ 46%]
test_verify_language.py::test_flags_violates PASSED        [ 53%]
test_verify_language.py::test_flags_vulnerability PASSED   [ 61%]
test_verify_language.py::test_flags_unauthorized_access PASSED [ 69%]
test_verify_language.py::test_clean_text_exit_zero PASSED  [ 76%]
test_verify_language.py::test_case_insensitive PASSED      [ 84%]
test_verify_language.py::test_word_boundary_no_false_positive PASSED [ 92%]
test_verify_language.py::test_json_output PASSED           [100%]

13 passed in 0.37s
```

No warnings, no noise — pristine.

---

## Files Created

- `skills/verify-security-language/test_verify_language.py` — 13 tests verbatim from brief
- `skills/verify-security-language/verify-language.py` — linter implementation, stdlib only

---

## Implementation Notes

### Ambiguities resolved by what the tests require

1. **`unauthorized access` suggestion string:** The test asserts `"inappropriate access" in r.stdout`. The brief's LOADED dict shows the full suggestion as `"inappropriate access — state authN/authZ + what was accessed"`. Since the test checks for substring containment, the longer form satisfies it. Used the full form.

2. **`compliance violation` vs bare `violation`:** `test_flags_compliance_opinion` uses text `"This is a compliance violation of GDPR."` and `test_flags_violation_word` uses `"This is a clear violation."` Both must hit `legal-compliance-opinion`. The multi-word phrase is matched first (longer keys sorted first), so "compliance violation" wins when present; bare "violation" is then independently flagged in the second test. This design matches the brief's "match longer phrases before constituent single words" rule.

3. **`vulnerabilities` key:** Added to LOADED dict as a separate entry (alongside `vulnerability`) since the table in word-substitutions.md distinguishes singular/plural suggestions.

### Design decisions

- `_sorted_by_length()` sorts each dict by key length (longest first) before building the CATEGORIES list, ensuring multi-word phrases always win over their constituent single words.
- `claimed_spans` per line prevents double-reporting the same character range across multiple categories.
- Second-person blame is implemented as a dedicated `re.compile` (not a dict), matching the brief's explicit regex pattern `\byou (failed|should have|neglected|forgot)\b`.
- All matching uses `re.IGNORECASE` for case-insensitive detection.
- `\b` word boundaries on both sides prevent partial-word matches (validated by `test_word_boundary_no_false_positive`: "aware warehouse" doesn't trigger "war").

---

## Self-Review

- [x] Stdlib only — no third-party imports
- [x] Reads from file arg if given, else stdin
- [x] `--json` emits valid JSON array of `{line, col, category, term, suggestion}`
- [x] Human output format: `LINE:COL [category] "term" → suggestion`
- [x] Exit code 1 if any hits, 0 if clean
- [x] Six required categories present: `loaded-term`, `absolute`, `hyperbole`, `legal-term`, `second-person-blame`, `legal-compliance-opinion`
- [x] Word-boundary matching for all terms
- [x] Multi-word phrases matched before constituent single words (span-claiming + length-sort)
- [x] Term dicts mirror word-substitutions.md

## Concerns

None. All 13 tests pass cleanly. The `campaign` and `war` entries in LOADED use `\b` boundaries, so common words like "war" won't fire inside larger compound words — confirmed by the word-boundary test. The one deliberate over-flagging trade-off (bare "violation" hitting benign technical uses) is explicitly acknowledged in the brief as intentional house policy handled at triage.

---

## Fix Round 1

**Commit:** `e04d11a` — `fix: precompile linter patterns, strengthen tests, add spy/espionage + file error handling`

### GREEN Evidence

**Command:**
```
cd skills/verify-security-language && python3 -m pytest test_verify_language.py -v
```

**Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/thug/Projects/security-writing/skills/verify-security-language
collecting ... collected 14 items

test_verify_language.py::test_flags_attacker PASSED                      [  7%]
test_verify_language.py::test_flags_absolute PASSED                      [ 14%]
test_verify_language.py::test_flags_legal_term PASSED                    [ 21%]
test_verify_language.py::test_flags_second_person_blame PASSED           [ 28%]
test_verify_language.py::test_flags_compliance_opinion PASSED            [ 35%]
test_verify_language.py::test_flags_violation_word PASSED                [ 42%]
test_verify_language.py::test_flags_violates PASSED                      [ 50%]
test_verify_language.py::test_flags_vulnerability PASSED                 [ 57%]
test_verify_language.py::test_flags_unauthorized_access PASSED           [ 64%]
test_verify_language.py::test_clean_text_exit_zero PASSED                [ 71%]
test_verify_language.py::test_case_insensitive PASSED                    [ 78%]
test_verify_language.py::test_word_boundary_no_false_positive PASSED     [ 85%]
test_verify_language.py::test_json_output PASSED                         [ 92%]
test_verify_language.py::test_missing_file_exits_2 PASSED                [100%]

============================== 14 passed in 0.43s ==============================
```

No warnings, no noise — pristine.

### What Each Fix Changed

- **Fix 1 (precompile patterns):** Introduced `_compile_category()` to build `(compiled_pattern, term, suggestion)` tuples at module load. `CATEGORIES` now holds compiled entries; the hot loop iterates them without calling `re.compile`. Longest-first ordering and `claimed_spans` overlap logic preserved.
- **Fix 2 (strengthen tests):** Added `assert r.returncode == 1` to `test_flags_legal_term` and `test_flags_second_person_blame`.
- **Fix 3 (spy/espionage):** Added `"spy"` and `"espionage"` to LOADED with suggestion `"collection of information beyond approved scope"`. Word-boundary `\b` matching applies via the existing compile path.
- **Fix 4 (graceful file error):** Wrapped `open()` in a `try/except OSError` block; on failure prints a clean message to stderr and calls `sys.exit(2)`. Added `test_missing_file_exits_2` which invokes the script with a nonexistent path and asserts `returncode == 2` and non-empty stderr.

---

## URL Suppression

**Commit:** `feat: suppress linter matches inside URLs (reference links are literals)`

### Change

Added URL-span pre-claiming to `lint_lines()` in `verify-language.py`. Before running any category matchers on a line, the linter now finds all URL tokens with `re.finditer(r"https?://\S+", raw_line, re.IGNORECASE)` and adds their spans to `claimed_spans`. This composes with the existing proper-noun allow-list pre-claiming — both run before category matching, so the overlap check suppresses any banned term whose character range falls inside a URL.

Bare banned terms in prose are still flagged; allow-listed proper-noun phrases still pass. No other behavior changed.

Three new tests added (18 → 21 total):
- `test_allows_url_with_banned_slug` — URL containing "vulnerabilities" slug → exit 0
- `test_url_does_not_suppress_surrounding_prose` — bare "vulnerability" in prose before a URL → exit 1, "weakness" in stdout
- `test_plain_url_clean` — innocuous URL → exit 0

### GREEN Evidence

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/thug/Projects/security-writing/skills/verify-security-language
collecting ... collected 21 items

test_verify_language.py::test_flags_attacker PASSED                      [  4%]
test_verify_language.py::test_flags_absolute PASSED                      [  9%]
test_verify_language.py::test_flags_legal_term PASSED                    [ 14%]
test_verify_language.py::test_flags_second_person_blame PASSED           [ 19%]
test_verify_language.py::test_flags_compliance_opinion PASSED            [ 23%]
test_verify_language.py::test_flags_violation_word PASSED                [ 28%]
test_verify_language.py::test_flags_violates PASSED                      [ 33%]
test_verify_language.py::test_flags_vulnerability PASSED                 [ 38%]
test_verify_language.py::test_flags_unauthorized_access PASSED           [ 42%]
test_verify_language.py::test_clean_text_exit_zero PASSED                [ 47%]
test_verify_language.py::test_case_insensitive PASSED                    [ 52%]
test_verify_language.py::test_word_boundary_no_false_positive PASSED     [ 57%]
test_verify_language.py::test_json_output PASSED                         [ 61%]
test_verify_language.py::test_missing_file_exits_2 PASSED                [ 66%]
test_verify_language.py::test_allows_cisa_kev PASSED                     [ 71%]
test_verify_language.py::test_allows_nvd PASSED                          [ 76%]
test_verify_language.py::test_allows_cve_fullname PASSED                 [ 80%]
test_verify_language.py::test_bare_vulnerability_still_flagged PASSED    [ 85%]
test_verify_language.py::test_allows_url_with_banned_slug PASSED         [ 90%]
test_verify_language.py::test_url_does_not_suppress_surrounding_prose PASSED [ 95%]
test_verify_language.py::test_plain_url_clean PASSED                     [100%]

============================== 21 passed in 0.63s ==============================
```

No warnings, no noise — pristine.
