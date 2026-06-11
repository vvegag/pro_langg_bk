"""Utilitários de configuração da aplicação."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - contingência opcional
    def load_dotenv() -> None:  # type: ignore[no-redef]
        return None


@dataclass(frozen=True)
class Settings:
    aws_region: str = "us-east-1"
    bedrock_chat_model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"
    bedrock_embed_model_id: str = "amazon.titan-embed-text-v2:0"
    streamlit_server_port: int = 8501
    data_dir: str = "data"
    default_customer_id: str = "123"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Carregar as variáveis de ambiente e retornar as configurações do projeto."""
    # Carregar o `.env` quando existir, mas manter o projeto utilizável sem ele.
    load_dotenv()
    return Settings(
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        bedrock_chat_model_id=os.getenv(
            "BEDROCK_CHAT_MODEL_ID",
            "anthropic.claude-3-haiku-20240307-v1:0",
        ),
        bedrock_embed_model_id=os.getenv(
            "BEDROCK_EMBED_MODEL_ID",
            "amazon.titan-embed-text-v2:0",
        ),
        streamlit_server_port=int(os.getenv("STREAMLIT_SERVER_PORT", "8501")),
        data_dir=os.getenv("DATA_DIR", "data"),
        default_customer_id=os.getenv("DEFAULT_CUSTOMER_ID", "123"),
    )
