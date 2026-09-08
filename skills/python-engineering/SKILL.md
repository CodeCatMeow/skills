---
name: python-engineering
description: >
  Apply concise engineering guardrails whenever creating, modifying, debugging,
  testing, reviewing, refactoring, or organizing Python code. Follow repository
  conventions and Google Python Style, keep changes scoped, use risk-matched
  evidence, and use uv for Python workflows.
user-invocable: true
disable-model-invocation: false
---

# Python Engineering

Write clear Python that fits the repository and the task at hand.

## Work in the existing system

Before a meaningful change, inspect the target code, its direct callers, relevant
tests, and project configuration. Preserve public imports, signatures, exceptions,
side effects, serialized forms, and CLI behavior unless the task changes their
contract.

Make the smallest coherent change and keep unrelated cleanup separate. Let the
repository's Python version, formatter, linter, type checker, and established
conventions take precedence over generic preferences.

## Follow Google Python Style

Where the repository has no conflicting convention:

- use standard naming and explicit imports;
- keep control flow direct and exception handling narrow;
- make module state and external work explicit;
- annotate public and cross-module boundaries when types clarify the contract; and
- write concise Google-style docstrings for public APIs and for behavior whose
  contract is not evident from its name, signature, and short body.

Comments and docstrings should explain contracts, intent, or non-obvious constraints
instead of repeating the code.

## Keep responsibilities coherent

Place new behavior with the code that owns its concept. Extract an adjacent module
when a concern has distinct vocabulary, dependencies, lifecycle, interface, or a
useful test boundary. Base that decision on responsibility rather than file length;
small cohesive modules and larger cohesive modules are both valid.

Introduce abstractions for variants that exist now. Prefer a direct function or
class until a shared interface, factory, protocol, or registry solves a concrete
problem in the project.

## Validate the real risk

For a bug, reproduce the reported failure when practical. A regression test is
valuable when it fails on the defect and protects observable behavior.

Choose evidence by failure mode:

- deterministic logic: focused unit tests;
- parsing or transformation: representative real samples and edge cases;
- files, services, databases, and public interfaces: contract or integration checks
  plus a realistic smoke test;
- small low-risk edits: the nearest existing checks.

Exercise the boundary where failure is expected. If realistic validation is
unavailable, report the remaining gap clearly.

## Use uv

Use uv for Python commands, environments, dependencies, and requirements migration.
Follow the dedicated uv skill for exact commands and migration policy, while
preserving the repository's locked environment.

Finish when the requested behavior works, the change remains scoped, and the
strongest practical evidence matches the real risk.
