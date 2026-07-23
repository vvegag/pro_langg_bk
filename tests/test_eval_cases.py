"""Garante que os casos de avaliacao continuam no formato esperado."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


class EvalCasesTests(unittest.TestCase):
    def test_eval_cases_have_required_fields(self) -> None:
        path = Path("evals/casos_teste.jsonl")
        required = {
            "id",
            "customer_id",
            "question",
            "expected_risk",
            "expected_human_review",
        }

        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        self.assertGreaterEqual(len(rows), 3)
        for row in rows:
            self.assertTrue(required.issubset(row))
            self.assertIn(row["expected_risk"], {"baixo", "medio", "alto"})
