# lean-proof-skills

语言: [English](README.md) | **中文**

## 在三仓框架中的定位

本仓库是 Lean + Codex 数学证明体系里的上游 **skillpack** 仓库。
不要把它当作论文本体工作区直接做证明。
正确方式是把它装配进论文仓库：

- 作为 submodule 挂到 `.agents/skillpacks/lean-proof-skills`
- 在 `.agents/skills/` 放 facade symlink 暴露技能入口

## 三个仓库的角色与接口

在真实仓库名确认前，使用占位符：

- `<ORG>/<LEAN-PROOF-SKILLS-REPO>`：可复用 Codex 技能（`$lean4`、`$ml-paper-workflow`、`$mltheory-*`）
- `<ORG>/<MLTHEORY-LEAN-REPO>`：ML/OR 方向的共享 Lean 定理库
- `<ORG>/<LEAN-PAPER-TEMPLATE-REPO>`：每篇论文项目的模板仓库

本仓库只负责：

- 提供可复用 skills
- 暴露 skill IDs 与调用契约
- 维护论文仓库侧的集成说明

## Skill ID 与调用契约

- `$lean4`：底层 proving 引擎；允许隐式触发。
- `$ml-paper-workflow`：论文任务卡编排层；优先显式调用。
- `$mltheory-snapshot`：施工前状态快照（diagnostics/goal/outline/声明定位）。
- `$mltheory-retrieval`：目标驱动检索，严格遵循 `本地 -> loogle -> 外部(可选)`。
- `$mltheory-import`：最小 import 建议器，优先 slice/aggregator，缺失时自动降级。
- `$mltheory-graph`：刷新 slice/graph 产物并生成邻域检索上下文（`decl_graph` 缺失时自动降级）。

## 论文仓库中的固定目录约定

```text
paper-foo/
├── .agents/
│   ├── skillpacks/
│   │   └── lean-proof-skills/              # git submodule
│   └── skills/
│       ├── lean4 -> ../skillpacks/lean-proof-skills/.agents/skills/lean4
│       ├── ml-paper-workflow -> ../skillpacks/lean-proof-skills/.agents/skills/ml-paper-workflow
│       ├── mltheory-snapshot -> ../skillpacks/lean-proof-skills/.agents/skills/mltheory-snapshot
│       ├── mltheory-retrieval -> ../skillpacks/lean-proof-skills/.agents/skills/mltheory-retrieval
│       ├── mltheory-import -> ../skillpacks/lean-proof-skills/.agents/skills/mltheory-import
│       └── mltheory-graph -> ../skillpacks/lean-proof-skills/.agents/skills/mltheory-graph
├── .codex/
│   └── config.toml                          # 项目级 Codex 配置
└── lakefile.toml
```

Codex 会扫描 repo scope 的 `.agents/skills` 并跟随 symlink，因此 facade 目录是实际接入入口。

## 装配步骤（在论文仓库执行）

### 1) 添加本仓库作为 submodule

```bash
git submodule add https://github.com/<ORG>/<LEAN-PROOF-SKILLS-REPO>.git .agents/skillpacks/lean-proof-skills
git submodule update --init --recursive
```

### 2) 在 `.agents/skills` 创建 facade 链接

#### macOS / Linux

```bash
mkdir -p .agents/skills
ln -s ../skillpacks/lean-proof-skills/.agents/skills/lean4 .agents/skills/lean4
ln -s ../skillpacks/lean-proof-skills/.agents/skills/ml-paper-workflow .agents/skills/ml-paper-workflow
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-snapshot .agents/skills/mltheory-snapshot
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-retrieval .agents/skills/mltheory-retrieval
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-import .agents/skills/mltheory-import
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-graph .agents/skills/mltheory-graph
```

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path .agents/skills | Out-Null
New-Item -ItemType SymbolicLink -Path .agents/skills/lean4 -Target ../skillpacks/lean-proof-skills/.agents/skills/lean4
New-Item -ItemType SymbolicLink -Path .agents/skills/ml-paper-workflow -Target ../skillpacks/lean-proof-skills/.agents/skills/ml-paper-workflow
New-Item -ItemType SymbolicLink -Path .agents/skills/mltheory-snapshot -Target ../skillpacks/lean-proof-skills/.agents/skills/mltheory-snapshot
New-Item -ItemType SymbolicLink -Path .agents/skills/mltheory-retrieval -Target ../skillpacks/lean-proof-skills/.agents/skills/mltheory-retrieval
New-Item -ItemType SymbolicLink -Path .agents/skills/mltheory-import -Target ../skillpacks/lean-proof-skills/.agents/skills/mltheory-import
New-Item -ItemType SymbolicLink -Path .agents/skills/mltheory-graph -Target ../skillpacks/lean-proof-skills/.agents/skills/mltheory-graph
```

Windows 创建符号链接通常需要开启开发者模式或使用管理员权限。

#### Git Bash (Windows)

```bash
mkdir -p .agents/skills
ln -s ../skillpacks/lean-proof-skills/.agents/skills/lean4 .agents/skills/lean4
ln -s ../skillpacks/lean-proof-skills/.agents/skills/ml-paper-workflow .agents/skills/ml-paper-workflow
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-snapshot .agents/skills/mltheory-snapshot
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-retrieval .agents/skills/mltheory-retrieval
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-import .agents/skills/mltheory-import
ln -s ../skillpacks/lean-proof-skills/.agents/skills/mltheory-graph .agents/skills/mltheory-graph
```

### 3) 配置项目级 Codex

`.codex/config.toml` 应放在**论文仓库**中，而不是本 skillpack 仓库。
例如 MCP（`lean-lsp-mcp`）配置应写在论文仓库的 `.codex/config.toml`，保持项目隔离。

### 4) 验证技能可见性

在论文仓库根目录启动 Codex，并验证：

- `/skills` 里出现 `lean4`、`ml-paper-workflow`、`mltheory-snapshot`、`mltheory-retrieval`、`mltheory-import`、`mltheory-graph`，或
- 输入 `$` 时能看到这些技能 chip

## 升级与回滚（论文仓库侧）

### 升级到新的 skillpack 提交或 tag

```bash
git submodule update --init --recursive
cd .agents/skillpacks/lean-proof-skills
git fetch --tags origin
git checkout <target-commit-or-tag>
cd ../../..
git add .agents/skillpacks/lean-proof-skills
git commit -m "chore: bump lean-proof-skills submodule"
```

### 回滚到旧的 submodule 指针

```bash
git checkout <older-paper-repo-commit> -- .agents/skillpacks/lean-proof-skills
git commit -m "chore: rollback lean-proof-skills submodule"
```

## 边界

- 本仓库是 skillpack 上游仓库，不是论文本体证明仓库。
- skills 通过论文仓库的 repo scope 暴露，不依赖全局技能目录。
- 最终证明质量仍以 Lean 构建门禁为准（`lake build`、范围约束、禁止未授权公理）。
