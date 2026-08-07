# Migrating to Hydra

Migrate progressively. Ask before adding Hydra.

## Worth it when

- train scripts differ mostly by parameters
- YAML is copied and lightly edited per experiment
- model × data × loss combinations matter
- people want CLI overrides/multirun without more argparse

**Skip** when tiny, ending soon, mature non-Hydra system works, or user refuses.

Do **not** auto-introduce Lightning, Optuna, Slurm, W&B/SwanLab, full templates,
or Structured Configs for every leaf.

## Steps

1. **Stabilize one entrypoint.** Understand differences among train scripts first;
   Hydra alone does not fix pure copy-paste architecture.
2. **Collect real axes** (`model`, `data`, `optimizer`, `loss`, `trainer`, …).
   No speculative empty groups.
3. **Minimal primary config** + `@hydra.main(version_base=None, ...)`.
4. **Extract groups gradually:** move baseline option → defaults → `--cfg job` →
   then add a second option.
5. **Map argparse flags** (`--lr` → `trainer.lr=`, `--model big` → `model=big`).
6. **Historical runs → experiment deltas** with old → new command mapping.
7. **`instantiate` optional** if type-name factories already exist; plain
   `build_model(cfg.model)` is fine otherwise.
8. **Parity:** baseline + key ablations work; paths/chdir understood; then delete
   or thin-wrap old launchers.

Intermediate states are OK (Hydra baseline while old scripts still exist →
experiments ported → parameter-only scripts removed). Do not jump A→D in one PR.

## Paths at migration time

Prefer keeping `hydra.job.chdir=false` for existing relative paths. Set
`hydra.run.dir`, gitignore outputs. Do not change path semantics silently while
also changing composition.

## Anti-patterns

| Bad | Good |
| --- | --- |
| Paste Lightning-Hydra-Template wholesale | borrow ideas; minimal deps |
| One mega-PR | staged axes and experiments |
| Full-clone experiment files | deltas only |
| Multirun + Optuna on day one | single-run correctness first |
| argparse and Hydra dual forever | short dual-run, then cut over |
| Everything needs `_target_` | instantiate only where selection needs it |

## Thin end state

```text
configs/
  config.yaml
  model/{baseline,big}.yaml
  data/default.yaml
  experiment/{baseline,no_aux,big_model}.yaml
train.py
```

```bash
python train.py

# form depends on primary Defaults List:
# no experiment group     → +experiment=... / -m +experiment=...
# `- experiment: null`    → experiment=...  / -m experiment=...
python train.py +experiment=no_aux
python train.py -m +experiment=baseline,no_aux seed=1,2,3
python train.py +experiment=no_aux --cfg job --resolve
```
