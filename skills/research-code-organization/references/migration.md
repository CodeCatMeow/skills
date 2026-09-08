# Migrating a Research Script Graveyard

Use this workflow when several launchers or model copies overlap enough that nobody
can tell which path is authoritative.

1. Inventory training entrypoints, shell wrappers, notebooks, and configuration.
2. Compare behavior rather than filenames. Classify each difference as:
   - a parameter or runtime option;
   - reusable model, loss, data, or evaluation logic;
   - training control flow; or
   - a separate lifecycle such as evaluation or export.
3. Identify the most complete shared path and establish one stable training
   entrypoint around it.
4. Move parameters into the existing configuration system, reusable differences
   into domain modules, and control-flow differences into selectable strategies.
5. Record equivalent commands for important prior runs and verify their behavior.
6. Retire redundant launchers and version-named modules once parity is established.

Migrate one coherent slice at a time so that results remain attributable and review
stays practical. Preserve an old path only when it is still needed for an active
comparison or reproducibility requirement.

Hydra is an optional follow-up when the dominant problem is composition across many
small configuration deltas. Confirm that migration cost is justified before adding
it; the same routing works with a simpler existing configuration system.
