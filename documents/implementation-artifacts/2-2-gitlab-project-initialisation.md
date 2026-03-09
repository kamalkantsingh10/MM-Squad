# Story 2.2: GitLab Project Initialisation

Status: review

## Story

As a PM (Shifu),
I want to initialise a GitLab project with the standard label taxonomy, milestone structure, and pipeline stage board,
So that the modernisation engagement has a properly configured tracking structure from day one.

## Acceptance Criteria

1. **AC1: Create Pipeline Stage Labels**
   - Given gitlab-mcp is running and authenticated
   - When the PM invokes the project initialisation workflow
   - Then the following pipeline stage labels are created: `Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`
   - And the following complexity labels are created: `Complexity::Low`, `Complexity::Medium`, `Complexity::High`
   - And the following status labels are created: `In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`
   - And FR40 is satisfied

2. **AC2: Create Engagement Phase Milestones**
   - Given labels have been created
   - When the PM creates the milestone structure
   - Then milestones are created for each engagement phase (configurable per engagement)
   - And FR41 is satisfied

3. **AC3: Create Pipeline Stage Board**
   - Given labels and milestones exist
   - When the PM creates the issue board
   - Then a board is created with columns mapped to pipeline stages: In-Analysis, Awaiting-Review, In-Migration, Blocked, Done
   - And FR42 is satisfied

4. **AC4: Safe Re-initialization (Idempotent)**
   - Given the project is already initialised
   - When the PM re-runs project initialisation
   - Then existing labels, milestones, and boards are not duplicated
   - And the operation is idempotent

## Tasks / Subtasks

