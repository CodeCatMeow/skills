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

Treat unknown recipient context as absent. Local paths and experiment IDs support
traceability but do not substitute for evidence the external reader needs to see.

## Deliver a few directly usable files

Prefer one or two upload files, chosen by content rather than experiment count.

- Use `analysis.txt` for text and small numerical comparisons. Write plain text
  with simple section labels, without relying on Markdown rendering. A small
  text-only update can be delivered directly in chat if the user prefers.
- Use one compact `report.pdf` when text, plots, images, or many experimental
  comparisons are easier to review together. Combine relevant experiments in the
  same document. Integrate analysis beside its evidence rather than duplicating
  the report in TXT and PDF.
- Add a consolidated `metrics.csv` only when detailed numerical reanalysis needs
  it. Combine compatible experiment records using experiment and condition columns;
  do not create one CSV per experiment. Explain units, fields, and missing values
  briefly in the main report. Large time series belong here rather than in pages
  of PDF tables when the actual values are needed.

Deliver TXT/PDF and any necessary CSV directly, without a ZIP or package hierarchy.
For PDF, use readable, selectable text and tables, labeled figures, and compact
layout. Omit covers, contents pages, and decorative filler. Compactness means less
repetition and wasted space, not tiny labels or illegible plots.

## Preserve evidence, compress repetition

Keep original data, configurations, logs, and images intact in their existing
locations. Select the evidence relevant to the requested discussion rather than
re-exporting the entire archive. Process large source files programmatically;
inspect relevant records and computed results instead of dumping full JSON or logs
into the conversation.

Separate observations, interpretations, and supported conclusions. Connect key
claims to experiment IDs, relevant configuration differences, and supplied data
or figures. Preserve numerical precision in exported data and explain any
filtering or aggregation. Retain relevant failed runs, anomalies, counterexamples,
and uncertainty; mark unavailable evidence explicitly.

Analyze important patterns and competing explanations in enough depth for the
external reader to challenge them. Include the specific questions that remain
open. Present evidence independently of the proposed explanation so cross-checking
does not depend on accepting that explanation first.

State shared background and settings once. Let a table or figure carry its data;
use prose for implications rather than repeating every value. Choose length by
the evidence and questions, with no minimum word, token, or page count. Keep the
same factual material when preparing the report for multiple external models.

## Check and hand off

Check numerical agreement with sources, evidence references, important omissions,
and repeated content. For PDFs, inspect both text extraction and rendered pages
for reading order, clipped tables, and unreadable labels.

Finish with the files to upload, their sizes, the covered experiment and data
counts, and any important evidence not included. State the source-data size when
readily available, and label token estimates as estimates. Leave delivery to the
user; report preparation does not authorize contacting external models or running
additional experiments.
