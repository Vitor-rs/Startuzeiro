import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(r"C:\Users\Vitor\AppData\Local\Google\Chrome\User Data\Default\AccountBookmarks")

if not p.exists():
    print("Arquivo AccountBookmarks não encontrado.")
    sys.exit(1)

with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

def explore(node, current_path=None):
    if current_path is None:
        current_path = []
    
    name = node.get("name", "")
    node_type = node.get("type")
    new_path = current_path + [name]

    if node_type == "folder":
        lower_name = name.lower().strip()
        lower_path = [x.lower().strip() for x in current_path]

        # Se for a pasta 'Tools' dentro de 'Ferramentas' (ou com 'ferramentas' no caminho)
        if lower_name == "tools" and any("ferramentas" in x for x in lower_path):
            print(f"\n=======================================================")
            print(f"🎯 ALVO ENCONTRADO: {' > '.join(new_path)}")
            print(f"=======================================================\n")
            children = node.get("children", [])
            print(f"Total de itens encontrados: {len(children)}\n")
            for i, c in enumerate(children, 1):
                ctype = c.get("type")
                cname = c.get("name")
                curl = c.get("url")
                if ctype == "url":
                    print(f"{i:2d}. {cname}\n    🔗 {curl}\n")
                elif ctype == "folder":
                    sub_count = len(c.get("children", []))
                    print(f"{i:2d}. 📁 [PASTA] {cname} ({sub_count} itens)\n")
                    for j, sc in enumerate(c.get("children", []), 1):
                        print(f"     {i}.{j}. {sc.get('name')} -> {sc.get('url')}")
            return

        for child in node.get("children", []):
            explore(child, new_path)

roots = data.get("roots", {})
for rname, rnode in roots.items():
    explore(rnode, [rname])
