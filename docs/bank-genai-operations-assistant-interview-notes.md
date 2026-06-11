# Bank GenAI Operations Assistant - Perguntas e Respostas

Este material reúne respostas curtas para ajudar a explicar a solução de forma objetiva.

---

## 1. Por que usar LangGraph?

Porque a solução não é apenas pergunta e resposta. Ela precisa de etapas: interpretar a solicitação, buscar evidências, consultar dados, avaliar risco e decidir se o caso pode seguir sozinho ou se precisa de revisão humana.

---

## 2. Por que usar RAG?

Porque a resposta precisa considerar políticas internas e não apenas o que o modelo “lembra”. O RAG reduz alucinação e deixa a resposta mais sustentada por evidências.

---

## 3. Por que o LLM não deve agir sozinho?

Porque em um contexto bancário existe risco operacional. O modelo ajuda a interpretar e redigir, mas a decisão precisa passar por regras, evidências e, em casos sensíveis, revisão humana.

---

## 4. O que o Bedrock faz aqui?

Ele é a camada de acesso ao modelo de linguagem na AWS. Isso aproxima a solução de uma arquitetura mais realista e facilita evolução futura.

---

## 5. Por que o modelo pode ser trocado depois?

Porque a arquitetura foi desenhada para manter o fluxo separado do provedor. Assim, trocar o modelo exige menos mudança estrutural.

---

## 6. O que acontece se uma dependência não estiver disponível?

A solução pode usar um plano de contingência local para continuar executável e facilitar o desenvolvimento incremental.

---

## 7. Como as responsabilidades foram separadas no código?

- `app.py` cuida da interface.
- `src/graph.py` cuida do fluxo.
- `src/rag.py` cuida da busca em documentos.
- `src/llm.py` cuida da chamada ao modelo.
- `src/tools.py` cuida dos dados simulados e da regra de risco.

---

## 8. O que a solução demonstra?

Ela demonstra organização de um fluxo de GenAI com controle, evidência, validação e linguagem adequada para um contexto operacional bancário.

---

## 9. Como resumir a solução em uma frase?

“A solução local demonstra um assistente operacional bancário que combina LangGraph, RAG, LLM e validação de risco para apoiar decisões com mais contexto e controle.”
