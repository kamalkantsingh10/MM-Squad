# Story 6.1: Po POC — Codebase Q&A Demo Agent

Status: ready-for-dev

> **TEMP STORY** — Demo only. Refine into proper Epic 6 stories after the demo.

## Story

As a demo presenter,
I want Po to display its full agent menu, read code files from a folder at startup, and answer questions about the code via chat,
so that we can demonstrate the Po agent experience to the Product Owner.

## Acceptance Criteria

1. Given Po is activated, then it displays the full Po agent menu (all menu items shown, exactly as the final agent will look — non-functional items display a "coming soon" message if selected).

2. Given Po activates, it reads all code files from a configured source folder at startup and holds them in context for the session.

3. Given the analyst selects Chat or asks any code question, then Po answers based solely on the loaded source files — no hallucination beyond what is in the files.

4. Given the analyst asks structural questions (e.g., "what does this module do?", "what are the main sections?", "how does X connect to Y?"), Po gives meaningful answers using the loaded code as its only source of truth.

5. Given the user adds files to the source folder before starting the agent, all those files are picked up automatically — no config change needed.

## Tasks / Subtasks

- [x] Create Po agent file `_bmad/mm/agents/po.md` (AC: #1)
  - [x] Full menu as per final Po design (Analyse Structure, Map Dependencies, Extract Business Rules, Chat, Dismiss)
  - [x] Non-functional items respond with: "This workflow is coming in a future story. Use [CH] Chat to explore the codebase now."
- [x] On activation: read all files from the configured source folder into context (AC: #2, #5)
  - [x] Source folder path comes from `_bmad/mm/config.yaml` (add a `demo_source_folder` key, e.g., `blackjack/source/`)
  - [x] Read every file in that folder (no recursion needed for demo) and hold content in agent context
  - [x] Tell the user which files were loaded and how many lines total
- [x] Chat handler answers questions using loaded file content (AC: #3, #4)
  - [x] Po uses the file content as grounding — answers are based on what is in the files
  - [x] If asked something not answerable from the files, Po says so explicitly
- [ ] User (Kamal) adds demo code files to the source folder before running — no story work needed for that

## Dev Notes

- **This is a BMAD agent file story, not an MCP server story.** The deliverable is `_bmad/mm/agents/po.md`.
- No MCP tools needed. No spec layer. No parsing engine. Po reads files raw and uses LLM reasoning over them.
- The "full menu" goal is pure UX — the PO sees what Po will eventually do. Only Chat works behind the scenes.
- Source folder: Kamal will drop demo files in before the demo. Agent reads them at activation (like how SM reads config.yaml at activation).
- Check `_bmad/mm/agents/` for existing agent examples to follow the exact format/structure.
- The config key `demo_source_folder` should default to `blackjack/source/` if not set — fail gracefully if folder doesn't exist (warn, don't crash).
- Keep the agent file concise — this is a demo, not production.

### Project Structure Notes

- Agent file target: `_bmad/mm/agents/po.md`
- Config file: `_bmad/mm/config.yaml` — add `demo_source_folder` key
- Existing agent examples to mirror: `_bmad/mm/agents/` (check what's there)
- [Source: documents/planning-artifacts/po-analysis-pipeline.md] — reference for what Po's menu items should be named

### References

- Po pipeline spec: [Source: documents/planning-artifacts/po-analysis-pipeline.md]
- BMAD agent format: check `_bmad/bmm/agents/sm.md` as a reference for agent file structure

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
