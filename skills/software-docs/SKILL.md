---
name: software-docs
description: >
  Create, review, or substantially revise software usage guides, API documentation,
  or design documents when the user requests that deliverable. Routine code changes
  and research notes do not trigger this skill.
user-invocable: true
disable-model-invocation: false
---

# Software Docs

Keep durable documentation correct at the lowest maintenance cost.

## Scope

Work on the software documentation requested by the user. This includes usage
guides for research code; research questions, experiment evidence, and results
belong in research notes.

Correcting a known stale statement during a code change can stay part of that edit;
it does not require loading this skill or starting a broader documentation review.

## Update the closest document

1. Inspect the implemented behavior and the nearest relevant document.
2. Treat code, types, schemas, and checked-in configuration as the source of truth
   for exact technical facts.
3. Correct the smallest coherent section while preserving the project's language
   and organization.
4. Verify commands, paths, examples, links, and stated behavior.

Prefer purpose, constraints, usage, and non-obvious rationale over a narration of
the implementation. Point readers to authoritative schemas or generated reference
material when copying them into prose would create another source to synchronize.

Create a new file only when it has an independent, durable purpose, a clear future
reader, and no suitable home in the current documentation. Follow an existing
project convention when one exists. Keep temporary execution plans in the project's
task workflow unless the user asks to preserve them as documentation.

A design note is most useful for an expensive-to-reverse decision with meaningful
alternatives or migration, compatibility, security, or operational consequences.

Finish when the changed long-lived facts are correct and easy to find.
