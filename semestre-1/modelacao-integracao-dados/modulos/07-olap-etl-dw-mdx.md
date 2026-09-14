# Módulo 07 — OLAP, ETL para DW, MDX e Reporting

**UC:** Modelação e Integração de Dados · **Fase 3** · **Tempo sugerido:** 7–9 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Diferenciar OLTP de OLAP e compreender arquitecturas ROLAP, MOLAP e HOLAP
- Aplicar operações OLAP: roll-up, drill-down, slice, dice, pivot
- Descrever o pipeline ETL específico para data warehouse
- Escrever consultas básicas em MDX
- Compreender princípios de reporting e ferramentas de BI

---

## 1. OLTP vs OLAP

### 1.1 Comparação

| Aspeto | OLTP | OLAP |
|--------|------|------|
| Propósito | Transacções operacionais | Análise e decisão |
| Utilizadores | Operadores, clientes | Analistas, gestores |
| Queries | Simples, ponto (CRUD) | Complexas, agregações |
| Dados | Actuais, normalizados | Históricos, denormalizados |
| Writes | Frequentes | Raros (ETL batch) |
| Reads | Poucos registos | Milhões agregados |
| Modelo | 3NF relacional | Dimensional (star) |
| Latência | Milissegundos | Segundos a minutos |
| Exemplo | Registar venda | Vendas por região/trimestre |

### 1.2 Porque separar?

- Queries analíticas degradam performance OLTP
- Modelos diferentes optimizados para propósitos diferentes
- Histórico e agregações não pertencem ao operacional
- Segurança: analistas não acedem directamente ao OLTP

---

## 2. Arquitecturas OLAP

### 2.1 ROLAP (Relational OLAP)

Cubo OLAP implementado sobre **base de dados relacional** (star schema). Motor traduz operações OLAP em SQL.

**Vantagens:** escala a grandes volumes, SQL standard, flexível  
**Desvantagens:** performance inferior a MOLAP para agregações complexas  
**Exemplos:** Mondrian, Apache Druid (parcial), PostgreSQL + BI tool

### 2.2 MOLAP (Multidimensional OLAP)

Dados armazenados em **estrutura multidimensional** pré-calculada (cubos materializados).

**Vantagens:** queries extremamente rápidas, agregações pré-computadas  
**Desvantagens:** storage intensivo, cubos rígidos, difícil escalar  
**Exemplos:** Microsoft Analysis Services (modo MOLAP), essbase

### 2.3 HOLAP (Hybrid OLAP)

Combina MOLAP (agregações frequentes em cache) + ROLAP (detalhe em relacional).

**Vantagens:** balance entre performance e flexibilidade  
**Desvantagens:** complexidade de gestão  
**Exemplos:** Analysis Services (modo HOLAP)

### 2.4 Comparação

| Critério | ROLAP | MOLAP | HOLAP |
|----------|-------|-------|-------|
| Storage | Eficiente | Alto | Médio |
| Speed agregações | Médio | Muito rápido | Rápido |
| Detalhe (drill-down) | Nativo | Limitado | Híbrido |
| Escala dados | Alta | Média | Alta |
| Flexibilidade | Alta | Baixa | Média |

Tendência moderna: **ROLAP** sobre DW cloud (Snowflake, BigQuery) + caching (Materialized Views).

---

## 3. Operações OLAP

### 3.1 Roll-up (drill-up / agregação)

**Subir** na hierarquia dimensional — menos detalhe, mais agregação.

```
Drill-down:  Dia → Semana → Mês → Trimestre → Ano
Roll-up:     Ano → Trimestre → Mês → Semana → Dia (inverso)
```

Exemplo: vendas por **cidade** → roll-up → vendas por **região** → roll-up → vendas por **país**.

```sql
-- Roll-up: cidade → região
SELECT l.regiao, SUM(f.valor_venda) AS total
FROM fact_vendas f
JOIN dim_loja l ON f.loja_sk = l.loja_sk
GROUP BY l.regiao;
```

### 3.2 Drill-down

**Descer** na hierarquia — mais detalhe.

Exemplo: vendas por **ano** → drill-down → vendas por **trimestre** → por **mês** → por **dia**.

```sql
-- Drill-down: ano → mês
SELECT d.ano, d.mes, SUM(f.valor_venda) AS total
FROM fact_vendas f
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE d.ano = 2024
GROUP BY d.ano, d.mes
ORDER BY d.mes;
```

### 3.3 Slice (fatia)

Seleccionar uma **sub-cubo** fixando **uma dimensão** a um valor.

