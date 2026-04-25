# Development

This repository is a multi-plugin collection for Codex API mode.

## Rules for adding future plugins

Every new plugin must follow this contract:

1. Create `plugins/<plugin-name>/`
2. Include `plugins/<plugin-name>/.codex-plugin/plugin.json`
3. Register the plugin in `.agents/plugins/marketplace.json`
4. Add install and usage docs
5. Add troubleshooting notes if the plugin has external dependencies or known failure modes

## Required metadata

Every plugin manifest should provide:

- stable plugin id
- version
- description
- author
- repository URL
- license
- UI-facing `interface` metadata

## Repository update checklist

When you add a plugin:

- update `.agents/plugins/marketplace.json`
- update the plugin table in `README.md`
- add usage docs under `docs/usage/`
- update troubleshooting docs if needed
- run `scripts/validate-repo.ps1`

## Compatibility expectations

Plugins in this repository should be designed for:

- Codex API mode first
- local plugin installation
- reproducible marketplace registration

Avoid designs that require:

- ChatGPT app-only auth flows
- hidden connector dependencies
- undocumented machine-local configuration

## Validation standard

Before publishing a plugin update:

- JSON manifests parse successfully
- Python helper scripts compile successfully
- install docs match the actual config shape
- the plugin can be discovered from the registered marketplace
