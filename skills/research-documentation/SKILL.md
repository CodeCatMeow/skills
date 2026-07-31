---
name: research-documentation
description: Use when initializing a research/documentation system; updating research status or ISO-week logs; planning or reporting experiments; preserving research knowledge, pitfalls, ADRs, protocols, or paper evidence; organizing research Markdown; routing research information; or locating research context. Do not use for ordinary code fixes, experiment execution, non-research READMEs, Quarto syntax alone, translation, or general project management.
argument-hint: "[task or research document]"
user-invocable: true
disable-model-invocation: false
---

# Research Documentation

## Purpose

Maintain a lightweight, durable, searchable, traceable research-documentation system for long-running projects and AI collaboration. The core system uses only Markdown and the filesystem. It does not run experiments, judge novelty, or replace experiment platforms, version control, or specialist publishing tools.

The system helps researchers and agents re-enter a project, locate evidence, understand prior decisions, and identify the next action. It is not a way to make a directory look complete.

## Core Rules

- Write Skill instructions, references, CLI text, and initializer-generated index scaffolding in English. Keep bundled project-document templates in Chinese. Agent-authored project research content, including logs, status, plans, reports, knowledge, decisions, and protocols, defaults to Chinese. If the user explicitly requests another language, follow that request and localize headings as well as content.
- Record facts, observations, interpretations, conclusions, and decisions separately. Do not invent missing data, conceal failed runs, or represent speculation as evidence.
- Every executed experiment needs a traceable `EXP` record, whether exploratory or formal and regardless of outcome. Create or associate its EXP directory and `plan.md` when the experiment starts, before results appear useful.
- One EXP groups runs that answer the same research question. Create a new EXP only when that question materially changes. Preserve successful, failed, anomalous, aborted, and no-gain runs.
- Start every experiment with a `plan.md` containing the design information known before execution. After the first actual exploratory run, create a minimum `report.md` immediately. For other executed work, create or update the single report in Markdown or, when the existing Quarto criteria apply, Quarto. Leave genuinely unknown report fields blank, then progressively complete the report as the work becomes comparative, decision-relevant, formal, or paper-facing.
- Weekly logs may link to experiment records, but never replace them.

## Decide Before Writing

Classify research information by responsibility before writing it. Do not append everything to a log.

| Information | Primary location |
| --- | --- |
| Current question, effective baseline, active work, blockers, near-term actions | `research/status.md` |
| Daily work, provisional ideas, temporary observations, one-off context | Current ISO-week log |
| A defined research question, pre-execution design, expected runs, and evaluation criteria | Experiment `plan.md` |
| Actual runs, statuses, evidence, results, analysis, conclusions, and decisions | Experiment `report.md` or `report.qmd` |
| Relatively stable knowledge reusable across sessions and experiments | `research/knowledge/` |
| A recurring problem worth preventing | `research/knowledge/pitfalls/` |
| A durable choice and its trade-offs | `research/decisions/` |
| A method that must be performed consistently | `research/protocols/` |
| Paper claims, evidence, limits, and review status | Optional `research/paper/` |

Evidence and knowledge may be promoted progressively:

```text
Temporary idea -> weekly log -> experiment plan -> experiment report -> stable knowledge -> paper evidence
```

Keep the original timeline. After promotion, leave a short summary and link at the original location. Logs and experiments may also directly create a pitfall, ADR, or protocol when that better matches the responsibility. Read the [document system](references/document-system.md) for directory roles, routing, naming, and maintenance rules.

## Start Work

1. Inspect existing documents, project conventions, and user requirements. Reuse a mature structure that already has clear responsibilities; do not force it into the default layout.
2. For research context, read `research/README.md` and `research/status.md` first. If they do not exist, locate the existing documents with equivalent roles.
3. Retrieve only relevant knowledge, decisions, protocols, pitfalls, and experiment reports. Use filenames, directories, search terms, and existing links before reading all logs, experiments, or `research/`.
4. Identify the primary source, evidence state, and smallest necessary change. When material is duplicated, summarize and link instead of copying it.
5. Preserve historical context when editing existing files. Do not overwrite incompatible documents or bulk-move and rename files without a migration map.

Read [workflows](references/workflows.md) for task procedures. Read [examples](references/examples.md) when deciding wording or identifying anti-patterns.

## Fact and Judgment Boundary

Distinguish these levels in research documents:

1. **Fact or data**: Directly from a file, experiment platform, or user input, with a locatable source.
2. **Observation**: Directly visible in data, a figure, a log, or a run record.
3. **Interpretation**: A possible explanation of an observation, including alternatives and uncertainty.
4. **Conclusion**: What the current evidence supports, with its scope.
5. **Decision**: What to do, defer, or stop next based on that evidence.

