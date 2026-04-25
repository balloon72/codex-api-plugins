---
name: gh-address-comments
description: Address actionable GitHub pull request review feedback. Use when the user wants to inspect unresolved review threads, requested changes, or inline review comments on a PR, then implement selected fixes. Use the bundled GraphQL script via `gh` whenever thread-level state, resolution status, or inline review context matters.
---

# GitHub PR Comment Handler

Use this skill when the user wants to work through requested changes on a GitHub pull request. Treat thread-aware review data as a `gh api graphql` problem because GitHub review state, resolution status, and line anchors need GraphQL or `gh`-backed reads.

## Preflight

Run these checks before any PR review work:

- Set `$env:GODEBUG='http2client=0'` for the current PowerShell session before running `gh`.
- `gh --version`
- `gh auth status`

If `gh` is missing on Windows, stop and tell the user to run:

- `winget install --id GitHub.cli`

If `gh` is installed but unauthenticated, stop and tell the user to run:

- `gh auth login`

## Workflow

1. Resolve the PR.
   - If the user provides a repository and PR number or URL, use that directly.
   - If the request is about the current branch PR, use local git context plus `gh pr view --json number,url` to resolve it.
2. Inspect review context with thread-aware reads.
   - Use `gh pr view --json title,body,author,files,headRefName,baseRefName,url` and `gh pr diff` for PR metadata and patch context.
   - Use the bundled `scripts/fetch_comments.py` workflow whenever the task depends on unresolved review threads, inline review locations, or resolution state. That script first tries GraphQL for `reviewThreads`, `isResolved`, `isOutdated`, and file and line anchors.
   - If GraphQL still fails on this machine, the script falls back to REST review comments. In that fallback mode, inline comments are still available, but thread resolution state and true thread grouping are not.
   - Use lightweight `gh pr view --comments` or `gh api` only for top-level PR comment summaries.
3. Cluster actionable review threads.
   - Group comments by file or behavior area.
   - Separate actionable change requests from informational comments, approvals, already-resolved threads, and duplicates.
4. Confirm scope before editing.
   - Present numbered actionable threads with a one-line summary of the required change.
   - If the user did not ask to fix everything, ask which threads to address.
   - If the user asks to fix everything, interpret that as all unresolved actionable threads and call out anything ambiguous.
5. Implement the selected fixes locally.
   - Keep each code change traceable back to the thread or feedback cluster it addresses.
   - If a comment calls for explanation rather than code, draft the response rather than forcing a code change.
6. Summarize the result.
   - List which threads were addressed, which were intentionally left open, and what tests or checks support the change.

## Write Safety

- Do not reply on GitHub, resolve review threads, or submit a review unless the user explicitly asks for that write action.
- If review comments conflict with each other or would cause a behavioral regression, surface the tradeoff before making changes.
- If a comment is ambiguous, ask for clarification or draft a proposed response instead of guessing.
- Do not treat top-level PR comments as a complete representation of review-thread state.
- If `gh` hits auth or rate-limit issues mid-run, ask the user to re-authenticate and retry.

## Fallback

If `gh` cannot resolve the PR cleanly, tell the user whether the blocker is missing repository scope, missing PR context, missing `gh`, CLI authentication, or a GraphQL transport failure. If the blocker is GraphQL transport, continue with REST comments and explicitly note that thread resolution state is unavailable.
