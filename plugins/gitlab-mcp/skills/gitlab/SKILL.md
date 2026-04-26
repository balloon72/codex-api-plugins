---
name: gitlab
description: Triage and orient GitLab project, merge request, issue, discussion, wiki, and pipeline work through the bundled GitLab MCP server.
---

# GitLab

## Overview

Use this skill as the umbrella entrypoint for general GitLab work in this plugin. It should resolve project or merge request context, inspect the relevant GitLab objects, and route to the review or pipeline specialist skill when the request becomes narrower.

This plugin is MCP-first:

- Use the bundled GitLab MCP server for project, branch, file, merge request, discussion, issue, wiki, milestone, and pipeline workflows.
- Prefer a merge request URL, issue URL, or project path from the user when available.
- Treat self-hosted GitLab the same as GitLab.com as long as `GITLAB_API_URL` is configured correctly.

## Preflight

Check these prerequisites before GitLab work:

- `GITLAB_PERSONAL_ACCESS_TOKEN` is present in the local environment.
- `GITLAB_API_URL` is present and points to the GitLab REST root ending in `/api/v4`.
- The token scope matches the requested action:
  - `api` for read and write workflows such as review comments or draft notes
  - `read_api` for read-only inspection

If the token or API URL is missing, stop and tell the user exactly which variable is missing. If the API URL does not end in `/api/v4`, ask the user to correct it before continuing.

## Direct Responsibilities

Handle these directly when the request does not need a narrower specialist workflow:

- repository and merge request orientation
- project, issue, label, milestone, and wiki lookups
- merge request metadata, diff, and discussion summaries
- top-level draft note or discussion drafting when the user already knows what they want to send
- general GitLab object navigation from a URL

## Routing Rules

1. Resolve the operating context first.
   - If the user provides a merge request URL, issue URL, pipeline URL, or project path, use that directly.
   - If the request is about "this MR" or "the latest pipeline", resolve the project and item before proceeding.
2. Classify the request before taking action.
   - `general triage`: summarize a project, merge request, issue, wiki page, or discussions
   - `review workflow`: analyze a merge request, cluster findings, or draft review feedback
   - `pipeline workflow`: inspect failed jobs, status transitions, or likely CI root causes
3. Route immediately when the category is clear.
   - Merge request review and feedback drafting: `../gitlab-review/SKILL.md`
   - Pipeline inspection and failure analysis: `../gitlab-pipeline/SKILL.md`

## Default Workflow

1. Resolve the project and GitLab object from a URL or explicit identifier.
2. Gather metadata, diff, discussions, and linked pipeline context through GitLab MCP.
3. Decide whether the task stays in general GitLab triage or should move to review or pipeline handling.
4. Route to the specialist skill as soon as the work becomes narrower than general triage.
5. End with a concise summary of what was inspected, what was written, and what remains.

## Write Safety

- Do not publish review feedback, reply to discussions, approve merge requests, merge branches, or retry pipelines unless the user explicitly asks for that write action.
- If the request is ambiguous between "summarize" and "write back to GitLab", default to summarize only.
- If the user has a read-only token, do not imply that draft notes or discussions can be created.

## Examples

- "Use GitLab to summarize this merge request and tell me what needs attention."
- "Inspect this GitLab issue and the linked wiki page."
- "Check the latest discussions on this MR."
- "Help with this GitLab merge request."
