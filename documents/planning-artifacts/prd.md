---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
inputDocuments:
  - docs/project_idea.md
  - docs/prd.md
  - docs/architecture.md
workflowType: 'prd'
classification:
  projectType: developer_tool
  domain: mainframe_modernisation
  complexity: high
  projectContext: greenfield
rebooted: true
rebootDate: '2026-03-06'
rebootReason: 'Restructured as BMAD expansion pack module (MM) with human-orchestrated workflows, independent agent deployability, and proper BMAD module conventions'
---

# Product Requirements Document — Mainframe Modernisation Agents

**Author:** Kamal
**Date:** 2026-03-06 (rebooted from 2026-03-01 original)
**Type:** BMAD Expansion Pack Module (`mm`) — locally deployed, greenfield

---

## Executive Summary

Mainframe Modernisation Agents is a **BMAD Expansion Pack** — a self-contained module that installs into `_bmad/mm/` alongside existing BMAD modules (core, bmm) to add mainframe modernisation capability to any BMAD-compatible IDE.

The expansion pack addresses a specific industry failure: traditional agile assumes you understand what you're building. COBOL estates break that assumption entirely — no documentation, no living institutional knowledge, systems that have accreted business rules over decades that nobody fully understands. The industry has a 70% project failure rate applying standard agile to mainframe modernisation.

This module delivers a reimagined SDLC for COBOL modernisation through:

- **One new BMAD agent (Po)** — the centrepiece analysis agent, built from scratch with multiple independent workflows for structural analysis, dependency mapping, and business rule extraction
- **Existing BMAD agents used as-is** — PM (Shifu), SM (Shifu) require no modification, only access to the new MCP servers
- **Specialised MM agents** — Architect (Tigress), Auditor (Oogway), QA (Tai Lung), and three Dev variants for Java (Crane), Python (Monkey), and COBOL (Viper) target code generation
- **Five MCP servers** — the capability layer providing COBOL parsing, spec layer CRUD, middleware knowledge, JCL parsing, and GitLab integration

### Human-Orchestrated, Not Automated

Unlike a traditional CI/CD pipeline, this is **human-orchestrated**. The analyst decides what to run, when, and on which module. Each agent presents a menu of independently runnable workflows — just like existing BMAD agents. The recommended pipeline order exists as guidance, not enforcement:

```
Po (Analyse Structure) --> Po (Map Dependencies) --> Po (Extract Business Rules)
    --> Tigress (Migration Architecture) --> Shifu (GitLab Project Setup)
    --> Crane/Viper/Monkey (Code Generation) --> Oogway (Code Review) --> Tai Lung (QA Validation)
```

Each workflow can be run, re-run, or skipped at the operator's discretion. The spec layer (SQLite) carries context between workflows — the operator carries intent.

### What Makes This Special

**A BMAD module, not a standalone tool** — Installs into `_bmad/mm/`, deploys via the standard BMAD installer, and appears as slash commands alongside existing agents. No separate tooling, no separate workflow.

**SQLite spec layer as the shared backbone** — `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` — the first open-source formalisation of COBOL program semantics as a relational schema. Every agent consumes structured data, not unstructured markdown.

**Build incrementally, use immediately** — Each MCP server and each agent is independently deployable. After deploying Crane, you can invoke `/bmad-agent-mm-crane` and use it — you don't need the full suite to start working.

**Existing BMAD agents gain new superpowers** — The PM and SM agents you already use get access to COBOL analysis tools and GitLab integration through the MCP servers. Specialised MM agents handle architecture (Tigress), auditing (Oogway), QA (Tai Lung), and code generation (Crane, Viper, Monkey).

---

## Expansion Pack Architecture

### Module Identity

| Property | Value |
|---|---|
| Module name | `mm` |
| Module location | `_bmad/mm/` |
| Full name | Mainframe Modernisation |
| Installs alongside | `core` (no BMM dependency) |
| Installer | Standard BMAD reinstall |

### Module Structure

The MM module is a standalone BMAD expansion pack built on BMAD core. Each agent has its own complete definition and workflows — no dependency on BMM.

