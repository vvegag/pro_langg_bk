# POC Itaú GenAI Multiagentes — Versão 2 para Aprendizado e Entrevista

**Objetivo:** evoluir a POC inicial para aprender mais e chegar na entrevista sabendo explicar uma arquitetura realista de **LLMs + RAG + LangGraph + AWS + multiagentes + validação + human-in-the-loop** para processos operacionais de banco.

> Estratégia: não tentar construir “um sistema gigante”. Construir uma POC pequena, clara e bem explicada, com camadas que mostram maturidade técnica.

---

## 1. Por que vale a pena modificar a POC?

Sim, vale a pena. A primeira versão mostra o fluxo básico. A versão 2 deve mostrar que você entende problemas reais de banco:

- O LLM não pode responder sem evidência.
- O agente não pode executar ação crítica sozinho.
- É necessário classificar risco.
- É necessário recuperar documentos internos via RAG.
- É necessário consultar dados operacionais via ferramenta/API.
- É necessário validar a resposta.
- É necessário ter logs, rastreabilidade e human-in-the-loop.
- É necessário pensar em AWS, segurança, custo e escalabilidade.

A nova POC deve ser uma simulação de um **copiloto operacional bancário**, não apenas um chatbot.

---

## 2. Tema recomendado da POC

## Banking Operations GenAI Copilot

Um assistente multiagente que recebe uma solicitação operacional, consulta políticas internas fictícias, consulta dados simulados de cliente/transação, classifica risco, valida se existe evidência suficiente e recomenda uma ação.

### Exemplo de pergunta

```text
Cliente 123 contesta uma transação de R$ 12.500 realizada pelo app.
Existe indício de risco? Qual procedimento o analista deve seguir?
```

### Resposta esperada

A resposta deve conter:

- entendimento da solicitação;
- documentos usados como evidência;
- dados transacionais consultados;
- classificação de risco;
- recomendação operacional;
- necessidade ou não de revisão humana;
- alerta de que nenhuma ação financeira foi executada automaticamente.

---

## 3. Arquitetura lógica

```text
Usuário / Analista
      ↓
Interface Streamlit ou FastAPI
      ↓
LangGraph Supervisor
      ↓
Intent Agent
      ↓
RAG Agent
      ↓
Data Tool Agent
      ↓
Risk / Compliance Agent
      ↓
Answer Agent
      ↓
Critic / Validation Agent
      ↓
Resposta final ou Human-in-the-loop
```

---

## 4. Arquitetura AWS conceitual

Para a POC local:

```text
Python + LangGraph
Amazon Bedrock para LLM
FAISS/Chroma para vetor local
Arquivos .txt simulando políticas internas
Streamlit para interface
Logs locais em JSON
```

Para explicar uma versão corporativa na entrevista:

```text
S3
  ↓
Bedrock Knowledge Bases
  ↓
Vector Store gerenciado
  ↓
LangGraph em ECS/EKS/Lambda/SageMaker
  ↓
Amazon Bedrock como LLM
  ↓
APIs internas via API Gateway/Lambda
  ↓
Secrets Manager + IAM + KMS
  ↓
CloudWatch Logs
  ↓
Human approval workflow
```

---

## 5. O que deve mudar em relação à POC inicial

### Antes

```text
classificação → RAG → consulta simulada → risco → resposta final
```

### Agora

```text
classificação
  ↓
roteamento condicional
  ↓
RAG com documentos e fontes
  ↓
consulta de dados simulados
  ↓
classificação de risco
  ↓
validação crítica
  ↓
decisão:
    - se risco baixo/médio e evidência suficiente → resposta final
    - se risco alto ou pouca evidência → human-in-the-loop
```

---

## 6. Conceitos técnicos que você deve aprender fazendo

### LangGraph

Aprender na prática:

- `State`
- `Node`
- `Edge`
- `Conditional Edge`
- `Tool`
- roteamento
- validação
- estado acumulado
- subfluxos

