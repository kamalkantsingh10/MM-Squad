# Step 1: Identify Active Sprint Milestone

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml are available in memory: {communication_language}, {user_name}
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call list_milestones() via gitlab-mcp and display all milestones with: name, date range, state.

Ask {user_name}: Select the milestone to review from the list above (or type "latest" to use the most recent active milestone).

Store the selected milestone as {selected_milestone}.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-get-burndown-and-status.md`
