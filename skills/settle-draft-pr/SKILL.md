---
name: settle-draft-pr
description: (hgto/security-skills) Use when asked to open a draft pull request for a finished branch — writing a very short description that reports the final code-review and security-review results with the exact scanned commit SHA, then returning a Markdown link to the PR. Trigger on "open a draft PR for this", "record the review results in the PR description", or as the final stage of settle.
---

## 1. Overview

The last stage of the settle pipeline: open the draft PR with a short, sweet description that reports the review results, and hand the human a Markdown link to it — without merging anything.

**Autonomy boundary:** this is the one stage in the pipeline that pushes. Get the human's explicit go-ahead before pushing — commit and push are separate approvals even when the human already approved the branch's contents in earlier stages. This skill never merges and never sends Slack messages or DMs.

## 2. Preconditions

Confirm the current branch is not `main`/`master`. This skill assumes `settle-security` and `settle-comments-and-docs` (or equivalent manual work) already ran — it needs their output:
- The **last round's code-review and security-review findings and the commit SHA scanned**, from `settle-security`.
- A clean working tree with all fixes and cleanup already committed.

If that context is not available (this skill is being run standalone), reconstruct it by using OpenCode's Skill tool to load and execute `security-review` and `code-review` (never with `--comment`) against the current HEAD.

## 3. Open the Draft PR

1. **Write the body.** Use the shape in §4 and nothing more — no template, no What/Why/How essay. The commits already carry the detail.
2. **Confirm the push.** Ask the user explicitly before pushing — this is the pipeline's one push, and it is what makes the PR visible to others.
3. **Open the PR as a draft** (`gh pr create --draft --body-file ...`, or the GitHub MCP `create_pull_request` with `draft: true`). If a PR already exists, replace its `## Review` section and preserve everything else.
4. **Return the link.** Reply with a single Markdown link to the PR — `[PR_title](PR_URL)` — and nothing else.

## 4. PR Description

Keep it to a one-line summary of the change plus this section:

```markdown
<one sentence: what the change does>

## Review

Scanned commit: `<full SHA>`

- Code review: No findings | N fixed | <accepted items, one line each with the human's reason>
- Security review: No findings | N fixed | <accepted items, one line each with the human's reason>
```

Use one `## Review` section. Replace an existing one rather than appending a duplicate.

The scanned SHA must equal the PR branch's current `HEAD`. Because `settle-comments-and-docs` normally commits after `settle-security`, load and execute `security-review` and `code-review` again whenever the recorded SHA differs from `HEAD`. Update the section with that result before creating or updating the PR.

**Never post the security result as a PR comment or review.** Use the PR body through `gh pr create --body-file` / `gh pr edit --body-file`, or the GitHub MCP create/update pull-request tools. Do not use issue-comment or review-comment tools, and never run `code-review --comment`.

## 5. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Push without approval | Pushing and opening the PR without asking first | Confirm the push explicitly — it's a separate approval from everything already committed |
| Merging | Merging the PR once it's open | Out of scope — this skill stops at a draft PR |
| Recording a stale review | Recording round-3 findings when a later commit already landed | Re-scan whenever the recorded SHA differs from `HEAD` |
| Missing the scanned SHA | Recording findings without saying which commit they apply to | Always name the exact SHA in the `## Review` section |
| Posting a PR comment | Publishing review results in the conversation timeline | Put them in the `## Review` section of the PR description |
| Bloated description | Template sections, finding write-ups, or a review-process narrative | One sentence plus the `## Review` section |
| Sending a Slack message | DMing the human the PR link | Return a Markdown link in the reply instead |
