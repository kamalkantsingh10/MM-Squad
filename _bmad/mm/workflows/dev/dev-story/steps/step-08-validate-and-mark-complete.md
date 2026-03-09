# Step 8: Validate and Mark Task Complete ONLY When Fully Done

## CONTEXT BOUNDARIES:
- Implementation validated and tests passing from step 7
- Current task/subtask details are in context
- {story_key}, review_continuation, {pending_review_items} are available
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- NEVER mark a task complete unless ALL conditions are met — NO LYING OR CHEATING
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

**VALIDATION GATES:**
- Verify ALL tests for this task/subtask ACTUALLY EXIST and PASS 100%
- Confirm implementation matches EXACTLY what the task/subtask specifies — no extra features
- Validate that ALL acceptance criteria related to this task are satisfied
- Run full test suite to ensure NO regressions introduced

**REVIEW FOLLOW-UP HANDLING:**
If task has [AI-Review] prefix:
- Extract review item details (severity, description, related AC/file)
- Add to resolution tracking list: {resolved_review_items}
- Mark task checkbox [x] in "Tasks/Subtasks → Review Follow-ups (AI)" section
- Find matching action item in "Senior Developer Review (AI) → Action Items" section and mark [x] as resolved
- Add to Dev Agent Record → Completion Notes: "✅ Resolved review finding [{severity}]: {description}"

**MARK COMPLETE (only if ALL validation gates pass AND tests actually exist and pass):**
- Mark the task (and subtasks) checkbox with [x]
- Update File List section with ALL new, modified, or deleted files (paths relative to repo root)
- Add completion notes to Dev Agent Record summarizing what was ACTUALLY implemented and tested
- Use gitlab-mcp add_comment to log task completion (if available)

If ANY validation fails → DO NOT mark task complete — fix issues first. HALT if unable to fix.

If review_continuation == true and {resolved_review_items} is not empty:
- Add Change Log entry: "Addressed code review findings — {resolved_count} items resolved (Date: {date})"

Save the story file.

Determine if more incomplete tasks remain:
- If more tasks remain → return to step 5 (Next task)
- If no tasks remain → proceed to step 9

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-09-story-completion.md`
