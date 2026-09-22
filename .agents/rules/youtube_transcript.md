---
trigger: always_on
---

# Regra de Automação: Transcrição Rápida de YouTube (/ <link>)

Quando o usuário digitar uma mensagem que contenha ou comece com barra `/` seguida de um link ou ID do YouTube (por exemplo: `/ https://www.youtube.com/watch?v=...`, `/ https://youtu.be/...`, ou `/yt <link>`):

### Ação Automática Obrigatória:
1. Execute imediatamente o comando:
   ```bash
   uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<link>"
   ```
2. O script irá:
   - Extrair a transcrição completa com timestamps via TranscriptAPI.
   - Normalizar o título do vídeo para o nome do arquivo (`yt_base/yt_lake/<nome_normalizado>.md`), convertendo espaços em `_`, removendo acentos (`ç` -> `c`, etc.) e caracteres especiais.
   - Gerar metadados completos (Canal, Data de Publicação, Visualizações, Assunto Resumido).
   - Atualizar a tabela de catálogo central em `yt_base/README.md`.
3. Responda ao usuário confirmando a transcrição com:
   - Link direto para o arquivo gerado em [`yt_base/yt_lake/<nome_normalizado>.md`](file:///<workspace_root>/yt_base/yt_lake/<nome_normalizado>.md)
   - Nome do canal e data de postagem
   - O assunto resumido
   - O link clicável para o catálogo [`yt_base/README.md`](file:///<workspace_root>/yt_base/README.md)
