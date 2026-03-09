# MM — Mainframe Modernisation Expansion Pack

BMAD expansion pack module providing AI-driven mainframe modernisation capability. Installs into `_bmad/mm/` alongside BMAD core. Agents are invoked via `/bmad-agent-mm-<name>` slash commands after `bmad reinstall`.

## Agents

| Agent | Character | Role | MCP Access |
|-------|-----------|------|------------|
| **Po** | Panda | Analysis Agent (NEW) | `cobol-parser-mcp`, `specdb-mcp`, `delta-macros-mcp`, `jcl-parser-mcp` |
| **Oogway** | Tortoise | Migration Architect | `specdb-mcp`, `gitlab-mcp` |
| **Shifu** | Red Panda | PM + SM — Delivery Orchestrator | `gitlab-mcp`, `specdb-mcp` |
| **Tigress** | Tiger | Dev (Java) | `specdb-mcp`, `cobol-parser-mcp` |
| **Viper** | Snake | Dev (COBOL) | `specdb-mcp`, `cobol-parser-mcp` |
| **Monkey** | Monkey | Dev (Python) | `specdb-mcp`, `cobol-parser-mcp` |
| **Mantis** | Mantis | QA — Migration Validation | `specdb-mcp`, `gitlab-mcp` |

## Agent Menus

### Po — Analysis Agent
| # | Command | Workflow |
|---|---------|----------|
| 1 | Analyse COBOL Module Structure | `analyse-structure/` — static pre-pass, semantic clustering, AI analysis, review gate, spec write |
| 2 | Map Cross-Module Dependencies | `map-dependencies/` — regex extraction, graph build, subsystem detection, migration order |
| 3 | Extract Business Rules | `extract-business-rules/` — consume analysis, extract rules, business markdown, spec layer |
| 4 | View Consolidated Flags | `view-flags/` — all unresolved constructs and macros across runs |
| 5 | Chat with Po | Free-form conversation |

### Shifu — PM + SM (Delivery Orchestrator)
| # | Command | Workflow |
|---|---------|----------|
| 1 | Project Initialisation | `create-epics-and-stories/` — GitLab labels, milestones, board, Epics, Issues |
| 2 | Sprint Planning | `sprint-planning/` — create milestone, assign modules by dependency order |
| 3 | Create Story | `create-story/` — new module Issue with complexity and milestone |
| 4 | Sprint Status | `sprint-status/` — progress, burndown, blockers |
| 5 | Course Correction | `correct-course/` — adjust scope, reassign Issues mid-sprint |
| 6 | Retrospective | `retrospective/` — sprint summary, learnings, post to Epic |
| 7 | Party Mode | Multi-agent group discussion |

### Oogway — Migration Architect
| # | Command | Workflow |
|---|---------|----------|
| 1 | Create Migration Architecture | `create-architecture/` — target architecture from spec layer |
| 2 | Check Implementation Readiness | `check-implementation-readiness/` — validate specs are complete |

### Tigress / Viper / Monkey — Dev Agents
| # | Command | Workflow |
|---|---------|----------|
| 1 | Dev Story | `dev-story/` — code generation from spec layer + architecture |
| 2 | Code Review | `code-review/` — adversarial review of generated code |

### Mantis — QA
| # | Command | Workflow |
|---|---------|----------|
| 1 | Generate E2E Tests | `qa-generate-e2e-tests/` — validate generated code against spec rules |

## Pipeline Order (Guidance, Not Enforcement)

```
Po (Analyse Structure) → Po (Map Dependencies) → Po (Extract Business Rules)
    → Oogway (Migration Architecture) → Shifu (GitLab Project Setup)
    → Tigress/Viper/Monkey (Code Generation) → Mantis (QA Validation)
```

Each workflow is independently runnable. The spec layer (SQLite) carries context between workflows — the operator carries intent.

## Configuration

Agent-level config lives in `_bmad/mm/config.yaml` (user name, language, glossary path). MCP server config is independent — each server has its own `config.yaml` and `.env` under `mcp-servers/<server>/`. See each server's README for details.

## Build Status

| Agent | Status |
|-------|--------|
| Shifu | Implemented — `agents/shifu.md` |
| Po | Not started |
| Oogway | Not started |
| Tigress | Not started |
| Viper | Not started |
| Monkey | Not started |
| Mantis | Not started |
