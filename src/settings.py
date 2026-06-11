"""Application settings helpers."""

from __future__ import annotations

from dotenv import load_dotenv


def load_settings() -> None:
    load_dotenv()
