---
name: mltheory-graph
description: "Refresh MLTheory slice/graph artifacts and prepare neighborhood retrieval context with decl_graph-aware fallback."
---

# MLTheory Graph

Use this skill when retrieval or visualization depends on project artifacts.

## Scope

- Artifact refresh for:
  - `artifacts/index/mathlib_slice.json`
  - `artifacts/index/mltheory_to_mathlib.json`
  - optional `artifacts/graphs/decl_graph.json`
- Lean interactions still use `lean-lsp-mcp` (no VSCode UI dependency).

## Workflow

1. Refresh index artifacts
   - Run project script (for example `tools/index/gen_mathlib_slice.sh`) to regenerate slice/index outputs.
2. Probe graph artifacts
   - If `artifacts/graphs/decl_graph.json` exists, enable neighbor-first retrieval mode.
   - If it does not exist, set `graph_mode = fallback` and continue with slice + LSP retrieval.
3. Build retrieval context pack
   - Include current module, relevant slice roots, and available graph files.
4. Hand off
   - Pass the context pack to `$mltheory-retrieval` / `$ml-paper-workflow`.

## Guardrails

- Do not hand-edit generated artifact JSON.
- If scripts fail, report exact failing command and keep existing artifacts untouched.
