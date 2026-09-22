# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Utilitário para extrair transcrições e pesquisar vídeos no YouTube via TranscriptAPI.
"""

import os
import sys
import argparse
import httpx
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BASE_URL = "https://transcriptapi.com/api/v2/youtube"

def get_api_key():
    key = os.getenv("TRANSCRIPT_API_KEY")
    if not key:
        print("[ERRO] TRANSCRIPT_API_KEY não encontrada no arquivo .env nem nas variáveis de ambiente.")
        sys.exit(1)
    return key

def get_headers():
    return {
        "Authorization": f"Bearer {get_api_key()}",
        "Accept": "application/json"
    }

def get_video_info(video_url: str):
    with httpx.Client(base_url=BASE_URL, headers=get_headers(), timeout=30.0) as client:
        r = client.get("/info", params={"video_url": video_url})
        r.raise_for_status()
        return r.json()

def get_transcript(video_url: str, fmt: str = "text", include_timestamp: bool = True, language: str = None):
    params = {
        "video_url": video_url,
        "format": fmt,
        "include_timestamp": str(include_timestamp).lower(),
        "send_metadata": "true"
    }
    if language:
        params["language"] = language

    with httpx.Client(base_url=BASE_URL, headers=get_headers(), timeout=45.0) as client:
        r = client.get("/transcript", params=params)
        if r.status_code == 404:
            print(f"[ERRO 404] Transcrição não encontrada para o vídeo: {video_url}")
            return None
        r.raise_for_status()
        return r.json()

def search_youtube(query: str, search_type: str = "video", sort: str = "relevance"):
    params = {"q": query, "type": search_type, "sort": sort}
    with httpx.Client(base_url=BASE_URL, headers=get_headers(), timeout=30.0) as client:
        r = client.get("/search", params=params)
        r.raise_for_status()
        return r.json()

def main():
    parser = argparse.ArgumentParser(description="Cliente CLI TranscriptAPI para Startuzeiro")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video", "-v", help="URL do vídeo ou ID de 11 caracteres")
    group.add_argument("--search", "-s", help="Termo de busca no YouTube")
    group.add_argument("--info", "-i", help="Consultar metadados e idiomas disponíveis (Grátis)")

    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Formato de saída (default: text)")
    parser.add_argument("--no-timestamps", action="store_true", help="Omitir timestamps")
    parser.add_argument("--lang", help="Lista de idiomas em ordem de prioridade (ex: pt,en,asr)")
    parser.add_argument("--output", "-o", help="Salvar saída em arquivo")

    args = parser.parse_args()

    if args.info:
        data = get_video_info(args.info)
        print(f"Título: {data.get('metadata', {}).get('title')}")
        print("Idiomas disponíveis:")
        for lang in data.get("available_languages", []):
            print(f"  - {lang.get('code')}: {lang.get('name')}")
        return

    if args.video:
        data = get_transcript(args.video, fmt=args.format, include_timestamp=not args.no_timestamps, language=args.lang)
        if not data:
            return

        out_content = ""
        if args.format == "text":
            out_content = data.get("transcript", "")
        else:
            import json
            out_content = json.dumps(data, indent=2, ensure_ascii=False)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out_content)
            print(f"[OK] Transcrição salva em {args.output}")
        else:
            print(out_content)
        return

    if args.search:
        data = search_youtube(args.search)
        results = data.get("results", [])
        print(f"Encontrados {len(results)} resultados para '{args.search}':\n")
        for idx, item in enumerate(results[:10], 1):
            title = item.get("title", "Sem título")
            vid = item.get("videoId", "")
            views = item.get("viewCountText", "")
            channel = item.get("channelTitle", "")
            print(f"{idx}. [{vid}] {title} ({views}) - {channel}")
            print(f"   URL: https://www.youtube.com/watch?v={vid}")

if __name__ == "__main__":
    main()
