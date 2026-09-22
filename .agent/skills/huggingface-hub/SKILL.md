---
name: huggingface-hub
description: Descoberta, inspeção e navegação em modelos de IA, datasets, Spaces, papers acadêmicos e trending no Hugging Face Hub via Hugging Face MCP. Ativa quando o usuário busca modelos abertos, pesos de IA, papers recentes do arXiv, datasets para fine-tuning, ou ferramentas no Hub.
---

# Hugging Face Hub MCP

O **Hugging Face Hub MCP** conecta o assistente diretamente ao maior repositório global de inteligência artificial aberta (modelos, datasets, papers e Spaces).

## Quando Usar Esta Skill

Ative esta skill sempre que o usuário:
- **Buscar modelos de IA**: LLMs abertos, modelos de visão (VLM), áudio/TTS/Whisper, embeddings, OCR ou classificação.
- **Investigar papers de pesquisa**: Descoberta dos artigos científicos mais populares do dia ou busca de papers por tema no arXiv via Hub.
- **Encontrar datasets**: Datasets em português, benchmarks de avaliação, dados para fine-tuning ou corpora de texto/áudio.
- **Explorar Spaces e Demonstrações**: Encontrar aplicações interativas construídas pela comunidade em Gradio/Streamlit.
- **Inspecionar Model Cards**: Ler o `README.md` oficial de um modelo ou dataset para checar licenças de uso, parâmetros e benchmarks.

---

## Ferramentas Disponíveis no MCP

O servidor oficial opera em `https://huggingface.co/mcp` e expõe:

### 1. `hub_repo_search`
Busca unificada no catálogo do Hub com filtros de tipo e tags.
- **Argumentos**:
  - `query`: Termo de pesquisa (ex: `"faster-whisper"`, `"portuguese llm"`, `"document parsing"`).
  - `type`: `"model"`, `"dataset"` ou `"space"`.
  - `limit`: Quantidade de resultados retornados.

### 2. `hub_repo_details`
Recupera metadados completos de um modelo, dataset ou space específico.
- **Argumentos**:
  - `repo_id`: Identificador do repositório no formato `owner/name` (ex: `"meta-llama/Llama-3.3-70B-Instruct"`, `"SWivid/F5-TTS"`).

### 3. `hf_fs` (Hub Virtual Filesystem)
Sistema de arquivos virtual com comandos estilo UNIX para explorar o ecossistema:
- **Trending Models**: `ls hf://models/trending`
- **Trending Datasets**: `ls hf://datasets/trending`
- **Trending Spaces**: `ls hf://spaces/trending`
- **Daily Papers & Artigos**: `ls hf://papers/daily/latest` ou `ls hf://papers/trending`
- **Leitura de README**: `cat hf://models/<owner>/<name>/README.md`
- **Busca**: `search hf://models <query>`

### 4. `hf_whoami`
Inspeciona a conta atual autenticada e limites de quota da API.

---

## Boas Práticas Operacionais

1. **Priorize Modelos Abertos**: Ao recomendar soluções para o Startuzeiro, verifique se a licença é comercial (Apache 2.0, MIT, Llama 3 Community) antes de sugerir para produção.
2. **Checagem de Formatos**: Para execução local em Windows 11 com baixo consumo, priorize quantizações GGUF (para llama.cpp / Ollama) ou modelos otimizados via ONNX / CTranslate2.
3. **Exploração de Papers**: Utilize `ls hf://papers/daily/latest` para monitorar tendências em pesquisas de IA que possam gerar novas teses ou ferramentas para o laboratório do Startuzeiro.
