"""Ponto de entrada do Streamlit para a POC."""

from __future__ import annotations

import streamlit as st

from src.graph import build_graph
from src.settings import get_settings


def _render_result_panel(result: dict) -> None:
    col1, col2, col3 = st.columns(3)

    col1.metric("Intenção", result.get("intent") or "N/D")
    col2.metric("Risco", result.get("risk_level") or "N/D")
    col3.metric(
        "Revisão humana",
        "Sim" if result.get("human_review_required") else "Não",
    )

    if result.get("review_reason"):
        st.warning(result["review_reason"])

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Resumo transacional")
        st.json(result.get("transaction_summary") or {})

    with right:
        st.subheader("Contexto recuperado")
        st.text(result.get("context") or "Sem contexto recuperado.")

    with st.expander("Resposta completa"):
        st.write(result.get("final_answer") or "Sem resposta gerada.")


def main() -> None:
    settings = get_settings()
    st.set_page_config(page_title="Bank GenAI Operations Assistant", layout="wide")
    st.title("Bank GenAI Operations Assistant")
    st.caption("Assistente operacional com LangGraph, RAG, Bedrock e revisão humana.")

    with st.sidebar:
        # Manter os controles de entrada juntos facilita refazer a análise rapidamente.
        st.header("Configuração")
        customer_id = st.selectbox(
            "Cliente simulado",
            options=["123", "456", "999"],
            index=0,
        )
        question = st.text_area(
            "Solicitação operacional",
            value=(
                "Cliente 123 contesta uma transação de valor elevado feita pelo app. "
    "Existe indício de risco? Qual procedimento o analista deve seguir?"
            ),
            height=140,
        )
        run_analysis = st.button("Executar análise", use_container_width=True)
        st.caption(f"Região AWS: {settings.aws_region}")

    if not run_analysis:
        # A aplicação fica em espera até a pessoa iniciar a análise.
        st.info("Preencha a solicitação e clique em Executar análise.")
        return

    # O grafo concentra o fluxo de negócio; a interface só envia entradas e mostra resultados.
    graph = build_graph()
    initial_state = {
        "user_question": question,
        "customer_id": customer_id,
    }

    with st.spinner("Executando o fluxo..."):
        result = graph.invoke(initial_state)

    _render_result_panel(result)


if __name__ == "__main__":
    main()
