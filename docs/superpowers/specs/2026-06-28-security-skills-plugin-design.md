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
- `security-writing-language` is the shared, strict standard for neutral,
  defensible language that the other skills require.
- `verifying-security-language` applies that standard to an existing draft:
  a regex linter catches mechanical violations, and skill guidance re-frames the
  prose to be clinical.

General-purpose and vendor-neutral. Cites public standards (NIST, OWASP, MITRE,
CISA, FIRST/CVSS, ODNI ICD 203). No org-specific names, scales, or templates.

## Plugin structure

```
.claude-plugin/plugin.json              # manifest (name, version, description)
README.md                               # what it is, the 5 skills, install
docs/superpowers/specs/                 # this design + plan
skills/
  security-writing-language/            # CENTRAL — strict discipline skill
    SKILL.md
    word-substitutions.md               # forbidden → preferred table (heavy ref)
    estimative-language.md              # ICD 203 WEP + confidence axes (heavy ref)
  verifying-security-language/          # verifier — script + clinical reframe
    SKILL.md
    verify-language.py                  # regex linter
  writing-security-findings/
    SKILL.md
    finding-template.md
    severity-rating.md                  # CVSS v3.1/v4.0 bands, OWASP risk, justification
  writing-incident-reports/
    SKILL.md
    incident-report-template.md         # NIST/PICERL-structured skeleton
    analysis-reference.md               # timeline format, IOC tables (defanged), ATT&CK
  writing-executive-summaries/
    SKILL.md
    exec-summary-template.md            # BLUF-first skeleton
    references-guide.md                 # annotated source format + authoritative tiers
```

## Skill: `security-writing-language` (central, discipline)

MUST-follow standard, referenced by the other four via `**REQUIRED SUB-SKILL:**`.
Discipline skill: includes a rationalization table and red-flags list so it
resists pressure.

Contents:
- **Word-substitution table** (~18 pairs): `attacker`→`external party`/`threat
  actor`; plus `hacker`, `victim`, `breach`, `compromised`, `stolen`/`exfiltrated`
  (unconfirmed), `malicious`, `negligent`/`careless`, `obviously`/`clearly`,
  hyperbole (`catastrophic`, `devastating`), `backdoor`, `guilty`/`culprit`, etc.
  Legal terms of art (`breach`, `negligent`, `stolen`) flagged as
  "escalate to counsel / use neutral synonym."
- **Absolutes blocklist**: "unhackable", "100% secure", "fully eliminated",
  "guaranteed", "impossible".
- **Fact vs. assessment**: observed (sourced, past tense, declarative) vs.
  assessed (hedged, confidence-qualified). The single load-bearing distinction.
- **Two separate axes** (detail in `estimative-language.md`): likelihood (WEP:
  likely/probable/almost certain, per ICD 203) ≠ confidence (low/moderate/high).
  Never collapse them.
- **Attribution caution**: default "unattributed"; describe TTPs not identity;
  confidence-qualify any attribution.
- **Blameless tone**: blame systems/process, not people; roles not names;
  forward-looking not punitive.

## Skill: `verifying-security-language` (verifier)

Verb-first process skill. Independently invocable ("make this clinical", "check
this draft for loaded language") and used as the final step of the three
document skills. Carries `REQUIRED SUB-SKILL: security-writing-language` and
reuses its word table as the single source of truth.

- **`verify-language.py`** — regex linter. Scans a draft; emits each hit with
  line, matched term, category (loaded-term / absolute / hyperbole / legal-term /
  second-person-blame), and the preferred replacement. Mechanical detection only.
- **Re-framing procedure** (skill judgment): run script → triage hits → reframe
  loaded terms; demote unsourced claims to assessments with confidence; strip
  absolutes/hyperbole; de-personalize blame → re-run script to confirm clean.

## Skill: `writing-security-findings`

Spine (each field forces specificity to counter the top pitfalls):
Title (names the vulnerability, not the symptom) → Severity (justified, with CVSS
vector or OWASP factors — not a bare label) → Affected assets (precise) →
Description (root cause/mechanism) → Impact (business + technical "so what") →
Evidence/PoC (reproducible, redacted, non-destructive) → Remediation (actionable,
specific, root-cause-oriented) → References (CWE, OWASP, CVE).
`severity-rating.md` carries CVSS v3.1/v4.0 bands, OWASP Risk Rating, and how to
justify a rating. Final step: run `verifying-security-language`.

## Skill: `writing-incident-reports`

NIST SP 800-61 / SANS PICERL structure: metadata + TLP → executive summary →
incident overview/classification → timeline (UTC, ISO 8601, evidence-anchored) →
technical detail / root cause → impact & scope (confirmed compromised vs.
potentially exposed; data *accessed* vs. *exfiltrated*) → IOCs (defanged, typed
table) → MITRE ATT&CK mapping (evidence-based) → response actions (PICERL) →
blameless lessons learned with owner + due date. `analysis-reference.md` carries
timeline columns, IOC table format/defanging, ATT&CK mapping format. Final step:
run `verifying-security-language`.

## Skill: `writing-executive-summaries`

BLUF-first, descending priority, ~1 page, no FUD: BLUF (situation + impact + ask
in ≤3 sentences) → context → key points → business/quantified risk →
prioritized recommendations (owner, cost, timeline) → annotated references.
`references-guide.md` carries authoritative source tiers (NIST/CISA/MITRE/vendor)
and the annotated-reference format (issuer + identifier + date + one-line "what
it establishes"). Final step: run `verifying-security-language`.

## Testing approach

Per the writing-skills Iron Law (no skill without a failing test first):
- `security-writing-language` and `verifying-security-language` are discipline
  skills — get baseline tests: a fresh agent writes "attacker"/absolutes without
  the skill; confirm the skill + verifier flip that. Capture rationalizations
  into the rationalization table.
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
(`**REQUIRED SUB-SKILL:** security-writing-language`), never `@`-links (which
force-load and burn context). Note plugin namespacing may surface skills as
`security-skills:<skill-name>`.
