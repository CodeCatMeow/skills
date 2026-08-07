# Project Structure

Preferred lightweight shape — not a mandatory scaffold. Inspect the repo first.

```text
project/
├── src/project_name/
│   ├── models/components/
│   ├── losses/
│   ├── data/
│   ├── training/strategies/
│   ├── evaluation/
│   └── utils/
├── configs/{model,loss,data,trainer,experiment}/
├── scripts/
├── notebooks/          # optional exploration
├── train.py
├── evaluate.py
└── pyproject.toml
```

Small projects can stay flatter (`models/`, `data/`, `configs/`, `train.py`).
Create packages when a second real member appears, not for aspirational layout.

## Entrypoints

| Good | Bad |
| --- | --- |
| `train.py`, `evaluate.py`, export helpers | `train_baseline.py`, `train_final_camera_ready.py` |

Entrypoints answer "what kind of job?" not "which paper table row?"

## Modules

| Package | Holds |
| --- | --- |
| `models/` | architectures, backbones, heads, blocks |
| `losses/` | loss functions and aggregates |
| `data/` | datasets, collate, samplers, augs |
| `training/` | loops, strategies, optim/sched helpers |
| `evaluation/` | metrics, evaluators |
| `utils/` | small shared helpers with no better home |

Prefer idea names (`focal_loss.py`) over versions (`loss_v3.py`). Do not dump
experimental models into `utils.py`.

## Configuration

Capture experiment identity and selectable implementations without forking code:

- hyperparameters, paths, runtime settings
- component selection
- named experiment deltas when supported

No specific config library is required. Follow the project's existing system;
do not create a second parallel config world. Do not invent empty groups "for
completeness."

## scripts/

```text
# Good                         # Bad
scripts/convert_dataset.py     scripts/run_baseline.py
scripts/inspect_checkpoint.py  scripts/run_final_v2.py
scripts/download_weights.py
```

If a script only changes training parameters, it should be a config or a
documented command to the stable train entry.

## Notebooks, tests, outputs

- Notebooks: fine for inspection and prototypes; promote before formal runs.
- Tests: optional focused checks; do not block research for an industrial pyramid.
- Outputs (`outputs/`, `logs/`, `runs/`): gitignore; do not commit checkpoints into `models/`.

## When to restructure

**Don't:** layout is unusual but consistent; project near completion; user asked
only for a small experiment.

**Do (narrowly):** multiple train scripts differ only by parameters; a component
is copied three times; new work requires choosing among dead entrypoints.

| Anti-pattern | Better |
| --- | --- |
| Empty packages everywhere | create when needed |
| Everything in `train.py` | extract as responsibilities appear |
| Parallel `src2/`, `old/` | migrate or delete |
