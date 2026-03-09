"""GitLab API client wrapper — all python-gitlab call logic lives here."""

import asyncio
import datetime
import logging
import os

import gitlab
import gitlab.exceptions

from gitlab_mcp.result import make_error, make_result
from pathlib import Path

from shared.config_loader import load_server_config

logger = logging.getLogger("gitlab-mcp")


class GitlabClient:
    """Lazy-authenticated wrapper around python-gitlab."""

    def __init__(self) -> None:
        self._gl: gitlab.Gitlab | None = None
        self._authenticated: bool = False

    def _ensure_authenticated(self) -> None:
        """Initialize and authenticate GitLab client on first call.

        Raises RuntimeError if GITLAB_TOKEN is not set.
        Raises gitlab.exceptions.GitlabAuthenticationError on auth failure.
        """
        if self._authenticated:
            return

        token = os.environ.get("GITLAB_TOKEN")
        if not token:
            raise RuntimeError("GITLAB_TOKEN environment variable not set")

        config = load_server_config(Path(__file__).parent)
        gitlab_url = config.get("gitlab_url", "https://gitlab.com")

        self._gl = gitlab.Gitlab(url=gitlab_url, private_token=token)
        self._gl.auth()
        self._authenticated = True
        logger.info("GitLab client initialized — connected to %s", gitlab_url)

    async def ping(self) -> dict:
        """Check GitLab connectivity and return version info."""
        try:
            self._ensure_authenticated()
            version_tuple = await asyncio.to_thread(self._gl.version)
            return make_result(
                data={
                    "gitlab_version": version_tuple[0],
                    "gitlab_url": self._gl.url,
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabAuthenticationError as e:
            logger.error("GitLab authentication failed: %s", e)
            return make_error(
                f"GitLab authentication failed: {e}",
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


    async def create_milestone(
        self,
        project_id: int,
        title: str,
        description: str = "",
        start_date: str | None = None,
        due_date: str | None = None,
    ) -> dict:
        """Create a single milestone. Idempotent — skips if title exists."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            existing = await asyncio.to_thread(
                project.milestones.list, get_all=True
            )
            for ms in existing:
                if ms.title == title:
                    logger.info("Milestone already exists, skipping: %s", title)
                    return make_result(
                        data={"milestone": title, "action": "skipped"},
                        message=f"Milestone '{title}' already exists",
                    )

            data = {"title": title, "description": description}
            if start_date:
                data["start_date"] = start_date
            if due_date:
                data["due_date"] = due_date

            ms = await asyncio.to_thread(project.milestones.create, data)
            logger.info("Created milestone: %s", title)
            return make_result(
                data={"milestone": title, "id": ms.id, "action": "created"}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def create_milestone_structure(
        self, project_id: int, phases: list[dict]
    ) -> dict:
        """Create milestones for a list of engagement phases. Idempotent."""
        results = []
        for phase in phases:
            result = await self.create_milestone(
                project_id=project_id,
                title=phase["title"],
                description=phase.get("description", ""),
                start_date=phase.get("start_date"),
                due_date=phase.get("due_date"),
            )
            results.append(result)

        created = [r for r in results if r["status"] == "ok" and r["data"].get("action") == "created"]
        skipped = [r for r in results if r["status"] == "ok" and r["data"].get("action") == "skipped"]
        errors = [r for r in results if r["status"] == "error"]

        if errors:
            return make_error(
                f"Failed to create {len(errors)} milestone(s)",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(errors)}],
            )

        return make_result(
            data={
                "created_count": len(created),
                "skipped_count": len(skipped),
                "total": len(phases),
            }
        )

    async def create_board(self, project_id: int, board_name: str) -> dict:
        """Create a project board. Idempotent — skips if name exists."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            existing = await asyncio.to_thread(
                project.boards.list, get_all=True
            )
            for board in existing:
                if board.name == board_name:
                    logger.info("Board already exists, skipping: %s", board_name)
                    return make_result(
                        data={"board": board_name, "id": board.id, "action": "skipped"},
                        message=f"Board '{board_name}' already exists",
                    )

            board = await asyncio.to_thread(
                project.boards.create, {"name": board_name}
            )
            logger.info("Created board: %s", board_name)
            return make_result(
                data={"board": board_name, "id": board.id, "action": "created"}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def create_board_lists(
        self, project_id: int, board_id: int, label_names: list[str]
    ) -> dict:
        """Create board columns mapped to labels. Idempotent."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )

            # Get all labels to resolve names to IDs
            labels = await asyncio.to_thread(
                project.labels.list, get_all=True
            )
            label_map = {label.name: label.id for label in labels}

            board = await asyncio.to_thread(
                project.boards.get, board_id
            )
            existing_lists = await asyncio.to_thread(
                board.lists.list, get_all=True
            )
            existing_label_ids = {
                lst.label["id"] for lst in existing_lists if hasattr(lst, "label") and lst.label
            }

            created = []
            skipped = []
            for name in label_names:
                label_id = label_map.get(name)
                if not label_id:
                    logger.error("Label not found: %s", name)
                    continue
                if label_id in existing_label_ids:
                    skipped.append(name)
                    continue
                await asyncio.to_thread(
                    board.lists.create, {"label_id": label_id}
                )
                created.append(name)
                logger.info("Created board list for label: %s", name)

            return make_result(
                data={
                    "created": created,
                    "skipped": skipped,
                    "created_count": len(created),
                    "skipped_count": len(skipped),
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


    # --- Issue Management (Story 2.3) ---

    async def create_issue(
        self,
        project_id: int,
        title: str,
        description: str = "",
        labels: list[str] | None = None,
    ) -> dict:
        """Create a GitLab Issue with optional labels."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            data = {"title": title, "description": description}
            if labels:
                data["labels"] = ",".join(labels)

            issue = await asyncio.to_thread(project.issues.create, data)
            logger.info("Created issue #%s: %s", issue.iid, title)
            return make_result(
                data={
                    "iid": issue.iid,
                    "title": issue.title,
                    "labels": issue.labels,
                    "web_url": issue.web_url,
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def get_issue(self, project_id: int, issue_iid: int) -> dict:
        """Fetch Issue details by IID."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            return make_result(
                data={
                    "iid": issue.iid,
                    "title": issue.title,
                    "labels": issue.labels,
                    "state": issue.state,
                    "web_url": issue.web_url,
                }
            )
        except gitlab.exceptions.GitlabGetError as e:
            logger.error("Issue not found: %s", e)
            return make_error(
                f"Issue #{issue_iid} not found: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def list_issues(
        self,
        project_id: int,
        labels: list[str] | None = None,
        milestone: str | None = None,
        state: str = "opened",
    ) -> dict:
        """Query Issues by filters."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            kwargs: dict = {"state": state, "get_all": True}
            if labels:
                kwargs["labels"] = ",".join(labels)
            if milestone:
                kwargs["milestone"] = milestone

            issues = await asyncio.to_thread(project.issues.list, **kwargs)
            return make_result(
                data={
                    "issues": [
                        {
                            "iid": i.iid,
                            "title": i.title,
                            "labels": i.labels,
                            "state": i.state,
                        }
                        for i in issues
                    ],
                    "count": len(issues),
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    # --- Label Operations on Issues (Story 2.3) ---

    async def apply_label(
        self, project_id: int, issue_iid: int, label_name: str
    ) -> dict:
        """Add a label to an Issue."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )

            # Validate label exists
            existing_labels = await asyncio.to_thread(
                project.labels.list, get_all=True
            )
            if not any(l.name == label_name for l in existing_labels):
                return make_error(
                    f"Label '{label_name}' not found on project",
                    flags=[{"code": "GITLAB_LABEL_NOT_FOUND", "message": f"Label '{label_name}' does not exist"}],
                )

            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            if label_name in issue.labels:
                return make_result(
                    data={"iid": issue_iid, "label": label_name, "action": "already_applied"},
                    message=f"Label '{label_name}' already on issue #{issue_iid}",
                )

            issue.labels = issue.labels + [label_name]
            await asyncio.to_thread(issue.save)
            logger.info("Applied label '%s' to issue #%s", label_name, issue_iid)
            return make_result(
                data={"iid": issue_iid, "label": label_name, "action": "applied"}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def remove_label(
        self, project_id: int, issue_iid: int, label_name: str
    ) -> dict:
        """Remove a label from an Issue."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            if label_name not in issue.labels:
                return make_result(
                    data={"iid": issue_iid, "label": label_name, "action": "not_present"},
                    message=f"Label '{label_name}' not on issue #{issue_iid}",
                )

            issue.labels = [l for l in issue.labels if l != label_name]
            await asyncio.to_thread(issue.save)
            logger.info("Removed label '%s' from issue #%s", label_name, issue_iid)
            return make_result(
                data={"iid": issue_iid, "label": label_name, "action": "removed"}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def transition_status(
        self, project_id: int, issue_iid: int, from_label: str, to_label: str
    ) -> dict:
        """Atomic status transition: remove old status label, apply new one."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )

            # Validate to_label exists
            existing_labels = await asyncio.to_thread(
                project.labels.list, get_all=True
            )
            if not any(l.name == to_label for l in existing_labels):
                return make_error(
                    f"Label '{to_label}' not found on project",
                    flags=[{"code": "GITLAB_LABEL_NOT_FOUND", "message": f"Label '{to_label}' does not exist"}],
                )

            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            new_labels = [l for l in issue.labels if l != from_label]
            if to_label not in new_labels:
                new_labels.append(to_label)
            issue.labels = new_labels
            await asyncio.to_thread(issue.save)
            logger.info(
                "Transitioned issue #%s: '%s' → '%s'",
                issue_iid, from_label, to_label,
            )
            return make_result(
                data={
                    "iid": issue_iid,
                    "from_label": from_label,
                    "to_label": to_label,
                    "action": "transitioned",
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


    # --- Milestone Management (Story 2.4) ---

    COMPLEXITY_CAPACITY = {
        "Complexity::Low": 1,
        "Complexity::Medium": 2,
        "Complexity::High": 3,
    }

    async def assign_to_milestone(
        self, project_id: int, issue_iid: int, milestone_id: int
    ) -> dict:
        """Assign an Issue to a milestone."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            issue.milestone_id = milestone_id
            await asyncio.to_thread(issue.save)
            logger.info("Assigned issue #%s to milestone %s", issue_iid, milestone_id)
            return make_result(
                data={
                    "iid": issue_iid,
                    "milestone_id": milestone_id,
                    "action": "assigned",
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def list_milestones(
        self, project_id: int, state: str = "active"
    ) -> dict:
        """List milestones with optional state filter."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            milestones = await asyncio.to_thread(
                project.milestones.list, state=state, get_all=True
            )
            return make_result(
                data={
                    "milestones": [
                        {
                            "id": ms.id,
                            "title": ms.title,
                            "state": ms.state,
                            "start_date": getattr(ms, "start_date", None),
                            "due_date": getattr(ms, "due_date", None),
                        }
                        for ms in milestones
                    ],
                    "count": len(milestones),
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def get_milestone(self, project_id: int, milestone_id: int) -> dict:
        """Fetch milestone details."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            ms = await asyncio.to_thread(
                project.milestones.get, milestone_id
            )
            return make_result(
                data={
                    "id": ms.id,
                    "title": ms.title,
                    "description": ms.description,
                    "state": ms.state,
                }
            )
        except gitlab.exceptions.GitlabGetError as e:
            logger.error("Milestone not found: %s", e)
            return make_error(
                f"Milestone #{milestone_id} not found: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def get_milestone_burndown(
        self, project_id: int, milestone_id: int
    ) -> dict:
        """Get burndown data for a milestone — open/closed/complexity breakdown."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )

            # Get milestone to use its title for issue query
            ms = await asyncio.to_thread(
                project.milestones.get, milestone_id
            )

            issues = await asyncio.to_thread(
                project.issues.list,
                milestone=ms.title,
                state="all",
                get_all=True,
            )

            open_issues = [i for i in issues if i.state == "opened"]
            closed_issues = [i for i in issues if i.state == "closed"]

            # Calculate complexity-based capacity
            total_capacity = 0
            completed_capacity = 0
            by_complexity = {}
            for issue in issues:
                complexity = 0
                for label in issue.labels:
                    if label in self.COMPLEXITY_CAPACITY:
                        complexity = self.COMPLEXITY_CAPACITY[label]
                        by_complexity.setdefault(label, {"total": 0, "closed": 0})
                        by_complexity[label]["total"] += 1
                        if issue.state == "closed":
                            by_complexity[label]["closed"] += 1
                        break
                total_capacity += complexity
                if issue.state == "closed":
                    completed_capacity += complexity

            return make_result(
                data={
                    "milestone": ms.title,
                    "total_issues": len(issues),
                    "open_issues": len(open_issues),
                    "closed_issues": len(closed_issues),
                    "total_capacity": total_capacity,
                    "completed_capacity": completed_capacity,
                    "remaining_capacity": total_capacity - completed_capacity,
                    "by_complexity": by_complexity,
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


    # --- Comments & Reporting (Story 2.5) ---

    async def add_comment(
        self, project_id: int, issue_iid: int, body: str
    ) -> dict:
        """Post a markdown comment to an Issue."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            issue = await asyncio.to_thread(project.issues.get, issue_iid)
            note = await asyncio.to_thread(
                issue.notes.create, {"body": body}
            )
            logger.info("Added comment to issue #%s", issue_iid)
            return make_result(
                data={"issue_iid": issue_iid, "note_id": note.id}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    @staticmethod
    def build_progress_comment(
        agent_name: str,
        stage: str,
        summary: list[str],
        flags: list[dict] | None = None,
    ) -> str:
        """Generate standardized progress comment markdown."""
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        lines = [
            f"## Stage Completion: {stage}",
            "",
            f"**Agent:** {agent_name}",
            f"**Stage:** {stage}",
            f"**Timestamp:** {ts}",
            "",
            "### Summary",
        ]
        for item in summary:
            lines.append(f"- {item}")

        if flags:
            lines.append("")
            lines.append("### Flags")
            for flag in flags:
                lines.append(f"- {flag.get('code', 'UNKNOWN')}: {flag.get('message', '')}")

        return "\n".join(lines)

    async def build_milestone_summary(
        self, project_id: int, milestone_id: int
    ) -> dict:
        """Build milestone summary markdown for posting on an Epic."""
        try:
            burndown = await self.get_milestone_burndown(project_id, milestone_id)
            if burndown["status"] == "error":
                return burndown

            data = burndown["data"]
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            lines = [
                f"## Sprint Summary: {data['milestone']}",
                "",
                f"**Generated:** {ts}",
                "",
                "### Progress",
                f"- Total modules: {data['total_issues']}",
                f"- Completed: {data['closed_issues']}",
                f"- Outstanding: {data['open_issues']}",
                f"- Capacity: {data['completed_capacity']}/{data['total_capacity']} units",
                "",
            ]

            if data.get("by_complexity"):
                lines.append("### By Complexity")
                for label, counts in data["by_complexity"].items():
                    lines.append(
                        f"- {label}: {counts['closed']}/{counts['total']} complete"
                    )

            return make_result(
                data={"markdown": "\n".join(lines), "burndown": data}
            )
        except Exception as e:
            logger.error("Milestone summary error: %s", e)
            return make_error(
                f"Failed to build milestone summary: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def update_readme_file(
        self, project_id: int, content: str, branch: str = "main"
    ) -> dict:
        """Write content to the project README via GitLab API."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            try:
                f = await asyncio.to_thread(
                    project.files.get, file_path="README.md", ref=branch
                )
                f.content = content
                await asyncio.to_thread(
                    f.save, branch=branch, commit_message="Update modernisation dashboard"
                )
                action = "updated"
            except gitlab.exceptions.GitlabGetError:
                await asyncio.to_thread(
                    project.files.create,
                    {
                        "file_path": "README.md",
                        "branch": branch,
                        "content": content,
                        "commit_message": "Create modernisation dashboard",
                    },
                )
                action = "created"

            logger.info("README %s on project %s", action, project_id)
            return make_result(
                data={"action": action, "project_id": project_id}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


    # --- Epic Labels (scoped labels replace Premium Epics on Free tier) ---

    _EPIC_PREFIX = "Epic::"
    _EPIC_COLOR = "#6699CC"

    async def create_epic_label(
        self, project_id: int, epic_name: str, color: str | None = None
    ) -> dict:
        """Create an Epic:: scoped label to group issues by subsystem."""
        label_name = f"{self._EPIC_PREFIX}{epic_name}"
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(self._gl.projects.get, project_id)
            label = await asyncio.to_thread(
                project.labels.create,
                {"name": label_name, "color": color or self._EPIC_COLOR},
            )
            logger.info("Created epic label: %s", label_name)
            return make_result(
                data={"label": label.name, "color": label.color, "action": "created"}
            )
        except gitlab.exceptions.GitlabCreateError as e:
            if "already exists" in str(e).lower():
                return make_result(
                    data={"label": label_name, "action": "already_exists"},
                    message=f"Epic label '{label_name}' already exists",
                )
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Create epic label error: %s", e)
            return make_error(
                f"Failed to create epic label: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def list_epic_labels(self, project_id: int) -> dict:
        """List all Epic:: scoped labels in the project."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(self._gl.projects.get, project_id)
            all_labels = await asyncio.to_thread(project.labels.list, get_all=True)
            epics = [
                {"label": l.name, "color": l.color}
                for l in all_labels
                if l.name.startswith(self._EPIC_PREFIX)
            ]
            return make_result(data={"epics": epics, "count": len(epics)})
        except Exception as e:
            logger.error("List epic labels error: %s", e)
            return make_error(
                f"Failed to list epic labels: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def close_epic_label(
        self, project_id: int, epic_name: str, qa_name: str = "QA"
    ) -> dict:
        """Validate all issues with an Epic:: label are QA-Complete, post summary, close them."""
        label_name = f"{self._EPIC_PREFIX}{epic_name}"
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(self._gl.projects.get, project_id)
            issues = await asyncio.to_thread(
                project.issues.list, labels=[label_name], state="opened", get_all=True
            )

            if not issues:
                return make_error(
                    f"No open issues found with label '{label_name}'",
                    flags=[{"code": "GITLAB_NO_ISSUES", "message": f"No issues with {label_name}"}],
                )

            incomplete = []
            complete = []
            for issue in issues:
                if "QA-Complete" in issue.labels:
                    complete.append({"iid": issue.iid, "title": issue.title})
                else:
                    incomplete.append({"iid": issue.iid, "title": issue.title})

            if incomplete:
                return make_error(
                    f"{len(incomplete)} module(s) not QA-Complete",
                    flags=[{
                        "code": "GITLAB_EPIC_INCOMPLETE",
                        "message": f"Incomplete modules: {[m['title'] for m in incomplete]}",
                    }],
                )

            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            lines = [
                f"## {label_name} — QA Sign-off",
                "",
                f"**QA Engineer:** {qa_name}",
                f"**Date:** {ts}",
                "",
                f"**All {len(complete)} modules QA-Complete. Epic approved for closure.**",
            ]
            summary = "\n".join(lines)

            for m in complete:
                await self.add_comment(project_id, m["iid"], summary)
                issue = await asyncio.to_thread(project.issues.get, m["iid"])
                issue.state_event = "close"
                await asyncio.to_thread(issue.save)

            return make_result(
                data={
                    "epic_label": label_name,
                    "qa_name": qa_name,
                    "modules_count": len(complete),
                    "closed_issues": [m["iid"] for m in complete],
                    "action": "epic_signed_off_and_closed",
                }
            )
        except Exception as e:
            logger.error("Epic label sign-off error: %s", e)
            return make_error(
                f"Epic label sign-off failed: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    # --- Epic Operations (Premium/Ultimate only — kept but not exposed as MCP tools) ---

    async def list_epics(
        self, group_id: int, state: str = "opened"
    ) -> dict:
        """List epics in a group with optional state filter."""
        try:
            self._ensure_authenticated()
            group = await asyncio.to_thread(self._gl.groups.get, group_id)
            epics = await asyncio.to_thread(
                group.epics.list, state=state, get_all=True
            )
            return make_result(
                data={
                    "epics": [
                        {
                            "iid": epic.iid,
                            "title": epic.title,
                            "state": epic.state,
                        }
                        for epic in epics
                    ],
                    "count": len(epics),
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def create_epic(
        self, group_id: int, title: str, description: str = ""
    ) -> dict:
        """Create a GitLab Epic at group level."""
        try:
            self._ensure_authenticated()
            group = await asyncio.to_thread(self._gl.groups.get, group_id)
            epic = await asyncio.to_thread(
                group.epics.create, {"title": title, "description": description}
            )
            logger.info("Created epic #%s: %s", epic.iid, title)
            return make_result(
                data={"iid": epic.iid, "title": epic.title, "web_url": epic.web_url}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def get_epic(self, group_id: int, epic_iid: int) -> dict:
        """Fetch Epic details."""
        try:
            self._ensure_authenticated()
            group = await asyncio.to_thread(self._gl.groups.get, group_id)
            epic = await asyncio.to_thread(group.epics.get, epic_iid)
            return make_result(
                data={
                    "iid": epic.iid,
                    "title": epic.title,
                    "state": epic.state,
                    "description": epic.description,
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def close_epic(self, group_id: int, epic_iid: int) -> dict:
        """Close an Epic."""
        try:
            self._ensure_authenticated()
            group = await asyncio.to_thread(self._gl.groups.get, group_id)
            epic = await asyncio.to_thread(group.epics.get, epic_iid)
            epic.state_event = "close"
            await asyncio.to_thread(epic.save)
            logger.info("Closed epic #%s", epic_iid)
            return make_result(
                data={"iid": epic_iid, "state": "closed", "action": "closed"}
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def validate_epic_closure(
        self, project_id: int, issue_iids: list[int]
    ) -> dict:
        """Check all Issues have QA-Complete label. Returns incomplete modules."""
        try:
            self._ensure_authenticated()
            project = await asyncio.to_thread(
                self._gl.projects.get, project_id
            )
            incomplete = []
            complete = []
            for iid in issue_iids:
                issue = await asyncio.to_thread(project.issues.get, iid)
                if "QA-Complete" in issue.labels:
                    complete.append({"iid": iid, "title": issue.title})
                else:
                    incomplete.append({"iid": iid, "title": issue.title, "labels": issue.labels})

            if incomplete:
                return make_error(
                    f"{len(incomplete)} module(s) not QA-Complete",
                    flags=[{
                        "code": "GITLAB_EPIC_INCOMPLETE",
                        "message": f"Incomplete modules: {[m['title'] for m in incomplete]}",
                    }],
                )

            return make_result(
                data={
                    "all_complete": True,
                    "complete_count": len(complete),
                    "modules": complete,
                }
            )
        except RuntimeError as e:
            logger.error("Auth error: %s", e)
            return make_error(
                str(e),
                flags=[{"code": "GITLAB_AUTH_ERROR", "message": str(e)}],
            )
        except gitlab.exceptions.GitlabError as e:
            logger.error("GitLab API error: %s", e)
            return make_error(
                f"GitLab API error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return make_error(
                f"Unexpected error: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def sign_off_module(
        self,
        project_id: int,
        issue_iid: int,
        validator_name: str,
        next_stage: str,
    ) -> dict:
        """Sign off a module: remove Awaiting-Review, apply next stage, post comment."""
        try:
            # Transition label
            transition_result = await self.transition_status(
                project_id, issue_iid, "Awaiting-Review", next_stage
            )
            if transition_result["status"] == "error":
                return transition_result

            # Post sign-off comment
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            comment = "\n".join([
                "## Module Sign-off",
                "",
                f"**Validator:** {validator_name}",
                "**Action:** Approved — review gate closed",
                f"**Previous Status:** Awaiting-Review",
                f"**New Status:** {next_stage}",
                f"**Timestamp:** {ts}",
            ])
            await self.add_comment(project_id, issue_iid, comment)

            return make_result(
                data={
                    "iid": issue_iid,
                    "validator": validator_name,
                    "new_status": next_stage,
                    "action": "signed_off",
                }
            )
        except Exception as e:
            logger.error("Sign-off error: %s", e)
            return make_error(
                f"Module sign-off failed: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def sign_off_epic(
        self,
        group_id: int,
        epic_iid: int,
        project_id: int,
        issue_iids: list[int],
        qa_name: str,
    ) -> dict:
        """Validate all modules QA-Complete, post summary, close Epic."""
        try:
            # Validate
            validation = await self.validate_epic_closure(project_id, issue_iids)
            if validation["status"] == "error":
                return validation

            # Build summary
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            modules = validation["data"]["modules"]
            lines = [
                "## Epic QA Sign-off",
                "",
                f"**QA Engineer:** {qa_name}",
                f"**Date:** {ts}",
                "",
                "### Module QA Status",
                "| Module | QA Status | Signed Off |",
                "|--------|-----------|-----------|",
            ]
            for m in modules:
                lines.append(f"| {m['title']} | QA-Complete | Yes |")
            lines.append("")
            lines.append(
                f"**All {len(modules)} modules QA-Complete. Epic approved for closure.**"
            )
            summary = "\n".join(lines)

            # Close Epic
            close_result = await self.close_epic(group_id, epic_iid)
            if close_result["status"] == "error":
                return close_result

            return make_result(
                data={
                    "epic_iid": epic_iid,
                    "qa_name": qa_name,
                    "modules_count": len(modules),
                    "summary": summary,
                    "action": "epic_signed_off_and_closed",
                }
            )
        except Exception as e:
            logger.error("Epic sign-off error: %s", e)
            return make_error(
                f"Epic sign-off failed: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )


client = GitlabClient()
