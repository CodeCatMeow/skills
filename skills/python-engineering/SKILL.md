---
name: python-engineering
description: Use whenever creating, modifying, debugging, testing, reviewing, refactoring, or organizing Python code, modules, packages, tests, or project configuration.
user-invocable: true
disable-model-invocation: false
---

# Python Engineering

## Goal

Use this skill as the default engineering discipline for Python project work. Apply it
before writing code, not as a style pass after the implementation has accumulated.

Aim for clear, idiomatic, cohesive, documented, and testable Python that fits the
repository. Do not optimize for minimum line count, maximum abstraction, or
production-process ceremony where the task does not need it.

## Rule Priority

Resolve conflicts in this order:

1. The user's explicit requirements for the current task.
2. The repository's architecture, supported Python version, public API commitments,
   and checked-in configuration.
3. Correctness, compatibility, security, data integrity, and operational safety.
4. This skill's explicit rules.
5. The upstream guidance summarized by this skill, including Google Python Style.
6. Personal preference or a convenient default.

Use project conventions and existing configuration when they apply. Do not reformat
unrelated code, replace a configured toolchain, or expand a focused change into a
repository-wide cleanup merely for consistency.

Read [precedence and scope](references/00-precedence-and-scope.md) when the project
kind, local conventions, or appropriate level of rigor is unclear.

## Decide Before Coding

Before creating code or making a non-trivial Python change, inspect the relevant
module, nearby modules, directly affected tests, callers when an interface is shared,
and project configuration. Determine:

1. The target module's current responsibility in one sentence.
2. The new or changed behavior's responsibility in one sentence.
3. Whether both change for the same reason and belong at the same boundary.
4. Which public imports, signatures, return values, exceptions, ordering, side effects,
   serialized forms, or CLI behavior require protection.
5. Whether the behavior belongs in the current module, a focused sibling, or a small
   extraction from the directly affected area.
6. The narrowest credible validation evidence for the risk of the change.

Do not put new behavior in the currently open file by default. The user does not need
to request a split explicitly: judge ownership and module boundaries proactively.
Make the decision internally unless its tradeoff materially affects the user.

For a new responsibility or uncertain boundary, read
[module and package design](references/04-module-and-package-design.md). For a new
function, class, or meaningful extension, read
[function and class design](references/05-function-and-class-design.md).

## New Code Workflow

For new modules, public APIs, and non-trivial behavior:

1. Inspect context and choose the ownership boundary before implementation.
2. Define caller-visible behavior and the smallest useful API.
3. Implement with repository conventions and a proportionate design.
4. Add focused tests for non-trivial behavior, important boundaries, and meaningful
   failures.
5. Add or update types and caller-facing documentation where the contract needs them.
6. Run focused validation, widening it only when shared behavior or risk warrants it.
7. Review whether the code introduced an independently changing responsibility.

Do not make every task full TDD or a production release process. A small script can
remain a small script, but it still needs clear behavior, safe resource handling, and
credible evidence appropriate to its risk.

## Existing Code Workflow

Before changing existing code, understand its current behavior and affected callers.
For a defect, add or identify a regression test that captures the reported behavior
before or alongside the fix when feasible. If reproduction is blocked, say why and
provide the strongest available evidence.

Preserve public imports, signatures, return semantics, exceptions, ordering, side
effects, and formats unless the task intentionally changes their contract. Update
tests, types, and docstrings when the contract changes.

Refactor the directly involved area when the requested feature would otherwise add a
second responsibility, duplicate behavior, obscure control flow, or create a dependency
problem. For an existing module, default to the smallest structural change: extract the
meaningful boundary required for the current behavior, then stop. Do not redistribute
other pre-existing responsibilities merely because they could also be separated.

For a large, fragile, or mixed-responsibility area, read
[refactoring existing code](references/08-refactoring-existing-code.md).

## Core Python Style

Write direct Python that makes normal control flow visible:

- Prefer clear standard-library constructs, direct iteration, `enumerate`, `zip`,
  unpacking, `any`, `all`, context managers, guard clauses, and `pathlib` when they
  clarify the operation.
- Keep comprehensions and generator expressions when they express a readable mapping,
  selection, or short linear transformation. Do not mechanically expand familiar
  Python merely to make it look simpler.
