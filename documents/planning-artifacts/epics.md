---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics']
inputDocuments:
  - documents/planning-artifacts/prd.md
  - documents/planning-artifacts/architecture.md
---

# MM-Squad - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for MM-Squad, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**COBOL Structural Analysis (Po — Analyse Structure Workflow)**

- FR1: Analyst can initiate structural analysis of a COBOL module and receive a paragraph call graph
- FR2: Analyst can view a complexity score (Low/Medium/High) for any analysed COBOL module
- FR3: Analyst can view anti-patterns detected in a COBOL module (GOTOs, nested PERFORMs, REDEFINES, etc.)
- FR4: Analyst can view extracted COPY, CALL, SQL, CICS, and Delta macro references per module
- FR5: Analyst can view AI-generated semantic cluster groupings for a module's paragraphs
- FR6: Analyst can view plain-English descriptions for each semantic cluster
- FR7: Analyst can review, correct, and approve AI analysis outputs before they are written to the spec layer
- FR8: Analyst can view a warning when Po encounters an unrecognised COBOL construct or unknown Delta macro

**Cross-Module Dependency Mapping (Po — Map Dependencies Workflow)**

- FR9: Analyst can initiate cross-module dependency analysis across all COBOL modules in scope
- FR10: Architect can view a Mermaid dependency diagram showing relationships between all modules
- FR11: Architect can view detected subsystem groupings emerging from the dependency structure
- FR12: Architect can view a recommended migration order based on module dependencies
- FR13: Analyst can view detected circular dependencies and dead code across modules

**Business Rule Extraction & Spec Layer (Po — Extract Business Rules Workflow)**

- FR14: Analyst can initiate business rule extraction for a COBOL module using structural analysis and dependency outputs
- FR15: Business Validator can view plain-English business markdown for any module (purpose, use cases, business rules, data entities with glossary names)
- FR16: Business Validator can validate each extracted business rule as confirmed, corrected, or rejected
- FR17: System writes approved business rules, entities, operations, and data flows to the SQLite spec layer
- FR18: Analyst can re-run business rule extraction on a module and have the spec layer update idempotently without duplicates

**Migration Architecture (Oogway — Existing BMAD Architect)**

- FR19: Architect can initiate migration architecture generation from the populated spec layer
- FR20: Architect can view a target architecture document mapping COBOL subsystems to target-language services
- FR21: Architect can specify the target language as an input to Oogway
- FR22: Architect can review and modify the generated architecture before it is finalised

**Code Generation (Tigress / Viper / Monkey — Modified BMAD Dev)**

- FR23: Developer can initiate target-language code generation for a module from the spec layer and architecture
- FR24: Developer can view generated target-language code for each COBOL module
- FR25: Developer can regenerate code for a specific module without affecting other modules

**QA Validation (Mantis — Existing BMAD QA)**

- FR26: QA can initiate validation of generated code against spec layer business rules
- FR27: QA can view a validation report showing which business rules are confirmed, partially covered, or missing in the generated code
- FR28: QA can flag a module as requiring rework before sign-off

**Pipeline Configuration & Infrastructure**

- FR29: Operator can initialise the SQLite spec layer schema with a single command via specdb-mcp
- FR30: Analyst can configure a client-specific glossary mapping COBOL field names to business terms
- FR31: Analyst can add a new macro definition to delta-macros-mcp without restarting the pipeline
- FR32: Operator can install the MM expansion pack into any BMAD-compatible IDE via standard bmad reinstall
- FR33: Analyst can re-run any individual workflow on a specific module without restarting the full pipeline
- FR34: Analyst can view a consolidated list of all unresolved constructs and macros flagged across workflow runs

**COBOL Dialect & Construct Coverage**

- FR35: System can parse and analyse IBM Enterprise COBOL and COBOL-85 modules
- FR36: System can detect and flag CICS transaction constructs within a COBOL module
- FR37: System can detect and flag DB2 embedded SQL constructs within a COBOL module
- FR38: System can parse COPY statements and resolve referenced copybooks
- FR39: All agents can resolve client-specific Delta macro references via delta-macros-mcp at analysis time

**GitLab Project Management (Shifu — PM + SM via gitlab-mcp)**

- FR40: PM can initialise a GitLab project with standard label taxonomy: pipeline stage labels, complexity labels, and status labels
- FR41: PM can create a standard milestone structure per engagement phase in GitLab
- FR42: PM can create a GitLab issue board configured with columns mapped to pipeline stages
- FR43: Each COBOL module has a dedicated GitLab Issue tracking its complete pipeline lifecycle from analysis through QA sign-off
- FR44: Any agent can apply the appropriate stage completion label to a module's GitLab Issue upon completing its stage
- FR45: Any agent can transition a module Issue to Awaiting-Review status when its stage output requires analyst approval
- FR46: Analyst can close the review gate on a module Issue and transition it to the next pipeline stage
- FR47: PM can create GitLab sprint milestones scoped to a specific set of modules based on dependency analysis migration order
- FR48: PM can assign module Issues to sprint milestones, respecting subsystem dependencies
- FR49: PM can view a milestone burndown showing open vs closed module Issues within a sprint
- FR50: Any agent can post a structured progress comment to a module's GitLab Issue when it completes a stage
- FR51: The GitLab project README is updated by any agent that changes module status
- FR52: Client Sponsor can view a README dashboard showing total modules, modules per pipeline stage, modules blocked, and Epics signed off
- FR53: PM can generate a milestone summary comment on any Epic showing sprint progress and outstanding items
- FR54: Business Validator can formally sign off on Po's business markdown by closing the Awaiting-Review gate on a module Issue
- FR55: QA can sign off on an Epic, triggering Epic completion in GitLab with a validation summary comment
- FR56: QA can formally close an Epic when all module Issues within it are QA-Complete

