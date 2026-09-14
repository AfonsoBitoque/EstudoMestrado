# Módulo 05 — Processos de Negócio e Informação

## Introdução

Sistemas de software não existem isoladamente — executam e suportam **processos de negócio** sobre **informação** estruturada e governada. Compreender BPM (Business Process Management), arquitectura de informação e data governance é fundamental para arquitectos que devem alinhar soluções técnicas com a realidade operacional das organizações. Este módulo explora estes três pilares.

## Business Process Management (BPM)

**BPM** é a disciplina que modela, implementa, executa, monitoriza e optimiza processos de negócio de forma sistemática e contínua. Um processo de negócio é um conjunto coordenado de actividades que transforma inputs em outputs de valor para clientes internos ou externos.

### Ciclo de Vida BPM

1. **Design:** modelar processos (BPMN), identificar actividades, decisões, participantes.
2. **Modeling:** formalizar com notação standard, validar com stakeholders.
3. **Execution:** implementar em BPMS (Business Process Management Suite) ou orquestrar via código/microserviços.
4. **Monitoring:** medir KPIs — tempo de ciclo, custo, taxa de erro, bottlenecks.
5. **Optimization:** analisar dados, redesenhar processos (reengenharia), iterar.

### BPM vs. Automação Simples

Automatizar uma tarefa (script, RPA) não é BPM completo. BPM abrange a **orquestração end-to-end** do processo, incluindo actividades humanas (aprovaciones), regras de negócio, escalonamentos e visibilidade gerencial. BPMS como Camunda, Activiti ou IBM BPM fornecem engines de workflow, modeladores visuais e dashboards.

### Relação com Arquitectura de Software

Processos de negócio definem **requisitos operacionais** que a arquitectura deve suportar: quais serviços invocar, em que ordem, com que SLAs, que dados trocar. Mapear processos para componentes software (módulo 08) é passo crítico. Processos mal compreendidos levam a sistemas que automatizam ineficiências ("paving the cow path").

## Arquitetura de Informação

**Arquitectura de Informação (Information Architecture — IA)** organiza, categoriza e rotula informação para torná-la encontrável, compreensível e utilizável. Origina-se em UX/web design mas estende-se ao contexto empresarial.

### Componentes da IA

**Organisation systems:** como a informação se agrupa (hierarquias, categorias, taxonomias). Exemplo: produtos por departamento vs. por tipo.

**Labelling systems:** nomenclatura consistente — termos que utilizadores compreendem. Exemplo: "Cliente" vs. "Account" vs. "User" — unificação semântica.

**Navigation systems:** como utilizadores (humanos ou sistemas) localizam informação — menus, breadcrumbs, APIs de descoberta.

**Search systems:** mecanismos de pesquisa e filtros.

**Metadata:** dados sobre dados — tags, classificações, proveniência.

No contexto empresarial, IA alinha-se com **modelos de dados conceptuais** e **ontologias** — vocabulario partilhado entre negócio e TI. Um bom modelo de entidades empresariais (módulo 07) é fundamento da arquitectura de informação.

### IA e Integração

Organizações com sistemas legados sofrem frequentemente de **silos semânticos** — o mesmo conceito designado diferentemente em ERP, CRM e data warehouse. IA empresarial, combinada com glossários de negócio e master data management, resolve ambiguidades e facilita integração.

## Data Governance

**Data Governance** é o conjunto de políticas, roles, processos e standards que garantem qualidade, segurança, privacidade e uso adequado dos dados organizacionais.

### Pilares

**Data Quality:** exactidão, completude, consistência, actualidade. Métricas e processos de cleansing.

**Data Ownership:** data owners (negócio) e data stewards (operacional) responsáveis por domínios de dados.

**Data Security & Privacy:** controlos de acesso, encriptação, conformidade (GDPR, LGPD), classificação de sensibilidade.

**Data Lifecycle:** criação, uso, arquivo, eliminação — retenção conforme regulamentação.

**Master Data Management (MDM):** fonte única de verdade para entidades core (cliente, produto, fornecedor) sincronizada entre sistemas.

### Frameworks de Referência

**DAMA-DMBOK** (Data Management Body of Knowledge): 11 áreas de conhecimento incluindo governance, architecture, quality, security.

**DCAM** (Enterprise Data Management Council): modelo de capacidade de data management.

### Relação com EA e Arquitectura de Software

Data governance traduz-se em decisões arquitecturais: onde persistir dados master, como replicar, que APIs expor, que eventos publicar quando dados mudam, como auditar acessos. Arquitectos devem colaborar com data stewards — ignorar governance leva a multas regulatórias, inconsistência operacional e projectos de integração intermináveis.

