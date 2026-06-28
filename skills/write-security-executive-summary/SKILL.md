---
name: write-security-executive-summary
description: (hgto/security-skills) Use when writing an executive summary or leadership briefing on a security topic, vulnerability, threat, or incident for a non-technical or senior audience, or when asked for a BLUF, board summary, or bottom-line-up-front writeup.
---

**REQUIRED SUB-SKILL:** security-language

---

## 1. Overview

An executive summary for a security topic has one job: tell a senior decision-maker what they need to know and what they need to decide, in the order of importance, in about one page.

**BLUF — Bottom Line Up Front.** Start with the conclusion, the impact, and the ask. Do not build to the point. A reader who stops after the first paragraph must still have the information they need to act.

**Descending priority.** Each section is less essential than the one above it. If the document were cut in half, the top half must remain complete and actionable. Never bury the most important information in the middle or at the end.

**Business language, not technical language.** The audience is accountable for business outcomes, not system configurations. Translate technical findings into business consequences: financial exposure, service continuity, data at risk, regulatory considerations. Technical detail belongs in a supporting brief, not the summary.

**Calm and factual — no FUD.** Fear, uncertainty, and doubt undermine credibility and impair decision-making. Quantify risk rather than dramatizing it. Avoid vague intensifiers ("critical," "alarming," "devastating") — replace them with specific numbers: dollars, records, hours of downtime, percentage of affected systems. If a number is unavailable, say what is known and what is under investigation.

**One page.** If the draft runs long, trim Context and Key Points before trimming Risk/Business Impact or Recommendations. Decision-makers need the stakes and the ask; they do not need extended background.

---

## 2. When to Use

Use this skill when:

- Writing an executive summary, board briefing, or leadership update on a security finding, active incident, threat, or risk topic.
- Translating a detailed technical report or incident timeline into a format appropriate for non-technical leadership.
- Producing a BLUF, one-pager, or bottom-line-up-front summary for a senior audience.
- Any time the primary reader is a decision-maker rather than a technical practitioner.

Do not use this skill to write a detailed technical finding, an incident timeline, or a technical remediation guide — those have their own skills.

---

## 3. Files in This Skill

| File | Purpose |
|---|---|
| `exec-summary-template.md` | Copy-paste skeleton — complete every **[REQUIRED]** field before delivery |
| `references-guide.md` | Source tier definitions, annotated-reference format, worked examples |

---

## 4. Procedure

1. **Start with `exec-summary-template.md`.** Copy the full template. Do not delete sections — if a section does not apply, note why and leave a brief explanation.

2. **Write the BLUF first.** Before writing anything else, draft the three-sentence bottom line: situation, impact, ask. The rest of the document supports this paragraph; if the BLUF is unclear, the document will not improve it.

3. **Quantify risk in the Risk / Business Impact section.** Every quantitative field must be populated or explicitly noted as unavailable with a statement of what is known. "May be significant" is not a business impact statement.

4. **Write recommendations with owners, costs, and timelines.** Each recommendation must name the specific action, the role responsible, the estimated cost or effort, the deadline, and the exact decision being requested. "Take appropriate action" is not a recommendation.

5. **Add annotated references for every major claim.** Consult `references-guide.md` for the source tier hierarchy and annotation format. Tie each urgency, scope, or exploitation characterization to a primary source. A bare hyperlink is not a reference.

6. **Review for language compliance.** Apply the language rules in Section 6 of this skill and the `security-language` standard throughout.

7. **Before delivering, run `verify-security-language`** on the draft and confirm it exits clean.

---

## 5. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Too technical / jargon-heavy | "The CVSSv3.1 base score of 9.8 AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H indicates critical severity." | Translate to business consequence: "The weakness can be exploited remotely without credentials across all affected systems." Keep the CVSS score in a supporting brief or footnote. |
| Burying the lede | Three paragraphs of context before stating what happened or why it matters | Write the BLUF first: situation + impact + ask, in that order, in the first paragraph. |
| No clear ask | "We wanted to bring this to leadership's attention." | Every executive summary must close with a specific decision requested, an owner for each action, and a timeline. If there is no ask, there should be no summary. |
| Fear-mongering / FUD | "This is a devastating, catastrophic threat that could destroy the company." | Replace vague intensifiers with specific numbers. "Approximately 40% of production systems are affected; estimated service disruption is 4–8 hours; financial exposure is estimated at $X." |
| Unsourced claims | "This weakness is being actively exploited globally." | Every major claim — especially exploitation status and urgency — must cite a primary source with issuer, identifier, and date. See `references-guide.md`. |
| Unquantified risk | "The potential impact could be severe." | Use the Risk / Business Impact table in `exec-summary-template.md`. State dollars, records, hours of downtime, percentage of systems — or explicitly state what is unknown and why. |
| Length bloat | Multi-page summary with extended technical detail | Aim for one page. Cut Context and Key Points if needed; protect the BLUF, Risk/Business Impact, and Recommendations sections. |

---

## 6. Language Rules

This skill inherits all language rules from the `security-language` standard. The following rules are especially important in executive summaries, where imprecise language reaches the widest and most consequential audience.

- **Do not use "attacker."** Use "external party" or "threat actor." Both are equally clear to any audience and remain defensible if attribution later changes or is contested.
- **Do not use "weakness" and "finding" interchangeably with CVE/CWE identifiers.** CVE and CWE are proper nouns and are kept as-is. The word "weakness" or "finding" is used to describe an unconfirmed or emerging condition; once a CVE is assigned, use the CVE identifier.
- **Do not write "unauthorized access."** State (a) whether authentication occurred and (b) whether the party held authorization for the resource. Describe the access using "inappropriate access" with specifics: (c) what was accessed, (d) how, and (e) the scope.
- **Do not render a compliance or legal opinion.** Any regulatory angle is phrased as a flagged consideration for counsel or compliance review: "this situation may warrant review under [framework]." Never assert that a situation constitutes a violation, is non-compliant, or is illegal.
- **Do not use vague intensifiers.** Replace "critical," "massive," "devastating," and similar terms with the specific number or scope they are intended to convey.
- **Separate observed fact from assessment.** What was confirmed is not the same as what is inferred. Inferences must carry a likelihood qualifier and a confidence level per the `security-language` estimative-language standard.
