---
title: 'MM Code Review Validation Checklist'
validation-target: 'Story markdown ({{story_path}})'
validation-criticality: 'HIGHEST'
---

# Code Review Validation Checklist

- [ ] Story file loaded from `{{story_path}}`
- [ ] Story Status verified as reviewable (review)
- [ ] Story Context located or warning recorded
- [ ] Architecture docs loaded (as available)
- [ ] Acceptance Criteria cross-checked against implementation
- [ ] File List reviewed and validated for completeness
- [ ] Tests identified and mapped to ACs; gaps noted
- [ ] Code quality review performed on changed files
- [ ] Security review performed on changed files and dependencies
- [ ] MM-specific: Spec layer compliance validated
- [ ] MM-specific: Business rule preservation verified
- [ ] MM-specific: COBOL construct handling validated
- [ ] MM-specific: No specdb-mcp access in dev code
- [ ] Outcome decided (Approve/Changes Requested/Blocked)
- [ ] Review notes appended under "Senior Developer Review (AI)"
- [ ] Change Log updated with review entry
- [ ] Status updated
- [ ] Sprint status synced (if sprint tracking enabled)
- [ ] Story saved successfully

_Reviewer: {{user_name}} on {{date}}_
