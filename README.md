# Alignbase plugin marketplace

This repository distributes the official Alignbase plugins for Codex, Claude Desktop, and Claude Code.

Each plugin connects the host to Alignbase's OAuth MCP server at `https://app.alignbase.ai/mcp`. The plugin also installs a session-start hook so Alignbase can load or request current context when a session begins. Codex receives a hook-injected instruction to call `get_current_context`; Claude Code calls the tool directly from its hook.

## Codex

Add the marketplace and install the plugin:

```sh
codex plugin marketplace add Sunpeak-AI/alignbase-marketplace &&
codex plugin add alignbase@alignbase
```

Complete the Alignbase sign-in prompt during installation. Then approve the Alignbase hook when Codex requests it and start a new session.

## Claude Desktop

Open **Customize > Plugins**. Under **Personal plugins**, select **+ > Add marketplace > Add from a repository**, then enter:

```text
https://github.com/Sunpeak-AI/alignbase-marketplace
```

Open the new Alignbase marketplace and install Alignbase. Complete the Alignbase sign-in prompt, then start a new Cowork or local Code session.

The `SessionStart` hook runs in Cowork and Code. Claude Desktop Chat can use the bundled connector, but Chat does not run plugin hooks.

## Claude Code

Add the marketplace and install the plugin:

```sh
claude plugin marketplace add Sunpeak-AI/alignbase-marketplace
claude plugin install alignbase@alignbase
```

Open `/mcp` in Claude Code and authenticate Alignbase. Start a new session after the server shows as connected.

## Repository layout

- `.agents/plugins/marketplace.json` is the Codex marketplace catalog.
- `.claude-plugin/marketplace.json` is the Claude marketplace catalog.
- `plugins/codex/alignbase` contains the Codex plugin.
- `plugins/claude/alignbase` contains the Claude plugin for Desktop and Code.

## Publishing updates

Keep the Codex manifest version, Claude Code manifest version, and Claude Code marketplace metadata version in sync. Bump all three before publishing any plugin change because both hosts cache installed plugin versions.

Run the local checks before pushing:

```sh
python3 scripts/validate.py
claude plugin validate .
```
