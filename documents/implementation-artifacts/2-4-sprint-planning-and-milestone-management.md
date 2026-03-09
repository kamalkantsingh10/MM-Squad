# Story 2.4: Sprint Planning & Milestone Management

Status: review

## Story

As a PM (Shifu),
I want to create sprint milestones scoped to specific modules based on dependency analysis,
So that sprints respect subsystem dependencies and the team works in a logical migration order.

## Acceptance Criteria

1. **AC1: Create Dependency-Aware Sprint Milestone**
   - Given module Issues exist and Po's dependency analysis has produced a migration order
   - When the PM creates a sprint milestone
   - Then the milestone is scoped to a specific set of modules based on the migration order
   - And FR47 is satisfied

2. **AC2: Assign Issues Respecting Dependencies**
   - Given a sprint milestone exists
   - When the PM assigns module Issues to the milestone
   - Then Issues are assigned respecting subsystem dependencies (shared services before consumers)
   - And FR48 is satisfied

3. **AC3: View Milestone Progress (Burndown)**
   - Given a sprint milestone has assigned Issues
   - When the PM views the milestone
   - Then a burndown is visible showing open vs closed module Issues within that sprint
   - And FR49 is satisfied

4. **AC4: Complexity-Informed Sprint Planning**
   - Given modules have complexity labels
   - When the PM plans a sprint
   - Then complexity labels on Issues inform sprint capacity decisions

## Tasks / Subtasks

- [x] Task 1: Add milestone assignment to `gitlab_client.py` (AC: #1, #2)
  - [x] 1.1: Implement `assign_to_milestone(project_id, issue_iid, milestone_id)` — assigns Issue to milestone
  - [x] 1.2: Implement `list_milestones(project_id, state)` — list milestones with optional state filter
  - [x] 1.3: Implement `get_milestone(project_id, milestone_id)` — fetch milestone details
  - [x] 1.4: All methods use `asyncio.to_thread()` and return structured results

- [x] Task 2: Add milestone query/burndown to `gitlab_client.py` (AC: #3, #4)
  - [x] 2.1: Implement `get_milestone_burndown(project_id, milestone_id)` — returns total Issues, open count, closed count, Issues by complexity label
  - [x] 2.2: Query Issues assigned to milestone via `project.issues.list(milestone=title, state='all')`
  - [x] 2.3: Calculate capacity from complexity labels: Low=1, Medium=2, High=3 units
  - [x] 2.4: Return structured burndown data via `make_result()`

- [x] Task 3: Add MCP tools to `server.py` (AC: #1, #2, #3)
  - [x] 3.1: Add `assign_to_milestone(project_id, issue_iid, milestone_id)` tool
  - [x] 3.2: Add `get_milestone_burndown(project_id, milestone_id)` tool — not in original PRD tool list but needed for FR49 burndown view
  - [x] 3.3: Thin wrappers with per-tool try/except

- [x] Task 4: Write comprehensive tests (AC: #1, #2, #3, #4)
  - [x] 4.1: Test milestone assignment — Issue receives milestone_id
  - [x] 4.2: Test burndown calculation — correct open/closed counts
  - [x] 4.3: Test complexity-based capacity — Low=1, Medium=2, High=3
  - [x] 4.4: Test error cases — missing milestone, missing Issue
  - [x] 4.5: Update mock fixtures for milestone operations
  - [x] 4.6: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **All milestone logic in gitlab_client.py** — extend existing class
- **create_milestone already exists from Story 2.2** — this story adds assignment and query
- **Tool name**: `assign_to_milestone` matches PRD exactly
- **Burndown is calculated, not stored**: Query GitLab Issues by milestone and compute open/closed/complexity in code

### Complexity Capacity Mapping

```python
COMPLEXITY_CAPACITY = {
    "Complexity::Low": 1,
    "Complexity::Medium": 2,
    "Complexity::High": 3,
}
```

### python-gitlab Milestone API

```python
# Assign Issue to milestone
issue = project.issues.get(issue_iid)
issue.milestone_id = milestone.id
issue.save()

# List Issues in milestone
issues = project.issues.list(milestone=milestone.title, state='all')

# Milestone details
milestone = project.milestones.get(milestone_id)
# milestone.iid, milestone.title, milestone.state
```

### Previous Stories Context

- Story 2.2: `create_milestone()` method exists in `gitlab_client.py`
- Story 2.3: `create_issue()`, `get_issue()`, `list_issues()` exist

### Files to MODIFY

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | Add assign_to_milestone, list_milestones, get_milestone, get_milestone_burndown |
| `mcp-servers/gitlab_mcp/server.py` | Add assign_to_milestone, get_milestone_burndown tools |
| `tests/gitlab_mcp/test_gitlab_client.py` | Add milestone assignment + burndown tests |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | Add mock milestone + Issue responses |

### Dependencies

- Story 2.1 (core + auth)
- Story 2.2 (milestone creation)
- Story 2.3 (Issue creation with complexity labels)
- Po's dependency analysis output (consumed for migration ordering — not produced here)

### Functional Requirements Satisfied

- **FR47**: PM can create sprint milestones scoped to modules by migration order
- **FR48**: PM can assign Issues to milestones respecting dependencies
- **FR49**: PM can view milestone burndown (open vs closed Issues)

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.4]
- [Source: documents/planning-artifacts/prd.md — FR47, FR48, FR49]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- Milestone assignment, listing, detail retrieval
- Burndown calculation with complexity capacity (Low=1, Med=2, High=3)
- 6 new tests, 130 total passing

### File List
- `mcp-servers/gitlab_mcp/gitlab_client.py` — MODIFIED: Added assign_to_milestone, list_milestones, get_milestone, get_milestone_burndown
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added 2 new tools (assign_to_milestone, get_milestone_burndown)
- `tests/gitlab_mcp/test_gitlab_client.py` — MODIFIED: Added 6 milestone + burndown tests

### Change Log
- 2026-03-07: Story 2.4 implemented — Milestone assignment, burndown with complexity capacity, 6 new tests
