# Roadmap — Arquitetura de Software

**UC:** 14741096 · **ECTS:** 6 · **Docente:** Marielba Silva de Zacarias · **Língua:** Inglês  
**Pré-requisitos recomendados:** Programação Imperativa, POO, Engenharia de Software, Análise e Modelação de Sistemas

> **Modelação EA:** segue o [ARCHIMATE-GUIA.md](./ARCHIMATE-GUIA.md) com os recursos oficialmente indicados pela professora.

## Objetivos de aprendizagem (resumo)

| ID | Objetivo |
|----|----------|
| O1 | Conceitos fundamentais de arquiteturas de software e tipos principais |
| O2 | Arquiteturas empresariais e suas dimensões |
| O3 | Alinhamento entre arquitetura de software e empresarial |
| O4 | Casos de estudo e tomada de decisão |
| O5 | Tendências emergentes |
| O6 | Modelar arquiteturas de software, processos de negócio e interligação |
| O7 | Aplicar conhecimentos em exercícios e projetos |

## Percurso de estudo (8–10 semanas)

### Fase 1 — Fundamentos (Semanas 1–2)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 1 | [01-conceitos-fundamentais](./modulos/01-conceitos-fundamentais.md) | O1 | 4–6 h |
| 2 | [02-padroes-arquiteturais](./modulos/02-padroes-arquiteturais.md) | O1 | 6–8 h |

**Checkpoint:** Explicar diferença entre arquitetura, design e implementação; listar 3 padrões e trade-offs.

### Fase 2 — Modelação de software (Semana 3)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 3 | [03-modelacao-arquitetura-software](./modulos/03-modelacao-arquitetura-software.md) | O1, O6, O7 | 5–7 h |

**Checkpoint:** Desenhar diagrama C4 (nível 2) para um sistema simples.

### Fase 3 — Arquitetura empresarial + ArchiMate (Semanas 4–5)

| Ordem | Módulo | Objetivos | Leitura ArchiMate | Tempo |
|-------|--------|-----------|-------------------|-------|
| 4 | [04-arquitetura-empresarial](./modulos/04-arquitetura-empresarial.md) | O2 | [ArchiMate 101 — Part I](https://archimate-community.pages.opengroup.org/workgroups/archimate-101/) + [VP Tutorial](https://online.visual-paradigm.com/diagrams/tutorials/archimate-tutorial/) | 5–7 h |
| 5 | [05-processos-negocio-informacao](./modulos/05-processos-negocio-informacao.md) | O2, O6 | ArchiMate 101 — Part II (Business layer) | 5–7 h |

**Checkpoint:** Diagrama ArchiMate 3 camadas (Business → Application → Technology) com ≥5 elementos e legenda.

Ver percurso detalhado: [ARCHIMATE-GUIA.md](./ARCHIMATE-GUIA.md)

### Fase 4 — Alinhamento, processos e interligação ArchiMate (Semanas 6–7)

| Ordem | Módulo | Objetivos | Leitura ArchiMate | Tempo |
|-------|--------|-----------|-------------------|-------|
| 6 | [06-alinhamento-arquiteturas](./modulos/06-alinhamento-arquiteturas.md) | O3 | ArchiMate 101 — Part III (methodology) | 4–5 h |
| 7 | [07-modelacao-processos-entidades](./modulos/07-modelacao-processos-entidades.md) | O6, O7 | Part II + VP exemplos Business Actor | 6–8 h |
| 8 | [08-interligacao-arquiteturas](./modulos/08-interligacao-arquiteturas.md) | O3, O6, O7 | Part IV (viewpoints) + relações serving | 5–7 h |

**Checkpoint:** Viewpoint ArchiMate que liga 1 Business Process a Application Components (interligação C8).

### Fase 5 — Aplicação e tendências (Semanas 8–10)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 9 | [09-casos-estudo](./modulos/09-casos-estudo.md) | O4 | 4–6 h |
| 10 | [10-tendencias-emergentes](./modulos/10-tendencias-emergentes.md) | O5 | 3–5 h |
| — | [materia-extra.md](./materia-extra.md) | Complementar | Contínuo |

**Checkpoint final:** Propor arquitetura para um projeto, justificando decisões com atributos de qualidade e alinhamento ao negócio.

## Mapa conteúdos programáticos → módulos

| Conteúdo (FUC) | Módulo |
|----------------|--------|
| C1 Conceitos fundamentais | 01 |
| C2 Padrões arquiteturais | 02 |
| C3 Modelação de arquiteturas | 03 |
| C4 Arquitetura empresarial | 04 |
| C5 Processos de negócio e informação | 05 |
| C6 Alinhamento | 06 |
| C7 Modelação de processos e entidades | 07 |
| C8 Interligação arquiteturas | 08 |
| C9 Casos de estudo | 09 |
| C10 Tendências emergentes | 10 |

## Avaliação (referência)

- **50%** teórica: apresentações (15%), testes (30%), participação (5%)
- **50%** prática: projeto em grupo com defesa individual

## Recursos oficiais da UC (modelação)

| Recurso | URL |
|---------|-----|
| **ArchiMate 101** (The Open Group) | https://archimate-community.pages.opengroup.org/workgroups/archimate-101/ |
| **When (not) using ArchiMate?** | https://archimate-community.pages.opengroup.org/workgroups/archimate-101/#_when_not_using_archimate |
| **ArchiMate Tutorial** (Visual Paradigm) | https://online.visual-paradigm.com/diagrams/tutorials/archimate-tutorial/ |
| **Guia de estudo integrado** | [ARCHIMATE-GUIA.md](./ARCHIMATE-GUIA.md) |

## Outras ligações

- [C4 Model](https://c4model.com/)
- [Archi — modeling tool](https://www.archimatetool.com/)
- [TOGAF — The Open Group](https://www.opengroup.org/togaf)
