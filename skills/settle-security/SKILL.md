---
name: settle-security
description: (hgto/security-skills) Use when asked to run a security review loop on a branch or PR until it is resolved — repeatedly reviewing the branch, presenting findings for a fix/alternative/waive decision, applying the chosen fix, and re-reviewing until the human explicitly signs off. Trigger on "run security review on this branch", "loop the security review until it's clean", "resolve the security findings on this PR before I merge", or as the first stage of settle.
---

## 1. Overview

A human-in-the-loop remediation loop, not a one-shot scan: review → present findings → human decides → apply → re-review, repeating until the human — never the skill itself — says the branch's security posture is acceptable.

**Autonomy boundary:** every fix decision belongs to the human. This skill commits accepted fixes to the current branch (never `main`) and never merges or pushes.

## 2. Identify the Branch and Base

Confirm the current branch is not `main`/`master` — if it is, stop and ask the user to check out or create a feature branch first. Determine the base to diff against (usually `main`): `git merge-base HEAD main`.

## 3. The Loop

Repeat until the human ends it:

1. **Review.** Use OpenCode's Skill tool to load and execute `security-review` against the pending changes. Preserve its structured findings and scanned SHA; later stages need both.
2. **Present and ask.** Show the findings to the human. If any exist, use OpenCode's Question tool (or plain conversation for a large finding set) to ask whether to apply the recommended fix, take an alternative approach the human specifies, or accept/waive the risk with a stated reason. Route finding language through the `security-language` and `write-security-finding` skills when a formal write-up is useful; do not invent new severity or wording conventions here.
3. **Resolve.** Apply whatever the human chose (directly, or via a subagent for a larger fix). Commit the result to the branch with a message describing the fix, not the review process.
4. **Re-review.** Load and execute `security-review` again against the new HEAD and return to step 2.

Exit only on explicit human sign-off. "No findings this round" is one valid exit condition; "the remaining items are accepted risks" is another — but the human must say so, not the skill inferring it from an empty finding list without asking. Keep every round's findings and scanned SHA. Return the last round's result, resolved findings, accepted items and reasons, and scanned SHA to `settle-draft-pr`, which records them at the bottom of the PR description.

**Do not post a PR comment, submit a review, or otherwise publish the result to a GitHub conversation.** This stage only reports to the human and passes structured results to `settle-draft-pr`.

## 4. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Skill decides a finding is fine | Skipping the human prompt because a finding "looks minor" | Every finding goes through the human; only they close the loop |
| Treating an empty finding list as automatic sign-off | Ending the loop the moment the review returns nothing, without confirming with the human | Still ask — the human may want a second pass, or may want to note accepted risk from an earlier round |
| Losing track of the scanned SHA | Reporting findings without recording which commit was reviewed | Capture `git rev-parse HEAD` at every review; the final one feeds `settle-draft-pr` |
| Fixing without committing | Applying a fix but leaving it uncommitted before re-reviewing | Commit each accepted fix before the next review, so the review reflects the branch's real state |
| Posting to the PR | Adding findings as an issue comment or review | Return the result to `settle-draft-pr`; it belongs at the bottom of the PR description |
