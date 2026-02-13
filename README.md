# lean-proof-skills

## 项目定位 / Project Purpose

本仓库用于沉淀可复用的 Lean4 证明技能包。目标是让后续项目在需要形式化数学证明时，直接 clone 本仓库并在 Codex 中显式调用技能使用。  
This repository provides a reusable Lean4 proof skill pack. The goal is to let future projects clone this repo and explicitly invoke skills in Codex for formal math proving tasks.

## 仓库结构 / Repository Structure

```text
.agents/skills/
├── lean4/
│   ├── SKILL.md
│   └── references/
└── ml-paper-workflow/
    ├── SKILL.md
    └── agents/openai.yaml
```

`lean4` 是底层 Lean4 proving 引擎；`ml-paper-workflow` 是上层论文任务卡编排层。  
`lean4` is the base Lean4 proving engine; `ml-paper-workflow` is the upper workflow wrapper for paper/task-card driven formalization.

## Skills 说明 / Skills

- `$lean4`: 直接处理 Lean 证明与修复循环（目标查看、mathlib 搜索、证明构造、构建验证）。
- `$ml-paper-workflow`: 将论文蓝图或任务卡转为证明步骤，并显式委托 `$lean4` 执行正式 proving cycle。

- `$lean4`: Use this skill for direct Lean proof development and repair cycles.
- `$ml-paper-workflow`: Use this wrapper to drive proving from paper blueprints/task cards and explicitly delegate formal proving to `$lean4`.

## 快速开始 / Quick Start

1. 克隆仓库并进入目录。  
   Clone the repository and enter it.
   ```bash
   git clone <your-repo-url>
   cd lean-proof-skills
   ```
2. 在 Codex 中把工作目录设为仓库根目录，并显式调用技能。  
   In Codex, set the working directory to the repository root and invoke skills explicitly.
3. 优先流程：先用 `$ml-paper-workflow` 组织任务，再由 `$lean4` 执行证明。  
   Preferred flow: use `$ml-paper-workflow` for task orchestration, then let `$lean4` run proving.

## 使用示例 / Prompt Examples

```text
Use $ml-paper-workflow to formalize this measure-theory lemma from my task card.
Keep theorem statements unchanged, produce minimal patch, and finish with lake build validation.
```

```text
Use $lean4 to solve the current sorry in this .lean file.
Search mathlib first, avoid new axioms, and stop after a verified compile pass.
```

## 边界与约束 / Boundaries and Constraints

- 仅用于 Lean 证明任务（`.lean` 文件）；非证明或非 Lean 任务应拒绝或回退。
- `ml-paper-workflow` 是编排层，不替代 `lean4` 的底层证明能力。
- 默认坚持最小改动（minimal patch），避免与当前任务无关的大范围重构。
- Skills 必须 repo-local 使用，不依赖仓库外 skill 目录。

- Lean-only proof scope (`.lean` files); non-proof/non-Lean tasks should be rejected or handed back.
- `ml-paper-workflow` is orchestration only and does not replace `$lean4`.
- Prefer minimal patches and avoid broad unrelated refactors.
- Skills must remain repo-local and not depend on external skill directories.

## 验收标准 / Acceptance Criteria

- `lake build` 通过（或先通过文件级 gate，再通过项目级 gate）。
- 不引入未授权公理（no unauthorized axioms）。
- 在约定范围内清除 `sorry`，且不擅自改动 theorem/lemma statement。
- 输出包含：变更内容、未解决阻塞、下一步任务卡。

- `lake build` passes (or file-level gate first, then project-level gate).
- No unauthorized axioms are introduced.
- Sorries are resolved within agreed scope without silent statement changes.
- Output reports what changed, blockers, and the next task card.
