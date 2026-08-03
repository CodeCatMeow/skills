---
name: software-docs
description: Maintains human-first, agent-navigable software documentation and architecture decision records for general software projects. Use when documenting or changing architecture, public behavior, APIs, configuration, deployment, operational knowledge, or other long-lived software-project context, and when checking whether a non-trivial software change requires documentation updates. Do not use for research projects, experiment logs, research knowledge systems, paper evidence, or scientific lab notebooks.
---

# Software Docs

## Overview

Document decisions and long-lived project knowledge, not just code. Code shows *what*; documentation explains *why*, constraints, and rejected alternatives. Write for human maintainers first. Keep structure predictable for agents, but never sacrifice readability for machine-friendly dumps.

Applies to frontend, backend, full-stack, CLI, desktop, services, AI product apps, and ordinary software. Not a research documentation system, experiment notebook, competition template, or compliance system.

**Research projects are out of scope.** Do not use this skill for research status, weekly research logs, experiment plans/reports, research knowledge bases, paper claim-evidence maps, or other scientific research documentation. Use the project's research documentation skill or process instead.

## When to Use

- Significant architectural or design decisions in a software project
- Public API, interface, config, or user-visible behavior changes
- Features that need durable explanation
- Onboarding people or agents to a software codebase
- Checking whether a software change needs documentation
- Recording reusable operational knowledge for software systems

**When NOT to use:**

- Research projects or mixed work where the documentation goal is research process, experiments, findings, or paper evidence — forbidden for this skill
- Obvious code, clear implementation restated as docs, temporary debugging, daily progress, or handoff dump files
- Full long-lived documentation systems for throwaway prototypes — document only what is necessary to run, evaluate, or hand off the prototype

## Core Principle

> Write for human maintainers first, while keeping the structure predictable and navigable for agents.

Good docs answer: what is this, why this way, what must not change, and where authority lives. Bad docs are file trees, class dumps, or session transcripts.

## Documentation System Model

| Information | Canonical location |
| --- | --- |
| Human-oriented current project knowledge | `README.md` and `docs/` |
| Exact executable technical contracts | Code, types, schemas, OpenAPI, or generated reference derived from them |
| Historical technical decisions | ADRs |
| Active work, bugs, implementation process | Task system, change review, version-control history |
| Released user-visible changes | `CHANGELOG.md` when maintained |

Narrative docs describe the system **as it is now** for maintainers and agents. Exact API, configuration, and data-structure facts still treat executable sources as authoritative; prose should link or explain them, not silently compete. ADRs preserve **why**. Tasks/reviews/VCS preserve **implementation process**. Changelog preserves **what shipped**. Temporary thinking is not long-lived documentation. Do not assume GitHub; use the project's existing mechanisms.

When current-state docs go stale: update, merge, redirect, archive, or delete them. Do not keep contradictory "current" docs for history; history belongs in version control and ADRs.

## Existing Conventions First

Before creating or reorganizing docs, inspect README, existing `docs/`, naming habits, contribution guides, authoritative API/config sources, and task/VCS practice.

Consistent local convention overrides this skill's defaults. Do not force a mature project into the recommended layout. If evidence conflicts, surface it; do not invent a second scheme.

## Optional Default Layout

Use only when no convention exists and the project needs more than a README:

```text
README.md
CHANGELOG.md                         # only when releases need one

docs/
├── index.md                         # map/overview when docs grow
├── architecture/
│   ├── overview.md                  # current architecture
│   └── decisions/                   # ADRs
├── design/                          # significant feature designs, optional
├── reference/                       # exact facts, optional
└── operations/                      # deploy/troubleshoot, optional
```

- On-demand default, not a scaffold to fill
- No empty directories or files for symmetry
- Small projects may use only README
- Add `docs/index.md` only when volume needs a map
- Same principles for frontend, backend, and full-stack; no stack-specific trees
- Default ADR path with no convention: `docs/architecture/decisions/`. If the project already uses `docs/decisions/`, `docs/adr/`, MADR, `adr-tools`, or similar, match that.

## Project Documentation Entry

With multiple long-lived docs, prefer `docs/index.md` as the shared map. It should answer: problem solved, main parts, important directories, core runtime flow, where architecture/design/reference/operations live, sources of truth, and still-valid constraints.

It must not copy child docs, store TODOs or daily progress, become a second README, or become an auto-generated inventory. For one or two docs, README is enough.

## Document Why, Not Only What

Record constraints, trade-offs, rejected alternatives, and non-obvious intent. Do not restate clear code. Prefer durable explanation over session narration.

## Architecture Overview vs ADRs

```text
architecture overview = current state
ADRs                  = historical rationale
```

**Current architecture** (`docs/architecture/overview.md` or equivalent): boundaries, major components, responsibilities, important dependencies, core runtime flow, data/state flow, deployment overview, invariants, known limits/risks.

**ADRs:** context, constraints, alternatives, decision, consequences, supersession links.

