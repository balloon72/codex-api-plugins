# Installation

This repository is designed for **Codex API mode** and currently documents a **Windows-first** installation path.

## Recommended: home-local installation

### Prerequisites

- Codex Desktop or another Codex environment that supports local plugins
- A local clone of this repository
- GitHub CLI installed if you plan to use `github-gh`
- GitHub CLI authenticated with:

  ```powershell
  gh auth login
  ```

### 1. Clone the repository

Clone the repo to a stable local path. Example:

```powershell
git clone https://github.com/balloon72/codex-api-plugins.git
cd .\codex-api-plugins
```

### 2. Register the marketplace in Codex

Run the installer from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-home-local.ps1
```

What the script does:

- finds your repo root
- updates `~/.codex/config.toml`
- registers the local marketplace `codex-api-plugins`
- enables `github-gh@codex-api-plugins`
- creates a timestamped config backup before writing changes

### 3. Restart Codex

Completely close Codex Desktop and launch it again.

### 4. Verify that the plugin is visible

Open the plugin picker or plugin management UI and look for:

- `GitHub (gh)`

If it does not appear, see [troubleshooting.md](troubleshooting.md).

## Optional: manual config update

The script is the supported path, but the equivalent config shape is:

```toml
[marketplaces.codex-api-plugins]
last_updated = "2026-04-25T00:00:00Z"
source_type = "local"
source = '\\?\C:\path\to\codex-api-plugins'

[plugins."github-gh@codex-api-plugins"]
enabled = true
```

Notes:

- Replace the path with your actual repository path.
- Keep the extended Windows path prefix `\\?\`.
- Use any valid UTC RFC3339 timestamp for `last_updated`.

## Optional: repo-local installation

This repository is optimized for home-local installation. If you want repo-local installation for another project:

1. Copy `plugins/github-gh/` into your target repository under `plugins/github-gh/`
2. Copy the marketplace entry from `.agents/plugins/marketplace.json`
3. Register the target repository as the marketplace source in that environment

This mode is intentionally not the default because it is harder to maintain across multiple projects.