```
_bmad/mm/
├── config.yaml                    # MM module configuration
├── module-help.csv                # Workflow/agent registry (required by installer)
├── agents/
│   ├── po.md                      # NEW — Analysis agent (structural, deps, business rules)
│   ├── tigress.md                 # Architect — migration architecture
│   ├── crane.md                   # Dev (Java) — code generation from spec layer
│   ├── viper.md                   # Dev (COBOL) — COBOL modernisation
│   ├── monkey.md                  # Dev (Python) — code generation from spec layer
│   ├── shifu.md                   # PM + SM — delivery orchestrator
│   ├── oogway.md                  # Auditor — PRD validation, code review, implementation readiness, retrospective
│   └── tai-lung.md                # QA — migration validation
├── workflows/
│   ├── po/
│   │   ├── analyse-structure/
│   │   │   ├── workflow.md
│   │   │   └── steps/
│   │   │       ├── step-01-init.md
│   │   │       ├── step-02-load-source.md
│   │   │       ├── step-03-static-prepass.md
│   │   │       ├── step-04-semantic-clustering.md
│   │   │       ├── step-05-ai-analysis.md
│   │   │       ├── step-06-review-gate.md
│   │   │       └── step-07-write-to-spec.md
│   │   ├── map-dependencies/
│   │   │   ├── workflow.md
│   │   │   └── steps/
│   │   │       ├── step-01-init.md
│   │   │       ├── step-02-regex-extraction.md
│   │   │       ├── step-03-build-graph.md
│   │   │       ├── step-04-ai-analysis.md
│   │   │       ├── step-05-subsystem-detection.md
│   │   │       └── step-06-migration-order.md
│   │   ├── extract-business-rules/
│   │   │   ├── workflow.md
│   │   │   └── steps/
│   │   │       ├── step-01-init.md
│   │   │       ├── step-02-consume-analysis.md
│   │   │       ├── step-03-extract-rules.md
│   │   │       ├── step-04-business-markdown.md
│   │   │       ├── step-05-review-gate.md
│   │   │       └── step-06-populate-spec-layer.md
│   │   └── view-flags/
│   │       └── workflow.md
│   ├── dev/
│   │   ├── dev-story/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   └── code-review/
│   │       ├── workflow.md
│   │       └── steps/...
│   ├── architect/
│   │   ├── create-architecture/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   └── check-implementation-readiness/
│   │       ├── workflow.md
│   │       └── steps/...
│   ├── pm/
│   │   ├── create-epics-and-stories/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   ├── sprint-planning/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   ├── create-story/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   ├── sprint-status/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   ├── correct-course/
│   │   │   ├── workflow.md
│   │   │   └── steps/...
│   │   └── retrospective/
│   │       ├── workflow.md
│   │       └── steps/...
│   └── qa/
│       └── qa-generate-e2e-tests/
│           ├── workflow.md
│           └── steps/...
├── data/
│   ├── glossary-template.md       # Empty glossary for new engagements
│   └── macro-template.md          # Empty Delta macro doc template
└── teams/
    └── default-party.csv          # MM agent party mode roster
```

### Deployed Files (Generated by BMAD Installer)

After `bmad reinstall`:

```
.claude/commands/
├── bmad-agent-mm-po.md                    # Po agent slash command
├── bmad-agent-mm-tigress.md               # Tigress agent slash command (Architect)
├── bmad-agent-mm-crane.md                 # Crane agent slash command (Dev Java)
├── bmad-agent-mm-viper.md                 # Viper agent slash command (Dev COBOL)
├── bmad-agent-mm-monkey.md                # Monkey agent slash command (Dev Python)
├── bmad-agent-mm-shifu.md                 # Shifu agent slash command (PM + SM)
├── bmad-agent-mm-oogway.md                # Oogway agent slash command (Auditor)
├── bmad-agent-mm-tai-lung.md              # Tai Lung agent slash command (QA)
├── bmad-mm-analyse-structure.md           # Po workflow: structural analysis
├── bmad-mm-map-dependencies.md            # Po workflow: dependency mapping
├── bmad-mm-extract-business-rules.md      # Po workflow: business rules
├── bmad-mm-dev-story.md                   # Dev workflow: story implementation
├── bmad-mm-code-review.md                 # Dev workflow: code review
├── bmad-mm-create-architecture.md         # Architect workflow
├── bmad-mm-create-epics-and-stories.md    # PM workflow: epics & stories
├── bmad-mm-sprint-planning.md             # SM workflow: sprint planning
├── bmad-mm-sprint-status.md               # SM workflow: sprint status
├── bmad-mm-qa-generate-e2e-tests.md       # QA workflow: test generation
└── ...

.github/agents/
├── bmad-agent-mm-po.agent.md
├── bmad-agent-mm-tigress.agent.md
├── bmad-agent-mm-crane.agent.md
├── bmad-agent-mm-viper.agent.md
├── bmad-agent-mm-monkey.agent.md
├── bmad-agent-mm-shifu.agent.md
├── bmad-agent-mm-oogway.agent.md
├── bmad-agent-mm-tai-lung.agent.md
└── ...
```

