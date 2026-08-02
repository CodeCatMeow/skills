---
name: agent-delegation
description: Use when routing work among Claude Code subagents, Codex external workers, or Grok Build; choosing Haiku, Sonnet, Luna, Sol, or Grok; writing atomic worker prompts; receiving worker reports; accepting important implementations; maintaining project docs after code changes; running heavy external research or multi-source web checks; or deciding whether a task needs worktree cleanup. Do not use for ordinary single-file edits the main agent can finish alone, or for inventing new model rankings outside the fixed routes.
argument-hint: "[task type or worker]"
user-invocable: true
disable-model-invocation: false
---

# Agent Delegation

## Purpose

Keep Claude Code as the only orchestrator while routing atomic work through fixed workers:

| Worker | Role |
| --- | --- |
| Claude Haiku subagent | Cheap mechanical internal work |
| Claude Sonnet subagent | Internal analysis that needs real reasoning |
| Codex Luna (`gpt-5.6-luna`, max effort) | Cheap, clear, objectively checkable external execution |
| Codex Sol (`gpt-5.6-sol`, high effort) | Rare high-value external analysis and candidate conclusions |
| Grok Build | Primary project implementation, existing-doc maintenance, and heavy external research |
| Main agent | Route choice with user, final conclusions, important acceptance |

This Skill is a fixed routing and acceptance contract. It is not an agent platform, job queue, or nested multi-agent framework.

For prices, benchmarks, and model notes that go stale, read [model routing](references/model-routing.md). Do not use that reference to invent ad-hoc routes.

## Non-Negotiable Rules

1. Only the main Claude Code agent may set the work plan with the user, start workers, order tasks, review results, accept or reject important implementations, form the final user-facing conclusion, and decide the next stage.
2. Workers must not call subagents, start Claude/Codex/Grok/other agents, nest delegation, expand scope, choose product or research direction, accept important conclusions, or continue to the next stage on their own.
3. Use fixed routes below. Do not guess which model is smarter, which harness is better, or whether an external agent “might help.” Classify the task, then call the assigned worker.
4. If no route fits, or two conflicting routes both fit: read `references/model-routing.md`, propose one recommendation and at most one alternative, explain the difference, ask the user with `AskUserQuestion`, and do not start an expensive worker before the user chooses.
5. Tiny work that needs no isolation may stay on the main agent. This exception does **not** override the fixed Grok Build route for existing project-documentation maintenance.
6. Important implementation acceptance is never outsourced. Haiku, Sonnet, Luna, Sol, and Grok may collect evidence or run mechanical checks; only the main agent signs off.
7. Existing project documentation that must stay in sync with accepted implementation changes is a separate Grok Build task after the implementation is accepted.
8. Prefer official plugin/CLI surfaces. Do not add custom wrapper frameworks for sessions, logs, cancel, model, or effort selection.

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

Rules:

1. One goal per delegation.
2. Do not hand A→B→C independent stages to one worker.
3. Do not let multiple workers mutate the same deliverable at once.
4. Doc maintenance is usually a separate Grok task after implementation acceptance.
5. Sequence, trade-offs, and cross-task coordination stay with the main agent.
6. Workers stop and report blockers instead of guessing missing direction.

## Delegation Prompt

No rigid schema. Include the semantics below when they matter. Natural-language template:

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

### Code or doc changes

Status (done / partial / blocked); files changed; main change per file; commands run; key command results; test/lint/build/link/smoke results; assumptions; open issues; risks and uncovered cases.

### Analysis

Sources used; steps; findings; supporting evidence; facts vs interpretations/candidates; limits; missing info; points the main agent should re-check.

### External research

Query scope; tools or MCPs used and any unavailable ones; main sources with URLs or stable identifiers; supporting evidence; conflicting information; unconfirmed items; verification date; facts vs interpretations; points the main agent must recheck before user-facing conclusions.

### Verification

Targets; methods; commands/checks; passes; failures; unknowns; whether main-agent follow-up is needed.

## Main-Agent Acceptance

Do not accept work because a worker said “done.” According to risk: inspect the diff, scope, key logic, verification commands, real test coverage, analysis inputs, and fact vs interpretation.

For important implementations that affect core features, data logic, critical config, security, databases, release behavior, experimental results, user conclusions, plan state, or public interfaces, the main agent must personally:

1. Read the relevant diff or artifact.
2. Check core logic.
3. Check execution evidence.
4. Run or directly review the critical verification.
5. Accept, request fixes, or reject.

Never outsource that final acceptance to Sol, Sonnet, Haiku, Grok, or another review agent.

Sol outputs are candidates only. Recheck key evidence before adopting or quoting them to the user.

## Worktrees and Branches

Default: no worktree.

Work in the current tree when the task is read-only, small, non-conflicting, Git state is clear, and recovery is easy.

Prefer a worktree when agents would edit in parallel, compare two implementations, change a large surface, run a throwaway experiment, or need clean discard.

After any worktree or temp branch, finish cleanup in the same round:

- Accept: main-agent acceptance → merge/rebase/cherry-pick to the target branch → confirm target has the change → remove worktree → delete temp branch → confirm no residue.
- Reject: confirm discard → remove worktree → delete temp branch → confirm no residue.

