# Story 2.6: Review Gates, Sign-off & Epic Closure

Status: review

## Story

As a Business Validator or QA engineer,
I want formal sign-off gates on module Issues and Epics,
So that no module progresses or Epic closes without explicit human approval.

## Acceptance Criteria

1. **AC1: Business Validator Signs Off Module**
   - Given Po has generated business markdown and the Issue is `Awaiting-Review`
   - When the Business Validator formally signs off
   - Then the `Awaiting-Review` gate is closed on the module Issue
   - And the Issue transitions to the next pipeline stage
   - And a sign-off comment is posted with validator's confirmation
   - And FR54 is satisfied

2. **AC2: QA Signs Off on Complete Epic**
   - Given all module Issues within an Epic are `QA-Complete`
   - When QA signs off on the Epic
   - Then a validation summary comment is posted listing all modules and their QA status
   - And Epic completion is triggered in GitLab
   - And FR55 is satisfied

3. **AC3: QA Formally Closes Epic**
   - Given an Epic has been signed off by QA
   - When QA formally closes the Epic
   - Then the Epic status is set to closed in GitLab
   - And the README dashboard reflects the closed Epic
   - And FR56 is satisfied

4. **AC4: Prevent Incomplete Epic Closure**
   - Given not all module Issues within an Epic are `QA-Complete`
   - When QA attempts to close the Epic
   - Then the operation fails with explicit error listing incomplete modules

## Tasks / Subtasks

