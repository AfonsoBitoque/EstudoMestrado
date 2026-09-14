# Módulo 10 — Tendências Emergentes em Arquitetura de Software

## Introdução

O panorama arquitectural evolui continuamente. Tendências emergentes — serverless, service mesh, inteligência artificial integrada na arquitectura, FinOps — reflectem respostas a novos requisitos de escala, custo, velocidade e inteligência. Este módulo apresenta estas tendências, os problemas que resolvem, trade-offs e implicações práticas para arquitectos.

## Serverless e Function-as-a-Service (FaaS)

**Serverless** não significa ausência de servidores — significa que o programador não gere servidores. O cloud provider aloca, escala e mantém infraestrutura automaticamente. Pagamento tipicamente por execução (invocações, duração, memória).

### Componentes

- **FaaS:** AWS Lambda, Azure Functions, Google Cloud Functions — funções event-triggered.
- **BaaS (Backend-as-a-Service):** serviços geridos (Auth, DB, Storage) consumidos via SDK.
- **Event sources:** API Gateway, queues, storage events, schedules.

### Benefícios

Escalabilidade automática (incluindo zero), redução de operações, custo proporcional ao uso, time-to-market rápido para workloads event-driven.

### Desafios

**Cold start:** latência na primeira invocação após idle. **Vendor lock-in:** APIs proprietárias. **Debugging e observabilidade:** fluxos distribuídos efémeros. **Limites:** timeout, memória, statelessness — funções não mantêm estado entre invocações. **Cost at scale:** workloads constantes podem ser mais caros que VMs reservadas.

### Quando Adoptar

APIs com tráfego irregular, processamento de ficheiros, ETL event-driven, backends mobile leves. Evitar para aplicações stateful de longa duração ou latência ultra-baixa consistente.

## Service Mesh

**Service mesh** é camada de infraestrutura dedicada à comunicação service-to-service em ambientes de microserviços. Implementada tipicamente via **sidecar proxies** (Envoy) injectados junto a cada serviço.

### Funcionalidades

- **Traffic management:** load balancing, retries, circuit breaking, canary deployments.
- **Security:** mTLS automático entre serviços, políticas de acesso.
- **Observability:** métricas, tracing e logs de comunicação inter-serviços.
- **Policy enforcement:** rate limiting, quotas.

### Plataformas

**Istio** (Kubernetes), **Linkerd** (mais leve), **Consul Connect**, AWS App Mesh.

### Benefícios vs. Desafios

**Benefícios:** observabilidade e segurança consistentes sem alterar código de cada serviço; control plane centralizado. **Desafios:** complexidade operacional adicional, overhead de latência (sidecar), curva de aprendizagem, debugging mais difícil.

Adoptar quando microserviços em escala com requisitos fortes de mTLS, canary e observabilidade distribuída — não para três serviços num cluster pequeno.

## Inteligência Artificial na Arquitetura

IA deixa de ser feature isolada e integra-se na arquitectura de múltiplas formas:

### Padrões Arquitecturais com IA

**ML as a Service:** APIs cloud (OpenAI, AWS SageMaker, Google Vertex AI) — integração via REST; arquitectura clássica com componente IA externo.

**Embedded ML:** modelos on-device (mobile, edge) — privacidade, latência, offline. TensorFlow Lite, Core ML.

**RAG (Retrieval-Augmented Generation):** LLM + vector database + pipeline de retrieval — arquitectura para Q&A sobre documentos corporativos.

**Feature stores:** componente arquitectural para servir features ML consistentes em training e inference.

**MLOps:** CI/CD estendido para modelos — versionamento, monitoring de drift, retraining pipelines.

### Implicações Arquitecturais

- **Latência e custo:** inferência LLM é cara e lenta — cache, batching, modelos menores para tarefas simples.
- **Data pipelines:** qualidade de dados afecta modelos — governance crítica.
- **Explainability e compliance:** decisões automatizadas requerem audit trail (GDPR Art. 22).
- **Fallbacks:** degradar gracefully quando modelo indisponível.

Arquitectos devem tratar componentes IA como qualquer serviço — SLAs, monitoring, versionamento — com atenção extra a não-determinismo e bias.

## FinOps — Gestão Financeira na Cloud

**FinOps** (Financial Operations) é prática cultural e técnica de gestão de custos cloud com responsabilidade partilhada entre engenharia, finanças e produto.

### Princípios

- **Visibility:** saber quem gasta o quê (tagging, cost allocation).
- **Optimization:** right-sizing, reserved instances, spot, eliminar waste.
- **Accountability:** equipas responsáveis pelo custo dos seus serviços.
- **Forecasting:** prever gastos vs. orçamento.

### Implicações Arquitecturais

Decisões arquitecturais têm custo directo:
- Microserviços com muitas invocações cross-AZ aumentam transfer costs.
- Serverless barato em baixo volume, caro em alto volume constante.
- Over-provisioning de réplicas vs. availability requirements.
- Data egress entre regiões cloud.

