---
name: security-language
description: (hgto/security-skills) Use when writing or editing any security report, finding, incident report, or executive summary, or when choosing how to describe an external party, an incident, attribution, or uncertain events in security prose.
---

## 1. Overview

Every assertion in a security document must be traceable to evidence. The security-language standard has three pillars:

1. **Separate observed fact from assessment.** What was seen is not the same as what it means.
2. **Neutral, defensible language.** Word choice that presumes intent, renders legal conclusions, or assigns blame creates liability and undermines credibility.
3. **Calibrated uncertainty.** Likelihood and confidence are quantified on explicit scales; absolutes are never used.

This skill governs all security prose. All document-level skills in this plugin depend on it.

---

## 2. The Load-Bearing Rule — Fact vs. Assessment

**Fact:** Something observed, sourced, past tense, declarative. It requires no hedging because it describes what was directly observed.

**Assessment:** An inference, interpretation, or conclusion drawn from facts. It requires a likelihood qualifier and a confidence level.

**Example pair:**

- Fact: "Authentication logs show 4,200 queries to the customer table from service account `svc-reporting` between 02:14 and 03:47 UTC."
- Assessment: "We assess with moderate confidence that the actor likely used this account to enumerate customer records during that window."

Never state an assessment as a fact. Never state a fact with false hedging — observed events do not require "we assess."

---

## 3. Word Choice

Use neutral terms. See `word-substitutions.md` for the full substitution table and the No Legal/Compliance Opinions and Absolutes Blocklist subsections.

**Headline rules:**

- Use "external party" or "threat actor." Never "attacker" or "hacker" — both presume hostile intent and attribution.
- Never assert "breach" or "stolen" until confirmed by counsel; both are legal terms of art that trigger regulatory duties.
- Never write "leak" (or "leaked," "leaking," "leakage"). It conflates two different claims: use "accessed," "transferred," or "observed leaving" when it is not yet confirmed that an unauthorized party obtained the data; use "information disclosure," "disclosed," or "inappropriately accessed" when that access is confirmed.
- Never write "vulnerability" when referring to an unconfirmed or alleged issue. Write "weakness," "potential weakness," "finding," or "observed condition." The term "vulnerability" infers a confirmed issue and is a compliance trigger. Proper nouns (CVE identifiers, CWE identifiers, CVSS scores) are kept as-is.
- Never write "unauthorized access." The phrase is ambiguous: it conflates whether authentication occurred with whether the actor was authorized. Instead, write "inappropriate access" and state specifically: (a) whether authentication occurred, (b) whether the actor held authorization for that resource, and (c) what was accessed.

---

## 4. Likelihood vs. Confidence

These are two independent axes. Never collapse them into a single term.

- **Likelihood** — how probable is the conclusion? (almost certain / very likely / likely / roughly even chance / unlikely / very unlikely / remote)
- **Confidence** — how good is the sourcing? (high / moderate / low)

See `estimative-language.md` for the full ICD 203 tables, canonical combined-form examples, and the "no evidence ≠ did not happen" rule.

Canonical form: "We assess with [confidence] confidence that [subject] [likelihood term] [conclusion]."

---

## 5. Attribution Caution

Default position on attribution: **unattributed.** Attribution requires independent corroboration from multiple source types and is rarely within scope for incident reports.

- Describe TTPs (tactics, techniques, and procedures) rather than identity claims.
- Use MITRE ATT&CK technique IDs to describe observed behavior without attributing intent or actor identity.
- If attribution is required, use hedged language with full confidence and likelihood qualifiers, and note the evidentiary basis.

---

## 6. No Legal/Compliance Opinions

Never give legal or compliance advice. Never advance a legal or compliance opinion. The following terms are prohibited unless attributing a statement to counsel or a regulatory body:

- `violation`, `compliance violation`, `non-compliant`
- `violates [regulation]`, `in breach of [regulation]`
- `illegal`, `unlawful`

**Rule:** State the observed fact. Flag the matter for counsel/compliance review.

