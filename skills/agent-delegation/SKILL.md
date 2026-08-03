---
name: agent-delegation
description: Use when the user asks for non-trivial engineering work that should be split across workers or subagents — exploring or inventorying a system, multi-file investigation, bug diagnosis or fix, feature implementation, tests, refactors, batch or script jobs, heavy web research, syncing existing docs after accepted changes, reviewing or accepting important results, or choosing among Haiku, Sonnet, Codex (Luna/Sol), or Grok — even if they never say "delegate", "routing", or a model name. Also use when they ask to actively use subagents, parallel agents, or external workers. Do not use for trivial one-step local edits, pure Q&A with no repo work, or inventing new model rankings outside the fixed routes.
argument-hint: "[task type or worker]"
user-invocable: true
disable-model-invocation: false
---

# Agent Delegation

## Purpose

Keep Claude Code as the only orchestrator while routing atomic work through fixed workers. Ordinary task commands ("examine this system", "fix this bug", "add this feature") count; the user does not need to request delegation. Classify first, dispatch the assigned worker, then accept results:

| Worker | Role |
| --- | --- |
| Claude Haiku subagent | Cheap mechanical internal work |
| Claude Sonnet subagent | Internal analysis that needs real reasoning |
| Codex Luna (`gpt-5.6-luna`, max effort) | Cheap, clear, objectively checkable external execution |
| Codex Sol (`gpt-5.6-sol`, high effort) | Rare high-value external analysis and candidate conclusions |
| Grok Build | Primary project implementation, existing-doc maintenance, and heavy external research |
| Main agent | Route choice with user, final conclusions, important acceptance |

This Skill is a fixed routing and acceptance contract. It is not an agent platform, job queue, or nested multi-agent framework.

- Stale model prices/benchmarks and route evidence: [model routing](references/model-routing.md). Do not invent ad-hoc routes from that file.
- Codex/Grok command forms, permissions, output formats, worktrees, serial/parallel writes, out-of-repo paths, retries, and Luna fallback: [worker execution](references/worker-execution.md). **Read it before** calling Codex or Grok, retrying a worker, using a worktree, running parallel writable workers, or modifying paths outside the repo.

## Non-Negotiable Rules

1. Only the main Claude Code agent may set the work plan with the user, start workers, order tasks, review results, accept or reject important implementations, form the final user-facing conclusion, and decide the next stage.
2. Workers must not call subagents, start Claude/Codex/Grok/other agents, nest delegation, expand scope, choose product or research direction, accept important conclusions, or continue to the next stage on their own.
3. Use fixed routes below. Do not guess which model is smarter, which harness is better, or whether an external agent “might help.” Classify the task, then call the assigned worker.
4. If no route fits, or two conflicting routes both fit: read `references/model-routing.md`, propose one recommendation and at most one alternative, explain the difference, ask the user with `AskUserQuestion`, and do not start an expensive worker before the user chooses.
5. **Proactive default:** if the request needs multi-file exploration, non-trivial analysis, implementation, tests, refactor, batch/script work, external research, or existing-doc sync, route it. Do not wait for the user to say "delegate" or name a worker. If the user asks to actively use subagents, parallel agents, or external workers, load this skill and dispatch by fixed route rather than bulk-doing the work alone. Tiny one-step work that needs no isolation may stay on the main agent. That exception does **not** cover multi-file exploration, bug investigation, feature work, or the fixed Grok Build documentation-maintenance route.
6. Important implementation acceptance is never outsourced. Haiku, Sonnet, Luna, Sol, and Grok may collect evidence or run mechanical checks; only the main agent signs off. Worker claims and exit codes are not completion; require real diffs/artifacts for write tasks.
7. Existing project documentation that must stay in sync with accepted implementation changes is a separate Grok Build task after the implementation is accepted.
8. Prefer official plugin/CLI surfaces. Do not add custom wrapper frameworks for sessions, logs, cancel, model, or effort selection.
9. Writable external workers default to **serial** under Claude Code Auto mode; parallel writes, worktrees, out-of-repo paths, retries, and fallbacks follow [worker execution](references/worker-execution.md). Do not invent looser rules.

## First Move on Ordinary User Commands

When the user issues a normal engineering command without mentioning workers, do this before bulk self-execution:

1. Map the request to one fixed route (or a short sequence of atomic routes).
2. Keep orchestration, trade-offs, and final acceptance on the main agent.
3. Read [worker execution](references/worker-execution.md) when the route needs Codex/Grok, a worktree, retry, parallel write, or out-of-repo path; then dispatch with an atomic prompt and report requirements.
4. Review the worker report and evidence; only then answer the user or continue.

| User says (examples) | Default route |
| --- | --- |
| Examine / inventory this system or its features | Haiku explore, then main-agent synthesis |
| Find where X is handled / list entry points | Haiku |
| This bug happens when … fix it | Sonnet for multi-file diagnosis if needed; Luna for small clear fix; Grok for non-trivial project fix |
| Add feature Y / implement this page or API | Grok Build |
| Clean this CSV / batch transform / make charts | Luna |
| Is this result strong enough to claim Z? | Sol (candidate only), then main-agent recheck |
| Compare current docs and community practice for tool T | Grok research route |
| Actively use subagents / parallel agents | Classify and dispatch fixed routes; do not only self-execute |
| After the change, update the README/docs | Separate Grok doc task after acceptance |

