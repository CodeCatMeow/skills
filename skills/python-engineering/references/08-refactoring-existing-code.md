# Refactoring Existing Code

## Contents

- [Purpose and boundaries](#purpose-and-boundaries)
- [When to refactor proactively](#when-to-refactor-proactively)
- [When to contain the work](#when-to-contain-the-work)
- [Preserve behavior deliberately](#preserve-behavior-deliberately)
- [Small-step refactoring](#small-step-refactoring)
- [Extracting functions, modules, and classes](#extracting-functions-modules-and-classes)
- [Public API and import migration](#public-api-and-import-migration)
- [Dependency direction and cycles](#dependency-direction-and-cycles)
- [Signals versus decisions](#signals-versus-decisions)
- [Completion checklist](#completion-checklist)

## Purpose and Boundaries

Refactoring improves the structure of existing code while preserving intended externally observable behavior. It is not a license to rewrite an unfamiliar subsystem, replace a project architecture, or fold unrelated cleanup into a focused user request.

Be proactive when the requested change would otherwise place a distinct responsibility into the wrong module, extend a fragile large function, duplicate existing logic, or deepen an existing dependency problem. The user does not need to ask for a split explicitly. Place the new responsibility where it belongs when the current task makes that boundary clear.

Keep the scope connected to the task. Fix the obstruction that prevents a clear, testable implementation; record or mention broader debt when relevant, but do not turn a bug fix into a repository-wide modernization without authorization.

## When to Refactor Proactively

Refactor as part of the current change when at least one of these conditions is true:

- The feature introduces a second independent reason for the current module to change.
- New domain rules would otherwise be coupled directly to HTTP, CLI, persistence, rendering, or another unrelated infrastructure concern.
- A requested behavior duplicates logic already present in the directly affected area.
- A function cannot accommodate the change without obscuring its control flow, combining unrelated side effects, or multiplying parameters with unrelated meanings.
- Tests for the new behavior require broad patching because a dependency boundary is missing.
- The change would create, strengthen, or expose an import cycle.
- The module name would become misleading after the new behavior is added.

Prefer a small, named boundary such as `checkpoint_store.py`, `result_serializer.py`, or `config_loader.py` over placing another unrelated feature in `utils.py`, `helpers.py`, `common.py`, or `misc.py`. For a focused change to an existing module, extract the one boundary needed to implement the requested behavior, then stop; do not also redistribute every legacy responsibility that could be separated. Do not create a new module just to hold a single trivial helper; extract only where the boundary gives a reader, caller, or test a meaningful unit.

## When to Contain the Work

Do not expand the task merely because existing code is imperfect. Keep a cohesive parser, state machine, algorithm, protocol implementation, or tightly related data model together when splitting would make its flow harder to follow. File length and method count are prompts for review, not automatic reasons to divide code.

Contain the change when a broader refactor would:

- Require changes across unrelated packages or public interfaces.
- Change persistence formats, protocol behavior, or operational deployment without a requirement to do so.
- Demand unverified assumptions about callers or production workflows.
- Consume the majority of the task while providing no direct benefit to the requested behavior.
- Replace a stable local convention with a personal architectural preference.

In that case, make the narrowest clear change, protect it with proportionate tests, and identify the larger concern separately when it materially affects future work.

## Preserve Behavior Deliberately

Before moving code, identify the behavior that must remain stable: public imports, call signatures, return values, exceptions, ordering, side effects, persisted formats, command output, and timing or retry semantics where callers depend on them. Search direct callers and existing tests before changing a boundary.

When behavior is poorly specified, add characterization tests around the relevant current behavior before rearranging it. A characterization test records what the system does today; it is not an endorsement of every legacy quirk. Use it to distinguish deliberate compatibility from accidental behavior that the current request explicitly changes.

Keep feature changes and pure restructuring separable in reasoning and in intermediate states. They may be implemented together when required, but first establish a stable movement path, then make the intended behavior change, then validate both.

## Small-Step Refactoring

Use reversible, testable steps. A typical sequence is:

1. State the affected contract and locate its existing tests or add characterization coverage.
2. Introduce the new function, module, or collaborator without changing callers.
3. Move one coherent operation at a time and preserve observable behavior.
4. Redirect callers through the new boundary.
5. Remove dead paths only after callers and tests use the new path.
6. Run focused validation after each meaningful step, then appropriate wider validation.

A clean intermediate state matters more than minimizing the number of edits. Do not leave duplicate production paths, half-moved imports, dead compatibility code, or temporary fallback behavior without a clear reason and removal condition.

## Extracting Functions, Modules, and Classes

Extract a function when a contiguous block has a nameable purpose, its inputs and outputs can be stated clearly, and the extraction reduces cognitive load without hiding essential flow. Keep related sequential steps together when extraction would turn a simple algorithm into a chain of tiny, indirection-heavy helpers.

Extract a module when code has an independent vocabulary, dependency set, lifecycle, or testing boundary. Good candidates separate parsing from serialization, domain decisions from transport, storage from orchestration, or configuration loading from execution. Define imports so lower-level domain code does not depend on entry points, UI, or concrete infrastructure.

Extract a class only for a stable concept with meaningful state, lifecycle, identity, or interchangeable behavior. Prefer a dataclass for structured data and a function for stateless behavior. Do not introduce managers, factories, registries, interfaces, inheritance layers, or dependency injection frameworks merely because a refactor is underway. Present duplication, a real alternate implementation, an external boundary, or a proven stateful concept is the evidence needed for an abstraction.

## Public API and Import Migration

Preserve public import paths and signatures unless the task explicitly changes them. When moving an established public symbol, use a temporary compatibility re-export only if callers are expected to depend on the old location and the project has a migration path. The compatibility layer should be thin, tested, documented at the appropriate project boundary, and removed when the support window ends.

Do not create re-export chains that obscure ownership or make import cycles harder to diagnose. New code should import from the owning module. Compatibility imports are a migration mechanism, not a permanent package design.

## Dependency Direction and Cycles

A cycle is usually a boundary signal. First identify what each side actually needs. Move shared data types or small protocols into a lower-level module only when they are truly shared. Invert a dependency at a narrow boundary when core logic needs behavior supplied by infrastructure. Avoid solving cycles with late imports, broad `TYPE_CHECKING` workarounds, globals, or implicit registries unless the project convention and the problem genuinely require them.

After a split, verify that the import graph follows a readable direction and that importing a module does not trigger I/O, configuration loading, or process startup. The CLI or service entry point should compose concrete dependencies; core logic should remain importable and testable without starting the application.

## Signals Versus Decisions

Structural measurements identify where to look; they do not prescribe a refactor.

| Category | Examples | Required response |
| --- | --- | --- |
| Hard failure | Broken imports, failing tests, syntax errors, changed public behavior without required compatibility | Fix or explicitly change the contract before completion |
| Soft structural signal | Long function, many parameters, mixed dependencies, repeated setup, high mock count, module size, or an unconfigured import-cycle warning | Inspect the local design and justify a focused refactor or a deliberate decision not to expand scope |
| Semantic judgment | Whether two responsibilities truly change together, whether an extraction improves readability, whether a compatibility layer is worth its cost | Apply system context and user intent; tools can inform but cannot decide |

Do not turn a soft signal into an automatic rule that large files must split or long
functions must be extracted. Conversely, do not use the absence of a metric threshold
to ignore a clear boundary violation.

## Completion Checklist

- Did the refactor directly support the requested behavior or remove a real obstacle to it?
- Are the protected public contracts and observable effects identified and tested at the appropriate risk level?
- Does each new function, module, or class have a clear, accurate responsibility?
- Were broad abstractions avoided unless current code demonstrated a need?
- Does the dependency direction remain understandable and free of newly introduced cycles?
- Are temporary compatibility paths necessary, tested, and governed by a removal condition?
- Were obsolete imports, duplicate paths, and dead code removed once safe?
- Did validation cover both the changed feature and the structure-sensitive boundary it touched?