Do not reconstruct numbers from memory, fabricate missing metrics, hide failed runs, selectively omit unfavorable results, treat one seed as a stable pattern, write correlation as causation, or state a hypothesis as confirmed fact. Leave unavailable fields blank and name the required source instead of inventing content to fill a template.

AI may organize evidence, show uncertainty, raise questions for confirmation, and draft documents. It does not own research conclusions or human review. Do not label any document "human-reviewed," "approved," or an equivalent status unless the user supplies an explicit human-review result.

## Task Routing

### Initialize Research Documentation

Inventory the existing structure first. Create only missing entry points with a clear role. A minimal initialization may create `research/README.md`, `status.md`, `roadmap.md`, the current weekly log, and short indexes for experiments, knowledge, decisions, and protocols. Do not pre-create `paper/`, experiment instances, `figures/`, `tables/`, or future weekly logs.

You may use `scripts/init_research_docs.py` to create a missing skeleton. It is a convenience, not a dependency. Confirm the target project root and never use it to overwrite existing files. By default, reject redirected research roots; use `--allow-redirected-research-root` only when the user explicitly intends that redirected location.

### Record Research Work

Locate the current ISO-week log at `research/logs/YYYY/YYYY-Www.md`. For each date, record goals, completed work, direct observations, problems, provisional interpretations, temporary decisions, related resources, and next steps. Remove or leave empty sections that do not apply. Do not manufacture conclusions. Synchronize current information that remains important across weeks into `status.md`, and promote reusable material according to its evidence state. Link each executed experiment to its EXP record; do not use the weekly log as its record.

### Update Current Status

Read the current status, recent logs, and directly relevant documents. Preserve active information, move historical process elsewhere, and distinguish confirmed facts, provisional judgments, unverified items, blockers, and three to seven priority actions. `status.md` is a compact snapshot. When it materially exceeds about 100 to 200 lines, extract content by responsibility rather than splitting it mechanically.

### Create or Associate an Experiment Record

When an experiment starts, create or associate `research/experiments/YYYY/EXP-YYYYMMDD-short-slug/` and its `plan.md` immediately. Use one record for related runs answering the same research question, including exploratory runs. Use a new record only if the question materially changes. `short-slug` uses lowercase ASCII letters, digits, and single hyphens.

Keep `plan.md` as the primary source for information known at experiment start: the research question, motivation, change, baseline, invariants, hypothesis, expected runs, evaluation criteria, risks, completion conditions, and planned configurations. It may contain a brief execution status and links to the report or run evidence, but not actual run data, observations, interpretations, conclusions, or decisions.

After the first actual exploratory run, create a minimum `report.md` immediately. For other executed work, create or update the single `report.md` or, when the Quarto criteria below apply, `report.qmd`. Record at least the run ID, run status, configuration or evidence location, direct observation, provisional interpretation, and rationale to continue, stop, or pivot. Keep all actual outcomes in that report, including successful, failed, anomalous, aborted, and no-gain runs. As the experiment becomes comparative, decision-relevant, formal, or paper-facing, progressively add the complete run inventory, confounders, uncertainty, reproduction, and human-review information. Do not maintain `report.md` and `report.qmd` as competing primary sources, create one EXP per seed or minor parameter variation, or run experiments as part of this Skill.

### Organize an Experiment Report

Use only locatable real data, run records, figures, or user-confirmed information. Create `report.md` after the first actual run and keep it as the primary source for actual run IDs, statuses, evidence locations, results, observations, interpretations, conclusions, and decisions. Record data completeness plus failed, anomalous, aborted, and no-gain runs. Separate observations, interpretations, conclusions, and decisions, and state conclusions the evidence cannot support.

Use `report.md` for simple results, existing figures, and analyses that do not require executable code. Consider `report.qmd` when structured data must be analyzed or used to generate figures or complex tables, when cross-references are needed, or when producing formal HTML, PDF, or Word output. Installing Quarto alone is not a reason to use `.qmd`.

### Preserve Knowledge, a Pitfall, a Decision, or a Protocol

- Keep temporary issues in weekly logs; put stable, reusable understanding in topical knowledge.
- Record a recurring problem with an unclear cause, error-prone fix, or prevention need as a pitfall.
- Record a durable choice that affects later work as an ADR, including alternatives, rationale, trade-offs, and consequences.
- Record repeatable work with defined inputs and outputs that requires consistent execution as a protocol.

### Organize Paper Claims and Evidence