Do not accept without integrating, keep temp branches after merge, leave worktrees around, pile up unexplained agent branches, or open new branches before old ones are closed. Merge-or-discard-and-clean is part of the delegated work.

## How to Call Workers

### Claude subagents

Use the Claude Code `Agent` tool with explicit `model`:

- Haiku: `model: "haiku"`
- Sonnet: `model: "sonnet"`

Put the atomic prompt and report requirements in the agent prompt. Keep the worker from spawning further agents.

### Codex

Prefer the installed OpenAI `codex-plugin-cc` companion. Current plugin help shape:

```text
task [--background] [--write] [--resume-last|--resume|--fresh] [--model <model|spark>] [--effort <none|minimal|low|medium|high|xhigh>] [prompt]
```

Fixed configs for this Skill:

| Local policy | Model | Effort | `--write` |
| --- | --- | --- | --- |
| Luna max | `gpt-5.6-luna` | `xhigh` (local “max”) | Only when the task truly needs file changes |
| Sol high | `gpt-5.6-sol` | `high` | Never by default; Sol is read-only |

Sol high (read-only):

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task --model gpt-5.6-sol --effort high "<atomic prompt>"
```

Luna max when edits are required:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task --write --model gpt-5.6-luna --effort xhigh "<atomic prompt>"
```

Luna max when the task is read-only execution or analysis of existing artifacts:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task --model gpt-5.6-luna --effort xhigh "<atomic prompt>"
```

Always pass both `--model` and `--effort`. Do not rely on Codex defaults. Do not use Ultra or any mode that spawns nested parallel subagents. Background/status/result/cancel stay on the plugin helpers; do not reimplement them.

Fallback only if the plugin cannot be called reliably. Prefer `codex exec` with `-m` and `-c model_reasoning_effort="..."`. For Sol, keep sandbox read-only; for Luna writes, only widen write access when the atomic task requires it:

```bash
codex exec -m gpt-5.6-sol -c model_reasoning_effort=\"high\" -s read-only "<atomic prompt>"
codex exec -m gpt-5.6-luna -c model_reasoning_effort=\"xhigh\" -s workspace-write "<atomic prompt>"
```

### Grok Build

Confirm the live default coding model first (`grok models`; local default expected `grok-4.5`). Prefer headless single-shot with hard no-subagents.

Ordinary code or documentation tasks that do not need the network:

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --disable-web-search \
  --rules "<task-specific worker rules>" \
  --output-format json \
  -p "<atomic prompt>"
```

Heavy external research tasks: omit `--disable-web-search`, require web search plus any relevant connected MCPs, and keep the task read-only unless the user explicitly asked for writes:

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --rules "<research rules: use web search and relevant MCPs; prefer primary sources; cross-check; do not edit project files>" \
  --output-format json \
  -p "<atomic research prompt>"
```

Do not default to unconstrained `--always-approve`. If headless work needs permissions, use an existing safe permission setup or state the prerequisite; do not silently widen global permissions. Put critical project rules in `--rules` and the prompt for every Grok call. Do not assume every MCP is available; unavailable tools must be reported.

## Runtime Scratch

Temporary prompts, worker stdout, job status, temp diffs, and intermediate analysis files may live under:

```text
.agent-runtime/
```

Ensure project `.gitignore` includes `.agent-runtime/`. Do not turn it into a database, formal task system, or project docs center. Keep using native Codex/Grok session logs.

## Static Routing Checks

| Request | Route |
| --- | --- |
| Quickly inventory backend entry points | Haiku |
| Analyze ordinary experiment data and check a hypothesis | Sonnet |
| Clean a CSV, compute stats, make charts | Luna max with `--write` only if files must change |
| Implement a Vue page and its API calls | Grok Build (`--disable-web-search` if offline is fine) |
| Deep-check whether key results support a candidate explanation | Sol high without `--write` |
| Survey current community reviews and cross-check official docs for a tool | Grok Build research route with web search and relevant MCPs |
| Accept Grok’s core backend feature | Main agent only |
| Sync README after an accepted change | Separate Grok doc task; not a main-agent “tiny task” shortcut |
| Core analysis plus code implementation | Split: Sol analysis (read-only), then Grok implementation |
| Unclassified new task | Read reference, ask user |

## Completion Check

1. Task classified into a fixed route, or user chose after a documented conflict.
2. Prompt is atomic; non-goals and prohibitions are explicit.
3. Nested delegation is blocked in text and, for Grok, with `--no-subagents`.
4. Worker returned a usable evidence-oriented report.
5. Important acceptance was done by the main agent.
6. Affected existing docs were handled as a separate accepted Grok task, or explicitly judged unaffected; not absorbed by the tiny-task exception.
7. External research used Grok with web search/relevant MCPs when required, stayed read-only by default, and listed sources, conflicts, gaps, and verification date.
8. Sol omitted `--write`; Luna used `--write` only when edits were required.
9. Worktrees/temp branches were integrated or discarded and cleaned.
10. No custom orchestration framework was invented for this run.
