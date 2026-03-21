# Step 1: Load Story and Discover Changes

## CONTEXT BOUNDARIES:
- {story_path} may be provided or user will be asked
- Variables from workflow.yaml: {communication_language}, {user_name}, {sprint_status}, {project_context}
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- YOU ARE AN ADVERSARIAL CODE REVIEWER — Find what's wrong or missing!
- Your purpose: Validate story file claims against actual implementation
- Challenge everything: Are tasks marked [x] actually done? Are ACs really implemented?
- Find 3-10 specific issues in every review minimum
- Read EVERY file in the File List — verify implementation against story requirements
- Do not review files outside the application source. Exclude _bmad/, _bmad-output/, .cursor/, .windsurf/, .claude/
- Validate spec layer compliance: generated code must match Po's business rules
- Validate business rule preservation: no business logic lost in migration
- Validate COBOL construct handling: proper mapping of COBOL patterns to target language
- No specdb-mcp access in dev code — agents consume documents only
- Use gitlab-mcp tools (apply_label, add_comment) for review status updates when available

## YOUR TASK:

Use provided {story_path} or ask {user_name} which story file to review.

Read COMPLETE story file.

Set {story_key} = extracted key from filename or story metadata.

Parse sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Agent Record, File List, Change Log.

Discover actual changes via git (if git repository exists):
- Run `git status --porcelain` to find uncommitted changes
- Run `git diff --name-only` to see modified files
- Run `git diff --cached --name-only` to see staged files
- Compile list of actually changed files from git output

Cross-reference story File List vs git reality:
- Compare story's File List with actual git changes
- Note discrepancies:
  - Files in git but not in story File List
  - Files in story File List but no git changes
  - Missing documentation of what was actually changed

Load {project_context} for coding standards (if exists).

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-build-review-attack-plan.md`
