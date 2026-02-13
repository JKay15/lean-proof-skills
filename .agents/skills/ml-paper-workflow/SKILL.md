---
name: ml-paper-workflow
description: "Use when formalizing mathematics in Lean from paper blueprints or task cards, especially measure theory, probability, statistics, optimization, and information theory. Coordinate Lean LSP MCP inspection, mathlib search, minimal patches, and lake build verification. Do not use for non-Lean files or non-proof tasks."
---

# ML Paper Workflow

Use this skill as a thin workflow wrapper over `$lean4`.
Delegate formal proving and repair cycles to `$lean4` instead of re-implementing low-level proving logic here.

## Scope

- Work only on `.lean` files and proof-oriented tasks.
- Refuse or hand back non-Lean or non-proof work.
- Keep theorem and lemma statements unchanged unless the user explicitly requests changes.

## Workflow

1. Translate the user request into a paper blueprint or task card:
   - target theorem or lemma name,
   - expected mathematical claim,
   - file path and scope,
   - acceptance gate (`lake build`, no unauthorized axioms).
2. Use Lean LSP MCP to inspect goals and diagnostics, then search mathlib before writing tactics.
3. Produce the smallest patch that advances only the active task card.
4. Delegate the formal cycle to `$lean4`:
   - Plan -> Work -> Checkpoint -> Review -> Replan
5. Validate with `lake build` (or file-level gate first), then report:
   - what changed,
   - unresolved blockers,
   - the next task card.

## Guardrails

- Prefer existing mathlib lemmas over custom constructions.
- Avoid broad refactors outside the active proof scope.
- Do not introduce custom axioms without explicit permission.
- If Lean LSP MCP is unavailable, state the limitation and continue conservatively with `lake`-based checks.
