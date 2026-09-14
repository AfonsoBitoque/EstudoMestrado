# Módulo 02 — Paradigmas de Integração de Dados

**UC:** Modelação e Integração de Dados · **Fase 1** · **Tempo sugerido:** 5–7 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Diferenciar integração virtual de integração materializada
- Compreender os paradigmas de mediação e data warehouse
- Avaliar trade-offs entre frescura dos dados, performance e complexidade
- Escolher o paradigma adequado a cenários empresariais concretos

---

## 1. Introdução

A **integração de dados** consiste em combinar informação proveniente de múltiplas fontes heterogéneas para fornecer uma visão unificada. O paradigma escolhido determina **onde** os dados são combinados, **quando** são actualizados e **como** são consultados. Esta decisão arquitectural afecta custos, latência, consistência e manutenção a longo prazo.

---

## 2. Integração virtual vs materializada

### 2.1 Integração virtual

Na **integração virtual**, os dados permanecem nas fontes originais. Um sistema intermediário (middleware, federated query engine, camada semântica) traduz consultas do utilizador em consultas às fontes subjacentes e combina os resultados **em tempo de execução**.

```
Utilizador → Consulta unificada → Middleware → [Fonte A, Fonte B, Fonte C]
                     ↑                              ↓
                     └──────── Resultados ──────────┘
```

**Características:**

- Dados **não são copiados** para um repositório central
- Resultados reflectem o estado **actual** das fontes (máxima frescura)
- Performance depende das fontes e da rede
- Sem custo de armazenamento duplicado

**Exemplos:** Presto/Trino, Apache Drill, views federadas SQL, camadas semânticas (LookML, Metric Layer).

### 2.2 Integração materializada

Na **integração materializada**, os dados são **extraídos, transformados e carregados** (ETL/ELT) num repositório central (data warehouse, data mart, data lake). As consultas executam sobre a cópia local.

```
Fontes → ETL/ELT → Repositório central → Consultas analíticas
```

**Características:**

- Dados **copiados e transformados** periodicamente ou em streaming
- Performance previsível e optimizada para consultas
- Possível desfasamento temporal (latência de actualização)
- Custo de armazenamento e pipeline de manutenção

**Exemplos:** Data warehouse (Snowflake, BigQuery), data marts departamentais, cubos OLAP materializados.

### 2.3 Comparação

| Critério | Virtual | Materializada |
|----------|---------|---------------|
| Frescura | Tempo real | Batch / near-real-time |
| Performance consultas | Variável | Alta (pré-agregações) |
| Carga nas fontes | Alta por consulta | Baixa (periódica) |
| Armazenamento | Mínimo | Significativo |
| Complexidade inicial | Menor | Maior (ETL) |
| Histórico temporal | Limitado às fontes | Snapshots, SCD |
| Offline / desacoplamento | Não | Sim |

---

## 3. Paradigma de mediação

### 3.1 Conceito

O paradigma de **mediação** (também designado **mediator/wrapper** ou **virtual data integration**) utiliza um componente **mediador** que recebe consultas num modelo global unificado e delega sub-consultas a **wrappers** adaptados a cada fonte.

```
         ┌────────── Mediator ──────────┐
         │   Global Schema (GAV/LAV)    │
         └──────┬──────────┬────────────┘
                │          │
         ┌──────▼──┐  ┌────▼─────┐
         │Wrapper A│  │Wrapper B │
         └──────┬──┘  └────┬─────┘
                │          │
           [Fonte A]   [Fonte B]
```

### 3.2 Componentes

| Componente | Função |
|------------|--------|
| **Global schema** | Modelo unificado (ontologia, views) |
| **Mediator** | Decomposição e optimização de consultas |
| **Wrapper** | Tradução entre modelo local e global |
| **Source schema** | Esquema nativo de cada fonte |

### 3.3 Abordagens de mapeamento

- **GAV (Global-as-View):** o esquema global é definido como views sobre as fontes
- **LAV (Local-as-View):** cada fonte é definida como view sobre o esquema global

GAV é mais comum na prática por facilitar a composição de consultas.

### 3.4 Vantagens e limitações

**Vantagens:**

- Sem duplicação de dados
- Integração rápida de novas fontes (adicionar wrapper)
- Dados sempre actualizados

**Limitações:**

- Performance imprevisível
- Dependência de disponibilidade das fontes
- Dificuldade em queries analíticas pesadas (agregações cross-source)
- Sem histórico se a fonte não o mantiver

---

## 4. Paradigma de data warehouse

### 4.1 Conceito

O paradigma de **data warehouse** (armazém de dados) materializa dados integrados num repositório orientado a **consultas analíticas** (OLAP). Segue tipicamente a abordagem **Inmon** (normalizado, enterprise-wide) ou **Kimball** (dimensional, data marts por subject area).

