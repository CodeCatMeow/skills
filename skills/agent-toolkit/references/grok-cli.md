# Grok Build CLI (agent-toolkit)

Call sheet for **Grok Build** (`grok`) when the user chooses Grok. Consent and acceptance: [`../SKILL.md`](../SKILL.md).

## Sources and verification

Verified for this skill on **2026-08-07**:

| Source | What we used |
| --- | --- |
| [Grok Build overview](https://docs.x.ai/build/overview) (also [`.md`](https://docs.x.ai/build/overview.md)) | Install, auth (`grok login` / `XAI_API_KEY`), headless `-p`, default model `grok-4.5` |
| [CLI reference](https://docs.x.ai/build/cli/reference) ([`.md`](https://docs.x.ai/build/cli/reference.md)) | Subcommands, common flags (`--cwd`, resume, worktree, allow/deny, `--no-subagents`, …) |
| [Headless & scripting](https://docs.x.ai/build/cli/headless-scripting) ([`.md`](https://docs.x.ai/build/cli/headless-scripting.md)) | `-p` / `--single`, output formats, session storage `~/.grok/sessions` |
| [Permissions](https://docs.x.ai/build/features/permissions) ([`.md`](https://docs.x.ai/build/features/permissions.md)) | Ask / Auto / Always-approve; `--allow` / `--deny`; deny wins; always-approve still respects deny |
| [Worktrees](https://docs.x.ai/build/features/worktrees) ([`.md`](https://docs.x.ai/build/features/worktrees.md)) | Isolation path, `grok worktree list\|rm\|gc` |
| Local install | `grok version` → **1.0.0**; flags from `grok --help`; models from `grok models` → default **grok-4.5** |
| Community [sanjay3290/ai-skills `grok-build`](https://github.com/sanjay3290/ai-skills/tree/main/skills/grok-build) | Review-gate idea only; not its default `--always-approve`. Older-CLI flags `--check` / `--best-of-n` are absent on local 1.0.0 help |

**Precedence when sources disagree:** live `grok --help` / `grok models` on the machine you are calling > this file > community skills. Re-check after major CLI upgrades.

Known doc vs local gaps (do not invent around them):

- Headless docs describe `-s` as “create or resume”; local 1.0.0 help says `-s` is for a **new** UUID only — use `--resume` / `--continue` to resume.
- Headless docs mention `--no-auto-update`; it does **not** appear in local 1.0.0 `--help`. Prefer config `auto_update = false` under `[cli]` in `~/.grok/config.toml` if updates interfere, or ignore if the flag is absent.
- Official docs list `--yolo` as alias of `--always-approve`; prefer the long flag.

## Preflight

```bash
grok models
```

- Must list models and show a default (currently often `grok-4.5`). Use the reported default; do not hardcode forever.
- Failure / logged out: stop. User runs `grok login` (or `grok login --device-auth` when browserless) or sets `XAI_API_KEY`.
- Optional: `grok inspect` to see discovered rules/skills/MCP for the cwd.

## Headless call shape

Prefer top-level headless (not `grok agent stdio` — that is ACP for IDE/tool integration):

```bash
grok -p "<prompt>"
# or
grok --prompt-file <path>   # local 1.0.0; avoids shell quoting issues
```

| Need | Flag (official + local) |
| --- | --- |
| One-shot prompt | `-p` / `--single` |
| Prompt from file | `--prompt-file` (local help) |
| Working directory | `--cwd <path>` |
| Model | `-m` / `--model <id>` |
| Disable nested Grok subagents | `--no-subagents` |
| Disable memory | `--no-memory` |
| Disable web tools | `--disable-web-search` |
| Output for machine review | `--output-format json` or `streaming-json` (`plain` default) |
| Extra constraints | `--rules "..."` |
| Turn cap | `--max-turns <n>` |
| Permission mode | `--permission-mode <mode>` — local values: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| Narrow tools | repeatable `--allow <RULE>` / `--deny <RULE>` |
| Wide auto-approve | `--always-approve` (official; **not** this skill’s default) |

Grok does not share Claude’s chat history. Prompts must be self-contained.

## Session / resume

| Flag | Meaning |
| --- | --- |
| `-r` / `--resume [<id-or-title>]` | Resume by id/title, or most recent if omitted (local: title match is cwd-scoped) |
| `-c` / `--continue` | Most recent session for current directory |
| `-s` / `--session-id <uuid>` | **New** session UUID only (local 1.0.0); not a resume shortcut |

Sessions live under `~/.grok/sessions` (official headless docs).

With `--output-format json`, capture whatever session id field the payload exposes (community skill historically used `sessionId`) and use it for a single fix-up resume. Prefer resume over a second concurrent write on the same paths.

## Permissions

- Permissions choose which tools may run; **sandbox** is separate (filesystem/network).
- Modes: Ask (default interactive), Auto (classifier), Always-approve (`--always-approve`). Deny rules and PreToolUse hooks still apply under always-approve.
- `--allow` / `--deny`: `Bash`, `Edit`, `Read`, `Grep`, `MCPTool`, `WebFetch`, `WebSearch`, … **Deny wins over allow.**
- Explicit CLI/config allow rules auto-approve matching tools.

**Defaults for this skill:**

1. Do **not** default to `--always-approve`.
2. Prefer narrow `--allow` / `--deny` (explicit allow auto-approves).
3. Prefer `--permission-mode auto`, or `dontAsk` when every needed tool is already allowed.
4. Cancelled with no tools/diff → fix allow/deny first. Use `--always-approve` only with user consent; still deny nested agents and `git commit` / `git push` unless authorized.

### Write task (edits; main agent runs broad shell checks)

Same default as [`../SKILL.md`](../SKILL.md) — kept here for copy-paste next to variants:

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
  --rules "Only edit listed paths. Do not commit or push. Stop and report blockers." \
  --output-format streaming-json \
  -p "<self-contained task prompt>"
```

(Replace `--model` with whatever `grok models` reports as default if different.)

### Write task that must run one named check

Do not combine blanket `--deny Bash` with a needed shell command. Allow only that form:

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
  --output-format streaming-json \
  -p "<task prompt>"
```

### Read-only research

```bash
grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --permission-mode auto \
  --deny Agent --deny Edit --deny Bash \
  --rules "Research only. Prefer primary sources. Do not edit project files." \
  --output-format json \
  -p "<research prompt>"
```

Omit `--disable-web-search` when research needs the web. Official filters include `WebSearch` / `WebFetch` if you need tighter control.

## Worktree

Official:

- Isolated git checkout under `~/.grok/worktrees/<repo>/<name>`; starts from current HEAD (including uncommitted changes unless `--ref` used).
- Create: `grok -w` / `grok --worktree[=name]` (interactive session). Manage: `grok worktree list|show|rm|gc`.
- Worktrees **persist** until removed; ending a session does not auto-delete them.

Local 1.0.0:

- Headless `-p` **does not** create a worktree from `--worktree`. For headless isolation: create/manage a worktree first, then `--cwd` into it, or use interactive worktree flows.

Main agent still merges/discards and cleans up (see SKILL.md).

## After every write run

1. Exit status + json/streaming-json tool or permission events when available
2. Real `git status` / `git diff` and target file contents
3. Run verification yourself when Bash was denied to the worker
4. No relevant diff when edits were expected → failed/blocked
5. Worker “done” text is never acceptance

## Failure notes

| Symptom | Action |
| --- | --- |
| `grok models` / auth fails | Stop; user fixes login or `XAI_API_KEY` |
| Cancelled / no tools / no diff | Fix narrow allow/deny (and mode); do not jump to always-approve by default |
| Partial edits | Inspect; resume once with specific feedback |
| Timeout, process dead | Report; user decides retry, other worker, or main-agent takeover |
| Process still running | Do not start a second writable Grok on the same scope |
| Still failing after one resume | Report evidence; user chooses next step (no auto model-swap) |
