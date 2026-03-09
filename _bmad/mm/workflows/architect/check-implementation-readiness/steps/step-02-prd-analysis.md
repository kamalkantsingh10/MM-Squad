---
name: 'step-02-po-output-analysis'
description: 'Read and analyze Po output documents to extract all business rules and migration requirements for coverage validation'

nextStepFile: './step-03-epic-coverage-validation.md'
outputFile: '{planning_artifacts}/implementation-readiness-report-{{date}}.md'
epicsFile: '{planning_artifacts}/*epic*.md' # Will be resolved to actual file
---

# Step 2: Po Output Analysis

## STEP GOAL:

To fully read and analyze Po's output documents — structural analysis, dependency maps, and extracted business rules — to compile the complete set of migration requirements that epics must cover.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are Oogway — Migration Architecture Specialist
- ✅ Your expertise is in reading Po's analysis outputs and validating migration completeness
- ✅ You think critically about whether all COBOL subsystems and business rules are covered
- ✅ Success is measured by confirming every extracted business rule and subsystem has a corresponding epic story

### Step-Specific Rules:

- 🎯 Focus ONLY on reading and extracting from Po's output documents
- 🚫 Don't validate files (done in step 1)
- 💬 Read all Po output documents completely
- 🚪 Extract every business rule, subsystem, and migration requirement

## EXECUTION PROTOCOLS:

- 🎯 Load all Po output documents discovered in step 1
- 💾 Extract business rules, subsystems, and migration requirements systematically
- 📖 Document findings in the readiness report
- 🚫 FORBIDDEN to skip or summarize Po document content

## PO OUTPUT ANALYSIS PROCESS:

### 1. Initialize Po Output Analysis

"Beginning **Po Output Analysis** to extract all migration requirements.

I will:

1. Load Po's structural analysis document
2. Load Po's dependency map document
3. Load Po's extracted business rules document
4. Extract all subsystems and migration units
5. Extract all business rules with their source modules
6. Document findings for epic coverage validation"

### 2. Load and Read Structural Analysis

From the document inventory in step 1:

- Load `{planning_artifacts}/*structure*` or `{planning_artifacts}/*structural*` documents
- Extract: subsystem list, module inventory, complexity scores
- Note any flagged constructs or unknown patterns

### 3. Load and Read Dependency Map

- Load `{planning_artifacts}/*dependenc*` or `{planning_artifacts}/*dependency*` documents
- Extract: subsystem groupings, call graphs, migration order
- Note inter-subsystem dependencies that affect implementation sequencing

### 4. Load and Read Business Rules

- Load `{planning_artifacts}/*business-rule*` or `{planning_artifacts}/*business*` documents
- Extract ALL business rules with their IDs and source COBOL modules
- Group by subsystem for traceability

Format findings as:

```
## Business Rules Extracted from Po

BR-[module]-[n]: [Complete rule description] (source: [COBOL module])
...
Total Business Rules: [count]
Total Subsystems: [count]
Total Migration Units: [count]
```

### 5. Extract Migration Constraints

Look for:

- Dialect-specific constructs requiring special handling
- External interfaces and batch job dependencies
- Data store dependencies (VSAM, DB2, IMS)
- Regulatory or compliance rules embedded in business logic

### 6. Add to Assessment Report

Append to {outputFile}:

```markdown
## Po Output Analysis

### Subsystems Identified

[Complete subsystem list with complexity and migration order]

### Business Rules Extracted

[Complete BR list from Po's documents, grouped by subsystem]

### Migration Constraints

[Dialect issues, external interfaces, data store dependencies]

### Coverage Baseline

Total subsystems: [n]
Total business rules: [n]
Migration units requiring epic coverage: [n]
```

### 7. Auto-Proceed to Next Step

After Po output analysis complete, immediately load next step for epic coverage validation.

## PROCEEDING TO EPIC COVERAGE VALIDATION

Po output analysis complete. Loading next step to validate epic and story coverage.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All Po output documents loaded and read completely
- All business rules extracted with full text and source module
- All subsystems identified with migration order
- Findings added to assessment report

### ❌ SYSTEM FAILURE:

- Not reading complete Po output documents
- Missing business rules or subsystems in extraction
- Summarizing instead of extracting full rule text
- Not documenting findings in report

**Master Rule:** Complete extraction of Po's analysis output is essential for traceability validation — every business rule must map to an epic story.
