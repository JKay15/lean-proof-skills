#!/usr/bin/env python3
"""Validate mandatory contract clauses in skillpack documents.

This script enforces that core workflow skills keep required guarantees from
MLTheory feedback specs (domain-profile retrieval order, two-phase intake, and
planner/builder handoff constraints).
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def require_contains(text: str, needle: str, *, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing required clause `{needle}`")


def require_in_order(text: str, needles: list[str], *, label: str, errors: list[str]) -> None:
    pos = 0
    for needle in needles:
        idx = text.find(needle, pos)
        if idx < 0:
            errors.append(f"{label}: missing ordered clause `{needle}`")
            return
        pos = idx + len(needle)


def validate_retrieval_skill(errors: list[str]) -> None:
    path = ROOT / ".agents" / "skills" / "mltheory-retrieval" / "SKILL.md"
    text = load(path)
    label = str(path.relative_to(ROOT))

    require_contains(text, "## Domain Sources (MUST)", label=label, errors=errors)
    require_contains(text, "tools/retrieval/query.py", label=label, errors=errors)
    for field in (
        "allowed_local_roots",
        "module_roots",
        "default_imports",
        "mathlib_slice_roots",
        "bridge_modules",
        "adjacent_domains",
    ):
        require_contains(text, field, label=label, errors=errors)

    require_in_order(
        text,
        [
            "1. Domain-local MLTheory first",
            "2. Domain mathlib slice second",
            "3. Adjacent-domain widening third",
            "4. Full MLTheory fourth",
            "5. Full mathlib fifth",
            "6. External semantic retrieval last",
        ],
        label=label,
        errors=errors,
    )
    require_contains(text, "## Existence Verification (MUST at every stage)", label=label, errors=errors)
    require_contains(text, "No unverified symbol may appear in output.", label=label, errors=errors)


def validate_workflow_skill(errors: list[str]) -> None:
    path = ROOT / ".agents" / "skills" / "ml-paper-workflow" / "SKILL.md"
    text = load(path)
    label = str(path.relative_to(ROOT))

    require_contains(text, "## Intake v2 Two-Phase Contract (MUST for new problems)", label=label, errors=errors)
    require_contains(text, "Research Pack phase", label=label, errors=errors)
    require_contains(text, "Lean Commit phase", label=label, errors=errors)
    require_contains(text, "Spec.lean", label=label, errors=errors)
    require_contains(text, "Cache.lean", label=label, errors=errors)
    require_contains(text, "Sketch.lean", label=label, errors=errors)
    require_contains(text, "Tasks.yaml", label=label, errors=errors)
    require_contains(text, "Problems/<Suite>/<ProblemName>/", label=label, errors=errors)
    require_contains(text, "ProofMap.json", label=label, errors=errors)
    require_contains(text, "tools/intake/sync_problem_workspace.py", label=label, errors=errors)
    require_contains(text, "tools/index/gen_proof_map.py", label=label, errors=errors)
    require_contains(text, "tools/ci/check_problem_workspace_contract.py", label=label, errors=errors)

    require_contains(text, "## Planner-Builder Batch Replan (MUST for stuck cards)", label=label, errors=errors)
    require_contains(text, "split_into", label=label, errors=errors)
    require_contains(text, "bridge lemmas", label=label, errors=errors)

    for gate in (
        "lake build",
        "lake env lean Eval/ImportSmoke.lean",
        "lake env lean Eval/CanonicalAPISmoke.lean",
        "tools/ci/check_no_sorry_axiom.sh",
        "tools/ci/check_placeholder_policy.sh",
    ):
        require_contains(text, gate, label=label, errors=errors)
    require_contains(text, "tools/retrieval/query.py", label=label, errors=errors)


def main() -> int:
    errors: list[str] = []
    try:
        validate_retrieval_skill(errors)
        validate_workflow_skill(errors)
    except FileNotFoundError as err:
        errors.append(str(err))

    if errors:
        print("[validate_skill_contracts] failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("[validate_skill_contracts] passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