Exemplo: vendas onde `região = 'Norte'` (todas as outras dimensões livres).

```sql
SELECT p.categoria, d.trimestre, SUM(f.valor_venda)
FROM fact_vendas f
JOIN dim_loja l ON f.loja_sk = l.loja_sk
JOIN dim_produto p ON f.produto_sk = p.produto_sk
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE l.regiao = 'Norte'
GROUP BY p.categoria, d.trimestre;
```

### 3.4 Dice (dado)

Seleccionar sub-cubo fixando **múltiplas dimensões** a valores específicos.

Exemplo: vendas onde `região = 'Norte'` AND `categoria = 'Electrónica'` AND `ano = 2024`.

```sql
SELECT d.mes, SUM(f.valor_venda)
FROM fact_vendas f
JOIN dim_loja l ON f.loja_sk = l.loja_sk
JOIN dim_produto p ON f.produto_sk = p.produto_sk
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE l.regiao = 'Norte'
  AND p.categoria = 'Electrónica'
  AND d.ano = 2024
GROUP BY d.mes;
```

### 3.5 Pivot (rotação)

Rotação de dimensões entre **linhas** e **colunas** — transformar dimensão em colunas.

```sql
-- Pivot: meses como colunas
SELECT l.regiao,
       SUM(CASE WHEN d.mes = 1 THEN f.valor_venda END) AS jan,
       SUM(CASE WHEN d.mes = 2 THEN f.valor_venda END) AS fev,
       SUM(CASE WHEN d.mes = 3 THEN f.valor_venda END) AS mar
FROM fact_vendas f
JOIN dim_loja l ON f.loja_sk = l.loja_sk
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE d.ano = 2024
GROUP BY l.regiao;
```

### 3.6 Resumo visual

```
Cubo 3D (Tempo × Produto × Região)

Slice:    fixar Região = Norte        → plano 2D
Dice:     fixar Região = Norte AND Produto = Laptop → linha/ponto
Roll-up:  Mês → Trimestre              → menos detalhe
Drill-down: Ano → Mês                  → mais detalhe
Pivot:    Meses de linhas → colunas    → rotação
```

---

## 4. ETL específico para Data Warehouse

### 4.1 Diferenças do ETL genérico

| Aspeto | ETL genérico | ETL para DW |
|--------|-------------|-------------|
| Destino | Qualquer | Star schema dimensional |
| Transformações | Limpeza | + SCD, surrogate keys, conformação |
| Granularidade | Preservada ou agregada | Definida pelo fact table |
| Dimensões | N/A | Lookup, SCD Type 1/2 |
| Factos | N/A | Incremental load, idempotência |

### 4.2 Pipeline típico

```
1. Extract fontes OLTP (incremental)
2. Stage (raw copy)
3. Transform:
   a. Limpar e normalizar
   b. Gerar surrogate keys (dimensões)
   c. Aplicar SCD (Type 1/2)
   d. Lookup dimensional (resolver FKs)
   e. Calcular medidas derivadas
   f. Rejeitar/flaggar registos inválidos
4. Load:
   a. Dimensões primeiro (FKs existem)
   b. Fact tables depois
   c. Actualizar aggregate tables / MVs
5. Validar (row counts, checksums, reconciliação)
```

### 4.3 Ordem de carga

```
dim_data → dim_produto → dim_cliente → dim_loja → fact_vendas
```

Dimensões **sempre antes** de factos (integridade referencial).

### 4.4 Surrogate key generation

```sql
-- Inserir nova dimensão com SK auto-gerado
INSERT INTO dim_produto (produto_sk, produto_id, nome, categoria, valid_from, is_current)
SELECT nextval('dim_produto_sk_seq'), src.id, src.nome, src.cat, CURRENT_DATE, true
FROM staging_produtos src
WHERE NOT EXISTS (
  SELECT 1 FROM dim_produto d
  WHERE d.produto_id = src.id AND d.is_current = true
);
```

### 4.5 Reconciliação

Comparar totais OLTP vs DW após carga:

```sql
-- Fonte OLTP
SELECT SUM(valor) FROM vendas WHERE data = '2024-06-01';  -- 125 430,50

-- DW
SELECT SUM(valor_venda) FROM fact_vendas f
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE d.data = '2024-06-01';  -- deve ser 125 430,50
```

Discrepâncias indicam perda de dados, duplicados ou regras de transformação incorrectas.

---

## 5. MDX — Multidimensional Expressions

### 5.1 Definição

**MDX** é a linguagem standard para consultar cubos OLAP (similar a SQL para dados relacionais). Usada em Microsoft Analysis Services, Mondrian, SAP BW.

