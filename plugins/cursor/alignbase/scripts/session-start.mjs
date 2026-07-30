#!/usr/bin/env node

process.stdout.write(JSON.stringify({
  additional_context: "Before answering the first user request, call the Alignbase MCP get_current_context tool exactly once. If the tool is unavailable or the call fails, tell the user that Alignbase context could not be loaded and ask whether they want to continue without it. Do not answer the user's request until they confirm.",
}));
