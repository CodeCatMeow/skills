# Google Python Style

## Contents

- [Role and local conventions](#role-and-local-conventions)
- [Imports and packages](#imports-and-packages)
- [Exceptions and assertions](#exceptions-and-assertions)
- [State, scope, and nesting](#state-scope-and-nesting)
- [Comprehensions, iterators, and generators](#comprehensions-iterators-and-generators)
- [Expressions and defaults](#expressions-and-defaults)
- [Objects, decorators, and dynamic features](#objects-decorators-and-dynamic-features)
- [Concurrency](#concurrency)
- [Formatting and layout](#formatting-and-layout)
- [Comments, strings, resources, and TODOs](#comments-strings-resources-and-todos)
- [Names, entry points, and function size](#names-entry-points-and-function-size)
- [Type annotations](#type-annotations)
- [Compact examples](#compact-examples)

## Role and local conventions

This reference is an original operational restatement of the Google Python Style
Guide. It covers code style only. [Google docstrings](02-google-docstrings.md) is
the sole normative format reference for module, class, function, method, generator,
and property docstrings.

First honor repository configuration and local conventions under the precedence
rules in [00-precedence-and-scope.md](00-precedence-and-scope.md). An existing
formatter, line length, import tool, supported Python version, or public API takes
precedence. Use this reference when the project has no applicable rule or when
choosing a clear direction for new code.

## Imports and packages

- Import packages and modules rather than individual runtime symbols. Prefer
  `import package.module` or `from package import module`, then qualify uses with
  the module name.
- Import individual names from `typing` and `collections.abc` when that makes type
  annotations concise. Their names should not be reused for unrelated local values.
- Use a standard abbreviation only when it is broadly established, such as
  `import numpy as np`.
- Avoid wildcard imports. They obscure the source of names and make static analysis
  less reliable.
- Use the project's package path and avoid ambiguous local imports. New code should
  not depend on the executable's directory accidentally appearing on `sys.path`.
- Put imports after the module docstring and before constants or other module state.
  Order them as future imports, standard library, third-party packages, then project
  packages. Sort each group by full package path and use separate import lines.
- Prefer a dependency change over a type-only import cycle. `TYPE_CHECKING` imports
  are an exceptional fallback, not routine architecture.

## Exceptions and assertions

- Use built-in exception types when their meaning fits. Custom library exceptions
  should inherit an appropriate existing exception and conventionally end in `Error`.
- Raise a precise exception for invalid input or a violated precondition. Do not use
  `assert` for required runtime validation because optimized Python can remove it.
  Assertions are appropriate in tests and for invariants whose removal would not
  change required behavior.
- Catch the narrowest useful exception and make the `try` block as small as possible.
  A bare `except` is forbidden. Catching `Exception` is only suitable at a deliberate
  isolation boundary that records, re-raises, or intentionally contains failure.
- Preserve cause when translating an error: `raise DomainError(message) from error`.
  Use `finally` or, preferably, a context manager for cleanup.

## State, scope, and nesting

- Avoid mutable module globals. Constants are encouraged and use uppercase names;
  rare mutable module state is private and must have a documented design reason.
- A nested function or class is appropriate when it closes over a meaningful local
  value. Do not nest code merely to hide it from callers; use a module-private name
  so tests can reach it when necessary.
- Be aware that assigning a name in a function changes how Python resolves it. Avoid
  confusing closure interactions and avoid `global` or `nonlocal` unless the state
  relationship is clear and intentional.
- Keep import-time execution limited to definitions, constants, and inexpensive,
  deterministic setup. Put program work behind an explicit entry point.

## Comprehensions, iterators, and generators

Use direct iteration and the operations native to the object: iterate a mapping rather
than `mapping.keys()`, iterate a file rather than `readlines()`, and use membership
operators where they express the question. Do not mutate a container while iterating
through it.

Use a list, set, or dictionary comprehension when it makes one mapping or selection
clearer than an explicit loop. Use a generator expression when a one-pass lazy stream
is appropriate. The skill's deliberately narrower variation on Google's strict rule
is recorded in [00-precedence-and-scope.md](00-precedence-and-scope.md): a small,
linear, side-effect-free combination can remain a comprehension, but nested iteration,
complex branching, or opaque work must be expanded.

Generators are appropriate for lazy production or streaming. They can retain local
state and resources until exhausted, so pair resource-owning generators with explicit
lifetime management. A generator's docstring uses `Yields:`, as specified in
[02-google-docstrings.md](02-google-docstrings.md).

## Expressions and defaults

- Use `lambda` only for a small, obvious expression. Prefer a named function when
  behavior needs a name, spans lines, or merits a useful traceback. Prefer a generator
  expression to `map()` or `filter()` with a lambda.
- A conditional expression is acceptable only when its condition and both outcomes
  are readily readable. Use an `if` statement when it needs line-by-line explanation.
- Never use a mutable value or a value that should be calculated at call time as a
  default argument. Use `None` or an immutable sentinel and initialize inside.
- Use implicit truth testing for normal containers, strings, and optional objects.
  Compare to `None` with `is` or `is not`; do not use `== None`. For numeric values,
  compare explicitly when zero has distinct meaning. Some array libraries reject
  implicit truth testing, so use their documented emptiness check.
- Use f-strings, `%` formatting, or `str.format` for ordinary string interpolation.
  Do not assemble formatted strings with repeated `+`, especially in loops.

## Objects, decorators, and dynamic features

- Use a property only for cheap, unsurprising access or simple derived state. A plain
  stored value should normally be a public attribute; significant work should be a
  method so its cost is visible.
- Use decorators when their benefit is explicit and test them. Decorator code runs at
  definition time, so it must not require unavailable external state. Prefer a module
  function to `@staticmethod`; reserve `@classmethod` for named constructors or
  genuinely class-wide behavior.
- Avoid metaclasses, bytecode manipulation, import hooks, broad reflection, dynamic
  inheritance, custom descriptors, and finalizer-driven cleanup unless the problem
  specifically requires them. Standard-library abstractions that internally use these
  mechanisms, such as `dataclasses` and `enum`, remain appropriate.

## Concurrency

Do not rely on apparent atomicity of builtin container operations or assignments.
Communicate between threads through `queue.Queue` or protect state with appropriate
synchronization. Prefer higher-level coordination such as `threading.Condition` when
it models the required state better than manual lock management. Keep process and
thread ownership, cancellation, and resource lifetime explicit.

## Formatting and layout

Project formatting configuration wins. Without it, follow these Google-oriented rules:

- Use four spaces for indentation, never tabs.
- Keep lines to 80 characters when practical. Do not use a backslash for ordinary
  line continuation; break inside parentheses, brackets, or braces at a clear
  syntactic level.
- Do not terminate statements with semicolons or place multiple statements on one
  line, except a very short one-line `if` without an `else` when local style permits.
- Use parentheses only when they clarify a tuple or enable wrapping; do not wrap
  ordinary `if`, `while`, or `return` expressions.
- Leave two blank lines between top-level definitions and one between methods.
- Use spaces around binary operators and after commas and colons. Do not align
  assignments or comments vertically with extra spaces.
- Add a trailing comma to a multi-line collection or call whose closing delimiter is
  on a separate line. A one-element tuple always needs its comma.
- A directly executable Python file may use an appropriate Python 3 shebang. Imported
  modules generally do not need one.

## Comments, strings, resources, and TODOs

Write comments for intent, constraints, non-obvious facts, or tradeoffs. Do not restate
what clear code already says. Write complete, readable prose with correct punctuation.
Use [02-google-docstrings.md](02-google-docstrings.md) for all docstring decisions.

Be consistent about single versus double quotes within a file, except when choosing the
other quote avoids escaping. Use triple double quotes for docstrings. For logging APIs
that accept a format pattern and arguments, pass a literal pattern plus values rather
than an f-string; this avoids eager formatting and retains structured information.
Error messages must describe the real failure condition and distinguish interpolated
values clearly.

Manage files, sockets, database connections, mappings, and similar resources with
`with`. Where a resource does not implement the context-manager protocol, use
`contextlib.closing()` or document the explicit owner and close path. Do not rely on
destructors for observable cleanup.

A temporary workaround uses `TODO:` followed by a durable issue, decision record, or
other traceable context and a brief explanation. Do not leave anonymous or owner-only
TODOs that future maintainers cannot resolve.

## Names, entry points, and function size

Names must reveal purpose at their scope. Use `lower_with_under` for modules,
packages, functions, methods, parameters, locals, and ordinary attributes;
`CapWords` for classes and exceptions; and `CAPS_WITH_UNDER` for constants. Avoid
unfamiliar abbreviations, type-encoded names, dashes in module names, and reserved
double-leading-and-trailing-underscore names. A single underscore marks internal
implementation. Avoid double-leading underscores unless name mangling is essential.

Related classes and functions may share a module. Python does not require one class
per file. A runnable module puts its work in `main()` and invokes it only under
`if __name__ == '__main__':`, preventing imports from executing the program.

Prefer focused functions. Function length can prompt a cohesion review, but it is not
a limit. Split only where named steps clarify behavior or are independently useful; do
not extract trivial fragments that make a single operation harder to read.

## Type annotations

Annotate public APIs, then add annotations where they clarify stable or error-prone
internal contracts. Do not mechanically annotate every local variable. Use modern
built-in generics such as `list[str]` and abstract interfaces such as
`collections.abc.Sequence` when callers need only that behavior. Specify generic
parameters rather than accepting implicit `Any`; use `Any` explicitly when dynamic
behavior genuinely needs it.

Use `X | None` for nullable values in supported Python versions, and use spaces around
`=` when an annotated parameter has a default. Do not annotate `self`, `cls`, or an
`__init__` return merely by habit. Use `from __future__ import annotations` or quoted
forward references when a same-module type is defined later. A circular import caused
by typing is a design signal to refactor; do not normalize it into routine conditional
imports.

Use a narrowly scoped type-checker suppression only with the tool's specific error
code and a reason. A type alias uses `CapWords`, or `_CapWords` when private.

## Compact examples

```python
from collections.abc import Iterable


def normalized_names(values: Iterable[str | None]) -> list[str]:
    """Returns non-empty names in normalized form."""
    return [value.strip().lower() for value in values if value and value.strip()]
```

```python
# Prefer a loop when stages, error handling, or nested work need to be visible.
def load_valid_records(paths: list[str]) -> list[Record]:
    records: list[Record] = []
    for path in paths:
        try:
            record = load_record(path)
        except OSError as error:
            logger.warning("Could not load record %r: %s", path, error)
            continue
        if record.is_valid():
            records.append(record)
    return records
```

```python
# Do not share a mutable default between calls.
def add_label(label: str, labels: list[str] | None = None) -> list[str]:
    """Returns labels with label appended."""
    if labels is None:
        labels = []
    labels.append(label)
    return labels
```
