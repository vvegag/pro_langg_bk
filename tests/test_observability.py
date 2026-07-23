"""Testes da camada local de observabilidade."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.observability import append_execution_log


class ObservabilityTests(unittest.TestCase):
    def test_append_execution_log_writes_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = append_execution_log(
                {
                    "customer_id": "555",
                    "risk_level": "alto",
                    "human_review_required": True,
                },
                log_dir=temp_dir,
            )

            self.assertEqual(log_path, Path(temp_dir) / "executions.jsonl")
            rows = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(rows), 1)

            payload = json.loads(rows[0])
            self.assertEqual(payload["customer_id"], "555")
            self.assertEqual(payload["risk_level"], "alto")
            self.assertTrue(payload["human_review_required"])
            self.assertIn("timestamp_utc", payload)