### NonFunctional Requirements

**Performance**

- NFR1: Po Phase 1 static pre-pass completes on any single COBOL module within 15 minutes on standard developer hardware
- NFR2: cobol-parser-mcp parsing tools return results within 30 seconds for any module up to 5,000 lines
- NFR3: specdb-mcp read and write operations complete within 2 seconds for any single spec layer record or query
- NFR4: delta-macros-mcp macro lookups resolve within 1 second per call
- NFR5: gitlab-mcp operations complete within 10 seconds per API call under normal network conditions

**Security & Data Privacy**

- NFR6: No COBOL source code, business rules, or extracted spec data is transmitted outside the local environment by any agent or MCP server
- NFR7: Where remote LLM API calls are used, source code is scoped to the minimum required context
- NFR8: GitLab credentials are stored via GITLAB_TOKEN environment variable — never hardcoded in agent definitions or MCP server config files
- NFR9: delta-macros-mcp macro library is stored locally and not synchronised to any external service

**Reliability & Reproducibility**

- NFR10: Running any workflow twice on the same input produces equivalent SQLite spec layer output — spec layer writes are idempotent
- NFR11: Any agent encountering an unrecognised construct, unknown macro, or LLM error fails with an explicit, actionable error message — silent failures are not permitted
- NFR12: A failed workflow run does not corrupt existing spec layer records — partial writes roll back or are clearly flagged as incomplete
- NFR13: All MCP servers remain operational across agent session restarts without requiring full reinitialisation

**Integration & Compatibility**

- NFR14: The MM expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)
- NFR15: All MCP servers conform to the MCP protocol specification — no proprietary extensions that break cross-IDE compatibility
- NFR16: gitlab-mcp supports GitLab Cloud and self-hosted GitLab instances (API v4)
- NFR17: The SQLite spec layer schema is versioned — schema migrations do not break existing data or require manual intervention

**Maintainability**

- NFR18: Each BMAD agent definition is independently updatable without requiring changes to any other agent or MCP server
- NFR19: Each MCP server exposes a clearly defined, versioned tool interface — adding new tools does not break existing tool calls
- NFR20: Glossary file format and macro library format use human-readable, plain-text markup — no binary formats or proprietary schemas
- NFR21: The BlackJack corpus serves as the regression test baseline — any change to an MCP server is validated against BlackJack end-to-end before release

### Additional Requirements

**From Architecture — Starter Template & Project Init:**

- No traditional starter template — foundation is BMAD module structure (_bmad/mm/) plus Python MCP server packages
- Poetry monorepo init required: single root pyproject.toml + poetry.lock, Python 3.12, all 5 MCP servers as packages under mcp-servers/
- Initial dependencies: fastmcp 3.1.0, aiosqlite 0.22.1, lark 0.12.0, python-gitlab 8.1.0, pytest (dev)

**From Architecture — Infrastructure & Configuration:**

- Single config file: _bmad/mm/config.yaml — all MCP servers read from one file via shared config_loader.py
- Shared config loader module: mcp-servers/shared/config_loader.py
- IDE config files must be generated: .claude/mcp.json and .vscode/mcp.json (identical format)
- STDIO transport for all 5 MCP servers (IDE spawns subprocess, stdin/stdout communication)
- Dual logging on all MCP servers: stderr (real-time) + log file (<project-root>/logs/<server-name>.log)
- SQLite DB location configurable via db_path in config.yaml, default: <project-root>/data/specdb.sqlite
- Runtime directories: data/ and logs/ (gitignored)

**From Architecture — Implementation Patterns (Cross-Cutting):**

- Structured result format: make_result() / make_error() / make_warning() from result.py in every MCP server
- Idempotency pattern: INSERT OR IGNORE + UPDATE (check-then-upsert) for all spec layer writes
- Transaction per tool call in specdb-mcp (rollback on failure)
- asyncio.to_thread() required for gitlab-mcp to wrap synchronous python-gitlab calls within async FastMCP tools
- All MCP tools named exactly as defined in PRD tool lists (verb-first snake_case)
- server.py contains ONLY thin wrapper tool definitions — business logic in domain modules
- Per-tool try/except error handling — no exceptions propagate to FastMCP's default handler
- ISO 8601 UTC timestamps in all SQLite columns and tool outputs
- program_name (COBOL PROGRAM-ID verbatim, uppercase with hyphens) as canonical identity key everywhere
- result.py copied per server for MVP (shared package deferred)

**From Architecture — MCP Server Boundaries:**

- cobol-parser-mcp owns: COBOL parsing, call graph, complexity, anti-patterns, dialect detection
- specdb-mcp owns: All SQLite reads/writes, schema management
- delta-macros-mcp owns: Macro library reads, search, ingest
- jcl-parser-mcp owns: JCL parsing, job step extraction, dataset allocation, job graphs
- gitlab-mcp owns: All GitLab API calls, label management, README updates
- Spec layer (SQLite) is the ONLY shared state between agents — no direct agent-to-agent communication

**From Architecture — Build Order (PRD Build Strategy):**

