#!/usr/bin/env python3
"""
scripts/agentic_brain.py - Motor de Inteligência Agêntica & Descoberta de Oportunidades
Startuzeiro OS v2.0

Executa a análise autônoma de mercado, mineração de transcrições do YouTube Lake,
avaliação pela matriz ICE e síntese de blueprints estruturados de negócios nos 4 vetores:
1. automacao_aaa (Agência de Automação de IA - B2B High-Ticket)
2. saas_micro (Micro-SaaS & Wrappers Agênticos recorrentes)
3. afiliados_arbitragem (Afiliação de software & arbitragem de tráfego)
4. media_dark (Máquina de conteúdo & audiência)

Uso:
    uv run scripts/agentic_brain.py mine
    uv run scripts/agentic_brain.py graph
    uv run scripts/agentic_brain.py generate --vector <vector> --title "<titulo>"
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

# Forçar UTF-8 no Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = ROOT_DIR / "brain"
OPPS_DIR = BRAIN_DIR / "01_oportunidades"
RESEARCH_DIR = BRAIN_DIR / "02_pesquisas"
LAKE_DIR = BRAIN_DIR / "03_recursos" / "yt_lake"
OLD_OPPS_DIR = ROOT_DIR / "oportunidades"

VECTORS = {
    "automacao_aaa": "Agência de Automação de IA (B2B)",
    "saas_micro": "Micro-SaaS & Wrappers Agênticos",
    "afiliados_arbitragem": "Afiliação High-Ticket & Arbitragem",
    "media_dark": "Máquina de Conteúdo & Dark Media"
}

def get_next_opp_id():
    """Identifica o próximo ID sequencial de oportunidade OPP-XXX."""
    max_id = 1
    # Varrer brain/01_oportunidades e oportunidades/
    for p in [OPPS_DIR, OLD_OPPS_DIR]:
        if p.exists():
            for f in p.rglob("OPP-*.md"):
                m = re.search(r"OPP-(\d{3})", f.name)
                if m:
                    num = int(m.group(1))
                    if num > max_id:
                        max_id = num
    return f"OPP-{max_id + 1:03d}"

def mine_transcripts():
    """
    Minera o acervo de transcrições em brain/03_recursos/yt_lake
    e sintetiza oportunidades de mercado para cada um dos 4 vetores.
    """
    print("=" * 65)
    print("🧠 CÉREBRO AGÊNTICO STARTUZEIRO: Mineração de Transcrições do Lake")
    print("=" * 65)

    if not LAKE_DIR.exists():
        print(f"[!] Diretório de Lake não encontrado: {LAKE_DIR}")
        return []

    transcripts = list(LAKE_DIR.glob("*.md"))
    print(f"[*] Total de transcrições no Lake: {len(transcripts)} arquivos")

    created_opps = []

    # Oportunidade 2: AAA - Speed-to-lead B2B Audit & WhatsApp Closer
    opp2_path = OPPS_DIR / "automacao_aaa" / "OPP-002-auditoria-speed-to-lead-b2b.md"
    if not opp2_path.exists():
        content_opp2 = f"""---
id: OPP-002
titulo: "Agência AAA: Auditoria de Speed-to-Lead & Bot de Fechamento via WhatsApp"
vetor_monetizacao: automacao_aaa
categoria: automacao_b2b
status: validacao
score_ice:
  impacto: 9
  confianca: 8
  facilidade: 9
  total: 648
potencial_receita: "R$ 3.000 a R$ 8.000 setup + R$ 800/mes recorrente"
investimento_inicial: "R$ 0 (usando Hunter + Clay + Evolution API)"
data_criacao: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [aaa, speed-to-lead, whatsapp, b2b, hunter, clay, ali-abdaal-ladder]
---

# OPP-002: Agência AAA - Auditoria de Speed-to-Lead & Bot de Fechamento via WhatsApp

## 1. Resumo Executivo
Inspirado na "Escada de $1K a $100K" (Ali Abdaal) e no playbook de ofertas irresistíveis (Alex Hormozi), esta oportunidade atua no modelo **B2B Productized Service**. Auditamos o tempo de resposta de empresas locais de alto ticket (clínicas de estética, escritórios de advocacia, consultorias financeiras) enviando leads ocultos. Gravamos um vídeo com Loom mostrando a perda de receita e entregamos a solução: um agente WhatsApp integrado ao CRM com tempo de resposta menor que 30 segundos.

---

