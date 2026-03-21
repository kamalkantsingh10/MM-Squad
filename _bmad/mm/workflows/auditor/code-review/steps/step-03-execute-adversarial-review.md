# Step 3: Execute Adversarial Review

## CONTEXT BOUNDARIES:
- Review plan is complete from step 2
- {story_key}, all ACs, task list, and file list are available
- Git discrepancy data is available from step 1
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- VALIDATE EVERY CLAIM — Check git reality vs story claims
- Communicate in {communication_language} with {user_name}
- NOT LOOKING HARD ENOUGH if fewer than 3 issues found — re-examine

## YOUR TASK:

**Git vs Story Discrepancies:**
1. Files changed but not in story File List → MEDIUM finding
2. Story lists files but no git changes → HIGH finding
3. Uncommitted changes not documented → MEDIUM finding

Create comprehensive review file list from story File List and git changes.

**AC Validation:**
For EACH Acceptance Criterion:
1. Read the AC requirement
2. Search implementation files for evidence
3. Determine: IMPLEMENTED, PARTIAL, or MISSING
4. If MISSING/PARTIAL → HIGH SEVERITY finding

**Task Completion Audit:**
For EACH task marked [x]:
1. Read the task description
2. Search files for evidence it was actually done
3. If marked [x] but NOT DONE → CRITICAL finding
4. Record specific proof (file:line)

**Code Quality Deep Dive:**
For EACH file in comprehensive review list:
1. **Security**: Injection risks, missing validation, auth issues
2. **Performance**: N+1 queries, inefficient loops, missing caching
3. **Error Handling**: Missing try/catch, poor error messages
4. **Code Quality**: Complex functions, magic numbers, poor naming
5. **Test Quality**: Are tests real assertions or placeholders?

**MM-Specific Review Criteria:**
For EACH implementation file:
1. **Spec Layer Compliance**: Generated code matches Po's business rules
2. **Business Rule Preservation**: No business logic lost in translation
3. **COBOL Construct Handling**: Proper mapping of COBOL patterns (PERFORM, COPY, EVALUATE, etc.)
4. **No specdb-mcp**: Dev code does not access spec layer directly

If total issues found < 3 → NOT LOOKING HARD ENOUGH — find more problems. Re-examine code for edge cases, architecture violations, documentation gaps, integration issues.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-present-findings-and-fix.md`
