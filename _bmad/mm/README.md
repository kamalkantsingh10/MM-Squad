# MM — Mainframe Modernisation Expansion Pack

BMAD expansion pack module providing AI-driven mainframe modernisation capability. Installs into `_bmad/mm/` alongside BMAD core. Agents are invoked via `/bmad-agent-mm-<name>` slash commands after `bmad reinstall`.

## Agents

| Agent | Character | Role | MCP Access |
|-------|-----------|------|------------|
| **Po** | Panda | Analysis Agent (NEW) | `cobol-parser-mcp`, `specdb-mcp`, `delta-macros-mcp`, `jcl-parser-mcp` |
| **Tigress** | Tiger | Migration Architect | `specdb-mcp`, `gitlab-mcp` |
| **Shifu** | Red Panda | PM + SM — Delivery Orchestrator | `gitlab-mcp`, `specdb-mcp` |
| **Oogway** | Tortoise | Auditor — Quality Gate Guardian | `specdb-mcp`, `gitlab-mcp` |
| **Crane** | Crane | Dev (Java) | `specdb-mcp`, `cobol-parser-mcp` |
| **Viper** | Snake | Dev (COBOL) | `specdb-mcp`, `cobol-parser-mcp` |
| **Monkey** | Monkey | Dev (Python) | `specdb-mcp`, `cobol-parser-mcp` |
| **Tai Lung** | Snow Leopard | QA — Migration Validation | `specdb-mcp`, `gitlab-mcp` |

## Agent Menus

### 🐼 Po — Analysis Agent (`/bmad-agent-mm-po`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Ask questions about the loaded codebase |
| AS | Analyse Structure | Parse COBOL module — call graph, complexity, anti-patterns, external refs |
| MD | Map Dependencies | Cross-module dependency graph, subsystems, migration order |
| BR | Extract Business Rules | Business entities, operations, rules, data flows per module |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐭 Shifu — Delivery Manager (`/bmad-agent-mm-shifu`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| PI | Project Initialisation | Set up GitLab project with labels, milestones, board, Epics, and module Issues |
| SP | Sprint Planning | Create sprint milestone and assign modules respecting dependency order |
| CS | Create Story | Create a new module Issue with complexity label and milestone assignment |
| SS | Sprint Status | View current sprint progress, burndown, and blockers |
| CC | Course Correction | Adjust sprint scope, reassign Issues, manage mid-sprint changes |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐯 Tigress — Migration Architect (`/bmad-agent-mm-tigress`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| CA | Create Architecture | Migration architecture from Po's analysis and spec layer |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐢 Oogway — Auditor (`/bmad-agent-mm-oogway`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| VP | Validate PRD | Validate a Product Requirements Document is comprehensive, lean and cohesive |
| IR | Implementation Readiness | Validate PRD, architecture, UX and epics are complete and aligned |
| CR | Code Review | Comprehensive adversarial code review across multiple quality facets |
| RR | Epic Retrospective | Post-epic review to extract lessons and assess success |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🦅 Crane — Java Dev Agent (`/bmad-agent-mm-crane`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| DS | Dev Story | Write the next or specified story's tests and code |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐍 Viper — COBOL Dev Agent (`/bmad-agent-mm-viper`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| DS | Dev Story | Write the next or specified story's tests and code |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐒 Monkey — Python Dev Agent (`/bmad-agent-mm-monkey`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| DS | Dev Story | Write the next or specified story's tests and code |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

### 🐆 Tai Lung — QA Agent (`/bmad-agent-mm-tai-lung`)
| Code | Command | Description |
|------|---------|-------------|
| MH | Menu Help | Redisplay menu |
| CH | Chat | Chat with the Agent about anything |
| QA | Automate | Generate validation tests for migrated code against business rules |
| PM | Party Mode | Multi-agent group discussion |
| DA | Dismiss Agent | Exit |

## Pipeline Order (Guidance, Not Enforcement)

```
Po (Analyse Structure) → Po (Map Dependencies) → Po (Extract Business Rules)
    → Tigress (Migration Architecture) → Shifu (GitLab Project Setup)
    → Crane/Viper/Monkey (Code Generation) → Oogway (Code Review) → Tai Lung (QA Validation)
```

Each workflow is independently runnable. The spec layer (SQLite) carries context between workflows — the operator carries intent.

## Configuration

Agent-level config lives in `_bmad/mm/config.yaml` (user name, language, glossary path). MCP server config is independent — each server has its own `config.yaml` and `.env` under `mcp-servers/<server>/`. See each server's README for details.

## Build Status

| Agent | Status |
|-------|--------|
| Shifu | Implemented — `agents/shifu.md` |
| Po | Not started |
| Tigress | Implemented — `agents/tigress.md` (Migration Architect) |
| Oogway | Implemented — `agents/oogway.md` (Auditor) |
| Crane | Implemented — `agents/crane.md` (Java Dev) |
| Viper | Implemented — `agents/viper.md` |
| Monkey | Implemented — `agents/monkey.md` |
| Tai Lung | Implemented — `agents/tai-lung.md` (QA) |
