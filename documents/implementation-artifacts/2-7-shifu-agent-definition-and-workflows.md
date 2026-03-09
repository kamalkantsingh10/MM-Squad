# Story 2.7: Shifu Agent Definition & Workflows

Status: review

## Story

As an operator,
I want the Shifu agent (PM+SM) fully authored with persona, menu, and workflow step files,
So that Shifu can be invoked via `/bmad-agent-mm-shifu` and orchestrate all GitLab delivery management operations.

## Acceptance Criteria

1. **AC1: Shifu Agent Definition File**
   - Given the Shifu agent definition exists at `_bmad/mm/agents/shifu.md`
   - When the operator inspects the file
   - Then it contains: combined PM+SM persona, GitLab-native project management identity, migration status tracking capability
   - And it declares access to `gitlab-mcp` MCP server
   - And the menu lists all delivery management workflows

2. **AC2: Workflow Step Files Authored**
   - Given the Shifu workflow step files exist under `_bmad/mm/workflows/pm/`
   - When the operator inspects the workflows
   - Then the following workflows are fully authored: create-epics-and-stories, sprint-planning, create-story, sprint-status, correct-course, retrospective
   - And each workflow follows BMAD workflow architecture (workflow.yaml or workflow.md + steps/)

3. **AC3: Agent Installation & Invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-shifu`
   - Then Shifu loads, presents its menu, and responds in character
   - And all menu items map to the authored workflows

4. **AC4: Workflow Execution with gitlab-mcp**
   - Given Shifu is active and gitlab-mcp is running
   - When the PM selects any delivery management workflow
   - Then Shifu can execute the workflow using gitlab-mcp tools
   - And all GitLab operations follow the structured result format

## Tasks / Subtasks

- [x] Task 1: Create Shifu agent definition (AC: #1, #3)
  - [x] 1.1: Create `_bmad/mm/agents/shifu.md` following BMAD agent format
  - [x] 1.2: Define combined PM+SM persona: pragmatic, detail-oriented, GitLab-native project management identity
  - [x] 1.3: Define capabilities: sprint planning, dependency tracking, progress monitoring, review gate management
  - [x] 1.4: Declare `gitlab-mcp` MCP server access
  - [x] 1.5: Define menu with all 6 workflows + standard items (MH, CH, PM, DA)
  - [x] 1.6: Include activation steps following BMAD agent activation pattern

- [x] Task 2: Create workflow directory structure (AC: #2)
  - [x] 2.1: Create `_bmad/mm/workflows/pm/` directory
  - [x] 2.2: Create subdirectories for each workflow

- [x] Task 3: Author `create-epics-and-stories` workflow (AC: #2, #4)
  - [x] 3.1: Create `workflow.yaml`
  - [x] 3.2: Steps: gather info → init_project → create Epics → create Issues → assign labels → report
  - [x] 3.3: References gitlab-mcp tools: `init_project`, `create_epic`, `create_issue`, `apply_label`

- [x] Task 4: Author `sprint-planning` workflow (AC: #2, #4)
  - [x] 4.1: Create `workflow.yaml`
  - [x] 4.2: Steps: review migration order → gather params → create milestone → assign Issues → report capacity
  - [x] 4.3: References gitlab-mcp tools: `create_milestone`, `assign_to_milestone`, `get_milestone_burndown`

- [x] Task 5: Author `create-story` workflow (AC: #2, #4)
  - [x] 5.1: Create `workflow.yaml`
  - [x] 5.2: Steps: gather module info → create Issue → assign to milestone → report
  - [x] 5.3: References gitlab-mcp tools: `create_issue`, `apply_label`, `assign_to_milestone`

- [x] Task 6: Author `sprint-status` workflow (AC: #2, #4)
  - [x] 6.1: Create `workflow.yaml`
  - [x] 6.2: Steps: identify milestone → get burndown → identify blockers → update dashboard → report
  - [x] 6.3: References gitlab-mcp tools: `get_milestone_burndown`, `update_readme`

- [x] Task 7: Author `correct-course` workflow (AC: #2, #4)
  - [x] 7.1: Create `workflow.yaml`
  - [x] 7.2: Steps: review sprint → identify changes → reassign → update labels → document → report
  - [x] 7.3: References gitlab-mcp tools: `assign_to_milestone`, `apply_label`, `add_comment`

- [x] Task 8: Author `retrospective` workflow (AC: #2, #4)
  - [x] 8.1: Create `workflow.yaml`
  - [x] 8.2: Steps: gather scope → get burndown → list completed → gather learnings → generate report → post to Epic
  - [x] 8.3: References gitlab-mcp tools: `get_milestone_burndown`, `add_comment`

- [x] Task 9: Update module-help.csv (AC: #3)
  - [x] 9.1: Verified — `_bmad/mm/module-help.csv` already has Shifu agent entry and all 6 workflow entries
  - [x] 9.2: No updates needed — all entries correct

- [x] Task 10: Write tests (AC: #1, #2, #3)
  - [x] 10.1: Test Shifu agent file exists and contains required sections (persona, menu, activation)
  - [x] 10.2: Test all 6 workflow directories and files exist
  - [x] 10.3: Test workflow files reference valid gitlab-mcp tools
  - [x] 10.4: Test module-help.csv has correct entries
  - [x] 10.5: Run full test suite — 179 tests, zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/shifu.md`** — follows BMAD agent file format exactly
