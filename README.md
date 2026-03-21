# MM-Squad — Mainframe Modernisation Agents

An AI agent pipeline for mainframe modernisation, built as a [BMAD](https://github.com/bmadcode/BMAD-METHOD) expansion pack. 8 agents and 5 MCP servers work together to analyse COBOL/JCL source code, extract business rules, design target architectures, generate modern code, and manage delivery through GitLab.

## What Is This?

Traditional agile assumes you understand what you're building. COBOL estates break that assumption — no documentation, no living institutional knowledge, systems that have accreted business rules over decades. The industry has a **70% failure rate** applying standard agile to mainframe modernisation.

MM-Squad reimagines the SDLC for COBOL modernisation through specialised AI agents, each with a distinct role in the pipeline. The agents are themed after characters from **Kung Fu Panda** — because modernising a 30-year-old mainframe takes a whole squad.

### How It Works

The pipeline is **human-orchestrated, not automated**. You invoke agents via slash commands, each presents a menu of workflows, and you decide what to run, when, and on which module. The recommended pipeline order:

```
Po (Analyse) → Tigress (Architecture) → Shifu (Project Setup)
    → Crane/Viper/Monkey (Code Generation) → Oogway (Review) → Tai Lung (QA)
```

Each workflow is independently runnable. A SQLite spec layer carries structured data between agents. You carry the intent.

## The Squad

### 🐼 Po — COBOL Analysis Agent
The centrepiece. Po analyses COBOL source code through three workflows: structural analysis (call graphs, complexity, anti-patterns), cross-module dependency mapping (subsystem detection, migration order), and business rule extraction (entities, operations, rules, data flows). Every finding goes through a human review gate before being written to the spec layer.

**Key workflows:** Analyse Structure, Map Dependencies, Extract Business Rules, View Flags

### 🐯 Tigress — Migration Architect
Fierce and disciplined. Tigress designs target-state architectures from the spec layer, mapping COBOL subsystems to modern services. She decides the target language and owns every architectural trade-off. Declarative, precise — treats the spec layer as a contract.

**Key workflows:** Create Architecture

### 🐭 Shifu — Delivery Manager (PM + SM)
Calm authority. Shifu orchestrates the entire project through GitLab — creating epics, planning sprints, tracking progress, and managing course corrections. Every deliverable has an owner, every milestone drives urgency.

**Key workflows:** Project Initialisation, Sprint Planning, Create Story, Sprint Status, Course Correction

### 🐢 Oogway — Auditor
The supreme quality gate. Wise, unhurried, philosophical. Nothing ships without Oogway's blessing. He validates PRDs, checks implementation readiness, performs adversarial code reviews, and runs epic retrospectives. Finds the one gap in a 50-page document and asks about it with a smile.

**Key workflows:** Validate PRD, Implementation Readiness, Code Review, Epic Retrospective

### 🦅 Crane — Java Dev Agent
Humble and quietly brilliant. Crane generates modern Java code from the spec layer and Tigress's architecture. Lets the code speak for itself. Apologises before suggesting a better approach, then delivers the simplest solution everyone else overcomplicated.

**Key workflows:** Dev Story

### 🐍 Viper — COBOL Dev Agent
Warm and respectful of legacy. Viper modernises COBOL — refactoring structure without changing semantics. Acknowledges what existing code got right before proposing changes. Treats every copybook as worth understanding.

**Key workflows:** Dev Story

### 🐒 Monkey — Python Dev Agent
High energy and pragmatic. Monkey generates modern Python from the spec layer. Fast iterations, clean results. Thinks out loud during implementation, celebrates small wins, and keeps "ship it and iterate" in check against the acceptance criteria.

**Key workflows:** Dev Story

### 🐆 Tai Lung — QA Agent
Powerful and uncompromising. Tai Lung validates generated code against spec layer business rules. Every test is a challenge issued. Every passing suite is a battle won. Clean implementations earn a rare "Worthy." Will run a test suite one extra time even after it passes, just to be certain.

**Key workflows:** Generate E2E Tests

## MCP Servers

The capability layer — 5 Python MCP servers that give agents access to specialised tools:

| Server | Purpose |
|--------|---------|
| `cobol-parser-mcp` | COBOL static parsing — call graphs, complexity scoring, anti-pattern detection |
| `specdb-mcp` | SQLite spec layer CRUD — the shared intermediate representation across all agents |
| `delta-macros-mcp` | Client-specific macro and middleware knowledge base |
| `jcl-parser-mcp` | JCL job/step/dataset parsing |
| `gitlab-mcp` | Full GitLab integration — epics, issues, milestones, boards, comments, README updates |

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) 1.8+

