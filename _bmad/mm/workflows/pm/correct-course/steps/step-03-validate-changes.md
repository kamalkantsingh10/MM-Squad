# Step 3: Validate Changes Against Dependency Order

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- {dependency_analysis_content} from step 0 and {proposed_changes} from step 2 are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Cross-reference proposed changes against {dependency_analysis_content}.

**Validation checks:**
- Deferring a module won't leave its consumers stranded in this sprint
- Adding a module won't introduce unmet dependencies
- Re-prioritisation respects shared-services-first ordering

If validation fails, present the dependency conflict and ask {user_name} to adjust.

If validation passes, present the validated change plan for approval.

Store the approved changes as {approved_changes}.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-execute-changes-in-gitlab.md`
