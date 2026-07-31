# Testing and Change Safety

## Contents

- [Testing is risk-scaled](#testing-is-risk-scaled)
- [Choose the minimum credible evidence](#choose-the-minimum-credible-evidence)
- [Bug fixes and behavior changes](#bug-fixes-and-behavior-changes)
- [Test design](#test-design)
- [Fixtures, doubles, and boundaries](#fixtures-doubles-and-boundaries)
- [Determinism](#determinism)
- [Running tests safely](#running-tests-safely)
- [When evidence is incomplete](#when-evidence-is-incomplete)

## Testing Is Risk-Scaled

Testing protects behavior; it is not a ritual for maximizing test count or enforcing full test-driven development on every edit. Scale the evidence to the consequence of being wrong, the uncertainty of the change, and the cost of a regression.

Use this guide when deciding test scope:

| Change profile | Minimum evidence | Usually appropriate additions |
| --- | --- | --- |
| Comment, docstring, or formatting-only edit | Relevant formatter, linter, or syntax check if available | No new behavioral test unless behavior changed indirectly |
| Tiny local change with clear existing coverage | Run the closest existing test | Add a focused test if the changed behavior was not already asserted |
| New non-trivial behavior | Focused automated tests for expected behavior, key boundary, and meaningful failure path | Relevant integration test when it crosses a real boundary |
| Bug fix | A regression test that demonstrates the reported failure before or alongside the fix | Validate that the test fails when the defect is restored when practical |
| Public API, persistence, security, concurrency, financial, or data-loss change | Focused unit tests plus boundary or integration evidence appropriate to the interface | Broader relevant suite, migration/compatibility checks, review of rollback and observability |
| One-off script or exploratory analysis | A minimal smoke run with representative input and an explicit expected output or invariant | Tests for destructive, repeatable, or reused logic |
| Scientific or data transformation code | Tests for shapes, units, ranges, invariants, and reproducibility | Known-result fixtures or property tests for transformations |

TDD is valuable where it improves design or clarifies an uncertain contract. It is not mandatory for every edit. For a bug fix, a failing regression test is the preferred default because it proves the fix reaches the actual defect. If reproducing it is infeasible, state why and provide the strongest available evidence rather than claiming equivalent confidence.

## Choose the Minimum Credible Evidence

Start with the behavior that changed and ask what observation would prove it works. Prefer a small, direct test over a broad suite that happens to execute the code without asserting the contract.

Test observable outcomes: returned values, raised exceptions, persisted state, emitted events, rendered output, and interactions at a genuine external boundary. Avoid tests that mirror private implementation steps. If a private helper needs isolated tests to be understandable, consider whether it has become a cohesive unit that deserves a clear module or public-internal contract.

A focused test should normally cover:

- The simplest meaningful success case.
- The boundary most likely to be mishandled, such as empty input, a limit, or a missing optional value.
- A specified failure or rejected input when the behavior can fail.

Use parametrization for a compact table of equivalent cases. Use property-based testing only when the input space is broad and there is a stable invariant, such as a round trip, order preservation, or a conservation rule. Do not add a property-testing dependency solely for a handful of examples.

## Bug Fixes and Behavior Changes

For a reported defect, write or identify a test that captures the bad input and expected corrected behavior. It should fail for the defect, not because of collection, an unrelated setup failure, or a missing dependency. After the fix, run that regression test first, then the closest relevant suite.

When behavior intentionally changes, update tests to describe the new contract and remove or revise tests that preserve the old contract. Do not silently weaken assertions to make an intentional behavior change pass. Document compatibility changes at the project-appropriate boundary, especially for public APIs, serialized data, or command-line behavior.

For high-consequence fixes, independently challenge the test once where practical: temporarily restore the faulty condition or mutate the changed guard and confirm the focused test becomes red. This is evidence that the test protects the defect rather than merely executing nearby code.

## Test Design

Name tests after the state and expected result, not the implementation detail. Keep setup close to the test unless it is truly shared. One test may assert a cohesive outcome, but avoid unrelated assertions that make failures ambiguous.

```python
def test_parse_port_rejects_values_below_the_unprivileged_range() -> None:
    with pytest.raises(ValueError, match="at least 1024"):
        parse_port("443")
```

Use assertions that could fail for the regression being tested. Do not guard assertions with conditionals, accept multiple incompatible outcomes, or assert only that a result exists when its contents matter. For generated or serialized output, check the complete relevant structure and count duplicates where duplicates would be harmful.

Prefer tests through a public interface. A test that requires deep patching of unrelated collaborators signals a boundary problem; improve the seam only when it simplifies the current change or isolates a real external dependency.

## Fixtures, Doubles, and Boundaries

Fixtures should be minimal, explicit, and independent. Default to function-scoped mutable state. Use wider scope only for immutable or deliberately shared setup whose lifecycle is understood. Every fixture that allocates a resource must clean it up deterministically, typically with `yield`, a context manager, or framework-provided temporary paths.

Use a fake, stub, or mock at an external boundary to avoid slow, unavailable, costly, or non-deterministic dependencies. Prefer the lightest double that proves the behavior. A fake must honor the parameters that the code is meant to handle; a canned response that ignores pagination, filters, or timeouts cannot prove those paths work.

Mock where the looked-up dependency is used, not where it was originally defined. Do not mock the function under test or each internal helper. Excessive interaction assertions bind a test to implementation details and make benign refactoring expensive.

## Determinism

Tests must control their inputs. Do not rely on wall-clock time, random global state, current working directory, locale, environment variables, network availability, filesystem contents outside temporary directories, execution order, or module caches left by earlier tests.

Inject or freeze time, pass a seeded random generator, use temporary directories, pin the environment variables that influence the code path, and reset mutable module state before and after tests that use it. Mark true integration tests clearly and keep their setup distinct from unit tests. A test that reaches a live service by accident is neither reliable nor a substitute for an integration contract.

## Running Tests Safely

Follow the project's documented commands and configured test runner first. During implementation, run the narrowest relevant test after a meaningful change. Before completion, widen validation in proportion to risk: directly affected tests first, then the package, service, or suite that can reasonably be impacted.

Do not install test tools, alter dependencies, edit test configuration, loosen coverage thresholds, add skips, or change markers to manufacture a green result. If a required tool or environment is absent, report the exact command that could not run and what evidence was obtained instead.

A passing test run is a hard result only for the tests actually executed. It is not evidence that unrun tests, unconfigured checkers, or unavailable integrations passed.

## When Evidence Is Incomplete

State the remaining uncertainty explicitly. Distinguish these cases:

- **Hard failure:** A test that ran failed, collection failed, or the test command returned non-zero. Do not report completion as validated.
- **Unavailable validation:** The appropriate test command could not run because a required tool, dependency, service, credential, or platform is unavailable. Report this as unexecuted, not passed.
- **Soft structural signal:** The change required many mocks, grew a complex fixture, or made a test difficult to set up. Review the design, but do not present the signal as a failing test.
- **Semantic judgment:** Decide whether the test asserts the right user-visible contract and whether the scope is proportionate to risk. Tools cannot make this decision.
