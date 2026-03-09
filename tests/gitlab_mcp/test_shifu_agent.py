"""Tests for Shifu agent definition and workflow files — Story 2.7."""

from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "agents"
WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "pm"

EXPECTED_WORKFLOWS = [
    "create-epics-and-stories",
    "sprint-planning",
    "create-story",
    "sprint-status",
    "correct-course",
    "retrospective",
]

GITLAB_MCP_TOOLS = [
    "init_project",
    "create_epic",
    "create_issue",
    "apply_label",
    "remove_label",
    "create_labels",
    "create_milestone",
    "assign_to_milestone",
    "get_milestone_burndown",
    "add_comment",
    "update_readme",
]


class TestShifuAgentFile:
    """AC#1: Shifu agent definition."""

    def test_agent_file_exists(self):
        assert (AGENTS_DIR / "shifu.md").exists()

    def test_agent_has_persona(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        assert "<persona>" in content
        assert "PM + SM" in content

    def test_agent_has_menu(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        assert "<menu>" in content

    def test_agent_has_activation(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        assert "<activation" in content

    def test_agent_declares_gitlab_mcp(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        assert "gitlab-mcp" in content

    def test_agent_has_all_workflow_menu_items(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        for workflow in EXPECTED_WORKFLOWS:
            assert workflow in content, f"Missing workflow reference: {workflow}"

    def test_agent_has_standard_menu_items(self):
        content = (AGENTS_DIR / "shifu.md").read_text()
        assert "[MH]" in content
        assert "[CH]" in content
        assert "[DA]" in content


class TestWorkflowDirectories:
    """AC#2: Workflow step files."""

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_directory_exists(self, workflow_name):
        assert (WORKFLOWS_DIR / workflow_name).is_dir()

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_yaml_exists(self, workflow_name):
        assert (WORKFLOWS_DIR / workflow_name / "workflow.yaml").exists()

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_yaml_valid(self, workflow_name):
        path = WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "name" in data
        assert "steps" in data

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_references_mcp_tools(self, workflow_name):
        path = WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        if "mcp_tools" in data:
            for tool in data["mcp_tools"]:
                assert tool in GITLAB_MCP_TOOLS, f"Unknown tool: {tool}"


class TestModuleHelpCsv:
    """AC#3: module-help.csv entries."""

    def test_shifu_agent_entry(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "shifu" in content.lower()
        assert "bmad-agent-mm-shifu" in content

    def test_workflow_entries(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        for workflow in EXPECTED_WORKFLOWS:
            assert workflow in content, f"Missing workflow in module-help.csv: {workflow}"
