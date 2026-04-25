# Codex API Plugins

`codex-api-plugins` is a public collection of Codex plugins designed for **Codex API mode**.

The repository starts with one productionized plugin, `github-gh`, and is structured to grow into a multi-plugin collection over time.

## Why this repository exists

Codex supports plugins, but many example or official plugin flows assume ChatGPT app login or bundled connectors.

This repository focuses on a different target:

- Codex API mode
- local plugin installation
- explicit marketplace registration
- plugin workflows that can run with local tools such as `gh`

## Included plugins

| Plugin | Status | What it does | Notes |
| --- | --- | --- | --- |
| `github-gh` | `v0.1.0` | Repository triage, PR review, CI debugging, and draft PR workflows through GitHub CLI | Built for Codex API mode without ChatGPT app login |

## Recommended installation

The recommended path is **home-local installation**.

1. Clone this repository to a stable local path.
2. Run the Windows installer script:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\install-home-local.ps1
   ```

3. Restart Codex Desktop.
4. Open the plugin picker and look for `GitHub (gh)`.

Detailed steps are in [docs/install.md](docs/install.md).

## Usage

The `github-gh` plugin is invoked through the plugin mention:

```text
[@github-gh](plugin://github-gh@codex-api-plugins)
```

Example prompts:

- `[@github-gh](plugin://github-gh@codex-api-plugins) summarize PR 123 in owner/repo`
- `[@github-gh](plugin://github-gh@codex-api-plugins) review the latest unresolved comments on PR 123`
- `[@github-gh](plugin://github-gh@codex-api-plugins) debug the failing checks on this branch`
- `[@github-gh](plugin://github-gh@codex-api-plugins) commit these changes, push, and open a draft PR`

Detailed usage is in [docs/usage/github-gh.md](docs/usage/github-gh.md).

## Repository layout

```text
.
├── .agents/plugins/marketplace.json
├── docs/
├── plugins/
│   └── github-gh/
└── scripts/
```

- `plugins/<plugin-name>/` contains each plugin bundle
- `.agents/plugins/marketplace.json` exposes the repository marketplace
- `docs/` contains installation, usage, troubleshooting, and development docs
- `scripts/` contains local install and repository validation helpers

## Current limitations

`github-gh` depends on GitHub CLI. In some Windows network environments, GitHub API transport may be flaky.

This repository already bakes in the current workaround:

- scripts inject `GODEBUG=http2client=0`
- retry logic is enabled for transient `EOF` / timeout failures
- comment-fetch workflows can fall back when GraphQL is unstable

Troubleshooting guidance lives in [docs/troubleshooting.md](docs/troubleshooting.md).

## Adding more plugins

Future plugins must follow the same repository contract:

- each plugin gets its own directory under `plugins/`
- each plugin must have `.codex-plugin/plugin.json`
- each plugin must be registered in the root marketplace
- each plugin must ship install and usage documentation

Development rules live in [docs/development.md](docs/development.md).
