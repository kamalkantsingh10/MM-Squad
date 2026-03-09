# Step 1: Find Next Ready Story and Load It

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml are available: {communication_language}, {user_name}, {sprint_status}, {implementation_artifacts}, {story_file}
- Do not assume knowledge from other steps — only what was communicated explicitly
- NOTE: `<anchor id="task_check">` is a goto target within this step — if story_path is provided directly, jump to task_check section below

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Target language is determined by the agent persona (Java for Tigress, COBOL for Viper, Python for Monkey) — NOT by this workflow
- Input documents come from Po's extracted business rules and Oogway's architecture — NOT from specdb-mcp or raw COBOL
- Use gitlab-mcp tools (apply_label, add_comment) for progress tracking when available
- Execute ALL steps in exact order; do NOT skip steps
- Absolutely DO NOT stop because of "milestones", "significant progress", or "session boundaries"
- Do NOT schedule a "next session" or request review pauses unless a HALT condition applies
- Only modify the story file in these areas: Tasks/Subtasks checkboxes, Dev Agent Record, File List, Change Log, and Status

## YOUR TASK:

If `{story_file}` (story_path) is provided directly:
- Use it directly, read the COMPLETE story file, extract story_key from filename or metadata, then jump to TASK CHECK section below.

If `{sprint_status}` file exists:
- MUST read COMPLETE sprint-status.yaml file from start to end to preserve order
- Load the FULL file
- Read ALL lines from beginning to end — do not skip any content
- Parse the development_status section completely to understand story order
- Find the FIRST story (by reading in order from top to bottom) where:
  - Key matches pattern: number-number-name (e.g., "1-2-user-auth")
  - NOT an epic key (epic-X) or retrospective (epic-X-retrospective)
  - Status value equals "ready-for-dev"

If no ready-for-dev or in-progress story found:
- Output: "No ready-for-dev stories found in sprint-status.yaml"
- Show current sprint status summary
- Ask user to choose:
  1. Run `create-story` to create next story from epics
  2. Specify a particular story file to develop (provide full path)
  3. Check sprint-status file to see current sprint status
- If user chooses 1: HALT — Run create-story
- If user chooses 2: Ask for file path, store as story_path, go to TASK CHECK
- If user chooses 3: Display detailed sprint status analysis, HALT
- If user provides story file path: Store as story_path, go to TASK CHECK

If `{sprint_status}` file does NOT exist:
- Search {implementation_artifacts} for stories directly
- Find stories with "ready-for-dev" status in files
- Look for story files matching pattern: *-*-*.md
- Read each candidate story file to check Status section
- If no ready-for-dev stories found: ask user to choose create-story, validate-create-story, or specify path
- If ready-for-dev story found: use that story file and extract story_key

Store the found story_key (e.g., "1-2-user-authentication") for later status updates.
Find matching story file in {implementation_artifacts} using story_key pattern: {story_key}.md
Read COMPLETE story file from discovered path.

---

### TASK CHECK (goto target):

Parse sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes, Dev Agent Record, File List, Change Log, Status

Load comprehensive context from story file's Dev Notes section.
Extract developer guidance from Dev Notes: architecture requirements, previous learnings, technical specifications.
Load Po's output documents (business rules, architecture) as referenced in input_file_patterns.
Use enhanced story context to inform implementation decisions and approaches.

Identify first incomplete task (unchecked [ ]) in Tasks/Subtasks.

- If no incomplete tasks → go to step 6 (Completion sequence)
- If story file inaccessible → HALT: "Cannot develop story without access to story file"
- If incomplete task or subtask requirements ambiguous → ASK user to clarify or HALT

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-load-project-context.md`
