---
status: draft
author: Kamal
date: '2026-03-06'
description: 'Detailed specification of how Po analyses COBOL modules — the core analytical pipeline of the MM expansion pack'
inputDocuments:
  - documents/planning-artifacts/prd.md
  - documents/planning-artifacts/architecture.md
---

# Po Analysis Pipeline — How COBOL Analysis Works

## Overview

Po is the centrepiece agent of the MM expansion pack. It is the only agent that interacts with the spec layer (SQLite) directly. Every other agent in the pipeline — Oogway (Architect), Tigress/Viper/Monkey (Dev), Mantis (QA), Shifu (PM+SM) — consumes documents that Po produces. Po is where institutional knowledge gets extracted from undocumented COBOL estates and formalised into structured, queryable data.

Po has three independent workflows, each runnable on its own, at the analyst's discretion:

| Workflow | Scope | Input | Output |
|----------|-------|-------|--------|
| **Analyse Structure** | Single module | One COBOL source file | Call graph, complexity, clusters, anti-patterns, external refs, macro calls |
| **Map Dependencies** | Entire estate | All analysed modules in spec layer | Cross-module graph, subsystems, migration order |
| **Extract Business Rules** | Single module | Structural analysis + glossary | Business entities, operations, rules, data flows |

The recommended order is Analyse Structure (per module, repeated) → Map Dependencies (once, estate-wide) → Extract Business Rules (per module, repeated). But the analyst decides what to run and when. Each workflow reads from and writes to the spec layer — the SQLite database is the message bus between workflows.

### The Two-Phase Analysis Pattern

Every Po workflow follows a fundamental pattern:

1. **Deterministic phase** — Static parsing via `cobol-parser-mcp`. Same input always produces same output. Regex and Lark grammar. No AI involvement. This is the trustworthy foundation.

2. **Probabilistic phase** — AI analysis via the LLM. Semantic clustering, plain-English descriptions, business rule extraction. This is where intelligence happens, but also where errors occur.

The boundary between these phases is explicit and architecturally enforced. The deterministic phase populates the spec layer with facts. The probabilistic phase proposes interpretations. The analyst reviews and approves interpretations before they are persisted. The spec layer only ever contains analyst-approved data.

### Spec Layer — The Shared Data Backbone

The spec layer is a SQLite database with 12 tables across 4 layers:

| Layer | Tables | Written By |
|-------|--------|------------|
| **Structure** | `cobol_files`, `paragraphs`, `paragraph_calls`, `clusters`, `antipatterns`, `external_references` | Analyse Structure workflow |
| **Macros** | `macro_calls` | Analyse Structure workflow |
| **Dependencies** | `dependencies`, `subsystems` | Map Dependencies workflow |
| **Business Rules** | `spec_entities`, `spec_operations`, `spec_rules`, `spec_data_flows` | Extract Business Rules workflow |

All tables are keyed on `program_name` (the COBOL PROGRAM-ID verbatim, uppercase with hyphens — e.g., `PAYROLL-CALC`). All writes are idempotent (INSERT OR IGNORE + UPDATE). All timestamps are ISO 8601 UTC. Re-running any workflow on the same module updates existing records without creating duplicates.

---

## Workflow 1: Analyse Structure

### Purpose

Take a single COBOL source file and produce a complete structural understanding: what paragraphs exist, how they call each other, how complex the program is, what anti-patterns are present, what external systems it references, and what functional clusters emerge from the structure.

### When to Run

- First workflow run on any new COBOL module
- Re-run after analyst corrections or source code updates
- Can be run on modules in any order — no dependencies between modules at this stage

### Input

- One COBOL source file (e.g., `PAYROLL-CALC.cbl`)
- Glossary file (for field name context, optional at this stage)
- Delta macro library (for macro resolution)

### Step-by-Step Flow

#### Step 1: Initialisation

The analyst invokes Po and selects "Analyse COBOL Module Structure" from the menu. Po loads the MM config (`_bmad/mm/config.yaml`) to resolve paths: source directories, glossary location, macro library path, spec layer database path.

The analyst selects or provides the path to the COBOL source file. Po verifies the file exists and is readable.

**Writes to spec layer:** Nothing yet.

#### Step 2: Load Source

Po reads the complete COBOL source file and performs initial structural validation:

