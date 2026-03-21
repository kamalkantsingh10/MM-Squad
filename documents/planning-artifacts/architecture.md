---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
status: 'complete'
completedAt: '2026-03-06'
lastStep: 8
inputDocuments:
  - documents/planning-artifacts/prd.md
  - documents/planning-artifacts/prd-validation-report.md
  - docs/architecture.md
  - docs/project_idea.md
workflowType: 'architecture'
project_name: 'MM-Squad'
user_name: 'Kamal'
date: '2026-03-06'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

56 FRs across 9 capability groups:
- **COBOL Analysis (FR1-8):** Po structural analysis — static pre-pass (paragraph call graph, complexity scoring, anti-pattern detection, external reference extraction) followed by AI semantic clustering. Expert review and correction before spec layer writes. Unknown construct flagging is mandatory.
- **Dependency Mapping (FR9-13):** Po cross-module analysis producing Mermaid dependency graph, subsystem groupings, migration order, circular dependency / dead code detection.
- **Business Rule Extraction & Spec Layer (FR14-18):** Po business markdown per module plus full population of spec layer SQLite tables. Idempotent re-run support.
- **Migration Architecture (FR19-22):** Tigress consumes spec layer to produce target architecture. Analyst review before finalisation.
- **Code Generation (FR23-25):** Crane (Java), Viper (COBOL), Monkey (Python) generate target-language code from architecture + spec layer context.
- **QA Validation (FR26-28):** Tai Lung validates generated code against spec layer business rules. Manages Epic sign-off via GitLab.
- **Pipeline Configuration (FR29-34):** Single-command schema init, glossary config, incremental macro updates, BMAD installer, individual workflow re-run, consolidated flag list.
- **COBOL Dialect Coverage (FR35-39):** IBM Enterprise COBOL, COBOL-85, CICS, DB2 SQL, COPY/copybook resolution, Delta macro resolution via MCP.
- **GitLab Project Management (FR40-56):** Shifu initialises GitLab project (label taxonomy, milestones, boards). Per-module Issues track pipeline lifecycle. Sprint milestones. Live README dashboard. Business rule sign-off gate. QA Epic sign-off gate.

**Non-Functional Requirements:**

21 NFRs across 5 domains:
- **Performance:** Po Phase 1 < 15 min per module; parser tools < 30s for modules up to 5k lines; specdb ops < 2s; macro lookups < 1s; GitLab ops < 10s.
- **Security & Data Privacy (hard constraint):** No source code, business rules, or spec data transmitted outside local environment. Credentials via environment variables. Macro library never synced externally.
- **Reliability & Reproducibility:** Idempotent spec layer writes. No silent failures. Partial writes roll back or are flagged. MCP servers persist data across agent session restarts.
- **Integration & Compatibility:** BMAD-compatible (Claude Code + Cursor minimum). MCP protocol compliant. GitLab Cloud + self-hosted API v4. Versioned SQLite schema with migration support.
- **Maintainability:** Independently updatable agents and MCP servers. Human-readable glossary and macro formats. BlackJack corpus as regression baseline.

**Scale & Complexity:**

- Primary domain: Local-first AI agent pipeline / developer tooling (BMAD Expansion Pack)
- Complexity level: **High** — 8 agents (Po, Oogway, Shifu, Tigress, Crane, Viper, Monkey, Tai Lung), 5 MCP servers, SQLite schema, GitLab integration, COBOL dialect handling, BMAD packaging
- Estimated architectural components: 5 MCP servers (cobol-parser, specdb, delta-macros, jcl-parser, gitlab), 8 agent definitions, 1 SQLite database, 1 BMAD module installer, 1 glossary system, 1 macro library system
- Deployment model: Single developer machine, greenfield, local-only

### Technical Constraints & Dependencies

- **Data locality (hard):** All processing, storage, and agent-to-agent communication must remain local. No cloud data transmission for source code or extracted artefacts.
- **BMAD format compliance:** All agents, workflows, and step files must conform to BMAD module conventions for cross-IDE compatibility. Expansion pack installer must follow BMAD installer pattern.
- **MCP protocol compliance:** All 5 MCP servers must use standard MCP protocol — no proprietary extensions. Tools must be versioned and backwards-compatible.
- **SQLite as the sole database:** No graph database. SQLite is the spec layer intermediate representation between analysis and implementation agents.
- **LLM as an unreliable actor:** Every AI-produced output must have an explicit review gate before downstream consumption. No AI output is authoritative without analyst sign-off.
- **Target language TBD for MVP:** Tigress decides the target language — Crane (Java), Viper (COBOL), or Monkey (Python) handles code generation accordingly. Po's analysis remains target-language agnostic.
- **GitLab dependency:** GitLab (Cloud or self-hosted, API v4) is required for delivery management. Analysis stays local; GitLab manages Epics, Issues, and the status dashboard.
- **BMAD Expansion Pack identity:** The module installs into `_bmad/mm/` alongside existing modules (core, bmm). Must deploy via standard `bmad reinstall` and appear as slash commands.

### Cross-Cutting Concerns Identified

