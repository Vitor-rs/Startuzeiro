# Scripts Firecrawl

Esta pasta contém scripts utilitários para raspagem de sites, concorrentes e materiais de pesquisa usando o Firecrawl.

---

## Como executar os scripts com `uv`

Com o `uv`, você não precisa instalar bibliotecas globais nem poluir o ambiente base. Os scripts podem ser rodados sob demanda:

```bash
uv run --with firecrawl-py,python-dotenv python scripts/firecrawl/exemplo_scraping.py
```

---

## Variáveis de Ambiente

Guarde sua chave de API em um arquivo `.env` na raiz do projeto (que já está no `.gitignore` e nunca irá para o GitHub):

```ini
FIRECRAWL_API_KEY=sua_chave_aqui
```
