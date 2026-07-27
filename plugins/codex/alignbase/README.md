# Alignbase for Codex

This plugin connects Codex to Alignbase through the hosted OAuth MCP server.

The `SessionStart` hook adds an instruction to the agent context that tells Codex to call `get_current_context` before responding to the next request.

Complete the Alignbase sign-in prompt during installation, approve the plugin hook when Codex requests it, and start a new session.
