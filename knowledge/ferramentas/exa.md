---
nome: Exa
categoria: busca-web-semantica-ia
tipo: mcp-servico-api
url: "https://exa.ai"
custo: "Freemium / API paga"
tags: [busca-web, semantica, neural-search, mcp, skills, enriquecimento-leads, pesquisa-empresas]
---

# Exa (Exa AI)

## O que é
O **Exa** (anteriormente Metaphor) é um mecanismo de busca neural e semântico projetado especificamente para agentes de IA e LLMs. Diferente de motores tradicionais baseados em palavras-chave (Google/Bing), o Exa compreende o significado semântico das perguntas, retorna conteúdo limpo diretamente pronto para o contexto de LLMs e oferece ferramentas de pesquisa autônoma profunda (Exa Agent).

---

## Modos de Operação no Startuzeiro

1. **Modo MCP (Model Context Protocol):**
   - Configurado no `~/.gemini/config/mcp_config.json`:
     - Endpoint: `https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa,agent_run`
     - Autenticação via header: `x-api-key: <EXA_API_KEY>`
   - Ferramentas MCP ativas:
     - `web_search_exa`: Busca web semântica rápida e limpa em linguagem natural.
     - `web_fetch_exa`: Extração de conteúdo completo e highlights de URLs conhecidas.
     - `web_search_advanced_exa`: Busca avançada com filtros por domínios, datas, categorias e frescor.
     - `agent_run`: Agente autônomo multi-step para pesquisas complexas, enriquecimento de leads e geração de saídas estruturadas em JSON.

2. **Skills Especializadas (.agents/skills/ e .agent/skills/):**
   - `build-with-exa`: Guia técnico de implementação e consumo das APIs do ecossistema Exa.
   - `company-research`: Pesquisa aprofundada de empresas, concorrentes, funding, notícias e perfis de liderança.
   - `exa-search`: Instruções para buscas semânticas diretas e sintetizadas.
   - `exa-contents`: Extração de texto, highlights e resumos de URLs específicas.
   - `lead-generation`: Descoberta e qualificação de listas de empresas e leads alinhados a um ICP (*Ideal Customer Profile*).

---

## Casos de Uso no Laboratório Startuzeiro
1. **Inteligência Competitiva e Dossiês:** Mapear empresas concorrentes em qualquer nicho em segundos usando busca neural.
2. **Geração e Qualificação de Leads B2B:** Prospecção ativa de empresas que se encaixam em critérios de negócios para validação de hipóteses comerciais.
3. **Extração e Monitoramento de Notícias/Tendências:** Acompanhar movimentos recentes de mercado, investimentos e lançamentos de startups.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"exa": {
  "serverUrl": "https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa,agent_run",
  "headers": {
    "x-api-key": "SUA_CHAVE_EXA_AQUI"
  }
}
```

---

## Links Relacionados
- [[Firecrawl]]
- [[youtube-transcript-api]]
- [[Context7]]
- [[catalogo]]
