# Step 2: Identify Changes Needed

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Current sprint state from step 1 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Ask {user_name} to describe the course correction needed. Choose from:
- **Defer modules**: Which modules to move to a future sprint?
- **Add modules**: Which modules to pull into this sprint?
- **Re-prioritise**: Which modules need changed priority or status?
- **Re-scope**: Is the sprint goal changing?

Ask {user_name} to provide rationale for each change.

Store the proposed changes as {proposed_changes} for validation.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-validate-changes.md`