- Identify the four COBOL divisions: IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE
- Extract the PROGRAM-ID from IDENTIFICATION DIVISION — this becomes the canonical `program_name` used everywhere
- Verify the file is parseable COBOL (basic syntax validation)
- Count total lines, identify division boundaries

If the file is not valid COBOL (missing divisions, unrecognisable syntax), Po halts with an explicit error and flags. No partial analysis proceeds.

**Writes to spec layer:** `cobol_files` record created with `program_name`, `source_path`, `line_count`, `divisions_found`, `analysis_status = 'in_progress'`.

#### Step 3: Static Pre-pass (Deterministic — cobol-parser-mcp)

This is the most critical step and is entirely deterministic. The `cobol-parser-mcp` tools do all the heavy lifting. No AI is involved. Same input always produces same output.

**3a. Paragraph Extraction**

Scan the PROCEDURE DIVISION for all paragraph headers. For each paragraph:
- Paragraph name (e.g., `3100-CALC-TAX`)
- Start line number
- End line number (determined by the next paragraph header or end of division)
- Line count

Tool: `cobol-parser-mcp → parse_module`

**3b. Paragraph Call Graph**

Scan every PERFORM statement in the PROCEDURE DIVISION. Build the graph:
- Caller paragraph → callee paragraph
- Call type: PERFORM (normal), PERFORM THRU (range), GO TO (anti-pattern)
- Detect paragraphs that are never called (potential dead code within the module)
- Detect paragraphs that call themselves (recursion — rare in COBOL, always flagged)

Example output:
```
0000-MAIN-LOGIC  →  1000-INIT           (PERFORM)
0000-MAIN-LOGIC  →  2000-PROCESS        (PERFORM)
0000-MAIN-LOGIC  →  3000-CALC-TAX       (PERFORM)
2000-PROCESS     →  2100-READ-INPUT     (PERFORM)
2000-PROCESS     →  2200-VALIDATE       (PERFORM)
3000-CALC-TAX    →  3100-GET-RATE       (PERFORM)
3000-CALC-TAX    →  3200-APPLY-BAND     (PERFORM)
3000-CALC-TAX    →  3300-HANDLE-SPECIAL (PERFORM)
9000-ERROR       →  9100-LOG-ERROR      (PERFORM)
9000-ERROR       →  9200-ABEND         (GO TO)      ← flagged
```

Tool: `cobol-parser-mcp → extract_call_graph`

**3c. Complexity Scoring**

Score the module on a Low/Medium/High scale based on measurable factors:
- Total line count (thresholds TBD during implementation)
- Paragraph count
- Maximum nesting depth (nested IF/EVALUATE/PERFORM)
- Number of GOTOs
- Number of REDEFINES
- Number of external references (CALL, COPY, SQL, CICS, macros)
- Cyclomatic complexity of the call graph

The scoring formula weights these factors. The exact thresholds are calibrated against the BlackJack corpus during implementation.

Tool: `cobol-parser-mcp → score_complexity`

**3d. Anti-pattern Detection**

Scan for known problematic COBOL patterns:

| Anti-pattern | What it means | Severity |
|-------------|---------------|----------|
| `GO TO` | Unstructured control flow — breaks call graph assumptions | High |
| `ALTER` | Dynamic control flow modification — nearly impossible to analyse statically | Critical |
| Nested `PERFORM` | PERFORM inside PERFORM — complex control flow | Medium |
| `REDEFINES` abuse | Multiple data interpretations of same memory — type ambiguity | Medium |
| `PERFORM THRU` | Range-based execution — implicit paragraph inclusion | Low-Medium |
| Fallthrough logic | Code between paragraphs that executes implicitly | High |
| Dead paragraphs | Paragraphs never reached by any PERFORM path | Low |

Each detection includes: pattern type, exact location (paragraph + line), severity rating, brief explanation.

Tool: `cobol-parser-mcp → detect_antipatterns`

**3e. External Reference Extraction**

Scan the entire source for references to external systems and resources:

| Reference Type | How Detected | Example |
|---------------|-------------|---------|
| `COPY` | `COPY <copybook-name>` in DATA or PROCEDURE DIVISION | `COPY PAYROLL-COPY` |
| `CALL` | `CALL '<program-name>'` in PROCEDURE DIVISION | `CALL 'TAX-CALC'` |
| `SQL` | `EXEC SQL ... END-EXEC` blocks | `EXEC SQL SELECT * FROM EMPLOYEE END-EXEC` |
| `CICS` | `EXEC CICS ... END-EXEC` blocks | `EXEC CICS SEND MAP('PAYMAP') END-EXEC` |
| `DELTA_MACRO` | Client-specific macro invocations (pattern from config) | `DLTM-ACCT-LOCK` |

