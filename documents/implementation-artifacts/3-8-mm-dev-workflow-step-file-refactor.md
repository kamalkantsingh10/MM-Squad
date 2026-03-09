# Story 3.8: MM Dev Workflow Step-File Refactor

Status: review

## Story

As an operator,
I want the MM dev workflows (`dev-story` and `code-review`) refactored from single `instructions.xml` files into the BMAD micro-file step architecture,
so that each workflow step is self-contained, LLM context does not bleed between steps, and individual steps are easy to maintain.

## Acceptance Criteria

1. **AC1: Both MM dev workflows use step-file architecture**
   - Given the 2 MM dev workflows currently have a single `instructions.xml`
   - When the refactor is complete
   - Then each workflow has a `steps/` subdirectory with one file per step
   - And the single `instructions.xml` file is removed
   - And `workflow.yaml` `instructions:` field points to the first step file as the entry point

2. **AC2: Step files are self-contained**
   - Given a step file is loaded by the LLM
   - When the step executes
   - Then the step file contains its own context boundaries, execution rules, and goal
   - And the step file ends with a "Proceed to:" directive pointing to the next step (or "Workflow complete" for the last step)

3. **AC3: Workflow execution is semantically equivalent**
   - Given the refactored workflows
   - When any MM dev agent executes a dev workflow
   - Then the sequence of actions, gitlab-mcp tool calls, and outputs are identical to the previous single-file version
   - And no workflow steps are lost, reordered, or semantically changed

4. **AC4: Step file naming convention**
   - Given the step files are created
   - When the operator inspects the `steps/` directory
   - Then files follow the naming pattern: `step-NN-goal-name.md` (e.g., `step-01-find-story.md`)

## Tasks / Subtasks

- [x] Task 1: Refactor `dev-story` workflow (AC: #1, #2, #3, #4)
  - [x] 1.1: Create `_bmad/mm/workflows/dev/dev-story/steps/` directory
  - [x] 1.2: Extract step 1 → `steps/step-01-find-story.md`
  - [x] 1.3: Extract step 2 → `steps/step-02-load-project-context.md`
  - [x] 1.4: Extract step 3 → `steps/step-03-detect-review-continuation.md`
  - [x] 1.5: Extract step 4 → `steps/step-04-mark-in-progress.md`
  - [x] 1.6: Extract step 5 → `steps/step-05-implement-task.md`
  - [x] 1.7: Extract step 6 → `steps/step-06-verify-test-coverage.md`
  - [x] 1.8: Extract step 7 → `steps/step-07-run-validations.md`
  - [x] 1.9: Extract step 8 → `steps/step-08-validate-and-mark-complete.md`
  - [x] 1.10: Extract step 9 → `steps/step-09-story-completion.md`
  - [x] 1.11: Extract step 10 → `steps/step-10-completion-communication.md`
  - [x] 1.12: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-01-find-story.md`
  - [x] 1.13: Delete `instructions.xml`

- [x] Task 2: Refactor `code-review` workflow (AC: #1, #2, #3, #4)
  - [x] 2.1: Create `_bmad/mm/workflows/dev/code-review/steps/` directory
  - [x] 2.2: Extract step 1 → `steps/step-01-load-story-and-discover-changes.md`
  - [x] 2.3: Extract step 2 → `steps/step-02-build-review-attack-plan.md`
  - [x] 2.4: Extract step 3 → `steps/step-03-execute-adversarial-review.md`
  - [x] 2.5: Extract step 4 → `steps/step-04-present-findings-and-fix.md`
  - [x] 2.6: Extract step 5 → `steps/step-05-update-story-status.md`
  - [x] 2.7: Update `workflow.yaml` `instructions:` to `{installed_path}/steps/step-01-load-story-and-discover-changes.md`
  - [x] 2.8: Delete `instructions.xml`

- [x] Task 3: Write tests (AC: #1, #2, #3, #4)
  - [x] 3.1: Test `steps/` directory exists for both MM dev workflows
  - [x] 3.2: Test all step files exist with correct naming convention (`step-NN-goal-name.md`)
  - [x] 3.3: Test no `instructions.xml` files remain in MM dev workflow directories
  - [x] 3.4: Test `workflow.yaml` `instructions:` field in each workflow points to a `steps/step-` path
  - [x] 3.5: Test each step file (except last) contains a "Proceed to:" directive to the next step
  - [x] 3.6: Test last step of each workflow contains "Workflow complete"
  - [x] 3.7: Test each step file has CONTEXT BOUNDARIES and EXECUTION RULES sections
  - [x] 3.8: Run full test suite — zero regressions

## Dev Notes

### Architecture — Step File Pattern

Reference: `_bmad/core/workflows/brainstorming/steps/step-01-session-setup.md` and `_bmad/mm/workflows/pm/sprint-status/steps/` (from Story 2.9).

Each step file should follow this structure:

```markdown
# Step N: <Goal Name>

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Do not assume knowledge from other steps — only what was communicated explicitly
- Critical rules from instructions.xml preamble apply throughout (target language, no specdb-mcp, etc.)

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- <any step-specific rules from the original XML step>

## YOUR TASK:

<The step's action content from the original instructions.xml <step n="N"> block — converted to natural language directives>

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-NN+1-next-goal.md`
```

For the **last step** of each workflow, replace `COMPLETION` with:
```markdown
## COMPLETION:
Workflow complete. Return to the agent's menu or await further instructions.
```

### Critical Preamble Rules to Embed in First Step

The `instructions.xml` preamble `<critical>` tags must be preserved in `step-01` of each workflow:

**dev-story step-01 must include:**
- Target language is determined by agent persona (Java/Tigress, COBOL/Viper, Python/Monkey)
- Input documents from Po's business rules and Oogway's architecture — NOT specdb-mcp
- gitlab-mcp tools (apply_label, add_comment) for progress tracking when available
- Execute continuously — do NOT stop at milestones or session boundaries

**code-review step-01 must include:**
- Adversarial reviewer mindset — find what's wrong
- Validate story file claims against actual implementation
- Find 3-10 specific issues minimum
- MM-specific: spec layer compliance, business rule preservation, COBOL construct handling
- No review of `_bmad/`, `.cursor/`, `.windsurf/`, `.claude/` directories

### Step Count Reference

| Workflow | Steps | Entry Point |
|---|---|---|
| dev-story | 01–10 | step-01-find-story.md |
| code-review | 01–05 | step-01-load-story-and-discover-changes.md |

### Updating workflow.yaml

Change only the `instructions:` line:
```yaml
# Before:
instructions: "{installed_path}/instructions.xml"

# After (dev-story):
instructions: "{installed_path}/steps/step-01-find-story.md"

# After (code-review):
instructions: "{installed_path}/steps/step-01-load-story-and-discover-changes.md"
```

### Key Implementation Rules

- **Do not change semantic content** of any step — only restructure into separate files
- The XML `<step n="X">` wrapper can be dropped; the step file IS the step
- `<action>`, `<ask>`, `<check>`, `<goto>` XML tags within steps should be preserved as natural language directives or kept as-is (LLMs understand both formats)
- `<critical>` tags from the preamble → embed their content in EXECUTION RULES of step-01
- `<anchor id="...">` in dev-story step-01 is a goto target — document this as a note in step-01

### Test Pattern

Follow `tests/test_pm_workflow_steps.py` parametrised pattern from Story 2.9. New test file: `tests/test_mm_dev_workflow_steps.py`.

### Dependencies

- Story 3.1 (dev-agent-workflows) — source files to refactor at `_bmad/mm/workflows/dev/`
- Story 2.9 (PM workflow step refactor) — establishes the pattern; use test_pm_workflow_steps.py as reference

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3]
- [Source: _bmad/mm/workflows/dev/dev-story/instructions.xml — source content to split (10 steps)]
- [Source: _bmad/mm/workflows/dev/code-review/instructions.xml — source content to split (5 steps)]
- [Source: _bmad/mm/workflows/pm/sprint-status/steps/ — step file architecture reference from Story 2.9]
- [Source: _bmad/core/workflows/brainstorming/steps/ — canonical step file pattern]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- Discovered `tests/test_dev_workflows.py::test_instructions_file_exists` checking for deleted `instructions.xml` — updated test to verify `steps/step-` path in workflow.yaml instead (story 3.1 test updated to reflect 3.8 refactor outcome)

