#!/usr/bin/env python3
"""
Servidor Backend Bridge para o Startuzeiro Hub Dashboard.
Fornece API REST local para executar e testar ferramentas (Clay, MailAccess,
Scrapling, YouTube Transcriber, etc.) e serve os arquivos estáticos do dashboard.

Uso:
    uv run scripts/app_server.py [--port 5050]
"""

import os
import sys
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

        if path == "/api/status":
            return self._send_json(200, {
                "status": "online",
                "port": PORT,
                "project": "Startuzeiro Hub",
                "python_version": sys.version.split()[0],
                "has_clay": bool(os.getenv("CLAY_API_KEY") and "sua_chave" not in os.getenv("CLAY_API_KEY", "")),
                "has_hunter": bool(os.getenv("HUNTER_API_KEY") and "sua_chave" not in os.getenv("HUNTER_API_KEY", "")),
                "has_cnpj_ai": bool(os.getenv("CNPJ_AI_API_KEY") and "sua_chave" not in os.getenv("CNPJ_AI_API_KEY", "")),
                "has_transcript_api": bool(os.getenv("TRANSCRIPT_API_KEY") and "sua_chave" not in os.getenv("TRANSCRIPT_API_KEY", ""))
            })

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
                            return self._send_json(200, tools_data)
                except Exception:
                    pass

            yaml_path = ROOT_DIR / "ferramentas" / "catalogo.yaml"
            if yaml_path.exists():
                try:
                    import yaml
                    with open(yaml_path, "r", encoding="utf-8") as f:
                        tools_data = yaml.safe_load(f)
                except Exception as e:
                    return self._send_json(500, {"error": f"Erro ao ler ferramentas: {e}"})
            return self._send_json(200, tools_data)

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

        # 1. Executar Clay Search
        if path == "/api/run/clay":
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

        # 2. Executar YouTube Transcribe
        if path == "/api/run/youtube":
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

        # 3. Executar MailAccess
        if path == "/api/run/mailaccess":
            action = payload.get("action", "doctor")
            cmd = ["uvx", "mailaccess"]
            if action == "doctor":
                cmd.append("doctor")
            elif action == "find-email":
                name = payload.get("name", "").strip()
                domain = payload.get("domain", "").strip()
                if not name or not domain:
                    return self._send_json(400, {"error": "Nome e domínio são obrigatórios para find-email"})
                cmd.extend(["find-email", "--name", name, "--domain", domain])
            elif action == "investigate":
                email = payload.get("email", "").strip()
                if not email:
                    return self._send_json(400, {"error": "E-mail é obrigatório para investigate"})
                cmd.extend(["investigate", email])
            elif action == "harvest":
                domain = payload.get("domain", "").strip()
                if not domain:
                    return self._send_json(400, {"error": "Domínio é obrigatório para harvest"})
                cmd.extend(["harvest-emails", "--domain", domain])
            else:
                return self._send_json(400, {"error": f"Ação desconhecida: {action}"})

            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=60, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 4. Executar Scrapling
        if path == "/api/run/scrapling":
            target_url = payload.get("url", "").strip()
            if not target_url:
                return self._send_json(400, {"error": "URL de destino vazia"})

            py_code = f"""
from scrapling import Fetcher
import json, sys

try:
    res = Fetcher().get({json.dumps(target_url)})
    titles = res.css('title::text')
    title = str(titles[0]).strip() if titles else 'Sem título'
    h1s = res.css('h1::text')
    h1 = str(h1s[0]).strip() if h1s else 'Sem H1'
    status = res.status
    text = res.get_all_text()[:1000].strip()
    print(json.dumps({{
        "status": status,
        "title": title,
        "h1": h1,
        "preview": text
    }}, ensure_ascii=False))
except Exception as e:
    print(f"[ERRO] {{e}}", file=sys.stderr)
    sys.exit(1)
"""
            cmd = ["uv", "run", "--with", "scrapling[all]", "python", "-c", py_code]
            try:
                res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=30, encoding="utf-8")
                return self._send_json(200, {
                    "code": res.returncode,
                    "stdout": res.stdout,
                    "stderr": res.stderr
                })
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 5. Consulta rápida Hunter.io
        if path == "/api/run/hunter":
            domain = payload.get("domain", "").strip()
            hunter_key = os.getenv("HUNTER_API_KEY")
            if not hunter_key or "sua_chave" in hunter_key:
                return self._send_json(400, {"error": "HUNTER_API_KEY não configurada no .env"})
            url = f"https://api.hunter.io/v2/email-count?domain={urllib.parse.quote(domain)}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "StartuzeiroHub/1.0"})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    return self._send_json(200, data)
            except urllib.error.HTTPError as e:
                return self._send_json(e.code, {"error": e.read().decode("utf-8")})
            except Exception as e:
                return self._send_json(500, {"error": str(e)})

        # 6. Consulta rápida cnpj.ai
        if path == "/api/run/cnpj":
            cnpj = payload.get("cnpj", "").replace(".", "").replace("/", "").replace("-", "").strip()
            clean_basic = cnpj[:8] if len(cnpj) >= 8 else cnpj
            graph_url = f"https://grafo.cnpj.ai/?q={clean_basic}"
            return self._send_json(200, {
                "cnpj": cnpj,
                "cnpj_basico": clean_basic,
                "graph_url": graph_url,
                "portal_url": f"https://cnpj.ai/{cnpj}"
            })

        self._send_json(404, {"error": "Endpoint não encontrado"})


def main():
    global PORT
    if len(sys.argv) > 1 and sys.argv[1] == "--port" and len(sys.argv) > 2:
        PORT = int(sys.argv[2])

    print("=" * 65)
    print(f"🚀 Startuzeiro Hub - Painel Centralizado de Ferramentas")
    print(f"📡 Servidor local ativo em: http://localhost:{PORT}")
    print(f"📁 Servindo frontend de:    {DASHBOARD_DIR}")
    print("=" * 65)
    print("Pressione Ctrl+C para encerrar o servidor.\n")

    httpd = HTTPServer(("127.0.0.1", PORT), StartuzeiroHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Encerrando servidor do Startuzeiro Hub...")
        httpd.server_close()


if __name__ == "__main__":
    main()
