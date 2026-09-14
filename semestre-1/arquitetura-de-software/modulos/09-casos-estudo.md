# Módulo 09 — Casos de Estudo

## Introdução

Casos de estudo de empresas reconhecidas ilustram como decisões arquitecturais reais respondem a contextos de negócio, escala e evolução organizacional. Analisar Netflix, Amazon e Spotify — com base em conhecimento público (engineering blogs, conferências) — permite extrair lições transferíveis sem prescrever soluções universais. Este módulo apresenta a evolução arquitectural de cada caso, decisões-chave e aprendizagens para arquitectos.

## Netflix — De Datacenter a Cloud e Microserviços

### Contexto

Netflix iniciou como serviço de DVD por correio, evoluindo para streaming de vídeo global. Crescimento explosivo de utilizadores e catálogo exigiu arquitectura capaz de escalar, tolerar falhas e inovar rapidamente.

### Evolução Arquitectural

**Fase inicial:** aplicação monolítica em datacenter próprio. Dificuldades de escala e disponibilidade.

**Migração cloud (2008–2016):** decisão estratégica de migrar para **AWS**, abandonando datacenters. Motivação: elasticidade, redução de capital expenditure, foco no core business (conteúdo e experiência).

**Microserviços:** decomposição gradual do monolito em centenas de microserviços. Cada equipa responsável por serviços específicos (recomendações, billing, playback, encoding).

**Resiliência — Chaos Engineering:** desenvolvimento do **Chaos Monkey** e suite Simian Army — injectam falhas deliberadamente em produção para validar tolerância. Filosofia "fail fast, recover gracefully".

**CDN — Open Connect:** Netflix desenvolveu CDN proprietária (Open Connect Appliances) colocada em ISPs, reduzindo latência e custos de bandwidth — arquitectura híbrida cloud + edge.

### Decisões e Atributos de Qualidade

| Decisão | Atributo prioritário |
|---------|---------------------|
| AWS + auto-scaling | Escalabilidade, elasticidade |
| Microserviços | Autonomia equipas, deploy independente |
| Chaos Engineering | Disponibilidade, resiliência |
| Open Connect | Desempenho (latência), custo |
| Event-driven (internamente) | Desacoplamento |

### Lições

- Migração cloud e microserviços são jornadas incrementais, não big-bang.
- Investir em observabilidade e resiliência desde cedo compensa em escala.
- Cultura organizacional (equipas autónomas, tolerância a falhas) é pré-requisito para microserviços.
- Soluções custom (CDN) justificam-se quando requisitos excedem oferta standard.

## Amazon — E-commerce, APIs e Two-Pizza Teams

### Contexto

Amazon cresceu de livraria online para marketplace global, AWS, streaming e mais. A arquitectura reflecte décadas de escala e diversificação de negócio.

### Evolução Arquitectural

**"Two-pizza teams":** equipas pequenas (alimentáveis por duas pizzas) com ownership end-to-end de serviços — manifestação de Conway's Law invertido. Cada equipa expõe funcionalidade via **APIs internas**.

**Mandato API (2002):** Jeff Bezos exigiu que toda comunicação interna fosse via interfaces servidas externamente — sem acesso directo a BD de outros serviços. Fundamento cultural para microserviços antes do termo ser popular.

**Decomposição por domínio:** serviços separados para catálogo, carrinho, checkout, pagamentos, fulfillment, reviews — cada um escala e evolui independentemente.

**AWS como produto:** infraestrutura interna (computação, storage) tornou-se produto externo — case study de como arquitectura interna gera negócio.

**Eventual consistency:** marketplace tolera consistência eventual em áreas não críticas (reviews, recomendações) enquanto checkout exige consistência forte.

### Decisões e Atributos

| Decisão | Atributo prioritário |
|---------|---------------------|
| API-first interno | Interoperabilidade, modularidade |
| Two-pizza teams | Time-to-market, autonomia |
| Separação read/write em áreas | Escalabilidade |
| AWS | Elasticidade, novo revenue stream |

### Lições

- Mandatos arquitecturais claros (API-only) moldam cultura duradoura.
- Organização e arquitectura co-evoluem — equipas pequenas e autónomas requerem boundaries de serviço claros.
- Investimento em plataforma interna pode tornar-se vantagem competitiva externa.
- Diferentes partes do sistema toleram diferentes garantias de consistência.

## Spotify — Squads, Tribes e Monolito Modular

### Contexto

Spotify revolucionou streaming de música com modelo organizacional ágil (Squads, Tribes, Chapters, Guilds) e arquitectura que evoluiu pragmaticamente.

### Evolução Arquitectural

**Squads e Tribes:** equipas multidisciplinares (squad) agrupadas por área de produto (tribe). **Chapters** (especialização técnica) e **Guilds** (comunidades de prática) cruzam squads.

**Backend evolution:** Spotify não adoptou microserviços puros de início. Evoluiu de monolito para **monolito modular** com boundaries internos, extraindo serviços quando necessário — abordagem pragmática vs. decomposição prematura.

**Client architecture:** aplicações cliente (mobile, desktop, web) com arquitectura modular; feature flags e experimentação contínua (A/B testing) integrados na plataforma.

**Data-driven:** pipeline de eventos para analytics e recomendações (Discover Weekly). Arquitectura orientada a dados e eventos para personalização.

**Developer experience:** Backstage (plataforma open-source de developer portal) nasceu internamente — catálogo de serviços, documentação, scaffolding.

