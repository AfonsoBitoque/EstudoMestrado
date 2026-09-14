# Módulo 08 — Interligação de Arquiteturas

## Introdução

Interligar arquitecturas significa estabelecer correspondências explícitas entre diferentes níveis de abstracção: processos de negócio, entidades de informação, componentes software e infraestrutura. Sem esta ligação, negócio e TI falam línguas diferentes, projectos desalinhados proliferam e a rastreabilidade de requisitos perde-se. Este módulo foca o mapeamento de processos de negócio para componentes de software e técnicas de interligação entre arquitectura empresarial e arquitectura de solução.

## Porque Interligar Arquiteturas?

Organizações possuem múltiplas "lentes" sobre o mesmo sistema:
- Gestor de negócio vê processos e KPIs.
- Arquitecto empresarial vê capabilities e portfolio.
- Arquitecto de software vê serviços e APIs.
- Developer vê classes e bases de dados.

**Interligação** ( também designada **architecture traceability** ou **mapping**) conecta estas lentes, permitindo:
- Impact analysis: "Se alterarmos este processo, que sistemas afecta?"
- Coverage analysis: "Todos os passos do processo estão automatizados?"
- Gap identification: "Que processo não tem suporte software?"
- Conformidade: "Implementação respeita modelo de EA?"

## Mapeamento Processo → Componente

O mapeamento mais operacional para arquitectos de software liga elementos BPMN a componentes arquitecturais.

### Correspondências Típicas

| Elemento BPMN | Componente Software |
|---------------|-------------------|
| Task automatizada | Serviço, API endpoint, função |
| Task humana | Aplicação web/mobile (UI), inbox BPMS |
| Gateway (decisão) | Rules engine, lógica no serviço, workflow engine |
| Evento de mensagem | Message queue consumer/producer |
| Evento timer | Scheduler, cron job, workflow timer |
| Sub-processo | Composição de serviços ou módulo |
| Data Object | Entidade de domínio, DTO, schema |

### Abordagem Prática

1. **Seleccionar processo** prioritário (value stream crítico).
2. **Decompor em tasks** com indicação manual vs. automatizada.
3. **Identificar entidades** manipuladas (data objects).
4. **Mapear cada task** para componente existente ou a construir.
5. **Documentar interfaces** — que API, que evento, que ecrã.
6. **Validar cobertura** — todos os caminhos do processo têm suporte?
7. **Identificar gaps** — tasks sem componente, componentes órfãos.

### Exemplo: Processo "Fulfillment de Encomenda"

| Task BPMN | Componente | Interface |
|-----------|------------|-----------|
| Validar Stock | InventoryService | GET /stock/{sku} |
| Processar Pagamento | PaymentService | POST /payments |
| Reservar Stock | InventoryService | POST /stock/reserve |
| Notificar Armazém | Event: OrderPaid | Kafka topic |
| Gerar Guia Transporte | ShippingService | (consome evento) |
| Actualizar Estado | OrderService | PATCH /orders/{id} |

Diagrama de interligação pode ser matriz (processo × componente) ou overlay BPMN com anotações de serviço.

## Mapeamento Entidade → Persistência → Serviço

Entidades de informação empresariais mapeiam para:
- **Bounded context** (domínio DDD).
- **Serviço responsável** (owner do dado).
- **Armazenamento** (schema, tabela, documento).
- **APIs e eventos** de acesso.

Exemplo: entidade **Cliente** → bounded context "Customer Management" → CustomerService → PostgreSQL schema `customers` → API REST + evento `CustomerUpdated`.

Master data partilhado exige decisão explícita: réplica read-only vs. API lookup vs. event-driven sync.

## Interligação EA ↔ Solução

### Capability → Application → Component

**Capability** "Gestão de Encomendas" (EA) → **Application** "Order Management System" (portfolio) → **Components** OrderService, OrderUI, OrderDB (software).

### Value Stream → System Landscape

Value stream "Cliente recebe produto" atravessa múltiplas applications; diagrama de interligação mostra sequência de sistemas e handoffs.

### Matrizes de Rastreabilidade

**CRUD matrix:** entidades × processos (Create/Read/Update/Delete) — identifica quem manipula o quê.

**Application interaction matrix:** quais aplicações comunicam entre si.

**Process-Application matrix:** quais processos são suportados por quais aplicações.

Ferramentas EA (LeanIX, Ardoq, Sparx EA) automatizam parte destas matrizes; em projectos menores, spreadsheets ou Markdown no repositório bastam.

## Padrões de Integração na Interligação

