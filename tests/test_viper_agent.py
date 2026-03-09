"""Tests for Viper agent definition — Story 3.3."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
AGENT_FILE = AGENTS_DIR / "viper.md"


class TestViperAgentFile:
    """AC#1: Agent definition file."""

    def test_agent_file_exists(self):
        assert AGENT_FILE.exists()

    def test_agent_has_persona(self):
        content = AGENT_FILE.read_text()
        assert "<persona>" in content
        assert "COBOL" in content

    def test_agent_has_cobol_role(self):
        content = AGENT_FILE.read_text()
        assert "COBOL Modernisation Specialist" in content

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


class TestViperPersonaIsolation:
    """Verify Viper persona is COBOL-only — no cross-language contamination."""

    def test_persona_does_not_reference_java(self):
        content = AGENT_FILE.read_text()
        start = content.find("<persona>")
        end = content.find("</persona>")
        persona = content[start:end] if start != -1 and end != -1 else content
        assert "Java" not in persona, "Viper persona must not reference Java"

    def test_persona_does_not_reference_python(self):
        content = AGENT_FILE.read_text()
        start = content.find("<persona>")
        end = content.find("</persona>")
        persona = content[start:end] if start != -1 and end != -1 else content
        assert "Python" not in persona, "Viper persona must not reference Python"

    def test_target_language_rule_is_cobol(self):
        content = AGENT_FILE.read_text()
        assert "Target language is COBOL" in content


class TestViperModuleHelp:
    """AC#2: Agent installation and invocation."""

    def test_module_help_has_viper(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "viper" in content.lower()
        assert "bmad-agent-mm-viper" in content

    def test_party_roster_has_viper(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "teams" / "default-party.csv"
        content = path.read_text()
        assert "viper" in content.lower()
        assert "COBOL Dev Agent" in content
