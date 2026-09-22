# 🧠 Modelos Mentais & Blueprints Visuais do Startuzeiro OS

Este diretório armazena e cataloga os modelos mentais e esquemas visuais capturados em `resources/web_imgs`, que servem de fundação teórica e arquitetural para o **Startuzeiro OS**.

---

## 📑 Índice dos 6 Blueprints

| Imagem | Nome do Modelo | Autor / Referência | Aplicação Prática no Startuzeiro OS |
| :--- | :--- | :--- | :--- |
| **`19174f7cfadb6423763e2d174c189d59.jpg`** | **The Agent Development Kit** | Brij Kishore Pandey | Estrutura de 5 camadas: Memória Constitucional (`AGENTS.md`) → Skills modulares (`.agents/skills/`) → Hooks de Guardrail → Subagentes (`.agents/subagents/`) → Plugins. |
| **`7bbe669fb9b290a21b676028574ccb8b.jpg`** | **How to Build an AI Agent** | GenAI.works | Ciclo de vida de 8 passos: Escopo → System Prompt → LLM → Ferramentas/MCPs → Memória Estruturada → Orquestração Agente-Agente → UI → Evals. |
| **`9124f505318b88dae1b9456b0460948c.jpg`** | **Building a Second Brain (C.O.D.E. + P.A.R.A.)** | Tiago Forte | Gestão de conhecimento do Lake: **Capture** (transcrições/raspagem), **Organize** (Projects, Areas, Resources, Archive), **Distill** (resumos YAML/GLiNER), **Express** (Blueprints e Dossiês). |
| **`ca6b6c0aa7ef41e185d9aaa18bf6afcc.jpg`** | **The 4-Folder AI Project Structure** | Brij Kishore Pandey | Organização do monorepo: `prompts/` (versionados como código), `data/` (raw e processed), `agents/` (skills e tools), `evals/` (scorecards e traces). "Zero Confusion". |
| **`d1978b806d59c4a3a4af8c9e289a0beb.jpg`** | **Evolution of AI Agents** | AI Research | Escala de maturidade agêntica: Transição dos Níveis 1-3 (prompts e scripts) para os Níveis 5-6 (Rede Agêntica Autônoma com governança e responsabilidade). |
| **`e71a2615560242dfb4504c7fe87b4427.jpg`** | **Master Enterprise Architecture (TMF Structure)** | Yonnie Otieno | Taxonomia padronizada numerada (`01_...`, `02_...`), rastreador de documentos (`DOCUMENT_TRACKER`), controle de versão (`VERSION_LOG.md`) e registro de alterações. |

---

## 🧭 Como Usar no Startuzeiro OS

1. **Ao criar um novo prompt**: Armazene em `prompts/system/`, `prompts/tasks/` ou `prompts/tools/` com versionamento claro.
2. **Ao criar uma nova oportunidade**: Classifique no P.A.R.A. em `brain/01_oportunidades/<vetor>/` com cálculo de pontuação ICE.
3. **Ao avaliar ferramentas**: Utilize a matriz de maturidade agêntica (Image 2 e Image 5) antes de integrar à bancada.
