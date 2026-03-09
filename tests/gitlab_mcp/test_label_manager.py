"""Unit tests for LabelManager — AC#1, AC#4."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from tests.gitlab_mcp.fixtures.mock_gitlab import make_mock_gitlab


@pytest.fixture(autouse=True)
def reset_client():
    from gitlab_mcp.gitlab_client import client

    client._gl = None
    client._authenticated = False
    yield
    client._gl = None
    client._authenticated = False


def _make_mock_project(existing_labels=None):
    """Create a mock project with label management."""
    project = MagicMock()
    if existing_labels is None:
        existing_labels = []
    mock_labels = []
    for name in existing_labels:
        label = MagicMock()
        label.name = name
        mock_labels.append(label)
    project.labels.list.return_value = mock_labels
    project.labels.create.return_value = MagicMock()
    return project


class TestCreateLabelTaxonomy:
    """AC#1: Create all 12 standard labels."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_creates_all_12_labels_on_empty_project(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        assert result["status"] == "ok"
        assert result["data"]["created_count"] == 12
        assert result["data"]["skipped_count"] == 0
        assert result["data"]["total"] == 12
        assert project.labels.create.call_count == 12

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_creates_correct_label_names(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import ALL_LABELS, LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        expected_names = [label["name"] for label in ALL_LABELS]
        assert result["data"]["created"] == expected_names

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_has_pipeline_stage_labels(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        created = result["data"]["created"]
        for name in ["Po-Analysis-Complete", "Architecture-Complete", "Code-Generated", "QA-Complete"]:
            assert name in created

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_has_complexity_labels(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        created = result["data"]["created"]
        for name in ["Complexity::Low", "Complexity::Medium", "Complexity::High"]:
            assert name in created

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_has_status_labels(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project()
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        created = result["data"]["created"]
        for name in ["In-Analysis", "Awaiting-Review", "In-Migration", "Blocked", "Done"]:
            assert name in created


class TestLabelIdempotency:
    """AC#4: Re-initialization doesn't duplicate labels."""

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_skips_existing_labels(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl
        project = _make_mock_project(
            existing_labels=["Po-Analysis-Complete", "Complexity::Low", "Done"]
        )
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client
        from gitlab_mcp.label_manager import LabelManager

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        assert result["status"] == "ok"
        assert result["data"]["created_count"] == 9
        assert result["data"]["skipped_count"] == 3
        assert "Po-Analysis-Complete" in result["data"]["skipped"]
        assert project.labels.create.call_count == 9

    @patch.dict("os.environ", {"GITLAB_TOKEN": "test-token"})
    @patch("gitlab_mcp.gitlab_client.gitlab.Gitlab")
    def test_all_existing_skips_all(self, mock_gitlab_cls):
        mock_gl = make_mock_gitlab()
        mock_gitlab_cls.return_value = mock_gl

        from gitlab_mcp.label_manager import ALL_LABELS, LabelManager

        all_names = [label["name"] for label in ALL_LABELS]
        project = _make_mock_project(existing_labels=all_names)
        mock_gl.projects.get.return_value = project

        from gitlab_mcp.gitlab_client import client

        manager = LabelManager(client)
        result = asyncio.run(manager.create_label_taxonomy(123))

        assert result["status"] == "ok"
        assert result["data"]["created_count"] == 0
        assert result["data"]["skipped_count"] == 12
        assert project.labels.create.call_count == 0
