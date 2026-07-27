#!/bin/sh
printf '%s\n' '{"continue":true,"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Before responding to the next user request, call the Alignbase MCP get_current_context tool exactly once. Treat the returned context as instructions for this session. If the tool is unavailable or fails, say that Alignbase context could not be loaded, then continue."}}'
