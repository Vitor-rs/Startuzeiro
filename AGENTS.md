# Regras Operacionais do Startuzeiro

## 1. Princípio Fundamental

- A infraestrutura deve ser menor que a pesquisa.
- Todo conhecimento deve ser registrado em Markdown + metadados YAML.

## 2. Atalho de Transcrição do YouTube (`/ <link>`)

Sempre que o usuário enviar uma mensagem começando ou contendo `/ <link_do_youtube>` (ou `/yt <link>`):

1. Execute imediatamente no terminal:

   ```bash
   uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<link>"
   ```

2. Este script salva a transcrição no lake em `yt_base/yt_lake/<titulo_normalizado>.md` (sem acentos, 'ç' -> 'c', espaços virando '_') e atualiza a tabela de catálogo em `yt_base/README.md`.
3. Retorne a resposta ao usuário com os links clicáveis do arquivo gerado e do catálogo.

## 3. Consulta de Documentações com Context7

Sempre que surgirem dúvidas de APIs, bibliotecas, SDKs modernos ou configurações (React, Next.js, Prisma, Tailwind, FastAPI, etc.), utilize o **Context7** para obter documentação oficial em tempo real sem alucinações:
- Via CLI:
  ```bash
  npx ctx7@latest library <nome_da_lib> "<o_que_procura>"
  npx ctx7@latest docs <library_id> "<conceito_especifico>"
  ```
- Via MCP: Ferramentas `resolve-library-id` e `query-docs`.

## 4. Busca Semântica e Pesquisa Profunda com Exa

Para pesquisas de mercado, inteligência de concorrentes, descoberta de leads e recuperação semântica na web, utilize o **Exa**:
- Via MCP:
  - `web_search_exa`: busca web rápida em linguagem natural.
  - `web_fetch_exa`: extração e leitura de páginas a partir de URLs.
  - `web_search_advanced_exa`: busca avançada com filtros de domínio, datas e categorias.
  - `agent_run`: pesquisa autônoma em múltiplos passos com enriquecimento e saída estruturada.
- Via Skills (`.agents/skills/`): `company-research`, `lead-generation`, `exa-search`, `exa-contents`, `build-with-exa`.

## 5. Investigação Societária e Inteligência de Empresas com cnpj.ai

Para due diligence de empresas brasileiras, análise de sócios, QSA, grupos econômicos e dívida ativa da PGFN, utilize o **cnpj.ai**:
- Via MCP:
  - `investigar_empresa`: investigação cadastral e societária completa em 1 chamada (situação, QSA, dívida ativa, vínculos ocultos).
  - `empresas_do_socio`: descobre todas as empresas de um sócio pessoa física.
  - `rede_societaria`: mapeia relacionamentos societários em até 3 níveis.
  - `vinculos_ocultos`: identifica empresas com mesmo e-mail ou telefone cadastrado.
  - `encontrar_conexao`: menor caminho societário entre dois CNPJs.
  - `listar_empresas` & `buscar_cnae`: prospecção e filtragem de empresas por CNAE e região.
  - `panorama_empresarial`: estatísticas e contagens de mercado por UF/município.
- Via Skill (`.agents/skills/`): `cnpj-ai-research`.
- Sempre inclua os links do grafo interativo (`https://grafo.cnpj.ai/?q=<cnpj_basico>`) nos relatórios.

## 6. Prospecção B2B, Descoberta de E-mails e Enriquecimento com Hunter.io

Para encontrar tomadores de decisão, mapear contatos por domínio corporativo, verificar entregabilidade de e-mails e estruturar listas de leads, utilize o **Hunter.io**:
- Via MCP:
  - `Domain-Search`: lista e-mails e contatos de uma empresa a partir do domínio (com filtros de departamento e senioridade).
  - `Email-Finder`: descobre o e-mail exato de um executivo com base em nome completo e domínio.
  - `Email-Verifier`: valida entregabilidade (MX, SMTP, score e risco de bounce).
  - `Find-Companies`: descoberta gratuita de empresas por nicho/setor (0 créditos).
  - `Email-Count`: contagem gratuita de e-mails em um domínio antes de gastar créditos.
  - `Person-Enrichment` / `Company-Enrichment`: enriquecimento de dados a partir de e-mail ou domínio.
  - `Create-Lead` / `Create-Lead-If-Missing`: salva contatos diretamente na conta do Hunter.
