"""Streamlit entrypoint for the POC."""

from __future__ import annotations

import streamlit as st

from src.graph import build_graph


def main() -> None:
    st.set_page_config(page_title="POC Itaú GenAI", layout="wide")
    st.title("POC Itaú GenAI")

    graph = build_graph()
    st.write("Aplicacao base pronta para evoluir com LangGraph, RAG e AWS.")
    st.caption(f"Graph carregado: {graph is not None}")


if __name__ == "__main__":
    main()
