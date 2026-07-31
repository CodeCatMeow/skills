# Function and Class Design

## Contents

- [Design for the current requirement](#design-for-the-current-requirement)
- [Functions should make one decision or action clear](#functions-should-make-one-decision-or-action-clear)
- [Shape usable function interfaces](#shape-usable-function-interfaces)
- [Separate calculation from effects](#separate-calculation-from-effects)
- [Extract helpers when they create a real unit](#extract-helpers-when-they-create-a-real-unit)
- [Choose functions, data objects, and classes deliberately](#choose-functions-data-objects-and-classes-deliberately)
- [Keep class boundaries and public APIs small](#keep-class-boundaries-and-public-apis-small)
- [Prefer composition to inheritance](#prefer-composition-to-inheritance)
- [Introduce abstractions only under present pressure](#introduce-abstractions-only-under-present-pressure)
- [Treat size metrics as review signals](#treat-size-metrics-as-review-signals)

## Design for the Current Requirement

The aim is not maximum flexibility. It is the smallest clear design that satisfies current behavior while leaving ordinary changes understandable. Add an abstraction when a concrete pressure exists now: real duplication, multiple implementations, an external boundary, or a stable behavior that needs independent testing. "We might need it later" is not evidence.

Prefer code that can be straightforwardly changed after a new requirement arrives over speculative factories, registries, base classes, generic configuration objects, or plugin systems. Simple, well-named concrete code is usually the best preparation for an uncertain future.

## Functions Should Make One Decision or Action Clear

A function should have one primary responsibility at one useful level of abstraction. Its name should tell a caller what it does without needing a comment to decode it.

```python
# Avoid: validation, calculation, persistence, and notification share one function.
def process_order(order: Order, database: Database, mailer: Mailer) -> Receipt:
    if not order.items:
        raise ValueError("order must contain items")
    total = sum(item.price * item.quantity for item in order.items)
    database.save(order, total)
    mailer.send(order.customer.email, f"Total: {total}")
    return Receipt(order.id, total)

# Prefer: names expose the separate responsibilities.
def calculate_order_total(order: Order) -> Decimal:
    if not order.items:
        raise ValueError("order must contain items")
    return sum((item.price * item.quantity for item in order.items), Decimal())

def complete_order(order: Order, database: Database, mailer: Mailer) -> Receipt:
    total = calculate_order_total(order)
    database.save(order, total)
    mailer.send_receipt(order.customer.email, total)
    return Receipt(order.id, total)
```

The orchestration function may legitimately coordinate several steps. Keep it readable, keep policy in named collaborators or pure functions, and do not turn it into a second implementation of each step.

Use verbs for actions, nouns for values, and question-like names for booleans: `parse_header`, `calculate_total`, `is_expired`, `has_access`. Use the project's domain vocabulary consistently.

## Shape Usable Function Interfaces

A function signature is a contract. Make required inputs clear, options hard to confuse, and return values stable enough for callers to use without studying the implementation.

### Keep parameters purposeful

```python
# Avoid: callers must memorize positional flags and ordering.
export(records, True, False, "csv", 1000)

# Prefer: the subject is positional; options name themselves.
def export(
    records: list[Record],
    *,
    include_headers: bool = True,
    compress: bool = False,
    format: str = "csv",
    batch_size: int = 1000,
) -> bytes:
    ...
```

Use keyword-only parameters for booleans, related options, or values that are easy to misorder. Do not make every parameter keyword-only when two or three positional arguments form an obvious, stable phrase at the call site.

When a signature contains many related settings, consider a named configuration dataclass only if the options are already a coherent value that is passed, compared, reused, or independently validated. Do not introduce a generic `config: dict` merely to reduce parameter count.

### Return one clear shape

```python
# Avoid: a caller must branch on unrelated return forms.
def locate_user(user_id: str) -> User | str | None:
    ...

# Prefer: return the successful value or raise a meaningful domain error.
def locate_user(user_id: str) -> User:
    ...
```

Use `None` for a normal, documented absence when it is unambiguous. Use an exception when absence violates the function's contract. For multiple related outputs, use a named tuple, dataclass, or domain value rather than an unlabelled tuple whose positions callers must memorize.

### State mutations and effects plainly

A function that mutates an input, writes data, sends a request, or consumes an iterator should make that behavior apparent in its name, documentation, or return contract. Avoid a routine that looks like a query but changes state.

```python
# Avoid: the name suggests inspection, but the input is changed.
def validate(records: list[Record]) -> list[Record]:
    records[:] = [record for record in records if record.is_valid]
    return records

# Prefer: either return a new value or make mutation explicit.
def valid_records(records: list[Record]) -> list[Record]:
    return [record for record in records if record.is_valid]

def remove_invalid_records(records: list[Record]) -> None:
    records[:] = [record for record in records if record.is_valid]
```

## Separate Calculation From Effects

Keep decisions, validation, and transformations independent from I/O where that separation matches the task. A pure function accepts values and returns values; it is easy to test and reuse without mocks. Filesystems, databases, network clients, clocks, and user interfaces belong near the orchestration boundary.

```python
# Avoid: parsing policy is tied to a file and cannot be tested directly.
def load_threshold(path: Path) -> int:
    return int(path.read_text(encoding="utf-8").strip())

# Prefer: keep the decision reusable, place I/O at the edge.
def parse_threshold(text: str) -> int:
    return int(text.strip())

def load_threshold(path: Path) -> int:
    return parse_threshold(path.read_text(encoding="utf-8"))
```

Do not force an artificial split for a three-line operation with no reusable logic. Separate effects when doing so clarifies ownership, isolates a dependency, or creates a directly testable rule.

## Extract Helpers When They Create a Real Unit

Extract a helper when it has a nameable responsibility, independent edge cases, real reuse, or a distinct abstraction level. Keep logic inline when extraction would force readers to jump to a trivial wrapper before they can understand the main flow.

```python
# Avoid: a long predicate is repeated and hides a business rule.
if user.is_active and user.email_verified and not user.is_suspended:
    grant_access(user)
if user.is_active and user.email_verified and not user.is_suspended:
    send_digest(user)

# Prefer: the rule earns a domain name.
def can_receive_member_services(user: User) -> bool:
    return user.is_active and user.email_verified and not user.is_suspended
```

```python
# Avoid: a helper adds a name but no boundary.
def get_name(user: User) -> str:
    return user.name

# Prefer: use the attribute directly.
notify(user.name)
```

Do not split a function at every blank line. A sequence of short steps may be clearest in one function when the steps are only meaningful in that local workflow.

## Choose Functions, Data Objects, and Classes Deliberately

Use the lightest construct that accurately models the current need.

| Need | Prefer |
|---|---|
| Stateless transformation or policy | module-level function |
| Named value with stable fields | `@dataclass` or another value type |
| Stable concept with state, invariants, or lifecycle | class |
| Resource that must be acquired and released | context-manager-capable class or helper |
| A real interchangeable capability | narrow `Protocol`, callable, or small interface |

### Prefer functions for stateless behavior

```python
# Avoid: a class exists only to hold one stateless method.
class SlugFormatter:
    def format(self, title: str) -> str:
        return title.strip().lower().replace(" ", "-")

# Prefer.
def format_slug(title: str) -> str:
    return title.strip().lower().replace(" ", "-")
```

A class is useful when its instances represent a stable domain thing, carry state through a lifecycle, enforce invariants across operations, own a resource, or group behavior around an identity. Do not create `Manager`, `Handler`, `Processor`, or `Service` classes just to make free functions look object-oriented.

### Prefer dataclasses for data, not behaviorless ceremony

```python
# Avoid: boilerplate obscures a small value object.
class Window:
    def __init__(self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end

# Prefer.
from dataclasses import dataclass

@dataclass(frozen=True)
class Window:
    start: datetime
    end: datetime
```

Add methods when they preserve the value's invariants or express behavior natural to that concept. Do not turn a dataclass into a container for unrelated application operations.

## Keep Class Boundaries and Public APIs Small

A class should represent one stable concept and expose the smallest surface its callers need. Keep internal details private with a single leading underscore; avoid double-underscore name mangling unless a subclass name collision is the actual problem.

```python
# Avoid: a general-purpose object accumulates unrelated ownership.
class AccountManager:
    def validate_account(self, account: Account) -> None: ...
    def save_account(self, account: Account) -> None: ...
    def send_welcome_email(self, account: Account) -> None: ...
    def render_dashboard(self, account: Account) -> str: ...

# Prefer: each object owns a coherent concern.
class AccountRepository:
    def save(self, account: Account) -> None: ...

class WelcomeMailer:
    def send(self, account: Account) -> None: ...
```

Do not create a class per function. The split above is useful because persistence and email have independent dependencies and reasons to change; a simple `validate_account()` function can remain a function.

Keep constructors explicit about the dependencies and state an instance needs. Do not construct hidden global clients inside methods when callers or tests need to control them.

```python
# Avoid: dependency and lifetime are hidden.
class ReportPublisher:
    def publish(self, report: Report) -> None:
        HttpClient().post("/reports", report.to_json())

# Prefer: the boundary is visible and substitutable when needed.
class ReportPublisher:
    def __init__(self, transport: ReportTransport) -> None:
        self._transport = transport

    def publish(self, report: Report) -> None:
        self._transport.send(report.to_json())
```

## Prefer Composition to Inheritance

Composition keeps collaborators explicit and permits each part to evolve separately. Prefer it over inheritance when the goal is only to reuse helpers or swap a dependency.

```python
# Avoid: inheritance is used only to borrow an implementation detail.
class CachedUserRepository(DatabaseUserRepository):
    ...

# Prefer: wrap or compose the capability that varies.
class CachedUserRepository:
    def __init__(self, source: UserRepository, cache: Cache) -> None:
        self._source = source
        self._cache = cache
```

Use inheritance for a genuine, stable "is a" relationship with a contract that subclasses can preserve. Avoid deep hierarchies, base classes that exist only for tests, and subclass hooks with no current consumer.

## Introduce Abstractions Only Under Present Pressure

An abstraction is justified when at least one observable condition exists now:

- The same meaningful behavior is duplicated and the variation is understood.
- Two or more implementations already exist.
- A concrete external dependency needs isolation from policy or test setup.
- A stable replacement boundary is part of the current product requirement.
- Tests must control a real source of nondeterminism or I/O, such as time, randomness, network transport, or storage.

```python
# Avoid: a factory and protocol predict variants that do not exist.
class Formatter(Protocol):
    def format(self, value: str) -> str: ...

def create_formatter(kind: str) -> Formatter:
    return DefaultFormatter()

# Prefer: keep the sole current behavior concrete.
def format_title(value: str) -> str:
    return value.strip().title()
```

```python
# Prefer abstraction once the current boundary is real.
class Clock(Protocol):
    def now(self) -> datetime: ...

def is_expired(token: Token, clock: Clock) -> bool:
    return token.expires_at <= clock.now()
```

Here the injected clock is justified because time is an external, nondeterministic dependency that current tests and behavior need to control. A `Protocol` should describe only the methods actually used. Do not add a broad interface or a dependency-injection framework for one concrete call.

As a practical refactoring heuristic, wait until a repeated behavior appears enough times to reveal what is truly shared and what varies. Three similar occurrences often provide that evidence, but it is not a quota: extract earlier when a real external seam requires it, and later when apparent duplication is likely to diverge for valid domain reasons.

## Treat Size Metrics as Review Signals

Long functions, many parameters, deep nesting, large classes, and multiple public methods are signals to inspect design. They are not automated proof that a split improves the code.

A function flagged during review may still be a cohesive parser, algorithm, or
orchestration routine. A short function may still mix validation, database writes,
HTTP calls, and formatting. When a size or complexity concern appears, review:

- Can the unit be described with one precise responsibility?
- Are different parts changed, tested, or depended on independently?
- Would extraction produce a meaningful name and a simpler contract?
- Would a new function or class clarify the main path, or only force navigation?
- Is an abstraction supported by current use rather than imagined future use?

Choose the design that improves comprehension and change safety. Do not mechanically split code to satisfy a line count, parameter count, or class-size threshold.