1. **Data locality enforcement** — Must be architecturally guaranteed across all 5 MCP servers and all 8 agents. No component should have a code path that transmits source or spec data externally.
2. **Idempotency** — Spec layer writes across all agents must be idempotent. Re-running any workflow on any module must produce equivalent output without duplication or contradiction.
3. **Error propagation (no silent failures)** — Every unrecognised construct, unknown macro, LLM error, or partial write must surface an explicit, actionable error. This crosses all 5 MCP servers and all 8 agents.
4. **BMAD format compliance** — Agent definitions, workflow files, step files, and config patterns must all conform to BMAD standards. This is a cross-cutting structural constraint on how every component is authored.
5. **LLM reliability gating** — Human review gates (analyst approval before spec layer writes) are a cross-cutting concern that must be architecturally enforced at every AI-output stage.
6. **COBOL dialect handling** — Unknown or unsupported constructs must be flagged at the `cobol-parser-mcp` layer and propagated correctly through the pipeline — not silently ignored.
7. **MCP server lifecycle** — All 5 MCP servers must start via IDE config and remain data-persistent across agent session restarts without requiring full reinitialisation.

## Starter Template Evaluation

### Primary Technology Domain

Local-first Python MCP server suite + BMAD markdown agent definitions.
No UI, no frontend framework, no cloud runtime.

### Technology Foundations

This project has no traditional "starter template" — there is no `create-mcp-app`. The foundation is the BMAD module structure (`_bmad/mm/`) plus Python MCP server packages.

The old architecture (docs/architecture.md) established technology choices that remain largely sound. Updated versions verified March 2026:

### MCP Server Framework: FastMCP 3.1.0

FastMCP is the official Python MCP SDK authoring layer (integrated into `mcp` package).
Powers ~70% of MCP servers across all languages. Python 3.12.

FastMCP 3.1.0 (released March 3, 2026) adds Code Mode for dynamic tool discovery
and MCP Apps support. These are optional capabilities — our servers use standard
tool definitions via STDIO transport.

### Package Management: Poetry

Poetry manages the monorepo — single root `pyproject.toml` + `poetry.lock`.
All five MCP servers live as Python packages under `mcp-servers/`.

**Monorepo setup (root-level, one-time):**

```bash
poetry init --python "^3.12"
poetry add fastmcp aiosqlite lark python-gitlab
poetry add --group dev pytest
```

### Per-Server Library Decisions

| MCP Server | Libraries | Version |
|---|---|---|
| `cobol-parser-mcp` | fastmcp, lark | FastMCP 3.1.0, Lark 0.12.0 |
| `jcl-parser-mcp` | fastmcp | FastMCP 3.1.0 (regex-based JCL parsing) |
| `specdb-mcp` | fastmcp, aiosqlite | FastMCP 3.1.0, aiosqlite 0.22.1 |
| `delta-macros-mcp` | fastmcp | FastMCP 3.1.0 |
| `gitlab-mcp` | fastmcp, python-gitlab | FastMCP 3.1.0, python-gitlab 8.1.0 |

All libraries work locally — no cloud dependencies, no external service calls (except GitLab API via gitlab-mcp when enabled).

### Configuration: Single Config File

All shared MCP server configuration lives in one file: `_bmad/mm/config.yaml`.
Settings include db_path, macro_library_path, glossary_path, source_paths,
gitlab_url, and any engagement-specific values.

A shared config loader module reads this file and provides typed access to all
settings. Each MCP server imports the shared loader — no server has its own
config module or reads settings independently.

The only exception is `GITLAB_TOKEN`, which remains an environment variable
by security design (never written to config files).

### Architectural Decisions Established

**Language & Runtime:** Python 3.12, Poetry for package management
**MCP Authoring:** FastMCP 3.1.0 (type-hint-driven tool definitions, lifecycle management)
**Database Access:** aiosqlite 0.22.1 (async, non-blocking SQLite for specdb-mcp)
**GitLab Client:** python-gitlab 8.1.0 (GitLab API v4, Cloud + self-hosted)
**COBOL Parsing:** Regex-based static pre-pass (deterministic) + Lark 0.12.0 for grammar-level parsing
**Project Structure:** Poetry monorepo — single root `pyproject.toml` + `poetry.lock`; all five MCP servers as Python packages under `mcp-servers/`
**Configuration:** Single `_bmad/mm/config.yaml` — all servers read from one file via shared loader
**Testing:** pytest (root-level tests/ directory)

**Note:** Project initialisation (poetry init for all 5 servers) should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- SQLite DB location: configurable via `db_path` in config.yaml
- MCP transport: STDIO (all 5 servers)
- MCP error response format: structured result dict (consistent across all servers)
- GitLab credential strategy: GITLAB_TOKEN environment variable
- IDE targets: Claude Code + GitHub Copilot (VS Code)

**Important Decisions (Shape Architecture):**
- Schema versioning: direct table structure modifications in specdb-mcp
- Idempotency pattern: INSERT OR IGNORE + UPDATE (check-then-upsert)
- Logging: stderr + log file dual handler

**Deferred Decisions (Post-MVP):**
- Installer mechanism (to be decided during implementation)
- Parallel Po processing (Phase 2)
- Multi-engagement DB isolation (Scale phase)

### Data Architecture

**SQLite DB Location:** Configurable via `db_path` in `_bmad/mm/config.yaml`.
Default: `<project-root>/data/specdb.sqlite`. All agents reference this path
from config, not hardcoded.

