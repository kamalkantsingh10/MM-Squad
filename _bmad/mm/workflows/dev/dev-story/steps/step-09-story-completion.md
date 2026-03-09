# Step 9: Story Completion and Mark for Review

## CONTEXT BOUNDARIES:
- All tasks and subtasks are marked [x]
- {story_key}, {current_sprint_status} are available
- {sprint_status} path is available from workflow.yaml
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- HALT conditions below must be checked before marking review

## YOUR TASK:

Verify ALL tasks and subtasks are marked [x] (re-scan the story document now).

Run the full regression suite (do not skip).

Confirm File List includes every changed file.

Execute enhanced definition-of-done validation:
- All tasks/subtasks marked complete with [x]
- Implementation satisfies every Acceptance Criterion
- Unit tests for core functionality added/updated
- Integration tests for component interactions added when required
- All tests pass (no regressions, new tests successful)
- Code quality checks pass (linting, static analysis if configured)
- File List includes every new/modified/deleted file (relative paths)
- Dev Agent Record contains implementation notes
- Change Log includes summary of changes
- Only permitted story sections were modified

Update the story Status to: "review"

If {sprint_status} file exists AND {current_sprint_status} != "no-sprint-tracking":
- Load the FULL file
- Find development_status key matching {story_key}
- Verify current status is "in-progress"
- Update development_status[{story_key}] = "review"
- Save file, preserving ALL comments and structure including STATUS DEFINITIONS
- Use gitlab-mcp apply_label to mark story as "review" (if available)
- Output: "✅ Story status updated to 'review' in sprint-status.yaml"

If {sprint_status} file does NOT exist OR {current_sprint_status} == "no-sprint-tracking":
- Output: "ℹ️ Story status updated to 'review' in story file (no sprint tracking configured)"

HALT conditions:
- If any task is incomplete → HALT: Complete remaining tasks before marking ready for review
- If regression failures exist → HALT: Fix regression issues before completing
- If File List is incomplete → HALT: Update File List with all changed files
- If definition-of-done validation fails → HALT: Address DoD failures before completing

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-10-completion-communication.md`
