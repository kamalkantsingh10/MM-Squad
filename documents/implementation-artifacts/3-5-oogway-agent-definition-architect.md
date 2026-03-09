# Story 3.5: Oogway Agent Definition (Architect)

Status: review

## Story

As an operator,
I want the Oogway agent fully authored as the migration architect,
so that Oogway can be invoked via `/bmad-agent-mm-oogway` with the full architect agent menu adapted for mainframe migration.

## Acceptance Criteria

1. **AC1: Agent definition file**
   - Given the BMAD architect agent definition and workflows exist
   - When the developer copies and adapts the agent to `_bmad/mm/agents/oogway.md`
   - Then it contains: mainframe migration architect persona, consumes Po's output documents for architecture decisions
   - And the menu mirrors the full BMAD architect agent menu (create-architecture, check-implementation-readiness, chat, and all other items)
   - And it declares access to `gitlab-mcp` MCP server only

2. **AC2: Architect workflows copied and adapted**
   - Given the BMAD architect workflows exist at `_bmad/bmm/workflows/3-solutioning/`
   - When the developer copies and adapts them to `_bmad/mm/workflows/architect/`
   - Then all architect workflows are present with step files adapted for MM context
   - And create-architecture workflow accepts Po's dependency maps and business rules documents as inputs
   - And the target language decision (FR21) is captured in the architecture workflow
   - And FR19, FR20, FR21, FR22 are addressable through the adapted workflows

3. **AC3: Agent installation and invocation**
   - Given the MM module is installed via `bmad reinstall`
   - When the operator invokes `/bmad-agent-mm-oogway`
   - Then Oogway loads with his migration architect persona, presents the full architect menu, and responds in character

## Tasks / Subtasks