### Decisões e Atributos

| Decisão | Atributo prioritário |
|---------|---------------------|
| Squads autónomas | Time-to-market, inovação |
| Monolito modular inicial | Simplicidade operacional |
| Feature flags | Experimentação, deploy seguro |
| Event pipeline | Personalização, analytics |

### Lições

- Microserviços não são obrigatórios desde dia um — monolito modular bem feito escala organizacionalmente antes de escala técnica exigir decomposição.
- Modelo organizacional (squads) deve alinhar com boundaries de software.
- Developer experience e tooling são investimento arquitectural, não luxo.
- Experimentação contínua requer arquitectura que suporte feature flags e rollback.

## Comparação Transversal

| Aspeto | Netflix | Amazon | Spotify |
|--------|---------|--------|---------|
| Driver principal | Escala global streaming | Marketplace + diversificação | Inovação produto, UX |
| Cloud | AWS (100%) | AWS (origem) | Multi-cloud/híbrido |
| Microserviços | Extensivo, maduro | Extensivo, cultural | Gradual, pragmático |
| Organização | Equipas por serviço | Two-pizza teams | Squads/Tribes |
| Diferenciador | Chaos Eng., CDN | API mandate, AWS | DX, experimentação |

## Como Usar Casos de Estudo

Casos de estudo **não são receitas**. Contexto importa: Netflix tinha escala e maturidade que startup não tem. Lições transferíveis:
- Priorize atributos de qualidade explicitamente.
- Alinhe organização e arquitectura.
- Evolua incrementalmente.
- Invista em observabilidade, resiliência e developer experience proporcionalmente ao risco e escala.

## Exercícios

1. Qual foi a principal motivação da migração da Netflix para AWS e que atributos de qualidade endereçou?

2. Explique o "mandato API" da Amazon e como influenciou a arquitectura actual.

3. Compare a abordagem da Netflix (microserviços agressivos) com a da Spotify (monolito modular gradual). Quando cada uma faz sentido?

4. O que é Chaos Engineering e porque a Netflix o adoptou?

5. Como o modelo de Squads da Spotify se relaciona com Conway's Law?

6. Identifique um trade-off comum entre os três casos de estudo (ex.: consistência vs. disponibilidade) e como cada empresa o resolve.

7. Uma startup de streaming com 10 developers deve copiar a arquitectura da Netflix? Justifique.

8. Que lição comum extrairia dos três casos sobre relação entre organização e arquitectura?

## Soluções

1. **Motivação:** escala imprevisível de streaming global, custos de datacenter, necessidade de elasticidade e foco no core business. **Atributos:** escalabilidade (auto-scaling AWS), disponibilidade (redundância cloud), elasticidade (pagar por uso), time-to-market (infra managed).

2. **Mandato API (2002):** toda comunicação interna via APIs documentadas, expostas externamente; proibido aceder directamente a bases de dados ou recursos internos de outros serviços. **Influência:** forçou desacoplamento, ownership claro de dados, evolução independente de serviços — base cultural e técnica para microserviços e eventualmente AWS.

3. **Netflix (microserviços agressivos):** escala massiva, centenas de equipas, necessidade de deploy e escala independente, maturidade operacional (Chaos Eng.). **Spotify (gradual):** fase inicial com equipa menor, monolito modular reduz overhead operacional, extrai serviços quando boundaries maduros. **Quando:** microserviços agressivos com escala e maturidade DevOps; gradual para startups/médias empresas que crescem orgânica e tecnicamente.

4. **Chaos Engineering:** prática de injectar falhas controladas em produção (servidor termina, latência injectada) para validar resiliência. **Netflix adoptou** porque escala distribuída torna falhas inevitáveis — melhor descobrir vulnerabilidades proactivamente do que em incidentes reais. Valida atributo disponibilidade e cultura "fail gracefully".

5. **Conway's Law:** software espelha comunicação organizacional. **Squads** são equipas autónomas multidisciplinares alinhadas a features/domínios — promovem arquitectura modular onde cada squad ownership de componentes específicos. Tribes agrupam squads relacionados; chapters/guilds partilham conhecimento sem quebrar autonomia. Organização desenhada para produzir sistemas desacoplados.

6. **Trade-off consistência vs. disponibilidade (CAP):** **Amazon** — checkout e pagamentos com consistência forte (ACID); reviews e recomendações eventual consistency. **Netflix** — playback prioriza disponibilidade (cache local, CDN); billing mais consistente. **Spotify** — playback offline tolera stale data; subscrições exigem consistência. Cada empresa segmenta por criticidade de domínio.

7. **Não.** Netflix tem centenas de serviços, milhares de engenheiros, anos de investimento em observabilidade e Chaos Engineering. Startup com 10 developers beneficiaria de monolito modular ou poucos serviços, foco em product-market fit, infra managed simples. Copiar Netflix seria over-engineering — complexidade operacional mataria velocidade. Adoptar **princípios** (APIs, separação de concerns, preparar evolução) sim; copiar **estrutura** não.

8. **Lição comum:** organização e arquitectura devem co-evoluir deliberadamente. Netflix (equipas por serviço), Amazon (two-pizza teams + API mandate), Spotify (squads + monolito modular) — todos alinharam estrutura organizacional com boundaries de software. Ignorar esta relação produz friction, dependências e sistemas que não escalam humanamente nem tecnicamente.
