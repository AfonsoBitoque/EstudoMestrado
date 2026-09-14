# Módulo 06 — Alinhamento entre Arquiteturas

## Introdução

O valor da tecnologia manifesta-se quando suporta efectivamente os objectivos de negócio. O **alinhamento business-IT** — e, mais especificamente, entre arquitectura empresarial e arquitectura de software — é desafio persistente nas organizações. Este módulo aborda estratégias de alinhamento, métodos de avaliação arquitectural (incluindo ATAM) e práticas para garantir coerência entre visão estratégica e implementação técnica.

## Alinhamento Business-IT

**Alinhamento business-IT** significa que investimentos, projectos e decisões de TI são coerentes com prioridades estratégicas de negócio, e que capacidades tecnológicas habilitam vantagem competitiva.

### Níveis de Alinhamento (Henderson & Venkatraman)

Modelo **Strategic Alignment Model** propõe quatro domínios e ligações:
- **Business Strategy** ↔ **IT Strategy** (estratégico)
- **Organizational Infrastructure** ↔ **IT Infrastructure** (operacional)
- **Business Strategy** ↔ **Organizational Infrastructure** (execução negócio)
- **IT Strategy** ↔ **IT Infrastructure** (execução TI)

Alinhamento pode ser:
- **Strategy execution:** TI implementa estratégia de negócio definida.
- **Technology transformation:** TI identifica oportunidades tecnológicas que moldam estratégia.
- **Competitive potential:** TI e negócio co-evoluem.
- **Service level:** TI optimiza infraestrutura para eficiência operacional.

Desalinhamento manifesta-se como: projectos técnicos sem valor de negócio claro, requisitos de negócio ignorados na implementação, redundância de sistemas, incapacidade de responder a mudanças de mercado.

### Práticas de Alinhamento

**Tradução de objectivos:** OKRs ou metas de negócio mapeados para capabilities e requisitos arquitecturais. Exemplo: "Reduzir time-to-market em 30%" → arquitectura modular, CI/CD, feature flags.

**Comités de arquitectura:** forum multidisciplinar (negócio, EA, arquitectos de solução) que revê propostas antes de investimento significativo.

**Architecture runway:** capacidade técnica preparada antecipadamente para features de negócio previstas — evita que cada feature exija refactor arquitectural.

**Value streams:** organizar equipas e sistemas ao longo de fluxos de valor end-to-end (cliente pede → recebe produto) em vez de silos funcionais.

**Feedback loops:** métricas de negócio (conversão, churn) ligadas a métricas técnicas (disponibilidade, latência) em dashboards partilhados.

## EA e Arquitectura de Software Alinhadas

EA define **constraints e oportunidades** ao nível empresarial; arquitectura de software opera dentro desse enquadramento:

| EA (macro) | Software (meso/micro) |
|------------|----------------------|
| Capability map | Bounded contexts / serviços |
| Application portfolio | Sistemas e APIs concretos |
| Data governance policies | Modelos de dados, eventos |
| Technology standards | Stack por projecto |
| Roadmap de transformação | ADRs, sprints, releases |

**Gap analysis:** comparar estado actual (as-is) com target architecture (to-be) identifica projectos de software necessários. Arquitectos de software participam na definição do to-be e executam migrações.

**Conway's Law inverso:** organizar equipas para reflectir arquitectura desejada (módulos independentes → equipas independentes).

## Métodos de Avaliação de Arquitectura

Avaliar arquitecturas antes e durante implementação reduz riscos de decisões inadequadas.

### ATAM — Architecture Tradeoff Analysis Method

**ATAM** (SEI/Carnegie Mellon) é método estruturado para avaliar se uma arquitectura satisfaz **quality attributes** (cenários de qualidade) e identificar **trade-offs** e **sensitivity points**.

**Participantes:** stakeholders, arquitectos, evaluators (facilitadores externos ou internos).

**Fases principais:**
1. **Presentação ATAM:** introduzir método e participantes.
2. **Apresentação negócio drivers:** motivação, requisitos, constraints.
3. **Apresentação arquitectura:** arquitectos apresentam abordagem.
4. **Identificação approaches arquitecturais:** estilos, patterns adoptados.
5. **Geração quality attribute utility tree:** priorizar cenários (H/M/L).
6. **Análise cenários:** para cada cenário prioritário, identificar componentes, decisões e riscos.
7. **Brainstorming sensitivity points e trade-offs.**
8. **Consolidação resultados:** riscos, não-riscos, pontos de sensibilidade.

**Outputs:** lista de riscos arquitecturais, trade-offs documentados, cenários não satisfitos, recomendações.

Exemplo de cenário: "Sob pico de 10.000 utilizadores simultâneos, checkout responde em <2s em 95% dos casos." ATAM analisa se load balancing, cache e async processing suportam o cenário.

### Outros Métodos

