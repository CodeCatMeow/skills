# Change Routing

Route first. Edit second.

```text
1. Only a parameter value?              -> configuration
2. Same component, different impl / on-off feature? -> config + component
3. New reusable algorithm piece?        -> module + config selection
4. Different training control flow?     -> strategy; keep train entry stable
5. Different task lifecycle/command?    -> new entrypoint
6. Short-lived idea?                    -> exploratory hack → promote or delete
```

Prefer the smallest sufficient durable abstraction.

Do not create a component when configuration alone expresses the change.
Do not force genuinely different behavior into configuration when a reusable
implementation component is required.
A change may legitimately require both a component and configuration selection.

## Hyperparameter

Examples: `lr`, `batch_size`, `epochs`, `weight_decay`, `dropout`, `seed`.

```text
# Bad
train_lr_1e4.py
train_bs64.py

# Good
# config or CLI override; no magic constants that define experiment identity
```

## Ablation / feature toggle

```yaml
# Good (project syntax may differ)
model:
  attention: none   # or baseline / relative / ...
loss:
  aux:
    enabled: false
```

```python
attention = build_attention(cfg.model.attention)
```

```text
# Bad
train_no_aux.py
if exp_name == "no_aux": ...
```

Temporary flags are fine while exploring. Durable alternatives become components.
Avoid a permanent forest of `if cfg.use_x` / `if cfg.hack_from_tuesday`.

## New component

```text
# Good
models/components/relative_attention.py
losses/focal_loss.py
data/samplers/balanced_batch_sampler.py

# Bad
model_v2.py
model_final_fix.py
copy of entire trainer with three lines changed
```

| Situation | Route |
| --- | --- |
| Same family, different width/depth | config parameters |
| Same interface, different backbone | component + config group |
| Breaks shared interface / different task | new module and/or strategy review |

## Loss / metric / data

| Situation | Route |
| --- | --- |
| Weight, temperature, label smoothing | config |
| New loss formula | `losses/` + selection |
| Loss needs teacher forward / loop change | may also need strategy |
| Metric threshold / top-k | config |
| New metric implementation | `evaluation/` |
| Different eval protocol or export | may be separate entrypoint |
| path, split, batch size | config |
| new aug/sampler | data component + config |
| one-off convert/download | `scripts/` |

Do not fork `train.py` only to log one extra metric.

## Training strategy

Use when **control flow** differs (continual, distillation, multi-stage, alternating),
not when only hyperparameters differ.

```text
# Good
training/strategies/supervised.py
training/strategies/distill.py
train.py   # selects strategy from config

# Bad
train_supervised.py
train_distill_v2.py
```

## New entrypoint

Valid: `train.py`, `evaluate.py`, `export_embeddings.py`, `generate_pseudo_labels.py`
(and `pretrain.py` only if pretrain is a distinct durable command).

Invalid reasons: baseline, ablation, different lr/model, "final" / "camera ready".

## Examples

| Request | Route |
| --- | --- |
| Turn off auxiliary loss | config toggle (+ stable loss interface) |
| Try lr 3e-4 for a day | temporary CLI/config override |
| Add relative attention vs baseline | component + config selection |
| Add knowledge distillation | strategy; keep `train.py` |
| Export embeddings | new entrypoint / eval script |

## Anti-patterns

| Anti-pattern | Better |
| --- | --- |
| `train_*.py` per idea | stable `train.py` + config/experiment |
| `model_vN.py` copies | components + selection |
| `if exp_name == ...` ladder | config-driven build |
| permanent `if old_failed` | delete; Git has history |
| strategy class for a single scalar | config parameter |
