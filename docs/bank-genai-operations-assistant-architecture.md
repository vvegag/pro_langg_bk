# Bank GenAI Operations Assistant - Arquitetura da Solução Local

**Objetivo:** mostrar, de forma clara e didática, como a solução local organiza um fluxo operacional com LLM, LangGraph, RAG, validação de risco e revisão humana quando necessário.

Esta solução local demonstra o fluxo completo de um assistente para operações bancárias, com foco em entendimento, rastreabilidade e segurança operacional.

---

## 1. Ideia central

A mensagem principal desta solução é simples:

> um LLM não deve tomar decisões sensíveis sozinho em um contexto bancário.

O fluxo foi organizado para que cada etapa tenha uma responsabilidade explícita:

```text
Entrada do usuário / analista operacional
        ↓
LangGraph orquestra o fluxo
        ↓
Classificação de intenção
        ↓
Busca de contexto em documentos internos via RAG
        ↓
Consulta de ferramenta ou dados simulados
        ↓
Classificação de risco operacional
        ↓
Validação de necessidade de revisão humana
        ↓
Resposta final estruturada com evidências
```

---

## 2. O que esta solução local precisa demonstrar

A solução foi desenhada para evidenciar:

1. Uso de LLM para interpretar e redigir respostas.
2. Uso de LangGraph para controlar o fluxo de execução.
3. Uso de RAG para recuperar políticas e orientações internas.
4. Uso de ferramentas simuladas para consultar dados operacionais.
5. Validação de risco antes de recomendar qualquer ação.
6. Resposta com contexto, evidências e linguagem clara.
7. Revisão humana em casos sensíveis.
8. Organização suficiente para facilitar explicação técnica em entrevista ou apresentação.

---

## 3. Fluxo lógico

```text
Streamlit
   |
   v
LangGraph
   |
   |-- Nó 1: Classificação de intenção
   |-- Nó 2: Recuperação de contexto
   |-- Nó 3: Consulta de dados simulados
   |-- Nó 4: Avaliação de risco
   |-- Nó 5: Validação humana, se necessário
   |-- Nó 6: Resposta final
   |
   v
Modelo de linguagem via AWS Bedrock
```

Essa estrutura permite separar decisão, contexto e resposta. Isso deixa a lógica mais fácil de entender e de evoluir.

---

## 4. Arquitetura atual da solução local

### Interface

- `app.py` recebe a solicitação do usuário.
- A interface é feita em Streamlit.
- O usuário executa a consulta e vê o resultado final na tela.

### Orquestração

- `src/graph.py` organiza o fluxo com nós e decisões.
- Cada nó executa uma etapa específica.
- O estado da execução é passado de uma etapa para outra.

### Modelo de linguagem

- `src/llm.py` centraliza a integração com o modelo.
- A lógica de acesso ao Bedrock fica isolada para facilitar manutenção.

### RAG

- `src/rag.py` lê os documentos em `data/politicas/`.
- O módulo divide os textos em partes menores e busca os trechos mais relevantes.

### Ferramentas simuladas

- `src/tools.py` contém dados simulados de cliente, transação e regra de risco.
- Essa camada substitui integrações reais durante a POC.

---

## 5. Estrutura de pastas

```text
pro_langg_bk/
├── app.py
├── src/
│   ├── settings.py
│   ├── llm.py
│   ├── graph.py
│   ├── rag.py
│   └── tools.py
├── data/
│   └── politicas/
├── docs/
│   ├── bank-genai-operations-assistant-architecture.md
│   ├── bank-genai-operations-assistant-concepts.md
│   ├── bank-genai-operations-assistant-interview-notes.md
│   └── bank-genai-operations-assistant-methodology.md
├── requirements.txt
├── .env.example
└── README.md
```

---

## 6. O que já está pronto

- Interface Streamlit funcional.
- Configurações separadas em `src/settings.py`.
- Integração com modelo centralizada em `src/llm.py`.
- Recuperação documental em `src/rag.py`.
- Regras e dados simulados em `src/tools.py`.
- Fluxo coordenado em `src/graph.py`.
- Documentação em português e com foco didático.

---

## 7. O que pode evoluir depois

- Logs estruturados.
- Métricas de execução.
- Integração com APIs reais.
- Persistência de histórico.
- Avaliação automática de qualidade das respostas.
- Autenticação e controle de acesso.

---

## 8. Resumo executivo

Esta solução local foi construída para mostrar como combinar LLM, LangGraph, RAG e validação de risco em um fluxo operacional bancário controlado. O objetivo não é substituir sistemas reais, mas demonstrar domínio técnico com uma arquitetura clara, explicável e segura.
