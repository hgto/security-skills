# Estimative Language Reference

**Standard:** ODNI ICD 203 (Intelligence Community Directive 203 — Analytic Standards), adapted for corporate security reporting.

Estimative language rests on two independent axes: **likelihood** (how probable is the event or conclusion?) and **confidence** (how good is the underlying sourcing?). These axes must never be collapsed into a single term. Both must be stated explicitly when making an assessment.

---

## Axis 1 — Likelihood (Words of Estimative Probability)

| Term | Probability Range | Notes |
|---|---|---|
| Almost no chance / Remote | 01–05% | Reserve for near-impossible outcomes; state basis |
| Very unlikely | 05–20% | Significantly below even odds |
| Unlikely | 20–45% | Below even odds |
| Roughly even chance | 45–55% | True uncertainty; neither direction favored |
| Likely / Probable | 55–80% | Above even odds |
| Very likely | 80–95% | Strongly favored |
| Almost certain | 95–99% | Reserve for near-certain outcomes; state basis |

**Usage notes:**

- Choose the term whose probability range best reflects the evidence, not the term that sounds most confident.
- Avoid "possible" as a standalone likelihood term — it covers nearly the entire range (1–99%) and conveys nothing.
- Numerical ranges may be stated parenthetically when the audience expects quantified risk: "likely (assessed at approximately 65–70%)."
- Do not use "certain" (100%) or "impossible" (0%) — see Absolutes Blocklist in `word-substitutions.md`.

---

## Axis 2 — Confidence (Sourcing Quality)

Confidence reflects the quantity, quality, and corroboration of the sources underlying an assessment. It is independent of likelihood.

| Confidence Level | Meaning |
|---|---|
| **High** | The assessment is based on high-quality information and/or multiple corroborating independent sources. Analytic reasoning is sound. Significant contrary evidence would be required to change the assessment. |
| **Moderate** | The assessment is based on credible information, but sources are limited, single-sourced, or partially corroborated. The assessment is reasonable but could change with additional reporting. |
| **Low** | The assessment is based on limited or questionable information, or relies heavily on analytic inference with minimal direct sourcing. The conclusion may change significantly as more information becomes available. |

**Usage notes:**

- High confidence does not mean high likelihood, and vice versa. A low-likelihood outcome can be assessed with high confidence (e.g., "We assess with high confidence that it is very unlikely the actor has access to additional systems").
- Confidence is about the evidence base, not about how certain the analyst feels.
- When sourcing is very thin, state the visibility limit explicitly rather than defaulting to "low confidence" alone (see Visibility Limits below).

---

## Canonical Combined Form

Both axes must appear together in any assessment statement. The standard form is:

> "We assess with [confidence level] confidence that [subject] [likelihood term] [conclusion]."

**Examples:**

- "We assess with moderate confidence that the actor almost certainly had access to the email server for a period prior to detection."
- "We assess with low confidence that it is unlikely additional accounts were used; our log visibility during this window was limited."
- "We assess with high confidence that customer records were likely accessible to the actor; database access logs confirm authenticated queries to the customer table during the window in question."

---

## "No Evidence" Is Not the Same as "Did Not Happen"

When investigation has not confirmed an event, state the visibility limit — do not assert the negative.

| Do not write | Write instead |
|---|---|
| "Data was not exfiltrated." | "No evidence of data transfer beyond the network perimeter was identified within the log retention window (14 days)." |
| "The actor did not access backups." | "Backup access logs were not available for the period in question; we cannot confirm or rule out backup access." |
| "No other systems were affected." | "No additional affected systems were identified in the scope of this investigation; systems outside scope were not reviewed." |

**Rule:** "No evidence of X" means "we looked and did not find it, within the limits of what we could see." It is not a statement that X did not occur. State the scope and limits of the investigation alongside any negative finding.

---

## Defining the Scale in Each Report

Define the likelihood and confidence scales once, near the beginning of any document that uses estimative language. Do not assume the reader shares a common reference:

> "This report uses ODNI ICD 203 estimative language. Likelihood terms (e.g., 'likely,' 'unlikely') correspond to probability ranges defined in the Estimative Language Reference. Confidence levels (high/moderate/low) reflect the quality and corroboration of underlying sources, not the degree of likelihood."

Subsequent uses of the terms within the same document do not need to be re-defined.
