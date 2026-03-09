# Step 1: Gather Module Information

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and step 0 are available in memory
- {module_analysis_content} is available from document discovery
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified
- If user says "auto" for description or complexity, look up the module in {module_analysis_content}

## YOUR TASK:

Call list_milestones() via gitlab-mcp and display available milestones.

Call list_epics() via gitlab-mcp and display available Epics.

Ask {user_name} to provide the following module details:
- **Module name**: The COBOL module name (e.g., PAYROLL-CALC)
- **Description**: Brief description of what the module does (or say "auto" to pull from Po's analysis)
- **Complexity**: Low, Medium, or High (or say "auto" to pull from Po's analysis)
- **Milestone**: Select from the list above (optional, can be assigned later via Sprint Planning)
- **Epic**: Select from the list above (optional, can reference subsystem name)

If user says "auto" for description or complexity, look up the module in {module_analysis_content} and use Po's analysis.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-create-module-issue.md`