When architecture changes: update or add the ADR, refresh the overview to present state, and keep decision history out of the overview.

## Architecture Decision Records

### When to write

Framework/library/major dependency choice; data model/storage; auth, API shape, build, hosting, or infrastructure strategy; expensive-to-reverse decisions; choices future maintainers would re-debate.

### Match existing convention first

Inspect existing ADRs, project instructions, and ADR tooling (for example `.adr-dir`). Match location, format, numbering, naming, and headings. Continue the sequence. Use the default only when no convention exists.

### Default template

```markdown
# ADR-001: Short decision title

## Status
Proposed | Accepted | Superseded by ADR-XXX | Deprecated

## Date
YYYY-MM-DD

## Context
Problem, constraints, and forces.

## Decision
What was chosen.

## Alternatives Considered
Option, pros/cons, why rejected or deferred.

## Consequences
Benefits, costs, follow-ups, and new constraints.
```

### Lifecycle

```text
PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)
```

Do not delete old ADRs. When a decision changes, add a new ADR that supersedes the old one. Agents may draft Proposed ADRs. Mark Accepted only when the task owner explicitly approves, the task already authorizes the agent to decide, or existing project convention allows it. If authority is unclear, leave the ADR Proposed and request review in the handoff.

## Feature Design Docs

Do not create a design doc per function, component, page, or ordinary endpoint.

Consider `docs/design/<feature>.md` only if it spans modules/systems; affects frontend and backend together; has complex state/data/async flow; has substantially different viable designs; needs multi-person or multi-agent coordination; has migration/compatibility/security impact; or cannot be explained long-term from the task alone.

Optional sections only as needed: objective, scope, non-goals, flows, proposed design, affected components, interfaces/data, errors/edge cases, security, testing, rollout/migration, related tasks/changes/ADRs. Do not force every section.

## Reference and Operations

**Reference** (`docs/reference/`): config keys, env vars, commands, API conventions, data formats, error codes. If facts come from code, types, OpenAPI, or schema, that source is authoritative; docs link or explain, not hand-copy a second full set.

**Operations** (`docs/operations/`): deploy, rollback, migration, backup/restore, troubleshooting, runbooks. One-off bug hunts stay in tasks/change records; promote only reusable conclusions.

## README

Every project README should cover: what it is, how to start, common commands, brief architecture, and deeper-doc links.

```markdown
# Project Name

One-paragraph description.

## Quick Start
...

## Commands
| Command | Description |
| --- | --- |

## Architecture
Brief overview and links to deeper docs or ADRs.
```

Adapt commands to the real stack. Do not invent npm-only instructions for non-JS repos. Add contributing guidance only if needed.

## API Documentation

For public APIs, library interfaces, and external contracts:

- Document parameters, returns, errors, and useful examples
- Prefer types, OpenAPI/Swagger, or another contract as source of truth
- Avoid multiple drifting hand-maintained copies
- Link the contract from README or `docs/index.md`

## Changelog

Maintain `CHANGELOG.md` only when releases need user-visible history. Record added/fixed/changed behavior that matters to users or integrators. Not a commit log or developer diary. Link tasks/releases only when that is local practice.

## Inline Documentation

Comment the *why*, not the *what*:

```text
Bad:  // increment counter
Good: // sliding window reset prevents edge bursts at fixed boundaries
```

Do not comment self-explanatory code, leave commented-out code, or restate signatures in prose. Prefer finishing work now over parking it as a TODO. If a TODO or FIXME must remain, state the blocker and, when the project supports it, link a tracked task. Source comments are not an untracked backlog. Document known gotchas next to the relevant code; link an ADR or long-lived doc for full rationale.

## Documentation Impact Mapping

Update long-lived documentation when a change alters a long-lived fact, contract, decision, constraint, or operating procedure.

| Change | Documentation to inspect |
| --- | --- |
| User-visible behavior | README, relevant design docs, changelog |
| Public API or interface | API reference/contract, examples, changelog |
| Configuration or environment variables | Reference, examples, deployment docs |
| Architecture or module boundaries | Architecture overview, possibly an ADR |
| Major dependency or expensive-to-reverse decision | ADR |
| Data model or migration behavior | Architecture, reference, migration/operations |
| Deployment, startup, backup, or recovery | Operations and runbooks |
| Repeated operational failure | Troubleshooting |
| Ordinary internal bug fix | Usually task, change record, and tests only |
| Internal refactor with no external/architectural change | Usually no long-lived doc update |
| Release | Changelog when maintained |

Not every code change needs a documentation change.

## Agent Workflow

### Before

1. Read README and the documentation entry point.
2. Find related architecture, design, ADR, reference, or operations docs.
3. Check code and tests; do not trust docs alone.
4. Search for existing coverage before creating anything.
5. Confirm sources of truth and local conventions.

### During

Update long-lived docs only when user-visible behavior, public interfaces, config, architecture boundaries, durable constraints, deployment/operations, or important design decisions change. Temporary exploration, rejected paths, and ordinary debugging stay out of long-lived docs. Durable decisions go to ADRs; task-only detail stays in the task or change record.

