# Step 5: Report Updated Sprint State

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- All change details from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call get_milestone_burndown(project_id, milestone_id) to get refreshed state.

Display course correction summary to {user_name}:

**Course Correction Applied**

| Change Type | Count | Details |
|-------------|-------|---------|
| Deferred | {{deferred_count}} | {{deferred_modules}} |
| Added | {{added_count}} | {{added_modules}} |
| Re-prioritised | {{reprioritised_count}} | {{reprioritised_modules}} |

**Updated Sprint Capacity:**
- Before: {{old_capacity}} complexity units
- After: {{new_capacity}} complexity units
- Delta: {{delta}} units

**Impact Assessment:**
- Sprint timeline impact: {{timeline_impact}}
- Dependency impact: {{dependency_impact}}

All changes documented on affected Issues with rationale.

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
