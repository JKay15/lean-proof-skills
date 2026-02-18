---
name: ml-paper-workflow
description: "Strict construction wrapper for Lean paper task cards. Enforce Snapshot -> Retrieval -> Screening -> Minimal Patch -> Gate -> Artifact update using lean-lsp-mcp and $lean4."
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
   - If repository phase already provides `artifacts/index` or `artifacts/graphs` (for example slice/decl_graph), update the relevant artifacts/index in the same task.
   - If those artifacts do not exist yet, record "artifact update skipped (fallback)" and continue without fabricating files.

## Guardrails

- Prefer existing mathlib lemmas over custom constructions.
- Avoid `import Mathlib` in business modules unless working in an explicit compat/entry module.
- Retrieval order is mandatory; do not jump directly to external search.
- If `lean-lsp-mcp` is unavailable, state degradation explicitly and run conservative `lake` + grep checks.
