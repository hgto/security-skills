---
name: settle-security
description: (hgto/security-skills) Use when asked to run an offline code and security review loop on a branch or PR until it is resolved — repeatedly running code-review and security-review against the branch, applying fixes, and re-reviewing until no actionable findings remain and the agent is satisfied with the branch's correctness and security posture, without posting anything to GitHub. Trigger on "run security review on this branch", "loop the security review until it's clean", "resolve the security findings on this PR before I merge", or as the first stage of settle.
---

## 1. Overview

An autonomous, offline remediation loop, not a one-shot scan: review → assess → apply → re-review, repeating until neither `code-review` nor `security-review` has actionable findings and the agent is satisfied with the branch's correctness and security posture.

**Autonomy boundary:** apply safe, scoped fixes without waiting for approval. Ask the human only when a finding requires a material product tradeoff, the safe implementation is ambiguous, or accepting the risk is the only practical resolution. This skill commits fixes to the current branch (never `main`) and never merges or pushes.

## 2. Identify the Branch and Base

Confirm the current branch is not `main`/`master` — if it is, stop and ask the user to check out or create a feature branch first. Determine the base to diff against (usually `main`): `git merge-base HEAD main`.

## 3. The Loop

Repeat until the agent is satisfied:

1. **Review.** Use OpenCode's Skill tool to load and execute `code-review` against the pending changes — never with `--comment`, so nothing is posted to GitHub. Then load and execute `security-review` against the same HEAD. Preserve both reviews' structured findings and the scanned SHA; later stages need them.
2. **Assess and resolve.** Evaluate every finding and apply the recommended fix or a safer, more appropriate alternative. Use a subagent for a larger fix when useful. Ask the human only for a material tradeoff, unsafe ambiguity, or explicit risk acceptance. Route finding language through the `security-language` and `write-security-finding` skills when a formal write-up is useful; do not invent new severity or wording conventions here.
3. **Commit.** If fixes changed the branch, commit them with a message describing the fix, not the review process.
4. **Re-review.** After committing fixes, load and execute `code-review` and `security-review` again against the new HEAD and return to step 2. If no fixes were needed, evaluate the exit condition below instead of repeating an identical review.

Exit when the latest round of both reviews has no actionable findings and the agent is satisfied that they covered the changed code and attack surface. Do not stop merely because one pass is empty if coverage is incomplete or a prior finding remains unresolved. If the loop is blocked on a human decision, ask rather than claiming completion. Keep every round's findings and scanned SHA. Return each review's last-round result, resolved findings, accepted items and reasons, and the scanned SHA to `settle-draft-pr`, which records them at the bottom of the PR description.

**Do not post a PR comment, submit a review, or otherwise publish the result to a GitHub conversation.** This stage runs entirely offline: it only reports to the human and passes structured results to `settle-draft-pr`.

## 4. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Silently dismissing a finding | Skipping a finding because it "looks minor" | Resolve every actionable finding; ask the human if resolution requires accepting risk |
| Treating an empty finding list as sufficient | Ending the loop after an empty pass despite incomplete coverage or unresolved earlier findings | Check review coverage and prior findings, then exit only when the agent is satisfied |
| Losing track of the scanned SHA | Reporting findings without recording which commit was reviewed | Capture `git rev-parse HEAD` at every review; the final one feeds `settle-draft-pr` |
| Fixing without committing | Applying a fix but leaving it uncommitted before re-reviewing | Commit each fix before the next review, so the review reflects the branch's real state |
| Posting to the PR | Adding findings as an issue comment or review, or running `code-review --comment` | Return the result to `settle-draft-pr`; it belongs at the bottom of the PR description |
