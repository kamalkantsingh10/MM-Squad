# Step 5: Implement Task Following Red-Green-Refactor Cycle

## CONTEXT BOUNDARIES:
- Story file is loaded; current task/subtask is identified
- {story_key}, {current_sprint_status}, {pending_review_items} are available
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- FOLLOW THE STORY FILE TASKS/SUBTASKS SEQUENCE EXACTLY AS WRITTEN — NO DEVIATION
- NEVER implement anything not mapped to a specific task/subtask in the story file
- NEVER proceed to next task until current task/subtask is complete AND tests pass
- Execute continuously without pausing until all tasks/subtasks are complete or explicit HALT condition
- Do NOT propose to pause for review until Step 9 completion gates are satisfied
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Review the current task/subtask from the story file — this is your authoritative implementation guide.
Plan implementation following red-green-refactor cycle.

**RED PHASE:**
- Write FAILING tests first for the task/subtask functionality
- Confirm tests fail before implementation — this validates test correctness

**GREEN PHASE:**
- Implement MINIMAL code to make tests pass
- Run tests to confirm they now pass
- Handle error conditions and edge cases as specified in task/subtask

**REFACTOR PHASE:**
- Improve code structure while keeping tests green
- Ensure code follows architecture patterns and coding standards from Dev Notes

Document technical approach and decisions in Dev Agent Record.

HALT conditions:
- If new dependencies required beyond story specifications → HALT: "Additional dependencies need user approval"
- If 3 consecutive implementation failures occur → HALT and request guidance
- If required configuration is missing → HALT: "Cannot proceed without necessary configuration files"

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-06-verify-test-coverage.md`
