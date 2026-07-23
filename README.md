# Private Claude Code Skills Repository

这是一个供个人维护的 Claude Code Skills 集合仓库，目录结构兼容 cc-switch 的远程仓库扫描和 ZIP 导入。

## 仓库结构

```text
.
├── skills/
│   └── uv/
│       └── SKILL.md
├── scripts/
│   └── validate-skills.ps1
├── docs/
│   └── cc-switch.md
├── .github/workflows/
│   └── validate.yml
├── .editorconfig
├── .gitattributes
└── .gitignore
```

每个 Skill 必须是 `skills/<skill-id>/` 下的独立目录，并且入口文件必须命名为大写的 `SKILL.md`：

```text
skills/<skill-id>/
├── SKILL.md       # 必需
├── references/    # 可选：按需加载的详细资料
├── scripts/       # 可选：Skill 自带脚本
├── assets/        # 可选：静态资源或输出模板
└── examples/      # 可选：示例
```

不要在 `skills/` 或仓库根目录放置 `SKILL.md`。cc-switch 找到某个目录中的 `SKILL.md` 后，不会继续扫描该目录下的嵌套 Skill。

## 新增 Skill

1. 创建 `skills/<skill-id>/SKILL.md`。
2. 使用小写 kebab-case 作为目录名和 frontmatter 中的 `name`，并保持两者一致。
3. 添加明确说明触发场景的 `description`。
4. 将较长的参考材料或辅助脚本放入同一 Skill 目录的相应子目录。
5. 在仓库根目录运行校验：

```powershell
pwsh -NoProfile -File scripts/validate-skills.ps1
```

最小入口示例：

```markdown
---
name: example-skill
description: Describe what this skill does and when Claude should use it.
---

# Example skill

Write the instructions Claude should follow.
```

## 当前 Skills

| Skill | 用途 |
|---|---|
| [`uv`](skills/uv/SKILL.md) | 使用 uv 管理 Python 项目、脚本、依赖和工具 |

## cc-switch 导入

详细方式和私有仓库限制见 [`docs/cc-switch.md`](docs/cc-switch.md)。

简要说明：

- cc-switch 递归扫描整个下载内容，因此 `skills/` 只是本仓库的组织约定，不是 cc-switch 的硬性要求。
- 远程仓库输入应为 `owner/repository` 或标准 GitHub HTTPS 仓库地址，分支单独填写为 `main`。
- cc-switch v3.18.0 使用匿名 GitHub ZIP 下载，不支持通过 PAT、SSH 或系统 Git 凭据认证私有 GitHub 仓库。
- 仓库保持私有时，应使用 cc-switch 的本地 ZIP 导入；以后若公开仓库，则可直接添加 GitHub 仓库。

## 本地 Git

仓库使用 `main` 作为初始分支。本次初始化只建立本地仓库，不创建远端、不提交，也不推送。

建议在首次提交前检查：

```powershell
git status
git diff --check
pwsh -NoProfile -File scripts/validate-skills.ps1
```

## 安全约定

不要提交令牌、私钥、Cookie、`.env`、本地配置、日志、缓存或打包产物。若 Skill 依赖环境变量，只提交不含真实值的 `.env.example`，并在 Skill 文档中说明配置方式。
