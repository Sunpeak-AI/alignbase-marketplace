#!/usr/bin/env python3

import json
import struct
import subprocess
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://app.alignbase.ai/mcp"
MAX_OPENAI_IMAGE_BYTES = 5 * 1024 * 1024
MIN_OPENAI_RASTER_DIMENSION = 48
MAX_OPENAI_RASTER_DIMENSION = 4096


def read_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_mcp_server(relative_path: str, wrapped: bool = True) -> None:
    config = read_json(relative_path)
    server = config["mcpServers"]["alignbase"] if wrapped else config["alignbase"]
    assert server["url"] == MCP_URL
    assert "oauth" not in server
    assert "headers" not in server


def assert_svg_logo(relative_path: str) -> None:
    path = ROOT / relative_path
    assert 0 < path.stat().st_size <= MAX_OPENAI_IMAGE_BYTES
    svg_text = path.read_text(encoding="utf-8")
    upper_svg_text = svg_text.upper()
    assert "<!DOCTYPE" not in upper_svg_text
    assert "<!ENTITY" not in upper_svg_text
    root = ET.fromstring(svg_text)
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert root.attrib["width"] == "400"
    assert root.attrib["height"] == "400"
    assert root.attrib["viewBox"] == "0 0 400 400"
    forbidden_elements = {
        "audio",
        "embed",
        "foreignObject",
        "iframe",
        "image",
        "object",
        "script",
        "style",
        "video",
    }
    for element in root.iter():
        element_name = element.tag.rsplit("}", 1)[-1]
        assert element_name not in forbidden_elements
        for attribute_name, attribute_value in element.attrib.items():
            local_attribute_name = attribute_name.rsplit("}", 1)[-1]
            assert not local_attribute_name.lower().startswith("on")
            assert local_attribute_name not in {"href", "src"}
            if "url(" in attribute_value.lower():
                assert attribute_value.lower().startswith("url(#")
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    background = root.find("svg:rect", namespace)
    assert background is not None
    assert background.attrib["width"] == "400"
    assert background.attrib["height"] == "400"
    assert len(root.findall("svg:path", namespace)) == 3


