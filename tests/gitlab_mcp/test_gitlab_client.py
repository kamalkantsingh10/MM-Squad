"""Unit tests for GitlabClient — AC#1, #2, #3, #4, #5."""

import asyncio
from unittest.mock import MagicMock, patch

import gitlab.exceptions
import pytest

from tests.gitlab_mcp.fixtures.mock_gitlab import (
    make_api_error_gitlab,
    make_auth_error_gitlab,
    make_mock_epic,
    make_mock_gitlab,
    make_mock_group,
    make_mock_issue,
    make_mock_project,
)


@pytest.fixture(autouse=True)
def reset_client():
    """Reset GitlabClient singleton state between tests."""
    from gitlab_mcp.gitlab_client import client

    client._gl = None
    client._authenticated = False
    yield
    client._gl = None
    client._authenticated = False


class TestLazyInitialization:
    """AC#1: Client not created until first tool call."""

    def test_client_not_authenticated_at_import(self):
        from gitlab_mcp.gitlab_client import client

        assert client._gl is None
        assert client._authenticated is False

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_client_initializes_on_first_call(self, mock_gitlab_cls):
        mock_gitlab_cls.return_value = make_mock_gitlab()
        from gitlab_mcp.gitlab_client import client

        client._ensure_authenticated()
        assert client._gl is not None
        assert client._authenticated is True


class TestAuthentication:
    """AC#1: Successful authentication flow."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_successful_auth(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        from gitlab_mcp.gitlab_client import client

        client._ensure_authenticated()
        mock_gitlab_cls.assert_called_once()
        mock_gl.auth.assert_called_once()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_reads_gitlab_url_from_config(self, mock_gitlab_cls):
        mock_gitlab_cls.return_value = make_mock_gitlab()
        from gitlab_mcp.gitlab_client import client

        client._ensure_authenticated()
        call_kwargs = mock_gitlab_cls.call_args
        assert "url" in call_kwargs.kwargs or len(call_kwargs.args) > 0

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_auth_only_happens_once(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        from gitlab_mcp.gitlab_client import client

        client._ensure_authenticated()
        client._ensure_authenticated()
        mock_gitlab_cls.assert_called_once()
        mock_gl.auth.assert_called_once()


class TestMissingToken:
    """AC#2: Missing GITLAB_TOKEN error handling."""

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_token_raises_error(self):
        from gitlab_mcp.gitlab_client import client

        with pytest.raises(RuntimeError, match="GITLAB_TOKEN"):
            client._ensure_authenticated()

    @patch.dict("os.environ", {}, clear=True)
    def test_ping_returns_make_error_on_missing_token(self):
        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.ping())
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_AUTH_ERROR" for f in result["flags"])


class TestAsyncWrapping:
    """AC#3: Async event loop non-blocking calls."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    @patch("gitlab_mcp.gitlab_client.asyncio.to_thread")
    def test_ping_uses_asyncio_to_thread(self, mock_to_thread, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        mock_to_thread.return_value = ("17.5.0", "abc123")
        from gitlab_mcp.gitlab_client import client

        asyncio.run(client.ping())
        mock_to_thread.assert_called_once()


class TestGitLabApiErrors:
    """AC#4: GitLab API error handling."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_auth_error_returns_make_error(self, mock_gitlab_cls):
        mock_gitlab_cls.return_value = make_auth_error_gitlab()
        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.ping())
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_AUTH_ERROR" for f in result["flags"])

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_api_error_returns_make_error(self, mock_gitlab_cls):
        mock_gl = make_api_error_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.ping())
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_API_ERROR" for f in result["flags"])


