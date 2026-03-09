# MM-Squad

BMAD expansion pack for mainframe modernisation — AI agent pipeline with 7 agents and 5 MCP servers that analyse COBOL/JCL source, build spec databases, and manage delivery through GitLab.

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) 1.8+

## Setup

```bash
poetry install
```

## Running MCP Servers

Individual servers are run via:

```bash
poetry run python -m <package>.server
```

Where `<package>` is one of: `cobol_parser_mcp`, `specdb_mcp`, `delta_macros_mcp`, `jcl_parser_mcp`, `gitlab_mcp`.
