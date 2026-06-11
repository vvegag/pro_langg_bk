"""RAG helpers."""

from __future__ import annotations

from pathlib import Path


def list_documents(data_dir: str = "data") -> list[Path]:
    base_path = Path(data_dir)
    return sorted(
        [path for path in base_path.rglob("*.txt") if path.is_file()]
    )


def load_retriever():
    return list_documents()
