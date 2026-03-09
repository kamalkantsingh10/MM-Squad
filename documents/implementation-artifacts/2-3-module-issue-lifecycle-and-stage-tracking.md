# Story 2.3: Module Issue Lifecycle & Stage Tracking

Status: review

## Story

As a PM (Shifu),
I want each COBOL module to have a dedicated GitLab Issue that tracks its complete pipeline lifecycle,
So that the team has clear visibility into where every module stands in the modernisation pipeline.

## Acceptance Criteria

1. **AC1: Create Issue with Complexity Label**
   - Given a GitLab project is initialised (labels exist)
   - When the PM creates a module Issue for a COBOL module (e.g., `PAYROLL-CALC`)
   - Then a GitLab Issue is created with the module name as the title
   - And the Issue is assigned the appropriate `Complexity::` label based on Po's analysis
   - And the Issue is assigned the `In-Analysis` status label
   - And FR43 is satisfied

2. **AC2: Agent Applies Stage Completion Label**
   - Given a module Issue exists
   - When any agent completes its pipeline stage for that module
   - Then the agent applies the appropriate stage completion label (e.g., `Po-Analysis-Complete`)
   - And FR44 is satisfied

3. **AC3: Transition to Awaiting-Review**
   - Given a module Issue exists
   - When any agent's output requires analyst approval
   - Then the agent transitions the Issue to `Awaiting-Review` by applying the label
   - And FR45 is satisfied

4. **AC4: Analyst Closes Review Gate**
   - Given a module Issue is in `Awaiting-Review` status
   - When the analyst approves and closes the review gate
   - Then the `Awaiting-Review` label is removed
   - And the Issue transitions to the next pipeline stage label
   - And FR46 is satisfied

5. **AC5: Board Column Placement**
   - Given a module Issue exists with status labels
   - When the operator inspects the pipeline board
   - Then the Issue appears in the correct column matching its current status label

## Tasks / Subtasks

- [x] Task 1: Add issue management to `gitlab_client.py` (AC: #1)
  - [x] 1.1: Implement `create_issue(project_id, title, description, labels)` — creates GitLab Issue
  - [x] 1.2: Implement `get_issue(project_id, issue_iid)` — fetches Issue details
  - [x] 1.3: Implement `list_issues(project_id, labels, milestone, state)` — query Issues by filters
  - [x] 1.4: All methods use `asyncio.to_thread()` wrapping
  - [x] 1.5: All methods return `make_result()` / `make_error()` format

- [x] Task 2: Add label operations to `gitlab_client.py` (AC: #2, #3, #4)
  - [x] 2.1: Implement `apply_label(project_id, issue_iid, label_name)` — adds label to Issue
  - [x] 2.2: Implement `remove_label(project_id, issue_iid, label_name)` — removes label from Issue
  - [x] 2.3: Implement `transition_status(project_id, issue_iid, from_label, to_label)` — atomic remove + apply for status transitions
  - [x] 2.4: Validate label exists before applying (return `make_error()` with `GITLAB_LABEL_NOT_FOUND` if missing)

- [x] Task 3: Add MCP tools to `server.py` (AC: #1, #2, #3, #4)
  - [x] 3.1: Add `create_issue(project_id, title, description, labels)` tool
  - [x] 3.2: Add `apply_label(project_id, issue_iid, label_name)` tool
  - [x] 3.3: Add `remove_label(project_id, issue_iid, label_name)` tool
  - [x] 3.4: Add `update_issue_status(project_id, issue_iid, new_status)` tool — wraps transition logic (remove old status label, apply new one)
  - [x] 3.5: All tools thin wrappers with per-tool try/except

- [x] Task 4: Write comprehensive tests (AC: #1, #2, #3, #4, #5)
  - [x] 4.1: Test Issue creation with module name as title + complexity + status labels
  - [x] 4.2: Test apply_label adds stage completion label to existing Issue
  - [x] 4.3: Test Awaiting-Review transition applies label correctly
  - [x] 4.4: Test review gate closure — removes Awaiting-Review, applies next stage label
  - [x] 4.5: Test error cases — missing Issue, missing label, API errors
  - [x] 4.6: Update mock fixtures for Issue operations
  - [x] 4.7: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **All Issue/label logic in gitlab_client.py** — no new domain modules needed for this story
- **Status transition is remove + apply**: GitLab doesn't have built-in status machines for labels. Implement as atomic remove old status → apply new status
- **Label validation**: Check label exists on project before applying. Return structured error if not found
- **Tool names must match PRD exactly**: `create_issue`, `apply_label`, `remove_label`, `update_issue_status`

### Status Label Workflow

```
Initial: In-Analysis
  → Po completes → apply Po-Analysis-Complete + transition to Awaiting-Review
  → Analyst approves → remove Awaiting-Review + transition to In-Migration
  → Oogway completes → apply Architecture-Complete
  → Dev completes → apply Code-Generated
  → Mantis completes → apply QA-Complete + transition to Done
  → Any blocker → transition to Blocked
```

### python-gitlab Issue API

```python
# Create Issue
project.issues.create({"title": "PAYROLL-CALC", "description": "...", "labels": ["In-Analysis", "Complexity::High"]})

# Get Issue
issue = project.issues.get(issue_iid)

# Apply/Remove Labels
issue.labels  # returns list of label names
issue.labels = issue.labels + ["Po-Analysis-Complete"]  # add label
issue.labels = [l for l in issue.labels if l != "Awaiting-Review"]  # remove label
issue.save()  # persist changes
```

### Previous Stories Context

- Story 2.1: `GitlabClient` with lazy auth, `asyncio.to_thread()` pattern
- Story 2.2: `LabelManager` with full taxonomy — all labels exist on project before this story runs

### Files to MODIFY

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | Add issue CRUD + label apply/remove methods |
| `mcp-servers/gitlab_mcp/server.py` | Add create_issue, apply_label, remove_label, update_issue_status tools |
| `tests/gitlab_mcp/test_gitlab_client.py` | Add issue + label operation tests |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | Add mock Issue responses |

### Dependencies

- Story 2.1 (gitlab-mcp core + authentication)
- Story 2.2 (label taxonomy created on project)
- Po analysis output for complexity scoring (consumed, not produced here)

### Functional Requirements Satisfied

- **FR43**: Each COBOL module has a dedicated GitLab Issue
- **FR44**: Any agent can apply stage completion labels
- **FR45**: Any agent can transition to Awaiting-Review
- **FR46**: Analyst can close review gate and transition to next stage

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.3]
- [Source: documents/planning-artifacts/prd.md — FR43, FR44, FR45, FR46]
- [Source: documents/planning-artifacts/architecture.md — gitlab-mcp tool boundaries]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- Issue CRUD: create_issue, get_issue, list_issues with filter support
- Label ops: apply_label with validation, remove_label, transition_status (atomic remove+apply)
- update_issue_status tool auto-detects current status label before transitioning
- 10 new tests, 124 total passing

### File List
- `mcp-servers/gitlab_mcp/gitlab_client.py` — MODIFIED: Added issue + label operation methods
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added 4 new tools (create_issue, apply_label, remove_label, update_issue_status)
- `tests/gitlab_mcp/test_gitlab_client.py` — MODIFIED: Added 10 issue + label tests
- `tests/gitlab_mcp/fixtures/mock_gitlab.py` — MODIFIED: Added make_mock_issue fixture

### Change Log
- 2026-03-07: Story 2.3 implemented — Issue lifecycle, label operations, status transitions, 10 new tests
