# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "youtube-transcript-api",
#     "httpx",
#     "yt-dlp",
# ]
# ///
"""
Automação de Transcrição e Catalogação do YouTube para Startuzeiro.
Motor 100% Gratuito & Open-Source (youtube-transcript-api + oEmbed + yt-dlp).

Salva transcrições em:
- yt_base/yt_lake/<nome_normalizado>.md
- brain/03_recursos/yt_lake/<nome_normalizado>.md (P.A.R.A. Second Brain)
E cataloga os metadados em:
- yt_base/README.md

Uso:
    uv run scripts/utilitarios/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=CzDTaLqozlQ"
"""

import sys
import os
import re
import unicodedata
import argparse
from datetime import datetime
from pathlib import Path
import httpx
from youtube_transcript_api import YouTubeTranscriptApi

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

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

def normalize_filename(title: str) -> str:
    """Normaliza o título: sem acentos, 'ç' -> 'c', espaços viram '_'"""
    nfkd = unicodedata.normalize("NFKD", title)
    ascii_str = nfkd.encode("ASCII", "ignore").decode("ASCII")
    clean = ascii_str.lower()
    clean = re.sub(r"[^a-z0-9]+", "_", clean)
    clean = clean.strip("_")
    return clean[:120] if clean else "video_sem_titulo"

def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    hours = s // 3600
    minutes = (s % 3600) // 60
    secs = s % 60
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes:02d}:{secs:02d}]"

def fetch_oembed(video_id: str) -> dict:
    """Busca metadados essenciais via API pública oEmbed da Google (instantâneo, 0 chaves)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        r = httpx.get("https://www.youtube.com/oembed", params={"url": url, "format": "json"}, timeout=12.0)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[AVISO] Falha ao consultar oEmbed: {e}")
    return {}

def fetch_ytdlp_metadata(video_id: str) -> dict:
    """Enriquece metadados detalhados (views, data exata, descrição) via yt-dlp sem baixar o vídeo."""
    try:
        import yt_dlp
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_id, download=False)
            if info:
                upload_raw = info.get("upload_date") or ""
                if len(upload_raw) == 8:
                    upload_date = f"{upload_raw[:4]}-{upload_raw[4:6]}-{upload_raw[6:]}"
                else:
                    upload_date = upload_raw or "Desconhecido"

                views = info.get("view_count")
                views_str = f"{views:,}".replace(",", ".") if views else "Não informado"

                return {
                    "title": info.get("title"),
                    "channel": info.get("uploader") or info.get("channel"),
                    "publish_date": upload_date,
                    "views": views_str,
                    "description": info.get("description") or "",
                    "duration": info.get("duration") or 0
                }
    except Exception as e:
        print(f"[AVISO] Não foi possível obter metadados enriquecidos via yt-dlp: {e}")
    return {}

def fetch_transcript_ytta(video_id: str) -> list:
    """Extrai legendas via youtube-transcript-api com fallback inteligente de idiomas."""
    ytt = YouTubeTranscriptApi()

    # 1. Tentar faixas preferenciais (Português, Português Brasileiro, Inglês)
    for target_langs in [["pt", "pt-BR"], ["en"], None]:
        try:
            if target_langs:
                t = ytt.fetch(video_id, languages=target_langs)
            else:
                # Tenta qualquer legenda disponível na lista
                t_list = ytt.list(video_id)
                for item in t_list:
                    t = item.fetch()
                    break
            if t and t.snippets:
                return [
                    {"start": s.start, "duration": s.duration, "text": s.text}
                    for s in t.snippets
                ]
        except Exception:
            continue
    return []

def format_smart_transcript(snippets: list) -> str:
    """Agrupa snippets em parágrafos lógicos com timestamps a cada ~30-45 segundos."""
    if not snippets:
        return ""

    paragraphs = []
    current_ts = snippets[0]["start"]
    current_texts = []
    block_start = current_ts

    for s in snippets:
        txt = s["text"].strip()
        if not txt:
            continue

        current_texts.append(txt)
        # Se passaram mais de 35 segundos ou se terminar em pontuação forte após 25 segundos
        elapsed = s["start"] - block_start
        if elapsed >= 35 or (elapsed >= 20 and txt.endswith((".", "!", "?"))):
            ts_str = format_timestamp(block_start)
            para = f"{ts_str} " + " ".join(current_texts)
            paragraphs.append(para)
            current_texts = []
            block_start = s["start"] + s.get("duration", 2)

    if current_texts:
        ts_str = format_timestamp(block_start)
        paragraphs.append(f"{ts_str} " + " ".join(current_texts))

    return "\n\n".join(paragraphs)

def generate_summary(title: str, description: str, transcript_text: str) -> str:
    """Gera resumo conciso a partir da descrição ou início da transcrição."""
    if description and len(description.strip()) > 30:
        clean_desc = description.strip().split("\n")[0]
        if len(clean_desc) > 160:
            clean_desc = clean_desc[:157] + "..."
        return clean_desc

    clean_lines = [l for l in transcript_text.split("\n") if l.strip() and not l.startswith("[")]
    sample = " ".join(clean_lines[:3]).strip()
    if len(sample) > 150:
        sample = sample[:147] + "..."
    return sample if sample else f"Vídeo abordando o tema '{title}'."

def update_catalog(yt_base_dir: Path, video_data: dict):
    catalog_md = yt_base_dir / "README.md"

    if not catalog_md.exists():
        initial_content = """# 📺 YouTube Base (yt_base)