## Installation

All installations share a common first step — copying the BMAD framework and MCP servers.

### Step 1: Common Files (required for all IDEs)

```bash
# BMAD framework (agents, workflows, config)
cp -r _bmad/ <target-project>/_bmad/

# MCP servers (Python packages)
cp -r mcp-servers/ <target-project>/mcp-servers/
cp pyproject.toml poetry.lock <target-project>/

# Install Python dependencies
cd <target-project>
poetry install
```

### Step 2a: Claude Code

```bash
# Slash commands (one per agent + workflow shortcuts)
mkdir -p <target-project>/.claude/commands
cp .claude/commands/bmad-*.md <target-project>/.claude/commands/

# MCP server registration (tells Claude Code how to start each server)
cp .claude/mcp.json <target-project>/.claude/mcp.json

# Auto-allow permissions for GitLab operations (optional — saves clicking "allow" each time)
cp .claude/settings.local.json <target-project>/.claude/settings.local.json
```

**Usage:** Type `/bmad-agent-mm-crane` (or any agent name) in Claude Code to invoke an agent.

| What gets copied | Purpose |
|-----------------|---------|
| `.claude/commands/bmad-*.md` | Slash commands — one per agent and workflow |
| `.claude/mcp.json` | Registers 5 MCP servers with Claude Code |
| `.claude/settings.local.json` | Pre-approves GitLab MCP tool permissions |

### Step 2b: GitHub Copilot (VS Code / Cursor)

```bash
# Agent files (one per agent — appears as @mention in Copilot Chat)
mkdir -p <target-project>/.github/agents
cp .github/agents/bmad-*.md <target-project>/.github/agents/

# MCP server registration (tells VS Code how to start each server)
mkdir -p <target-project>/.vscode
cp .vscode/mcp.json <target-project>/.vscode/mcp.json
```

**Usage:** Type `@bmad-agent-mm-crane` (or any agent name) in Copilot Chat to invoke an agent.

| What gets copied | Purpose |
|-----------------|---------|
| `.github/agents/bmad-*.agent.md` | Copilot agent definitions — one per agent |
| `.vscode/mcp.json` | Registers 5 MCP servers with VS Code |

### Step 2c: Both IDEs

If you use both Claude Code and GitHub Copilot, run both Step 2a and Step 2b.

### MCP Servers

MCP servers start automatically when the IDE invokes them. To run one manually:

```bash
poetry run python -m <package>.server
```

Where `<package>` is one of: `cobol_parser_mcp`, `specdb_mcp`, `delta_macros_mcp`, `jcl_parser_mcp`, `gitlab_mcp`.

## Quick Reference

| Agent | Role | Claude Code | GitHub Copilot |
|-------|------|-------------|----------------|
| **Po** 🐼 | COBOL Analysis | `/bmad-agent-mm-po` | `@bmad-agent-mm-po` |
| **Tigress** 🐯 | Migration Architect | `/bmad-agent-mm-tigress` | `@bmad-agent-mm-tigress` |
| **Shifu** 🐭 | Delivery Manager | `/bmad-agent-mm-shifu` | `@bmad-agent-mm-shifu` |
| **Oogway** 🐢 | Auditor | `/bmad-agent-mm-oogway` | `@bmad-agent-mm-oogway` |
| **Crane** 🦅 | Dev (Java) | `/bmad-agent-mm-crane` | `@bmad-agent-mm-crane` |
| **Viper** 🐍 | Dev (COBOL) | `/bmad-agent-mm-viper` | `@bmad-agent-mm-viper` |
| **Monkey** 🐒 | Dev (Python) | `/bmad-agent-mm-monkey` | `@bmad-agent-mm-monkey` |
| **Tai Lung** 🐆 | QA | `/bmad-agent-mm-tai-lung` | `@bmad-agent-mm-tai-lung` |

## Project Structure

```
<project>/
├── _bmad/
│   ├── core/              # BMAD core framework
│   ├── bmm/               # BMAD Module Manager
│   └── mm/                # MM expansion pack
│       ├── agents/        # 8 agent definitions
│       ├── workflows/     # Agent workflows
│       ├── config.yaml    # Module config
│       └── module-help.csv
├── .claude/
│   ├── commands/          # Claude Code slash commands
│   └── mcp.json           # MCP server config (Claude Code)
├── .github/agents/        # GitHub Copilot agent files
├── .vscode/
│   └── mcp.json           # MCP server config (VS Code / Cursor)
├── mcp-servers/           # 5 Python MCP servers
├── pyproject.toml         # Poetry config
└── poetry.lock
```

See `_bmad/mm/README.md` for detailed agent menus and build status.