class TestSuccessfulToolExecution:
    """AC#5: Successful tool returns make_result."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_ping_returns_make_result_on_success(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.ping())
        assert result["status"] == "ok"
        assert "gitlab_version" in result["data"]
        assert "gitlab_url" in result["data"]


class TestMilestoneManagement:
    """Story 2.2 AC#2: Milestone creation and idempotency."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_milestone_success(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_milestone(123, "Phase 1", "Discovery phase")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "created"
        assert result["data"]["milestone"] == "Phase 1"
        project.milestones.create.assert_called_once()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_milestone_idempotent(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_milestones=["Phase 1"])
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_milestone(123, "Phase 1", "Discovery phase")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "skipped"
        project.milestones.create.assert_not_called()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_milestone_with_dates(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_milestone(
                123, "Phase 1", "Desc",
                start_date="2026-01-01", due_date="2026-03-31",
            )
        )
        assert result["status"] == "ok"
        call_data = project.milestones.create.call_args[0][0]
        assert call_data["start_date"] == "2026-01-01"
        assert call_data["due_date"] == "2026-03-31"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_milestone_structure(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        phases = [
            {"title": "Phase 1", "description": "Discovery"},
            {"title": "Phase 2", "description": "Migration"},
        ]
        result = asyncio.run(
            client.create_milestone_structure(123, phases)
        )
        assert result["status"] == "ok"
        assert result["data"]["created_count"] == 2
        assert result["data"]["total"] == 2


class TestBoardManagement:
    """Story 2.2 AC#3: Board creation and idempotency."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_board_success(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_board(123, "Pipeline Stages")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "created"
        assert result["data"]["board"] == "Pipeline Stages"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_board_idempotent(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_boards=["Pipeline Stages"])
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_board(123, "Pipeline Stages")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "skipped"
        project.boards.create.assert_not_called()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_board_lists(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(
            existing_labels=["In-Analysis", "Awaiting-Review", "In-Migration", "Blocked", "Done"]
        )
        mock_gl.projects.get.return_value = project
        board = MagicMock()
        board.lists.list.return_value = []
        project.boards.get.return_value = board

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_board_lists(
                123, 888, ["In-Analysis", "Awaiting-Review", "In-Migration", "Blocked", "Done"]
            )
        )
        assert result["status"] == "ok"
        assert result["data"]["created_count"] == 5


class TestIssueManagement:
    """Story 2.3 AC#1: Issue CRUD."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_issue(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue()
        project.issues.create.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.create_issue(123, "PAYROLL-CALC", "Module desc", ["In-Analysis", "Complexity::High"])
        )
        assert result["status"] == "ok"
        assert result["data"]["iid"] == 1
        assert result["data"]["title"] == "PAYROLL-CALC"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_issue_with_labels(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue()
        project.issues.create.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        asyncio.run(
            client.create_issue(123, "PAYROLL-CALC", "", ["In-Analysis", "Complexity::High"])
        )
        call_data = project.issues.create.call_args[0][0]
        assert "In-Analysis" in call_data["labels"]
        assert "Complexity::High" in call_data["labels"]

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_get_issue(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue()
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.get_issue(123, 1))
        assert result["status"] == "ok"
        assert result["data"]["iid"] == 1

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_list_issues(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = [make_mock_issue(), make_mock_issue(iid=2, title="BATCH-JOB")]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.list_issues(123))
        assert result["status"] == "ok"
        assert result["data"]["count"] == 2


class TestLabelOperations:
    """Story 2.3 AC#2, #3, #4: Label apply/remove/transition."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_apply_label(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_labels=["Po-Analysis-Complete", "In-Analysis", "Complexity::High"])
        mock_issue = make_mock_issue(labels=["In-Analysis", "Complexity::High"])
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.apply_label(123, 1, "Po-Analysis-Complete"))
        assert result["status"] == "ok"
        assert result["data"]["action"] == "applied"
        mock_issue.save.assert_called_once()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_apply_label_already_present(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_labels=["In-Analysis"])
        mock_issue = make_mock_issue(labels=["In-Analysis"])
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.apply_label(123, 1, "In-Analysis"))
        assert result["status"] == "ok"
        assert result["data"]["action"] == "already_applied"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_apply_label_not_found(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_labels=[])
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.apply_label(123, 1, "NonExistent"))
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_LABEL_NOT_FOUND" for f in result["flags"])

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_remove_label(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue(labels=["In-Analysis", "Awaiting-Review"])
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.remove_label(123, 1, "Awaiting-Review"))
        assert result["status"] == "ok"
        assert result["data"]["action"] == "removed"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_transition_status(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_labels=["In-Analysis", "Awaiting-Review", "In-Migration"])
        mock_issue = make_mock_issue(labels=["In-Analysis", "Po-Analysis-Complete"])
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.transition_status(123, 1, "In-Analysis", "Awaiting-Review")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "transitioned"
        assert result["data"]["from_label"] == "In-Analysis"
        assert result["data"]["to_label"] == "Awaiting-Review"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_transition_status_invalid_target(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_labels=[])
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.transition_status(123, 1, "In-Analysis", "NonExistent")
        )
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_LABEL_NOT_FOUND" for f in result["flags"])


class TestMilestoneAssignment:
    """Story 2.4 AC#1, #2: Milestone assignment."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_assign_to_milestone(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue()
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.assign_to_milestone(123, 1, 999))
        assert result["status"] == "ok"
        assert result["data"]["action"] == "assigned"
        assert result["data"]["milestone_id"] == 999
        mock_issue.save.assert_called_once()

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_list_milestones(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(existing_milestones=["Sprint 1", "Sprint 2"])
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.list_milestones(123))
        assert result["status"] == "ok"
        assert result["data"]["count"] == 2

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_get_milestone(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        ms = MagicMock()
        ms.id = 999
        ms.title = "Sprint 1"
        ms.description = "First sprint"
        ms.state = "active"
        project.milestones.get.return_value = ms
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.get_milestone(123, 999))
        assert result["status"] == "ok"
        assert result["data"]["title"] == "Sprint 1"