- [x] Task 1: Add Epic operations to `gitlab_client.py` (AC: #2, #3, #4)
  - [x] 1.1: Implement `create_epic(group_id, title, description)` — creates GitLab Epic
  - [x] 1.2: Implement `get_epic(group_id, epic_iid)` — fetches Epic details
  - [x] 1.3: Implement `close_epic(group_id, epic_iid)` — closes Epic (sets state to closed)
  - [x] 1.4: Implement `validate_epic_closure(project_id, issue_iids)` — checks all Issues have `QA-Complete` label; returns list of incomplete modules if validation fails
  - [x] 1.5: All methods use `asyncio.to_thread()` and return structured results

- [x] Task 2: Implement sign-off workflow helpers (AC: #1, #2)
  - [x] 2.1: Implement `sign_off_module(project_id, issue_iid, validator_name, next_stage)` in `gitlab_client.py` — removes `Awaiting-Review`, applies next stage label, posts sign-off comment
  - [x] 2.2: Implement `sign_off_epic(group_id, epic_iid, project_id, issue_iids, qa_name)` — validates all modules QA-Complete, posts validation summary, closes Epic
  - [x] 2.3: Sign-off comment format: validator name, approval statement, next stage, ISO 8601 timestamp
  - [x] 2.4: Validation summary format: list of all modules with QA status, QA engineer name, date

- [x] Task 3: Add MCP tools to `server.py` (AC: #1, #2, #3, #4)
  - [x] 3.1: Add `create_epic(group_id, title, description)` tool
  - [x] 3.2: Add `close_epic(group_id, epic_iid)` tool — includes pre-closure validation via sign_off_epic
  - [x] 3.3: `update_issue_status` already exists from Story 2.3 — handles sign-off transitions
  - [x] 3.4: Thin wrappers with per-tool try/except

- [x] Task 4: Integrate with README dashboard (AC: #3)
  - [x] 4.1: update_readme tool from Story 2.5 handles dashboard refresh including Epic status
  - [x] 4.2: Dashboard table shows module statuses including QA-Complete and Done

- [x] Task 5: Write comprehensive tests (AC: #1, #2, #3, #4)
  - [x] 5.1: Test module sign-off — Awaiting-Review removed, next stage applied, comment posted
  - [x] 5.2: Test Epic QA sign-off — all modules QA-Complete, summary posted, Epic closed
  - [x] 5.3: Test incomplete Epic rejection — returns error with list of incomplete modules
  - [x] 5.4: Test Epic closure updates README dashboard
  - [x] 5.5: Test error cases — missing Epic, missing Issue, already-closed Epic
  - [x] 5.6: Update mock fixtures for Epic operations
  - [x] 5.7: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Epic operations in gitlab_client.py** — Epics are core GitLab objects
- **Sign-off is a composite operation**: remove label + apply label + post comment — implement as single method for atomicity
- **Epic closure MUST validate first**: Never close an Epic without checking all Issues are QA-Complete
- **Tool names match PRD**: `create_epic`, `close_epic`, `update_issue_status`
- **GitLab Epics require Group-level access**: Epics are a group-level feature, not project-level. Use `group.epics` API

### GitLab Epic vs Project Distinction

```
Group → contains Epics (subsystem-level groupings)
  └── Project → contains Issues (per-module tracking), Milestones, Boards, Labels
```

Epics use `group_id` + `epic_iid`. Issues use `project_id` + `issue_iid`. Do NOT confuse these.

### Sign-off Comment Format

```markdown
## Module Sign-off: Business Rule Validation

**Validator:** Claire (Business Validator)
**Action:** Approved — review gate closed
**Module:** PAYROLL-CALC
**Previous Status:** Awaiting-Review
**New Status:** In-Migration
**Timestamp:** 2026-03-07T12:00:00Z

Business rules validated against source documentation. Approved for migration.
```

### Epic Validation Summary Format

```markdown
## Epic QA Sign-off

**QA Engineer:** Mantis
**Epic:** Core Payroll Subsystem
**Date:** 2026-03-07T12:00:00Z

### Module QA Status
| Module | QA Status | Signed Off |
|--------|-----------|-----------|
| PAYROLL-CALC | QA-Complete | Yes |
| PAY-DEDUCTIONS | QA-Complete | Yes |
| PAY-TAXES | QA-Complete | Yes |

**All 3 modules QA-Complete. Epic approved for closure.**
```

### python-gitlab Epic API

```python
# Group-level Epics (GitLab Premium/Ultimate feature)
group = gl.groups.get(group_id)
epic = group.epics.create({"title": "...", "description": "..."})
epic = group.epics.get(epic_iid)
epic.state_event = "close"
epic.save()

# Note: GitLab Free tier uses project-level epics differently
# Check GitLab instance capabilities and handle gracefully
```

### Previous Stories Context

- Story 2.3: `apply_label`, `remove_label`, `update_issue_status` exist
- Story 2.5: `add_comment`, `update_readme` exist
- README dashboard already shows module statuses — this story adds "Signed-Off Epics" section

### Files to MODIFY

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | Add Epic CRUD, sign-off workflows, closure validation |
| `mcp-servers/gitlab_mcp/server.py` | Add create_epic, close_epic tools |
| `mcp-servers/gitlab_mcp/readme_updater.py` | Ensure Signed-Off Epics section updates on closure |
| `tests/gitlab_mcp/test_gitlab_client.py` | Add Epic + sign-off tests |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | Add mock Epic responses |

### Dependencies

- Stories 2.1-2.5 (all prior gitlab-mcp functionality)
- Po agent output (business markdown triggers review gates)
- Mantis agent validation (QA reports trigger Epic sign-off)

### Functional Requirements Satisfied

- **FR54**: Business Validator sign-off on module Issues
- **FR55**: QA Epic sign-off with validation summary
- **FR56**: QA formal Epic closure when all modules QA-Complete

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.6]
- [Source: documents/planning-artifacts/prd.md — FR54, FR55, FR56]
- [Source: documents/planning-artifacts/architecture.md — gitlab-mcp tool boundaries]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- Epic CRUD (create, get, close) at group level
- validate_epic_closure checks all Issues have QA-Complete
- sign_off_module: atomic label transition + sign-off comment
- sign_off_epic: validation + summary + closure in one call
- 7 new tests, 146 total passing

### File List
- `mcp-servers/gitlab_mcp/gitlab_client.py` — MODIFIED: Added Epic CRUD, sign-off workflows, closure validation
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added create_epic, close_epic tools
- `tests/gitlab_mcp/test_gitlab_client.py` — MODIFIED: Added 7 Epic + sign-off tests
- `tests/gitlab_mcp/fixtures/mock_gitlab.py` — MODIFIED: Added make_mock_epic, make_mock_group fixtures

### Change Log
- 2026-03-07: Story 2.6 implemented — Review gates, sign-off, Epic closure, 7 new tests