**Schema Versioning:** Direct table structure modifications managed by `specdb-mcp`.
On server startup: apply any pending schema changes programmatically.
No external migration framework — single-developer local tool does not warrant
Alembic overhead.

**Idempotency Pattern:** `INSERT OR IGNORE` + `UPDATE` (check-then-upsert)
across all spec layer writes.
- Safer than `INSERT OR REPLACE` for partial re-runs — only updates fields
  present in the new write.
- All `specdb-mcp` write tools implement this pattern consistently.
- Partial writes on error: wrap in SQLite transaction; rollback on failure
  rather than leaving inconsistent state.

### Authentication & Security

**GitLab Credentials:** `GITLAB_TOKEN` environment variable.
- `gitlab-mcp` reads from `os.environ["GITLAB_TOKEN"]` at startup; fails
  with explicit error if not set.
- No `.env` file dependency; no keychain library.
- All other MCP servers: no authentication required (local-only, STDIO transport).

### API & Communication Patterns (MCP Layer)

**MCP Transport:** STDIO (all 5 servers).
- IDE spawns each MCP server as a subprocess; communication via stdin/stdout.
- Supported by Claude Code and GitHub Copilot (VS Code) with identical config format.
- No network port, no firewall configuration required.
- FastMCP handles STDIO transport natively.

**Structured Error/Result Format:** Consistent schema across all 5 MCP servers:
```python
{
  "status": "ok" | "error" | "warning",
  "data": <tool-specific payload>,
  "flags": [{"code": str, "message": str, "location": str}],
  "message": str
}
```
- `warning`: recoverable issue (unknown macro, unrecognised construct) —
  agent flags and continues.
- `error`: non-recoverable failure (DB write error, parse failure) —
  agent halts and surfaces error.
- `flags`: structured list of all flagged items, enabling FR34
  (consolidated unresolved construct list).

**MCP Tool Limit:** GitHub Copilot caps at 128 tools across all servers.
Projected tool count: ~28 tools total (cobol-parser: 4, jcl-parser: 4,
specdb: 4, delta-macros: 4, gitlab: 12). Well within limit.

**GitHub Copilot Constraint:** Copilot supports MCP tools only (not resources
or prompts). No impact — all 5 servers expose tools only by design.

### Infrastructure & Deployment

**IDE Configuration Files:** Installer writes MCP server registration to:
- `.claude/mcp.json` — Claude Code
- `.vscode/mcp.json` — GitHub Copilot (VS Code)

Both files use identical format:
```json
{
  "servers": {
    "cobol-parser-mcp": {
      "command": "poetry",
      "args": ["run", "python", "-m", "cobol_parser_mcp.server"],
      "env": {}
    }
  }
}
```

**Installer Mechanism:** Deferred — to be designed during implementation planning.

**Logging:** Dual handler on all MCP servers.
- stderr: real-time visibility in IDE's MCP server output panel (required for
  STDIO servers — stdout is reserved for JSON-RPC).
- Log file: `<project-root>/logs/<server-name>.log` — persistent, reviewable
  after pipeline runs.
- Standard Python `logging` module with StreamHandler (stderr) + FileHandler
  (log file).

## Implementation Patterns & Consistency Rules

### Critical Conflict Points Identified

7 areas where AI agents could make different choices without explicit rules:
code style, SQLite naming, MCP tool naming, result dict construction,
timestamp format, module identity key, error handling scope.

### Naming Patterns

**Python Code (PEP 8 — mandatory):**
- Functions and variables: `snake_case` — `parse_module()`, `program_name`
- Classes: `PascalCase` — `CobolParser`, `SpecDbServer`
- Constants: `SCREAMING_SNAKE` — `DEFAULT_DB_PATH`, `SCHEMA_VERSION`
- Private helpers: prefix with `_` — `_build_call_graph()`

**MCP Tool Names (snake_case, verb-first):**
- Pattern: `<verb>_<noun>` — `parse_module`, `get_macro`, `write_spec`, `create_epic`
- Exactly as defined in the PRD tool lists — no variation permitted
- Tool docstrings become the MCP tool description: keep them concise and accurate

**SQLite Naming (snake_case throughout):**
- Tables: `snake_case` plural — `cobol_files`, `spec_business_rules`, `dependencies`
- Columns: `snake_case` — `program_name`, `created_at`, `source_paragraph`
- Foreign keys: `<table_singular>_id` — `cobol_file_id`, `spec_entity_id`
- No PascalCase or camelCase anywhere in the schema

**COBOL Identifiers in the DB:**
- Store COBOL program names in UPPERCASE as-is: `PAYROLL-CALC`, `ACCT-BATCH`
- Store COBOL field names in UPPERCASE as-is: `WS-CUST-BAL`
- Business term mappings (glossary/rosetta) use the human-readable casing from the glossary file
- The `program_name` column always contains the COBOL PROGRAM-ID value verbatim

**File Naming:**
- Python modules: `snake_case.py` — `server.py`, `cobol_parser.py`, `db_helpers.py`
- Config files: `snake_case.yaml` / `snake_case.json`
- Macro library files: SCREAMING-SNAKE matching the macro name — `DLTM-ACCT-LOCK.md`

### Structure Patterns