- Phase 1 (Foundation): Initial setup, gitlab-mcp, Shifu agent
- Phase 2 (Remaining Agents): Tigress, Viper, Monkey, Oogway, Mantis
- Phase 3 (Analysis + MCP): specdb-mcp, delta-macros-mcp, cobol-parser-mcp, jcl-parser-mcp, Po agent, E2E demo

**From Architecture — All 7 MM agents are net-new:**

- All agents require full authoring from scratch following BMAD module conventions
- Agent files live in _bmad/mm/agents/ with corresponding workflows in _bmad/mm/workflows/

### FR Coverage Map

- FR1: Epic 5 / Epic 6 — COBOL parsing tools (Epic 5) consumed by Po workflows (Epic 6)
- FR2: Epic 5 / Epic 6 — Complexity scoring tool (Epic 5) consumed by Po workflows (Epic 6)
- FR3: Epic 5 / Epic 6 — Anti-pattern detection tool (Epic 5) consumed by Po workflows (Epic 6)
- FR4: Epic 5 / Epic 6 — Reference extraction tool (Epic 5) consumed by Po workflows (Epic 6)
- FR5: Epic 6 — Po AI semantic clustering workflow
- FR6: Epic 6 — Po plain-English description generation workflow
- FR7: Epic 6 — Po review gate before spec layer writes
- FR8: Epic 5 / Epic 6 — Unknown construct flagging (parser tool Epic 5, surfaced in Po workflow Epic 6)
- FR9: Epic 6 — Po Map Dependencies workflow
- FR10: Epic 6 — Po Mermaid dependency diagram generation
- FR11: Epic 6 — Po subsystem grouping detection
- FR12: Epic 6 — Po migration order recommendation
- FR13: Epic 6 — Po circular dependency and dead code detection
- FR14: Epic 6 — Po Extract Business Rules workflow
- FR15: Epic 6 — Po business markdown generation
- FR16: Epic 6 — Po business rule validation (confirm/correct/reject)
- FR17: Epic 4 / Epic 6 — specdb-mcp write tools (Epic 4), consumed by Po workflows (Epic 6)
- FR18: Epic 4 / Epic 6 — Idempotent spec layer updates (Epic 4), exercised by Po (Epic 6)
- FR19: Epic 3 — Oogway agent definition and migration architecture workflow
- FR20: Epic 3 — Oogway target architecture document generation
- FR21: Epic 3 — Oogway target language input
- FR22: Epic 3 — Oogway architecture review and modification
- FR23: Epic 3 — Tigress/Viper/Monkey agent definitions and code generation workflows
- FR24: Epic 3 — Dev agents target-language code output
- FR25: Epic 3 — Dev agents per-module regeneration
- FR26: Epic 3 / Epic 7 — Mantis agent definition (Epic 3), validated in E2E pipeline (Epic 7)
- FR27: Epic 3 / Epic 7 — Mantis validation report (Epic 3), proven in E2E pipeline (Epic 7)
- FR28: Epic 3 / Epic 7 — Mantis rework flagging (Epic 3), proven in E2E pipeline (Epic 7)
- FR29: Epic 4 — specdb-mcp init_schema tool
- FR30: Epic 4 — Glossary configuration via config.yaml + agent workflows
- FR31: Epic 4 — delta-macros-mcp add_macro tool
- FR32: Epic 1 — MM expansion pack installer via bmad reinstall
- FR33: Epic 1 / Epic 6 — Re-run infra (Epic 1), exercised by Po workflows (Epic 6)
- FR34: Epic 4 / Epic 6 — Flags array in result format (Epic 4), consolidated view in Po (Epic 6)
- FR35: Epic 5 — cobol-parser-mcp IBM Enterprise COBOL and COBOL-85 support
- FR36: Epic 5 — cobol-parser-mcp CICS construct detection
- FR37: Epic 5 — cobol-parser-mcp DB2 SQL construct detection
- FR38: Epic 5 — cobol-parser-mcp COPY statement and copybook resolution
- FR39: Epic 4 / Epic 5 — delta-macros-mcp resolution (Epic 4), integrated in parser (Epic 5)
- FR40: Epic 2 — gitlab-mcp label taxonomy + Shifu project initialisation
- FR41: Epic 2 — gitlab-mcp milestone creation + Shifu milestone structure
- FR42: Epic 2 — gitlab-mcp board creation + Shifu board configuration
- FR43: Epic 2 — gitlab-mcp issue creation + Shifu per-module Issue tracking
- FR44: Epic 2 — gitlab-mcp apply_label tool for stage completion
- FR45: Epic 2 — gitlab-mcp apply_label tool for Awaiting-Review transition
- FR46: Epic 2 — gitlab-mcp remove_label + apply_label for review gate closure
- FR47: Epic 2 — gitlab-mcp create_milestone + Shifu sprint milestone planning
- FR48: Epic 2 — gitlab-mcp assign_to_milestone + Shifu dependency-aware assignment
- FR49: Epic 2 — gitlab-mcp milestone query + Shifu burndown view
- FR50: Epic 2 — gitlab-mcp add_comment for structured progress updates
- FR51: Epic 2 — gitlab-mcp update_readme for status-triggered README updates
- FR52: Epic 2 — gitlab-mcp update_readme + Shifu dashboard generation
- FR53: Epic 2 — gitlab-mcp add_comment + Shifu milestone summary
- FR54: Epic 2 — gitlab-mcp update_issue_status for business rule sign-off
- FR55: Epic 2 — gitlab-mcp close_epic + add_comment for QA Epic sign-off
- FR56: Epic 2 — gitlab-mcp close_epic for QA-Complete Epic closure

