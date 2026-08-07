# Composition: Config Groups and Defaults List

Source: https://hydra.cc/docs/advanced/defaults_list/

```text
Config Groups  →  Defaults List  →  Output Config  →  CLI overrides
```

## Config Groups

```text
configs/
├── config.yaml
├── model/{baseline,big}.yaml
├── data/{cifar,imagenet}.yaml
└── trainer/default.yaml
```

Create a group only when the project actually switches options on that axis.

```text
# Good axes: model, data, optimizer, loss, trainer
# Bad: single never-overridden file "for symmetry"; one-key YAML explosion
```

## Defaults List

```yaml
# configs/config.yaml
defaults:
  - model: baseline
  - data: cifar
  - trainer: default
  - _self_

seed: 0
```

- Defaults List is not part of the ordinary output fields.
- Forms: `some_config`, `group: option`, `optional local: default`,
  `override group: other`, `group: null`.
- Paths use `/` on all OSes; absolute paths start with `/`. No `..` traversal.

## Composition order

1. Last config wins on conflicts; dicts merge.
2. By default the **containing config body** overrides groups from its defaults
   (`_self_` auto-appended last when omitted).

```yaml
# body wins (default)
defaults:
  - db: mysql
db:
  host: backup

# groups win over body
defaults:
  - _self_
  - db: mysql
```

## Overrides

```yaml
# in another defaults entry
defaults:
  - override server/db: sqlite
```

```bash
python train.py model=big
python train.py +experiment=no_aux   # add group not already in primary defaults
python train.py ~server/apache       # remove
```

## Packages

Nested groups compose nested output. Experiment files under `experiment/` that
must change top-level keys use `# @package _global_` and absolute overrides
(`override /model: big`).

Defaults List interpolation exists but is restricted; prefer explicit experiment
configs unless the project already uses specializing-config patterns.

## Inspect

```bash
python train.py --info defaults-tree
python train.py --info defaults
python train.py --cfg job
python train.py --cfg job --resolve
```

Use these when migrating, debugging unexpected values, or reviewing an experiment.

## Minimal example

```yaml
# config.yaml
defaults:
  - model: baseline
  - data: cifar
  - _self_
seed: 0
```

```bash
python train.py                 # baseline + cifar
python train.py model=big
python train.py --cfg job
```

| Bad | Good |
| --- | --- |
| 800-line YAML per experiment | groups + composition |
| Defaults order copied blindly | deliberate `_self_` placement |
| Guess final config from memory | `--cfg` / `--info` |
| Parallel non-Hydra config beside Hydra | one source of truth |
