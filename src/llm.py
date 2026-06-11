"""Utilitários de LLM."""

from __future__ import annotations

import json
from typing import Any

from src.settings import get_settings


def _build_anthropic_body(prompt: str, max_tokens: int, temperature: float) -> dict[str, Any]:
    return {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }


def call_llm(prompt: str, max_tokens: int = 900, temperature: float = 0.2) -> str:
    """Chamar o modelo de chat configurado no Bedrock e retornar texto puro."""
    settings = get_settings()

    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError
    except ImportError as exc:  # pragma: no cover - contingência opcional
        # Manter a POC executável mesmo quando as dependências da AWS ainda não estiverem instaladas.
        return (
            "[ERRO_LLM] boto3 não está disponível neste ambiente. "
            f"Detalhe: {exc}"
        )

    body = _build_anthropic_body(prompt, max_tokens, temperature)

    try:
        # O Bedrock é chamado aqui para manter o restante da aplicação independente do provedor.
        client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
        response = client.invoke_model(
            modelId=settings.bedrock_chat_model_id,
            body=json.dumps(body),
        )
        payload = json.loads(response["body"].read())
        return payload["content"][0]["text"]
    except (BotoCoreError, ClientError, KeyError, json.JSONDecodeError, TypeError, ValueError) as exc:
        # Expor a falha de forma clara para permitir um plano de contingência local no grafo.
        return (
            "[ERRO_LLM] Não foi possível chamar o modelo no Bedrock. "
            f"Detalhe: {exc}"
        )