### Agent Roster

| Character | Agent Type | Based On | What the MM Agent Adds |
|---|---|---|---|
| **Po** | Analysis Agent | **NEW** — built from scratch | Centrepiece. Multiple workflows: structural analysis, dependency mapping, business rule extraction |
| **Tigress** | Architect | Built on BMAD core (architect pattern) | Migration architecture persona, spec layer awareness, `specdb-mcp` + `gitlab-mcp` MCP access. Own workflows: create-architecture |
| **Shifu** | PM + SM | Built on BMAD core (PM + SM patterns combined) | Combined PM/SM persona, GitLab-native project management, migration status tracking, `gitlab-mcp` + `specdb-mcp` MCP access. Own workflows: create-epics-and-stories, sprint-planning, create-story, sprint-status, correct-course |
| **Oogway** | Auditor | Built on BMAD core (quality gate pattern) | Quality gate guardian — validates PRDs, architecture, code, and sprint outcomes. `specdb-mcp` + `gitlab-mcp` MCP access. Own workflows: validate-prd, check-implementation-readiness, code-review, retrospective |
| **Crane** | Dev (Java) | Built on BMAD core (dev pattern) | Java code generation persona, spec layer consumption, `specdb-mcp` + `cobol-parser-mcp` MCP access. Own workflows: dev-story |
| **Viper** | Dev (COBOL) | Built on BMAD core (dev pattern) | COBOL modernisation persona, `specdb-mcp` + `cobol-parser-mcp` MCP access. Own workflows: dev-story |
| **Monkey** | Dev (Python) | Built on BMAD core (dev pattern) | Python code generation persona, spec layer consumption, `specdb-mcp` + `cobol-parser-mcp` MCP access. Own workflows: dev-story |
| **Tai Lung** | QA | Built on BMAD core (QA pattern) | Migration validation persona (original COBOL vs generated code), `specdb-mcp` + `gitlab-mcp` MCP access. Own workflows: qa-generate-e2e-tests |

### MCP Servers (Capability Layer)

MCP servers live at the **project root** as Python packages, not inside `_bmad/`. They are infrastructure, not methodology.

```
<project-root>/
├── mcp-servers/
│   ├── cobol_parser_mcp/      # COBOL static parsing, call graph, complexity
│   ├── specdb_mcp/            # SQLite spec layer CRUD
│   ├── delta_macros_mcp/      # Middleware knowledge base
│   ├── jcl_parser_mcp/        # JCL job/step/dataset parsing
│   ├── gitlab_mcp/            # GitLab API integration
│   └── shared/                # config_loader.py, common utilities
├── pyproject.toml             # Poetry monorepo — all servers
├── poetry.lock
└── tests/
    ├── cobol_parser_mcp/
    ├── specdb_mcp/
    ├── delta_macros_mcp/
    ├── jcl_parser_mcp/
    └── gitlab_mcp/
```

Each MCP server is self-contained with its own `config.yaml` (non-secret settings), `.env` (secrets — gitignored), `.env.example` (committed template), and `log/` directory. Servers load config via `shared/config_loader.py`.


| MCP Server | Purpose | Tools Exposed |
|---|---|---|
| `cobol-parser-mcp` | COBOL static pre-pass: parsing, call graph, complexity scoring | `parse_module`, `extract_call_graph`, `score_complexity`, `detect_antipatterns` |
| `specdb-mcp` | SQLite spec layer CRUD — shared IR across all agents | `read_spec`, `write_spec`, `query_spec`, `init_schema` |
| `delta-macros-mcp` | Client-specific macro and middleware knowledge | `get_macro`, `search_macros`, `list_categories`, `add_macro` |
| `jcl-parser-mcp` | JCL parsing, job steps, dataset allocations | `parse_jcl`, `extract_job_graph`, `list_datasets`, `get_job_steps` |
| `gitlab-mcp` | Full GitLab integration for all agents | `create_epic`, `create_issue`, `apply_label`, `remove_label`, `create_milestone`, `assign_to_milestone`, `create_board`, `add_comment`, `update_readme`, `close_epic`, `update_issue_status` |

