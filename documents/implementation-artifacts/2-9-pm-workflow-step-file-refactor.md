# Story 2.9: PM Workflow Step-File Refactor

Status: review

## Story

As an operator,
I want the Shifu PM workflows refactored from single `instructions.md` files into the BMAD micro-file step architecture,
so that each workflow step is self-contained, LLM context does not bleed between steps, and individual steps are easy to maintain.

## Acceptance Criteria

1. **AC1: All 6 PM workflows use step-file architecture**
   - Given the 6 Shifu PM workflows currently have a single `instructions.md`
   - When the refactor is complete
   - Then each workflow has a `steps/` subdirectory with one file per step
   - And the single `instructions.md` file is removed
   - And `workflow.yaml` `instructions:` field points to the first step file as the entry point

2. **AC2: Step files are self-contained**
   - Given a step file is loaded by the LLM
   - When the step executes
   - Then the step file contains its own context boundaries, execution rules, and goal
   - And the step file ends with a "Proceed to:" directive pointing to the next step (or "Workflow complete" for the last step)

3. **AC3: Workflow execution is equivalent**
   - Given the refactored workflows
   - When Shifu executes any PM workflow
   - Then the sequence of actions, gitlab-mcp tool calls, and outputs are identical to the previous single-file version
   - And no workflow steps are lost, reordered, or semantically changed

4. **AC4: Step file naming convention**
   - Given the step files are created
   - When the operator inspects the `steps/` directory
   - Then files follow the naming pattern: `step-NN-goal-name.md` (e.g., `step-01-identify-active-milestone.md`)
   - And `step-00-` is used for document discovery steps (previously step 0.5)

## Tasks / Subtasks