## Integração dos Três Domínios

```
Processos de Negócio → consomem e produzem → Informação
                              ↓
                    governada por Data Governance
                              ↓
                    implementada em Arquitectura de Software
```

Exemplo: processo "Onboarding de Cliente" (BPM) cria entidade Cliente (informação), sujeita a políticas GDPR (governance), persistida em CRM e data lake via APIs (software).

## Desafios e Boas Práticas

**Desafios:** processos documentados desactualizados vs. prática real ("workarounds"), resistência cultural a governance ("burocracia"), ferramentas BPMS abandonadas após projecto inicial.

**Boas práticas:** envolver donos de processo desde o início; glossário de negócio vivo; começar governance em domínios críticos (clientes, financeiro); ligar KPIs de processo a observabilidade técnica; modelos BPMN como contrato entre negócio e TI.

## Exercícios

1. Defina BPM e descreva as cinco fases do ciclo de vida BPM.

2. Qual a diferença entre automatizar tarefas com RPA e implementar BPM completo?

3. Explique os quatro componentes da arquitectura de informação (organização, labelling, navigation, search) com exemplos.

4. O que é Master Data Management e porque é relevante para arquitectos?

5. Descreva três pilares de data governance e um artefacto associado a cada um.

6. Um hospital tem o termo "Utente" no sistema clínico e "Paciente" no administrativo. Que problema de arquitectura de informação é este e como resolver?

7. Como KPIs de processos de negócio (tempo de ciclo) se relacionam com métricas técnicas (latência de API)?

8. Proponha um data owner e um data steward para o domínio "Produto" num retailer — quais as responsabilidades de cada?

## Soluções

1. **BPM** gere processos de negócio de forma sistemática. **Ciclo:** (1) Design — identificar e esboçar processos; (2) Modeling — formalizar em BPMN; (3) Execution — implementar e executar; (4) Monitoring — medir desempenho; (5) Optimization — melhorar com base em dados.

2. **RPA** automatiza tarefas repetitivas em interfaces existentes (copiar dados entre sistemas) sem alterar processo ou arquitectura. **BPM completo** modela e orquestra o processo end-to-end, inclui decisões, actividades humanas, regras, monitorização e optimização contínua. RPA é tactico; BPM é estratégico-operacional.

3. **Organização:** produtos agrupados por categoria e subcategoria no e-commerce. **Labelling:** botão "Adicionar ao Carrinho" em vez de "Insert Item" — linguagem do utilizador. **Navigation:** menu principal, filtros laterais, breadcrumbs "Electrónica > Telemóveis". **Search:** barra de pesquisa com autocomplete e filtros facetados (marca, preço).

4. **MDM** estabelece fonte autoritativa única para entidades master (cliente, produto, fornecedor), sincronizando entre sistemas. Relevante para arquitectos porque define onde reside verdade, como replicar (eventos, APIs batch), padrões de identificação (IDs globais) e impacto em bounded contexts de microserviços.

5. **Data Quality:** métricas de completude, regras de validação, relatórios de qualidade. **Data Ownership:** matriz RACI de domínios de dados, nomes de data owners. **Data Security:** política de classificação (público, confidencial, restrito), controlos de acesso RBAC/ABAC. (Alternativas válidas: lifecycle com política de retenção; privacy com DPIA.)

6. Problema de **inconsistência semântica / silo de vocabulario** — mesmo conceito, termos diferentes, dificultando integração, reporting e compreensão. **Resolução:** glossário empresarial com termo canónico ("Utente" ou "Paciente"), mapeamento nos sistemas, modelo de entidades unificado, e MDM ou hub de identidade que unifica registos.

7. Tempo de ciclo de processo ("aprovação de crédito em 24h") decompõe-se em actividades, cada uma suportada por APIs/serviços. Latência de API afecta directamente duração de actividades automatizadas. Arquitectos devem definir SLAs técnicos alinhados com KPIs de negócio; monitorização (APM, tracing) deve permitir correlacionar latência técnica com bottlenecks de processo. Dashboards combinados negócio+TI identificam se atraso é técnico ou humano.

8. **Data Owner (negócio):** Director de Merchandising — accountable pela definição de atributos de produto, regras de categorização, aprovação de standards. **Data Steward (operacional):** analista de dados de catálogo — responsável pela qualidade diária, correcção de inconsistências, execução de políticas, ponto de contacto para TI. Owner decide "o quê"; steward garante "como" no dia-a-dia.
