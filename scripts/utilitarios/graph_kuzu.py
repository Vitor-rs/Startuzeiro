#!/usr/bin/env python3
"""
graph_kuzu.py - Banco de grafos local embutido em Cypher para o Startuzeiro
Startuzeiro Lab

Permite modelar, ingerir e consultar redes societárias (QSA), relações de investidores,
startups e clientes localmente sem precisar de servidor Neo4j.

Uso:
  uv run scripts/utilitarios/graph_kuzu.py demo
  uv run scripts/utilitarios/graph_kuzu.py query "MATCH (a)-[r]->(b) RETURN a.nome, label(r), b.nome"
  uv run scripts/utilitarios/graph_kuzu.py query "MATCH (p:Pessoa)-[:SOCIO_DE]->(e:Empresa) RETURN p.nome, e.razao_social"
"""

import sys
import argparse
from pathlib import Path

DEFAULT_DB_PATH = Path("dados/grafos/kuzu_startuzeiro")

def get_connection(db_path: Path):
    import kuzu
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = kuzu.Database(str(db_path))
    return kuzu.Connection(db)

def init_demo_schema(conn):
    """Cria um grafo de exemplo com empresas, sócios e investimentos."""
    # Tabelas de nós
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Empresa(cnpj STRING, razao_social STRING, setor STRING, PRIMARY KEY(cnpj))")
    conn.execute("CREATE NODE TABLE IF NOT EXISTS Pessoa(cpf STRING, nome STRING, cargo STRING, PRIMARY KEY(cpf))")

    # Tabelas de relacionamentos
    conn.execute("CREATE REL TABLE IF NOT EXISTS SOCIO_DE(FROM Pessoa TO Empresa, participacao DOUBLE)")
    conn.execute("CREATE REL TABLE IF NOT EXISTS INVESTIU_EM(FROM Empresa TO Empresa, valor_aporte DOUBLE)")

    # Inserir dados de demonstração se vazios
    check = conn.execute("MATCH (e:Empresa) RETURN count(e) AS total").get_as_df()
    if check["total"][0] == 0:
        conn.execute("CREATE (:Empresa {cnpj: '00000000000191', razao_social: 'Banco do Brasil S.A.', setor: 'Financeiro'})")
        conn.execute("CREATE (:Empresa {cnpj: '11111111000122', razao_social: 'Startuzeiro Tech LTDA', setor: 'Software & IA'})")
        conn.execute("CREATE (:Pessoa {cpf: '12345678900', nome: 'Vitor Fundador', cargo: 'CEO & Founder'})")

        conn.execute("MATCH (p:Pessoa {cpf: '12345678900'}), (e:Empresa {cnpj: '11111111000122'}) CREATE (p)-[:SOCIO_DE {participacao: 100.0}]->(e)")
        print("[Demo] Grafo de demonstração inicializado com sucesso!")
    else:
        print("[Demo] Banco já contém registros.")

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Gerenciador e consulta de grafos locais via KùzuDB.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando demo
    sub_demo = subparsers.add_parser("demo", help="Inicializa o esquema de demonstração do grafo")
    sub_demo.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Diretório do banco KùzuDB")

    # Subcomando query
    sub_query = subparsers.add_parser("query", help="Executa uma consulta Cypher no banco")
    sub_query.add_argument("cypher", help="Comando Cypher (ex: MATCH (n) RETURN n)")
    sub_query.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Diretório do banco KùzuDB")
    sub_query.add_argument("-f", "--format", choices=["table", "markdown", "df"], default="markdown",
                           help="Formato de exibição dos resultados")

    args = parser.parse_args()
    db_path = Path(args.db)

    try:
        import kuzu
    except ImportError:
        print("Erro: kuzu não está instalado no ambiente.", file=sys.stderr)
        sys.exit(1)

    conn = get_connection(db_path)

    if args.command == "demo":
        init_demo_schema(conn)
        res = conn.execute("MATCH (p:Pessoa)-[r:SOCIO_DE]->(e:Empresa) RETURN p.nome, r.participacao, e.razao_social")
        print(res.get_as_df().to_markdown(index=False))

    elif args.command == "query":
        try:
            res = conn.execute(args.cypher)
            df = res.get_as_df()
            if args.format == "markdown":
                print(df.to_markdown(index=False))
            else:
                print(df)
        except Exception as e:
            print(f"[KùzuDB Error] Erro ao executar Cypher: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
