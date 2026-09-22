---
nome: Hunter.io
categoria: prospeccao-b2b-email-intel
tipo: mcp-servico-api
url: "https://hunter.io"
custo: "Freemium (50 créditos/mês gratuitos)"
tags: [hunter, emails, prospeccao, leads-b2b, cold-outreach, deliverability, verificacao, mcp]
---

# Hunter.io

## O que é
O **Hunter.io** é a plataforma líder global de inteligência de contatos B2B e busca de e-mails corporativos. Ele permite mapear as pessoas e endereços de e-mail por trás de qualquer domínio corporativo, encontrar o e-mail exato de executivos sabendo nome e empresa, verificar a entregabilidade de e-mails para evitar bounces, enriquecer perfis de pessoas e organizações e estruturar sequências de cold outreach.

---

## Modos de Operação no Startuzeiro

1. **Modo MCP (Model Context Protocol):**
   - Configurado no `~/.gemini/config/mcp_config.json`:
     - Endpoint: `https://mcp.hunter.io/mcp`
     - Autenticação: `X-API-Key: <HUNTER_API_KEY>`
   - Mais de 100 ferramentas disponíveis, divididas em:
     - **Pesquisa & Descoberta**:
       - `Domain-Search`: Lista contatos por domínio com filtros de departamento e senioridade.
       - `Email-Finder`: Localiza o e-mail de um profissional pelo nome e domínio.
       - `Email-Verifier`: Valida entregabilidade, status MX e SMTP de um e-mail.
       - `Email-Count`: Consulta contagem gratuita de e-mails disponíveis por domínio.
       - `Find-Companies`: Descoberta de empresas por setor e termos de busca (0 créditos).
     - **Enriquecimento B2B**:
       - `Person-Enrichment`: Cargo, LinkedIn, Twitter e perfil a partir do e-mail.
       - `Company-Enrichment`: Dados cadastrais e tecnologias a partir do domínio.
       - `Combined-Enrichment`: Enriquecimento simultâneo de indivíduo e organização.
     - **Gestão de Leads & Campanhas**:
       - `Create-Lead` / `Create-Lead-If-Missing`: Salva contatos como leads oficiais.
       - `List-Leads` / `List-Leads-Lists`: Consulta e organização de listas de prospecção.
       - `Create-Sequence` / `Start-Sequence`: Cadências de e-mail e automação de contato.
       - `Push-Leads-To-CRM`: Sincronização com HubSpot, Pipedrive ou Salesforce.
     - **Gestão de Quota & Uso**:
       - `Get-Account-Details`: Status do plano, créditos consumidos e disponíveis.
       - `Get-Usage`: Métricas de consumo do período atual.

2. **Skill Dedicada:**
   - `.agents/skills/hunter-b2b-intel/` e `.agent/skills/hunter-b2b-intel/`: Guia passo a passo de prospecção, validação de e-mails e pipeline de enriquecimento.

---

## Casos de Uso no Laboratório Startuzeiro

1. **Descoberta de Tomadores de Decisão (GTM & Parcerias):**
   - Encontrar os e-mails diretos de founders, diretores de tecnologia, marketing e parcerias a partir do domínio corporativo.
2. **Higienização de Listas e Prevenção de Bounces:**
   - Auditar listas de contatos com o `Email-Verifier` antes de disparos para manter taxas de rejeição abaixo de 2% e preservar a reputação do domínio.
3. **Cruzamento de Inteligência (cnpj.ai + Hunter):**
   - Identificar o sócio administrador de uma empresa brasileira no `cnpj.ai` e localizar seu e-mail corporativo institucional no `Hunter`.
4. **Prospecção Ativa B2B (Exa + Hunter):**
   - Identificar empresas com fit com o `Exa` e extrair os responsáveis de área com o `Hunter` salvando-os como leads organizados.

---

## Configuração do MCP
Configurado em `~/.gemini/config/mcp_config.json`:
```json
"hunter": {
  "serverUrl": "https://mcp.hunter.io/mcp",
  "headers": {
    "X-API-Key": "SUA_CHAVE_HUNTER_AQUI"
  }
}
```

---

## Links Relacionados
- [[cnpj-ai]]
- [[Exa]]
- [[Firecrawl]]
- [[TranscriptAPI]]
- [[Context7]]
- [[catalogo]]
