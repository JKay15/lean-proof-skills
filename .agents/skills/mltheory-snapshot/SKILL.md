---
name: mltheory-snapshot
description: "Create a reproducible MLTheory Lean state snapshot (diagnostics/goal/outline/declaration locations) before patching."
allow_implicit_invocation: false
---

# MLTheory Snapshot

Use this skill before editing Lean task cards in MLTheory.
It captures a stable baseline so later retrieval/patch/gate steps are auditable.

## Scope

- Lean files only (`.lean`) in MLTheory workspaces.
- Lean interaction must go through `lean-lsp-mcp` tools.
- Do not modify source files in this step.

## Snapshot Contract (MUST)

1. Diagnostics
   - Run `lean_diagnostic_messages` on the target file.
2. Goal state
   - Run `lean_goal` at the active line/position.
3. Outline
   - Run `lean_file_outline` for imports + declaration signatures.
4. Declaration location checks
   - For task-card symbols, resolve declaration files (`lean_declaration_file` or local equivalent).
5. Artifact presence probe
   - Check whether these artifacts exist:
   - `docs/meta/taxonomy.yaml`
   - `docs/meta/aliases.yaml`
   - `docs/meta/canon.yaml`
   - `artifacts/index/modules.json`
   - `artifacts/index/imports.json`
   - `artifacts/graphs/module_graph.json`
   - `artifacts/index/mathlib_slice.json`
   - `artifacts/index/mathlib_aggregators.json`
   - `artifacts/graphs/decl_graph.json`
   - `artifacts/graphs/usage_graph.json`
   - `artifacts/graphs/subgraph.json`
   - `docs/GraphExplorer.html`
6. Structured output
   - Report: file, goal, blockers, symbols with source module, artifact availability by phase (2/3/4), and fallback mode.

## Fallback

- If graph/slice artifacts are missing, mark `artifact_mode = fallback` and proceed with LSP-only retrieval.
- If `lean-lsp-mcp` is unavailable, stop and report degraded mode explicitly.