For each reference: type, name, location (paragraph + line), and whether it was resolved.

**3f. Delta Macro Resolution**

For every detected Delta macro reference, Po calls `delta-macros-mcp → get_macro`:

- **Found:** Store the macro definition, category, and mark `resolved = true`
- **Not found:** Flag as `UNKNOWN_MACRO`, mark `resolved = false`, continue analysis

Unknown macros do NOT halt analysis. They are flagged and the analyst addresses them later (Journey 2 in the PRD — Alex adds the macro definition and re-runs just the affected area).

**3g. COBOL Dialect Handling**

The parser must handle or explicitly flag dialect variants:

| Dialect Feature | Handling |
|----------------|----------|
| IBM Enterprise COBOL | Full parsing support |
| COBOL-85 (VS COBOL II) | Full parsing support |
| CICS constructs (`EXEC CICS ... END-EXEC`) | Detected, extracted as external references, content parsed for transaction type |
| DB2 embedded SQL (`EXEC SQL ... END-EXEC`) | Detected, extracted as external references, SQL statement preserved |
| COPY with REPLACING | Copybook reference extracted, REPLACING clause captured |
| Compiler directives | Recognised and skipped (not flagged as unknown) |
| Unrecognised syntax | **Flagged as UNKNOWN_CONSTRUCT** — never silently ignored |

The cardinal rule: **if the parser doesn't understand something, it flags it.** Silent misparsing produces a corrupt spec layer and a wrong architecture downstream. Every unrecognised construct becomes a flag with code `UNKNOWN_CONSTRUCT`, the exact location, and the raw source text.

**Writes to spec layer after Step 3:** `paragraphs`, `paragraph_calls`, `antipatterns`, `external_references`, `macro_calls` records. Updates `cobol_files` with `complexity_score`.

#### Step 4: Semantic Clustering (AI Phase Begins)

This is where the LLM enters. The deterministic pre-pass has established the structural facts. Now AI proposes an interpretation: which paragraphs belong together functionally?

**Input to AI:**
- Complete paragraph list with line counts
- Full call graph (who calls whom)
- Paragraph names (COBOL naming conventions often encode meaning: `3100-CALC-TAX` tells you something)
- Code snippets from each paragraph (enough context for the LLM to understand purpose)
- Anti-patterns detected (helps contextualise unusual flow)

**What AI produces:**
- Groups of paragraphs that form functional clusters
- A proposed cluster name for each group
- Rationale for the grouping

**Example output:**
```
Cluster A: "Tax Calculation"
  Paragraphs: 3000-CALC-TAX, 3100-GET-RATE, 3200-APPLY-BAND, 3300-HANDLE-SPECIAL
  Rationale: These paragraphs form a self-contained tax calculation pipeline.
             3000 orchestrates, 3100 looks up the rate, 3200 applies it,
             3300 handles edge cases.

Cluster B: "Input Processing"
  Paragraphs: 2000-PROCESS, 2100-READ-INPUT, 2200-VALIDATE
  Rationale: Sequential input reading and validation before processing.

Cluster C: "Error Handling"
  Paragraphs: 9000-ERROR, 9100-LOG-ERROR, 9200-ABEND
  Rationale: Centralised error handling. Note: 9200-ABEND uses GO TO
             (flagged anti-pattern) to force program termination.

Cluster D: "Program Control"
  Paragraphs: 0000-MAIN-LOGIC, 1000-INIT
  Rationale: Top-level orchestration and initialisation.
```

**Important:** Clustering is a proposal. It has NOT been written to the spec layer yet.

**Writes to spec layer:** Nothing. Clusters are proposed, not persisted.

#### Step 5: AI Analysis — Plain-English Descriptions

For each proposed cluster, AI generates a detailed plain-English description:

**Input to AI:**
- The cluster's paragraph grouping from Step 4
- Actual COBOL source code for those paragraphs
- External references within those paragraphs
- Anti-patterns detected within those paragraphs
- Resolved macro definitions (if any macros are in those paragraphs)

**What AI produces:**
- Per-cluster: A plain-English description of what the cluster does, suitable for a non-technical business reader
- Per-cluster: A technical summary noting any complications (anti-patterns, unresolved macros, complex data flows)
- Per-module: An overall summary describing the program's purpose

