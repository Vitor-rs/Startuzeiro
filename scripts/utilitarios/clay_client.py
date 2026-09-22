#!/usr/bin/env python3
"""
Utilitario CLI para o Clay (https://clay.com)
Permite executar buscas avançadas no banco GTM da Clay, consultar referências de campos
e disparar rotinas/enriquecimentos através da Public API oficial v0.

Uso:
    uv run scripts/utilitarios/clay_client.py search "select from companies where industry = 'Software Development' limit 5"
    uv run scripts/utilitarios/clay_client.py search "select from people where experiences.any(job_title is_similar_to ('CTO') and is_current = true) limit 5"
    uv run scripts/utilitarios/clay_client.py reference
    uv run scripts/utilitarios/clay_client.py routine <routine_id> '{"items": [{"id": "1", "inputs": {"domain": "stripe.com"}}]}'
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Forcar UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Carregar variaveis do .env local
def load_env():
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
CLAY_API_KEY = os.getenv("CLAY_API_KEY")
BASE_URL = "https://api.clay.com/public/v0"

def get_headers():
    if not CLAY_API_KEY or "sua_chave" in CLAY_API_KEY:
        print("[!] Erro: CLAY_API_KEY nao configurada no .env", file=sys.stderr)
        sys.exit(1)
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "clay-api-key": CLAY_API_KEY,
        "User-Agent": "Startuzeiro-Clay-Client/1.0"
    }

def fetch_reference():
    """Consulta a gramatica e campos disponiveis para busca."""
    url = f"{BASE_URL}/search/query-mode/reference"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(json.dumps(data, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(f"[!] Erro {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

import re

def normalize_query(query: str) -> str:
    """Converte aspas simples em aspas duplas, exigidas pelo parser da Clay."""
    return re.sub(r"'([^']*)'", r'"\1"', query)

def run_search(query: str, limit: int = 10):
    """Cria uma busca e extrai os resultados paginados."""
    headers = get_headers()
    normalized = normalize_query(query)
    # 1. Criar a busca
    create_url = f"{BASE_URL}/search/query-mode"
    payload = json.dumps({"query": normalized}).encode("utf-8")
    req = urllib.request.Request(create_url, data=payload, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            search_id = res_data.get("search_id")
            source_type = res_data.get("source_type")
            print(f"[*] Busca criada: {search_id} (Fonte: {source_type})")
    except urllib.error.HTTPError as e:
        print(f"[!] Erro ao criar busca ({e.code}): {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    # 2. Executar e coletar resultados
    run_url = f"{BASE_URL}/search/query-mode/{search_id}/run"
    run_payload = json.dumps({"limit": limit}).encode("utf-8")
    req_run = urllib.request.Request(run_url, data=run_payload, headers=headers)
    
    try:
        with urllib.request.urlopen(req_run) as res:
            results = json.loads(res.read().decode("utf-8"))
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(f"[!] Erro ao coletar resultados ({e.code}): {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

def run_routine(routine_id: str, items_json: str):
    """Executa uma rotina ou funcao do Clay."""
    headers = get_headers()
    url = f"{BASE_URL}/routines/{routine_id}/run"
    try:
        items = json.loads(items_json)
    except Exception as e:
        print(f"[!] Erro ao parsear JSON de items: {e}", file=sys.stderr)
        sys.exit(1)
        
    payload = json.dumps(items).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            print(json.dumps(res_data, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(f"[!] Erro ao disparar rotina ({e.code}): {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Clay GTM Client para Startuzeiro")
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")

    # Comando: search
    search_parser = subparsers.add_parser("search", help="Executa busca no banco GTM da Clay")
    search_parser.add_argument("query", help="Query SQL-like (ex: select from companies where industry = 'SaaS' limit 5)")
    search_parser.add_argument("--limit", type=int, default=10, help="Limite de resultados (padrao: 10)")

    # Comando: reference
    subparsers.add_parser("reference", help="Exibe os campos e gramatica de consulta suportados")

    # Comando: routine
    routine_parser = subparsers.add_parser("routine", help="Executa uma rotina ou funcao personalizada")
    routine_parser.add_argument("routine_id", help="ID da rotina (ex: function:t_abc123)")
    routine_parser.add_argument("payload", help="JSON de entrada com os items")

    args = parser.parse_args()

    if args.command == "search":
        run_search(args.query, args.limit)
    elif args.command == "reference":
        fetch_reference()
    elif args.command == "routine":
        run_routine(args.routine_id, args.payload)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
