# Story 3.6: Mantis Agent Definition (QA)

Status: review

## Story

As an operator,
I want the Mantis agent fully authored as the migration QA validator,
so that Mantis can be invoked via `/bmad-agent-mm-mantis` with the full QA agent menu adapted for migration validation.

## Acceptance Criteria

1. **AC1: Agent definition file**
   - Given the BMAD QA agent definition and workflows exist
   - When the developer copies and adapts the agent to `_bmad/mm/agents/mantis.md`
   - Then it contains: migration validation persona, validates generated code against Po's business rules documents
   - And the menu mirrors the full BMAD QA agent menu (qa-generate-e2e-tests, chat, and all other items)
   - And it declares access to `gitlab-mcp` MCP server only

2. **AC2: QA workflows copied and adapted**
   - Given the BMAD QA workflows exist at `_bmad/bmm/workflows/qa-generate-e2e-tests/`
   - When the developer copies and adapts them to `_bmad/mm/workflows/qa/`
   - Then all QA workflows are present with step files adapted for MM context
   - And validation workflows compare generated code against Po's business markdown and extracted rules documents
   - And QA workflows can trigger Epic sign-off via gitlab-mcp (FR55, FR56)
   - And FR26, FR27, FR28 are addressable through the adapted workflows

3. **AC3: Agent installation and invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-mantis`
   - Then Mantis loads with his QA validation persona, presents the full QA menu, and responds in character

## Tasks / Subtasks

- [x] Task 1: Create Mantis agent definition (AC: #1, #3)
  - [x] 1.1: Create `_bmad/mm/agents/mantis.md` following BMAD agent format
  - [x] 1.2: Define migration QA persona using party roster values:
    - name: "Mantis", title: "QA Agent", icon: "🦗"
    - role: "Migration QA Specialist"
    - identity: "QA expert validating generated code against spec layer business rules. Manages quality gates and epic sign-off through GitLab."
    - communication_style: "Exacting and relentless. Every business rule must be provably preserved. No shortcuts past the quality gate."
    - principles: "Quality is not negotiable. Every business rule has a test. Sign-off means verified, not assumed."
  - [x] 1.3: Define capabilities: migration validation, business rule verification, epic sign-off, test generation
  - [x] 1.4: Add activation steps following BMAD agent activation pattern — config from `_bmad/mm/config.yaml`
  - [x] 1.5: Declare `gitlab-mcp` MCP server access via `<mcp-servers>` section
  - [x] 1.6: Add QA-specific activation steps (never skip running tests, use standard test framework APIs, focus on realistic scenarios) — mirror BMM QA agent steps 4-7
  - [x] 1.7: Define menu mirroring BMM QA agent:
    - [MH] Redisplay Menu Help
    - [CH] Chat with the Agent
    - [QA] Automate — workflow: `{project-root}/_bmad/mm/workflows/qa/qa-generate-e2e-tests/workflow.yaml`
    - [PM] Start Party Mode — exec: `{project-root}/_bmad/core/workflows/party-mode/workflow.md`
    - [DA] Dismiss Agent

- [x] Task 2: Create QA workflow directory structure (AC: #2)
  - [x] 2.1: Create `_bmad/mm/workflows/qa/qa-generate-e2e-tests/` directory

- [x] Task 3: Copy and adapt qa-generate-e2e-tests workflow (AC: #2)
  - [x] 3.1: Copy `_bmad/bmm/workflows/qa-generate-e2e-tests/workflow.yaml` to `_bmad/mm/workflows/qa/qa-generate-e2e-tests/workflow.yaml`
  - [x] 3.2: Update `config_source` to `{project-root}/_bmad/mm/config.yaml`
  - [x] 3.3: Update `installed_path` to `{project-root}/_bmad/mm/workflows/qa/qa-generate-e2e-tests`
  - [x] 3.4: Copy `instructions.md` and `checklist.md`, adapt for MM context:
    - Validation compares generated code against Po's business markdown
    - Test generation validates business rule preservation
    - Epic sign-off capability via gitlab-mcp (FR55, FR56)
  - [x] 3.5: Add `gitlab-mcp` references for Epic sign-off (close_epic, add_comment tools)

- [x] Task 4: Verify module-help.csv entries (AC: #3)
  - [x] 4.1: Confirm `module-help.csv` has Mantis agent entry
  - [x] 4.2: Confirm qa-generate-e2e-tests workflow entry exists
  - [x] 4.3: Confirm paths point to `_bmad/mm/workflows/qa/`

- [x] Task 5: Verify party roster entry (AC: #3)
  - [x] 5.1: Confirm `_bmad/mm/teams/default-party.csv` has Mantis entry

- [x] Task 6: Write tests (AC: #1, #2, #3)
  - [x] 6.1: Test `_bmad/mm/agents/mantis.md` exists
  - [x] 6.2: Test agent file contains `<persona>` with QA/validation content
  - [x] 6.3: Test agent file contains `<menu>` with all required items (MH, CH, QA, PM, DA)
  - [x] 6.4: Test agent file contains `<activation` section
  - [x] 6.5: Test agent file references `_bmad/mm/config.yaml` (not BMM config)
  - [x] 6.6: Test agent file references `_bmad/mm/workflows/qa/` for workflow paths
  - [x] 6.7: Test agent file declares `gitlab-mcp` access
  - [x] 6.8: Test QA workflow directory exists with workflow files
  - [x] 6.9: Test workflow.yaml is valid YAML with required keys
  - [x] 6.10: Test module-help.csv has Mantis + workflow entries
  - [x] 6.11: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/mantis.md`** — per architecture project structure