### RAG

Aprender na prática:

- carregar documentos;
- quebrar em chunks;
- gerar embeddings;
- buscar trechos relevantes;
- passar contexto ao LLM;
- citar fontes;
- detectar falta de evidência.

### LLM

Aprender na prática:

- prompt estruturado;
- temperatura baixa;
- resposta em JSON ou Markdown;
- redução de hallucination;
- validação da resposta;
- fallback.

### Banco / ambiente operacional

Aprender na prática:

- simular API interna;
- simular dados de cliente;
- simular transações;
- calcular risco;
- não executar decisão crítica automaticamente.

---

## 7. Estrutura do projeto recomendada

```text
poc-itau-genai-v2/
│
├── app.py
├── main.py
├── graph.py
├── agents/
│   ├── __init__.py
│   ├── llm.py
│   ├── intent_agent.py
│   ├── rag_agent.py
│   ├── risk_agent.py
│   ├── answer_agent.py
│   └── critic_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── customer_tool.py
│   ├── transaction_tool.py
│   └── risk_rules.py
│
├── rag/
│   ├── __init__.py
│   ├── loader.py
│   ├── vectorstore.py
│   └── retriever.py
│
├── data/
│   ├── policies/
│   │   ├── politica_atendimento.txt
│   │   ├── procedimento_contestacao.txt
│   │   ├── regras_risco_operacional.txt
│   │   └── politica_privacidade_dados.txt
│   │
│   └── mock/
│       ├── customers.csv
│       └── transactions.csv
│
├── logs/
│   └── .gitkeep
│
├── tests/
│   ├── test_risk_rules.py
│   ├── test_tools.py
│   └── test_graph_smoke.py
│
├── .env.example
├── requirements.txt
├── README.md
└── INTERVIEW_NOTES.md
```

---

## 8. Comandos iniciais em Bash

```bash
mkdir poc-itau-genai-v2
cd poc-itau-genai-v2

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

pip install \
  boto3 \
  streamlit \
  pandas \
  pydantic \
  python-dotenv \
  langgraph \
  langchain \
  langchain-community \
  langchain-aws \
  faiss-cpu \
  pytest
```

Gerar `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## 9. Arquivo `.env.example`

```bash
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
USE_BEDROCK=true
```

Nunca commitar `.env` real.

---

## 10. Dados fictícios

### `data/policies/politica_atendimento.txt`

```text
Política de atendimento operacional:
Toda solicitação crítica deve conter identificação do cliente, produto, canal, motivo e evidência.
Casos com impacto financeiro devem ser classificados como risco médio ou alto.
Solicitações sem evidência documental devem ser enviadas para revisão humana.
Nenhuma ação financeira deve ser executada automaticamente por sistemas generativos sem validação humana.
```

### `data/policies/procedimento_contestacao.txt`

```text
Procedimento de contestação:
Para contestação de transação, verificar data, valor, canal, histórico do cliente e evidências.
Se houver divergência entre relato e dados transacionais, abrir análise manual.
Se o valor for superior a R$ 10.000, exigir validação adicional.
Casos com suspeita de fraude devem ser encaminhados para análise especializada.
```

### `data/policies/regras_risco_operacional.txt`

```text
Regras de risco operacional:
Risco baixo: solicitação informativa sem impacto financeiro.
Risco médio: alteração cadastral, contestação simples ou divergência de dados.
Risco alto: impacto financeiro elevado, possível fraude, dados sensíveis ou ausência de evidência.
Todo risco alto exige human-in-the-loop.
```

### `data/policies/politica_privacidade_dados.txt`

```text
Política de privacidade:
Dados sensíveis, dados pessoais e informações financeiras devem ser minimizados na resposta.
O assistente deve evitar expor dados pessoais completos.
O assistente deve indicar quando uma solicitação exige autorização adicional.
```

### `data/mock/customers.csv`

```csv
customer_id,name,segment,account_status
123,Cliente A,premium,active
456,Cliente B,mass,active
789,Cliente C,private,inactive
```

### `data/mock/transactions.csv`

```csv
transaction_id,customer_id,amount,channel,days_ago,is_suspicious
tx001,123,12500,mobile,2,true
tx002,123,350,card,10,false
tx003,456,850,branch,5,false
tx004,789,30000,mobile,1,true
```

---

## 11. Fluxo LangGraph recomendado

### Estado

O estado deve guardar:

```python
class AgentState(TypedDict):
    user_question: str
    customer_id: str | None
    intent: str | None
    retrieved_context: str | None
    sources: list[str]
    customer_data: dict | None
    transaction_data: dict | None
    risk_level: str | None
    risk_reasons: list[str]
    draft_answer: str | None
    validation_status: str | None
    validation_notes: list[str]
    final_answer: str | None
    requires_human_review: bool
