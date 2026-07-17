---
name: security-review
description: (hgto/security-skills) Use when asked to review the pending changes on the current git branch for concrete security vulnerabilities, or when another skill needs a high-confidence security pass before a pull request is opened or merged.
---

## 1. Purpose and Boundary

Perform a read-only, security-focused review of changes introduced by the current branch. Report only high-confidence, actionable vulnerabilities with a concrete exploitation path. This is not a general code review and must not edit files, commit, push, post to GitHub, or review pre-existing issues outside the branch diff.

## 2. Establish the Review Scope

1. Confirm the working directory is inside a git repository. If not, stop and tell the user to enter the repository before retrying.
2. Determine the base from the remote default branch (`origin/HEAD`) when available. Otherwise use the repository's configured base or ask the user; do not assume `main` when the target is ambiguous.
3. Collect the status, changed-file list, commit list, complete diff from the merge base through the working tree, and the current `HEAD` SHA.
4. Treat the complete branch diff as the review scope. Read surrounding code, callers, validation, framework behavior, and tests as needed to establish reachability and mitigations.
5. If the working tree is dirty, clearly state that the result covers uncommitted content and cannot be identified solely by the `HEAD` SHA.

## 3. Find Candidate Vulnerabilities

Use OpenCode's Task tool to spawn a general-purpose subagent. Give it the base, changed files, complete diff, and instructions to inspect repository context before assessing the changes.

Prioritize these classes:

- Injection and unsafe execution: SQL, command, template, NoSQL, XML/XXE, path traversal, unsafe deserialization, `eval`, and unsafe DOM APIs.
- Authentication and authorization: bypasses, privilege escalation, insecure session or JWT handling, and missing server-side resource authorization.
- Cryptography and secrets: embedded credentials in source, weak algorithms, predictable security tokens, improper key handling, and certificate-validation bypasses.
- Data exposure: logging or returning secrets or personally identifiable information, cross-tenant disclosure, debug exposure, and unintended public access.
- Trust-boundary failures: untrusted values reaching sensitive operations, externally supplied destinations used for requests or transfers, and unsafe workflow interpolation.

For every candidate, require a precise location, severity, category, attacker-controlled source, sensitive sink or boundary, exploit scenario, existing mitigations considered, recommended fix, and confidence from 1 to 10.

## 4. Noise Exclusions

Do not report:

- Denial of service, rate limiting, resource exhaustion, memory/descriptor leaks, or regex performance.
- Dependency-version findings; dependency scanners own those.
- Documentation-only or test-only issues without a production path.
- Missing hardening, audit logs, or validation without demonstrated security impact.
- Theoretical races or timing attacks without a practical exploit scenario.
- SSRF when an untrusted party controls only a path, not the host or protocol.
- XSS in auto-escaping frameworks unless code uses an unsafe escape hatch such as `dangerouslySetInnerHTML` or equivalent.
- Client-side authorization omissions; authorization must be enforced at a trusted server boundary.
- Environment variables or CLI flags as attacker-controlled inputs unless the repository's threat model establishes that control.
- Log spoofing, regex injection without another security impact, or user content merely appearing in an AI prompt.
- Low-impact browser issues or workflow concerns without a specific, realistic attack path.

Secrets committed directly in source remain in scope. Do not report properly secured secret storage merely because it exists on disk.

## 5. Independently Validate Candidates

For each candidate from the first pass, launch a separate general-purpose Task subagent. Launch independent validations in parallel. Each validator must remain read-only and answer:

1. Do the cited lines contain the described weakness?
2. Can an untrusted party reach the vulnerable path under realistic conditions?
3. Do nearby validation, authorization, framework protections, or deployment constraints prevent exploitation?
4. What exact source-to-sink path and impact remain after considering those mitigations?
5. Should the candidate be kept or discarded, and with what confidence from 1 to 10?

Give each validator the exclusions and relevant repository context. Discard every finding with validator confidence below 8/10. Prefer no findings over speculative noise.

## 6. Report

Return Markdown in this form:

```markdown
# Security review: `<branch>`

- Base: `<base ref and merge-base SHA>`
- Scanned commit: `<full HEAD SHA>`
- Working tree: `clean` or `includes uncommitted changes`
- Candidates: `<N>`
- Confirmed: `<M>`

## Findings

### High | Medium: `<category>` at `<file:line>`

- Confidence: `<N>/10`
- Description: `<specific weakness introduced by this branch>`
- Exploit scenario: `<concrete attacker path and impact>`
- Recommendation: `<specific fix>`
```

If nothing survives validation, write `No confirmed High or Medium security vulnerabilities found.` under `## Findings`. Include only High and Medium findings; Medium findings must be obvious, concrete, and actionable.

The report is returned to the caller only. Never publish it as a GitHub comment or review.
