# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "firecrawl-py",
#     "python-dotenv",
# ]
# ///
"""
Exemplo de extração de conteúdo limpo para Markdown com Firecrawl e uv.
Para executar diretamente:
    uv run scripts/firecrawl/exemplo_scraping.py
"""

import os
import sys
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

def main():
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("[AVISO] FIRECRAWL_API_KEY não encontrada no arquivo .env!")
        return

    try:
        from firecrawl import FirecrawlApp
        app = FirecrawlApp(api_key=api_key)
        
        url = "https://example.com"
        print(f"[INFO] Raspando {url} via Firecrawl...")
        res = app.scrape(url, formats=["markdown"])
        
        print("\n--- Conteúdo Retornado em Markdown ---")
        markdown_text = getattr(res, "markdown", None) or (res.get("markdown") if isinstance(res, dict) else str(res))
        print(markdown_text)
        print("\n[SUCESSO] Firecrawl Python SDK testado e funcionando!")
    except Exception as e:
        print(f"[ERRO] Falha ao executar raspagem: {e}")

if __name__ == "__main__":
    main()
