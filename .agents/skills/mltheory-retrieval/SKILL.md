---
name: mltheory-retrieval
description: "Goal-driven retrieval for MLTheory with mandatory order: local existence -> loogle -> external semantic search (optional)."
---

# MLTheory Retrieval

Use this skill to build a high-signal candidate set for a Lean goal.
This skill is retrieval-only; proof construction stays in `$lean4` or `$ml-paper-workflow`.

## Scope

- Lean files and goals in MLTheory.
- Must use `lean-lsp-mcp` tools.
- Must verify every emitted symbol exists locally.

## Fixed Retrieval Order (MUST)

1. Local existence first
   - Use `lean_local_search` and/or declaration-location checks.
   - Discard symbols that cannot be resolved locally.
2. Structural/type search second
   - Use `lean_loogle` with goal-shape queries.
3. External semantic search last (optional)
   - Use `lean_leanfinder` / `lean_leansearch` only if steps 1-2 are insufficient.

## Candidate Narrowing (MUST when artifacts exist)

- If `artifacts/graphs/decl_graph.json` exists:
  - Restrict first pass to 1-2 hop neighbors of current declarations.
- If `artifacts/index/mathlib_slice.json` exists:
  - Prefer symbols/modules inside slice before global mathlib expansion.

## Fallback (when artifacts are missing)

- Use LSP-only neighborhood:
  - current module declarations,
  - imported modules from file outline,
  - local + loogle search results.
- Mark output as `artifact_mode = fallback`.

## Output Contract

- Goal summary.
- Candidate declarations with:
  - existence proof method (`local_search`/`declaration_file`),
  - source module,
  - why selected (type match / graph neighbor / slice hit).
