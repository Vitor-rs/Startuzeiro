#!/usr/bin/env python3
"""
graph_networkx.py - Análise e Visualização de Redes Societárias & Grafos B2B
Startuzeiro Lab

Utiliza NetworkX para modelagem ágil em memória, identificação de caminhos mais curtos,
detecção de grupos econômicos, centralidade de sócios e exportação para HTML interativo.

Uso:
  uv run scripts/utilitarios/graph_networkx.py demo
  uv run scripts/utilitarios/graph_networkx.py shortest-path --from "Investidor Anjo" --to "Startuzeiro Tech"
  uv run scripts/utilitarios/graph_networkx.py groups
  uv run scripts/utilitarios/graph_networkx.py centrality
  uv run scripts/utilitarios/graph_networkx.py export-html -o "pesquisas/grafo_interativo.html"
"""

import sys
import json
import argparse
from pathlib import Path
import networkx as nx

def build_demo_graph() -> nx.DiGraph:
    """Cria uma rede societária e de investimentos de demonstração."""
    G = nx.DiGraph()

    # Adicionar Nós com Metadados
    nodes = [
        ("Vitor Fundador", {"tipo": "pessoa", "cargo": "Fundador & CEO"}),
        ("Startuzeiro Tech", {"tipo": "empresa", "cnpj": "11.111.111/0001-22", "setor": "Software & IA"}),
        ("Investidor Anjo", {"tipo": "pessoa", "cargo": "Angel Investor"}),
        ("Holding Participações", {"tipo": "empresa", "cnpj": "22.222.222/0001-33", "setor": "Holding"}),
        ("Fundo Venture Capital", {"tipo": "empresa", "cnpj": "33.333.333/0001-44", "setor": "Venture Capital"}),
        ("Fintech Parceira", {"tipo": "empresa", "cnpj": "44.444.444/0001-55", "setor": "Fintech"}),
        ("Sócio Oculto", {"tipo": "pessoa", "cargo": "Diretor Operacional"}),
    ]
    for node, attrs in nodes:
        G.add_node(node, **attrs)

    # Adicionar Conexões (Arestas com Relações)
    edges = [
        ("Vitor Fundador", "Startuzeiro Tech", {"relacao": "SÓCIO_FUNDADOR", "detalhe": "60% das quotas"}),
        ("Investidor Anjo", "Startuzeiro Tech", {"relacao": "INVESTIU_EM", "detalhe": "R$ 500k Seed"}),
        ("Investidor Anjo", "Holding Participações", {"relacao": "SÓCIO_ADMINISTRADOR", "detalhe": "Controle 80%"}),
        ("Holding Participações", "Fintech Parceira", {"relacao": "CONTROLADORA", "detalhe": "Participação Majoritária"}),
        ("Fundo Venture Capital", "Fintech Parceira", {"relacao": "INVESTIU_EM", "detalhe": "Série A R$ 12M"}),
        ("Sócio Oculto", "Holding Participações", {"relacao": "CONSELHEIRO", "detalhe": "Membro do Conselho"}),
        ("Sócio Oculto", "Startuzeiro Tech", {"relacao": "MENTOR_ADVISOR", "detalhe": "Equity 5%"}),
    ]
    for u, v, attrs in edges:
        G.add_edge(u, v, **attrs)

    return G

def find_shortest_path(G: nx.DiGraph, source: str, target: str):
    """Encontra o menor caminho e intermediários entre duas entidades."""
    U = G.to_undirected()
    try:
        path = nx.shortest_path(U, source=source, target=target)
        print(f"\n🎯 Menor caminho encontrado ({len(path) - 1} graus de separação):")
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            # Identificar relação no grafo direcionado original
            rel = G.get_edge_data(u, v) or G.get_edge_data(v, u) or {}
            rel_nome = rel.get("relacao", "CONECTADO_A")
            rel_det = rel.get("detalhe", "")
            print(f"   [{u}] ──({rel_nome}: {rel_det})──> [{v}]")
    except nx.NetworkXNoPath:
        print(f"\n❌ Nenhum caminho societário encontrado entre '{source}' e '{target}'.")
    except nx.NodeNotFound as e:
        print(f"\n❌ Erro: {e}")

