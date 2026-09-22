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


