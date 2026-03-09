# GitLab MCP Server

Project management and delivery orchestration for mainframe modernisation. Manages Issues, Labels, Milestones, Boards, Epics, and a live README dashboard — all through the GitLab API via `python-gitlab`.

## Credentials & Configuration

**Secrets** — add your personal access token to `.env` (never committed):

```
GITLAB_TOKEN=glpat-your-token-here
```

Generate one at GitLab → Settings → Access Tokens with `api` scope.

**Config** — set your GitLab instance, project, and IDs in `config.yaml`:

```yaml
gitlab_url: "https://gitlab.com"
gitlab_project: "your-group/your-project"
project_id: 12345678          # numeric GitLab project ID (Settings > General)
group_id: 12345678             # numeric GitLab group ID (Group > Settings > General)
```

When `project_id` and `group_id` are set in config, all tools use them as defaults — no need to pass IDs explicitly on every call. You can still override by passing the parameter directly.

## Capabilities

| Tool | Description |
|------|-------------|
| `ping_gitlab` | Check connectivity and return GitLab version |
| `init_project` | Full project setup — creates labels, milestones, and a board in one call |
| `create_labels` | Create the standard label taxonomy (pipeline stages, complexity, status) |
| `create_milestone` | Create a sprint milestone with optional start/due dates |
| `create_board` | Create an issue board |
| `create_issue` | Create an Issue with optional labels |
| `list_issues` | List Issues with optional filters (state, labels, milestone) |
| `create_epic` | Create an Epic at group level |
| `list_epics` | List Epics in a group with optional state filter |
| `apply_label` | Apply a label to an Issue |
| `remove_label` | Remove a label from an Issue |
| `update_issue_status` | Transition an Issue's status label (auto-removes the previous status) |
| `assign_to_milestone` | Assign an Issue to a milestone |
| `list_milestones` | List milestones with state filter and date ranges |
| `add_comment` | Post a markdown comment to an Issue |
| `get_milestone_burndown` | Get burndown data — open/closed counts and complexity breakdown |
| `update_readme` | Regenerate and push the modernisation dashboard to the project README |
| `close_epic` | Validate all modules are QA-Complete, post summary, and close the Epic |

## Label Taxonomy

Created by `init_project` or `create_labels`:

- **Pipeline stages** — `Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`
- **Complexity** — `Complexity::Low`, `Complexity::Medium`, `Complexity::High`
- **Status** — `In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`

All label operations are idempotent — existing labels are skipped.
