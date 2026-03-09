"""Tests for Monkey agent definition — Story 3.4."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
AGENT_FILE = AGENTS_DIR / "monkey.md"


class TestMonkeyAgentFile:
    """AC#1: Agent definition file."""

    def test_agent_file_exists(self):
        assert AGENT_FILE.exists()

    def test_agent_has_persona(self):
        content = AGENT_FILE.read_text()
        assert "<persona>" in content
        assert "Python" in content

    def test_agent_has_python_role(self):
        content = AGENT_FILE.read_text()
        assert "Python Code Generation Specialist" in content

    def test_agent_has_menu(self):
        content = AGENT_FILE.read_text()
        assert "<menu>" in content

    def test_agent_has_all_menu_items(self):
        content = AGENT_FILE.read_text()
        for code in ["[MH]", "[CH]", "[DS]", "[CR]", "[PM]", "[DA]"]:
            assert code in content, f"Missing menu item: {code}"

    def test_agent_has_activation(self):
        content = AGENT_FILE.read_text()
        assert "<activation" in content

    def test_agent_references_mm_config(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/config.yaml" in content
        assert "_bmad/bmm/config.yaml" not in content

    def test_agent_references_mm_dev_workflows(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/workflows/dev/" in content

    def test_agent_declares_gitlab_mcp(self):
        content = AGENT_FILE.read_text()
        assert "gitlab-mcp" in content

    def test_agent_no_specdb_mcp(self):
        content = AGENT_FILE.read_text()
        lines = content.split("\n")
        for line in lines:
            if "specdb-mcp" in line.lower():
                assert "never" in line.lower() or "not" in line.lower() or "no" in line.lower(), \
                    f"specdb-mcp referenced without negation: {line}"


class TestMonkeyPersonaIsolation:
    """Verify Monkey persona is Python-only — no cross-language contamination."""

    def test_persona_does_not_reference_java(self):
        content = AGENT_FILE.read_text()
        start = content.find("<persona>")
        end = content.find("</persona>")
        persona = content[start:end] if start != -1 and end != -1 else content
        assert "Java" not in persona, "Monkey persona must not reference Java"

    def test_persona_role_is_not_cobol(self):
        """COBOL may appear as source language in identity — but the role must be Python."""
        content = AGENT_FILE.read_text()
        start = content.find("<role>")
        end = content.find("</role>")
        role = content[start:end] if start != -1 and end != -1 else content
        assert "COBOL" not in role, "Monkey role must not reference COBOL as target"
        assert "Python" in role

    def test_target_language_rule_is_python(self):
        content = AGENT_FILE.read_text()
        assert "Target language is Python" in content


class TestMonkeyModuleHelp:
    """AC#2: Agent installation and invocation."""

    def test_module_help_has_monkey(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "monkey" in content.lower()
        assert "bmad-agent-mm-monkey" in content

    def test_party_roster_has_monkey(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "teams" / "default-party.csv"
        content = path.read_text()
        assert "monkey" in content.lower()
        assert "Python Dev Agent" in content
