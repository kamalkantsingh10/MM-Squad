# Step 3: Create Epics from Subsystem Groupings

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {dependency_analysis_content} from step 0 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

From {dependency_analysis_content}, identify subsystem groupings.

For each subsystem identified by Po's dependency analysis:

1. Determine Epic title from subsystem name
2. Build description including: subsystem scope, contained modules, dependency relationships
3. Call create_epic(group_id, title, description) via gitlab-mcp

Record mapping of subsystem name to Epic ID for later Issue assignment.

Report: number of Epics created, titles, and IDs.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-create-module-issues.md`