- Via Skill (`.agents/skills/`): `hunter-b2b-intel`.
- Lembre-se: o plano Free possui 50 créditos/mês. Sempre use `Email-Count` e `Find-Companies` gratuitamente antes de executar buscas intensivas.

## 7. Inteligência de Vendas e Prospecção Global com Apollo.io

Para busca de decisores internacionais por ICP, enriquecimento de contatos com telefones diretos e e-mails, análise de vagas abertas e automação de cadências de vendas, utilize o **Apollo.io**:
- Via MCP:
  - `apollo_search_people` / `apollo_mixed_people_api_search`: busca decisores por cargo, hierarquia e localização.
  - `apollo_search_organizations` / `apollo_mixed_companies_search`: prospecção de contas e empresas.
  - `apollo_get_job_postings`: sinais de intenção de compra através de vagas ativas da empresa.
  - `apollo_enrich_person` & `apollo_people_match`: revela e-mails e telefones diretos (consome créditos).
  - `apollo_enrich_organization`: dados firmográficos e tecnográficos completos da empresa.
  - `apollo_create_contacts` & `apollo_add_contacts_to_sequence`: cadastra leads e matricula em sequências de cold mail.
- Via Skill (`.agents/skills/`): `apollo-sales-intel`.
- Lembre-se: Enriquecimento consome créditos do Apollo. Sempre apresente a lista de prospectos encontrados para aprovação antes de executar chamadas de enriquecimento de contatos.

## 8. Inteligência GTM, Enriquecimento em Cascata e Busca Avançada com Clay

Para buscas estruturadas no banco global de 75M+ empresas e pessoas, enriquecimento com 150+ provedores e orquestração de rotinas, utilize o **Clay**:
- Via CLI (`clay_client.py`):
  - Consultar empresas: `uv run scripts/utilitarios/clay_client.py search "select from companies where industry = 'Software Development' limit 5"`
  - Consultar decisores atuais: `uv run scripts/utilitarios/clay_client.py search 'select from people where experiences.any(is_current = true and job_title is_similar_to ("CTO"))' --limit 5`
  - Consultar catálogo e gramática: `uv run scripts/utilitarios/clay_client.py reference`
  - Disparar rotinas: `uv run scripts/utilitarios/clay_client.py routine <routine_id> '<payload_json>'`
- Via MCP:
  - Conectado em `https://api.clay.com/v3/mcp` via header `clay-api-key`.
- Via Skill (`.agents/skills/` e `.agent/skills/`): `clay-gtm-intel`.
- Lembre-se: Use a busca cruzada do Clay (`experiences.any(...)`, `people.exists(...)`, `technographics.any(...)`) para qualificação fina de ICP antes de enriquecer dados via Hunter e Apollo.

## 9. Descoberta de Modelos, Datasets e Papers com Hugging Face Hub MCP

Para pesquisa e descoberta de modelos abertos, datasets para fine-tuning/análise, papers do arXiv e Spaces interativos, utilize o **Hugging Face Hub**:
- Via MCP:
  - `hub_repo_search`: busca modelos, datasets e spaces por query e tipo.
  - `hub_repo_details`: inspeciona metadados completos de repositórios no Hub.
  - `hf_fs`: navega no sistema de arquivos virtual (`ls hf://models/trending`, `ls hf://papers/daily/latest`, `cat hf://models/<owner>/<repo>/README.md`).
  - `hf_whoami`: checa autenticação e quotas.
- Via Skill (`.agents/skills/` e `.agent/skills/`): `huggingface-hub`.
- Lembre-se: O servidor oficial roda em `https://huggingface.co/mcp`. Sempre priorize modelos com licença comercial aberta (Apache 2.0, MIT) e formatos otimizados (GGUF, ONNX).

