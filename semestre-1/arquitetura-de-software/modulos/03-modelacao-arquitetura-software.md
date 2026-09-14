# Módulo 03 — Modelação de Arquitetura de Software

## Introdução

Modelar arquitecturas permite comunicar decisões, analisar alternativas e preservar conhecimento ao longo do ciclo de vida do sistema. Sem modelos adequados, a arquitectura existe apenas na cabeça de alguns indivíduos — risco enorme para manutenção e evolução. Este módulo aborda o modelo C4, diagramas UML de deployment, Architecture Decision Records (ADRs) e o conceito de views and viewpoints.

## Porque Modelar Arquitecturas?

Modelos arquitecturais servem múltiplos propósitos: comunicação entre stakeholders técnicos e não técnicos, documentação para onboarding, base para avaliação (ATAM, revisões), conformidade com standards e suporte à evolução. Um bom modelo é **justo suficiente** — detalhe adequado ao público e ao propósito, sem burocracia excessiva.

Princípios úteis: um diagrama deve ter uma mensagem clara; usar notação consistente; incluir legendas; datar e versionar; e distinguir o que está implementado do que é planeado.

## Modelo C4

O **C4 Model** (Simon Brown) propõe quatro níveis de zoom hierárquicos, do contexto geral ao código:

### Nível 1 — System Context
Mostra o sistema como caixa central, utilizadores (personas) e sistemas externos com que interage. Responde: "Quem usa o sistema e com que se integra?" Público: todos os stakeholders.

### Nível 2 — Container
Decompõe o sistema em **containers** — aplicações, bases de dados, filas, filesystems — unidades deployáveis ou executáveis. Mostra tecnologias e comunicação entre containers. Responde: "De que partes executáveis se compõe o sistema?" Público: equipa técnica e arquitectos.

### Nível 3 — Component
Detalha um container individual em **componentes** — agrupamentos lógicos de código (controllers, services, repositories). Responde: "Como está organizado este serviço internamente?" Público: developers da equipa.

### Nível 4 — Code
Diagramas UML de classes ou equivalentes para componentes específicos. Opcional e gerado frequentemente a partir do IDE. Responde: "Como implementar esta classe?"

A força do C4 está na hierarquia: cada nível adiciona detalhe sem sobrecarregar. Para a maioria dos projectos, os níveis 1 e 2 são os mais valiosos para documentação persistente.

**Exemplo conceptual:** Sistema "Loja Online" (Context) → API Gateway, Serviço de Catálogo, Serviço de Pagamentos, PostgreSQL, Redis (Containers) → dentro do Serviço de Catálogo: ProductController, ProductService, ProductRepository (Components).

## Views and Viewpoints (ISO/IEEE 42010)

O standard **ISO/IEEE 42010** define arquitectura como conjunto de **views** sobre um sistema, cada uma descrita por um **viewpoint** que especifica stakeholders, preocupações e notações.

Conceitos-chave:
- **Viewpoint:** template/metodologia para construir views (ex.: viewpoint de deployment, de segurança).
- **View:** instância concreta de um viewpoint para um sistema específico.
- **Stakeholder:** quem tem preocupações a endereçar.
- **Concern:** interesse ou requisito (desempenho, segurança, modularidade).

Views clássicas (Philippe Kruchten, 4+1):
1. **Logical view** — funcionalidade e abstrações de domínio.
2. **Process view** — concorrência, threads, fluxos.
3. **Development view** — organização do código e módulos.
4. **Physical view** — deployment em hardware/nós.
5. **Scenarios (+1)** — casos de uso que validam coerência entre views.

A ideia central: **não existe um diagrama único** que sirva todos. Diferentes stakeholders necessitam de perspectivas diferentes sobre o mesmo sistema.

## UML — Diagrama de Deployment

O **diagrama de deployment** UML modela a arquitectura física: nós (servidores, dispositivos, VMs, containers), artefactos (JARs, executáveis, ficheiros) e ligações de comunicação.

Elementos principais:
- **Node:** ambiente de execução (ex.: «Servidor Web», «AWS EC2», «Kubernetes Pod»).
- **Artifact:** peça de software deployada num nó (ex.: «api-service.jar»).
- **Communication path:** ligação entre nós (HTTP, JDBC, messaging).
- **Device:** hardware físico (opcional em cloud).

Utilização: planear infraestrutura, documentar ambientes (dev, staging, prod), analisar pontos únicos de falha, comunicar com operações.

Exemplo: nó «Load Balancer» liga a nós «App Server 1» e «App Server 2», cada um com artefacto «webapp.war»; ambos ligam a nó «Database Server» com artefacto «PostgreSQL».

## Architecture Decision Records (ADRs)

**ADRs** documentam decisões arquitecturais significativas de forma estruturada e versionada (tipicamente em Markdown no repositório).

Estrutura típica (Michael Nygard):
1. **Title** — identificador curto.
2. **Status** — proposed, accepted, deprecated, superseded.
3. **Context** — forças e constraints que motivam a decisão.
4. **Decision** — o que foi decidido.
5. **Consequences** — impactos positivos, negativos e neutros.