**Example output:**
```
Cluster A: "Tax Calculation"
  Business description: This section calculates the employee's monthly tax
  deduction. It looks up their tax band from the TAX-BAND table, retrieves
  the current rate, and applies it to their gross pay. There is special
  handling for employees whose overtime exceeds a threshold — these use a
  different tax rate looked up from the same table.

  Technical notes: 4 paragraphs, no anti-patterns detected. One COPY
  reference (TAX-TABLES-COPY) for the tax band data structure. Complexity
  is moderate — the special case handling adds branching but is well-structured.
```

**What AI also flags:**
- Clusters where the AI has low confidence in its grouping
- Paragraphs that could reasonably belong to multiple clusters
- Areas where the code is ambiguous or the COBOL naming doesn't match what the code actually does

**Writes to spec layer:** Nothing. Descriptions are proposed, not persisted.

#### Step 6: Review Gate (Human Decision Point)

This is where the analyst takes the expert seat. Everything up to this point is a proposal. Now the analyst reviews, corrects, and approves.

**What the analyst sees:**
- The static pre-pass results: call graph, complexity, anti-patterns, external references (these are facts — no review needed, just awareness)
- The proposed clusters with AI descriptions
- Any flags: unknown macros, unrecognised constructs, low-confidence areas

**What the analyst can do for each cluster:**

| Action | What happens |
|--------|-------------|
| **Approve** | Cluster and its description are accepted as-is |
| **Correct** | Analyst modifies the description, renames the cluster, or moves paragraphs between clusters. AI re-generates affected descriptions with the correction as context. |
| **Split** | Analyst breaks a cluster into two or more smaller clusters |
| **Merge** | Analyst combines two clusters that should be one |
| **Re-analyse** | Analyst asks AI to re-examine a cluster with additional context or guidance |

The review gate is iterative. The analyst can correct, review the correction, correct again, until satisfied. There is no time limit and no automatic progression.

**Completion condition:** Every cluster has been explicitly approved by the analyst. No cluster remains in "proposed" state.

**Writes to spec layer:** Nothing yet — approval is tracked in the workflow state, not persisted until Step 7.

#### Step 7: Write to Spec Layer

Only after the analyst has approved all clusters does Po write the analysis to the spec layer via `specdb-mcp`.

**What gets written:**

| Table | Records |
|-------|---------|
| `cobol_files` | Updated: `analysis_status = 'approved'`, final `complexity_score` |
| `paragraphs` | One record per paragraph: name, lines, cluster assignment |
| `paragraph_calls` | One record per call graph edge: caller, callee, type |
| `clusters` | One record per approved cluster: name, description, `review_status = 'approved'` |
| `antipatterns` | One record per detected anti-pattern: type, location, severity |
| `external_references` | One record per external reference: type, name, location, resolved status |
| `macro_calls` | One record per Delta macro call: name, location, context, resolved status, definition |

**Idempotency:** If this module has been analysed before (re-run), all writes use INSERT OR IGNORE + UPDATE. Existing records are updated, not duplicated. The entire write is wrapped in a single SQLite transaction — if any write fails, the whole transaction rolls back and the analyst is notified.

**Post-write validation:** Po queries the spec layer to confirm all records were written correctly and reports the final count to the analyst.

### Analyse Structure — Summary

```
COBOL Source File
    │
    ▼
┌─────────────────────────────────┐
│  Step 1-2: Init + Load Source   │  ← Verify file, extract PROGRAM-ID
│  Step 3: Static Pre-pass        │  ← DETERMINISTIC: paragraphs, call graph,
│          (cobol-parser-mcp)     │     complexity, anti-patterns, references, macros
├─────────────────────────────────┤
│  Step 4: Semantic Clustering    │  ← AI: group paragraphs into functional clusters
│  Step 5: AI Analysis            │  ← AI: plain-English descriptions per cluster
├─────────────────────────────────┤
│  Step 6: Review Gate            │  ← HUMAN: approve/correct/split/merge clusters
├─────────────────────────────────┤
│  Step 7: Write to Spec Layer    │  ← PERSIST: only approved data written
└─────────────────────────────────┘
    │
    ▼
Spec Layer: cobol_files, paragraphs, paragraph_calls,
            clusters, antipatterns, external_references, macro_calls
```
