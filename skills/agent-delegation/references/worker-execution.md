# Worker Execution Reference

Stable routing and acceptance rules live in [`../SKILL.md`](../SKILL.md). This file holds **conditional execution detail**: worktrees, serial/parallel writable workers, out-of-repo paths, Codex/Grok command forms, Grok permissions and output formats, failure recovery, runtime scratch, and execution static checks.

**Read this file before** calling Codex or Grok, retrying a worker, using a worktree, running parallel writable workers, or modifying paths outside the current repository.

Do not invent ad-hoc model rankings here. Fixed routes stay in `SKILL.md`.

## Worktrees and Branches

Default: no worktree.

Work in the current tree when the task is read-only, small, non-conflicting, Git state is clear, and recovery is easy.

Prefer a worktree when agents would edit in parallel, compare two implementations, change a large surface, run a throwaway experiment, or need clean discard.

After any worktree or temp branch, finish cleanup in the same round:

- Accept: main-agent acceptance → merge/rebase/cherry-pick to the target branch → confirm target has the change → remove worktree → delete temp branch → confirm no residue.
- Reject: confirm discard → remove worktree → delete temp branch → confirm no residue.

Do not accept without integrating, keep temp branches after merge, leave worktrees around, pile up unexplained agent branches, or open new branches before old ones are closed. Merge-or-discard-and-clean is part of the delegated work.

## External Writable Workers: Serial by Default

Under Claude Code Auto mode, **writable external workers** (Grok Build write tasks, and similarly scoped Codex Luna `--write` runs) **default to serial execution**.

1. Do not start multiple auto-writing Grok agents at once from one Bash command via `&`, background loops, or fire-and-forget batches.
2. Run one writable external worker to completion (or hard stop), main-agent-check artifacts, then start the next.
3. Grok’s own subagent fan-out remains forbidden (`--no-subagents` on every call).
4. Parallel writable external workers are allowed **only** when all of the following hold:
   - the user explicitly authorized parallel writable workers for this work;
   - write scopes do not overlap;
   - each worker uses an independent worktree;
   - each worker uses narrow permissions (see Grok section);
   - the main agent can accept, merge/discard, and clean each worker one by one.
5. Read-only workers may run in parallel when scopes and tools stay non-mutating and do not thrash the same checkout.

## Paths Outside the Repository

External workers may modify files **only inside the current repository or an authorized worktree of that repository** by default.

- User-level config, Claude memory, credentials, agent config, home-directory files, and other repos are **out of scope** for ordinary project code or doc tasks.
- Any write outside the repo/worktree must be a **separate atomic task**, with explicit user authorization before the worker starts.
- Do not mix out-of-repo writes into project doc/code tasks.
- Do not batch or parallelize out-of-repo write tasks.

## Codex

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

## Grok Build

Confirm the live default coding model first (`grok models`; local default expected `grok-4.5`). Prefer headless single-shot with hard no-subagents.

### Headless permissions (Claude Code Auto mode)

When the main agent launches Grok Build from Claude Code Auto mode:

1. **Do not use `--always-approve` by default.** It auto-approves all tool executions and is too wide for unattended writes.
2. Prefer **`--permission-mode auto`** plus explicit allow/deny (or tools allow-list) limited to the atomic task.
3. For pure documentation or file-edit tasks that do **not** need shell commands: allow **`Read`**, **`Grep`**, **`Edit`**; deny **`Agent`** and **`Bash`**. Prefer the main agent to run verification after the worker exits.
4. If the worker **must** run a named command, do **not** blanket `--deny Bash` at the same time as allowing a Bash form — that is contradictory. Use a narrow config that allows only the explicit command(s) required by the prompt and denies other Bash (and still denies `Agent`, `git commit`, `git push` unless authorized).
5. Keep writes inside the repo/worktree. Out-of-repo paths need a separate authorized task.

### Headless output format

- **Write / modify tasks:** prefer `--output-format streaming-json` or `json` so the main agent can inspect tool calls, permission denials, and final status.
- **`plain`:** fine for simple read-only prompts; **not** the default for automatic write tasks.
- After the process exits, still verify real diffs and target files. JSON success text without a diff is not completion.

### Call examples

Pure documentation or file-edit task (no shell; main agent runs checks afterward):

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --disable-web-search \
  --permission-mode auto \
  --allow Read --allow Grep --allow Edit \
  --deny Agent --deny Bash \
  --rules "<task-specific worker rules: only edit listed paths; do not run shell; do not commit/push; stop and report blockers>" \
  --output-format streaming-json \
  -p "<atomic prompt>"
```

Worker must run one named check command (no blanket Bash deny; allow only that command form):

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --disable-web-search \
  --permission-mode auto \
  --allow Read --allow Grep --allow Edit \
  --allow "Bash(pwsh -NoProfile -File scripts/validate-skills.ps1)" \
  --deny Agent \
  --deny "Bash(git commit:*)" --deny "Bash(git push:*)" \
  --rules "<only listed paths; only the named check command; no commit/push>" \
  --output-format streaming-json \
  -p "<atomic prompt>"
```

Heavy external research (read-only by default):

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --permission-mode auto \
  --deny Agent --deny Edit --deny Bash \
  --rules "<research rules: use web search and relevant MCPs; prefer primary sources; cross-check; do not edit project files>" \
  --output-format json \
  -p "<atomic research prompt>"