- **Workflows at `_bmad/mm/workflows/pm/`** — PM workflows directory per architecture
- **BMAD workflow format**: Each workflow needs a `workflow.yaml` (or `workflow.md`) — reference existing BMM workflows in `_bmad/bmm/workflows/` as templates
- **This is primarily YAML/markdown authoring** — no Python code changes. The MCP tools already exist from Stories 2.1-2.6
- **Shifu does NOT access specdb-mcp** — only gitlab-mcp for all GitLab operations

### BMAD Agent File Format Reference

Use existing agents as templates:
- `_bmad/bmm/agents/sm.md` — Scrum Master (Bob) — closest match for format
- `_bmad/bmm/agents/pm.md` — PM agent — for PM persona reference

Key sections in agent .md file:
```xml
<agent id="shifu.agent.yaml" name="Shifu" title="PM + SM Agent" icon="🐼">
  <activation>...</activation>
  <persona>
    <role>PM + SM — Delivery Orchestrator</role>
    <identity>GitLab-native project management...</identity>
    <communication_style>Pragmatic, detail-oriented...</communication_style>
  </persona>
  <menu>
    <item cmd="..." workflow="...">[XX] Workflow Name</item>
    ...
  </menu>
</agent>
```

### Shifu Menu Items

1. [MH] Redisplay Menu Help
2. [CH] Chat with the Agent
3. [PI] Project Initialisation — create-epics-and-stories workflow
4. [SP] Sprint Planning — sprint-planning workflow
5. [CS] Create Story — create-story workflow (module Issue)
6. [SS] Sprint Status — sprint-status workflow
7. [CC] Course Correction — correct-course workflow
8. [RR] Retrospective — retrospective workflow
9. [PM] Start Party Mode
10. [DA] Dismiss Agent

### Workflow YAML Format Reference

Reference existing BMM workflows in `_bmad/bmm/workflows/4-implementation/` for structure:
- `workflow.yaml` — config, variables, instructions path, template path
- `instructions.xml` — step-by-step execution instructions
- `template.md` — output template (if producing a document)

For Shifu workflows, most are **action-workflows** (template: false) — they execute gitlab-mcp tools rather than producing documents.

### Party Roster

Shifu is already listed in `_bmad/mm/teams/default-party.csv` from Story 1.2 — verify entry is correct.

### Previous Stories Context

- Stories 2.1-2.6: All gitlab-mcp tools exist and are tested
- Story 1.2: `_bmad/mm/config.yaml`, `module-help.csv`, `default-party.csv` created
- Story 1.4: IDE configuration with MCP server registration

### Files to CREATE

| File | Purpose |
|------|---------|
| `_bmad/mm/agents/shifu.md` | Shifu PM+SM agent definition |
| `_bmad/mm/workflows/pm/create-epics-and-stories/workflow.yaml` | Project init workflow |
| `_bmad/mm/workflows/pm/sprint-planning/workflow.yaml` | Sprint planning workflow |
| `_bmad/mm/workflows/pm/create-story/workflow.yaml` | Module Issue creation workflow |
| `_bmad/mm/workflows/pm/sprint-status/workflow.yaml` | Sprint status view workflow |
| `_bmad/mm/workflows/pm/correct-course/workflow.yaml` | Course correction workflow |
| `_bmad/mm/workflows/pm/retrospective/workflow.yaml` | Sprint retrospective workflow |

### Files to MODIFY

| File | Changes |
|------|---------|
| `_bmad/mm/module-help.csv` | Verify/update Shifu + workflow entries |

### Dependencies

- Stories 2.1-2.6 (all gitlab-mcp tools must be implemented)
- Epic 1 Story 1.2 (MM module config + registry)
- Epic 1 Story 1.4 (IDE configuration)
- BMAD agent framework (core module)

### Functional Requirements Satisfied

- Enables all FR40-FR56 through Shifu agent UI/UX
- Provides PM workflows for project initialization, sprint planning, progress tracking, sign-off

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.7]
- [Source: documents/planning-artifacts/architecture.md — Shifu agent definition, workflow directory]
- [Source: _bmad/bmm/agents/sm.md — BMAD agent file format reference]
- [Source: _bmad/bmm/workflows/4-implementation/ — BMAD workflow format reference]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- None

### Completion Notes List
- Shifu agent definition with PM+SM persona, gitlab-mcp access, 10 menu items
- 6 workflow YAML files: create-epics-and-stories, sprint-planning, create-story, sprint-status, correct-course, retrospective
- All workflows are action-workflows (template: false) referencing gitlab-mcp tools
- module-help.csv already had all required entries from Story 1.2
- 33 new tests (7 agent + 24 workflow + 2 CSV), 179 total passing

### File List
- `_bmad/mm/agents/shifu.md` — NEW: Shifu PM+SM agent definition
- `_bmad/mm/workflows/pm/create-epics-and-stories/workflow.yaml` — NEW: Project init workflow
- `_bmad/mm/workflows/pm/sprint-planning/workflow.yaml` — NEW: Sprint planning workflow
- `_bmad/mm/workflows/pm/create-story/workflow.yaml` — NEW: Module Issue creation workflow
- `_bmad/mm/workflows/pm/sprint-status/workflow.yaml` — NEW: Sprint status workflow
- `_bmad/mm/workflows/pm/correct-course/workflow.yaml` — NEW: Course correction workflow
- `_bmad/mm/workflows/pm/retrospective/workflow.yaml` — NEW: Retrospective workflow
- `tests/gitlab_mcp/test_shifu_agent.py` — NEW: Agent + workflow tests

### Change Log
- 2026-03-07: Story 2.7 implemented — Shifu agent definition, 6 workflows, 33 new tests
