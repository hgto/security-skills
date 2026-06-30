---
name: verify-security-language
description: (hgto/security-skills) Use when reviewing, checking, or cleaning up a security draft for loaded or non-neutral language, or when asked to make security writing clinical, neutral, or defensible before it is delivered.
---

## 1. Overview

This skill applies the `security-language` standard to an existing draft. Mechanical detection is handled by `verify-language.py`; clinical re-framing is handled by judgment. The script is a necessary first pass — it is not sufficient on its own.

**REQUIRED SUB-SKILL:** security-language

---

## 2. Procedure

1. **Run the script** against the draft to establish a baseline hit list:
   ```
   python3 verify-language.py <draft>
   ```
   Or pipe via stdin:
   ```
   cat <draft> | python3 verify-language.py
   ```

2. **Triage every hit.** For each flagged term, decide whether it is (a) a clear rewrite, (b) a fact-vs-assessment separation problem, or (c) context-dependent. Do not bulk-delete — read the surrounding sentence.

   **Proper-noun false positives — "vulnerability / vulnerabilities":** A linter hit on "vulnerability" or "vulnerabilities" that is part of an official proper noun is a FALSE POSITIVE — keep it verbatim. The following names (and any similarly official title) must NEVER be renamed to satisfy the linter:
   - CVE — Common Vulnerabilities and Exposures
   - CVSS — Common Vulnerability Scoring System
   - CISA Known Exploited Vulnerabilities (KEV) Catalog
   - NIST National Vulnerability Database (NVD)

   Renaming a standard, catalog, advisory, or product's official name (e.g. "Known Exploited Vulnerabilities" → "Known Exploited Weaknesses") is a factual error. The linter suppresses these automatically via its allow-list, but exercise the same judgment for any official title not yet in the allow-list.

3. **Reframe loaded terms** using the substitution table in `security-language/word-substitutions.md`. Common substitutions:
   - "hacker" / "attacker" → "external party" or "threat actor"
   - "breach" → "incident" or "inappropriate access" (pending counsel confirmation)
   - "stolen" → "accessed" or "transferred"
   - "leaked" / "leak" / "leaking" / "leakage" → "accessed," "transferred," or "observed leaving"
   - "catastrophic" → quantify: "affected N records" or "resulted in X hours of unavailability"

4. **Demote unsourced claims to assessments.** Any inference or conclusion that is not directly observed must carry an explicit likelihood qualifier and a confidence level. Canonical form:
   > "We assess with [confidence] confidence that [subject] [likelihood term] [conclusion]."
   Use the likelihood and confidence scales from `security-language/estimative-language.md`.

5. **Strip absolutes and hyperbole.** Delete "obviously," "clearly," "catastrophic," "massive," and all epistemically false guarantees. Replace with quantified, sourced alternatives or remove entirely.

6. **De-personalize blame.** Attribute findings to systems, configurations, processes, and controls — not individuals. Use roles, not names. Reframe "the ops team dropped the ball" as "the alerting configuration did not produce a timely notification" or equivalent process-level framing.

7. **Re-run the script and confirm exit 0** before delivering:
   ```
   python3 verify-language.py <draft>; echo "Exit: $?"
   ```
   Do not deliver a draft that exits non-zero.

---

## 3. What the Script Cannot Catch

The script performs term-level pattern matching. These four failure modes require human judgment and cannot be caught mechanically:

- **Fact-vs-assessment separation.** The script cannot tell whether an assertion is a direct observation or an inferred conclusion. An inference stated without a likelihood qualifier will pass the script even though it violates the standard.

- **Missing confidence qualifiers.** An assessment may use a correct likelihood term but omit the confidence level. The script will not flag "the actor likely exfiltrated data" — a human must notice that the confidence level is absent.

- **Premature attribution.** The script does not evaluate whether the evidentiary basis for an attribution claim is sufficient. A sentence can be term-clean and still attribute identity, TTPs, or motive without adequate corroboration.

- **Hindsight bias.** The script cannot detect when a report frames a past outcome as foreseeable without evidence that it was assessed as such at the time. This is a structural problem in the narrative, not a vocabulary problem.

- **Proper nouns not yet in the allow-list.** The script suppresses "vulnerability/vulnerabilities" inside known official titles (CVE, CVSS, CISA KEV, NVD). Any other official name containing the word that is not yet in the allow-list will produce a false positive — keep it verbatim and do not rename it.

The script is necessary, not sufficient. A clean script exit is a floor, not a ceiling.

---

## 4. Example

**Before (loaded, unverified, blame-assigning):**

> The hacker obviously broke into our server and stole all our customer data. It was a catastrophic breach and the ops team totally dropped the ball.

**After (clinical, fact-separated, confidence-qualified):**

> **Observed fact:** Authentication logs show that an external party authenticated to the web application server between 02:14 and 03:47 UTC using a valid service account credential.
>
> **Assessment:** We assess with moderate confidence that the external party likely accessed customer records during this window; the full scope of records accessed is under investigation and has not been confirmed.
>
> **Assessment:** We assess with low confidence that customer data was transferred outside the environment; no confirmed exfiltration artifact has been identified at this time.
>
> **Process finding:** The alerting configuration did not produce a notification within the detection window. This finding is referred to the detection-and-response process review.

**Changes made:**

| Original | Rewrite | Reason |
|---|---|---|
| "hacker" | "external party" | Loaded term — presumes hostile intent and attribution |
| "obviously broke into" | "authenticated to … using a valid service account credential" | "Obviously" is hyperbole; state the evidence instead |
| "stole all our customer data" | "likely accessed customer records … scope under investigation" | "Stolen" is a legal conclusion; "all" is an unsourced absolute; demoted to assessment with likelihood + confidence |
| "catastrophic breach" | removed / quantified as process finding | "Catastrophic" is hyperbole; "breach" is a legal term of art pending counsel confirmation |
| "ops team totally dropped the ball" | "alerting configuration did not produce a notification within the detection window" | De-personalized from team-level blame to process/system-level finding |
