# Mantis QA Automate - Validation Checklist

## Test Generation

- [ ] Business rule validation tests generated
- [ ] Integration tests generated (if applicable)
- [ ] Tests use standard test framework APIs
- [ ] Tests cover all HIGH priority business rules
- [ ] Tests cover 1-2 critical error cases per rule

## Test Quality

- [ ] All generated tests run successfully
- [ ] Tests have clear descriptions referencing business rule IDs
- [ ] No hardcoded waits or sleeps
- [ ] Tests are independent (no order dependency)
- [ ] Tests trace to Po's extracted business rules

## Migration Validation

- [ ] Business rule preservation verified
- [ ] COBOL construct mapping validated
- [ ] Cross-module data flow tested (if applicable)
- [ ] Structural compliance with Oogway's architecture checked

## Output

- [ ] Validation summary created
- [ ] Tests saved to appropriate directories
- [ ] Summary includes business rule coverage metrics
- [ ] Epic sign-off readiness assessed

## Quality Gate

Run the tests using your project's test command.

**Expected**: All tests pass

**Epic Sign-off**: If all HIGH priority rules validated, recommend sign-off via gitlab-mcp.
