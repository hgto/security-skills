# Executive Summary Template

Copy this template in full. Work top to bottom. Complete every **[REQUIRED]** field before delivery. Fields marked **[if applicable]** may be omitted only if they genuinely do not apply — note why.

Aim for one page. If the draft exceeds one page, trim Context and Key Points before trimming Risk/Business Impact or Recommendations.

---

## [Document Title]

**Classification:** [e.g., Confidential — Internal Distribution Only]
**Prepared for:** [Audience: e.g., Executive Leadership Team]
**Prepared by:** [Author / Team]
**Date:** [YYYY-MM-DD]
**Status:** [Draft / For Review / Final]

---

## BLUF — Bottom Line Up Front

**[REQUIRED — ≤3 sentences. Lead with: (1) what the situation is, (2) what the business impact is, and (3) what decision or action you are asking for. Write for a reader who will read only this paragraph.]**

Example structure:
> [Situation in one clause]. [Business impact in one clause]. [The specific ask — approval, decision, or action — in one clause].

---

## Context

**[REQUIRED — 2–4 sentences. Provide the minimum background needed to understand the BLUF. Do not introduce new recommendations here — this section provides context, not analysis.]**

Cover: what the affected system or service is; how the situation came to our attention; the timeline of relevant events. Avoid technical jargon. If a technical term is unavoidable, define it in plain language on first use.

---

## Key Points

**[REQUIRED — 3–5 bullets. Each bullet leads with the point, not the supporting detail. Write the conclusion first, then one phrase of support. Do not bury the finding at the end of a bullet.]**

- **[Point]:** [one phrase of supporting detail]
- **[Point]:** [one phrase of supporting detail]
- **[Point]:** [one phrase of supporting detail]
- **[Point — if applicable]:** [one phrase of supporting detail]
- **[Point — if applicable]:** [one phrase of supporting detail]

---

## Risk / Business Impact

**[REQUIRED — quantify. Generic impact statements ("this could be severe") are not acceptable. Use the fields below. Omit a row only if the figure is genuinely unavailable; if unavailable, say so and state what is known.]**

| Dimension | Current Estimate | Basis |
|---|---|---|
| Systems or services affected | [# or % of fleet, or N/A with explanation] | [Source or method] |
| Data at potential exposure | [# records, data types, or N/A] | [Source or method] |
| Estimated downtime / service disruption | [hours or range, or N/A] | [Source or method] |
| Estimated financial exposure | [$range, or N/A with explanation] | [Source or method] |

**Regulatory considerations [if applicable]:** [State the observed condition in factual terms. If it may be relevant to a compliance framework, flag it for review — do not render a legal or compliance opinion. Example: "Personal data was accessible without authentication controls in place; this situation may warrant review under applicable data protection requirements — recommend referral to legal/compliance."]

---

## Recommendations / Decisions Needed

**[REQUIRED — list in priority order. Each recommendation must specify: the exact action, the owner, the estimated cost or effort, the timeline, and the specific decision you are asking this audience to make or approve. "Take action" is not a recommendation.]**

### 1. [Highest-priority recommendation title]

- **Action:** [Specific action in plain language]
- **Owner:** [Role or team, not a personal name]
- **Cost / effort:** [Dollar figure or person-days]
- **Timeline:** [By when; state whether this is driven by an external deadline such as a CISA BOD or a contractual date]
- **Decision requested:** [Exactly what you are asking the reader to approve, fund, or decide]

### 2. [Next recommendation]

- **Action:**
- **Owner:**
- **Cost / effort:**
- **Timeline:**
- **Decision requested:**

### 3. [if applicable]

*(Add additional recommendations in priority order. Limit to what requires this audience's decision or awareness — operational details belong in the supporting technical brief.)*

---

## References

**[REQUIRED — cite every Tier 1 or Tier 2 source that supports a major claim in this document. Format: Issuer + Identifier + Date — what it establishes and why relevant + primary source URL. See `references-guide.md` for the full format and tier definitions.]**

1. [Issuer] [Identifier] ([Date]) — [What it establishes and why relevant]. [Primary source URL]
2. [Issuer] [Identifier] ([Date]) — [What it establishes and why relevant]. [Primary source URL]
3. [if applicable]

---

*Delivery checklist — confirm before sending:*

- [ ] BLUF is ≤3 sentences: situation + impact + the ask
- [ ] No technical jargon without a plain-language definition on first use
- [ ] Every bullet leads with the point, not the supporting detail
- [ ] All quantitative fields in Risk / Business Impact are populated or noted as unavailable
- [ ] Any regulatory angle is phrased as a flagged consideration, not an asserted finding or legal opinion
- [ ] Every recommendation specifies owner, cost, timeline, and the exact decision requested
- [ ] Every major claim in the body has a corresponding annotated reference
- [ ] `verify-security-language` has been run and exited clean