**MCP Server Internal Structure (all 5 servers):**
```
mcp-servers/<package_name>/          # e.g. cobol_parser_mcp (snake_case Python package)
├── __init__.py
├── server.py        # FastMCP app, tool definitions (thin wrappers only)
├── <domain>.py      # Core logic (e.g. cobol_parser.py, spec_db.py)
├── result.py        # make_result() / make_error() / make_warning() helpers
└── config.py        # Shared config loader — reads _bmad/mm/config.yaml

tests/<package_name>/                # Root-level tests, mirroring package structure
├── test_server.py
├── test_<domain>.py
└── fixtures/        # Sample COBOL files, mock DB, etc.
```

- `server.py` contains ONLY tool definitions — each tool is a thin wrapper calling into `<domain>.py`
- Business logic lives in domain modules, not in tool functions
- This separation means logic can be tested without running the MCP server

**Tests Location:** Root-level `tests/<package_name>/` directory (not co-located with source)

**Config Loading:** All servers share a single config loader that reads `_bmad/mm/config.yaml`. Never hardcode paths.

### Format Patterns

**MCP Tool Result Format (mandatory for all tools in all 5 servers):**
```python
# result.py — shared in every MCP server
def make_result(data=None, flags=None, message="", status="ok"):
    return {
        "status": status,       # "ok" | "warning" | "error"
        "data": data,           # tool-specific payload (dict, list, str, None)
        "flags": flags or [],   # list of {"code": str, "message": str, "location": str}
        "message": message      # human-readable summary
    }

def make_error(message, flags=None):
    return make_result(status="error", message=message, flags=flags)

def make_warning(data, message, flags):
    return make_result(status="warning", data=data, message=message, flags=flags)
```

**Flag Code Format:** `SCREAMING_SNAKE` with category prefix:
- `UNKNOWN_MACRO` — delta-macros-mcp
- `UNKNOWN_CONSTRUCT` — cobol-parser-mcp
- `PARSE_ERROR` — cobol-parser-mcp
- `DB_WRITE_CONFLICT` — specdb-mcp
- `GITLAB_API_ERROR` — gitlab-mcp

**Timestamp Format:** ISO 8601 UTC strings in all SQLite columns and tool outputs.
```python
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()  # "2026-03-01T14:30:00.123456+00:00"
```
Never Unix timestamps — the DB must be human-readable in any SQLite browser.

**Program Identity Key:** `program_name` is the canonical identifier for a COBOL module across all tables, all agents, and all MCP tool parameters. Value is the COBOL PROGRAM-ID verbatim (uppercase with hyphens): `"PAYROLL-CALC"`.

### Process Patterns

**Error Handling in MCP Tools:**
```python
@mcp.tool()
def parse_module(program_name: str, source_path: str) -> dict:
    """Parse a COBOL module and return structural analysis."""
    try:
        result = _do_parse(program_name, source_path)
        return make_result(data=result)
    except FileNotFoundError as e:
        return make_error(f"Source file not found: {source_path}", flags=[{
            "code": "FILE_NOT_FOUND", "message": str(e), "location": source_path
        }])
    except Exception as e:
        return make_error(f"Unexpected parse error: {e}")
```
- Every tool has its own try/except — no silent propagation to FastMCP's default error handler
- Catch specific exceptions first, broad `Exception` last
- Always return a result dict — never raise from a tool function

**SQLite Transaction Pattern (specdb-mcp):**
```python
async with db.execute("BEGIN"):
    try:
        # all writes for this tool call
        await db.execute("INSERT OR IGNORE INTO ...")
        await db.execute("UPDATE ... WHERE ...")
        await db.execute("COMMIT")
    except Exception as e:
        await db.execute("ROLLBACK")
        return make_error(f"DB write failed: {e}")
```
Transaction per tool call — never per individual statement.

**Idempotent Write Pattern:**
```python
# INSERT OR IGNORE creates the row if absent
await db.execute(
    "INSERT OR IGNORE INTO spec_business_rules (program_name, rule_id) VALUES (?, ?)",
    (program_name, rule_id)
)
# UPDATE sets all fields — runs whether INSERT created or skipped the row
await db.execute(
    "UPDATE spec_business_rules SET description=?, source_paragraph=?, updated_at=? "
    "WHERE program_name=? AND rule_id=?",
    (description, source_paragraph, now, program_name, rule_id)
)
```

**Logging Pattern:**
```python
import logging
logger = logging.getLogger(__name__)  # module-level logger

logger.info("parse_module called: program=%s", program_name)
logger.warning("Unknown macro encountered: macro=%s program=%s", macro_name, program_name)
logger.error("DB write failed: table=%s error=%s", table_name, str(e))
```
- `DEBUG`: detailed internal state (call graphs, regex matches)
- `INFO`: tool calls, stage completions
- `WARNING`: flagged items (unknown constructs, macros) — mirrors tool `flags` output
- `ERROR`: failures that return `status: "error"`

### Enforcement Guidelines

**All AI Agents MUST:**
- Use `make_result()` / `make_error()` / `make_warning()` from `result.py` — never construct the dict inline
- Use `program_name` (uppercase COBOL PROGRAM-ID) as the module identity key in all tool calls and DB writes
- Wrap every tool body in try/except — no exceptions may propagate to FastMCP's handler
- Use ISO 8601 UTC timestamps — never Unix integers
- Name all MCP tools exactly as defined in the PRD tool lists — no additions or renames without architecture update
- Keep `server.py` thin — logic goes in domain modules

