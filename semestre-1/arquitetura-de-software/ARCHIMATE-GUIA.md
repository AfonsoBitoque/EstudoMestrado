# Guia ArchiMate — Recursos da Professora

A Prof. Marielba Silva de Zacarias disponibilizou dois recursos oficiais para modelação de arquitetura empresarial e interligação negócio–software. Este guia integra-os no percurso de estudo da UC.

## Recursos oficiais

| Recurso | URL | Uso |
|---------|-----|-----|
| **ArchiMate 101** (The Open Group Community) | https://archimate-community.pages.opengroup.org/workgroups/archimate-101/ | Leitura principal — linguagem, camadas, viewpoints |
| **ArchiMate Tutorial** (Visual Paradigm) | https://online.visual-paradigm.com/diagrams/tutorials/archimate-tutorial/ | Referência visual, exemplos, ligação TOGAF ADM |

> Secção destacada pela professora: [When (not) using ArchiMate?](https://archimate-community.pages.opengroup.org/workgroups/archimate-101/#_when_not_using_archimate)

### Ferramentas recomendadas

| Ferramenta | Tipo | Notas |
|------------|------|-------|
| [Archi](https://www.archimatetool.com/) | Desktop, open-source | Referida no ArchiMate 101 (Part V) |
| [Visual Paradigm Online](https://online.visual-paradigm.com/) | Web | Tutorial oficial da professora |
| C4 / draw.io | Complementar | Arquitetura de software (módulo 03) |

---

## Quando usar ArchiMate (e quando não)

Resumo do ArchiMate 101 — essencial para a UC:

```
Pesquisa (notas, mind maps)
        ↓
Coerência ← ARCHIMATE vive aqui (visão de conjunto EA)
        ↓
Detalhe (BPMN, UML, C4, código)
```

| Fase | Ferramenta | Exemplo na UC |
|------|------------|---------------|
| **Pesquisa** | Notas, entrevistas, whiteboard | Sem. 1–2: perceber o domínio |
| **Coerência** | **ArchiMate** | Sem. 4–8: EA, processos, interligação |
| **Detalhe** | BPMN, UML, C4, ADRs | Sem. 3, 7: processos e software |

**Usa ArchiMate quando:**
- Precisas de comunicar arquitetura empresarial a stakeholders diversos
- Queres ligar negócio → aplicação → tecnologia num modelo coerente
- Fazes gap analysis, cenários ou decisões de alto nível
- O projeto da UC pede modelação de processos **e** interligação com software

**Não uses ArchiMate quando:**
- Precisas de detalhe de implementação (→ UML, C4 nível 3–4)
- Modelas um processo executável (→ BPMN)
- Desenhas infraestrutura de rede detalhada (→ diagramas específicos)
- O diagrama é só para developers (→ C4 containers/components)

---

## Estrutura do ArchiMate 101 → módulos da UC

| Parte ArchiMate 101 | Conteúdo | Módulo UC | Semana sugerida |
|---------------------|----------|-----------|-----------------|
| **Part I** — Introdução | Porquê ArchiMate, viewpoints, quando usar | [04-arquitetura-empresarial](./modulos/04-arquitetura-empresarial.md) | 4 |
| **Part II** — Linguagem | Business, Application, Technology layers | [04](./modulos/04-arquitetura-empresarial.md), [05](./modulos/05-processos-negocio-informacao.md) | 4–5 |
| **Part II** — Metamodela | Actors, roles, processes, services, components | [07](./modulos/07-modelacao-processos-entidades.md) | 6 |
| **Part II** — Relações | Serving, assignment, flow, realization | [08-interligacao-arquiteturas](./modulos/08-interligacao-arquiteturas.md) | 7 |
| **Part III** — Metodologia | Estruturar o modelo, reference models | [06-alinhamento-arquiteturas](./modulos/06-alinhamento-arquiteturas.md) | 6 |
| **Part IV** — Viewpoints | Biblioteca de viewpoints | [08-interligacao-arquiteturas](./modulos/08-interligacao-arquiteturas.md) | 7 |
| **Part V** — Archi tool | Dicas da ferramenta Archi | Projeto prático | 8–10 |
| **Visual Paradigm Tutorial** | TOGAF ADM + camadas, exemplos | [04](./modulos/04-arquitetura-empresarial.md), [06](./modulos/06-alinhamento-arquiteturas.md) | 4–6 |

---

## As 3 camadas core (memorizar)

ArchiMate organiza a EA em camadas com serviços entre elas:

```
┌─────────────────────────────────────────┐
│  BUSINESS LAYER                        │
│  Actors, Roles, Processes, Business    │
│  Services, Business Objects            │
├─────────────────────────────────────────┤
│  APPLICATION LAYER                     │
│  Application Components, Application   │
│  Services, Data Objects                │
├─────────────────────────────────────────┤
│  TECHNOLOGY LAYER                      │
│  Nodes, Devices, System Software,      │
│  Technology Services                   │
└─────────────────────────────────────────┘
         ↑ camada superior USA serviços da inferior
```

### Três aspetos (forma dos elementos)

| Aspeto | Pergunta | Forma | Exemplos |
|--------|----------|-------|----------|
| **Active Structure** | Quem? | Retângulo cantos retos | Business Actor, Application Component, Node |
| **Behavior** | Como? | Retângulo cantos arredondados | Business Process, Application Function |
| **Passive Structure** | O quê? | Vários | Business Object, Data Object |

Fonte: [Visual Paradigm — ArchiMate Tutorial](https://online.visual-paradigm.com/diagrams/tutorials/archimate-tutorial/)

---

## Relações essenciais (para a UC)

| Relação | Significado | Uso típico |
|---------|-------------|------------|
| **Assignment** | Atribuição de responsabilidade | Role → Process; Component → Function |
| **Serving** | Servir / suportar | Application Service → Business Process |
| **Flow** | Transferência de info/material | Process → Process; Object entre processos |
| **Triggering** | Disparo temporal/causal | Evento → Process |
| **Realization** | Implementação abstracta→concreta | Process → Business Service |
| **Composition** | Parte de um todo | Actor composto por sub-actores |

**Interligação negócio–software (C8 da FUC):**
```
Business Process ──serving──► Application Service
                                    ▲
                                    │ realization
                              Application Component
                                    │
                                    │ serving
                                    ▼
                              Technology Service (Node)
```

---

## Viewpoints — framework ISO 42010

Do ArchiMate 101 — antes de desenhar, define:

1. **Stakeholder** — quem vai ver? (CEO, CISO, developer)
2. **Purpose** — informar / decidir / desenhar
3. **Content** — overview / coherence / details
4. **Representation** — diagrama, catálogo, matriz

### Viewpoint journey (sequência típica)

1. Motivação e propósito da organização
2. Visão estratégica e capacidades
3. Processos de negócio chave
4. Modelo de informação (business objects)
5. Gap analysis de aplicações
6. Tecnologia lógica

Cada viewpoint = uma "cena" do filme; juntas contam a história da arquitetura.

### Regras práticas (ArchiMate 101)

- Máximo **20 elementos** por diagrama (40 no limite)
- **Sempre legenda**
- Cor **não tem semântica formal** — usa para scope, gaps, ênfase
- Preferir **nesting** a muitas relações (mais legível para não-especialistas)

---

## ArchiMate + TOGAF ADM

O tutorial Visual Paradigm mapeia ArchiMate às fases TOGAF:

| Fase TOGAF | Elementos ArchiMate |
|------------|---------------------|
| Preliminary, Vision, Requirements | Motivation (Goals, Drivers, Requirements) |
| Phase B — Business | Business layer |
| Phase C — IS Architecture | Application + Data |
| Phase D — Technology | Technology layer |
| Phase E–G — Migration | Implementation & Migration |
| Phase H — Change | Motivation + gaps |

Ver módulo [04-arquitetura-empresarial](./modulos/04-arquitetura-empresarial.md) para ADM completo.

---

## ArchiMate vs outras notações (esta UC)

| Notação | Foco | Módulo |
|---------|------|--------|
| **ArchiMate** | EA holística, 3 camadas, stakeholders | 04, 05, 06, 07, 08 |
| **C4** | Arquitetura de software por sistema | 03 |
| **BPMN** | Processos executáveis / detalhados | 07 |
| **UML deployment** | Deployment físico | 03 |
| **ADRs** | Decisões arquiteturais | 03 |

**Workflow recomendado para o projeto da UC:**
1. ArchiMate — visão negócio + aplicações + tecnologia
2. BPMN — detalhe de 1–2 processos críticos
3. C4 (nível 2) — containers do sistema software
4. ADRs — decisões justificadas

---

## Percurso de estudo ArchiMate (4 semanas)

### Semana A — Fundamentos (Part I ArchiMate 101)

- [ ] Ler: Why ArchiMate + When (not) using ArchiMate
- [ ] Ler: Importance of viewpoints
- [ ] Módulo: [04-arquitetura-empresarial](./modulos/04-arquitetura-empresarial.md)
- [ ] VP Tutorial: "What is ArchiMate" + "Why ArchiMate"
- [ ] Exercício: listar 3 stakeholders do teu projeto e as suas concerns

### Semana B — Camadas (Part II)

- [ ] Ler: Business, Application, Technology layer elements
- [ ] VP Tutorial: Core Layers + Aspects
- [ ] Módulos: [05-processos-negocio-informacao](./modulos/05-processos-negocio-informacao.md)
- [ ] Exercício: diagrama 3 camadas com 5 elementos (Archi ou VP Online)

### Semana C — Processos e entidades

- [ ] Ler: Sample viewpoints (Part IV) — process + application cooperation
- [ ] Módulo: [07-modelacao-processos-entidades](./modulos/07-modelacao-processos-entidades.md)
- [ ] VP Tutorial: exemplos Business Actor, Application Cooperation
- [ ] Exercício: mapear 1 processo BPMN → elementos ArchiMate

### Semana D — Interligação e projeto

- [ ] Ler: Story and viewpoint journeys
- [ ] Módulos: [08-interligacao-arquiteturas](./modulos/08-interligacao-arquiteturas.md), [06-alinhamento](./modulos/06-alinhamento-arquiteturas.md)
- [ ] Part V ArchiMate 101 (se usares Archi)
- [ ] Exercício: viewpoint completo para o projeto (overview + interligação)

---

## Exercícios integrados

1. Explica com o modelo "the Squiggle" quando usarias ArchiMate vs. BPMN num projeto de e-commerce.
2. Desenha um diagrama ArchiMate com: Business Actor, Business Process, Application Component, Application Service, Node — com relações serving e assignment.
3. Define um viewpoint para o CISO (stakeholder, purpose, content, restrições) — segue template do ArchiMate 101.
4. Num diagrama com 25 elementos, como o simplificarias para 20? O que removerias?
5. Mapeia Phase B e Phase C do TOGAF ADM para camadas ArchiMate.
6. Compara um Business Object ArchiMate com uma entidade do módulo 07 — semelhanças e diferenças.
7. Cria interligação: processo "Processar Encomenda" → serviço "Payment API" → componente "Payment Service" → node "AWS EC2".
8. Seguindo o tutorial VP, reproduz o exemplo "Application Cooperation" adaptado ao teu cenário de projeto.

## Soluções

1. **Squiggle:** Pesquisa = entender requisitos (notas). Coerência = ArchiMate para visão EA e alinhar stakeholders. Detalhe = BPMN para fluxo de checkout executável, C4 para serviços.

2. **Diagrama:** Customer (Actor) assigned to Browse Catalog (Process). Catalog Service (App Service) serves Browse Catalog. Catalog API (Component) realizes Catalog Service. Catalog API deployed on Web Server (Node) via serving.

3. **Viewpoint CISO:** Nome: External Data Flow View. Stakeholder: CISO. Purpose: Deciding. Content: Overview. Concepts: Node, Communication Network, Flow. Convenção: flows externos a vermelho, legenda obrigatória.

4. **Simplificar:** Agrupar componentes num composite; remover nodes redundantes; fundir processos de baixo valor; usar nesting em vez de relações explícitas; mover detalhe para diagrama separado (viewpoint de details).

5. **TOGAF→ArchiMate:** Phase B = Business layer. Phase C = Application layer + Business Objects (data). Phase D = Technology layer.

6. **Business Object vs entidade:** Ambos modelam conceitos de informação. Business Object é passive structure ArchiMate, independente de implementação. Entidade (módulo 07) pode ser conceptual/ lógica/ física; Business Object liga a Data Object na application layer via representation.

7. **Interligação:** Processar Encomenda (Process) ← served by — Payment API (App Service) ← realized by — Payment Service (Component) ← running on — AWS EC2 (Node). Label relações serving e realization.

8. **Application Cooperation:** Dois Application Components (Order Service, Inventory Service) com flow de information/data object "Order" entre eles; ambos servem Business Processes distintos; documentar interfaces como application interfaces.
