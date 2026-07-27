# Alignbase for Claude Code

This plugin connects Claude Code to Alignbase through the hosted OAuth MCP server. Its `SessionStart` hook calls `get_current_context` and adds the returned text to Claude's context.

After installation, open `/mcp` and authenticate Alignbase. Start a new session after the server shows as connected because Claude runs `SessionStart` before a new MCP connection finishes.
