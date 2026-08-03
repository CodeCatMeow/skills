# Skills

A personal collection of Claude Code skills. The repository follows the layout that [cc-switch](https://github.com/farion1231/cc-switch) expects for repository imports.

## Included skills

| Skill | Description |
| --- | --- |
| [`agent-delegation`](skills/agent-delegation/SKILL.md) | Fixed routing and acceptance for Claude Code subagents, Codex workers, and Grok Build on ordinary non-trivial tasks. |
| [`python-engineering`](skills/python-engineering/SKILL.md) | Provides practical engineering guidance for creating, changing, testing, and organizing Python code. |
| [`research-documentation`](skills/research-documentation/SKILL.md) | Maintains traceable research status, logs, experiment plans and reports, durable knowledge, decisions, protocols, and paper evidence. |
| [`software-docs`](skills/software-docs/SKILL.md) | Maintains human-first software documentation and ADRs for general software projects. Do not use for research documentation. |
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
