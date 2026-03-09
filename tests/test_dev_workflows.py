"""Tests for dev agent workflows — Story 3.1."""

from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEV_WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "dev"
MM_CONFIG_PATH = "_bmad/mm/config.yaml"

EXPECTED_WORKFLOWS = [
    "dev-story",
    "code-review",
]

REQUIRED_YAML_KEYS = ["name", "config_source", "installed_path", "instructions"]


class TestDevWorkflowDirectories:
    """AC#1: Dev workflows present in MM module."""

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_directory_exists(self, workflow_name):
        assert (DEV_WORKFLOWS_DIR / workflow_name).is_dir()

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_yaml_exists(self, workflow_name):
        assert (DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml").exists()

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_instructions_entry_point_exists(self, workflow_name):
        """After step-file refactor (story 3.8), instructions points to steps/step-01-*.md."""
        yaml_path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(yaml_path) as f:
            import yaml as _yaml
            data = _yaml.safe_load(f)
        instructions = data.get("instructions", "")
        assert "steps/step-" in instructions, (
            f"{workflow_name}: instructions must point to a step file after refactor"
        )

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_checklist_file_exists(self, workflow_name):
        assert (DEV_WORKFLOWS_DIR / workflow_name / "checklist.md").exists()


class TestWorkflowYamlContent:
    """AC#2: Workflows adapted for MM context."""

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_yaml_valid(self, workflow_name):
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        for key in REQUIRED_YAML_KEYS:
            assert key in data, f"Missing required key: {key}"

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_config_source_points_to_mm(self, workflow_name):
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "_bmad/mm/config.yaml" in data["config_source"]
        assert "_bmad/bmm/" not in data["config_source"]

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_installed_path_points_to_mm(self, workflow_name):
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "_bmad/mm/workflows/dev/" in data["installed_path"]
        assert "_bmad/bmm/" not in data["installed_path"]

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_workflow_declares_gitlab_mcp(self, workflow_name):
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "mcp_tools" in data
        assert "apply_label" in data["mcp_tools"]
        assert "add_comment" in data["mcp_tools"]

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_no_specdb_mcp_in_tools(self, workflow_name):
        """specdb-mcp must not appear in mcp_tools — comments excluding it are fine."""
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        mcp_tools = data.get("mcp_tools", [])
        assert "specdb-mcp" not in mcp_tools

    @pytest.mark.parametrize("workflow_name", EXPECTED_WORKFLOWS)
    def test_references_po_output_documents(self, workflow_name):
        path = DEV_WORKFLOWS_DIR / workflow_name / "workflow.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert "input_file_patterns" in data
        patterns = data["input_file_patterns"]
        has_business_rules = "business_rules" in patterns
        has_architecture = "architecture" in patterns
        assert has_business_rules or has_architecture, "Must reference Po's output documents or architecture"


class TestModuleHelpCsvDevEntries:
    """AC#3: module-help.csv entries reference correct paths."""

    def test_dev_story_entry_exists(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "Dev Story" in content
        assert "_bmad/mm/workflows/dev/dev-story/workflow.yaml" in content

    def test_code_review_entry_exists(self):
        path = PROJECT_ROOT / "_bmad" / "mm" / "module-help.csv"
        content = path.read_text()
        assert "Code Review" in content
        assert "_bmad/mm/workflows/dev/code-review/workflow.yaml" in content
