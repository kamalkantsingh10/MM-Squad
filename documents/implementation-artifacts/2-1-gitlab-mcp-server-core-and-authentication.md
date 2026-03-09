# Story 2.1: gitlab-mcp Server Core & Authentication

Status: review

## Story

As a developer,
I want a working gitlab-mcp MCP server that authenticates with GitLab and provides the foundation for all GitLab tools,
So that all downstream tools have a reliable, tested connection to the GitLab API.

## Acceptance Criteria

1. **AC1: Successful Authentication with Environment Variable**
   - Given `GITLAB_TOKEN` is set as an environment variable
   - When gitlab-mcp starts via `poetry run python -m gitlab_mcp.server`
   - Then it connects to the GitLab instance specified in `_bmad/mm/config.yaml` (`gitlab_url`)
   - And the python-gitlab client is initialised and authenticated
   - And the server registers with FastMCP via STDIO transport

2. **AC2: Missing GITLAB_TOKEN Error Handling**
   - Given `GITLAB_TOKEN` is NOT set
   - When gitlab-mcp starts
   - Then it starts successfully (server registers with IDE)
   - But when any tool function is called, it fails with explicit error: `make_error("GITLAB_TOKEN environment variable not set", flags=[{"code": "GITLAB_AUTH_ERROR", ...}])`
   - And the error is logged to stderr and the log file at ERROR level

3. **AC3: Async Event Loop Non-Blocking Calls**
   - Given gitlab-mcp is running
   - When any tool function calls the GitLab API
   - Then the synchronous python-gitlab call is wrapped in `asyncio.to_thread()` to avoid blocking the async event loop

4. **AC4: GitLab API Error Handling**
   - Given gitlab-mcp is running
   - When any tool encounters a GitLab API error
   - Then it returns `make_error()` with a `GITLAB_API_ERROR` flag code, the HTTP status, and an actionable message
   - And the error is logged at ERROR level

5. **AC5: Successful Tool Execution**
   - Given gitlab-mcp is running
   - When any tool completes successfully
   - Then it returns `make_result()` with `status: "ok"` and the relevant data payload

6. **AC6: Package Architecture & Code Structure**
   - Given the gitlab-mcp package structure
   - When a developer inspects the code
   - Then `server.py` contains only thin wrapper tool definitions
   - And `gitlab_client.py` contains all python-gitlab API call logic
   - And `result.py` contains make_result/make_error/make_warning helpers (already exists)
   - And NFR5 (< 10s per API call), NFR8 (env var auth), NFR15 (MCP protocol), NFR16 (Cloud + self-hosted) are satisfied

## Tasks / Subtasks