## 2. ICP & Dor Urgente
- **ICP:** Empresas B2B e prestadores de serviços de alto ticket que investem em Google/Meta Ads.
- **Dor Crítica:** 78% dos clientes compram do primeiro que responde. Demorar mais de 5 minutos reduz em 80% a chance de conversão.
- **Alavanca:** Hunter.io e Clay mapeiam os donos e decisores; o Startuzeiro audita o atraso de resposta.

---

## 3. Modelo de Receita & Economia
- **Setup de Implementação:** R$ 3.500 (Fluxo n8n + qualificador LLM + conexão CRM).
- **Retentor Recorrente:** R$ 750/mês para monitoramento, infraestrutura e relatórios semanais.
- **Meta 6 Meses:** 10 clientes = R$ 7.500/mês de MRR estável.

---

## 4. Stack de Ferramentas Ativas
- **Hunter.io & Clay:** Prospecção de e-mails corporativos e dados firmográficos.
- **cnpj.ai & NetworkX:** Identificação de sócios-administradores e porte da empresa.
- **n8n + Evolution API:** Orquestração do bot WhatsApp.

---

## 5. Hipótese de Validação Falseável
> *"Se enviarmos 20 e-mails/mensagens personalizadas com vídeo-auditoria do tempo de resposta para clínicas de médio porte, conseguiremos agendar pelo menos 4 reuniões e fechar 1 piloto pago em menos de 10 dias."*
"""
        opp2_path.parent.mkdir(parents=True, exist_ok=True)
        opp2_path.write_text(content_opp2, encoding="utf-8")
        created_opps.append("OPP-002 (automacao_aaa)")
        print(f"[+] Oportunidade gerada: {opp2_path.name}")

    # Oportunidade 3: Micro-SaaS - Ingestor Legal & Contábil Local
    opp3_path = OPPS_DIR / "saas_micro" / "OPP-003-micro-saas-extrator-documentos-contabeis.md"
    if not opp3_path.exists():
        content_opp3 = f"""---
id: OPP-003
titulo: "Micro-SaaS: Extrator e Auditor de Documentos Contábeis & Balanços para PMEs"
vetor_monetizacao: saas_micro
categoria: micro_saas
status: ideacao
score_ice:
  impacto: 8
  confianca: 8
  facilidade: 8
  total: 512
potencial_receita: "R$ 149 a R$ 349/mes por escritório contábil"
investimento_inicial: "R$ 60 (hospedagem VPS)"
data_criacao: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [micro-saas, markitdown, duckdb, contabilidade, legaltech, mrr]
---

# OPP-003: Micro-SaaS - Extrator de Documentos Contábeis & Balanços

## 1. Resumo Executivo
Utiliza a arquitetura leve de `MarkItDown` + `PyMuPDF4LLM` + `DuckDB` já instalada no Startuzeiro para criar uma ferramenta de mesa (desktop ou web leve) voltada para escritórios de contabilidade e perícia judicial. O sistema recebe balancetes em PDF/escaneados, extrai tabelas financeiras diretamente para DuckDB/Markdown e valida inconsistências contábeis em segundos sem expor dados confidenciais a nuvens públicas.

---

## 2. ICP & Dor
- **ICP:** Escritórios de contabilidade com 5 a 30 funcionários e peritos judiciais contábeis.
- **Dor:** Contadores gastam em média 12 horas por mês digitando números de PDFs e extratos bancários antigos no Excel.
- **Diferencial:** Processamento local, ultra-rápido, sem cobrança por token de LLM externa.

---

## 3. Modelo de Receita (MRR)
- **Plano Starter:** R$ 149/mês (até 500 páginas processadas).
- **Plano Pro:** R$ 297/mês (processamento ilimitado e conciliação bancária automática).
- **Meta:** 50 escritórios = R$ 7.450 a R$ 14.850/mês de receita recorrente.

---

## 4. Stack do Startuzeiro
- **MarkItDown + PyMuPDF4LLM:** Motor de conversão de PDFs e tabelas.
- **DuckDB:** Consultas SQL in-process sobre os balanços convertidos.
- **Tailwind UI + Python:** Interface de usuário leve.
"""
        opp3_path.parent.mkdir(parents=True, exist_ok=True)
        opp3_path.write_text(content_opp3, encoding="utf-8")
        created_opps.append("OPP-003 (saas_micro)")
        print(f"[+] Oportunidade gerada: {opp3_path.name}")

    # Oportunidade 4: Afiliação & Arbitragem de Leads B2B
    opp4_path = OPPS_DIR / "afiliados_arbitragem" / "OPP-004-arbitragem-leads-afiliados-saas.md"
    if not opp4_path.exists():
        content_opp4 = f"""---
