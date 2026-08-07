---
name: research-code-organization
description: >
  Organize and modify long-running ML/research Python code so experiments do not
  accumulate as train_xxx.py copies, model_v2 files, or permanent if-exp flags.
  Use when adding ablations, new models/losses/modules, training strategies,
  experiment entrypoints, cleaning a script graveyard, deciding config vs module
  vs entrypoint, promoting exploratory hacks, or refactoring research project
  structure. Do not use for research direction, result analysis, paper writing,
  SwanLab/Quarto tutorials, ordinary business CRUD, pure Python syntax help, or
  full Hydra syntax teaching.
---

# Research Code Organization

Prefer stable entrypoints + reusable implementation + configuration-defined
experiments over one Python launcher per experiment.

Inspect the existing project first. Reuse a clear local structure; do not force
a template onto a working codebase.

## Change routing

**Use when:** Creating files or branching core training logic.

| Change kind | Destination | Do not create |
| --- | --- | --- |
| Hyperparameter / ordinary parameter | configuration | `train_lr_1e4.py` |
| Ablation / feature toggle | config + component selection | `train_no_aux.py`, permanent `if exp_name == ...` |
| New reusable algorithm piece | module under models/losses/data/evaluation/training | `model_v2.py`, `model_final.py` |
| New training strategy | `training/strategies/` (or equivalent) + one train entry | one launcher per strategy variant |
| Different lifecycle/command | new entrypoint (`train`, `evaluate`, `export`, ...) | new entrypoint for baseline vs ablation |

```text
parameter value?                       -> config
same interface, different implementation? -> component + config selection
different training control flow?       -> strategy, keep train entry stable
different task lifecycle/command?      -> new entrypoint
unsure / one-off idea?                 -> exploratory hack, then promote or delete
```

More examples: [change-routing.md](references/change-routing.md),
[experiment-code-patterns.md](references/experiment-code-patterns.md).

## Stable entrypoints

**Use when:** Choosing layout or where to put a new command.

Preferred shape (not mandatory):

```text
project/
├── src/project_name/{models,losses,data,training,evaluation,utils}/
├── configs/{model,loss,data,trainer,experiment}/
├── scripts/          # utilities, not experiment launchers
├── train.py
├── evaluate.py
└── pyproject.toml
```

**Important:**

- Keep a small number of long-lived commands; express variants via config/components.
- `scripts/` is for dataset conversion, checkpoint inspection, export — not
  `run_baseline.py` / `run_final_v2.py`.
- If the project already has a clear layout, follow it.

Details: [project-structure.md](references/project-structure.md).

## Explore → promote or remove

**Use when:** Trying an idea whose value is still unknown.

```text
explore  →  validate  →  promote or remove
```

**Allowed while exploring:** temporary `if use_new_attention:`, hardcoded values,
notebooks, short-lived scratch scripts.

**When kept:** move into a named component/strategy, select via config, delete
the temporary branch and one-off launcher.

**When failed:** delete temporary code; rely on Git. Keep a failed path only for
active comparison, reproduction, or teaching value.

**Important:**

- During an experiment request, change only what the experiment needs. Note
  structural debt; do not rewrite unrelated code in the same change.
- History lives in Git, not permanent `if old_failed_experiment:`.

Details: [exploration-and-promotion.md](references/exploration-and-promotion.md).

## Scientific change vs engineering change

**Use when:** Implementing an ablation or experiment.

```text
# Bad — user asked only to disable aux loss
also change lr, rewrite evaluator, replace scheduler

# Good
disable aux via config/component
fix only the logging/schema break caused by that change
```

If extra behavior must change for the experiment to run, say so explicitly.

## Brownfield migration

**Use when:** Facing `train.py`, `train_a.py`, `train_b_fix.py`, `train_final.py`.

1. Inventory training entrypoints; diff what they actually change.
2. Separate parameter, implementation, and lifecycle differences.
3. Extract shared training logic; establish one stable train entry.
4. Move parameters into configuration; reusable diffs into components; control
   flow into strategies.
5. Verify important old behaviors remain expressible; then delete redundant launchers.

Do not rewrite the whole project in one pass.
Details: [migration.md](references/migration.md).

## When to suggest Hydra

**Use when:** Composition pain is real — parameters/variants multiply, YAML or
scripts differ only slightly, model×data×loss×trainer combinations matter, or
several `train_xxx.py` files are really config variants.

Ask before installing or migrating. Do not teach Defaults List / experiment YAML
here; if a Hydra skill is available, defer syntax to it. If the user declines
Hydra, keep organizing with the existing config system.

**Do not suggest** when the project is tiny, nearly finished, already has a
mature config system, migration cost exceeds benefit, or the user refuses.

## Common patterns

### Prefer config over launcher copies

```text
# Bad
train_baseline.py
train_no_aux.py
train_attention_v2.py
train_final_fix.py

# Good
train.py
configs/experiment/   # or project-equivalent variants
models/components/
```

### Prefer components over exp_name ladders

```python
# Bad
if exp_name == "exp1":
    ...
elif exp_name == "camera_ready":
    ...

# Good
# config selects component or toggle; training code uses a stable interface
```

### Prefer utilities in scripts/

```text
# Bad
scripts/run_baseline.py
scripts/run_final_v2.py

# Good
scripts/convert_dataset.py
scripts/inspect_checkpoint.py
```
