# Research Documentation System

This reference defines the default directory model, document responsibilities, information routing, and long-term maintenance rules. It is a responsibility model, not a migration requirement: adopt parts of it incrementally only where an existing project lacks a clear equivalent role.

Skill instructions, references, CLI text, and initializer-generated index scaffolding are written in English. Bundled project-document templates are written in Chinese. Agent-authored project research content, including logs, status, plans, reports, knowledge, decisions, and protocols, defaults to Chinese. If the user explicitly requests another language, follow that request and localize headings as well as content.

## Directory Model

```text
research/
|- README.md
|- status.md
|- roadmap.md
|- logs/
|  `- YYYY/
|     `- YYYY-Www.md
|- experiments/
|  |- README.md
|  `- YYYY/
|     `- EXP-YYYYMMDD-short-slug/
|        |- plan.md
|        |- report.md or report.qmd
|        |- figures/               # as needed
|        `- tables/                # as needed
|- knowledge/
|  |- README.md
|  |- architecture.md              # as needed
|  |- data.md                      # as needed
|  |- evaluation.md                # as needed
|  `- pitfalls/
|     `- descriptive-name.md
|- decisions/
|  |- README.md
|  `- ADR-YYYYMMDD-short-name.md
|- protocols/
|  |- README.md
|  `- descriptive-name.md
|- paper/                          # create only during paper preparation
|  |- outline.md
|  |- claim-evidence-map.md
|  `- figure-plan.md
`- templates/                      # optional project-specific templates
```

Minimal initialization creates entry points, current status, a roadmap, the current weekly log, and needed indexes. Do not create `paper/`, experiment instances, `figures/`, `tables/`, future weekly logs, or empty topical documents. Keep raw data, complete metrics, reproducible intermediate data, and plotting code in their existing authoritative locations; reference them from research documents through stable identifiers and links.

If using `scripts/init_research_docs.py`, confirm the target project root and do not overwrite existing files. The initializer rejects redirected research roots by default. Use `--allow-redirected-research-root` only when the user explicitly intends the redirected location.

## Document Responsibilities

### `research/README.md`

**Responsibility**: Explain how to use the documentation system and provide navigation.

Include purpose, directory responsibilities, information routing, naming, Markdown/Quarto selection, status and experiment/knowledge entry points, maintenance principles, and optional tool integrations. Exclude daily progress, a full conclusion for one experiment, complete hyperparameters, temporary todos, and long research background unrelated to navigation.

Use the [research README template](../templates/research-readme.md).

### `research/status.md`

**Responsibility**: Provide a compact snapshot of current project state and the primary re-entry point for researchers and agents.

Include last update, current core question, effective baselines, active work, confirmed facts, provisional judgments, unverified items, blockers, the three to seven most important actions, and links to relevant experiments, knowledge, and decisions. State evidence status explicitly; avoid non-actionable wording such as "generally good" or "continue optimizing."

Keep it near 100 to 200 lines. Move historical process to logs, complete results to experiment reports, and stable understanding to knowledge; retain only summaries and links. Use the [status template](../templates/status.md).

### `research/roadmap.md`

**Responsibility**: Record medium-term goals, relationships among research questions, and the stage plan.

Include the overall goal, core questions, workstreams or research branches, stage milestones, dependencies, stop or pivot criteria, current priority, and connections to experiments or paper claims. It is not a daily task list and should not say "change code today" or "run something tomorrow." Use the [roadmap template](../templates/roadmap.md).

### `research/logs/YYYY/YYYY-Www.md`

**Responsibility**: Preserve the research timeline, temporary observations, and daily context.

Use one file per ISO week by default, with a level-two heading per date. A date section may contain goals, completed work, direct observations, issues, provisional interpretations, temporary decisions, related resources, and next steps. Remove empty sections. Split only when the week becomes large and separate responsibilities emerge; do not default to one file per day or an ever-growing total log.

Logs record what was known at the time and must not be rewritten later as more certain conclusions. Keep links when content is promoted. Link experiment-related entries to the EXP plan and, after any actual run, its report. A weekly log cannot replace either document. Use the [weekly log template](../templates/weekly-log.md).

### Experiment Directories and IDs

Use `EXP-YYYYMMDD-short-slug`, for example `EXP-20260731-no-aux-loss`. The `short-slug` uses lowercase ASCII letters, digits, and single hyphens. One EXP directory represents related runs that answer one research question. Do not create a separate directory for every seed, training process, or minor parameter variant.

Every experiment that is actually run, exploratory or formal and regardless of outcome, must have a traceable EXP record. Create or associate the EXP directory and `plan.md` when the experiment starts, before any result looks useful. Preserve successful, failed, anomalous, aborted, and no-gain runs. Start a new EXP only when the research question materially changes.

#### `plan.md`

**Responsibility**: Be the primary source for information known before or at experiment start: why the experiment is being run, what will change, what will remain fixed, and how it will be assessed.

Include the experiment ID, research question, motivation, planned change, baseline or reference, important invariants, pre-experiment hypothesis, expected runs and configurations, evidence that would support or refute the hypothesis, variables and controls, seed strategy, data and evaluation constraints, risks and confounders, completion criteria, and related knowledge, decisions, and earlier experiments. A plan may retain a brief execution status and links to the report or run evidence for navigation.

Do not maintain actual run IDs, actual run statuses, actual result data, direct observations, interpretations, conclusions, or decisions in the plan. Those belong to the report as their single primary source. Update the plan only when the intended design changes, and preserve material deviations in the report. Do not run the experiment here or state expected results as facts. Use the [experiment plan template](../templates/experiment-plan.md).

#### `report.md` or `report.qmd`

**Responsibility**: Be the primary source for information produced by execution: actual runs, evidence, results, analysis, uncertainty, conclusions, and decisions.

After the first actual exploratory run, create a minimum `report.md` immediately. For other executed work, create or update the single `report.md` or, when the Quarto criteria apply, `report.qmd`. At minimum, record the run ID, run status, configuration or evidence location, direct observation, provisional interpretation, and rationale to continue, stop, or pivot. Unknown fields may remain blank; do not copy these execution facts back into the plan or maintain competing Markdown and Quarto reports.

As the experiment becomes comparative, decision-relevant, formal, or paper-facing, progressively add the complete run inventory, experiment and report status, question and design summary, data sources, configuration or platform links, necessary tables and figures, completeness checks, failed, anomalous, aborted, and no-gain outcomes, competing interpretations, confounders, uncertainty, limits, conclusions, unsupported conclusions, decisions, follow-up experiments, reproducibility information, and human-review status.

Observations state only what data shows. Interpretations state possible mechanisms. Conclusions limit their evidence strength. Decisions state the next action. Never silently exclude failed or unfavorable results. Update human-review status only from explicit human input.

Use the [Markdown report template](../templates/experiment-report.md) or [Quarto report template](../templates/experiment-report.qmd).

### `research/knowledge/`

**Responsibility**: Preserve reasonably validated, stable knowledge that can be reused across sessions and experiments.

Organize by topic, such as architecture, data, evaluation, or loss design. Each document includes scope, current understanding, supporting evidence, practical implications, known limits, remaining uncertainty, related experiments and decisions, and last update. Knowledge is not a complete timeline; keep raw attempts in logs and reports.

"Stable" does not mean absolutely true. Update state and limits when evidence changes. Preserve the replacement relationship when superseded. Use the [knowledge note template](../templates/knowledge-note.md).

### `research/knowledge/pitfalls/`

**Responsibility**: Preserve issues likely to recur and worth preventing researchers or agents from repeating.

Each pitfall includes symptoms, context, root cause or root-cause status, ineffective handling, correct handling, prevention, related code/tests/experiments/decisions, and residual risk. Create a standalone note only for a recurring issue with a non-obvious cause, error-prone fix, or prevention need; leave one-off, low-value errors in logs. Use the [pitfall template](../templates/pitfall.md).

### `research/decisions/ADR-*.md`

**Responsibility**: Preserve choices that affect later work, including their context, rationale, alternatives, and cost.

Use IDs in the form `ADR-YYYYMMDD-short-name`. Use `proposed`, `accepted`, `superseded`, or `rejected` as status. Record context, the decision, alternatives considered, rationale, trade-offs, consequences, and replacement relationships. AI may draft a proposed ADR but may not mark it accepted itself. Use the [decision template](../templates/decision.md).

### `research/protocols/`

**Responsibility**: Record methods that must be repeated consistently, such as data checks, formal experiment launch, evaluation, reproduction, figure generation, or anomalous-run handling.

Include purpose, scope, preconditions, inputs, steps, expected outputs, common failures, recovery, version or environment assumptions, and related knowledge and decisions. A protocol states how to work; knowledge states what is currently known. Use the [protocol template](../templates/protocol.md).

### `research/paper/`

Create this directory only during paper preparation.

- `outline.md`: Paper question, sections, central message per section, missing material, and links to experiments and knowledge.
- `claim-evidence-map.md`: Each Claim ID, exact claim, supporting experiments, counterexamples or limits, corresponding figures, current state, risk, and human-review status. Prefer `draft`, `partial`, `supported`, `unsupported`, `needs-review`, or project-equivalent states. Retain superseded claims with a link to the replacement claim.
- `figure-plan.md`: Figure purpose, target claim, data source, needed experiments, status, and output location.

Do not remove unsupported claims or unfavorable evidence to improve a paper narrative. Mark a claim `unsupported`, `partial`, or unverified when evidence is insufficient instead of inventing support.

## Information Routing

For each new item, decide in order:

1. Does it describe the current question, effective baseline, active work, current blocker, important current fact, or priority action? Write it in `status.md`.
2. Does it describe today's work, a temporary idea, a one-off issue, daily context, or a question not yet formed into an experiment? Write it in the current weekly log.
3. Does it define a question to test, an ablation, a control, or an expected run group that is starting? Create or update its EXP `plan.md` immediately, even for exploratory work.
4. Does it come from the first or any later actual run, including status, evidence, results, observations, interpretations, conclusions, or decisions? Create or update that EXP report.
5. Is it reusable across sessions or experiments, essential for newcomers, likely to appear in methods, or repeatedly re-learned by agents? Distill it into topical knowledge.
6. Is it likely to recur, with a non-obvious cause, an error-prone remedy, or a prevention need? Write a pitfall.
7. Does it explain a durable choice, a rejected approach, alternatives, or trade-offs? Write an ADR.
8. Is it a repeatable procedure with defined inputs and outputs that different people must perform consistently? Write a protocol.
9. Is it a paper claim, supporting or opposing evidence, a corresponding figure, a limit, or review status? Write it in `paper/claim-evidence-map.md` or another paper document only during paper preparation.
10. If it cannot yet be classified, write it in the current weekly log and mark it for routing. Do not create an ambiguous standalone file.

An item may need a current summary plus a primary source, but maintain complete content in only one place. For example, state a blocker in `status.md` and link to the pitfall instead of copying its root-cause analysis.

## Information Lifecycle

The primary evidence and knowledge path is:

```text
Temporary idea -> weekly log -> experiment plan -> experiment report -> stable knowledge -> paper evidence
```

Logs and experiments may directly produce a pitfall, ADR, or protocol when their responsibilities call for it. These branches need not first pass through an experiment report or knowledge. Experiment reports and knowledge may both support a claim-evidence map.

Promotion distills rather than copies:

- Weekly logs preserve the timeline and contemporary uncertainty.
- Experiment plans preserve the question, hypothesis, and constraints at the experiment start.
- Experiment reports preserve executed runs and analysis, including all outcomes.
- Knowledge distills understanding that remains useful across contexts and links to reports.
- Claim-evidence maps connect paper claims to supporting and opposing evidence.

Not every item follows the entire path. A one-off issue may remain in a log. An observation with insufficient evidence should not become stable knowledge. Do not create paper documents before paper preparation.

## Markdown and Quarto

Use `.md` by default. Markdown suits status, roadmaps, weekly logs, knowledge, pitfalls, ADRs, protocols, experiment plans, and simple reports.

Consider `.qmd` only when there is a real need to:

- execute Python or R to produce results;
- dynamically generate figures or tables from CSV, JSON, or experiment-platform exports;
- use complex mathematics, figures, or cross-references;
- produce formal HTML, PDF, or Word output;
- publish an analysis report; or
- use Quarto citations, numbering, or frozen computation.

An existing Quarto environment is insufficient reason. Use `report.md` when figures already exist, the report is primarily prose with a few static tables, and no code must run. Without Quarto or its corresponding Skill, complete the Markdown work that is possible and state what cannot be rendered automatically.

## Single Primary Source

| Information | Primary source |
| --- | --- |
| Current state | `status.md` |
| Timeline | `logs/` |
| Pre-execution experiment motivation, design, expected runs, and planned configurations | Experiment `plan.md` |
| Actual runs, statuses, evidence, results, analysis, conclusions, and decisions | Experiment `report.md` or `report.qmd` |
| Stable understanding | `knowledge/` |
| Rationale for durable choices | `decisions/` |
| Repeatable methods | `protocols/` |
| Paper claims | `claim-evidence-map.md` |
| Complete experiment metrics | Experiment platform or structured export |

Elsewhere, write only a necessary summary and a relative link. Do not hand-copy full configurations, maintain the same manual table in multiple reports, or keep data, motivation, and conclusions in multiple competing "latest" files.

## Control Growth and Fragmentation

### Prevent Endless Appending

When a file grows too long, distill by responsibility instead of mechanically splitting it into `part1` and `part2`:

- Move historical progress to weekly logs.
- Move complete experiment analysis to reports.
- Move stable understanding to knowledge.
- Move durable-choice rationale to decisions.
- Move operational steps to protocols.
- Keep only current summaries and links in `status.md`.

### Prevent Over-Fragmentation

Do not create standalone documents for a one- or two-sentence temporary idea, a one-off low-value error, a tiny todo, an addition that naturally belongs in an existing topic, or a single seed run. Prefer the current weekly log or an existing topical document.

Split content only when it has an independent responsibility, will be cited repeatedly, needs an independent lifecycle, or is materially hurting the readability of an existing document. Do not split by fixed line count.

## Stale and Conflicting Content

Do not silently remove superseded knowledge, pitfalls, ADRs, protocols, reports, or paper claims:

- Mark `status: superseded`.
- State the replacement date and reason.
- Use `superseded_by` or an in-body link to the new document.
- Preserve the prior context and evidence so historical decisions remain understandable.

When content conflicts, do not choose the more appealing version. Locate each source and timestamp, mark the conflict, update the current primary source, and retain questions that require human confirmation.

## Incrementally Adapt Existing Projects

1. Inspect existing directories, entry points, naming, and link conventions.
2. Determine whether the structure already clearly serves state, timeline, experiments, knowledge, decisions, and protocol responsibilities.
3. Reuse existing documents first; address only the clearest responsibility confusion, duplication, broken links, or unbounded growth.
4. Before restructuring, provide a mapping from old to target paths and identify inbound links.
5. Move or distill small topic batches, repairing links and indexes after each batch. Do not rename or move many files at once.
6. Where an old file retains historical value, mark its replacement relationship instead of overwriting it.

Migration is complete when researchers and agents can reach current status, relevant evidence, and historical rationale from entry points, not when the directory exactly matches the default layout.
