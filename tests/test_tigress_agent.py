"""Tests for Tigress agent definition — Story 3.2."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
AGENT_FILE = AGENTS_DIR / "tigress.md"


class TestTigressAgentFile:
    """AC#1: Agent definition file."""

    def test_agent_file_exists(self):
        assert AGENT_FILE.exists()

    def test_agent_has_persona(self):
        content = AGENT_FILE.read_text()
        assert "<persona>" in content
        assert "Java" in content

    def test_agent_has_java_role(self):
        content = AGENT_FILE.read_text()
        assert "Java Code Generation Specialist" in content

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


class TestTigressPersonaIsolation:
    """Verify Tigress persona is Java-only — no cross-language contamination."""

    def test_persona_does_not_reference_python(self):
        content = AGENT_FILE.read_text()
        # Extract persona section only to avoid matching language rules
        start = content.find("<persona>")
        end = content.find("</persona>")
        persona = content[start:end] if start != -1 and end != -1 else content
        assert "Python" not in persona, "Tigress persona must not reference Python"

    def test_persona_does_not_reference_cobol_as_target(self):
        content = AGENT_FILE.read_text()
        start = content.find("<persona>")
        end = content.find("</persona>")
        persona = content[start:end] if start != -1 and end != -1 else content
        assert "COBOL Modernisation" not in persona, "Tigress persona must not reference COBOL Modernisation role"

    def test_target_language_rule_is_java(self):
        content = AGENT_FILE.read_text()
        assert "Target language is Java" in content


class TestTigressModuleHelp:
    """AC#2: Agent installation and invocation."""

    def test_module_help_has_tigress(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "tigress" in content.lower()
        assert "bmad-agent-mm-tigress" in content

    def test_party_roster_has_tigress(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "teams" / "default-party.csv"
        content = path.read_text()
        assert "tigress" in content.lower()
        assert "Java Dev Agent" in content
