---
nome: cnpj.ai
categoria: inteligencia-societaria-osint
tipo: mcp-servico-api
url: "https://cnpj.ai"
custo: "Freemium / API paga"
tags: [cnpj, receita-federal, societario, qsa, pgfn, divida-ativa, leads-b2b, mcp, osint]
---

# cnpj.ai

## O que é
O **cnpj.ai** é uma plataforma e servidor MCP de inteligência corporativa e dados públicos da Receita Federal do Brasil. Ele indexa mais de 72,3 milhões de CNPJs e permite navegar em linguagem natural por redes societárias, quadros de sócios e administradores (QSA), grupos econômicos informais através de vínculos de contato (e-mail/telefone idênticos) e apontamentos de dívida ativa da União junto à PGFN.

---

## Modos de Operação no Startuzeiro

1. **Modo MCP (Model Context Protocol):**
   - Configurado no `~/.gemini/config/mcp_config.json`:
     - Endpoint: `https://mcp.cnpj.ai/mcp`
     - Autenticação: `Authorization: Bearer <CNPJ_AI_API_KEY>`
   - 11 ferramentas disponíveis:
     - `investigar_empresa`: Dossiê cadastral, societário e fiscal completo em 1 chamada.
     - `buscar_empresas`: Busca por razão social, nome fantasia ou número.
     - `ficha_cnpj`: Ficha cadastral oficial individualizada de matriz ou filial.
     - `buscar_socios`: Busca de sócios (pessoas físicas) em todo o Brasil.
     - `empresas_do_socio`: Mapeamento de todas as empresas de um sócio.
     - `rede_societaria`: Grafo e relações societárias em até 3 níveis.
     - `encontrar_conexao`: Menor caminho societário entre dois CNPJs.
     - `vinculos_ocultos`: Empresas que compartilham o mesmo e-mail ou telefone.
     - `panorama_empresarial`: Estatísticas e contagens de CNPJs por Brasil, UF ou município.
     - `listar_empresas`: Prospecção B2B com filtros cadastrais e regionais.
     - `buscar_cnae`: Busca de códigos de atividade econômica por texto livre.

2. **Skill Dedicada:**
   - `.agents/skills/cnpj-ai-research/` e `.agent/skills/cnpj-ai-research/`: Guia passo a passo de investigação, fluxogramas de decisão e geração de relatórios com links para o grafo visual (`https://grafo.cnpj.ai`).

---

## Casos de Uso no Laboratório Startuzeiro
1. **Due Diligence de Parceiros e Concorrentes:** Investigar quem realmente controla uma empresa, capital social, matrizes e filiais e situação cadastral.
2. **Identificação de Grupos Econômicos Informais:** Mapear empresas satélites e holdings não declaradas via cruzamento de e-mails e telefones idênticos.
3. **Análise de Risco de Crédito e Compliance:** Identificar débitos inscritos na Dívida Ativa da União (PGFN) antes de fechar contratos ou parcerias.
4. **Prospecção de Leads B2B:** Segmentar empresas ativas por código CNAE, porte e localidade geográfica.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"cnpj-ai": {
  "serverUrl": "https://mcp.cnpj.ai/mcp",
  "headers": {
    "Authorization": "Bearer SUA_CHAVE_CNPJ_AI_AQUI"
  }
}
```

---

## Links Relacionados
- [[Exa]]
- [[Firecrawl]]
- [[TranscriptAPI]]
- [[catalogo]]