```

### Nós

```text
1. parse_request_node
2. classify_intent_node
3. retrieve_context_node
4. fetch_customer_data_node
5. fetch_transaction_data_node
6. classify_risk_node
7. generate_answer_node
8. critic_validation_node
9. human_review_node
10. final_response_node
```

### Roteamento condicional

```text
Se intent = "contestacao" → RAG + dados + risco
Se intent = "consulta_informativa" → RAG + resposta
Se risk_level = "alto" → human_review
Se validation_status = "failed" → human_review
Caso contrário → resposta final
```

---

## 12. Critérios de validação

O agente crítico deve verificar:

- A resposta citou documentos recuperados?
- Existe evidência suficiente?
- O risco foi classificado?
- Há dados sensíveis expostos?
- A resposta inventou alguma informação?
- O caso exige revisão humana?
- A resposta deixa claro que nenhuma transação foi executada?

---

## 13. Resultado ideal da POC

A interface deve mostrar:

```text
Pergunta original
Intenção detectada
Fontes recuperadas
Dados simulados consultados
Classificação de risco
Resposta preliminar
Validação crítica
Resposta final
Requer revisão humana? Sim/Não
```

---

## 14. Prompt principal para VS Code Copilot

Copie e cole no Copilot Chat do VS Code:

```text
I want to build an interview-ready proof-of-concept for a Banking Operations GenAI Copilot.

Context:
I am preparing for a Senior Data Science / GenAI Specialist interview in a bank.
The role involves LLMs, LangGraph, AWS, and multi-agent solutions for operational banking processes.

Build a Python project with:
- LangGraph for orchestration
- Amazon Bedrock as the LLM provider, but with a fallback mock LLM for local testing
- Simple RAG over local policy documents
- FAISS vector store
- Streamlit interface
- Simulated tools for customer and transaction lookup
- Risk classification
- Critic/validator agent
- Human-in-the-loop recommendation for high-risk or low-evidence cases
- Logs in JSON
- Tests with pytest
- Clear README and INTERVIEW_NOTES.md

Please create the project structure and implement it step by step.
Prioritize clarity, explainability, and interview value over production complexity.
Use only fictitious data.
Do not include real credentials.
```

---

## 15. Prompt principal para Codex

Copie e cole no Codex:

```text
You are a senior GenAI engineer helping me build an interview-ready POC.

Project:
Banking Operations GenAI Copilot

Goal:
Create a proof-of-concept that demonstrates:
1. LangGraph multi-agent orchestration
2. LLM usage through Amazon Bedrock, with local mock fallback
3. RAG over banking policy documents
4. Simulated API/tools for customer and transaction data
5. Risk and compliance classification
6. Critic agent for validation
7. Human-in-the-loop recommendation
8. Streamlit UI
9. Logs and tests
10. Clean README and interview notes

