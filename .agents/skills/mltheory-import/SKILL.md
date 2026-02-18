---
name: mltheory-import
description: "Recommend minimal, verifiable imports for MLTheory tasks, prioritizing local modules and mathlib slice/aggregator hints."
---

# MLTheory Import

Use this skill to propose minimal imports for declarations selected by retrieval.

## Scope

- Lean import planning for MLTheory modules.
- Works with `lean-lsp-mcp` declaration lookups and local search.
- Does not edit files automatically; returns import recommendations and rationale.

## Import Policy (MUST)

1. Prefer MLTheory modules first
   - Prefer canonical/bridge module paths that already expose the declaration.
2. For Mathlib symbols
   - Prefer slice-limited modules when `artifacts/index/mathlib_slice.json` exists.
   - Prefer aggregator modules from `artifacts/index/mathlib_aggregators.json` when valid.
   - If no aggregator fit, use declaration-owning module as fallback.
3. Avoid broad imports
   - Do not recommend `import Mathlib` in business modules.
   - Only allow broad import in explicit compat/entry modules, and explain why.

## Validation (MUST)

- Every suggested import must map to at least one existence-verified declaration.
- Show mapping: declaration -> declaring module -> suggested import.

## Fallback

- If slice/aggregator artifacts are absent:
  - use declaration-owning module imports only,
  - keep recommendations conservative and explicit.

## Output Contract

- Ordered import list (most preferred first).
- For each import: covered declarations + reason + whether it came from slice/aggregator/fallback.
