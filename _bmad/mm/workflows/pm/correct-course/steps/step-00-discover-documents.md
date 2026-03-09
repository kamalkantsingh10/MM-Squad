# Step 0: Discover and Load Project Documents

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml are available in memory
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Use the discover_inputs protocol as described

## YOUR TASK:

Execute the discover_inputs protocol to load project documents.

Invoke the `discover_inputs` protocol from the workflow execution engine ({project-root}/_bmad/core/tasks/workflow.xml).

After discovery, {dependency_analysis_content} is available for migration order validation.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-01-review-current-sprint-state.md`
