# Step 5: Present Sprint Status Report

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- All burndown data, blockers and risks from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Display status report to {user_name}:

**Sprint Status: {{milestone_name}}**

| Metric | Value |
|--------|-------|
| Progress | {{progress}}% ({{closed}}/{{total}} modules) |
| In-Analysis | {{in_analysis_count}} |
| Awaiting-Review | {{awaiting_review_count}} |
| In-Migration | {{in_migration_count}} |
| Blocked | {{blocked_count}} |
| Done | {{done_count}} |

**Complexity Burndown:**
- Low: {{low_done}}/{{low_total}} complete
- Medium: {{med_done}}/{{med_total}} complete
- High: {{high_done}}/{{high_total}} complete

**Blockers:** (if any)
- {{blocker_list}}

**Risks:** (if any)
- {{risk_list}}

**Next Steps:**
1. Address blockers immediately
2. Monitor risks
3. Use Course Correction [CC] if sprint scope needs adjustment

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
