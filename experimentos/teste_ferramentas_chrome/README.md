# 🧪 Registro de Testes Locais: Ferramentas dos Favoritos do Chrome

Ambiente de Testes: **Windows 11**  
Runtimes Disponíveis:
- **Python 3.12** com **`uv` / `uvx`** (✅ Testado e Operacional)
- **Node.js v24.12.0** com **`npm` / `npx`** (✅ Testado e Operacional)
- **Docker v29.4.0** (Instalado; requer inicializar o Docker Desktop para containers)

---

## 1. Ferramentas Testadas e Validadas com Sucesso

### ✉️ MailAccess (`KatrielMoses/MailAccess`) — 1.4k ⭐
- **Tipo:** CLI de OSINT de e-mails em 2500+ serviços, detecção de vazamentos e resolução de padrões.
- **Resultado do Teste:** Executado com sucesso via `uvx` sem poluir o ambiente global.
- **Comandos Validados:**
  ```bash
  # Diagnóstico completo de conectividade e módulos
  uvx mailaccess doctor

  # Listar comandos disponíveis
  uvx mailaccess --help

  # Resolver padrão corporativo de e-mail (Nome + Domínio)
  uvx mailaccess find-email --name "Nome Sobrenome" --domain "empresa.com"

  # Investigar endereço de e-mail completo
  uvx mailaccess investigate "contato@empresa.com"

  # Coleta de e-mails associados a um domínio
  uvx mailaccess harvest-emails --domain "empresa.com"
  ```
- **Sinergia:** Integra-se com as chaves que você já tem no Startuzeiro (Hunter.io, GitHub token, etc.).

---

### 🕷️ Scrapling (`d4vinci/Scrapling`) — 82.9k ⭐
- **Tipo:** Framework adaptativo de web scraping com bypass de proteção anti-bot (Cloudflare Turnstile).
- **Resultado do Teste:** Instalado e importado via `uv run` em 536ms.
- **Comandos Validados:**
  ```bash
  uv run --with scrapling python -c "import scrapling; print('Scrapling operacional!')"
  ```
- **Como usar nos seus scripts:**
  ```python
  from scrapling import Fetcher

  fetcher = Fetcher(auto_match=True)
  response = fetcher.get("https://exemplo.com")
  print(response.css("h1::text").first())
  ```
- **Sinergia:** O assistente já possui a skill oficial `scrapling-official` configurada.

---

### 📊 PPT Master (`hugohe3/ppt-master`) — 56.0k ⭐
- **Tipo:** Geração de apresentações PowerPoint `.pptx` reais e editáveis a partir de materiais e notas de pesquisa usando IA.
- **Como Testar:**
  ```bash
  # Clone do repositório para a pasta de experimentos
  git clone https://github.com/hugohe3/ppt-master.git experimentos/ppt-master
  ```
- **Sinergia:** Cria apresentações comerciais nativas a partir das notas da pasta `knowledge/` e `pesquisas/`.

---

### 🌐 AI Website Cloner Template (`JCodesMore/ai-website-cloner-template`) — 34.8k ⭐
- **Tipo:** Template Next.js + Playwright para agentes recriarem landing pages completas a partir de uma URL.
- **Como Testar:**
  ```bash
  git clone https://github.com/JCodesMore/ai-website-cloner-template.git experimentos/ai-cloner
  cd experimentos/ai-cloner
  npm install
  npm run dev
  ```