def detect_groups(G: nx.DiGraph):
    """Detecta componentes conexos (grupos econômicos independentes)."""
    U = G.to_undirected()
    components = list(nx.connected_components(U))
    print(f"\n🏢 Grupos Econômicos Detectados: {len(components)}")
    for idx, comp in enumerate(components, 1):
        print(f"\n--- Grupo #{idx} ({len(comp)} membros) ---")
        empresas = [n for n in comp if G.nodes[n].get("tipo") == "empresa"]
        pessoas = [n for n in comp if G.nodes[n].get("tipo") == "pessoa"]
        print(f"  Pessoas Físicas: {', '.join(pessoas) if pessoas else 'Nenhuma'}")
        print(f"  Empresas: {', '.join(empresas) if empresas else 'Nenhuma'}")

def compute_centrality(G: nx.DiGraph):
    """Calcula nós de maior influência e poder de intermediação."""
    U = G.to_undirected()
    degree = nx.degree_centrality(U)
    betweenness = nx.betweenness_centrality(U)

    print("\n👑 Ranking de Centralidade & Influência:")
    print(f"{'Entidade':<25} | {'Tipo':<10} | {'Conexões (Grau)':<15} | {'Intermediação (Hub)'}")
    print("-" * 75)
    
    sorted_nodes = sorted(U.nodes(), key=lambda n: (betweenness[n], degree[n]), reverse=True)
    for n in sorted_nodes:
        tipo = G.nodes[n].get("tipo", "n/a")
        deg_score = f"{degree[n]:.2f}"
        bet_score = f"{betweenness[n]:.2f}"
        print(f"{n:<25} | {tipo:<10} | {deg_score:<15} | {bet_score}")

def export_interactive_html(G: nx.DiGraph, output_file: Path):
    """Gera um visualizador HTML interativo e autônomo com D3.js."""
    nodes_data = []
    for n, attrs in G.nodes(data=True):
        tipo = attrs.get("tipo", "pessoa")
        color = "#3b82f6" if tipo == "pessoa" else "#10b981"
        nodes_data.append({
            "id": n,
            "name": n,
            "tipo": tipo,
            "color": color,
            "detalhes": str(attrs)
        })

    links_data = []
    for u, v, attrs in G.edges(data=True):
        links_data.append({
            "source": u,
            "target": v,
            "label": attrs.get("relacao", ""),
            "detalhe": attrs.get("detalhe", "")
        })

    graph_json = json.dumps({"nodes": nodes_data, "links": links_data}, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grafo Societário Interativo - Startuzeiro</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            margin: 0;
            background-color: #0b0f19;
            color: #f8fafc;
            font-family: system-ui, -apple-system, sans-serif;
            overflow: hidden;
        }}
        #header {{
            position: absolute;
            top: 16px;
            left: 20px;
            z-index: 10;
            background: rgba(15, 23, 42, 0.85);
            padding: 12px 20px;
            border-radius: 12px;
            border: 1px solid rgba(51, 65, 85, 0.6);
            backdrop-filter: blur(8px);
        }}
        #header h1 {{ margin: 0 0 4px 0; font-size: 16px; font-weight: 700; color: #60a5fa; }}
        #header p {{ margin: 0; font-size: 12px; color: #94a3b8; }}
        #legend {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            z-index: 10;
            background: rgba(15, 23, 42, 0.85);
            padding: 10px 16px;
            border-radius: 8px;
            border: 1px solid rgba(51, 65, 85, 0.6);
            font-size: 12px;
            display: flex;
            gap: 16px;
        }}
        .legend-item {{ display: flex; items-center; gap: 6px; }}
        .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-top: 2px; }}
        .link {{ stroke: #475569; stroke-opacity: 0.6; stroke-width: 1.5px; }}
        .link-label {{ font-size: 9px; fill: #94a3b8; text-anchor: middle; pointer-events: none; }}
        .node {{ cursor: pointer; }}
        .node-label {{ font-size: 11px; fill: #f1f5f9; font-weight: 600; pointer-events: none; text-shadow: 0 1px 3px rgba(0,0,0,0.8); }}
        #tooltip {{
            position: absolute;
            display: none;
            background: #1e293b;
            color: #fff;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 11px;
            border: 1px solid #334155;
            pointer-events: none;
            z-index: 20;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🌐 Visualizador de Rede Societária & B2B</h1>
        <p>Arraste os nós para navegar. Scroll para zoom.</p>
    </div>

    <div id="legend">
        <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> Pessoa Física</div>
        <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> Pessoa Jurídica / Empresa</div>
    </div>

    <div id="tooltip"></div>
    <svg id="graph" width="100%" height="100vh"></svg>

    <script>
        const data = {graph_json};
        const width = window.innerWidth;
        const height = window.innerHeight;

        const svg = d3.select("#graph");
        const g = svg.append("g");

        // Zoom & Pan
        svg.call(d3.zoom().scaleExtent([0.3, 4]).on("zoom", (event) => {{
            g.attr("transform", event.transform);
        }}));

        // Simulation
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(140))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(40));

        // Links
        const link = g.append("g")
            .selectAll("line")
            .data(data.links)
            .join("line")
            .attr("class", "link");

        // Link Labels
        const linkLabel = g.append("g")
            .selectAll("text")
            .data(data.links)
            .join("text")
            .attr("class", "link-label")
            .text(d => d.label);

        // Nodes
        const tooltip = d3.select("#tooltip");
        const node = g.append("g")
            .selectAll("g")
            .data(data.nodes)
            .join("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("circle")
            .attr("r", d => d.tipo === "pessoa" ? 14 : 18)
            .attr("fill", d => d.color)
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5);

        node.append("text")
            .attr("class", "node-label")
            .attr("x", 22)
            .attr("y", 4)
            .text(d => d.name);

        node.on("mouseover", (event, d) => {{
            tooltip.style("display", "block")
                .html(`<strong>${{d.name}}</strong><br>Tipo: ${{d.tipo}}<br>Info: ${{d.detalhes}}`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 20) + "px");
        }}).on("mouseout", () => {{
            tooltip.style("display", "none");
        }});

        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            linkLabel
                .attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2 - 4);

            node
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});

        function dragstarted(event) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }}

        function dragged(event) {{
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }}

        function dragended(event) {{
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }}
    </script>
