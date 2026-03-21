> **NOTE: Tigress has been reassigned to Migration Architect. The Java Dev role is now handled by Crane (`/bmad-agent-mm-crane`). This story documents the original implementation.**

# Story 3.2: Tigress Agent Definition (Dev — Java)

Status: review

## Story

As an operator,
I want the Tigress agent fully authored as the Java code generation dev agent,
so that Tigress can be invoked via `/bmad-agent-mm-tigress` with the full dev agent menu adapted for Java modernisation.

## Acceptance Criteria

1. **AC1: Agent definition file**
   - Given the BMAD dev agent definition exists at `_bmad/bmm/agents/dev.md`
   - When the developer copies and adapts it to `_bmad/mm/agents/tigress.md`
   - Then it contains: Java code generation persona, spec layer consumption via Po's documents, mainframe modernisation context
   - And the menu mirrors the full BMAD dev agent menu (dev-story, code-review, chat, and all other items)
   - And menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
   - And it declares access to `gitlab-mcp` MCP server only

2. **AC2: Agent installation and invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-tigress`
   - Then Tigress loads with her Java persona, presents the full dev menu, and responds in character
   - And FR23, FR24, FR25 are addressable through the dev-story workflow

## Tasks / Subtasks

- [x] Task 1: Create Tigress agent definition (AC: #1, #2)
  - [x] 1.1: Create `_bmad/mm/agents/tigress.md` following BMAD agent format
  - [x] 1.2: Define Java code generation persona using party roster values:
    - name: "Tigress", title: "Java Dev Agent", icon: "🐯"
    - role: "Java Code Generation Specialist"
    - identity: "Senior Java developer generating modern Java code from COBOL spec layer analysis. Expert in enterprise patterns and migration best practices."
    - communication_style: "Confident and precise. Speaks in clean code patterns. Every generated line traces to a spec layer entry."
    - principles: "Generated code must be as readable as hand-written. Spec layer is the contract. Test coverage is non-negotiable."
  - [x] 1.3: Define capabilities: story execution, test-driven development, Java code generation, spec layer consumption
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
  - [x] 2.1: Confirm `module-help.csv` has Tigress agent entry pointing to `_bmad/mm/agents/tigress.md`
  - [x] 2.2: Confirm slash command is `bmad-agent-mm-tigress`

- [x] Task 3: Verify party roster entry (AC: #2)
  - [x] 3.1: Confirm `_bmad/mm/teams/default-party.csv` has Tigress entry with correct persona values

- [x] Task 4: Write tests (AC: #1, #2)
  - [x] 4.1: Test `_bmad/mm/agents/tigress.md` exists
  - [x] 4.2: Test agent file contains `<persona>` with Java-specific content
  - [x] 4.3: Test agent file contains `<menu>` with all required items (MH, CH, DS, CR, PM, DA)
  - [x] 4.4: Test agent file contains `<activation` section
  - [x] 4.5: Test agent file references `_bmad/mm/config.yaml` (not BMM config)
  - [x] 4.6: Test agent file references `_bmad/mm/workflows/dev/` for workflow paths
  - [x] 4.7: Test agent file declares `gitlab-mcp` access
  - [x] 4.8: Test agent file does NOT reference `specdb-mcp`
  - [x] 4.9: Test module-help.csv has Tigress entry
  - [x] 4.10: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/tigress.md`** — per architecture project structure
- **Config source: `_bmad/mm/config.yaml`** — MM module config, NOT BMM
- **Workflows point to `_bmad/mm/workflows/dev/`** — shared dev workflows from Story 3.1 (MUST be completed first)
- **MCP access: `gitlab-mcp` only** — dev agents consume Po's documents, not specdb directly
- **No specdb-mcp access** — this is explicit in the architecture. Agents work from documents produced by Po
- **Java persona drives target language** — the workflow is language-agnostic; the agent persona determines Java-specific behaviour

### BMAD Dev Agent Format Reference

