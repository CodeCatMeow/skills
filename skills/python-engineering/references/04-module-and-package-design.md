# Module and Package Design

## Contents

- [Design around a cohesive responsibility](#design-around-a-cohesive-responsibility)
- [Decide where new behavior belongs](#decide-where-new-behavior-belongs)
- [Signals to split a module](#signals-to-split-a-module)
- [Signals to keep a module intact](#signals-to-keep-a-module-intact)
- [Choose useful boundaries](#choose-useful-boundaries)
- [Name modules for their responsibility](#name-modules-for-their-responsibility)
- [Keep dependencies directional](#keep-dependencies-directional)
- [Make package APIs deliberate](#make-package-apis-deliberate)
- [Use review signals, not mechanical split rules](#use-review-signals-not-mechanical-split-rules)

## Design Around a Cohesive Responsibility

A module is a home for code that changes for a related reason. Its boundary should make the module name, dependencies, tests, and public interface coherent. It is not a bucket determined by the file currently open, a line count, or a rule that every class must have its own file.

Before adding behavior, state in one sentence what the current module owns and what the new behavior owns. If both statements describe the same domain concept and change together, extending the module is usually right. If the new behavior has a separate lifecycle, dependencies, public API, or reason to change, give it a clearer home now.

## Decide Where New Behavior Belongs

Answer these questions before adding a non-trivial responsibility to an existing module:

1. What responsibility does this module currently own?
2. Does the new behavior belong to that same domain concept?
3. Would the same product, policy, or operational change normally affect both?
4. Does the new behavior require substantially different infrastructure or third-party dependencies?
5. Could it be tested without setting up the module's unrelated collaborators?
6. Will the current module name still accurately describe the combined contents?
7. Does the behavior need an independent public interface or reuse boundary?

Use the answers to choose one of three actions:

- **Extend the module** when the behavior is cohesive with its existing responsibility.
- **Create a focused sibling module** when the new responsibility is independently meaningful.
- **Extract part of the existing module first** when adding the feature would deepen an existing mix of responsibilities. For a focused change, extract only the one boundary required for that feature; do not turn it into a migration of every existing concern that could be separated.

Do not make users request "a refactor" before applying the third option. A current feature that would otherwise create a second independent responsibility is sufficient reason to reorganize the code directly involved in that feature.

## Signals to Split a Module

These conditions warrant a boundary review. Several together are stronger evidence than any one alone.

- One module serves distinct workflows with separate callers or release cadence.
- Domain policy, persistence, HTTP, CLI/UI presentation, and formatting live together without a compelling reason.
- Separate parts depend on unrelated libraries or operational concerns.
- A change to one behavior repeatedly requires reading, patching, or testing unrelated behavior.
- Tests require extensive patching of collaborators irrelevant to the behavior under test.
- The module name has become vague or inaccurate after additions.
- A new feature has a stable public interface or is reused independently.
- The module has acquired a second clear reason to change.
- Imports are becoming circular or force a high-level layer to import a low-level detail.

A split should improve the code's explanation, not merely distribute lines. Move a cohesive unit with the dependencies it actually needs, define a narrow interface, update imports and tests, then preserve public import paths when they are part of the supported API.

## Signals to Keep a Module Intact

Do not split simply because a module is large, a class is large, or an arbitrary metric was crossed. Keep a module together when its pieces form one concept that readers need to understand as a whole:

- A parser with tokenization, grammar rules, and AST construction that evolve together.
- A state machine whose transitions, states, and invariants are inseparable.
- A numerical algorithm whose helper functions are steps of one calculation.
- A protocol implementation with closely coupled encoding, decoding, and validation.
- A group of related data types and operations that share invariants and dependencies.
- A short module split would create one-function files, excessive imports, or navigation without a useful boundary.

For example, extending a cohesive parser with a new token normally belongs in that parser. A 450-line parser is a review prompt, not a command to split it. Keep it intact when one responsibility, one vocabulary, and one change driver still describe it accurately.

## Choose Useful Boundaries

Use boundaries that match the problem rather than a universal architecture template. Common useful separations include:

| Concern | Typical boundaries |
|---|---|
| Product behavior | domain rules, application orchestration, infrastructure adapters |
| Data processing | parsing, validation, transformation, serialization |
| External systems | repository or store, transport client, service policy |
| Execution | configuration loading, command/API entry point, core execution |
| Data lifecycle | model, persistence, reporting or presentation |
| Operational tools | computation, filesystem operations, plotting or rendering |

A small script may legitimately keep configuration, execution, and output in one module. A shared service often benefits from separating pure policy from I/O adapters because the dependencies and test setup differ. Apply only the boundaries the current code needs.

Keep side effects at the edges where practical. Core policy should consume values or narrow capabilities rather than importing a concrete CLI, database, HTTP client, or filesystem detail. This makes dependency direction and testing simpler without requiring a framework or a named architecture.

## Name Modules for Their Responsibility

A module name should tell readers what belongs inside. Prefer a concrete noun or noun phrase tied to the module's responsibility:

```text
config_loader.py
checkpoint_store.py
experiment_runner.py
metric_reporter.py
result_serializer.py
user_repository.py
```

Avoid catch-all names for new code:

```text
utils.py
helpers.py
common.py
misc.py
manager.py
base.py
```

An established, narrowly scoped convention can justify an otherwise generic name, such as a package-local `utils.py` whose single stated purpose is stable and small. It is not permission to add unrelated behavior there. Prefer a new focused name rather than growing a junk-drawer module.

Name packages after a domain or a coherent subsystem, not after implementation leftovers. Use a private module name such as `_validation.py` only when the boundary is intentionally internal; the underscore is a compatibility signal, not a substitute for structure.

## Keep Dependencies Directional

Dependencies should move from entry points and adapters toward stable policy and data concepts, not back again.

```text
CLI / HTTP entry point -> application service -> domain policy
                                      -> infrastructure adapter
```

The exact layers vary by project. Preserve these practical rules:

- Core logic must not import a CLI, template, web handler, or presentation layer.
- Domain policy should not construct or directly depend on a concrete database or network client when a narrow collaborator can be supplied at the boundary.
- Separate I/O from calculations and decisions where they change or test differently.
- Avoid circular imports by moving shared concepts to the lowest sensible module or by passing dependencies inward.
- Do not solve a cycle with a maze of runtime imports; reassess the ownership and direction first.
- Keep dependencies explicit in function parameters or constructors rather than hidden module globals.

```python
# Avoid: policy reaches outward into a concrete persistence detail.
from app.database import Session

def can_publish(article_id: int) -> bool:
    return Session().load_article(article_id).is_approved

# Prefer: policy receives the value or a narrow capability from its caller.
def can_publish(article: Article) -> bool:
    return article.is_approved
```

A full dependency-inversion layer is justified only when there is a present substitution boundary: multiple implementations, an external system that must be isolated, or a stable test seam. A direct import is often clearer inside a small, cohesive module.

## Make Package APIs Deliberate

A package is an API boundary. Decide which names users may import, document those names, and keep internal organization free to change.

- Expose a small, stable public surface from package modules or `__init__.py` when callers genuinely benefit from it.
- Keep re-exports shallow and intentional. A package root that re-exports every internal type hides ownership and makes changes harder.
- Use leading underscores for names without a compatibility promise.
- Avoid import-time network calls, configuration loading, registration side effects, and expensive work in `__init__.py`.
- Keep package initialization lightweight so imports remain predictable and cycle-free.

```python
# Avoid: package initialization imports an entire implementation graph.
from .client import Client
from .database import Database
from .jobs import JobRunner
from .internal.cache import Cache

# Prefer: export the small public API consumers should use.
from .client import Client

__all__ = ["Client"]
```

Do not add `__all__` mechanically to every internal module. Use it where the public contract needs to be explicit.

## Use Review Signals, Not Mechanical Split Rules

Large modules, long functions, high public-definition counts, deep nesting, broad parameter lists, or complex import graphs are useful prompts to inspect cohesion. They are not automatic refactoring commands.

When a project tool or code review flags a large module or long function, ask:

- Is there more than one independent responsibility?
- Would a move yield a named boundary with simpler dependencies and tests?
- Would keeping the unit intact better preserve a single algorithm, protocol, or state model?
- Can the current task improve the directly affected boundary without expanding into unrelated cleanup?

Do not split merely to satisfy a threshold. Do not keep an incoherent module merely because each part is individually short. The outcome should be a structure that makes the next relevant change clearer and safer.
