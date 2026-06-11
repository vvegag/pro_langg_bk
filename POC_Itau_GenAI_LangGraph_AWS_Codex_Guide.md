# POC bank — Assistente Multiagente com GenAI, LangGraph e AWS

**Objetivo:** construir uma POC curta, apresentável em entrevista, mostrando domínio de **LLMs, LangGraph, RAG, agentes, AWS Bedrock, validação de risco, ferramentas externas e human-in-the-loop**.

Esta POC foi pensada para uma vaga de **Especialista em Data Science com foco em IA Generativa**, usando AWS e soluções multiagentes para apoiar processos operacionais de um banco.

---

## 1. Mensagem central da POC para a entrevista

A POC demonstra que um LLM não deve trabalhar sozinho em ambiente bancário. O fluxo correto é:

```text
Entrada do usuário / analista operacional
        ↓
LangGraph controla o fluxo multiagente
        ↓
Classificação de intenção
        ↓
Busca de contexto em documentos internos via RAG
        ↓
Consulta de ferramenta/API simulada
        ↓
Classificação de risco operacional
        ↓
Validação e recomendação de human-in-the-loop
        ↓
Resposta final estruturada com evidências
```

Frase para explicar:

> “Construi uma POC de assistente operacional bancário usando LangGraph para orquestrar um fluxo com classificação de intenção, recuperação documental, consulta a ferramenta simulada, avaliação de risco e geração de resposta com LLM via AWS Bedrock. A solução reduz hallucination usando contexto recuperado, valida risco antes de recomendar ação e envia casos sensíveis para revisão humana.”

---

## 2. O que esta POC precisa mostrar

A POC precisa evidenciar:

1. Uso de **LLM** via AWS Bedrock.
2. Uso de **LangGraph** para orquestração.
3. Uso de **RAG** para recuperar contexto documental.
4. Uso de **ferramentas externas** simulando APIs ou bases internas do banco.
5. Validação de **risco operacional**.
6. Resposta estruturada e auditável.
7. Recomendação de **human-in-the-loop** em casos sensíveis.
8. Código organizado para mostrar autonomia técnica.

---

## 3. Arquitetura proposta

```text
Streamlit App
   |
   v
LangGraph Workflow
   |
   |-- Node 1: Classificador de intenção
   |-- Node 2: RAG / recuperação de contexto
   |-- Node 3: Consulta de ferramenta transacional simulada
   |-- Node 4: Classificação de risco
   |-- Node 5: Geração de resposta final
   |
   v
AWS Bedrock LLM
```

Em produção, essa arquitetura poderia evoluir para:

```text
Usuário / Sistema interno
        ↓
API Gateway / FastAPI
        ↓
Serviço Python com LangGraph em ECS, EKS, Lambda ou SageMaker
        ↓
Amazon Bedrock para LLM
        ↓
Bedrock Knowledge Bases ou OpenSearch/Aurora pgvector para RAG
        ↓
S3 para documentos
        ↓
APIs internas / bancos / filas
        ↓
CloudWatch + IAM + KMS + Secrets Manager + auditoria
```

---

## 4. Stack da POC

- Python
- LangGraph
- LangChain
- AWS Bedrock
- Bedrock Runtime
- Bedrock Embeddings, se disponível
- FAISS para vector store local
- Streamlit para interface
- Boto3 para conexão AWS
- python-dotenv para configuração local
- Git/GitHub para versionamento
- VS Code Copilot ou Codex para acelerar implementação

---

## 5. Pré-requisitos

### 5.1. Local

Instalar:

- Python 3.10 ou superior
- Git
- VS Code
- AWS CLI
- Conta AWS com acesso ao Amazon Bedrock

Verificar:

```bash
python --version
git --version
aws --version
```

### 5.2. AWS

No Console AWS:

1. Abrir **Amazon Bedrock**.
2. Ir em **Model access**.
3. Habilitar pelo menos um modelo de chat, por exemplo:
   - Claude 3 Haiku
   - Claude 3.5 Sonnet
   - outro modelo disponível na sua região
4. Habilitar também um modelo de embeddings, se possível:
   - Amazon Titan Text Embeddings

Configurar credenciais localmente:

```bash
aws configure
```

