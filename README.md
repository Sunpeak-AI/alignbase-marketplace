# Alignbase plugin marketplace

This repository distributes the official Alignbase plugins for Codex, Claude Desktop, and Claude Code.

## Codex

```sh
codex plugin marketplace add Sunpeak-AI/alignbase-marketplace &&
codex plugin add alignbase@alignbase
```

Sign in, approve Alignbase in `/hooks`, and start a new session.

## Claude Desktop

Open **Customize > Plugins > + > Add marketplace > Add from a repository**.

```text
https://github.com/Sunpeak-AI/alignbase-marketplace
```

Install Alignbase, sign in, and start a new Cowork or local Code session.

## Claude Code

```sh
claude plugin marketplace add Sunpeak-AI/alignbase-marketplace
claude plugin install alignbase@alignbase
```

Run `/mcp`, connect Alignbase, and start a new session.

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
