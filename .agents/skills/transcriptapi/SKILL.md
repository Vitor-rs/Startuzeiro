---
name: transcriptapi
description: >-
  Extract YouTube transcripts (with or without timestamps, plain text or JSON), pull video metadata, and catalog videos into the YouTube Lake using the 100% free and open-source YouTube Transcript Engine (youtube-transcript-api + oEmbed + yt-dlp). Use when the user needs YouTube video transcripts, video content analysis, or market research from YouTube.
---

# YouTube Transcript Skill & Slash Command (`/ <link>` ou `/yt <link>`)

The **YouTube Transcript** skill enables the agent to extract full video transcripts with timestamps, format logical paragraphs, gather rich video metadata (Title, Channel, Publish Date, Views), and catalog everything into the lake without any API keys, credits, or subscriptions.

---

## ⚡ Slash Command Action (`/ <url>` or `/yt <url>`)

Whenever this skill is triggered via `/ <link>` (or when the user provides a YouTube URL to transcribe):

### Mandatory Execution:
Run the cataloging utility immediately:
```bash
uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<url>"
```

### What this action does:
1. **Metadata & Transcript:** Fetches the full transcript with timestamps via `youtube-transcript-api` and video metadata (Title, Channel, Publish Date, Views, Summary) via Google oEmbed and `yt-dlp`. **Zero API keys required.**
2. **Normalized Lake File:** Normalizes the video title (removing accents: `ç` -> `c`, `ã` -> `a`, lowercase, spaces to `_`) and saves the full markdown transcript in `yt_base/yt_lake/<normalized_title>.md` and syncs with `brain/03_recursos/yt_lake/<normalized_title>.md`.
3. **Master Catalog Index:** Updates the catalog table in `yt_base/README.md` with:
   - Clickable link to the transcript in `yt_lake/`
   - Channel Name
   - Publish Date
   - Concise topic summary
   - Original YouTube video link
4. **Agent Response:** Returns direct clickable links to the generated file in `yt_lake/` and to `yt_base/README.md`.

---

## 🔑 Authentication & Configuration

- **Cost:** **100% Free & Open-Source (Zero API keys, zero credits)**
- **Libraries:** `youtube-transcript-api`, `httpx`, `yt-dlp`
- **Execution:** Runs locally in Python 3.12+ via `uv`
- **No external paid API dependencies.**

---

## 🛠️ CLI Usage

```bash
# Transcribe and catalog into the Lake
uv run scripts/utilitarios/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Inspect available subtitle languages or test video transcript directly
uv run scripts/utilitarios/yt_transcript.py --video "VIDEO_ID"
uv run scripts/utilitarios/yt_transcript.py --info "VIDEO_ID"
```
