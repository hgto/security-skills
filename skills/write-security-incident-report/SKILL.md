---
name: write-security-incident-report
description: (hgto/security-skills) Use when writing a security incident report, post-incident report, security event report, or incident response writeup, or when documenting what happened during a security event with a timeline, scope, IOCs, and lessons learned.
---

**REQUIRED SUB-SKILL:** security-language

Use OpenCode's Skill tool to load `security-language` before beginning. Its rules govern every word choice, fact/assessment distinction, likelihood qualifier, and confidence level in the report. Pay particular attention to likelihood-vs-confidence (two separate axes, never collapsed) and IOC defanging (all network IOCs in human-readable sections must be defanged).

---

## 1. Overview

A security incident report serves two audiences simultaneously: the technical team reconstructing what happened, and the leadership and legal team assessing exposure and deciding response. A report that works for one but not the other has failed.

The structural spine of this skill is:

- **NIST SP 800-61** (Computer Security Incident Handling Guide) — defines incident phases and evidence-handling standards.
- **SANS PICERL** — Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned — provides the response action framework for the Response Actions section.

**Fact vs. assessment is the paramount discipline.** Every statement in the report is either:

1. An observed fact — directly sourced, past tense, declarative, no hedging required.
2. An assessment — an inference or conclusion drawn from facts — which requires an explicit likelihood qualifier and a confidence level.

Conflating these two categories is the most common and consequential error in incident reporting. An assessment stated as a fact overstates certainty. A fact hedged with "we assess" underreports what is known. Both damage credibility and may create legal exposure.

---

## 2. When to Use

Use this skill when:

- Writing a formal incident report or post-incident report for a security event that has been scoped, investigated, and at least partially responded to.
- Documenting an incident that requires a timeline, IOC table, MITRE ATT&CK mapping, and a lessons learned section.
- Translating raw investigation notes, log exports, or a verbal debrief into a structured, defensible report.

Do not use this skill to write a security finding from a penetration test or audit — use `write-security-finding` for that. Do not use this skill for an executive briefing slide deck or a regulatory notification letter — those are separate document types.

---

## 3. Files in This Skill

| File | Purpose |
|---|---|
| `incident-report-template.md` | Copy-paste skeleton — complete every `[REQUIRED]` field before delivery |
| `analysis-reference.md` | Reference for timeline construction, IOC defanging, and ATT&CK mapping |

---

## 4. Procedure

1. Open `incident-report-template.md` and copy the full template into a working draft.
2. Fill the **Metadata** section first: report ID, TLP classification, author (role), date, version, status, and distribution list.
3. Write the **Timeline** before any other narrative section. The timeline is the evidentiary foundation of the report. Every other section references it. Use `analysis-reference.md` § 1 for format, inferred-timing conventions, and dwell time / MTTD / MTTR calculation.
4. Write **Technical Detail / Root Cause** using the timeline as the reference spine. Separate observed facts from assessments explicitly.
5. Write **Impact and Scope** with precision. Distinguish systems confirmed affected, potentially exposed, and cleared. Distinguish data *accessed* from data *exfiltrated* from data *at risk*. Where scope is unknown, state the visibility limit — do not silently claim no impact.
6. Populate the **IOC table**. Defang all network IOCs. Apply the confidence scale from `analysis-reference.md` § 2.
7. Build the **ATT&CK mapping** from the timeline. Each technique must be anchored to a specific observed event. Use `analysis-reference.md` § 3 for guidance.
8. Complete **Response Actions** in PICERL order with timestamps, responsible roles, and outcomes.
9. Write **Lessons Learned** blameless. Attribute findings to systems, processes, and controls. Every corrective action must have an owner (by role) and a due date.
10. Write the **Executive Summary** last — it summarizes the completed report in plain language for non-technical leadership.
11. Before delivering, use OpenCode's Skill tool to load `verify-security-language` and apply it to the full draft.

---

