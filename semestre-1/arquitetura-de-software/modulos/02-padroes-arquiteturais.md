# Módulo 02 — Padrões Arquiteturais

## Introdução

Padrões arquiteturais são soluções recorrentes para problemas estruturais comuns em sistemas de software. Não são receitas a copiar cegamente, mas templates que capturam experiência acumulada da indústria. Compreender os principais padrões — layered, microservices, event-driven — e os trade-offs entre monolitos e sistemas distribuídos é essencial para tomar decisões informadas.

## Arquitetura em Camadas (Layered Architecture)

A arquitetura em camadas organiza o sistema em níveis horizontais, cada um com responsabilidade específica. O fluxo típico segue: **Apresentação → Negócio (Application/Domain) → Persistência → Base de Dados**.

A camada de apresentação trata da interface com utilizadores ou APIs externas. A camada de negócio contém regras de domínio e orquestração. A camada de persistência abstrai acesso a dados. Regra fundamental: dependências fluem para baixo — a apresentação depende do negócio, nunca o inverso.

**Vantagens:** simplicidade conceptual, separação clara de responsabilidades, adequada para equipas pequenas e projectos com domínio coeso. **Desvantagens:** risco de "camadas anémicas" que apenas passam dados, dificuldade em escalar partes independentes, acoplamento vertical se mal implementado.

Variantes incluem **hexagonal (ports and adapters)** e **clean architecture**, que invertem a dependência colocando o domínio no centro e tratando infraestrutura como plugável.

## Monolito vs. Sistemas Distribuídos

**Monolito** é uma aplicação deployada como unidade única. Todo o código corre no mesmo processo (ou conjunto de processos idênticos). Pode ser bem estruturado internamente (monolito modular) com boundaries claros entre módulos.

**Sistema distribuído** decompõe funcionalidade em múltiplos serviços ou componentes que comunicam via rede. Cada parte pode ser desenvolvida, deployada e escalada independentemente.

| Aspeto | Monolito | Distribuído |
|--------|----------|-------------|
| Complexidade operacional | Baixa | Alta |
| Escalabilidade | Vertical ou réplicas completas | Granular por serviço |
| Consistência de dados | Transacções ACID simples | Eventual consistency, sagas |
| Time-to-market inicial | Geralmente mais rápido | Mais lento (infra, contratos) |
| Acoplamento | Lógico (módulos) | Rede + contratos de API |
| Debugging | Mais simples | Requer tracing distribuído |

A escolha não é binária permanente. Estratégias como **monolito modular com extração gradual** permitem evoluir para distribuído quando o contexto o justifica.

## Microserviços

Microserviços decompõem o sistema em serviços pequenos, autónomos, alinhados a capacidades de negócio. Cada serviço possui base de dados própria (idealmente), deploy independente e equipa responsável.

**Princípios:** bounded contexts (DDD), comunicação via APIs bem definidas, descentralização de dados e governança, automação de infraestrutura (CI/CD, containers, orquestração).

**Benefícios:** escalabilidade selectiva, tecnologias heterogéneas por serviço, resiliência por isolamento de falhas, autonomia de equipas (modelo Conway).

**Desafios:** complexidade de rede (latência, partições), consistência eventual, testes de integração difíceis, overhead operacional (service discovery, monitoring, deployment), risco de "distributed monolith" se serviços forem demasiado acoplados.

Microserviços fazem sentido com equipas maduras, domínios claramente separados, necessidade de escala diferenciada e investimento em plataforma (Kubernetes, observabilidade).

## Arquitetura Orientada a Eventos (Event-Driven Architecture)

EDA baseia-se na produção, detecção e consumo de **eventos** — notificações de que algo aconteceu no sistema ("PedidoCriado", "PagamentoConfirmado"). Componentes publicam eventos sem conhecer consumidores; consumidores reagem assincronamente.

Componentes típicos: **event producers**, **event brokers** (Kafka, RabbitMQ, AWS EventBridge), **event consumers** e **event stores**.

**Vantagens:** desacoplamento temporal e espacial, escalabilidade via processamento assíncrono, auditabilidade natural (log de eventos), extensibilidade (novos consumidores sem alterar produtores).

**Desvantagens:** debugging complexo, garantias de ordem e entrega exigem design cuidadoso, consistência eventual, necessidade de idempotência nos consumidores.

EDA combina frequentemente com microserviços (comunicação assíncrona entre serviços) e com padrões como **CQRS** e **Event Sourcing** (ver matéria extra).

## Outros Padrões Relevantes

**Cliente-Servidor:** separação entre cliente (UI) e servidor (lógica e dados). Base da web moderna.

**Pipe-and-Filter:** fluxo de dados através de componentes de processamento sequencial. Comum em ETL e streaming.

**Space-Based Architecture:** processamento distribuído em memória para alta performance. Usado em trading e sistemas de baixa latência.

**Service-Oriented Architecture (SOA):** precursor dos microserviços, com serviços empresariais e frequentemente ESB (Enterprise Service Bus). Serviços tipicamente maiores e mais acoplados via barramento central.

