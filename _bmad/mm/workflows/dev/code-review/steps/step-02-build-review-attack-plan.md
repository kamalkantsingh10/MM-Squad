# Step 2: Build Review Attack Plan

## CONTEXT BOUNDARIES:
- Story file is loaded and git changes are discovered from step 1
- {story_key}, file lists, git discrepancies are available
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Adversarial mindset — assume problems exist until proven otherwise

## YOUR TASK:

Extract ALL Acceptance Criteria from story.

Extract ALL Tasks/Subtasks with completion status ([x] vs [ ]).

From File List, compile list of claimed changes.

Create review plan:
1. **AC Validation**: Verify each AC is actually implemented
2. **Task Audit**: Verify each [x] task is really done
3. **Code Quality**: Security, performance, maintainability
4. **Test Quality**: Real tests vs placeholder assertions
5. **MM-Specific**: Spec layer compliance, business rule preservation, COBOL construct handling

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-execute-adversarial-review.md`
