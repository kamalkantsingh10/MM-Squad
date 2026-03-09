# Step 2: Create the Module Issue in GitLab

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Module name, description, complexity, milestone, and epic from step 1 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Build the Issue description including:
- Module purpose and scope
- Key dependencies (from Po's analysis if available)
- Complexity rationale

Call create_issue(project_id, title=module_name, description, labels=['In-Analysis', 'Complexity::' + complexity]) via gitlab-mcp.

Record the Issue IID as {issue_iid}.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-assign-to-milestone-and-epic.md`
