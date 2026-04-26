---
name: gitlab-pipeline
description: Inspect GitLab merge request pipelines and failed jobs, then summarize likely root causes and next actions.
---

# GitLab Pipeline Inspector

Use this skill when the user wants to inspect a GitLab pipeline, understand why a job failed, or connect merge request changes to pipeline outcomes.

## Preflight

Check these prerequisites before pipeline work:

- `GITLAB_PERSONAL_ACCESS_TOKEN` is configured.
- `GITLAB_API_URL` ends in `/api/v4`.
- The token has at least `read_api` scope. Use `api` only when the user explicitly asks for write actions such as retrying jobs or posting comments about the failure.

## Workflow

1. Resolve the target pipeline context.
   - Prefer a pipeline URL, merge request URL, or explicit project plus pipeline identifier.
   - If the user references "the latest pipeline on this MR", resolve the merge request first and then inspect the latest linked pipeline.
2. Gather pipeline data.
   - Read overall pipeline status, failed jobs, stage ordering, and any available logs or error summaries.
   - Cross-check the merge request diff when the failure is likely change-related.
3. Separate failure classes.
   - code or test regressions
   - infrastructure or environment failures
   - flaky or transient failures
   - permission or configuration problems
4. Summarize the likely root cause and the smallest next action.
   - State clearly when the evidence is weak or logs are incomplete.

## Write Safety

- Do not retry jobs, cancel pipelines, or post back to GitLab unless the user explicitly asks.
- If logs are unavailable through the server or token scope, say so instead of inventing a root cause.
- If the failure appears unrelated to the merge request diff, call that out explicitly.

## Output Expectations

- Give the current pipeline status first.
- List the failed jobs and the likely cause of each.
- End with the smallest next action that would reduce uncertainty or unblock the merge request.
