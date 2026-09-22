#!/usr/bin/env python3
"""
doc_to_markdown.py - Conversor universal de documentos para Markdown + Metadados YAML
Startuzeiro Lab

Suporta: PDF, DOCX, PPTX, XLSX, CSV, HTML, Imagens e Áudios.
Engines:
- markitdown (Microsoft, default universal)
- pymupdf4llm (Especialista em PDFs com preservação de tabelas e blocos RAG)

Uso:
  uv run scripts/utilitarios/doc_to_markdown.py "caminho/do/documento.pdf"
  uv run scripts/utilitarios/doc_to_markdown.py "relatorio.docx" -o "pesquisas/relatorio.md"
  uv run scripts/utilitarios/doc_to_markdown.py "arquivo.pdf" --engine pymupdf
"""

import os
import sys
import argparse
import datetime
from pathlib import Path

def sanitize_title(name: str) -> str:
    """Gera um título limpo a partir do nome do arquivo."""
    base = Path(name).stem
    return base.replace("_", " ").replace("-", " ").strip().title()

def convert_with_markitdown(file_path: Path) -> str:
    """Converte documento utilizando o MarkItDown da Microsoft."""
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(str(file_path))
        return result.text_content
    except Exception as e:
        print(f"[doc_to_markdown] Erro na conversão com MarkItDown: {e}", file=sys.stderr)
        raise

def convert_with_pymupdf(file_path: Path) -> str:
    """Converte PDF utilizando o PyMuPDF4LLM."""
    try:
        import pymupdf4llm
        return pymupdf4llm.to_markdown(str(file_path))
    except Exception as e:
        print(f"[doc_to_markdown] Erro na conversão com PyMuPDF4LLM: {e}", file=sys.stderr)
        raise

def main():
    parser = argparse.ArgumentParser(description="Conversor universal de documentos para Markdown + YAML do Startuzeiro.")
    parser.add_argument("input_file", help="Caminho do arquivo (PDF, DOCX, PPTX, XLSX, etc.)")
    parser.add_argument("-o", "--output", help="Caminho de saída para o arquivo .md (opcional)")
    parser.add_argument("--engine", choices=["auto", "markitdown", "pymupdf"], default="auto",
                        help="Motor de conversão (padrão: auto)")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Erro: Arquivo não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    ext = input_path.suffix.lower()
    engine = args.engine

    if engine == "auto":
        if ext == ".pdf":
            # Tenta pymupdf4llm primeiro para PDFs por melhor fidelidade de tabelas, se falhar cai no markitdown
            try:
                content = convert_with_pymupdf(input_path)
                selected_engine = "pymupdf4llm"
            except Exception:
                content = convert_with_markitdown(input_path)
                selected_engine = "markitdown"
        else:
            content = convert_with_markitdown(input_path)
            selected_engine = "markitdown"
    elif engine == "pymupdf":
        content = convert_with_pymupdf(input_path)
        selected_engine = "pymupdf4llm"
    else:
        content = convert_with_markitdown(input_path)
        selected_engine = "markitdown"

    # Criar metadados YAML de cabeçalho
    now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = sanitize_title(input_path.name)
    file_size_kb = round(input_path.stat().st_size / 1024, 2)

    yaml_header = f"""---
titulo: "{title}"
arquivo_original: "{input_path.name}"
formato_origem: "{ext.replace('.', '')}"
tamanho_kb: {file_size_kb}
data_ingestao: "{now_iso}"
motor_conversao: "{selected_engine}"
tags:
  - documento-ingerido
  - {ext.replace('.', '')}
  - startuzeiro-lake
---

"""

    final_markdown = yaml_header + content.strip() + "\n"

    # Determinar caminho de saída
    if args.output:
        out_path = Path(args.output)
    else:
        # Padrão: salvar no mesmo diretório com extensão .md
        out_path = input_path.with_suffix(".md")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_markdown, encoding="utf-8")

    print(f"[OK] Documento convertido com sucesso via {selected_engine}!")
    print(f"     Origem: {input_path}")
    print(f"     Destino: {out_path} ({len(final_markdown)} caracteres)")

if __name__ == "__main__":
    main()
