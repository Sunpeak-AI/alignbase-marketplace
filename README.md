# Alignbase plugin marketplace

This repository contains the official Alignbase plugin packages for the OpenAI universal plugin directory, the Claude plugin directory, and Cursor Marketplace.

## OpenAI

```sh
codex plugin marketplace add Sunpeak-AI/alignbase-marketplace &&
codex plugin add alignbase@alignbase
```

Enable the plugin, connect the Alignbase MCP server when prompted, and sign in to Alignbase. In Codex, approve the startup hook and begin a new session.

## Claude

Open **Customize > Plugins > + > Add marketplace > Add from a repository**.

```text
https://github.com/Sunpeak-AI/alignbase-marketplace
```

Or install with Claude Code:

```sh
claude plugin marketplace add Sunpeak-AI/alignbase-marketplace &&
claude plugin install alignbase@alignbase &&
claude
```

Connect the Alignbase MCP server when prompted, sign in, and start a new Cowork or Claude Code session.

## Cursor

The Cursor package is in `plugins/cursor/alignbase`. Install it from Cursor Marketplace after publication, or test it as a local plugin before submission.

## Repository layout

- `.agents/plugins/marketplace.json` is the Codex marketplace catalog.
- `.claude-plugin/marketplace.json` is the Claude marketplace catalog.
- `.cursor-plugin/marketplace.json` is the Cursor marketplace catalog.
- `plugins/codex/alignbase` contains the Codex plugin.
- `plugins/claude/alignbase` contains the Claude plugin for Cowork and Claude Code.
- `plugins/cursor/alignbase` contains the Cursor plugin.

## Publishing updates

Keep all three plugin manifest versions and both marketplace metadata versions in sync. Bump them before publishing a plugin update because hosts cache installed plugin versions.

Run the local checks before pushing:

```sh
python3 scripts/validate.py
claude plugin validate plugins/claude/alignbase --strict
```

See `SUBMISSION.md` for the store fields, review checks, and unresolved submission blockers.
