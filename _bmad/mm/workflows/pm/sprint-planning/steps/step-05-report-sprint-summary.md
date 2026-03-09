# Step 5: Report Sprint Capacity and Summary

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Sprint milestone and assigned modules from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call get_milestone_burndown(project_id, milestone_id) via gitlab-mcp.

Calculate sprint capacity using complexity weights: Low=1, Medium=2, High=3 units.

Display sprint summary to {user_name}:

**Sprint Created Successfully**

- **Milestone:** {{sprint_name}}
- **Date Range:** {{start_date}} to {{end_date}}
- **Modules Assigned:** {{module_count}}
- **Total Capacity:** {{capacity}} complexity units
- **Breakdown:** Low: {{low_count}} ({{low_units}}u), Medium: {{med_count}} ({{med_units}}u), High: {{high_count}} ({{high_units}}u)

**Migration Order (this sprint):**
1. {{module_1}} (shared service)
2. {{module_2}} ...

**Next Steps:**
1. Use Sprint Status [SS] to monitor progress
2. Use Create Story [CS] to add ad-hoc modules if needed
3. Use Course Correction [CC] if scope changes are required

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
