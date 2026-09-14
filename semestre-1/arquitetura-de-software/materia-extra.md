# Matéria Extra — Tópicos Complementares

Este documento reúne tópicos avançados e recursos complementares à disciplina de Arquitetura de Software. Não fazem parte do programa obrigatório, mas enriquecem a formação e aparecem frequentemente em contexto profissional.

## Domain-Driven Design (DDD)

**Domain-Driven Design** (Eric Evans, 2003) é abordagem de desenvolvimento que coloca o **domínio de negócio** no centro do design de software.

### Conceitos-Chave

**Ubiquitous Language:** linguagem partilhada entre developers e especialistas de domínio, reflectida no código.

**Bounded Context:** limite explícito dentro do qual um modelo de domínio é válido. Cada contexto tem o seu modelo — "Cliente" em Vendas difere de "Cliente" em Suporte.

**Entities:** objectos com identidade persistente (Pedido, Cliente).

**Value Objects:** objectos definidos por atributos, sem identidade (Endereço, Dinheiro).

**Aggregates:** cluster de entidades/value objects tratado como unidade de consistência, com **Aggregate Root** como ponto de acesso.

**Domain Events:** factos significativos no domínio ("PedidoEnviado").

**Repositories:** abstracção de persistência para aggregates.

**Anti-Corruption Layer (ACL):** traduz modelos entre bounded contexts, protegendo domínio de influências externas.

### Relação com Arquitectura

DDD informa decomposição em microserviços (um bounded context ≈ um serviço), modelagem de APIs e eventos de domínio. Não é sinónimo de microserviços — DDD aplica-se também a monolitos modulares.

**Leitura:** Evans, E. — *Domain-Driven Design: Tackling Complexity in the Heart of Software*.

---

## CQRS — Command Query Responsibility Segregation

**CQRS** separa operações de **escrita** (commands — alteram estado) de **leitura** (queries — consultam estado) em modelos distintos.

### Motivação

Modelos de leitura e escrita têm requisitos diferentes: writes exigem consistência e validação de negócio; reads exigem desempenho, projeções optimizadas, denormalização.

### Implementação

- **Command side:** recebe commands, valida, persiste em write model, emite eventos.
- **Query side:** consome eventos ou réplicas, mantém read models optimizados para consultas (views, caches, search indexes).

### Benefícios e Custos

**Benefícios:** escala independente read/write, modelos optimizados por operação, flexibilidade de projeções. **Custos:** complexidade, consistência eventual entre read e write sides, mais infraestrutura.

### Quando Usar

Sistemas com ratio read/write muito assimétrico, UIs complexas com views diversas, ou combinado com Event Sourcing. Evitar em CRUD simples.

---

## Event Sourcing

**Event Sourcing** persiste o estado de uma entidade como **sequência de eventos** imutáveis, em vez de guardar apenas o estado actual.

### Funcionamento

Estado actual = replay de todos os eventos (ou snapshot + eventos recentes). Exemplo: conta bancária reconstruída de `ContaAberta`, `DepositoEfectuado`, `LevantamentoEfectuado`.

### Benefícios

Audit trail completo, capacidade de reconstruir estado histórico, facilita debugging temporal, natural fit com event-driven architecture e CQRS.

### Desafios

Modelagem de eventos requer cuidado (eventos imutáveis — correções via eventos compensatórios), storage crecente (snapshots mitigam), curva de aprendizagem, queries complexas sem projeções (CQRS resolve).

### Combinação CQRS + Event Sourcing

Padrão frequente: event store como write side; projeções alimentam read models. Usado em domínios financeiros, booking, gaming.

**Leitura:** Young, G. — materiais sobre CQRS and Event Sourcing (Codurance, GOTO conferences).

---

## AWS Well-Architected Framework

Framework da Amazon Web Services para avaliar arquitecturas cloud segundo seis pilares:

1. **Operational Excellence:** operações eficientes, observabilidade, automação, aprendizagem contínua.
2. **Security:** protecção de dados, least privilege, detecção de incidentes, encryption.
3. **Reliability:** recuperação de falhas, distribuição geográfica, auto-healing, quotas e limits.
4. **Performance Efficiency:** recursos adequados, serverless/containers, caching, seleção de região.
5. **Cost Optimization:** right-sizing, reserved capacity, eliminar waste, FinOps.
6. **Sustainability:** minimizar impacto ambiental — efficient resources, managed services, regiões verdes.

Cada pilar inclui **design principles** e **best practices** organizadas por workload. AWS oferece **Well-Architected Review** (questionário gratuito) e **Well-Architected Tool** no console.

Adaptável a outros clouds — princípios são vendor-agnostic em essência; Microsoft tem **Azure Well-Architected Framework** equivalente.

