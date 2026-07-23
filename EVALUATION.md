# Avaliação Da POC

A avaliação desta POC é simples e determinística. Ela não mede qualidade linguística profunda, mas verifica se os comportamentos mínimos esperados continuam funcionando.

## Critérios

Cada caso em `evals/casos_teste.jsonl` possui:

- `customer_id`
- `question`
- `expected_risk`
- `expected_human_review`

O script compara:

- risco retornado pelo fluxo;
- necessidade de revisão humana;
- quantidade de evidências recuperadas.

## Como Rodar

```bash
python -m evals.run_eval
```

Saída esperada:

```text
id,risk_ok,human_review_ok,evidence_count
alto_fraude,True,True,3
...
score,8/8
```

## Por Que Isso Importa

Em GenAI aplicada a banco, não basta a resposta "parecer boa". O fluxo precisa manter comportamentos controlados:

- risco alto exige revisão humana;
- casos simples não devem ser escalados sem motivo;
- a resposta deve ser apoiada por evidências;
- o sistema não deve executar ação financeira automaticamente.

## Evolução Futura

Uma versão mais robusta poderia incluir:

- avaliação de groundedness;
- verificação automática de citação de fontes;
- testes de regressão para prompts;
- métricas de latência e custo;
- LLM-as-judge com rubricas controladas;
- dataset maior com cenários de fraude, cadastro, atendimento e contestação.