## Fixed Routes

| Task class | Worker | Config |
| --- | --- | --- |
| Read code, explore, inventory, find entry points/refs, collect scoped facts, existence checks, rule-based mechanical checks, summarize known command output, smoke tests, simple path/link/status/format checks | Claude Haiku | Agent `model: "haiku"` |
| Ordinary data analysis, hypothesis checks, complex code analysis, call/state/data-flow analysis, bug cause investigation, compare options already supplied, test-coverage thinking, multi-file multi-evidence read-only analysis | Claude Sonnet | Agent `model: "sonnet"` |
| Data cleaning, deterministic stats, chart generation, transforms, batch jobs, standalone utility scripts, analysis helper scripts, clear small bug fixes, mechanical implementation after a locked design, objectively checkable execution | Codex Luna | `gpt-5.6-luna` + max effort |
| Core data analysis, complex reasoning, complex evidence synthesis, critical stats/method review, candidate explanations for important conclusions, deep analysis of user-listed options | Codex Sol | `gpt-5.6-sol` + high effort |
| Frontend/backend/experiment code, bounded feature work, tests, in-project data-processing code, designed local refactors, cross-file implementation under a fixed interface, prototypes, independent implementation proposals, **existing project doc maintenance** | Grok Build | Current official Grok Build default coding model; confirm before call; no silent downgrade |
| Broad external research, heavy web search, time-sensitive fact checks, community-review surveys, multi-source cross-checks | Grok Build | Same model; web search enabled; use relevant connected MCPs; default read-only |
| Important implementation acceptance | Main agent | Never delegate final sign-off |
| Overall direction and key decisions | User / main agent with user | Workers may only compare supplied options |

### Route notes

- Haiku is the default internal worker. Sonnet is not default; use it only when the task clearly exceeds mechanical work.
- Project feature implementation prefers Grok over Luna. Luna is for data/script/batch/small deterministic work.
- Sol only produces candidate conclusions. It does not decide direction, implement ordinary code, clean data, inventory files, scan a repo aimlessly, or accept important implementations. Sol tasks are read-only by default.
- Terra has no fixed route. Use it only after user choice on a routing conflict.
- When using Grok, rewrite the critical rules into that prompt. Do not rely only on earlier `CLAUDE.md` loads.
- Heavy external research is a Grok Build route, not Sol, Sonnet, or Haiku. Prefer official or primary sources and cross-check with independent sources. Research tasks are read-only by default and must not edit project files.

### Documentation maintenance route

If the working tree already has docs that must track implementation, config, or behavior changes (`README.md`, `docs/`, guides, config/architecture/API/dev docs, experiment status notes, changelogs, migration notes):

1. Finish and accept the implementation first.
2. Decide whether those docs are affected.
3. If yes, open a separate atomic Grok Build doc task with confirmed facts, paths, forbidden changes, and checks.
4. Grok only updates docs.
5. Main agent checks docs against real commands, paths, configs, and behavior.
6. Only then close the overall work.

Do not leave doc updates for “later.” Do not ask Grok to invent docs from an open-ended “look at the code.” Do not create pointless new docs when nothing existing is affected. Code comments and docstrings may ship with the implementation task. The “tiny task on main agent” exception never absorbs this documentation route.

### External research route

Route broad external research to Grok Build when the work needs wide web search, time-sensitive checks, community-review collection, or multi-source cross-validation.

1. Keep the task atomic and default read-only: no project file edits unless the user explicitly asked for a separate write task.
2. Require Grok to use its own web search and any relevant connected MCPs that are actually available.
3. Prefer official or primary sources first; cross-check with independent sources.
4. Do not assume every MCP is present. If a needed MCP or web search is unavailable, the worker must report that gap instead of inventing coverage.
5. The worker report must list query scope, main sources, supporting evidence, conflicting information, unconfirmed items, and verification date.
6. Facts that affect the final user-facing conclusion still need independent main-agent recheck.

## Atomic Delegation

An atomic task has one clear goal, one coherent change/analysis boundary, and one acceptance set that can be checked once. It is not “one file only.” Implementation plus the tests required for that same goal may travel together. Independent stages must not.

1. One goal per delegation.
2. Do not hand A→B→C independent stages to one worker.
3. Do not let multiple workers mutate the same deliverable at once.
4. Doc maintenance is usually a separate Grok task after implementation acceptance.
5. Sequence, trade-offs, and cross-task coordination stay with the main agent.
6. Workers stop and report blockers instead of guessing missing direction.

## Delegation Prompt

No rigid schema. Include the semantics below when they matter:

