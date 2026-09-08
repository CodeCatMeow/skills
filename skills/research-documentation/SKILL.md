---
name: research-documentation
description: >
  Create or update a durable research note or report when the user explicitly asks
  for one. Consolidate current state in the closest existing note or research.md.
  Experiment execution, code changes, and metric queries alone do not trigger
  documentation work.
argument-hint: "[research note or report]"
user-invocable: true
disable-model-invocation: false
---

# Research Documentation

Preserve research context when it will influence a decision, prevent repeated
investigation, support reproduction, or contribute to a formal report.

## Maintain one useful current note

Inspect existing notes first and update the closest suitable file. When the user
wants research state persisted and no suitable file exists, start with one
`research.md`.

Capture only what a future reader needs:

- the current question or claim;
- decision-relevant evidence and its source;
- uncertainty or competing explanations; and
- the next experiment or decision.

Create another file when the content has an independent, durable purpose. Update
notes at meaningful checkpoints rather than treating each run as a documentation
event.

## Record evidence proportionately

A separate experiment note is worthwhile when a run is expensive,
decision-relevant, difficult to reproduce, likely to be cited, or specifically
requested. Link to the project's run ID, tracker, configuration, and artifacts as
the authoritative details; summarize the evidence that affects the research
question.

Label observed results, interpretation, and uncertainty distinctly. Preserve failed
or anomalous results when they change the conclusion or prevent wasted repetition.
Leave unavailable evidence unknown rather than filling gaps by inference.

## Choose Markdown or Quarto

Use Markdown for ordinary notes, reasoning, status, and static figures. It is the
default because it is quick to open and easy to maintain.

Use Quarto (`.qmd`) when the report itself should execute analysis to produce tables
or figures, or when citations, cross-references, or formal HTML, PDF, or Word output
matter. A report that only embeds an already generated image gains little from QMD.

Short analysis used only by one report can live in QMD. Put complex or reusable
logic in a Python module and let the report call it. Use a dedicated Quarto skill
for Quarto syntax and rendering details.

Finish when the important question, evidence, uncertainty, and next action can be
recovered from the smallest useful set of notes.
