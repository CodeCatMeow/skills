---
name: research-handoff
description: >-
  Prepare research reports for external AI review only at the user's explicit
  request, within their specified scope. Deliver concise plain-text or compact
  PDF reports with traceable evidence and few upload files.
---

# Research Handoff

Prepare material the user will manually share with external AI models for research
discussion and cross-checking. Apply this workflow only when the user explicitly
requests such a report or invokes this skill for that purpose. Experiment runs,
code changes, and ordinary result discussions do not authorize report generation.

## Follow the requested scope

Use the experiments and discussion questions identified by the user. If the scope
is unclear, ask a focused question rather than expanding to the entire project.

- For a first introduction, supply the research goal, relevant method, evaluation
  setup, and prior findings needed to understand the requested scope. Include
  formulas or short implementation excerpts when the interpretation depends on them.
- For selected experiments or a current-run update, focus on those results and
  necessary comparisons. Use an incremental report when the recipient already has
  the earlier material; identify that material and explain additions and corrections.

Treat unknown recipient context as absent. Include the evidence needed to assess
claims directly in the report; the external reader cannot access the local project.

## Deliver a self-contained report

Default to one self-contained TXT or compact PDF containing the analysis and
necessary tables or figures. Choose by content rather than experiment count.

- Use `analysis.txt` for plain text and tables with simple section labels. A small
  text-only update can stay in chat if the user prefers.
- Use `report.pdf` for integrated text, tables, plots, and images. Combine relevant
  experiments and place analysis beside its evidence, without duplicating a TXT report.

Deliver files directly, without a ZIP or package hierarchy.
For PDF, use selectable text and tables, labeled figures, and compact layout without
covers, contents pages, or decorative filler. Keep labels and plots readable.

## Organize data before choosing its format

State shared settings, units, and field meanings once per relevant group. For
comparable results, put metrics such as mAP and R1 in adjacent columns of the same
row, rather than repeating experiment metadata for each metric. Retain the seed,
stage, dataset, or condition distinctions needed to interpret the comparison.

Choose representations by analytical role. When interpretation depends on trends,
distributions, stage relationships, or visual examples, include the relevant plots
or images. Preserve that visual structure rather than replacing it with long
numeric sequences or summary values alone. Pair visuals with precise key values
and short analysis: visual structure, numerical precision, and interpretation are
complementary, not redundant. Representations of the same data are not independent
experimental confirmations.

For scalar comparisons, prefer compact text tables; use grouped text or embedded
TOON inside the TXT when it reduces repetition without obscuring meaning. Changing
format alone is not data reduction.

Attach a consolidated CSV only when the user explicitly requests programmatic
reanalysis of substantial row-level data. Include the required records and fields,
not a flattened dump of every source. Otherwise, keep discussion-relevant values
and important anomalies in the report.

## Preserve evidence, compress repetition

Keep original data, configurations, logs, and images intact. Select evidence for
the requested discussion rather than re-exporting the archive. Process large files
programmatically and inspect relevant results instead of dumping full JSON or logs
into context.

Keep detailed provenance in existing local project records. Omit local path lists,
file hashes, and internal ID dictionaries from outgoing material unless requested.
Use descriptive experiment labels, relevant configuration differences, and actual
evidence rather than references the recipient cannot open.

Separate observations, interpretations, and supported conclusions. Tie key claims
to the experiments and tables or figures supplied in the report. Preserve numerical
precision and explain any filtering or aggregation. Retain relevant failed runs,
anomalies, counterexamples, and uncertainty; mark unavailable evidence explicitly.

Analyze important patterns and competing explanations deeply enough to challenge
them, and identify open questions. Present evidence independently of the proposed
explanation so other models can assess it on its merits.

State background once. Remove repeated exposition and point-by-point narration
that adds no understanding, while retaining complementary visual and numerical
evidence. Let the evidence and questions determine length, with no minimum word,
token, or page count. Give different external models the same factual material.

## Check and hand off

Check numerical agreement with sources, evidence references, and important omissions.
Inspect the actual delivery content for repeated metadata, inaccessible references,
and unhelpful duplication; a small file count does not establish compactness.
For PDFs, inspect text extraction and rendered pages for reading order, clipped
tables, and unreadable labels.

In the delivery reply, list upload files, sizes, experiment and data counts, and
important evidence not included. Give source-data size when readily available;
label token estimates. Leave delivery to the user; this workflow does not authorize
contacting external models or running additional experiments.
