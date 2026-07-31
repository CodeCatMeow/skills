# Precedence and Scope

## Contents

- [Purpose](#purpose)
- [Rule precedence](#rule-precedence)
- [Project rigor matrix](#project-rigor-matrix)
- [Always-required practices](#always-required-practices)
- [Scaled practices](#scaled-practices)
- [Google guide deviations](#google-guide-deviations)
- [Change scope](#change-scope)
- [Using this skill with existing code](#using-this-skill-with-existing-code)

## Purpose

This reference defines how the Python Engineering skill resolves competing guidance
and adjusts engineering effort to the work at hand. It is a decision framework, not
a license to lower the correctness bar. Apply it before choosing an implementation,
not after code has already accumulated in a convenient file.

The goal is clear, idiomatic, cohesive, testable Python. It is not minimum line
count, maximal abstraction, or uniform production process for every script.

## Rule precedence

Apply rules in this order:

1. The user's explicit request for the current task.
2. The repository's documented architecture, public API commitments, supported
   Python versions, and checked-in tool configuration.
3. Correctness, compatibility, security, data integrity, and operational safety.
4. This skill's explicit requirements.
5. Upstream references, including the Google Python Style Guide.
6. Personal preference or a convenient default.

The higher rule wins only for the actual conflict. For example, a project configured
for Black is not reformatted with a different formatter merely because another tool is
available. A repository's established relative-import convention is preserved unless
changing it is necessary to correct a defect or the user requests the migration.

When project code is inconsistent, follow the nearest coherent local convention for
the changed area. Do not use local inconsistency as a reason to ignore a documented
project rule or a correctness issue.

## Project rigor matrix

Use the matrix to choose the depth of testing, typing, documentation, and validation.
The entries describe a minimum target; a project's own requirements can raise it.

| Practice | Production application or service | Shared library, SDK, or reusable package | Research, data, or exploratory code | One-off script or local automation |
| --- | --- | --- | --- | --- |
| Public API and compatibility | Treat as a contract; preserve unless the task changes it. | Treat as a versioned contract; document and test changes. | Stabilize only interfaces used beyond the experiment. | Keep invocation and output behavior clear; no implied long-term API. |
| Type annotations | Annotate public and cross-module interfaces; annotate complex internals. | Annotate public APIs and stable extension points. | Annotate boundaries, data shapes, and error-prone transforms. | Annotate non-obvious inputs and outputs when it clarifies the script. |
| Tests | Cover new behavior, important failure paths, and regressions. | Cover supported behavior, errors, and compatibility promises. | Test critical transformations, invariants, shapes, ranges, and reproducibility controls. | Run a smoke check and test non-trivial or destructive logic. |
| Docstrings | Document public and non-obvious behavior using [Google docstrings](02-google-docstrings.md). | Document every public module, class, function, and extension contract. | Document assumptions, units, data expectations, and non-obvious algorithms. | Document entry points and non-obvious behavior; avoid empty ceremony. |
| Error handling | Validate boundaries, preserve causes, and log useful context. | Raise stable, meaningful exceptions and avoid process exits in library code. | Fail clearly on invalid data and record assumptions that affect results. | Handle expected operational failures and leave useful diagnostics. |
| Tooling | Use the project's existing formatter, linter, type checker, and relevant tests at a proportionate scope. | Use the configured quality suite for release-facing work when available. | Use existing tooling; do not add a stack solely for a short investigation. | Use available syntax checks and relevant project commands. |
| Structure | Separate independently changing domain, I/O, orchestration, and presentation concerns. | Keep import surfaces deliberate and dependencies stable. | Keep data loading, transforms, analysis, and plotting separable when they change independently. | Use a small, direct structure; do not create package layers without a present need. |

A short script may be simple, but it is never exempt from correct behavior, safe
resource handling, clear names, or preserving user data.

## Always-required practices

The following expectations apply to every Python change, regardless of project type:

- Respect explicit user and repository constraints.
- Preserve unrelated behavior and avoid unrequested rewrites.
- Use names that communicate the domain role of a value, function, class, or module.
- Keep normal control flow understandable; use guard clauses where they reduce nesting.
- Catch only exceptions that can be handled meaningfully. Never silently discard an
  exception.
- Avoid mutable default arguments, hidden mutable global state, and import-time work
  with external effects.
- Close files, sockets, database connections, and comparable resources deterministically.
- Keep comments for rationale, constraints, or surprising behavior rather than a
  narration of the code.
- Use a [Google-format docstring](02-google-docstrings.md) whenever a public,
  non-trivial, or non-obvious callable needs a contract.
- Run the most relevant available validation and report any check that could not run.

## Scaled practices

The following are deliberately proportional to the change:

- Full type coverage is not required for every local value or exploratory cell.
- Test breadth follows risk. A public library change needs more than a formatting-only
  maintenance edit; a disposable script may only need a representative smoke run.
- Modules are split when responsibilities or dependencies diverge, not at a fixed
  line count. Size thresholds are review prompts, never automatic split commands.
- Performance work requires a measured bottleneck, stated scale requirement, or clear
  algorithmic concern. During review, inspect changed hot paths for data-size
  assumptions, repeated I/O, accidental quadratic work, eager materialization, and
  unnecessary concurrency; judge them against the actual workload. Do not obscure
  ordinary code for hypothetical speed.
- New abstractions require present duplication, multiple implementations, a genuine
  boundary, or a testability need. Possible future use alone is insufficient.

## Google guide deviations

[Google Python Style](01-google-python-style.md) is the upstream baseline for this
skill, except where this section explicitly says otherwise.

### Comprehensions and generator expressions

Google's guide permits simple comprehensions but rejects expressions containing
multiple `for` clauses or multiple filters. This skill makes a narrow, explicit
exception: a limited linear combination may remain a comprehension when it has no
side effects, no nesting, no branching beyond its filters, and a reader can understand
its source, condition, and produced value at a glance.

For example, one source with two short, directly related predicates can be reasonable:

```python
active_names = [user.name for user in users if user.enabled if user.name]
```

This is not permission for density. Expand to statements when an expression has nested
loops, non-obvious calls, complex boolean logic, mutation, logging, exception handling,
or requires an explanation to be read safely. Prefer an explicit loop when it makes the
stages or error handling clearer.

All other Google guidance in this skill is restated rather than copied. The exact
Google docstring format is consolidated in [02-google-docstrings.md](02-google-docstrings.md);
that file is the only normative docstring-format reference in this skill.

## Change scope

Inspect the target module, nearby modules, tests, configuration, and callers before a
non-trivial change. State internally what the current module owns and whether the new
behavior changes for the same reason. Put a new responsibility in the existing module
only when its name, dependencies, and tests still describe one cohesive concern.

Do not turn a feature task into a repository-wide cleanup. Refactor the directly
involved area when the requested change would otherwise add an independent
responsibility, deepen an existing defect, or make safe testing impractical. Keep such
refactoring incremental, behavior-preserving, and covered by relevant tests.

Do not create catch-all modules such as `utils.py`, `helpers.py`, `common.py`, or
`misc.py` for new behavior. Existing files with those names do not make them suitable
homes for another unrelated responsibility.

## Using this skill with existing code

New code should follow the skill where it does not conflict with the project. Existing
code is not an invitation to normalize every neighboring style choice. Make the smallest
coherent change that satisfies the task, preserve public imports and behavior unless
asked otherwise, and update documentation or tests when their contract changes.

When legacy behavior is unclear, first locate existing tests or add a characterization
test around the affected behavior. If a broad improvement is valuable but outside the
request, identify it separately rather than silently expanding the patch.
