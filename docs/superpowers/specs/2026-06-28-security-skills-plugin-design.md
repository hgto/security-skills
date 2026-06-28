# Design: `security-skills` Claude Code Plugin

**Date:** 2026-06-28
**Status:** Approved (design); pending implementation plan
**Repo:** to be renamed `hgto/security-writing` → `hgto/security-skills`

## Overview

A Claude Code plugin providing intent-triggered skills for security report
writing. There are five skills total: three document-writing skills, one shared
language *standard*, and one language *verifier*.

- The three document skills (findings, incident reports, executive summaries)
  each guide the author through a proven structure.
- `security-language` is the shared, strict standard for neutral, defensible
  language that the other skills require.
- `verify-security-language` applies that standard to an existing draft: a regex
  linter catches mechanical violations, and skill guidance re-frames the prose to
  be clinical.

Every skill's `description` begins with `(hgto/security-skills)` so its origin is
visible at a glance.

**No legal or compliance opinions.** Across every skill, these tools never give
legal or compliance advice and never advance a legal or compliance opinion. They
state observed facts neutrally and *flag* any matter with potential legal or
regulatory implications for review by counsel/compliance. They never assert a
"violation", a "compliance violation", or that a compliance/regulatory obligation
is being broken — that determination belongs to counsel/compliance, not the
report.

General-purpose and vendor-neutral. Cites public standards (NIST, OWASP, MITRE,
CISA, FIRST/CVSS, ODNI ICD 203). No org-specific names, scales, or templates.

## Plugin structure

```
.claude-plugin/plugin.json              # manifest (name, version, description)
README.md                               # what it is, the 5 skills, install
docs/superpowers/specs/                 # this design + plan
skills/
  security-language/                    # CENTRAL — strict discipline skill
    SKILL.md
    word-substitutions.md               # forbidden → preferred table (heavy ref)
    estimative-language.md              # ICD 203 WEP + confidence axes (heavy ref)
  verify-security-language/             # verifier — script + clinical reframe
    SKILL.md
    verify-language.py                  # regex linter
  write-security-finding/
    SKILL.md
    finding-template.md
    severity-rating.md                  # CVSS v3.1/v4.0 bands, OWASP risk, justification
  write-security-incident-report/
    SKILL.md
    incident-report-template.md         # NIST/PICERL-structured skeleton
    analysis-reference.md               # timeline format, IOC tables (defanged), ATT&CK
  write-security-executive-summary/
    SKILL.md
    exec-summary-template.md            # BLUF-first skeleton
    references-guide.md                 # annotated source format + authoritative tiers
```

## Skill: `security-language` (central, discipline)

MUST-follow standard, referenced by the other four via `**REQUIRED SUB-SKILL:**`.
Discipline skill: includes a rationalization table and red-flags list so it
resists pressure.

Contents:
- **Word-substitution table** (~20 pairs): `attacker`→`external party`/`threat
  actor`; plus `hacker`, `victim`, `breach`, `compromised`, `stolen`/`exfiltrated`
  (unconfirmed), `malicious`, `negligent`/`careless`, `obviously`/`clearly`,
  hyperbole (`catastrophic`, `devastating`), `backdoor`, `guilty`/`culprit`, etc.
  Legal terms of art (`breach`, `negligent`, `stolen`) flagged as
  "escalate to counsel / use neutral synonym."
- **No "vulnerability"**: the word infers a confirmed issue and is a compliance
  trigger. Use `weakness` / `potential weakness` / `finding` / `observed
  condition`. (Standard proper nouns — CVE, CWE, CVSS — are kept as names, and
  direct quotes from external advisories are left verbatim; the verifier's triage
  step handles those.)
- **No "unauthorized access"** (ambiguous): instead state whether authentication
  occurred and whether the actor was authorized, and describe the access as
  `inappropriate access` with specifics of what was accessed. Replacements
  elsewhere in the table that previously read "unauthorized access" /
  "unauthorized user" / "without authorization" are revised to this framing.
- **Absolutes blocklist**: "unhackable", "100% secure", "fully eliminated",
  "guaranteed", "impossible".
- **Fact vs. assessment**: observed (sourced, past tense, declarative) vs.
  assessed (hedged, confidence-qualified). The single load-bearing distinction.