**Anti-Patterns to Avoid:**
- `return {"error": "something went wrong"}` — use `make_error()`
- `program_name = "payroll_calc"` — must be `"PAYROLL-CALC"` (COBOL PROGRAM-ID verbatim)
- `created_at = int(time.time())` — use ISO 8601 string
- Business logic inside tool functions in `server.py`
- `INSERT OR REPLACE` — use the idempotent INSERT OR IGNORE + UPDATE pattern
- Bare `except:` or `except Exception: raise` inside a tool function

## Project Structure & Boundaries

### Complete Project Directory Structure

```
MM-Squad/                                      # Project root
├── README.md
├── pyproject.toml                             # Root Poetry monorepo — all deps managed here
├── poetry.lock
├── .gitignore                                 # Excludes data/, logs/, client COBOL source
│
├── _bmad/
│   ├── core/                                  # BMAD core (installed, not modified)
│   ├── bmm/                                   # BMAD BMM module (installed, not modified)
│   └── mm/                                    # MM Expansion Pack — OUR MODULE
│       ├── config.yaml                        # SINGLE config file for all MCP servers + module
│       ├── module-help.csv                    # Workflow/agent registry (required by installer)
│       ├── agents/
│       │   ├── po.md                          # NEW — Analysis agent (structure, deps, business rules)
│       │   ├── tigress.md                     # Architect — migration architecture
│       │   ├── crane.md                      # Dev (Java) — code generation from spec layer
│       │   ├── viper.md                       # Dev (COBOL) — COBOL modernisation
│       │   ├── monkey.md                      # Dev (Python) — code generation from spec layer
│       │   ├── shifu.md                       # PM + SM — delivery orchestrator
│       │   ├── oogway.md                      # Auditor — validate PRD, implementation readiness, code review, retrospective
│       │   └── tai-lung.md                    # QA — migration validation
│       ├── workflows/
│       │   ├── po/
│       │   │   ├── analyse-structure/
│       │   │   │   ├── workflow.md
│       │   │   │   └── steps/
│       │   │   │       ├── step-01-init.md
│       │   │   │       ├── step-02-load-source.md
│       │   │   │       ├── step-03-static-prepass.md
│       │   │   │       ├── step-04-semantic-clustering.md
│       │   │   │       ├── step-05-ai-analysis.md
│       │   │   │       ├── step-06-review-gate.md
│       │   │   │       └── step-07-write-to-spec.md
│       │   │   ├── map-dependencies/
│       │   │   │   ├── workflow.md
│       │   │   │   └── steps/
│       │   │   │       ├── step-01-init.md
│       │   │   │       ├── step-02-regex-extraction.md
│       │   │   │       ├── step-03-build-graph.md
│       │   │   │       ├── step-04-ai-analysis.md
│       │   │   │       ├── step-05-subsystem-detection.md
│       │   │   │       └── step-06-migration-order.md
│       │   │   ├── extract-business-rules/
│       │   │   │   ├── workflow.md
│       │   │   │   └── steps/
│       │   │   │       ├── step-01-init.md
│       │   │   │       ├── step-02-consume-analysis.md
│       │   │   │       ├── step-03-extract-rules.md
│       │   │   │       ├── step-04-business-markdown.md
│       │   │   │       ├── step-05-review-gate.md
│       │   │   │       └── step-06-populate-spec-layer.md
│       │   │   └── view-flags/
│       │   │       └── workflow.md
│       │   ├── dev/
│       │   │   ├── dev-story/
│       │   │   │   ├── workflow.md
│       │   │   │   └── steps/...
│       │   │   └── code-review/
│       │   │       ├── workflow.md
│       │   │       └── steps/...
│       │   ├── architect/
│       │   │   ├── create-architecture/
│       │   │   │   ├── workflow.md
│       │   │   │   └── steps/...
│       │   │   └── check-implementation-readiness/
│       │   │       ├── workflow.md
│       │   │       └── steps/...
│       │   ├── pm/
│       │   │   ├── create-epics-and-stories/...
│       │   │   ├── sprint-planning/...
│       │   │   ├── create-story/...
│       │   │   ├── sprint-status/...
│       │   │   ├── correct-course/...
│       │   │   └── retrospective/...
│       │   └── qa/
│       │       └── qa-generate-e2e-tests/...
│       ├── data/
│       │   ├── glossary-template.md           # Empty glossary for new engagements
│       │   └── macro-template.md              # Empty Delta macro doc template
│       └── teams/
│           └── default-party.csv              # MM agent party mode roster
│
├── mcp-servers/                               # Python packages — NOT inside _bmad/
│   │
│   ├── cobol_parser_mcp/                      # FR1-8, FR35-39 | NFR1, NFR2
│   │   ├── __init__.py
│   │   ├── server.py                          # FastMCP app + tool definitions (thin wrappers)
│   │   ├── cobol_parser.py                    # IDENTIFICATION/DATA/PROCEDURE division parsing
│   │   ├── call_graph.py                      # Paragraph PERFORM graph builder
│   │   ├── cluster_builder.py                 # Semantic paragraph clustering
│   │   ├── complexity_scorer.py               # Low/Medium/High scoring logic
│   │   ├── antipattern_detector.py            # GOTO, ALTER, nested PERFORM detection
│   │   ├── dialect_handler.py                 # CICS, DB2 SQL, COPY statement handling
│   │   └── result.py                          # make_result(), make_error(), make_warning()
│   │
│   ├── specdb_mcp/                            # FR17-18, FR29, FR33 | NFR3, NFR10, NFR12, NFR17
│   │   ├── __init__.py
│   │   ├── server.py                          # FastMCP app + tool definitions (thin wrappers)
│   │   ├── spec_db.py                         # All read/write operations — core domain logic
│   │   ├── schema.py                          # CREATE TABLE statements + schema modifications
│   │   └── result.py                          # make_result(), make_error(), make_warning()
│   │
│   ├── delta_macros_mcp/                      # FR8, FR31, FR34, FR39 | NFR4, NFR9
│   │   ├── __init__.py
│   │   ├── server.py                          # FastMCP app + tool definitions (thin wrappers)
│   │   ├── macro_library.py                   # Markdown file parsing + search logic
│   │   └── result.py                          # make_result(), make_error(), make_warning()
│   │
│   ├── jcl_parser_mcp/                        # JCL parsing | NFR1, NFR2
│   │   ├── __init__.py
│   │   ├── server.py                          # FastMCP app + tool definitions (thin wrappers)
│   │   ├── jcl_parser.py                      # JOB/STEP/DD statement parsing
│   │   ├── job_graph.py                       # Cross-job execution graph builder
│   │   └── result.py                          # make_result(), make_error(), make_warning()
│   │
│   ├── gitlab_mcp/                            # FR40-56 | NFR5, NFR8, NFR16
│   │   ├── __init__.py
│   │   ├── server.py                          # FastMCP app + tool definitions (thin wrappers)
│   │   ├── gitlab_client.py                   # python-gitlab wrapper — all API calls
│   │   ├── label_manager.py                   # Label taxonomy creation and management
│   │   ├── readme_updater.py                  # README dashboard generation
│   │   └── result.py                          # make_result(), make_error(), make_warning()
│   │
│   └── shared/                                # Shared utilities across all servers
│       ├── __init__.py
│       └── config_loader.py                   # Reads _bmad/mm/config.yaml — single config loader
│
├── tests/                                     # Root-level tests, mirroring mcp-servers/ structure
│   ├── __init__.py
│   ├── cobol_parser_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_cobol_parser.py
│   │   ├── test_call_graph.py
│   │   ├── test_cluster_builder.py
│   │   ├── test_complexity_scorer.py
│   │   ├── test_antipattern_detector.py
│   │   └── fixtures/
│   │       └── blackjack/                     # git submodule — real IBM Enterprise COBOL corpus
│   │           ├── src/                       # .cob source files
│   │           └── copy/                      # .cpy copybooks
│   ├── specdb_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_spec_db.py
│   │   ├── test_schema.py
│   │   └── fixtures/
│   │       └── seed_data.py                   # Test data for spec layer tables
│   ├── delta_macros_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_macro_library.py
│   │   └── fixtures/
│   │       └── macros/
│   │           └── DLTM-EXAMPLE.md
│   ├── jcl_parser_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_jcl_parser.py
│   │   └── fixtures/
│   │       └── sample_jcl/
│   └── gitlab_mcp/
│       ├── __init__.py
│       ├── test_server.py
│       ├── test_gitlab_client.py
│       ├── test_label_manager.py
│       ├── test_readme_updater.py
│       └── fixtures/
│           └── mock_gitlab.py
│
├── templates/
│   ├── glossary-template.md                   # Empty glossary for new client engagements
│   └── macro-template.md                      # Empty Delta macro doc template
│
├── blackjack/                                 # BlackJack demo engagement (not client data)
│   ├── glossary.md                            # BlackJack field-name to business-term mappings
│   └── macros/                                # BlackJack Delta macro docs (if any)
│
├── data/                                      # Runtime — SQLite DB lives here (gitignored)
│   └── .gitkeep
│
├── logs/                                      # Runtime — MCP server logs (gitignored)
│   └── .gitkeep
│
├── documents/                                 # BMAD planning & implementation artifacts
│   ├── planning-artifacts/
│   └── implementation-artifacts/
│
└── docs/                                      # Project knowledge
    ├── project_idea.md
    └── architecture.md                        # Old architecture (reference)
```

