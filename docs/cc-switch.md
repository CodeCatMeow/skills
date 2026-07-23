# cc-switch 导入说明

本仓库按 cc-switch v3.18.0（2026-07-21）的实际扫描行为组织。

## 兼容规则

cc-switch 下载并递归扫描仓库内容。一个目录只要直接包含 `SKILL.md`，就会被识别为一个 Skill。它不要求 `manifest.json`、`index.json` 或其他仓库清单。

扫描遇到某个 Skill 后，不再继续寻找它内部的嵌套 Skill。因此本仓库采用扁平的独立目录：

```text
skills/
├── first-skill/
│   └── SKILL.md
└── second-skill/
    └── SKILL.md
```

辅助文件应放在对应 Skill 目录内部，这样安装时会和入口文件一起复制。

## 公开 GitHub 仓库导入

如果以后允许公开读取仓库，可在 cc-switch 的 Skills 仓库管理界面中填写：

```text
Repository: <github-owner>/<repository-name>
Branch: main
```

Repository 也可填写：

```text
https://github.com/<github-owner>/<repository-name>
```

不要填写：

- `git@github.com:owner/repo.git`
- `/tree/main/skills` 形式的子目录 URL
- GitHub API URL
- GitHub Enterprise URL

cc-switch 当前会尝试下载所填分支，并回退到 `main`、`master`。它会扫描整个仓库，不能在界面中限制只扫描 `skills/`。

## 私有 GitHub 仓库限制

cc-switch v3.18.0 的仓库导入不是 `git clone`，而是匿名请求：

```text
https://github.com/<owner>/<repo>/archive/refs/heads/<branch>.zip
```

其配置中没有 GitHub PAT、OAuth、SSH key 或认证请求头，因此普通私有 GitHub 仓库无法直接通过 Repository 功能导入。把 token 写入 URL 也不是受支持或安全的方案。

### 私有仓库推荐流程

1. 保持 GitHub 仓库为 private。
2. 在本地仓库运行校验。
3. 生成一个不包含 Git 元数据的 ZIP：

   ```powershell
   git archive --format=zip --output=skills.zip HEAD
   ```

   这要求先至少创建一次本地提交。如果还未提交，可在文件资源管理器中压缩 `skills/` 下需要导入的 Skill 目录；不要把 `.git/` 打包进去。

4. 在 cc-switch 中使用本地 ZIP 导入。

如果 cc-switch 后续版本增加私有仓库认证，应重新核对该版本文档与实现后再改用远程导入。

## 相关资料

- cc-switch Skills 用户手册：<https://github.com/farion1231/cc-switch/blob/v3.18.0/docs/user-manual/en/3-extensions/3.3-skills.md>
- Claude Code Skills 文档：<https://code.claude.com/docs/en/skills>
