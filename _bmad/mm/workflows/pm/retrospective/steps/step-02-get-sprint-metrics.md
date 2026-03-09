# Step 2: Get Sprint Metrics from GitLab

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and step 1 are available in memory
- {selected_milestone_id} from step 1 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call get_milestone_burndown(project_id, milestone_id) via gitlab-mcp.

Extract final sprint metrics:

- Total modules planned
- Modules completed (closed Issues)
- Modules deferred or carried over
- Modules blocked at sprint close
- Complexity units delivered vs planned
- Sprint duration (start to end date)

Store all extracted metrics for use in the report step.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-review-completed-modules.md`
