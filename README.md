## Técnicas Aplicadas (Fase 2)

- **Role Prompting**
  - Justificativa: define claramente a persona e o contexto do prompt, reduz ambiguidade e orienta o modelo para gerar User Stories no formato esperado.
  - Exemplo prático: o `SystemMessagePromptTemplate` do `bug_to_user_story_v2.yml` apresenta o modelo como um "Analista de Produto Sênior (Product Owner) especializado em times ágeis" e instrui-o a seguir critérios INVEST e gerar critérios de aceitação em Gherkin.

- **Few-shot Learning**
  - Justificativa: exemplos de entrada/saída demonstram o comportamento desejado, alinham o formato e ajudam a reduzir erros de interpretação.
  - Exemplo prático: o prompt otimizado inclui exemplos claros de relatos de bug e a saída esperada com User Story, Critérios de Aceitação e Contexto Técnico.

- **Chain of Thought (CoT)**
  - Justificativa: orienta o modelo a raciocinar passo a passo antes de gerar a saída, melhorando consistência e precisão.
  - Exemplo prático: o prompt solicita um processo interno de análise que identifica ator, classifica o bug, preserva fatos concretos e estrutura a resposta em etapas claras.

- **Tratamento de casos e regras explícitas**
  - Justificativa: regras rígidas evitam respostas vagas, adicionam requisitos de qualidade e garantem que o modelo não replique o relato como texto livre.
  - Exemplo prático: o prompt exige sempre o formato de User Story, critérios Gherkin, preservação de fatos concretos e tratamento condicional de bugs de segurança, UI/responsividade, concorrência e performance.

---

## Resultados Finais

- Dashboard público do LangSmith: (https://smith.langchain.com/public/1543cd55-7a12-4794-bf19-82d6db89b5f1/d)


### Capturas de tela das avaliações

- mba-ia-pull-evaluation-prompt/screenshots/print-langsmith-3.png

### Tabela comparativa: prompt ruim (v1) vs prompt otimizado (v2)

| Item | Prompt v1 | Prompt v2 |
|---|---|---|
| Persona | Assistente genérico | Analista de Produto Sênior / Product Owner |
| Estrutura | Instrução única simples | System/Human claramente separados, meta, regras e exemplos |
| Técnica aplicada | Sem técnica estruturada | Role Prompting, Few-shot, Chain of Thought |
| Saída esperada | Apenas User Story genérica | User Story + Critérios Gherkin + Contexto Técnico + enriquecimento de especialista |
| Tratamento de edge cases | Ausente | Regras explícitas para segurança, UI, performance, concorrência |
| Avaliação | Baixos scores, falta de consistência | Mais alta clareza, precisão e corretude potencial |

---

## Como Executar

### Pré-requisitos

- Python 3.9+ instalado
- Ambiente virtual Python configurado
- API Key do LangSmith (`LANGSMITH_API_KEY`)
- Username do LangSmith Hub (`USERNAME_LANGSMITH_HUB`)
- API Key do provedor LLM escolhido:
  - OpenAI: `OPENAI_API_KEY`
  - Google Gemini: `GOOGLE_API_KEY`
- Arquivo `.env` preenchido a partir de `.env.example`

### Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env` e preencha pelo menos as seguintes variáveis:

- `LANGSMITH_API_KEY`
- `USERNAME_LANGSMITH_HUB`
- `OPENAI_API_KEY` ou `GOOGLE_API_KEY`
- `LLM_PROVIDER` (openai ou google)
- `LLM_MODEL` e `EVAL_MODEL`

### Fases do projeto

1. Pull do prompt v1 do LangSmith:

```bash
python src/pull_prompts.py
```

2. Refatorar o prompt localmente em `prompts/bug_to_user_story_v2.yml`.

3. Publicar o prompt otimizado no LangSmith Hub:

```bash
python src/push_prompts.py
```

4. Executar a avaliação automática:

```bash
python src/evaluate.py
```

5. Validar os testes de prompt:

```bash
pytest tests/test_prompts.py
```

### Dicas extras

- O script `src/evaluate.py` cria/atualiza o dataset de avaliação em LangSmith usando `datasets/bug_to_user_story.jsonl`.
- A avaliação é feita com o prompt disponível no LangSmith Hub, por isso sempre publique após atualizar `prompts/bug_to_user_story_v2.yml`.
- Para capturar os resultados no dashboard, use o `project` configurado em `LANGSMITH_PROJECT` ou o valor padrão `prompt-optimization-challenge-resolved`.

---

## Evidências no LangSmith

#Dashboard público do LangSmith:  
https://smith.langchain.com/public/1543cd55-7a12-4794-bf19-82d6db89b5f1/d

#Screenshots:
mba-ia-pull-evaluation-prompt/screenshots