- ✗ "This is a GDPR violation."
- ✓ "Personal data was accessible without authentication; this may have implications under GDPR — recommend review by compliance/counsel."

---

## 7. Blameless Tone

Security reports address systems and processes, not people.

- Attribute findings to systems, configurations, processes, and controls — not to individuals.
- Use roles, not names: "the on-call engineer," "the account owner," not personal names.
- Frame deficiencies forward: "the alerting configuration did not produce a notification" rather than "the analyst missed the alert."
- Avoid "should have," "failed to," or "neglected to" applied to individuals. Reframe to the system or process level.

---

## 8. Red Flags — STOP

Before finalizing any security document, check for these:

- [ ] I wrote "attacker" or "hacker".
- [ ] I wrote "vulnerability" for an unconfirmed or alleged issue (should be "weakness," "finding," or "observed condition").
- [ ] I wrote "unauthorized access" instead of stating whether authentication occurred, whether authorization was held, and what was accessed.
- [ ] I stated exfiltration, theft, leakage, or data loss as confirmed fact without a sourced log entry or forensic finding — it should be "assessed … likely."
- [ ] I wrote "leak," "leaked," "leaking," or "leakage" instead of "accessed"/"transferred"/"observed leaving" (unconfirmed) or "information disclosure"/"disclosed"/"inappropriately accessed" (confirmed).
- [ ] I used an absolute: "unhackable," "100% secure," "fully eliminated," "guaranteed," "impossible," "cannot be breached."
- [ ] I named or described an individual in a way that assigns personal blame.
- [ ] I called the event a "breach" before counsel confirmed it meets the regulatory definition.
- [ ] I wrote "violation," "violates [regulation]," "non-compliant," or "illegal" — I rendered a compliance/legal opinion I am not qualified to give.

---

## 9. Rationalization Table

These are common objections to the security-language standard, with responses.

| Rationalization | Counter |
|---|---|
| "'Attacker' is just clearer — everyone knows what it means." | Clarity does not require an intent-plus-attribution claim. "External party" and "threat actor" are equally clear to any security audience and remain defensible if attribution later changes or is contested. |
| "'Breach' is the industry word — clients expect it." | "Breach" is a regulatory term of art in HIPAA, GDPR, state notification laws, and others. Using it prematurely triggers notification duties and shapes legal exposure before counsel has assessed the facts. "Incident" or "inappropriate access" conveys the same information without that risk. |
| "'Stolen' is accurate — the data left the network." | Data leaving the network is an observation. "Stolen" is a legal conclusion about intent and authorization that requires a court or regulatory determination. Write "transferred," "copied," or "observed leaving" and let counsel assess the legal characterization. |
| "'Leaked' is softer than 'stolen' — it's fine to say data leaked." | "Leaked" still asserts that an unauthorized party obtained the data — the same unconfirmed legal conclusion as "stolen" or "exfiltrated," just gentler-sounding. If that is not yet confirmed, write "accessed," "transferred," or "observed leaving." If confirmed, write "information disclosure," "disclosed," or "inappropriately accessed." |
| "'Vulnerability' is the right word — there's clearly a bug." | "Vulnerability" has a defined meaning in CVE/CVSS that implies confirmed exploitability. Calling an unconfirmed finding a "vulnerability" before full assessment is a compliance trigger and may overstate certainty. Use "weakness," "potential weakness," or "finding" until the assessment is complete. |
| "Saying 'this violates GDPR' is just being direct and helpful." | Rendering a regulatory opinion requires legal expertise and creates discovery risk. It may also be wrong, and a wrong legal conclusion in a report is worse than none. State the observed condition and flag it for compliance/counsel — that is the helpful, accurate, and defensible path. |
| "Using 'almost certain' instead of 'certain' sounds weak and hedged." | "Certain" is an absolute that is epistemically false in security contexts and creates legal exposure if later refuted. "Almost certain" (95–99%) conveys the same high probability while remaining calibrated and defensible. Precision is not weakness; overstatement is. |
