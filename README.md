# Bank GenAI Operations Assistant

POC local de um assistente operacional bancário com Streamlit, LangGraph, RAG, Amazon Bedrock, regras de risco e recomendação de revisão humana.

O objetivo é demonstrar uma arquitetura de GenAI controlada e explicável para entrevista técnica em ambiente bancário. A solução usa dados fictícios e não executa nenhuma ação financeira.

## O Que A POC Demonstra

- Interface Streamlit para entrada do caso operacional.
- Orquestração com LangGraph.
- Busca de evidências em documentos locais em `data/politicas/`.
- Consulta simulada de cliente e transação.
- Classificação determinística de risco.
- Roteamento para human-in-the-loop em casos de risco alto ou baixa evidência.
- Integração com Bedrock isolada em `src/llm.py`, com fallback local.
- Logs locais em JSONL com minimização de dados.
- Testes e avaliação simples de comportamento.

## Fluxo

```text
Analista operacional
  -> Streamlit
  -> LangGraph
  -> Classificação de intenção
  -> Recuperação documental
  -> Consulta simulada de dados
  -> Classificação de risco
  -> Revisão humana, se necessário
  -> Resposta estruturada
```

## Estrutura

```text
app.py                         Interface Streamlit
src/settings.py                Configuração por ambiente
src/llm.py                     Integração com Amazon Bedrock
src/rag.py                     Recuperação documental local
src/tools.py                   Dados simulados e regra de risco
src/graph.py                   Fluxo LangGraph e contrato da resposta
src/observability.py           Logs locais estruturados
data/politicas/                Documentos fictícios para RAG
tests/                         Testes de smoke e comportamento
evals/                         Casos simples de avaliação
docs/                          Arquitetura, metodologia e notas de entrevista
GOVERNANCE.md                  Governança, limites e evolução para produção
pyproject.toml                 Configuração de qualidade
```

## Como Executar

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.port 8502
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py --server.port 8502
```

## Variáveis De Ambiente

Copie `.env.example` para `.env` se quiser ajustar a configuração local.

```text
AWS_REGION
BEDROCK_CHAT_MODEL_ID
BEDROCK_EMBED_MODEL_ID
STREAMLIT_SERVER_PORT
DATA_DIR
LOG_DIR
ENABLE_LOCAL_LOGS
DEFAULT_CUSTOMER_ID
```

Credenciais reais não devem ser versionadas.

## Testes

```bash
python -m unittest discover -s tests
```

## Avaliação Simples

```bash
python -m evals.run_eval
```

A avaliação verifica se os cenários principais retornam o risco e a recomendação de revisão humana esperados.

Leia [`EVALUATION.md`](EVALUATION.md) para detalhes dos critérios.

## Qualidade

```bash
python -m ruff check .
python -m black --check .
```

## Governança

Leia [`GOVERNANCE.md`](GOVERNANCE.md) para os controles da POC: dados fictícios, minimização, rastreabilidade, revisão humana e limites de produção.

## Materiais De Apoio

- [`docs/bank-genai-operations-assistant-architecture.md`](docs/bank-genai-operations-assistant-architecture.md)
- [`docs/bank-genai-operations-assistant-methodology.md`](docs/bank-genai-operations-assistant-methodology.md)
- [`docs/bank-genai-operations-assistant-concepts.md`](docs/bank-genai-operations-assistant-concepts.md)
- [`docs/bank-genai-operations-assistant-interview-notes.md`](docs/bank-genai-operations-assistant-interview-notes.md)

## Limites Da POC

- Dados e documentos são fictícios.
- A recuperação local é simples e lexical.
- A ferramenta transacional é simulada.
- Não há autenticação, autorização ou integração real com sistemas bancários.
- O LLM apoia redação e interpretação, mas não executa decisões críticas.