Informar:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name: us-east-1
Default output format: json
```

**Importante:** nunca subir credenciais para GitHub, Codex ou Copilot. O arquivo `.env` deve ficar no `.gitignore`.

---

## 6. Criar projeto no terminal Bash

```bash
mkdir poc-itau-genai-agents
cd poc-itau-genai-agents
python -m venv .venv
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
python -m pip install --upgrade pip
```

Criar `requirements.txt`:

```bash
cat > requirements.txt <<'EOF_REQ'
boto3>=1.34.0
python-dotenv>=1.0.0
streamlit>=1.35.0
pandas>=2.0.0
langgraph>=0.2.0
langchain>=0.2.0
langchain-community>=0.2.0
langchain-aws>=0.1.0
faiss-cpu>=1.8.0
pydantic>=2.0.0
EOF_REQ
```

Instalar:

```bash
pip install -r requirements.txt
```

Criar estrutura:

```bash
mkdir -p data src
```

---

## 7. Criar arquivos de configuração

### 7.1. `.gitignore`

```bash
cat > .gitignore <<'EOF_GIT'
.venv/
__pycache__/
*.pyc
.env
.faiss/
.DS_Store
EOF_GIT
```

### 7.2. `.env.example`

```bash
cat > .env.example <<'EOF_ENV'
AWS_REGION=us-east-1
BEDROCK_CHAT_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_EMBED_MODEL_ID=amazon.titan-embed-text-v2:0
EOF_ENV
```

Copiar para `.env`:

```bash
cp .env.example .env
```

Ajustar o `.env` se o modelo disponível na sua conta/região for diferente.

---

## 8. Criar documentos fictícios para RAG

### 8.1. `data/politicas/atendimento/politica_atendimento.txt`

```bash
cat > data/politicas/atendimento/politica_atendimento.txt <<'EOF_DOC'
Política de atendimento operacional bancário:
Toda solicitação crítica deve conter identificação do cliente, produto, canal, motivo e evidência.
Casos com impacto financeiro devem ser classificados como risco médio ou alto.
Solicitações sem evidência documental devem ser enviadas para revisão humana.
O assistente deve informar quando não houver evidência suficiente para conclusão automática.
EOF_DOC
```

### 8.2. `data/politicas/contestacao/procedimento_contestacao.txt`

```bash
cat > data/politicas/contestacao/procedimento_contestacao.txt <<'EOF_DOC'
Procedimento de contestação de transação:
Para contestação de transação, verificar data, valor, canal, histórico do cliente e evidências.
Se houver divergência entre relato e dados transacionais, abrir análise manual.
Se o valor for superior a R$ 10.000, exigir validação adicional.
Se houver indício de fraude, classificar como risco alto e encaminhar para especialista humano.
EOF_DOC
```

### 8.3. `data/politicas/risco_operacional/regras_risco_operacional.txt`

```bash
cat > data/politicas/risco_operacional/regras_risco_operacional.txt <<'EOF_DOC'
Regras de risco operacional:
Risco baixo: solicitação informativa sem impacto financeiro.
Risco médio: alteração cadastral, contestação simples ou divergência de dados sem indício forte de fraude.
Risco alto: impacto financeiro elevado, possível fraude, dados sensíveis, ausência de evidência ou transação acima de R$ 10.000.
Todo risco alto exige human-in-the-loop antes de execução de qualquer ação.
EOF_DOC
```

---

## 9. Código da POC

### 9.1. `src/settings.py`

```bash
cat > src/settings.py <<'EOF_PY'
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_CHAT_MODEL_ID = os.getenv(
    "BEDROCK_CHAT_MODEL_ID",
    "anthropic.claude-3-haiku-20240307-v1:0"
)
BEDROCK_EMBED_MODEL_ID = os.getenv(
    "BEDROCK_EMBED_MODEL_ID",
    "amazon.titan-embed-text-v2:0"
)
EOF_PY
```

### 9.2. `src/llm.py`

```bash
cat > src/llm.py <<'EOF_PY'
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from src.settings import AWS_REGION, BEDROCK_CHAT_MODEL_ID

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def call_llm(prompt: str, max_tokens: int = 900, temperature: float = 0.2) -> str:
    """Call an Anthropic Claude model through Amazon Bedrock."""
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = bedrock.invoke_model(
            modelId=BEDROCK_CHAT_MODEL_ID,
            body=json.dumps(body)
        )
        result = json.loads(response["body"].read())
        return result["content"][0]["text"]
    except (BotoCoreError, ClientError, KeyError, json.JSONDecodeError) as exc:
        return (
            "[LLM_ERROR] Não foi possível chamar o modelo no Amazon Bedrock. "
            f"Detalhe técnico: {exc}"
        )
