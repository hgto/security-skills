# Finding Template

Copy this template for each discrete finding. Complete every field. Fields marked **[REQUIRED]** must not be left blank; fields marked **[IF APPLICABLE]** may be omitted with a note explaining why.

Replace all placeholder text in `<angle brackets>` before delivery.

---

## `<N>. <Finding title>` **[REQUIRED]**

The finding's header is its number plus its title — nothing else. Number findings sequentially: 1, 2, 3, 4. Do not add a separate "Title" field or a `PREFIX-YYYY-NNN` ID.

e.g. `## 1. SQL Injection — /api/login username Parameter`

**Rules for the title:**
- Name the weakness class, not the symptom or the observable artifact. "SQL Injection in Login Endpoint" is correct. "Database Error Returned to Client" names a symptom. "Security Issue in Login" is too vague.
- Do not use the word "vulnerability" in the title. Write the weakness name directly.
- Do not start with "Possible" or "Potential" — qualify severity instead.
- Keep it under 80 characters.

**Examples:**
- 1. SQL Injection — `/api/login` `username` Parameter
- 2. Reflected Cross-Site Scripting — `/search` `q` Parameter
- 3. Missing Authorization Check on Administrative Endpoint `/admin/users`
- 4. Insecure Direct Object Reference — Order Records Accessible Without Ownership Verification

---

## Severity **[REQUIRED]**

Single dense line — rating, then the full vector string, then the score:

`<Rating> — <full vector string> → <score>`

e.g. `Critical — CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H → 9.8`

(For OWASP Risk Rating, give the rating then the Likelihood × Impact result — e.g. `High — Likelihood 6.5 × Impact 7.0`.)

**Metric Rationale:**

| Metric | Value | Rationale |
|---|---|---|
| `<Metric name>` | `<Value>` | `<One-line explanation tied to the specific finding>` |

*(Repeat rows for each metric. See `severity-rating.md` for CVSS metric definitions and the OWASP factor table.)*

**Business/Environmental Context:**

`<One sentence reconciling the base score with the specific environment — data classification, compensating controls, exposure scope, or other organizational factors.>`

---

## Affected Assets **[REQUIRED]**

List each affected component precisely. Vague entries ("the web application") are not acceptable.

| Asset | Details |
|---|---|
| Host / URL | `<e.g., https://api.example.com/api/login>` |
| Parameter / Field | `<e.g., POST body: username>` |
| Component / Version | `<e.g., ExampleApp v3.4.1 — commit a1b2c3d>` |
| Environment | `<Production | Staging | Development>` |

---

## Description **[REQUIRED]**

Explain the root cause and mechanism of the weakness — not what was observed on screen, but why the condition exists and how it operates.

Structure:

1. **Root cause:** `<What configuration, code pattern, or missing control creates this condition?>`
2. **Mechanism:** `<How does the weakness operate? What can be done because the control is absent or ineffective?>`
3. **Scope:** `<Is this an instance (one location) or a class (pattern recurring across the codebase/system)?>`

**Example:**

> The `/api/login` endpoint constructs a SQL query by concatenating the `username` POST parameter directly into the query string without parameterization or input validation. The database account used by the application has read and write access to all tables in the schema. This pattern appears in one confirmed location; a full codebase review should determine whether the pattern recurs elsewhere.

---

## Impact **[REQUIRED]**

State the business consequence and the technical mechanism in separate sentences. "This could be bad" is not acceptable.

**Technical impact:** `<What can be done at the system or data level? Be specific — table names, record counts (if known), operations (read/write/delete).>`

**Business impact:** `<What does the technical impact mean for the organization — data exposure, service disruption, financial exposure, reputational harm, regulatory implications (note: flag for counsel/compliance if applicable — do not render a legal opinion)?>`

**Example:**

> **Technical:** An external party with network access to the endpoint can read, modify, or delete any row in the application database, including the `users`, `orders`, and `payment_methods` tables.
>
> **Business:** Exposure of customer records from the `users` table (approximately 1.2 million accounts per the production data dictionary) would likely result in mandatory notification obligations and significant reputational harm. Modification of the `orders` or `payment_methods` tables could disrupt order processing. This finding has potential regulatory implications that should be reviewed by counsel/compliance.

