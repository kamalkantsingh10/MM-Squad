# Story 2.8: IDE Slash Command Registration for All MM Agents

Status: review

## Story

As an operator,
I want all MM agents fully registered as slash commands in both Claude Code and GitHub Copilot,
so that I can invoke any MM agent (`/bmad-agent-mm-*`) without manually copying files.

## Acceptance Criteria

1. **AC1: Claude Code slash commands — all MM agents**
   - Given the `.claude/commands/` directory is the Claude Code slash command location
   - When the operator opens a Claude Code session in this project
   - Then all 7 MM agents are available as slash commands: `bmad-agent-mm-shifu`, `bmad-agent-mm-tigress`, `bmad-agent-mm-crane`, `bmad-agent-mm-viper`, `bmad-agent-mm-monkey`, `bmad-agent-mm-tai-lung`, `bmad-agent-mm-oogway`
   - And each command file loads the correct agent from `_bmad/mm/agents/`

2. **AC2: GitHub Copilot agent files — all MM agents**
   - Given the `.github/agents/` directory is the GitHub Copilot agent location
   - When the operator uses GitHub Copilot Chat in VS Code
   - Then all 7 MM agents are available as Copilot agents
   - And each `.agent.md` file has the correct `description` and `tools` frontmatter
   - And each file loads the correct agent from `_bmad/mm/agents/`

3. **AC3: Consistent activation across both IDEs**
   - Given the slash command files exist in both locations
   - When any MM agent is invoked in either IDE
   - Then the activation instructions are identical — load the agent file, follow activation, display menu, wait for input

## Tasks / Subtasks

