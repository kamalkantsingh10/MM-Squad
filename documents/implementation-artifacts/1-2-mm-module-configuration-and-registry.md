# Story 1.2: MM Module Configuration & Registry

Status: review

## Story

As an operator,
I want the MM BMAD module configuration and registry files in place,
So that the BMAD installer can discover and deploy all MM agents and workflows.

## Acceptance Criteria

1. **MM config.yaml** — `_bmad/mm/config.yaml` contains all required fields: `db_path` (default: `<project-root>/data/specdb.sqlite`), `macro_library_path`, `glossary_path`, `source_paths`, `gitlab_url`, `project_name`. No credentials stored in the file.
2. **Module help registry** — `_bmad/mm/module-help.csv` lists all 7 MM agents with slash command names and all MM workflows with slash command names.
3. **Data templates** — `_bmad/mm/data/glossary-template.md` with markdown table format (`| COBOL Name | Business Term |`), `_bmad/mm/data/macro-template.md` with empty Delta macro document template.
4. **Party mode roster** — `_bmad/mm/teams/default-party.csv` lists all 7 MM agents for party mode.

## Tasks / Subtasks

- [x] Task 1: Create MM config.yaml (AC: 1)
  - [x] Create `_bmad/mm/config.yaml` with all required fields
  - [x] Set `db_path: "<project-root>/data/specdb.sqlite"`
  - [x] Set `macro_library_path` pointing to macro library location
  - [x] Set `glossary_path` pointing to glossary location
  - [x] Set `source_paths` as empty list (client-specific)
  - [x] Set `gitlab_url` as placeholder
  - [x] Set `project_name: "MM-Squad"`
  - [x] Add comment: "GITLAB_TOKEN must be set as environment variable"
  - [x] Verify NO credentials in the file
- [x] Task 2: Create module-help.csv (AC: 2)
  - [x] Create `_bmad/mm/module-help.csv`
  - [x] List all 7 agents: Po, Tigress, Viper, Monkey, Shifu, Oogway, Mantis with slash commands (e.g., `bmad-agent-mm-po`)
  - [x] List all workflows with slash commands (e.g., `bmad-mm-analyse-structure`)
- [x] Task 3: Create data templates (AC: 3)
  - [x] Create `_bmad/mm/data/` directory
  - [x] Create `_bmad/mm/data/glossary-template.md` — markdown table: `| COBOL Name | Business Term | Description |` with header separator and example row
  - [x] Create `_bmad/mm/data/macro-template.md` — Delta macro document template with sections for macro name, description, expansion pattern, usage context
- [x] Task 4: Create party mode roster (AC: 4)
  - [x] Create `_bmad/mm/teams/` directory
  - [x] Create `_bmad/mm/teams/default-party.csv` listing all 7 agents (po, tigress, viper, monkey, shifu, oogway, mantis)

## Dev Notes

- **Config is the single source of truth** for all 5 MCP servers. Every server reads this file via `shared/config_loader.py` (Story 1.3). Never hardcode paths in server code.
- **module-help.csv format**: Follow existing BMAD module-help.csv format in `_bmad/bmm/` for reference. Check the existing file for the expected CSV column structure.
- **The `_bmad/mm/` directory must be created** — it does not exist yet. The `_bmad/` directory does exist with `core/` and `bmm/` subdirectories.
- **Agent and workflow files are NOT created in this story** — only the config, registry, templates, and party roster. Agent definitions come in Epics 2-3.

### Project Structure Notes

- `_bmad/mm/` is the MM expansion pack module root — parallel to `_bmad/bmm/`
- Config at `_bmad/mm/config.yaml` is read by MCP servers at `mcp-servers/` (not inside _bmad)
- Data templates at `_bmad/mm/data/` are reference files for new engagements
- Party roster at `_bmad/mm/teams/` follows BMAD party mode conventions

### References

- [Source: documents/planning-artifacts/architecture.md#Configuration: Single Config File] — Config schema and design rationale
- [Source: documents/planning-artifacts/architecture.md#Authentication & Security] — GITLAB_TOKEN env-var only policy
- [Source: documents/planning-artifacts/architecture.md#Project Structure & Boundaries] — _bmad/mm/ directory structure
- [Source: documents/planning-artifacts/architecture.md#Config Flow] — How config flows to each MCP server
- [Source: documents/planning-artifacts/epics.md#Story 1.2] — Full acceptance criteria

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

None — clean implementation.

### Completion Notes List

- Created _bmad/mm/config.yaml with all 7 required fields + target_language (deferred)
- No credentials in config; GITLAB_TOKEN env var comment included
- module-help.csv follows bmm format exactly: 7 agent rows + 16 workflow rows, all module=mm
- Glossary template has 3-column table (COBOL Name, Business Term, Description)
- Macro template has 4 sections (Name, Description, Expansion Pattern, Usage Context)
- Party roster CSV follows bmm default-party.csv format with all 7 agents
- 17 unit tests covering all 4 ACs — all passing
- 43 total tests (including Story 1-1) — zero regressions

### File List

- _bmad/mm/config.yaml (new)
- _bmad/mm/module-help.csv (new)
- _bmad/mm/data/glossary-template.md (new)
- _bmad/mm/data/macro-template.md (new)
- _bmad/mm/teams/default-party.csv (new)
- tests/test_mm_module_registry.py (new)