### Architectural Boundaries

**MCP Tool Boundaries (what each server owns):**

| Server | Owns | Does NOT own |
|---|---|---|
| `cobol-parser-mcp` | COBOL parsing, call graph, complexity, anti-patterns, dialect detection | Spec layer writes, business logic extraction |
| `jcl-parser-mcp` | JCL parsing, job step extraction, dataset allocation parsing, job graphs | COBOL source parsing, spec layer writes |
| `specdb-mcp` | All SQLite reads/writes, schema management | Parsing logic, GitLab calls |
| `delta-macros-mcp` | Macro library reads, macro search, macro ingest | Anything about COBOL source files |
| `gitlab-mcp` | All GitLab API calls, label management, README updates | Any local data reads or DB operations |

**The spec layer is the only shared state between agents.**
Agents do not communicate with each other directly — Po reads its own earlier
analysis outputs via specdb-mcp. The DB is the message bus between analysis
and downstream agents.

**All agents have GitLab access.**
Every agent can post progress, comments, and status updates to GitLab via
`gitlab-mcp`. Shifu orchestrates the overall GitLab project structure as PM + SM.

### Requirements to Structure Mapping

| FR Group | Component | Key Files |
|---|---|---|
| FR1-8 (Po/COBOL Analysis) | `cobol-parser-mcp` | `cobol_parser.py`, `call_graph.py`, `cluster_builder.py`, `complexity_scorer.py`, `antipattern_detector.py` |
| FR9-13 (Po/Dependencies) | `cobol-parser-mcp` + `jcl-parser-mcp` + `specdb-mcp` | Static CALL/COPY deps + JCL runtime deps + spec writes |
| FR14-18 (Po/Spec Layer) | `specdb-mcp` | `spec_db.py`, `schema.py` (all spec_* tables) |
| FR19-22 (Tigress/Architecture) | `_bmad/mm/agents/tigress.md` | Agent consumes spec layer via specdb-mcp |
| FR23-25 (Code Generation) | `_bmad/mm/agents/crane.md`, `viper.md`, `monkey.md` | Language-specific Dev agents |
| FR26-28 (QA Validation) | `_bmad/mm/agents/tai-lung.md` | Validates code against spec_rules; Epic sign-off |
| FR29 (Schema init) | `specdb-mcp` | `schema.py` `init_schema` tool |
| FR30 (Glossary config) | `_bmad/mm/config.yaml` + agent workflows | Glossary path in config |
| FR31 (Add macro) | `delta-macros-mcp` | `macro_library.py` `add_macro` tool |
| FR32 (BMAD installer) | BMAD core installer | Deferred |
| FR34 (Consolidated flags) | All MCP servers | `flags` array in result dict; Po agent aggregates |
| FR35-39 (COBOL dialects) | `cobol-parser-mcp` | `dialect_handler.py` |
| FR40-56 (GitLab PM) | `gitlab-mcp` + `_bmad/mm/agents/shifu.md` | `gitlab_client.py`, `label_manager.py`, `readme_updater.py` |

