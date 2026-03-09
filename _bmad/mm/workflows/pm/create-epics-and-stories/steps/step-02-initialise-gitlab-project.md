# Step 2: Initialise GitLab Project with Label Taxonomy and Board

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Call gitlab-mcp tools as specified
- Operation is idempotent: if labels/board already exist, skip creation

## YOUR TASK:

Call init_project() via gitlab-mcp to create the standard project structure.

The following should be created:

**Pipeline Stage Labels:**
- `Po-Analysis-Complete`
- `Architecture-Complete`
- `Code-Generated`
- `QA-Complete`

**Complexity Labels:**
- `Complexity::Low`
- `Complexity::Medium`
- `Complexity::High`

**Status Labels:**
- `In-Analysis`
- `Awaiting-Review`
- `In-Migration`
- `Blocked`
- `Done`

**Issue Board:**
- Create board with columns: In-Analysis, Awaiting-Review, In-Migration, Blocked, Done

If labels/board already exist, skip creation (idempotent operation).

Report what was created vs what already existed.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-03-create-epics.md`
