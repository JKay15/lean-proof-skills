# lean-proof-skills

language: [English](README.md) | **Chinese**

## Positioning in the Three Cang Framework

This warehouse is Lean + Codex Upstream in the mathematical proof system **skillpack** storehouse.
Don’t use it as a thesis ontology workspace to do proofs directly..
The correct way is to assemble it into the paper warehouse:

- as submodule hang on `.agents/skillpacks/lean-proof-skills`
- exist `.agents/skills/` put facade symlink Expose skill entrance

## The roles and interfaces of the three warehouses

Before confirming the real warehouse name,Use placeholders:

- `<ORG>/<LEAN-PROOF-SKILLS-REPO>`:Reusable Codex Skill(`$lean4`,`$ml-paper-workflow`,`$mltheory-*`)
- `<ORG>/<MLTHEORY-LEAN-REPO>`:ML/OR Sharing of directions Lean Theorem library
- `<ORG>/<LEAN-PAPER-TEMPLATE-REPO>`:Template repository for each paper project

This warehouse is only responsible for:

- Provide reusable skills
- exposed skill IDs and call contract
- Integration instructions for maintaining the paper repository side

## Skill ID and call contract

- `$lean4`:Ground floor proving engine;Allow implicit triggering.
- `$ml-paper-workflow`:Thesis task card arrangement layer;Prioritize explicit calls.
- `$mltheory-snapshot`:Pre-construction status snapshot(diagnostics/goal/outline/Declare positioning).
- `$mltheory-retrieval`:goal-driven retrieval,strictly follow `local -> loogle -> external(Optional)`.
- `$mltheory-import`:smallest import suggester,priority slice/aggregator,Automatically downgrade when missing.
- `$mltheory-graph`:refresh slice/graph product and generate neighborhood search context(`decl_graph` Automatically downgrade when missing).

## Fixed directory conventions in thesis repository

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
│   └── config.toml                          # project level Codex Configuration
└── lakefile.toml
```

Codex Will scan repo scope of `.agents/skills` and follow symlink,therefore facade The directory is the actual access entrance.

## Assembly steps(Executed in the paper repository)

### 1) Add this repository as submodule

```bash
git submodule add https://github.com/<ORG>/<LEAN-PROOF-SKILLS-REPO>.git .agents/skillpacks/lean-proof-skills
git submodule update --init --recursive
```

### 2) exist `.agents/skills` create facade Link

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

Windows Creating symbolic links usually requires turning on developer mode or using administrator privileges.

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

### 3) Configure project level Codex

`.codex/config.toml` should be placed**Paper warehouse**middle,instead of Ben skillpack storehouse.
For example MCP(`lean-lsp-mcp`)The configuration should be written in the paper repository `.codex/config.toml`,Keep projects isolated.

### 4) Verify skill visibility

Start in the root directory of the paper repository Codex,and verify:

- `/skills` appear in `lean4`,`ml-paper-workflow`,`mltheory-snapshot`,`mltheory-retrieval`,`mltheory-import`,`mltheory-graph`,or
- enter `$` These skills can be seen when chip

## Upgrades and rollbacks(Thesis warehouse side)

### upgrade to new skillpack submit or tag

```bash
git submodule update --init --recursive
cd .agents/skillpacks/lean-proof-skills
git fetch --tags origin
git checkout <target-commit-or-tag>
cd ../../..
git add .agents/skillpacks/lean-proof-skills
git commit -m "chore: bump lean-proof-skills submodule"
```

### rollback to old submodule pointer

```bash
git checkout <older-paper-repo-commit> -- .agents/skillpacks/lean-proof-skills
git commit -m "chore: rollback lean-proof-skills submodule"
```

## boundary

- This warehouse is skillpack upstream warehouse,Not a paper ontology proof warehouse.
- skills Through thesis repository repo scope exposed,Does not rely on global skill catalog.
- The final proof is that the quality is still Lean Construction of access control shall prevail(`lake build`,scope constraints,No unauthorized axiom).
