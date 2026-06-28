# References Guide — Executive Summary

Authoritative sources tell the reader *why* a claim is credible. Annotated references let an executive verify the claim without reading a technical paper. Every major factual assertion in an executive summary must trace to a primary source. This guide explains which sources to use, in what order, and how to format each citation.

---

## Source Tiers — Credibility Order

Use the highest-tier source available. Layer lower-tier sources only when they add distinct supporting evidence.

### Tier 1 — Government and Standards Bodies

These sources carry regulatory weight, are subject to federal review processes, and are the primary basis for urgency and business-impact claims.

| Source | What It Provides |
|---|---|
| NIST Special Publications (SP 800-series, SP 1800-series) | Baseline controls, risk management frameworks, configuration guidance |
| CISA Advisories (AA-series) and Known Exploited Weaknesses (KEV) Catalog | Confirmed active exploitation, affected products, recommended mitigations |
| NSA Cybersecurity Advisories | Nation-state TTPs, critical infrastructure guidance |
| FBI / IC3 Advisories | Criminal threat actor TTPs, sector-specific fraud patterns |

### Tier 2 — Frameworks and Catalogs

These sources describe observed behavior and weakness classifications. They provide vocabulary and context, not urgency.

| Source | What It Provides |
|---|---|
| MITRE ATT&CK | Taxonomy of observed adversary tactics, techniques, and procedures |
| MITRE D3FEND | Defensive countermeasure taxonomy, mapped to ATT&CK |
| CVE (Common Vulnerabilities and Exposures) | Unique identifier and description for a disclosed weakness |
| CWE (Common Weakness Enumeration) | Root-cause weakness classification |

### Tier 3 — Vendor Advisories

Vendor advisories are the **primary source** for patch status, affected versions, and remediation steps. Use them for those claims. Do not use them to establish urgency or scope beyond the vendor's own products.

| Source | What It Provides |
|---|---|
| Vendor security bulletins and advisories | Affected versions, patch availability, workarounds, severity scores |

### Tier 4 — Reputable Research and Reporting

Third-party research and security reporting corroborate claims or provide context. Use as supporting evidence alongside a Tier 1–3 source. Do not use as the sole basis for a major claim.

| Source | What It Provides |
|---|---|
| Peer-reviewed security research, established security firms, recognized news outlets | Corroborating context, technical detail, observed patterns |

---

## Annotated-Reference Format

Each citation must include five elements in this order:

```
[Issuer] [Identifier] ([Date]) — [What it establishes and why it is relevant to this document]. [Primary source URL]
```

**All five elements are required.** A bare hyperlink is not a reference. A reference without a date is not a reference.

---

## Worked Example

> CISA Advisory AA23-320A (Nov 2023) — Confirms active exploitation of a remote code execution weakness in Citrix NetScaler products and identifies affected versions; basis for the urgency and active-exploitation characterization in this summary. https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a

Breaking it down:

| Element | Value |
|---|---|
| Issuer | CISA |
| Identifier | AA23-320A |
| Date | Nov 2023 |
| What it establishes | Active exploitation confirmed; affected versions identified |
| Why relevant | Basis for urgency and active-exploitation characterization |
| Primary source URL | https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a |

---

## Worked Example — Multi-Source Claim

A claim that a finding affects a specific product version and is under active exploitation requires two sources: the vendor advisory (Tier 3) for the version claim, and the CISA KEV or advisory (Tier 1) for the exploitation characterization.

> Citrix Security Advisory CTX579459 (Oct 2023) — Identifies NetScaler ADC and Gateway versions affected by CVE-2023-4966; primary source for patch versions and recommended upgrade path. https://support.citrix.com/article/CTX579459
>
> CISA Known Exploited Weaknesses Catalog — CVE-2023-4966 entry (added Oct 2023) — Confirms active exploitation in the wild; basis for CISA's required remediation deadline under BOD 22-01. https://www.cisa.gov/known-exploited-vulnerabilities-catalog

---

## Rules for Use

**Tie every major claim to a source.** "Major claim" means any of the following:

- Active exploitation status ("this weakness is being exploited in the wild")
- Affected versions or products
- Scope of exposure (number of systems, percentage of fleet)
- Regulatory considerations ("this situation may warrant review under [framework]")
- Urgency characterization ("remediation is time-sensitive")

**Do not paraphrase sources in ways that change their scope.** A CISA advisory about a specific product family does not become evidence about a different product.

**Use the primary source URL, not an aggregator.** Link to the CISA advisory itself, not to a news article that quotes it. Link to the vendor bulletin itself, not to a CVE aggregator.

**Date every citation.** Sources are time-sensitive. An advisory from three years ago may have been superseded. Include the month and year; include the full date when available.

**Do not cite a source you have not read.** Citing an advisory for a claim it does not support is a credibility risk that will surface in executive scrutiny.
