# Pythonic Idioms

## Contents

- [Use idioms to clarify](#use-idioms-to-clarify)
- [Iteration and collection transforms](#iteration-and-collection-transforms)
- [Values, mappings, and unpacking](#values-mappings-and-unpacking)
- [Resources and paths](#resources-and-paths)
- [Data and standard-library tools](#data-and-standard-library-tools)
- [Control flow and dispatch](#control-flow-and-dispatch)
- [Protocols and lazy pipelines](#protocols-and-lazy-pipelines)
- [Power features need a concrete reason](#power-features-need-a-concrete-reason)

## Use Idioms to Clarify

Pythonic code uses the language's direct vocabulary when it makes the behavior easier to see. It is not code golf, a requirement to use every advanced feature, or a reason to hide important work in one expression.

Choose the form a capable reader can understand in one pass. Expand code when it has nested iteration, several unrelated conditions, mutation or I/O, error handling, or domain rules that deserve names. A shorter expression that requires mental simulation is not clearer.

## Iteration and Collection Transforms

### Iterate over values, not indices

```python
# Avoid: the index has no meaning.
for index in range(len(users)):
    send_notice(users[index])

# Prefer: state the value being processed.
for user in users:
    send_notice(user)
```

Use `enumerate()` only when the position is part of the work.

```python
# Avoid: manual counter maintenance.
line_number = 1
for line in lines:
    report(line_number, line)
    line_number += 1

# Prefer.
for line_number, line in enumerate(lines, start=1):
    report(line_number, line)
```

### Walk related sequences with `zip()`

```python
# Avoid: indexing couples the loop to sequence mechanics.
for index in range(len(names)):
    records.append({"name": names[index], "score": scores[index]})

# Prefer: make the relationship explicit.
for name, score in zip(names, scores, strict=True):
    records.append({"name": name, "score": score})
```

Use `strict=True` when unequal lengths would mean corrupt or incomplete input. Omit it only when truncation to the shorter input is intentional and clear from the contract.

### Use simple comprehensions for a map or filter

```python
# Avoid: ceremony for a single transformation and filter.
normalized = []
for name in names:
    cleaned = name.strip()
    if cleaned:
        normalized.append(cleaned.lower())

# Prefer: one readable data transformation.
normalized = [name.strip().lower() for name in names if name.strip()]
```

A comprehension may combine a small, linear transformation and filter when it remains immediately legible. Do not hide branching, side effects, or nested workflows inside one.

```python
# Avoid: nested loops, mutation, and a non-obvious condition in one expression.
results = [save(item) for group in groups for item in group if validate(item)]

# Prefer: name the stages and make effects visible.
results = []
for group in groups:
    for item in group:
        if not validate(item):
            continue
        results.append(save(item))
```

### Use generator expressions for one-pass consumption

```python
# Avoid: allocate an intermediate list only to sum it.
total = sum([invoice.amount for invoice in invoices])

# Prefer: stream values to the consumer.
total = sum(invoice.amount for invoice in invoices)
```

A generator is single-use. Materialize it when callers need multiple passes, indexing, length, or a stable snapshot.

```python
# Avoid: the second pass silently sees no values.
active_users = (user for user in users if user.is_active)
notify(active_users)
archive(active_users)

# Prefer: preserve reusable data when two consumers need it.
active_users = [user for user in users if user.is_active]
notify(active_users)
archive(active_users)
```

### Express existence and universal conditions directly

```python
# Avoid: flags and break obscure the question being answered.
has_overdue = False
for invoice in invoices:
    if invoice.is_overdue:
        has_overdue = True
        break

# Prefer.
has_overdue = any(invoice.is_overdue for invoice in invoices)
```

```python
# Avoid: an accumulator for a direct universal check.
all_valid = True
for record in records:
    if not record.is_valid:
        all_valid = False

# Prefer.
all_valid = all(record.is_valid for record in records)
```

Do not use `any()` or `all()` when the loop must also collect diagnostics or perform work for every item.

## Values, Mappings, and Unpacking

### Unpack values that have a known shape

```python
# Avoid: positional indexing obscures the record shape.
start = interval[0]
end = interval[1]

# Prefer.
start, end = interval
```

Use a starred target when the remaining values are intentionally irrelevant.

```python
# Avoid.
first = columns[0]
remaining = columns[1:]

# Prefer.
first, *remaining = columns
```

Do not unpack a value whose length or ordering is uncertain just to make code shorter.

### Merge mappings declaratively when precedence is simple

```python
# Avoid: repeated mutation hides which value wins.
options = defaults.copy()
options.update(project_options)
options.update(cli_options)

# Prefer: later mappings intentionally override earlier mappings.
options = {**defaults, **project_options, **cli_options}
```

Use explicit validation or named merge steps when conflicting values require policy beyond "last one wins."

### Use mapping methods that match the contract

```python
# Avoid: two lookups and an ambiguous fallback.
if key in headers:
    content_type = headers[key]
else:
    content_type = "application/octet-stream"

# Prefer when absence has a valid default.
content_type = headers.get(key, "application/octet-stream")
```

Do not use `.get()` when a missing key is a contract violation. Direct indexing raises the useful `KeyError`.

```python
# Avoid: turns malformed input into a later, harder-to-debug failure.
account_id = payload.get("account_id")

# Prefer when the key is required.
account_id = payload["account_id"]
```

## Resources and Paths

### Use context managers for owned resources

```python
# Avoid: cleanup depends on every path reaching `close()`.
stream = open(path, encoding="utf-8")
contents = stream.read()
stream.close()

# Prefer: cleanup occurs on success and failure.
with open(path, encoding="utf-8") as stream:
    contents = stream.read()
```

Use `with` for files, locks, transactions, temporary directories, connections, and any object whose lifetime must be ended reliably.

### Use `pathlib` for filesystem paths

```python
# Avoid: string concatenation is platform-sensitive and loses path operations.
report_path = base_dir + "/reports/summary.json"

# Prefer.
from pathlib import Path

report_path = Path(base_dir) / "reports" / "summary.json"
```

Keep paths as `Path` values through filesystem work. Convert to `str` only at an API boundary that specifically requires strings.

## Data and Standard-Library Tools

### Use a dataclass for named, mostly-data state

```python
# Avoid: an unstructured dictionary makes fields and defaults implicit.
retry = {"attempts": 3, "delay_seconds": 1.0}

# Prefer.
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 3
    delay_seconds: float = 1.0
```

A dataclass is appropriate when the value has stable fields and value-like behavior. Do not create one merely to wrap a single temporary value or to imitate a Java bean.

### Reach for focused standard-library types

```python
# Avoid: manually count values and branch for a missing key.
counts: dict[str, int] = {}
for status in statuses:
    counts[status] = counts.get(status, 0) + 1

# Prefer.
from collections import Counter

counts = Counter(statuses)
```

```python
# Avoid: handwritten adjacent-pair indexing.
pairs = [(points[index], points[index + 1]) for index in range(len(points) - 1)]

# Prefer.
from itertools import pairwise

pairs = list(pairwise(points))
```

Use `Counter`, `defaultdict`, `deque`, `itertools`, and `functools` when their names make the shape of the operation clearer. Do not introduce them for a one-off operation that a direct loop explains better.

### Cache only a demonstrated repeatable computation

```python
# Avoid: cache state and invalidation are added before a cost is known.
def load_schema(name: str) -> Schema:
    return parse_schema(read_schema_file(name))

# Prefer when repeated calls, stable inputs, and profiling or scale justify it.
from functools import cache

@cache
def load_schema(name: str) -> Schema:
    return parse_schema(read_schema_file(name))
```

Caching changes memory use, freshness, and observability. Add it for a real repeated cost and define invalidation or lifetime where data can change.

## Control Flow and Dispatch

### Use guard clauses to keep the main path flat

```python
# Avoid: useful work is buried under nested conditions.
def publish(report: Report) -> None:
    if report.is_complete:
        if report.items:
            upload(report)

# Prefer.
def publish(report: Report) -> None:
    if not report.is_complete:
        return
    if not report.items:
        return
    upload(report)
```

A guard should state a meaningful exit condition. Do not fragment a short, readable conditional sequence into guards solely to reduce indentation.

### Use `match` for closed structural alternatives

```python
# Avoid: a growing chain repeats extraction and makes variants hard to scan.
def format_event(event: Event) -> str:
    if event.kind == "created":
        return f"created {event.resource}"
    if event.kind == "deleted":
        return f"deleted {event.resource}"
    raise ValueError(f"unknown event: {event.kind}")

# Prefer when variants have distinct shapes or a closed dispatch is clearer.
def format_event(event: Event) -> str:
    match event:
        case Event(kind="created", resource=resource):
            return f"created {resource}"
        case Event(kind="deleted", resource=resource):
            return f"deleted {resource}"
        case _:
            raise ValueError(f"unknown event: {event.kind}")
```

Keep simple two-way choices as `if`/`else`. Do not use `match` as a novelty replacement for ordinary predicates.

## Protocols and Lazy Pipelines

### Accept the capability needed, not an accidental concrete type

```python
# Avoid: callers must inherit from a base class just to supply one operation.
class FileStore:
    def read_text(self, key: str) -> str: ...

def load_config(store: FileStore, key: str) -> Config:
    return parse_config(store.read_text(key))

# Prefer when multiple implementations already exist or an external boundary needs isolating.
from typing import Protocol

class TextStore(Protocol):
    def read_text(self, key: str) -> str: ...

def load_config(store: TextStore, key: str) -> Config:
    return parse_config(store.read_text(key))
```

A `Protocol` earns its place at a real substitution boundary. Do not define one for every class with one caller or before a second implementation, test double, or boundary requirement exists.

### Build generator pipelines only when streaming is meaningful

```python
# Avoid: eagerly load every log line before filtering.
def error_messages(paths: list[Path]) -> list[str]:
    lines = [line for path in paths for line in path.read_text().splitlines()]
    return [line for line in lines if "ERROR" in line]

# Prefer when input can be large and one-pass processing is intended.
def error_messages(paths: list[Path]):
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            yield from (line.rstrip("\n") for line in stream if "ERROR" in line)
```

Document that the result is an iterator. Do not return a lazy value where callers reasonably expect a reusable collection.

## Power Features Need a Concrete Reason

Keep dynamic attribute access, descriptors, metaclasses, runtime code generation, and deep decorator stacks out of ordinary application code. They are appropriate only when the problem itself needs their capability, such as a framework extension point, declarative field system, or language-interoperability layer.

```python
# Avoid: dynamic dispatch turns a spelling error into runtime behavior.
def call_action(name: str, value: str) -> None:
    getattr(service, name)(value)

# Prefer: an explicit, validated dispatch table.
ACTIONS = {"start": service.start, "stop": service.stop}

def call_action(name: str, value: str) -> None:
    try:
        ACTIONS[name](value)
    except KeyError as error:
        raise ValueError(f"unsupported action: {name}") from error
```

Prefer a direct function, class, or mapping until a real requirement makes a power feature the clearest model. Do not trade maintainability for apparent sophistication.
