# Skills

A personal collection of Claude Code skills. The repository follows the layout that [cc-switch](https://github.com/farion1231/cc-switch) expects for repository imports.

## Included skills

| Skill | Description |
| --- | --- |
| [`agent-toolkit`](skills/agent-toolkit/SKILL.md) | Explicit-only use of Claude Code native/named agents and optional Grok Build CLI. |
| [`gflow-ops`](skills/gflow-ops/SKILL.md) | Local-first gflow scheduler inspection, job operations, logs, and safe validation through MCP or CLI. |
| [`hydra-configuration`](skills/hydra-configuration/SKILL.md) | Correct Hydra composition: Config Groups, Defaults List, experiment deltas, overrides, multirun, outputs, instantiate, and progressive migration. |
| [`python-engineering`](skills/python-engineering/SKILL.md) | Concise Python guardrails: repository fit, Google style, cohesive boundaries, risk-matched evidence, and uv. |
| [`research-code-organization`](skills/research-code-organization/SKILL.md) | Explicit-only cleanup guidance for duplicated experiment launchers, permanent flags, and established research script sprawl. |
| [`research-documentation`](skills/research-documentation/SKILL.md) | Records only decision-relevant research context; Markdown for daily notes and Quarto for executable or formal reports. |
| [`software-docs`](skills/software-docs/SKILL.md) | Makes the smallest necessary update when long-lived software documentation would otherwise be wrong. |
| [`uv`](skills/uv/SKILL.md) | Guides Claude Code to use uv for Python projects, scripts, dependencies, environments, and command-line tools. |

## Import with cc-switch

Add this repository in the cc-switch Skills repository manager:

```text
Repository: CodeCatMeow/skills
Branch: main
```

cc-switch scans the repository for `SKILL.md` files and lists each matching directory as an installable skill.

## Layout

Each skill lives in its own directory:

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # optional
├── scripts/      # optional
├── templates/    # optional
├── assets/       # optional
└── examples/     # optional
```

Run the repository check after editing or adding a skill:

```powershell
pwsh -NoProfile -File scripts/validate-skills.ps1
```

This repository is public so cc-switch can import it. Its contents are maintained for personal use and may change without notice.
