---
name: mltheory-upgrade
description: "Structured mathlib upgrade workflow for MLTheory with pre/post index graph validation and rollback checkpoints."
---

# MLTheory Upgrade

Use this skill for dedicated mathlib upgrade phases only.
Do not use it for routine theorem patching.

## Scope

- Upgrade planning/execution for `lake-manifest` / mathlib rev changes in MLTheory.
- Lean interaction and symbol validation must still use `lean-lsp-mcp`.
- Keep upgrade in isolated PRs with explicit rollback points.

## Workflow (MUST)

1. Baseline snapshot
   - Run: `lake build`, two smoke tests, no-sorry/placeholder gates.
   - Regenerate baseline artifacts:
   - `tools/index/gen_mltheory_index.sh`
   - `tools/index/gen_mathlib_slice.sh`
   - `tools/index/gen_decl_graph.sh` (if available)
   - `tools/index/gen_graph_artifacts.sh` (if available)
2. Upgrade execution
   - Update mathlib dependency revision only (no mixed feature changes).
   - Run `lake update` / equivalent lock refresh.
3. Breakage triage
   - Use retrieval order:
   - local existence check -> loogle -> external semantic (optional).
   - Avoid broad `import Mathlib` quick fixes in business modules.
4. Patch in small batches
   - Keep each batch compilable; rerun gates after every batch.
5. Post-upgrade artifacts
   - Regenerate index/slice/decl_graph/subgraph artifacts.
   - Compare pre/post hub, slice size, and key API availability.
6. Upgrade report
   - Summarize:
   - changed dependency rev,
   - breakage categories,
   - files touched,
   - commands run,
   - rollback commit hash.

## Guardrails

- No `sorry`.
- No new custom `axiom`.
- No Placeholder theorem/lemma in `Core/Methods`.
- If regression persists, roll back to pre-upgrade commit and split batch smaller.
