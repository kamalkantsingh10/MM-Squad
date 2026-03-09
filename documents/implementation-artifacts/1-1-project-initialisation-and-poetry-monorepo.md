# Story 1.1: Project Initialisation & Poetry Monorepo

Status: review

## Story

As an operator,
I want a fully initialised Poetry monorepo with all project dependencies and directory scaffolding,
So that all downstream MCP servers and agents have a consistent, reproducible foundation to build on.

## Acceptance Criteria

1. **Poetry monorepo initialised** — `pyproject.toml` exists at project root with Python ^3.12 target, all dependencies declared (fastmcp 3.1.0, aiosqlite 0.22.1, lark 0.12.0, python-gitlab 8.1.0), pytest as dev dependency. `poetry install` succeeds cleanly.
2. **MCP server package directories** — `mcp-servers/` contains 5 package directories (`cobol_parser_mcp/`, `specdb_mcp/`, `delta_macros_mcp/`, `jcl_parser_mcp/`, `gitlab_mcp/`) each with `__init__.py`. `mcp-servers/shared/` exists with `__init__.py`.
3. **Test directory structure** — `tests/` at root mirrors mcp-servers structure: `tests/__init__.py`, and 5 subdirectories (`cobol_parser_mcp/`, `specdb_mcp/`, `delta_macros_mcp/`, `jcl_parser_mcp/`, `gitlab_mcp/`) each with `__init__.py` and `fixtures/` subdirectory. `tests/cobol_parser_mcp/fixtures/blackjack/` with `src/` and `copy/` subdirs.
4. **Runtime directories** — `data/` and `logs/` exist at project root, each with `.gitkeep`.
5. **BlackJack directory** — `blackjack/` exists at project root with `glossary.md` placeholder and `macros/` subdirectory.
6. **Templates** — `templates/glossary-template.md` contains markdown table header (`| COBOL Name | Business Term |`) and `templates/macro-template.md` contains empty Delta macro document template.
7. **Gitignore updated** — `.gitignore` includes `data/`, `logs/`, and patterns for client COBOL source directories. Does NOT exclude `data/.gitkeep` or `logs/.gitkeep`.
8. **README** — `README.md` at project root with project name (MM-Squad), brief description of the mainframe modernisation pipeline, and setup instructions (`poetry install`).

## Tasks / Subtasks

- [x] Task 1: Initialise Poetry monorepo (AC: 1)
  - [x] Check if pyproject.toml already exists; if so, update rather than overwrite
  - [x] Run `poetry init --python "^3.12"` or create pyproject.toml manually
  - [x] Add dependencies: `poetry add fastmcp aiosqlite lark python-gitlab`
  - [x] Add dev dependency: `poetry add --group dev pytest`
  - [x] Verify `poetry install` completes without errors
  - [x] Verify `poetry.lock` is generated
- [x] Task 2: Create MCP server package directories (AC: 2)
  - [x] Create `mcp-servers/cobol_parser_mcp/__init__.py`
  - [x] Create `mcp-servers/specdb_mcp/__init__.py`
  - [x] Create `mcp-servers/delta_macros_mcp/__init__.py`
  - [x] Create `mcp-servers/jcl_parser_mcp/__init__.py`
  - [x] Create `mcp-servers/gitlab_mcp/__init__.py`
  - [x] Create `mcp-servers/shared/__init__.py`
- [x] Task 3: Create test directory structure (AC: 3)
  - [x] Create `tests/__init__.py`
  - [x] Create `tests/cobol_parser_mcp/__init__.py` and `tests/cobol_parser_mcp/fixtures/blackjack/src/` and `copy/` (with .gitkeep)
  - [x] Create `tests/specdb_mcp/__init__.py` and `tests/specdb_mcp/fixtures/`
  - [x] Create `tests/delta_macros_mcp/__init__.py` and `tests/delta_macros_mcp/fixtures/`
  - [x] Create `tests/jcl_parser_mcp/__init__.py` and `tests/jcl_parser_mcp/fixtures/`
  - [x] Create `tests/gitlab_mcp/__init__.py` and `tests/gitlab_mcp/fixtures/`
- [x] Task 4: Create runtime and support directories (AC: 4, 5, 6)
  - [x] Create `data/.gitkeep`
  - [x] Create `logs/.gitkeep`
  - [x] Create `blackjack/glossary.md` with placeholder content
  - [x] Create `blackjack/macros/` with `.gitkeep`
  - [x] Create `templates/glossary-template.md` with `| COBOL Name | Business Term |` table header
  - [x] Create `templates/macro-template.md` with empty Delta macro template
