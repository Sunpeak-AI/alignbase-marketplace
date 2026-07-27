# Alignbase for Codex

This plugin connects Codex to Alignbase through the hosted OAuth MCP server.

The `SessionStart` hook adds an instruction to the agent context that tells Codex to call `get_current_context` before responding to the next request.

After installation, approve the plugin hook in `/hooks`, connect the Alignbase MCP server in `/mcp`, and start a new session.
