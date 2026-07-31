# Google Docstrings

## Contents

- [Authority and applicability](#authority-and-applicability)
- [Universal form](#universal-form)
- [Module docstrings](#module-docstrings)
- [Callable docstrings](#callable-docstrings)
- [Section rules](#section-rules)
- [Class, exception, and property docstrings](#class-exception-and-property-docstrings)
- [Overrides and small private helpers](#overrides-and-small-private-helpers)
- [Comments versus docstrings](#comments-versus-docstrings)
- [Executable templates](#executable-templates)
- [Review procedure](#review-procedure)

## Authority and applicability

This is the Python Engineering skill's only normative format specification for
Google-style docstrings. Do not combine it with NumPy, Sphinx field-list, Epytext, or
ad hoc section formats in the same project unless a higher-precedence project rule
requires a different format. The precedence rules in
[00-precedence-and-scope.md](00-precedence-and-scope.md) still apply.

Use this specification for public modules, classes, functions, methods, generators,
and properties. A function or method also requires a docstring when it is non-trivial
in size or has logic that a caller cannot infer from its name and signature. A tiny,
private helper whose name and signature state its complete contract does not need a
mechanical sentence.

A docstring describes the calling contract: what callers supply, what they receive,
what observable effects occur, and what interface-level failures mean. It does not
narrate local variables or algorithm steps that callers need not know. Put those
implementation explanations in nearby comments.

## Universal form

Every docstring uses triple double quotes: `"""`. The opening summary is one physical
line of at most 80 characters and ends with a period, question mark, or exclamation
mark. The summary may be descriptive (for example, `"""Fetches cached records."""`) or
imperative (for example, `"""Fetch cached records."""`); keep one choice consistent
within a file.

A one-line docstring opens and closes on that line. A multi-line docstring has this
shape:

```python
"""Summarizes the public contract.

Explains caller-relevant behavior in one or more complete paragraphs.

Args:
    source: Identifies the data to read.
"""
```

The blank line after the summary is required when more text follows. The body begins
at the same column as the opening quotes. Section headings end in a colon. Entries and
continuation lines use a consistent hanging indent of either two or four spaces within
a file. Use normal spelling, capitalization, grammar, and punctuation.

## Module docstrings

A non-test Python module begins with a module docstring after any required license
boilerplate and before imports. It states the module's contents, purpose, and necessary
usage. It may identify central exports or include a short usage example when that
would help a reader use the module without opening its implementation.

```python
"""Loads and validates experiment configuration.

Typical usage:

    config = load_config(config_path)
"""
```

A test module has no required docstring. Add one only when it gives useful execution,
environment, fixture, golden-file, or other non-obvious setup information. Do not add
an empty label such as `"""Tests for configuration."""`.

Keep the repository's required license header exactly as configured. A docstring does
not replace that header.

## Callable docstrings

For a required callable docstring, begin with the operation's caller-visible meaning.
Then add a concise behavior paragraph when the summary alone cannot answer how to call
it safely. Include sections only when they add contract information:

- `Args:` for parameters whose meaning, constraints, defaults, units, permitted values,
  `None` meaning, mutation, or relationship to other arguments is not fully obvious.
- `Returns:` for a non-`None` result when the summary and type annotation do not already
  state its semantic value.
- `Yields:` instead of `Returns:` for a generator; describe each value produced by
  `next()`, not the generator object.
- `Raises:` for exceptions that are meaningful promises of the interface.

The docstring must disclose caller-relevant side effects, including mutation of an
argument, persistent writes, network calls with material semantics, caching behavior
that affects callers, or consumption of an iterator. It must also state important
preconditions that the signature cannot express.

A function that returns only `None` normally omits `Returns:`. A concise summary that
starts with `Returns`, `Return`, `Yields`, or `Yield` may replace a redundant result
section when it fully conveys the value. This exception does not allow a summary to
hide important tuple shape, ownership, or failure semantics.

## Section rules

### `Args:`

List parameters in signature order by their exact spelling. Include `*args` and
`**kwargs` with their asterisks. Each entry has the parameter name, a colon, and a
caller-focused description. When the signature lacks an annotation, include needed
type information in the description. Do not repeat an obvious annotation solely to
satisfy the section.

```python
Args:
    timeout_seconds: Maximum time to wait. `None` disables the timeout.
    *paths: Candidate files, evaluated in order.
    **options: Parser settings forwarded to the selected reader.
```

Describe defaults when their behavior is non-obvious, and record units, ranges,
accepted formats, ownership, mutation, and `None` semantics when relevant. Wrap a long
description with a hanging indent that matches the file's established two- or four-space
style.

### `Returns:` and `Yields:`

Describe semantic content, not merely the Python type. If a type annotation already
says `dict[str, Result]`, explain what keys identify and what the result represents.
For a tuple, document it as one tuple and explain its elements rather than presenting
unnamed pseudo-return values.

```python
Returns:
    A tuple (accepted, rejected), where accepted contains normalized records and
    rejected contains input records that failed validation.
```

Use `Yields:` for generators even if the generator is also annotated with an iterator
type. State any important ordering, laziness, or resource-lifetime behavior.

### `Raises:`

List only exceptions callers can reasonably depend on or need to handle. Name each
exception followed by a colon and the triggering condition.

```python
Raises:
    FileNotFoundError: The configured input file does not exist.
    ConfigError: The file exists but violates the supported configuration schema.
```

Do not make unspecified behavior after violating a documented precondition part of the
API by cataloging every internal `ValueError`, `KeyError`, or implementation failure.
Document a translated domain error when it is the intended stable contract.

### `Attributes:`

Public class attributes, excluding properties, belong in `Attributes:` in the class
docstring. Format entries exactly as `Args:` entries. Describe their public meaning,
not private storage or constructor assignments.

## Class, exception, and property docstrings

A class docstring begins by describing the object represented by an instance. Do not
begin with empty phrasing such as `Class that ...`. An exception docstring describes
the error state represented, rather than saying only that it is raised somewhere.

```python
class CacheEntry:
    """A validated value stored with its expiration time.

    Attributes:
        value: Application value available before expiration.
        expires_at: UTC timestamp after which the value is stale.
    """


class ConfigurationError(ValueError):
    """A configuration value violates the supported schema."""
```

A property docstring describes the attribute itself, such as `"""The configured cache
directory."""`, rather than using a method-style `Returns ...` summary. Properties
must not conceal expensive, remote, or surprising work; use a method for that contract.

## Overrides and small private helpers

An overridden method may omit its docstring only when it is explicitly marked with
`@override` from `typing` or `typing_extensions` and preserves the base method's
contract. If it refines behavior, adds meaningful side effects, changes constraints,
or needs caller guidance, document those differences directly on the override.

A private helper does not earn a docstring solely because it exists. Add one when its
algorithm, return convention, error behavior, state change, or resource ownership is
non-obvious. The result must contain information a reader cannot get from its name,
signature, and short body.

## Comments versus docstrings

Use a docstring for a stable interface contract. Use a block or inline comment for a
local implementation rationale, a protocol quirk, an algorithmic invariant, a security
constraint, or a surprising step. Do not put implementation walkthroughs in a public
API docstring, and do not use comments to avoid documenting a caller-visible effect.

## Executable templates

```python
def load_records(
    path: Path,
    *,
    strict: bool = True,
) -> list[Record]:
    """Loads records from a validated input file.

    Args:
        path: File containing one serialized record per line.
        strict: When true, rejects the file if any record is invalid. When false,
            returns valid records and skips invalid lines.

    Returns:
        Records in their input order after successful parsing and validation.

    Raises:
        FileNotFoundError: path does not identify an existing file.
        RecordFormatError: strict is true and an input line is invalid.
    """
```

```python
def iter_batches(records: Iterable[Record], size: int) -> Iterator[list[Record]]:
    """Yields consecutive batches of at most size records.

    Args:
        records: Source records consumed once in input order.
        size: Positive maximum number of records in each yielded batch.

    Yields:
        Lists of records in input order. The final list can contain fewer than size
        records.

    Raises:
        ValueError: size is not positive.
    """
```

## Review procedure

Before finishing a change, verify the following for every new or modified docstring:

1. The docstring uses `"""`, has a punctuated summary within 80 characters, and has
   a blank line after a multi-line summary.
2. The documented callable, class, or module actually needs a docstring under this
   reference, and no empty test-module label was added.
3. `Args:` entries exactly match the signature, including `*args` and `**kwargs`.
4. `Returns:` or `Yields:` describes semantics and follows the callable's execution
   model. A `None`-only callable does not have a meaningless result section.
5. `Raises:` contains interface-level failures rather than accidental implementation
   details.
6. Side effects, mutation, units, ranges, `None` behavior, ordering, and ownership
   are documented whenever they affect a caller.
7. The wording remains true after reading the implementation and tests.
