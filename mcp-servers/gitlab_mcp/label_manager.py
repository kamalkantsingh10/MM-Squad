"""Label taxonomy management for GitLab project initialisation."""

import asyncio
import logging

import gitlab.exceptions

from gitlab_mcp.result import make_error, make_result

logger = logging.getLogger("gitlab-mcp")

PIPELINE_STAGE_LABELS = [
    {"name": "Po-Analysis-Complete", "color": "#0075B8"},
    {"name": "Architecture-Complete", "color": "#5CB85C"},
    {"name": "Code-Generated", "color": "#F0AD4E"},
    {"name": "QA-Complete", "color": "#5BC0DE"},
]

COMPLEXITY_LABELS = [
    {"name": "Complexity::Low", "color": "#69D100"},
    {"name": "Complexity::Medium", "color": "#E65100"},
    {"name": "Complexity::High", "color": "#D9534F"},
]

STATUS_LABELS = [
    {"name": "In-Analysis", "color": "#428BCA"},
    {"name": "Awaiting-Review", "color": "#F0AD4E"},
    {"name": "In-Migration", "color": "#5CB85C"},
    {"name": "Blocked", "color": "#D9534F"},
    {"name": "Done", "color": "#5BC0DE"},
]

ALL_LABELS = PIPELINE_STAGE_LABELS + COMPLEXITY_LABELS + STATUS_LABELS


class LabelManager:
    """Manages GitLab label taxonomy creation with idempotency."""

    def __init__(self, gitlab_client) -> None:
        self._client = gitlab_client

    async def create_label_taxonomy(self, project_id: int) -> dict:
        """Create all standard labels for a project. Idempotent — skips existing."""
        try:
            self._client._ensure_authenticated()
            project = await asyncio.to_thread(
                self._client._gl.projects.get, project_id
            )
            existing_labels = await asyncio.to_thread(
                project.labels.list, get_all=True
            )
            existing_names = {label.name for label in existing_labels}

            created = []
            skipped = []

            for label_def in ALL_LABELS:
                if label_def["name"] in existing_names:
                    skipped.append(label_def["name"])
                    logger.info("Label already exists, skipping: %s", label_def["name"])
                    continue

                await asyncio.to_thread(
                    project.labels.create,
                    {"name": label_def["name"], "color": label_def["color"]},
                )
                created.append(label_def["name"])
                logger.info("Created label: %s", label_def["name"])

            return make_result(
                data={
                    "created": created,
                    "skipped": skipped,
                    "created_count": len(created),
                    "skipped_count": len(skipped),
                    "total": len(ALL_LABELS),
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
