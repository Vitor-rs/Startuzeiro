---
nome: Clay.io
categoria: gtm-data-enrichment-waterfall
tipo: mcp-servico-api
url: "https://clay.com"
custo: "Freemium (créditos de busca e enriquecimento multiprovedor)"
tags: [clay, gtm, sales-intelligence, leads-b2b, enrichment, waterfall, query-mode, mcp]
---

# Clay.io

## O que é
O **Clay** (https://clay.com) é a plataforma líder mundial de orquestração de Go-To-Market (GTM) e inteligência de dados B2B. A plataforma unifica mais de 150 provedores de enriquecimento em cascata (waterfall), agentes de pesquisa de inteligência artificial e uma base de dados proprietária de mais de 75 milhões de empresas e profissionais. No Clay, equipes de receita e inteligência conseguem realizar buscas de altíssima precisão com cruzamento de entidades (ex: pessoas que trabalham em empresas com certa stack tecnológica e faturamento), disparar pesquisas web automatizadas e acionar rotinas de enriquecimento e geração de mensagens hiper-personalizadas.

---

## Modos de Operação no Startuzeiro

1. **Utilitário CLI Nativo (`clay_client.py`)**:
   - Localizado em `scripts/utilitarios/clay_client.py`.
   - Conecta-se diretamente à **Clay Public API v0** (`https://api.clay.com/public/v0`) usando a chave configurada no `.env` (`CLAY_API_KEY`).
   - Permite consultas rápidas, seguras e com codificação UTF-8 no Windows:
     - `uv run scripts/utilitarios/clay_client.py search "select from companies where industry = 'Software Development' limit 5"`
     - `uv run scripts/utilitarios/clay_client.py search 'select from people where experiences.any(is_current = true and job_title is_similar_to ("CTO"))' --limit 5`
     - `uv run scripts/utilitarios/clay_client.py reference`: cataloga campos, operadores e gramática SQL-like.
     - `uv run scripts/utilitarios/clay_client.py routine <routine_id> '<payload_json>'`: executa funções e rotinas de enriquecimento.

2. **Modo MCP (Model Context Protocol)**:
   - Configurado no `~/.gemini/config/mcp_config.json`:
     - Endpoint: `https://api.clay.com/v3/mcp`
     - Header: `clay-api-key: <CLAY_API_KEY>` (ou OAuth 2.0 via `mcp-remote`)
   - Permite consultas interativas pelo assistente de IA durante o fluxo de trabalho.

3. **Skills Dedicadas**:
   - `.agents/skills/clay-gtm-intel/` e `.agent/skills/clay-gtm-intel/`: Instruções completas sobre a gramática Query Mode, padrões de filtros (cargos similares, histórico profissional, stack tecnológica) e orquestração de prospecção.

---

## Casos de Uso no Laboratório Startuzeiro

1. **Prospecção Hiper-Segmentada com Query Mode**:
   - Encontrar executivos atuais com base em características complexas da empresa empregadora (ex: empresas com stack Stripe ou Salesforce e sede em determinado país).
2. **Enriquecimento em Cascata (Waterfall Data)**:
   - Aproveitar o pool de 150+ provedores da Clay para maximizar a taxa de cobertura de contatos e informações financeiras.
3. **Cruzamento de Inteligência Multi-Plataforma**:
   - Usar **cnpj.ai** para identificar sócios no Brasil, **Clay** para mapear o time técnico e stack global, **Hunter** para validação estrita de DNS/MX de e-mails corporativos e **Apollo** para telefones diretos e sinais de vagas abertas.
4. **Execução de Rotinas Customizadas**:
   - Disparar pipelines sob demanda na Clay a partir de scripts Python do laboratório.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"clay": {
  "serverUrl": "https://api.clay.com/v3/mcp",
  "headers": {
    "clay-api-key": "SUA_CHAVE_CLAY_AQUI"
  }
}
```

Para obter a chave:
1. Acesse sua conta em [Clay.com](https://app.clay.com/).
2. Vá em **Settings** ➔ **API Keys**.
3. Gere uma API Key com escopo e adicione ao `.env` local (`CLAY_API_KEY=clay_scoped_...`).

---

## Links Relacionados
- [[apollo]]
- [[hunter]]
- [[cnpj-ai]]
- [[exa]]
- [[firecrawl]]
- [[catalogo]]
