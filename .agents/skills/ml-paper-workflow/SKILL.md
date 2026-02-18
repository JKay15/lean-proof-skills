---
name: ml-paper-workflow
description: "Strict MLTheory wrapper: Intake v2 two-phase commit + Lean proof workflow with hard gates."
allow_implicit_invocation: false
---

# ML Paper Workflow (Strict Wrapper)

Use this skill as a strict construction wrapper over `$lean4`.
This skill controls process and guardrails; low-level proof search/repair still delegates to `$lean4`.

## Scope

- Lean-oriented MLTheory tasks (`.lean`) and task-card execution.
- New-problem ingestion MUST use Intake v2 two-phase commit.
- Do not use VSCode UI assumptions; use `lean-lsp-mcp` as Lean interaction entrypoint.
- Keep theorem/lemma statements unchanged unless the user explicitly requests statement edits.
- No custom `axiom`; no `sorry`; no Placeholder theorem/lemma in `Core/Methods`.

## Intake v2 Two-Phase Contract (MUST for new problems)

When task is a fresh problem (no existing `Spec.lean`/task card), run:

1. Research Pack phase
   - Create or verify:
   - `Incubator/<Domain>/<Problem>/research/sources.md`
   - `Incubator/<Domain>/<Problem>/research/glossary.yaml`
   - `Incubator/<Domain>/<Problem>/research/outline.md`
   - `Incubator/<Domain>/<Problem>/research/candidate_lemmas.md`
   - `Incubator/<Domain>/<Problem>/research/gaps.md`
   - Require source traceability for key claims; uncertain items must be marked.
2. Lean Commit phase
   - Run `python3 tools/intake/intake_v2.py lean-commit ...`.
   - Confirm generated:
   - `Spec.lean` (compilable, no sorry),
   - `Cache.lean` (proved lemmas only, compilable),
   - `Sketch.lean` (incubator-only decomposition file),
   - `Tasks.yaml`, `Telemetry.jsonl`.
   - Confirm metadata/artifact updates:
   - `docs/meta/taxonomy.yaml`, `docs/meta/aliases.yaml`,
   - refreshed `artifacts/index/*` and `artifacts/graphs/subgraph.json`.

If task is not a new problem, skip Intake generation and execute the standard proof flow below.

## Planner-Builder Batch Replan (MUST for stuck cards)

Use fixed role split when progress stalls:

1. Builder pass (Codex)
   - Try local retrieval/tactics first and record failed attempts per card.
2. Batch packaging
   - Aggregate multiple blocked cards into `Incubator/<Domain>/<Problem>/stuck_batches/<batch_id>.yaml`.
   - Include: goal, attempted tactics, blocker category, required missing lemmas/defs.
3. Planner pass (GPTPro)
   - Replan in batch (single call for multiple blocked cards).
   - Return split suggestions (`split_into`), bridge lemmas, and definition fixes.
4. Builder resume (Codex)
   - Update `Sketch.lean` + `Tasks.yaml`, prove leaves, and move proved lemmas into `Cache.lean`.
   - Re-run gates and refresh artifacts.

Planner calls should be low-frequency and high-bandwidth; Builder loops should stay high-frequency and gate-driven.

## Fixed 6-Step Proof Flow (MUST)

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
   - `docs/GraphExplorer.html` consumes refreshed subgraph data.
   - If scripts/artifacts do not exist yet, record `artifact_update = skipped(fallback)` and continue without fabricating files.

## Guardrails

- Prefer existing mathlib lemmas over custom constructions.
- Avoid `import Mathlib` in business modules unless working in an explicit compat/entry module.
- Retrieval order is mandatory; do not jump directly to external search.
- `Sketch.lean` may contain temporary decomposition only in `Incubator`; never move that state into `Core/Methods`.
- `Cache.lean` stores proved lemmas only (no sorry) and should be reused before opening new subgoals.
- If `lean-lsp-mcp` is unavailable, state degradation explicitly and run conservative `lake` + grep checks.
