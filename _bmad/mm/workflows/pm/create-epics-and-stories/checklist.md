# Create Epics and Stories - Validation Checklist

## Core Validation

- [ ] All pipeline stage labels exist: `Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`
- [ ] All complexity labels exist: `Complexity::Low`, `Complexity::Medium`, `Complexity::High`
- [ ] All status labels exist: `In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`
- [ ] Issue board exists with correct columns

## Epic Validation

- [ ] Every subsystem from Po's dependency analysis has a corresponding Epic
- [ ] Each Epic has a descriptive title and scope description
- [ ] No duplicate Epics exist

## Issue Validation

- [ ] Every COBOL module has a corresponding GitLab Issue
- [ ] Every Issue has exactly one `Complexity::` label assigned
- [ ] Every Issue has `In-Analysis` status label
- [ ] Every Issue is assigned to exactly one Epic
- [ ] No orphaned Issues (Issues without an Epic)
- [ ] No orphaned modules (modules without an Issue)

## Dashboard Validation

- [ ] README dashboard reflects correct counts for all modules and stages