EOF_PY
```

### 9.3. `src/rag.py`

```bash
cat > src/rag.py <<'EOF_PY'
from pathlib import Path
from typing import List

import boto3
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

from src.settings import AWS_REGION, BEDROCK_EMBED_MODEL_ID


_VECTORSTORE = None


def load_documents(data_dir: str = "data") -> List[Document]:
    docs: List[Document] = []
    for file_path in Path(data_dir).glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        docs.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name}
            )
        )
    return docs


def build_vectorstore():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(docs)

    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    embeddings = BedrockEmbeddings(
        client=client,
        model_id=BEDROCK_EMBED_MODEL_ID
    )

    return FAISS.from_documents(chunks, embeddings)


def get_vectorstore():
    global _VECTORSTORE
    if _VECTORSTORE is None:
        _VECTORSTORE = build_vectorstore()
    return _VECTORSTORE


def retrieve_context(question: str, k: int = 3) -> str:
    try:
        vectorstore = get_vectorstore()
        docs = vectorstore.similarity_search(question, k=k)
    except Exception as exc:
        return (
            "[RAG_ERROR] Não foi possível recuperar contexto por embeddings. "
            f"Detalhe técnico: {exc}"
        )

    context_parts = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        context_parts.append(f"[Fonte: {source}]\n{doc.page_content}")

    return "\n\n".join(context_parts)
EOF_PY
```

### 9.4. `src/tools.py`

```bash
cat > src/tools.py <<'EOF_PY'
from typing import Dict, Any


def get_customer_transaction_summary(customer_id: str) -> Dict[str, Any]:
    """Simulates an internal banking API or database lookup."""
    fake_database = {
        "123": {
            "customer_id": "123",
            "transactions_last_30_days": 18,
            "total_amount": 12500.00,
            "suspicious_activity": True,
            "main_channel": "mobile",
            "last_transaction_value": 10800.00,
            "product": "credit_card"
        },
        "456": {
            "customer_id": "456",
            "transactions_last_30_days": 4,
            "total_amount": 850.00,
            "suspicious_activity": False,
            "main_channel": "branch",
            "last_transaction_value": 120.00,
            "product": "checking_account"
        }
    }

    return fake_database.get(
        customer_id,
        {
            "customer_id": customer_id,
            "transactions_last_30_days": 0,
            "total_amount": 0.0,
            "suspicious_activity": None,
            "main_channel": "unknown",
            "last_transaction_value": 0.0,
            "product": "unknown"
        }
    )


def classify_risk(transaction_summary: Dict[str, Any]) -> str:
    amount = float(transaction_summary.get("total_amount", 0.0) or 0.0)
    last_value = float(transaction_summary.get("last_transaction_value", 0.0) or 0.0)
    suspicious = transaction_summary.get("suspicious_activity")

    if suspicious or amount > 10000 or last_value > 10000:
        return "alto"
    if amount > 1000 or last_value > 1000:
        return "medio"
    return "baixo"
EOF_PY
```

### 9.5. `src/graph.py`

```bash
cat > src/graph.py <<'EOF_PY'
from typing import TypedDict, Optional, Dict, Any

from langgraph.graph import StateGraph, END

from src.llm import call_llm
from src.rag import retrieve_context
from src.tools import get_customer_transaction_summary, classify_risk


class AgentState(TypedDict):
    user_question: str
    customer_id: str
    intent: Optional[str]
    context: Optional[str]
    transaction_summary: Optional[Dict[str, Any]]
    risk_level: Optional[str]
    human_review_required: Optional[bool]
    final_answer: Optional[str]