**Coverage Summary:**
- All 56 FRs mapped
- Epic 1: FR32, FR33
- Epic 2: FR40-FR56 (17 FRs)
- Epic 3: FR19-FR28 (10 FRs)
- Epic 4: FR17-FR18, FR29-FR31, FR33-FR34, FR39 (8 FRs)
- Epic 5: FR1-FR4, FR8, FR35-FR39 (9 FRs)
- Epic 6: FR1-FR18, FR34 (18 FRs — Po workflows consuming all upstream tools)
- Epic 7: FR26-FR28 (3 FRs — E2E validation of full pipeline)
- Note: Some FRs span multiple epics (tool built in one, consumed in another)

## Epic List

### Epic 1: MM Expansion Pack Foundation
*(Phase 1, item 1)*

Operator can install the MM expansion pack via `bmad reinstall` and have a working BMAD module structure — scaffolding, config.yaml, module-help.csv, Poetry monorepo with all dependencies, shared config loader, result.py pattern, IDE config files, directory structure.

**FRs covered:** FR32, FR33 (infra)
**Additional:** All architecture scaffolding requirements

### Epic 2: GitLab Delivery Management
*(Phase 1, items 2-3)*

Shifu (PM+SM) can initialise a GitLab project with label taxonomy, milestones, issue boards, per-module Issue tracking, sprint management, README dashboard, and formal review gates/sign-offs. gitlab-mcp is fully operational. Validates the expansion pack installer pattern on both Claude Code and GitHub Copilot.

**FRs covered:** FR40-FR56

### Epic 3: Dev, Architect & QA Agent Definitions
*(Phase 2, items 4-8)*

All remaining agent definitions are authored, deployed via `bmad reinstall`, and invocable as slash commands. Tigress (Java), Viper (COBOL), Monkey (Python), Oogway (Architect), Mantis (QA) — each with complete workflow step files and persona definitions following BMAD conventions.

**FRs covered:** FR19-FR28

### Epic 4: Spec Layer & Knowledge Infrastructure
*(Phase 3, items 9-10)*

Operator can initialise the SQLite spec layer schema. Analyst can configure a glossary and manage Delta macros without restarting the pipeline. specdb-mcp and delta-macros-mcp are fully operational with idempotent writes, transaction rollback, and structured result format.

**Cross-cutting:** Each MCP server story must include a README.md with setup instructions (prerequisites, env vars, `.mcp.json` config, verification steps).

**FRs covered:** FR17-FR18, FR29-FR31, FR33-FR34, FR39

### Epic 5: COBOL & JCL Parsing Engines
*(Phase 3, items 11-12)*

cobol-parser-mcp can parse IBM Enterprise COBOL and COBOL-85 modules — call graphs, complexity scoring, anti-pattern detection, CICS/DB2 SQL/COPY/Delta macro reference extraction. jcl-parser-mcp can parse JCL jobs, steps, and dataset allocations. Full dialect coverage with explicit flagging of unrecognised constructs.

**Cross-cutting:** Each MCP server story must include a README.md with setup instructions (prerequisites, env vars, `.mcp.json` config, verification steps).

**FRs covered:** FR1-FR4, FR8, FR35-FR39

### Epic 6: Po Analysis Agent
*(Phase 3, item 13)*

Po is fully operational with all 3 core workflows: Analyse Structure (semantic clustering, AI analysis, review gates, spec layer writes), Map Dependencies (Mermaid diagrams, subsystem detection, migration order, circular deps), Extract Business Rules (business markdown, validation, idempotent spec population). Consolidated flag view across all runs.

**FRs covered:** FR1-FR18, FR34

### Epic 7: End-to-End Pipeline Validation
*(Phase 3, item 14)*

Full pipeline proven on BlackJack corpus (8 modules, 3 copybooks): Po analyse -> Po dependencies -> Po business rules -> Oogway architecture -> Tigress/Viper/Monkey code gen -> Mantis QA validation -> Shifu GitLab tracking. All NFRs validated. BlackJack established as regression baseline.

**FRs covered:** FR26-FR28 (QA validation in live pipeline context), all FRs validated end-to-end

---

## Epic 1: MM Expansion Pack Foundation

Operator can install the MM expansion pack via `bmad reinstall` and have a working BMAD module structure — scaffolding, config.yaml, module-help.csv, Poetry monorepo with all dependencies, shared config loader, result.py pattern, IDE config files, directory structure.

### Story 1.1: Project Initialisation & Poetry Monorepo

As an operator,
I want a fully initialised Poetry monorepo with all project dependencies and directory scaffolding,
So that all downstream MCP servers and agents have a consistent, reproducible foundation to build on.

**Acceptance Criteria:**

**Given** the project root exists
**When** the operator runs `poetry install`
**Then** all dependencies are installed: fastmcp 3.1.0, aiosqlite 0.22.1, lark 0.12.0, python-gitlab 8.1.0
**And** pytest is available as a dev dependency
**And** Python 3.12 is the target runtime

