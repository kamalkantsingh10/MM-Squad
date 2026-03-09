# Step 6: Post Retrospective to Epic and Report

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {retrospective_markdown} from step 5 and {selected_epic_iid} from step 1 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified

## YOUR TASK:

Call add_comment(project_id, epic_iid, retrospective_markdown) via gitlab-mcp to post the retrospective on the relevant Epic.

Display confirmation to {user_name}:

**Retrospective Posted**

- **Sprint:** {{milestone_name}}
- **Posted to:** Epic #{{epic_iid}}
- **Modules Completed:** {{completed}}/{{planned}}
- **Completion Rate:** {{completion_rate}}%
- **Action Items:** {{action_item_count}}

**Next Steps:**
1. Review action items before next sprint planning
2. Use Sprint Planning [SP] to create the next sprint
3. Apply learnings to complexity estimates for upcoming modules

## COMPLETION:
Workflow complete. Return to Shifu's menu or await further instructions.