- **Workflows at `_bmad/mm/workflows/qa/`** — per architecture directory structure
- **Config source: `_bmad/mm/config.yaml`** — MM module config
- **MCP access: `gitlab-mcp` only** — Mantis validates code against Po's documents and manages Epic sign-off
- **No specdb-mcp access** — agents consume documents, not spec layer directly
- **Epic sign-off** — Mantis can close Epics via `gitlab-mcp` (close_epic tool) when all module Issues are QA-Complete

### BMAD QA Agent Format Reference

Copy structure from `_bmad/bmm/agents/qa.md` (Quinn):
- Note: BMM QA agent uses `workflow` handler type (same as dev agent)
- Has QA-specific activation steps (4-7): never skip running tests, use standard APIs, keep tests simple, focus on realistic scenarios
- Has a `<prompts>` section with welcome message — adapt or omit for MM
- Menu item uses `workflow="path/to/workflow.yaml"` format

### Source Files to Copy From

| BMM Source | MM Target |
|---|---|
| `_bmad/bmm/agents/qa.md` | `_bmad/mm/agents/mantis.md` |
| `_bmad/bmm/workflows/qa-generate-e2e-tests/workflow.yaml` | `_bmad/mm/workflows/qa/qa-generate-e2e-tests/workflow.yaml` |
| `_bmad/bmm/workflows/qa-generate-e2e-tests/instructions.md` | `_bmad/mm/workflows/qa/qa-generate-e2e-tests/instructions.md` |
| `_bmad/bmm/workflows/qa-generate-e2e-tests/checklist.md` | `_bmad/mm/workflows/qa/qa-generate-e2e-tests/checklist.md` |

### Key Adaptations for MM Context

1. **Validation focus**: Instead of generic test generation, Mantis validates:
   - Generated code (from Tigress/Viper/Monkey) against Po's business markdown
   - Business rule preservation — every extracted rule must be provably present in generated code
   - Spec layer compliance — generated code structure matches Oogway's architecture
2. **Epic sign-off**: Mantis can trigger Epic completion via `gitlab-mcp`:
   - `close_epic` — when all module Issues in an Epic are QA-Complete
   - `add_comment` — post validation summary to Epic
3. **FR coverage**:
   - FR26: QA can initiate validation of generated code against business rules
   - FR27: QA can view validation report (confirmed/partial/missing coverage)
   - FR28: QA can flag module for rework before sign-off
   - FR55: QA Epic sign-off via GitLab
   - FR56: QA can close Epic when all modules QA-Complete

### Functional Requirements Addressed

- FR26: Initiate validation of generated code against spec layer business rules
- FR27: View validation report showing business rule coverage
- FR28: Flag module for rework before sign-off
- FR55: Epic sign-off via GitLab with validation summary
- FR56: Close Epic when all module Issues are QA-Complete

### Party Roster Values (from default-party.csv)

```
name: "mantis"
displayName: "Mantis"
title: "QA Agent"
icon: "🦗"
role: "Migration QA Specialist"
identity: "QA expert validating generated code against spec layer business rules..."
communicationStyle: "Exacting and relentless. Every business rule must be provably preserved..."
principles: "Quality is not negotiable. Every business rule has a test..."
```

### Dependencies

- Epic 1 (MM module foundation) — complete
- Epic 2 Story 2.7 (Shifu) — MM agent pattern reference
- No dependency on Stories 3.1-3.4 — Mantis has its own QA workflows

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.6]
- [Source: documents/planning-artifacts/architecture.md — Agent Roster, Mantis definition]
- [Source: documents/planning-artifacts/prd.md — FR26-28, FR55-56]
- [Source: _bmad/bmm/agents/qa.md — BMAD QA agent format reference]
- [Source: _bmad/bmm/workflows/qa-generate-e2e-tests/ — BMM source workflow]
- [Source: _bmad/mm/teams/default-party.csv — Mantis persona values]
- [Source: _bmad/mm/module-help.csv — Mantis + workflow registry entries]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Created Mantis agent at _bmad/mm/agents/mantis.md with migration QA persona
- QA-specific activation steps 4-7: never skip tests, standard APIs, simple/maintainable, business rule preservation
- Created QA workflow at _bmad/mm/workflows/qa/qa-generate-e2e-tests/ (workflow.yaml, instructions.md, checklist.md)
- Workflow adapted for MM: validates generated code against Po's business rules, epic sign-off via gitlab-mcp
- mcp_tools includes close_epic and add_comment for epic sign-off (FR55, FR56)
- module-help.csv and party roster already had correct entries
- 20 new tests all pass; zero regressions (20 pre-existing failures from earlier stories)

### Change Log

- 2026-03-08: Story 3.6 implemented — Mantis QA agent and workflow created

### File List

- _bmad/mm/agents/mantis.md (new)
- _bmad/mm/workflows/qa/qa-generate-e2e-tests/workflow.yaml (new)
- _bmad/mm/workflows/qa/qa-generate-e2e-tests/instructions.md (new)
- _bmad/mm/workflows/qa/qa-generate-e2e-tests/checklist.md (new)
- tests/test_mantis_agent.py (new)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-6-mantis-agent-definition-qa.md (modified)