**Given** the project root exists
**When** the operator inspects the directory structure
**Then** `mcp-servers/` contains 5 empty package directories: `cobol_parser_mcp/`, `specdb_mcp/`, `delta_macros_mcp/`, `jcl_parser_mcp/`, `gitlab_mcp/`
**And** `mcp-servers/shared/` exists with `__init__.py`
**And** `tests/` mirrors the mcp-servers structure with `__init__.py` files
**And** `data/` exists with `.gitkeep`
**And** `logs/` exists with `.gitkeep`
**And** `blackjack/` directory exists for the demo engagement
**And** `templates/` contains `glossary-template.md` and `macro-template.md`

**Given** the project root exists
**When** the operator inspects `.gitignore`
**Then** `data/`, `logs/`, and client COBOL source directories are excluded from version control

**Given** the project root exists
**When** the operator inspects `README.md`
**Then** it contains the project name, a brief description, and setup instructions

### Story 1.2: MM Module Configuration & Registry

As an operator,
I want the MM BMAD module configuration and registry files in place,
So that the BMAD installer can discover and deploy all MM agents and workflows.

**Acceptance Criteria:**

**Given** the `_bmad/mm/` directory exists
**When** the operator inspects `_bmad/mm/config.yaml`
**Then** it contains all required fields: `db_path`, `macro_library_path`, `glossary_path`, `source_paths`, `gitlab_url`, `project_name`
**And** `db_path` defaults to `<project-root>/data/specdb.sqlite`
**And** no credentials are stored in the config file (GITLAB_TOKEN is env-var only)

**Given** the `_bmad/mm/` directory exists
**When** the operator inspects `_bmad/mm/module-help.csv`
**Then** it lists all 7 MM agents (Po, Tigress, Viper, Monkey, Shifu, Oogway, Mantis) with their slash command names
**And** it lists all MM workflows with their slash command names

**Given** the `_bmad/mm/` directory exists
**When** the operator inspects `_bmad/mm/data/`
**Then** `glossary-template.md` exists with the markdown table format (`| COBOL Name | Business Term |`)
**And** `macro-template.md` exists with the empty Delta macro document template

**Given** the `_bmad/mm/` directory exists
**When** the operator inspects `_bmad/mm/teams/`
**Then** `default-party.csv` exists listing all 7 MM agents for party mode

### Story 1.3: Shared MCP Server Infrastructure

As a developer,
I want shared config loading and result formatting infrastructure available to all MCP servers,
So that every server reads configuration consistently and returns structured results in the same format.

**Acceptance Criteria:**

**Given** the shared module exists at `mcp-servers/shared/`
**When** any MCP server imports `config_loader`
**Then** it reads `_bmad/mm/config.yaml` and provides typed access to all settings
**And** config is loaded once and cached for the server's lifetime

**Given** the `result.py` template exists
**When** a developer copies it into any MCP server package
**Then** `make_result(data, flags, message, status)` returns the structured dict with `status`, `data`, `flags`, `message`
**And** `make_error(message, flags)` returns a result with `status: "error"`
**And** `make_warning(data, message, flags)` returns a result with `status: "warning"`
**And** `flags` is always a list of dicts with `code`, `message`, `location` keys

**Given** the logging pattern is established
**When** any MCP server starts
**Then** it logs to both stderr (StreamHandler) and a log file at `<project-root>/logs/<server-name>.log` (FileHandler)
**And** log levels follow the architecture: DEBUG (internal state), INFO (tool calls), WARNING (flagged items), ERROR (failures)

**Given** all 5 MCP server packages exist under `mcp-servers/`
**When** the developer inspects any server package
**Then** it contains `__init__.py` and a skeleton `server.py` with FastMCP app initialisation
**And** `server.py` imports from the shared config loader
**And** each server can be started with `poetry run python -m <package_name>.server` (even if no tools are registered yet)

### Story 1.4: IDE Configuration & Installer Validation

As an operator,
I want the MM expansion pack to install correctly via `bmad reinstall` and register all MCP servers in IDE configuration,
So that I can invoke MM agents as slash commands and IDE can spawn MCP server subprocesses.

**Acceptance Criteria:**

**Given** the MM module is in `_bmad/mm/`
**When** the operator runs `bmad reinstall`
**Then** MM agent slash commands are deployed to `.claude/commands/` (e.g., `bmad-agent-mm-po.md`, `bmad-agent-mm-shifu.md`)
**And** MM workflow slash commands are deployed (e.g., `bmad-mm-analyse-structure.md`)

**Given** the IDE config files are generated
**When** the operator inspects `.claude/mcp.json`
**Then** all 5 MCP servers are registered with `command: "poetry"`, `args: ["run", "python", "-m", "<package>.server"]`
**And** the format matches the architecture specification

**Given** the IDE config files are generated
**When** the operator inspects `.vscode/mcp.json`
**Then** it contains identical server registration as `.claude/mcp.json`
**And** GitHub Copilot can discover all registered MCP servers

**Given** the MM module is installed
**When** the operator invokes any MM agent slash command (e.g., `/bmad-agent-mm-shifu`)
**Then** the agent loads and presents its menu
**And** FR32 is satisfied

---

## Epic 2: GitLab Delivery Management

Shifu (PM+SM) can initialise a GitLab project with label taxonomy, milestones, issue boards, per-module Issue tracking, sprint management, README dashboard, and formal review gates/sign-offs. gitlab-mcp is fully operational. Validates the expansion pack installer pattern on both Claude Code and GitHub Copilot.

