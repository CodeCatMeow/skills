# Research Documentation Examples

This page uses examples to show how information enters a research documentation system. The identifiers, paths, datasets, and values in these examples are instructional. Unless explicitly identified as a "real source," they are not results from any project. Every path after `Example path:` shows a naming convention only and must not be treated as a repository link.

Skill instructions, references, examples, CLI text, and initializer-generated index scaffolding are English, but bundled project-document templates and Agent-authored project research content default to Chinese unless the user explicitly requests another language. These examples remain English because they demonstrate the bundled English references, not because English is the default language for authored project output.

## Contents

- [README](#readme-an-entry-point-not-a-process-dump)
- [Status](#status-a-compressed-view-of-current-actions)
- [Roadmap](#roadmap-questions-and-sequence-not-fictional-progress)
- [Weekly Log](#weekly-log-facts-from-the-week)
- [Experiment Plan](#experiment-plan-define-the-comparison-before-running)
- [Report](#report-separate-observation-interpretation-conclusion-and-decision)
- [Knowledge](#knowledge-promoted-from-evidence-not-copied-slogans)
- [Pitfall](#pitfall-a-preventable-failure-not-blame)
- [ADR](#adr-record-a-decided-or-proposed-matter)
- [Protocol](#protocol-a-procedure-that-can-be-followed)
- [Claim-Evidence Map](#claim-evidence-map-make-claims-traceable)
- [Information Routing](#information-routing-put-the-same-fact-in-the-right-place)
- [Markdown and Quarto](#markdown-and-quarto-choose-the-format-for-the-need)
- [AI Boundaries](#ai-boundaries-organize-evidence-do-not-substitute-for-facts-or-approval)

## README: An Entry Point, Not a Process Dump

**Positive example**

```md
# Representation Learning Research Records

For current work, active experiments, and confirmed conclusions, see [status.md](./status.md).

- [Roadmap](./roadmap.md): questions, priorities, and milestones.
- [Experiments](./experiments/): plans and results for each comparison.
- [Weekly logs](./logs/): research process recorded by ISO week.
- [Knowledge base](./knowledge/): reusable conclusions with sources and scope.
```

The entry point tells readers where to begin and what each location is responsible for. Its links use resolvable relative paths.

**Negative example**

```md
# README

We have proven that auxiliary loss significantly improves performance on all tasks. Next week we might try more things.
```

**Why this is wrong**: The README mixes an unlocated conclusion, a tentative plan, and entry-point responsibility. "All tasks" has neither scope nor evidence.

**Rewrite**

```md
# Research Records

For current conclusions and pending work, see [status.md](./status.md).
Specific evidence about auxiliary loss belongs in the relevant experiment report; do not summarize a conclusion here before its evidence is locatable.
```

## Status: A Compressed View of Current Actions

**Positive example**

```md
## Current Status

- In progress: organizing records for the three completed runs in EXP-20260731-aux-loss; raw metrics are in
  `artifacts/exp-014/metrics.csv`.
- Blocked: the data-split version awaits confirmation from the data owner; do not compare results across splits before confirmation.
- Next: write locatable runs into the report's Observation section, then request human review of the interpretation.
- Recent change: the process record for 2026-W31 is in [the weekly log](./logs/2026/2026-W31.md).
```

**Negative example**

```md
## status

- 2024: read papers
- 2025: ran several experiments
- Current: the model is good and has been human-reviewed
- TODO: continue
```

**Why this is wrong**: Accumulated history obscures the current state. "The model is good" is not actionable. AI has no authority to mark an item as "human-reviewed."

**Rewrite**

```md
## Current Status

- Current conclusion: no conclusion across data splits yet.
- Pending confirmation: the data-split version and interpretation; human-review status is "not human-confirmed."
- Next: create a claim-evidence map for locatable results.
- History: earlier work has moved to `logs/` and `experiments/`; Example path.
```

## Roadmap: Questions and Sequence, Not Fictional Progress

**Positive example**

```md
## M2: Confirm the Applicability Conditions of Auxiliary Loss

- Question: with the main-task setting fixed, does the auxiliary-loss weight change the validation metric?
- Dependencies: confirmation of the data-split version, completion of the EXP-20260731-aux-loss plan, and a fixed evaluation script.
- Definition of done: locatable control runs, recorded limitations, and an owner decision on whether to enter the next stage.
- Excludes: changing data processing or the main model ad hoc to pursue a higher score.
```

**Negative example**

```md
## Q3

- Achieve SOTA
- All experiments succeed
- Write the paper
```

**Why this is wrong**: The goals are not verifiable, dependencies and completion criteria are absent, and "all experiments succeed" assumes unknown results as fact.

**Rewrite**

```md
## Candidate Q3 Milestone

Complete one pre-defined set of controlled comparisons and decide whether the evidence supports expanding the experimental scope.
```

## Weekly Log: Facts from the Week

**Positive example**

```md
# 2026-W31

## Completed

- Reviewed the metric definition in the plan for EXP-20260731-aux-loss; training was not started.
- Recorded the pending data-split question in status.

## Evidence and Blockers

- The data-version label has two candidate values, sourced from `data/manifest.json` and the run notes; no decision has been made.

## Next-Week Actions

- After the data owner confirms the version, organize existing run artifacts; do not invent results for missing runs.
```

The weekly log records daily process and links the associated EXP plan and, after an actual run, its report. It cannot replace the EXP directory, `plan.md`, or `report.md`, including for exploratory work.

**Negative example**

```md
# This Week

The model improved by 3%, the experiment is complete, and everyone should agree.
```

**Why this is wrong**: It has no ISO week identifier, comparison target, metric, source, or reviewer. It also presents assumed consensus as fact.

**Rewrite**

```md
# 2026-W31

No locatable metric file has been received. This week only completed plan review; "improved by 3%" cannot be written in the log or status.
```

## Experiment Plan: Define the Comparison Before Running

Every actually executed experiment, including an exploratory run and regardless of outcome, uses the same EXP system. At the start, associate the work with a related EXP directory or create one. One EXP collects related runs addressing one research question, not one seed or process. Create a new EXP only for a material change in the research question.

**Positive example**

```md
# EXP-20260731-aux-loss: Effect of Auxiliary-Loss Weight on a Validation Metric

- Question: with the model, data split, and training budget fixed, does `lambda=0.1` change the primary validation metric relative to `lambda=0`?
- Motivation: determine whether this pre-defined weight warrants a repeated comparison.
- Baseline/reference: `lambda=0`; planned change: `lambda=0.1`.
- Invariants: the same data version, training budget, evaluation script, and three pre-registered random seeds.
- Expected runs: one control and one treatment for each pre-registered seed.
- Planned configurations: Example path: `configs/exp-014/<condition>.yaml`.
- Execution status: not started.
- Report: create `report.md` immediately after the first actual run; no execution evidence exists yet.
- Primary metric: the three-run mean of the validation primary metric and each individual result.
- Decision criterion: report only the difference and variation in this setting; do not infer effectiveness on other tasks from three results.
- Risks and completion condition: the data-split version requires human confirmation before execution; complete after all expected runs are accounted for.
```

**Negative example**

```md
# New Experiment

Add auxiliary loss, try several parameters, and use whichever is highest. It will definitely work.
```

**Why this is wrong**: Variables, control, data, evaluation, and stopping scope are undefined. Selecting the highest value enables selective reporting, and the expected result is written as a conclusion.

**Rewrite**

```md
This formal comparison uses only the two pre-listed weights. Record any exploratory parameter search in an EXP plan and label its runs exploratory. If it answers the same research question, retain it in the same EXP while keeping its analysis distinct from the pre-declared comparison; create another EXP only if the question materially changes.
```

### Exploratory Run: Minimum Report After First Execution

Exploratory work is not kept only in the weekly log or copied back into the plan. It uses the same EXP system. After its first actual run, create a minimum `report.md`; leave genuinely unknown report fields blank rather than inferring them.

**Positive example**

```md
# EXP-20260731-aux-loss: Minimum Exploratory Report

- Plan: [plan.md](plan.md)

| Run ID | Status | Configuration or evidence location | Direct observation | Provisional interpretation | Continue, stop, or pivot rationale |
| --- | --- | --- | --- | --- | --- |
| run-021 | aborted after validation initialization | `configs/run-021.yaml`; Example path: `artifacts/exp-014/run-021/stdout.log` | The log ends before a metric is written. | Cause unknown; no performance interpretation is possible. | Stop this comparison and resolve the missing data-split metadata before another run. |
```

**Negative example**

```md
Tried `lambda=0.05`; it did not help, so it is not worth recording.
```

**Why this is wrong**: An exploratory run is omitted, its status and evidence are unavailable, and "did not help" claims an observation without a reference or metric.

**Rewrite**

```md
Keep the pre-execution design in `plan.md`. Record the aborted exploratory run and its unknowns in the related EXP's `report.md`, then link that report from the weekly log. Do not copy the run data into the plan or create another EXP merely because the run used a different seed.
```

### Repeated or Formal Work: Progressive Report Completion

For repeated comparisons, formal work, or evidence intended for a decision or paper, progressively complete the same report with all actual runs, configuration IDs, deviations, confounders, uncertainty treatment, reproduction information, and human-review status.

**Positive example**

```md
## Run List and Evidence Status

| Run ID | Seed | Condition | Status | Direct observation | Notes |
| --- | --- | --- | --- | --- | --- |
| run-031 | 11 | `lambda=0` | completed | metric in `metrics.json` | data split confirmed |
| run-032 | 11 | `lambda=0.1` | completed | metric in `metrics.json` | data split confirmed |
| run-033 | 17 | `lambda=0.1` | anomalous | metric is outside expected range | retain; investigate confounders |
| run-034 | 23 | `lambda=0.1` | no-gain | metric does not exceed baseline | retain in aggregation |

- Uncertainty: report individual values and the planned aggregation; do not remove `run-033` or `run-034` without a documented, reviewable rule.
- Reproduction: configuration paths and environment details are pending.
- Human review: interpretation not human-confirmed.
```

**Negative example**

```md
Only the best treatment run is included because the other runs were noisy or showed no improvement.
```

**Why this is wrong**: It removes anomalous and no-gain evidence, prevents review of confounders and uncertainty, and changes the evidentiary record to support a preferred narrative.

**Rewrite**

```md
Keep successful, failed, anomalous, aborted, and no-gain runs in the report. Describe a documented exclusion rule, any resulting uncertainty, reproduction status, and human-review status without claiming approval that has not occurred.
```

## Report: Separate Observation, Interpretation, Conclusion, and Decision

The following example uses a hypothetical auxiliary-loss scenario. Its values demonstrate format only and are not experiment data.

**Positive example**

```md
## Observation

Instructional example: if `metrics.csv` contains three control values of 0.70, 0.71, and 0.69, and treatment values of
0.72, 0.70, and 0.71, the report can state each value and its location in that file. The report must not replace this example
with a conclusion before real results are available.

## Interpretation

Provided that the identical settings have actually been verified, the treatment mean being higher may be associated with
the auxiliary loss. Three runs do not exclude random variation and do not establish reproduction on another data split.

## Conclusion

This hypothetical demonstration alone cannot form a project conclusion. Once real, locatable run artifacts are received, a
limited conclusion may be made about this specific setting.

## Decision

Do not change the default training configuration. First confirm the data version and have the owner review whether to expand
the number of repetitions.
```

**Negative example**

```md
Auxiliary loss improved accuracy from 70% to 71%, proving that it works, so enable it by default from today.
```

**Why this is wrong**: Observation, causal interpretation, general conclusion, and configuration decision are compressed into one sentence. Real sources, variation, conditions, and approval are missing.

**Rewrite**

```md
Observation: real run artifacts have not been supplied, so an improvement magnitude cannot be reported.
Interpretation: the effect of auxiliary loss remains a hypothesis to test.
Conclusion: there is no conclusion about the default configuration.
Decision: retain the current default and decide after real results and human review.
```

## Knowledge: Promoted from Evidence, Not Copied Slogans

**Positive example**

```md
# Training Stability: Fixed Comparison Conditions

Status: hypothesis awaiting reproduction.
Claim: when comparing loss terms, fixing the data split, training budget, and evaluation script can reduce unexplained differences.
Applicability: controlled comparisons within the same task.
Does not apply: performance extrapolation across datasets or model families.
Source: Example path: `experiments/2026/EXP-20260731-aux-loss/report.md`; an actual entry must replace this with an existing relative link.
```

**Negative example**

```md
# Knowledge

Auxiliary loss is always useful.
```

**Why this is wrong**: It has no evidence, conditions, scope, or evidence status, and promotes a local intuition into a rule.

**Rewrite**

```md
Status: awaiting verification.
Claim: whether auxiliary loss is beneficial depends on the task, weight, and training setting; controlled runs must provide evidence.
```

## Pitfall: A Preventable Failure, Not Blame

**Positive example**

```md
# Pitfall: Different Data Splits Mistaken for the Same Control

Trigger: run notes do not record the data-split version.
Symptom: metric differences for identical configurations cannot be explained.
Impact: the comparison cannot support a causal interpretation of the loss term.
Mitigation: record the split identifier in the plan and artifact metadata; when it is missing, mark the comparison as non-comparable.
Evidence status: root cause awaits human confirmation.
```

**Negative example**

```md
# Mistake

Someone ran the experiment incorrectly. Be more careful next time.
```

**Why this is wrong**: Blame replaces reusable information. There are no trigger conditions, impacts, or safeguards.

**Rewrite**

```md
Record the process gap and its verifiable impact; do not record unverified personal attribution.
```

## ADR: Record a Decided or Proposed Matter

**Positive example**

```md
# ADR-20260731-report-format: Markdown Is the Default Report Format

Status: proposed; awaiting owner approval.
Context: current reports are primarily prose, tables, and links, with no controlled execution or multi-format rendering requirement.
Options: Markdown; Quarto.
Recommendation: use Markdown while retaining the option to migrate an individual report when a rendering need exists.
Consequences: reports do not execute code automatically; figures must be referenced from generated, locatable artifacts.
Review trigger: repeatable computation, chart generation, or multi-format output becomes necessary.
```

**Negative example**

```md
# ADR

AI approved that everyone switch to Quarto.
```

**Why this is wrong**: AI cannot substitute for owner approval. Context, options, consequences, and status are missing.

**Rewrite**

```md
Status: proposed; human review is incomplete. AI may organize options but must not write "approved."
```

## Protocol: A Procedure That Can Be Followed

**Positive example**

```md
# Protocol: Archive Metrics from Completed Runs

Prerequisites: the run has ended; `run-id`, data version, and metric file exist.
Input: the run directory and its experiment identifier.
Steps:
1. Confirm that the metric file is readable and record its relative path.
2. Transcribe raw metric values and units without changing the aggregation method.
3. List missing metadata as a blocker; do not infer a default value.
4. Link the source in the report Observation and record the organizing action in the weekly log.
Checkpoint: another reader can trace from the report to the same metric file.
Failure handling: if the file is missing or versions conflict, stop archival and record the pending confirmation.
```

**Negative example**

```md
Collect the results and make the nicest-looking table.
```

**Why this is wrong**: Inputs, sequence, checkpoints, and failure handling are absent. "Nicest-looking" can invite selective presentation.

**Rewrite**

```md
Present all eligible runs according to pre-declared rows, columns, and aggregation rules. Explain anomalous runs in a separate field; do not silently remove them.
```

## Claim-Evidence Map: Make Claims Traceable

**Positive example**

```md
| Claim | Evidence | Limitation | Status |
| --- | --- | --- | --- |
| This comparison uses the same data split | `artifacts/exp-014/run-*/metadata.json` | metadata needs sample verification | awaiting human confirmation |
| The treatment mean is higher in this setting | `artifacts/exp-014/metrics.csv` | only three runs; do not extrapolate | awaiting report review |
| Enable auxiliary loss by default | none | the first two items are not yet reviewed | no decision |
```

The first two columns state which evidence supports which claim. The third prevents over-interpretation, and the fourth makes clear that the human process is incomplete.

**Negative example**

```md
| Conclusion | Evidence |
| --- | --- |
| The new method is better | experiment results |
```

**Why this is wrong**: "Experiment results" cannot be located. "Better" lacks a metric, scope, and comparison condition.

**Rewrite**

```md
| Claim | Evidence |
| --- | --- |
| Pending confirmation: whether the treatment primary metric exceeds the control | actual relative path, run identifier, metric column, and aggregation rule |
```

## Information Routing: Put the Same Fact in the Right Place

Scenario: this week, the data-split version was found to be unrecorded, and EXP-20260731-aux-loss has not yet run.

**Positive routing**

- Write in current `status`: the data version is a blocker and the next action is to confirm it.
- Write in the weekly log: when it was found, which material was inspected, and that no experiment ran.
- Write in the EXP-20260731-aux-loss plan: list the data-split identifier as a run prerequisite.
- If this issue has repeatedly created non-comparable results, then write a pitfall. Otherwise, do not create a general entry prematurely.

**Negative routing**

- Write the entire investigation process in the README.
- Write "the result is poor" in the report.
- Write "every experiment requires human review" in the knowledge base.

**Why this is wrong**: Process facts pollute the entry point, results, and reusable knowledge respectively. It also inflates one unconfirmed issue into a general rule.

## Markdown and Quarto: Choose the Format for the Need

**Positive Markdown example**: a report only needs to reference generated PNG files, list a real metric table, explain limitations, and link a plan. Use `.md` because it does not require code execution or rendering.

**Positive Quarto example**: a defined analysis report must compute tables and figures from a versioned CSV and output HTML and PDF. The project already has Quarto configuration, an executable environment, and a person responsible for rendering. Use `.qmd` and fix input paths and execution conditions in the document.

**Negative example**: convert an ordinary weekly log to `.qmd`, add unexecuted Python cells, then claim that a chart came from this week's experiment.

**Why this is wrong**: Format complexity does not serve the need; unexecuted cells cannot produce evidence.

**Rewrite**: keep the weekly log as `.md` and link only real figure artifacts. Adopt `.qmd` for that analysis report only when a repeatable analysis and supported rendering need actually exist.

## AI Boundaries: Organize Evidence, Do Not Substitute for Facts or Approval

Scenario: the user provides a summary of a real metric CSV but does not provide the data version or an owner review record.

**What AI may do**

```md
- Organize user-provided rows into Observation according to the established aggregation rule.
- Mark "data version not provided" and "human review incomplete."
- Draft questions awaiting confirmation and a claim-evidence map.
```

**What AI may not do**

```md
- Run training to fill missing repetitions.
- Guess the data version or generate plausible-looking metrics.
- Write "reproduced," "the owner agrees," or "human review passed."
- Overwrite existing status, weekly logs, or reports to make documentation appear complete.
```

**Rewrite version**

```md
Observation: values have been organized from the summary supplied by the user; the original file path and data version remain to be supplied.
Interpretation: before the version is confirmed, the comparison can be a lead but not controlled evidence.
Conclusion: do not form a configuration conclusion yet.
Decision: ask the owner to provide the version identifier and complete review; keep the review status as "not human-confirmed."
```

The shared requirement across these examples is to preserve the evidence chain, fact boundaries, and human responsibility. Documentation can help research progress, but it cannot substitute for execution, validation, or approval.
