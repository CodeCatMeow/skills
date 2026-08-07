# Migrating Messy Research Repos

Typical start:

```text
train.py / train_a.py / train_b_fix.py / train_final.py
model.py / model_v2.py / model_new.py
```

Do not begin by deleting everything or forcing a template.

## Flow

1. **Inventory** `train*.py`, shell wrappers, training notebooks, make targets.
2. **Diff behavior**, not filenames. Classify each difference:

   | Kind | Examples |
   | --- | --- |
   | Parameter | lr, batch size, seed |
   | Config surface | different yaml/argparse defaults |
   | Implementation | different model/loss/data path |
   | Lifecycle | train vs eval vs export |

3. **Find shared core** (data, model build, loop, eval hooks, checkpointing).
4. **Establish one stable train entry** (most complete current file or thin new
   `train.py`). Do not delete other entrypoints yet.
5. **Parameters → configuration**; document old → new commands.
6. **Reusable code diffs → components** + config selection (factory is enough).
7. **True control-flow diffs → strategies**; `train.py` stays the chooser.
8. **Verify expressibility** of baseline and important ablations.
9. **Delete** redundant launchers and dead `model_vN.py` after parity. Use Git;
   do not keep `train_final_old.py` "just in case" without a reproduction need.
10. **Stop regression:** README note to use `train.py` + configs; refuse new
    `train_*.py` unless lifecycle is truly new. No scoring services or heavy process.

## Micro-example

```text
# Before
train.py, train_focal.py, train_no_aux.py, model.py, model_attn.py

# After
train.py
configs/experiment/{baseline,focal,no_aux,attn}.yaml
models/{baseline.py,components/attention.py}
losses/{ce.py,focal.py}
```

Order: shared loop → selectable loss → aux toggle → attention component →
replace scripts with config commands → delete after verification.

## Hydra during migration

Suggest Hydra only when dominant pain is composition (small deltas, multiplying
combinations, diverging YAML/scripts, need for overrides/multirun). **Ask first.**

If a Hydra skill is available, hand off syntax there; this skill still decides
component vs experiment vs entrypoint. If the user declines, continue with the
existing config system.

Skip Hydra when the project is tiny, ending soon, already has a mature system,
or the user refuses.

## Anti-patterns

| Anti-pattern | Better |
| --- | --- |
| Big-bang rewrite before inventory | stage by slice |
| Delete scripts before parity | map old → new commands first |
| Keep all old scripts forever after parity | remove once expressible |
| Introduce Lightning/DVC/CI "while cleaning" | only on request |
| Template overlay without command mapping | preserve reproducibility |
