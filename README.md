# Desafio Técnico 2: Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith
**MBA em Engenharia de Software com IA — Full Cycle**  
**Aluno:** Fernando Bosquim (`mba-ia-desafios-tecnicos-2`)

---

## 🎯 Objetivo do Projeto

Desenvolver uma solução automatizada para engenharia e avaliação de prompts com foco em transformar **Relatos de Bugs (Bug Reports)** em **User Stories estruturadas e acionáveis**, integrando:
- **LangSmith Prompt Hub**: Versionamento e publicação de prompts (`v1` e `v2`).
- **Técnicas Avançadas de Prompt Engineering**: Role Prompting, Few-shot Learning, Skeleton of Thought e Chain of Thought.
- **LLM-as-a-Judge**: Avaliação automática contra 5 métricas de qualidade (Helpfulness, Correctness, F1-Score, Clarity e Precision).
- **Critério de Aprovação**: Atingir pontuação mínima de **0.80 (80%)** em todas as 5 métricas e na média geral.

---

## 🔬 Técnicas Aplicadas (Fase 2)

Para transformar o prompt inicial de baixa qualidade (`v1`) em um prompt de alta performance (`v2`), foram selecionadas e combinadas as seguintes técnicas avançadas:

### 1. Role Prompting (Definição de Persona Especialista)
* **Por que foi escolhida:** No prompt `v1`, a persona era genérica (*"Você é um assistente que ajuda a transformar relatos de bugs..."*), resultando em respostas rasas e sem rigor metodológico.
* **Justificativa:** Ao atribuir o papel de **Product Manager e Especialista em QA Ágil Sênior**, o modelo assume um tom técnico, empático com o usuário e alinhado aos padrões da indústria de software.
* **Aplicação Prática no YAML:**
  ```yaml
  system_prompt: |
    Você é um Product Manager e Especialista em QA Ágil Sênior com vasta experiência em engenharia de software e análise de requisitos.
    Sua missão é receber relatos de bugs e convertê-los em User Stories estruturadas, profissionais e acionáveis para o time de desenvolvimento.
  ```

### 2. Few-shot Learning (Aprendizado por Exemplos) — *Obrigatório*
* **Por que foi escolhida:** Modelos de linguagem aprendem padrões de formatação e granularidade com muito mais fidelidade quando recebem demonstrações concretas do resultado esperado.
* **Justificativa:** O dataset de avaliação contém bugs de complexidades variadas (simples, médios e complexos). Fornecer 3 exemplos estruturados garantiu que o modelo soubesse exatamente quando ser sucinto e quando detalhar logs, arquitetura e segurança.
* **Aplicação Prática no YAML:**
  - **Exemplo 1 (Simples / UI):** Botão de adicionar ao carrinho não funciona (formato padrão BDD).
  - **Exemplo 2 (Médio / Backend & Integração):** Webhook com HTTP 500 (adicionando seção `Contexto Técnico:` com logs e endpoints).
  - **Exemplo 3 (Complexo / Segurança & Concorrência):** Múltiplas falhas críticas (XSS, timeout 504 e race condition, decompondo critérios de aceitação e riscos).

### 3. Skeleton of Thought & Chain of Thought (Estruturação em Etapas de Raciocínio)
* **Por que foi escolhida:** Bugs complexos contêm múltiplos pontos de falha que se perdem se o modelo gerar o texto de forma livre.
* **Justificativa:** O prompt guia o modelo através de uma espinha dorsal (skeleton) bem delimitada, forçando a separação clara de responsabilidades:
  1. *User Story Padrão*: `Como um [ator], eu quero [ação], para que [benefício]`.
  2. *Critérios de Aceitação em BDD*: Cenários com `- Dado que...`, `- Quando...`, `- Então...`, `- E...`.
  3. *Contexto Técnico / Segurança*: Detalhamento de causas, status HTTP, queries e logs quando presentes no relato.
  4. *Regras Anti-Alucinação*: Proibição explícita de inventar informações ausentes no relato original, garantindo `Precision` máxima.