- [x] Task 1: Create `gitlab_client.py` — GitLab API client wrapper (AC: #1, #2, #3, #4, #5)
  - [x] 1.1: Create `mcp-servers/gitlab_mcp/gitlab_client.py` with `GitlabClient` class
  - [x] 1.2: Implement lazy authentication — read `GITLAB_TOKEN` from `os.environ` and `gitlab_url` from config at first API call, NOT at import/startup time (per Story 1.3 learning)
  - [x] 1.3: Use `gitlab.Gitlab(url=gitlab_url, private_token=token)` then `gl.auth()` for connection verification
  - [x] 1.4: Implement `_ensure_authenticated()` private method that initializes client on first call and raises on missing token
  - [x] 1.5: Wrap all synchronous python-gitlab calls in `asyncio.to_thread()` via async helper methods
  - [x] 1.6: Implement structured error handling — catch `gitlab.exceptions.GitlabAuthenticationError`, `gitlab.exceptions.GitlabError`, and generic exceptions, returning `make_error()` with `GITLAB_API_ERROR` or `GITLAB_AUTH_ERROR` flag codes
  - [x] 1.7: Add INFO logging for client initialization and ERROR logging for failures

- [x] Task 2: Create initial tool — `ping_gitlab` health check tool (AC: #1, #4, #5)
  - [x] 2.1: Add `ping_gitlab` tool to `server.py` as thin wrapper calling `gitlab_client`
  - [x] 2.2: Tool calls `gl.version()` (wrapped in `asyncio.to_thread()`) to verify connectivity
  - [x] 2.3: Returns `make_result(data={"gitlab_version": version, "gitlab_url": url})` on success
  - [x] 2.4: Returns `make_error()` with `GITLAB_API_ERROR` on failure
  - [x] 2.5: Add per-tool try/except — no exceptions propagate to FastMCP's handler

- [x] Task 3: Update `server.py` to import and wire client (AC: #6)
  - [x] 3.1: Import `GitlabClient` and instantiate as module-level singleton
  - [x] 3.2: Keep `server.py` thin — only tool registration and wrappers
  - [x] 3.3: Verify `__main__.py` still works for `poetry run python -m gitlab_mcp.server`

- [x] Task 4: Write comprehensive tests (AC: #1, #2, #3, #4, #5, #6)
  - [x] 4.1: Create `tests/gitlab_mcp/test_gitlab_client.py` — unit tests for GitlabClient
  - [x] 4.2: Create `tests/gitlab_mcp/fixtures/mock_gitlab.py` — mock GitLab API responses using `unittest.mock`
  - [x] 4.3: Test successful authentication flow (mock `gitlab.Gitlab` + `gl.auth()`)
  - [x] 4.4: Test missing GITLAB_TOKEN returns proper `make_error()` with `GITLAB_AUTH_ERROR`
  - [x] 4.5: Test GitLab API errors return `make_error()` with `GITLAB_API_ERROR` and HTTP status
  - [x] 4.6: Test `asyncio.to_thread()` wrapping — verify sync calls don't block event loop
  - [x] 4.7: Test lazy initialization — client not created until first tool call
  - [x] 4.8: Create `tests/gitlab_mcp/test_server.py` — test ping_gitlab tool returns correct result format
  - [x] 4.9: Run full test suite (`poetry run pytest tests/`) — all 80+ existing tests plus new tests must pass

- [x] Task 5: Verify end-to-end server startup (AC: #1, #6)
  - [x] 5.1: Verify `poetry run python -m gitlab_mcp.server` starts without error (no GITLAB_TOKEN needed at startup)
  - [x] 5.2: Verify server registers with FastMCP and is ready for STDIO communication
  - [x] 5.3: Verify logging outputs to both stderr and `logs/gitlab-mcp.log`

- [ ] Task 6: Create MCP server setup README (AC: #1)
  - [ ] 6.1: Create `mcp-servers/gitlab_mcp/README.md` with setup instructions: prerequisites, environment variables (`GITLAB_TOKEN`), `.mcp.json` configuration, how to verify connectivity via `ping_gitlab`

## Dev Notes

### Architecture Constraints — MUST FOLLOW

- **server.py is thin**: ONLY FastMCP tool registration + thin wrappers. ALL logic in `gitlab_client.py`
- **result.py already exists**: Use existing `make_result()`, `make_error()`, `make_warning()` — do NOT reconstruct dicts inline
- **No startup crash on missing token**: Server must start even without `GITLAB_TOKEN` (per Story 1.3 learning). Check token at tool-call time, not import time
- **asyncio.to_thread()**: ALL synchronous python-gitlab calls MUST be wrapped. FastMCP is async; python-gitlab is sync
- **Per-tool try/except**: Every tool function must catch exceptions. No exceptions propagate to FastMCP's default handler
- **Flag codes**: Use `SCREAMING_SNAKE` with category prefix: `GITLAB_API_ERROR`, `GITLAB_AUTH_ERROR`
- **Logging**: Use existing `setup_logging("gitlab-mcp")` from shared config_loader. Levels: INFO for tool calls, ERROR for failures
- **Config**: Read `gitlab_url` from `_bmad/mm/config.yaml` via existing `shared/config_loader.py`. NEVER hardcode URLs
- **Naming**: MCP tool names = `<verb>_<noun>` in snake_case, verb-first. Exactly as PRD defines
- **Timestamps**: ISO 8601 UTC strings everywhere, never Unix integers

### python-gitlab 8.1.0 — Key API Reference

```python
import gitlab

# Authentication with private token
gl = gitlab.Gitlab(url='https://gitlab.example.com', private_token='your-token')
gl.auth()  # Verifies token and populates gl.user

# Version check (useful for ping/health)
version = gl.version()  # Returns tuple: ('17.x.x', 'revision')

# Exception hierarchy
# gitlab.exceptions.GitlabAuthenticationError — 401 Unauthorized
# gitlab.exceptions.GitlabGetError — GET failures
# gitlab.exceptions.GitlabCreateError — POST failures
# gitlab.exceptions.GitlabError — Base exception for all API errors
```

### FastMCP 3.1.0 — Key Patterns

```python
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("gitlab-mcp")

@mcp.tool()
async def ping_gitlab() -> dict:
    """Check GitLab connectivity and return version info."""
    try:
        result = await asyncio.to_thread(client.ping)
        return make_result(data=result)
    except Exception as e:
        return make_error(str(e))

# STDIO transport (default)
mcp.run(transport="stdio")
```

**Known Issue**: FastMCP 2.13+ had a busy-loop issue with fakeredis/pydocket worker on STDIO transport (100% CPU idle). Verify 3.1.0 resolves this. If not, may need workaround.

### Existing Code State (from Epic 1)

| File | State | Notes |
|------|-------|-------|
| `mcp-servers/gitlab_mcp/__init__.py` | Exists | Empty package init |
| `mcp-servers/gitlab_mcp/__main__.py` | Exists | Entry point for `python -m` |
| `mcp-servers/gitlab_mcp/server.py` | Exists | Skeleton with FastMCP init, config load, logging setup |
| `mcp-servers/gitlab_mcp/result.py` | Exists | Complete `make_result/make_error/make_warning` helpers |
| `mcp-servers/shared/config_loader.py` | Exists | Complete config loader + logging setup |
| `tests/gitlab_mcp/__init__.py` | Exists | Empty test package init |
| `_bmad/mm/config.yaml` | Exists | Has `gitlab_url: "https://gitlab.example.com"` |
| `.claude/mcp.json` | Exists | Has gitlab-mcp server registration |

### Files to CREATE in This Story

| File | Purpose |
|------|---------|
| `mcp-servers/gitlab_mcp/gitlab_client.py` | NEW — All python-gitlab API call logic |
| `tests/gitlab_mcp/test_gitlab_client.py` | NEW — Unit tests for GitlabClient |
| `tests/gitlab_mcp/test_server.py` | NEW — Tool-level tests for server.py |
| `tests/gitlab_mcp/fixtures/__init__.py` | NEW — Fixtures package init |
| `tests/gitlab_mcp/fixtures/mock_gitlab.py` | NEW — Mock GitLab API responses |

### Files to MODIFY in This Story

| File | Changes |
|------|---------|
| `mcp-servers/gitlab_mcp/server.py` | Add `ping_gitlab` tool, import GitlabClient |

### Dependencies

- **Epic 1 Story 1.1**: Poetry monorepo with `python-gitlab 8.1.0` dependency — DONE (review)
- **Epic 1 Story 1.3**: Shared config loader, result.py, logging infrastructure — DONE (review)
- **`_bmad/mm/config.yaml`**: Must have `gitlab_url` field — EXISTS
- **`GITLAB_TOKEN` env var**: Must be set by operator for actual GitLab connectivity (not needed for tests)

### Non-Functional Requirements

- **NFR5**: Operations complete within 10 seconds per API call under normal network conditions
- **NFR8**: GitLab credentials via `GITLAB_TOKEN` env var — never hardcoded
- **NFR15**: MCP protocol conformance — no proprietary extensions
- **NFR16**: Supports GitLab Cloud and self-hosted (API v4)

### Project Structure Notes

- All paths align with architecture document
- `mcp-servers/` at project root, NOT inside `_bmad/`
- `tests/` at project root, NOT inside `mcp-servers/`
- `gitlab_client.py` follows the domain-module pattern established by architecture (same as `label_manager.py`, `readme_updater.py` which come in later stories)

### References

- [Source: documents/planning-artifacts/architecture.md — MCP Server Internal Structure, gitlab-mcp section]
- [Source: documents/planning-artifacts/architecture.md — Naming & Code Conventions section]
- [Source: documents/planning-artifacts/architecture.md — Error Handling Pattern section]
- [Source: documents/planning-artifacts/architecture.md — Async/Sync Bridge Pattern section]
- [Source: documents/planning-artifacts/epics.md — Epic 2, Story 2.1 full requirements]
- [Source: documents/planning-artifacts/prd.md — FR40-FR56, NFR5, NFR8, NFR15, NFR16]
- [Source: documents/implementation-artifacts/1-3-shared-mcp-server-infrastructure.md — FastMCP import pattern, no-startup-crash learning]
- [Source: python-gitlab docs — https://python-gitlab.readthedocs.io/en/stable/api-usage.html]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6

### Debug Log References
- Mock fixtures initially used `spec=gitlab.Gitlab` which conflicts with `@patch` — removed spec constraint
- `asyncio.get_event_loop().run_until_complete()` deprecation — switched to `asyncio.run()`
- Thin-wrapper test matched `import gitlab_client` as containing `import gitlab` — refined assertion

### Completion Notes List
- GitlabClient with lazy auth, asyncio.to_thread wrapping, structured error handling
- ping_gitlab tool as thin wrapper in server.py
- 18 new tests (11 client + 7 server), 98 total passing (80 existing + 18 new)
- Server starts without GITLAB_TOKEN, logs to stderr + file

### File List
- `mcp-servers/gitlab_mcp/gitlab_client.py` — NEW: GitLab API client wrapper
- `mcp-servers/gitlab_mcp/server.py` — MODIFIED: Added ping_gitlab tool, imported gitlab_client
- `tests/gitlab_mcp/test_gitlab_client.py` — NEW: 11 unit tests for GitlabClient
- `tests/gitlab_mcp/test_server.py` — NEW: 7 tool-level tests for server.py
- `tests/gitlab_mcp/fixtures/__init__.py` — NEW: Fixtures package init
- `tests/gitlab_mcp/fixtures/mock_gitlab.py` — NEW: Mock GitLab API responses

### Change Log
- 2026-03-07: Story 2.1 implemented — GitLab MCP server core with lazy auth, ping tool, 18 tests
