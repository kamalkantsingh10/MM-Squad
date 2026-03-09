# Step 1: Review Current Sprint State

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and step 0 are available in memory
- {dependency_analysis_content} from step 0 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call list_milestones(state="active") via gitlab-mcp and display active milestones.

Ask {user_name}: Select the sprint milestone to adjust from the list above.

Call get_milestone_burndown(milestone_id) via gitlab-mcp to understand current state.

Display current sprint snapshot: open Issues, closed Issues, blocked Issues, progress percentage.

Store {selected_milestone_id} for later steps.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-identify-changes-needed.md`