---

## Build Strategy

### Principle: Build MCP Servers First, Then Agents One by One

Each component is independently deployable and immediately usable after deployment.

### Build Order

```
Phase 1 — Foundation (installer validation + project management):
  1. Initial setup       # MM module scaffolding, config.yaml, module-help.csv
  2. gitlab-mcp          # GitLab MCP server
  3. Shifu               # PM + SM agent — GitLab project setup, sprint management
  Validation: MM module installs correctly via BMAD installer on both GitHub Copilot and Claude
  Result: Shifu can connect to GitLab, create projects, manage epics/stories/sprints

Phase 2 — Remaining Agents:
  4. Tigress             # Architect — migration architecture
  5. Oogway              # Auditor — PRD validation, code review, implementation readiness, retrospective
  6. Crane               # Dev (Java) — code generation from spec layer
  7. Viper               # Dev (COBOL) — COBOL modernisation
  8. Monkey              # Dev (Python) — code generation from spec layer
  9. Tai Lung            # QA — migration validation
  Result: All agents operational with GitLab connectivity via gitlab-mcp

Phase 3 — Analysis Agent + MCP Servers:
  9. specdb-mcp          # SQLite spec layer CRUD (Po depends on this)
  10. delta-macros-mcp   # Middleware knowledge base
  11. cobol-parser-mcp   # COBOL static parsing engine
  12. jcl-parser-mcp     # JCL parsing
  13. Po                 # NEW analysis agent — the big build
  14. End-to-end demo    # COBOL BlackJack modernisation
  Result: Full pipeline operational — analyse, architect, develop, test, manage
```

**Why Shifu first (Phase 1)?** It validates the expansion pack installer pattern on both GitHub Copilot and Claude. If `_bmad/mm/agents/shifu.md` deploys correctly via `bmad reinstall` and appears as `/bmad-agent-mm-shifu`, the module structure is proven. Pairing it with `gitlab-mcp` delivers immediate value — Shifu can manage the project in GitLab from day one.

---

## Success Criteria

### User Success

**Alex (COBOL Factory Analyst — primary pipeline operator):**
- Po structural analysis on any COBOL module: **< 15 minutes** for static pre-pass
- AI analysis accuracy on first pass validated by COBOL expert: **> 90%**
- Programs tractably analysable per sprint: **10-20** (vs 1-2 manually)
- Alex stays in the expert/reviewer seat — every agent output is reviewed, not built from scratch

**Priya (Enterprise Architect — primary output consumer):**
- Po dependency graph surfaces subsystem boundaries and migration order without manual cross-referencing
- Spec layer is directly consumable by Oogway — no manual translation step
- Full estate structural picture available before any migration commitment

**Claire (Business Validator — Po output consumer):**
- Business rules correctly extracted on first Po pass: **> 85%**
- Every business rule traceable: Po markdown -> spec layer -> Crane output -> Tai Lung validation

### Business Success

| Horizon | Objective |
|---|---|
| **3 months** | BlackJack pipeline runs end-to-end: Po -> Tigress -> Shifu -> Crane/Viper/Monkey -> Oogway -> Tai Lung. Full demo in a single session. |
| **6 months** | Pipeline configurable for a real client estate — glossary loaded, `delta-macros-mcp` populated, first real COBOL program analysed |
| **12 months** | At least one complete application (all modules) processed through to verified GitLab Epics closed |

### Technical Success

- All agents produce correct, well-formed outputs at their stage
- SQLite spec layer fully populated after Po — all `spec_*` tables have data, queryable by downstream agents
- `delta-macros-mcp` resolves macro lookups correctly for all agents
- Each agent is independently invocable via BMAD slash commands
- Pipeline is re-runnable: re-processing a module updates the spec layer without requiring a full reset
- MM module installs cleanly alongside existing BMM module via `bmad reinstall`