- [x] Task 1: Create missing Claude Code slash commands (AC: #1, #3)
  - [x] 1.1: Create `.claude/commands/bmad-agent-mm-tigress.md`
  - [x] 1.2: Create `.claude/commands/bmad-agent-mm-viper.md`
  - [x] 1.3: Create `.claude/commands/bmad-agent-mm-monkey.md`
  - [x] 1.4: Create `.claude/commands/bmad-agent-mm-tai-lung.md`
  - [x] 1.5: Create `.claude/commands/bmad-agent-mm-oogway.md`
  - [x] 1.6: Create `.claude/commands/bmad-agent-mm-crane.md`
  - Note: `.claude/commands/bmad-agent-mm-shifu.md` already exists from Story 2.7 — verify it is correct

- [x] Task 2: Create GitHub Copilot agent files — all MM agents (AC: #2, #3)
  - [x] 2.1: Create `.github/agents/bmad-agent-mm-shifu.agent.md`
  - [x] 2.2: Create `.github/agents/bmad-agent-mm-tigress.agent.md`
  - [x] 2.3: Create `.github/agents/bmad-agent-mm-viper.agent.md`
  - [x] 2.4: Create `.github/agents/bmad-agent-mm-monkey.agent.md`
  - [x] 2.5: Create `.github/agents/bmad-agent-mm-tai-lung.agent.md`
  - [x] 2.7: Create `.github/agents/bmad-agent-mm-crane.agent.md`
  - [x] 2.6: Create `.github/agents/bmad-agent-mm-oogway.agent.md`

- [x] Task 3: Write tests (AC: #1, #2, #3)
  - [x] 3.1: Test all 7 `.claude/commands/bmad-agent-mm-*.md` files exist
  - [x] 3.2: Test each Claude Code command file has valid frontmatter (`name`, `description`)
  - [x] 3.3: Test each Claude Code command file references the correct `_bmad/mm/agents/` path
  - [x] 3.4: Test all 7 `.github/agents/bmad-agent-mm-*.agent.md` files exist
  - [x] 3.5: Test each Copilot agent file has valid frontmatter (`description`, `tools`)
  - [x] 3.6: Test each Copilot agent file references the correct `_bmad/mm/agents/` path
  - [x] 3.7: Run full test suite — zero regressions

## Dev Notes

### File Format References

**Claude Code command file** (`.claude/commands/bmad-agent-mm-<name>.md`):
```markdown
---
name: '<name>'
description: '<name> agent'
---

You must fully embody this agent's persona and follow all activation instructions exactly as specified. NEVER break character until given an exit command.

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from {project-root}/_bmad/mm/agents/<name>.md
2. READ its entire contents - this contains the complete agent persona, menu, and instructions
3. FOLLOW every step in the <activation> section precisely
4. DISPLAY the welcome/greeting as instructed
5. PRESENT the numbered menu
6. WAIT for user input before proceeding
</agent-activation>
```

**GitHub Copilot agent file** (`.github/agents/bmad-agent-mm-<name>.agent.md`):
```markdown
---
description: '<DisplayName> — <title>: <capabilities>'
tools: ['read', 'edit', 'search', 'execute']
---

You must fully embody this agent's persona and follow all activation instructions exactly as specified.

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from {project-root}/_bmad/mm/agents/<name>.md
2. READ its entire contents - this contains the complete agent persona, menu, and instructions
3. FOLLOW every step in the <activation> section precisely
4. DISPLAY the welcome/greeting as instructed
5. PRESENT the numbered menu
6. WAIT for user input before proceeding
</agent-activation>
```

### Agent Identity Reference

| Name | DisplayName | Title | Icon | Capabilities |
|------|-------------|-------|------|--------------|
| shifu | Shifu | Delivery Manager | 🐭 | sprint planning, dependency tracking, progress monitoring, review gate management, GitLab project orchestration |
| tigress | Tigress | Migration Architect | 🐯 | migration architecture, target language selection, subsystem mapping, dependency analysis |
| crane | Crane | Java Dev Agent | 🏗️ | story execution, test-driven development, Java code generation, spec layer consumption |
| viper | Viper | COBOL Dev Agent | 🐍 | story execution, test-driven development, COBOL modernisation, dialect handling |
| monkey | Monkey | Python Dev Agent | 🐒 | story execution, test-driven development, Python code generation, spec layer consumption |
| tai-lung | Tai Lung | QA Agent | 🐆 | migration validation, business rule verification, epic sign-off, test generation |
| oogway | Oogway | Auditor | 🐢 | quality gate guardian, migration audit, compliance verification, architecture review |

### Existing Reference Files

- `.claude/commands/bmad-agent-mm-shifu.md` — existing Shifu Claude Code command (use as template)
- `.claude/commands/bmad-agent-bmm-dev.md` — BMM dev agent command (format reference)
- `.github/agents/bmad-agent-bmm-dev.agent.md` — BMM dev Copilot agent (format reference)

### Test Pattern

Follow `tests/test_tigress_agent.py` for file existence tests. New test file: `tests/test_ide_slash_commands.py`.

### Dependencies

- Epic 1 Story 1.4 (IDE configuration) — established .claude/commands and .github/agents structure
- Stories 2.7, 3.2, 3.3, 3.4, 3.5, 3.6 (all MM agents must exist at `_bmad/mm/agents/`)

### References

- [Source: documents/planning-artifacts/epics.md — Epic 2]
- [Source: .claude/commands/bmad-agent-mm-shifu.md — existing Claude Code command format]
- [Source: .github/agents/bmad-agent-bmm-dev.agent.md — Copilot agent format]

## Dev Agent Record

### Agent Model Used
claude-sonnet-4-6

### Debug Log References
- Pre-existing test failures in `test_shifu_agent.py`, `test_mm_module_registry.py`, `test_shared_infrastructure.py` confirmed unrelated to this story (MCP tool names, config loader — separate stories).
- ROS Jazzy pytest plugin conflict resolved via `PYTHONPATH=""` isolation (same approach used by all existing tests).

### Completion Notes List
- ✅ Created 6 missing Claude Code slash command files (tigress, crane, viper, monkey, tai-lung, oogway) matching shifu template format exactly.
- ✅ Verified existing `.claude/commands/bmad-agent-mm-shifu.md` is correct and matches expected format.
- ✅ Created 7 GitHub Copilot agent files (all MM agents) with correct frontmatter and activation blocks.
- ✅ Created `tests/test_ide_slash_commands.py` with 72 parametrised tests covering all ACs. All 72 pass.
- ✅ Zero regressions introduced (341 existing passing tests still pass).

### File List
- `.claude/commands/bmad-agent-mm-tigress.md` (created)
- `.claude/commands/bmad-agent-mm-viper.md` (created)
- `.claude/commands/bmad-agent-mm-monkey.md` (created)
- `.claude/commands/bmad-agent-mm-tai-lung.md` (created)
- `.claude/commands/bmad-agent-mm-crane.md` (created)
- `.claude/commands/bmad-agent-mm-oogway.md` (created)
- `.github/agents/bmad-agent-mm-shifu.agent.md` (created)
- `.github/agents/bmad-agent-mm-tigress.agent.md` (created)
- `.github/agents/bmad-agent-mm-viper.agent.md` (created)
- `.github/agents/bmad-agent-mm-monkey.agent.md` (created)
- `.github/agents/bmad-agent-mm-tai-lung.agent.md` (created)
- `.github/agents/bmad-agent-mm-crane.agent.md` (created)
- `.github/agents/bmad-agent-mm-oogway.agent.md` (created)
- `tests/test_ide_slash_commands.py` (created)
- `documents/implementation-artifacts/2-8-ide-slash-command-registration-for-mm-agents.md` (updated)
- `documents/implementation-artifacts/sprint-status.yaml` (updated)

### Change Log
- 2026-03-08: Implemented Story 2.8 — created 5 Claude Code slash commands, 6 GitHub Copilot agent files, 72-test test suite. All ACs satisfied.
