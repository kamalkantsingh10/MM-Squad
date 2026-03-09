"""Tests for Story 1.4: IDE Configuration & Installer Validation.

Validates AC 1-4: Claude Code mcp.json, VS Code mcp.json, installer, end-to-end.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERVERS = {
    "cobol-parser-mcp": "cobol_parser_mcp.server",
    "specdb-mcp": "specdb_mcp.server",
    "delta-macros-mcp": "delta_macros_mcp.server",
    "jcl-parser-mcp": "jcl_parser_mcp.server",
    "gitlab-mcp": "gitlab_mcp.server",
}


class TestAC1ClaudeCodeMcpConfig:
    """AC 1: .claude/mcp.json registers all 5 MCP servers."""

    def test_file_exists(self):
        assert (ROOT / ".claude" / "mcp.json").is_file()

    def test_valid_json(self):
        data = json.loads((ROOT / ".claude" / "mcp.json").read_text())
        assert "mcpServers" in data or "servers" in data

    def test_all_servers_registered(self):
        data = json.loads((ROOT / ".claude" / "mcp.json").read_text())
        servers = data.get("mcpServers", data.get("servers", {}))
        for name in SERVERS:
            assert name in servers, f"Missing server: {name}"

    def test_server_command_format(self):
        data = json.loads((ROOT / ".claude" / "mcp.json").read_text())
        servers = data.get("mcpServers", data.get("servers", {}))
        for name, module in SERVERS.items():
            srv = servers[name]
            assert srv["command"] == "poetry", f"{name} command should be 'poetry'"
            assert srv["args"] == ["run", "python", "-m", module], f"{name} args mismatch"

    def test_env_empty(self):
        data = json.loads((ROOT / ".claude" / "mcp.json").read_text())
        servers = data.get("mcpServers", data.get("servers", {}))
        for name in SERVERS:
            assert servers[name].get("env", {}) == {}, f"{name} env should be empty"


class TestAC2VsCodeMcpConfig:
    """AC 2: .vscode/mcp.json identical to .claude/mcp.json."""

    def test_file_exists(self):
        assert (ROOT / ".vscode" / "mcp.json").is_file()

    def test_valid_json(self):
        data = json.loads((ROOT / ".vscode" / "mcp.json").read_text())
        assert "servers" in data

    def test_all_servers_registered(self):
        data = json.loads((ROOT / ".vscode" / "mcp.json").read_text())
        servers = data.get("servers", {})
        for name in SERVERS:
            assert name in servers, f"Missing server in VS Code config: {name}"

    def test_identical_server_config(self):
        claude_data = json.loads((ROOT / ".claude" / "mcp.json").read_text())
        vscode_data = json.loads((ROOT / ".vscode" / "mcp.json").read_text())
        claude_servers = claude_data.get("mcpServers", claude_data.get("servers", {}))
        vscode_servers = vscode_data.get("servers", {})
        for name in SERVERS:
            assert claude_servers[name] == vscode_servers[name], \
                f"Server config mismatch for {name} between Claude and VS Code"


class TestAC3InstallerReadiness:
    """AC 3: BMAD installer can discover MM module."""

    def test_module_help_csv_exists(self):
        assert (ROOT / "_bmad" / "mm" / "module-help.csv").is_file()

    def test_module_help_has_agent_commands(self):
        content = (ROOT / "_bmad" / "mm" / "module-help.csv").read_text()
        assert "bmad-agent-mm-po" in content
        assert "bmad-agent-mm-shifu" in content


class TestAC4EndToEnd:
    """AC 4: Server startup via IDE config format."""

    def test_servers_importable(self):
        for name, module in SERVERS.items():
            pkg = module.replace(".server", "")
            mod = __import__(f"{pkg}.server", fromlist=["mcp"])
            assert hasattr(mod, "mcp"), f"{name} server missing 'mcp' attribute"

    def test_server_names_match(self):
        for name, module in SERVERS.items():
            pkg = module.replace(".server", "")
            mod = __import__(f"{pkg}.server", fromlist=["mcp"])
            assert mod.mcp.name == name, f"Expected server name '{name}', got '{mod.mcp.name}'"
