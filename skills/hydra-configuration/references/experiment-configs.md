# Experiment Configs

Source: https://hydra.cc/docs/patterns/configuring_experiments/

> Experiment configuration describes differences from the default configuration,
> not a full copy.

## Shape

```yaml
# experiment/aplite.yaml
# @package _global_

defaults:
  - override /db: sqlite

server:
  port: 8080
```

```bash
# primary defaults has no experiment group
python train.py +experiment=aplite
python train.py -m +experiment=aplite,nglite

# primary defaults has `- experiment: null`
python train.py experiment=aplite
python train.py -m experiment=aplite,nglite
```

| Primary defaults | CLI / multirun |
| --- | --- |
| no experiment group | `+experiment=name`, `-m +experiment=a,b` |
| `- experiment: null` | `experiment=name`, `-m experiment=a,b` |

Follow the project's primary Defaults List; neither form is universal.

## What belongs

Include only intentional deltas: group overrides, hyperparameter changes, feature
toggles, tags/names, seed if part of experiment identity.

```yaml
# Good (delta)
# @package _global_
defaults:
  - override /model: baseline
tags: ["ablation", "no_aux"]
model:
  aux_loss:
    enabled: false
```

```yaml
# Bad — full tree paste that hides the ablation
defaults:
  - override /model: baseline
  - override /data: cifar
  # ... every group ...
data: { ... entire tree ... }
model: { ... entire tree ... }
```

## CLI → named experiment

```bash
# temporary
python train.py model.dropout=0.3 trainer.lr=1e-4
```

```yaml
# configs/experiment/dropout03_lr1e4.yaml
# @package _global_
model:
  dropout: 0.3
trainer:
  lr: 0.0001
```

Promote when repeated, shared, paper/table-facing, or only recorded in shell history.

## Experiment vs component

| Concern | Where |
| --- | --- |
| New attention implementation | Python module + maybe `model/` group option |
| Choosing it for a study | experiment override |
| One-off lr try | CLI override |

Do not paste large architectures only inside experiment YAML.

## Inspect and multirun

Use the same `+experiment` / `experiment` form as the project's primary defaults:

```bash
# example when experiment is not in primary defaults
python train.py +experiment=no_aux --cfg job
python train.py +experiment=no_aux --info defaults
python train.py -m +experiment=baseline,no_aux seed=1,2,3

# if primary has `- experiment: null`, drop the `+`
# python train.py experiment=no_aux --cfg job
# python train.py -m experiment=baseline,no_aux seed=1,2,3
```

Do not glob every half-finished draft in `experiment/` by accident.

| Bad | Good |
| --- | --- |
| `experiment_full_v3.yaml` cloning defaults | 5–20 intentional lines |
| one file per seed only | sweep `seed=1,2,3` |
| silent default edits for a study | named delta; keep defaults stable |

## Ablation without a new launcher

```yaml
# experiment/no_attention.yaml
# @package _global_
defaults:
  - override /model: baseline
model:
  attention: identity
```

```bash
# no experiment in primary defaults → +experiment=...
# primary has `- experiment: null` → experiment=...
python train.py +experiment=no_attention
```

No `train_no_attention.py`.
