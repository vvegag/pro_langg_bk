# Bank GenAI Operations Assistant - Guia de Conceitos

Este documento explica, em linguagem simples, os conceitos usados na solução local e como eles aparecem no código.

---

## 1. LLM

Um LLM é o modelo que interpreta linguagem natural e gera texto.

Na solução:

- ajuda a entender a solicitação;
- ajuda a montar a resposta final;
- pode apoiar classificações simples quando o fluxo precisar.

Cuidados importantes:

- ele pode errar;
- ele pode inventar detalhes;
- por isso precisa de contexto, regras e validação.

---

## 2. Prompt

Prompt é a instrução enviada ao modelo.

Na prática, um bom prompt deve definir:

- o papel do modelo;
- o contexto da tarefa;
- o formato da resposta;
- o que não deve ser feito.

Na solução local, prompts curtos funcionam bem para classificação, enquanto prompts mais completos funcionam melhor na resposta final.

---

## 3. RAG

RAG significa Retrieval-Augmented Generation.

A ideia é:

1. buscar contexto em documentos;
2. enviar esse contexto ao modelo;
3. gerar a resposta com base nas evidências recuperadas.

Na solução:

- os documentos ficam em `data/politicas/`;
- `src/rag.py` faz a leitura e a busca;
- o contexto recuperado entra no fluxo antes da resposta final.

Por que isso é importante:

- reduz alucinação;
- aproxima a resposta das políticas internas;
- melhora a rastreabilidade.

---

## 4. Embeddings

Embeddings transformam texto em vetores numéricos.

Isso permite comparar trechos de texto por similaridade.

Na solução:

- embeddings podem ajudar a localizar trechos relevantes;
- se um caminho mais simples for necessário, o projeto pode usar busca lexical como plano de contingência.

---

## 5. Vector Store

Vector store é o armazenamento dos vetores usados na busca.

Na prática, ele serve para:

- guardar representações numéricas dos documentos;
- buscar os trechos mais próximos da pergunta do usuário;
- acelerar a recuperação de contexto.

---

## 6. LangGraph

LangGraph organiza o fluxo em nós e conexões.

Na solução, cada nó representa uma etapa:

- classificar intenção;
- recuperar contexto;
- consultar dados simulados;
- avaliar risco;
- decidir revisão humana;
- gerar resposta final.

Por que usar:

- o fluxo não é apenas pergunta e resposta;
- há decisões intermediárias;
- cada etapa pode ser auditada.

---

## 7. Revisão humana

Revisão humana significa que um caso sensível deve ser analisado por uma pessoa antes de qualquer ação.

Na solução:

- risco alto aciona revisão humana;
- falta de evidência também pode acionar revisão.

Isso é importante porque:

- reduz erro operacional;
- evita ação automática indevida;
- combina melhor com o contexto bancário.

---

## 8. Amazon Bedrock

Amazon Bedrock é a camada de acesso aos modelos de linguagem na AWS.

Na solução:

- `src/llm.py` concentra a chamada ao modelo;
- `src/rag.py` pode usar embeddings compatíveis com a pilha AWS.

Por que faz sentido:

- deixa a arquitetura mais próxima de produção;
- facilita o discurso técnico com foco em AWS;
- ajuda a manter a integração com o provedor centralizada.

---

## 9. Por que o modelo pode ser trocado depois

A escolha do modelo é uma decisão de configuração, não o centro da arquitetura.

Isso significa que a solução pode, no futuro:

- usar outro modelo para classificação;
- usar outro modelo para resposta final;
- manter o mesmo fluxo de LangGraph e o mesmo RAG.

Esse desacoplamento é importante porque evita redesenhar tudo quando o provedor muda.

---

## 10. Regras de risco

As regras de risco classificam a operação como baixo, médio ou alto risco.

Na solução:

- `src/tools.py` contém a regra;
- `src/graph.py` usa essa classificação para decidir a sequência do fluxo.

Por que isso existe:

- nem toda solicitação deve virar ação automática;
- o nível de risco define o comportamento do sistema.

---

## 11. Fallback

Fallback é um plano alternativo quando uma dependência falha.

Na solução local:

- se a chamada ao modelo não estiver disponível, o projeto pode retornar erro claro;
- se o fluxo principal falhar, a aplicação pode continuar de forma mais simples;
- se a busca vetorial não funcionar, a recuperação pode cair para uma alternativa lexical.

Isso ajuda porque:

- permite desenvolvimento incremental;
- facilita testes;
- evita travar a demonstração por completo.

---

## 12. Como ler o código

Ordem sugerida:

1. `README.md`
2. `src/settings.py`
3. `src/tools.py`
4. `src/rag.py`
5. `src/llm.py`
6. `src/graph.py`
7. `app.py`

---

## 13. O que memorizar para explicar a solução

- LLM gera texto, mas precisa de contexto e validação.
- RAG reduz alucinação.
- LangGraph controla o fluxo.
- Risco alto exige revisão humana.
- Bedrock entra como camada de modelo na AWS.

