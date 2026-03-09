# Step 3: Create Sprint Milestone in GitLab

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Sprint parameters from step 2 are available: {sprint_name}, {start_date}, {end_date}, {target_modules}
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call create_milestone(project_id, title=sprint_name, description, start_date, due_date) via gitlab-mcp.

Description should include: sprint goal, target modules listed, dependency rationale.

Record the {milestone_id} for Issue assignment.

Report: milestone created with ID and date range.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-assign-issues-to-milestone.md`
