# Módulo 04 — Arquitetura Empresarial

## Introdução

Enquanto a arquitectura de software foca sistemas individuais, a **Arquitetura Empresarial (Enterprise Architecture — EA)** abrange a totalidade dos activos de TI e o seu alinhamento com a estratégia de negócio da organização. EA fornece uma visão holística que permite decisões coerentes em projectos dispersos, evitando silos e redundâncias. Este módulo define EA, apresenta frameworks reconhecidos (TOGAF, Zachman) e explora as dimensões fundamentais da arquitectura empresarial.

## Definição de Arquitetura Empresarial

**Arquitetura Empresarial** é a disciplina que define a estrutura actual e futura de uma organização em termos de processos de negócio, sistemas de informação, tecnologias e infraestrutura, visando alinhar capacidades de TI com objectivos estratégicos.

EA responde a perguntas de alto nível:
- Que processos de negócio a organização executa e como se relacionam?
- Que sistemas de informação suportam esses processos?
- Que tecnologias e infraestrutura subjacentes existem?
- Como evoluir de forma coerente face a mudanças estratégicas?

Benefícios: redução de redundância (múltiplos sistemas fazendo o mesmo), interoperabilidade, governança de investimentos em TI, agilidade estratégica (adaptar TI a fusões, novos mercados), conformidade regulatória e comunicação entre negócio e TI.

O arquitecto empresarial colabora com executivos, gestores de negócio e arquitectos de solução. Não implementa código — define standards, roadmaps e princípios que guiam implementações.

## Dimensões da Arquitetura Empresarial

Modelos de EA organizam-se tipicamente em **dimensões** ou **domínios** inter-relacionados:

### Dimensão de Negócio (Business Architecture)
Processos, capacidades, organização, estratégia e value streams. Responde: "O que a empresa faz e porque?" Inclui modelos de capacidades (capability maps), processos de negócio (BPMN), organogramas e análise de stakeholders.

### Dimensão de Aplicações (Application Architecture)
Portfolio de aplicações, funcionalidades, interfaces e dependências entre sistemas. Responde: "Que software suporta o negócio?" Inclui application landscape, mapas de integração e ciclo de vida de aplicações (build, buy, retire).

### Dimensão de Dados (Data Architecture)
Entidades de informação, fluxos de dados, governança e qualidade. Responde: "Que dados existem, onde residem e quem os gere?" Inclui modelos de dados empresariais, políticas de master data management (MDM) e conformidade (GDPR).

### Dimensão Tecnológica (Technology Architecture)
Hardware, software base, redes, cloud, standards técnicos. Responde: "Sobre que plataformas corre tudo?" Inclui reference architectures, catálogos de tecnologia aprovada e infraestrutura.

Estas dimensões não são independentes. Uma alteração na dimensão de negócio (novo processo) propaga impactos em aplicações, dados e tecnologia. EA explicita estas relações.

## Framework TOGAF — Visão Geral

**TOGAF** (The Open Group Architecture Framework) é o framework de EA mais adoptado globalmente. A versão TOGAF 9.x/10 estrutura-se em:

### ADM — Architecture Development Method
Processo iterativo de desenvolvimento de arquitectura em fases:
- **Preliminary:** preparar organização e princípios.
- **Phase A — Architecture Vision:** definir scope, stakeholders, visão.
- **Phase B — Business Architecture:** modelar negócio.
- **Phase C — Information Systems Architecture:** aplicações e dados.
- **Phase D — Technology Architecture:** infraestrutura e plataformas.
- **Phase E — Opportunities and Solutions:** identificar work packages e roadmaps.
- **Phase F — Migration Planning:** planear transição.
- **Phase G — Implementation Governance:** supervisionar implementação.
- **Phase H — Architecture Change Management:** gerir evolução contínua.

### Architecture Content Framework
Templates e deliverables padronizados (catalogues, matrices, diagrams) produzidos em cada fase.

### Enterprise Continuum
Repositório de activos arquitecturais reutilizáveis — desde patterns genéricos até soluções específicas da organização.

### Architecture Capability Framework
Guidelines para estabelecer função de EA na organização (governança, competências, ferramentas).

TOGAF é prescritivo no processo mas agnóstico em tecnologias — adaptável a contextos diversos.

## Framework Zachman — Visão Geral

O **Zachman Framework** (John Zachman, 1987) organiza EA numa matriz 6×6:

**Colunas (interrogativos — perspectivas):**
1. **What (Data)** — entidades e relações.
2. **How (Function)** — processos e transformações.
3. **Where (Network)** — localização e interconexão.
4. **Who (People)** — responsabilidades e roles.
5. **When (Time)** — eventos e ciclos temporais.
6. **Why (Motivation)** — objectivos, regras e estratégia.

**Linhas (perspectivas dos stakeholders):**
1. **Scope (Contextual)** — executivos; visão de negócio.
2. **Business Model (Conceptual)** — gestores de negócio.
3. **System Model (Logical)** — arquitectos e designers.
4. **Technology Model (Physical)** — engenheiros e implementadores.
5. **Detailed Representations** — developers.
6. **Functioning Enterprise** — utilizadores finais.

