#!/usr/bin/env python3
"""
duckdb_query.py - Motor analítico in-process ultrarrápido para datasets do Startuzeiro
Startuzeiro Lab

Executa consultas SQL padrão em arquivos CSV, JSON, Parquet ou tabelas em memória,
sem necessidade de instalar ou rodar servidores de banco de dados.

Uso:
  uv run scripts/utilitarios/duckdb_query.py "SELECT 42 AS startuzeiro"
  uv run scripts/utilitarios/duckdb_query.py "SELECT * FROM 'leads.csv' WHERE email LIKE '%@gmail.com' LIMIT 10"
  uv run scripts/utilitarios/duckdb_query.py "SELECT count(*) FROM read_json_auto('empresas.json')"
  uv run scripts/utilitarios/duckdb_query.py "SELECT * FROM 'dados.parquet'" --format markdown
"""

import sys
import argparse
import json

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Consulta SQL ultra-rápida via DuckDB in-process.")
    parser.add_argument("query", help="Consulta SQL a ser executada")
    parser.add_argument("-f", "--format", choices=["table", "markdown", "json", "csv"], default="table",
                        help="Formato de saída dos resultados (padrão: table)")
    parser.add_argument("-d", "--db", default=":memory:", help="Arquivo de banco DuckDB persistente (padrão: memória)")
    args = parser.parse_args()

    try:
        import duckdb
    except ImportError:
        print("Erro: duckdb não está instalado no ambiente.", file=sys.stderr)
        sys.exit(1)

    try:
        con = duckdb.connect(database=args.db)
        rel = con.sql(args.query)

        if rel is None:
            print("[OK] Consulta executada sem retorno de linhas.")
            return

        fmt = args.format
        if fmt == "table":
            rel.show()
        elif fmt == "markdown":
            df = rel.to_df()
            print(df.to_markdown(index=False))
        elif fmt == "json":
            df = rel.to_df()
            print(df.to_json(orient="records", indent=2, force_ascii=False))
        elif fmt == "csv":
            df = rel.to_df()
            print(df.to_csv(index=False))

    except Exception as e:
        print(f"[DuckDB Error] Falha na execução da query: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