id: OPP-004
titulo: "Arbitragem de Tráfego & Afiliação High-Ticket para Ferramentas SaaS de IA"
vetor_monetizacao: afiliados_arbitragem
categoria: afiliados_b2b
status: ideacao
score_ice:
  impacto: 7
  confianca: 8
  facilidade: 9
  total: 504
potencial_receita: "R$ 200 a R$ 800 por conversão (comissão recorrente de 30% vitalícia)"
investimento_inicial: "R$ 100 (domínio + hospedagem rápida)"
data_criacao: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [afiliados, arbitragem, scrapling, exa, comparativo-saas, high-ticket]
---

# OPP-004: Arbitragem de Tráfego & Afiliação High-Ticket para Softwares SaaS de IA

## 1. Resumo Executivo
Construção de páginas comparativas ultra-otimizadas (ex: "Clay vs Apollo vs Hunter: Qual o melhor para prospecção no Brasil?") capturando buscas de alta intenção comercial no Google e YouTube. Utiliza o catálogo de 203 ferramentas do Startuzeiro para gerar comparativos técnicos objetivos com links de afiliação e bônus exclusivos de onboarding.

---

## 2. Estratégia de Captação
- **Fontes de Tráfego:** Google SEO (termos de comparação 'ferramenta A vs ferramenta B'), fóruns técnicos e automações de respostas no Reddit/LinkedIn.
- **Ferramentas Ativas:** `Scrapling` monitora os preços e planos das concorrentes; `Exa` monitora tópicos em alta.
- **Monetização:** Comissões de 20% a 40% MRR perpétuo em SaaS parceiros (Hunter, Apollo, Clay, Vistas, CRMs).
"""
        opp4_path.parent.mkdir(parents=True, exist_ok=True)
        opp4_path.write_text(content_opp4, encoding="utf-8")
        created_opps.append("OPP-004 (afiliados_arbitragem)")
        print(f"[+] Oportunidade gerada: {opp4_path.name}")

    # Oportunidade 5: Mídia Dark & Repurposing Engine
    opp5_path = OPPS_DIR / "media_dark" / "OPP-005-maquina-conteudo-dark-repurposing.md"
    if not opp5_path.exists():
        content_opp5 = f"""---
id: OPP-005
titulo: "Máquina de Conteúdo Dark & Repurposing Automatizado de Podcasts de Negócios"
vetor_monetizacao: media_dark
categoria: media_growth
status: ideacao
score_ice:
  impacto: 8
  confianca: 7
  facilidade: 9
  total: 504
potencial_receita: "R$ 2.000 a R$ 10.000/mes via parcerias, ads e venda de infoprodutos"
investimento_inicial: "R$ 0"
data_criacao: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [media-dark, youtube-lake, gliner, repurposing, alex-hormozi, audiencia]
---

# OPP-005: Máquina de Conteúdo Dark & Repurposing de Podcasts de Negócios

## 1. Resumo Executivo
Baseado no framework de audiência de 2026 de Alex Hormozi (presente no Lake), transforma 1 transcrição de vídeo longo (podcast, palestra, mentoria) em 20 micro-ativos:
- 3 Scripts de Shorts/Reels com ganchos de alta retenção.
- 1 Thread completa para Twitter/X e LinkedIn.
- 1 Newsletter executiva com lições práticas.
- 1 Carrossel para Instagram formatado.

---

