# Step 2: Gather Sprint Parameters

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Migration order from step 1 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call list_milestones() via gitlab-mcp to show {user_name} existing sprints for context.

Ask {user_name} to provide the following sprint details:
- **Sprint name**: e.g., "Sprint 1 - Core Services"
- **Start date**: ISO 8601 format (YYYY-MM-DD)
- **End date**: ISO 8601 format (YYYY-MM-DD)
- **Target modules**: Which modules to include in this sprint (reference the migration order above)

Store sprint parameters as {sprint_name}, {start_date}, {end_date}, {target_modules}.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-create-sprint-milestone.md`
