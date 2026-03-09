# Story 3.7: MM Dev Workflow Slash Command Registration

Status: review

## Story

As an operator,
I want the MM dev workflows (`dev-story` and `code-review`) registered as direct Claude Code slash commands,
so that I can invoke any MM dev workflow without navigating through an agent menu.

## Acceptance Criteria

1. **AC1: `bmad-mm-dev-story` Claude Code command exists**
   - Given the `.claude/commands/` directory is the Claude Code slash command location
   - When the operator opens a Claude Code session in this project
   - Then `/bmad-mm-dev-story` is available as a slash command
   - And it loads and executes `_bmad/mm/workflows/dev/dev-story/workflow.yaml`
   - And it follows the same `<steps CRITICAL="TRUE">` activation format as `bmad-bmm-dev-story.md`

2. **AC2: `bmad-mm-code-review` Claude Code command exists**
   - Given the `.claude/commands/` directory is the Claude Code slash command location
   - When the operator opens a Claude Code session in this project
   - Then `/bmad-mm-code-review` is available as a slash command
   - And it loads and executes `_bmad/mm/workflows/dev/code-review/workflow.yaml`
   - And it follows the same `<steps CRITICAL="TRUE">` activation format as `bmad-bmm-code-review.md`

3. **AC3: Commands reference the correct MM workflow paths**
   - Given the slash command files exist
   - When any MM dev workflow is invoked
   - Then the activation instructions reference `_bmad/mm/workflows/dev/` (not `_bmad/bmm/workflows/`)
   - And the `workflow.xml` core OS is loaded from `{project-root}/_bmad/core/tasks/workflow.xml`

## Tasks / Subtasks

- [x] Task 1: Create Claude Code slash command for dev-story (AC: #1, #3)
  - [x] 1.1: Create `.claude/commands/bmad-mm-dev-story.md`
  - [x] 1.2: Verify frontmatter has `name` and `description`
  - [x] 1.3: Verify activation steps reference `_bmad/mm/workflows/dev/dev-story/workflow.yaml`

- [x] Task 2: Create Claude Code slash command for code-review (AC: #2, #3)
  - [x] 2.1: Create `.claude/commands/bmad-mm-code-review.md`
  - [x] 2.2: Verify frontmatter has `name` and `description`
  - [x] 2.3: Verify activation steps reference `_bmad/mm/workflows/dev/code-review/workflow.yaml`

- [x] Task 3: Write tests (AC: #1, #2, #3)
  - [x] 3.1: Test `.claude/commands/bmad-mm-dev-story.md` exists
  - [x] 3.2: Test `.claude/commands/bmad-mm-code-review.md` exists
  - [x] 3.3: Test each command file has valid frontmatter (`name`, `description`)
  - [x] 3.4: Test `bmad-mm-dev-story.md` references `_bmad/mm/workflows/dev/dev-story/workflow.yaml`
  - [x] 3.5: Test `bmad-mm-code-review.md` references `_bmad/mm/workflows/dev/code-review/workflow.yaml`
  - [x] 3.6: Test each command has the `<steps CRITICAL="TRUE">` activation block
  - [x] 3.7: Test each command references `_bmad/core/tasks/workflow.xml`
  - [x] 3.8: Run full test suite — zero regressions

## Dev Notes

### File Format Reference

Follow `bmad-bmm-dev-story.md` exactly — a direct workflow invocation command (not an agent command):

```markdown
---
name: 'dev-story'
description: 'Execute story implementation... Use when the user says "dev this story [story file]"'
---

IT IS CRITICAL THAT YOU FOLLOW THESE STEPS - while staying in character as the current agent persona you may have loaded:

<steps CRITICAL="TRUE">
1. Always LOAD the FULL {project-root}/_bmad/core/tasks/workflow.xml
2. READ its entire contents - this is the CORE OS for EXECUTING the specific workflow-config {project-root}/_bmad/mm/workflows/dev/dev-story/workflow.yaml
3. Pass the yaml path {project-root}/_bmad/mm/workflows/dev/dev-story/workflow.yaml as 'workflow-config' parameter to the workflow.xml instructions
4. Follow workflow.xml instructions EXACTLY as written to process and follow the specific workflow config and its instructions
5. Save outputs after EACH section when generating any documents from templates
</steps>
```

### Key Difference from Agent Commands

| Type | Example | What it does |
|------|---------|--------------|
| Agent command | `bmad-agent-mm-tigress.md` | Loads an agent persona + full menu |
| Workflow command | `bmad-mm-dev-story.md` | Directly invokes a specific workflow |

### Reference Files

- `.claude/commands/bmad-bmm-dev-story.md` — BMM dev-story command (exact format to follow)
- `.claude/commands/bmad-bmm-code-review.md` — BMM code-review command (exact format to follow)
- `_bmad/mm/workflows/dev/dev-story/workflow.yaml` — target workflow
- `_bmad/mm/workflows/dev/code-review/workflow.yaml` — target workflow

### Test Pattern

Follow `tests/test_ide_slash_commands.py` parametrised pattern. New test file: `tests/test_mm_dev_workflow_commands.py`.

### No `.github/agents/` Files Required

Workflow slash commands (unlike agent commands) do not have GitHub Copilot agent counterparts — there is no `bmad-bmm-dev-story.agent.md` in `.github/agents/` in the BMM module. Do not create Copilot agent files for workflow commands.

### Dependencies

- Story 3.1 (dev-agent-workflows) — source workflows must exist at `_bmad/mm/workflows/dev/`
- `.claude/commands/bmad-bmm-dev-story.md` and `bmad-bmm-code-review.md` — format reference

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3]
- [Source: .claude/commands/bmad-bmm-dev-story.md — exact format to replicate]
- [Source: .claude/commands/bmad-bmm-code-review.md — exact format to replicate]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — straightforward file creation, no blockers.

### Completion Notes List

- Created `.claude/commands/bmad-mm-dev-story.md` following exact format of `bmad-bmm-dev-story.md`, pointing to `_bmad/mm/workflows/dev/dev-story/workflow.yaml`
- Created `.claude/commands/bmad-mm-code-review.md` following exact format of `bmad-bmm-code-review.md`, pointing to `_bmad/mm/workflows/dev/code-review/workflow.yaml`
- Created `tests/test_mm_dev_workflow_commands.py` with 12 parametrised tests covering AC1, AC2, AC3: file existence, frontmatter, workflow path references, core OS reference, activation block
- All 12 new tests pass; pre-existing 22 failures are unrelated (stories already in review)
- No Copilot agent files created per Dev Notes spec

### File List

- `.claude/commands/bmad-mm-dev-story.md` (new)
- `.claude/commands/bmad-mm-code-review.md` (new)
- `tests/test_mm_dev_workflow_commands.py` (new)

### Change Log

- 2026-03-08: Implemented story 3.7 — MM dev workflow slash command registration (bmad-mm-dev-story, bmad-mm-code-review)