- **Two separate axes** (detail in `estimative-language.md`): likelihood (WEP:
  likely/probable/almost certain, per ICD 203) ≠ confidence (low/moderate/high).
  Never collapse them.
- **Attribution caution**: default "unattributed"; describe TTPs not identity;
  confidence-qualify any attribution.
- **No legal/compliance opinions**: never write "violation", "compliance
  violation", "non-compliant", "violates [regulation]", "illegal/unlawful", or
  state that an obligation is breached. Instead, state the observed fact and flag
  for counsel/compliance review (e.g., "did not align with [control X]; may have
  implications under [framework] — recommend review by compliance"). Builds on the
  legal-terms-of-art handling above.
- **Blameless tone**: blame systems/process, not people; roles not names;
  forward-looking not punitive.

## Skill: `verify-security-language` (verifier)

Verb-first process skill. Independently invocable ("make this clinical", "check
this draft for loaded language") and used as the final step of the three
document skills. Carries `REQUIRED SUB-SKILL: security-language` and reuses its
word table as the single source of truth.

- **`verify-language.py`** — regex linter. Scans a draft; emits each hit with
  line, matched term, category (loaded-term / absolute / hyperbole / legal-term /
  second-person-blame / legal-compliance-opinion), and the preferred replacement.
  The `legal-compliance-opinion` category flags "violation", "compliance
  violation", "non-compliant", "violates", "illegal", "unlawful", "in breach of".
  Mechanical detection only.
- **Re-framing procedure** (skill judgment): run script → triage hits → reframe
  loaded terms; demote unsourced claims to assessments with confidence; strip
  absolutes/hyperbole; de-personalize blame → re-run script to confirm clean.

## Skill: `write-security-finding`

Spine (each field forces specificity to counter the top pitfalls):
Title (names the vulnerability, not the symptom) → Severity (justified, with CVSS
vector or OWASP factors — not a bare label) → Affected assets (precise) →
Description (root cause/mechanism) → Impact (business + technical "so what") →
Evidence/PoC (reproducible, redacted, non-destructive) → Remediation (actionable,
specific, root-cause-oriented) → References (CWE, OWASP, CVE).
`severity-rating.md` carries CVSS v3.1/v4.0 bands, OWASP Risk Rating, and how to
justify a rating. Final step: run `verify-security-language`.

## Skill: `write-security-incident-report`

NIST SP 800-61 / SANS PICERL structure: metadata + TLP → executive summary →
incident overview/classification → timeline (UTC, ISO 8601, evidence-anchored) →
technical detail / root cause → impact & scope (confirmed compromised vs.
potentially exposed; data *accessed* vs. *exfiltrated*) → IOCs (defanged, typed
table) → MITRE ATT&CK mapping (evidence-based) → response actions (PICERL) →
blameless lessons learned with owner + due date. `analysis-reference.md` carries
timeline columns, IOC table format/defanging, ATT&CK mapping format. Final step:
run `verify-security-language`.

## Skill: `write-security-executive-summary`

BLUF-first, descending priority, ~1 page, no FUD: BLUF (situation + impact + ask
in ≤3 sentences) → context → key points → business/quantified risk →
prioritized recommendations (owner, cost, timeline) → annotated references.
`references-guide.md` carries authoritative source tiers (NIST/CISA/MITRE/vendor)
and the annotated-reference format (issuer + identifier + date + one-line "what
it establishes"). Final step: run `verify-security-language`.

## Testing approach

Per the writing-skills Iron Law (no skill without a failing test first):
- `security-language` and `verify-security-language` are discipline skills — get
  baseline tests: a fresh agent writes "attacker"/absolutes without the skill;
  confirm the skill + verifier flip that. Capture rationalizations into the
  rationalization table.
- The three document skills are technique/reference skills — application-scenario
  checks: give an agent raw facts, verify output follows the spine and passes the
  verifier.

## Out of scope (YAGNI)

- No slash commands (intent triggers only).
- No org-specific templates, classification schemes, or distribution lists.
- No linting beyond the single `verify-language.py` (no CI integration, no editor
  plugin).

## Cross-reference convention

Skills reference each other by name with explicit requirement markers
(`**REQUIRED SUB-SKILL:** security-language`), never `@`-links (which force-load
and burn context). Note plugin namespacing may surface skills as
`security-skills:<skill-name>`.
