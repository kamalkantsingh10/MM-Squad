"""Mock GitLab API responses for testing."""

from unittest.mock import MagicMock

import gitlab.exceptions


def make_mock_gitlab(version=("17.5.0", "abc123")):
    """Create a mock gitlab.Gitlab instance with standard responses."""
    mock_gl = MagicMock()
    mock_gl.version.return_value = version
    mock_gl.auth.return_value = None
    mock_gl.user = MagicMock()
    mock_gl.user.username = "test-user"
    mock_gl.url = "https://gitlab.example.com"
    return mock_gl


def make_auth_error_gitlab():
    """Create a mock that raises GitlabAuthenticationError on auth()."""
    mock_gl = MagicMock()
    mock_gl.auth.side_effect = gitlab.exceptions.GitlabAuthenticationError(
        "401 Unauthorized"
    )
    return mock_gl


def make_api_error_gitlab():
    """Create a mock that raises GitlabGetError on version()."""
    mock_gl = MagicMock()
    mock_gl.auth.return_value = None
    mock_gl.user = MagicMock()
    mock_gl.version.side_effect = gitlab.exceptions.GitlabGetError(
        "500 Internal Server Error"
    )
    return mock_gl


def make_mock_project(
    existing_labels=None,
    existing_milestones=None,
    existing_boards=None,
):
    """Create a mock GitLab project with configurable existing resources."""
    project = MagicMock()

    # Labels
    mock_labels = []
    for name in (existing_labels or []):
        label = MagicMock()
        label.name = name
        label.id = hash(name) % 10000
        mock_labels.append(label)
    project.labels.list.return_value = mock_labels
    project.labels.create.return_value = MagicMock()

    # Milestones
    mock_milestones = []
    for title in (existing_milestones or []):
        ms = MagicMock()
        ms.title = title
        ms.id = hash(title) % 10000
        mock_milestones.append(ms)
    project.milestones.list.return_value = mock_milestones
    new_ms = MagicMock()
    new_ms.id = 999
    project.milestones.create.return_value = new_ms

    # Boards
    mock_boards = []
    for name in (existing_boards or []):
        board = MagicMock()
        board.name = name
        board.id = hash(name) % 10000
        board.lists.list.return_value = []
        mock_boards.append(board)
    project.boards.list.return_value = mock_boards
    new_board = MagicMock()
    new_board.id = 888
    new_board.name = "Pipeline Stages"
    new_board.lists.list.return_value = []
    project.boards.create.return_value = new_board
    project.boards.get.return_value = new_board

    return project


def make_mock_issue(iid=1, title="PAYROLL-CALC", labels=None, state="opened"):
    """Create a mock GitLab Issue."""
    issue = MagicMock()
    issue.iid = iid
    issue.title = title
    issue.labels = labels or ["In-Analysis", "Complexity::High"]
    issue.state = state
    issue.web_url = f"https://gitlab.example.com/issues/{iid}"
    issue.save.return_value = None
    note = MagicMock()
    note.id = 100 + iid
    issue.notes.create.return_value = note
    return issue


def make_mock_epic(iid=1, title="Core Payroll", state="opened"):
    """Create a mock GitLab Epic."""
    epic = MagicMock()
    epic.iid = iid
    epic.title = title
    epic.state = state
    epic.description = f"Epic: {title}"
    epic.web_url = f"https://gitlab.example.com/epics/{iid}"
    epic.save.return_value = None
    return epic


def make_mock_group(existing_epics=None):
    """Create a mock GitLab Group with epic management."""
    group = MagicMock()
    mock_epics = []
    for title in (existing_epics or []):
        mock_epics.append(make_mock_epic(title=title))
    group.epics.list.return_value = mock_epics
    new_epic = make_mock_epic()
    group.epics.create.return_value = new_epic
    group.epics.get.return_value = new_epic
    return group
