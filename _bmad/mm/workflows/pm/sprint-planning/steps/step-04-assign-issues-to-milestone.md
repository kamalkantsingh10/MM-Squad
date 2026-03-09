# Step 4: Assign Module Issues to Sprint Milestone

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {milestone_id} from step 3 and {target_modules} from step 2 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified
- Assign Issues in dependency order (shared services first)

## YOUR TASK:

For each target module, look up its Issue IID in GitLab.

Assign Issues in dependency order (shared services first):

1. For each target module Issue, call assign_to_milestone(project_id, issue_iid, milestone_id) via gitlab-mcp
2. Verify the assignment succeeded

Report: number of Issues assigned, assignment order.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-05-report-sprint-summary.md`
