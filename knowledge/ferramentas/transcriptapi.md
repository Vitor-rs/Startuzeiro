---
nome: TranscriptAPI
categoria: transcricao-audio-video
tipo: mcp-servico-api
url: "https://transcriptapi.com"
custo: "Freemium / API paga"
tags: [youtube, transcricao, video, podcast, mcp]
---

# TranscriptAPI

## O que é
O **TranscriptAPI** é um serviço focado em obter e transcrever vídeos do YouTube, áudios e mídias em texto estruturado rapidamente, com suporte nativo a MCP (Model Context Protocol).

---

## Casos de Uso no Startuzeiro
1. **Mineração de Dores e Tendências:** Extrair transcrições de dezenas de vídeos de nicho (ex: canais de corretores, afiliados, marketing) para analisar reclamações frequentes e tópicos em alta.
2. **Engenharia Reversa de Conteúdo:** Obter a estrutura de webinars de vendas (VSLs) e cursos de concorrentes para mapear ofertas e pontos de conversão.
3. **Resumo e Dossiês Rápidos:** Transformar podcasts de 2 horas sobre negócios ou tendências em resumos executivos comitáveis em `pesquisas/`.

---

## Configuração do MCP
Já configurado no `~/.gemini/config/mcp_config.json`:
```json
"transcript-api": {
  "serverUrl": "https://transcriptapi.com/mcp",
  "headers": {
    "Authorization": "Bearer SUA_CHAVE_TRANSCRIPTAPI_AQUI"
  }
}
```

---

## Links Relacionados
- [[Firecrawl]]
- [[template-pesquisa]]
