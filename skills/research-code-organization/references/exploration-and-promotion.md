# Exploration and Promotion

```text
explore  →  validate  →  promote or remove
```

## While exploring

Allowed: temporary `if use_idea:`, hardcoded constants, short-lived scripts,
notebooks, local-only modules, debug CLI flags.

**Important:**

- Keep blast radius small (one module, not scattered special cases).
- Name temporary things temporarily (`debug_use_foo`, not silent baseline overload).
- Do not create `train_idea_v3_final.py` if a flag or notebook will do.
- Do not silently change the default baseline unless the user asked.

## Validate

Enough evidence to keep or drop for the current question (smoke train, metric
movement, user confirmation). Not full production readiness.

## Promote (idea kept)

```python
# Temporary
if use_new_attention:
    h = new_attention_hack(h)
else:
    h = self.attn(h)

# Promoted
# models/components/new_attention.py
# config selects attention=new
h = self.attn(h)
```

1. Move to named module/component/strategy.
2. Expose selection through project config.
3. Remove temporary flags, dead paths, one-off launchers.
4. Narrow refactor to fit — not a redesign of unrelated systems.

## Failed exploration

Prefer delete. Avoid permanent `if cfg.old_failed_experiment:`.

Keep only when actively compared, required for paper/rebuttal reproduction, or
explicitly a teaching artifact — then isolate and document why.

## Refactoring boundary

| Phase | Do | Do not |
| --- | --- | --- |
| Experiment implementation | scientific change + minimum engineering so it runs | rewrite trainer, rename packages for taste, clean whole repo |
| Promotion | extract, remove hacks, align names | unrelated cleanups |
| Dedicated cleanup (user asked) | incremental migration, preserve expressibility | big-bang rewrite |

If structural debt blocks the experiment, fix that slice and say so. Otherwise
mention debt without fixing it in the same scientific change.

## Scientific vs engineering package

Request: disable auxiliary loss; logging expects `loss_aux`.

```text
# Allowed
disable aux; keep loss dict schema stable / skip missing key

# Not allowed unless asked
change lr, augs, evaluator, scheduler, checkpoint naming
```

## Time-box hacks

| Stage | Shape |
| --- | --- |
| first hours / first useful runs | local hack OK if isolated |
| chosen for further comparison | promote soon |
| formal tables / shared baseline | must be promoted |
| rejected | delete |

Do not wait for "someday" promotion.

## Baselines and notebooks

- Exploratory changes must not silently redefine the default experiment.
- New baseline = deliberate default-config update, previous baseline still
  expressible via config/component when comparisons continue.
- Promote notebook code into importable modules before it is the official path.
