# Story 2.5: Progress Reporting & README Dashboard

Status: review

## Story

As any pipeline agent,
I want to post structured progress comments and update the project README dashboard,
So that all stakeholders have real-time visibility into modernisation progress.

## Acceptance Criteria

1. **AC1: Agent Posts Structured Progress Comment**
   - Given an agent completes a pipeline stage for a module
   - When the agent posts a progress comment to the module's GitLab Issue
   - Then the comment includes: agent name, stage completed, ISO 8601 UTC timestamp, summary of outputs, any flags raised
   - And the comment is formatted as markdown
   - And FR50 is satisfied

2. **AC2: Status-Triggered README Update**
   - Given any agent changes a module's pipeline status
   - When the README is updated
   - Then the project README reflects the current state of all modules
   - And FR51 is satisfied

3. **AC3: Client Sponsor Dashboard View**
   - Given the README dashboard exists
   - When a Client Sponsor views the project README
   - Then they see: total modules, modules per pipeline stage, modules blocked, Epics signed off
   - And the dashboard is a markdown table
   - And FR52 is satisfied

4. **AC4: Milestone Summary Comment on Epic**
   - Given a sprint milestone is active
   - When the PM generates a milestone summary
   - Then a comment is posted on the relevant Epic showing: sprint progress, completed modules, outstanding modules, blockers
   - And FR53 is satisfied

## Tasks / Subtasks