- [x] Task 1: Create `label_manager.py` — Label taxonomy management (AC: #1, #4)
  - [x] 1.1: Create `mcp-servers/gitlab_mcp/label_manager.py` with `LabelManager` class
  - [x] 1.2: Define label taxonomy constants — three groups: pipeline stage (4), complexity (3), status (5) — with names and colors
  - [x] 1.3: Implement `create_label_taxonomy(project_id)` — creates all 12 labels
  - [x] 1.4: Implement idempotency check — fetch existing labels first, skip creation if label already exists (match by name)
  - [x] 1.5: Use `asyncio.to_thread()` for all python-gitlab label API calls
  - [x] 1.6: Return `make_result()` with list of created/skipped labels and counts

- [x] Task 2: Add milestone management to `gitlab_client.py` (AC: #2, #4)
  - [x] 2.1: Implement `create_milestone(project_id, title, description, start_date, due_date)` in `gitlab_client.py`
  - [x] 2.2: Implement `create_milestone_structure(project_id, phases)` — creates milestones for a list of engagement phases
  - [x] 2.3: Implement idempotency — check existing milestones by title before creating
  - [x] 2.4: Use `asyncio.to_thread()` for all milestone API calls

- [x] Task 3: Add board management to `gitlab_client.py` (AC: #3, #4)
  - [x] 3.1: Implement `create_board(project_id, board_name)` in `gitlab_client.py`
  - [x] 3.2: Implement `create_board_lists(project_id, board_id, label_names)` — creates board columns mapped to status labels: In-Analysis, Awaiting-Review, In-Migration, Blocked, Done
  - [x] 3.3: Implement idempotency — check existing boards by name before creating
  - [x] 3.4: Use `asyncio.to_thread()` for all board API calls

- [x] Task 4: Add MCP tools to `server.py` (AC: #1, #2, #3, #4)
  - [x] 4.1: Add `init_project(project_id)` tool — orchestrates full project initialisation (labels + milestones + board)
  - [x] 4.2: Add `create_labels(project_id)` tool — creates label taxonomy only
  - [x] 4.3: Add `create_milestone(project_id, title, description, start_date, due_date)` tool
  - [x] 4.4: Add `create_board(project_id, board_name)` tool
  - [x] 4.5: All tools are thin wrappers with per-tool try/except

- [x] Task 5: Write comprehensive tests (AC: #1, #2, #3, #4)
  - [x] 5.1: Create `tests/gitlab_mcp/test_label_manager.py` — test all 12 labels created, idempotency
  - [x] 5.2: Add milestone tests to `tests/gitlab_mcp/test_gitlab_client.py` — test creation, idempotency
  - [x] 5.3: Add board tests to `tests/gitlab_mcp/test_gitlab_client.py` — test creation, column mapping, idempotency
  - [x] 5.4: Update `tests/gitlab_mcp/fixtures/mock_gitlab.py` — add mock responses for labels, milestones, boards
  - [x] 5.5: Test `init_project` orchestration — verifies all three phases run in order
  - [x] 5.6: Run full test suite — all existing + new tests pass

## Dev Notes

### Architecture Constraints

- **label_manager.py**: New domain module per architecture. Owns ALL label taxonomy logic — `server.py` only wraps
- **gitlab_client.py**: Extend with milestone + board methods. Do NOT create separate files for these — they're core GitLab operations
- **Idempotency is critical**: Every creation operation must check-before-create. Use python-gitlab's `project.labels.list()`, `project.milestones.list()`, `project.boards.list()` to check existence
- **Tool naming**: `init_project`, `create_labels`, `create_milestone`, `create_board` — verb_noun, snake_case per PRD

### Label Taxonomy — Exact Values

```python
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
```

### Board Column Order

Board columns map to STATUS_LABELS in pipeline order: In-Analysis → Awaiting-Review → In-Migration → Blocked → Done

### python-gitlab API Reference

```python
# Labels
project.labels.list()
project.labels.create({"name": "...", "color": "#..."})

# Milestones
project.milestones.list()
project.milestones.create({"title": "...", "description": "...", "start_date": "...", "due_date": "..."})

# Boards
project.boards.list()
project.boards.create({"name": "..."})
board.lists.create({"label_id": label.id})
```

### Previous Story (2.1) Context

- `gitlab_client.py` created with `GitlabClient` class — lazy auth pattern, `asyncio.to_thread()` wrapping
- `result.py` exists with `make_result/make_error/make_warning`
- `server.py` has FastMCP init and `ping_gitlab` tool
- `tests/gitlab_mcp/fixtures/mock_gitlab.py` exists — extend it, don't recreate

### Files to CREATE

| File | Purpose |
|------|---------|
| `mcp-servers/gitlab_mcp/label_manager.py` | Label taxonomy creation and management |
| `tests/gitlab_mcp/test_label_manager.py` | Label manager unit tests |

### Files to MODIFY

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | Add milestone + board methods |
| `mcp-servers/gitlab_mcp/server.py` | Add init_project, create_labels, create_milestone, create_board tools |
| `tests/gitlab_mcp/test_gitlab_client.py` | Add milestone + board tests |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | Add mock responses for labels, milestones, boards |

### Dependencies

- Story 2.1 (gitlab-mcp core + authentication) — must be complete
- `_bmad/mm/config.yaml` with `gitlab_url`
- `GITLAB_TOKEN` env var for actual connectivity

### Functional Requirements Satisfied

- **FR40**: PM can initialise a GitLab project with standard label taxonomy
- **FR41**: PM can create a standard milestone structure per engagement phase
- **FR42**: PM can create a GitLab issue board configured with columns mapped to pipeline stages

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.2]
- [Source: documents/planning-artifacts/architecture.md — gitlab_mcp package structure, label_manager.py]
- [Source: documents/planning-artifacts/prd.md — FR40, FR41, FR42]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- LabelManager with 12-label taxonomy (4 pipeline, 3 complexity, 5 status), full idempotency
- GitlabClient extended with milestone + board + board_lists methods, all idempotent
- 4 new server tools: init_project, create_labels, create_milestone, create_board
- 16 new tests (7 label + 7 client + 2 server), 114 total passing

### File List
- `mcp-servers/gitlab_mcp/label_manager.py` — NEW: Label taxonomy management
- `mcp-servers/gitlab_mcp/gitlab_client.py` — MODIFIED: Added milestone + board methods
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added 4 new tools
- `tests/gitlab_mcp/test_label_manager.py` — NEW: 7 label manager tests
- `tests/gitlab_mcp/test_gitlab_client.py` — MODIFIED: Added 7 milestone + board tests
- `tests/gitlab_mcp/test_server.py` — MODIFIED: Added 2 init_project tests
- `tests/gitlab_mcp/fixtures/mock_gitlab.py` — MODIFIED: Added make_mock_project fixture

### Change Log
- 2026-03-07: Story 2.2 implemented — Label taxonomy, milestones, boards, init_project, 16 new tests