class TestMilestoneBurndown:
    """Story 2.4 AC#3, #4: Burndown and complexity capacity."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_burndown_counts(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        ms = MagicMock()
        ms.id = 999
        ms.title = "Sprint 1"
        project.milestones.get.return_value = ms

        issues = [
            make_mock_issue(iid=1, labels=["Complexity::High"], state="opened"),
            make_mock_issue(iid=2, labels=["Complexity::Low"], state="closed"),
            make_mock_issue(iid=3, labels=["Complexity::Medium"], state="opened"),
        ]
        project.issues.list.return_value = issues
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.get_milestone_burndown(123, 999))
        assert result["status"] == "ok"
        assert result["data"]["total_issues"] == 3
        assert result["data"]["open_issues"] == 2
        assert result["data"]["closed_issues"] == 1

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_burndown_complexity_capacity(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        ms = MagicMock()
        ms.id = 999
        ms.title = "Sprint 1"
        project.milestones.get.return_value = ms

        issues = [
            make_mock_issue(iid=1, labels=["Complexity::High"], state="opened"),
            make_mock_issue(iid=2, labels=["Complexity::Low"], state="closed"),
            make_mock_issue(iid=3, labels=["Complexity::Medium"], state="opened"),
        ]
        project.issues.list.return_value = issues
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.get_milestone_burndown(123, 999))
        assert result["data"]["total_capacity"] == 6  # 3 + 1 + 2
        assert result["data"]["completed_capacity"] == 1  # Low closed
        assert result["data"]["remaining_capacity"] == 5

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_burndown_by_complexity(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        ms = MagicMock()
        ms.id = 999
        ms.title = "Sprint 1"
        project.milestones.get.return_value = ms

        issues = [
            make_mock_issue(iid=1, labels=["Complexity::High"], state="opened"),
            make_mock_issue(iid=2, labels=["Complexity::High"], state="closed"),
        ]
        project.issues.list.return_value = issues
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.get_milestone_burndown(123, 999))
        assert result["data"]["by_complexity"]["Complexity::High"]["total"] == 2
        assert result["data"]["by_complexity"]["Complexity::High"]["closed"] == 1


class TestCommentOperations:
    """Story 2.5 AC#1: Progress comments."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_add_comment(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_issue = make_mock_issue()
        note = MagicMock()
        note.id = 42
        mock_issue.notes.create.return_value = note
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.add_comment(123, 1, "Test comment"))
        assert result["status"] == "ok"
        assert result["data"]["note_id"] == 42

    def test_build_progress_comment_format(self):
        from gitlab_mcp.gitlab_client import GitlabClient

        comment = GitlabClient.build_progress_comment(
            agent_name="Po",
            stage="Po-Analysis-Complete",
            summary=["Call graph: 15 nodes", "Complexity: High"],
            flags=[{"code": "UNKNOWN_MACRO", "message": "XCALC not found"}],
        )
        assert "## Stage Completion: Po-Analysis-Complete" in comment
        assert "**Agent:** Po" in comment
        assert "Call graph: 15 nodes" in comment
        assert "UNKNOWN_MACRO: XCALC not found" in comment

    def test_build_progress_comment_iso_timestamp(self):
        from gitlab_mcp.gitlab_client import GitlabClient

        comment = GitlabClient.build_progress_comment(
            agent_name="Po", stage="Analysis", summary=["Done"]
        )
        # ISO 8601 has a T separator and timezone info
        assert "**Timestamp:** 20" in comment
        assert "T" in comment

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_build_milestone_summary(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        ms = MagicMock()
        ms.id = 999
        ms.title = "Sprint 1"
        project.milestones.get.return_value = ms
        project.issues.list.return_value = [
            make_mock_issue(iid=1, labels=["Complexity::High"], state="opened"),
            make_mock_issue(iid=2, labels=["Complexity::Low"], state="closed"),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.build_milestone_summary(123, 999))
        assert result["status"] == "ok"
        md = result["data"]["markdown"]
        assert "## Sprint Summary: Sprint 1" in md
        assert "Completed: 1" in md
        assert "Outstanding: 1" in md


class TestEpicOperations:
    """Story 2.6: Epic CRUD."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_create_epic(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        group = make_mock_group()
        mock_gl.groups.get.return_value = group

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.create_epic(10, "Core Payroll", "Payroll subsystem"))
        assert result["status"] == "ok"
        assert result["data"]["title"] == "Core Payroll"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_close_epic(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        group = make_mock_group()
        mock_gl.groups.get.return_value = group

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.close_epic(10, 1))
        assert result["status"] == "ok"
        assert result["data"]["action"] == "closed"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_validate_epic_closure_all_complete(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.get.side_effect = [
            make_mock_issue(iid=1, labels=["QA-Complete"]),
            make_mock_issue(iid=2, labels=["QA-Complete"]),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.validate_epic_closure(123, [1, 2]))
        assert result["status"] == "ok"
        assert result["data"]["all_complete"] is True
        assert result["data"]["complete_count"] == 2

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_validate_epic_closure_incomplete(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.get.side_effect = [
            make_mock_issue(iid=1, labels=["QA-Complete"]),
            make_mock_issue(iid=2, title="BATCH-JOB", labels=["In-Migration"]),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(client.validate_epic_closure(123, [1, 2]))
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_EPIC_INCOMPLETE" for f in result["flags"])


class TestSignOffWorkflows:
    """Story 2.6 AC#1, #2: Sign-off operations."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_sign_off_module(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project(
            existing_labels=["Awaiting-Review", "In-Migration", "In-Analysis"]
        )
        mock_issue = make_mock_issue(labels=["Awaiting-Review", "Complexity::High"])
        project.issues.get.return_value = mock_issue
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.sign_off_module(123, 1, "Claire", "In-Migration")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "signed_off"
        assert result["data"]["validator"] == "Claire"
        assert result["data"]["new_status"] == "In-Migration"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_sign_off_epic_success(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.get.side_effect = [
            make_mock_issue(iid=1, labels=["QA-Complete"]),
            make_mock_issue(iid=2, labels=["QA-Complete"]),
        ]
        mock_gl.projects.get.return_value = project
        group = make_mock_group()
        mock_gl.groups.get.return_value = group

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.sign_off_epic(10, 1, 123, [1, 2], "Mantis")
        )
        assert result["status"] == "ok"
        assert result["data"]["action"] == "epic_signed_off_and_closed"
        assert result["data"]["modules_count"] == 2

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_sign_off_epic_rejected_incomplete(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.get.side_effect = [
            make_mock_issue(iid=1, labels=["QA-Complete"]),
            make_mock_issue(iid=2, labels=["In-Migration"]),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        result = asyncio.run(
            client.sign_off_epic(10, 1, 123, [1, 2], "Mantis")
        )
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_EPIC_INCOMPLETE" for f in result["flags"])
