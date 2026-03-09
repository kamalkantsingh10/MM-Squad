# Step 4: Present Findings and Fix Them

## CONTEXT BOUNDARIES:
- All review findings are compiled from step 3
- {story_key}, {story_file}, finding counts by severity are available
- Git discrepancy count is available from step 1
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Categorize findings: HIGH (must fix), MEDIUM (should fix), LOW (nice to fix)

## YOUR TASK:

Categorize findings: HIGH (must fix), MEDIUM (should fix), LOW (nice to fix).

Set {fixed_count} = 0
Set {action_count} = 0

Output:
```
**CODE REVIEW FINDINGS**

Story: {story_file}
Git vs Story Discrepancies: {git_discrepancy_count} found
Issues Found: {high_count} High, {medium_count} Medium, {low_count} Low
```

Ask {user_name}: "What should I do with these issues?

1. **Fix them automatically** — I'll update the code and tests
2. **Create action items** — Add to story Tasks/Subtasks for later
3. **Show me details** — Deep dive into specific issues

Choose [1], [2], or specify which issue to examine:"

If user chooses 1:
- Fix all HIGH and MEDIUM issues in the code
- Add/update tests as needed
- Update File List in story if files changed
- Update story Dev Agent Record with fixes applied
- Use gitlab-mcp add_comment to log review fixes (if available)

If user chooses 2:
- Add "Review Follow-ups (AI)" subsection to Tasks/Subtasks
- For each issue: `- [ ] [AI-Review][Severity] Description [file:line]`

If user chooses 3:
- Show detailed explanation with code examples
- Return to fix decision

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-05-update-story-status.md`
