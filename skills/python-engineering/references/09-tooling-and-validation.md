# Tooling and Validation

This reference explains how to select and interpret validation already available in a
project.

## Contents

- [Principles](#principles)
- [Tool selection order](#tool-selection-order)
- [Validation by change risk](#validation-by-change-risk)
- [Interpreting results](#interpreting-results)
- [Missing tools and blocked checks](#missing-tools-and-blocked-checks)
- [Non-mutating tool use](#non-mutating-tool-use)
- [Efficient command scope](#efficient-command-scope)
- [Completion report](#completion-report)

## Principles

Validation should provide reliable evidence about the change without taking control of the project. Prefer the repository's documented workflow and checked-in configuration. Run tools that are already available; do not manufacture a passing result by changing the environment, toolchain, configuration, or test selection.

Tools are evidence sources with different strengths. Syntax checks, formatter checks,
configured lint, configured type checking, and tests can yield deterministic pass/fail
results. Metrics and heuristics from existing project tools, together with the Agent's
own review, can identify code that deserves inspection. Architectural fitness, test
adequacy, and scope appropriateness require semantic judgment.

## Tool Selection Order

Use the first applicable source in this order:

1. The project's documented developer, test, or CI commands.
2. Its existing task runner, scripts, Make targets, tox/nox sessions, or CI workflow commands.
3. Tool configuration already committed in `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg`, or equivalent files.
4. Existing project tools, commonly a formatter/linter such as Ruff, a configured type checker such as Pyright or mypy, and pytest.
5. Minimal built-in checks available in the current environment, such as compiling changed Python files, only when higher-priority project guidance is absent.

Do not treat this order as a requirement to introduce Ruff, a type checker, pytest, coverage, a task runner, or a formatter. A tool not present in the repository or environment is not permission to install or configure it.

Respect project choices. A project using Black must not be switched to Ruff formatting for a one-off task. A project with mypy should not be assessed as though Pyright were authoritative. Do not apply a personal strictness profile over a repository's intentional configuration.

## Validation by Change Risk

Start narrow and widen only as the risk and blast radius justify it.

| Change | Initial validation | Broaden before completion when |
| --- | --- | --- |
| Documentation or comments only | Markdown or documentation checks already configured | The edit affects generated documentation or API-facing material |
| Local Python implementation | Syntax plus directly related formatter/linter/type/test checks that exist | Shared utility, public contract, or widely imported code changed |
| Bug fix | New or existing focused regression test | The defect crosses modules, has user-visible impact, or touches a critical path |
| New public API or changed contract | Focused tests, configured lint/type checks, relevant callers | Compatibility, serialized formats, plugins, or downstream packages are affected |
| Refactor or module move | Focused behavior tests plus import and type checks | Multiple packages, public imports, or dependency boundaries moved |
| Concurrency, persistence, security, money, destructive I/O, or production operations | Focused tests and the relevant configured suite | The consequence of failure warrants integration, migration, or environment-specific evidence |

Run affected tests first for fast feedback. Then run the widest reasonable configured check for the change. Do not claim an entire suite passed when only a focused test ran.

## Interpreting Results

Classify output precisely.

| Result class | Examples | Meaning and response |
| --- | --- | --- |
| Hard failure | Syntax error, formatter check failure, configured lint/type failure, failed test, failed import check | The executed validation did not pass. Fix it, obtain an explicit exception from the user, or report the unresolved failure plainly. |
| Soft structural signal | A project tool or code review identifies a large module, long function, broad parameter list, complex dependency graph, or generic module name | Review cohesion and scope. The signal never automatically requires splitting or blocks a correct change by itself. |
| Semantic judgment | Whether an API is clear, a module has one responsibility, a test proves the contract, or a refactor is proportionate | Evaluate with codebase context and user intent. Explain the decision when it is consequential. |
| Unavailable validation | Missing executable, absent dependency, unavailable service, unsupported platform, inaccessible credential | The check did not run. Report its absence and any alternative evidence; never represent it as a pass. |

A tool's exit status does not settle semantic questions. Conversely, clean results from
available tools do not prove that a design is coherent. Treat tool output and code
review observations as inputs to engineering judgment.

## Missing Tools and Blocked Checks

Check whether a command and its dependencies already exist before relying on it. Do not automatically install packages, create virtual environments, run a package manager, download binaries, modify lock files, edit `pyproject.toml`, adjust test configuration, change tool versions, or relax rules to make validation pass.

When a useful check cannot run, report:

- The command or tool that was unavailable.
- The concrete reason, such as `ruff` not found, dependencies not installed, or integration credentials absent.
- The scope that was therefore not validated.
- Any smaller check that did run, clearly labeled as partial evidence.

For example: "`pytest` could not run because the project's test dependencies are absent; `python -m compileall` passed for the two changed modules. Test behavior remains unverified." This is useful and honest. Do not substitute a manual assertion of success for an unavailable test suite.

## Non-Mutating Tool Use

Default validation commands must be read-only with respect to source and project configuration. Prefer check modes over auto-fix modes, such as formatter `--check` or lint without `--fix`. Do not run commands that rewrite source, lock files, generated artifacts, snapshots, caches, migrations, dependencies, or configuration unless the user explicitly requests that effect and its output is part of the task.

Do not silence failures by adding `# noqa`, `# type: ignore`, skip markers, exclusions, baseline files, or coverage exceptions unless the source change itself has a justified, reviewed need. A suppression must name the narrow diagnostic where supported and state why it is safe.

Do not use tool output to override user requirements, existing public contracts, or project conventions. Tools enforce their configured subset of rules; they do not authorize unrelated formatting or modernization.

## Efficient Command Scope

Inspect the changed files, nearby tests, and existing configuration before choosing commands. During editing, use file-level or test-node-level checks where the project supports them. Before completion, expand to the affected package or suite when the change reaches shared behavior.

Avoid expensive full-repository validation for a trivial isolated edit when it adds no meaningful evidence. Conversely, do not stop at a single file check after changing a shared API, package boundary, build configuration, or central utility. Make the chosen scope explicit when reporting results.

Limit displayed diagnostics to actionable failures from the commands run. Preserve enough context to locate the issue, but do not bury the result under unrelated warnings or thousands of lines of passing output.

## Completion Report

A concise validation report states:

- What changed and the validation scope selected.
- Which commands passed, grouped by formatter/lint/type/test or equivalent project terms.
- Any hard failures, unavailable checks, or remaining risks.
- Any structural signals reviewed and the resulting design decision when material.

Do not say "all checks passed" unless every applicable planned check ran and passed. Prefer precise statements such as "the targeted pytest module and configured Ruff checks passed; no project type-check command is configured" or "tests were not run because the environment lacks the project's dependencies."
