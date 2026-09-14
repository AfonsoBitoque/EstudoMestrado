# Roadmap — Modelação e Integração de Dados

**UC:** 14741095 · **ECTS:** 6 · **Língua:** PT ou EN  
**Pré-requisitos recomendados:** Bases de Dados, Análise e Modelação de Sistemas, Programação

## Objetivos de aprendizagem (resumo)

| # | Competência |
|---|-------------|
| a | Diferenciar SQL vs NoSQL e escolher abordagem adequada |
| b | Filtrar, agregar e extrair dados heterogéneos em grande escala |
| c | Diferenciar OLTP vs OLAP |
| d | Desenhar e implementar data warehouse pequeno/médio |
| e | Integrar dados transacionais em data warehouses |

## Percurso de estudo (8–10 semanas)

### Fase 1 — Tipos e paradigmas (Semanas 1–2)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 1 | [01-tipos-dados-estruturados-semiestruturados](./modulos/01-tipos-dados-estruturados-semiestruturados.md) | a | 4–6 h |
| 2 | [02-paradigmas-integracao-dados](./modulos/02-paradigmas-integracao-dados.md) | a, b | 5–7 h |

**Checkpoint:** Classificar 5 fontes de dados reais por tipo e paradigma de integração.

### Fase 2 — Integração virtual e ETL (Semanas 3–5)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 3 | [03-fontes-dados-wrappers-streaming](./modulos/03-fontes-dados-wrappers-streaming.md) | b | 6–8 h |
| 4 | [04-etl-transformacao-profiling](./modulos/04-etl-transformacao-profiling.md) | b, e | 6–8 h |
| 5 | [05-xml-nosql](./modulos/05-xml-nosql.md) | a, b | 5–7 h |

**Checkpoint:** Pipeline ETL simples com deteção de duplicados e profiling.

### Fase 3 — Data Warehousing e OLAP (Semanas 6–9)

| Ordem | Módulo | Objetivos | Tempo sugerido |
|-------|--------|-----------|----------------|
| 6 | [06-modelo-multidimensional-dw](./modulos/06-modelo-multidimensional-dw.md) | c, d | 6–8 h |
| 7 | [07-olap-etl-dw-mdx](./modulos/07-olap-etl-dw-mdx.md) | c, d, e | 7–9 h |
| — | [materia-extra.md](./materia-extra.md) | Complementar | Contínuo |

**Checkpoint final:** Modelo estrela + cubo OLAP + 3 consultas analíticas (SQL/MDX).

## Mapa conteúdos programáticos → módulos

| Conteúdo (FUC) | Módulo |
|----------------|--------|
| Tipos de dados (estruturados, semi, não) | 01 |
| Paradigmas de integração | 02 |
| Fontes, wrappers, streaming, mapeamento | 03 |
| ETL, profiling, duplicados | 04 |
| XML e NoSQL | 05 |
| Data warehouse multidimensional | 06 |
| OLAP, ETL DW, MDX, reporting | 07 |

## Avaliação (referência)

- **90%** — Projetos P1 e P2 (mín. 10 cada), com defesa individual
- **10%** — Exercícios presenciais (média 0–5)

## Ferramentas sugeridas

| Área | Ferramentas |
|------|-------------|
| ETL | Apache NiFi, Pentaho, dbt |
| Streaming | Apache Kafka, Flink |
| DW | PostgreSQL + star schema, DuckDB |
| OLAP | Apache Druid, Mondrian, Excel Pivot |
| NoSQL | MongoDB, Redis |