Catálogo central de vídeos transcritos e analisados para pesquisa de mercado, inteligência de concorrentes e extração de insights no **Startuzeiro**.

Todas as transcrições completas ficam armazenadas no lake: [`yt_lake/`](./yt_lake/).

---

## 📑 Catálogo de Vídeos Transcritos

| Vídeo / Transcrição | Canal | Publicado em | Assunto Resumido | Link Original |
| :--- | :--- | :--- | :--- | :--- |
"""
        with open(catalog_md, "w", encoding="utf-8") as f:
            f.write(initial_content)

    with open(catalog_md, "r", encoding="utf-8") as f:
        lines = f.readlines()

    vid_id = video_data["video_id"]
    file_rel = f"yt_lake/{video_data['filename']}"

    table_row = f"| **[[{file_rel}\\|{video_data['title']}]]** | {video_data['channel']} | {video_data['publish_date']} | {video_data['summary']} | [Assistir ↗]({video_data['url']}) |\n"

    exists = False
    new_lines = []
    for line in lines:
        if vid_id in line or video_data['url'] in line:
            new_lines.append(table_row)
            exists = True
        else:
            new_lines.append(line)

    if not exists:
        new_lines.append(table_row)

    with open(catalog_md, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"📖 Catálogo atualizado em: {catalog_md}")

def main():
    parser = argparse.ArgumentParser(description="Transcrever e catalogar vídeo do YouTube (Motor Gratuito & Open-Source)")
    parser.add_argument("url", help="Link do YouTube ou ID do vídeo")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    full_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n🔍 Processando vídeo ID: {video_id} ({full_url})")

    # 1. Obter metadados
    print("📥 Coletando metadados (oEmbed & yt-dlp)...")
    oembed_meta = fetch_oembed(video_id)
    ytdlp_meta = fetch_ytdlp_metadata(video_id)

    title = ytdlp_meta.get("title") or oembed_meta.get("title") or f"YouTube Video {video_id}"
    channel_name = ytdlp_meta.get("channel") or oembed_meta.get("author_name") or "Canal Desconhecido"
    publish_date = ytdlp_meta.get("publish_date") or "Não informado"
    views = ytdlp_meta.get("views") or "Não informado"
    desc = ytdlp_meta.get("description") or ""

    # 2. Obter transcrição
    print("🎙️ Extraindo transcrição com timestamps...")
    snippets = fetch_transcript_ytta(video_id)

    if not snippets:
        print(f"[ERRO] Não foi possível obter legendas para o vídeo {video_id}.")
        print("Verifique se o vídeo possui legendas disponíveis ou se o link está correto.")
        sys.exit(1)

    formatted_transcript = format_smart_transcript(snippets)

    # 3. Preparar arquivo e diretórios
    norm_name = normalize_filename(title)
    filename = f"{norm_name}.md"

    yt_base = REPO_ROOT / "yt_base"
    yt_lake = yt_base / "yt_lake"
    yt_lake.mkdir(parents=True, exist_ok=True)

    # Lake no Segundo Cérebro (P.A.R.A.)
    brain_lake = REPO_ROOT / "brain" / "03_recursos" / "yt_lake"
    brain_lake.mkdir(parents=True, exist_ok=True)

    summary = generate_summary(title, desc, formatted_transcript)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_content = f"""---
video_id: "{video_id}"
titulo_original: "{title}"
canal: "{channel_name}"
data_publicacao: "{publish_date}"
visualizacoes: "{views}"
url_original: "{full_url}"
data_transcricao: "{now_str}"
motor_transcricao: "youtube-transcript-api (Open-Source / Free)"
tags: [youtube, transcricao, yt_lake, second_brain]
---

# {title}

- **📺 Canal:** {channel_name}
- **📅 Publicado em:** {publish_date}
- **👁️ Visualizações:** {views}
- **🔗 Link Original:** [{full_url}]({full_url})

---

## 📌 Assunto Resumido
{summary}

---

## 🎙️ Transcrição Completa
{formatted_transcript}
"""

    # Gravar em yt_base/yt_lake
    file_path = yt_lake / filename
    file_path.write_text(md_content, encoding="utf-8")

    # Sincronizar em brain/03_recursos/yt_lake
    brain_file_path = brain_lake / filename
    brain_file_path.write_text(md_content, encoding="utf-8")

    print(f"✅ Transcrição salva com sucesso em:")
    print(f"   -> {file_path}")
    print(f"   -> {brain_file_path}")

    # Atualizar o catálogo central
    video_summary_info = {
        "video_id": video_id,
        "filename": filename,
        "title": title,
        "channel": channel_name,
        "publish_date": publish_date,
        "summary": summary,
        "url": full_url
    }
    update_catalog(yt_base, video_summary_info)
    print("🎉 Vídeo transcrito e catalogado perfeitamente no Lake e no Segundo Cérebro!\n")

if __name__ == "__main__":
    main()