```text
Goal:
[one goal only]

Scope:
Read first:
- [...]

May modify:
- [...]

Must not modify:
- [...]

Non-goals:
- [...]

Already decided:
- [...]

Required steps:
- [...]

Expected artifacts:
- [...]

Verification:
- [...]

Prohibitions:
- Do not expand scope.
- Do not call other agents or subagents.
- Do not start the next stage.
- Do not reopen decided direction.
- Do not commit, push, or delete branches unless explicitly authorized.
- If information is missing, stop and report.

Return a worker report as required by the agent-delegation skill.
```

## Worker Reports

Reports must let the main agent locate evidence without re-exploring the whole project. They are not final evidence and never replace main-agent acceptance.

| Kind | Required content |
| --- | --- |
| Code or doc changes | Status (done / partial / blocked); files changed; main change per file; commands run; key results; test/lint/build/link/smoke; assumptions; open issues; risks |
| Analysis | Sources; steps; findings; evidence; facts vs interpretations/candidates; limits; missing info; main-agent recheck points |
| External research | Query scope; tools/MCPs used and gaps; main sources with URLs/ids; supporting evidence; conflicts; unconfirmed items; verification date; facts vs interpretations; recheck points |
| Verification | Targets; methods; commands/checks; passes; failures; unknowns; whether main-agent follow-up is needed |

## Main-Agent Acceptance

Do not accept work because a worker said “done.” According to risk: inspect the diff, scope, key logic, verification commands, real test coverage, analysis inputs, and fact vs interpretation.

**Completion is defined by real artifacts, not worker claims.** Natural-language “done”, a normal exit code, or streaming text that says files are being modified does **not** prove completion. For write tasks check: actual diff, target file contents, required verification, and (for headless workers) tool/permission events. No relevant diff when edits were expected → **failed or blocked**; see [worker execution](references/worker-execution.md) for inspect/retry/fallback.

For important implementations that affect core features, data logic, critical config, security, databases, release behavior, experimental results, user conclusions, plan state, or public interfaces, the main agent must personally:

1. Read the relevant diff or artifact.
2. Check core logic.
3. Check execution evidence.
4. Run or directly review the critical verification.
5. Accept, request fixes, or reject.

Never outsource that final acceptance to Sol, Sonnet, Haiku, Grok, or another review agent. Sol outputs are candidates only; recheck key evidence before adopting or quoting them.

## How to Call Workers

### Claude subagents

Use the Claude Code `Agent` tool with explicit `model`:

- Haiku: `model: "haiku"`
- Sonnet: `model: "sonnet"`

Put the atomic prompt and report requirements in the agent prompt. Keep the worker from spawning further agents.

### Codex and Grok

Before any Codex or Grok call, retry, worktree, parallel writable worker, or out-of-repo write, read [worker execution](references/worker-execution.md). Fixed configs stay:

| Local policy | Worker | Config |
| --- | --- | --- |
| Luna max | Codex | `gpt-5.6-luna` + `xhigh`; `--write` only if files must change |
| Sol high | Codex | `gpt-5.6-sol` + `high`; no `--write` by default (read-only) |
| Grok Build | Grok | Current official default coding model; `--no-subagents`; no silent model downgrade |

Do not use Ultra or nested-parallel modes. Prefer official plugin/CLI surfaces only.

## Static Routing Checks

| Request | Route |
| --- | --- |
| Quickly inventory backend entry points | Haiku |
| Analyze ordinary experiment data and check a hypothesis | Sonnet |
| Clean a CSV, compute stats, make charts | Luna max with `--write` only if files must change |
| Implement a Vue page and its API calls | Grok Build |
| Deep-check whether key results support a candidate explanation | Sol high without `--write` |
| Survey current community reviews and cross-check official docs for a tool | Grok Build research route |
| Accept Grok’s core backend feature | Main agent only |
| Sync README after an accepted change | Separate Grok doc task; not a main-agent “tiny task” shortcut |
| Core analysis plus code implementation | Split: Sol analysis (read-only), then Grok implementation |
| Actively use subagents / parallel agents on a multi-file task | Load this skill; dispatch fixed routes instead of bulk self-execution |
| Unclassified new task | Read `references/model-routing.md`, ask user |

Execution, permission, serial/parallel, and failure-recovery cases: [worker execution](references/worker-execution.md#static-execution-checks).

## Completion Check

1. Task classified into a fixed route, or user chose after a documented conflict; ordinary commands and “use subagents” counted without waiting for “delegate”.
2. Prompt is atomic; non-goals and prohibitions are explicit.
3. Nested delegation blocked; Grok used `--no-subagents` when called.
4. Worker returned a usable evidence-oriented report.
5. Main agent accepted using real artifacts (diff, files, checks), not claims or exit code alone.
6. Affected existing docs handled as a separate accepted Grok task, or judged unaffected; not absorbed by the tiny-task exception.
7. External research stayed on the Grok research route (read-only by default) with sources, conflicts, gaps, and verification date when required.
8. Sol omitted `--write`; Luna used `--write` only when edits were required.
9. Codex/Grok calls, retries, worktrees, parallel writes, and out-of-repo paths followed [worker execution](references/worker-execution.md).
10. No custom orchestration framework was invented for this run.
