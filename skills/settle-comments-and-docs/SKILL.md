---
name: settle-comments-and-docs
description: (hgto/security-skills) Use when asked to clean up comments and documentation on a branch or PR's changed files — dispatching parallel subagents to apply a keep/cut comment rubric so comments and docs are coherent with the code, concise, and pitched at the right level of detail, without touching logic. Trigger on "tidy the comments on this branch", "clean up the docs before merge", "make the comments coherent with the code", or as the second stage of settle.
---

## 1. Overview

Comments and docs drift from the code they describe, especially after a burst of changes. This skill dispatches one subagent per changed file (or small batch) to bring comments and docs in line with the current code — coherent, concise, and valuable to the next reader, human or agent. It never touches executable code.

**Autonomy boundary:** this skill commits its own changes to the current branch (never `main`) and never pushes or merges.

## 2. Files in This Skill

| File | Purpose |
|---|---|
| `comment-rubric.md` | Keep/cut rubric — load the full contents into each subagent's prompt |

## 3. Identify the Changed Files

Confirm the current branch is not `main`/`master`. Compute the changed-file set fresh, even if a prior stage (like `settle-security`) already ran: `git diff <merge-base>...HEAD --name-only`. Filter out generated files, lockfiles, fixtures, and binary/data files — this pass only touches source and doc files.

## 4. Dispatch Subagents

Use OpenCode's Task tool to spawn one general-purpose subagent per file or small batch. Launch independent tasks in parallel, and give each subagent:

- The file(s) to work on, plus the surrounding diff for context — they're revising comments to fit the *current* code, not the pre-change version.
- The full contents of `comment-rubric.md`.
- An explicit instruction: **touch only comments, docstrings, and doc prose — never executable code, imports, or signatures.** If a comment is wrong because the code changed, fix the comment, not the code.

Have each subagent return a short summary of what it changed and why.

## 5. Verify and Commit

Run `git diff` yourself and confirm no non-comment lines changed — a comment-only diff touches whitespace and `#` / `//` / `/* */` / docstring lines, never logic. If a subagent drifted into a real code change, revert that hunk and re-run it with a tighter instruction. Once clean, commit with a message like "Tidy comments and docs" on the current branch.

## 6. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Logic sneaks into a "comment" pass | A subagent renames a variable or changes a condition while "clarifying" it | Diff-check after every run; revert and re-run any hunk touching real code |
| Comment references the session | New comment reads "// fixed per settle run" | Apply `comment-rubric.md` — state the durable reason, never the task/session that touched it |
| Scope creep | Rewriting comments repo-wide instead of on the changed files | Recompute the changed-file set from the diff each time; stay inside it |
| Skipping doc files | Only touching source comments, leaving a stale README paragraph next to it | The changed-file set includes docs that reference the changed code, not just source |
