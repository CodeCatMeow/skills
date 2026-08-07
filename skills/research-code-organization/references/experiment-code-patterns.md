# Experiment Code Patterns

## Launchers

```text
# Bad
train.py / train_baseline.py / train_no_aux.py / train_attention_v2.py / train_final.py

# Good
train.py
configs/experiment/{baseline,no_aux,attention}.yaml
models/components/...
```

Without Hydra, same idea:

```bash
python train.py --config configs/no_aux.yaml
```

## Parameter-only variants

```text
# Bad
train_lr_1e4.py   # lr = 1e-4
train_lr_3e4.py

# Good
optimizer.lr=1e-4   # config or CLI
```

## Ablations

```text
# Bad — nearly identical loops
train_with_aux.py / train_no_aux.py

# Good
loss.aux.enabled: false  +  losses = build_losses(cfg.loss)
```

```python
# Bad — eternal flag soup
if cfg.use_attn: ...
if cfg.use_old_attn: ...
if cfg.exp_name == "camera_ready": ...

# Good
h = self.attn(h)  # attn selected: identity | baseline | relative
```

## Models / losses / strategies

```text
# Bad                              # Good
model.py / model_v2.py / model_final.py
                                   models/{baseline.py,components/...}

# Bad                              # Good
40-line if/elif losses in train.py
                                   losses/{cross_entropy,focal}.py + build_loss

# Bad                              # Good
train_distill.py fork
                                   training/strategies/{supervised,distill}.py
```

## scripts/ and notebooks

```text
# Bad: scripts/run_*.py as experiment launchers
# Good: scripts for convert/inspect/download; train via stable entry

# Bad: formal numbers only in an untitled notebook
# Good: promote to package + config; notebook analyzes saved outputs
```

## Promote and delete

```python
# Bad — still temporary months after validation
if use_new_attention: ...

# Good
# models/components/new_attention.py
# config: model.attention=new
# delete temporary flag
```

```python
# Bad — failed idea gated forever
if cfg.use_failed_method_from_march: ...

# Good
delete; Git retains history
# keep only for active comparison or required reproduction
```

## Drive-by engineering

User: "Disable auxiliary loss."

```text
# Bad: also rename trainer, change augs, refactor evaluator
# Good: disable aux; fix only schema/logging break; note unrelated debt
```

## Shared interface

```text
build_model(cfg) / build_loss(cfg) / build_strategy(cfg)
```

Stable training depends on interfaces; config chooses implementations.
A simple factory is enough — no plugin framework required.

## Choice cheat sheet

| User request | Prefer |
| --- | --- |
| change lr / wd / epochs | config |
| turn off module X | config + component or intentional toggle |
| try new attention | new component + selection |
| compare 3 seeds | same code, config/CLI repeats or multirun |
| add distillation | strategy |
| dump embeddings | eval/export entrypoint |
| "quick try" | exploratory hack, then promote or delete |

Prefer the smallest sufficient durable abstraction. Configuration alone when it
expresses the change; component + selection when a reusable implementation is
required; strategy or entrypoint only when control flow or lifecycle demands it.
