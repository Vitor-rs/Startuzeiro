# 💻 Guia de Sincronização e Uso no Laptop ASUS

> **Desktop:** `Vitor-pc` (Windows 10 Pro) — `C:\Users\Vitor\Documents\projetos\Startuzeiro`  
> **Laptop:** `ASUS-Wizard-Navirai` (Windows 11 Home) — `C:\Users\user\Documents\Vitor\Startuzeiro`

---

## ⚡ Setup Inicial no Laptop (Feito apenas 1 vez)

Ao clonar o repositório no laptop pela primeira vez:

```powershell
cd C:\Users\user\Documents\Vitor\
git clone https://github.com/Vitor-rs/Startuzeiro.git
cd Startuzeiro
```

Execute o script de setup automático que configura o `.env`, o `uv` e os MCPs no Antigravity:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup/setup_machine.ps1
```

Esse script realiza automaticamente:
1. **Criação do `.env`:** Copia o `.env.example` para `.env` para você preencher suas chaves de API com segurança.
2. **Instalação/Verificação do `uv`:** Garante que o `uv` está instalado no sistema.
3. **Configuração Global dos MCPs:** Injeta automaticamente no `C:\Users\user\.gemini\config\mcp_config.json` as entradas de:
   - `transcript-api` (com seu token obtido do `.env`)
   - `firecrawl` (com seu token e runner `npx -y firecrawl-mcp`)
   - `context7` (com seu token obtido do `.env`)
   - `exa` (com sua chave obtida do `.env`)
   - `cnpj-ai` (com sua chave obtida do `.env`)
   - `hunter` (com sua chave obtida do `.env`)
   - `apollo` (com sua chave obtida do `.env`)

---

## 🔄 Rotina Diária de Sincronização entre as Máquinas

Como a fonte da verdade é o **Git + GitHub**, a rotina é muito simples:

### Quando for sair do Desktop para o Laptop:
No Desktop:
```bash
git add .
git commit -m "docs: atualizacoes do dia"
git push origin main
```

No Laptop:
```bash
git pull origin main
```

### Quando for sair do Laptop de volta para o Desktop:
No Laptop:
```bash
git add .
git commit -m "docs: progresso no laptop"
git push origin main
```

No Desktop:
```bash
git pull origin main
```

---

## 🧰 Estado dos Componentes nas Duas Máquinas

| Componente | Onde fica armazenado | Status de Portabilidade |
| :--- | :--- | :--- |
| **39 Skills (`firecrawl*`, `transcriptapi`, `context7*`, `exa*`, `cnpj-ai*`, `hunter-b2b*`, `apollo-sales*`)** | `.agents/skills/` (no repositório) | ✅ 100% versionado no Git |
| **Regras do Agente (`AGENTS.md`, rules)** | `.agents/rules/` e raiz | ✅ 100% versionado no Git (caminhos dinâmicos) |
| **Catálogo de 61 Ferramentas** | `ferramentas/catalogo.yaml` e `knowledge/` | ✅ 100% versionado no Git |
| **Lake de Transcrições (`yt_base`)** | `yt_base/` | ✅ 100% versionado no Git |
| **Scripts e Utilitários** | `scripts/` | ✅ 100% portáveis (usam caminhos relativos ao repositório) |
| **Chaves de API (`.env`)** | Raiz do projeto | ⚠️ Ignorado pelo Git por segurança. Gerado via `.env.example` |
| **Configuração de MCPs** | `~/.gemini/config/mcp_config.json` | ⚙️ Configurado via `scripts/setup/setup_machine.ps1` |