- Expand nested iteration, complex branching, side effects, error handling, or opaque
  calls into named steps when the compact form is not understandable at a glance.
- Name modules, functions, variables, and parameters with `snake_case`; use `CapWords`
  for classes and exceptions and `CAPS_WITH_UNDER` for constants.
- Use descriptive domain names, explicit import sources, and no wildcard imports.
- Catch only exceptions that the current layer can handle. Keep `try` blocks narrow
  and preserve translated causes with `raise ... from error`.
- Avoid mutable default arguments, hidden mutable global state, import-time external
  effects, and `assert` for required runtime validation.
- Use parameterized logging rather than eager f-string formatting, and never log
  secrets.
- Comment on rationale, constraints, invariants, or surprising behavior rather than
  narrating code that a clear name already explains.

Read [Google Python style](references/01-google-python-style.md) for a precise general
style rule, or [Pythonic idioms](references/03-pythonic-idioms.md) when choosing
comprehensions, generators, standard-library tools, `dataclass`, `Protocol`, `match`,
lazy processing, or another advanced construct.

## Module Boundaries

Organize modules around cohesive responsibilities, not arbitrary line counts or the
file currently open. Before adding behavior, ask whether the module name, dependencies,
tests, and change driver still describe one concern.

Create a focused sibling module when the behavior has an independent vocabulary,
dependency set, lifecycle, public surface, or testing boundary. Extract only a
meaningful unit; do not create one-function files, a class per file, or package layers
without a present need.

Do not place new unrelated behavior in `utils.py`, `helpers.py`, `common.py`, or
`misc.py`. Existing catch-all modules are not justification for growing them. Keep
orchestration, domain policy, I/O, storage, presentation, and configuration separate
when they change or test independently, while preserving a cohesive parser, state
machine, algorithm, protocol, or data model as one module when that is clearer.

Treat file size, function size, parameter count, nesting, complexity, and import cycles
as prompts for human review. They never automatically require a split or prove that a
short unit is cohesive.

## Google Docstrings

Follow [Google docstrings](references/02-google-docstrings.md) as this skill's sole
normative docstring format. Use triple double quotes and a punctuated one-line summary.

Document public non-test modules, public classes, and public functions or methods. Also
document a private callable when its contract, algorithm, state change, failure
behavior, or resource ownership is not evident from its name, signature, and short
body. Do not create empty docstrings for simple private helpers or test modules.

Describe the caller contract, not an implementation walkthrough. Add `Args:`,
`Returns:`, `Yields:`, `Raises:`, or `Attributes:` only when they convey useful
semantics. Do not repeat obvious annotation syntax. Use `Yields:` for generators and
omit a meaningless `Returns: None` section.

## Types, Errors, and Logging

Annotate public APIs and cross-module contracts, then add types where stable or
error-prone internal behavior needs clarification. Do not mechanically annotate every
local variable or distort a clear API to satisfy a type checker.

Validate external and dynamic data at the boundary. Use precise exceptions, meaningful
messages, deterministic cleanup, and narrow suppressions with a specific diagnostic and
reason. Library layers normally raise rather than exit the process.

Read [types, errors, and logging](references/06-types-errors-and-logging.md) whenever
these concerns materially affect the change.

## Tests and Behavior Protection

Scale testing to risk. New non-trivial behavior needs focused evidence for expected
behavior, an important boundary, and a meaningful failure path. Bug fixes normally need
a regression test. Public APIs, persistence, security, concurrency, money, and
destructive I/O warrant broader evidence appropriate to their consequence.

Test observable behavior rather than private implementation steps. Keep fixtures
minimal and deterministic; isolate real external boundaries without mocking every
internal call. Run focused tests first, then a broader relevant suite when the blast
radius justifies it. Do not require complete TDD or the full repository suite for every
small change.

Read [testing and change safety](references/07-testing-and-change-safety.md) for new
behavior, bug fixes, test design, fixtures, determinism, or incomplete evidence.

## Validation Principles

Use validation as engineering evidence. Prefer the project's documented commands and
checked-in configuration. Choose scope by risk: run directly related tests first, then broaden when a shared contract, dependency
boundary, or high-consequence behavior changed.

