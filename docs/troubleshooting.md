# Troubleshooting

## The plugin does not appear in Codex UI

Check these items in order:

1. Confirm the marketplace is registered in `~/.codex/config.toml`
2. Confirm `github-gh@codex-api-plugins` and `gitlab-mcp@codex-api-plugins` are enabled in the same file
3. Confirm the repository path in the marketplace block points to your local clone
4. Fully restart Codex Desktop

If you used the installer script, rerun it once:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-home-local.ps1
```

## `gh` is missing

Install GitHub CLI:

```powershell
winget install --id GitHub.cli
```

Then verify:

```powershell
gh --version
```

## `gh` is installed but not authenticated

Run:

```powershell
gh auth login
gh auth status
```

## GitHub API requests fail with `EOF`

This is a known transport problem in some Windows environments.

Recommended workaround for manual commands:

```powershell
$env:GODEBUG='http2client=0'
```

What this repository already does:

- injects `GODEBUG=http2client=0` inside plugin scripts
- retries transient GitHub CLI failures
- falls back when GraphQL comment reads are unstable

## Review-thread data is incomplete

If GitHub GraphQL transport fails, `github-gh` can fall back to REST comment reads.

In fallback mode:

- PR comments are still available
- review comments are still available
- true review-thread grouping may be missing
- resolved / unresolved thread state may be unavailable

## The wrong GitHub account is active

Check your active account:

```powershell
gh auth status
```

If needed, switch accounts or re-authenticate before using the plugin.

## `gitlab-mcp` reports `invalid_token`

Your GitLab token is missing, expired, or not the token value that the current Codex session inherited.

Check these items:

1. Confirm `GITLAB_PERSONAL_ACCESS_TOKEN` is set at the user or machine scope.
2. Confirm the token has not expired in GitLab.
3. Restart Codex Desktop after changing the user environment variable so new sessions inherit the new token.

## `gitlab-mcp` cannot connect to the server

The most common cause is a bad `GITLAB_API_URL`.

Use this format:

```powershell
[Environment]::SetEnvironmentVariable('GITLAB_API_URL', 'https://gitlab.example.com/api/v4', 'User')
```

Checks:

- use the GitLab base URL for your instance
- include `/api/v4`
- avoid the project or merge request web URL here

## `gitlab-mcp` can read but cannot write

This usually means the token only has `read_api` scope.

For write-back workflows such as draft review notes or published feedback, create a token with:

- `api`

If you want read-only inspection only, `read_api` is enough.

## GitLab review feedback does not appear in the MR

Check whether the workflow only drafted notes and never published them.

The plugin defaults to draft-first review:

- create draft notes first
- publish only when explicitly requested

If the token is read-only, draft creation may fail and the plugin should fall back to chat-only feedback.

## How to validate the repo after changes

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-repo.ps1
```