### Completion Notes List

- Created `steps/` directories for both `dev-story` and `code-review` MM dev workflows
- Extracted all 10 `dev-story` steps into self-contained step files with CONTEXT BOUNDARIES, EXECUTION RULES, YOUR TASK, and COMPLETION sections
- Extracted all 5 `code-review` steps into self-contained step files with same structure
- Critical preamble rules embedded in step-01 of each workflow (target language, no specdb-mcp, adversarial mindset)
- Each non-last step has "Proceed to:" directive; last step has "Workflow complete"
- Updated `workflow.yaml` `instructions:` field for both workflows to point to step-01 entry point
- Deleted `instructions.xml` from both workflow directories
- Created `tests/test_mm_dev_workflow_steps.py` with 85 parametrised tests covering AC1–AC4
- Updated `tests/test_dev_workflows.py::test_instructions_file_exists` → `test_instructions_entry_point_exists` (obsolete check replaced with step-file validation)
- All 85 new tests pass; 22 pre-existing failures unchanged (zero regressions)

### File List

- `_bmad/mm/workflows/dev/dev-story/steps/step-01-find-story.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-02-load-project-context.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-03-detect-review-continuation.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-04-mark-in-progress.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-05-implement-task.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-06-verify-test-coverage.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-07-run-validations.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-08-validate-and-mark-complete.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-09-story-completion.md` (new)
- `_bmad/mm/workflows/dev/dev-story/steps/step-10-completion-communication.md` (new)
- `_bmad/mm/workflows/dev/dev-story/workflow.yaml` (modified — instructions field updated)
- `_bmad/mm/workflows/dev/dev-story/instructions.xml` (deleted)
- `_bmad/mm/workflows/dev/code-review/steps/step-01-load-story-and-discover-changes.md` (new)
- `_bmad/mm/workflows/dev/code-review/steps/step-02-build-review-attack-plan.md` (new)
- `_bmad/mm/workflows/dev/code-review/steps/step-03-execute-adversarial-review.md` (new)
- `_bmad/mm/workflows/dev/code-review/steps/step-04-present-findings-and-fix.md` (new)
- `_bmad/mm/workflows/dev/code-review/steps/step-05-update-story-status.md` (new)
- `_bmad/mm/workflows/dev/code-review/workflow.yaml` (modified — instructions field updated)
- `_bmad/mm/workflows/dev/code-review/instructions.xml` (deleted)
- `tests/test_mm_dev_workflow_steps.py` (new)
- `tests/test_dev_workflows.py` (modified — updated obsolete instructions.xml test)

### Change Log

- 2026-03-08: Implemented story 3.8 — MM dev workflow step-file refactor (dev-story: 10 steps, code-review: 5 steps)
