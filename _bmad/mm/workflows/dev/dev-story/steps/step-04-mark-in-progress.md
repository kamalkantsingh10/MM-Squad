# Step 4: Mark Story In-Progress

## CONTEXT BOUNDARIES:
- {story_key}, review_continuation are available from previous steps
- {sprint_status} path is available from workflow.yaml
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Use gitlab-mcp add_comment to log story start (if available)

## YOUR TASK:

If {sprint_status} file exists:
- Load the FULL file
- Read all development_status entries to find {story_key}
- Get current status value for development_status[{story_key}]

  - If current status == "ready-for-dev" OR review_continuation == true:
    - Update the story in the sprint status report to = "in-progress"
    - Use gitlab-mcp add_comment to log story start (if available)
    - Output: "🚀 Starting work on story {story_key} — Status: ready-for-dev → in-progress"

  - If current status == "in-progress":
    - Output: "⏯️ Resuming work on story {story_key} — already marked in-progress"

  - If current status is neither ready-for-dev nor in-progress:
    - Output: "⚠️ Unexpected story status: {current_status} — continuing anyway..."

- Store {current_sprint_status} for later use

If {sprint_status} file does NOT exist:
- Output: "ℹ️ No sprint status file — story progress tracked in story file only"
- Set {current_sprint_status} = "no-sprint-tracking"

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-05-implement-task.md`