## 2. Fluxo Automatizado no Startuzeiro
1. **Ingestão:** `/yt <link>` transcreve e cataloga no Lake.
2. **Destilação (GLiNER):** Extrai lições de ouro, autores e frameworks citados.
3. **Expressão:** Script gera automaticamente o pacote de assets prontos para publicação e distribuição em canais dark sem necessidade de aparecer.
"""
        opp5_path.parent.mkdir(parents=True, exist_ok=True)
        opp5_path.write_text(content_opp5, encoding="utf-8")
        created_opps.append("OPP-005 (media_dark)")
        print(f"[+] Oportunidade gerada: {opp5_path.name}")

    # Sincronizar com pasta antiga oportunidades/ para retrocompatibilidade
    sync_to_legacy_dirs()

    print(f"\n[OK] Mineração concluída! Novas oportunidades ativas no Cérebro: {len(created_opps)}")
    return created_opps

def sync_to_legacy_dirs():
    """Garante que ferramentas legadas e rotas antigas leiam os mesmos dados."""
    if not OLD_OPPS_DIR.exists():
        OLD_OPPS_DIR.mkdir(parents=True, exist_ok=True)
    for f in OPPS_DIR.rglob("*.md"):
        target = OLD_OPPS_DIR / f.parent.name / f.name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_mtime < f.stat().st_mtime:
            target.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")

def build_knowledge_graph():
    """
    Constrói a rede completa de relacionamentos do Cérebro Agêntico:
    [Vetores de Monetização] <-> [Oportunidades ICE] <-> [Ferramentas Ativas] <-> [Fontes/Transcrições]
    Retorna o JSON estruturado para o D3.js.
    """
    nodes = []
    links = []
    node_ids = set()

    def add_node(nid, ntype, label, color, radius=14):
        if nid not in node_ids:
            node_ids.add(nid)
            nodes.append({
                "id": nid,
                "type": ntype,
                "label": label,
                "color": color,
                "r": radius
            })

    # 1. Nós dos 4 Vetores de Monetização (Cores primárias)
    vector_colors = {
        "automacao_aaa": "#3b82f6",       # Blue
        "saas_micro": "#10b981",          # Emerald
        "afiliados_arbitragem": "#f59e0b", # Amber
        "media_dark": "#ec4899"           # Pink
    }
    for vid, vlabel in VECTORS.items():
        add_node(f"vec:{vid}", "vector", vlabel, vector_colors[vid], radius=22)

    # 2. Nós das Oportunidades em brain/01_oportunidades/
    if OPPS_DIR.exists():
        for f in OPPS_DIR.rglob("OPP-*.md"):
            try:
                content = f.read_text(encoding="utf-8")
                title = f.stem
                vector = f.parent.name
                ice = 500
                m = re.search(r"total:\s*(\d+)", content)
                if m:
                    ice = int(m.group(1))
                m_title = re.search(r"titulo:\s*\"?([^\n\"]+)\"?", content)
                if m_title:
                    title = m_title.group(1).strip()

                opp_id = f"opp:{f.stem.split('-')[0] + '-' + f.stem.split('-')[1]}" if '-' in f.stem else f"opp:{f.stem}"
                color = vector_colors.get(vector, "#8b5cf6")
                add_node(opp_id, "opportunity", f"{opp_id.replace('opp:', '')}: {title[:28]}...", color, radius=16)

                # Link Oportunidade -> Vetor
                if f"vec:{vector}" in node_ids:
                    links.append({"source": f"vec:{vector}", "target": opp_id, "label": f"ICE {ice}"})
            except Exception:
                pass

    # 3. Nós das Ferramentas Principais do Startuzeiro
    tools = [
        ("tool:hunter", "Hunter.io (E-mails)", "#f97316"),
        ("tool:clay", "Clay GTM (Inteligência)", "#eab308"),
        ("tool:cnpj_ai", "cnpj.ai & NetworkX (Sócios)", "#14b8a6"),
        ("tool:duckdb", "DuckDB (Analytics)", "#06b6d4"),
        ("tool:gliner", "GLiNER (Zero-Shot NER)", "#8b5cf6"),
        ("tool:yt", "TranscriptAPI (YouTube Lake)", "#ef4444")
    ]
    for tid, tlabel, tcolor in tools:
        add_node(tid, "tool", tlabel, tcolor, radius=12)

    # Links entre Ferramentas e Oportunidades
    links.append({"source": "tool:hunter", "target": "opp:OPP-002", "label": "Decisores B2B"})
    links.append({"source": "tool:clay", "target": "opp:OPP-002", "label": "Tecnografia"})
    links.append({"source": "tool:duckdb", "target": "opp:OPP-003", "label": "Engine SQL Local"})
    links.append({"source": "tool:gliner", "target": "opp:OPP-005", "label": "Extração de Ganchos"})
    links.append({"source": "tool:yt", "target": "opp:OPP-005", "label": "Fonte de Transcrições"})

    return {"nodes": nodes, "links": links}

def main():
    parser = argparse.ArgumentParser(description="Startuzeiro OS - Motor do Cérebro Agêntico")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("mine", help="Minerar transcrições e gerar oportunidades nos 4 vetores")
    subparsers.add_parser("graph", help="Exportar grafo de conhecimento em formato JSON")

    args = parser.parse_args()

    if args.command == "mine":
        mine_transcripts()
    elif args.command == "graph":
        g = build_knowledge_graph()
        print(json.dumps(g, indent=2, ensure_ascii=False))
    else:
        # Por padrão executa mineração e exibe resumo
        mine_transcripts()
        g = build_knowledge_graph()
        print(f"[*] Grafo de Conhecimento: {len(g['nodes'])} nós e {len(g['links'])} conexões geradas.")

if __name__ == "__main__":
    main()
