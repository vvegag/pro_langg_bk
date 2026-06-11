"""LangGraph workflow for the POC."""

from __future__ import annotations

from typing import Any, Dict, Optional, TypedDict

from langgraph.graph import END, StateGraph

from src.llm import get_llm
from src.rag import load_retriever
from src.tools import get_tools


class AgentState(TypedDict, total=False):
    user_question: str
    customer_id: str
    intent: Optional[str]
    context: Optional[str]
    transaction_summary: Optional[Dict[str, Any]]
    risk_level: Optional[str]
    human_review_required: Optional[bool]
    final_answer: Optional[str]


def classify_intent_node(state: AgentState) -> AgentState:
    state["intent"] = "pending"
    return state


def retrieve_context_node(state: AgentState) -> AgentState:
    documents = load_retriever()
    state["context"] = ", ".join(path.as_posix() for path in documents)
    return state


def data_tool_node(state: AgentState) -> AgentState:
    tools = get_tools()
    state["transaction_summary"] = {"tools_loaded": len(tools)}
    return state


def risk_node(state: AgentState) -> AgentState:
    state["risk_level"] = "pendente"
    state["human_review_required"] = False
    return state


def final_answer_node(state: AgentState) -> AgentState:
    llm = get_llm()
    state["final_answer"] = f"LLM configurado: {llm is not None}"
    return state


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("data_tool", data_tool_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("final_answer", final_answer_node)

    workflow.set_entry_point("classify_intent")
    workflow.add_edge("classify_intent", "retrieve_context")
    workflow.add_edge("retrieve_context", "data_tool")
    workflow.add_edge("data_tool", "risk")
    workflow.add_edge("risk", "final_answer")
    workflow.add_edge("final_answer", END)

    return workflow.compile()
