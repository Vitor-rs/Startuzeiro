---
name: transcriptapi
description: >-
  Extract YouTube transcripts (with or without timestamps, plain text or JSON), search YouTube videos, channels and playlists, pull video metadata and inspect channel uploads, shorts, posts and sections using TranscriptAPI. Use when the user needs YouTube video transcripts, YouTube search, channel research, VSL extraction, or video content analysis.
---

# TranscriptAPI Skill & Slash Command (`/transcriptapi`)

The **TranscriptAPI** skill enables the agent to search YouTube, extract video transcripts (with or without timestamps), inspect channel profiles, playlists, community posts, and gather video metadata for competitive intelligence, market research, and content reverse engineering.

---

## ⚡ Slash Command Action (`/transcriptapi <url>`)

Whenever this skill is triggered via `/transcriptapi <link>` (or when the user provides a YouTube URL to transcribe):

### Mandatory Execution:
Run the cataloging utility immediately:
```bash
uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<url>"
```

### What this action does:
1. **Metadata & Transcript:** Fetches the full transcript with timestamps and video metadata (Title, Channel, Publish Date, Views, Summary) using the configured `TRANSCRIPT_API_KEY`.
2. **Normalized Lake File:** Normalizes the video title (removing accents: `ç` -> `c`, `ã` -> `a`, lowercase, spaces to `_`) and saves the full markdown transcript in `yt_base/yt_lake/<normalized_title>.md`.
3. **Master Catalog Index:** Updates the catalog table in `yt_base/README.md` with:
   - Clickable link to the transcript in `yt_lake/`
   - Channel Name
   - Publish Date
   - Concise topic summary
   - Original YouTube video link
4. **Agent Response:** Returns direct clickable links to the generated file in `yt_lake/` and to `yt_base/README.md`.

---

## 🔑 Authentication & Configuration

- **Base URL:** `https://transcriptapi.com` (all endpoints under `/api/v2/youtube`)
- **API Key:** Stored in `.env` as `TRANSCRIPT_API_KEY`
- **Auth Header:** `Authorization: Bearer YOUR_API_KEY`
- **MCP Server:** Configured as `transcript-api` in `~/.gemini/config/mcp_config.json`

---

## 💰 Credit Cost & Rate Limits

- **Free Endpoints (0 credits):**
  - `GET /api/v2/youtube/info?video_url=<ID>` (Metadata + available language list)
  - `GET /api/v2/youtube/channel/resolve?input=<@handle|URL|ID>` (Resolve to UC... ID)
  - `GET /api/v2/youtube/channel/latest?channel=<handle|ID>` (Latest 15 videos via RSS)
- **Billable Endpoints (1 credit per request/page):**
  - `GET /api/v2/youtube/transcript`
  - `GET /api/v2/youtube/search`
  - `GET /api/v2/youtube/video/metadata`
  - `GET /api/v2/youtube/channel/info`, `/videos`, `/playlists`, `/posts`, `/sections`
  - `GET /api/v2/youtube/playlist/videos`
- **Rate Limit:** 200 requests per minute per key.
- **Retry Rules:** Only retry HTTP `408`, `429` (respect `Retry-After`), and `503`. Do **not** retry `400`, `401`, `402`, `404`, or `422`.

---

## 🛠️ Execution Methods

### Method 1: Automated Lake Ingestion (Recommended)
```bash
uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<url>"
```

### Method 2: Raw CLI Utility
```bash
# Check available languages for free:
uv run scripts/utilitarios/yt_transcript.py --info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Search YouTube videos on a topic:
uv run scripts/utilitarios/yt_transcript.py --search "automacao whatsapp n8n"
```

### Method 3: Via MCP (`transcript-api`)
Call tools directly via MCP client where applicable.

---

## 📚 References & Specifications

- Full OpenAPI 3.1.0 specification: [openapi.json](./references/openapi.json)
- Script Ingestion: [yt_transcribe_and_catalog.py](../../../scripts/utilitarios/yt_transcribe_and_catalog.py)
