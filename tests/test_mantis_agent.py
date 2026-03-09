"""Tests for Mantis agent definition and QA workflows — Story 3.6."""

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
AGENT_FILE = AGENTS_DIR / "mantis.md"
QA_WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "qa"


class TestMantisAgentFile:
    """AC#1: Agent definition file."""

    def test_agent_file_exists(self):
        assert AGENT_FILE.exists()

    def test_agent_has_persona(self):
        content = AGENT_FILE.read_text()
        assert "<persona>" in content
        assert "QA" in content or "Migration" in content

    def test_agent_has_qa_role(self):
        content = AGENT_FILE.read_text()
        assert "Migration QA Specialist" in content

    def test_agent_has_menu(self):
        content = AGENT_FILE.read_text()
        assert "<menu>" in content

    def test_agent_has_all_menu_items(self):
        content = AGENT_FILE.read_text()
        for code in ["[MH]", "[CH]", "[QA]", "[PM]", "[DA]"]:
            assert code in content, f"Missing menu item: {code}"

    def test_agent_has_activation(self):
        content = AGENT_FILE.read_text()
        assert "<activation" in content

    def test_agent_references_mm_config(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/config.yaml" in content
        assert "_bmad/bmm/config.yaml" not in content

    def test_agent_references_mm_qa_workflows(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/workflows/qa/" in content

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


class TestQaWorkflowDirectory:
    """AC#2: QA workflows copied and adapted."""

    def test_qa_workflow_directory_exists(self):
        assert (QA_WORKFLOWS_DIR / "qa-generate-e2e-tests").is_dir()

    def test_workflow_yaml_exists(self):
        assert (QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "workflow.yaml").exists()

    def test_instructions_exist(self):
        assert (QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "instructions.md").exists()

    def test_checklist_exists(self):
        assert (QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "checklist.md").exists()

    def test_workflow_yaml_valid(self):
        path = QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "name" in data
        assert "config_source" in data
        assert "installed_path" in data

    def test_workflow_config_points_to_mm(self):
        path = QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "_bmad/mm/config.yaml" in data["config_source"]
        assert "_bmad/bmm/" not in data["config_source"]

    def test_workflow_declares_gitlab_mcp(self):
        path = QA_WORKFLOWS_DIR / "qa-generate-e2e-tests" / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "mcp_tools" in data
        assert "close_epic" in data["mcp_tools"]
        assert "add_comment" in data["mcp_tools"]


class TestMantisModuleHelp:
    """AC#3: Agent installation and invocation."""

    def test_module_help_has_mantis(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "mantis" in content.lower()
        assert "bmad-agent-mm-mantis" in content

    def test_module_help_has_qa_workflow(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "QA Automation Test" in content
        assert "_bmad/mm/workflows/qa/qa-generate-e2e-tests/" in content

    def test_party_roster_has_mantis(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "teams" / "default-party.csv"
        content = path.read_text()
        assert "mantis" in content.lower()
        assert "QA Agent" in content
