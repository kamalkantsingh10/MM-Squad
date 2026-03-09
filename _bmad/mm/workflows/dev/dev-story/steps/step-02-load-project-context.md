# Step 2: Load Project Context and Story Information

## CONTEXT BOUNDARIES:
- Story file has been identified and read in step 1
- {story_key}, {story_path} are available from step 1
- Variables from workflow.yaml are available: {communication_language}, {user_name}, {project_context}
- Do not assume knowledge beyond what was passed from step 1

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Load all available context to inform implementation
- Target language is determined by the agent persona — NOT by this workflow
- Input documents come from Po's extracted business rules and Oogway's architecture — NOT specdb-mcp

## YOUR TASK:

Load {project_context} for coding standards and project-wide patterns (if exists).

Parse sections from story file: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes, Dev Agent Record, File List, Change Log, Status.

Load comprehensive context from story file's Dev Notes section.
Extract developer guidance from Dev Notes: architecture requirements, previous learnings, technical specifications.
Use enhanced story context to inform implementation decisions and approaches.

Output: "Context Loaded — Story and project context available for implementation"

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-detect-review-continuation.md`
