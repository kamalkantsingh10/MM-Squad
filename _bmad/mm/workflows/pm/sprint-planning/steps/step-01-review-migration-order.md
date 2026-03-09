# Step 1: Review Migration Order from Dependency Analysis

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and step 0 are available in memory
- {dependency_analysis_content} is available from document discovery
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

From {dependency_analysis_content}, extract the recommended migration order.

Identify which modules are shared services (must migrate first) and which are consumers.

Present the migration order to {user_name} for confirmation.

**Migration Order Principles:**
- Shared services and utility modules before consumers
- Modules with fewer dependencies before highly-coupled modules
- Subsystem boundaries respected (complete subsystems together where possible)

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-02-gather-sprint-parameters.md`
