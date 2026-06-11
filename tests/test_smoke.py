"""Verificações leves de sanidade para o projeto da POC 1."""

from __future__ import annotations

import unittest

from src.graph import build_graph
from src.rag import load_documents
from src.tools import classify_risk, get_customer_transaction_summary


class SmokeTests(unittest.TestCase):
    def test_documents_exist(self) -> None:
        documents = load_documents()
        self.assertGreaterEqual(len(documents), 3)

    def test_risk_rules(self) -> None:
        high = classify_risk(get_customer_transaction_summary("123"))
        medium_or_low = classify_risk(get_customer_transaction_summary("456"))
        self.assertEqual(high, "alto")
        self.assertIn(medium_or_low, {"baixo", "medio"})

    def test_graph_invokes(self) -> None:
        graph = build_graph()
        result = graph.invoke(
            {
                "user_question": "Cliente 123 contesta uma transação acima de R$ 10.000.",
                "customer_id": "123",
            }
        )
        self.assertIn("intent", result)
        self.assertIn("risk_level", result)
        self.assertIn("final_answer", result)


if __name__ == "__main__":
    unittest.main()
