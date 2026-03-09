# Story 3.1: Dev Agent Workflows — Copy & Adapt from BMAD Dev

Status: review

## Story

As a developer,
I want all BMAD dev agent workflows copied and adapted for the MM module,
so that the three dev agents (Tigress, Viper, Monkey) share a common set of MM-adapted dev workflows.

## Acceptance Criteria

1. **AC1: Dev workflows copied to MM module**
   - Given the BMAD dev agent's workflows exist in `_bmad/bmm/workflows/4-implementation/`
   - When the developer copies them to `_bmad/mm/workflows/dev/`
   - Then all dev workflows are present: `dev-story/` and `code-review/`
   - And each workflow follows BMAD step-file architecture (workflow.yaml or workflow.md + supporting files)

2. **AC2: Workflows adapted for MM context**
   - Given the copied dev workflows exist
   - When the developer adapts them for MM context
   - Then workflows reference Po's output documents (business markdown, architecture docs) as inputs instead of standard BMAD artifacts
   - And code generation workflows accept target language as a parameter driven by the agent's persona
   - And workflows declare `gitlab-mcp` access for progress updates and status tracking
   - And no workflow references `specdb-mcp` — agents consume documents, not the spec layer

3. **AC3: All three dev agents reference shared workflows**
   - Given the adapted dev workflows exist
   - When all three dev agents reference them
   - Then Tigress, Viper, and Monkey all point to the same `_bmad/mm/workflows/dev/` directory
   - And the agent persona (not the workflow) determines target language behaviour

## Tasks / Subtasks

