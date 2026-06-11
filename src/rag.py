"""Utilitários de RAG."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.settings import get_settings


@dataclass(frozen=True)
class PolicyDocument:
    page_content: str
    metadata: dict[str, str]


def load_documents(data_dir: str | None = None) -> list[PolicyDocument]:
    """Carregar documentos de texto da taxonomia de políticas."""
    settings = get_settings()
    base_path = Path(data_dir or settings.data_dir)
    documents: list[PolicyDocument] = []

    # A taxonomia é recursiva de propósito para permitir novas pastas de políticas no futuro.
    for file_path in sorted(base_path.rglob("*.txt")):
        if not file_path.is_file():
            continue
        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        documents.append(
            PolicyDocument(
                page_content=text,
                metadata={"source": file_path.as_posix()},
            )
        )

    return documents


def _chunk_text(text: str, chunk_size: int = 700, chunk_overlap: int = 100) -> list[str]:
    # Manter os blocos pequenos facilita a recuperação sem perder contexto entre eles.
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(0, end - chunk_overlap)
    return chunks


def _split_documents(documents: Iterable[PolicyDocument]) -> list[PolicyDocument]:
    chunks: list[PolicyDocument] = []
    for document in documents:
        for index, chunk in enumerate(_chunk_text(document.page_content)):
            source = document.metadata.get("source", "unknown")
            chunks.append(
                PolicyDocument(
                    page_content=chunk,
                    metadata={"source": source, "chunk": str(index)},
                )
            )
    return chunks


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if len(token) > 2}


def _lexical_rank(question: str, documents: list[PolicyDocument], k: int) -> list[PolicyDocument]:
    question_tokens = _tokenize(question)

    def score(document: PolicyDocument) -> tuple[int, int]:
        doc_tokens = _tokenize(document.page_content)
        overlap = len(question_tokens & doc_tokens)
        return (overlap, len(document.page_content))

    ranked = sorted(documents, key=score, reverse=True)
    return ranked[:k]


def _build_vectorstore(chunks: list[PolicyDocument]):
    try:
        import boto3
        from langchain.schema import Document
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_aws import BedrockEmbeddings
        from langchain_community.vectorstores import FAISS
    except ImportError:
        return None

    settings = get_settings()
    try:
        # Usar embeddings do Bedrock quando a pilha de dependências estiver disponível.
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
        langchain_docs = [
            Document(page_content=doc.page_content, metadata=doc.metadata) for doc in chunks
        ]
        split_docs = splitter.split_documents(langchain_docs)
        client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
        embeddings = BedrockEmbeddings(
            client=client,
            model_id=settings.bedrock_embed_model_id,
        )
        return FAISS.from_documents(split_docs, embeddings)
    except Exception:
        return None


def retrieve_context(question: str, k: int = 3) -> str:
    """Retornar o contexto de política mais relevante para a pergunta."""
    documents = load_documents()
    if not documents:
        return "[ERRO_RAG] Nenhum documento de política encontrado em data/politicas/."

    chunks = _split_documents(documents)
    vectorstore = _build_vectorstore(chunks)

    if vectorstore is not None:
        try:
            docs = vectorstore.similarity_search(question, k=k)
            relevant = [
                PolicyDocument(
                    page_content=doc.page_content,
                    metadata={k: str(v) for k, v in doc.metadata.items()},
                )
                for doc in docs
            ]
        except Exception:
            # Se a busca vetorial falhar, cair para uma ordenação lexical simples.
            relevant = _lexical_rank(question, chunks, k)
    else:
        relevant = _lexical_rank(question, chunks, k)

    context_parts: list[str] = []
    for document in relevant:
        source = document.metadata.get("source", "unknown")
        chunk = document.metadata.get("chunk")
        heading = f"[Fonte: {source}]"
        if chunk is not None:
            heading = f"{heading} [Chunk: {chunk}]"
        context_parts.append(f"{heading}\n{document.page_content}")

    return "\n\n".join(context_parts)
