"""Busca simples de contexto documental.

O objetivo aqui é manter uma base leve e clara para a POC 2. Mais tarde,
esta camada pode ser trocada por Knowledge Bases, OpenSearch ou outro índice
vetorial gerenciado.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class EvidenciaDocumento:
    caminho: str
    titulo: str
    trecho: str
    pontuacao: int


def _ler_arquivos_texto(base_dir: str) -> list[tuple[str, str]]:
    raiz = Path(base_dir) / "politicas"
    arquivos: list[tuple[str, str]] = []

    if not raiz.exists():
        return arquivos

    for caminho in sorted(raiz.rglob("*.txt")):
        arquivos.append((str(caminho), caminho.read_text(encoding="utf-8")))

    return arquivos


def _titulo_legivel(caminho: str) -> str:
    path = Path(caminho)
    pasta = path.parent.name.replace("_", " ").title()
    nome = path.stem.replace("_", " ").title()
    if pasta and pasta != "Politicas":
        return f"{pasta} / {nome}"
    return nome


def _palavras_chave(pergunta: str) -> set[str]:
    return {
        palavra.strip(".,!?;:()[]{}").lower()
        for palavra in pergunta.split()
        if len(palavra.strip(".,!?;:()[]{}")) > 3
    }


def buscar_contexto(pergunta: str, base_dir: str, limite: int = 3) -> list[EvidenciaDocumento]:
    """Executa uma recuperação lexical simples para apoiar a resposta."""

    palavras_chave = _palavras_chave(pergunta)
    candidatos: list[EvidenciaDocumento] = []

    for caminho, conteudo in _ler_arquivos_texto(base_dir):
        titulo = _titulo_legivel(caminho)
        for trecho in conteudo.splitlines():
            trecho_limpo = trecho.strip()
            if not trecho_limpo:
                continue

            texto_normalizado = trecho_limpo.lower()
            pontuacao = sum(1 for palavra in palavras_chave if palavra in texto_normalizado)
            if titulo.lower().split(" / ")[0] in texto_normalizado:
                pontuacao += 1

            if pontuacao:
                candidatos.append(
                    EvidenciaDocumento(
                        caminho=caminho,
                        titulo=titulo,
                        trecho=trecho_limpo,
                        pontuacao=pontuacao,
                    )
                )

    candidatos.sort(key=lambda item: item.pontuacao, reverse=True)
    return candidatos[:limite]


def formatar_evidencias(evidencias: Iterable[EvidenciaDocumento]) -> str:
    """Formata as evidências para uso no prompt e na interface."""

    linhas = []
    for item in evidencias:
        linhas.append(f"- {item.titulo}: {item.trecho}")
    return "\n".join(linhas)


def load_documents(base_dir: str = "data") -> list[EvidenciaDocumento]:
    """Retorna uma evidencia por documento para testes e smoke checks."""

    evidencias: list[EvidenciaDocumento] = []
    for caminho, conteudo in _ler_arquivos_texto(base_dir):
        linhas = [linha.strip() for linha in conteudo.splitlines() if linha.strip()]
        if not linhas:
            continue
        evidencias.append(
            EvidenciaDocumento(
                caminho=caminho,
                titulo=_titulo_legivel(caminho),
                trecho=" ".join(linhas),
                pontuacao=1,
            )
        )
    return evidencias


def retrieve_context(question: str, base_dir: str = "data", k: int = 3) -> str:
    """Busca contexto documental e retorna texto formatado para o grafo."""

    evidencias = buscar_contexto(question, base_dir=base_dir, limite=k)
    if not evidencias:
        return "[ERRO_RAG] Nenhuma evidencia documental relevante foi encontrada."
    return formatar_evidencias(evidencias)
