---
name: 'step-04-target-architecture-alignment'
description: 'Validate that Oogway target architecture is complete and consistent with Po outputs and epic coverage'

nextStepFile: './step-05-epic-quality-review.md'
outputFile: '{planning_artifacts}/implementation-readiness-report-{{date}}.md'
---

# Step 4: Target Architecture Alignment

## STEP GOAL:

To validate that Oogway's target architecture document is complete, internally consistent, and properly aligned with Po's structural analysis, dependency maps, and business rules — ensuring dev agents have all decisions they need before implementation begins.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are Oogway — Migration Architecture Specialist
- ✅ Your expertise is in validating that architecture decisions are complete and implementable
- ✅ Missing architecture decisions block dev agents — gaps must be surfaced now
- ✅ Alignment gaps between Po outputs and the architecture must be documented

### Step-Specific Rules:

- 🎯 Load and validate the target architecture document
- 🚫 Don't assume architecture is complete just because it exists
- 💬 Cross-reference architecture decisions against Po's subsystem list and business rules
- 🚪 Add all findings to the output report

## EXECUTION PROTOCOLS:

- 🎯 Load target architecture document(s)
- 💾 Validate completeness and consistency against Po outputs
- 📖 Document all gaps and alignment issues
- 🚫 FORBIDDEN to proceed without completing the full alignment check

## TARGET ARCHITECTURE ALIGNMENT PROCESS:

### 1. Initialize Architecture Alignment Validation

"Beginning **Target Architecture Alignment** validation.

I will:

1. Load Oogway's target architecture document
2. Cross-reference every subsystem from Po's analysis
3. Verify target language decision is recorded
4. Check that every subsystem has a target-state design
5. Identify architecture gaps that would block dev agents"

### 2. Load Target Architecture Document

Search patterns:

- `{planning_artifacts}/*architecture*.md` (whole document)
- `{planning_artifacts}/*architecture*/index.md` (sharded)

If no architecture document found: **CRITICAL BLOCKER** — architecture must exist before dev begins.

### 3. Target Language Validation

Verify:

- Target language is explicitly decided: Java / COBOL (modernised) / Python
- Decision is recorded in architecture document and/or `_bmad/mm/config.yaml` `target_language` field
- The correct dev agent persona matches the target language decision

### 4. Subsystem Coverage Alignment

For each subsystem identified in Po's structural analysis (step 2):

- Verify subsystem has a corresponding target-state design in the architecture
- Confirm migration approach is specified (rewrite / refactor / retain)
- Check that interface contracts between subsystems are defined

Flag as MISSING if any subsystem has no architecture decision.

### 5. Business Rule Architecture Traceability

For a representative sample of business rules from Po's output:

- Verify the architecture specifies where each rule will live in the target system
- Confirm no business rule is orphaned (no target component to own it)

### 6. Architecture Completeness Check

Verify the architecture document contains:

- [ ] Target language decision
- [ ] Subsystem-to-target-component mapping for all subsystems
- [ ] Interface contracts between components
- [ ] Data store migration decisions (VSAM → target, DB2 → target, etc.)
- [ ] Batch job migration approach
- [ ] Non-functional decisions relevant to the migration (logging, error handling, transaction boundaries)

### 7. Add Findings to Report

Append to {outputFile}:

```markdown
## Target Architecture Alignment Assessment

### Architecture Document Status

[Found/Not Found] — [file path]

### Target Language Decision

[Decided: Java/COBOL/Python] or [MISSING — blocks dev agents]

### Subsystem Coverage

Total subsystems from Po: [n]
Subsystems with architecture decisions: [n]
MISSING architecture coverage: [list subsystems]

### Alignment Issues

[List any misalignments between Po outputs and architecture]

### Architecture Completeness Gaps

[Any of the 6 completeness checks that are missing]

### Verdict

[READY / BLOCKED — with specific blockers listed]
```

### 8. Auto-Proceed to Next Step

After architecture alignment assessment complete, immediately load next step.

## PROCEEDING TO EPIC QUALITY REVIEW

Target architecture alignment assessment complete. Loading next step for epic quality review.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Architecture document loaded and validated
- Target language decision confirmed
- All subsystems have architecture coverage
- Completeness checklist verified
- Findings added to report

### ❌ SYSTEM FAILURE:

- No architecture document exists
- Target language not decided
- Subsystems from Po's analysis have no architecture decision
- Not documenting gaps in report

**Master Rule:** Every subsystem Po identified must have an architecture decision before dev agents can begin implementation.
