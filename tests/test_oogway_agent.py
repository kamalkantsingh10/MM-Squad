"""Tests for Oogway agent definition and architect workflows — Story 3.5."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
AGENT_FILE = AGENTS_DIR / "oogway.md"
ARCHITECT_WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "architect"

EXPECTED_WORKFLOWS = [
    "create-architecture",
    "check-implementation-readiness",
]


class TestOogwayAgentFile:
    """AC#1: Agent definition file."""

    def test_agent_file_exists(self):
        assert AGENT_FILE.exists()

    def test_agent_has_persona(self):
        content = AGENT_FILE.read_text()
        assert "<persona>" in content
        assert "Migration" in content or "Architect" in content

    def test_agent_has_architect_role(self):
        content = AGENT_FILE.read_text()
        assert "Migration Architecture Specialist" in content

    def test_agent_has_menu(self):
        content = AGENT_FILE.read_text()
        assert "<menu>" in content

    def test_agent_has_all_menu_items(self):
        content = AGENT_FILE.read_text()
        for code in ["[MH]", "[CH]", "[CA]", "[IR]", "[PM]", "[DA]"]:
            assert code in content, f"Missing menu item: {code}"

    def test_agent_has_activation(self):
        content = AGENT_FILE.read_text()
        assert "<activation" in content

    def test_agent_references_mm_config(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/config.yaml" in content
        assert "_bmad/bmm/config.yaml" not in content

    def test_agent_references_mm_architect_workflows(self):
        content = AGENT_FILE.read_text()
        assert "_bmad/mm/workflows/architect/" in content

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


class TestArchitectWorkflowDirectories:
    """AC#2: Architect workflows copied and adapted."""

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_directory_exists(self, workflow_name):
        assert (ARCHITECT_WORKFLOWS_DIR / workflow_name).is_dir()

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_md_exists(self, workflow_name):
        assert (ARCHITECT_WORKFLOWS_DIR / workflow_name / "workflow.md").exists()

    def test_create_architecture_has_steps(self):
        steps_dir = ARCHITECT_WORKFLOWS_DIR / "create-architecture" / "steps"
        assert steps_dir.is_dir()
        step_files = list(steps_dir.glob("step-*.md"))
        assert len(step_files) >= 8

    def test_create_architecture_has_template(self):
        assert (ARCHITECT_WORKFLOWS_DIR / "create-architecture" / "architecture-decision-template.md").exists()

    def test_check_readiness_has_steps(self):
        steps_dir = ARCHITECT_WORKFLOWS_DIR / "check-implementation-readiness" / "steps"
        assert steps_dir.is_dir()
        step_files = list(steps_dir.glob("step-*.md"))
        assert len(step_files) >= 6

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_references_mm_config(self, workflow_name):
        content = (ARCHITECT_WORKFLOWS_DIR / workflow_name / "workflow.md").read_text()
        assert "_bmad/mm/config.yaml" in content
        assert "_bmad/bmm/config.yaml" not in content


class TestOogwayModuleHelp:
    """AC#3: Agent installation and invocation."""

    def test_module_help_has_oogway(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "oogway" in content.lower()
        assert "bmad-agent-mm-oogway" in content

    def test_module_help_has_create_architecture(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "Create Architecture" in content
        assert "_bmad/mm/workflows/architect/create-architecture/" in content

    def test_module_help_has_check_readiness(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "Check Implementation Readiness" in content
        assert "_bmad/mm/workflows/architect/check-implementation-readiness/" in content

    def test_party_roster_has_oogway(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "teams" / "default-party.csv"
        content = path.read_text()
        assert "oogway" in content.lower()
        assert "Migration Architect" in content
