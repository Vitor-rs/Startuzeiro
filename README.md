# ⚡ Startuzeiro

> *"Laboratório de inteligência de mercado, investigação e experimentos práticos para criar negócios digitais viáveis."*

O **Startuzeiro** é um monorepo investigativo. Ele não é uma aplicação ou sistema complexo; é uma **bancada de testes e documentador de hipóteses**, focado em descobrir o que realmente dá dinheiro (automação, marketing digital, IA aplicada, SaaS enxuto, afiliados e serviços) antes de escrever milhares de linhas de código.

---

## 🧭 Princípio Fundamental

> **"A infraestrutura deve ser menor que a pesquisa."**  
> Se um documento de validação tem 300 linhas e o código para gerenciá-lo tem 2.000 linhas, algo saiu errado. A fonte de verdade é simples, portável e à prova de obsolescência: **Git + Markdown + YAML**.

---

## 🏛️ A Arquitetura do Laboratório

| Papel | Ferramenta | Como opera |
| :--- | :--- | :--- |
| **Fonte de Verdade** | Git + GitHub | Versionamento, histórico de decisões e backup central |
| **Formato Universal** | Markdown + YAML | Documentação rica com metadados estruturados para filtragem |
| **Oficina Técnica** | VS Code | Edição de código, git, terminal e scripts |
| **Mapa Mental & Conexões** | Obsidian | Navegação em rede via `[[WikiLinks]]` e grafo visual sem custos |
| **Ambiente Experimental** | `uv` (Python 3.12+) | Execução isolada, ultrarrápida e sem poluição de dependências |
| **Instrumentos de Coleta** | Firecrawl, MCPs, APIs | Raspagem de sites, extração de dados e monitoramento de concorrentes |
| **Operadores & Pesquisadores** | Antigravity / Claude / IAs | Agentes encarregados de investigar, resumir e entregar **artefatos** |

---

## 📁 Estrutura de Pastas

```text
Startuzeiro/
├── .gitignore                      # Proteção para .venv, .env, caches e datasets pesados
├── pyproject.toml                  # Ambiente uv (zero dependências iniciais no core)
├── README.md                       # Este guia de bordo
│
├── metodologia/                    # Regras do jogo e processos
│   ├── funil-de-validacao.md       # Da ideia ao descarte ou negócio ativo
│   ├── criterios-ice.md            # Matriz de priorização (Impacto, Confiança, Facilidade)
│   └── templates/                  # Modelos prontos para copiar
│       ├── template-oportunidade.md
│       ├── template-pesquisa.md
│       └── template-experimento.md
│
├── oportunidades/                  # Propostas e ideias catalogadas
│   ├── afiliados/                  # Produtos, comissões, canais e ofertas
│   ├── automacao/                  # n8n, WhatsApp, bots, fluxos B2B
│   ├── ia-aplicada/                # Agentes, wrappers, automações cognitivas
│   ├── saas-micro/                 # Micro-produtos com receita recorrente
│   └── servicos-digitais/          # Prestação de serviço pontual ou consultoria
│
├── pesquisas/                      # Dossiês profundos de mercado
│   ├── concorrentes/               # Quem já fatura e onde está errando
│   ├── ferramentas/                # Análise técnica e de custos de ferramentas
│   └── mercado/                    # Tamanho de nicho, demanda e público
│
├── experimentos/                   # Testes no mundo real (outreach, tráfego, landing page)
│
├── knowledge/                      # Base de conhecimento e Zettelkasten (Obsidian)
│   ├── conceitos/                  # Termos, teses e modelos mentais
│   ├── playbooks/                  # Manuais passo a passo reutilizáveis
│   └── ferramentas/                # Notas atômicas sobre ferramentas ([[Firecrawl]], [[n8n]])
│
├── scripts/                        # Utilitários de pesquisa e automação
│   └── firecrawl/                  # Scripts para coleta e raspagem de sites
│
├── datasets/                       # Dados brutos coletados e planilhas
│   ├── raw/                        # Coletas brutas (ignorado no git)
│   └── processed/                  # Amostras consolidadas
│
└── archive/                        # O "cemitério de hipóteses" com motivo do descarte
```

---

## 🚀 Como Usar no Dia a Dia

### 1. Teve uma nova ideia?

1. Copie o arquivo `metodologia/templates/template-oportunidade.md`.
2. Salve em `oportunidades/<categoria>/OPP-XXX-nome-da-ideia.md`.
3. Preencha o resumo e estime o [[criterios-ice|Score ICE]].

### 2. Pedindo para um Agente de IA pesquisar

Não deixe a conversa morrer no chat. Exija artefatos comitáveis:
> *"Pesquise 5 concorrentes da ferramenta X no Brasil. Verifique preços e pontos fracos usando Firecrawl e salve o resultado em `pesquisas/concorrentes/PESQ-001-concorrentes-X.md` usando nosso template."*

### 3. Rodando scripts com `uv`

O `uv` executa scripts Python autocontidos com dependências automáticas (PEP 723):

```bash
# Rodar o script de exemplo de scraping:
uv run scripts/firecrawl/exemplo_scraping.py

# Ou rodar qualquer biblioteca sob demanda sem instalar no sistema:
uv run --with requests,beautifulsoup4 python -c "import requests; print('OK')"
```

### 4. Abrindo no Obsidian

1. Abra o Obsidian.
2. Selecione **"Open folder as vault"**.
3. Aponte para esta pasta `Startuzeiro/`.
4. Pronto! Use o Grafo (`Ctrl + G`) e navegue pelas conexões `[[OPP-001]]`, `[[firecrawl]]`, etc.
