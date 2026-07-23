"""Avaliacao deterministica dos comportamentos centrais da POC."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.graph import executar_fluxo


def _load_cases(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    result = executar_fluxo(case["question"], cliente_id=case["customer_id"])
    actual_risk = result["risco"]["nivel"]
    actual_review = bool(result["revisao_humana"])
    return {
        "id": case["id"],
        "expected_risk": case["expected_risk"],
        "actual_risk": actual_risk,
        "risk_ok": actual_risk == case["expected_risk"],
        "expected_human_review": case["expected_human_review"],
        "actual_human_review": actual_review,
        "human_review_ok": actual_review == case["expected_human_review"],
        "evidence_count": len(result.get("evidencias", [])),
    }


def main() -> int:
    cases = _load_cases(Path("evals/casos_teste.jsonl"))
    rows = [_evaluate_case(case) for case in cases]
    total_checks = len(rows) * 2
    passed_checks = sum(1 for row in rows if row["risk_ok"]) + sum(
        1 for row in rows if row["human_review_ok"]
    )

    print("id,risk_ok,human_review_ok,evidence_count")
    for row in rows:
        print(f"{row['id']},{row['risk_ok']},{row['human_review_ok']},{row['evidence_count']}")
    print(f"score,{passed_checks}/{total_checks}")

    return 0 if passed_checks == total_checks else 1


if __name__ == "__main__":
    raise SystemExit(main())
