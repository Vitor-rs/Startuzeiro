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

