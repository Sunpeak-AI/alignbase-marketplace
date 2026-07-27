# Alignbase plugin marketplace

This repository distributes the official Alignbase plugins for Codex and Claude Code.

Each plugin connects the host to Alignbase's OAuth MCP server at `https://app.alignbase.ai/mcp`. The plugin also installs a session-start hook so Alignbase can load or request current context when a session begins.

## Codex

Add the marketplace and install the plugin:

```sh
codex plugin marketplace add Sunpeak-AI/alignbase-marketplace
codex plugin add alignbase@alignbase
```

Open `/mcp` in Codex and connect Alignbase. Then open `/hooks`, approve the Alignbase hook, and start a new session.

Codex session hooks cannot call MCP tools or add tool output to the model context yet. Keep the short Alignbase startup instruction in your global `AGENTS.md` until Codex adds that hook support.

## Claude Code

Add the marketplace and install the plugin:

```sh
claude plugin marketplace add Sunpeak-AI/alignbase-marketplace
claude plugin install alignbase@alignbase
```

Open `/mcp` in Claude Code and authenticate Alignbase. Start a new session after the server shows as connected.

## Repository layout

- `.agents/plugins/marketplace.json` is the Codex marketplace catalog.
- `.claude-plugin/marketplace.json` is the Claude Code marketplace catalog.
- `plugins/codex/alignbase` contains the Codex plugin.
- `plugins/claude/alignbase` contains the Claude Code plugin.

## Publishing updates

Keep the Codex manifest version, Claude Code manifest version, and Claude Code marketplace metadata version in sync. Bump all three before publishing any plugin change because both hosts cache installed plugin versions.

Run the local checks before pushing:

```sh
python3 scripts/validate.py
claude plugin validate .
```
