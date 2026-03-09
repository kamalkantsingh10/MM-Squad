"""Unit tests for ReadmeUpdater — AC#2, AC#3."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from tests.gitlab_mcp.fixtures.mock_gitlab import make_mock_gitlab, make_mock_issue, make_mock_project


@pytest.fixture(autouse=True)
def reset_client():
    from gitlab_mcp.gitlab_client import client

    client._gl = None
    client._authenticated = False
    yield
    client._gl = None
    client._authenticated = False


class TestGenerateDashboard:
    """AC#3: Dashboard generation."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_dashboard_has_header(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = []
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.readme_updater import ReadmeUpdater

        updater = ReadmeUpdater(client)
        result = asyncio.run(updater.generate_dashboard(123))
        assert result["status"] == "ok"
        assert "# Modernisation Dashboard" in result["data"]["markdown"]

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_dashboard_has_table(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = [
            make_mock_issue(title="PAYROLL-CALC", labels=["Complexity::High", "In-Analysis"]),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.readme_updater import ReadmeUpdater

        updater = ReadmeUpdater(client)
        result = asyncio.run(updater.generate_dashboard(123))
        md = result["data"]["markdown"]
        assert "PAYROLL-CALC" in md
        assert "High" in md
        assert "| Module |" in md

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_dashboard_has_summary(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = [
            make_mock_issue(iid=1, labels=["Complexity::High", "In-Analysis"]),
            make_mock_issue(iid=2, labels=["Complexity::Low", "Done"]),
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.readme_updater import ReadmeUpdater

        updater = ReadmeUpdater(client)
        result = asyncio.run(updater.generate_dashboard(123))
        md = result["data"]["markdown"]
        assert "## Summary" in md
        assert "Total Modules | 2" in md

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_dashboard_has_footer(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = []
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.readme_updater import ReadmeUpdater

        updater = ReadmeUpdater(client)
        result = asyncio.run(updater.generate_dashboard(123))
        md = result["data"]["markdown"]
        assert "Last updated:" in md
        assert "Shifu" in md

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_dashboard_issue_count(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = make_mock_project()
        project.issues.list.return_value = [
            make_mock_issue(iid=1), make_mock_issue(iid=2), make_mock_issue(iid=3)
        ]
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.readme_updater import ReadmeUpdater

        updater = ReadmeUpdater(client)
        result = asyncio.run(updater.generate_dashboard(123))
        assert result["data"]["issue_count"] == 3
