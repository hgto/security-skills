---
name: security-review-pr
description: (hgto/security-skills) Use when asked to run a security review against one or more live GitHub pull requests — in one repo or several related repos at once — and publish the findings back as an inline-commented GitHub review, not just a report. Trigger on "security review this PR", "review these PRs for security issues and post it", "do a security pass on this pull request and leave comments", or "/security-review-pr <PR URL> [<PR URL> ...]".
---

## 1. Purpose and Boundary

This is not `security-review`. That skill reviews the *current local branch's* diff and is explicitly forbidden from posting anywhere — it returns a report to the caller only. This skill does the opposite: it takes one or more **live PR URLs**, which may span **multiple repositories** when they're stacked or companion PRs implementing one feature, and its entire purpose is to **publish** the findings as a real GitHub review — inline comments plus a submitted summary.

Because publishing is the point, treat this with the same care as any other action visible to others (see §8 before submitting anything). **Hard boundary, no exceptions: every review this skill submits is either `COMMENT` or `REQUEST_CHANGES`. It never submits `APPROVE`, regardless of how clean a PR looks or how confident the analysis is.** Formal approval is a decision for a human reviewer to make, not this skill — its job ends at surfacing findings clearly enough for that human to decide quickly. This applies identically to every domain-specific subagent forked under §6; carry the rule forward explicitly into that subagent's instructions rather than assuming it infers it.

## 2. Gather Inputs

Parse the PR reference(s) out of the invocation — full URLs, or `owner/repo#123` shorthand. If the user names a feature or ticket instead of explicit PRs, ask for the PR list rather than guessing which ones are in scope.

If invoked with no explicit PR and the current directory is inside a repo whose checked-out branch has an open PR, use that PR — confirm which one (`gh pr view --json url,number,title`) before proceeding rather than assuming silently.

## 3. Fetch Each PR's Full Context

For every PR in scope, get more than the diff:

1. **Metadata** — title, body, base/head SHA (`gh pr view <n> --repo <owner/repo> --json ...`, or the GitHub MCP `pull_request_read` `get` method). Read the description: authors often state their own known tradeoffs, deferred work, and ticket references there — that's legitimate context for judging severity, not proof of safety.
2. **The full diff** — `gh pr diff <n> --repo <owner/repo>`, or `pull_request_read` `get_diff`.
3. **Full file content at the head SHA when you need it** — diff hunks alone are not enough to get inline-comment line numbers right, and they don't show helper functions, callers, or tests that determine whether something is actually reachable. Pull full files via `gh api -H "Accept: application/vnd.github.raw" repos/<owner>/<repo>/contents/<path>?ref=<head-sha>`, or `get_file_contents`.

Prefer a local clone when one already exists on disk — `git fetch origin pull/<n>/head:<tmp-branch>` into it, then use plain `grep -n`/`git show <sha>:<path>` for exact line numbers; this is faster and cheaper than repeated API calls. Otherwise work directly against the API/`gh` with no local checkout required. Either way, delete any temporary local branches/refs you created once done (`git branch -D <tmp-branch>`) — leave the workspace as you found it.

## 4. Analyze for Concrete Vulnerabilities

Use `security-review`'s vulnerability-class priorities and noise exclusions as your triage checklist — load that skill's §3–4 rather than re-deriving the list. In short: prioritize injection/unsafe execution, authn/authz bypasses, crypto/secret handling, data exposure, and trust-boundary failures where an untrusted party controls the host or destination, not just a path segment; skip DoS/rate-limiting, dependency-version findings, theoretical races, and hardening-without-demonstrated-impact.

When reviewing more than one PR together, treat them as **one combined change set for reachability purposes**. A default or config value in one repo and an enforcement gap in another can combine into a single exploitable finding that neither PR shows in isolation — this is common in stacked/cross-repo features (e.g., an app-side default that only becomes dangerous because a service-side validator is missing a boundary check). When that happens:

- Post the finding on the PR that owns the root-cause code, with the full technical explanation.
- Cross-link it (by `owner/repo#N`) from every other PR whose code contributes to or is affected by it — a short pointer, not a duplicate essay.

## 5. Independently Validate Before Posting

