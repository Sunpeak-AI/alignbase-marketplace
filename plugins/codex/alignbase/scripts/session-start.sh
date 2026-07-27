#!/bin/sh
printf '%s\n' '{"continue":true,"systemMessage":"Alignbase startup hook ran. Codex hooks cannot call MCP tools or add context yet, so keep the get_current_context startup instruction in your global AGENTS.md."}'
