# Step 1: Gather Retrospective Scope

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml are available in memory
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call list_milestones(state="all") via gitlab-mcp and display milestones with: name, date range, state.

Call list_epics() via gitlab-mcp and display Epics with: title, state.

Ask {user_name} to select from the lists above:
- **Milestone**: Which completed sprint to retrospect?
- **Epic**: Which Epic to post the retrospective summary to?

Store {selected_milestone_id} and {selected_epic_iid} for later steps.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-get-sprint-metrics.md`
