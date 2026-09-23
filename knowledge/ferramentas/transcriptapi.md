---
nome: YouTube Transcript Engine (youtube-transcript-api + oEmbed + yt-dlp)
categoria: transcricao-audio-video
tipo: open-source-python
url: "https://github.com/jdepoix/youtube-transcript-api"
custo: "100% Gratuito / Open Source (Sem API Keys)"
tags: [youtube, transcricao, video, lake, open-source, yt-dlp]
---

# YouTube Transcript Engine (Livre & Open-Source)

## O que é
O **YouTube Transcript Engine** é o pipeline nativo, gratuito e de alta velocidade do Startuzeiro para obter transcrições completas com timestamps e metadados de vídeos do YouTube. Utiliza internamente:
- **`youtube-transcript-api`**: Extrai faixas de legendas (manuais e geradas por IA - ASR) e suporta traduções em frações de segundo.
- **YouTube `oEmbed`**: API pública e gratuita da Google para extração imediata de título, autor e metadados sem autenticação.
- **`yt-dlp`**: Mecanismo de alta resiliência e fallback para extração detalhada de metadados e contorno de bloqueios.

---

## Casos de Uso no Startuzeiro
1. **Mineração de Dores e Tendências:** Extrair transcrições de dezenas de vídeos de nicho para alimentar o Lake em `yt_base/yt_lake/` e `brain/03_recursos/yt_lake/`.
2. **Engenharia Reversa de Conteúdo:** Obter a estrutura de palestras, podcasts e tutoriais para mapear oportunidades de automação AAA, Micro-SaaS e Afiliados.
3. **Alimentação do Cérebro Agêntico:** Ingestão contínua de transcrições mineradas pelo `scripts/agentic_brain.py mine`.

---

## Como Usar

### 1. Atalho Rápido no Agente
Basta enviar no chat:
```text
/ <link_do_youtube>
```
ou
```text
/yt <link_do_youtube>
```

### 2. Via Terminal (uv)
```bash
uv run scripts/utilitarios/yt_transcribe_and_catalog.py "<link_do_youtube>"
```

### 3. Vantagens sobre a API Antiga
- **R$ 0,00 de custo**: Sem créditos, sem quotas limitantes e sem mensalidades.
- **Zero chaves**: Nenhuma dependência de variáveis como `TRANSCRIPT_API_KEY`.
- **Privacidade e velocidade**: Processamento local em menos de 1 segundo por vídeo.

---

## Links Relacionados
- [[Firecrawl]]
- [[template-pesquisa]]
