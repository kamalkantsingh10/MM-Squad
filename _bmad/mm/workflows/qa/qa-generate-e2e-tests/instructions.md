# Mantis QA - Automate

**Goal**: Generate automated validation tests for migrated code, verifying business rule preservation against Po's extracted documents.

**Scope**: This workflow generates tests ONLY. It does **not** perform code review or story validation (use Code Review `CR` for that).

## Instructions

### Step 0: Detect Test Framework

Check project for existing test framework:

- Look for `package.json` or `pyproject.toml` dependencies
- Check for existing test files to understand patterns
- Use whatever test framework the project already has
- If no framework exists, suggest the recommended framework for the stack

### Step 1: Identify Features to Validate

Ask user what to test:

- Specific migrated module or component
- Directory to scan (e.g., generated code output)
- Or auto-discover features in the codebase
- Load Po's business rules documents for the target module as validation baseline

### Step 2: Generate Business Rule Validation Tests

For each business rule extracted by Po, generate tests that:

- Verify the rule is implemented in the generated/migrated code
- Test boundary conditions from the original COBOL logic
- Cover happy path + critical error cases
- Use project's existing test framework patterns
- Tag each test with the business rule ID it validates

### Step 3: Generate Integration Tests (if applicable)

For cross-module interactions, generate tests that:

- Test subsystem boundaries identified in Oogway's architecture
- Validate data flow between migrated components
- Assert structural compliance with target architecture

### Step 4: Run Tests

Execute tests to verify they pass (use project's test command).

If failures occur, fix them immediately.

### Step 5: Create Validation Summary

Output markdown summary:

```markdown
# Migration Validation Summary

## Business Rules Validated
- [x] BR-001: Customer account validation - PRESERVED
- [x] BR-002: Interest calculation logic - PRESERVED
- [ ] BR-003: Batch processing sequence - PARTIAL

## Generated Tests
### Validation Tests
- [x] tests/validation/module-x.spec.ts - Business rule preservation

### Integration Tests
- [x] tests/integration/subsystem-a.spec.ts - Cross-module data flow

## Coverage
- Business rules: 15/20 validated
- Modules: 3/5 covered

## Epic Sign-off Readiness
- All HIGH priority rules validated: YES/NO
- Recommendation: READY FOR SIGN-OFF / NEEDS REWORK
```

### Step 6: Epic Sign-off (if all rules validated)

If all business rules for an Epic are validated:
- Use gitlab-mcp `add_comment` to post validation summary to Epic
- Use gitlab-mcp `close_epic` to trigger sign-off (with user confirmation)
- Use gitlab-mcp `apply_label` to mark modules as QA-Complete

## Keep It Simple

**Do:**
- Use standard test framework APIs
- Focus on business rule preservation
- Write readable, maintainable tests
- Run tests to verify they pass
- Tag tests with business rule IDs

**Avoid:**
- Complex fixture composition
- Over-engineering
- Unnecessary abstractions

## Output

Save summary to: `{implementation_artifacts}/tests/test-summary.md`

**Done!** Validation tests generated and verified.