When a code change requires documentation updates, finish code and docs in the same change set. Do not knowingly leave docs wrong for later. If true synchronization is impossible, state the temporary inconsistency and open a tracked follow-up in the project's existing task system.

### Before completion

Confirm docs match code; check public behavior/interfaces, config, architecture/major dependencies, ADR need, deploy/rollback/troubleshooting impact, accidental one-off docs, link health, and cold-reader clarity.

### Handoff

In the normal task result, PR, or equivalent change record, state: changed, why, affected areas, verification, documentation impact, unresolved risks/follow-ups. Do not create `TASK_COMPLETE.md`, `IMPLEMENTATION_SUMMARY.md`, or `WORK_LOG.md`.

## Traceability

For important work, when the project has task/review/version links:

```text
task or issue ↔ design document ↔ ADR ↔ change record ↔ changelog entry
```

Major design docs link tasks/ADRs; ADRs may link triggering tasks and implementing changes; change records link tasks and modified design docs; changelog may link tasks/releases. Use existing link formats. Do not invent records to complete a chain. Ordinary small fixes do not need the full chain.

## Human Readability

State the reader question up front; overview before detail; define scope; use stable terms; navigate with headings/links; explain reasons, constraints, interfaces, and key flows; keep examples complete but lean; use diagrams for relationships and prose for meaning; avoid file-tree or class-list dumps; one primary reader question per doc; understandable without this chat. Do not impose one rigid template on every doc type.

## Anti-Proliferation

Unless already used by the project, do not create:

```text
TODO.md  DEBUG.md  DEVLOG.md  PROGRESS.md  NOTES.md
WORK_LOG.md  IMPLEMENTATION_COMPLETE.md  IMPLEMENTATION_SUMMARY.md
TASK_COMPLETE.md  STATUS.md
```

Route instead: TODOs/bugs/status → task system; process → VCS/change records; reusable troubleshooting → operations; decisions → ADRs; releases → changelog; durable knowledge → README/`docs/`.

Before creating any new Markdown file: is it long-lived? Does an existing place fit? Who reads it later? What is the source of truth? Will it duplicate? Is it a doc, ADR, or task record? If unclear, do not create it.

## Project Instructions

If the project already keeps agent or contributor instruction files, update durable conventions there only when that is local practice. This skill does not require creating those files, and they are not part of the default documentation system.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The code is self-documenting" | Code shows what, not why, rejected options, or constraints. |
| "We'll document when it stabilizes" | Durable contracts stabilize faster when written down. |
| "Nobody reads docs" | Future maintainers and agents do. |
| "ADRs are overhead" | A short ADR prevents re-litigating the same decision. |
| "Comments get outdated" | Why-comments are stable; what-comments rot. |
| "Every change needs a doc update" | Only long-lived facts, contracts, decisions, constraints, and procedures do. |
| "I'll leave a summary Markdown for the next agent" | Use the task or change record. |
| "Docs can catch up in a later PR" | If the change made docs wrong, update them in the same change set or open a tracked follow-up. |
| "Create the full docs tree now" | Empty trees rot. Grow docs with real content. |
| "This skill layout beats the repo's docs" | Existing consistent conventions win. |
| "Keep the outdated overview for history" | Current-state docs must be current; history lives in VCS and ADRs. |

## Red Flags

- Architectural choices with no rationale
- Public APIs or configs with no discoverable contract
- README that cannot get a newcomer running
- Architecture overview used as a decision diary
- ADRs that only restate implementation detail
- Multiple conflicting sources of truth
- Commented-out code instead of deletion
- Stale TODOs or FIXMEs used as an untracked backlog
- New `DEBUG.md` / `STATUS.md` / handoff dumps
- Docs that restate code or dump file trees
- Public behavior/interface changes without doc checks
- Code landed with knowingly stale long-lived docs and no tracked follow-up
- Contradictory current-state docs kept "for history"
- Empty `docs/` scaffolding "for completeness"

## Verification

- [ ] Existing conventions checked before defaults
- [ ] Long-lived docs match current code and behavior, or a tracked follow-up explains temporary drift
- [ ] Public interfaces, config, and user-visible behavior covered or intentionally unchanged
- [ ] Exact contracts still point at executable sources of truth
- [ ] Architecture overview is current state, not decision history
- [ ] ADRs exist or were updated for expensive-to-reverse choices; Accepted only with clear authority
- [ ] No duplicate, contradictory current-state, or one-off Markdown invented
- [ ] Temporary work stayed in tasks, reviews, or VCS history
- [ ] Remaining TODO/FIXME comments name blockers and link tasks when possible
- [ ] Operations/troubleshooting updated only for reusable knowledge
- [ ] Changelog updated only when the project ships that way and the change warrants it
- [ ] Links resolve; a cold reader can understand the result
- [ ] Known gotchas documented near relevant code when needed
