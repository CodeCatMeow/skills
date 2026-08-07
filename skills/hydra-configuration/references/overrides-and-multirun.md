# Overrides and Multirun

Sources:
- https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/
- https://hydra.cc/docs/patterns/configuring_experiments/

## CLI overrides

```bash
python train.py trainer.lr=3e-4 seed=1   # change existing
python train.py model=big                 # group option
python train.py +model.use_ckpt=true      # add new key
python train.py ~logger                   # remove

# primary defaults has no experiment group
python train.py +experiment=no_aux
# primary defaults has `- experiment: null`
python train.py experiment=no_aux
```

Match the form to the project's primary Defaults List. When unsure, read that
list or run `--info defaults`.

| Situation | Prefer |
| --- | --- |
| try lr once | CLI override |
| table row / shared ablation | experiment config |
| weekly baseline | default or named experiment |

## Multirun

```bash
python train.py --multirun db=mysql,postgresql schema=warehouse,support
python train.py -m x=range(1,4)

# primary defaults has no experiment group
python train.py -m +experiment=baseline,no_aux seed=1,2,3
python train.py -m '+experiment=glob(*)'

# primary defaults has `- experiment: null`
python train.py -m experiment=baseline,no_aux seed=1,2,3
```

```yaml
hydra:
  mode: MULTIRUN   # RUN | MULTIRUN (Hydra >= 1.2)
  sweeper:
    params:
      db: mysql, postgresql
```

- Default sweeper runs **locally and serially**.
- Builds the **Cartesian product** of axes.
- Composes configs **lazily at job launch** — do not edit shared YAML mid-sweep.
- Not scientific design; not Bayesian HPO by itself.
- Do not add Optuna/Ax/Joblib/Slurm plugins unless the user asks.

```bash
# Good — intentional axes (use +experiment or experiment per primary defaults)
python train.py -m +experiment=baseline,no_aux,attention seed=1,2,3

# Bad — accidental explosion
python train.py -m model=glob(*) data=glob(*) loss=glob(*) seed=1,2,3,4,5
```

Before large sweeps: estimate job count, inspect one config with `--cfg job`,
optionally smoke 1–2 jobs.

## Inspect

```bash
# +experiment or experiment — match primary Defaults List
python train.py +experiment=a --cfg job --resolve
python train.py --info defaults-tree
```

Reduce multirun surprises to a single job that reproduces the bad composition.

## Cheatsheet

```bash
python train.py trainer.lr=3e-4

# no experiment in primary defaults
python train.py +experiment=no_aux
python train.py -m +experiment=baseline,no_aux
python train.py -m +experiment=baseline seed=1,2,3
python train.py +experiment=no_aux --cfg job --resolve

# primary has `- experiment: null` (same commands without `+`)
python train.py experiment=no_aux
python train.py -m experiment=baseline,no_aux
```
