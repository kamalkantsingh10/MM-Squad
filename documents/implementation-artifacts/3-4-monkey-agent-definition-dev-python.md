# Story 3.4: Monkey Agent Definition (Dev — Python)

Status: review

## Story

As an operator,
I want the Monkey agent fully authored as the Python code generation dev agent,
so that Monkey can be invoked via `/bmad-agent-mm-monkey` with the full dev agent menu adapted for Python modernisation.

## Acceptance Criteria

1. **AC1: Agent definition file**
   - Given the BMAD dev agent definition exists at `_bmad/bmm/agents/dev.md`
   - When the developer copies and adapts it to `_bmad/mm/agents/monkey.md`
   - Then it contains: Python code generation persona, works from Po's output documents, mainframe modernisation context
   - And the menu mirrors the full BMAD dev agent menu
   - And menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
   - And it declares access to `gitlab-mcp` MCP server only

2. **AC2: Agent installation and invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-monkey`
   - Then Monkey loads with his Python persona, presents the full dev menu, and responds in character

## Tasks / Subtasks

- [x] Task 1: Create Monkey agent definition (AC: #1, #2)
  - [x] 1.1: Create `_bmad/mm/agents/monkey.md` following BMAD agent format
  - [x] 1.2: Define Python code generation persona using party roster values:
    - name: "Monkey", title: "Python Dev Agent", icon: "🐒"
    - role: "Python Code Generation Specialist"
    - identity: "Senior Python developer generating modern Python code from COBOL spec layer analysis. Expert in Pythonic patterns and clean architecture."
    - communication_style: "Energetic and pragmatic. Writes Pythonic code that reads like documentation. Fast iterations, clean results."
    - principles: "Python should be beautiful. Spec layer drives every decision. Simple is better than complex."
  - [x] 1.3: Define capabilities: story execution, test-driven development, Python code generation, Pythonic patterns
  - [x] 1.4: Add activation steps following BMAD agent activation pattern — config from `_bmad/mm/config.yaml`
  - [x] 1.5: Declare `gitlab-mcp` MCP server access via `<mcp-servers>` section
  - [x] 1.6: Define dev-specific activation steps (read story file, execute tasks in order, mark complete, run tests, etc.) — mirror BMM dev agent steps 4-11
  - [x] 1.7: Define menu mirroring BMM dev agent:
    - [MH] Redisplay Menu Help
    - [CH] Chat with the Agent
    - [DS] Dev Story — workflow: `{project-root}/_bmad/mm/workflows/dev/dev-story/workflow.yaml`
    - [CR] Code Review — workflow: `{project-root}/_bmad/mm/workflows/dev/code-review/workflow.yaml`
    - [PM] Start Party Mode — exec: `{project-root}/_bmad/core/workflows/party-mode/workflow.md`
    - [DA] Dismiss Agent

- [x] Task 2: Verify module-help.csv entry (AC: #2)
  - [x] 2.1: Confirm `module-help.csv` has Monkey agent entry pointing to `_bmad/mm/agents/monkey.md`
  - [x] 2.2: Confirm slash command is `bmad-agent-mm-monkey`

- [x] Task 3: Verify party roster entry (AC: #2)
  - [x] 3.1: Confirm `_bmad/mm/teams/default-party.csv` has Monkey entry with correct persona values

- [x] Task 4: Write tests (AC: #1, #2)
  - [x] 4.1: Test `_bmad/mm/agents/monkey.md` exists
  - [x] 4.2: Test agent file contains `<persona>` with Python-specific content
  - [x] 4.3: Test agent file contains `<menu>` with all required items (MH, CH, DS, CR, PM, DA)
  - [x] 4.4: Test agent file contains `<activation` section
  - [x] 4.5: Test agent file references `_bmad/mm/config.yaml` (not BMM config)
  - [x] 4.6: Test agent file references `_bmad/mm/workflows/dev/` for workflow paths
  - [x] 4.7: Test agent file declares `gitlab-mcp` access
  - [x] 4.8: Test agent file does NOT reference `specdb-mcp`
  - [x] 4.9: Test module-help.csv has Monkey entry
  - [x] 4.10: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/monkey.md`** — per architecture project structure
- **Config source: `_bmad/mm/config.yaml`** — MM module config, NOT BMM
- **Workflows point to `_bmad/mm/workflows/dev/`** — shared dev workflows from Story 3.1
- **MCP access: `gitlab-mcp` only** — dev agents consume Po's documents, not specdb directly
- **No specdb-mcp access** — agents work from documents produced by Po
- **Python persona drives target language** — the workflow is language-agnostic; Monkey's persona determines Python-specific behaviour

### Copy Pattern

Structure is identical to Tigress (Story 3.2) — only persona values differ. Copy Tigress agent file and update:
- All persona fields from `default-party.csv` Monkey row
- Agent id, name, title, icon, capabilities

### Party Roster Values (from default-party.csv)

```
name: "monkey"
displayName: "Monkey"
title: "Python Dev Agent"
icon: "🐒"
role: "Python Code Generation Specialist"
identity: "Senior Python developer generating modern Python code from COBOL spec layer analysis..."
communicationStyle: "Energetic and pragmatic. Writes Pythonic code that reads like documentation..."
principles: "Python should be beautiful. Spec layer drives every decision..."
```

### Dependencies

- **Story 3.1** (dev workflows) — MUST be completed first
- **Story 3.2** (Tigress) — recommended to complete first as template, but not blocking

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.4]
- [Source: documents/planning-artifacts/architecture.md — Agent Roster, Monkey definition]
- [Source: _bmad/bmm/agents/dev.md — BMAD dev agent format reference]
- [Source: _bmad/mm/agents/shifu.md — MM agent format reference]
- [Source: _bmad/mm/teams/default-party.csv — Monkey persona values]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Created Monkey agent at _bmad/mm/agents/monkey.md with Python code generation persona
- Follows same pattern as Tigress (Story 3.2) with Python-specific persona values
- module-help.csv and party roster already had correct entries
- 12 new tests all pass; zero regressions
- Code review fix: added TestMonkeyPersonaIsolation tests — COBOL check scoped to <role> only (identity legitimately references COBOL as source language)

### Change Log

- 2026-03-08: Story 3.4 implemented — Monkey Python dev agent definition created
- 2026-03-08: Code review fix — persona isolation tests added

### File List

- _bmad/mm/agents/monkey.md (new)
- tests/test_monkey_agent.py (new)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-4-monkey-agent-definition-dev-python.md (modified)