- [x] Task 5: Update .gitignore (AC: 7)
  - [x] Add `data/` (with `!data/.gitkeep` exception)
  - [x] Add `logs/` (with `!logs/.gitkeep` exception)
  - [x] Add patterns for client COBOL source (e.g., `*.cob`, `*.cpy` outside blackjack fixtures)
  - [x] Add `__pycache__/`, `*.pyc`, `.pytest_cache/`
- [x] Task 6: Create README.md (AC: 8)
  - [x] Project name: MM-Squad
  - [x] Brief description: BMAD expansion pack for mainframe modernisation — AI agent pipeline with 7 agents and 5 MCP servers
  - [x] Setup instructions: prerequisites (Python 3.12, Poetry), `poetry install`, running MCP servers

## Dev Notes

- **Poetry monorepo pattern**: Single root `pyproject.toml` manages all 5 MCP server packages. Individual servers are run via `poetry run python -m <package>.server`.
- **Package discovery**: For Poetry to find packages under `mcp-servers/`, the `pyproject.toml` needs `packages` configuration pointing to `mcp-servers/` subdirectories.
- **__init__.py files**: All package and test directories need `__init__.py` for Python import resolution.
- **No server code yet**: This story creates ONLY the directory scaffolding and `__init__.py` files. Skeleton `server.py` files with FastMCP app init come in Story 1.3.

### Project Structure Notes

- All paths follow the architecture document's complete directory tree exactly
- `mcp-servers/` lives at project root, NOT inside `_bmad/`
- `tests/` lives at project root, NOT inside `mcp-servers/`
- `_bmad/` already exists with core and bmm modules — do not modify
- `documents/` already exists — do not modify

### References

- [Source: documents/planning-artifacts/architecture.md#Starter Template Evaluation] — Poetry init commands, dependency versions
- [Source: documents/planning-artifacts/architecture.md#Project Structure & Boundaries] — Complete directory tree
- [Source: documents/planning-artifacts/architecture.md#Naming Patterns] — File and package naming conventions
- [Source: documents/planning-artifacts/architecture.md#Implementation Handoff] — Phase 1 item 1: Initial setup
- [Source: documents/planning-artifacts/epics.md#Story 1.1] — Full acceptance criteria

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

None — clean implementation, no issues encountered.

### Completion Notes List

- Created pyproject.toml with Poetry monorepo config, packages pointing to mcp-servers/ subdirs
- All 4 pinned deps (fastmcp 3.1.0, aiosqlite 0.22.1, lark 0.12.0, python-gitlab 8.1.0) + pytest dev dep
- poetry install succeeded, poetry.lock generated (78 packages)
- 5 MCP server packages + shared package under mcp-servers/, all with __init__.py
- Test directory structure mirrors mcp-servers with fixtures dirs; blackjack fixtures has src/ and copy/ subdirs
- Runtime dirs data/ and logs/ with .gitkeep; blackjack/ with glossary.md and macros/
- Templates: glossary-template.md with COBOL Name/Business Term table, macro-template.md with Delta macro scaffold
- .gitignore updated: data/, logs/ with !.gitkeep exceptions, Python patterns, COBOL source patterns with fixture exceptions
- README.md with project name, description, prerequisites, setup, and run instructions
- 26 unit tests covering all 8 ACs — all passing

### File List

- pyproject.toml (new)
- poetry.lock (new)
- README.md (modified)
- .gitignore (modified)
- mcp-servers/cobol_parser_mcp/__init__.py (new)
- mcp-servers/specdb_mcp/__init__.py (new)
- mcp-servers/delta_macros_mcp/__init__.py (new)
- mcp-servers/jcl_parser_mcp/__init__.py (new)
- mcp-servers/gitlab_mcp/__init__.py (new)
- mcp-servers/shared/__init__.py (new)
- tests/__init__.py (new)
- tests/test_project_structure.py (new)
- tests/cobol_parser_mcp/__init__.py (new)
- tests/specdb_mcp/__init__.py (new)
- tests/delta_macros_mcp/__init__.py (new)
- tests/jcl_parser_mcp/__init__.py (new)
- tests/gitlab_mcp/__init__.py (new)
- data/.gitkeep (new)
- logs/.gitkeep (new)
- blackjack/glossary.md (new)
- blackjack/macros/.gitkeep (new)
- templates/glossary-template.md (new)
- templates/macro-template.md (new)
