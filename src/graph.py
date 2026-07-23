"""Fluxo de LangGraph para a POC."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypedDict

from src.llm import call_llm
from src.observability import append_execution_log
from src.rag import buscar_contexto, retrieve_context
from src.settings import get_settings
from src.tools import classify_risk, get_customer_transaction_summary


class AgentState(TypedDict, total=False):
    user_question: str
    customer_id: str
    intent: str | None
    context: str | None
    transaction_summary: dict[str, Any] | None
    risk_level: str | None
    evidence_sufficient: bool | None
    human_review_required: bool | None
    review_reason: str | None
    final_answer: str | None


INTENT_LABELS = (
    "contestacao",
    "consulta_operacional",
    "risco",
    "cadastro",
    "outro",
)


def _intent_from_text(text: str) -> str:
    normalized = text.lower()
    keyword_map = {
        "contestacao": ["contest", "chargeback", "transacao", "transação", "fraude"],
        "consulta_operacional": [
            "procedimento",
            "orientacao",
            "orientação",
            "como faço",
            "como faco",
        ],
        "risco": ["risco", "fraude", "suspeit", "alto impacto"],
        "cadastro": ["cadastro", "atualizar", "alterar", "endereco", "endereço"],
    }
    for label, keywords in keyword_map.items():
        if any(keyword in normalized for keyword in keywords):
            return label
    return "outro"


def _llm_or_fallback_classification(question: str) -> str:
    # Tentar o LLM primeiro, mas cair para heurísticas determinísticas por palavra-chave.
    prompt = f"""
Você é um classificador de intenção para uma operação bancária.

Escolha apenas uma das categorias abaixo:
- contestacao
- consulta_operacional
- risco
- cadastro
- outro

Regras:
- Responda somente com uma categoria.
- Não explique a resposta.
- Não use pontuação.

Solicitação:
{question}
"""
    result = call_llm(prompt, max_tokens=20, temperature=0.0).strip().lower()
    return result if result in INTENT_LABELS else _intent_from_text(question)


def _extract_evidence_sufficiency(context: str | None) -> bool:
    if not context:
        return False
    return not context.startswith("[ERRO_RAG]") and len(context.strip()) > 30


def classify_intent_node(state: AgentState) -> AgentState:
    # Primeiro passo: entender o que a pessoa está pedindo.
    state["intent"] = _llm_or_fallback_classification(state["user_question"])
    return state


def retrieve_context_node(state: AgentState) -> AgentState:
    # Segundo passo: trazer evidências da taxonomia de políticas.
    state["context"] = retrieve_context(state["user_question"])
    state["evidence_sufficient"] = _extract_evidence_sufficiency(state["context"])
    return state


def data_tool_node(state: AgentState) -> AgentState:
    # Terceiro passo: buscar os dados operacionais simulados.
    customer_id = state.get("customer_id", "123")
    state["transaction_summary"] = get_customer_transaction_summary(customer_id)
    return state


def risk_node(state: AgentState) -> AgentState:
    # Quarto passo: classificar o risco operacional e decidir se precisa de revisão humana.
    summary = state.get("transaction_summary") or {}
    risk_level = classify_risk(summary)
    state["risk_level"] = risk_level
    state["human_review_required"] = bool(
        risk_level == "alto" or not state.get("evidence_sufficient")
    )

    reasons: list[str] = []
    if risk_level == "alto":
        reasons.append("risco operacional classificado como alto")
    if not state.get("evidence_sufficient"):
        reasons.append("evidência insuficiente recuperada dos documentos de política")
    state["review_reason"] = "; ".join(reasons) if reasons else None
    return state


def human_review_node(state: AgentState) -> AgentState:
    # Quando o risco é alto ou a evidência é fraca, o fluxo passa por aqui antes da resposta final.
    if state.get("review_reason"):
        note = f"Revisão humana necessária: {state['review_reason']}."
    else:
        note = "Revisão humana necessária."
    state["final_answer"] = note
    return state


def _build_local_answer(state: AgentState) -> str:
    summary = state.get("transaction_summary") or {}
    review_flag = "sim" if state.get("human_review_required") else "não"
    return (
        "## Resultado da análise\n\n"
        f"- Intenção: {state.get('intent')}\n"
        f"- Risco: {state.get('risk_level')}\n"
        f"- Revisão humana: {review_flag}\n\n"
        "## Evidências consultadas\n"
        f"{state.get('context') or 'Sem contexto recuperado.'}\n\n"
        "## Resumo transacional\n"
        f"{summary}\n"
    )


def final_answer_node(state: AgentState) -> AgentState:
    # Gerar a resposta final somente depois que evidências e risco estiverem reunidos.
    prompt = f"""
Você é um assistente operacional bancário.

Contexto do trabalho:
- Você recebe solicitações operacionais de um analista.
- Você deve ser objetivo, auditável e conservador.
- Você nunca deve inventar fatos.