Use an existing formatter, linter, type checker, or test tool when it provides relevant
evidence. Do not install tools, create an environment, edit lock files, change tool
configuration, add suppressions, or weaken checks merely to manufacture a pass. Prefer
non-mutating check modes. If a tool or test cannot run, state what was unavailable,
what remains unvalidated, and what partial evidence was obtained.

A small isolated change does not require every repository check. Tool output also does
not decide whether a module is cohesive, an abstraction is warranted, or a test proves
the contract. Read [tooling and validation](references/09-tooling-and-validation.md)
when selecting commands, choosing scope, handling unavailable tools, or interpreting
results from existing project tools.

## Avoid

- Do not continuously add unrelated behavior to one file or a catch-all module.
- Do not use size or complexity thresholds as mechanical reasons to split or retain code.
- Do not replace clear Pythonic code with ceremony, or compact complex logic into an
  opaque one-liner.
- Do not create speculative factories, registries, protocols, inheritance layers,
  generic configuration objects, or dependency-injection machinery.
- Do not silently swallow exceptions, use unjustified `# noqa` or `# type: ignore`, or
  hide required runtime validation in `assert`.
- Do not expose secrets in logs, add import-time external work, or leave resource
  ownership implicit.
- Do not alter public behavior or imports accidentally during a refactor.
- Do not expand a focused change into unrelated cleanup, formatting, or modernization.
- Do not generate unrequested Markdown summary files.

## Dynamic Reference Routing

Do not load every reference by default. Load each reference whose condition applies.
A substantial feature often needs several references, especially module design,
function design, documentation, and testing; a small local change may need only this
entry and one focused reference.

| Situation | Read |
| --- | --- |
| Scope, rigor, or convention conflict | [00 precedence and scope](references/00-precedence-and-scope.md) |
| Precise general Python-style question | [01 Google Python style](references/01-google-python-style.md) |
| Public or non-obvious module, class, or callable | [02 Google docstrings](references/02-google-docstrings.md) |
| Idiom, comprehension, generator, or advanced syntax choice | [03 Pythonic idioms](references/03-pythonic-idioms.md) |
| New module, package, responsibility, or import boundary | [04 module and package design](references/04-module-and-package-design.md) |
| Function, class, interface, or abstraction design | [05 function and class design](references/05-function-and-class-design.md) |
| Type, exception, resource, or logging behavior | [06 types, errors, and logging](references/06-types-errors-and-logging.md) |
| New behavior, bug, test, fixture, or validation evidence | [07 testing and change safety](references/07-testing-and-change-safety.md) |
| Legacy restructuring, API migration, or dependency cycle | [08 refactoring existing code](references/08-refactoring-existing-code.md) |
| Selecting validation commands or scope, unavailable tools, or interpreting existing tool results | [09 tooling and validation](references/09-tooling-and-validation.md) |

The comprehension policy intentionally permits a limited linear, side-effect-free
combination when it is immediately readable. Read
[precedence and scope](references/00-precedence-and-scope.md) before relying on that
narrow deviation from Google's stricter rule.

For review work, report findings first in severity order. A blocker must be fixed before
merge; an important finding should be fixed unless its risk is explicitly accepted and
recorded; a suggestion is non-blocking. For each finding, include a precise location,
symptom, cause, consequence, and actionable fix. If there are no findings, say so and
identify residual test gaps or assumptions.

## Before Finishing

Review the change as a whole, proportionate to its risk:

1. Confirm the implementation meets the user's requirements and preserves relevant
   existing behavior, public contracts, security, and data integrity.
2. Confirm each new behavior belongs in the right module and has not introduced a
   second independent responsibility; keep functions, classes, and modules cohesive.
3. Retain clear idiomatic Python, and expand any opaque one-liner, nested expression, or
   side-effecting compact form.
4. Keep Google docstrings synchronized with actual interfaces, and make types,
   exceptions, resource ownership, and logging clear.
5. Add or run focused tests and existing project checks at a scope justified by the
   change; report unavailable evidence honestly.
6. Remove unrelated churn, debug output, generated artifacts, unapproved configuration
   changes, unnecessary abstractions, files, dependencies, and redundant documentation.
