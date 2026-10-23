---
name: settle
description: (hgto/security-skills) Use when asked to settle, finalize, or wrap up a pull request or branch end-to-end before merge — the full pipeline of an offline code and security review loop to resolution, comment/doc cleanup, and opening a draft PR whose short description reports both reviews' results. Trigger on "settle this PR", "get this branch ready to merge", or "run the full settle pipeline on this branch". If the user only wants one stage, use settle-security, settle-comments-and-docs, or settle-draft-pr directly.
---

## 1. Overview

This skill runs three sub-skills, strictly in order, each of which is also independently invocable:

1. **settle-security** — offline, loops `code-review` and `security-review`, fixing and re-reviewing until neither has actionable findings and the agent is satisfied. Nothing is posted to GitHub.
2. **settle-comments-and-docs** — tidies comments and docs on the changed files without touching logic.
3. **settle-draft-pr** — opens the draft PR with a short description reporting the code-review and security-review results, and returns a Markdown link to it.

The order is load-bearing, not stylistic: security fixes must land before the comment pass touches the same files (otherwise the comment pass reads a diff that's about to change again), and both must land before the PR is opened (a reviewer should see the settled diff, not a work-in-progress one).

## 2. Precondition

Confirm the current branch is not `main`/`master` and has commits ahead of its base. If not, stop and ask the user to check out or create a feature branch first — none of the three stages can proceed without one.

## 3. Procedure

1. Use OpenCode's Skill tool to load and execute **settle-security** to completion. It owns its autonomous review cycle — do not move to the next stage until it reports no actionable findings remain and it is satisfied with the review coverage.
2. Use OpenCode's Skill tool to load and execute **settle-comments-and-docs**.
3. Use OpenCode's Skill tool to load and execute **settle-draft-pr**.

Each stage recomputes the branch's changed-file set for itself when it starts, since the prior stage may have added commits — don't try to precompute or cache this in the orchestrator.

## 4. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Skipping a stage's completion condition | Moving to comment cleanup while security findings are still open, to "save time" | Complete each stage's own exit condition before continuing |
| Running stages out of order | Opening the PR before the comment pass | Follow the fixed order — later stages assume earlier ones already landed |
| Restarting from scratch after an interruption | Re-running settle-security's whole loop despite completed review rounds in a prior session | Check for existing progress (e.g., a security fix-up commit already on the branch) before re-looping |