---

## User Journeys

### Journey 1 — Alex Analyses a COBOL Module (Human-Orchestrated)

Alex has received `PAYROLL-CALC.cbl` — a 4,200-line COBOL program last modified in 1994.

He invokes `/bmad-agent-mm-po` and sees Po's menu:

```
[1] Analyse COBOL Module Structure
[2] Map Cross-Module Dependencies
[3] Extract Business Rules
[4] View Consolidated Flags
[5] Chat with Po
```

He picks **[1] Analyse COBOL Module Structure**. The workflow runs through its steps: loads the source, runs the static pre-pass (call graph of 47 paragraphs, complexity: High, 2 GOTOs flagged), then AI semantic clustering and plain-English descriptions. Alex reviews, corrects one misidentification, approves the rest. The workflow writes results to the spec layer.

Later, after analysing several modules, he picks **[2] Map Cross-Module Dependencies** to build the cross-program graph. Then **[3] Extract Business Rules** per module. Each workflow is a separate session, run when Alex decides.

**The moment that matters:** Alex chose what to run and when. The workflows guided him through multi-step processes with review gates, but he drove the sequence.

*Requirements: FR1-FR8, FR14-FR18*

### Journey 2 — Alex Hits an Unknown Delta Macro

During Po's structural analysis of `ACCOUNTS-BATCH.cbl`, the agent calls `delta-macros-mcp` for `DLTM-ACCT-LOCK`. Not found.

Po flags the unknown macro, marks the affected paragraph, and continues. Alex writes a markdown file describing the macro, adds it via `add_macro`, and re-runs the analysis on just the affected cluster.

**The moment that matters:** The workflow flagged what it didn't know, let Alex fill the gap, and let him re-run only what was affected.

*Requirements: FR8, FR31, FR39*

### Journey 3 — Priya Designs Migration Architecture

Priya opens the Migration Architect agent (Tigress). Because `specdb-mcp` is now available, Tigress can query the spec layer directly. Po's dependency map shows three subsystems. `spec_entities` reveals `TAX-BAND` as a shared service candidate.

Tigress produces a target Java architecture following the seam lines Po surfaced.

**The moment that matters:** The Architect agent gained mainframe migration capability through MCP servers and spec layer awareness.

*Requirements: FR9-FR13, FR19-FR22*

### Journey 4 — First Expansion Pack Install

A new engagement. Alex installs the MM expansion pack via `bmad reinstall`. The agents appear as slash commands. He initialises the SQLite schema via `specdb-mcp init_schema`. He creates a glossary, points `delta-macros-mcp` at an empty macro library. 45 minutes to pipeline-ready.

**The moment that matters:** Standard BMAD install. Two inputs — glossary + macro library — contextualise the pipeline for any COBOL estate.

*Requirements: FR29-FR32*

---

## Domain-Specific Requirements

### LLM Reliability

Agent outputs depend on probabilistic LLM responses. The pipeline must surface confidence and flag uncertainty explicitly — AI output is never treated as authoritative without analyst review. Agents must indicate unresolved or low-confidence analysis in their output; workflows include explicit review gate steps before spec layer writes.

### COBOL Dialect Coverage

COBOL is not a single language. Po must handle or explicitly flag:
- IBM Enterprise COBOL and VS COBOL II syntax variants
- CICS transaction constructs (`EXEC CICS ... END-EXEC`)
- DB2 embedded SQL (`EXEC SQL ... END-EXEC`)
- Client-specific Delta macros (resolved via `delta-macros-mcp`)

Silent misparsing of a dialect variant produces a corrupt spec layer and a wrong architecture. Unrecognised constructs must be flagged, not ignored.

### Pipeline Reproducibility

Running any workflow twice on the same input must produce equivalent SQLite spec layer output. LLM variance in intermediate markdown is acceptable; variance in the spec layer is not. Spec layer writes must be idempotent — re-running a module updates records rather than creating duplicates or contradictions.

### Data Locality

Client COBOL source code and extracted business rules are confidential. No source code, business rules, or extracted spec data may leave the local environment. All MCP servers run locally via STDIO transport.

---

## Innovation & Novel Patterns

### The SDLC as a BMAD Module