**GitLab Project Structure:**
- **Project** = one modernisation engagement
- **Epic** = one COBOL subsystem (group of related modules from dependency analysis)
- **Issue** = one COBOL module's pipeline lifecycle
- **Milestone** = one sprint (scoped to modules by migration order)
- **Board** = pipeline stage view (In-Analysis, Awaiting-Review, In-Migration, Blocked, Done)
- **Labels** = pipeline stage (`Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`), complexity (`Complexity::Low`, `Complexity::Medium`, `Complexity::High`), status (`In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`)

### Story 2.1: gitlab-mcp Server Core & Authentication

As a developer,
I want a working gitlab-mcp MCP server that authenticates with GitLab and provides the foundation for all GitLab tools,
So that all downstream tools have a reliable, tested connection to the GitLab API.

**Acceptance Criteria:**

**Given** `GITLAB_TOKEN` is set as an environment variable
**When** gitlab-mcp starts via `poetry run python -m gitlab_mcp.server`
**Then** it connects to the GitLab instance specified in `_bmad/mm/config.yaml` (`gitlab_url`)
**And** the python-gitlab client is initialised and authenticated
**And** the server registers with FastMCP via STDIO transport

**Given** `GITLAB_TOKEN` is NOT set
**When** gitlab-mcp starts
**Then** it fails with an explicit error message: "GITLAB_TOKEN environment variable not set"
**And** the error is logged to stderr and the log file

**Given** gitlab-mcp is running
**When** any tool function calls the GitLab API
**Then** the synchronous python-gitlab call is wrapped in `asyncio.to_thread()` to avoid blocking the async event loop

**Given** gitlab-mcp is running
**When** any tool encounters a GitLab API error
**Then** it returns `make_error()` with a `GITLAB_API_ERROR` flag code, the HTTP status, and an actionable message
**And** the error is logged at ERROR level

**Given** gitlab-mcp is running
**When** any tool completes successfully
**Then** it returns `make_result()` with `status: "ok"` and the relevant data payload

**Given** the gitlab-mcp package structure
**When** a developer inspects the code
**Then** `server.py` contains only thin wrapper tool definitions
**And** `gitlab_client.py` contains all python-gitlab API call logic
**And** `result.py` contains make_result/make_error/make_warning helpers
**And** NFR5 (< 10s per API call), NFR8 (env var auth), NFR15 (MCP protocol), NFR16 (Cloud + self-hosted) are satisfied

### Story 2.2: GitLab Project Initialisation

As a PM (Shifu),
I want to initialise a GitLab project with the standard label taxonomy, milestone structure, and pipeline stage board,
So that the modernisation engagement has a properly configured tracking structure from day one.

**Acceptance Criteria:**

**Given** gitlab-mcp is running and authenticated
**When** the PM invokes the project initialisation workflow
**Then** the following pipeline stage labels are created: `Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`
**And** the following complexity labels are created: `Complexity::Low`, `Complexity::Medium`, `Complexity::High`
**And** the following status labels are created: `In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`
**And** FR40 is satisfied

**Given** labels have been created
**When** the PM creates the milestone structure
**Then** milestones are created for each engagement phase (configurable per engagement)
**And** FR41 is satisfied

**Given** labels and milestones exist
**When** the PM creates the issue board
**Then** a board is created with columns mapped to pipeline stages: In-Analysis, Awaiting-Review, In-Migration, Blocked, Done
**And** FR42 is satisfied

**Given** the project is already initialised
**When** the PM re-runs project initialisation
**Then** existing labels, milestones, and boards are not duplicated
**And** the operation is idempotent

### Story 2.3: Module Issue Lifecycle & Stage Tracking

As a PM (Shifu),
I want each COBOL module to have a dedicated GitLab Issue that tracks its complete pipeline lifecycle,
So that the team has clear visibility into where every module stands in the modernisation pipeline.

**Acceptance Criteria:**

**Given** a GitLab project is initialised
**When** the PM creates a module Issue for `PAYROLL-CALC`
**Then** a GitLab Issue is created with the module name as the title
**And** the Issue is assigned the appropriate `Complexity::` label based on Po's analysis
**And** the Issue is assigned the `In-Analysis` status label
**And** FR43 is satisfied

**Given** a module Issue exists
**When** any agent completes its pipeline stage for that module
**Then** the agent applies the appropriate stage completion label (e.g., `Po-Analysis-Complete`)
**And** FR44 is satisfied

**Given** a module Issue exists
**When** any agent's output requires analyst approval
**Then** the agent transitions the Issue to `Awaiting-Review` by applying the label
**And** FR45 is satisfied

**Given** a module Issue is in `Awaiting-Review` status
**When** the analyst approves the output and closes the review gate
**Then** the `Awaiting-Review` label is removed
**And** the Issue transitions to the next pipeline stage label
**And** FR46 is satisfied

**Given** a module Issue exists
**When** the operator inspects the Issue on the pipeline board
**Then** it appears in the correct column matching its current status label

### Story 2.4: Sprint Planning & Milestone Management

As a PM (Shifu),
I want to create sprint milestones scoped to specific modules based on dependency analysis,
So that sprints respect subsystem dependencies and the team works in a logical migration order.

**Acceptance Criteria:**

**Given** module Issues exist and Po's dependency analysis has produced a migration order
**When** the PM creates a sprint milestone
**Then** the milestone is scoped to a specific set of modules based on the migration order
**And** FR47 is satisfied