</body>
</html>
"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content, encoding="utf-8")
    print(f"\n[OK] Grafo interativo HTML gerado com sucesso!")
    print(f"     Arquivo: {output_file}")
    print(f"     Abra diretamente no navegador para interagir!")

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Análise e visualização de grafos societários via NetworkX.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando demo
    subparsers.add_parser("demo", help="Exibe estatísticas do grafo de demonstração")

    # Subcomando shortest-path
    sub_path = subparsers.add_parser("shortest-path", help="Encontra o menor caminho entre duas entidades")
    sub_path.add_argument("--from", dest="source", required=True, help="Nome da entidade de origem")
    sub_path.add_argument("--to", dest="target", required=True, help="Nome da entidade de destino")

    # Subcomando groups
    subparsers.add_parser("groups", help="Detecta grupos econômicos e componentes conexos")

    # Subcomando centrality
    subparsers.add_parser("centrality", help="Calcula centralidade e nós mais influentes")

    # Subcomando export-html
    sub_export = subparsers.add_parser("export-html", help="Exporta o grafo para visualização HTML interativa")
    sub_export.add_argument("-o", "--output", default="pesquisas/grafo_societario.html", help="Caminho do arquivo HTML")

    args = parser.parse_args()
    G = build_demo_graph()

    if args.command == "demo":
        print(f"📊 Rede Societária Carregada:")
        print(f"   Total de Entidades (Nós): {G.number_of_nodes()}")
        print(f"   Total de Relações (Arestas): {G.number_of_edges()}")
        print("\nEntidades cadastradas:")
        for n, attrs in G.nodes(data=True):
            tipo = attrs.get("tipo", "n/a")
            print(f"   - [{tipo.upper()}] {n}")
        print("\nConexões societárias:")
        for u, v, attrs in G.edges(data=True):
            print(f"   - {u} -> ({attrs.get('relacao')}) -> {v}")

    elif args.command == "shortest-path":
        find_shortest_path(G, args.source, args.target)

    elif args.command == "groups":
        detect_groups(G)

    elif args.command == "centrality":
        compute_centrality(G)

    elif args.command == "export-html":
        export_interactive_html(G, Path(args.output))

if __name__ == "__main__":
    main()
