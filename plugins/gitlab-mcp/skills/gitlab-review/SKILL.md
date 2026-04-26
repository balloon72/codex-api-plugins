---
name: gitlab-review
description: Review GitLab merge requests, cluster findings, and draft feedback through GitLab MCP with draft notes as the default write mode.
---

# GitLab Merge Request Review

Use this skill when the user wants a GitLab merge request reviewed, wants structured findings, or wants review feedback drafted or published back to GitLab.

## Preflight

Check these prerequisites before merge request review work:

- `GITLAB_PERSONAL_ACCESS_TOKEN` is configured.
- `GITLAB_API_URL` ends in `/api/v4`.
- The token has `api` scope if the request includes writing draft notes, discussions, or publishing feedback.

If the token only has `read_api`, continue with read-only review but explicitly note that feedback cannot be written back to GitLab.

## Default Review Mode

Default to a draft-first workflow:

- read the merge request metadata, diff, discussions, and relevant pipeline state
- analyze the change and cluster findings by severity or behavior area
- draft review notes first
- publish draft notes only when the user explicitly asks

Do not default to public inline discussions. Do not approve, merge, or resolve discussions unless the user explicitly asks.

## Workflow

1. Resolve the merge request.
   - Prefer a full merge request URL.
   - If the user gives a project path and IID, use that directly.
2. Gather review context.
   - Read merge request metadata, diff, and linked discussions.
   - Read pipeline state when the changes could be affected by failing checks or deployment status.
3. Perform the review.
   - Prioritize blocking bugs, regressions, data-loss risks, auth issues, concurrency problems, and missing tests.
   - Separate blocking findings from non-blocking suggestions and open questions.
4. Decide whether the request is read-only or write-back.
   - If the user asked for suggestions only, return the review result in chat.
   - If the user asked to write to GitLab, create draft notes first.
5. Publish only on explicit request.
   - If the user asks to publish the prepared review, publish the draft notes as the final step.

## Write Safety

- Do not create public discussions when a draft note can represent the same feedback.
- If a finding cannot be anchored to a precise file and line, use a top-level draft note instead of fabricating inline context.
- If the merge request diff is outdated or the file position cannot be resolved, tell the user and fall back to a summary note.
- If the user asks for "write suggestions" but the token is read-only, return the drafted wording and explain the permission blocker.

## Output Expectations

When returning review results in chat, use this order:

1. blocking findings
2. non-blocking suggestions
3. open questions
4. what was drafted or published back to GitLab

If no issues are found, state that explicitly and mention any remaining testing or context gaps.
