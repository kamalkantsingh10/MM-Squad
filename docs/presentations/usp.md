# Unique Selling Propositions

## USP 1 — Zero Procurement, Start Next Week

Built entirely on tooling the client already has:
- **GitHub Copilot** — already licensed
- **GitLab** — already running
- **BMAD methodology** — already available

No new software. No security approval cycle. No licensing cost. No months of onboarding.
In regulated IT departments where new software procurement takes months and carries significant cost, this is the difference between starting next week and starting next year.

No other proposal or product in this space can make this claim.

**Supporting data:**
- Vendor approval and procurement in regulated sectors typically takes **3–12 months** before a single line of work begins *(Swimm Guide 2025)*
- The average mainframe modernisation project costs **$7.2M in 2025** — the majority absorbed by tooling, licensing, and setup before delivery starts *(IT Jungle / Royal Cyber research)*
- **74% of organisations** rely on third-party SIs for modernisation — tool adoption is slowed further by multi-vendor procurement cycles *(Kyndryl 2025 State of Mainframe Modernization Survey)*
- Decision cycles for significant tooling spend run **6–18 months** in regulated sectors, requiring board-level sign-off *(OpenLegacy / Swimm 2025)*

---

## USP 2 — Agile, Reinvented for COBOL — Traceable End to End

Standard agile breaks on COBOL estates because it assumes you understand what you are building. This process does not make that assumption.

The proposed SDLC is fully aligned with best agile practices — sprints, epics, stories, review gates — but rebuilt for COBOL modernisation from the ground up. Every stage is tracked natively in GitLab: issues, labels, milestones, boards, and a live README dashboard. Every decision is traceable. Every output is auditable.

The process is fully repeatable. Once proven on one application, it applies to every application in the estate using the same method, the same tooling, and the same artefacts.

**Supporting data:**
- **70% of mainframe modernisation projects fail** when standard agile methodology is applied to COBOL estates *(industry consensus, multiple sources)*
- **80% of enterprises** shifted away from "big bang" rewrites toward phased, incremental approaches in 2024–2025 — but lacked a structured repeatable method to execute them *(Kyndryl 2025 survey)*
- **94% of organisations** say regulatory compliance shapes their modernisation plans — yet current tools produce outputs that regulators cannot review: no structured record of what was found, decided, or why *(Software Mining / Phase Change Software research)*
- Enterprises that see quick wins from a structured process expand scope; those that don't, stall — the absence of a repeatable method is the single most common stall factor *(CIO Magazine / MarketsAndMarkets)*

---

## USP 3 — Frontier AI, Customised to Your Codebase

The solution is powered by frontier AI models — Claude Opus and GPT Codex — but is not a generic AI tool.

It is customised at two levels:
1. **Framework level** — agents and workflows are purpose-built for COBOL analysis, migration architecture, code generation, and QA validation
2. **Application level** — the system learns the client's specific macros, business terminology, and naming conventions as it runs, making every subsequent analysis sharper

Generic AI tools apply to everything and are optimised for nothing. This is built specifically for this problem.

**Supporting data:**
- On **23 February 2026**, Anthropic announced Claude Code's COBOL modernisation capability — **IBM stock dropped 13% in a single day**, losing over **$31 billion in market cap** — its worst day since 2000. The market is signalling that frontier AI applied to COBOL is a genuine threat to the status quo *(CNBC / Bloomberg / Yahoo Finance)*
- Generic AI tools fail specifically on **middleware-specific knowledge** — proprietary macros, CICS constructs, DB2 variants — the most organisation-specific and critical parts of any COBOL estate. Tools that are not customised to the client's environment produce unreliable output precisely where it matters most *(Software Mining / IBM Blog)*
- LLMs without additional scaffolding have limited token windows — large COBOL programs exceed context limits, causing loss of critical context mid-analysis. This solution addresses that directly through structured pre-processing and a persistent spec layer *(RT Insights / Kathalyst research)*

---

## USP 4 — Documentation Is a Byproduct, Not a Project

One of the most persistent and costly problems in legacy estates: documentation does not exist, and creating it is treated as a separate, never-prioritised project.

This process produces documentation as a structural output of every workflow:
- Business rules extracted and written in plain English
- Dependency maps and subsystem boundaries
- Structured spec layer capturing entities, operations, data flows, and rules

By the time a program is analysed, it is documented. There is no separate documentation phase.

**Supporting data:**
- COBOL codebases are characterised by **outdated or missing internal documentation** — institutional knowledge is held by individuals, not systems. When those individuals retire, the knowledge is gone *(AWS ML Blog / Pragmatic Coders Legacy Stats 2025)*
- The **average COBOL programmer is ~60 years old**; nearly **one-third will retire by 2030**. For many departments, there is one person who understands a program — and no documentation safety net when they leave *(TechTarget / Franklin Skills 2025)*
- **94% of organisations** say regulatory compliance shapes their plans — but cannot produce structured, human-readable records of what their legacy systems actually do. This is an audit exposure that documentation-by-design directly addresses *(Software Mining research)*
- No existing commercial tool produces a **queryable, structured intermediate representation** of COBOL program semantics — business rules, entities, operations, and data flows in a form that both developers and business stakeholders can consume. This is a gap this solution fills as a first-principles design decision *(PRD — Innovation & Novel Patterns)*

---

## USP 5 — Built for Maintenance, Not Just Migration

Most modernisation tools are one-shot: analyse, migrate, done. This process is designed to be part of ongoing operations.

The analysis agent (Po) can be invoked on any program at any time:
- Impact analysis before any change to a legacy program
- Onboarding new developers onto unfamiliar programs
- Re-analysis after a change to verify the spec layer is current

The tooling does not retire after the migration project closes. It becomes part of how the team works with legacy code day to day.

**Supporting data:**
- Legacy system maintenance consumes up to **80% of IT budgets** in regulated sectors — the majority of that cost is the labour of understanding systems before touching them safely *(IBM / AWS research)*
- **53% of IT leaders** report their teams cannot keep up with delivery demands at current capacity — the bottleneck is not developer effort, it is the time spent understanding legacy programs before any change can be made *(Software Mind research)*
- Organisations that have invested in analysis tooling **without a clear path beyond the initial project** feel they paid for a report, not progress. A tool that supports day-to-day maintenance has an ongoing ROI case, not just a one-time project justification *(Kathalyst / FairCom research)*
- **70% of organisations** realise value within 12 months of adopting a structured approach to legacy operations — the faster the analysis loop, the faster the value realisation *(BMC DevOps Insights 2025 Mainframe Survey)*
