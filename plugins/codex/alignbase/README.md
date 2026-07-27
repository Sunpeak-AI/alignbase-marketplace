# Alignbase for Codex

This plugin connects Codex to Alignbase through the hosted OAuth MCP server.

The session hook shows a startup reminder, but current Codex hooks cannot call an MCP tool or add the tool result to model context. Keep Alignbase's short startup instruction enabled in the global Codex `AGENTS.md` until Codex supports direct startup context loading.

After installation, approve the plugin hook in `/hooks`, connect the Alignbase MCP server in `/mcp`, and start a new session.
