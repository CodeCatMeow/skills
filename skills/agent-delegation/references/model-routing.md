# Model Routing Reference

Verification date: **2026-08-02**.

This file stores routing evidence that ages: official model roles, prices/credits, effort options, independent benchmarks, community notes, and the user's local policy. Stable delegation rules live in [`../SKILL.md`](../SKILL.md).

The main agent must not leave the fixed routes in `SKILL.md` because a benchmark looks attractive. When a task is uncovered or hits conflicting routes, read this file, recommend at most two options, and ask the user.

## Reliability levels

| Level | Meaning |
| --- | --- |
| Official fact | Vendor docs, pricing pages, model pages, CLI help |
| Independent evaluation | Artificial Analysis and similar reproducible indices |
| Community experience | Reddit, forum, product-community anecdotes |
| Local experience | User-observed behavior in this environment |
| Local policy | Explicit user route even when it differs from vendor defaults |

Official API prices are not the same as ChatGPT/Codex subscription credits, third-party gateways, or discounted enterprise contracts.

## Official model positioning

### Claude Code internal models

- Claude Code supports family aliases such as `haiku` and `sonnet` on subagents. The alias resolves to the environment's allowed current model in that family. Source type: official Claude Code subagent docs (verified 2026-08-02).
- Anthropic pricing page lists **Claude Haiku 4.5** at **$1 / MTok input**, **$5 / MTok output**. Source: [Claude Platform pricing](https://platform.claude.com/docs/en/about-claude/pricing) (official, 2026-08-02).
- **Claude Sonnet 5** introductory API price through **2026-08-31**: **$2 / MTok input**, **$10 / MTok output**. From **2026-09-01**: **$3 / $15**. Source: same pricing page (official, 2026-08-02).
- Official guidance favors cheaper models for simple agent work and stronger models for multi-step coding/tool use. Source type: official.

Local policy for Haiku: code reading, exploration, inventory, mechanical checks, smoke tests, simple fact collection.

Local policy for Sonnet: ordinary analysis, hypothesis checks, complex code/call-flow analysis, multi-evidence read-only investigation. Sonnet is not the default subagent.

### GPT-5.6 Codex models

OpenAI positions the three models as:

- **Sol**: complex, open-ended, high-value work that needs analysis and judgment
- **Terra**: everyday general work
- **Luna**: clear, concrete, repeatable, high-throughput work

OpenAI recommends the lowest reasoning effort that still meets the task. Higher effort gives a single task more reasoning time. Ultra-style modes that fan out nested subagents are incompatible with this Skill's no-nesting rule and must not be used.

Model IDs used by this Skill:

- `gpt-5.6-sol`
- `gpt-5.6-terra` (no fixed route)
- `gpt-5.6-luna`

Sources: OpenAI model pages and GPT-5.6 materials (official, 2026-08-02).

### Grok 4.5 and Grok Build

xAI positions Grok 4.5 for coding, agent work, knowledge work, and science/engineering. Grok Build is the native coding-agent harness with headless mode, structured output, model/effort selection, worktrees, permissions, `--rules`, and `--no-subagents`.

Local environment check on 2026-08-02:

- `grok models` reports default **`grok-4.5`**
- CLI version: `grok 0.2.118`
- `grok inspect` discovers Claude Code skills, agents, MCP, hooks, and the installed Codex plugin

## Current official prices or credits

### Anthropic API (official, 2026-08-02)

| Model | Input / MTok | Output / MTok | Notes |
| --- | ---: | ---: | --- |
| Claude Haiku 4.5 | $1 | $5 | Current Haiku line |
| Claude Sonnet 5 | $2 | $10 | Intro price through 2026-08-31 |
| Claude Sonnet 5 | $3 | $15 | Standard from 2026-09-01 |

Source: [Claude Platform pricing](https://platform.claude.com/docs/en/about-claude/pricing).

### OpenAI GPT-5.6 API (official model pages, 2026-08-02)

| Model | Input / MTok | Cached input / MTok | Output / MTok |
| --- | ---: | ---: | ---: |
| GPT-5.6 Sol | $5.00 | $0.50 | $30.00 |
| GPT-5.6 Terra | $2.00 | $0.20 | $12.00 |
| GPT-5.6 Luna | $0.20 | $0.02 | $1.20 |

Sources: [gpt-5.6-sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol), [gpt-5.6-terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [gpt-5.6-luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

Long-context surcharge can apply on large Sol requests; check the live model page before estimating cost.

### Codex credits

Codex subscription usage is billed in credits, not raw API dollars. Public rate-card documentation exists, but the live credit table could not be scraped from this environment on 2026-08-02 (help page returned 403). Treat the following as **secondary calculator/community-derived ratios pending live rate-card confirmation**, not as a guaranteed official table:

| Model | Approx. relative credit rate vs Sol | Secondary source type |
| --- | --- | --- |
| Sol | 1× baseline | community/calculator |
| Terra | lower than Sol | community/calculator |
| Luna | much lower than Sol; often cited near ~1/25 of Sol for matching token mix | community/calculator |

Do not equate API $ prices with Codex credit burn. Context, reasoning, tools, retrieval, caching, and duration all change real cost.

Useful official entry points:

- [Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card)
- [Codex pricing overview](https://chatgpt.com/codex/pricing/)

### xAI Grok 4.5 API

Public listings commonly state **$2 / MTok input** and **$6 / MTok output** for Grok 4.5. The official pricing page returned 403 from this environment on 2026-08-02, so reconfirm on [x.ai/pricing](https://x.ai/pricing) before budget-critical work. Source type for the $2/$6 figure: secondary report of official pricing (2026-08-02).

## Reasoning effort

### Codex plugin / companion (local, 2026-08-02)

Installed `codex-plugin-cc` 1.0.6 companion help:

```text
task [--background] [--write] [--resume-last|--resume|--fresh] [--model <model|spark>] [--effort <none|minimal|low|medium|high|xhigh>] [prompt]
```

Local fixed mapping:

| Local policy name | Model | Effort flag | Write flag |
| --- | --- | --- | --- |
| Luna max | `gpt-5.6-luna` | `xhigh` | `--write` only when files must change |
| Sol high | `gpt-5.6-sol` | `high` | omit `--write`; read-only by default |

Notes:

- The plugin does not expose a literal `max` effort token. This Skill treats `xhigh` as the highest available plugin effort and uses it for the local “Luna max” policy.
- Do not leave model or effort unset for Luna/Sol routes.
- Do not use Ultra / nested-subagent fan-out modes.
- Sol high must not pass `--write`.
- Luna max passes `--write` only for true edit work; omit it for read-only execution against existing artifacts.
- Fallback CLI: `codex exec -m <model> -c model_reasoning_effort="<effort>" ...` with `-s read-only` for Sol and only broader sandbox when Luna must write.

### Grok Build (local, 2026-08-02)

`grok --help` exposes `--reasoning-effort` / `--effort`, `--no-subagents`, `--no-memory`, `--disable-web-search`, `--rules`, `--output-format`, `-p` / `--single`, and worktree flags. Prefer hard `--no-subagents` over prose-only bans.

Local call policy:

- Ordinary code/doc tasks that need no network: keep `--disable-web-search`.
- Heavy external research: omit `--disable-web-search`, require web search, and use any relevant connected MCPs that are actually available.
- Do not assume every MCP is present; report unavailable tools.
- Research tasks default to read-only project trees.

## Independent benchmark summary

Source type: independent evaluation. Dates below are article/publish context, not raw lab logs.

From Artificial Analysis coverage of GPT-5.6 (article context 2026-07-09) and Grok 4.5:

| Configuration | Coding Agent Index (approx.) | Notes |
| --- | ---: | --- |
| GPT-5.6 Sol max in Codex | ~80 | Reported leader in that write-up |
| GPT-5.6 Terra max | ~77 | Between Sol and Luna |
| GPT-5.6 Luna max | ~75 | Much cheaper per task in that setup |
| Grok 4.5 in Grok Build | ~76 | Strong token efficiency reported |

These scores measure **model + harness + effort product configs**, not bare model weights. They do not authorize the main agent to invent new routes.

Sources:

- [Artificial Analysis: GPT-5.6 has landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)
- [Artificial Analysis: Grok 4.5](https://artificialanalysis.ai/articles/grok-4-5-brings-spacexai-to-the-the-intelligence-frontier)

## Community evaluation summary

Source type: community experience only. Not proven universal facts.

Recurring positive patterns:

- Sol for planning, hard debugging, high-level analysis
- Luna max for long, clear, checkable implementation or batch work with lower subscription burn
- Grok Build for fast feature implementation and competitive coding output

Recurring warnings:

- Sol max / Ultra can burn credits quickly without proportional quality gains
- Large-repo re-ingestion wastes tokens even on cheap models
- Grok may forget project rules, expand scope, over-implement, over-abstract, or sound confident while wrong
- Some users report Claude Sonnet reasoning modes can be token-heavy or uneven

Local experience informing policy:

- Grok may partially ignore earlier `CLAUDE.md` on later turns inside Claude Code, so each Grok prompt must restate critical rules
- Codex is available locally via plugin + CLI; Grok Build CLI is installed and authenticated for `grok-4.5`

## User fixed routes

| Task type | Fixed worker | Config |
| --- | --- | --- |
| Code reading, exploration, inventory, mechanical checks, smoke tests | Claude Haiku | `haiku` |
| Ordinary data analysis, hypothesis checks, complex code analysis | Claude Sonnet | `sonnet` |
| Data cleaning, stats, charts, scripts, clear small bugs, objectively checkable execution | Codex Luna | `gpt-5.6-luna` + max (`xhigh`); `--write` only if edits needed |
| Core data analysis, complex reasoning, important candidate conclusions | Codex Sol | `gpt-5.6-sol` + high; no `--write` |
| Frontend, backend, experiment code, tests, project implementation | Grok Build | current official flagship coding model; `--disable-web-search` when offline is fine |
| Existing project documentation maintenance | Grok Build | current official flagship coding model; not absorbable by main-agent tiny-task exception |
| Broad external research, heavy search, time-sensitive checks, community surveys, multi-source cross-checks | Grok Build | web search enabled; relevant connected MCPs; default read-only |
| Important implementation core acceptance | Main Claude Code agent | never outsource |
| Final direction and key decisions | User / main agent with user | workers do not decide |

Why Luna uses max effort locally: Luna is cheap enough that the user prefers buying more reasoning on a low-price model for clear execution work. That is a **local cost strategy**, not OpenAI's universal recommendation.

Why Terra has no fixed route: official everyday-balance role is currently covered in practice by Haiku/Sonnet/Luna/Sol/Grok splits; use Terra only after explicit user choice.

Why heavy external research goes to Grok: Grok Build can combine its native web search with connected MCPs discovered for the workspace, while remaining a single non-nested worker under `--no-subagents`. Critical user-facing facts still require main-agent recheck.

## Conflict handling

Typical priority:

1. Formal project feature implementation → Grok
2. Broad external research / multi-source web verification → Grok research route
3. Data/script/batch/objectively checkable execution → Luna max
4. Ordinary internal analysis → Sonnet
5. High-value core analysis / candidate conclusions on already-held evidence → Sol high
6. Fast mechanical exploration → Haiku
7. Important implementation acceptance → main agent only
8. Existing doc maintenance → separate Grok task after acceptance; not a main-agent tiny-task shortcut

If still ambiguous: do not guess. Read this file, propose one recommendation and at most one alternative, and ask the user.

## Update rules

1. Stamp a new verification date.
2. Update official models, prices, and effort options first.
3. Then update independent benchmarks.
4. Keep community notes labeled as experience.
5. Preserve local policy unless the user changes it.
6. Do not flip fixed routes because of one forum post.
7. Never treat API dollars as identical to subscription credits or gateway bills.
8. After an update, state whether fixed routes changed.

## Source list

### Official / local tooling

- Claude Code skills docs: https://code.claude.com/docs/en/skills
- Claude Code subagents docs: https://code.claude.com/docs/en/sub-agents
- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
- OpenAI GPT-5.6 overview: https://openai.com/index/gpt-5-6/
- OpenAI model pages: https://developers.openai.com/api/docs/models/gpt-5.6-sol , `gpt-5.6-terra`, `gpt-5.6-luna`
- Codex rate card: https://help.openai.com/en/articles/20001106-codex-rate-card
- Codex pricing overview: https://chatgpt.com/codex/pricing/
- OpenAI official `codex-plugin-cc` (installed 1.0.6): companion `task [--write] --model --effort`
- Local CLIs on 2026-08-02: `codex-cli 0.146.0`, `grok 0.2.118`, Claude Code `2.1.220`
- xAI pricing / CLI pages: https://x.ai/pricing , https://x.ai/cli

### Independent evaluations

- https://artificialanalysis.ai/articles/gpt-5-6-has-landed
- https://artificialanalysis.ai/articles/grok-4-5-brings-spacexai-to-the-the-intelligence-frontier

### Community / secondary

- Public discussions of Luna/Terra price cuts and Codex credit calculators (experience only)
- User reports about Grok rule drift, over-scope, and Sol credit burn (experience only)
