---
name: agent-toolkit
description: >
  Use Claude Code native/named agents and optional Grok Build CLI with user consent.
  Trigger when the user names a worker, asks to delegate or use subagents, wants Grok,
  or non-trivial multi-file work might benefit from delegation. Skip for trivial edits
  and pure Q&A with no repo work.
argument-hint: "[agent name | grok | task summary]"
user-invocable: true
disable-model-invocation: false
---

# Agent Toolkit

Claude Code orchestrates; optional workers are native subagents, named agents in
`~/.claude/agents/` or `.claude/agents/`, and Grok (`grok`) when the user asks.
Small tasks stay on the main agent. Grok variants and source notes:
[references/grok-cli.md](references/grok-cli.md).

## When to use

- User names a worker, or asks to delegate / use subagents / call Grok
- Non-trivial multi-file code, docs, research, or analysis where delegation might help
- User asks to install templates from `templates/agents/`

**Not for:** trivial one-step edits; pure Q&A with no repo work; inventing model
rankings or multi-model fallback; Codex / Claude CLI reference workflows.

## Named worker

**Use when:** User names an Agent or Grok.

**Do:**

1. Use that worker. Do not re-ask which worker.
2. Claude named agents — list and match `~/.claude/agents/` and `.claude/agents/`.
   Respect frontmatter (`model`, effort, tools, MCP, permissions, isolation); do not
   override model/config unless the user asked.
3. Grok — `grok models`, then the default write call below (variants in the reference).
4. One clear task block (implementation + tightly related tests/verification may travel
   together). Self-contained prompt: goal, scope, non-goals, paths, verification, prohibitions.

**Important:**

- Claude agents ≠ Grok `.grok/agents/`. Do not mix.
- Prefer existing named agents; ad-hoc native subagent only if user wants generic and none fit.
- Workers must not nest agents, expand scope, or start the next stage alone.

### Default Grok write call

```bash
grok models   # auth + default model

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

Use the model from `grok models` if not `grok-4.5`. Prefer `--prompt-file` for long
prompts. Do not default to `--always-approve`. Read the reference for a single allowed
shell check, read-only research, resume, worktree, or permission fixes.

## Unnamed non-trivial work

**Use when:** No worker named, task clearly non-trivial, delegation looks useful.

**Do:** Do not start any worker. Briefly offer main agent vs currently available named
agent / Grok. Wait for the choice.

**Important:** Small/simple work → do it yourself. After the user chooses, follow
**Named worker** or stay on the main agent.

## Accept write results

**Use when:** A worker finished a write or claimed "done".

**Do:** Check real `git status` / `git diff` and target files; confirm allowed paths;
run or review required verification (especially if Bash was denied).

**Important:** "Done", exit code alone, or streaming claims without a diff are not
completion. One feature block may include its tests — still verify both.

## Worker failure

**Use when:** Timeout, cancel, no tools, no expected diff, or partial edits.

**Do:** Inspect process, logs, permissions, partial diffs → **one resume** of the same
worker if session/artifacts exist → still blocked, report and let the user choose
continue / other worker / main-agent takeover.

**Important:** No auto model-swap. No second writable worker on the same paths while the
first still runs. Grok permission cancels → fix `--allow` / `--deny` first (reference).

## Worktree cleanup

**Use when:** A worktree or temp branch was used.

**Do (same round):** Accept → integrate → confirm → remove worktree/branch → no residue.
Reject → discard → remove worktree/branch → no residue.

**Important:** Main agent owns cleanup. Prefer the current tree when safe.

## Agent templates

**Use when:** User explicitly asks to install/update from this skill.

```text
templates/agents/    # e.g. deepseek-flash.md
```

Copy only requested `.md` files to `~/.claude/agents/` and/or `<project>/.claude/agents/`.
Do not invent templates, install unprompted, or overwrite custom agents without confirmation.
If the requested template is missing, say so and use agents the user already has.

## Don't

- Auto-start workers without a named worker or an explicit user choice
- Fixed model routing tables or automatic multi-model fallback
- Override named-agent frontmatter without user-driven need
- Accept writes without real diffs and needed verification
- Leave worktrees or temp branches after the round

## Good / bad

**User:** "帮我实现这个功能。"

```text
# Bad  — start Grok and several subagents immediately
# Good — ask once: main agent vs available named agent / Grok → wait → act
```

**User:** "用 Grok 完成这个功能，包括相关测试。"

```text
# Bad  — four Grok calls: implement → tests → run tests → notes
# Good — one Grok block (implement + related tests + verification)
#        → main agent: git diff + run/review tests
```

## Done when

- [ ] Consent path followed (named / asked / or main agent for small work)
- [ ] Writes checked via real artifacts, not claims
- [ ] Worktrees/temp branches cleaned if used
