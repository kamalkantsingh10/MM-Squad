"""GitLab MCP Server — project management and delivery orchestration."""

from pathlib import Path

from fastmcp import FastMCP
from shared.config_loader import load_server_config, load_server_env, setup_logging

_SERVER_DIR = Path(__file__).parent
load_server_env(_SERVER_DIR)

from gitlab_mcp import gitlab_client
from gitlab_mcp.label_manager import LabelManager, STATUS_LABELS
from gitlab_mcp.readme_updater import ReadmeUpdater

logger = setup_logging("gitlab-mcp", _SERVER_DIR)
config = load_server_config(_SERVER_DIR)

mcp = FastMCP("gitlab-mcp")

_default_project_id: int | None = config.get("project_id")
_default_group_id: int | None = config.get("group_id")

_label_manager = LabelManager(gitlab_client.client)
_readme_updater = ReadmeUpdater(gitlab_client.client)


def _resolve_project_id(project_id: int | None) -> int:
    """Return explicit project_id or fall back to config default."""
    pid = project_id if project_id is not None else _default_project_id
    if pid is None:
        raise ValueError("project_id not provided and not set in config.yaml")
    return pid


def _resolve_group_id(group_id: int | None) -> int:
    """Return explicit group_id or fall back to config default."""
    gid = group_id if group_id is not None else _default_group_id
    if gid is None:
        raise ValueError("group_id not provided and not set in config.yaml")
    return gid


@mcp.tool()
async def ping_gitlab() -> dict:
    """Check GitLab connectivity and return version info."""
    return await gitlab_client.client.ping()


@mcp.tool()
async def create_labels(project_id: int | None = None) -> dict:
    """Create the standard label taxonomy for a GitLab project."""
    return await _label_manager.create_label_taxonomy(_resolve_project_id(project_id))


@mcp.tool()
async def create_milestone(
    title: str,
    description: str = "",
    project_id: int | None = None,
    start_date: str | None = None,
    due_date: str | None = None,
) -> dict:
    """Create a milestone in a GitLab project."""
    return await gitlab_client.client.create_milestone(
        _resolve_project_id(project_id), title, description, start_date, due_date
    )


@mcp.tool()
async def create_board(board_name: str, project_id: int | None = None) -> dict:
    """Create an issue board in a GitLab project."""
    return await gitlab_client.client.create_board(_resolve_project_id(project_id), board_name)


@mcp.tool()
async def init_project(project_id: int | None = None, phases: list[dict] | None = None) -> dict:
    """Initialise a GitLab project with labels, milestones, and board."""
    project_id = _resolve_project_id(project_id)
    try:
        # Phase 1: Labels
        label_result = await _label_manager.create_label_taxonomy(project_id)
        if label_result["status"] == "error":
            return label_result

        # Phase 2: Milestones (if phases provided)
        milestone_result = None
        if phases:
            milestone_result = await gitlab_client.client.create_milestone_structure(
                project_id, phases
            )
            if milestone_result["status"] == "error":
                return milestone_result

        # Phase 3: Board with status label columns
        board_result = await gitlab_client.client.create_board(
            project_id, "Pipeline Stages"
        )
        if board_result["status"] == "error":
            return board_result

        board_id = board_result["data"]["id"]
        status_label_names = [label["name"] for label in STATUS_LABELS]
        lists_result = await gitlab_client.client.create_board_lists(
            project_id, board_id, status_label_names
        )

        from gitlab_mcp.result import make_result
        return make_result(
            data={
                "labels": label_result["data"],
                "milestones": milestone_result["data"] if milestone_result else None,
                "board": board_result["data"],
                "board_lists": lists_result["data"],
            }
        )
    except Exception as e:
        from gitlab_mcp.result import make_error
        logger.error("Init project error: %s", e)
        return make_error(
            f"Project initialisation failed: {e}",
            flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
        )


@mcp.tool()
async def create_issue(
    title: str,
    description: str = "",
    labels: list[str] | None = None,
    project_id: int | None = None,
) -> dict:
    """Create a GitLab Issue for a COBOL module."""
    return await gitlab_client.client.create_issue(
        _resolve_project_id(project_id), title, description, labels
    )


@mcp.tool()
async def apply_label(
    issue_iid: int, label_name: str, project_id: int | None = None
) -> dict:
    """Apply a label to a GitLab Issue."""
    return await gitlab_client.client.apply_label(
        _resolve_project_id(project_id), issue_iid, label_name
    )


