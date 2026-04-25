# `github-gh` usage

`github-gh` is the first plugin published in this repository.

It is designed for **Codex API mode** and uses:

- `gh` for GitHub data and write actions
- `git` for branch-aware local workflows
- local plugin skills instead of ChatGPT app login

## Prerequisites

- GitHub CLI installed
- GitHub CLI authenticated
- The plugin installed and visible in Codex

Check your GitHub CLI session:

```powershell
gh auth status
```

If GitHub API transport is flaky on your machine, start your PowerShell session with:

```powershell
$env:GODEBUG='http2client=0'
```

The plugin scripts already apply this internally, but it is still useful for manual `gh` commands.

## Plugin mention

Use the plugin with:

```text
[@github-gh](plugin://github-gh@codex-api-plugins)
```

## Common workflows

### Repository and PR triage

Examples:

- `[@github-gh](plugin://github-gh@codex-api-plugins) summarize the latest open PRs in balloon72/draw-io`
- `[@github-gh](plugin://github-gh@codex-api-plugins) inspect PR 123 in owner/repo and tell me what needs attention`
- `[@github-gh](plugin://github-gh@codex-api-plugins) summarize issue 456 in owner/repo`

### Review comments and requested changes

Examples:

- `[@github-gh](plugin://github-gh@codex-api-plugins) review the latest comments on PR 123 in owner/repo`
- `[@github-gh](plugin://github-gh@codex-api-plugins) list unresolved review feedback on this branch PR`
- `[@github-gh](plugin://github-gh@codex-api-plugins) fix the actionable review threads on PR 123`

### CI debugging

Examples:

- `[@github-gh](plugin://github-gh@codex-api-plugins) debug the failing checks on PR 123 in owner/repo`
- `[@github-gh](plugin://github-gh@codex-api-plugins) inspect the failing GitHub Actions jobs on this branch`

### Publish changes and open a draft PR

Examples:

- `[@github-gh](plugin://github-gh@codex-api-plugins) commit these changes, push them, and open a draft PR`
- `[@github-gh](plugin://github-gh@codex-api-plugins) create a draft PR targeting main with a summary of this diff`

## What the plugin currently does well

- repository summaries
- PR summaries
- issue lookup
- draft PR creation through `gh`
- GitHub Actions check inspection
- local branch aware workflows

## Known limitations

- review-thread GraphQL reads may still be unstable in some environments
- the plugin includes retry logic and fallback behavior, but thread resolution state may be unavailable when GraphQL transport fails
- the plugin is Windows-tested first; other platforms may need minor installation adjustments
