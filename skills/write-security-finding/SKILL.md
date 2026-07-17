---
name: write-security-finding
description: (hgto/security-skills) Use when writing up a security finding, vulnerability, pentest result, code-review issue, or audit observation, or when documenting a single discovered weakness with its severity, impact, evidence, and remediation.
---

**REQUIRED SUB-SKILL:** security-language

Use OpenCode's Skill tool to load `security-language` before drafting the finding.

---

## 1. Overview

This skill structures a single security finding so that it is defensible, actionable, and readable by both technical and non-technical audiences. Every finding follows the same spine:

1. **Header** — the finding number plus its title (e.g. `## 1. SQL Injection — /api/login username Parameter`); names the weakness class, not the symptom or a generic label
2. **Severity** — justified with a full CVSS vector string or an OWASP Risk Rating factor table; never a bare label
3. **Affected Assets** — precise: host, URL, parameter, component version, environment
4. **Description** — root cause and mechanism; distinguishes instance from class
5. **Impact** — business consequence and technical mechanism, stated separately
6. **Likelihood / Exploitability** — likelihood and confidence stated as independent axes
7. **Evidence / PoC** — reproducible, redacted, non-destructive; numbered repro steps
8. **Remediation** — short-term tactical action plus durable root-cause-oriented fix
9. **References** — CWE, OWASP, CVE identifiers; no bare hyperlinks
10. **Status** — lifecycle tracking

A finding that omits any of these fields is incomplete and should not be delivered.

---

## 2. When to Use

Use this skill when:

- Documenting a confirmed or potential weakness from a penetration test, red team engagement, code review, threat model, or audit.
- Writing up a single finding for a report section, a ticket, or a standalone advisory.
- Translating a raw scanner output, a bug report, or informal notes into a structured finding that meets the security-language standard.

Do not use this skill to write an executive summary, an incident report, or a full report introduction — those have their own skills.

---

## 3. Files in This Skill

| File | Purpose |
|---|---|
| `finding-template.md` | Copy-paste skeleton — complete every **[REQUIRED]** field before delivery |
| `severity-rating.md` | CVSS and OWASP Risk Rating reference — use for the Severity field |

---

## 4. The Spine in Detail

### 4.1 Header

The header is the finding number plus the title — e.g. `## 1. SQL Injection — /api/login username Parameter`. Number findings simply: 1, 2, 3, 4. Do not label the field "Title" and do not use a `PREFIX-YYYY-NNN` ID.

Name the weakness, not the symptom. The title is the most-read field in any finding list.

| Wrong | Right | Why |
|---|---|---|
| "Database Error Returned to Client" | "SQL Injection — `/api/login` `username` Parameter" | Names the symptom, not the weakness |
| "Security Issue in Login" | "SQL Injection — `/api/login` `username` Parameter" | Too vague to triage or search |
| "Vulnerability in Search Endpoint" | "Reflected Cross-Site Scripting — `/search` `q` Parameter" | Do not use "vulnerability" in the title — write the weakness name directly |

### 4.2 Severity

A severity label without a vector or factor table is not a justification. See `severity-rating.md` for:

- CVSS v3.1 vs v4.0 differences (v4.0 removed Scope, added Attack Requirements, introduced CVSS-B/BT/BTE nomenclature).
- Score bands: None 0.0 / Low 0.1–3.9 / Medium 4.0–6.9 / High 7.0–8.9 / Critical 9.0–10.0.
- Required: full vector string, metric-by-metric rationale, one-sentence business/environmental reconciliation.
- OWASP Risk Rating: Likelihood × Impact, each averaged 0–9, 3×3 matrix.

### 4.3 Description

Explain root cause and mechanism. Do not describe what appeared on screen — explain why the condition exists.

Distinguish **instance** (one location) from **class** (pattern that may recur). If the weakness is a class, say so and recommend a codebase-wide review.

### 4.4 Impact

State business consequence and technical mechanism separately. "This could be bad" is not acceptable. Quantify where possible: table names, estimated record counts, affected operations, service disruption scope.

When impact has regulatory implications, state the observed condition and flag it for counsel/compliance review. Do not render a legal or compliance opinion.

### 4.5 Evidence / PoC

Evidence must be:

- **Reproducible:** numbered steps that another person can follow to observe the same condition.
- **Redacted:** replace all real credentials, PII, internal hostnames, and tokens with clearly marked placeholders (`[REDACTED]`, `<token>`, `<username>`).
- **Non-destructive:** demonstrate the weakness class using a benign payload or a staging environment; do not include steps that delete records, exfiltrate real data, or disrupt production services.

### 4.6 Remediation

Provide two tiers:

- **Short-term (tactical):** immediate exposure reduction without a full fix. State its limitations explicitly.
- **Durable fix:** the root-cause-oriented change — specific code pattern, configuration, or architectural change required. Reference the relevant library, API, or specification.

"Apply security best practices" is not remediation. Reference the exact fix.

---

## 5. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| No impact articulation | "This could allow unauthorized access." | State business consequence and technical mechanism separately; quantify. Replace "unauthorized access" with authentication/authorization status and "inappropriate access" with specifics. |
| Scanner-dump vagueness | Paste of tool output with no context | Translate to the finding spine; explain root cause and mechanism in your own words |
| Severity not justified | "Severity: High" with no vector or factors | Include the full CVSS vector string or OWASP factor tables; see `severity-rating.md` |
| Non-actionable remediation | "Fix the SQL injection" or "apply best practices" | Name the specific fix — parameterized queries, specific library, configuration change — with a reference |
| Non-reproducible PoC | "I confirmed this in Burp" | Provide numbered repro steps with the exact request/response, redacted |
| Instance-vs-class confusion | Reports one URL when the pattern recurs across the codebase | State whether this is one instance or a class; recommend scope review where appropriate |
| Unredacted data | Request/response contains real PII, tokens, or credentials | Replace with `[REDACTED]` or typed placeholders before delivery |
| Symptom-as-title | "Error Message Disclosure" for an injection finding | Name the weakness class: "SQL Injection — `/api/login` `username` Parameter" |

---

## 6. Language Rules

This skill inherits all language rules from the `security-language` standard. The rules below apply to finding prose:

- Do not use the word "vulnerability" to describe a finding or weakness. Use "weakness," "potential weakness," "finding," or "observed condition." The proper nouns CVE, CWE, CVSS, and "Common Vulnerability Scoring System" are kept as-is.
- Do not write "unauthorized access." State (a) whether authentication occurred, (b) whether the actor held authorization for the resource, and (c) what was accessed. Use "inappropriate access" with those specifics.
- Do not write "attacker" or "hacker." Use "external party" or "threat actor."
- Do not render a legal or compliance opinion ("this is a GDPR violation," "this is non-compliant"). State the observed condition and flag it for counsel/compliance review.
- Separate observed fact from assessment. Inferences must carry an explicit likelihood qualifier and confidence level.

---

## 7. Procedure

1. Open `finding-template.md` and copy the full template.
2. Work through each field top to bottom. Do not skip fields — if a field does not apply, mark it `N/A` with a note.
3. For the Severity field, open `severity-rating.md` and complete either the CVSS metric table or the OWASP factor tables before writing the label.
4. Write Evidence / PoC as numbered repro steps. Review every line for PII, credentials, and internal hostnames before including them.
5. For Remediation, write both the short-term action and the durable fix. If you cannot write a specific durable fix, state what additional information is needed.
6. Before delivering, use OpenCode's Skill tool to load `verify-security-language` and apply it to the finding.
