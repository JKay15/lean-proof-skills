---
name: mltheory-retrieval
description: "Domain-profile-first retrieval for MLTheory with progressive widening: domain-local -> domain-slice -> adjacent domains -> full library -> external semantic search."
allow_implicit_invocation: false
---

# MLTheory Retrieval

Use this skill to build a high-signal candidate set for a Lean goal.
This skill is retrieval-only; proof construction stays in `$lean4` or `$ml-paper-workflow`.

## Scope

- Lean files and goals in MLTheory.
- Must call MLTheory unified retrieval entrypoint: `tools/retrieval/query.py`.
- Must verify every emitted symbol exists locally.
- Must honor MLTheory Domain Profile boundaries when available.

## Domain Sources (MUST)

Load and use these sources when present:

- `docs/meta/domains.yaml`
- `artifacts/graphs/subgraph.json` (`domains.profiles`, node `domains`)
- `artifacts/index/mathlib_slice.json`

Domain Profile fields to consume:

- `allowed_local_roots`
- `module_roots`
- `default_imports`
- `mathlib_slice_roots`
- `bridge_modules`
- `adjacent_domains`

If domain cannot be inferred from the task/card, use `default_domain`; if still unresolved, use `all`.

## Executable Entry (MUST)

Do not directly call ad-hoc MCP search tools here. Call the wrapper:

```bash
python3 /path/to/MLTheory/tools/retrieval/query.py \
  --query "<goal or keyword>" \
  --goal "<goal summary>" \
  --domain "<active_domain>" \
  --context-module "<current module>" \
  --task "<task card id>" \
  --emit-limit 30
```

Wrapper backend order is fixed and auditable:
- local confirm (decl index + local Lean check)
- local `rg` search
- Loogle JSON
- LeanExplore (optional, endpoint-driven)

## Fixed Retrieval Order (MUST)

Progressive widening is mandatory. Do not skip stages unless required artifacts are missing.

1. Domain-local MLTheory first
   - Search current module + local declarations inside active domain `allowed_local_roots/module_roots`.
   - Use `lean_local_search` and declaration-file checks.
2. Domain mathlib slice second
   - Search only `mathlib_slice_roots` (or slice modules tagged with active domain).
   - Use `lean_loogle` constrained by slice/module context.
3. Adjacent-domain widening third
   - Expand only to `adjacent_domains` (+ declared `bridge_modules`).
   - Keep search boundary local to those domains.
4. Full MLTheory fourth
   - Search all MLTheory modules if stages 1-3 are insufficient.
5. Full mathlib fifth
   - Search global mathlib only after local/domain passes are exhausted.
6. External semantic retrieval last (optional)
   - Keep this inside `query.py` external backend only when 1-5 are insufficient.

## Existence Verification (MUST at every stage)

For every candidate emitted at any stage:

- Verify existence via wrapper verification (`decl_index` and/or local Lean `#check`).
- Drop unresolved symbols immediately.
- Record verification method per candidate.

No unverified symbol may appear in output.

## Candidate Narrowing (MUST when artifacts exist)

- If `artifacts/index/imports.json` and `artifacts/graphs/module_graph.json` exist:
  - Restrict first pass to current module and 1-2 hop import neighbors.
- If `artifacts/graphs/decl_graph.json` exists:
  - Restrict first pass to 1-2 hop declaration neighbors.
- If `artifacts/graphs/subgraph.json` exists:
  - Prefer nodes with `spine=true` and higher `used_recently` weight.
  - Respect node `domains` before widening.
- If `docs/meta/aliases.yaml` exists:
  - Expand user keywords by aliases before query construction.
- Always keep telemetry enabled (`artifacts/telemetry/retrieval.jsonl` + usage events for final hits).

## Fallback

If domain artifacts are missing or incomplete:

- Degrade to LSP-only neighborhood:
  - current module declarations,
  - imported modules from file outline,
  - local + loogle results,
  - external semantic search last.
- Mark output with `artifact_mode = fallback` and list missing files.

## Output Contract

- Goal summary.
- Domain context:
  - `active_domain`,
  - `widening_path` (stages used),
  - whether bridge modules were used.
- Candidate declarations with:
  - `stage` (1-6),
  - existence proof method (`local_search`/`declaration_file`),
  - source module,
  - why selected (type match / graph neighbor / domain match / bridge).