**Given** a sprint milestone exists
**When** the PM assigns module Issues to the milestone
**Then** Issues are assigned respecting subsystem dependencies (e.g., shared services before consumers)
**And** FR48 is satisfied

**Given** a sprint milestone has assigned Issues
**When** the PM views the milestone
**Then** a burndown is visible showing open vs closed module Issues within that sprint
**And** FR49 is satisfied

**Given** modules have been analysed with complexity scores
**When** the PM plans a sprint
**Then** the complexity labels on Issues inform sprint capacity decisions

### Story 2.5: Progress Reporting & README Dashboard

As any pipeline agent,
I want to post structured progress comments and update the project README dashboard,
So that all stakeholders have real-time visibility into modernisation progress.

**Acceptance Criteria:**

**Given** an agent completes a pipeline stage for a module
**When** the agent posts a progress comment to the module's GitLab Issue
**Then** the comment includes: agent name, stage completed, timestamp, summary of outputs, any flags raised
**And** FR50 is satisfied

**Given** any agent changes a module's pipeline status
**When** the README is updated
**Then** the project README reflects the current state of all modules
**And** FR51 is satisfied

**Given** the README dashboard exists
**When** a Client Sponsor views the project README
**Then** they see: total modules, modules per pipeline stage, modules blocked, Epics signed off
**And** the dashboard is rendered as a markdown table
**And** FR52 is satisfied

**Given** a sprint milestone is active
**When** the PM generates a milestone summary
**Then** a comment is posted on the relevant Epic showing: sprint progress, completed modules, outstanding modules, blockers
**And** FR53 is satisfied

### Story 2.6: Review Gates, Sign-off & Epic Closure

As a Business Validator or QA engineer,
I want formal sign-off gates on module Issues and Epics,
So that no module progresses or Epic closes without explicit human approval.

**Acceptance Criteria:**

**Given** Po has generated business markdown for a module and the Issue is `Awaiting-Review`
**When** the Business Validator formally signs off
**Then** the `Awaiting-Review` gate is closed on the module Issue
**And** the Issue transitions to the next pipeline stage
**And** a sign-off comment is posted on the Issue with the validator's confirmation
**And** FR54 is satisfied

**Given** all module Issues within an Epic are `QA-Complete`
**When** QA signs off on the Epic
**Then** a validation summary comment is posted on the Epic listing all modules and their QA status
**And** Epic completion is triggered in GitLab
**And** FR55 is satisfied

**Given** an Epic has been signed off by QA
**When** QA formally closes the Epic
**Then** the Epic status is set to closed in GitLab
**And** the README dashboard reflects the closed Epic
**And** FR56 is satisfied

**Given** not all module Issues within an Epic are `QA-Complete`
**When** QA attempts to close the Epic
**Then** the operation fails with an explicit error listing which modules are incomplete

### Story 2.7: Shifu Agent Definition & Workflows

As an operator,
I want the Shifu agent (PM+SM) fully authored with persona, menu, and workflow step files,
So that Shifu can be invoked via `/bmad-agent-mm-shifu` and orchestrate all GitLab delivery management operations.

**Acceptance Criteria:**

**Given** the Shifu agent definition exists at `_bmad/mm/agents/shifu.md`
**When** the operator inspects the file
**Then** it contains: combined PM+SM persona, GitLab-native project management identity, migration status tracking capability
**And** it declares access to `gitlab-mcp` MCP server
**And** the menu lists all delivery management workflows

**Given** the Shifu workflow step files exist under `_bmad/mm/workflows/pm/`
**When** the operator inspects the workflows
**Then** the following workflows are fully authored with step files: create-epics-and-stories, sprint-planning, create-story, sprint-status, correct-course, retrospective
**And** each workflow follows BMAD step-file architecture (workflow.md + steps/)

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-shifu`
**Then** Shifu loads, presents its menu, and responds in character
**And** all menu items map to the authored workflows

**Given** Shifu is active and gitlab-mcp is running
**When** the PM selects any delivery management workflow
**Then** Shifu can execute the workflow using gitlab-mcp tools
**And** all GitLab operations follow the structured result format

---

## Epic 3: Dev, Architect & QA Agent Definitions

All remaining agent definitions are authored by copying and adapting their base BMAD agents, deployed via `bmad reinstall`, and invocable as slash commands. Tigress (Java), Viper (COBOL), Monkey (Python) mirror the BMAD dev agent. Oogway mirrors the BMAD architect agent. Mantis mirrors the BMAD QA agent. Each retains the full menu and workflow set of its base agent, adapted for mainframe modernisation context. All agents work from documents produced by Po — none access the spec layer directly. All agents have gitlab-mcp access for project management.

### Story 3.1: Dev Agent Workflows — Copy & Adapt from BMAD Dev

As a developer,
I want all BMAD dev agent workflows copied and adapted for the MM module,
So that the three dev agents (Tigress, Viper, Monkey) share a common set of MM-adapted dev workflows.

**Acceptance Criteria:**

**Given** the BMAD dev agent's workflows exist in the bmm module
**When** the developer copies them to `_bmad/mm/workflows/dev/`
**Then** all dev workflows are present (dev-story, code-review, and any other workflows from the BMAD dev menu)
**And** each workflow follows BMAD step-file architecture (workflow.md + steps/)

**Given** the copied dev workflows exist
**When** the developer adapts them for MM context
**Then** workflows reference Po's output documents (business markdown, architecture docs) as inputs instead of standard BMAD artifacts
**And** code generation workflows accept target language as a parameter driven by the agent's persona
**And** workflows declare `gitlab-mcp` access for progress updates and status tracking
**And** no workflow references `specdb-mcp` — agents consume documents, not the spec layer

**Given** the adapted dev workflows exist
**When** all three dev agents reference them
**Then** Tigress, Viper, and Monkey all point to the same `_bmad/mm/workflows/dev/` directory
**And** the agent persona (not the workflow) determines target language behaviour

### Story 3.2: Tigress Agent Definition (Dev — Java)

As an operator,
I want the Tigress agent fully authored as the Java code generation dev agent,
So that Tigress can be invoked via `/bmad-agent-mm-tigress` with the full dev agent menu adapted for Java modernisation.

**Acceptance Criteria:**

**Given** the BMAD dev agent definition exists
**When** the developer copies and adapts it to `_bmad/mm/agents/tigress.md`
**Then** it contains: Java code generation persona, spec layer consumption via Po's documents, mainframe modernisation context
**And** the menu mirrors the full BMAD dev agent menu (dev-story, code-review, chat, and all other items)
**And** menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
**And** it declares access to `gitlab-mcp` MCP server only

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-tigress`
**Then** Tigress loads with her Java persona, presents the full dev menu, and responds in character
**And** FR23, FR24, FR25 are addressable through the dev-story workflow

