# Step 3: Identify Blockers and Risks

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Burndown data from step 2 is available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}
- Categorise each finding as BLOCKER or RISK

## YOUR TASK:

From the milestone Issues, identify:

**Blockers:**
- Issues with `Blocked` status label
- Issues that have been in `Awaiting-Review` for an extended period
- Issues whose dependencies are not yet complete

**Risks:**
- High-complexity modules still in early pipeline stages
- Sprint end date approaching with significant open work
- Modules with no recent activity

Categorise each finding as BLOCKER (action required) or RISK (monitor).

Store {blocker_list} and {risk_list} for the final report.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-04-update-readme.md`