def classify_intent_node(state: AgentState) -> AgentState:
    prompt = f"""
Você é um classificador de intenção para processos operacionais bancários.

Solicitação:
{state['user_question']}

Classifique a intenção em apenas uma opção:
- contestacao
- consulta_operacional
- risco
- cadastro
- outro

Responda apenas com a categoria.
"""
    intent = call_llm(prompt, max_tokens=50, temperature=0.0).strip().lower()
    state["intent"] = intent
    return state


def retrieve_context_node(state: AgentState) -> AgentState:
    state["context"] = retrieve_context(state["user_question"])
    return state


def data_tool_node(state: AgentState) -> AgentState:
    customer_id = state.get("customer_id", "123")
    state["transaction_summary"] = get_customer_transaction_summary(customer_id)
    return state


def risk_node(state: AgentState) -> AgentState:
    summary = state.get("transaction_summary") or {}
    risk = classify_risk(summary)
    state["risk_level"] = risk
    state["human_review_required"] = risk == "alto"
    return state


def final_answer_node(state: AgentState) -> AgentState:
    prompt = f"""
Você é um assistente operacional bancário.

Regras importantes:
- Não invente fatos.
- Use apenas as evidências disponíveis no contexto e no resumo transacional.
- Se faltar evidência, recomende revisão humana.
- Para risco alto, recomende human-in-the-loop.
- Seja claro, objetivo e auditável.

Solicitação do usuário:
{state['user_question']}

Intenção classificada:
{state.get('intent')}

Contexto documental recuperado:
{state.get('context')}

Resumo transacional:
{state.get('transaction_summary')}

Nível de risco:
{state.get('risk_level')}

Revisão humana obrigatória:
{state.get('human_review_required')}

Gere uma resposta estruturada em português com:
1. Entendimento da solicitação
2. Evidências consultadas
3. Avaliação de risco
4. Recomendação operacional
5. Necessidade de revisão humana
6. Limitações da análise
"""
    state["final_answer"] = call_llm(prompt, max_tokens=900, temperature=0.2)
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
EOF_PY
```

### 9.6. `app.py`

```bash
cat > app.py <<'EOF_PY'
import streamlit as st

from src.graph import build_graph

st.set_page_config(
    page_title="POC Itaú GenAI Multiagent Assistant",
    layout="wide"
)

st.title("POC Itaú — GenAI Multiagent Banking Assistant")
st.write("LangGraph + AWS Bedrock + RAG + ferramenta simulada + validação de risco")

with st.sidebar:
    st.header("Configuração")
    customer_id = st.selectbox("Cliente simulado", options=["123", "456", "999"])
    st.caption("123 = caso de risco alto; 456 = caso simples; 999 = cliente desconhecido")

question = st.text_area(
    "Solicitação operacional",
    value=(
        "Cliente 123 contesta uma transação de valor elevado feita pelo aplicativo. "
        "Existe risco operacional? Qual procedimento devo seguir?"
    ),
    height=120
)

if st.button("Executar análise multiagente"):
    with st.spinner("Executando LangGraph..."):
        graph = build_graph()
        initial_state = {
            "user_question": question,
            "customer_id": customer_id,
            "intent": None,
            "context": None,
            "transaction_summary": None,
            "risk_level": None,
            "human_review_required": None,
            "final_answer": None
        }
        result = graph.invoke(initial_state)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Intenção")
        st.write(result.get("intent"))

        st.subheader("Resumo transacional")
        st.json(result.get("transaction_summary"))

        st.subheader("Risco")
        st.write(result.get("risk_level"))
        st.write("Revisão humana obrigatória:", result.get("human_review_required"))

    with col2:
        st.subheader("Contexto recuperado via RAG")
        st.text(result.get("context"))

    st.subheader("Resposta final")
    st.write(result.get("final_answer"))
EOF_PY
```

### 9.7. `README.md`

```bash
cat > README.md <<'EOF_MD'
# POC Itaú — GenAI Multiagent Banking Assistant

POC para demonstrar uma arquitetura de IA Generativa aplicada a processos operacionais bancários.

## Objetivo

Demonstrar um fluxo multiagente usando:

- LangGraph
- AWS Bedrock
- RAG sobre documentos operacionais fictícios
- Ferramenta simulada de consulta transacional
- Classificação de risco operacional
- Recomendação de human-in-the-loop

