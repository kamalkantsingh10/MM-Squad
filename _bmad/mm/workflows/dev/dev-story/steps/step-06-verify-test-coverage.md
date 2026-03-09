# Step 6: Verify Test Coverage Completeness Across All ACs

## CONTEXT BOUNDARIES:
- Implementation for the current task is complete and tests pass
- Full story file is in context with all Acceptance Criteria
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Tests must exist for EVERY acceptance criterion, not just the current task
- No test is a placeholder (e.g., `assert True`, empty test body, `pass`)
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Review ALL Acceptance Criteria from the story file.

For each AC, verify at least one test explicitly covers it — trace test names to AC IDs.

Identify any AC without test coverage and write the missing tests now.

Verify edge cases from Dev Notes are covered (null inputs, boundary values, error paths).

Confirm no test is a placeholder (e.g., `assert True`, empty test body, `pass`).

If any AC lacks test coverage → write missing tests before proceeding to step 7.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-07-run-validations.md`
