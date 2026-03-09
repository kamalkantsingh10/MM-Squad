# Step 7: Run Validations and Tests

## CONTEXT BOUNDARIES:
- Implementation and tests are in place from steps 5–6
- Full story file with all ACs is in context
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- STOP and fix before continuing if any tests fail — do not proceed with red tests

## YOUR TASK:

Determine how to run tests for this repo (infer test framework from project structure).

Run all existing tests to ensure no regressions.

Run the new tests to verify implementation correctness.

Run linting and code quality checks if configured in project.

Validate implementation meets ALL story acceptance criteria.

- If regression tests fail → STOP and fix before continuing — identify breaking changes immediately
- If new tests fail → STOP and fix before continuing — ensure implementation correctness

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-08-validate-and-mark-complete.md`