Important:
- Use fictitious data only.
- Do not use real bank data.
- Do not include secrets or credentials.
- Code must be simple enough to explain in an interview.
- Prefer modular files and type hints.
- Add comments explaining why each agent exists.
- Add a README with architecture and how to run.
- Add INTERVIEW_NOTES.md with how to explain the project.

Please create the full repository structure, implement the MVP first, then suggest improvements.
```

---

## 16. Prompt para melhorar o README

```text
Improve the README for this repository as if it will be reviewed by a GenAI / Data Science hiring manager at a bank.

The README must explain:
- Business problem
- Why multi-agent architecture
- Why LangGraph
- Why RAG
- Why risk validation and human-in-the-loop
- AWS production architecture
- How to run locally
- What is simulated
- What would change in production
- Security and governance considerations
```

---

## 17. Prompt para revisar antes da entrevista

```text
Review this POC as if you were an interviewer for a Senior Data Scientist / GenAI Specialist role in a bank.

Please provide:
1. Strong points
2. Weak points
3. Questions the interviewer might ask
4. Improvements to make it more realistic
5. A 2-minute explanation script
6. A 5-minute technical deep dive script
7. Risks I should not overclaim
```

---

## 18. MVP mínimo para terminar rápido

Se o tempo for curto, implemente apenas isto:

```text
Streamlit
  ↓
LangGraph com 5 nós:
  1. classify_intent
  2. retrieve_context
  3. get_transaction_data
  4. classify_risk
  5. generate_final_answer
  ↓
