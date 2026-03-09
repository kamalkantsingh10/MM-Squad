---
title: 'MM Dev Story Definition of Done Checklist'
validation-target: 'Story markdown ({{story_path}})'
validation-criticality: 'HIGHEST'
required-inputs:
  - 'Story markdown file with Dev Notes containing implementation context'
  - 'Completed Tasks/Subtasks section with all items marked [x]'
  - 'Updated File List section with all changed files'
  - 'Updated Dev Agent Record with implementation notes'
optional-inputs:
  - 'Test results output'
  - 'CI logs'
  - 'Linting reports'
validation-rules:
  - 'Only permitted story sections modified: Tasks/Subtasks checkboxes, Dev Agent Record, File List, Change Log, Status'
  - 'All implementation requirements from story Dev Notes must be satisfied'
  - 'Definition of Done checklist must pass completely'
  - 'No specdb-mcp access — dev agents consume Po output documents only'
  - 'Target language determined by agent persona, not hardcoded in workflow'
---

# Definition of Done Checklist

**Critical validation:** Story is truly ready for review only when ALL items below are satisfied

## Context & Requirements Validation

- [ ] **Story Context Completeness:** Dev Notes contains ALL necessary technical requirements
- [ ] **Architecture Compliance:** Implementation follows architectural requirements from Oogway's design
- [ ] **Input Documents:** Implementation uses Po's output documents (business rules, architecture), NOT specdb-mcp
- [ ] **Target Language:** Code generation uses agent persona's language (Java/COBOL/Python), not hardcoded

## Implementation Completion

- [ ] **All Tasks Complete:** Every task and subtask marked complete with [x]
- [ ] **Acceptance Criteria Satisfaction:** Implementation satisfies EVERY Acceptance Criterion
- [ ] **No Ambiguous Implementation:** Clear, unambiguous implementation
- [ ] **Edge Cases Handled:** Error conditions and edge cases addressed

## Testing & Quality Assurance

- [ ] **Unit Tests:** Unit tests added/updated for ALL core functionality
- [ ] **Integration Tests:** Integration tests added when story requirements demand them
- [ ] **Regression Prevention:** ALL existing tests pass (no regressions introduced)
- [ ] **Code Quality:** Linting and static checks pass when configured
- [ ] **Test Framework Compliance:** Tests use project's testing frameworks and patterns

## Documentation & Tracking

- [ ] **File List Complete:** File List includes EVERY new, modified, or deleted file
- [ ] **Dev Agent Record Updated:** Contains relevant implementation notes
- [ ] **Change Log Updated:** Change Log includes clear summary of changes
- [ ] **Story Structure Compliance:** Only permitted sections of story file were modified
- [ ] **GitLab Progress:** Progress comments posted via gitlab-mcp (when available)

## Final Status Verification

- [ ] **Story Status Updated:** Story Status set to "review"
- [ ] **Sprint Status Updated:** Sprint status updated to "review" (when sprint tracking is used)
- [ ] **Quality Gates Passed:** All quality checks completed successfully
- [ ] **No HALT Conditions:** No blocking issues remaining