Quando processos atravessam múltiplos componentes:

**Síncrono (REST/gRPC):** task requer resposta imediata — validação, cálculo.

**Assíncrono (events):** task desencadeia trabalho posterior — notificações, fulfillment.

**Orchestration (BPMS):** engine central coordena chamadas — processos longos com human tasks.

**Choreography (events):** serviços reagem independentemente — desacoplamento máximo.

A escolha afecta diagrama de interligação: orchestration centraliza linhas; choreography dispersa eventos.

## Desafios e Anti-padrões

**Processo vs. implementação divergentes:** BPMN documentado não reflecte sistema real — validar com walkthroughs.

**Componentes monolíticos opacos:** impossível mapear tasks granularmente — refactor ou aceitar mapeamento grosso.

**Over-mapping:** documentar cada task de processos irrelevantes — focar processos críticos.

**Falta de manutenção:** mapeamento feito uma vez no projecto inicial e nunca actualizado.

## Exercícios

1. O que significa "interligar arquitecturas" e que benefícios traz?

2. Complete o mapeamento: Task BPMN "Enviar Email de Confirmação" → ? (componente e interface)

3. Descreva os passos de uma abordagem prática para mapear um processo de negócio a componentes software.

4. O que é uma matriz CRUD e como a utiliza um arquitecto?

5. Diferencie orchestration e choreography no contexto de interligação processo-componente.

6. Entidade "Produto" é master data partilhada por Catálogo, Encomendas e Warehouse. Que decisões arquitecturais de interligação são necessárias?

7. Um gap analysis revela que o passo "Aprovação Manual de Crédito" no BPMN não tem componente associado. Que acções tomar?

8. Como interligar uma capability de EA ("Gestão de Clientes") com microserviços concretos?

## Soluções

1. **Interligar** estabelece correspondências explícitas entre modelos de diferentes níveis (negócio, EA, software). **Benefícios:** impact analysis, rastreabilidade de requisitos, identificação de gaps, conformidade com EA, comunicação entre stakeholders, e suporte a evolução coerente.

2. **Componente:** NotificationService (ou EmailService). **Interface:** POST /notifications/email com payload {to, template, data} ou publicação evento `OrderConfirmed` consumido por NotificationService que envia email. Alternativa: serviço SaaS (SendGrid) invocado via adapter.

3. **Passos:** (1) seleccionar processo prioritário; (2) decompor BPMN em tasks classificando manual/automático; (3) identificar entidades (data objects); (4) mapear cada task a componente existente ou novo; (5) definir interfaces (API, evento, UI); (6) validar cobertura de todos os caminhos; (7) documentar gaps e plano de acção.

4. **Matriz CRUD:** linhas = entidades, colunas = processos ou sistemas, células = C/R/U/D indicando operação. Arquitecto identifica: quem cria Cliente? quem lê Encomenda? detecta duplicação, gaps (ninguém faz Update de Stock), e violações de ownership (dois sistemas fazem Create de Cliente).

5. **Orchestration:** engine BPMS ou serviço orquestrador coordena sequência de chamadas — interligação centralizada, visibilidade do fluxo, ponto único de falha. **Choreography:** cada serviço publica/consome eventos autonomamente — interligação dispersa, desacoplamento, mais difícil rastrear fluxo global. Mapeamento BPMN: orchestration = um componente "ProcessManager" liga a todos; choreography = linhas de eventos entre serviços.

6. **Decisões:** (1) owner do master — qual serviço é fonte autoritativa (CatalogService); (2) outros serviços acedem via API ou réplica local; (3) sincronização — eventos `ProductCreated/Updated` para réplicas; (4) identificador global (SKU); (5) consistência eventual aceite ou lookup síncrono para preço/stock crítico; (6) evitar updates directos cross-service na BD.

7. **Acções:** (1) confirmar com negócio se passo ainda é necessário; (2) se sim, definir componente — inbox de aprovação (UI + workflow), integração com BPMS, ou task queue para analistas; (3) estimar esforço e priorizar; (4) actualizar mapeamento após implementação; (5) se passo obsoleto, actualizar BPMN e remover do fluxo.

8. **Capability** "Gestão de Clientes" decompõe em: **Application** CRM no portfolio EA → **Microserviços:** CustomerService (CRUD, perfil), CustomerAuthService (autenticação), CustomerNotificationService (comunicações) → cada um com APIs, BD e eventos documentados. Matriz capability-to-service mantida no repositório EA ou ADRs. Bounded context DDD alinha com capability.