human_review se risco alto
```

Isso já é suficiente para explicar a arquitetura.

---

## 19. Versão intermediária

Depois do MVP:

- adicionar critic agent;
- adicionar logs em JSON;
- adicionar testes;
- adicionar fontes na resposta;
- adicionar fallback se Bedrock não estiver configurado;
- adicionar README completo.

---

## 20. Versão avançada

Só faça se sobrar tempo:

- usar embeddings reais do Bedrock;
- usar Bedrock Knowledge Bases;
- colocar documentos no S3;
- criar FastAPI;
- criar Dockerfile;
- simular deploy em ECS;
- adicionar avaliação automática de respostas;
- adicionar métricas de custo/latência.

---

## 21. Como explicar na entrevista

### Explicação de 30 segundos

```text
Construí uma POC de um copiloto operacional bancário usando LangGraph para orquestrar agentes com responsabilidades separadas: classificação de intenção, recuperação de documentos via RAG, consulta simulada de dados transacionais, classificação de risco, geração de resposta e validação. A ideia é mostrar que o LLM não decide sozinho: ele é controlado por um fluxo com evidências, regras, validação e human-in-the-loop para casos sensíveis.
```

### Explicação de 2 minutos

```text
O problema simulado é apoiar analistas em processos operacionais, como contestação de transações. O usuário envia uma solicitação; o LangGraph coordena o fluxo. Primeiro, um agente classifica a intenção. Depois, um agente RAG busca políticas e procedimentos internos relevantes. Em seguida, ferramentas simuladas consultam dados de cliente e transações. Com essas informações, um agente classifica o risco operacional. O agente de resposta gera uma recomendação estruturada, mas antes da saída final um agente crítico valida se há evidência suficiente, se existe risco alto, se há exposição de dados sensíveis e se a resposta está aderente aos documentos. Se o risco for alto ou a evidência for insuficiente, o sistema recomenda revisão humana.
```

### Explicação de arquitetura AWS

```text
Na POC usei documentos locais e vetor local para ganhar velocidade. Em produção na AWS, eu colocaria documentos no S3, usaria Bedrock Knowledge Bases ou OpenSearch para recuperação vetorial, Amazon Bedrock como camada de LLM, LangGraph rodando em ECS, EKS, Lambda ou SageMaker, APIs internas via API Gateway/Lambda, credenciais em Secrets Manager, criptografia com KMS, permissões via IAM e observabilidade com CloudWatch. Para decisões sensíveis, incluiria human-in-the-loop e trilha de auditoria.
```

---

## 22. O que não falar

Evite dizer:

```text
Tenho experiência profunda em RAG em produção.
Já implementei LangGraph em ambiente bancário.
Esse sistema toma decisão automática.
O LLM decide se aprova ou reprova uma operação.
```

Melhor dizer:

```text
Tenho experiência forte em Data Science, ML, Databricks, PySpark e produtos analíticos, e preparei uma POC prática para consolidar GenAI com RAG, LangGraph, agentes, AWS e validação. Entendo a arquitetura e os cuidados necessários para evoluir isso com segurança em ambiente bancário.
```

---

## 23. Checklist final antes da entrevista

- [ ] O projeto roda localmente.
- [ ] A interface Streamlit funciona.
- [ ] O fluxo LangGraph executa de ponta a ponta.
- [ ] Existem pelo menos 3 documentos de política.
- [ ] A resposta cita evidências.
- [ ] Existe classificação de risco.
- [ ] Risco alto gera human-in-the-loop.
- [ ] Há um README claro.
- [ ] Há um INTERVIEW_NOTES.md.
- [ ] Você consegue desenhar a arquitetura em papel.
- [ ] Você consegue explicar o que mudaria em produção na AWS.
- [ ] Você sabe dizer honestamente o que é POC e o que é experiência real.

---

## 24. Ordem ideal de execução

### Dia 1

- Criar estrutura.
- Rodar Streamlit.
- Criar documentos fictícios.
- Criar tools simuladas.
- Criar LangGraph simples.

### Dia 2

- Adicionar RAG.
- Adicionar risco.
- Adicionar critic agent.
- Adicionar human-in-the-loop.

### Dia 3

- Melhorar README.
- Adicionar testes.
- Treinar explicação.
- Preparar perguntas e respostas.

---

## 25. Perguntas que podem cair

### “Por que LangGraph?”

```text
Porque o problema não é apenas pergunta-resposta. Há etapas, decisões condicionais, ferramentas, validação e possibilidade de revisão humana. LangGraph permite controlar o fluxo, manter estado e separar responsabilidades entre agentes.
```

### “Por que RAG?”

```text
Porque o LLM não deve responder apenas com conhecimento genérico. RAG permite recuperar políticas, procedimentos e documentos internos, reduzindo hallucination e tornando a resposta mais auditável.
```

### “Como reduzir hallucination?”

```text
Usando RAG, instruções para responder apenas com base no contexto, validação crítica, fontes citadas, fallback quando não há evidência, logs e revisão humana em casos sensíveis.
```

### “Como isso iria para produção?”

```text
Eu separaria ingestão documental, indexação vetorial, orquestração dos agentes, APIs internas, autenticação, logs, monitoramento, avaliação, controle de custo, segurança e human-in-the-loop. Na AWS, usaria Bedrock, S3, Knowledge Bases/OpenSearch, IAM, Secrets Manager, KMS e CloudWatch.
```

### “Qual o papel do especialista?”

```text
Receber um problema ambíguo, estruturar arquitetura, construir POC, validar com usuários, medir riscos, documentar decisões, evoluir para produção e atuar com autonomia sem perder governança.
```

---

## 26. Melhor frase para você usar

```text
Minha proposta não é vender um chatbot, mas um fluxo operacional controlado por agentes. O LLM gera linguagem e raciocina sobre contexto, mas o processo é governado por LangGraph, evidências recuperadas por RAG, ferramentas controladas, regras de risco, validação e human-in-the-loop. Essa arquitetura é mais adequada para banco porque permite segurança, explicabilidade e auditoria.
```

---

## 27. Entrega final esperada

Ao final, o repositório deve ter:

```text
1. Código funcionando
2. Interface simples
3. Dados fictícios
4. LangGraph claro
5. RAG simples
6. Ferramentas simuladas
7. Risco e validação
8. README bom
9. INTERVIEW_NOTES.md
10. Discurso pronto para entrevista
```

