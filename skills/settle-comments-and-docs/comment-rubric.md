# Comment & Doc Rubric

Used by the subagents dispatched in `settle-comments-and-docs`. Apply this file-by-file — never to executable logic.

## Keep or write a comment only when the WHY is non-obvious

A comment earns its place when the code alone can't convey it:

- A hidden constraint or invariant the code depends on but doesn't express (ordering requirements, units, a value range assumed elsewhere).
- A workaround for a specific external bug or limitation — name the thing being worked around.
- Behavior that looks wrong at a glance but is intentional, with the reason stated.
- A non-obvious tradeoff: why this approach over the seemingly simpler one.

If a comment doesn't do one of these, cut it or fold its content into a clearer identifier name.

## Cut or rewrite

| Pattern | Example | Why it's wrong |
|---|---|---|
| Restates the code | `// increment counter` above `counter++` | Adds no information the code doesn't already give |
| References the current task/session | `// added this for the auth fix`, `// per PR #123`, `// updated per review comment` | Meaningless once the PR merges; the code has no memory of why *this* session touched it |
| Names a caller instead of a constraint | `// used by the checkout flow` | Callers change; if the constraint matters, state the constraint instead |
| Changelog-in-comment | `// changed from X to Y on 2026-01-01` | Git history already owns this |
| TODO with no owner or ticket | `// TODO: fix later` | Not actionable; either file it and reference the tracker, or remove it |
| Commented-out code | `// old_function()` | Dead weight; git history preserves it if ever needed |
| Multi-paragraph docstring for a simple function | Restating every parameter the signature already makes clear | Buries the one sentence that matters under boilerplate |

## Docs (README, reference files, architecture notes)

- Every claim must match current code — remove statements that describe how something *used to* work or *will eventually* work.
- Prefer one concise, accurate paragraph over three hedged ones.
- Match the existing doc's altitude: a README section that lists capabilities shouldn't suddenly drop into function-level detail, and vice versa.
- If a doc references a file, flag, or function that no longer exists, fix or remove the reference — don't leave it dangling.

## Wrong → Right

| Wrong | Right | Why |
|---|---|---|
| `// retry logic added for the flaky API fix` | `// retries: this endpoint drops ~1% of requests under load (see incident-2026-03)` | States the durable reason, not the session that added it |
| `// used by settle skill` above a shared util | *(no comment, or state the invariant the util enforces)* | Callers are not a fact worth freezing into the code |
| `/** * Fetches the user. * @param id the user id * @returns the user */` above `function getUser(id)` | *(no comment — the signature already says this)* | Docstring adds zero information over the type signature |
| `// TODO: handle edge case` | Remove, or `// TODO(SEC-482): null org_id not yet handled — see ticket` | Actionable only with an owner/reference |
