---
name: mltheory-graph
description: "Refresh MLTheory slice/graph artifacts and prepare neighborhood retrieval context with decl_graph-aware fallback."
allow_implicit_invocation: false
---

# MLTheory Graph

Use this skill when retrieval or visualization depends on project artifacts.

## Scope

- Artifact refresh for:
  - `artifacts/index/modules.json`
  - `artifacts/index/imports.json`
  - `artifacts/graphs/module_graph.json`
  - `docs/_auto/CodeIndex.md`
  - `artifacts/index/mathlib_slice.json`
  - `artifacts/index/mltheory_to_mathlib.json`
  - `artifacts/graphs/usage_graph.json`
  - `artifacts/index/usage_suggestions.json`
  - `artifacts/graphs/subgraph.json`
  - `docs/_auto/GraphArtifacts.md`
  - `docs/GraphExplorer.html` (data consumer)
  - optional `artifacts/graphs/decl_graph.json`
- Lean interactions still use `lean-lsp-mcp` (no VSCode UI dependency).

## Workflow

1. Refresh index artifacts
   - Run `tools/index/gen_mltheory_index.sh` if present (Phase 2).
   - Run `tools/index/gen_mathlib_slice.sh` if present (Phase 3).
   - Run `tools/index/gen_decl_graph.sh` if present and declaration-level edges are needed (Phase 4).
   - Run `tools/index/gen_graph_artifacts.sh` if present (Phase 5/6 optional telemetry + subgraph).
2. Optional telemetry writeback
   - If this run solved a concrete task card and `tools/index/record_usage.py` exists, append one usage event with the final used declarations.
3. Probe graph artifacts
   - If `artifacts/graphs/decl_graph.json` exists, enable neighbor-first retrieval mode.
   - If it does not exist, set `graph_mode = fallback` and continue with module graph + slice + LSP retrieval.
4. Build retrieval context pack
   - Include current module, relevant import neighbors, slice roots, and available graph files.
5. Hand off
   - Pass the context pack to `$mltheory-retrieval` / `$ml-paper-workflow`.

## Guardrails

- Do not hand-edit generated artifact JSON.
- If scripts fail, report exact failing command and keep existing artifacts untouched.
