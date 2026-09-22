# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Automação de Transcrição e Catalogação do YouTube para Startuzeiro.
Salva transcrições em yt_base/yt_lake/<nome_normalizado>.md
E cataloga os metadados em yt_base/README.md

Uso:
    uv run scripts/utilitarios/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
"""

import os
import sys
import re
import unicodedata
import argparse
from datetime import datetime
from pathlib import Path
import httpx
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

BASE_URL = "https://transcriptapi.com/api/v2/youtube"

def get_api_key():
    key = os.getenv("TRANSCRIPT_API_KEY")
    if not key:
        print("[ERRO] TRANSCRIPT_API_KEY não configurada no arquivo .env!")
        sys.exit(1)
    return key

def extract_video_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    
    # Padrões comuns de URL
    patterns = [
        r"(?:v=|\/v\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"(?:watch\?v=)([a-zA-Z0-9_-]{11})"
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
            
    # Fallback básico
    clean = re.sub(r"[?&].*$", "", url_or_id)
    parts = clean.split("/")
    if parts and len(parts[-1]) == 11:
        return parts[-1]
        
    return url_or_id

def normalize_filename(title: str) -> str:
    """Normaliza o título: sem acentos, 'ç' -> 'c', espaços viram '_'"""
    # Decomposição unicode e remoção de marcas de acento
    nfkd = unicodedata.normalize("NFKD", title)
    ascii_str = nfkd.encode("ASCII", "ignore").decode("ASCII")
    
    # Minúsculo
    clean = ascii_str.lower()
    # Substituir qualquer caractere não alfanumérico por underscore
    clean = re.sub(r"[^a-z0-9]+", "_", clean)
    clean = clean.strip("_")
    
    return clean[:120] if clean else "video_sem_titulo"

def fetch_metadata(client: httpx.Client, video_id: str) -> dict:
    try:
        r = client.get("/video/metadata", params={"video_url": video_id})
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"[AVISO] Não foi possível obter metadados completos: {e}")
    return {}

def fetch_transcript(client: httpx.Client, video_id: str) -> dict:
    # 1. Tentar com prioridade de idioma pt, en, asr
    for lang in ["pt,en,asr", "en,asr", None]:
        params = {
            "video_url": video_id,
            "format": "text",
            "include_timestamp": "true",
            "send_metadata": "true"
        }
        if lang:
            params["language"] = lang

        r = client.get("/transcript", params=params)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            continue
        elif r.status_code == 401:
            print("[ERRO 401] Chave de API inválida.")
            sys.exit(1)
        elif r.status_code == 402:
            print("[ERRO 402] Créditos insuficientes no TranscriptAPI.")
            sys.exit(1)
        r.raise_for_status()

    return {}

def generate_summary(title: str, description: str, transcript_text: str) -> str:
    """Gera um resumo conciso do assunto a partir da descrição e início da transcrição."""
    if description and len(description.strip()) > 30:
        clean_desc = description.strip().split("\n")[0]
        if len(clean_desc) > 160:
            clean_desc = clean_desc[:157] + "..."
        return clean_desc
    
    # Se não tiver descrição, pegar os primeiros 150 caracteres da transcrição limpa
    clean_lines = [l for l in transcript_text.split("\n") if l.strip() and not l.startswith("[")]
    sample = " ".join(clean_lines[:3]).strip()
    if len(sample) > 150:
        sample = sample[:147] + "..."
    return sample if sample else f"Vídeo abordando o tema '{title}'."

def update_catalog(yt_base_dir: Path, video_data: dict):
    catalog_md = yt_base_dir / "README.md"
    
    # Se o arquivo não existir, criar estrutura inicial
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

    # Ler conteúdo atual
    with open(catalog_md, "r", encoding="utf-8") as f:
        lines = f.readlines()

    vid_id = video_data["video_id"]
    file_rel = f"yt_lake/{video_data['filename']}"
    
    # Linha da tabela
    table_row = f"| **[[{file_rel}\\|{video_data['title']}]]** | {video_data['channel']} | {video_data['publish_date']} | {video_data['summary']} | [Assistir ↗]({video_data['url']}) |\n"

    # Verificar se o vídeo já está catalogado
    exists = False
    new_lines = []
    for line in lines:
        if vid_id in line or video_data['url'] in line:
            new_lines.append(table_row) # Atualiza a linha existente
            exists = True
        else:
            new_lines.append(line)

    if not exists:
        new_lines.append(table_row)

    with open(catalog_md, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"📖 Catálogo atualizado em: {catalog_md}")

def main():
    parser = argparse.ArgumentParser(description="Transcrever e catalogar vídeo do YouTube")
    parser.add_argument("url", help="Link do YouTube ou ID do vídeo")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    full_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n🔍 Processando vídeo ID: {video_id} ({full_url})")

    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Accept": "application/json"
    }

    yt_base = REPO_ROOT / "yt_base"
    yt_lake = yt_base / "yt_lake"
    yt_lake.mkdir(parents=True, exist_ok=True)

    with httpx.Client(base_url=BASE_URL, headers=headers, timeout=60.0) as client:
        # 1. Metadados
        print("📥 Obtendo informações do vídeo...")
        meta = fetch_metadata(client, video_id)
        
        # 2. Transcrição
        print("🎙️ Extraindo transcrição...")
        t_data = fetch_transcript(client, video_id)

    if not t_data or not t_data.get("transcript"):
        print(f"[ERRO] Não foi possível obter a transcrição do vídeo {video_id}.")
        print("Verifique se o vídeo possui legendas disponíveis ou se o link está correto.")
        sys.exit(1)

    transcript_text = t_data.get("transcript", "")
    
    # Extração de campos de metadados
    title = meta.get("title") or t_data.get("metadata", {}).get("title") or f"YouTube Video {video_id}"
    channel_info = meta.get("channel") or {}
    channel_name = channel_info.get("name") or t_data.get("metadata", {}).get("author_name") or "Canal Desconhecido"
    publish_date = meta.get("publishDate") or meta.get("relativeDate") or "Não informado"
    views = meta.get("viewCountText") or "Não informado"
    desc = meta.get("description") or ""

    # Normalizar nome do arquivo: minúsculo, sem acentos, ç -> c, espaços -> _
    norm_name = normalize_filename(title)
    filename = f"{norm_name}.md"
    file_path = yt_lake / filename

    summary = generate_summary(title, desc, transcript_text)

    # Escrever arquivo de transcrição no yt_lake
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_content = f"""---
video_id: "{video_id}"
titulo_original: "{title}"
canal: "{channel_name}"
data_publicacao: "{publish_date}"
visualizacoes: "{views}"
url_original: "{full_url}"
data_transcricao: "{now_str}"
tags: [youtube, transcricao, yt_lake]
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
{transcript_text}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Transcrição salva com sucesso em:\n   -> {file_path}")

    # Atualizar o catálogo em yt_base/README.md
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
    print("🎉 Vídeo transcrito e catalogado perfeitamente!\n")

if __name__ == "__main__":
    main()
