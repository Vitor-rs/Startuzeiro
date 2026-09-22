# 📊 Rubrica de Avaliação ICE (Scorecard) do Startuzeiro OS

Este documento padroniza como o Cérebro Agêntico avalia e pontua oportunidades de negócio em `brain/01_oportunidades/`.

---

## 📐 Fórmula do ICE Score

$$\text{ICE Score} = \text{Impacto} \times \text{Confiança} \times \text{Facilidade}$$

Variação: de **1** (inviável) a **1000** (oportunidade de ouro).

---

## 1. Impacto (1 a 10)
*Quanto dinheiro esse negócio pode gerar e qual o nível de alavancagem?*

- **1 - 3**: Receita baixa, venda pontual < R$ 100, esforço 1:1 sem escala.
- **4 - 6**: Ticket médio moderado (R$ 500 a R$ 1.500) ou micro-SaaS nichado com TAM limitado.
- **7 - 8**: Receita recorrente (MRR R$ 3.000 a R$ 15.000/mês) ou tickets B2B de R$ 3.000 a R$ 10.000.
- **9 - 10**: Alavancagem infinita (SaaS escalável, arbitragem automatizada de R$ 50k+/mês).

---

## 2. Confiança (1 a 10)
*Quão comprovada é essa dor no mundo real e qual a certeza de que as pessoas pagarão?*

- **1 - 3**: Ideia teórica baseada em suposições, sem concorrentes validando o mercado.
- **4 - 6**: Dor confirmada em fóruns/redes, mas modelo de monetização ainda incerto.
- **7 - 8**: Concorrentes já faturam alto com essa solução, e mentores/vídeos recomendam a abordagem.
- **9 - 10**: Alvo já gasta dinheiro com soluções piores e aceita pilotos pagos imediatamente.

---

## 3. Facilidade (1 a 10)
*Quão rápido conseguimos construir e testar a solução usando a bancada do Startuzeiro?*

- **1 - 3**: Exige meses de desenvolvimento, infraestrutura pesada ou certificações complexas.
- **4 - 6**: Requer 2 a 3 semanas de montagem e integrações com múltiplas APIs pagas.
- **7 - 8**: Construível em 3 a 5 dias usando Python, FastAPI, Hunter, Clay e n8n.
- **9 - 10**: Testável em menos de 48 horas usando scripts já prontos em `scripts/utilitarios/`.

---

## 🚦 Faixas de Decisão Estratégica

| ICE Score | Classificação | Decisão Agêntica |
| :--- | :--- | :--- |
| **>= 400** | 🟢 **Prioridade Máxima (Tier 1)** | Executar experimento piloto de validação imediatamente (< 7 dias). |
| **200 - 399** | 🟡 **Alta Prioridade (Tier 2)** | Mapear concorrentes e enriquecer lista de ICPs no CRM. |
| **100 - 199** | ⚪ **Em Observação (Tier 3)** | Manter no Lake e monitorar movimentações de mercado. |
| **< 100** | 🔴 **Descartada / Arquivo** | Arquivar em `brain/04_arquivo/`. |