### 5.2 Conceitos MDX

| Conceito | Descrição |
|----------|-----------|
| **Cube** | Conjunto de dimensões e medidas |
| **Dimension** | Eixo de análise |
| **Hierarchy** | Níveis ordenados (Ano → Trimestre → Mês) |
| **Level** | Nível específico (Mês) |
| **Member** | Valor num nível (Junho) |
| **Measure** | Valor numérico agregável |
| **Tuple** | Combinação de members `( [Tempo].[2024], [Produto].[Laptop] )` |
| **Set** | Conjunto de tuples `{ (2024, Laptop), (2024, Rato) }` |

### 5.3 Sintaxe básica

**Query simples:**

```mdx
SELECT
  { [Measures].[Vendas], [Measures].[Margem] } ON COLUMNS,
  { [Produto].[Categoria].Members } ON ROWS
FROM [CuboVendas]
WHERE ( [Tempo].[2024], [Loja].[Região].[Norte] )
```

**Com filtros:**

```mdx
SELECT
  { [Measures].[Vendas] } ON COLUMNS,
  NON EMPTY { [Produto].[Nome].Members } ON ROWS
FROM [CuboVendas]
WHERE ( [Tempo].[2024].[Q2], [Loja].[Região].[Norte] )
```

### 5.4 Funções MDX essenciais

| Função | Descrição |
|--------|-----------|
| `SUM()` | Soma de conjunto |
| `AVG()` | Média |
| `COUNT()` | Contagem |
| `TOPCOUNT(set, n, measure)` | Top N |
| `FILTER(set, condition)` | Filtrar conjunto |
| `CROSSJOIN(set1, set2)` | Produto cartesiano |
| `DESCENDANTS(member, level)` | Drill-down programático |
| `ANCESTOR(member, level)` | Roll-up programático |
| `ParallelPeriod()` | Período paralelo (YoY) |
| `YTD()` | Year-to-date |

### 5.5 Exemplos práticos

**Vendas por categoria em 2024:**

```mdx
SELECT
  [Measures].[Vendas] ON COLUMNS,
  [Produto].[Categoria].Members ON ROWS
FROM [CuboVendas]
WHERE [Tempo].[2024]
```

**Top 5 produtos por vendas:**

```mdx
SELECT
  [Measures].[Vendas] ON COLUMNS,
  TOPCOUNT([Produto].[Nome].Members, 5, [Measures].[Vendas]) ON ROWS
FROM [CuboVendas]
WHERE [Tempo].[2024]
```

**Comparação YoY (2024 vs 2023):**

```mdx
WITH
  MEMBER [Measures].[Vendas 2024] AS
    ([Measures].[Vendas], [Tempo].[2024]),
  MEMBER [Measures].[Vendas 2023] AS
    ([Measures].[Vendas], [Tempo].[2023]),
  MEMBER [Measures].[Crescimento %] AS
    ([Measures].[Vendas 2024] - [Measures].[Vendas 2023])
    / [Measures].[Vendas 2023] * 100
SELECT
  { [Measures].[Vendas 2024], [Measures].[Vendas 2023], [Measures].[Crescimento %] }
  ON COLUMNS,
  [Loja].[Região].Members ON ROWS
FROM [CuboVendas]
```

**Drill-down programático (região → lojas):**

```mdx
SELECT
  [Measures].[Vendas] ON COLUMNS,
  DESCENDANTS([Loja].[Região].[Norte], [Loja].[Nome]) ON ROWS
FROM [CuboVendas]
```

### 5.6 MDX vs SQL

| Aspeto | MDX | SQL |
|--------|-----|-----|
| Modelo | Multidimensional | Relacional |
| Agregações | Implícitas (cubo) | Explícitas (GROUP BY) |
| Hierarquias | Nativas (drill) | CASE/GROUP BY manual |
| Calculated members | WITH MEMBER | Subqueries / CTEs |
| Uso | Cubos OLAP | Tabelas ROLAP |

Muitas ferramentas BI (Excel Pivot, Power BI, Tableau) geram MDX ou SQL automaticamente.

---

## 6. Reporting e BI

### 6.1 Camadas de reporting

```
Data Sources (OLTP, APIs)
        ↓ ETL
Data Warehouse (star schema)
        ↓
Semantic Layer (métricas, dimensões de negócio)
        ↓
BI Tool (dashboards, reports)
        ↓
Utilizadores (analistas, gestores)
```

### 6.2 Tipos de relatórios