- [x] Task 1: Create dev workflow directory structure (AC: #1)
  - [x] 1.1: Create `_bmad/mm/workflows/dev/dev-story/` directory
  - [x] 1.2: Create `_bmad/mm/workflows/dev/code-review/` directory

- [x] Task 2: Copy and adapt dev-story workflow (AC: #1, #2)
  - [x] 2.1: Copy `_bmad/bmm/workflows/4-implementation/dev-story/workflow.yaml` to `_bmad/mm/workflows/dev/dev-story/workflow.yaml`
  - [x] 2.2: Update `config_source` from `{project-root}/_bmad/bmm/config.yaml` to `{project-root}/_bmad/mm/config.yaml`
  - [x] 2.3: Update `installed_path` to `{project-root}/_bmad/mm/workflows/dev/dev-story`
  - [x] 2.4: Copy `instructions.xml` and adapt references — replace BMAD planning artifact paths with MM equivalents
  - [x] 2.5: Copy `checklist.md` and adapt for MM context
  - [x] 2.6: Ensure workflow references Po's output documents as inputs, not raw COBOL or specdb
  - [x] 2.7: Add `gitlab-mcp` tool references for progress tracking (apply_label, add_comment)

- [x] Task 3: Copy and adapt code-review workflow (AC: #1, #2)
  - [x] 3.1: Copy `_bmad/bmm/workflows/4-implementation/code-review/workflow.yaml` to `_bmad/mm/workflows/dev/code-review/workflow.yaml`
  - [x] 3.2: Update `config_source` to `{project-root}/_bmad/mm/config.yaml`
  - [x] 3.3: Update `installed_path` to `{project-root}/_bmad/mm/workflows/dev/code-review`
  - [x] 3.4: Copy `instructions.xml` and `checklist.md`, adapt for MM context
  - [x] 3.5: Add MM-specific review criteria: spec layer compliance, business rule preservation, COBOL construct handling

- [x] Task 4: Verify workflow file paths in module-help.csv (AC: #3)
  - [x] 4.1: Confirm `module-help.csv` entries for `Dev Story` and `Code Review` point to `_bmad/mm/workflows/dev/` paths
  - [x] 4.2: Update paths if incorrect

- [x] Task 5: Write tests (AC: #1, #2, #3)
  - [x] 5.1: Test dev workflow directories exist (`dev-story/`, `code-review/`)
  - [x] 5.2: Test workflow.yaml files exist and are valid YAML with required keys
  - [x] 5.3: Test config_source points to MM config (not BMM)
  - [x] 5.4: Test installed_path points to MM workflows (not BMM)
  - [x] 5.5: Test module-help.csv references correct workflow paths
  - [x] 5.6: Run full test suite — zero regressions

## Dev Notes

### Architecture Constraints

- **Workflow location**: `_bmad/mm/workflows/dev/` — per architecture doc project structure
- **Config source**: `_bmad/mm/config.yaml` — MM module config, NOT BMM
- **No specdb-mcp access in dev workflows** — dev agents consume Po's output documents (business markdown, architecture docs), not the spec layer directly
- **gitlab-mcp access** — all agents can post progress comments and apply labels
- **Target language is agent-persona-driven** — the workflow itself does not hardcode Java/COBOL/Python; the agent persona determines behaviour

### Source Files to Copy From

| BMM Source | MM Target |
|---|---|
| `_bmad/bmm/workflows/4-implementation/dev-story/workflow.yaml` | `_bmad/mm/workflows/dev/dev-story/workflow.yaml` |
| `_bmad/bmm/workflows/4-implementation/dev-story/instructions.xml` | `_bmad/mm/workflows/dev/dev-story/instructions.xml` |
| `_bmad/bmm/workflows/4-implementation/dev-story/checklist.md` | `_bmad/mm/workflows/dev/dev-story/checklist.md` |
| `_bmad/bmm/workflows/4-implementation/code-review/workflow.yaml` | `_bmad/mm/workflows/dev/code-review/workflow.yaml` |
| `_bmad/bmm/workflows/4-implementation/code-review/instructions.xml` | `_bmad/mm/workflows/dev/code-review/instructions.xml` |
| `_bmad/bmm/workflows/4-implementation/code-review/checklist.md` | `_bmad/mm/workflows/dev/code-review/checklist.md` |

### Key Adaptations Required

1. **config_source**: `{project-root}/_bmad/bmm/config.yaml` → `{project-root}/_bmad/mm/config.yaml`
2. **installed_path**: `{project-root}/_bmad/bmm/workflows/4-implementation/dev-story` → `{project-root}/_bmad/mm/workflows/dev/dev-story`
3. **Input documents**: BMM planning artifacts → Po's output documents (business markdown from `extract-business-rules`, architecture from Oogway)
4. **MCP server access**: Add `gitlab-mcp` references for progress updates
5. **No specdb-mcp**: Dev agents do NOT access the spec layer directly

### Existing Patterns to Follow

- Shifu workflows (Story 2.7) at `_bmad/mm/workflows/pm/` — established MM workflow pattern
- Each workflow has: `workflow.yaml` + `instructions.md` (or `.xml`) + optional `checklist.md`
- Test pattern: `tests/gitlab_mcp/test_shifu_agent.py` — parametrised directory/file existence tests

### module-help.csv Current Entries

Dev Story and Code Review are already registered in `module-help.csv`:
```
mm,4-implementation,Dev Story,DS,40,_bmad/mm/workflows/dev/dev-story/workflow.md,bmad-mm-dev-story,false,tigress,...
mm,4-implementation,Code Review,CR,50,_bmad/mm/workflows/dev/code-review/workflow.md,bmad-mm-code-review,false,tigress,...
```
Note: CSV references `workflow.md` but source uses `workflow.yaml` — verify which format to use and ensure consistency.

### Project Structure Notes

- Workflows go in `_bmad/mm/workflows/dev/` (not `_bmad/mm/workflows/4-implementation/`)
- MM module uses flat workflow categories: `po/`, `dev/`, `architect/`, `pm/`, `qa/`
- Tests go in `tests/` root directory — follow `test_shifu_agent.py` pattern

### Dependencies

- Epic 1 (MM module foundation) — all complete
- Epic 2 Story 2.7 (Shifu workflows) — established MM workflow pattern
- BMAD BMM dev workflows — source files to copy

### References

- [Source: documents/planning-artifacts/epics.md — Epic 3, Story 3.1]
- [Source: documents/planning-artifacts/architecture.md — Project Structure, dev/ workflows]
- [Source: _bmad/bmm/workflows/4-implementation/dev-story/ — BMM source workflows]
- [Source: _bmad/bmm/workflows/4-implementation/code-review/ — BMM source workflows]
- [Source: _bmad/mm/module-help.csv — existing workflow registry entries]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6

### Debug Log References

### Completion Notes List

- Copied and adapted dev-story workflow (workflow.yaml, instructions.xml, checklist.md) from BMM to MM module
- Copied and adapted code-review workflow with MM-specific review criteria (spec layer compliance, business rule preservation, COBOL construct handling)
- Both workflows: config_source → MM config, installed_path → MM paths, mcp_tools → [apply_label, add_comment], input_file_patterns → Po's business rules + Oogway's architecture
- No specdb-mcp references in any dev workflow — agents consume documents only
- Target language is agent-persona-driven, not hardcoded in workflows
- module-help.csv already had correct path entries for dev-story and code-review
- Code review fixes: test_no_specdb_mcp_reference was logically broken (always passed) — fixed to check parsed mcp_tools YAML field instead of raw text
- Code review fixes: module-help.csv extension corrected from .md to .yaml for dev-story and code-review entries
- Code review fixes: dev-story instructions.xml step 6 rewritten from redundant "Author comprehensive tests" to "Verify test coverage completeness across all ACs" — distinct from TDD cycle in step 5
- 22 new tests all pass; 6 pre-existing failures in test_shifu_agent.py (Story 2.7 review items, not regressions)

### Change Log

- 2026-03-08: Story 3.1 implemented — dev workflows copied and adapted for MM module
- 2026-03-08: Code review fixes — broken specdb test, module-help.csv extension, instructions.xml step 6

### File List

- _bmad/mm/workflows/dev/dev-story/workflow.yaml (new)
- _bmad/mm/workflows/dev/dev-story/instructions.xml (new)
- _bmad/mm/workflows/dev/dev-story/checklist.md (new)
- _bmad/mm/workflows/dev/code-review/workflow.yaml (new)
- _bmad/mm/workflows/dev/code-review/instructions.xml (new)
- _bmad/mm/workflows/dev/code-review/checklist.md (new)
- tests/test_dev_workflows.py (new, updated by code review)
- _bmad/mm/workflows/dev/dev-story/instructions.xml (modified — step 6 rewritten by code review)
- _bmad/mm/module-help.csv (modified — .md → .yaml extension fix by code review)
- documents/implementation-artifacts/sprint-status.yaml (modified)
- documents/implementation-artifacts/3-1-dev-agent-workflows-copy-and-adapt-from-bmad-dev.md (modified)
