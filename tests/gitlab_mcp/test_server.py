"""Tool-level tests for server.py — AC#1, #4, #5, #6."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from tests.gitlab_mcp.fixtures.mock_gitlab import make_mock_gitlab, make_mock_project


@pytest.fixture(autouse=True)
def reset_client():
    """Reset GitlabClient singleton state between tests."""
    from gitlab_mcp.gitlab_client import client

    client._gl = None
    client._authenticated = False
    yield
    client._gl = None
    client._authenticated = False


class TestPingGitlabTool:
    """AC#1, #5: ping_gitlab tool returns correct result format."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_ping_returns_ok_status(self, mock_gitlab_cls):
        mock_gitlab_cls.return_value = make_mock_gitlab()
        from gitlab_mcp.server import ping_gitlab

        result = asyncio.run(ping_gitlab())
        assert result["status"] == "ok"

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_ping_returns_version_data(self, mock_gitlab_cls):
        mock_gitlab_cls.return_value = make_mock_gitlab(version=("17.5.0", "rev"))
        from gitlab_mcp.server import ping_gitlab

        result = asyncio.run(ping_gitlab())
        assert result["data"]["gitlab_version"] == "17.5.0"
        assert result["data"]["gitlab_url"] == "https://gitlab.example.com"

    @patch.dict("os.environ", {}, clear=True)
    def test_ping_returns_error_without_token(self):
        from gitlab_mcp.server import ping_gitlab

        result = asyncio.run(ping_gitlab())
        assert result["status"] == "error"
        assert any(f["code"] == "GITLAB_AUTH_ERROR" for f in result["flags"])


class TestServerStructure:
    """AC#6: Package architecture & code structure."""

    def test_server_imports_gitlab_client(self):
        from gitlab_mcp import server

        assert hasattr(server, "gitlab_client")

    def test_server_has_mcp_instance(self):
        from gitlab_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "gitlab-mcp"

    def test_server_is_thin_wrapper(self):
        """server.py should only have tool registrations, not business logic."""
        import inspect

        from gitlab_mcp import server

        source = inspect.getsource(server)
        # Should NOT contain direct python-gitlab imports or gitlab.Gitlab calls
        assert "import gitlab\n" not in source
        assert "from gitlab import" not in source
        assert "gitlab.Gitlab(" not in source

    def test_ping_gitlab_is_registered(self):
        from gitlab_mcp.server import ping_gitlab

        assert callable(ping_gitlab)


class TestInitProjectTool:
    """Story 2.2: init_project orchestrates labels + milestones + board."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_init_project_orchestration(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.server import init_project

        result = asyncio.run(init_project(123))
        assert result["status"] == "ok"
        assert "labels" in result["data"]
        assert "board" in result["data"]
        assert "board_lists" in result["data"]

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_init_project_with_phases(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.server import init_project

        phases = [{"title": "Phase 1", "description": "Discovery"}]
        result = asyncio.run(init_project(123, phases=phases))
        assert result["status"] == "ok"
        assert result["data"]["milestones"] is not None
