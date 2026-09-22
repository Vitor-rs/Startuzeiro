#!/usr/bin/env python3
"""
extract_metadata_instructor.py - Extração estruturada de metadados com Instructor & Pydantic
Startuzeiro Lab

Demonstra como forçar LLMs a responderem esquemas estritos (resumos, entidades, tags e scores)
para catalogação de documentos e vídeos no formato do Startuzeiro.

Uso:
  uv run scripts/utilitarios/extract_metadata_instructor.py "Texto ou transcricao de exemplo..."
"""

import sys
import argparse
from typing import List, Optional
from pydantic import BaseModel, Field

class ResumoAnaliticoStartuzeiro(BaseModel):
    titulo_sugerido: str = Field(description="Título conciso e direto do assunto tratado")
    resumo_executivo: str = Field(description="Resumo em 2 ou 3 frases dos pontos-chave")
    startups_citadas: List[str] = Field(default_factory=list, description="Startups ou empresas citadas no texto")
    tecnologias_mencionadas: List[str] = Field(default_factory=list, description="Linguagens, frameworks ou ferramentas")
    tags: List[str] = Field(default_factory=list, description="3 a 5 tags temáticas normalizadas")
    score_relevancia: int = Field(ge=0, le=100, description="Nota de 0 a 100 de utilidade para o Startuzeiro")

def main():
    parser = argparse.ArgumentParser(description="Demonstração do Instructor para extração estruturada de dados.")
    parser.add_argument("texto", nargs="?", default="A Stripe anunciou uma nova integração com IA usando LangChain e modelos Llama 3 para automatizar antifraude.",
                        help="Texto a ser analisado")
    args = parser.parse_args()

    try:
        import instructor
        import pydantic
        print(f"[OK] Instructor ({instructor.__version__}) e Pydantic ({pydantic.__version__}) prontos!")
    except ImportError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nEsquema de extração carregado:")
    print(ResumoAnaliticoStartuzeiro.model_json_schema())
    print("\nTexto de entrada:")
    print(f'"{args.texto}"')
    print("\n[Dica] Para conectar a uma API real de LLM:")
    print("  client = instructor.from_openai(OpenAI()) ou instructor.from_gemini(client)")
    print("  resposta = client.chat.completions.create(model='...', response_model=ResumoAnaliticoStartuzeiro, messages=[...])")

if __name__ == "__main__":
    main()