### Integration Points

**Internal Data Flow:**
```
COBOL source files
    -> cobol-parser-mcp (parse_module, extract_call_graph, score_complexity, detect_antipatterns)
    -> specdb-mcp (write_spec: cobol_files, analyses, dependencies, metrics tables)
    -> delta-macros-mcp (get_macro — called during parse for unknown macros)
    -> specdb-mcp (write_spec: spec_* tables — written by Po workflows)
    -> tigress.md (consumes spec layer for migration architecture)
    -> crane.md / viper.md / monkey.md (code generation from spec + architecture)
    -> oogway.md (code review — validates implementation against spec + architecture)
    -> tai-lung.md (QA — validates generated code against spec layer business rules)
    -> gitlab-mcp (create_epic, create_issue, apply_label, update_readme — all agents)
```

**External Integrations:**
- GitLab Cloud or self-hosted (API v4, HTTPS) — via `gitlab-mcp` only
- LLM provider (Claude API) — called by IDE for agent AI analysis; no MCP server involvement

**Config Flow:**
```
_bmad/mm/config.yaml (single source of truth)
    -> db_path        -> specdb-mcp       -> aiosqlite connection
    -> macro_lib_path -> delta-macros-mcp -> macro file reads
    -> gitlab_url     -> gitlab-mcp       -> python-gitlab client
    -> glossary_path  -> Po workflows     -> glossary loading
    -> source_paths   -> Po workflows     -> COBOL source discovery
    GITLAB_TOKEN (env var) -> gitlab-mcp  -> python-gitlab auth
```

### Development Workflow

**Running a single MCP server for development (from project root):**
```bash
poetry run python -m cobol_parser_mcp.server
poetry run python -m specdb_mcp.server
poetry run python -m delta_macros_mcp.server
poetry run python -m jcl_parser_mcp.server
poetry run python -m gitlab_mcp.server
```

**Running tests (from project root):**
```bash
poetry run pytest tests/                          # all servers
poetry run pytest tests/cobol_parser_mcp/         # single server
```

**BlackJack regression run:** Load BlackJack corpus files from
`tests/cobol_parser_mcp/fixtures/blackjack/src/` and `copy/` and run the full
pipeline against them. All modules must produce valid spec layer output.

## Architecture Validation Results

### Coherence Validation

**Decision Compatibility:** All technology choices are compatible.
One bridging pattern required: `gitlab-mcp` must use `asyncio.to_thread()` to wrap
synchronous python-gitlab calls within async FastMCP tool functions.

**Pattern Consistency:** All naming, structure, format, and process patterns are
internally consistent and aligned with the chosen technology stack.

**Structure Alignment:** Project structure supports all architectural decisions.
The `mcp-servers/shared/config_loader.py` module ensures the single-config-file
decision is structurally enforced.

### Requirements Coverage Validation

**Functional Requirements:** 55 of 56 FRs fully covered.
FR32 (BMAD installer) deferred by design — module structure defined,
installer mechanism intentionally deferred.

**Non-Functional Requirements:** All 21 NFRs covered.
NFR13 clarification: "MCP servers persist across restarts" means SQLite data persists
(local file), not the server process. STDIO servers are spawned per
IDE session by design; data integrity is the persistence guarantee.

