# Troubleshooting

## The plugin does not appear in Codex UI

Check these items in order:

1. Confirm the marketplace is registered in `~/.codex/config.toml`
2. Confirm `github-gh@codex-api-plugins` is enabled in the same file
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

## How to validate the repo after changes

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-repo.ps1
```