Regras obrigatórias:
- Use apenas o contexto e o resumo transacional.
- Se faltar evidência, recomende revisão humana.
- Se o risco for alto, recomende revisão humana.
- Se houver incerteza, diga isso claramente.
- Responda em português do Brasil.

Solicitação:
{state['user_question']}

Intenção classificada:
{state.get('intent')}

Contexto recuperado:
{state.get('context')}

Resumo transacional:
{state.get('transaction_summary')}

Risco:
{state.get('risk_level')}

Revisão humana obrigatória:
{state.get('human_review_required')}

Responda com exatamente estas seções:
1. Entendimento da solicitação
2. Evidências consultadas
3. Avaliação de risco
4. Recomendação operacional
5. Necessidade de revisão humana
6. Limitações da análise
"""
    llm_answer = call_llm(prompt, max_tokens=700, temperature=0.2)
    if llm_answer.startswith("[ERRO_LLM]"):
        state["final_answer"] = _build_local_answer(state)
    else:
        state["final_answer"] = llm_answer
    return state


class SimpleGraph:
    def __init__(self, runner: Callable[[AgentState], AgentState]):
        self._runner = runner

    def invoke(self, state: AgentState) -> AgentState:
        # Fallback mínimo quando o langgraph não está instalado.
        return self._runner(state)


def _run_pipeline(state: AgentState) -> AgentState:
    # A execução alternativa espelha a ordem do grafo em um pipeline linear Python.
    state = classify_intent_node(state)
    state = retrieve_context_node(state)
    state = data_tool_node(state)
    state = risk_node(state)
    if state.get("human_review_required"):
        state = human_review_node(state)
    else:
        state = final_answer_node(state)
    return state


def build_graph():
    """Construir o grafo do fluxo, com plano de contingência para pipeline local quando necessário."""
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        # Manter o projeto executável em ambientes sem langgraph.
        return SimpleGraph(_run_pipeline)

    workflow = StateGraph(AgentState)

    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("data_tool", data_tool_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("final_answer", final_answer_node)

    workflow.set_entry_point("classify_intent")
    workflow.add_edge("classify_intent", "retrieve_context")
    workflow.add_edge("retrieve_context", "data_tool")
    workflow.add_edge("data_tool", "risk")

    def route_after_risk(state: AgentState) -> str:
        # Roteia para revisão humana quando o risco é alto ou a evidência é fraca.
        return "human_review" if state.get("human_review_required") else "final_answer"

    workflow.add_conditional_edges(
        "risk",
        route_after_risk,
        {
            "human_review": "human_review",
            "final_answer": "final_answer",
        },
    )
    workflow.add_edge("human_review", "final_answer")
    workflow.add_edge("final_answer", END)

    return workflow.compile()


def executar_fluxo(pergunta: str, cliente_id: str | None = None) -> dict[str, Any]:
    """Executa o grafo e adapta o resultado para a interface Streamlit."""

    settings = get_settings()
    customer_id = cliente_id or settings.default_customer_id
    graph = build_graph()
    result = graph.invoke(
        {
            "user_question": pergunta,
            "customer_id": customer_id,
        }
    )

    evidencias = buscar_contexto(pergunta, base_dir=settings.data_dir, limite=3)
    risco = result.get("risk_level") or "desconhecido"
    revisao_humana = bool(result.get("human_review_required"))
    final_answer = result.get("final_answer") or "Fluxo executado sem resposta final."

    etapas = [
        "classify_intent",
        "retrieve_context",
        "data_tool",
        "risk",
        "human_review" if revisao_humana else "final_answer",
    ]

    resposta = {
        "resumo": f"Analise concluida para o cliente {customer_id}.",
        "resumo_executivo": final_answer,
        "texto_completo": final_answer,
        "recomendacao": (
            "Encaminhar para revisao humana e anexar as evidencias recuperadas."
            if revisao_humana
            else "Seguir o procedimento operacional com base nas evidencias consultadas."
        ),
        "alerta": (
            "Caso exige revisao humana antes de qualquer acao operacional ou financeira."
            if revisao_humana
            else None
        ),
        "risco": {
            "nivel": risco,
            "motivos": result.get("review_reason"),
        },
        "revisao_humana": revisao_humana,
        "origem_llm": (
            "fallback_local"
            if final_answer.startswith("## Resultado") or final_answer.startswith("Revis")
            else "bedrock"
        ),
        "evidencias": [
            {
                "titulo": evidencia.titulo,
                "trecho": evidencia.trecho,
                "caminho": evidencia.caminho,
            }
            for evidencia in evidencias
        ],
        "etapas": etapas,
        "estado": result,
    }

    if settings.enable_local_logs:
        append_execution_log(
            {
                "customer_id": customer_id,
                "question_length": len(pergunta),
                "intent": result.get("intent"),
                "risk_level": risco,
                "human_review_required": revisao_humana,
                "evidence_count": len(evidencias),
                "sources": [evidencia.caminho for evidencia in evidencias],
                "llm_source": resposta["origem_llm"],
            },
            log_dir=settings.log_dir,
        )

    return resposta