**SAAM (Software Architecture Analysis Method):** predecessor do ATAM, focado em modificabilidade.

**CBAM (Cost Benefit Analysis Method):** estende ATAM com análise custo-benefício de estratégias arquitecturais.

**LAAAM (Lightweight Architecture Alternative Assessment Method):** versão simplificada para iterações ágeis.

**Architecture Reviews informais:** walkthroughs regulares em comité de arquitectura — menos formal que ATAM mas contínuos.

### Quando Usar ATAM

Projectos de alto risco ou investimento significativo, sistemas críticos (saúde, finanças), múltiplas alternativas arquitecturais plausíveis, ou stakeholders com preocupações conflituosas sobre qualidade. Para MVPs de baixo risco, reviews leves podem bastar.

## Métricas de Alinhamento

- **Business-IT alignment score:** surveys periódicos a executivos.
- **Time from idea to production:** proxy de agilidade alinhada.
- **Percentage of IT budget on strategic vs. maintenance:** "run vs. change".
- **Architecture compliance rate:** projectos conformes com EA standards.
- **Technical debt ratio vs. feature delivery:** equilíbrio investimento.

## Exercícios

1. O que é alinhamento business-IT e quais sinais de desalinhamento numa organização?

2. Explique o modelo de Henderson & Venkatraman em termos simples. Dê um exemplo de ligação estratégica.

3. Descreva as fases principais do ATAM e os outputs esperados.

4. Crie um cenário de qualidade (stimulus, environment, response, measure) para disponibilidade num sistema de pagamentos.

5. O que é "architecture runway" e como contribui para alinhamento?

6. Um projecto de software ignora standards de EA e escolhe tecnologia não aprovada. Que riscos de desalinhamento existem?

7. Compare ATAM com uma architecture review informal — quando preferir cada uma?

8. Como o Conway's Law afecta alinhamento entre arquitectura de software e estrutura organizacional?

## Soluções

1. **Alinhamento business-IT:** TI coerente com objectivos e prioridades de negócio. **Sinais de desalinhamento:** projectos entregues que negócio não usa; requisitos ignorados; sistemas duplicados; TI bloqueia inovação ou negócio contorna TI (shadow IT); métricas de sucesso diferentes entre departamentos; incapacidade de responder a oportunidades de mercado por limitações técnicas.

2. Modelo liga **estratégia de negócio** a **estratégia de TI** (estratégico) e **infraestrutura organizacional** a **infraestrutura de TI** (operacional). Exemplo ligação estratégica: negócio decide expandir para novos mercados → estratégia de TI inclui plataforma multi-idioma, multi-moeda e compliance regional → arquitectura de software implementa i18n, localização e modularidade por região.

3. **Fases ATAM:** apresentações (método, drivers, arquitectura); identificação de approaches; utility tree de quality attributes; análise de cenários prioritários; identificação de sensitivity points e trade-offs; consolidação. **Outputs:** riscos arquitecturais, trade-offs, cenários problemáticos, recomendações de mitigação.

4. **Cenário disponibilidade:** Stimulus: falha do servidor de aplicação principal. Environment: produção, carga normal, deployment com 3 réplicas atrás de load balancer. Response: tráfego redireccionado para réplicas saudáveis sem interrupção perceptível ao utilizador. Measure: disponibilidade mantida ≥99,9%; failover em <30 segundos; zero perda de transacções em curso (com retry idempotente).

5. **Architecture runway:** capacidade técnica preparada antecipadamente (APIs base, infra CI/CD, módulos core) para acelerar entrega de features de negócio futuras. Contribui para alinhamento porque negócio pode planear features assumindo fundação pronta, reduzindo time-to-market e evitando que cada iniciativa exija rework arquitectural — TI antecipa necessidades derivadas da roadmap de negócio.

6. **Riscos:** integração difícil com resto do portfolio; custos de operação e formação elevados; vulnerabilidades de segurança por falta de expertise; lock-in com fornecedor; impossibilidade de partilhar dados conforme governance; dívida de conformidade quando EA exigir migração; silo técnico que impede reutilização e escala de equipas.

7. **ATAM:** projectos críticos, alto investimento, múltiplas alternativas, stakeholders diversos — avaliação formal, documentada, com utility tree e cenários. **Review informal:** iteraciones ágeis, MVPs, equipas pequenas, risco baixo — feedback rápido em comité semanal. Preferir ATAM quando erro arquitectural tem impacto severo e reversão cara; reviews informais para fluxo contínuo e decisões incrementais.

8. **Conway's Law:** organizações produzem sistemas que espelham estruturas de comunicação. Se equipas estão organizadas por camada (frontend, backend, BD), software tende a monolitos acoplados. Para alinhamento, estruturar equipas por domínio/capability (squads alinhadas a serviços) promove arquitectura modular correspondente. Desalinhamento organizacional-arquitectural gera friction, dependências e deploys coordenados.