Copy structure from `_bmad/bmm/agents/dev.md` (Amelia):
- Frontmatter: `name`, `description`
- XML agent block with: `id`, `name`, `title`, `icon`, `capabilities`
- `<activation>` section with config loading + dev-specific steps (4-11)
- `<persona>` section with role, identity, communication_style, principles
- `<mcp-servers>` section (add this — not in BMM dev but needed for MM)
- `<menu>` section with workflow/exec attributes
- `<rules>` section

### Shifu Agent as MM Agent Reference

Use `_bmad/mm/agents/shifu.md` as the MM-specific agent reference:
- Shows how to reference `_bmad/mm/config.yaml` in activation step 2
- Shows `<mcp-servers>` section format
- Shows MM-specific rule for gitlab-mcp usage

### Key Differences from BMM Dev Agent

| Aspect | BMM Dev (Amelia) | MM Dev (Tigress) |
|---|---|---|
| Config | `_bmad/bmm/config.yaml` | `_bmad/mm/config.yaml` |
| Workflows | `_bmad/bmm/workflows/4-implementation/` | `_bmad/mm/workflows/dev/` |
| MCP access | None declared | `gitlab-mcp` |
| Persona | Generic software engineer | Java code generation specialist |
| Context | Standard BMAD projects | Mainframe modernisation |

### Party Roster Values (from default-party.csv)

```
name: "tigress"
displayName: "Tigress"
title: "Java Dev Agent"
icon: "🐯"
role: "Java Code Generation Specialist"
identity: "Senior Java developer generating modern Java code from COBOL spec layer analysis..."
communicationStyle: "Confident and precise. Speaks in clean code patterns..."
principles: "Generated code must be as readable as hand-written..."
```

### Functional Requirements Addressed

- FR23: Developer can initiate target-language code generation (Java via Tigress)
- FR24: Developer can view generated target-language code
- FR25: Developer can regenerate code for a specific module

### Dependencies

- **Story 3.1** (dev workflows) — MUST be completed first. Tigress menu references these workflows
- Epic 1 (MM module foundation) — complete
- Epic 2 Story 2.7 (Shifu) — MM agent pattern reference

### Project Structure Notes

- Agent file: `_bmad/mm/agents/tigress.md`
- Workflows: `_bmad/mm/workflows/dev/dev-story/` and `_bmad/mm/workflows/dev/code-review/` (from Story 3.1)
- Tests: `tests/` root directory

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.2]
- [Source: documents/planning-artifacts/architecture.md — Agent Roster, Tigress definition]
- [Source: _bmad/bmm/agents/dev.md — BMAD dev agent format reference]
- [Source: _bmad/mm/agents/shifu.md — MM agent format reference]
- [Source: _bmad/mm/teams/default-party.csv — Tigress persona values]
- [Source: _bmad/mm/module-help.csv — Tigress agent registry entry]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Created Tigress agent at _bmad/mm/agents/tigress.md with Java code generation persona from party roster
- Agent follows Shifu/BMM dev agent pattern: activation steps 1-16, menu-handlers, rules
- Dev-specific steps 4-11 mirror BMM dev agent (read story, execute tasks, mark complete, run tests)
- Menu items: MH, CH, DS, CR, PM, DA — DS and CR point to _bmad/mm/workflows/dev/ (Story 3.1)
- gitlab-mcp declared in <mcp-servers> section; no specdb-mcp access
- module-help.csv and party roster already had correct entries (pre-populated by SM)
- 12 new tests all pass; zero regressions
- Code review fix: added TestTigressPersonaIsolation tests to prevent cross-language persona contamination

### Change Log

- 2026-03-08: Story 3.2 implemented — Tigress Java dev agent definition created
- 2026-03-08: Code review fix — persona isolation tests added

### File List

- _bmad/mm/agents/tigress.md (new)
- tests/test_tigress_agent.py (new)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-2-tigress-agent-definition-dev-java.md (modified)