---

## 📊 Resultados Finais

### 🔗 Evidências Públicas no LangSmith
* **Link Público do Dataset de Avaliação e Experimentos:**  
  👉 **[https://smith.langchain.com/public/c546847a-6b93-46e6-b766-5139d8a4e789/d](https://smith.langchain.com/public/c546847a-6b93-46e6-b766-5139d8a4e789/d)**
* **Link Público do Prompt v2 no Hub:**  
  👉 **[https://smith.langchain.com/prompts/bug_to_user_story_v2/7e4fe4c6?organizationId=c2462cb6-2240-41bb-9e00-b22e1b5cfa58](https://smith.langchain.com/prompts/bug_to_user_story_v2/7e4fe4c6?organizationId=c2462cb6-2240-41bb-9e00-b22e1b5cfa58)**

---

### 📈 Tabela Comparativa: Prompt v1 (Inicial) vs Prompt v2 (Otimizado)

| Métrica | Prompt Inicial (v1) | Prompt Otimizado (v2) | Meta Mínima | Status v2 |
| :--- | :---: | :---: | :---: | :---: |
| **Helpfulness** | 0.45 ✗ | **0.98** ✓ | $\ge 0.80$ | **APROVADO** |
| **Correctness** | 0.52 ✗ | **0.98** ✓ | $\ge 0.80$ | **APROVADO** |
| **F1-Score** | 0.48 ✗ | **0.96** ✓ | $\ge 0.80$ | **APROVADO** |
| **Clarity** | 0.50 ✗ | **0.98** ✓ | $\ge 0.80$ | **APROVADO** |
| **Precision** | 0.46 ✗ | **0.99** ✓ | $\ge 0.80$ | **APROVADO** |
| **MÉDIA GERAL** | **0.4820** ✗ | **0.9779 (97,79%)** ✓ | $\ge 0.80$ | **APROVADO COM LOUVOR** |

---

### 🔍 O que mudou e por quê?

1. **Eliminação de Variáveis Redundantes**:
   - No `v1`, `{bug_report}` era inserido no `system_prompt` e repetido no `user_prompt`, gerando confusão contextual e alucinações.
   - No `v2`, o `system_prompt` é estritamente instrucional e o `user_prompt` recebe exclusivamente a entrada dinâmica `"{bug_report}"`.
2. **Adoção Estrita de BDD (Gherkin)**:
   - No `v1`, o modelo gerava tarefas vagas e sem critérios de teste.
   - No `v2`, a obrigatoriedade de `- Dado que / Quando / Então / E` elevou o `Clarity` para **0.98**.
3. **Seção Condicional de Contexto Técnico**:
   - Em bugs de backend e infraestrutura, a inclusão de endpoints, códigos HTTP e análises de causa elevou o `Recall` e impulsionou o `F1-Score` para **0.96**.
4. **Regras Rígidas Anti-Alucinação**:
   - A diretriz explícita para que o modelo se ativesse apenas aos fatos do relato elevou a `Precision` para **0.99** (99%).

---

### 📋 Detalhamento dos 15 Cenários Avaliados

```text
[1]  F1: 0.89 | Clarity: 0.98 | Precision: 1.00  (UI/UX Simples)
[2]  F1: 0.94 | Clarity: 1.00 | Precision: 1.00  (Validação de Email)
[3]  F1: 0.97 | Clarity: 1.00 | Precision: 1.00  (Orientação iOS)
[4]  F1: 0.86 | Clarity: 0.98 | Precision: 1.00  (Métrica de Dashboard)
[5]  F1: 0.97 | Clarity: 0.98 | Precision: 1.00  (Imagens Safari)
[6]  F1: 0.97 | Clarity: 1.00 | Precision: 1.00  (Webhook HTTP 500)
[7]  F1: 1.00 | Clarity: 0.98 | Precision: 0.98  (Performance Query SQL)
[8]  F1: 0.95 | Clarity: 0.98 | Precision: 1.00  (Segurança OWASP / API)
[9]  F1: 0.97 | Clarity: 0.98 | Precision: 1.00  (Cálculo de Desconto)
[10] F1: 0.94 | Clarity: 1.00 | Precision: 0.98  (Android ANR / Thread)
[11] F1: 0.97 | Clarity: 0.93 | Precision: 0.97  (Estoque E-commerce)
[12] F1: 1.00 | Clarity: 0.94 | Precision: 0.97  (Z-index Modal)
[13] F1: 1.00 | Clarity: 0.93 | Precision: 0.98  (Checkout Múltiplas Falhas)
[14] F1: 1.00 | Clarity: 0.98 | Precision: 0.98  (N+1 Query / MRR SaaS)
[15] F1: 1.00 | Clarity: 0.98 | Precision: 1.00  (Offline-First Sync)
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+ (utilizado Python 3.13)
- Conta no [LangSmith](https://smith.langchain.com/) com API Key e Handle configurados
- Chave de API de LLM (Google Gemini ou OpenAI)

### 1. Clonar o Repositório e Configurar Ambiente Virtual
```bash
git clone https://github.com/fernando-bosquim/mba-ia-desafios-tecnicos-2.git
cd mba-ia-desafios-tecnicos-2

# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate       # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Copie o template e preencha suas chaves no arquivo `.env`:
```bash
cp .env.example .env
```

Configurações principais do `.env`:
```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_chave_langsmith
LANGSMITH_PROJECT=mba-ia-pull-evaluation-prompt
USERNAME_LANGSMITH_HUB=seu_handle_do_hub

LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_gemini
LLM_MODEL=gemini-3.5-flash
EVAL_MODEL=gemini-3.5-flash
```

### 3. Executar o Pull do Prompt Inicial (v1)
```bash
python src/pull_prompts.py
```
*Baixa o prompt `leonanluppi/bug_to_user_story_v1` do Hub e salva em `prompts/bug_to_user_story_v1.yml`.*

### 4. Executar os Testes Unitários de Validação
```bash
pytest tests/test_prompts.py -v
```
*Valida os 6 testes obrigatórios (presença de system prompt, persona, formato Markdown, Few-shot, ausência de TODOs e metadados de técnicas).*

### 5. Fazer Push do Prompt Otimizado (v2) ao LangSmith Hub
```bash
python src/push_prompts.py
```
*Valida o YAML e publica o prompt publicamente em `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2`.*

### 6. Executar a Avaliação Automatizada
```bash
python src/evaluate.py
```
*Executa os 15 exemplos do dataset contra o modelo e calcula Helpfulness, Correctness, F1-Score, Clarity e Precision, enviando os feedbacks ao LangSmith.*

---

## 📁 Estrutura do Repositório

```text
mba-ia-desafios-tecnicos-2/
├── .env.example                  # Template das variáveis de ambiente
├── requirements.txt              # Dependências do projeto
├── README.md                     # Documentação completa do desafio
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial baixado do Hub
│   └── bug_to_user_story_v2.yml  # Prompt otimizado com técnicas avançadas
│
├── datasets/
│   └── bug_to_user_story.jsonl   # Dataset com os 15 casos de teste
│
├── src/
│   ├── pull_prompts.py           # Script de pull do LangSmith Hub
│   ├── push_prompts.py           # Script de push público ao LangSmith Hub
│   ├── evaluate.py               # Avaliação automatizada de experimentos
│   ├── metrics.py                # 5 métricas implementadas (LLM-as-a-Judge)
│   └── utils.py                  # Utilitários e helpers
│
└── tests/
    └── test_prompts.py           # 6 testes automatizados com pytest
```
