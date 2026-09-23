# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "youtube-transcript-api",
#     "httpx",
# ]
# ///
"""
Utilitário de linha de comando para extrair transcrições e inspecionar vídeos do YouTube
de forma 100% gratuita, sem chaves de API nem limites de créditos.

Executar com uv:
    uv run scripts/utilitarios/yt_transcript.py --video "https://www.youtube.com/watch?v=CzDTaLqozlQ"
    uv run scripts/utilitarios/yt_transcript.py --info "CzDTaLqozlQ"
"""

import sys
import re
import json
import argparse
from pathlib import Path
import httpx
from youtube_transcript_api import YouTubeTranscriptApi

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def extract_video_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    patterns = [
        r"(?:v=|\/v\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"(?:watch\?v=)([a-zA-Z0-9_-]{11})"
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    clean = re.sub(r"[?&].*$", "", url_or_id)
    parts = clean.split("/")
    if parts and len(parts[-1]) == 11:
        return parts[-1]
    return url_or_id

def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    hours = s // 3600
    minutes = (s % 3600) // 60
    secs = s % 60
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes:02d}:{secs:02d}]"

def fetch_oembed(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        r = httpx.get("https://www.youtube.com/oembed", params={"url": url, "format": "json"}, timeout=10.0)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}

def get_video_info(video_id: str):
    meta = fetch_oembed(video_id)
    title = meta.get("title", "Desconhecido")
    author = meta.get("author_name", "Desconhecido")
    print(f"\n📺 Título: {title}")
    print(f"👤 Canal: {author}")
    print(f"🔗 URL: https://www.youtube.com/watch?v={video_id}\n")

    try:
        ytt = YouTubeTranscriptApi()
        transcript_list = ytt.list(video_id)
        print("🌐 Faixas de Legendas Disponíveis:")
        for t in transcript_list:
            gen_label = "Automática (ASR)" if t.is_generated else "Manual"
            trans_label = "Sim" if t.is_translatable else "Não"
            print(f"  - [{t.language_code}] {t.language} ({gen_label}) | Traduzível: {trans_label}")
    except Exception as e:
        print(f"⚠️ Não foi possível listar legendas para {video_id}: {e}")

def get_transcript(video_id: str, fmt: str = "text", include_timestamps: bool = True, languages=None, translate_to: str = None):
    if languages is None:
        languages = ["pt", "pt-BR", "en"]

    ytt = YouTubeTranscriptApi()
    
    transcript = None
    if translate_to:
        transcript_list = ytt.list(video_id)
        # Tenta achar transcrição para traduzir
        for t in transcript_list:
            if t.is_translatable:
                transcript = t.translate(translate_to).fetch()
                break
    
    if transcript is None:
        try:
            transcript = ytt.fetch(video_id, languages=languages)
        except Exception:
            # Fallback para qualquer legenda disponível
            transcript_list = ytt.list(video_id)
            for t in transcript_list:
                transcript = t.fetch()
                break

    if not transcript:
        print(f"❌ Nenhuma legenda encontrada para o vídeo {video_id}.")
        return None

    if fmt == "json":
        data = transcript.to_raw_data()
        return json.dumps(data, ensure_ascii=False, indent=2)

    lines = []
    for s in transcript.snippets:
        if include_timestamps:
            ts = format_timestamp(s.start)
            lines.append(f"{ts} {s.text}")
        else:
            lines.append(s.text)
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Cliente CLI Livre do YouTube para Startuzeiro (100% Gratuito)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video", "-v", help="URL do vídeo ou ID de 11 caracteres")
    group.add_argument("--info", "-i", help="Consultar metadados e idiomas disponíveis")

    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Formato de saída (default: text)")
    parser.add_argument("--no-timestamps", action="store_true", help="Omitir timestamps")
    parser.add_argument("--lang", help="Lista de idiomas separados por vírgula (ex: pt,pt-BR,en)")
    parser.add_argument("--translate", help="Traduzir automaticamente para código de idioma (ex: pt)")
    parser.add_argument("--output", "-o", help="Salvar saída em arquivo")

    args = parser.parse_args()

    if args.info:
        vid_id = extract_video_id(args.info)
        get_video_info(vid_id)
        return

    if args.video:
        vid_id = extract_video_id(args.video)
        langs = [l.strip() for l in args.lang.split(",")] if args.lang else ["pt", "pt-BR", "en"]
        res = get_transcript(
            vid_id,
            fmt=args.format,
            include_timestamps=not args.no_timestamps,
            languages=langs,
            translate_to=args.translate
        )
        if res:
            if args.output:
                Path(args.output).write_text(res, encoding="utf-8")
                print(f"✅ Transcrição salva em: {args.output}")
            else:
                print(res[:1500])
                if len(res) > 1500:
                    print(f"\n... [{len(res)} caracteres no total]")

if __name__ == "__main__":
    main()
