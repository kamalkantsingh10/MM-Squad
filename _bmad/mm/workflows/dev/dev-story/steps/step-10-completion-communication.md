# Step 10: Completion Communication and User Support

## CONTEXT BOUNDARIES:
- Story is complete and marked "review"
- {story_key}, all implementation details are available from previous steps
- Variables from workflow.yaml: {communication_language}, {user_name}, {user_skill_level}

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Tailor explanations to {user_skill_level}

## YOUR TASK:

Execute the enhanced definition-of-done checklist using the validation framework.

Prepare a concise summary in Dev Agent Record → Completion Notes.

Communicate to {user_name} that story implementation is complete and ready for review.

Summarize key accomplishments: story ID, story key, title, key changes made, tests added, files modified.

Provide the story file path and current status (now "review").

Based on {user_skill_level}, ask if {user_name} needs any explanations about:
- What was implemented and how it works
- Why certain technical decisions were made
- How to test or verify the changes
- Any patterns, libraries, or approaches used
- Anything else they'd like clarified

If user asks for explanations:
- Provide clear, contextual explanations tailored to {user_skill_level}
- Use examples and references to specific code when helpful

Once explanations are complete (or user indicates no questions), suggest logical next steps:
- Review the implemented story and test the changes
- Verify all acceptance criteria are met
- Ensure deployment readiness if applicable
- Run `code-review` workflow for peer review
- Optional: If Test Architect module installed, run `/bmad:tea:automate` to expand guardrail tests

Output: "💡 Tip: For best results, run `code-review` using a **different** LLM than the one that implemented this story."

If {sprint_status} file exists: suggest checking {sprint_status} to see project progress.

Remain flexible — allow {user_name} to choose their own path or ask for other assistance.

## COMPLETION:
Workflow complete. Return to the agent's menu or await further instructions.