@mcp.tool()
async def remove_label(
    issue_iid: int, label_name: str, project_id: int | None = None
) -> dict:
    """Remove a label from a GitLab Issue."""
    return await gitlab_client.client.remove_label(
        _resolve_project_id(project_id), issue_iid, label_name
    )


@mcp.tool()
async def update_issue_status(
    issue_iid: int, new_status: str, project_id: int | None = None
) -> dict:
    """Transition an Issue's status label (removes old status, applies new one)."""
    project_id = _resolve_project_id(project_id)
    from gitlab_mcp.label_manager import STATUS_LABELS

    status_names = [l["name"] for l in STATUS_LABELS]
    if new_status not in status_names:
        from gitlab_mcp.result import make_error
        return make_error(
            f"Invalid status '{new_status}'. Must be one of: {status_names}",
            flags=[{"code": "GITLAB_LABEL_NOT_FOUND", "message": f"Invalid status: {new_status}"}],
        )

    # Find current status label on the issue
    issue_result = await gitlab_client.client.get_issue(project_id, issue_iid)
    if issue_result["status"] == "error":
        return issue_result

    current_labels = issue_result["data"]["labels"]
    current_status = None
    for label in current_labels:
        if label in status_names:
            current_status = label
            break

    if current_status == new_status:
        from gitlab_mcp.result import make_result
        return make_result(
            data={"iid": issue_iid, "status": new_status, "action": "already_set"},
            message=f"Issue already has status '{new_status}'",
        )

    return await gitlab_client.client.transition_status(
        project_id, issue_iid,
        from_label=current_status or "",
        to_label=new_status,
    )


@mcp.tool()
async def assign_to_milestone(
    issue_iid: int, milestone_id: int, project_id: int | None = None
) -> dict:
    """Assign a GitLab Issue to a milestone."""
    return await gitlab_client.client.assign_to_milestone(
        _resolve_project_id(project_id), issue_iid, milestone_id
    )


@mcp.tool()
async def get_milestone_burndown(milestone_id: int, project_id: int | None = None) -> dict:
    """Get burndown data for a milestone — open/closed counts and complexity breakdown."""
    return await gitlab_client.client.get_milestone_burndown(
        _resolve_project_id(project_id), milestone_id
    )


@mcp.tool()
async def add_comment(issue_iid: int, body: str, project_id: int | None = None) -> dict:
    """Post a markdown comment to a GitLab Issue."""
    return await gitlab_client.client.add_comment(_resolve_project_id(project_id), issue_iid, body)


@mcp.tool()
async def update_readme(project_id: int | None = None) -> dict:
    """Regenerate and push the modernisation dashboard to the project README."""
    return await _readme_updater.update_readme(_resolve_project_id(project_id))


@mcp.tool()
async def list_milestones(
    state: str = "active", project_id: int | None = None
) -> dict:
    """List milestones in a GitLab project. State: 'active', 'closed', or 'all'."""
    return await gitlab_client.client.list_milestones(
        _resolve_project_id(project_id), state
    )


@mcp.tool()
async def create_epic(epic_name: str, color: str | None = None, project_id: int | None = None) -> dict:
    """Create an Epic:: scoped label to group issues by subsystem (e.g. 'Account-Subsystem' creates 'Epic::Account-Subsystem')."""
    return await gitlab_client.client.create_epic_label(
        _resolve_project_id(project_id), epic_name, color
    )


@mcp.tool()
async def list_epics(project_id: int | None = None) -> dict:
    """List all Epic:: scoped labels in the project."""
    return await gitlab_client.client.list_epic_labels(
        _resolve_project_id(project_id)
    )


@mcp.tool()
async def close_epic(
    epic_name: str,
    project_id: int | None = None,
    qa_name: str = "QA",
) -> dict:
    """Validate all issues with an Epic:: label are QA-Complete, post summary, and close them."""
    return await gitlab_client.client.close_epic_label(
        _resolve_project_id(project_id), epic_name, qa_name
    )


@mcp.tool()
async def list_issues(
    state: str = "opened",
    labels: list[str] | None = None,
    milestone: str | None = None,
    project_id: int | None = None,
) -> dict:
    """List issues in a GitLab project with optional filters."""
    return await gitlab_client.client.list_issues(
        _resolve_project_id(project_id), state=state, labels=labels, milestone=milestone
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