**Recurso:** [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

---

## Outros Tópicos Relevantes

| Tópico | Descrição breve |
|--------|------------------|
| **Saga Pattern** | Transacções distribuídas via sequência de transacções locais + compensações |
| **API Gateway / BFF** | Ponto único de entrada; Backend-for-Frontend por tipo de cliente |
| **Strangler Fig** | Migração incremental de legacy (módulo 02) |
| **Cell-based Architecture** | Isolamento em células para blast radius reduzido (usado por Amazon, Slack) |
| **Data Mesh** | Descentralização de ownership de dados por domínio |
| **Team Topologies** | Tipos de equipas (stream-aligned, platform, enabling, complicated-subsystem) |

---

## Livros Recomendados

| Livro | Autor | Foco |
|-------|-------|------|
| *Software Architecture in Practice* (4th ed.) | Bass, Clements, Kazman | Fundamentos, quality attributes, ATAM |
| *Fundamentals of Software Architecture* | Richards & Ford | Prático, padrões, soft skills |
| *Building Evolutionary Architectures* | Ford, Parsons, Kua | Fitness functions, evolução guiada |
| *Domain-Driven Design* | Eric Evans | DDD clássico |
| *Implementing Domain-Driven Design* | Vaughn Vernon | DDD prático |
| *Enterprise Integration Patterns* | Hohpe & Woolf | Messaging, EAI |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Dados, distribuição, consistência |
| *The Software Architect Elevator* | Gregor Hohpe | EA, comunicação, organização |
| *Team Topologies* | Skelton & Pais | Organização e arquitectura |
| *Continuous Architecture in Practice* | Murat Erder et al. | EA ágil |

---

## Recursos Online

### Documentação e Standards
- [C4 Model](https://c4model.com/) — Simon Brown
- [TOGAF — The Open Group](https://www.opengroup.org/togaf)
- [BPMN 2.0 Specification — OMG](https://www.omg.org/spec/BPMN/)
- [ISO/IEEE 42010](https://www.iso-architecture.org/) — Architecture description
- [ADR GitHub organization](https://adr.github.io/) — templates e exemplos

### Blogs e Engineering
- [Netflix Tech Blog](https://netflixtechblog.com/)
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/)
- [Martin Fowler's Blog](https://martinfowler.com/) — microservices, DDD, patterns
- [High Scalability](http://highscalability.com/) — casos de estudo de escala
- [InfoQ Architecture & Design](https://www.infoq.com/architecture-design/)

### Cursos e Certificações (referência)
- SEI Software Architecture Professional Certificate (Carnegie Mellon)
- AWS/Azure/GCP Solutions Architect certifications
- TOGAF Certification (The Open Group)

### Ferramentas
- **Modelação:** Structurizr, draw.io, PlantUML, Lucidchart
- **BPMN:** Camunda Modeler, bpmn.io
- **EA:** LeanIX, Ardoq, Sparx Enterprise Architect
- **Observabilidade:** Grafana, Prometheus, Jaeger, OpenTelemetry

---

## Exercícios de Consolidação

1. Explique como DDD bounded contexts se relacionam com microserviços.

2. Quando faria sentido combinar CQRS com Event Sourcing?

3. Descreva um dos seis pilares do Well-Architected Framework com duas best practices.

4. Que livro recomendaria para aprofundar quality attributes e ATAM?

5. O que é um Anti-Corruption Layer e quando usá-lo?

## Soluções

1. **Bounded context** define limite de um modelo de domínio coerente. **Microserviço** idealmente implementa um bounded context — ownership de dados, API e equipa alinhados ao domínio. Nem todo bounded context exige serviço separado (podem ser módulos num monolito); nem todo microserviço reflecte bounded context (anti-pattern "technical microservices"). DDD guia *onde* cortar; microserviços são *como* deployar.

2. **CQRS + Event Sourcing** quando: audit trail completo necessário (finanças, saúde); múltiplas projeções de leitura sobre mesmos dados; domínio rico com eventos significativos; necessidade de temporal queries ("estado em data X"). Exemplo: sistema de encomendas que guarda eventos e projeta views para cliente, armazém e analytics.

3. **Reliability (exemplo):** (1) testar recovery procedures regularmente (game days, chaos engineering); (2) usar múltiplas Availability Zones/regiões para workloads críticos; (3) implementar health checks e auto-healing; (4) definir quotas e monitorizar throttling. (Qualquer pilar com 2+ practices válidas.)

4. **Software Architecture in Practice** (Bass, Clements, Kazman) — referência académica e profissional para quality attributes, cenários, ATAM e documentação arquitectural. Alternativa mais acessível: *Fundamentals of Software Architecture* (Richards & Ford).

5. **Anti-Corruption Layer (ACL):** camada de tradução entre bounded context e sistema externo (legacy, third-party), convertendo modelos externos para modelos internos sem contaminar domínio. **Usar quando:** integrar sistema legacy com modelo diferente; consumir API externa instável; proteger domínio core de conceptos externos. Exemplo: adapter que traduz formato de cliente do ERP antigo para entidade Cliente do domínio.