### Implementation Readiness Validation

- All critical decisions documented with verified versions
- Implementation patterns comprehensive with code examples and anti-patterns
- Project structure complete with file-level specificity
- All 56 FRs mapped to specific components and files
- Integration points and data flow explicitly defined

### Gap Analysis Results

**Critical (addressed in this document):**
- `gitlab-mcp` async/sync bridge: `asyncio.to_thread()` pattern needed for
  python-gitlab calls within async FastMCP tools

**Important (to address at implementation start):**
- Glossary file format: markdown table (`| COBOL Name | Business Term |`) —
  simple, human-editable, parseable by agents
- config.yaml complete schema: `db_path`, `macro_library_path`, `gitlab_url`,
  `glossary_path`, `source_paths`, `project_name`, `target_language` (TBD by Tigress)
- All 8 MM agents are net-new — require full authoring from scratch
  following BMAD module conventions

**Deferred (post-MVP):**
- Shared `result.py` as published package (currently copied per server — acceptable for MVP)
- Pre-commit hooks for PEP 8 enforcement

### Architecture Completeness Checklist

**Requirements Analysis**
- [x] 56 FRs and 21 NFRs analyzed for architectural implications
- [x] Scale assessed: High complexity, 8 agents, 5 MCP servers
- [x] Hard constraints identified: data locality, BMAD compliance, STDIO transport
- [x] 7 cross-cutting concerns mapped

**Architectural Decisions**
- [x] MCP framework: FastMCP 3.1.0 (Python 3.12, Poetry monorepo)
- [x] Database: SQLite via aiosqlite 0.22.1, configurable path
- [x] Transport: STDIO (Claude Code + GitHub Copilot)
- [x] GitLab: python-gitlab 8.1.0, GITLAB_TOKEN env var
- [x] COBOL parsing: regex + Lark 0.12.0 (custom implementation)
- [x] Schema versioning: direct table modifications, programmatic
- [x] Idempotency: INSERT OR IGNORE + UPDATE
- [x] Error format: structured result dict across all servers
- [x] Logging: dual handler (stderr + log file)
- [x] Configuration: single _bmad/mm/config.yaml

**Implementation Patterns**
- [x] Python naming: PEP 8 (snake_case, PascalCase, SCREAMING_SNAKE)
- [x] MCP tool names: verb-first snake_case, exactly per PRD tool lists
- [x] SQLite naming: snake_case, COBOL identifiers verbatim uppercase
- [x] Server structure: thin server.py + domain modules + result.py
- [x] Error handling: per-tool try/except, make_result() helpers
- [x] Transaction pattern: per-tool-call in specdb-mcp
- [x] Timestamps: ISO 8601 UTC strings
- [x] Program identity key: program_name = COBOL PROGRAM-ID verbatim

**Project Structure**
- [x] Complete directory tree with file-level specificity
- [x] All 5 MCP server structures defined
- [x] BMAD agent definitions mapped
- [x] Workflow/step file structure defined
- [x] BlackJack corpus location specified
- [x] Runtime directories (data/, logs/) defined
- [x] IDE config files (.claude/mcp.json, .vscode/mcp.json) defined

### Architecture Readiness Assessment

**Overall Status: READY FOR IMPLEMENTATION**

**Confidence Level: High**

**Key Strengths:**
- SQLite spec layer as the message bus between agents eliminates direct agent coupling
- Structured result dict with flags array directly implements "no silent failures" (NFR11)
- Poetry monorepo with single lock file ensures reproducible installs across all 5 servers
- STDIO transport confirmed compatible with both target IDEs
- Single config file prevents configuration drift across servers
- BlackJack corpus provides immediate regression baseline (NFR21)

**Areas for Future Enhancement:**
- Shared `result.py` as a published package (avoids copy-per-server)
- Parallel Po processing for large estates (Phase 2)
- Formal installer mechanism (currently deferred)

### Implementation Handoff

**Implementation order (from PRD Build Strategy):**
```
Phase 1 — Foundation:
  1. Initial setup       # MM module scaffolding, config.yaml, module-help.csv, Poetry init
  2. gitlab-mcp          # GitLab MCP server
  3. Shifu               # PM + SM agent
  Validation: MM module installs correctly via BMAD installer

Phase 2 — Remaining Agents:
  4. Tigress             # Architect
  5. Crane               # Dev (Java)
  6. Viper               # Dev (COBOL)
  7. Monkey              # Dev (Python)
  8. Oogway              # Auditor (validate PRD, implementation readiness, code review, retrospective)
  9. Tai Lung            # QA

Phase 3 — Analysis Agent + MCP Servers:
  10. specdb-mcp         # SQLite spec layer CRUD
  11. delta-macros-mcp   # Middleware knowledge base
  12. cobol-parser-mcp   # COBOL static parsing engine
  13. jcl-parser-mcp     # JCL parsing
  14. Po                 # Analysis agent — the big build
  15. End-to-end demo    # COBOL BlackJack modernisation
```

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented
- Use `make_result()` / `make_error()` / `make_warning()` — never construct result dicts inline
- Use `asyncio.to_thread()` for all synchronous library calls within async FastMCP tools
- `program_name` = COBOL PROGRAM-ID verbatim (uppercase with hyphens) — everywhere
- Refer to this document before any implementation decision not covered in the story
