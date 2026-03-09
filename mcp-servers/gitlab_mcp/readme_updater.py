"""README dashboard generation for GitLab project modernisation tracking."""

import datetime
import logging

from gitlab_mcp.label_manager import PIPELINE_STAGE_LABELS, STATUS_LABELS
from gitlab_mcp.result import make_error, make_result

logger = logging.getLogger("gitlab-mcp")

STATUS_NAMES = [label["name"] for label in STATUS_LABELS]
STAGE_NAMES = [label["name"] for label in PIPELINE_STAGE_LABELS]


class ReadmeUpdater:
    """Generates and updates the modernisation dashboard README."""

    def __init__(self, gitlab_client) -> None:
        self._client = gitlab_client

    async def generate_dashboard(
        self, project_id: int, agent_name: str = "Shifu"
    ) -> dict:
        """Query all Issues and build markdown dashboard."""
        try:
            issues_result = await self._client.list_issues(
                project_id, state="all"
            )
            if issues_result["status"] == "error":
                return issues_result

            issues = issues_result["data"]["issues"]
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

            lines = ["# Modernisation Dashboard", ""]
            lines.append("| Module | Complexity | Stage | Status | Last Updated |")
            lines.append("|--------|-----------|-------|--------|-------------|")

            status_counts = {name: 0 for name in STATUS_NAMES}
            status_counts["Total Modules"] = len(issues)

            for issue in issues:
                complexity = ""
                stage = ""
                status = ""
                for label in issue["labels"]:
                    if label.startswith("Complexity::"):
                        complexity = label.split("::")[1]
                    elif label in STAGE_NAMES:
                        stage = label
                    elif label in STATUS_NAMES:
                        status = label
                        status_counts[label] = status_counts.get(label, 0) + 1

                lines.append(
                    f"| {issue['title']} | {complexity} | {stage} | {status} | {ts} |"
                )

            lines.extend(["", "## Summary", "| Status | Count |", "|--------|-------|"])
            lines.append(f"| Total Modules | {status_counts['Total Modules']} |")
            for name in STATUS_NAMES:
                lines.append(f"| {name} | {status_counts.get(name, 0)} |")

            lines.extend(["", f"*Last updated: {ts} by {agent_name}*", ""])

            markdown = "\n".join(lines)
            return make_result(data={"markdown": markdown, "issue_count": len(issues)})

        except Exception as e:
            logger.error("Dashboard generation error: %s", e)
            return make_error(
                f"Failed to generate dashboard: {e}",
                flags=[{"code": "GITLAB_API_ERROR", "message": str(e)}],
            )

    async def update_readme(
        self, project_id: int, agent_name: str = "Shifu"
    ) -> dict:
        """Generate dashboard and push to project README."""
        dashboard = await self.generate_dashboard(project_id, agent_name)
        if dashboard["status"] == "error":
            return dashboard

        return await self._client.update_readme_file(
            project_id, dashboard["data"]["markdown"]
        )
