---
name: settle-draft-pr
description: (hgto/security-skills) Use when asked to open a draft pull request for a finished branch and notify the human — filling the repo's PR template (or a What/Why/How body), appending the final security-review result and exact scanned commit SHA to the PR description, then sending the human a personal Slack DM in pr-review-request format. Trigger on "open a draft PR for this", "finish this PR and let me know on Slack", "record the security review in the PR description", or as the final stage of settle.
---

**RELATED SKILL:** `pr-review-request` (if installed) — this skill's closing Slack message follows the same formatting convention, adapted for a DM to the human instead of a channel post. See §5.

## 1. Overview

The last stage of the settle pipeline: open the draft PR, record the security result at the bottom of its description, and let the human know on Slack — without merging anything.

**Autonomy boundary:** this is the one stage in the pipeline that pushes. Get the human's explicit go-ahead before pushing — commit and push are separate approvals even when the human already approved the branch's contents in earlier stages. This skill never merges.

## 2. Preconditions

Confirm the current branch is not `main`/`master`. This skill assumes `settle-security` and `settle-comments-and-docs` (or equivalent manual work) already ran — it needs their output:
- The **last round's security findings and the commit SHA scanned**, from `settle-security`.
- A clean working tree with all fixes and cleanup already committed.

If that context is not available (this skill is being run standalone), reconstruct it by using OpenCode's Task tool to run one focused security review against the current HEAD.

## 3. Open the Draft PR

1. **Find a template.** Check `.github/pull_request_template.md` and `.github/PULL_REQUEST_TEMPLATE/*.md`. If one exists, fill it in.
2. **Otherwise, write the body in three sections:** **What** (the change, plainly), **Why** (the problem or need driving it), **How** (the approach, and anything a reviewer should look at first).
3. **Append the security result.** Add the section from §4 after all template or generated content so it is the final section of the PR description.
4. **Confirm the push.** Ask the user explicitly before pushing — this is the pipeline's one push, and it is what makes the PR visible to others.
5. **Open the PR as a draft** (`gh pr create --draft ...`, or the GitHub MCP `create_pull_request` with `draft: true`). If a PR already exists, update its body while preserving all content above the security section.

## 4. Record the Final Security Review

Append an idempotent final section to the PR description using this shape:

```markdown
## Security review

- Scanned commit: `<full SHA>`
- Result: No findings | Findings resolved | Accepted risk remains

<concise list of fixed findings and accepted/waived items, including the human's stated reason for each waiver>
```

Use one `## Security review` section. Replace an existing section rather than appending a duplicate. Preserve the rest of the PR description exactly.

The scanned SHA must equal the PR branch's current `HEAD`. Because `settle-comments-and-docs` normally commits after `settle-security`, run a fresh focused security review here whenever the recorded SHA differs from `HEAD`. Update the section with that result before creating or updating the PR.

**Never post the security result as a PR comment or review.** Use the PR body through `gh pr create --body-file` / `gh pr edit --body-file`, or the GitHub MCP create/update pull-request tools. Do not use issue-comment or review-comment tools for this result.

## 5. Send the Slack DM

Notify the human directly rather than posting to a team channel — this is a personal heads-up that their PR is ready, not a review request to others.

1. Look up the current user's own Slack ID (e.g., a profile-lookup call with no user specified returns the caller's own identity) — don't hardcode a user ID.
2. Get the PR URL and title (`gh pr view --json number,title,url`, or from the create-PR response).
3. Format the message the same way `pr-review-request` formats a channel post — a bare Slack hyperlink to the PR, no added commentary: `<PR_URL|PR_title>`. Since this is a self-DM rather than a review request to a teammate, there are no reviewer mentions to append.
4. Send it as a direct message to the human's own Slack ID.

## 6. Common Mistakes

| Mistake | What it looks like | Correct approach |
|---|---|---|
| Push without sign-off | Pushing and opening the PR without asking first | Confirm the push explicitly — it's a separate approval from everything already committed |
| Merging | Merging the PR once it's open | Out of scope — this skill stops at a draft PR |
| Recording a stale review | Recording round-3 findings when a later commit already landed | Re-scan whenever the recorded SHA differs from `HEAD` |
| Missing the scanned SHA | Recording findings without saying which commit they apply to | Always name the exact SHA in the PR description's security section |
| Posting a PR comment | Publishing the security result in the conversation timeline | Append or replace the security section at the bottom of the PR description |
| Posting to a channel instead of DMing | Sending the heads-up to `#eng-pr-review` like a review request | This is a personal notification to the author, not a review request — send it as a DM |
| Cluttering the DM | Adding a paragraph of context around the PR link | Follow `pr-review-request`'s own rule: the link (and title) is the whole message |
