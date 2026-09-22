"""
evals/tests/test_brain_pipeline.py - Teste Automatizado do Pipeline do Cérebro Agêntico
Valida o servidor, a mineração de oportunidades, o grafo de conhecimento e os endpoints do CRM.
"""

import urllib.request
import json
import time
import subprocess
import sys
from pathlib import Path

# Forçar UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def run_tests():
    print("[*] Iniciando servidor de teste na porta 5058...")
    proc = subprocess.Popen(["uv", "run", "scripts/app_server.py", "5058"], cwd=str(ROOT_DIR))
    time.sleep(2.5)

    try:
        base = "http://localhost:5058"

        # 1. Status
        res = urllib.request.urlopen(f"{base}/api/status")
        status = json.loads(res.read().decode("utf-8"))
        print(f"[✓] Status: {status['system']} - Active Tools: {status['active_tools_count']}")
        assert status["status"] == "online"

        # 2. Grafo de Conhecimento do Cérebro
        res = urllib.request.urlopen(f"{base}/api/brain/graph")
        graph = json.loads(res.read().decode("utf-8"))
        print(f"[✓] Grafo do Cérebro: {len(graph['nodes'])} nós e {len(graph['links'])} conexões")
        assert len(graph["nodes"]) >= 8

        # 3. Mineração de Transcrições
        req = urllib.request.Request(f"{base}/api/brain/mine", data=b"{}", headers={"Content-Type": "application/json"})
        res = urllib.request.urlopen(req)
        mine_res = json.loads(res.read().decode("utf-8"))
        print(f"[✓] Mineração Agêntica: {mine_res['status']}")
        assert mine_res["status"] == "success"

        # 4. Oportunidades do CRM
        res = urllib.request.urlopen(f"{base}/api/crm/opportunities")
        opps = json.loads(res.read().decode("utf-8"))
        print(f"[✓] Oportunidades no CRM: {len(opps)} cadastradas")
        assert len(opps) >= 4
        # Verificar se as oportunidades possuem ICE Score válido
        for opp in opps:
            print(f"    - {opp['id']}: {opp['title']} (ICE: {opp['ice_score']}) [{opp['category']}]")
            assert opp["ice_score"] > 0

        # 5. Lake de Vídeos
        res = urllib.request.urlopen(f"{base}/api/crm/lake")
        lake = json.loads(res.read().decode("utf-8"))
        print(f"[✓] Vídeos no Lake: {len(lake)} catalogados")
        assert len(lake) >= 5

        print("\n========================================================")
        print("  🎉 TODOS OS TESTES DO CÉREBRO AGÊNTICO PASSARAM COM SUCESSO!")
        print("========================================================\n")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    run_tests()
