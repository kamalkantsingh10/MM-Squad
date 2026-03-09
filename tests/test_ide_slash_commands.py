"""Tests for IDE slash command registration — Story 2.8."""

from pathlib import Path
import re
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MM_AGENTS = ["shifu", "tigress", "viper", "monkey", "mantis", "oogway"]

CLAUDE_COMMANDS_DIR = PROJECT_ROOT / ".claude" / "commands"
GITHUB_AGENTS_DIR = PROJECT_ROOT / ".github" / "agents"


# ---------------------------------------------------------------------------
# AC1: Claude Code slash commands — all MM agents
# ---------------------------------------------------------------------------

class TestClaudeCodeCommands:
    """AC#1: All 6 MM agents are registered as Claude Code slash commands."""

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_command_file_exists(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        assert path.exists(), f"Missing Claude Code command: {path}"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_command_has_name_frontmatter(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        content = path.read_text()
        assert "name:" in content, f"{agent}: missing 'name:' in frontmatter"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_command_has_description_frontmatter(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        content = path.read_text()
        assert "description:" in content, f"{agent}: missing 'description:' in frontmatter"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_command_references_correct_agent_path(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        content = path.read_text()
        expected = f"_bmad/mm/agents/{agent}.md"
        assert expected in content, f"{agent}: missing agent path reference '{expected}'"


# ---------------------------------------------------------------------------
# AC2: GitHub Copilot agent files — all MM agents
# ---------------------------------------------------------------------------

class TestGitHubCopilotAgents:
    """AC#2: All 6 MM agents are registered as GitHub Copilot agents."""

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_file_exists(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        assert path.exists(), f"Missing Copilot agent file: {path}"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_has_description_frontmatter(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        content = path.read_text()
        assert "description:" in content, f"{agent}: missing 'description:' in frontmatter"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_has_tools_frontmatter(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        content = path.read_text()
        assert "tools:" in content, f"{agent}: missing 'tools:' in frontmatter"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_references_correct_agent_path(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        content = path.read_text()
        expected = f"_bmad/mm/agents/{agent}.md"
        assert expected in content, f"{agent}: missing agent path reference '{expected}'"


# ---------------------------------------------------------------------------
# AC3: Consistent activation across both IDEs
# ---------------------------------------------------------------------------

class TestConsistentActivation:
    """AC#3: Activation instructions are identical in both IDEs."""

    ACTIVATION_KEYWORDS = [
        "LOAD the FULL agent file",
        "READ its entire contents",
        "FOLLOW every step",
        "DISPLAY the welcome",
        "PRESENT the numbered menu",
        "WAIT for user input",
    ]

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_claude_command_has_activation_block(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        content = path.read_text()
        assert "agent-activation" in content, f"{agent}: missing agent-activation block"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_has_activation_block(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        content = path.read_text()
        assert "agent-activation" in content, f"{agent}: missing agent-activation block"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_claude_activation_keywords(self, agent):
        path = CLAUDE_COMMANDS_DIR / f"bmad-agent-mm-{agent}.md"
        content = path.read_text()
        for keyword in self.ACTIVATION_KEYWORDS:
            assert keyword in content, f"{agent} Claude command missing activation keyword: '{keyword}'"

    @pytest.mark.parametrize("agent", MM_AGENTS)
    def test_copilot_activation_keywords(self, agent):
        path = GITHUB_AGENTS_DIR / f"bmad-agent-mm-{agent}.agent.md"
        content = path.read_text()
        for keyword in self.ACTIVATION_KEYWORDS:
            assert keyword in content, f"{agent} Copilot file missing activation keyword: '{keyword}'"
