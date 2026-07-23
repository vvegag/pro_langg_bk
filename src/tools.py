"""Utilitários de ferramentas usados pelo grafo."""

from __future__ import annotations

from typing import Any


def get_customer_transaction_summary(customer_id: str) -> dict[str, Any]:
    """Retornar um resumo simulado e determinístico do cliente e da transação."""
    # Esses mocks mantêm a POC autocontida e segura para execução local.
    fake_database: dict[str, dict[str, Any]] = {
        "123": {
            "cliente_id": "123",
            "nome_cliente": "Cliente Simulado A",
            "transacoes_ultimos_30_dias": 18,
            "valor_total": 12500.00,
            "atividade_suspeita": True,
            "canal_principal": "mobile",
            "valor_ultima_transacao": 10800.00,
            "produto": "credit_card",
            "caso_em_aberto": True,
        },
        "456": {
            "cliente_id": "456",
            "nome_cliente": "Cliente Simulado B",
            "transacoes_ultimos_30_dias": 4,
            "valor_total": 850.00,
            "atividade_suspeita": False,
            "canal_principal": "branch",
            "valor_ultima_transacao": 120.00,
            "produto": "checking_account",
            "caso_em_aberto": False,
        },
        "111": {
            "cliente_id": "111",
            "nome_cliente": "Cliente Simulado Baixo Risco",
            "transacoes_ultimos_30_dias": 2,
            "valor_total": 180.00,
            "atividade_suspeita": False,
            "canal_principal": "branch",
            "valor_ultima_transacao": 80.00,
            "produto": "checking_account",
            "caso_em_aberto": False,
        },
        "222": {
            "cliente_id": "222",
            "nome_cliente": "Cliente Simulado Medio Risco",
            "transacoes_ultimos_30_dias": 7,
            "valor_total": 3200.00,
            "atividade_suspeita": False,
            "canal_principal": "mobile",
            "valor_ultima_transacao": 1800.00,
            "produto": "credit_card",
            "caso_em_aberto": False,
        },
        "555": {
            "cliente_id": "555",
            "nome_cliente": "Cliente Simulado Alto Risco",
            "transacoes_ultimos_30_dias": 18,
            "valor_total": 12500.00,
            "atividade_suspeita": True,
            "canal_principal": "mobile",
            "valor_ultima_transacao": 12500.00,
            "produto": "credit_card",
            "caso_em_aberto": True,
        },
    }

    return fake_database.get(
        customer_id,
        {
            "cliente_id": customer_id,
            "nome_cliente": "Desconhecido",
            "transacoes_ultimos_30_dias": 0,
            "valor_total": 0.0,
            "atividade_suspeita": None,
            "canal_principal": "desconhecido",
            "valor_ultima_transacao": 0.0,
            "produto": "desconhecido",
            "caso_em_aberto": False,
        },
    )


def classify_risk(transaction_summary: dict[str, Any]) -> str:
    # Os limiares de risco são explícitos para facilitar a explicação na entrevista.
    amount = float(transaction_summary.get("valor_total", 0.0) or 0.0)
    last_value = float(transaction_summary.get("valor_ultima_transacao", 0.0) or 0.0)
    suspicious = transaction_summary.get("atividade_suspeita")
    has_open_case = bool(transaction_summary.get("caso_em_aberto"))

    if suspicious is True or amount > 10000 or last_value > 10000 or has_open_case:
        return "alto"
    if amount > 1000 or last_value > 1000:
        return "medio"
    return "baixo"


def get_tools() -> list[dict[str, str]]:
    return [
        {
            "name": "get_customer_transaction_summary",
            "description": "Retornar um resumo simulado do cliente e da transação.",
        },
        {
            "name": "classify_risk",
            "description": "Classificar o risco operacional a partir do resumo da transação.",
        },
    ]
