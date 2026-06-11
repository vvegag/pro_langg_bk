# Bank GenAI Operations Assistant

Esta solução local demonstra o fluxo de um assistente bancário com Streamlit, LangGraph, RAG, Bedrock e validação de risco.

## O que esta solução faz

- Recebe uma solicitação operacional via Streamlit
- Classifica a intenção da solicitação
- Recupera contexto a partir de documentos fictícios em `data/politicas/`
- Consulta dados simulados de cliente e transação
- Classifica o risco operacional
- Recomenda revisão humana quando necessário
- Gera uma resposta final estruturada

## Estrutura principal

- `app.py`: interface Streamlit
- `src/settings.py`: configuração por ambiente
- `src/llm.py`: integração com Bedrock
- `src/rag.py`: carga e busca de documentos
- `src/tools.py`: mocks de cliente, transação e risco
- `src/graph.py`: fluxo principal
- `data/politicas/`: taxonomia de documentos para RAG
- `tests/test_smoke.py`: checagens básicas
- `tests/test_flow_behavior.py`: testes de comportamento do fluxo

## Como executar

```bash
python -m venv .venv
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste se necessário:

- `AWS_REGION`
- `BEDROCK_CHAT_MODEL_ID`
- `BEDROCK_EMBED_MODEL_ID`
- `STREAMLIT_SERVER_PORT`
- `DATA_DIR`
- `DEFAULT_CUSTOMER_ID`

## Teste de sanidade

```bash
python -m unittest discover -s tests
```

## Guia de conceitos

Leia [`docs/bank-genai-operations-assistant-concepts.md`](docs/bank-genai-operations-assistant-concepts.md) para uma explicação curta sobre os conceitos de LLM, prompt, RAG, LangGraph, Bedrock, embeddings, risco e revisão humana usados aqui.

## Perguntas e respostas

Leia [`docs/bank-genai-operations-assistant-interview-notes.md`](docs/bank-genai-operations-assistant-interview-notes.md) para uma versão curta das respostas que explicam o funcionamento da solução.

## Observação

Esta solução local usa documentos, dados de cliente e transações fictícios, e o fluxo foi desenhado para demonstrar arquitetura, não produção.
