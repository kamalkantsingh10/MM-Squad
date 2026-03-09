# Step 6: Update README Dashboard and Report

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- All Epic and Issue counts from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call update_readme(project_id) via gitlab-mcp to generate the initial README dashboard.

Display completion summary to {user_name}:

**Project Initialisation Complete**

- **Epics Created:** {{epic_count}} (one per subsystem)
- **Issues Created:** {{issue_count}} (one per COBOL module)
- **Complexity Breakdown:** Low: {{low_count}}, Medium: {{medium_count}}, High: {{high_count}}
- **Board Configured:** In-Analysis | Awaiting-Review | In-Migration | Blocked | Done
- **README Dashboard:** Updated

**Next Steps:**
1. Review the created Epics and Issues in GitLab
2. Use Sprint Planning [SP] to create your first sprint milestone
3. Use Sprint Status [SS] to monitor progress

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
