# lean-proof-skills

Language: **English** | [中文](README.zh-CN.md)

## Position in the 3-Repo Framework

This repository is the upstream **skillpack** for Lean + Codex formal proving.
Do not use this repository as the paper workspace itself.
Instead, mount it into a paper project repository via:

- submodule at `.agents/skillpacks/lean-proof-skills`
- facade symlinks under `.agents/skills/`

## Three-Repo Roles and Interfaces

Use placeholder names until real repos are finalized:

- `<ORG>/<LEAN-PROOF-SKILLS-REPO>`: reusable Codex skills (`$lean4`, `$ml-paper-workflow`, `$mltheory-*`)
- `<ORG>/<MLTHEORY-LEAN-REPO>`: shared Lean theorem library for ML/OR domains
- `<ORG>/<LEAN-PAPER-TEMPLATE-REPO>`: project template used to bootstrap each paper repo

This repository only owns:

- reusable skills
- skill IDs and invocation contracts
- integration instructions for paper repositories

## Skill IDs and Invocation Contract

- `$lean4`: base proving engine; implicit invocation is allowed.
- `$ml-paper-workflow`: orchestration wrapper; explicit invocation preferred.
- `$mltheory-snapshot`: pre-edit state snapshot wrapper (diagnostics/goal/outline/declaration locations).
- `$mltheory-retrieval`: goal-driven retrieval with strict `local -> loogle -> external(optional)` order.
- `$mltheory-import`: minimal import recommendation with slice/aggregator-aware fallback.
- `$mltheory-graph`: artifact refresh/context pack for slice + optional decl graph neighborhood mode.

## Required Layout in a Paper Repository

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
│   └── config.toml                          # project-level Codex config
└── lakefile.toml
```

Codex scans repo-scoped `.agents/skills` and follows symlinks, so the facade directory is the integration entrypoint.

## Assembly Steps (in a Paper Repository)

### 1) Add this repo as submodule

```bash
git submodule add https://github.com/<ORG>/<LEAN-PROOF-SKILLS-REPO>.git .agents/skillpacks/lean-proof-skills
git submodule update --init --recursive
```

### 2) Create facade links in `.agents/skills`

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

Windows symlink creation usually requires Developer Mode enabled or elevated privileges.

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

### 3) Configure Codex at project scope

Create or edit `.codex/config.toml` in the **paper repository**, not in this skillpack repository.
Put MCP settings (for example `lean-lsp-mcp`) there so configuration stays project-local.

### 4) Verify skill visibility

Start Codex from paper repo root and verify:

- `/skills` lists `lean4`, `ml-paper-workflow`, `mltheory-snapshot`, `mltheory-retrieval`, `mltheory-import`, and `mltheory-graph`, or
- typing `$` shows those skill chips

## Upgrade and Rollback (paper repo side)

### Upgrade to a newer skillpack commit/tag

```bash
git submodule update --init --recursive
cd .agents/skillpacks/lean-proof-skills
git fetch --tags origin
git checkout <target-commit-or-tag>
cd ../../..
git add .agents/skillpacks/lean-proof-skills
git commit -m "chore: bump lean-proof-skills submodule"
```

### Rollback to a previous submodule pointer

```bash
git checkout <older-paper-repo-commit> -- .agents/skillpacks/lean-proof-skills
git commit -m "chore: rollback lean-proof-skills submodule"
```

## Boundaries

- This repo is a skillpack upstream, not a proof project workspace.
- Keep skills repo-local in each paper repository; avoid global skill pollution.
- Keep proving output gated by Lean checks (`lake build`, agreed scope, no unauthorized axioms).
