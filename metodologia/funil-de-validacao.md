# Funil de Validação do Startuzeiro

O objetivo deste funil é evitar que tempo, dinheiro e energia sejam gastos em código ou automações complexas antes que a viabilidade de mercado seja comprovada.

---

## 1. Princípio Fundamental

> **"A infraestrutura deve ser menor que a pesquisa."**  
> Antes de criar uma ferramenta ou aplicação, criamos documentos, levantamos evidências e testamos a intenção de compra.

---

## 2. As Fases do Funil

```text
 [ Ideia ]
     │
     ▼
 [ Investigação ] ──> (Inviável? ──> [ Archive ])
     │
     ▼
 [ Experimento / Validação ] ──> (Sem tração? ──> [ Archive ])
     │
     ▼
 [ Execução / Projeto Ativo ]
```

### Fase 1: `ideia` (Captura Rápida)

- **O que é:** Qualquer faísca de proposta, mercado, tendência ou nicho.
- **Onde mora:** Arquivo rascunho em `oportunidades/<categoria>/` com status `ideia`.
- **Critério para avançar:** Ter um problema claro identificado e pelo menos uma suspeita de como monetizar.

### Fase 2: `investigacao` (Inteligência & Mercado)

- **O que é:** Pesquisa ativa usando ferramentas (Firecrawl, Google, redes, MCPs).
- **Entregáveis:**
  - Mapeamento de 3 a 5 concorrentes ou soluções existentes.
  - Estimativa de preço praticado no mercado.
  - Identificação do público-alvo (quem tem a dor e tem dinheiro para pagar).
  - Pontuação preliminar pelo [[criterios-ice|Score ICE]].
- **Critério para avançar:** ICE score aceitável e barreira de entrada superável.

### Fase 3: `validando` (Teste de Hipótese Prático)

- **O que é:** Teste no mundo real com o menor custo possível.
- **Exemplos de testes:**
  - 20 mensagens frias (cold outreach) para tomadores de decisão.
  - Landing page simples com botão de "Entrar na lista de espera" ou "Comprar".
  - Proposta manual prestada como serviço antes de virar automação/SaaS.
  - Teste com R$ 50 a R$ 100 de tráfego pago para medir CTR/Conversão.
- **Onde mora:** Pasta dedicada em `experimentos/EXP-xxx/`.
- **Critério para avançar:** Pelo menos uma pessoa demonstrou intenção real de pagamento (sinal verde).

### Fase 4: `executando` (Projeto / Negócio Ativo)

- **O que é:** A proposta provou viabilidade econômica e tração real.
- **O que acontece:** Pode virar um repositório dedicado, um SaaS ou um serviço recorrente com código próprio.

### Fase 5: `descartado` (Arquivo com Aprendizado)

- **O que é:** A ideia foi investigada ou testada e mostrou-se inviável (ex: mercado saturado, ticket muito baixo, CAC maior que LTV).
- **Regra de ouro:** Nunca delete! Mova para a pasta `archive/` com a seção **"Por que foi descartado"** preenchida. O maior valor de um laboratório é não repetir pesquisas que já foram feitas.
