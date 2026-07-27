#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://app.alignbase.ai/mcp"


def read_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_mcp_server(relative_path: str) -> None:
    config = read_json(relative_path)
    server = config["mcpServers"]["alignbase"]
    assert server["url"] == MCP_URL
    assert server["type"] == "http"


def main() -> None:
    codex_catalog = read_json(".agents/plugins/marketplace.json")
    assert codex_catalog["name"] == "alignbase"
    assert codex_catalog["plugins"][0]["source"] == {
        "source": "local",
        "path": "./plugins/codex/alignbase",
    }

    claude_catalog = read_json(".claude-plugin/marketplace.json")
    assert claude_catalog["name"] == "alignbase"
    assert claude_catalog["plugins"][0]["source"] == "./plugins/claude/alignbase"

    codex_manifest = read_json("plugins/codex/alignbase/.codex-plugin/plugin.json")
    assert codex_manifest["name"] == "alignbase"
    assert codex_manifest["mcpServers"] == "./.mcp.json"
    assert_mcp_server("plugins/codex/alignbase/.mcp.json")

    codex_hooks = read_json("plugins/codex/alignbase/hooks/hooks.json")
    codex_hook = codex_hooks["hooks"]["SessionStart"][0]["hooks"][0]
    assert codex_hook["command"] == '"$PLUGIN_ROOT/scripts/session-start.sh"'
    assert "PLUGIN_ROOT" in codex_hook["commandWindows"]

    hook_output = subprocess.run(
        ["sh", str(ROOT / "plugins/codex/alignbase/scripts/session-start.sh")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    response = json.loads(hook_output)
    assert response["continue"] is True
    hook_context = response["hookSpecificOutput"]
    assert hook_context["hookEventName"] == "SessionStart"
    assert "get_current_context" in hook_context["additionalContext"]
    assert "before responding" in hook_context["additionalContext"].lower()
    assert "systemMessage" not in response
    assert "AGENTS.md" not in hook_output

    claude_manifest = read_json("plugins/claude/alignbase/.claude-plugin/plugin.json")
    assert claude_manifest["name"] == "alignbase"
    assert_mcp_server("plugins/claude/alignbase/.mcp.json")
    assert codex_manifest["version"] == claude_manifest["version"]
    assert claude_catalog["metadata"]["version"] == claude_manifest["version"]

    claude_hooks = read_json("plugins/claude/alignbase/hooks/hooks.json")
    claude_hook = claude_hooks["hooks"]["SessionStart"][0]["hooks"][0]
    assert claude_hook == {
        "type": "mcp_tool",
        "server": "alignbase",
        "tool": "get_current_context",
        "input": {},
    }

    print("Marketplace validation passed.")


if __name__ == "__main__":
    main()
