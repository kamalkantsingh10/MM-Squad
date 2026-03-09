# Step 5: Generate Retrospective Report

## CONTEXT BOUNDARIES:
- Variables from workflow.yaml and previous steps are available in memory
- Sprint metrics, completed modules, and qualitative feedback from previous steps are available
- Do not assume knowledge from other steps — only what was communicated explicitly

## EXECUTION RULES:
- Communicate in {communication_language} with {user_name}

## YOUR TASK:

Build the retrospective markdown report combining quantitative metrics and qualitative feedback:

```markdown
# Sprint Retrospective: {{milestone_name}}
**Date:** {{date}}
**Sprint:** {{start_date}} to {{end_date}}

## Sprint Metrics
| Metric | Planned | Actual |
|--------|---------|--------|
| Modules | {{planned}} | {{completed}} |
| Complexity Units | {{planned_units}} | {{delivered_units}} |
| Completion Rate | - | {{completion_rate}}% |

## Completed Modules
{{completed_module_list_with_stages}}

## Carried Over / Deferred
{{deferred_module_list}}

## What Went Well
{{went_well}}

## What Didn't Go Well
{{didnt_go_well}}

## Issues Encountered
{{issues}}

## Action Items
{{action_items}}
```

Store the generated report as {retrospective_markdown}.

## COMPLETION:
**Proceed to:** `{installed_path}/steps/step-06-post-to-epic-and-report.md`