### Story 3.3: Viper Agent Definition (Dev — COBOL)

As an operator,
I want the Viper agent fully authored as the COBOL modernisation dev agent,
So that Viper can be invoked via `/bmad-agent-mm-viper` with the full dev agent menu adapted for COBOL modernisation.

**Acceptance Criteria:**

**Given** the BMAD dev agent definition exists
**When** the developer copies and adapts it to `_bmad/mm/agents/viper.md`
**Then** it contains: COBOL modernisation persona, works from Po's output documents, mainframe modernisation context
**And** the menu mirrors the full BMAD dev agent menu
**And** menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
**And** it declares access to `gitlab-mcp` MCP server only

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-viper`
**Then** Viper loads with her COBOL persona, presents the full dev menu, and responds in character

### Story 3.4: Monkey Agent Definition (Dev — Python)

As an operator,
I want the Monkey agent fully authored as the Python code generation dev agent,
So that Monkey can be invoked via `/bmad-agent-mm-monkey` with the full dev agent menu adapted for Python modernisation.

**Acceptance Criteria:**

**Given** the BMAD dev agent definition exists
**When** the developer copies and adapts it to `_bmad/mm/agents/monkey.md`
**Then** it contains: Python code generation persona, works from Po's output documents, mainframe modernisation context
**And** the menu mirrors the full BMAD dev agent menu
**And** menu items point to the adapted workflows in `_bmad/mm/workflows/dev/`
**And** it declares access to `gitlab-mcp` MCP server only

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-monkey`
**Then** Monkey loads with his Python persona, presents the full dev menu, and responds in character

### Story 3.5: Oogway Agent Definition (Architect)

As an operator,
I want the Oogway agent fully authored as the migration architect,
So that Oogway can be invoked via `/bmad-agent-mm-oogway` with the full architect agent menu adapted for mainframe migration.

**Acceptance Criteria:**

**Given** the BMAD architect agent definition and workflows exist
**When** the developer copies and adapts the agent to `_bmad/mm/agents/oogway.md`
**Then** it contains: mainframe migration architect persona, consumes Po's output documents for architecture decisions
**And** the menu mirrors the full BMAD architect agent menu (create-architecture, check-implementation-readiness, chat, and all other items)
**And** it declares access to `gitlab-mcp` MCP server only

**Given** the BMAD architect workflows exist
**When** the developer copies and adapts them to `_bmad/mm/workflows/architect/`
**Then** all architect workflows are present with step files adapted for MM context
**And** create-architecture workflow accepts Po's dependency maps and business rules documents as inputs
**And** the target language decision (FR21) is captured in the architecture workflow
**And** FR19, FR20, FR21, FR22 are addressable through the adapted workflows

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-oogway`
**Then** Oogway loads with his migration architect persona, presents the full architect menu, and responds in character

### Story 3.6: Mantis Agent Definition (QA)

As an operator,
I want the Mantis agent fully authored as the migration QA validator,
So that Mantis can be invoked via `/bmad-agent-mm-mantis` with the full QA agent menu adapted for migration validation.

**Acceptance Criteria:**

**Given** the BMAD QA agent definition and workflows exist
**When** the developer copies and adapts the agent to `_bmad/mm/agents/mantis.md`
**Then** it contains: migration validation persona, validates generated code against Po's business rules documents
**And** the menu mirrors the full BMAD QA agent menu (qa-generate-e2e-tests, chat, and all other items)
**And** it declares access to `gitlab-mcp` MCP server only

**Given** the BMAD QA workflows exist
**When** the developer copies and adapts them to `_bmad/mm/workflows/qa/`
**Then** all QA workflows are present with step files adapted for MM context
**And** validation workflows compare generated code against Po's business markdown and extracted rules documents
**And** QA workflows can trigger Epic sign-off via gitlab-mcp (FR55, FR56)
**And** FR26, FR27, FR28 are addressable through the adapted workflows

**Given** the MM module is installed via `bmad reinstall`
**When** the operator invokes `/bmad-agent-mm-mantis`
**Then** Mantis loads with his QA validation persona, presents the full QA menu, and responds in character
