---
name: research-code-organization
description: >
  Organize long-running ML or research Python code when the user explicitly invokes
  this skill or asks to clean duplicated experiment launchers, permanent experiment
  flags, or an established script graveyard. Ordinary experiment implementation
  does not trigger project-wide reorganization.
argument-hint: "[research code organization task]"
user-invocable: true
disable-model-invocation: true
---

# Research Code Organization

Reduce experiment-code duplication with stable entrypoints, reusable implementation,
and configuration-defined variants. Adapt the smallest useful part of this pattern
to the existing repository.

## Route each kind of change

| Change | Durable home |
| --- | --- |
| Parameter value or runtime option | existing configuration or CLI override |
| Ablation or selectable behavior | configuration plus a clear component boundary |
| Reusable model, loss, data, or evaluation logic | a module owned by that domain |
| Different training control flow | a strategy or equivalent implementation selected by the training entrypoint |
| Different lifecycle or command | a separate entrypoint such as train, evaluate, or export |

Keep a small number of commands whose meaning is stable. Configuration identifies
an experiment; modules implement reusable ideas; entrypoints identify distinct jobs.
Use concept names such as `focal_loss.py` rather than chronology such as
`loss_v3_final.py`.

Existing project boundaries take precedence. A flat layout can remain flat while it
is clear, and a new abstraction should correspond to a present variant or
responsibility.

## Explore, then decide

An uncertain idea may begin as an isolated flag, notebook cell, or scratch script.
After useful evidence exists:

- promote a kept idea into the appropriate module or strategy and select it through
  configuration; or
- remove a rejected idea, relying on version control for history.

Keep the scientific change visible by separating unrelated cleanup. When structural
debt blocks the requested experiment, repair only that boundary and explain why it
was necessary.

## Migrate an established script graveyard

For several overlapping `train_*.py` or `model_v*.py` files, first inventory their
actual behavior. Classify differences as parameters, reusable implementation,
training control flow, or separate lifecycle. Establish a shared path incrementally,
verify that important previous runs remain expressible, and retire redundant paths
after parity.

Read [references/migration.md](references/migration.md) when performing this
migration. It is unnecessary for ordinary placement decisions.

## Consider Hydra only for real composition pressure

Hydra can help when configuration variants multiply and model × data × loss ×
trainer combinations are difficult to express with the current system. Ask before
installing or migrating, and use the dedicated Hydra skill for syntax. A small or
nearly finished project can keep its current configuration approach.

Finish when the requested variants are expressible through clear, stable paths and
the migration has not widened beyond the user's problem.
