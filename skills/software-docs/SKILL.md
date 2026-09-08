---
name: software-docs
description: >
  Maintain long-lived software documentation when the user asks for documentation
  or when a change would make existing README, API, configuration, deployment, or
  operational guidance wrong. Routine implementation work whose documented
  behavior remains correct does not need this skill.
user-invocable: true
disable-model-invocation: false
---

# Software Docs

Keep durable documentation correct at the lowest maintenance cost.

## Decide the scope

Documentation work is useful when:

- the user requests a document or documentation update;
- user-facing behavior, a public interface, configuration, commands, deployment,
  or operations changed;
- an existing long-lived document would otherwise mislead its readers; or
- the project already records a consequential design decision and this change
  alters that decision.

A bug fix, test change, or internal refactor normally requires documentation only
when it changes one of those durable facts.

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