- [x] Task 1: Add comment operations to `gitlab_client.py` (AC: #1, #4)
  - [x] 1.1: Implement `add_comment(project_id, issue_iid, body)` — posts markdown comment to Issue
  - [x] 1.2: Implement `add_epic_comment(project_id, epic_iid, body)` — covered via add_comment (GitLab epics use same notes API)
  - [x] 1.3: Implement `build_progress_comment(agent_name, stage, summary, flags)` — generates standardized markdown comment body with ISO 8601 timestamp
  - [x] 1.4: Implement `build_milestone_summary(project_id, milestone_id)` — queries milestone Issues, builds summary markdown
  - [x] 1.5: All API calls use `asyncio.to_thread()`

- [x] Task 2: Create `readme_updater.py` — README dashboard generation (AC: #2, #3)
  - [x] 2.1: Create `mcp-servers/gitlab_mcp/readme_updater.py` with `ReadmeUpdater` class
  - [x] 2.2: Implement `generate_dashboard(project_id)` — queries all Issues, builds markdown dashboard table
  - [x] 2.3: Dashboard columns: Module Name, Complexity, Current Stage, Status, Last Updated
  - [x] 2.4: Summary row: Total Modules, counts per status (In-Analysis, Awaiting-Review, In-Migration, Blocked, QA-Complete, Done)
  - [x] 2.5: Signed-off Epics section
  - [x] 2.6: Footer: "Last updated: {ISO 8601 timestamp} by {agent_name}"
  - [x] 2.7: Implement `update_readme(project_id, content)` — writes dashboard to project README via GitLab API

- [x] Task 3: Add MCP tools to `server.py` (AC: #1, #2, #3, #4)
  - [x] 3.1: Add `add_comment(project_id, issue_iid, body)` tool
  - [x] 3.2: Add `update_readme(project_id)` tool — triggers full dashboard regeneration and push
  - [x] 3.3: Thin wrappers with per-tool try/except

- [x] Task 4: Write comprehensive tests (AC: #1, #2, #3, #4)
  - [x] 4.1: Create `tests/gitlab_mcp/test_readme_updater.py` — test dashboard generation, table format, summary counts
  - [x] 4.2: Test progress comment formatting — agent name, stage, timestamp (ISO 8601), summary, flags
  - [x] 4.3: Test milestone summary — correct Issue counts, blocker listing
  - [x] 4.4: Test README update API call
  - [x] 4.5: Update mock fixtures for comment + file API operations
  - [x] 4.6: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **readme_updater.py**: New domain module per architecture spec — owns ALL README dashboard logic
- **Comment formatting in gitlab_client.py**: Comments are core GitLab operations, not a separate module
- **Tool names match PRD**: `add_comment`, `update_readme`
- **ISO 8601 UTC timestamps everywhere**: Use `datetime.datetime.now(datetime.timezone.utc).isoformat()`, never Unix integers
- **Markdown formatting**: All comments and dashboard use clean markdown tables

### Dashboard Table Format

```markdown
# Modernisation Dashboard

| Module | Complexity | Stage | Status | Last Updated |
|--------|-----------|-------|--------|-------------|
| PAYROLL-CALC | High | Po-Analysis-Complete | Awaiting-Review | 2026-03-07T12:00:00Z |
| BENEFITS-MGR | Low | In-Analysis | In-Analysis | 2026-03-07T10:00:00Z |

## Summary
| Status | Count |
|--------|-------|
| Total Modules | 15 |
| In-Analysis | 5 |
| Awaiting-Review | 3 |
| In-Migration | 4 |
| Blocked | 1 |
| Done | 2 |

## Signed-Off Epics
- Epic 1: Core Payroll (QA-Complete, signed off 2026-03-06)

*Last updated: 2026-03-07T12:00:00Z by Shifu*
```

### Progress Comment Format

```markdown
## Stage Completion: Po-Analysis-Complete

**Agent:** Po
**Stage:** Analysis Phase 1
**Timestamp:** 2026-03-07T12:00:00Z

### Summary
- Call graph extracted: 15 nodes, 23 edges
- Complexity score: High (cyclomatic: 45)
- Business rules extracted: 12

### Flags
- UNKNOWN_MACRO: `XCALC` macro not found in delta-macros library
```

### python-gitlab API Reference

```python
# Issue comments
issue = project.issues.get(issue_iid)
issue.notes.create({"body": "markdown comment"})

# Repository file (README)
project.files.get(file_path="README.md", ref="main")
project.files.create({"file_path": "README.md", "branch": "main", "content": "...", "commit_message": "..."})
# or update:
f = project.files.get("README.md", ref="main")
f.content = new_content
f.save(branch="main", commit_message="Update dashboard")
```

### Previous Stories Context

- Story 2.1: Core client + auth
- Story 2.2: Labels + milestones + boards exist
- Story 2.3: Issue CRUD + label operations exist
- Story 2.4: Milestone assignment + burndown query exist

### Files to CREATE

| File | Purpose |
|------|---------|
| `mcp-servers/gitlab_mcp/readme_updater.py` | README dashboard generation |
| `tests/gitlab_mcp/test_readme_updater.py` | README updater tests |

### Files to MODIFY

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | Add comment methods + milestone summary builder |
| `mcp-servers/gitlab_mcp/server.py` | Add add_comment, update_readme tools |
| `tests/gitlab_mcp/test_gitlab_client.py` | Add comment tests |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | Add mock comment + file API responses |

### Dependencies

- Stories 2.1-2.4 (all prior gitlab-mcp functionality)
- All downstream agents (Po, Oogway, Tigress, Viper, Monkey, Mantis) will call these tools

### Functional Requirements Satisfied

- **FR50**: Any agent can post structured progress comments
- **FR51**: README updated on status changes
- **FR52**: Client Sponsor dashboard with summary stats
- **FR53**: PM can generate milestone summary on Epic

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.5]
- [Source: documents/planning-artifacts/architecture.md — readme_updater.py domain module]
- [Source: documents/planning-artifacts/prd.md — FR50, FR51, FR52, FR53]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- Comment posting (add_comment), progress comment builder (ISO 8601 timestamps), milestone summary builder
- ReadmeUpdater with dashboard generation (table, summary, footer) and GitLab file API push
- update_readme_file handles both create and update scenarios
- 9 new tests (4 comment + 5 dashboard), 139 total passing

### File List
- `mcp-servers/gitlab_mcp/readme_updater.py` — NEW: README dashboard generation
- `mcp-servers/gitlab_mcp/gitlab_client.py` — MODIFIED: Added add_comment, build_progress_comment, build_milestone_summary, update_readme_file
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added add_comment, update_readme tools + ReadmeUpdater
- `tests/gitlab_mcp/test_readme_updater.py` — NEW: 5 dashboard tests
- `tests/gitlab_mcp/test_gitlab_client.py` — MODIFIED: Added 4 comment tests

### Change Log
- 2026-03-07: Story 2.5 implemented — Comments, README dashboard, milestone summaries, 9 new tests