## Trade-offs e Decisão

Nenhum padrão é universalmente superior. A decisão deve considerar:

1. **Contexto organizacional:** tamanho e distribuição das equipas, maturidade DevOps.
2. **Requisitos de qualidade:** quais atributos são críticos?
3. **Domínio de negócio:** há bounded contexts naturais?
4. **Restrições:** orçamento, prazos, competências existentes.
5. **Evolução prevista:** o sistema crescerá em funcionalidade, carga ou equipas?

Anti-padrão comum: adoptar microserviços numa startup com cinco developers porque "empresas grandes usam". O resultado frequentemente é complexidade prematura sem benefícios proporcionais.

## Exercícios

1. Descreva as três camadas principais de uma arquitetura em camadas e a direcção das dependências entre elas.

2. Um sistema de gestão académica universitária tem 15 developers e domínios distintos (matrículas, avaliações, financeiro). Monolito ou microserviços? Justifique.

3. Explique o que é um "distributed monolith" e como evitá-lo.

4. Compare comunicação síncrona (REST) e assíncrona (eventos) entre dois serviços num cenário de processamento de encomendas.

5. Liste três vantagens e três desvantagens da arquitectura orientada a eventos.

6. Um e-commerce em fase MVP com prazo de três meses e equipa de quatro pessoas: que padrão arquitectural recomendaria e porquê?

7. O que significa "cada microserviço com a sua base de dados" e quais problemas resolve e cria?

8. Descreva uma estratégia de migração de monolito para microserviços sem parar o negócio (Strangler Fig Pattern).

## Soluções

1. **Apresentação** (UI, controllers, API gateways), **Negócio** (regras de domínio, casos de uso), **Persistência** (repositórios, ORM, acesso a BD). Dependências fluem de cima para baixo: Apresentação → Negócio → Persistência → BD. Camadas inferiores não conhecem superiores.

2. **Microserviços (ou monolito modular com extração futura)** são plausíveis. Com 15 developers e domínios distintos, microserviços permitem equipas autónomas por domínio (matrículas, avaliações, financeiro). Porém, se a maturidade operacional for baixa, um **monolito modular** com boundaries claros entre módulos pode ser mais pragmático inicialmente, extraindo serviços quando a separação estiver estável. A decisão depende da maturidade DevOps e da necessidade real de deploy independente.

3. **Distributed monolith:** serviços separados fisicamente mas logicamente acoplados — alterar um exige alterar outros, deploys coordenados, partilham base de dados ou chamadas síncronas em cadeia. **Evitar:** definir bounded contexts claros, bases de dados separadas, comunicação assíncrona quando possível, contratos de API versionados, evitar transacções distribuídas desnecessárias, e extrair serviços apenas quando o boundary de domínio estiver maduro.

4. **REST síncrono:** cliente chama serviço de encomendas que chama serviço de pagamento e espera resposta. Simples, consistência imediata, mas acoplamento temporal — se pagamento estiver lento ou indisponível, encomenda bloqueia. **Eventos assíncronos:** encomenda publica `EncomendaCriada`; serviço de pagamento consome e processa; serviço de envio consome `PagamentoConfirmado`. Desacoplamento, melhor resiliência, mas consistência eventual — utilizador pode ver "encomenda criada" antes de "pagamento confirmado". Para checkout, combinação comum: síncrono para pagamento (feedback imediato) + eventos para fulfillment.

5. **Vantagens:** desacoplamento entre produtores e consumidores, escalabilidade independente de consumidores, extensibilidade (adicionar consumidor sem alterar produtor), audit trail natural. **Desvantagens:** debugging e rastreio difíceis, complexidade de garantias (ordem, exactly-once delivery), consistência eventual, necessidade de handlers idempotentes, infraestrutura adicional (broker).

6. **Monolito modular em camadas.** Prazo curto, equipa pequena, MVP — microserviços adicionam overhead operacional desproporcional. Um monolito bem estruturado (camadas, módulos por domínio) permite entrega rápida e refactor posterior. Investir em testes automatizados e boundaries internos claros facilita eventual decomposição.

7. Significa que cada microserviço gere a sua persistência sem partilhar tabelas com outros serviços. **Resolve:** acoplamento de dados, impedindo que alterações num serviço quebrem outros; permite escolher tecnologia de BD adequada por serviço; reforça bounded contexts. **Cria:** necessidade de duplicar dados (denormalização), queries cross-service complexas, transacções distribuídas ou sagas para consistência, desafios de sincronização.

8. **Strangler Fig Pattern:** construir nova funcionalidade (ou versão) como serviços/módulos paralelos; encaminhar tráfego gradualmente do monolito para o novo via API gateway ou routing; funcionalidades migradas uma a uma; monolito "encolhe" até ser descomissionado. Permite migração incremental, rollback por funcionalidade, e negócio continua operacional durante transição. Exemplo: extrair primeiro módulo de notificações (baixo risco), depois catálogo, por último checkout.
