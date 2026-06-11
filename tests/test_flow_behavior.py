"""Testes de comportamento do fluxo da POC 1."""

from __future__ import annotations

import unittest

from src.graph import build_graph


class FlowBehaviorTests(unittest.TestCase):
    def test_high_risk_triggers_human_review(self) -> None:
        graph = build_graph()
        result = graph.invoke(
            {
                "user_question": "Cliente 123 contesta uma transação acima de R$ 10.000.",
                "customer_id": "123",
            }
        )
        self.assertEqual(result["risk_level"], "alto")
        self.assertTrue(result["human_review_required"])
        self.assertIn("Revisão humana", result["final_answer"])

    def test_low_risk_can_produce_final_answer(self) -> None:
        graph = build_graph()
        result = graph.invoke(
            {
                "user_question": "Cliente 456 quer orientação sobre um procedimento simples.",
                "customer_id": "456",
            }
        )
        self.assertIn(result["risk_level"], {"baixo", "medio"})
        self.assertIn("final_answer", result)
        self.assertTrue(result["final_answer"])


if __name__ == "__main__":
    unittest.main()
