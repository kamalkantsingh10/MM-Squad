# MM-Squad

BMAD expansion pack for mainframe modernisation — AI agent pipeline with 8 agents and 5 MCP servers that analyse COBOL/JCL source, build spec databases, and manage delivery through GitLab.

## Agents

| Agent | Role | Slash Command |
|-------|------|---------------|
| **Po** 🐼 | COBOL Analysis | `/bmad-agent-mm-po` |
| **Tigress** 🐯 | Migration Architect | `/bmad-agent-mm-tigress` |
| **Shifu** 🐭 | Delivery Manager (PM + SM) | `/bmad-agent-mm-shifu` |
| **Oogway** 🐢 | Auditor | `/bmad-agent-mm-oogway` |
| **Crane** 🦅 | Dev (Java) | `/bmad-agent-mm-crane` |
| **Viper** 🐍 | Dev (COBOL) | `/bmad-agent-mm-viper` |
| **Monkey** 🐒 | Dev (Python) | `/bmad-agent-mm-monkey` |
| **Tai Lung** 🐆 | QA | `/bmad-agent-mm-tai-lung` |

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

See `_bmad/mm/README.md` for detailed agent menus, pipeline order, and build status.