Cada célula da matriz contém artefactos específicos. Zachman não prescreve metodologia — é uma taxonomia para classificar artefactos e garantir completude. Pergunta: "Temos documentação para cada perspectiva em cada dimensão?"

## TOGAF vs. Zachman

| Aspeto | TOGAF | Zachman |
|--------|-------|---------|
| Natureza | Processo/metodologia | Taxonomia/classificação |
| Foco | Como desenvolver EA | O que documentar |
| Prescritividade | Fases e deliverables definidos | Matriz de perguntas |
| Uso típico | Roadmaps, governança, migração | Inventário e gap analysis |

Organizações frequentemente combinam ambos: Zachman para estruturar repositório de artefactos; TOGAF ADM para conduzir projectos de transformação.

## Outros Frameworks e Abordagens

**FEAF (Federal Enterprise Architecture Framework):** usado por agências governamentais dos EUA; cinco reference models (performance, business, data, application, technology).

**Gartner Enterprise Architecture:** abordagem mais pragmática focada em business outcomes e continuous EA.

**BizBOK (Business Architecture Guild):** foco específico na dimensão de negócio e capability-based planning.

## Governança e EA na Prática

EA só gera valor com **governança** — comités de arquitectura, review gates em projectos, compliance com standards, e métricas (application rationalization, technical debt enterprise-wide). Desafios comuns: EA percebida como burocracia, documentação desactualizada, desconexão de equipas ágeis. Abordagens modernas favorecem EA "lean" — princípios e decisões vivas integradas em CI/CD e repositórios, não documentos estáticos num portal esquecido.

## Exercícios

1. Defina Arquitetura Empresarial e distinga-a de arquitectura de software.

2. Descreva as quatro dimensões clássicas de EA e dê um artefacto exemplo de cada uma.

3. Quais são as fases B, C e D do ADM do TOGAF e o que cada uma produz?

4. Explique a matriz Zachman: o que representam as colunas e as linhas?

5. Uma empresa adquire outra com sistemas duplicados (dois ERPs, três CRMs). Como EA ajuda nesta situação?

6. Compare TOGAF e Zachman: são concorrentes ou complementares?

7. O que é um "capability map" na dimensão de negócio?

8. Porque é importante alinhar a dimensão de dados com a dimensão de aplicações num projecto de EA?

## Soluções

1. **EA** é a disciplina que modela e governa a totalidade dos activos de TI (processos, aplicações, dados, tecnologia) alinhados à estratégia empresarial. **Arquitectura de software** foca a estrutura de um sistema ou solução específica. EA é macro (organização inteira); arquitectura de software é micro/meso (sistema ou produto). EA define constraints e standards; arquitectura de software opera dentro desse enquadramento.

2. **Negócio:** process map BPMN ou capability map. **Aplicações:** application portfolio catalog ou integration map. **Dados:** enterprise data model ou data governance policy. **Tecnologia:** technology reference architecture ou approved technology stack list.

3. **Phase B — Business Architecture:** processos, organização, value streams → Business Architecture document. **Phase C — Information Systems Architecture:** aplicações e dados → Application Architecture e Data Architecture. **Phase D — Technology Architecture:** hardware, software, redes → Technology Architecture document com standards e plataformas.

4. **Colunas (interrogativos):** What (dados), How (funções/processos), Where (localização), Who (pessoas/roles), When (tempo/eventos), Why (motivação/objectivos). **Linhas (perspectivas):** Scope/Contextual (executivos), Business Model (gestores), System Model (arquitectos), Technology Model (engenheiros), Detailed Representations (developers), Functioning Enterprise (utilizadores). Cada célula = artefacto específico para aquela perspectiva e dimensão.

5. EA fornece **application rationalization:** inventariar aplicações de ambas empresas, mapear funcionalidades sobrepostas, definir target architecture (qual ERP/CRM manter), planear migração de dados e processos, e estabelecer roadmap de consolidação. Evita manter redundância indefinida e alinha TI com sinergias da fusão.

6. **Complementares.** TOGAF diz **como** conduzir projectos de EA (processo ADM). Zachman diz **o que** documentar (taxonomia completa). Organizações usam ADM para executar e Zachman para organizar o repositório de artefactos e identificar gaps de documentação.

7. **Capability map** é diagrama que representa **capacidades de negócio** (o que a organização sabe fazer) independentemente de organização ou sistemas. Exemplo: "Gestão de Clientes", "Processamento de Encomendas", "Análise de Risco". Capabilities são estáveis; processos e sistemas implementam-nas. Útil para identificar gaps e priorizar investimentos.

8. Aplicações manipulam dados — sem alinhamento, surgem silos de dados, inconsistências entre sistemas e violações de governança. Alinhar garante que entidades empresariais (Cliente, Produto) têm representação coerente, APIs expõem dados conforme modelo empresarial, e políticas de qualidade/privacidade aplicam-se uniformemente. Essencial para integração, MDM e conformidade regulatória.
