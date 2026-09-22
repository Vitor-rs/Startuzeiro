---
nome: Apollo.io
categoria: sales-intelligence-gtm-prospeccao
tipo: mcp-servico-api
url: "https://www.apollo.io"
custo: "Freemium (créditos de busca e enriquecimento)"
tags: [apollo, sales-intelligence, gtm, leads-b2b, outbound, enrichment, emails, direct-dials, mcp]
---

# Apollo.io

## O que é
O **Apollo.io** é a plataforma líder mundial de inteligência de vendas (GTM) e engajamento B2B. Com uma base de dados de mais de 275 milhões de contatos corporativos e 73 milhões de organizações, o Apollo permite que equipes de vendas e inteligência pesquisem tomadores de decisão por ICP (cargo, senioridade, faturamento, localização), enriqueçam perfis com e-mails verificados e telefones diretos (direct dials), detectem sinais de compra através de vagas abertas (job postings) e cadastrem leads em cadências de vendas personalizadas.

---

## Modos de Operação no Startuzeiro

1. **Modo MCP (Model Context Protocol):**
   - Configurado no `~/.gemini/config/mcp_config.json`:
     - Endpoint: `https://mcp.apollo.io/mcp`
     - Autenticação: `X-Api-Key: <APOLLO_API_KEY>` (ou OAuth 2.0)
   - Ferramentas disponíveis:
     - **Pesquisa de Pessoas e Empresas**:
       - `apollo_search_people` / `apollo_mixed_people_api_search`: Busca de profissionais por cargo, senioridade e perfil corporativo.
       - `apollo_search_organizations` / `apollo_mixed_companies_search`: Mapeamento de empresas por setor, faturamento e tecnologias.
     - **Sinais de Vagas e Intenção de Compra**:
       - `apollo_get_job_postings`: Consulta de vagas ativas para identificar tecnologias e planos de contratação.
     - **Enriquecimento de Contatos e Contas**:
       - `apollo_enrich_person` / `apollo_people_match`: Revela e-mail verificado, telefone direto e LinkedIn.
       - `apollo_enrich_organization`: Traz receita anual estimada, tecnologias utilizadas e filiais.
       - `apollo_bulk_enrich_people` / `apollo_organizations_bulk_enrich`: Enriquecimento em lote.
     - **CRM e Gestão de Contatos**:
       - `apollo_create_contacts` / `apollo_update_contacts`: Insere leads no banco de contatos do Apollo.
       - `apollo_search_contacts`: Consulta de contatos já cadastrados.
     - **Automação de Sequências**:
       - `apollo_search_sequences`: Localiza sequências de e-mail por nome.
       - `apollo_add_contacts_to_sequence`: Enrola contatos em cadências de outbound.
       - `apollo_list_email_accounts`: Lista caixas de envio conectadas.
     - **Analytics de Vendas**:
       - `apollo_analytics_sync_report`: Relatórios de atividade e desempenho comercial.

2. **Skill Dedicada:**
   - `.agents/skills/apollo-sales-intel/` e `.agent/skills/apollo-sales-intel/`: Fluxo estruturado de ICP, enriquecimento com controle de créditos e enrolamento em cadências de vendas.

---

## Casos de Uso no Laboratório Startuzeiro

1. **Descoberta de Decisores Globais:**
   - Encontrar VPs de Engenharia, Founders e Heads de Produto em empresas internacionais de software ou inteligência artificial.
2. **Identificação de Sinais de Compra (Buying Signals):**
   - Rastrear vagas de tecnologia abertas (`apollo_get_job_postings`) para saber quais empresas estão migrando de stack ou expandindo operações.
3. **Cruzamento de Inteligência B2B:**
   - Usar **cnpj.ai** para identificar sócios no Brasil, **Hunter** para validação de e-mails institucionais e **Apollo** para telefones diretos e cargos corporativos globais.
4. **Alimentação de Sequências de Outbound:**
   - Montar listas altamente qualificadas e matriculá-las diretamente em sequências de prospecção do Apollo.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"apollo": {
  "serverUrl": "https://mcp.apollo.io/mcp",
  "headers": {
    "X-Api-Key": "SUA_CHAVE_APOLLO_AQUI"
  }
}
```

Para gerar a chave:
1. Acesse [Apollo.io](https://app.apollo.io/).
2. Vá em **Settings** ➔ **Integrations** ➔ **API Keys**.
3. Crie uma chave nova e insira no seu `.env` local (`APOLLO_API_KEY=...`).

---

## Links Relacionados
- [[hunter]]
- [[cnpj-ai]]
- [[Exa]]
- [[Firecrawl]]
- [[Context7]]
- [[catalogo]]