- [x] Task 1: Create Oogway agent definition (AC: #1, #3)
  - [x] 1.1: Create `_bmad/mm/agents/oogway.md` following BMAD agent format
  - [x] 1.2: Define migration architect persona using party roster values:
    - name: "Oogway", title: "Migration Architect", icon: "🐢"
    - role: "Migration Architecture Specialist"
    - identity: "Senior architect designing target-state architectures from spec layer analysis. Expert in mainframe-to-modern migration patterns."
    - communication_style: "Wise and deliberate. Considers every trade-off. Architecture decisions are permanent — measure twice, cut once."
    - principles: "There are no accidents in architecture. Spec layer is truth. Target architecture serves the business, not the technology."
  - [x] 1.3: Define capabilities: migration architecture, target language selection, subsystem mapping, dependency analysis
  - [x] 1.4: Add activation steps following BMAD agent activation pattern — config from `_bmad/mm/config.yaml`
  - [x] 1.5: Declare `gitlab-mcp` MCP server access via `<mcp-servers>` section
  - [x] 1.6: Define menu mirroring BMM architect agent:
    - [MH] Redisplay Menu Help
    - [CH] Chat with the Agent
    - [CA] Create Architecture — workflow/exec: `{project-root}/_bmad/mm/workflows/architect/create-architecture/workflow.md`
    - [IR] Implementation Readiness — workflow/exec: `{project-root}/_bmad/mm/workflows/architect/check-implementation-readiness/workflow.md`
    - [PM] Start Party Mode — exec: `{project-root}/_bmad/core/workflows/party-mode/workflow.md`
    - [DA] Dismiss Agent

- [x] Task 2: Create architect workflow directory structure (AC: #2)
  - [x] 2.1: Create `_bmad/mm/workflows/architect/create-architecture/` directory
  - [x] 2.2: Create `_bmad/mm/workflows/architect/check-implementation-readiness/` directory

- [x] Task 3: Copy and adapt create-architecture workflow (AC: #2)
  - [x] 3.1: Copy `_bmad/bmm/workflows/3-solutioning/create-architecture/workflow.md` and adapt for MM context
  - [x] 3.2: Copy step files from `steps/` directory and adapt:
    - Inputs reference Po's dependency maps, business rules documents, structural analysis
    - Target language decision (FR21) captured as explicit step
    - Architecture outputs inform downstream dev agents (Tigress/Viper/Monkey)
  - [x] 3.3: Copy `architecture-decision-template.md` and adapt for migration context
  - [x] 3.4: Copy `data/` directory (domain-complexity.csv, project-types.csv) if applicable
  - [x] 3.5: Add `gitlab-mcp` references for progress tracking

- [x] Task 4: Copy and adapt check-implementation-readiness workflow (AC: #2)
  - [x] 4.1: Copy `_bmad/bmm/workflows/3-solutioning/check-implementation-readiness/workflow.md` and adapt
  - [x] 4.2: Copy step files and adapt — validation checks Po's outputs + Oogway's architecture
  - [x] 4.3: Copy templates directory and adapt readiness report for migration context

- [x] Task 5: Verify module-help.csv entries (AC: #3)
  - [x] 5.1: Confirm `module-help.csv` has Oogway agent entry
  - [x] 5.2: Confirm create-architecture and check-implementation-readiness workflow entries exist
  - [x] 5.3: Confirm all paths point to `_bmad/mm/workflows/architect/`

- [x] Task 6: Verify party roster entry (AC: #3)
  - [x] 6.1: Confirm `_bmad/mm/teams/default-party.csv` has Oogway entry

- [x] Task 7: Write tests (AC: #1, #2, #3)
  - [x] 7.1: Test `_bmad/mm/agents/oogway.md` exists
  - [x] 7.2: Test agent file contains `<persona>` with architect/migration content
  - [x] 7.3: Test agent file contains `<menu>` with all required items (MH, CH, CA, IR, PM, DA)
  - [x] 7.4: Test agent file contains `<activation` section
  - [x] 7.5: Test agent file references `_bmad/mm/config.yaml` (not BMM config)
  - [x] 7.6: Test agent file references `_bmad/mm/workflows/architect/` for workflow paths
  - [x] 7.7: Test agent file declares `gitlab-mcp` access
  - [x] 7.8: Test architect workflow directories exist with workflow files and step files
  - [x] 7.9: Test create-architecture workflow references Po's outputs as inputs
  - [x] 7.10: Test module-help.csv has Oogway + workflow entries
  - [x] 7.11: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Agent file at `_bmad/mm/agents/oogway.md`** — per architecture project structure
- **Workflows at `_bmad/mm/workflows/architect/`** — per architecture directory structure
- **Config source: `_bmad/mm/config.yaml`** — MM module config
- **MCP access: `gitlab-mcp` only** — Oogway consumes Po's documents for architecture decisions
- **No specdb-mcp access** — explicit in architecture: agents consume documents, not spec layer
- **Target language decision (FR21)** — Oogway decides Java/COBOL/Python; this decision feeds into `_bmad/mm/config.yaml` `target_language` field

### BMAD Architect Agent Format Reference

Copy structure from `_bmad/bmm/agents/architect.md` (Winston):
- Note: BMM architect uses `exec` handler type, not `workflow` handler type
- Menu items use `exec="path/to/workflow.md"` format
- `<menu-handlers>` section defines `exec` handler (read file and follow instructions)
- This is different from dev/SM agents which use `workflow` handler

### Source Files to Copy From

| BMM Source | MM Target |
|---|---|
| `_bmad/bmm/agents/architect.md` | `_bmad/mm/agents/oogway.md` |
| `_bmad/bmm/workflows/3-solutioning/create-architecture/` (entire dir) | `_bmad/mm/workflows/architect/create-architecture/` |
| `_bmad/bmm/workflows/3-solutioning/check-implementation-readiness/` (entire dir) | `_bmad/mm/workflows/architect/check-implementation-readiness/` |

### Create-Architecture Workflow Structure (BMM source)

```
create-architecture/
├── workflow.md
├── architecture-decision-template.md
├── data/
│   ├── domain-complexity.csv
│   └── project-types.csv
└── steps/
    ├── step-01-init.md
    ├── step-01b-continue.md
    ├── step-02-context.md
    ├── step-03-starter.md
    ├── step-04-decisions.md
    ├── step-05-patterns.md
    ├── step-06-structure.md
    ├── step-07-validation.md
    └── step-08-complete.md
```

### Check-Implementation-Readiness Workflow Structure (BMM source)

```
check-implementation-readiness/
├── workflow.md
├── templates/
│   └── readiness-report-template.md
└── steps/
    ├── step-01-document-discovery.md
    ├── step-02-prd-analysis.md
    ├── step-03-epic-coverage-validation.md
    ├── step-04-ux-alignment.md
    ├── step-05-epic-quality-review.md
    └── step-06-final-assessment.md
```

### Key Adaptations for MM Context

1. **Create-Architecture inputs**: Instead of generic PRD/UX, consume Po's outputs:
   - Structural analysis (call graphs, complexity scores)
   - Dependency maps (Mermaid diagrams, subsystem groupings, migration order)
   - Business rules documents (extracted business markdown)
2. **Target language decision**: Add explicit step for Oogway to decide Java/COBOL/Python
3. **Architecture output**: Must inform Tigress/Viper/Monkey — target architecture maps COBOL subsystems to target-language services
4. **Check-readiness inputs**: Validate Po's outputs + Oogway's architecture are complete before dev starts

### Functional Requirements Addressed

- FR19: Architect can initiate migration architecture generation
- FR20: Architect can view target architecture document
- FR21: Architect can specify target language
- FR22: Architect can review and modify architecture

### Party Roster Values (from default-party.csv)

```
name: "oogway"
displayName: "Oogway"
title: "Migration Architect"
icon: "🐢"
role: "Migration Architecture Specialist"
identity: "Senior architect designing target-state architectures from spec layer analysis..."
communicationStyle: "Wise and deliberate. Considers every trade-off..."
principles: "There are no accidents in architecture. Spec layer is truth..."
```

### Dependencies

- Epic 1 (MM module foundation) — complete
- Epic 2 Story 2.7 (Shifu) — MM agent pattern reference
- No dependency on Story 3.1 (dev workflows) — Oogway has its own architect workflows

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.5]
- [Source: documents/planning-artifacts/architecture.md — Agent Roster, Oogway definition]
- [Source: _bmad/bmm/agents/architect.md — BMAD architect agent format reference]
- [Source: _bmad/bmm/workflows/3-solutioning/create-architecture/ — BMM source workflow]
- [Source: _bmad/bmm/workflows/3-solutioning/check-implementation-readiness/ — BMM source workflow]
- [Source: _bmad/mm/teams/default-party.csv — Oogway persona values]
- [Source: _bmad/mm/module-help.csv — Oogway + workflow registry entries]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Created Oogway agent at _bmad/mm/agents/oogway.md with migration architect persona
- Uses `exec` handler type (same as BMM architect), not `workflow` handler
- Copied create-architecture workflow (workflow.md + 9 step files + template + data/) from BMM and adapted all paths
- Copied check-implementation-readiness workflow (workflow.md + 6 step files + templates/) from BMM and adapted all paths
- All BMM path references replaced with MM equivalents across all step files (verified zero remaining)
- gitlab-mcp declared; specdb-mcp excluded per architecture
- module-help.csv and party roster already had correct entries
- 23 new tests all pass; zero regressions
- Code review fix: step-02-prd-analysis.md fully rewritten as step-02-po-output-analysis.md — now validates Po's structural analysis, dependency maps, and business rules rather than PRD/FRs/NFRs; persona corrected from "Product Manager and Scrum Master" to Oogway's architect role
- Code review fix: step-04-ux-alignment.md fully rewritten as step-04-target-architecture-alignment.md — UX validation replaced with target architecture completeness check (target language decision, subsystem coverage, architecture-to-Po-output alignment)

### Change Log

- 2026-03-08: Story 3.5 implemented — Oogway architect agent and workflows created
- 2026-03-08: Code review fixes — step-02 and step-04 rewritten for MM context (Po output analysis + architecture alignment)

### File List

- _bmad/mm/agents/oogway.md (new)
- _bmad/mm/workflows/architect/create-architecture/workflow.md (new, adapted from BMM)
- _bmad/mm/workflows/architect/create-architecture/architecture-decision-template.md (new, copied from BMM)
- _bmad/mm/workflows/architect/create-architecture/data/domain-complexity.csv (new, copied from BMM)
- _bmad/mm/workflows/architect/create-architecture/data/project-types.csv (new, copied from BMM)
- _bmad/mm/workflows/architect/create-architecture/steps/step-01-init.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-01b-continue.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-02-context.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-03-starter.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-04-decisions.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-05-patterns.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-06-structure.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-07-validation.md (new, adapted)
- _bmad/mm/workflows/architect/create-architecture/steps/step-08-complete.md (new, adapted)
- _bmad/mm/workflows/architect/check-implementation-readiness/workflow.md (new, adapted from BMM)
- _bmad/mm/workflows/architect/check-implementation-readiness/templates/readiness-report-template.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-01-document-discovery.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-02-prd-analysis.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-03-epic-coverage-validation.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-04-ux-alignment.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-05-epic-quality-review.md (new, copied)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-06-final-assessment.md (new, copied)
- tests/test_oogway_agent.py (new)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-02-prd-analysis.md (modified — rewritten for MM context by code review)
- _bmad/mm/workflows/architect/check-implementation-readiness/steps/step-04-ux-alignment.md (modified — rewritten for MM context by code review)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-5-oogway-agent-definition-architect.md (modified)
