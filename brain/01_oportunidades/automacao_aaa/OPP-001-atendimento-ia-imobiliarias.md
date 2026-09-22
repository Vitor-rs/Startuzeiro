---
id: OPP-001
titulo: "Automação de Triagem e Agendamento com IA para Imobiliárias Locais"
categoria: automacao
status: investigacao
score_ice:
  impacto: 8
  confianca: 7
  facilidade: 8
  media: 7.6
potencial_receita: "R$ 1.500 - R$ 3.000/mes por cliente"
investimento_inicial: "R$ 50 (hospedagem VPS)"
data_criacao: 2026-09-22
tags: [imobiliaria, whatsapp, n8n, ia, leads]
---

# OPP-001: Automação de Triagem e Agendamento com IA para Imobiliárias Locais

## 1. Resumo Executivo

Implementar um agente de IA no WhatsApp integrado ao CRM imobiliário para qualificar leads que entram fora do horário comercial (noites e finais de semana), respondendo dúvidas sobre imóveis e pré-agendando visitas diretamente na agenda do corretor de plantão.

---

## 2. A Dor & O Público-Alvo

- **ICP:** Pequenas e médias imobiliárias locais (3 a 15 corretores) que investem em anúncios (Meta Ads / Portais como Zap/VivaReal), mas demoram horas para responder contatos.
- **Dor urgente:** Leads esfriam rapidamente (o tempo médio de resposta no setor passa de 2 horas). Corretores perdem tempo respondendo curiosos que não têm renda compatível.
- **Custo de não resolver:** Perda direta de comissões de R$ 5.000 a R$ 20.000 por venda não concluída.

---

## 3. Solução Proposta & Modelo de Negócio

- **Modelo:** Setup inicial de implementação (R$ 1.500) + Manutenção/Hospedagem recorrente (R$ 450 a R$ 750/mês).
- **Entrega técnica:** Fluxo no [[n8n]] conectado a uma API não-oficial ou Cloud API de WhatsApp + LLM com prompt de triagem e busca vetorial/tabela de imóveis disponíveis.
- **Diferencial:** Não tenta fechar a venda; foca estritamente em **qualificar renda/bairro** e **agendar visita**.

---

## 4. Benchmark & Concorrentes

| Concorrente | Modelo/Preço | O que faz bem | Onde falha / Brecha |
| :--- | :--- | :--- | :--- |
| Plataformas SaaS Genéricas (ex: chatbots tradicionais) | R$ 300 - R$ 800/mês | Painel bonito | Respostas robóticas em árvore, difícil integração local |
| Agências de Tráfego locais | Vendem lead, mas não resolvem o atendimento | Entregam volume | O cliente reclama que "os leads são ruins" porque ninguém atende rápido |

---

## 5. Ferramentas & Tecnologias Envolvidas

- [[n8n]] (orquestrador de fluxo)
- [[Evolution API]] ou Cloud API (WhatsApp)
- [[OpenAI]] ou Groq (processamento de linguagem natural e extração de dados)

---

## 6. Hipótese de Validação Falseável
>
> **"Se abordarmos 15 imobiliárias da região que estão rodando anúncios no Facebook/Instagram oferecendo auditar o tempo de resposta delas e demonstrar um bot de triagem em vídeo personalizado, pelo menos 3 aceitarão uma reunião e 1 contratará um piloto pago."**

---

## 7. Experimentos Associados

- [[EXP-001-auditoria-tempo-resposta-imobiliarias]]

---

## 8. Decisão & Próximos Passos

- [ ] Listar 15 imobiliárias anunciando ativamente na Biblioteca de Anúncios da Meta
- [ ] Testar tempo de resposta enviando mensagem no WhatsApp comercial delas em um domingo à noite
- [ ] Gravar vídeo de demonstração de 2 minutos no Loom
