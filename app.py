"""Interface Streamlit da POC 2.

Este arquivo reúne a experiência do usuário, exibe a resposta do fluxo e
mantém a aplicação fácil de executar localmente.
"""

from __future__ import annotations

import streamlit as st

from src.graph import executar_fluxo
from src.settings import carregar_configuracao

config = carregar_configuracao()

st.set_page_config(
    page_title=config.nome_aplicacao,
    page_icon="🏦",
    layout="wide",
)

st.title("Bank GenAI Operations Assistant AWS")
st.caption("Solução local para demonstrar um fluxo operacional com GenAI e nuvem.")

cenarios = {
    "Risco baixo": {
        "cliente_id": "111",
        "pergunta": (
            "Cliente 111 solicita orientação sobre uma atualização cadastral sem impacto financeiro. "
            "Existe indício de risco? Qual procedimento o analista deve seguir?"
        ),
    },
    "Risco médio": {
        "cliente_id": "222",
        "pergunta": (
            "Cliente 222 contesta uma transação de valor moderado realizada no app. "
            "Existe indício de risco? Qual procedimento o analista deve seguir?"
        ),
    },
    "Risco alto": {
        "cliente_id": "555",
        "pergunta": (
            "Cliente 555 contesta uma transação de R$ 12.500 realizada no app com suspeita de fraude. "
            "Existe indício de risco? Qual procedimento o analista deve seguir?"
        ),
    },
}

coluna_entrada, coluna_saida = st.columns([1, 1])

with coluna_entrada:
    st.subheader("Solicitação operacional")
    cenario_escolhido = st.selectbox(
        "Escolha o cenário de demonstração",
        list(cenarios.keys()),
        index=2,
    )

    pergunta_padrao = cenarios[cenario_escolhido]["pergunta"]
    cliente_padrao = cenarios[cenario_escolhido]["cliente_id"]

    pergunta = st.text_area(
        "Descreva o caso operacional",
        value=pergunta_padrao,
        height=180,
    )

    cliente_id = st.text_input("ID do cliente", value=cliente_padrao)
    enviar = st.button("Executar análise")

with coluna_saida:
    st.subheader("Resultado da análise")
    if enviar:
        resultado = executar_fluxo(pergunta, cliente_id=cliente_id)
        risco = resultado.get("risco", {})

        st.write(resultado["resumo"])
        col1, col2, col3 = st.columns(3)
        col1.metric("Nível de risco", risco.get("nivel", "desconhecido").title())
        col2.metric("Revisão humana", "Sim" if resultado.get("revisao_humana") else "Não")
        col3.metric("Fonte da resposta", resultado.get("origem_llm", "fallback_local"))

        if resultado.get("alerta"):
            st.warning(resultado["alerta"])

        tab_resposta, tab_evidencias, tab_auditoria = st.tabs(
            ["Resposta", "Evidências", "Auditoria"]
        )

        with tab_resposta:
            st.markdown("### Resumo executivo")
            st.write(
                resultado.get("resumo_executivo")
                or resultado.get("texto_completo")
                or resultado["resumo"]
            )

            st.markdown("### Recomendação")
            st.write(resultado.get("recomendacao", "Sem recomendação adicional."))

            st.caption("Nenhuma ação operacional ou financeira é executada automaticamente.")

        with tab_evidencias:
            if resultado.get("evidencias"):
                for item in resultado["evidencias"]:
                    st.write(f"- {item['titulo']}: {item['trecho']}")
            else:
                st.info("Nenhuma evidência documental foi recuperada.")

        with tab_auditoria:
            st.markdown("### Etapas do fluxo")
            for etapa in resultado.get("etapas", []):
                st.write(f"- {etapa}")

            st.markdown("### Governança")
            st.write("- Dados utilizados são fictícios.")
            st.write("- Casos de alto risco exigem human-in-the-loop.")
            st.write("- Logs locais minimizam texto livre do usuário.")

            with st.expander("Ver JSON completo"):
                st.json(resultado)
    else:
        st.info("Execute a análise para ver o fluxo completo e as evidências recuperadas.")

st.divider()
st.caption("Documentação, risco, RAG e resposta final aparecem de forma rastreável no fluxo.")