def assert_png_logo(relative_path: str) -> None:
    path = ROOT / relative_path
    data = path.read_bytes()
    assert 0 < len(data) <= MAX_OPENAI_IMAGE_BYTES
    assert data[:8] == b"\x89PNG\r\n\x1a\n"

    offset = 8
    chunks: list[tuple[bytes, bytes]] = []
    while offset < len(data):
        assert offset + 12 <= len(data)
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        assert chunk_end <= len(data)
        chunk_data = data[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack(">I", data[offset + 8 + length : chunk_end])[0]
        assert zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF == expected_crc
        chunks.append((chunk_type, chunk_data))
        offset = chunk_end
        if chunk_type == b"IEND":
            break

    assert offset == len(data)
    assert chunks[0][0] == b"IHDR"
    assert chunks[-1][0] == b"IEND"
    ihdr = chunks[0][1]
    assert len(ihdr) == 13
    width, height, bit_depth, color_type, compression, filtering, interlace = (
        struct.unpack(">IIBBBBB", ihdr)
    )
    assert (width, height) == (400, 400)
    assert MIN_OPENAI_RASTER_DIMENSION <= width <= MAX_OPENAI_RASTER_DIMENSION
    assert width == height
    assert (bit_depth, color_type, compression, filtering, interlace) == (
        8,
        6,
        0,
        0,
        0,
    )
    compressed = b"".join(
        chunk_data for chunk_type, chunk_data in chunks if chunk_type == b"IDAT"
    )
    expected_decoded_bytes = height * (1 + width * 4)
    decompressor = zlib.decompressobj()
    decoded = decompressor.decompress(compressed, expected_decoded_bytes + 1)
    assert len(decoded) == expected_decoded_bytes
    assert decompressor.eof
    assert not decompressor.unused_data
    assert not decompressor.unconsumed_tail
    row_bytes = 1 + width * 4
    for row in range(height):
        assert decoded[row * row_bytes] in range(5)


def assert_no_fixed_oauth_config(plugin_root: str) -> None:
    for path in (ROOT / plugin_root).rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png"}:
            continue
        content = path.read_text(encoding="utf-8")
        for forbidden in ("ab_client_", "oauth_client_id", "clientId"):
            assert forbidden not in content, f"{path} contains {forbidden}"


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

    cursor_catalog = read_json(".cursor-plugin/marketplace.json")
    assert cursor_catalog["name"] == "alignbase"
    assert cursor_catalog["plugins"][0]["source"] == "plugins/cursor/alignbase"
    assert cursor_catalog["plugins"][0]["logo"] == (
        "plugins/cursor/alignbase/assets/alignbase-logo.svg"
    )

    codex_manifest = read_json("plugins/codex/alignbase/.codex-plugin/plugin.json")
    assert codex_manifest["name"] == "alignbase"
    assert codex_manifest["mcpServers"] == "./.mcp.json"
    assert "hooks" not in codex_manifest
    assert codex_manifest["interface"]["defaultPrompt"] == [
        "Load the Alignbase context assigned to this agent.",
        "List the Alignbase Skills available to this agent.",
    ]
    assert len(codex_manifest["interface"]["shortDescription"]) <= 30
    codex_logo = codex_manifest["interface"]["logo"]
    assert codex_logo == "./assets/alignbase-logo.png"
    assert codex_manifest["interface"]["composerIcon"] == codex_logo
    assert_png_logo("plugins/codex/alignbase/assets/alignbase-logo.png")
    assert_svg_logo("plugins/codex/alignbase/assets/alignbase-logo.svg")
    assert_mcp_server("plugins/codex/alignbase/.mcp.json", wrapped=False)

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
    assert "ask whether they want to continue without it" in hook_context["additionalContext"]
    assert "until they confirm" in hook_context["additionalContext"]
    assert "then continue" not in hook_context["additionalContext"]
    assert "systemMessage" not in response
    assert "AGENTS.md" not in hook_output

    claude_manifest = read_json("plugins/claude/alignbase/.claude-plugin/plugin.json")
    assert claude_manifest["name"] == "alignbase"
    assert claude_manifest["$schema"].endswith(
        "/claude-code-plugin-manifest.json"
    )
    assert "userConfig" not in claude_manifest
    assert_mcp_server("plugins/claude/alignbase/.mcp.json")
    assert_png_logo("plugins/claude/alignbase/assets/alignbase-logo.png")
    assert_svg_logo("plugins/claude/alignbase/assets/alignbase-logo.svg")

    cursor_manifest = read_json(
        "plugins/cursor/alignbase/.cursor-plugin/plugin.json"
    )
    assert cursor_manifest["name"] == "alignbase"
    assert cursor_manifest["logo"] == "assets/alignbase-logo.svg"
    assert cursor_manifest["hooks"] == "./hooks/hooks.json"
    assert cursor_manifest["mcpServers"] == "./mcp.json"
    assert_svg_logo("plugins/cursor/alignbase/assets/alignbase-logo.svg")
    assert_png_logo("plugins/cursor/alignbase/assets/alignbase-logo.png")
    assert_mcp_server("plugins/cursor/alignbase/mcp.json")

    png_logos = {
        (ROOT / f"plugins/{vendor}/alignbase/assets/alignbase-logo.png").read_bytes()
        for vendor in ("codex", "claude", "cursor")
    }
    svg_logos = {
        (ROOT / f"plugins/{vendor}/alignbase/assets/alignbase-logo.svg").read_bytes()
        for vendor in ("codex", "claude", "cursor")
    }
    assert len(png_logos) == 1
    assert len(svg_logos) == 1

    versions = {
        codex_manifest["version"],
        claude_manifest["version"],
        cursor_manifest["version"],
        claude_catalog["metadata"]["version"],
        cursor_catalog["metadata"]["version"],
    }
    assert len(versions) == 1
    assert claude_catalog["metadata"]["version"] == claude_manifest["version"]
    for plugin_root in (
        "plugins/codex/alignbase",
        "plugins/claude/alignbase",
        "plugins/cursor/alignbase",
    ):
        assert_no_fixed_oauth_config(plugin_root)

    claude_hooks = read_json("plugins/claude/alignbase/hooks/hooks.json")
    claude_hook = claude_hooks["hooks"]["SessionStart"][0]["hooks"][0]
    assert claude_hook == {
        "type": "command",
        "command": "node",
        "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/session-start.mjs"],
        "timeout": 10,
    }
    claude_hook_output = subprocess.run(
        ["node", str(ROOT / "plugins/claude/alignbase/scripts/session-start.mjs")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    claude_response = json.loads(claude_hook_output)
    claude_context = claude_response["hookSpecificOutput"]
    assert claude_context["hookEventName"] == "SessionStart"
    assert "get_current_context" in claude_context["additionalContext"]
    assert "ask whether they want to continue without it" in claude_context["additionalContext"]
    assert "until they confirm" in claude_context["additionalContext"]
    assert "then continue" not in claude_context["additionalContext"]

    cursor_hooks = read_json("plugins/cursor/alignbase/hooks/hooks.json")
    cursor_command = cursor_hooks["hooks"]["sessionStart"][0]["command"]
    assert cursor_hooks["version"] == 1
    assert "${CURSOR_PLUGIN_ROOT}" in cursor_command
    cursor_hook_output = subprocess.run(
        ["node", str(ROOT / "plugins/cursor/alignbase/scripts/session-start.mjs")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    cursor_context = json.loads(cursor_hook_output)["additional_context"]
    assert "get_current_context" in cursor_context
    assert "ask whether they want to continue without it" in cursor_context
    assert "until they confirm" in cursor_context

    print("Marketplace validation passed.")


if __name__ == "__main__":
    main()
