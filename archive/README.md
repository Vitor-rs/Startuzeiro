# 🪦 Arquivo de Ideias Descartadas (O Cemitério de Hipóteses)

Esta pasta é uma das mais importantes do laboratório **Startuzeiro**.

---

## Por que guardar ideias descartadas?
1. **Evitar amnésia investigativa:** Daqui a 6 meses você terá a mesma ideia e esquecerá por que ela era inviável.
2. **Mudança de contexto de mercado:** Uma ideia que era ruim hoje pode se tornar viável se uma nova ferramenta surgir ou o custo de API cair 90%.
3. **Economia de tempo:** Consultar o arquivo antes de começar uma pesquisa economiza dias de trabalho repetido.

---

## Como arquivar uma oportunidade
Quando uma oportunidade for considerada inviável (na fase de `investigacao` ou após um `experimento` sem tração):
1. Altere o frontmatter dela para `status: descartado`.
2. Adicione uma seção no final chamada `## 9. Motivo do Descarte & Aprendizado`.
3. Mova o arquivo para esta pasta `archive/`.

---

## Estrutura recomendada da seção de descarte
```markdown
## 9. Motivo do Descarte & Aprendizado
- **Data do descarte:** YYYY-MM-DD
- **Principal motivo:** (Ex: CAC muito alto / Margem baixa / Clientes não valorizam a solução / Ferramenta instável)
- **O que precisaria mudar para esta ideia voltar à mesa:** (Ex: "Se surgir uma API oficial de WhatsApp com custo zero para mensagens receptivas")
```