```
Sistemas OLTP → Staging Area → ETL → Data Warehouse → OLAP / BI
```

### 4.2 Características do DW

| Característica | Descrição |
|----------------|-----------|
| Subject-oriented | Organizado por áreas de negócio (vendas, RH) |
| Integrated | Dados de múltiplas fontes harmonizados |
| Time-variant | Histórico com timestamps e SCD |
| Non-volatile | Append-only; dados não são alterados in-place |

### 4.3 Processo ETL/ELT

1. **Extract:** ler dados das fontes (full ou incremental)
2. **Transform:** limpeza, normalização, deduplicação, agregação
3. **Load:** carregar no DW (batch ou micro-batch)

Variante **ELT:** carregar dados brutos primeiro (data lake) e transformar dentro do DW (dbt, SQL).

### 4.4 Vantagens e limitações

**Vantagens:**

- Performance previsível para analytics
- Histórico completo e snapshots
- Desacoplamento das fontes operacionais
- Governança centralizada

**Limitações:**

- Latência de actualização
- Custo de infraestrutura e manutenção ETL
- Risco de data silos se mal governado
- Complexidade de modelação dimensional

---

## 5. Mediação vs Data Warehouse

| Aspeto | Mediação | Data Warehouse |
|--------|----------|----------------|
| Propósito | Acesso unificado ad-hoc | Analytics e reporting |
| Dados | Nas fontes | Copiados e transformados |
| Utilizadores | Desenvolvedores, power users | Analistas, gestores |
| Queries | Operacionais + leves | Pesadas, agregações |
| Latência | Tempo real | Horas a dias |
| Histórico | Não (salvo na fonte) | Sim (SCD, snapshots) |
| Exemplo | API gateway unificada | Cubo de vendas mensal |

---

## 6. Paradigmas híbridos e modernos

### 6.1 Data virtualization + caching

Camadas de virtualização com **cache materializado** para queries frequentes — combina frescura com performance.

### 6.2 Data mesh

Descentraliza a propriedade dos dados por domínio, com **produtos de dados** como unidade de partilha. Não substitui DW, mas complementa a governança federada.

### 6.3 Lakehouse

Combina data lake (raw, barato) com capacidades DW (ACID, SQL) — materialização flexível com schema-on-read e schema-on-write.

### 6.4 CQRS (Command Query Responsibility Segregation)

Separa modelos de escrita (OLTP) e leitura (projeções materializadas) — paradigma comum em microserviços.

---

## 7. Critérios de escolha

| Requisito | Paradigma recomendado |
|-----------|----------------------|
| Dados em tempo real, sem histórico | Virtual / Mediação |
| Reporting pesado, tendências históricas | Data Warehouse |
| Múltiplas fontes, consultas ad-hoc leves | Mediação |
| Compliance, auditoria temporal | Materializado (DW) |
| Orçamento limitado, poucas fontes | Virtual |
| Milhões de registos, agregações | Materializado |
| Self-service BI para gestores | DW + camada semântica |

---

## Exercícios

### Exercício 1
Uma empresa tem CRM (Salesforce), ERP (SAP) e website (PostgreSQL). Os analistas de marketing precisam de cruzar dados de clientes entre os três sistemas para campanhas, mas os dados operacionais devem permanecer nas fontes. Que paradigma recomendaria?

### Exercício 2
Explique porque um data warehouse é considerado integração **materializada**. Dê um exemplo concreto de latência que isto implica.

### Exercício 3
Num sistema de mediação com GAV, o esquema global define `Cliente(id, nome, email, total_compras)`. As fontes são: BD local (id, nome) e API externa (email, compras). Descreva o papel do mediator e dos wrappers.

### Exercício 4
Compare os paradigmas virtual e materializado para um dashboard executivo que mostra vendas do dia anterior às 8h00. Qual é mais adequado e porquê?

### Exercício 5
Uma startup com 3 fontes de dados e 5 utilizadores de BI tem orçamento limitado. Deve investir num DW completo ou numa solução de virtualização? Justifique com três argumentos.

### Exercício 6
Identifique qual paradigma (mediação ou DW) corresponde a cada cenário:

a) Cubo OLAP de vendas com histórico de 5 anos  
b) API que agrega stock de 4 armazéns em tempo real  
c) Relatório regulatório trimestral com auditoria  
d) Pesquisa federada sobre catálogos de bibliotecas  

### Exercício 7
Desenhe (em texto ou diagrama ASCII) a arquitectura híbrida para uma empresa que usa virtualização para queries operacionais e DW para analytics históricos.

