# Step 4: Report

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- All Issue details from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Display confirmation to {user_name}:

**Module Issue Created**

- **Issue:** {{module_name}} (#{{issue_iid}})
- **Complexity:** {{complexity}}
- **Status:** In-Analysis
- **Milestone:** {{milestone_name}} (or "Not assigned")
- **Epic:** {{epic_name}} (or "Not assigned")

**Next Steps:**
- Po can now begin structural analysis of this module
- Use Sprint Planning [SP] to assign to a sprint if not already assigned

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
