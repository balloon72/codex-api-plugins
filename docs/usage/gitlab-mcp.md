# `gitlab-mcp` usage

`gitlab-mcp` is the GitLab-focused plugin in this repository.

It is designed for **Codex API mode** and uses:

- the bundled `@zereight/mcp-gitlab` MCP server
- local environment variables for PAT authentication
- plugin skills to steer review, pipeline, and general GitLab workflows

## Prerequisites

- Node.js with `npx`
- The plugin installed and visible in Codex
- `GITLAB_PERSONAL_ACCESS_TOKEN` configured in your local environment
- `GITLAB_API_URL` configured in your local environment and ending in `/api/v4`

Recommended token scopes:

- `api` for read and write workflows such as draft review notes or publishing feedback
- `read_api` for read-only summaries and inspection

## Plugin mention

Use the plugin with:

```text
[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins)
```

## Common workflows

### Merge request review

Examples:

- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) inspect this merge request URL and tell me the top risks`
- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) review this MR and draft feedback without publishing it yet`
- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) publish the draft review notes you prepared for this merge request`

Default behavior:

- read the MR, diff, discussions, and pipeline context
- summarize blocking findings first
- draft review notes before publishing anything

### Issues and project context

Examples:

- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) summarize issue 321 in group/project`
- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) inspect this project wiki page and explain what is outdated`
- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) summarize the recent discussions on this merge request`

### Pipeline inspection

Examples:

- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) inspect the latest failed pipeline on this merge request`
- `[@gitlab-mcp](plugin://gitlab-mcp@codex-api-plugins) tell me which failed jobs look flaky versus change-related`

## What the plugin currently does well

- merge request summaries
- diff-aware review findings
- draft review notes and publish workflows
- issue and wiki lookup
- pipeline and failed job inspection
- self-hosted GitLab support through `GITLAB_API_URL`

## Known limitations

- write-back flows require a token with `api` scope
- if `GITLAB_API_URL` omits `/api/v4`, requests fail before useful work starts
- draft note or inline position accuracy depends on GitLab returning resolvable diff context
- the plugin assumes local environment variable auth rather than an interactive OAuth flow