Exemplo: ADR-007 "Usar PostgreSQL como base de dados principal" — Context: necessidade de transacções ACID e queries complexas; Decision: PostgreSQL; Consequences: (+) maturidade, ACID; (-) escalabilidade horizontal de escrita limitada vs. NoSQL.

Benefícios: rastreabilidade do "porquê", onboarding mais rápido, evita repetir debates já resolvidos, suporta revisão quando contexto muda.

Boas práticas: ADRs imutáveis (alterar status, não apagar histórico), um ADR por decisão significativa, linguagem clara, referência cruzada entre ADRs.

## Integração das Técnicas

Num projecto típico:
- **C4 L1/L2** para visão geral e comunicação.
- **Diagrama de deployment** para infraestrutura e operações.
- **ADRs** para decisões controversas ou irreversíveis.
- **Views adicionais** (segurança, dados) conforme preocupações dos stakeholders.

Estas ferramentas complementam-se. O C4 não substitui ADRs (C4 mostra estrutura; ADR explica escolha). Deployment complementa C4 L2 (containers abstractos ganham nós concretos).

## Exercícios

1. Explique os quatro níveis do modelo C4 e indique o público-alvo de cada um.

2. Descreva um diagrama de System Context para um sistema de telemedicina (consultas online). Inclua atores e sistemas externos.

3. Qual a diferença entre viewpoint e view segundo ISO 42010? Dê um exemplo.

4. Redija um ADR fictício para a decisão "Adoptar API REST em vez de GraphQL" num projecto de catálogo de produtos.

5. Quando usar diagrama C4 Container vs. diagrama UML de deployment?

6. Liste as cinco views do modelo 4+1 de Kruchten e a preocupação principal de cada uma.

7. Porque é problemático ter um único diagrama arquitectural "completo" para todo o projecto?

8. Que informação mínima deve constar num diagrama C4 Container para ser útil a uma equipa de desenvolvimento?

## Soluções

1. **L1 System Context:** sistema, utilizadores e externos — todos os stakeholders. **L2 Container:** aplicações, BD, filas — equipa técnica e arquitectos. **L3 Component:** módulos internos de um container — developers. **L4 Code:** classes e interfaces — developers implementadores. Cada nível aumenta detalhe e reduz audiência.

2. **Actores:** Paciente, Médico, Administrador. **Sistema central:** Plataforma de Telemedicina. **Sistemas externos:** Sistema de Prescrição Electrónica, Gateway de Pagamentos, Serviço de Vídeo (WebRTC), Sistema de Agendamento Hospitalar, Serviço de Notificações (SMS/email). Ligações: Paciente/Médico usam plataforma; plataforma integra prescrição, pagamentos, vídeo e agendamento.

3. **Viewpoint** é a especificação/template (metodologia, notação, stakeholders alvo, preocupações endereçadas). **View** é a instância concreta aplicada a um sistema. Exemplo: viewpoint de segurança define que se modelam zonas de confiança e fluxos de autenticação; a view de segurança do sistema bancário X mostra DMZ, firewalls e OAuth entre frontend e API.

4. **ADR-003: Adoptar REST em vez de GraphQL** — Status: Accepted. Context: catálogo com estrutura estável, equipa familiarizada com REST, clientes móveis e web; GraphQL ofereceria flexibilidade de queries mas aumentaria complexidade. Decision: API REST com recursos `/products`, `/categories`; paginação via query params. Consequences: (+) simplicidade, cache HTTP, ferramentas maduras; (-) over-fetching em ecrãs complexos, múltiplos endpoints para dashboards; mitigação futura: BFF se necessário.

5. **C4 Container:** visão lógica/deployment abstracto — que serviços existem e como comunicam, independente de infra concreta. **UML Deployment:** infra física/virtual — servidores, regiões cloud, replicas, load balancers, ligações de rede. Usar C4 para design e comunicação geral; deployment para implementação operacional e capacidade.

6. **Logical:** funcionalidade e domínio. **Process:** concorrência e performance runtime. **Development:** organização de código e módulos. **Physical:** mapeamento para hardware/nós. **Scenarios (+1):** casos de uso que validam coerência entre as outras views.

7. Diferentes stakeholders têm preocupações distintas — um diagrama "completo" ou fica ilegível (demasiado detalhe) ou omite informação crítica para alguns (detalhe insuficiente). Viola o princípio de separation of concerns na documentação. Views especializadas permitem foco e clareza; o diagrama único torna-se rapidamente obsoleto e difícil de manter.

8. Nome de cada container, tecnologia (ex.: «Spring Boot», «PostgreSQL 15»), responsabilidade em poucas palavras, protocolos de comunicação entre containers (HTTPS, JDBC, Kafka), e opcionalmente diagrama de contexto simplificado para orientação. Deve ser possível inferir boundaries de deploy e dependências principais.