## Fluxo

1. Usuário descreve uma solicitação operacional.
2. O LangGraph classifica a intenção.
3. O sistema recupera contexto em documentos internos fictícios.
4. Uma ferramenta simulada consulta dados transacionais.
5. O sistema classifica o risco.
6. O LLM gera resposta estruturada usando evidências.
7. Casos de risco alto são enviados para revisão humana.

## Como executar

```bash
python -m venv .venv
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
aws configure
streamlit run app.py
```

## Importante

Esta POC usa dados fictícios e não deve conter dados reais de clientes, credenciais ou documentos confidenciais.
EOF_MD
```

---

## 10. Rodar a aplicação

```bash
streamlit run app.py
```

Abrir no navegador o endereço mostrado pelo Streamlit, normalmente:

```text
http://localhost:8501
```

Testar os casos:

### Caso 1 — risco alto

```text
Cliente 123 contesta uma transação de valor elevado feita pelo aplicativo. Existe risco operacional? Qual procedimento devo seguir?
```

Resultado esperado:

- intenção: contestação ou risco
- risco: alto
- recomendação: human-in-the-loop
- evidência: procedimento de contestação + regras de risco

### Caso 2 — risco baixo ou médio

```text
Cliente 456 solicita orientação sobre uma contestação simples de baixo valor. Qual procedimento seguir?
```

Resultado esperado:

- risco menor
- resposta orientativa
- sem decisão crítica automática

---

## 11. Como explicar LangGraph na entrevista

LangGraph organiza o fluxo em:

- **State:** estado compartilhado do processo.
- **Nodes:** etapas do fluxo, por exemplo classificar intenção, recuperar contexto, consultar ferramenta e gerar resposta.
- **Edges:** conexões entre etapas.
- **Conditional edges:** caminhos condicionais, por exemplo enviar para revisão humana se risco for alto.

Frase curta:

> “Usei LangGraph porque um processo bancário com GenAI não é apenas pergunta e resposta. Precisa de etapas controladas: classificar, buscar evidências, consultar dados, avaliar risco, validar e só então responder.”

---

## 12. Como explicar RAG na entrevista

RAG significa **Retrieval-Augmented Generation**.

Na POC:

1. Documentos operacionais fictícios ficam organizados em `data/politicas/`.
2. O sistema quebra os documentos em chunks.
3. Gera embeddings com Amazon Bedrock.
4. Armazena os vetores em FAISS.
5. Busca trechos relevantes para a pergunta.
6. Passa esses trechos ao LLM.
7. O LLM responde com base no contexto recuperado.

Frase curta:

> “Usei RAG para reduzir hallucination e fazer o LLM responder com base em documentos operacionais recuperados, não apenas com conhecimento genérico.”

---

## 13. Como explicar AWS na entrevista

Na POC:

- AWS Bedrock fornece o LLM.
- Bedrock embeddings podem gerar vetores para RAG.
- A execução está local, mas conectada à AWS.

Em produção:

- S3 armazenaria documentos.
- Bedrock Knowledge Bases ou OpenSearch fariam RAG gerenciado.
- ECS/EKS/Lambda hospedariam o serviço.
- API Gateway exporia o endpoint.
- CloudWatch faria logs.
- IAM/KMS/Secrets Manager fariam segurança.

Frase curta:

> “Para a entrevista eu construí uma POC local usando Bedrock, mas a evolução natural seria colocar documentos em S3, usar Bedrock Knowledge Bases ou OpenSearch para recuperação, expor uma API e instrumentar tudo com CloudWatch, IAM, KMS e Secrets Manager.”

---

## 14. Como falar sobre autonomia

Frase para usar:

> “Para mim, autonomia de especialista é pegar um problema ambíguo, decompor em arquitetura, identificar riscos, montar um POC funcional, validar com usuários, documentar decisões e propor o caminho para produção com segurança, métricas e governança.”

---

## 15. Prompts para usar no VS Code Copilot

### Prompt 1 — gerar/ajustar projeto

```text
Estou criando uma POC para entrevista de Especialista em Data Science com foco em IA Generativa em banco.

