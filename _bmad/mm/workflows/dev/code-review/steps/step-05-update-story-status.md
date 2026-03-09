# Step 5: Update Story Status and Sync Sprint Tracking

## CONTEXT BOUNDARIES:
- Review findings and fixes from step 4 are available
- {story_key}, {fixed_count}, {action_count} are available
- {sprint_status} path is available from workflow.yaml
- Variables from workflow.yaml: {communication_language}, {user_name}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Use gitlab-mcp apply_label to update story status label (if available)

## YOUR TASK:

If all HIGH and MEDIUM issues fixed AND all ACs implemented:
- Set {new_status} = "done"
- Update story Status field to "done"

If HIGH or MEDIUM issues remain OR ACs not fully implemented:
- Set {new_status} = "in-progress"
- Update story Status field to "in-progress"

Save story file.

If {sprint_status} file exists:
- Load the FULL file
- Update development_status[{story_key}] = {new_status}
- Save file, preserving ALL comments and structure
- Use gitlab-mcp apply_label to update story status label (if available)

Output:
```
**Review Complete!**

Story Status: {new_status}
Issues Fixed: {fixed_count}
Action Items Created: {action_count}
```

## COMPLETION:
Workflow complete. Return to the agent's menu or await further instructions.