**FinOps-aware architecture:** incluir custo estimado em ADRs; dashboards de custo por serviço; auto-scaling com limites; revisão periódica de recursos idle.

### Ferramentas

AWS Cost Explorer, Azure Cost Management, CloudHealth, Kubecost (Kubernetes), Infracost (custo em CI/CD).

## Outras Tendências Relevantes

**Platform Engineering:** equipas internas constroem "Internal Developer Platforms" (IDP) — golden paths, self-service, reduzindo carga cognitiva. Backstage, Crossplane.

**WebAssembly (Wasm):** módulos portáveis para edge computing e plugins seguros.

**Zero Trust Architecture:** nunca confiar, sempre verificar — identidade, micro-segmentation, mTLS.

**Green Software / Sustainable Architecture:** optimizar carbon footprint — regiões com energia renovável, efficient code, right-sizing.

**Event-driven maturity:** event mesh, event catalog, schema registry (AsyncAPI, Kafka Schema Registry).

## Avaliar Tendências Critically

Nem toda tendência é adequada a todo contexto. Framework de avaliação:
1. Que problema resolve concretamente no **nosso** contexto?
2. Qual a maturidade da equipa e organização?
3. Qual o custo total (licenças, formação, operação)?
4. Existe lock-in ou path de saída?
5. Métricas de sucesso definidas?

Anti-padrão: adoptar serverless, mesh e LLM simultaneamente num MVP porque "são tendências".

## Exercícios

1. O que é serverless e quais dois desafios principais associados?

2. Explique o papel de um service mesh e quando justifica a sua adopção.

3. Descreva a arquitectura RAG em componentes principais.

4. Como FinOps influencia decisões arquitecturais? Dê dois exemplos concretos.

5. Compare custo de serverless vs. VMs para workload com tráfego constante 24/7.

6. Quais implicações arquitecturais de integrar LLM num chatbot de suporte ao cliente?

7. O que é Platform Engineering e como se relaciona com arquitectura de software?

8. Uma empresa adopta Istio num cluster com 4 microserviços e equipa junior. Avalie criticamente esta decisão.

## Soluções

1. **Serverless:** modelo onde developer deploya funções/código sem gerir servidores; provider gere escala e infra; pagamento por uso. **Desafios:** cold start (latência inicial); vendor lock-in (APIs proprietárias). Outros válidos: debugging complexo, limites de execução, statelessness.

2. **Service mesh:** camada infra para comunicação inter-serviços via sidecars, oferecendo mTLS, traffic management, observabilidade e policies sem alterar código. **Justifica adopção:** dezenas/centenas de microserviços, requisitos fortes de segurança zero-trust entre serviços, canary deployments frequentes, observabilidade distribuída madura. Não justifica para poucos serviços.

3. **RAG:** (1) **Ingestion pipeline** — documentos chunkados e embedados; (2) **Vector database** — armazena embeddings (Pinecone, pgvector); (3) **Retrieval** — query embedada, busca chunks relevantes; (4) **LLM** — recebe query + contexto retrieved, gera resposta; (5) **API/Gateway** — expõe ao cliente. Opcional: reranker, cache, feedback loop.

4. **FinOps influencia arquitectura** tornando custo critério explícito. **Exemplos:** (1) escolher região cloud com menor egress para utilizadores target; (2) preferir async/event-driven vs. chamadas síncronas cross-region que cobram transfer; (3) auto-scaling com max replicas alinhado a budget; (4) ADR documenta custo estimado mensal de cada alternativa.

5. **Serverless:** paga por invocação + duração — tráfego constante 24/7 gera invocações contínuas, potencialmente mais caro que VM reservada optimizada. **VMs reservadas/savings plans:** custo previsível, mais baixo para baseline constante. Serverless vence em tráfego esporádico ou imprevisível; VMs vencem em workload estável e previsível. FinOps recomenda modelar ambos.

6. **Implicações LLM:** latência variável — timeout e indicadores de loading; custo por token — cache de respostas frequentes, limitar contexto; fallback para FAQ estático se LLM down; guardrails contra respostas inadequadas; logging para audit sem expor PII; rate limiting; monitorização de qualidade (feedback, escalation to human); compliance GDPR se dados pessoais no contexto.

7. **Platform Engineering:** equipa constrói plataforma interna self-service (IDP) com golden paths, templates, catálogo de serviços — acelera developers e standardiza práticas. **Relação com arquitectura:** implementa decisões arquitecturais (patterns aprovados, scaffolding de microserviço, pipelines CI/CD) como produto interno; arquitectos definem standards, platform engineers productizam-nos.

8. **Avaliação crítica: provavelmente inadequado.** Istio adiciona complexidade significativa (control plane, sidecars, configuração) desproporcional para 4 serviços — overhead operacional, latência, curva de aprendizagem alta para equipa junior. Alternativas: observabilidade via OpenTelemetry + library patterns; mTLS via cert-manager mais simples; reavaliar mesh quando escala justificar. Risco: equipa gasta tempo em infra em vez de produto; debugging torna-se nightmare. Tendência ≠ necessidade no contexto.
