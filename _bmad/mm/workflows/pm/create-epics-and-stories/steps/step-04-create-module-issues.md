# Step 4: Create Module Issues with Labels

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {module_analysis_content} from step 0 and Epic IDs from step 3 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

From {module_analysis_content}, get the full list of COBOL modules with their complexity scores.

For each COBOL module:

1. Set title = module name
2. Build description including: module purpose, key dependencies, complexity rationale
3. Determine complexity label from Po's analysis: `Complexity::Low`, `Complexity::Medium`, or `Complexity::High`
4. Call create_issue(project_id, title, description, labels=['In-Analysis', complexity_label]) via gitlab-mcp

Record mapping of module name to Issue IID for Epic assignment.

Report: number of Issues created with their complexity breakdown.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-05-assign-issues-to-epics.md`
