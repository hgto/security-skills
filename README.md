# security-skills

A Claude Code plugin providing skills for writing security findings, incident reports, and executive summaries in neutral, defensible language. These tools help security teams communicate vulnerabilities, incidents, and risk assessments with clarity and precision.

## Skills

- **security-language** — The central word-choice and estimative-language standard. Governs every other skill in this plugin: word substitution table, likelihood/confidence scales (ICD 203), no-legal-opinion rule, and blameless tone. Invoke this first whenever you are writing or editing any security document.
- **verify-security-language** — Runs the `verify-language.py` regex linter against a draft, triages every flagged term, and applies the clinical re-framing procedure from `security-language`. The mandatory final step before delivering any document produced by the three writing skills.
- **write-security-finding** — Produces a single, structured security finding (title, CVSS/OWASP severity with full vector, evidence with numbered repro steps, two-tier remediation). Use for penetration-test results, code-review issues, audit observations, and scanner findings that require a defensible write-up.
- **write-security-incident-report** — Structures a security incident report following NIST SP 800-61 phases and the SANS PICERL framework: ISO 8601 UTC timeline, fact-vs-assessment separation, IOC table with defanged network indicators, MITRE ATT&CK mapping, and blameless lessons learned.
- **write-security-executive-summary** — Produces a BLUF-first, one-page leadership briefing that translates technical findings into business consequences with quantified risk, sourced claims (annotated references with issuer/identifier/date), and specific recommendations with owners and deadlines.

### How they work together

The three writing skills (`write-security-finding`, `write-security-incident-report`, `write-security-executive-summary`) each require `security-language` as a sub-skill — invoke it first to load the word-choice and estimative-language rules. Each writing skill ends the same way: run `verify-security-language` on the completed draft and confirm it exits clean before delivering. `security-language` defines the standard; `verify-security-language` enforces it.

### Example invocations

```
/security-language
```
Load the word-choice and estimative-language rules before beginning any security document.

```
/verify-security-language
```
Check an existing draft for loaded language and apply clinical re-framing; re-run until exit 0.

```
/write-security-finding
```
Produce a structured finding from a pentest result, code-review issue, or scanner output.

```
/write-security-incident-report
```
Build a NIST/PICERL incident report from investigation notes, log exports, or a debrief.

```
/write-security-executive-summary
```
Translate a technical report or incident into a BLUF-first, one-page leadership briefing.

## Install

Install via the `/plugin` marketplace command in Claude Code, or clone this repository into your Claude Code plugins directory.