---

## Likelihood / Exploitability **[REQUIRED]**

Assess how likely exploitation of this weakness is in the current environment. Separate **likelihood** from **confidence** — they are independent.

- **Likelihood of exploitation:** `<almost certain | very likely | likely | roughly even chance | unlikely | very unlikely | remote>`
- **Confidence in this assessment:** `<high | moderate | low>`
- **Key factors:** `<What drives likelihood? Authentication requirements, network exposure, known exploit code, active exploitation reports, complexity of exploitation, required privileges.>`

**Example:**

> We assess with **high confidence** that exploitation is **likely**. The endpoint is internet-reachable, requires no authentication, and the weakness class (SQL injection) is well understood and routinely exploited. No confirmed exploit of this specific instance has been identified.

---

## Evidence / PoC **[REQUIRED]**

Provide evidence sufficient for a developer to reproduce and confirm the condition independently. Evidence must be:

- **Reproducible:** Step-by-step — another person must be able to follow these steps and observe the same result.
- **Redacted:** Remove or replace all real credentials, PII, internal hostnames, and tokens. Use clearly marked placeholders: `[REDACTED]`, `<token>`, `<username>`.
- **Non-destructive:** Do not include steps that delete records, exfiltrate real data, or disrupt production services. Demonstrate the weakness class with a benign payload or a staging environment.

**Reproduction steps:**

1. `<Step 1 — e.g., Send the following HTTP request to the target endpoint:>`
2. `<Step 2>`
3. `<Step n>`

**Request:**

```
POST /api/login HTTP/1.1
Host: <target-host>
Content-Type: application/json

{
  "username": "' OR '1'='1",
  "password": "[REDACTED]"
}
```

**Response / Observed behavior:**

```
<Paste the relevant portion of the response. Redact PII, tokens, and credentials.
Include only the fields necessary to demonstrate the condition.>
```

**Screenshot / Artifact:** `<Path to screenshot or attach inline. Redact before attaching.>` **[IF APPLICABLE]**

---

## Remediation **[REQUIRED]**

Remediation must be actionable and root-cause-oriented. "Fix the issue" or "apply security best practices" is not acceptable.

### Short-Term (Tactical)

`<What can be done immediately to reduce exposure without a full fix? Examples: disable the affected endpoint, add a WAF rule, revoke the affected credential, restrict network access. Note limitations — these are not permanent fixes.>`

### Durable Fix

`<What is the correct, root-cause-oriented fix? Reference the specific code pattern, configuration, or architectural change required. Link to a library, API, or specification where appropriate.>`

**Example:**

> **Short-term:** Temporarily restrict access to `/api/login` to known IP ranges via the load balancer ACL. This reduces exposure but does not eliminate the weakness.
>
> **Durable:** Replace the string-concatenation query construction with parameterized queries (prepared statements) using the application's existing database library. Reference: OWASP SQL Injection Prevention Cheat Sheet. Audit all other query-construction patterns in the codebase for the same pattern (see Description — scope).

---

## References **[REQUIRED]**

| Type | Reference |
|---|---|
| CWE | `<e.g., CWE-89: Improper Neutralization of Special Elements used in an SQL Command>` |
| OWASP | `<e.g., OWASP Top 10 A03:2021 – Injection>` |
| CVE | `<CVE identifier if a known CVE applies — e.g., CVE-2024-XXXXX>` **[IF APPLICABLE]** |
| Additional | `<Vendor advisory, internal policy, framework documentation, or other reference>` **[IF APPLICABLE]** |

---

## Status **[REQUIRED]**

| Field | Value |
|---|---|
| Status | `<Open | In Remediation | Remediated | Accepted Risk | Duplicate | Won't Fix>` |
| Date identified | `<YYYY-MM-DD>` |
| Date reported | `<YYYY-MM-DD>` |
| Target remediation date | `<YYYY-MM-DD>` **[IF APPLICABLE]** |
| Date verified resolved | `<YYYY-MM-DD>` **[IF APPLICABLE]** |
| Assigned to | `<Team or role — not individual name>` |
| Notes | `<Anything affecting status — e.g., "risk accepted pending architectural redesign scheduled for Q3">` **[IF APPLICABLE]** |
