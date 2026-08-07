---
name: hydra-configuration
description: >
  Use Hydra correctly for Python config composition, Config Groups, Defaults
  List, experiment configs, CLI overrides, multirun, output directories, and
  hydra.utils.instantiate. Use when a project already uses Hydra, when creating
  or editing Hydra YAML, when migrating argparse/flat YAML to Hydra, or when
  debugging composition with --cfg/--info. Do not use for research direction,
  result analysis, code-structure governance without Hydra, Lightning/W&B/Optuna
  tutorials, or general non-Hydra Python work.
---

# Hydra Configuration

Hydra's value is **composition** (Config Groups + Defaults List + Overrides),
not "YAML instead of argparse."

Prefer group composition and experiment deltas over giant copied YAML trees.
Start simple; Structured Configs and plugins are optional upgrades.

## Minimal app

**Use when:** Adding Hydra or checking the basic shape.

```text
project/
├── configs/
│   ├── config.yaml
│   ├── model/{baseline,big}.yaml
│   ├── data/default.yaml
│   └── experiment/{baseline,no_aux}.yaml
└── train.py
```

```python
import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    ...

if __name__ == "__main__":
    main()
```

Only create Config Groups for dimensions that actually vary.

## Defaults List

**Use when:** Writing or debugging primary composition.

```yaml
# configs/config.yaml
defaults:
  - model: baseline
  - data: default
  - trainer: default
  - _self_

seed: 0
```

**Important:**

- Defaults List builds the output config; it is not itself a normal output field.
- Composition is ordered; later entries win; dicts merge.
- By default the containing config body overrides groups from defaults (`_self_`
  is appended last if omitted). Place `_self_` deliberately.
- Override a group from another defaults entry with `override`.
- CLI group override: `model=big`
- Inspect: `--info defaults-tree`, `--info defaults`, `--cfg job`

Details: [composition.md](references/composition.md).

## Experiment configs

**Use when:** Encoding a named ablation or repeated run.

```yaml
# configs/experiment/no_aux.yaml
# @package _global_

defaults:
  - override /model: baseline

model:
  aux_loss:
    enabled: false
```

```bash
# primary defaults has no experiment group
python train.py +experiment=no_aux

# primary defaults has `- experiment: null`
python train.py experiment=no_aux
```

**Important:**

- Follow the project's primary Defaults List; neither form is universal.
- Experiment files store **deltas from defaults**, not full replicas.
- Use `# @package _global_` when the file lives under `experiment/` but should
  modify the global config.
- Use absolute paths like `/model` when overriding groups outside `experiment/`.

Details: [experiment-configs.md](references/experiment-configs.md).

## CLI overrides vs named experiments

**Use when:** Choosing how to express a change.

| Need | Prefer |
| --- | --- |
| One-off try | CLI: `trainer.lr=3e-4 seed=1` |
| Repeated / shared / paper-facing run | `configs/experiment/` |
| Add a new key | `+path.to.key=value` |
| Remove a default | `~path` |

Do not rely on shell history as the only record of important experiments.

## Multirun

**Use when:** Sweeping intentional config axes.

```bash
# primary defaults has no experiment group
python train.py -m +experiment=baseline,no_aux seed=1,2,3

# primary defaults has `- experiment: null`
python train.py -m experiment=baseline,no_aux seed=1,2,3
```

Also: `hydra.mode=MULTIRUN`, `x=range(1,4)`, `schema=glob(*)`.

**Important:**

- Match `+experiment` vs `experiment` to the project's primary Defaults List.
- Multirun builds the Cartesian product of the axes you provide — keep grids small.
- Multirun is not experimental design and not automatic HPO.
- Do not add Optuna/Ax/Joblib/Slurm plugins unless the user explicitly needs them.
- Configs are composed lazily at launch; do not edit shared YAML mid-sweep.

Details: [overrides-and-multirun.md](references/overrides-and-multirun.md).

## Output / working directory

**Use when:** Paths, logs, or checkpoints misbehave under Hydra.

Each run gets a unique output dir with `.hydra/{config,hydra,overrides}.yaml`.

```python
from hydra.core.hydra_config import HydraConfig
out = HydraConfig.get().runtime.output_dir
```

**Important:**

- `hydra.job.chdir` defaults to **False** (Hydra >= 1.2). CWD usually stays at
  the original process directory. Do not force chdir on a repo-relative project.
- Output dirs are still created when chdir is false.
- Customize with `hydra.run.dir`, `hydra.sweep.dir`, `hydra.sweep.subdir`.
- Helpers: `hydra.utils.get_original_cwd()`, `hydra.utils.to_absolute_path()`.

Details: [runtime-and-output.md](references/runtime-and-output.md).

## `hydra.utils.instantiate`

**Use when:** Config should choose among implementations of a stable interface.

```yaml
model:
  _target_: my_proj.models.BaselineModel
  hidden: 256
```

```python
from hydra.utils import instantiate
model = instantiate(cfg.model)
```

**Important:**

- Good for models, losses, optimizers, datamodules with stable construction APIs.
- Recursive by default. Do not put `_target_` on every scalar-filled dict.
- Do not invent class wrappers solely to please Hydra.
- A plain `build_model(cfg.model)` factory is fine when that already works.

## Progressive migration

**Use when:** Moving from argparse / flat YAML / script copies.

1. Stabilize one entrypoint; collect real variation axes.
2. Minimal primary `config.yaml` + groups only for axes that vary.
3. Convert important historical runs into experiment deltas.
4. Verify with `--cfg job` / `--info defaults`; confirm old behaviors.
5. Remove redundant launchers only after parity.

Details: [migration.md](references/migration.md).

## Common patterns

```text
# Bad                              # Good
full config copy per experiment    delta experiment config
one giant flat YAML for all choices Config Groups + defaults
important runs only in shell history named experiment configs
blind Cartesian multirun           intentional axes, small grids
assume CWD is always the output dir check hydra.job.chdir / runtime.output_dir
everything uses _target_           instantiate only selectable implementations
auto-add Optuna/Slurm/Lightning    only when user needs them
```

## Documentation

- https://hydra.cc/docs/advanced/defaults_list/
- https://hydra.cc/docs/patterns/configuring_experiments/
- https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/
- https://hydra.cc/docs/tutorials/basic/running_your_app/working_directory/
- https://hydra.cc/docs/advanced/instantiate_objects/overview/
