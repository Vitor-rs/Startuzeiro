---
nome: Firecrawl
categoria: web-scraping-ia
tipo: servico-api
url: "https://www.firecrawl.dev"
custo: "Freemium / API paga"
tags: [crawling, scraping, llm-ready, markdown]
---

# Firecrawl

## O que é
O **Firecrawl** é um serviço que transforma qualquer website ou aplicação web em Markdown limpo e estruturado, ideal para ser consumido por LLMs (como Claude, Gemini, ChatGPT e agentes autônomos).

---

## Principais Recursos no Startuzeiro
1. **Crawl recursivo:** Mapeia um site inteiro de um concorrente e gera documentos consolidados.
2. **Bypass de bloqueios:** Lida com JavaScript rendering (SPAs), proxies reversos e proteções anti-bot.
3. **Extração estruturada:** Consegue extrair tabelas de preços, listas de produtos e FAQs diretamente em JSON usando prompts.

---

## Casos de Uso no Laboratório
- Investigação profunda de concorrentes em minutos.
- Monitoramento de mudanças de preços em páginas de planos de ferramentas SaaS.
- Scraping de diretórios de afiliados para minerar produtos em alta.

---

## Como Rodar no uv (Exemplo Rápido)
```bash
uv run --with firecrawl-py python -c "
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key='SEU_TOKEN')
res = app.scrape_url('https://exemplo.com', params={'formats': ['markdown']})
print(res['markdown'][:500])
"
```

---

## Links Relacionados
- [[OPP-001]]
- [[template-pesquisa]]
