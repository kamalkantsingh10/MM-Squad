# Story 1.3: Shared MCP Server Infrastructure

Status: review

## Story

As a developer,
I want shared config loading and result formatting infrastructure available to all MCP servers,
So that every server reads configuration consistently and returns structured results in the same format.

## Acceptance Criteria

1. **Config loader** — `mcp-servers/shared/config_loader.py` reads `_bmad/mm/config.yaml`, provides typed access to all settings (`db_path`, `macro_library_path`, `glossary_path`, `source_paths`, `gitlab_url`, `project_name`), caches config for server lifetime.
2. **Result helpers** — `result.py` exists in each of the 5 MCP server packages with `make_result(data, flags, message, status)`, `make_error(message, flags)`, `make_warning(data, message, flags)`. `flags` is always a list of dicts with keys `code`, `message`, `location`.
3. **Dual logging** — Every MCP server logs to stderr (StreamHandler) and `<project-root>/logs/<server-name>.log` (FileHandler). Log levels: DEBUG (internal state), INFO (tool calls), WARNING (flagged items), ERROR (failures).
4. **Skeleton servers** — All 5 server packages contain `server.py` with FastMCP app init, import from shared config loader, and can be started via `poetry run python -m <package_name>.server` with no tools registered.

## Tasks / Subtasks

- [x] Task 1: Create shared config loader (AC: 1)
  - [x] Create `mcp-servers/shared/config_loader.py`
  - [x] Implement `load_config()` that reads `_bmad/mm/config.yaml`
  - [x] Parse YAML and return typed config object/dict
  - [x] Cache config on first load (module-level singleton)
  - [x] Resolve `<project-root>` placeholder in paths to actual project root
  - [x] Add type hints for all config fields
- [x] Task 2: Create result.py template and copy to all servers (AC: 2)
  - [x] Create canonical `result.py` with `make_result()`, `make_error()`, `make_warning()`
  - [x] Copy to all 5 packages: `cobol_parser_mcp/`, `specdb_mcp/`, `delta_macros_mcp/`, `jcl_parser_mcp/`, `gitlab_mcp/`
  - [x] Ensure `flags` defaults to empty list, never None
- [x] Task 3: Create logging setup utility (AC: 3)
  - [x] Create logging setup function (in shared or per-server)
  - [x] Configure dual handlers: StreamHandler(stderr) + FileHandler(logs/<name>.log)
  - [x] Set log format with timestamp, level, module, message
  - [x] Ensure log directory exists before creating FileHandler
- [x] Task 4: Create skeleton server.py for each MCP server (AC: 4)
  - [x] `mcp-servers/cobol_parser_mcp/server.py` — FastMCP("cobol-parser-mcp")
  - [x] `mcp-servers/specdb_mcp/server.py` — FastMCP("specdb-mcp")
  - [x] `mcp-servers/delta_macros_mcp/server.py` — FastMCP("delta-macros-mcp")
  - [x] `mcp-servers/jcl_parser_mcp/server.py` — FastMCP("jcl-parser-mcp")
  - [x] `mcp-servers/gitlab_mcp/server.py` — FastMCP("gitlab-mcp")
  - [x] Each imports shared config_loader and sets up logging
  - [x] Each can start via `poetry run python -m <package>.server`
- [x] Task 5: Verify all servers start (AC: 4)
  - [x] `poetry run python -m cobol_parser_mcp.server` starts without error
  - [x] `poetry run python -m specdb_mcp.server` starts without error
  - [x] `poetry run python -m delta_macros_mcp.server` starts without error
  - [x] `poetry run python -m jcl_parser_mcp.server` starts without error
  - [x] `poetry run python -m gitlab_mcp.server` starts without error (gitlab-mcp should NOT fail on missing GITLAB_TOKEN at startup — only when tools are called)

## Dev Notes