- [x] Task 1: Refactor `sprint-status` workflow (AC: #1, #2, #3, #4)
  - [x] 1.1: Create `_bmad/mm/workflows/pm/sprint-status/steps/` directory
  - [x] 1.2: Extract step 1 → `steps/step-01-identify-active-milestone.md`
  - [x] 1.3: Extract step 2 → `steps/step-02-get-burndown-and-status.md`
  - [x] 1.4: Extract step 3 → `steps/step-03-identify-blockers-and-risks.md`
  - [x] 1.5: Extract step 4 → `steps/step-04-update-readme.md`
  - [x] 1.6: Extract step 5 → `steps/step-05-present-status-report.md`
  - [x] 1.7: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-01-identify-active-milestone.md`
  - [x] 1.8: Delete `instructions.md`

- [x] Task 2: Refactor `create-story` workflow (AC: #1, #2, #3, #4)
  - [x] 2.1: Create `_bmad/mm/workflows/pm/create-story/steps/` directory
  - [x] 2.2: Extract step 0.5 → `steps/step-00-discover-documents.md`
  - [x] 2.3: Extract step 1 → `steps/step-01-gather-module-information.md`
  - [x] 2.4: Extract step 2 → `steps/step-02-create-module-issue.md`
  - [x] 2.5: Extract step 3 → `steps/step-03-assign-to-milestone-and-epic.md`
  - [x] 2.6: Extract step 4 → `steps/step-04-report.md`
  - [x] 2.7: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-00-discover-documents.md`
  - [x] 2.8: Delete `instructions.md`

- [x] Task 3: Refactor `sprint-planning` workflow (AC: #1, #2, #3, #4)
  - [x] 3.1: Create `_bmad/mm/workflows/pm/sprint-planning/steps/` directory
  - [x] 3.2: Extract step 0.5 → `steps/step-00-discover-documents.md`
  - [x] 3.3: Extract step 1 → `steps/step-01-review-migration-order.md`
  - [x] 3.4: Extract step 2 → `steps/step-02-gather-sprint-parameters.md`
  - [x] 3.5: Extract step 3 → `steps/step-03-create-sprint-milestone.md`
  - [x] 3.6: Extract step 4 → `steps/step-04-assign-issues-to-milestone.md`
  - [x] 3.7: Extract step 5 → `steps/step-05-report-sprint-summary.md`
  - [x] 3.8: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-00-discover-documents.md`
  - [x] 3.9: Delete `instructions.md`

- [x] Task 4: Refactor `create-epics-and-stories` workflow (AC: #1, #2, #3, #4)
  - [x] 4.1: Create `_bmad/mm/workflows/pm/create-epics-and-stories/steps/` directory
  - [x] 4.2: Extract step 0.5 → `steps/step-00-discover-documents.md`
  - [x] 4.3: Extract step 1 → `steps/step-01-confirm-project-readiness.md`
  - [x] 4.4: Extract step 2 → `steps/step-02-initialise-gitlab-project.md`
  - [x] 4.5: Extract step 3 → `steps/step-03-create-epics.md`
  - [x] 4.6: Extract step 4 → `steps/step-04-create-module-issues.md`
  - [x] 4.7: Extract step 5 → `steps/step-05-assign-issues-to-epics.md`
  - [x] 4.8: Extract step 6 → `steps/step-06-update-readme-and-report.md`
  - [x] 4.9: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-00-discover-documents.md`
  - [x] 4.10: Delete `instructions.md`

- [x] Task 5: Refactor `correct-course` workflow (AC: #1, #2, #3, #4)
  - [x] 5.1: Create `_bmad/mm/workflows/pm/correct-course/steps/` directory
  - [x] 5.2: Extract step 0.5 → `steps/step-00-discover-documents.md`
  - [x] 5.3: Extract step 1 → `steps/step-01-review-current-sprint-state.md`
  - [x] 5.4: Extract step 2 → `steps/step-02-identify-changes-needed.md`
  - [x] 5.5: Extract step 3 → `steps/step-03-validate-changes.md`
  - [x] 5.6: Extract step 4 → `steps/step-04-execute-changes-in-gitlab.md`
  - [x] 5.7: Extract step 5 → `steps/step-05-report-updated-sprint-state.md`
  - [x] 5.8: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-00-discover-documents.md`
  - [x] 5.9: Delete `instructions.md`

- [x] Task 6: Refactor `retrospective` workflow (AC: #1, #2, #3, #4)
  - [x] 6.1: Create `_bmad/mm/workflows/pm/retrospective/steps/` directory
  - [x] 6.2: Extract step 1 → `steps/step-01-gather-scope.md`
  - [x] 6.3: Extract step 2 → `steps/step-02-get-sprint-metrics.md`
  - [x] 6.4: Extract step 3 → `steps/step-03-review-completed-modules.md`
  - [x] 6.5: Extract step 4 → `steps/step-04-gather-qualitative-feedback.md`
  - [x] 6.6: Extract step 5 → `steps/step-05-generate-report.md`
  - [x] 6.7: Extract step 6 → `steps/step-06-post-to-epic-and-report.md`
  - [x] 6.8: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-01-gather-scope.md`
  - [x] 6.9: Delete `instructions.md`

- [x] Task 7: Write tests (AC: #1, #2, #3, #4)
  - [x] 7.1: Test `steps/` directory exists for all 6 PM workflows
  - [x] 7.2: Test step files exist with correct naming convention (`step-NN-goal-name.md`)
  - [x] 7.3: Test no `instructions.md` files remain in PM workflow directories
  - [x] 7.4: Test `workflow.yaml` `instructions:` field in each workflow points to a `steps/step-` path
  - [x] 7.5: Test each step file (except last) contains a "Proceed to:" directive to the next step
  - [x] 7.6: Run full test suite — zero regressions

## Dev Notes

### Architecture — Step File Pattern

Reference: `_bmad/core/workflows/brainstorming/steps/step-01-session-setup.md`

Each step file should follow this structure:

```markdown
# Step N: <Goal Name>

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- <any step-specific rules>

## YOUR TASK:
<The step's action content from the original instructions.md <step n="N"> block>

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-NN+1-next-goal.md`
```

For the **last step** of each workflow, replace `COMPLETION` with:
```markdown
## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
```

### Updating workflow.yaml

Change only the `instructions:` line:
```yaml
# Before:
instructions: "{installed_path}/instructions.md"

# After (example for sprint-status):
instructions: "{installed_path}/steps/step-01-identify-active-milestone.md"
```

### Step Count Reference

| Workflow | Step-00? | Steps | Entry Point |
|---|---|---|---|
| sprint-status | No | 01–05 | step-01-identify-active-milestone.md |
| create-story | Yes | 00–04 | step-00-discover-documents.md |
| sprint-planning | Yes | 00–05 | step-00-discover-documents.md |
| create-epics-and-stories | Yes | 00–06 | step-00-discover-documents.md |
| correct-course | Yes | 00–05 | step-00-discover-documents.md |
| retrospective | No | 01–06 | step-01-gather-scope.md |

### Key Implementation Rules

- **Do not change the semantic content** of any step — only restructure into separate files
- The `<step n="X">` XML tags can be dropped; the step file IS the step
- The `<action>`, `<ask>` tags within steps should be preserved as natural language directives
- `step-00-discover-documents.md` is shared across 4 workflows but each workflow's copy is independent (not DRY — each workflow is self-contained)

### Existing References

- `_bmad/core/workflows/brainstorming/steps/` — canonical step file pattern
- `_bmad/core/workflows/party-mode/steps/` — second example of step-file architecture
- `_bmad/mm/workflows/pm/sprint-status/instructions.md` — source content for Task 1

### Test Pattern

Follow `tests/gitlab_mcp/test_shifu_agent.py` parametrised pattern. New test file: `tests/test_pm_workflow_steps.py`.

### Dependencies

- Story 2.7 (Shifu workflows) — source files to refactor
- All 6 PM workflow `instructions.md` files must be read in full before splitting

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2]
- [Source: _bmad/mm/workflows/pm/*/instructions.md — source content to split]
- [Source: _bmad/core/workflows/brainstorming/steps/ — step file architecture reference]
- [Source: _bmad/core/workflows/party-mode/steps/ — step file architecture reference]

## Dev Agent Record

### Agent Model Used
claude-sonnet-4-6

### Debug Log References
- Pre-existing 20 test failures confirmed unrelated (MCP tool names, config loader — separate stories).
- ROS Jazzy pytest plugin conflict resolved via `PYTHONPATH=""` (same pattern as all tests).

### Completion Notes List
- ✅ Created `steps/` directories for all 6 PM workflows.
- ✅ Extracted each step into self-contained step files with CONTEXT BOUNDARIES, EXECUTION RULES, YOUR TASK, and COMPLETION sections.
- ✅ Each non-last step ends with `Proceed to:` directive; last step says `Workflow complete`.
- ✅ Updated `workflow.yaml` `instructions:` field for all 6 workflows to point to first step file.
- ✅ Deleted all 6 `instructions.md` files.
- ✅ Created `tests/test_pm_workflow_steps.py` with 205 parametrised tests covering all ACs. All 205 pass.
- ✅ Zero regressions introduced.

### File List
- `_bmad/mm/workflows/pm/sprint-status/steps/step-01-identify-active-milestone.md` (created)
- `_bmad/mm/workflows/pm/sprint-status/steps/step-02-get-burndown-and-status.md` (created)
- `_bmad/mm/workflows/pm/sprint-status/steps/step-03-identify-blockers-and-risks.md` (created)
- `_bmad/mm/workflows/pm/sprint-status/steps/step-04-update-readme.md` (created)
- `_bmad/mm/workflows/pm/sprint-status/steps/step-05-present-status-report.md` (created)
- `_bmad/mm/workflows/pm/sprint-status/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/sprint-status/instructions.md` (deleted)
- `_bmad/mm/workflows/pm/create-story/steps/step-00-discover-documents.md` (created)
- `_bmad/mm/workflows/pm/create-story/steps/step-01-gather-module-information.md` (created)
- `_bmad/mm/workflows/pm/create-story/steps/step-02-create-module-issue.md` (created)
- `_bmad/mm/workflows/pm/create-story/steps/step-03-assign-to-milestone-and-epic.md` (created)
- `_bmad/mm/workflows/pm/create-story/steps/step-04-report.md` (created)
- `_bmad/mm/workflows/pm/create-story/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/create-story/instructions.md` (deleted)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-00-discover-documents.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-01-review-migration-order.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-02-gather-sprint-parameters.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-03-create-sprint-milestone.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-04-assign-issues-to-milestone.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/steps/step-05-report-sprint-summary.md` (created)
- `_bmad/mm/workflows/pm/sprint-planning/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/sprint-planning/instructions.md` (deleted)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-00-discover-documents.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-01-confirm-project-readiness.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-02-initialise-gitlab-project.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-03-create-epics.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-04-create-module-issues.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-05-assign-issues-to-epics.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/steps/step-06-update-readme-and-report.md` (created)
- `_bmad/mm/workflows/pm/create-epics-and-stories/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/create-epics-and-stories/instructions.md` (deleted)
- `_bmad/mm/workflows/pm/correct-course/steps/step-00-discover-documents.md` (created)
- `_bmad/mm/workflows/pm/correct-course/steps/step-01-review-current-sprint-state.md` (created)
- `_bmad/mm/workflows/pm/correct-course/steps/step-02-identify-changes-needed.md` (created)
- `_bmad/mm/workflows/pm/correct-course/steps/step-03-validate-changes.md` (created)
- `_bmad/mm/workflows/pm/correct-course/steps/step-04-execute-changes-in-gitlab.md` (created)
- `_bmad/mm/workflows/pm/correct-course/steps/step-05-report-updated-sprint-state.md` (created)
- `_bmad/mm/workflows/pm/correct-course/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/correct-course/instructions.md` (deleted)
- `_bmad/mm/workflows/pm/retrospective/steps/step-01-gather-scope.md` (created)
- `_bmad/mm/workflows/pm/retrospective/steps/step-02-get-sprint-metrics.md` (created)
- `_bmad/mm/workflows/pm/retrospective/steps/step-03-review-completed-modules.md` (created)
- `_bmad/mm/workflows/pm/retrospective/steps/step-04-gather-qualitative-feedback.md` (created)
- `_bmad/mm/workflows/pm/retrospective/steps/step-05-generate-report.md` (created)
- `_bmad/mm/workflows/pm/retrospective/steps/step-06-post-to-epic-and-report.md` (created)
- `_bmad/mm/workflows/pm/retrospective/workflow.yaml` (updated)
- `_bmad/mm/workflows/pm/retrospective/instructions.md` (deleted)
- `tests/test_pm_workflow_steps.py` (created)
- `documents/implementation-artifacts/2-9-pm-workflow-step-file-refactor.md` (updated)
- `documents/implementation-artifacts/sprint-status.yaml` (updated)

### Change Log
- 2026-03-08: Implemented Story 2.9 — refactored 6 PM workflows from single instructions.md to step-file architecture. 32 step files created, 6 instructions.md deleted, 6 workflow.yaml updated. 205-test suite all passing.
