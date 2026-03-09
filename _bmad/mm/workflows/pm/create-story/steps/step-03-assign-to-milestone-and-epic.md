# Step 3: Assign to Milestone and Epic

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {issue_iid} from step 2, milestone and epic selections from step 1 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified
- Both milestone and epic assignment are conditional on whether they were specified

## YOUR TASK:

If milestone was specified:
- Call assign_to_milestone(project_id, issue_iid, milestone_id) via gitlab-mcp

If epic was specified:
- Associate the Issue with the specified Epic via gitlab-mcp

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-report.md`
