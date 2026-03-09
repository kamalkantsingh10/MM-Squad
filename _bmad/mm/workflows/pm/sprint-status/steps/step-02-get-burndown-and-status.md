# Step 2: Get Sprint Burndown and Issue Status Breakdown

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and step 1 are available in memory
- {selected_milestone} contains the milestone selected in step 1
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call get_milestone_burndown(project_id, milestone_id) via gitlab-mcp.

From the burndown data, extract:

- Total Issues in milestone
- Open Issues (with status labels)
- Closed Issues (completed modules)
- Issues by pipeline stage (In-Analysis, Awaiting-Review, In-Migration, Done)
- Issues by complexity label

Calculate progress percentage: (closed / total) * 100

Store all extracted data as variables for use in later steps.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-identify-blockers-and-risks.md`