```

Do not silently widen global permissions. Put critical project rules in `--rules` and the prompt for every Grok call. Do not assume every MCP is available; unavailable tools must be reported. Writable Grok runs stay serial under Auto mode unless the parallel conditions above are all met.

## Worker Failure Recovery

Worker timeout, abnormal exit, or output that only states intent with **no** real artifacts is an **execution failure**. The main agent must **not** take over a fixed outsourced task just because the worker failed.

### Before any retry

1. Check whether the original process or background session is still running.
2. Read worker output and permission errors.
3. Inspect git diff and target file contents.
4. Decide whether partial edits already exist.

Only one active writable worker may exist for the same atomic task. Do **not** start another write worker until the previous process is confirmed finished or hard-stopped.

### Recovery chain (upper bound, not a mandatory triple retry)

1. Same worker may be retried after inspection.
2. At most **three** total **model execution attempts** on the original worker for one atomic task.
3. Three is a **ceiling**, not a requirement to always burn three attempts. If the failure is a confirmed **deterministic configuration error** (wrong flags, contradictory allow/deny, missing auth) that the same worker will hit again unchanged, fix the config and, when the fixed Grok→Luna path applies, you may enter the allowed fallback **early** instead of repeating the broken form.
4. Prefer **resume** when a recoverable session or partial artifacts exist. Use a **fresh** session when there are no usable artifacts.

Retries may adjust timeout, `max-turns`, `json` / `streaming-json` output, narrow permission config, and prompt compression/disambiguation. Retries must **not** expand goals, change scope, add independent tasks, or relax safety boundaries.

### Permission / classifier denials

- Claude Code safety-classifier or permission denials that block the worker **before it actually starts** (no model run, no tool loop) **do not count** as one of the three model execution attempts.
- Do not blindly retry the same blocked command. Fix the permission or invocation form first (for example remove `--always-approve`, apply non-contradictory narrow allow/deny), then retry.
- Do not bypass denials by widening global permissions.

### Fixed fallback after exhausted Grok attempts

If Grok Build still fails after up to three model execution attempts (or earlier when the same deterministic config failure is confirmed and retries would be pointless) on these **bounded, objectively checkable** tasks, fall back to **Codex Luna**:

- frontend/backend/experiment implementation
- test writing
- in-project data-processing code
- existing documentation maintenance
- other clear execution work with fixed acceptance

Fallback config (unchanged Luna max route):

- model: `gpt-5.6-luna`
- effort: `xhigh` (local Luna max)
- `--write` only when files must change

The Luna task must keep the **same** atomic goal, scope, facts, prohibitions, and verification. Luna must not redesign the task.

### No automatic cross-model fallback

- Grok **heavy external research** does **not** auto-fallback to Luna (web search / MCP capabilities differ). After consecutive failures, report causes and ask the user.
- Codex **Sol high** and other core-analysis / important candidate-conclusion tasks do **not** auto-fallback across models. After consecutive failures, ask the user.

### When the main agent may take over

The main agent may personally do work that this skill fixed to an external worker only if:

1. the user explicitly authorizes takeover; or
2. the task is reclassified as a tiny one-step job that needs no isolation, **and** it is not the mandatory Grok existing-doc-maintenance route.

Worker timeout alone is **not** authorization for main-agent takeover.

### Acceptance still applies

Whether the original worker, a retry, or Luna fallback finished the run: the worker still returns the required report; the main agent still checks real diffs, artifacts, and verification; important implementation acceptance is never outsourced.

## Runtime Scratch

Temporary prompts, worker stdout, job status, temp diffs, and intermediate analysis files may live under:

```text
.agent-runtime/
```

Ensure project `.gitignore` includes `.agent-runtime/`. Do not turn it into a database, formal task system, or project docs center. Keep using native Codex/Grok session logs.

## Static Execution Checks

| Situation | Action |
| --- | --- |
| Grok claims done but no relevant diff | Not complete; inspect permissions, tool events; treat as failed/blocked |
| Claude Auto mode: batch-start many writable Grok agents with `&` / background loops | Forbidden; run writable external workers serially |
| Two non-overlapping write tasks want parallel Grok | Only if user authorized, independent worktrees, narrow permissions, and main-agent per-worker accept/clean |
| Edit project-external Claude memory / user config | Separate task; ask explicit user authorization first; never mix into project doc/code work |
| Pure Grok documentation edit | Allow Read/Grep/Edit; deny Agent and Bash; no `--always-approve`; `streaming-json` or `json`; main agent checks real diff and may run verification |
| Grok must run one named check command | Narrow allow for that command only; do not also blanket `--deny Bash` |
| Grok doc task times out once; process dead; no useful artifacts | Inspect; retry same Grok worker if attempts remain |
| Same deterministic Grok config error confirmed | Fix config; may enter allowed Luna fallback early without burning three identical failures |
| Grok three model attempts with no artifacts on a bounded doc/code task | Fall back to Luna xhigh with the same atomic prompt; `--write` if files must change |
| Grok timed out but process still running | Do not start a second writable worker; wait, inspect, or hard-stop first |
| Claude classifier rejects Grok launch before start | Does not count as a model attempt; fix invocation/permissions; do not widen global permissions |
| Grok denied because of `--always-approve` / classifier | Fix narrow permissions; do not retry the blocked form unchanged |
| Grok heavy research fails repeatedly | Report and ask user; do not auto-hand to Luna |
| Grok failed and main agent starts rewriting the deliverable alone | Forbidden unless user authorized takeover or task is reclassified tiny (not forced doc route); follow recovery chain first |
