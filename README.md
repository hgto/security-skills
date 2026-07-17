# security-skills

An OpenCode skill collection for writing security findings, incident reports, and executive summaries in neutral, defensible language. These tools help security teams communicate vulnerabilities, incidents, and risk assessments with clarity and precision.

## Skills

- **security-language** — The central word-choice and estimative-language standard. Governs every other skill in this collection: word substitution table, likelihood/confidence scales (ICD 203), no-legal-opinion rule, and blameless tone. Load this first whenever you are writing or editing any security document.
- **verify-security-language** — Runs the `verify-language.py` regex linter against a draft, triages every flagged term, and applies the clinical re-framing procedure from `security-language`. The mandatory final step before delivering any document produced by the three writing skills.
- **write-security-finding** — Produces a single, structured security finding (title, CVSS/OWASP severity with full vector, evidence with numbered repro steps, two-tier remediation). Use for penetration-test results, code-review issues, audit observations, and scanner findings that require a defensible write-up.
- **write-security-incident-report** — Structures a security incident report following NIST SP 800-61 phases and the SANS PICERL framework: ISO 8601 UTC timeline, fact-vs-assessment separation, IOC table with defanged network indicators, MITRE ATT&CK mapping, and blameless lessons learned.
- **write-security-executive-summary** — Produces a BLUF-first, one-page leadership briefing that translates technical findings into business consequences with quantified risk, sourced claims (annotated references with issuer/identifier/date), and specific recommendations with owners and deadlines.
- **security-review** — Reviews the current branch diff for concrete High and Medium security vulnerabilities, then independently validates each candidate and discards findings below 8/10 confidence.
- **settle** — Orchestrates the three skills below, in order, to take a branch from finished changes to an open draft PR. Workflow skills rather than report-writing ones; they don't use `security-language` directly (though `settle-security` routes finding language through it).
- **settle-security** — Loops focused security reviews against human-approved fixes — review, human decides fix/alternative/waive, apply, re-review — until the human signs off.
- **settle-comments-and-docs** — Dispatches parallel subagents to tidy comments and docs on the branch's changed files against a keep/cut rubric, without touching logic.
- **settle-draft-pr** — Opens the draft PR (using the repo's template or a What/Why/How body), appends the final security review and scanned commit SHA to the PR description, and sends the human a personal Slack DM in `pr-review-request` format.

### How they work together

The three writing skills (`write-security-finding`, `write-security-incident-report`, `write-security-executive-summary`) each require `security-language` as a sub-skill. Load it first with OpenCode's Skill tool to apply the word-choice and estimative-language rules. Each writing skill ends the same way: load `verify-security-language`, check the completed draft, and confirm the linter exits clean before delivering. `security-language` defines the standard; `verify-security-language` enforces it.

### Example invocations

> Load the security-language skill before drafting this incident report.

Loads the word-choice and estimative-language rules before beginning a security document.

> Check this draft with verify-security-language.

Check an existing draft for loaded language and apply clinical re-framing; re-run until exit 0.

> Write a security finding from these review notes.

Produce a structured finding from a pentest result, code-review issue, or scanner output.

> Turn these investigation notes into a security incident report.

Build a NIST/PICERL incident report from investigation notes, log exports, or a debrief.

> Write an executive security summary from this report.

Translate a technical report or incident into a BLUF-first, one-page leadership briefing.

> Settle this branch.

Run the full pipeline on the current branch: security review to resolution, comment/doc cleanup, then a draft PR with a Slack DM.

> Run a security review of this branch.

Review the pending branch changes for concrete vulnerabilities and independently filter false positives.

> Run the settle-security review loop on this branch.

Loop the security review against human-approved fixes until the branch is clean or accepted risks are explicit.

> Tidy the comments and docs on this branch.

Tidy comments and docs on the branch's changed files without touching logic.

> Open the settled branch as a draft PR.

Open the draft PR, append the final security review with the scanned commit SHA to its description, and DM the human on Slack.

### Note on linter scope

The linter (`verify-language.py`) is intended for the content of security reports and findings — not for skill metadata or documentation. Skill `description` fields and this README intentionally use trigger keywords like "vulnerability" so users can discover the skills, and are not themselves linted.

## Install

Clone the repository, then add its `skills` directory to your OpenCode configuration (`~/.config/opencode/opencode.json` for global use):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/absolute/path/to/security-skills/skills"]
  }
}
```

Quit and restart OpenCode after changing the configuration. The repository's own `opencode.json` loads the skills automatically when OpenCode is started from this checkout. The existing `.claude-plugin` manifest remains available for Claude Code users.