Stack:
- Python
- LangGraph
- AWS Bedrock
- Streamlit
- RAG com documentos locais
- FAISS
- ferramenta simulada de consulta transacional
- classificação de risco operacional

Objetivo:
Criar uma aplicação simples e bem organizada que receba uma solicitação operacional, classifique a intenção, recupere contexto documental, consulte uma ferramenta simulada, avalie risco e gere uma resposta final com recomendação de human-in-the-loop quando necessário.

Revise o projeto, melhore organização, tratamento de erros, type hints, README e clareza do código.
```

### Prompt 2 — revisar como projeto de entrevista

```text
Revise este repositório como se fosse uma POC técnica para vaga de Especialista em Data Science / GenAI em um banco. Avalie:
1. Clareza da arquitetura
2. Uso correto de LangGraph
3. Uso de RAG
4. Segurança e riscos
5. O que falta para produção
6. Como explicar isso em entrevista
Sugira melhorias sem tornar o projeto complexo demais.
```

### Prompt 3 — melhorar README

```text
Melhore o README para explicar a POC para uma entrevista técnica. O README deve conter: objetivo, arquitetura, fluxo LangGraph, como executar, limitações, próximos passos para produção em AWS e principais pontos para defesa técnica.
```

---

## 16. Prompts para usar no Codex

### Prompt principal para Codex

```text
You are helping me build an interview-ready proof-of-concept for a GenAI Specialist / Senior Data Scientist role in a bank.

Project goal:
Build a multi-agent banking operational assistant using Python, LangGraph, AWS Bedrock, Streamlit, simple RAG over local policy documents, and simulated banking tools.

The system should:
1. Receive an operational request from a user.
2. Classify the intent.
3. Retrieve relevant policy/procedure context using RAG.
4. Call a simulated customer transaction tool.
5. Classify operational risk.
6. Generate a final grounded response.
7. Recommend human-in-the-loop for high-risk cases.

Please:
- Review the code structure.
- Improve code quality.
- Add error handling.
- Add type hints.
- Improve README.
- Keep it simple enough for an interview demo.
- Do not add real credentials, real banking data, or unnecessary infrastructure.
```

### Prompt para Codex corrigir erro

```text
I am getting this error when running the Streamlit app:

[PASTE ERROR HERE]

Please identify the root cause and fix the minimum necessary code. Keep the architecture simple and explain what changed.
```

### Prompt para Codex preparar apresentação

```text
Create a short technical explanation for this POC that I can use in an interview. Include:
- Problem statement
- Architecture
- Why LangGraph
- Why RAG
- Why human-in-the-loop
- AWS production evolution
- Main limitations
- Next steps
```

---

## 17. Possíveis erros e correções

### Erro: modelo Bedrock sem acesso

Sintoma:

```text
AccessDeniedException or model access denied
```

Correção:

1. Ir em Amazon Bedrock.
2. Abrir Model access.
3. Solicitar acesso ao modelo.
4. Confirmar região correta no `.env`.

### Erro: modelo não existe na região

Sintoma:

```text
The provided model identifier is invalid
```

Correção:

Trocar `BEDROCK_CHAT_MODEL_ID` no `.env` por um modelo disponível na sua região.

### Erro: AWS credentials not found

Correção:

```bash
aws configure
aws sts get-caller-identity
```

### Erro: langchain_community não encontrado

Correção:

```bash
pip install langchain-community
```

### Erro: faiss não encontrado

Correção:

```bash
pip install faiss-cpu
```

---

## 18. Próximos passos para deixar mais forte

Se sobrar tempo, implementar:

1. Conditional edge no LangGraph:
   - se risco alto, ir para node `human_review`.
   - se risco baixo/médio, ir direto para resposta final.

2. Logs:
   - salvar intenção, risco, fontes recuperadas e tempo de resposta.

3. Avaliação:
   - criar 5 perguntas teste e comparar respostas.

4. API:
   - criar FastAPI além do Streamlit.

5. AWS mais real:
   - colocar documentos em S3.
   - migrar RAG para Bedrock Knowledge Bases.
   - usar CloudWatch para logs.

---

## 19. Versão com conditional edge opcional

Explicação para entrevista:

> “A versão inicial executa um fluxo linear para clareza. Em produção, eu usaria conditional edges para direcionar risco alto a uma etapa de human-in-the-loop, risco médio para validação adicional e risco baixo para resposta automática.”

Pseudo-fluxo:

```text
risk_node
   ├── risco alto  → human_review_node → final_answer
   └── risco baixo/médio → final_answer
