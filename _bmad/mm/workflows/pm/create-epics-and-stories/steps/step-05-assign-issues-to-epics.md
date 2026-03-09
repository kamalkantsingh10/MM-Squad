# Step 5: Assign Module Issues to Parent Epics

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Subsystem-to-Epic and module-to-Issue mappings from steps 3 and 4 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Using the subsystem-to-Epic and module-to-Issue mappings:

1. For each module Issue, identify its parent subsystem from the dependency analysis
2. Associate the Issue with its parent Epic via gitlab-mcp

Verify every Issue has been assigned to exactly one Epic.

Report any orphaned modules (modules not belonging to any subsystem).

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-06-update-readme-and-report.md`
