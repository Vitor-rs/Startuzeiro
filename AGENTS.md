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



