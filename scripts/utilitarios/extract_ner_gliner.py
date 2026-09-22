#!/usr/bin/env python3
"""
extract_ner_gliner.py - Extração de Entidades Nomeadas (NER) Zero-Shot com GLiNER / GLiNER2
Startuzeiro Lab

Extrai entidades arbitrárias (startups, pessoas, valores, cargos, tecnologias) de transcrições
de vídeos e páginas web diretamente na CPU sem gastar tokens de APIs de LLMs.

Uso:
  uv run scripts/utilitarios/extract_ner_gliner.py "A Stripe recebeu aporte da Sequoia Capital e fechou parceria com a OpenAI."
  uv run scripts/utilitarios/extract_ner_gliner.py --file "pesquisas/artigo.md" --labels empresa fundador tecnologia
  uv run scripts/utilitarios/extract_ner_gliner.py "Texto..." --format yaml
"""

import sys
import json
import argparse
from pathlib import Path

DEFAULT_LABELS = ["empresa", "startup", "fundador", "investidor", "cargo", "tecnologia", "valor_financeiro"]

def extract_with_gliner(text: str, labels: list, model_name: str = "urchade/gliner_small-v2.1", threshold: float = 0.4):
    """Extrai entidades utilizando a biblioteca GLiNER original (Urchade)."""
    from gliner import GLiNER
    print(f"[GLiNER] Carregando modelo '{model_name}'...", file=sys.stderr)
    model = GLiNER.from_pretrained(model_name)
    entities = model.predict_entities(text, labels, threshold=threshold)
    return entities

def extract_with_gliner2(text: str, labels: list, model_name: str = "fastino/gliner-v2"):
    """Extrai entidades utilizando GLiNER2 (Fastino AI) com extração baseada em esquemas."""
    try:
        from gliner2 import AutoExtractor
        print(f"[GLiNER2] Carregando AutoExtractor '{model_name}'...", file=sys.stderr)
        extractor = AutoExtractor.from_pretrained(model_name)
        return extractor.extract_entities(text, labels)
    except Exception as e:
        print(f"[GLiNER2 Fallback] Erro ao carregar GLiNER2 ({e}). Tentando GLiNER...", file=sys.stderr)
        return None

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Extração Zero-Shot de Entidades via GLiNER / GLiNER2.")
    parser.add_argument("text", nargs="?", default=None, help="Texto para análise de entidades")
    parser.add_argument("-f", "--file", help="Caminho do arquivo de texto ou Markdown para analisar")
    parser.add_argument("-l", "--labels", nargs="+", default=DEFAULT_LABELS,
                        help=f"Lista de rótulos de entidades a extrair (padrão: {DEFAULT_LABELS})")
    parser.add_argument("-t", "--threshold", type=float, default=0.4,
                        help="Limiar de confiança (padrão: 0.4)")
    parser.add_argument("--model", default="urchade/gliner_small-v2.1",
                        help="Modelo do Hugging Face (padrão: urchade/gliner_small-v2.1)")
    parser.add_argument("--format", choices=["table", "json", "yaml"], default="table",
                        help="Formato de saída (padrão: table)")
    args = parser.parse_args()

    # Obter texto
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Erro: Arquivo não encontrado: {file_path}", file=sys.stderr)
            sys.exit(1)
        input_text = file_path.read_text(encoding="utf-8")
    elif args.text:
        input_text = args.text
    else:
        input_text = "O Nubank anunciou que David Vélez liderou a expansão para o México com novo aporte de R$ 500 milhões utilizando tecnologia em Clojure e Kubernetes."

    print(f"\nTexto de entrada ({len(input_text)} caracteres):")
    print(f'"{input_text[:180]}..."\n' if len(input_text) > 180 else f'"{input_text}"\n')
    print(f"Rótulos buscados: {args.labels}")

    try:
        entities = extract_with_gliner(input_text, args.labels, model_name=args.model, threshold=args.threshold)
    except Exception as e:
        print(f"[Erro GLiNER] Falha na inferência: {e}", file=sys.stderr)
        sys.exit(1)

    # Formatar resultados
    if args.format == "json":
        clean_entities = [{"text": e["text"], "label": e["label"], "score": round(float(e["score"]), 3)} for e in entities]
        print(json.dumps(clean_entities, indent=2, ensure_ascii=False))
    elif args.format == "yaml":
        print("entidades_extraidas:")
        for e in entities:
            print(f'  - termo: "{e["text"]}"')
            print(f'    tipo: "{e["label"]}"')
            print(f'    score: {round(float(e["score"]), 3)}')
    else:
        print("\n🎯 Entidades Detectadas:")
        print(f"{'Entidade / Termo':<30} | {'Rótulo / Tipo':<18} | {'Confiança'}")
        print("-" * 65)
        for e in entities:
            score_str = f"{float(e['score']):.1%}"
            print(f"{e['text']:<30} | {e['label']:<18} | {score_str}")

if __name__ == "__main__":
    main()
