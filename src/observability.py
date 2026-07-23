"""Observabilidade local para a POC.

Os logs sao intencionalmente simples e evitam gravar texto livre do usuario.
Isso demonstra rastreabilidade sem estimular armazenamento desnecessario de dados.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def append_execution_log(payload: dict[str, Any], log_dir: str = "logs") -> Path:
    """Append de um registro JSONL de execucao e retorna o caminho do arquivo."""

    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    log_path = target_dir / "executions.jsonl"

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    return log_path