Traditional modernisation methodologies are documents. This project packages a complete modernisation SDLC as a BMAD module — installable, versionable, and executable through standard BMAD agent menus. The process methodology *is* the software.

### SQLite as a Structured Intermediate Representation for COBOL

No existing commercial or open-source COBOL tool implements a queryable, structured IR between analysis and implementation. `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` — the first open-source formalisation of COBOL program semantics as a relational schema.

### Existing Agents Gain Domain Capability Through MCP Servers

The PM, Architect, QA, and SM agents already exist in BMAD. By adding MCP servers (specdb, gitlab, cobol-parser), these agents gain mainframe modernisation capability without any agent modification. This establishes the pattern for how BMAD expansion packs extend the platform.

### Local MCP Server as Domain Knowledge Injection

`delta-macros-mcp` is a novel pattern: a locally-running MCP server that gives every agent on-demand access to client-specific institutional knowledge without model fine-tuning or prompt stuffing. Knowledge is maintained as human-readable markdown files, updated incrementally.

### Market Context

| Tool | What They Do | What's Missing |
|---|---|---|
| IBM watsonx Code Assistant | AI-assisted COBOL -> Java conversion | No structured IR; skips understanding; cloud-locked |
| AWS Mainframe Modernisation | Automated refactoring and replatforming | No business rule extraction; no compliance artefacts |
| Micro Focus / OpenText | Modernisation tooling + services | Tool-centric, not process-enforcing; no open IR |
| Microsoft/Bankdata (open-source) | COBOL parsing and analysis | No business rule extraction; no delivery integration; no IR |

---

## Functional Requirements

### COBOL Structural Analysis (Po — Analyse Structure Workflow)

- **FR1:** Analyst can initiate structural analysis of a COBOL module and receive a paragraph call graph
- **FR2:** Analyst can view a complexity score (Low/Medium/High) for any analysed COBOL module
- **FR3:** Analyst can view anti-patterns detected in a COBOL module (GOTOs, nested PERFORMs, REDEFINES, etc.)
- **FR4:** Analyst can view extracted COPY, CALL, SQL, CICS, and Delta macro references per module
- **FR5:** Analyst can view AI-generated semantic cluster groupings for a module's paragraphs
- **FR6:** Analyst can view plain-English descriptions for each semantic cluster
- **FR7:** Analyst can review, correct, and approve AI analysis outputs before they are written to the spec layer
- **FR8:** Analyst can view a warning when Po encounters an unrecognised COBOL construct or unknown Delta macro

### Cross-Module Dependency Mapping (Po — Map Dependencies Workflow)

- **FR9:** Analyst can initiate cross-module dependency analysis across all COBOL modules in scope
- **FR10:** Architect can view a Mermaid dependency diagram showing relationships between all modules
- **FR11:** Architect can view detected subsystem groupings emerging from the dependency structure
- **FR12:** Architect can view a recommended migration order based on module dependencies
- **FR13:** Analyst can view detected circular dependencies and dead code across modules

### Business Rule Extraction & Spec Layer (Po — Extract Business Rules Workflow)

- **FR14:** Analyst can initiate business rule extraction for a COBOL module using structural analysis and dependency outputs
- **FR15:** Business Validator can view plain-English business markdown for any module (purpose, use cases, business rules, data entities with glossary names)
- **FR16:** Business Validator can validate each extracted business rule as confirmed, corrected, or rejected
- **FR17:** System writes approved business rules, entities, operations, and data flows to the SQLite spec layer
- **FR18:** Analyst can re-run business rule extraction on a module and have the spec layer update idempotently without duplicates

### Migration Architecture (Tigress — Migration Architect)

- **FR19:** Architect can initiate migration architecture generation from the populated spec layer
- **FR20:** Architect can view a target architecture document mapping COBOL subsystems to target-language services
- **FR21:** Architect can specify the target language as an input to Tigress
- **FR22:** Architect can review and modify the generated architecture before it is finalised

### Code Generation (Crane / Viper / Monkey — Dev Agents)

- **FR23:** Developer can initiate target-language code generation for a module from the spec layer and architecture
- **FR24:** Developer can view generated target-language code for each COBOL module
- **FR25:** Developer can regenerate code for a specific module without affecting other modules

### QA Validation (Tai Lung — QA Agent)

