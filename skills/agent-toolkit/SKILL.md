---
name: agent-toolkit
description: >
  Use Claude Code native or named agents and optional Grok Build CLI when the user
  explicitly invokes this skill, names a worker, asks for delegation or subagents,
  requests Grok, or asks to install an included agent template.
argument-hint: "[agent name | grok | task summary]"
user-invocable: true
disable-model-invocation: true
---

# Agent Toolkit

When invoked, delegate one bounded unit of work while the main agent retains scope,
acceptance, and cleanup responsibility.

## Select and brief the worker

- For a named Claude agent, match it in `~/.claude/agents/` or
  `.claude/agents/` and respect its frontmatter.
- For Grok, run `grok models`, use the reported default model, and consult
  [references/grok-cli.md](references/grok-cli.md) for current flags and variants.
- For a generic delegation request, prefer an existing suitable agent; otherwise
  use one native subagent.

Send one self-contained task block containing the goal, allowed scope and paths,
relevant context, expected artifacts, and verification. Closely related
implementation and tests belong in the same block. Workers stay within that block,
leave commits and pushes to the main agent, and do not spawn further workers.

## Default Grok write call

```bash
grok models

grok \
  --cwd "$PWD" \
  --model grok-4.5 \
  --no-subagents \
  --no-memory \
  --disable-web-search \
  --permission-mode auto \
  --allow Read --allow Grep --allow Edit \
  --deny Agent --deny Bash \
  --rules "Edit only the listed paths. Leave commits and pushes to the main agent. Stop and report blockers." \
  --output-format streaming-json \
  -p "<self-contained task prompt>"
```

Replace the model with the current default reported by `grok models`. Use
`--prompt-file` for a long prompt. The reference covers narrow shell permissions,
read-only research, resume, worktrees, and permission failures.

## Accept the result

Inspect the actual target files, `git status`, and `git diff`, then run or review the
appropriate checks. Worker prose and process exit status are supporting evidence,
not substitutes for the resulting artifacts.

If a worker times out or produces partial work, inspect its process, permissions,
logs, and diff. Resume the same worker once when a session or usable partial result
exists. If it remains blocked, report the evidence and let the user choose between
retrying, another worker, or main-agent completion. Keep a second writable worker
off the same paths while the first is active.

When isolation created a worktree or temporary branch, the main agent integrates or
discards the result and removes that temporary state in the same round.

## Agent templates

When requested, copy the selected file from `templates/agents/` into the user's or
project's `.claude/agents/` directory. Preserve existing customized agents unless
the user approves replacement.
