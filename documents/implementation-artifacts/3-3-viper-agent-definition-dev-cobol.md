# Story 3.3: Viper Agent Definition (Dev — COBOL)

Status: review

## Story

As an operator,
I want the Viper agent fully authored as the COBOL modernisation dev agent,
so that Viper can be invoked via `/bmad-agent-mm-viper` with the full dev agent menu adapted for COBOL modernisation.

## Acceptance Criteria

1. **AC1: Agent definition file**
   - Given the BMAD dev agent definition exists at `_bmad/bmm/agents/dev.md`
   - When the developer copies and adapts it to `_bmad/mm/agents/viper.md`
   - Then it contains: COBOL modernisation persona, works from Po's output documents, mainframe modernisation context
   - And the menu mirrors the full BMAD dev agent menu
   - And menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
   - And it declares access to `gitlab-mcp` MCP server only

2. **AC2: Agent installation and invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-viper`
   - Then Viper loads with her COBOL persona, presents the full dev menu, and responds in character

## Tasks / Subtasks

- [x] Task 1: Create Viper agent definition (AC: #1, #2)
  - [x] 1.1: Create `_bmad/mm/agents/viper.md` following BMAD agent format
  - [x] 1.2: Define COBOL modernisation persona using party roster values:
    - name: "Viper", title: "COBOL Dev Agent", icon: "🐍"
    - role: "COBOL Modernisation Specialist"
    - identity: "Senior COBOL developer modernising legacy code. Expert in COBOL refactoring, dialect handling, and structured programming patterns."
    - communication_style: "Direct and efficient. Thinks in paragraphs and copybooks. Respects the mainframe heritage while pushing forward."
    - principles: "Modernise without breaking. Preserve business logic exactly. Refactor structure, not semantics."
  - [x] 1.3: Define capabilities: story execution, test-driven development, COBOL modernisation, dialect handling
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
  - [x] 2.1: Confirm `module-help.csv` has Viper agent entry pointing to `_bmad/mm/agents/viper.md`
  - [x] 2.2: Confirm slash command is `bmad-agent-mm-viper`

- [x] Task 3: Verify party roster entry (AC: #2)
  - [x] 3.1: Confirm `_bmad/mm/teams/default-party.csv` has Viper entry with correct persona values

- [x] Task 4: Write tests (AC: #1, #2)
  - [x] 4.1: Test `_bmad/mm/agents/viper.md` exists
  - [x] 4.2: Test agent file contains `<persona>` with COBOL-specific content
  - [x] 4.3: Test agent file contains `<menu>` with all required items (MH, CH, DS, CR, PM, DA)
  - [x] 4.4: Test agent file contains `<activation` section
  - [x] 4.5: Test agent file references `_bmad/mm/config.yaml` (not BMM config)
  - [x] 4.6: Test agent file references `_bmad/mm/workflows/dev/` for workflow paths
  - [x] 4.7: Test agent file declares `gitlab-mcp` access
  - [x] 4.8: Test agent file does NOT reference `specdb-mcp`
  - [x] 4.9: Test module-help.csv has Viper entry
  - [x] 4.10: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/viper.md`** — per architecture project structure
- **Config source: `_bmad/mm/config.yaml`** — MM module config, NOT BMM
- **Workflows point to `_bmad/mm/workflows/dev/`** — shared dev workflows from Story 3.1
- **MCP access: `gitlab-mcp` only** — dev agents consume Po's documents, not specdb directly
- **No specdb-mcp access** — agents work from documents produced by Po
- **COBOL persona drives target language** — Viper modernises COBOL (refactoring, not cross-language translation)

### Key Differences from Tigress (Story 3.2)

| Aspect | Tigress | Viper |
|---|---|---|
| Target language | Java | COBOL (modernised) |
| Role | Code generation from COBOL to Java | COBOL refactoring and modernisation |
| Persona focus | Enterprise Java patterns | COBOL dialect handling, structured programming |
| FR coverage | FR23-25 (target code gen) | COBOL modernisation (refactoring existing code) |

### Copy Pattern

Structure is identical to Tigress (Story 3.2) — only persona values differ. Copy Tigress agent file and update:
- All persona fields from `default-party.csv` Viper row
- Agent id, name, title, icon, capabilities

### Party Roster Values (from default-party.csv)

```
name: "viper"
displayName: "Viper"
title: "COBOL Dev Agent"
icon: "🐍"
role: "COBOL Modernisation Specialist"
identity: "Senior COBOL developer modernising legacy code..."
communicationStyle: "Direct and efficient. Thinks in paragraphs and copybooks..."
principles: "Modernise without breaking. Preserve business logic exactly..."
```

### Dependencies

- **Story 3.1** (dev workflows) — MUST be completed first
- **Story 3.2** (Tigress) — recommended to complete first as template, but not blocking

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.3]
- [Source: documents/planning-artifacts/architecture.md — Agent Roster, Viper definition]
- [Source: _bmad/bmm/agents/dev.md — BMAD dev agent format reference]
- [Source: _bmad/mm/agents/shifu.md — MM agent format reference]
- [Source: _bmad/mm/teams/default-party.csv — Viper persona values]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Created Viper agent at _bmad/mm/agents/viper.md with COBOL modernisation persona
- Follows same pattern as Tigress (Story 3.2) with COBOL-specific persona values
- module-help.csv and party roster already had correct entries
- 12 new tests all pass; zero regressions
- Code review fix: added TestViperPersonaIsolation tests to prevent cross-language persona contamination

### Change Log

- 2026-03-08: Story 3.3 implemented — Viper COBOL dev agent definition created
- 2026-03-08: Code review fix — persona isolation tests added

### File List

- _bmad/mm/agents/viper.md (new)
- tests/test_viper_agent.py (new)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-3-viper-agent-definition-dev-cobol.md (modified)