## 10. Ingestão de Documentos e Análise Analítica Local (DuckDB, NetworkX, MarkItDown)

Para manter a premissa de que a infraestrutura deve ser menor que a pesquisa:
- **Ingestão de Decks & Documentos**: Use `uv run scripts/utilitarios/doc_to_markdown.py "<arquivo>"` para converter PDFs, DOCX, XLSX e PPTX diretamente em Markdown no Lake com metadados YAML.
- **Análises SQL In-Process**: Use `duckdb` (`uv run scripts/utilitarios/duckdb_query.py`) para cruzar arquivos CSV, Parquet e JSON sem subir servidores pesados de banco.
- **Grafos Societários & Conexões**: Use `networkx` (`uv run scripts/utilitarios/graph_networkx.py`) para modelar redes de sócios/empresas, identificar menor caminho societário, detectar grupos econômicos e exportar visualizações interativas em HTML (`export-html`).
- **Monitoramento Web Concorrentes**: Use `changedetection.io` (`scripts/utilitarios/start_changedetection.bat`) para monitorar alterações visuais e textuais em sites e termos.

## 11. Arquitetura do Segundo Cérebro (C.O.D.E. + P.A.R.A.) & 4-Folders

O repositório é governado pelos modelos mentais do **Agent Development Kit**, **P.A.R.A.** e **4-Folder Structure**:
- **`prompts/`**: Prompts versionados como código (`system/`, `tasks/`, `tools/`).
- **`data/`**: Entradas brutas e processadas (`raw/`, `processed/`).
- **`.agents/`**: Suíte de agentes, skills (41 módulos) e guardrail hooks.
- **`evals/`**: Rubricas de avaliação ICE (`scorecards/`), telemetria (`traces/`) e testes (`tests/`).
- **`brain/`**: O Segundo Cérebro:
  - `01_oportunidades/`: Projetos ativos com prazos e hipóteses falseáveis nos 4 vetores de monetização.
  - `02_pesquisas/`: Áreas de inteligência contínua (dossiês 360° de concorrentes e panoramas de nicho).
  - `03_recursos/`: Acervo de referência (transcrições do YouTube Lake, catálogo master e modelos mentais).
  - `04_arquivo/`: Memória fria de investigações e testes finalizados.

## 12. Os 4 Vetores de Monetização na Internet

Toda oportunidade de negócio descoberta pelo agente deve ser enquadrada e avaliada pela ótica dos 4 vetores:
1. **Agência de Automação de IA (AAA)**: Venda de serviços B2B de alto ticket (R$ 1.500 a R$ 10.000) automatizando speed-to-lead e qualificação no WhatsApp (Hunter + Clay + Evolution API/n8n).
2. **Micro-SaaS & Wrappers Agênticos**: Criação de ferramentas leves com receita recorrente (MRR R$ 97 a R$ 497/mês) resolvendo dores específicas com IA local e DuckDB.
3. **Afiliação High-Ticket & Arbitragem**: Mapeamento de programas de afiliados com comissões de R$ 150 a R$ 800/venda e produção de páginas comparativas capturando tráfego de alta intenção comercial.
4. **Máquina de Conteúdo & Dark Media**: Repurposing de transcrições de mentorias em 20 micro-ativos virais (carrosséis, scripts de shorts, threads) para monetização com audiência.

## 13. O Motor Autônomo de Inteligência Agêntica (`scripts/agentic_brain.py`)

Para rodar a mineração autônoma de mercado:
- Mineração de transcrições e síntese de oportunidades:
  ```bash
  uv run scripts/agentic_brain.py mine
  ```
- Exportação do grafo de conexões de mercado:
  ```bash
  uv run scripts/agentic_brain.py graph
  ```
- Painel Web Unificado: Execute `abrir_painel.bat` e acesse a aba **"🧠 Cérebro Agêntico"** em `http://localhost:5050`.

