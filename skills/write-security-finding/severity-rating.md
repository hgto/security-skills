# Severity Rating Reference

Use this reference when completing the **Severity** field of a finding. Every rating must be justified — a bare label is not acceptable. Choose either CVSS or OWASP Risk Rating; record both if the audience warrants it.

---

## 1. CVSS — Common Vulnerability Scoring System

### 1.1 Score Bands

| Band | Score Range | Meaning |
|---|---|---|
| None | 0.0 | No exploitable condition identified |
| Low | 0.1–3.9 | Exploitation requires significant preconditions or yields minimal impact |
| Medium | 4.0–6.9 | Partial impact or moderate complexity; prioritize with other factors |
| High | 7.0–8.9 | Significant impact or low complexity; prioritize promptly |
| Critical | 9.0–10.0 | High impact, low complexity, widely reachable; remediate immediately |

### 1.2 Version Differences: CVSS v3.1 vs CVSS v4.0

| Aspect | CVSS v3.1 | CVSS v4.0 |
|---|---|---|
| Scope concept | **Scope** (Changed / Unchanged) — does exploitation affect a component beyond the vulnerable one? | Removed. Replaced by separate **Vulnerable System** and **Subsequent System** impact groups |
| Attack complexity | Attack Complexity (Low / High) | Attack Complexity (Low / High) **+** new **Attack Requirements** metric (None / Present) — captures preconditions beyond the scorer's control |
| Score nomenclature | Single base score | Named tiers: **CVSS-B** (base), **CVSS-BT** (base + threat), **CVSS-BTE** (base + threat + environmental) |
| Environmental metrics | Available (unchanged) | Retained and expanded |

**Practical guidance:** Use v4.0 for new findings when your tooling supports it. When a finding references an existing CVE scored under v3.1, note the version and do not mix scores across versions in the same comparison table.

### 1.3 What to Record

Record the **full vector string**, not just the numeric score. The number is not reproducible without the vector.

**CVSS v3.1 example:**

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N  →  8.1 (High)
```

**CVSS v4.0 example:**

```
CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N  →  CVSS-B 9.3 (Critical)
```

### 1.4 Justification Rule

For every finding, record a metric-by-metric rationale:

| Metric | Value | Rationale |
|---|---|---|
| Attack Vector | Network | Endpoint is internet-reachable |
| Attack Complexity | Low | No preconditions beyond sending the request |
| Privileges Required | None | No authentication required |
| User Interaction | None | Exploitation does not require user action |
| Confidentiality Impact | High | Full contents of the target table are accessible |
| Integrity Impact | High | Insert and update operations are reachable |
| Availability Impact | None | No service disruption observed |

Then add one sentence reconciling the base score with business or environmental context:

> "Environmental factors — the table contains PII for approximately 1.2 million accounts, and no compensating WAF rule is deployed — align the environmental score with the base score of 8.1 High."

---

## 2. OWASP Risk Rating

### 2.1 Method

Score **Likelihood** and **Impact** independently, each on a 0–9 scale. Average the sub-factor scores within each dimension.

**Likelihood factors:** Skill level of threat agent, motive, opportunity, size of threat agent population, ease of discovery, ease of exploit, awareness, intrusion detection.

**Impact factors:** Loss of confidentiality, loss of integrity, loss of availability, loss of accountability; financial damage, reputational damage, non-compliance implications (note: flag for counsel/compliance — do not render a legal opinion), privacy exposure.

### 2.2 Score Buckets

| Score Range | Rating |
|---|---|
| 0–3 | Low |
| 3–6 | Medium |
| 6–9 | High |

### 2.3 Combined Risk Matrix (3×3)

|  | **Low Impact** | **Medium Impact** | **High Impact** |
|---|---|---|---|
| **Low Likelihood** | Note | Low | Medium |
| **Medium Likelihood** | Low | Medium | High |
| **High Likelihood** | Medium | High | Critical |

### 2.4 Justification Rule

Record a factor table for both dimensions:

**Likelihood factors:**

| Factor | Score | Notes |
|---|---|---|
| Ease of discovery | 9 | Discoverable via automated scanning |
| Ease of exploit | 7 | Public exploit code exists |
| Awareness | 6 | Well-known weakness class |
| Intrusion detection | 3 | Queries logged; alerting not confirmed |
| **Average** | **6.25** | **→ Medium Likelihood** |

**Impact factors:**

| Factor | Score | Notes |
|---|---|---|
| Confidentiality | 9 | Full table exposure |
| Integrity | 7 | Data modification possible |
| Availability | 3 | No disruption observed |
| Financial damage | 7 | PII at scale; regulatory implications (flag for counsel) |
| **Average** | **6.5** | **→ High Impact** |

**Combined rating:** Medium Likelihood × High Impact → **High**

Add one sentence of business/environmental reconciliation:

> "The table contains PII for approximately 1.2 million accounts; the Medium × High combination maps to High risk in the organizational context."

---

## 3. Complementary Frameworks

| Framework | Role | When to Use |
|---|---|---|
| **EPSS** (Exploit Prediction Scoring System) | Probabilistic likelihood that a known CVE will be exploited in the wild within 30 days | Use alongside CVSS for patching prioritization of known CVEs; not a replacement for CVSS |
| **SSVC** (Stakeholder-Specific Vulnerability Categorization) | Decision-tree model for prioritization based on exploitation status, utility to threat actors, and organizational impact | Use when prioritizing response across a large inventory; provides actionable deployment-decision outputs |
| **DREAD** | Historical severity rating model (Damage, Reproducibility, Exploitability, Affected users, Discoverability) | **Deprecated.** DREAD scores are subjective and not reproducible across teams. Do not use in new findings. Reference only when discussing a historical finding that originally used DREAD. |

---

## 4. Checklist Before Publishing a Severity Rating

- [ ] Full vector string recorded (not just the numeric score).
- [ ] Every metric has a one-line rationale.
- [ ] Business/environmental context sentence is present.
- [ ] CVSS version is stated (v3.1 or v4.0); scores from different versions are not mixed.
- [ ] If OWASP Risk Rating is used, both a Likelihood factor table and an Impact factor table are present.
- [ ] DREAD not used.
- [ ] No bare severity label without supporting evidence.
