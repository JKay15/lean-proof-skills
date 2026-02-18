---
name: ml-paper-workflow
description: "Strict construction wrapper for Lean paper task cards. Enforce Snapshot -> Retrieval -> Screening -> Minimal Patch -> Gate -> Artifact update using lean-lsp-mcp and $lean4."
allow_implicit_invocation: false
---

# ML Paper Workflow (Strict Wrapper)

Use this skill as a strict construction wrapper over `$lean4`.
This skill controls process and guardrails; low-level proof search/repair still delegates to `$lean4`.

## Scope

- Lean-only (`.lean`) and proof-oriented tasks.
- Do not use VSCode UI assumptions; use `lean-lsp-mcp` as the Lean interaction entrypoint.
- Keep theorem/lemma statements unchanged unless the user explicitly requests statement edits.
- No custom `axiom`; no `sorry`; no Placeholder theorem/lemma in `Core/Methods`.

## Fixed 6-Step Flow (MUST)

1. Snapshot
   - Collect diagnostics, current goal, file outline, and declaration location before editing.
   - Minimum calls: `lean_diagnostic_messages`, `lean_goal`, `lean_file_outline`, and declaration location (`lean_declaration_file`/local equivalent).
2. Retrieval
   - Enforce search order:
   - `local existence check first` (`lean_local_search` or declaration location check).
   - `structure/type search next` (`lean_loogle`).
   - `external semantic search last and optional` (`lean_leanfinder` / `lean_leansearch` only when needed).
   - Any symbol written into code must be existence-verified in step 1/2.
3. Screening
   - If tactic direction is uncertain, run parallel tactic screening with `lean_multi_attempt`.
   - Screening must not mutate source files.
4. Minimal Patch
   - Apply the smallest patch that advances only the active task card.
   - Avoid broad refactors or unrelated import rewrites.
5. Gate
   - Run repository gates before claiming success:
   - `lake build`
   - `lake env lean Eval/ImportSmoke.lean`
   - `lake env lean Eval/CanonicalAPISmoke.lean`
   - `tools/ci/check_no_sorry_axiom.sh`
   - `tools/ci/check_placeholder_policy.sh`
6. Artifact Update
   - If `tools/index/gen_mltheory_index.sh` exists, run it to refresh:
   - `artifacts/index/modules.json`
   - `artifacts/index/imports.json`
   - `artifacts/graphs/module_graph.json`
   - `docs/_auto/CodeIndex.md`
   - If `tools/index/gen_graph_artifacts.sh` exists, run it to refresh:
   - `artifacts/graphs/usage_graph.json`
   - `artifacts/index/usage_suggestions.json`
   - `artifacts/graphs/subgraph.json`
   - `docs/_auto/GraphArtifacts.md`
   - `docs/GraphExplorer.html` consumes refreshed subgraph data
   - If `tools/index/gen_mathlib_slice.sh` exists, run it when task touches mathlib retrieval/import scope.
   - If `tools/index/gen_decl_graph.sh` exists, run it when task changed declaration-level dependencies.
   - After a successful task card, if `tools/index/record_usage.py` exists, append one telemetry event with key declarations used in the final patch.
   - If scripts/artifacts do not exist yet, record `artifact_update = skipped(fallback)` and continue without fabricating files.

## Artifact/Phase Mapping (Repo A alignment)

- Phase 2: `docs/meta/*.yaml` + `modules/imports/module_graph`.
- Phase 3: `mathlib_slice` + `mltheory_to_mathlib`.
- Phase 4: `decl_graph` (`uses_type` / `uses_value`).
- Phase 5/6 (optional): `usage_graph` + `subgraph` + GraphExplorer.

Workflow should consume the highest available phase and degrade to lower phase/LSP-only mode when missing.

## Guardrails

- Prefer existing mathlib lemmas over custom constructions.
- Avoid `import Mathlib` in business modules unless working in an explicit compat/entry module.
- Retrieval order is mandatory; do not jump directly to external search.
- If `lean-lsp-mcp` is unavailable, state degradation explicitly and run conservative `lake` + grep checks.
