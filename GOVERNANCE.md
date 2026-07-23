# Governança da POC

Esta POC demonstra um fluxo de apoio operacional com GenAI em contexto bancário. Ela não executa ações financeiras, não usa dados reais de clientes e não substitui decisão humana em casos sensíveis.

## Princípios

- **Dados fictícios:** todos os clientes, valores e documentos são simulados.
- **Minimização:** logs locais evitam armazenar texto livre completo do usuário.
- **Rastreabilidade:** a execução registra intenção, risco, necessidade de revisão humana e fontes recuperadas.
- **Human-in-the-loop:** risco alto ou evidência insuficiente exige revisão humana.
- **Não automação de decisão crítica:** o LLM apoia análise e redação, mas não aprova, bloqueia ou executa operações.
- **Separação de responsabilidades:** RAG, regras de risco, LLM, fluxo e interface ficam em módulos separados.

## Controles Implementados

- Recuperação de evidências em `data/politicas/`.
- Classificação determinística de risco em `src/tools.py`.
- Roteamento explícito para revisão humana em `src/graph.py`.
- Integração Bedrock isolada em `src/llm.py`.
- Logs estruturados em JSONL, quando habilitados.
- Testes de smoke e comportamento em `tests/`.

## Limitações

- A base documental é pequena e fictícia.
- A busca RAG local é lexical e simples.
- A ferramenta transacional é simulada.
- Não há autenticação, autorização ou segregação de perfis.
- Não há integração real com sistemas bancários.
- Não há avaliação formal de factualidade por LLM judge.

## Evolução Para Produção

Em ambiente corporativo, a solução exigiria:

- IAM, KMS e Secrets Manager para segurança.
- S3 e Bedrock Knowledge Bases ou OpenSearch para RAG gerenciado.
- API autenticada e segregação de acesso.
- Logs centralizados no CloudWatch.
- Monitoramento de custo, latência e qualidade.
- Versionamento de prompts, documentos e regras.
- Processo formal de aprovação humana para casos sensíveis.
