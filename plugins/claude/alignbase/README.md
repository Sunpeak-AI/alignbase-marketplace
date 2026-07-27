# Alignbase for Claude

This plugin connects Claude Desktop and Claude Code to Alignbase through the hosted OAuth MCP server. Its `SessionStart` hook calls `get_current_context` and adds the returned text to Claude's context in Cowork and Code sessions.

In Claude Desktop, complete the Alignbase sign-in prompt during plugin installation, then start a new Cowork or local Code session. Claude Desktop Chat can use the bundled connector, but Chat does not run plugin hooks.

In Claude Code, open `/mcp` and authenticate Alignbase. Start a new session after the server shows as connected because Claude runs `SessionStart` before a new MCP connection finishes.
