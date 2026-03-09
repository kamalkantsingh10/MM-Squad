# Step 4: Execute Approved Changes in GitLab

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {approved_changes} from step 3 and {selected_milestone_id} from step 1 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified
- Each change must be documented with a comment

## YOUR TASK:

For each approved change:

**Deferred modules:**
1. Reassign Issue to a future milestone via assign_to_milestone
2. Apply appropriate status label update via apply_label
3. Post comment documenting deferral rationale via add_comment

**Added modules:**
1. Assign Issue to current milestone via assign_to_milestone
2. Verify labels are current
3. Post comment documenting addition rationale via add_comment

**Re-prioritised modules:**
1. Update status labels as needed via apply_label
2. Post comment documenting priority change via add_comment

Each change gets a GitLab comment with: date, change type, rationale, approver ({user_name}).

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-05-report-updated-sprint-state.md`