- **FR26:** QA can initiate validation of generated code against spec layer business rules
- **FR27:** QA can view a validation report showing which business rules are confirmed, partially covered, or missing in the generated code
- **FR28:** QA can flag a module as requiring rework before sign-off

### Pipeline Configuration & Infrastructure

- **FR29:** Operator can initialise the SQLite spec layer schema with a single command via `specdb-mcp`
- **FR30:** Analyst can configure a client-specific glossary mapping COBOL field names to business terms
- **FR31:** Analyst can add a new macro definition to `delta-macros-mcp` without restarting the pipeline
- **FR32:** Operator can install the MM expansion pack into any BMAD-compatible IDE via standard `bmad reinstall`
- **FR33:** Analyst can re-run any individual workflow on a specific module without restarting the full pipeline
- **FR34:** Analyst can view a consolidated list of all unresolved constructs and macros flagged across workflow runs

### COBOL Dialect & Construct Coverage

- **FR35:** System can parse and analyse IBM Enterprise COBOL and COBOL-85 modules
- **FR36:** System can detect and flag CICS transaction constructs within a COBOL module
- **FR37:** System can detect and flag DB2 embedded SQL constructs within a COBOL module
- **FR38:** System can parse COPY statements and resolve referenced copybooks
- **FR39:** All agents can resolve client-specific Delta macro references via `delta-macros-mcp` at analysis time

### GitLab Project Management (Shifu — Existing BMAD PM + SM via gitlab-mcp)

**Project Initialisation**

- **FR40:** PM can initialise a GitLab project with standard label taxonomy: pipeline stage labels (`Po-Analysis-Complete`, `Architecture-Complete`, `Code-Generated`, `QA-Complete`), complexity labels (`Complexity::Low`, `Complexity::Medium`, `Complexity::High`), and status labels (`In-Analysis`, `Awaiting-Review`, `In-Migration`, `Blocked`, `Done`)
- **FR41:** PM can create a standard milestone structure per engagement phase in GitLab
- **FR42:** PM can create a GitLab issue board configured with columns mapped to pipeline stages

**Module Lifecycle Tracking**

- **FR43:** Each COBOL module has a dedicated GitLab Issue tracking its complete pipeline lifecycle from analysis through QA sign-off
- **FR44:** Any agent can apply the appropriate stage completion label to a module's GitLab Issue upon completing its stage
- **FR45:** Any agent can transition a module Issue to `Awaiting-Review` status when its stage output requires analyst approval
- **FR46:** Analyst can close the review gate on a module Issue and transition it to the next pipeline stage

**Sprint & Iteration Planning**

- **FR47:** PM can create GitLab sprint milestones scoped to a specific set of modules based on dependency analysis migration order
- **FR48:** PM can assign module Issues to sprint milestones, respecting subsystem dependencies
- **FR49:** PM can view a milestone burndown showing open vs closed module Issues within a sprint

**Progress Reporting**

- **FR50:** Any agent can post a structured progress comment to a module's GitLab Issue when it completes a stage
- **FR51:** The GitLab project README is updated by any agent that changes module status
- **FR52:** Client Sponsor can view a README dashboard showing total modules, modules per pipeline stage, modules blocked, and Epics signed off
- **FR53:** PM can generate a milestone summary comment on any Epic showing sprint progress and outstanding items

**Review Gates & Sign-off**

- **FR54:** Business Validator can formally sign off on Po's business markdown by closing the `Awaiting-Review` gate on a module Issue
- **FR55:** QA can sign off on an Epic, triggering Epic completion in GitLab with a validation summary comment
- **FR56:** QA can formally close an Epic when all module Issues within it are `QA-Complete`

---

## Non-Functional Requirements

### Performance

- **NFR1:** Po Phase 1 static pre-pass completes on any single COBOL module within **15 minutes** on standard developer hardware
- **NFR2:** `cobol-parser-mcp` parsing tools return results within **30 seconds** for any module up to 5,000 lines
- **NFR3:** `specdb-mcp` read and write operations complete within **2 seconds** for any single spec layer record or query
- **NFR4:** `delta-macros-mcp` macro lookups resolve within **1 second** per call
- **NFR5:** `gitlab-mcp` operations complete within **10 seconds** per API call under normal network conditions

### Security & Data Privacy