- **FastMCP import**: `from mcp.server.fastmcp import FastMCP` — the `fastmcp` package is now integrated into the `mcp` package as of 3.x.
- **STDIO transport**: `mcp.run(transport="stdio")` — stdout is reserved for JSON-RPC protocol. ALL logging MUST go to stderr or file, never stdout.
- **result.py copied per server**: For MVP, each server has its own copy. Shared package is deferred post-MVP.
- **Config path resolution**: The config loader needs to find `_bmad/mm/config.yaml` relative to the project root. Use `Path(__file__).resolve()` to navigate from shared/ up to project root.
- **gitlab-mcp startup**: Should NOT crash if GITLAB_TOKEN is missing at import time. Token check should happen when tools are called, not at server startup. This allows the server to register with the IDE even if GitLab isn't configured.
- **Python path setup**: For `poetry run python -m <package>.server` to work, `mcp-servers/` needs to be in the Python path. Configure this in `pyproject.toml` via `packages` or `tool.poetry.packages` setting.

### Project Structure Notes

- `mcp-servers/shared/config_loader.py` — shared across all servers
- `mcp-servers/<package>/result.py` — copied per server (identical content)
- `mcp-servers/<package>/server.py` — skeleton FastMCP app per server
- Config reads from `_bmad/mm/config.yaml` (created in Story 1.2)
- Logs write to `logs/<server-name>.log` (directory created in Story 1.1)

### References

- [Source: documents/planning-artifacts/architecture.md#Format Patterns] — result.py implementation with make_result/make_error/make_warning
- [Source: documents/planning-artifacts/architecture.md#Structure Patterns] — MCP server internal structure
- [Source: documents/planning-artifacts/architecture.md#Process Patterns] — Error handling and logging patterns
- [Source: documents/planning-artifacts/architecture.md#Configuration: Single Config File] — Config loader design
- [Source: documents/planning-artifacts/architecture.md#Infrastructure & Deployment] — Logging dual handler, STDIO transport
- [Source: documents/planning-artifacts/architecture.md#Enforcement Guidelines] — Anti-patterns to avoid
- [Source: documents/planning-artifacts/epics.md#Story 1.3] — Full acceptance criteria

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

None — clean implementation.

### Completion Notes List

- config_loader.py: load_config() reads _bmad/mm/config.yaml, resolves <project-root> to absolute paths, caches as module-level singleton
- setup_logging() in config_loader: dual handler (StreamHandler->stderr + FileHandler->logs/<name>.log), DEBUG level, timestamped format
- result.py: make_result(data, flags, message, status), make_error(message, flags), make_warning(data, message, flags) — flags always defaults to []
- Identical result.py copied to all 5 server packages per architecture (shared package deferred post-MVP)
- 5 skeleton server.py files: FastMCP init, config loader import, logging setup, STDIO transport
- 5 __main__.py files for `python -m <package>.server` support
- All 5 servers import and initialise without error (verified via direct import test)
- FastMCP imports from `fastmcp` package directly (3.1.0)
- gitlab-mcp does NOT check GITLAB_TOKEN at startup — only when tools are called
- 24 new tests covering all 4 ACs, 67 total — zero regressions

### File List

- mcp-servers/shared/config_loader.py (new)
- mcp-servers/cobol_parser_mcp/result.py (new)
- mcp-servers/cobol_parser_mcp/server.py (new)
- mcp-servers/cobol_parser_mcp/__main__.py (new)
- mcp-servers/specdb_mcp/result.py (new)
- mcp-servers/specdb_mcp/server.py (new)
- mcp-servers/specdb_mcp/__main__.py (new)
- mcp-servers/delta_macros_mcp/result.py (new)
- mcp-servers/delta_macros_mcp/server.py (new)
- mcp-servers/delta_macros_mcp/__main__.py (new)
- mcp-servers/jcl_parser_mcp/result.py (new)
- mcp-servers/jcl_parser_mcp/server.py (new)
- mcp-servers/jcl_parser_mcp/__main__.py (new)
- mcp-servers/gitlab_mcp/result.py (new)
- mcp-servers/gitlab_mcp/server.py (new)
- mcp-servers/gitlab_mcp/__main__.py (new)
- tests/test_shared_infrastructure.py (new)