Create or update `research/paper/` only when the project is preparing a paper. For every claim, record a Claim ID, exact wording, supporting experiments, counterexamples or limitations, corresponding figures, evidence state, risks, and human-review state. Link to experiment reports and original evidence rather than copying complete results. Preserve unsupported and partial claims; do not hide counterexamples for a paper narrative. Read [workflows](references/workflows.md) for the procedure.

### Organize Existing Documents

Inventory responsibilities, duplicates, conflicts, stale material, fragments, and links before changing structure. Provide a mapping from old to target locations. Work by topic and repair links as you go. Mark stale content with its status and replacement; do not silently delete it. Split only for independent responsibility, citation needs, or lifecycle, not a fixed line count. Keep one-off errors, tiny todos, brief notes, and single runs in logs or existing topical documents.

## Single Source and Links

Maintain one primary source for each class of information. Keep complete metrics in an experiment platform or structured export; documentation records the question, necessary results, analysis, stable identifiers, and links. Do not manually duplicate parameters, run data, motivation, or conclusions across pages.

When related content already exists, add a necessary summary and a relative link. After moving a file, check inbound links, outbound links, and indexes. Retain historical rationale for superseded knowledge, pitfalls, decisions, protocols, reports, and paper claims; mark them `superseded` and link to the replacement.

## Load Resources as Needed

- [document system](references/document-system.md): Directory responsibilities, information lifecycle, format selection, naming, single-source, language, and maintenance rules.
- [workflows](references/workflows.md): Initialization, logs, status, experiments, promotion, organization, and layered retrieval procedures.
- [examples](references/examples.md): Positive and negative examples, rewrites, routing, Markdown/Quarto choices, and AI-boundary cases.
- [`templates/`](templates/): Choose one template for the current document role. Remove inapplicable sections; never invent content to fill it.
- `scripts/init_research_docs.py`: Use only to safely create a missing minimal skeleton and current weekly log.

Do not load every reference or template by default. Read only what the current decision and deliverable need.

## Work with Other Skills and Tools

### SwanLab

When a SwanLab Skill is available and the task needs real experiment information, use it to query or confirm run IDs, projects, groups, metrics, logs, or figure data. Do not recall metrics from memory or rewrite the SwanLab API in this Skill. Mark unavailable data as missing. Without SwanLab, continue maintaining Markdown from existing project evidence.

### Quarto

When a Quarto authoring Skill is available and a report genuinely needs complex presentation, this Skill owns report responsibility, evidence structure, and writing boundaries; the Quarto Skill owns syntax, execution, rendering, numbering, and layout. Do not convert ordinary documents to `.qmd` or initialize all of `research/` as a Quarto site.

### Other Tools

Reference Hydra, MLflow, W&B, DVC, and similar tools only as sources of configurations, runs, or data. Preserve stable identifiers and needed links. Do not duplicate complete configuration, teach their full APIs, or make them a core dependency.

## Scope Boundary

This Skill does not run training or experiments, change model architectures, choose research directions, judge paper novelty, perform statistical significance tests, publish reports, or replace experiment platforms, version control, or Quarto. It does not create hooks, CI, databases, document scorers, research-conclusion adjudicators, quality gates, or evaluation frameworks.

Do not over-trigger this Skill for ordinary code fixes, only running training, only querying an experiment-platform API, only writing Quarto syntax, ordinary non-research READMEs, general code formatting, or translation without research knowledge-management needs.

## Completion Check

1. Content is in its correct primary source and can be found from entry points and related documents through relative links.
2. Current status, timeline, experimental design, executed-experiment evidence, stable knowledge, durable decisions, and repeatable procedures do not mix responsibilities.
3. Every experiment has an EXP and `plan.md` created or associated at its start; after its first actual run it also has a minimum report that preserves every outcome without duplicating actual run data in the plan.
4. Facts, observations, interpretations, conclusions, and decisions are distinct; important claims have sources, conditions, or missing-data markers.
5. Bundled project-document templates and Agent-authored project research content use Chinese unless the user requests another language; Skill instructions, references, CLI text, and initializer-generated index scaffolding remain English.
6. No numbers are fabricated, failures hidden, evidence selectively presented, conclusions overstated, or human review claimed without authorization.
7. Summaries and links avoid duplicating full parameters, data, tables, or conclusions.
8. Long documents are distilled by responsibility, small material is not over-split, and superseded content retains history and a replacement link.
9. Changes to an existing project are incremental and compatible, without unnecessary bulk moves, overwrites, or empty directories.
10. Markdown or Quarto is selected by reporting need, and external tools remain optional integrations.
