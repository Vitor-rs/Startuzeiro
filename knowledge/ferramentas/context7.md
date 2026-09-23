---
nome: Context7
categoria: documentacao-ia-dev
tipo: mcp-servico-api
url: "https://context7.com"
custo: "Freemium / API paga"
tags: [documentacao, dev, llm-ready, mcp, skills, upstash]
---

# Context7

## O que é
O **Context7** (desenvolvido pela Upstash) é uma plataforma e servidor MCP/CLI focado em fornecer documentação atualizada, oficial e com exemplos de código em tempo real diretamente para agentes de IA e LLMs. Ele resolve o problema crítico de alucinação de APIs desatualizadas ou inexistentes ao consultar diretamente as fontes e repositórios oficiais.

---

## Modos de Operação no Startuzeiro

1. **Modo MCP (Model Context Protocol):**
   - Configurado no `~/.gemini/config/mcp_config.json`.
   - Permite que agentes chamem nativamente `resolve-library-id` e `query-docs`.
2. **Modo CLI & Skills:**
   - Skills instaladas em `.agents/skills/context7-mcp` e `.agents/skills/find-docs`.
   - Permite buscas diretas via CLI:
     ```bash
     npx ctx7 library <nome_da_lib> "<o_que_procura>"
     npx ctx7 docs <library_id> "<duvida_especifica>"
     ```

---

## Casos de Uso no Laboratório
1. **Consulta Rápida de APIs Modernas:** Obter exemplos reais e atualizados de bibliotecas como Next.js 15, React 19, FastAPI, Prisma, Tailwind, LangChain, etc.
2. **Construção de Automações e Protótipos:** Reduzir erros de código e versões obsoletas ao prototipar scripts de scraping, bots e webhooks no Startuzeiro.
3. **Validação de Métodos de SDKs:** Checagem rápida de parâmetros e retornos sem precisar abrir manualmente documentações extensas no navegador.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"context7": {
  "serverUrl": "https://mcp.context7.com/mcp",
  "headers": {
    "Authorization": "Bearer SUA_CHAVE_CONTEXT7_AQUI"
  }
}
```

---

## Links Relacionados
- [[Firecrawl]]
- [[youtube-transcript-api]]
- [[catalogo]]