- **NFR6:** No COBOL source code, business rules, or extracted spec data is transmitted outside the local environment by any agent or MCP server
- **NFR7:** Where remote LLM API calls are used, source code is scoped to the minimum required context
- **NFR8:** GitLab credentials are stored via `GITLAB_TOKEN` environment variable — never hardcoded in agent definitions or MCP server config files
- **NFR9:** `delta-macros-mcp` macro library is stored locally and not synchronised to any external service

### Reliability & Reproducibility

- **NFR10:** Running any workflow twice on the same input produces equivalent SQLite spec layer output — spec layer writes are idempotent
- **NFR11:** Any agent encountering an unrecognised construct, unknown macro, or LLM error fails with an explicit, actionable error message — silent failures are not permitted
- **NFR12:** A failed workflow run does not corrupt existing spec layer records — partial writes roll back or are clearly flagged as incomplete
- **NFR13:** All MCP servers remain operational across agent session restarts without requiring full reinitialisation

### Integration & Compatibility

- **NFR14:** The MM expansion pack installs and operates correctly in any BMAD-compatible IDE (Claude Code and Cursor as minimum baseline)
- **NFR15:** All MCP servers conform to the MCP protocol specification — no proprietary extensions that break cross-IDE compatibility
- **NFR16:** `gitlab-mcp` supports GitLab Cloud and self-hosted GitLab instances (API v4)
- **NFR17:** The SQLite spec layer schema is versioned — schema migrations do not break existing data or require manual intervention

### Maintainability

- **NFR18:** Each BMAD agent definition is independently updatable without requiring changes to any other agent or MCP server
- **NFR19:** Each MCP server exposes a clearly defined, versioned tool interface — adding new tools does not break existing tool calls
- **NFR20:** Glossary file format and macro library format use human-readable, plain-text markup — no binary formats or proprietary schemas
- **NFR21:** The BlackJack corpus serves as the regression test baseline — any change to an MCP server is validated against BlackJack end-to-end before release

---

## Product Scope & Phased Development

### MVP — BlackJack End-to-End

**Approach:** Prove the complete pipeline works end-to-end on the BlackJack COBOL corpus (8 modules, 3 copybooks) before any client engagement.

**Must-Have:**
- 5 MCP servers fully operational
- Po agent with 3 core workflows (analyse structure, map dependencies, extract business rules)
- 4 specialised agents: Tigress (Architect), Oogway (Auditor), Crane (Dev Java), Tai Lung (QA), plus Viper (Dev COBOL) and Monkey (Dev Python)
- Existing BMAD agents (PM, SM) working with MCP servers
- MM module installable via `bmad reinstall`

### Phase 2 — Expansion Pack Maturity

- Parallel Po processing for large estates
- Automated complexity-based sprint sizing
- AI-assisted glossary suggestion (Po proposes, analyst confirms)
- Client engagement playbook template

### Phase 3 — BMAD Ecosystem

- RPG and PL/I language support
- Behavioural equivalence testing framework in Tai Lung
- JIRA / Azure DevOps integration (post-GitLab)
- Factory metrics dashboard across engagements

### Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| **LLM reliability** — inaccurate COBOL analysis | Corrupt spec layer | Expert review gate steps in every Po workflow |
| **COBOL dialect gaps** — parser misparses variant syntax | Silent errors propagate | Unrecognised constructs flagged, not ignored; BlackJack regression |
| **BMAD module pattern untested** — installer doesn't pick up MM module | Can't deploy agents | Tigress first (Phase 2) — validates pattern before building the rest |
| **Quality gaps between agents** — artifacts pass without proper review | Inconsistent outputs | Oogway as dedicated Auditor validates all artifacts at every gate |
| **MCP server scope creep** | MVP delayed | Hard boundary: 5 servers, defined tool lists; no additions without PRD change |

---

## Reference

- [Microsoft + Bankdata Legacy Modernisation Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)
- [Bankdata announcement](https://www.bankdata.dk/about/news/microsoft-and-bankdata-launch-open-source-ai-framework-for-modernizing-legacy-systems)
- [COBOL BlackJack — demo application for end-to-end modernisation](https://github.com/kamalkantsingh10/cobol-blackjack)
- Original project idea: `docs/project_idea.md`
- Previous architecture: `docs/architecture.md`
