# Step 3: Detect Review Continuation and Extract Review Context

## CONTEXT BOUNDARIES:
- Story file is fully loaded and parsed from step 2
- {story_key}, {story_path} are available
- Variables from workflow.yaml: {communication_language}, {user_name}
- Do not assume knowledge beyond what was passed from previous steps

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Determine if this is a fresh start or a continuation after code review

## YOUR TASK:

Check if "Senior Developer Review (AI)" section exists in the story file.
Check if "Review Follow-ups (AI)" subsection exists under Tasks/Subtasks.

If "Senior Developer Review" section EXISTS:
- Set review_continuation = true
- Extract from "Senior Developer Review (AI)" section:
  - Review outcome (Approve/Changes Requested/Blocked)
  - Review date
  - Total action items with checkboxes (count checked vs unchecked)
  - Severity breakdown (High/Med/Low counts)
- Count unchecked [ ] review follow-up tasks in "Review Follow-ups (AI)" subsection
- Store list of unchecked review items as {pending_review_items}
- Output: "⏯️ Resuming Story After Code Review — {review_outcome}, {unchecked_review_count} action items remaining"

If "Senior Developer Review" section does NOT exist:
- Set review_continuation = false
- Set {pending_review_items} = empty
- Output: "🚀 Starting Fresh Implementation — Story: {story_key}, First incomplete task: {first_task_description}"

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-mark-in-progress.md`
