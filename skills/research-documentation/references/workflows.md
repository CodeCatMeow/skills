# Research Documentation Workflows

## Contents

- [Layered Discovery Before Work](#layered-discovery-before-work)
- [Initialize or Complete the Structure](#initialize-or-complete-the-structure)
- [Record the Current ISO Week Log](#record-the-current-iso-week-log)
- [Update Status and Move Historical Detail](#update-status-and-move-historical-detail)
- [Create and Maintain an Experiment Record](#create-and-maintain-an-experiment-record)
- [Prepare a Report from Real Data](#prepare-a-report-from-real-data)
- [Promote Knowledge](#promote-knowledge)
- [Record Pitfalls, ADRs, and Protocols](#record-pitfalls-adrs-and-protocols)
- [Organize Paper Claims and Evidence](#organize-paper-claims-and-evidence)
- [Tidy Existing Disorganized Documentation](#tidy-existing-disorganized-documentation)
- [Boundaries and Completion Criteria](#boundaries-and-completion-criteria)

## Layered Discovery Before Work

Before writing, build the minimum sufficient understanding of the existing documentation. Search from nearby to distant and from authoritative sources to narrative sources:

1. Locate the research root and read `research/README.md` and `research/status.md`; if either is absent, find and read the existing documents that serve the same entry-point and current-status responsibilities.
2. Inspect the target directory, parent indexes, and project naming conventions to confirm the target document's authoritative source and responsibility.
3. Search task keywords, experiment IDs, dataset versions, metric names, and relevant decisions. Read directly relevant plans, reports, knowledge entries, protocols, pitfalls, or recent weekly logs as needed.
4. For facts that could affect a conclusion, trace back to raw data, experiment run records, figure-generation scripts, or formal reports. Do not substitute a secondary summary for evidence.
5. Expand the search only when local material is insufficient. When expanding, state the gap instead of filling it with speculation.

The purpose of layered discovery is not exhaustive reading. It is to avoid recreating facts, decisions, or structures that already exist. Failure to find something means only that it was not found within the searched scope; it does not prove that it does not exist.

## Initialize or Complete the Structure

Initialization starts with inventory, not template generation. Inspect existing directories, indexes, naming, archival practices, and recent updates, then create only the files or directories that are both missing and required for the current work.

Recommended sequence:

1. List the existing structure and identify which locations already serve the `status`, experiment, report, knowledge, or decision responsibilities.
2. Reuse existing locations and names. If a necessary location is missing, create the smallest layer of structure needed and explain its purpose in an adjacent index.
3. Add missing sections to existing files instead of overwriting them with a complete template.
4. Optionally use a script for repetitive scaffolding, but the script must check whether a target exists, refuse to overwrite by default, and generate only items with an explicit purpose.

Minimal initialization may create `experiments/`, `knowledge/`, `decisions/`, and `protocols/` with short indexes, plus the current ISO week log. These entry points give information a clear home from day one. Do not pre-create `paper/`, individual experiment directories, `figures/`, `tables/`, future-week directories, or other categories with no actual content. Script-generated scaffolding does not represent research progress and must not contain fabricated status, experiments, or conclusions.

## Record the Current ISO Week Log

The weekly log records facts from the week, evidence locations, blockers, and subsequent actions. Use the ISO week-based year and week number rather than the ordinary calendar year. For example, early January 2026 can still belong to the preceding ISO week-year. Obtain the actual value from a system date tool, then name the file `YYYY-Www`, for example `2026-W31.md`.

For each update:

1. Confirm the current ISO week identifier and whether that week's file already exists.
2. If the file exists, append or revise the relevant entry for the week without copying existing content. If it does not exist, create the week's log only when it is actually needed.
3. Record verifiable facts: completed documentation work, data versions used, run identifiers, reviewed material, discovered blockers, and their evidence locations.
4. Link every experiment-related entry to its associated `EXP-.../plan.md` and, after any actual run, its report. The weekly log records day-to-day process; it cannot replace either the plan or report.
5. Synchronize conclusions that remain valid across weeks to `status` or the appropriate long-lived document. Keep only the week's context in the weekly log.

A weekly log must not claim that an experiment is complete unless real, locatable run artifacts exist. When no run occurred, record "plan written," "awaiting data," or "not executed," rather than inventing results. Exploratory experiments belong in the same EXP system as all other experiments; record the exploratory work in the weekly log as process and link to its EXP record.

## Update Status and Move Historical Detail

`status` is a compressed view of the current actionable state, not an ever-growing chronological log. Before every update, read the existing status and retain constraints, current decisions, next steps, and blockers that remain true.

Update steps:

1. Identify obsolete current items and facts that still affect subsequent choices.
2. Write the new current state as short statements and link to real primary sources. Instructional example: `experiments/2026/EXP-20260731-aux-loss/report.md`; an actual status page must replace this with an existing relative link.
3. Move superseded but still traceable background, former hypotheses, and process details to the appropriate weekly log, experiment plan, report, or historical section.
4. Check that the status page does not retain mutually contradictory "current conclusions" and "next steps."

Moving information is not deleting history. The status page may retain a one-line historical pointer, but detailed process must have a definite home. Unknown or pending human-review items must retain that status. AI must not independently mark something as "human-reviewed," "approved," or "reproduced."

## Create and Maintain an Experiment Record

Every actually executed experiment, including exploratory, failed, anomalous, aborted, and no-gain runs, must be documented in the same EXP system. At the start of work, associate the work with an existing related EXP directory or create `experiments/YYYY/EXP-YYYYMMDD-short-slug/` and its `plan.md`. One EXP groups related runs that answer one research question, not one seed, process, or invocation. Create a new EXP only when the research question changes materially.

Before a run, define the pre-execution design in `plan.md`: question, motivation, planned change, baseline, invariants, hypothesis, expected runs and configurations, evaluation criteria, risks, and completion conditions. The plan may contain a brief execution status and links to the report or run evidence, but actual run IDs, statuses, evidence, results, observations, interpretations, conclusions, and decisions belong only in the report. Link the EXP to existing roadmap, status, knowledge, decisions, or prior experiments where applicable. Documentation work itself does not run experiments.

After the first actual exploratory run, create a minimum `report.md` immediately. For other executed work, create or update the single `report.md` or, when the Quarto criteria apply, `report.qmd`. The minimum report record is:

- Run ID.
- Run status.
- Configuration or evidence location.
- Direct observation.
- Provisional interpretation.
- Continue, stop, or pivot rationale.

Unknown report fields may remain blank. Do not move exploratory execution evidence solely to a weekly log or copy it into `plan.md`. The weekly log records the daily process and links the EXP; it cannot replace either the plan or report.

For repeated comparisons, formal work, or evidence intended for a decision, report, or paper, progressively complete the report with:

- Actual run inventory: configurations, seeds, repetitions, statuses, deviations, artifact locations, and all successful, failed, anomalous, aborted, and no-gain outcomes.
- Data and scope: source, version or snapshot identifier, selection rules, actual coverage, and boundaries against extrapolation.
- Metrics and analysis: primary and secondary metrics, aggregation, direct observations, interpretations, conclusions, and decisions.
- Confounders and uncertainty: known confounders, missing metadata, anomalies, uncertainty treatment, conflicting evidence, and limitations.
- Reproduction and review: reproduction instructions or status, pending human-review items, who must confirm decisions, and the actual human-review status.

Keep all successful, failed, anomalous, aborted, and no-gain runs in the report. A run is not removed because it weakens a preferred narrative. A plan may contain command drafts, planned configuration locations, a brief execution status, and links to the report or evidence, but it must not become a second run record. AI may only organize run records supplied by the user. It must not execute training, download data, consume compute resources, or represent an unexecuted plan as a result.

## Prepare a Report from Real Data

A report may be prepared only from locatable real material: raw results, versioned data, run logs, tables, figures, or confirmed human records. First create a result inventory containing source paths, run identifiers, data versions, generation times, and missing items; only then begin the narrative.

Choose the format based on the deliverable:

- Use Markdown (`.md`) for stable reports that are primarily prose and lightweight tables and do not need executable computation or rendered outputs.
- Use Quarto (`.qmd`) only when the report needs controlled code execution, charts or complex tables generated from structured data, complex equations and cross-references, Quarto citations/numbering/frozen results, or formal HTML, PDF, or Word output. Before creating an executable or to-be-rendered report, confirm that the project has an available environment and a clear rendering owner.

Do not migrate ordinary records merely because `.qmd` looks more formal, and do not treat an unexecuted code block as a data source. In either format, keep these five statement types separate:

1. **Fact/Data**: Locate input facts in data sources, versions, run inventories, and raw records. Do not mix source metadata into analytical conclusions.
2. **Observation**: State what is directly visible from those facts, with values, units, conditions, and sources.
3. **Interpretation**: State what the observation may mean, including assumptions and limitations.
4. **Conclusion**: Summarize what can hold within the current evidence boundary.
5. **Decision**: State the action taken or deferred based on the conclusion, including an owner or review condition.

List missing data, failed runs, anomalous runs, aborted runs, no-gain runs, and conflicting results explicitly. Do not fill in values, draw nonexistent data, generalize a single run into a stable pattern, or describe correlation as causation.

## Promote Knowledge

Content in weekly logs and experiment reports does not automatically become knowledge. Promote only content that is reusable across contexts, sufficiently evidenced, and clear about its scope of applicability.

Promotion process:

1. Extract a candidate claim from specific records and link real sources.
2. Determine whether the candidate has been reused across sessions or experiments, will be repeatedly needed by new members or later agents, and state its conditions, counterexamples, or unknown boundaries.
3. Distinguish "relatively stable current understanding," "provisional heuristic," and "hypothesis awaiting reproduction." Observations from one run or one session normally remain in a log or experiment report.
4. Keep source links in the knowledge entry and add a brief forward link from the original record instead of duplicating the full history.
5. Revise or downgrade older entries as new evidence arrives; do not silently rewrite their evidence status.

A knowledge entry is not a collection of slogans. "Increasing auxiliary loss usually works" lacks task, weight range, data conditions, and evidence, so it is a hypothesis to test, not verified knowledge.

## Record Pitfalls, ADRs, and Protocols

The three document types serve different purposes and should not be mixed:

- **Pitfall** records a repeatably avoidable failure mode: trigger conditions, visible symptoms, root cause or known hypothesis, mitigation, evidence, and affected scope. It does not turn an isolated failure into a general law.
- **ADR (Architecture/Analysis Decision Record)** records an important decision that has been made or proposed: context, options, decision or recommendation, rationale, consequences, review triggers, and review status. An ADR is not a design draft, and AI cannot claim it has human approval.
- **Protocol** records a reproducible procedure: prerequisites, inputs, versions, ordered steps, checkpoints, expected observable outcomes, failure handling, and artifact locations. It must not contain unverified performance promises.

Each entry has one primary responsibility. Use real relative links when documents must be related. When a path is only instructional, write `Example path: docs/...` rather than a link that appears to be real.

## Organize Paper Claims and Evidence

Maintain `paper/` only after the project enters paper-preparation work. First read the paper outline, relevant knowledge, and directly relevant experiment plans and reports, then process every claim:

1. Assign a stable Claim ID and write precise text with a clear scope that evidence can support or refute.
2. Link supporting experiments, counterexamples, limitations, data, and corresponding figures. Do not copy complete report results into the mapping table.
3. Mark the status as `draft`, `partial`, `supported`, `unsupported`, `needs-review`, or an equivalent existing project status, and record human-review status separately.
4. When evidence conflicts or is insufficient, retain the claim and downgrade its status. Do not delete unsupported claims or failed results for the paper narrative.
5. When a claim is superseded, retain the original Claim and historical rationale and link to the replacement Claim.

`outline.md` describes what each section must convey and what material is still missing. `claim-evidence-map.md` maintains claims and evidence. `figure-plan.md` states which claim each figure supports, which data it uses, and which experiments are still missing. The three files summarize and cross-link only; they do not become a second primary source for experimental metrics or analysis.

## Tidy Existing Disorganized Documentation

When a directory is disorganized, first reduce the chance of accidental deletion and broken links, then improve discoverability. Bulk renaming, moving, and rewriting often loses context.

Recommended process:

1. **Inventory**: List documents, update times, owners where known, topics, evidence levels, duplicates, and clearly stale links.
2. **Map**: Create a mapping from old locations to target categories and mark each item retain, move, merge, archive, or pending confirmation. The mapping itself must be reviewable.
3. **Execute progressively**: Move or rewrite one topical cluster at a time. Retain historical documents or provide a clear redirect note. Address high-use and high-risk material first.
4. **Repair links**: After each move batch, check inbound and outbound relative links, indexes, and anchors. When a target cannot be confirmed, mark the link for repair; do not fabricate a target.
5. **Retain history**: Preserve the timing, original basis, and supersession relationship of old decisions. Remove a duplicate only when it is explicitly redundant, has no independent historical value, and its references have moved.

Tidy work is complete when a reader can find the current entry point and trace evidence and history, not when the directory merely looks neat. Do not create empty categories for symmetry or compress records with distinct meaning into ungrounded summaries.

## Boundaries and Completion Criteria

The completion criteria for documentation maintenance are that new or updated content has a clear purpose, facts are traceable, links resolve, current status and historical detail each reside in the right location, and no existing file is overwritten or experiment result fabricated.

Skill instructions, references, examples, CLI text, and initializer-generated index scaffolding are English. Bundled project-document templates and Agent-authored project research content default to Chinese unless the user explicitly requests another language. The English examples in this reference set demonstrate bundled English reference conventions; they do not change the default language for authored project output.

This workflow does not authorize autonomous experiment execution, code modification, data creation, external-system changes, data downloads, or consumption of research compute resources. It also does not authorize overwriting documentation or substituting for human approval. When a task requires real experiment information, use the relevant skill for read-only queries of established systems such as SwanLab. Complex reports may delegate execution and rendering details to the Quarto skill, while still following project permissions and user requirements. When evidence is missing, record the gap, required source, and person who must confirm it. That is more valuable than generating a conclusion that only appears complete.