```

---

## 20. Limitações honestas da POC

Explique com maturidade:

1. Os dados são fictícios.
2. A ferramenta transacional é simulada.
3. A vector store é local com FAISS.
4. Não há autenticação de usuário.
5. Não há observabilidade completa.
6. Não há avaliação formal de hallucination.
7. Não há integração real com sistemas bancários.

Frase boa:

> “A POC foi desenhada para provar arquitetura e raciocínio técnico, não para simular toda a complexidade de produção. Para produção, eu adicionaria autenticação, segregação de acesso, logs, métricas, avaliação contínua, governança de documentos, revisão humana, versionamento de prompts e controle de custo.”

---

## 21. Como conectar com sua experiência real

Na entrevista, conectar assim:

- CRMBONUS: produtos analíticos, Databricks, PySpark, SQL, dashboards, modelos, IA aplicada.
- ENEL: modelos preditivos para manutenção e suporte à decisão operacional.
- FUSP/Petrobras: ML, NLP, gêmeo digital e problemas industriais complexos.
- Professor/Pesquisador: capacidade de explicar, estruturar e aprender rápido.
- POC atual: ponte para GenAI, LLMs, LangGraph, RAG, agentes e AWS.

Frase:

> “Minha base é muito forte em Data Science aplicado, modelagem preditiva, séries temporais, PySpark, SQL, Databricks e produtos analíticos. Esta POC mostra minha transição prática para arquiteturas GenAI com agentes, RAG e AWS, mantendo o mesmo foco: resolver problemas operacionais reais com segurança, evidência e impacto.”

---

## 22. Pitch final de 60 segundos

> “Eu construí uma POC de assistente multiagente para apoiar processos operacionais bancários. Usei LangGraph para controlar o fluxo em etapas: classificação de intenção, recuperação de contexto documental via RAG, consulta a uma ferramenta simulada de dados transacionais, avaliação de risco e geração de resposta final com LLM via AWS Bedrock. A ideia principal é não deixar o LLM responder isoladamente: ele precisa de contexto, ferramentas, validação, logs e human-in-the-loop quando há risco alto. Essa arquitetura pode evoluir para produção em AWS com S3, Bedrock Knowledge Bases, APIs internas, CloudWatch, IAM, KMS e governança de dados.”

---

## 23. Checklist antes da entrevista

- [ ] Aplicação Streamlit abre sem erro.
- [ ] Caso cliente 123 gera risco alto.
- [ ] Caso cliente 456 gera risco baixo ou médio.
- [ ] Você consegue explicar LangGraph em 1 minuto.
- [ ] Você consegue explicar RAG em 1 minuto.
- [ ] Você consegue explicar por que human-in-the-loop é necessário.
- [ ] Você sabe quais serviços AWS usaria em produção.
- [ ] README está claro.
- [ ] Repositório não contém `.env`, chaves ou dados reais.
- [ ] Você consegue desenhar a arquitetura no papel.

---

## 24. Resumo do que dizer se perguntarem se isso está em produção

> “Não. Esta é uma POC criada para validar arquitetura, fluxo multiagente e raciocínio técnico. Em produção, eu reforçaria segurança, autenticação, observabilidade, avaliação, governança de documentos, controle de acesso por perfil, revisão humana e integração com sistemas internos do banco.”

---

## 25. Comando final para rodar tudo

```bash
cd poc-itau-genai-agents
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
pip install -r requirements.txt
aws sts get-caller-identity
streamlit run app.py
```

---

## 26. Entregável esperado

Ao final, você deve ter:

```text
poc-itau-genai-agents/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   └── politicas/
│       ├── atendimento/
│       │   └── politica_atendimento.txt
│       ├── contestacao/
│       │   └── procedimento_contestacao.txt
│       └── risco_operacional/
│           └── regras_risco_operacional.txt
└── src/
    ├── settings.py
    ├── llm.py
    ├── rag.py
    ├── tools.py
    └── graph.py
```