| Tipo | Descrição | Frequência |
|------|-----------|------------|
| **Operacional** | Transacções recentes, alertas | Tempo real / diário |
| **Táctico** | KPIs departamentais | Semanal / mensal |
| **Estratégico** | Tendências, benchmarks | Trimestral / anual |
| **Ad-hoc** | Exploração livre | Sob demanda |

### 6.3 KPIs e métricas

Definir **métricas de negócio** na camada semântica:

```
Receita Total = SUM(valor_venda)
Margem Bruta = SUM(margem)
Taxa Conversão = COUNT(vendas) / COUNT(visitas)
Ticket Médio = Receita Total / COUNT(DISTINCT num_encomenda)
YoY Growth = (Receita Ano Actual - Receita Ano Anterior) / Receita Ano Anterior
```

### 6.4 Ferramentas de BI

| Ferramenta | Tipo | Destaque |
|------------|------|----------|
| **Power BI** | Desktop + Cloud | Integração Microsoft, DAX |
| **Tableau** | Visual analytics | Visualizações ricas |
| **Apache Superset** | Open-source | SQL-native, dashboards |
| **Metabase** | Open-source | Simplicidade, self-service |
| **Excel Pivot** | Desktop | Acessível, MDX/SQL backend |
| **Grafana** | Observability | Time-series, alertas |

### 6.5 Boas práticas de reporting

1. **Single source of truth:** métricas definidas uma vez na camada semântica
2. **Performance:** pré-agregar queries frequentes (materialized views)
3. **Segurança:** row-level security por departamento/região
4. **Documentação:** dicionário de dados, definições de KPIs
5. **Mobile-first:** dashboards responsivos para gestores
6. **Alertas:** thresholds automáticos (vendas < target)

---

## 7. Integração transaccional → DW (objectivo e)

### 7.1 Fluxo completo

```
[Sistema POS] ──CDC──→ [Kafka] ──→ [ETL Streaming] ──→ [fact_vendas]
[ERP SAP]     ──batch──→ [Staging] ──→ [ETL Nocturno] ──→ [dim_produto, dim_cliente]
                                                              ↓
                                                    [Cubo OLAP / BI Dashboard]
```

### 7.2 Desafios

- **Latência:** batch nocturno vs near-real-time
- **Consistência:** reconciliar OLTP e DW
- **Volume:** incremental vs full load
- **Schema evolution:** novas colunas nas fontes
- **SCD:** manter histórico dimensional correcto

---

## Exercícios

### Exercício 1
Classifique cada operação OLAP:

a) Ver vendas por dia em vez de por mês  
b) Filtrar apenas região Sul  
c) Filtrar região Sul AND categoria Roupa AND ano 2024  
d) Ver vendas por país em vez de por cidade  

### Exercício 2
Escreva SQL equivalente a um roll-up de vendas: dia → mês → trimestre, para o ano 2024.

### Exercício 3
Escreva uma query MDX que mostre vendas e margem por categoria de produto, filtradas para Q1 2024 e região Norte.

### Exercício 4
Explique porque dimensões devem ser carregadas antes de fact tables no ETL do DW.

### Exercício 5
Após ETL, o total de vendas OLTP (1 250 000 €) difere do DW (1 248 750 €). Liste cinco possíveis causas.

### Exercício 6
Escreva MDX para calcular crescimento percentual de vendas de 2023 para 2024 por região (calculated members).

### Exercício 7
Compare ROLAP e MOLAP para um cubo com 10 dimensões, 500M fact rows, e queries que agregam 95% do tempo ao nível mensal.

### Exercício 8
Desenhe três relatórios (operacional, táctico, estratégico) para um gestor comercial de retalho, indicando métricas, frequência e ferramenta.

---

## Soluções

### Solução 1

| Operação | Tipo OLAP |
|----------|-----------|
| a) Dia em vez de mês | **Drill-down** |
| b) Apenas região Sul | **Slice** |
| c) Região Sul + Roupa + 2024 | **Dice** |
| d) País em vez de cidade | **Roll-up** |

### Solução 2

```sql
-- Roll-up: dia → mês → trimestre
SELECT
  d.trimestre,
  d.mes,
  SUM(f.valor_venda) AS total_vendas
FROM fact_vendas f
JOIN dim_data d ON f.data_sk = d.data_sk
WHERE d.ano = 2024
GROUP BY ROLLUP (d.trimestre, d.mes)
ORDER BY d.trimestre, d.mes;
```

Resultado inclui sub-totais por trimestre e total geral (ROLLUP gera agregações automáticas).

Alternativa explícita:

```sql
-- Nível trimestre
SELECT d.trimestre, SUM(f.valor_venda) FROM ... GROUP BY d.trimestre;
-- Nível mês
SELECT d.mes, SUM(f.valor_venda) FROM ... GROUP BY d.mes;
```

### Solução 3

```mdx
SELECT
  { [Measures].[Vendas], [Measures].[Margem] } ON COLUMNS,
  { [Produto].[Categoria].Members } ON ROWS
FROM [CuboVendas]
WHERE ( [Tempo].[2024].[Q1], [Loja].[Região].[Norte] )
```

### Solução 4

Dimensões devem ser carregadas **primeiro** porque:

1. Fact tables contêm **FKs (surrogate keys)** que referenciam dimensões
2. Inserir factos sem dimensão correspondente viola **integridade referencial**
3. ETL de factos faz **lookup** na dimensão para resolver SK (`produto_sk = SELECT ... FROM dim_produto WHERE produto_id = X`)
4. SCD Type 2 pode criar **novos SKs** que factos devem referenciar
5. Ordem incorrecta → factos rejeitados ou FKs órfãs

Sequência: dim_data → dim_produto → dim_cliente → dim_loja → **fact_vendas**.

### Solução 5

Diferença: 1 250 000 - 1 248 750 = **1 250 €** em falta.

Possíveis causas:

1. **Registos rejeitados** no ETL (NIF inválido, FK não resolvida)
2. **Filtro de negócio** exclui vendas canceladas/devolvidas no DW mas não no OLTP
3. **Timing:** vendas após cutoff do ETL (incremental incompleto)
4. **Duplicados** no OLTP contados duas vezes
5. **Conversão de moeda** ou arredondamento diferente
6. **SCD:** vendas associadas a dimensão inactiva e filtradas
7. **Timezone:** data diferente entre OLTP (UTC) e DW (local)

Investigar: `SELECT * FROM erros_etl WHERE data = '2024-06-01'` e reconciliar por sub-totais.

### Solução 6

```mdx
WITH
  MEMBER [Measures].[Vendas 2023] AS
    ([Measures].[Vendas], [Tempo].[2023]),
  MEMBER [Measures].[Vendas 2024] AS
    ([Measures].[Vendas], [Tempo].[2024]),
  MEMBER [Measures].[Crescimento %] AS
    IIF([Measures].[Vendas 2023] = 0, NULL,
      ([Measures].[Vendas 2024] - [Measures].[Vendas 2023])
      / [Measures].[Vendas 2023] * 100
    )
SELECT
  { [Measures].[Vendas 2023], [Measures].[Vendas 2024], [Measures].[Crescimento %] }
  ON COLUMNS,
  [Loja].[Região].Members ON ROWS
FROM [CuboVendas]
```

`IIF` evita divisão por zero.

### Solução 7

**MOLAP recomendado** porque:

- 95% das queries agregam ao nível mensal → agregações pré-computadas aceleram drasticamente
- 10 dimensões geram milhões de combinações — MOLAP materializa as frequentes
- 500M fact rows em ROLAP implicam scans pesados mesmo com star schema

**ROLAP** se:

- Queries ad-hoc ao nível de detalhe (drill-down a linha individual) forem frequentes
- Storage MOLAP for proibitivo
- Flexibilidade de adicionar dimensões/medidas sem rebuild

**HOLAP** como compromisso: agregações mensais em MOLAP, detalhe em ROLAP.

Cloud moderna: ROLAP + **materialized views** (BigQuery, Snowflake) simula MOLAP sem rigidez.

### Solução 8

| Relatório | Tipo | Métricas | Frequência | Ferramenta |
|-----------|------|----------|------------|------------|
| Vendas do dia por loja | Operacional | vendas €, nº transacções, ticket médio | Tempo real / horário | Grafana / dashboard POS |
| Performance semanal por vendedor | Táctico | vendas vs target, conversão, ranking | Semanal | Power BI / Superset |
| Tendência trimestral por categoria e região | Estratégico | YoY growth, margem %, market share | Trimestral | Power BI com cubo OLAP / MDX |

Operacional: acção imediata. Táctico: ajustes de curto prazo. Estratégico: decisões de investimento e expansão.

---

## Referências

- Microsoft MDX Reference
- Kimball, R. — *The Data Warehouse Toolkit* (OLAP chapter)
- Chaudhuri & Dayal — An Overview of Data Warehousing and OLAP Technology
- Power BI / Tableau Documentation

**Matéria complementar:** [materia-extra.md](./materia-extra.md)

---

## Checkpoint final

Modelo estrela + cubo OLAP + 3 consultas analíticas (SQL/MDX) — ver projectos P1/P2 da UC.