### Exercício 8
O conceito **non-volatile** do DW significa que os dados nunca mudam? Explique a nuance e dê um exemplo de como actualizações são tratadas (SCD).

---

## Soluções

### Solução 1

**Paradigma de mediação (integração virtual)** porque:

- Requisito explícito de manter dados nas fontes
- Necessidade de cruzamento ad-hoc (não reporting pesado pré-agregado)
- CRM, ERP e PostgreSQL permanecem systems of record

Implementação: camada de virtualização (Trino, Denodo) ou API de mediação com wrappers por fonte.

### Solução 2

Integração materializada porque os dados são **copiados fisicamente** para o repositório central via ETL. Exemplo de latência: se o ETL corre à meia-noite, uma venda às 23h50 só aparece no DW após o job completar (ex.: 01h30) — **latência de ~1,5 horas**. Em batch diário, latência máxima de 24 horas.

### Solução 3

| Componente | Papel |
|------------|-------|
| **Wrapper BD local** | Traduz consultas ao modelo global para SQL local; expõe id, nome |
| **Wrapper API** | Traduz para chamadas REST; expõe email, compras |
| **Mediator** | Recebe query sobre `Cliente`; decompõe em sub-queries; envia id/nome ao wrapper BD e email/compras ao wrapper API; faz **join** dos resultados por id; devolve tuplo unificado |

Com GAV, `Cliente` é definido como view que combina ambas as fontes.

### Solução 4

**Integração materializada (DW)** é mais adequada porque:

- Dashboard executivo implica agregações pesadas (sum, count por região/produto)
- "Dia anterior às 8h" tolera latência (não precisa de tempo real)
- Performance previsível é crítica para utilizadores C-level
- ETL nocturno garante dados prontos às 8h

Virtual seria inadequada: 4 fontes consultadas simultaneamente cada manhã degradaria performance.

### Solução 5

**Virtualização** recomendada:

1. **Custo:** sem infra DW dedicada, storage duplicado, pipelines ETL complexos
2. **Escala:** 3 fontes e 5 users — overhead de DW não se justifica
3. **Agilidade:** startup precisa iterar rápido; virtualização permite adicionar fontes sem redesenhar pipelines

Quando crescer (mais fontes, queries pesadas, requisitos históricos), migrar para DW híbrido.

### Solução 6

| Cenário | Paradigma |
|---------|-----------|
| a) Cubo OLAP 5 anos | **Data Warehouse** |
| b) Stock tempo real | **Mediação** (virtual) |
| c) Relatório regulatório | **Data Warehouse** (auditoria, histórico) |
| d) Pesquisa federada | **Mediação** (consulta distribuída) |

### Solução 7

```
┌─────────────────────────────────────────────────────────┐
│                    Camada de Acesso                      │
│  ┌──────────────────┐    ┌──────────────────────────┐ │
│  │ Virtualização    │    │ BI / OLAP (sobre DW)     │ │
│  │ (queries ops)    │    │ (analytics históricos)   │ │
│  └────────┬─────────┘    └────────────┬─────────────┘ │
└───────────┼─────────────────────────────┼───────────────┘
            │                             │
     ┌──────▼──────┐               ┌──────▼──────┐
     │  Mediator   │               │ Data        │
     │  + Wrappers │               │ Warehouse   │
     └──────┬──────┘               └──────▲──────┘
            │                             │
     ┌──────▼──────┐               ┌──────┴──────┐
     │ Fontes OLTP │─── ETL ──────▶│ Staging     │
     │ (CRM, ERP)  │   (nocturno)  │ Area        │
     └─────────────┘               └─────────────┘
```

Queries operacionais → virtualização (tempo real). Analytics → DW (batch nocturno).

### Solução 8

**Non-volatile** não significa imutabilidade absoluta. Significa que os dados **não são actualizados in-place** como num OLTP — não se faz `UPDATE` directo a registos analíticos.

Actualizações tratadas via:

- **Append:** novos registos para novos factos
- **SCD Type 2:** nova linha com `valid_from`/`valid_to` quando atributo dimensional muda (ex.: cliente muda de cidade — mantém-se histórico)
- **Snapshots periódicos:** foto do estado a uma data

Exemplo SCD2: cliente "Ana" muda de Lisboa para Porto → nova linha na dimensão com `valid_from = 2024-06-01`, linha anterior com `valid_to = 2024-05-31`.

---

## Referências

- Inmon, W.H. — *Building the Data Warehouse*
- Kimball, R. — *The Data Warehouse Toolkit*
- Lenzerini, M. — Data Integration: A Theoretical Perspective (mediation)
- Gartner — Data Virtualization Market Guide

**Próximo módulo:** [03 — Fontes de Dados, Wrappers e Streaming](./03-fontes-dados-wrappers-streaming.md)