## 5. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Speculation stated as fact | "The threat actor exfiltrated customer records." (no forensic confirmation) | Demote to assessment with likelihood and confidence qualifiers: "We assess with moderate confidence that customer records were likely accessed; exfiltration has not been confirmed at this time." |
| Blame assigned to individuals | "The analyst missed the alert." / "The ops team failed to patch the system." | Attribute to the system or process: "The alerting configuration did not produce a notification within the detection window." / "The patch deployment process did not apply the update within the maintenance window." |
| Missing or non-chronological timeline | Narrative prose with approximate times; events listed out of order | Tabular timeline, chronological, ISO 8601 UTC, with source evidence per row |
| Timezone not specified | "Alert fired at 2:32pm" | ISO 8601 UTC: `2026-06-28T14:32:00Z`; state "all times UTC" once at the top |
| "Accessed" vs. "exfiltrated" conflation | "Data was stolen / exfiltrated" when only access is confirmed | Separate: data accessed (confirmed by log), data exfiltrated (confirmed by forensic artifact showing data leaving environment), data at risk (co-located, not confirmed). State visibility limits. |
| Vague scope without stating visibility limits | "No other systems were affected." (when other systems were not investigated) | State what was investigated and what was not: "The following systems were within the investigation scope and found unaffected: [list]. The following systems were not within scope and cannot be assessed at this time: [list]." |
| Recommendations with no owner or deadline | "MFA should be implemented." | Assign a role and a date: "Owner: Identity and Access Management team. Due: 2026-07-15. Priority: High." |
| Live un-defanged IOCs | `http://malware.example.com/payload` in report body | `hxxp://malware[.]example[.]com/payload` in all human-readable sections |
| ATT&CK techniques unsupported by evidence | Including T1048 (Exfiltration Over Alternative Protocol) with no observed artifact | Only map techniques to events with evidence. List intelligence-sourced but unobserved techniques separately with "(unconfirmed)" and low-confidence qualifiers. |
| Overstating certainty before forensics is complete | "Root cause confirmed: phishing email opened by user in Finance." (before full investigation) | Use calibrated language: "We assess with moderate confidence that initial access was likely obtained via a phishing email attachment; full forensic confirmation is pending." |

---

## 6. Language Rules

This skill inherits all language rules from the `security-language` standard. The following rules have particular force in incident reports:

- **Never write "attacker."** Use "external party" or "threat actor." The term presumes hostile intent and attribution that may not be established.
- **Never write "unauthorized access."** State specifically: (a) whether authentication occurred, (b) whether the actor held authorization for the resource, and (c) what was accessed. Use "inappropriate access" with those specifics.
- **Do not use "vulnerability" as a label for an unconfirmed or alleged issue.** Use "weakness," "finding," or "observed condition." CVE identifiers, CWE identifiers, and CVSS scores are proper nouns and are kept as-is.
- **Distinguish data accessed from data exfiltrated.** "Accessed" means the data was touched or read in place, confirmed by log evidence. "Exfiltrated" means confirmed transfer outside the environment, supported by a forensic artifact (e.g., netflow, proxy log, DLP alert). Do not use the stronger term unless the evidence supports it.
- **Never assert a compliance outcome.** Do not write "this is a GDPR violation," "we are non-compliant," or "this violates [regulation]." State the observed condition and flag it for counsel/compliance review: "This may have implications under [framework] — recommend review by compliance/counsel."
- **Likelihood and confidence are two separate axes.** Never collapse them. Canonical form: "We assess with [confidence] confidence that [subject] [likelihood term] [conclusion]."
- **Blameless.** Attribute findings to systems, configurations, and processes. Use roles, not names. Do not use "should have," "failed to," or "neglected to" applied to individuals.

---

## 7. Final Step — Before Delivery

Use OpenCode's Skill tool to load `verify-security-language` and apply it to the completed draft. Confirm exit 0 before delivering the report. Do not deliver a draft that exits non-zero.
