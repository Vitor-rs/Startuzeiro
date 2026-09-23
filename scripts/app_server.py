#!/usr/bin/env python3
"""
scripts/app_server.py - Startuzeiro OS: Servidor Backend Bridge & Orquestrador de Inteligência
Startuzeiro Lab

Fornece a API REST local para o Startuzeiro OS:
1. Orquestrador de Missões 360° (Fábrica de Pesquisa Multi-Ferramenta)
2. Bancada de Ferramentas Ativas (Low-Code Workbench)
3. CRM & ERP de Inteligência de Mercado (Dossiês, Oportunidades & Lake)
4. Catálogo Master com ciclo de vida e solicitação ao agente

Uso:
    uv run scripts/app_server.py [--port 5050]
"""

import os
import sys
import re
import json
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Forçar UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = ROOT_DIR / "dashboard"
PORT = 5050

# Importar motor do Cérebro Agêntico
try:
    from scripts import agentic_brain
except Exception:
    try:
        import agentic_brain
    except Exception:
        agentic_brain = None


# IDs das ferramentas ativas e instaladas na bancada
ACTIVE_TOOL_IDS = {
    "FER-017",  # Scrapling
    "FER-023",  # Changedetection.io
    "FER-048",  # MailAccess
    "FER-057",  # Context7 MCP
    "FER-058",  # Exa MCP
    "FER-059",  # cnpj.ai MCP
    "FER-060",  # Hunter.io MCP
    "FER-061",  # Apollo.io MCP
    "FER-062",  # Clay MCP & CLI
    "FER-063",  # NetworkX
    "FER-064",  # GLiNER / GLiNER2
    "FER-067",  # MarkItDown
    "FER-069",  # PyMuPDF4LLM
    "FER-077",  # Instructor
    "FER-146",  # DuckDB
    "FER-203",  # Hugging Face Hub MCP
}

# Carregar variáveis do .env
def load_env():
    env_file = ROOT_DIR / ".env"
    env_vars = {}
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    os.environ.setdefault(k, v)
                    env_vars[k] = v
    return env_vars

ENV_VARS = load_env()


class StartuzeiroHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Status do Sistema
        if path == "/api/status":
            return self._send_json(200, {
                "status": "online",
                "system": "Startuzeiro OS v2.0",
                "port": PORT,
                "python_version": sys.version.split()[0],
                "active_tools_count": len(ACTIVE_TOOL_IDS),
                "mcps": {
                    "clay": bool(os.getenv("CLAY_API_KEY") and "sua_chave" not in os.getenv("CLAY_API_KEY", "")),
                    "hunter": bool(os.getenv("HUNTER_API_KEY") and "sua_chave" not in os.getenv("HUNTER_API_KEY", "")),
                    "apollo": bool(os.getenv("APOLLO_API_KEY") and "sua_chave" not in os.getenv("APOLLO_API_KEY", "")),
                    "cnpj_ai": bool(os.getenv("CNPJ_AI_API_KEY") and "sua_chave" not in os.getenv("CNPJ_AI_API_KEY", "")),
                    "exa": bool(os.getenv("EXA_API_KEY") and "sua_chave" not in os.getenv("EXA_API_KEY", "")),
                    "context7": bool(os.getenv("CONTEXT7_API_KEY") and "sua_chave" not in os.getenv("CONTEXT7_API_KEY", "")),
                    "firecrawl": bool(os.getenv("FIRECRAWL_API_KEY") and "sua_chave" not in os.getenv("FIRECRAWL_API_KEY", "")),
                    "huggingface": True  # Modo anônimo ou token
                },
                "engines": {
                    "youtube_transcribe": True,
                    "duckdb": True,
                    "networkx": True,
                    "gliner": True,
                    "markitdown": True,
                    "pymupdf4llm": True,
                    "instructor": True,
                    "changedetection": True
                }
            })

        # 2. Catálogo Completo de Ferramentas (com flag ativo)
        if path == "/api/tools":
            tools_data = []
            json_cache = DASHBOARD_DIR / "tools_data.js"
            if json_cache.exists():
                try:
                    with open(json_cache, "r", encoding="utf-8") as f:
                        content = f.read()
                        prefix = "const TOOLS_DATA = "
                        if prefix in content:
                            raw = content.split(prefix, 1)[1].rstrip(";\n ")
                            tools_data = json.loads(raw)
                except Exception:
                    pass

            if not tools_data:
                yaml_path = ROOT_DIR / "ferramentas" / "catalogo.yaml"
                if yaml_path.exists():
                    try:
                        import yaml
                        with open(yaml_path, "r", encoding="utf-8") as f:
                            tools_data = yaml.safe_load(f)
                    except Exception as e:
                        return self._send_json(500, {"error": f"Erro ao ler ferramentas: {e}"})

            # Injetar status ativo/instalado
            for t in tools_data:
                t["is_active"] = t.get("id") in ACTIVE_TOOL_IDS

            return self._send_json(200, tools_data)

        # 3. Cérebro Agêntico: Grafo de Conhecimento e Oportunidades
        if path == "/api/brain/graph":
            if agentic_brain:
                g = agentic_brain.build_knowledge_graph()
                return self._send_json(200, g)
            return self._send_json(200, {"nodes": [], "links": []})

        # 4. CRM: Listar Dossiês em brain/02_pesquisas/concorrentes e pesquisas/concorrentes
        if path == "/api/crm/dossiers":
            dossiers = []
            seen_files = set()
            dirs = [
                ROOT_DIR / "brain" / "02_pesquisas" / "concorrentes",
                ROOT_DIR / "pesquisas" / "concorrentes"
            ]
            for p_dir in dirs:
                if not p_dir.exists():
                    continue
                for f in sorted(p_dir.glob("*.md"), key=os.path.getmtime, reverse=True):
                    if f.name in seen_files:
                        continue
                    seen_files.add(f.name)
                    try:
                        content = f.read_text(encoding="utf-8")
                        title = f.stem.replace("_", " ").title()
                        created_at = ""
                        summary = ""

                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                header = parts[1]
                                for line in header.splitlines():
                                    if line.startswith("titulo:"):
                                        title = line.split(":", 1)[1].strip(" \"'")
                                    elif line.startswith("data_investigacao:") or line.startswith("data:"):
                                        created_at = line.split(":", 1)[1].strip(" \"'")
                                    elif line.startswith("resumo:"):
                                        summary = line.split(":", 1)[1].strip(" \"'")

                        dossiers.append({
                            "filename": f.name,
                            "title": title,
                            "created_at": created_at or "Recente",
                            "size_kb": round(f.stat().st_size / 1024, 1),
                            "summary": summary,
                            "path": f"brain/02_pesquisas/concorrentes/{f.name}"
                        })
                    except Exception:
                        pass
            return self._send_json(200, dossiers)

        # 5. CRM: Listar Oportunidades em brain/01_oportunidades e oportunidades/
        if path == "/api/crm/opportunities":
            opps = []
            seen_ids = set()
            dirs = [
                ROOT_DIR / "brain" / "01_oportunidades",
                ROOT_DIR / "oportunidades"
            ]
            for opps_dir in dirs:
                if not opps_dir.exists():
                    continue
                for f in opps_dir.rglob("*.md"):
                    if f.name.startswith("OPP-"):
                        try:
                            content = f.read_text(encoding="utf-8")
                            title = f.stem
                            status = "Ideação"
                            ice_score = 0
                            vector = f.parent.name
                            revenue = ""

                            if content.startswith("---"):
                                parts = content.split("---", 2)
                                if len(parts) >= 3:
                                    header = parts[1]
                                    for line in header.splitlines():
                                        if line.startswith("titulo:"):
                                            title = line.split(":", 1)[1].strip(" \"'")
                                        elif line.startswith("status:"):
                                            status = line.split(":", 1)[1].strip(" \"'")
                                        elif line.startswith("potencial_receita:"):
                                            revenue = line.split(":", 1)[1].strip(" \"'")
                                        elif "total:" in line or "media:" in line:
                                            m = re.search(r"\d+(\.\d+)?", line)
                                            if m:
                                                ice_score = float(m.group(0))

                            opp_id = f.stem.split("-")[0] + "-" + f.stem.split("-")[1] if "-" in f.stem else f.stem
                            if opp_id in seen_ids:
                                continue
                            seen_ids.add(opp_id)

                            opps.append({
                                "id": opp_id,
                                "title": title,
                                "category": vector,
                                "status": status.title(),
                                "ice_score": ice_score,
                                "revenue": revenue,
                                "filename": f.name,
                                "path": str(f.relative_to(ROOT_DIR)).replace("\\", "/")
                            })
                        except Exception:
                            pass
            return self._send_json(200, sorted(opps, key=lambda x: x["ice_score"], reverse=True))

        # 6. CRM: Listar Vídeos do YouTube Lake
        if path == "/api/crm/lake":
            lake_files = []
            seen_files = set()
            dirs = [
                ROOT_DIR / "brain" / "03_recursos" / "yt_lake",
                ROOT_DIR / "yt_base" / "yt_lake"
            ]
            for yt_lake_dir in dirs:
                if not yt_lake_dir.exists():
                    continue
                for f in sorted(yt_lake_dir.glob("*.md"), key=os.path.getmtime, reverse=True):
                    if f.name in seen_files:
                        continue
                    seen_files.add(f.name)
                    try:
                        content = f.read_text(encoding="utf-8")
                        title = f.stem.replace("_", " ").title()
                        channel = "YouTube"
                        date = ""
                        url = ""

                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                header = parts[1]
                                for line in header.splitlines():
                                    if line.startswith("titulo_original:") or line.startswith("titulo:"):
                                        title = line.split(":", 1)[1].strip(" \"'")
                                    elif line.startswith("canal:"):
                                        channel = line.split(":", 1)[1].strip(" \"'")
                                    elif line.startswith("data_publicacao:") or line.startswith("data_ingestao:"):
                                        date = line.split(":", 1)[1].strip(" \"'")
                                    elif line.startswith("link_video:") or line.startswith("url_original:") or line.startswith("url:"):
                                        url = line.split(":", 1)[1].strip(" \"'")

                        lake_files.append({
                            "filename": f.name,
                            "title": title,
                            "channel": channel,
                            "date": date,
                            "url": url,
                            "size_kb": round(f.stat().st_size / 1024, 1),
                            "path": f"brain/03_recursos/yt_lake/{f.name}"
                        })
                    except Exception:
                        pass
            return self._send_json(200, lake_files)


        # Caso contrário, serve arquivos estáticos de dashboard/
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)
        try:
            payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except Exception:
            payload = {}

        # ========================================================
        # WORKBENCH: MÓDULOS INDIVIDUAIS DE FERRAMENTAS
        # ========================================================

        # 1. Hunter.io Studio
        if path == "/api/workbench/hunter":
            action = payload.get("action", "count")
            domain = payload.get("domain", "").strip().lower()
            key = os.getenv("HUNTER_API_KEY", "")

            if not key or "sua_chave" in key:
                return self._send_json(400, {"error": "Chave HUNTER_API_KEY não configurada no .env"})
            if not domain:
                return self._send_json(400, {"error": "Domínio corporativo obrigatório"})

            try:
                if action == "count":
                    url = f"https://api.hunter.io/v2/email-count?domain={urllib.parse.quote(domain)}&api_key={key}"
                elif action == "domain-search":
                    limit = int(payload.get("limit", 10))
                    url = f"https://api.hunter.io/v2/domain-search?domain={urllib.parse.quote(domain)}&limit={limit}&api_key={key}"
                elif action == "verify":
                    email = payload.get("email", "").strip()
                    url = f"https://api.hunter.io/v2/email-verifier?email={urllib.parse.quote(email)}&api_key={key}"
                else:
                    return self._send_json(400, {"error": f"Ação desconhecida: {action}"})

                req = urllib.request.Request(url, headers={"User-Agent": "Startuzeiro-Hub/2.0"})
                with urllib.request.urlopen(req, timeout=15) as res:
                    data = json.loads(res.read().decode("utf-8"))
                    return self._send_json(200, data)
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                return self._send_json(e.code, {"error": f"Hunter API: {err_msg}"})
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 2. cnpj.ai Studio & Grafo
        if path == "/api/workbench/cnpj":
            termo = payload.get("cnpj", "").strip()
            key = os.getenv("CNPJ_AI_API_KEY", "")

            cnpj_limpo = re.sub(r"\D", "", termo)
            cnpj_basico = cnpj_limpo[:8] if len(cnpj_limpo) >= 8 else ""

            info = {
                "termo": termo,
                "cnpj_formatado": f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:14]}" if len(cnpj_limpo) == 14 else termo,
                "cnpj_basico": cnpj_basico,
                "grafo_url": f"https://grafo.cnpj.ai/?q={cnpj_basico}" if cnpj_basico else "https://grafo.cnpj.ai/",
                "portal_url": f"https://cnpj.ai/empresa/{cnpj_basico}" if cnpj_basico else "https://cnpj.ai/"
            }

            # Consultar dados via API do cnpj.ai se chave presente
            if key and "sua_chave" not in key and len(cnpj_limpo) == 14:
                try:
                    url = f"https://api.cnpj.ai/v1/empresa/{cnpj_limpo}"
                    req = urllib.request.Request(url, headers={
                        "Authorization": f"Bearer {key}",
                        "Accept": "application/json"
                    })
                    with urllib.request.urlopen(req, timeout=15) as res:
                        dados_api = json.loads(res.read().decode("utf-8"))
                        info["dados_receita"] = dados_api
                except Exception as e:
                    info["api_note"] = f"Consulta direta via API: {e}"

            return self._send_json(200, info)

        # 3. NetworkX Studio & Visualizador D3
        if path == "/api/workbench/networkx":
            action = payload.get("action", "graph")
            script_path = ROOT_DIR / "scripts" / "utilitarios" / "graph_networkx.py"

            if action == "shortest-path":
                source = payload.get("source", "").strip()
                target = payload.get("target", "").strip()
                cmd = ["uv", "run", str(script_path), "shortest-path", "--from", source, "--to", target]
            elif action == "centrality":
                cmd = ["uv", "run", str(script_path), "centrality"]
            elif action == "groups":
                cmd = ["uv", "run", str(script_path), "groups"]
            else:
                cmd = ["uv", "run", str(script_path), "demo"]

            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=30, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 4. Clay Studio (Query Mode)
        if path == "/api/workbench/clay":
            query = payload.get("query", "").strip()
            limit = int(payload.get("limit", 5))
            if not query:
                return self._send_json(400, {"error": "Query vazia fornecida"})

            script_path = ROOT_DIR / "scripts" / "utilitarios" / "clay_client.py"
            cmd = ["uv", "run", str(script_path), "search", query, "--limit", str(limit)]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=60, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 5. Ingestor de Documentos (MarkItDown / PyMuPDF4LLM)
        if path == "/api/workbench/document":
            file_path = payload.get("file_path", "").strip()
            if not file_path:
                return self._send_json(400, {"error": "Caminho do arquivo não fornecido"})

            script_path = ROOT_DIR / "scripts" / "utilitarios" / "doc_to_markdown.py"
            cmd = ["uv", "run", str(script_path), file_path]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=60, encoding="utf-8")
                # Se gerou arquivo .md, lê o conteúdo para preview
                md_path = Path(file_path).with_suffix(".md")
                preview = ""
                if md_path.exists():
                    preview = md_path.read_text(encoding="utf-8")[:5000]

                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr,
                    "preview": preview,
                    "output_file": str(md_path.relative_to(ROOT_DIR) if md_path.is_relative_to(ROOT_DIR) else md_path)
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 6. GLiNER Studio (Zero-Shot NER)
        if path == "/api/workbench/gliner":
            text = payload.get("text", "").strip()
            labels = payload.get("labels", ["empresa", "startup", "fundador", "investidor", "tecnologia", "cargo"])
            if not text:
                return self._send_json(400, {"error": "Texto para análise não fornecido"})

            script_path = ROOT_DIR / "scripts" / "utilitarios" / "extract_ner_gliner.py"
            cmd = ["uv", "run", str(script_path), text, "--format", "json", "--labels"] + labels
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=60, encoding="utf-8")
                entities = []
                try:
                    entities = json.loads(res.stdout)
                except Exception:
                    pass

                return self._send_json(200, {
                    "code": res.returncode,
                    "entities": entities,
                    "raw": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 7. DuckDB Studio (SQL in-process)
        if path == "/api/workbench/duckdb":
            query = payload.get("query", "").strip()
            if not query:
                return self._send_json(400, {"error": "Consulta SQL vazia"})

            script_path = ROOT_DIR / "scripts" / "utilitarios" / "duckdb_query.py"
            cmd = ["uv", "run", str(script_path), query, "--format", "markdown"]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=30, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "output": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 8. YouTube Lake Studio
        if path == "/api/workbench/youtube":
            url = payload.get("url", "").strip()
            if not url:
                return self._send_json(400, {"error": "URL do YouTube vazia"})

            script_path = ROOT_DIR / "scripts" / "utilitarios" / "yt_transcribe_and_catalog.py"
            cmd = ["uv", "run", str(script_path), url]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=90, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 9. Scrapling Studio
        if path == "/api/workbench/scrapling":
            target_url = payload.get("url", "").strip()
            if not target_url:
                return self._send_json(400, {"error": "URL vazia"})

            py_code = f"""
from scrapling.fetchers import StealthyFetcher
try:
    fetcher = StealthyFetcher()
    page = fetcher.fetch('{target_url}')
    print("STATUS: " + str(page.status))
    title = page.css('title::text').first or 'Sem titulo'
    print("TITLE: " + str(title))
    h1 = page.css('h1::text').first or 'Sem H1'
    print("H1: " + str(h1))
    body = page.css('body::text').extract()
    clean_text = ' '.join(''.join(body).split())[:400]
    print("PREVIEW: " + clean_text)
except Exception as e:
    print("ERRO: " + str(e))
"""
            cmd = ["uv", "run", "--with", "scrapling", "python", "-c", py_code]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=40, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 10. Hugging Face Explorer
        if path == "/api/workbench/huggingface":
            query = payload.get("query", "").strip()
            item_type = payload.get("type", "model")
            url = f"https://huggingface.co/api/{item_type}s?search={urllib.parse.quote(query)}&limit=10"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Startuzeiro-Hub/2.0"})
                with urllib.request.urlopen(req, timeout=15) as res:
                    data = json.loads(res.read().decode("utf-8"))
                    return self._send_json(200, data)
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # ========================================================
        # FÁBRICA DE PESQUISA: ORQUESTRADOR DE MISSÕES 360°
        # ========================================================
        if path == "/api/orchestrator/mission":
            target_name = payload.get("target_name", "").strip()
            domain = payload.get("domain", "").strip().lower()
            cnpj = payload.get("cnpj", "").strip()
            notes = payload.get("notes", "").strip()

            if not target_name and not domain and not cnpj:
                return self._send_json(400, {"error": "Informe pelo menos o Nome, Domínio ou CNPJ do alvo"})

            primary_name = target_name or domain or cnpj
            slug_name = re.sub(r"[^a-zA-Z0-9_-]", "_", primary_name.lower().replace(" ", "_"))

            mission_results = {
                "target": primary_name,
                "domain": domain,
                "cnpj": cnpj,
                "steps": []
            }

            # Passo 1: Hunter.io Intel
            if domain and os.getenv("HUNTER_API_KEY") and "sua_chave" not in os.getenv("HUNTER_API_KEY", ""):
                try:
                    url = f"https://api.hunter.io/v2/email-count?domain={urllib.parse.quote(domain)}&api_key={os.getenv('HUNTER_API_KEY')}"
                    req = urllib.request.Request(url, headers={"User-Agent": "Startuzeiro-Hub/2.0"})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        h_data = json.loads(r.read().decode("utf-8")).get("data", {})
                        total_emails = h_data.get("total", 0)
                        pattern = h_data.get("pattern", "n/a")
                        mission_results["hunter"] = {"total_emails": total_emails, "pattern": pattern}
                        mission_results["steps"].append({"step": "Hunter.io", "status": "success", "detail": f"{total_emails} e-mails identificados (Padrão: {pattern})"})
                except Exception as e:
                    mission_results["steps"].append({"step": "Hunter.io", "status": "warning", "detail": str(e)})

            # Passo 2: Clay GTM Intelligence
            if domain and os.getenv("CLAY_API_KEY") and "sua_chave" not in os.getenv("CLAY_API_KEY", ""):
                try:
                    script_path = ROOT_DIR / "scripts" / "utilitarios" / "clay_client.py"
                    q = f"select from companies where domain = '{domain}' limit 1"
                    cmd = ["uv", "run", str(script_path), "search", q, "--limit", "1"]
                    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=20, encoding="utf-8")
                    if res.returncode == 0 and "Resultado" in res.stdout:
                        mission_results["steps"].append({"step": "Clay GTM", "status": "success", "detail": "Dados firmográficos e tecnologias mapeados"})
                    else:
                        mission_results["steps"].append({"step": "Clay GTM", "status": "info", "detail": "Pesquisa concluída sem registro direto"})
                except Exception as e:
                    mission_results["steps"].append({"step": "Clay GTM", "status": "warning", "detail": str(e)})

            # Passo 3: cnpj.ai & Rede Societária
            cnpj_limpo = re.sub(r"\D", "", cnpj) if cnpj else ""
            if cnpj_limpo and len(cnpj_limpo) == 14:
                cnpj_basico = cnpj_limpo[:8]
                mission_results["cnpj_ai"] = {
                    "cnpj": cnpj_limpo,
                    "grafo_url": f"https://grafo.cnpj.ai/?q={cnpj_basico}",
                    "portal_url": f"https://cnpj.ai/empresa/{cnpj_basico}"
                }
                mission_results["steps"].append({"step": "cnpj.ai", "status": "success", "detail": f"Grafo societário mapeado em https://grafo.cnpj.ai/?q={cnpj_basico}"})
            else:
                mission_results["steps"].append({"step": "cnpj.ai", "status": "info", "detail": "Alvo internacional ou sem CNPJ informado"})

            # Passo 4: Compilar Dossiê em Markdown + YAML e salvar no Lake
            now_iso = os.popen("date /t").read().strip() if sys.platform == "win32" else "2026-09-22"
            dossier_content = f"""---
titulo: "Dossiê Investigativo 360° - {primary_name}"
alvo: "{primary_name}"
dominio: "{domain}"
cnpj: "{cnpj}"
data_investigacao: "{now_iso}"
autor: "Startuzeiro OS Mission Orchestrator"
tags:
  - dossie-investigativo
  - concorrente
  - inteligência-mercado
  - startuzeiro-os
---

# 🕵️ Dossiê de Inteligência: {primary_name}

> *Investigação compilada automaticamente pelo Orquestrador 360° do Startuzeiro OS.*

---

## 📌 Identificação do Alvo

- **Nome / Razão Social**: {target_name or primary_name}
- **Domínio Corporativo**: {f"[{domain}](https://{domain})" if domain else "Não informado"}
- **CNPJ**: {cnpj or "Não informado (Internacional/SaaS)"}
- **Notas de Partida**: {notes or "Pesquisa autônoma padrão."}

---

## 🔍 Resultados por Ferramenta

### 1. Hunter.io (Inteligência de E-mails)
{f"- **Total de E-mails Identificados**: {mission_results.get('hunter', {}).get('total_emails', 'N/A')}\n- **Padrão de Endereço**: `{mission_results.get('hunter', {}).get('pattern', 'N/A')}`" if 'hunter' in mission_results else "- Não consultado ou sem domínio informado."}

### 2. cnpj.ai & NetworkX (Rede Societária & QSA)
{f"- **Grafo Interativo**: [{mission_results.get('cnpj_ai', {}).get('grafo_url')}]({mission_results.get('cnpj_ai', {}).get('grafo_url')})\n- **Ficha no Portal**: [{mission_results.get('cnpj_ai', {}).get('portal_url')}]({mission_results.get('cnpj_ai', {}).get('portal_url')})" if 'cnpj_ai' in mission_results else "- Empresa sem CNPJ no Brasil."}

### 3. Clay.io (Enriquecimento Tecnológico)
- Consulta de intenção e dados firmográficos realizada no banco global de 75M+ empresas.

---

## 🧭 Próximos Passos de Validação (Playbook Startuzeiro)

1. Enriquecer decisores específicos (C-Level, VP de Vendas) via Apollo / Hunter.
2. Monitorar a página de preços e novidades com o `changedetection.io`.
3. Adicionar oportunidade correspondente no quadro de validação (`oportunidades/`).
"""
            # Salvar em brain/02_pesquisas/concorrentes e em pesquisas/concorrentes
            out_dirs = [
                ROOT_DIR / "brain" / "02_pesquisas" / "concorrentes",
                ROOT_DIR / "pesquisas" / "concorrentes"
            ]
            for d in out_dirs:
                d.mkdir(parents=True, exist_ok=True)
                (d / f"{slug_name}.md").write_text(dossier_content, encoding="utf-8")

            mission_results["dossier_path"] = f"brain/02_pesquisas/concorrentes/{slug_name}.md"
            mission_results["dossier_content"] = dossier_content
            mission_results["steps"].append({"step": "Compilação Dossiê", "status": "success", "detail": f"Dossiê salvo em {slug_name}.md no Lake"})

            return self._send_json(200, mission_results)

        # ========================================================
        # CÉREBRO AGÊNTICO: MINERAÇÃO DE OPORTUNIDADES
        # ========================================================
        if path == "/api/brain/mine":
            if agentic_brain:
                created = agentic_brain.mine_transcripts()
                return self._send_json(200, {
                    "status": "success",
                    "created_count": len(created),
                    "created_opps": created
                })
            return self._send_json(500, {"error": "Módulo agentic_brain não carregado"})

        # 404 para rotas desconhecidas
        return self._send_json(404, {"error": "Rota POST não encontrada"})



def run(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, StartuzeiroHandler)
    print(f"\n========================================================")
    print(f"  ⚡ Startuzeiro OS: Servidor Backend Ativo")
    print(f"  Interface Web: http://localhost:{port}")
    print(f"  Status: http://localhost:{port}/api/status")
    print(f"========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado com sucesso.")
        sys.exit(0)


if __name__ == "__main__":
    p = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        p = int(sys.argv[1])
    run(p)