Any finding you intend to tag **[BLOCKING]** gets a skeptical second pass before it goes out — spawn a subagent via OpenCode's Task tool, or deliberately re-argue against your own finding, asking: does this actually reach an untrusted boundary under realistic conditions, and is there an upstream/downstream mitigation not yet accounted for? Since this skill publishes rather than just reports, a wrong blocking claim costs the author's time and your credibility — that discipline isn't optional here the way it might feel for a private note.

## 6. Optional: Fork a Domain-Specific Subagent

When the changeset includes a specialized area that deserves its own narrowly-scoped pass — Kubernetes/infra manifests, IAM policy, cryptographic key management, a particular framework's auth model — consider forking one subagent per domain via OpenCode's Task tool instead of trying to cover everything in one general sweep. Give it:

- Exactly what the general pass already covered, so it doesn't restate those findings.
- The exact PR(s) and files in its scope.
- The classification rules (§7) and posting mechanics (§8) below, since it posts its **own** separate pending review rather than merging its findings into the main one.
- An explicit, standalone instruction that it must submit `COMMENT` or `REQUEST_CHANGES` only, never `APPROVE` — don't rely on it picking this up implicitly from "posting mechanics," state it directly in the subagent's own prompt.

## 7. Classify Every Finding

Tag every inline comment and every line of the summary with exactly one of:

- **[BLOCKING]** — concrete, reachable, would justify Request Changes on its own.
- **[NIT]** — worth raising, not worth blocking on.
- **[CAN BE FIXED LATER]** — real but deferrable. Say explicitly whether it's already tracked (cite the ticket/issue) or newly identified.

This is a lightweight triage vocabulary for fast PR review — it is **not** the formal CVSS/OWASP severity scheme from `write-security-finding`/`severity-rating.md`. Don't conflate the two: these tags describe what should happen to the PR, not a portable vulnerability rating. If a finding is severe enough to warrant a full CVSS-rated write-up beyond the PR conversation, say so and hand off to `write-security-finding` rather than trying to cram that rigor into a review comment.

## 8. Post the Review

For each PR carrying findings:

1. Create a pending review (`pull_request_review_write` method `create`, or `gh pr review <n> --repo <owner/repo>` mechanics if MCP tools aren't available).
2. Add each finding as an inline comment at the exact file and line, using line numbers from the head-SHA file content (§3), not raw diff-hunk positions.
3. Submit the review. The summary body **must**:
   - Start with the exact text `Hey, this is Thomas's agent with automated review feedback! This review is not an approval, and may not be comprehensive. Thomas will post personally separately.`
   - Name the other PRs in this review set (`owner/repo#N`), if any, so a reader on one PR knows to check the others.
   - Open with one or two sentences of genuine, specific observation about what's done well — a review that's only complaints reads as adversarial, not useful. Keep the tone factual, not effusive.
   - List findings grouped by tag (blocking, then nits, then can-fix-later) as short pointers to the inline comments, not restatements of their full text.
4. Choose the review event: **REQUEST_CHANGES** if any finding is [BLOCKING], otherwise **COMMENT**. These are the only two valid choices — see the hard boundary in §1.

**Confirm before submitting** unless the invocation already explicitly asked for the review to be posted (e.g., "review this PR and leave comments" makes intent explicit — proceed). If it's ambiguous whether the user wants a published review or just a report back, draft the findings and ask before calling the submit step, the same boundary `settle-draft-pr` draws around its one push.

## 9. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Using diff-hunk line numbers | Inline comment lands on the wrong line because it used the hunk's relative offset | Fetch the real file at the head SHA and get the actual line number |
| Reviewing each PR in total isolation | Missing a vulnerability that only exists because two PRs' changes combine | Treat a stacked/companion PR set as one change set for reachability; cross-link root-cause findings |
| Posting a false [BLOCKING] | Skipping the adversarial second pass because a finding "looks obviously bad" | Every blocking claim gets challenged before it's published — no exceptions |
| Selecting APPROVE | Marking a genuinely clean-looking PR as approved, including from a §6 domain subagent that wasn't told the rule explicitly | Only COMMENT or REQUEST_CHANGES are valid — state this directly in every subagent's prompt, don't assume it's inferred |
| Publishing without checking intent | Submitting a review the user only wanted as a private report | Confirm before the submit step unless the invocation already asked to post |
| Leaving temp refs behind | Local `pr-<n>` branches from a fetched-for-review PR still sitting in a shared clone afterward | Delete every temporary branch/ref you created once the review is posted |
