"""Tests for MM dev workflow slash command registration — Story 3.7."""

from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLAUDE_COMMANDS_DIR = PROJECT_ROOT / ".claude" / "commands"

MM_DEV_WORKFLOW_COMMANDS = [
    ("bmad-mm-dev-story", "_bmad/mm/workflows/dev/dev-story/workflow.yaml"),
    ("bmad-mm-code-review", "_bmad/mm/workflows/dev/code-review/workflow.yaml"),
]

MM_DEV_COMMAND_NAMES = [cmd for cmd, _ in MM_DEV_WORKFLOW_COMMANDS]


# ---------------------------------------------------------------------------
# AC1 + AC2: Command files exist
# ---------------------------------------------------------------------------

class TestCommandFilesExist:
    """AC#1 + AC#2: Both MM dev workflow slash command files exist."""

    @pytest.mark.parametrize("cmd,_", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_file_exists(self, cmd, _):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        assert path.exists(), f"Missing Claude Code command: {path}"


# ---------------------------------------------------------------------------
# AC1 + AC2: Frontmatter validation
# ---------------------------------------------------------------------------

class TestCommandFrontmatter:
    """AC#1 + AC#2: Command files have valid frontmatter."""

    @pytest.mark.parametrize("cmd,_", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_has_name_frontmatter(self, cmd, _):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        content = path.read_text()
        assert "name:" in content, f"{cmd}: missing 'name:' in frontmatter"

    @pytest.mark.parametrize("cmd,_", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_has_description_frontmatter(self, cmd, _):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        content = path.read_text()
        assert "description:" in content, f"{cmd}: missing 'description:' in frontmatter"


# ---------------------------------------------------------------------------
# AC3: Correct MM workflow paths
# ---------------------------------------------------------------------------

class TestCommandWorkflowPaths:
    """AC#3: Commands reference correct MM workflow paths under _bmad/mm/workflows/dev/."""

    @pytest.mark.parametrize("cmd,workflow_path", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_references_correct_workflow_path(self, cmd, workflow_path):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        content = path.read_text()
        assert workflow_path in content, (
            f"{cmd}: missing workflow path reference '{workflow_path}'"
        )

    @pytest.mark.parametrize("cmd,_", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_references_workflow_xml_core_os(self, cmd, _):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        content = path.read_text()
        assert "_bmad/core/tasks/workflow.xml" in content, (
            f"{cmd}: missing reference to '_bmad/core/tasks/workflow.xml'"
        )


# ---------------------------------------------------------------------------
# AC1 + AC2: Activation block
# ---------------------------------------------------------------------------

class TestCommandActivationBlock:
    """AC#1 + AC#2: Commands have the <steps CRITICAL="TRUE"> activation block."""

    @pytest.mark.parametrize("cmd,_", MM_DEV_WORKFLOW_COMMANDS)
    def test_command_has_steps_critical_block(self, cmd, _):
        path = CLAUDE_COMMANDS_DIR / f"{cmd}.md"
        content = path.read_text()
        assert '<steps CRITICAL="TRUE">' in content, (
            f"{cmd}: missing '<steps CRITICAL=\"TRUE\">' activation block"
        )
