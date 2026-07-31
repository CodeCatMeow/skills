# Types, Errors, and Logging

## Contents

- [Type contracts](#type-contracts)
- [Typing choices](#typing-choices)
- [Suppressions and untyped boundaries](#suppressions-and-untyped-boundaries)
- [Exception design](#exception-design)
- [Handling and translating errors](#handling-and-translating-errors)
- [Logging](#logging)
- [Review checklist](#review-checklist)

## Type Contracts

Type annotations describe a callable contract and let a configured checker find mismatches before runtime. Prefer the project's supported Python version, typing conventions, and configured checker over this reference's examples.

Annotate these by default:

- Public functions, methods, classes, and public attributes.
- Data passed across module or package boundaries.
- Stable, complex, or error-prone internal functions, especially parsers, validation, transformations, and asynchronous boundaries.
- Values returned from an external system after they have been validated or normalized.

Do not mechanically annotate obvious local variables merely to increase annotation count. Add a local annotation when inference is unclear, intentionally broad, or part of an important invariant. Types should improve a reader's model of the program, not obscure it with noise.

Use types to clarify a real contract. Do not distort an API, introduce needless wrapper classes, or replace clear runtime validation solely to satisfy a checker.

## Typing Choices

Use current syntax only when the project's minimum Python version supports it. In supported modern Python, prefer precise built-in generics and explicit nullability:

```python
from collections.abc import Iterable, Mapping


def index_names(records: Iterable[Mapping[str, str]]) -> dict[str, str]:
    """Maps each record identifier to its display name."""
    return {record["id"]: record["name"] for record in records}


def load_label(label: str | None) -> str:
    """Returns the configured label or the documented default."""
    return "default" if label is None else label
```

Prefer `collections.abc` interfaces such as `Iterable`, `Sequence`, `Mapping`, and `Callable` when a function accepts behavior rather than a particular concrete container. Use `list`, `dict`, or `set` when the function requires their mutation or concrete semantics.

Use a `Protocol` for a small, stable collaboration boundary when the implementation only needs a shape, such as a clock, storage adapter, or sender. Use a `TypedDict`, dataclass, or validated model to represent structured data according to its lifecycle. Do not add protocols or elaborate generic hierarchies for a single implementation without a present substitution or testing need.

Avoid bare generics such as `list` or `dict`; specify element types. Use `object` when a value is intentionally unknown and must be narrowed before use. Use `Any` only at a justified dynamic boundary or where the checker cannot model a sound interaction. `Any` disables checking transitively, so validate and convert external JSON, environment values, plugin data, and untyped library results as early as possible.

## Suppressions and Untyped Boundaries

A suppression is a narrow exception to static checking, not a cleanup mechanism. Prefer correcting a type, narrowing with a guard, improving a local stub, or isolating untyped code at a boundary.

When a suppression is necessary, use the smallest scope, name the diagnostic when the tool supports it, and record the reason next to it:

```python
value = legacy_client.fetch()  # type: ignore[no-any-return]  # Validated by parse_value().
```

Apply the same discipline to lint suppressions. A broad `# type: ignore`, `# noqa`, or tool-wide exclusion can hide later regressions and requires a compelling, documented reason. Do not add suppressions merely because a tool was invoked with a mode stricter than the project supports.

For legacy code, type public and cross-module boundaries first. Expand inward as contracts stabilize. A partial, accurate boundary is more valuable than mass annotations that encode guesses.

## Exception Design

Exceptions represent abnormal outcomes, not ordinary branching. Use built-in exceptions when their meaning matches the contract: `ValueError` for invalid values, `TypeError` for incompatible argument types, `KeyError` for a missing required key, and `LookupError` for a failed lookup. A library may define a domain exception when callers need to distinguish a meaningful failure class; name it with an `Error` suffix and inherit from an appropriate built-in exception.

Validate user-facing or public preconditions with ordinary conditionals and explicit exceptions. Do not rely on `assert` for required runtime behavior because assertions may be disabled. Assertions are appropriate for internal invariants whose removal must not change correct behavior.

Exception messages must identify the failed condition without inventing a cause. Include safe, relevant context such as an identifier, expected range, or operation. Do not expose secrets, credentials, raw personal data, or implementation details that make an error harder to act on.

## Handling and Translating Errors

Catch the most specific exception that the current layer can actually handle. Keep the `try` block narrow so an unrelated programming error is not mislabeled as an expected operational failure.

```python
try:
    raw_config = path.read_text(encoding="utf-8")
except OSError as error:
    raise ConfigurationError(f"Could not read configuration at {path}") from error

return parse_config(raw_config)
```

When translating an infrastructure exception into a domain-level contract, preserve causal context with `raise ... from error`. Let exceptions propagate when the current layer cannot recover, add useful context, or make a policy decision. Library and domain layers should normally raise rather than call `sys.exit()`; command-line entry points decide exit codes and user-facing presentation.

Never silently swallow an exception. A handler must recover with a defined outcome, return an explicit partial-result status, re-raise, or surface the failure at the boundary. Broad `except Exception` is reserved for a genuine isolation boundary, such as a worker supervisor, and must record enough context to diagnose the suppressed failure. Never use bare `except:` for routine handling; it also catches interrupts and system exits.

Use context managers for files, sockets, transactions, locks, and other closeable resources. Cleanup that cannot be expressed by a context manager belongs in a narrowly scoped `finally` block with its ownership made clear.

## Logging

Use a module-level logger and allow the application entry point to configure handlers, formatters, levels, and destinations. Libraries should emit useful records but should not configure global logging as an import-time side effect.

```python
import logging

logger = logging.getLogger(__name__)


def refresh_cache(cache_key: str) -> None:
    """Refreshes the cache entry identified by cache_key."""
    logger.info("Refreshing cache entry %s", cache_key)
```

Use parameterized logging: pass a literal format string and values as separate arguments. Do not use f-strings, eager `%` formatting, or string concatenation in logging calls. Parameterized calls avoid work when the level is disabled and preserve useful structure for log processors.

Log at the layer that owns the response to an error. If a lower layer logs an exception and re-raises it, callers often create duplicate stack traces with no additional information. At a boundary that handles an error, use `logger.exception()` while inside the handler to retain the traceback, then return or raise according to the boundary contract.

Choose levels by operational meaning: `DEBUG` for diagnostic detail, `INFO` for significant normal events, `WARNING` for unexpected but recoverable conditions, `ERROR` for an operation that failed, and `CRITICAL` for process-threatening conditions. Do not use logs as a substitute for a caller-visible error contract.

Include identifiers, operation names, and state needed to investigate an event, but never log secrets, authorization headers, passwords, tokens, private keys, or complete sensitive payloads. Redaction must happen before the value reaches the logging call.

## Review Checklist

- Are public and cross-module contracts annotated accurately?
- Does each use of `Any`, `cast`, or a suppression have a concrete reason and narrow scope?
- Are external values validated before the typed core relies on them?
- Does each handler catch a specific exception and cover only the intended operation?
- Does translated error handling preserve the original cause with `raise ... from error`?
- Can callers distinguish success, failure, and partial success without inspecting logs?
- Are resources closed deterministically?
- Are logs parameterized, contextual, non-duplicative, and free of secrets?
