# Módulo 03 — Fontes de Dados, Wrappers e Streaming

**UC:** Modelação e Integração de Dados · **Fase 2** · **Tempo sugerido:** 6–8 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Identificar tipos de fontes de dados e os seus desafios de integração
- Compreender o papel de wrappers na arquitectura mediada
- Aplicar técnicas de schema mapping entre modelos heterogéneos
- Diferenciar processamento batch de stream processing
- Descrever estratégias de execução de consultas federadas

---

## 1. Fontes de dados

### 1.1 Tipologia

| Tipo | Exemplos | Acesso típico |
|------|----------|---------------|
| Relacionais | PostgreSQL, Oracle, SQL Server | SQL, JDBC/ODBC |
| NoSQL | MongoDB, Cassandra, Redis | Drivers nativos, APIs |
| Ficheiros | CSV, JSON, Parquet, XML | File system, object storage |
| APIs | REST, GraphQL, SOAP | HTTP, autenticação OAuth |
| Streams | Kafka, Kinesis, MQTT | Consumers, subscrições |
| Web | HTML, scraping | Crawlers, parsers |
| SaaS | Salesforce, HubSpot | APIs proprietárias |

### 1.2 Desafios comuns

- **Heterogeneidade de esquema:** nomes, tipos e granularidade diferentes
- **Heterogeneidade de sintaxe:** SQL dialects, formatos de data
- **Disponibilidade:** fontes offline, rate limits
- **Qualidade:** valores nulos, duplicados, inconsistências
- **Segurança:** credenciais, encriptação, compliance

---

## 2. Wrappers

### 2.1 Definição

Um **wrapper** (invólucro) é um componente software que encapsula uma fonte de dados heterogénea, traduzindo entre o **modelo interno da fonte** e o **modelo canónico** do sistema de integração. Expõe a fonte como se fosse uma base de dados consultável.

### 2.2 Arquitectura

```
Consulta global → Wrapper → Tradução → Protocolo fonte → Resposta → Tradução inversa → Resultado
```

### 2.3 Tipos de wrappers

| Tipo | Fonte | Tradução |
|------|-------|----------|
| **Relational wrapper** | BD SQL | SQL global → SQL local |
| **Web wrapper** | Páginas HTML | Query → HTTP + parsing DOM |
| **API wrapper** | REST/SOAP | Query → HTTP request + JSON/XML mapping |
| **File wrapper** | CSV, Parquet | Query → scan de ficheiro |
| **Stream wrapper** | Kafka | Query → consumer + window |

### 2.4 Funcionalidades essenciais

1. **Schema extraction:** descobrir estrutura da fonte (DESCRIBE, OpenAPI spec)
2. **Query translation:** converter consulta canónica para formato nativo
3. **Result translation:** mapear resposta para modelo global
4. **Capability reporting:** informar que operações suporta (filter pushdown, joins)
5. **Connection management:** pools, retry, timeout

### 2.5 Exemplo conceptual

Wrapper para API REST de produtos:

```
Global: SELECT nome, preco FROM Produto WHERE categoria = 'Electrónica'

Wrapper traduz para:
  GET /api/v1/products?category=electronics
  Mapeia JSON response → tuplos (nome, preco)
```

---

## 3. Schema mapping

### 3.1 Problema

Fontes diferentes representam o mesmo conceito de negócio com estruturas distintas:

| Fonte A (ERP) | Fonte B (CRM) | Conceito global |
|---------------|---------------|-----------------|
| `cust_id` (INT) | `customerId` (STRING) | Cliente.id |
| `cust_name` | `fullName` | Cliente.nome |
| `addr_line1` | `address.street` | Cliente.morada |

### 3.2 Tipos de conflitos

| Conflito | Exemplo | Resolução |
|----------|---------|-----------|
| **Naming** | `cust_id` vs `customerId` | Renomear no mapping |
| **Type** | INT vs STRING | Cast / conversão |
| **Structure** | morada flat vs aninhada | Flatten / nest |
| **Semantic** | `price` com/sem IVA | Regra de transformação |
| **Granularity** | linha de encomenda vs encomenda | Agregação / explosão |

### 3.3 Abordagens de mapping

**Schema matching (automático):**

- Similaridade de nomes (Levenshtein, tokens)
- Similaridade de tipos e constraints
- Instance matching (overlap de valores)

**Schema mapping (manual/semi-automático):**

- Declarações explícitas: `FonteA.cust_id = Global.Cliente.id`
- Ferramentas: Apache Atlas, Informatica, custom YAML

### 3.4 Global-as-View (GAV) vs Local-as-View (LAV)

**GAV:** cada elemento global é view sobre fontes

```sql
-- Global Cliente definido como:
CREATE VIEW Cliente AS
  SELECT a.cust_id AS id, a.cust_name AS nome, b.email
  FROM erp_clientes a
  JOIN crm_contacts b ON CAST(a.cust_id AS VARCHAR) = b.customerId
```

**LAV:** cada fonte é view sobre global (mais flexível para adicionar fontes, mais complexo para query planning)

---

## 4. Stream processing

### 4.1 Batch vs Stream

| Aspeto | Batch | Stream |
|--------|-------|--------|
| Dados | Conjuntos finitos | Fluxos infinitos |
| Latência | Minutos a horas | Milissegundos a segundos |
| Modelo | Job completo → resultado | Evento a evento |
| Exemplos | ETL nocturno | Detecção de fraude |

### 4.2 Conceitos fundamentais

| Conceito | Descrição |
|----------|-----------|
| **Event** | Registo atómico com timestamp (ex.: click, sensor reading) |
| **Event stream** | Sequência ordenada de eventos |
| **Window** | Agrupamento temporal (tumbling, sliding, session) |
| **Watermark** | Estimativa de atraso para eventos tardios |
| **State** | Informação mantida entre eventos (contadores, joins) |

### 4.3 Tipos de janelas

```
Tumbling (5 min):  |----|----|----|
Sliding (5 min, 1 min step):  |----|
                              |----|
                              |----|
Session (gap-based):  |--|  |---|  |-----|
```

### 4.4 Arquitectura Lambda vs Kappa

**Lambda:** pipeline batch (DW) + pipeline stream (speed layer) — complexo, dois codebases.

**Kappa:** tudo como stream; reprocessamento via replay do log — mais simples, Kafka como source of truth.

### 4.5 Ferramentas

| Ferramenta | Papel |
|------------|-------|
| Apache Kafka | Message broker, log distribuído |
| Apache Flink | Stream processing com estado |
| Apache Spark Streaming | Micro-batch sobre Spark |
| ksqlDB | SQL sobre streams Kafka |

---

## 5. Execução de consultas federadas

### 5.1 Query decomposition

O **mediator** decompõe uma consulta global em sub-consultas por fonte:

```sql
-- Consulta global
SELECT c.nome, SUM(v.valor)
FROM Cliente c JOIN Venda v ON c.id = v.cliente_id
WHERE c.regiao = 'Norte'
GROUP BY c.nome
```

Decomposição:

1. Sub-query Fonte A (clientes): `SELECT id, nome FROM clientes WHERE regiao = 'Norte'`
2. Sub-query Fonte B (vendas): `SELECT cliente_id, valor FROM vendas`
3. Join + agregação no mediator

### 5.2 Query optimization

| Técnica | Descrição |
|---------|-----------|
| **Filter pushdown** | Enviar WHERE para a fonte (reduz dados transferidos) |
| **Projection pushdown** | Seleccionar apenas colunas necessárias |
| **Join ordering** | Executar join menor primeiro |
| **Semi-join** | Enviar apenas keys necessárias entre fontes |
| **Caching** | Materializar resultados frequentes |

### 5.3 Custos

Custo total ≈ Σ (transferência + processamento local + join no mediator)

Objectivo: **minimizar dados movidos** entre fontes (filter pushdown é crítico).

### 5.4 Exemplo de plano

```
Consulta: SELECT * FROM A JOIN B ON A.id = B.ref WHERE A.status = 'active'

Plano optimizado:
  1. Fonte A: SELECT id, ... FROM A WHERE status = 'active'  → 1000 rows
  2. Fonte B: SELECT ref, ... FROM B WHERE ref IN (ids de step 1)  → 950 rows
  3. Mediator: hash join local  → 950 rows

Plano ingénuo:
  1. Fonte A: SELECT * FROM A  → 1M rows
  2. Fonte B: SELECT * FROM B  → 5M rows
  3. Mediator: join de 6M rows  → catastrófico
```

---

## 6. Integração de streams com batch

Padrão **CDC (Change Data Capture):** capturar alterações OLTP em tempo real e alimentar DW/lake.

```
OLTP (PostgreSQL) → Debezium → Kafka → Flink/Spark → DW / Lake
```

Permite near-real-time analytics mantendo batch para agregações pesadas.

---

## Exercícios

### Exercício 1
Uma fonte expõe clientes via API REST (`GET /customers/{id}`) e outra via tabela SQL `clientes(id, nome, nif)`. Descreva que funcionalidades cada wrapper deve implementar.

### Exercício 2
Na Fonte A, datas estão em formato `DD/MM/YYYY`; na Fonte B, em `YYYY-MM-DD` (ISO). Na fonte global, o tipo é `DATE`. Escreva a regra de schema mapping para o campo `data_nascimento`.

### Exercício 3
Um stream Kafka recebe ~10 000 eventos/segundo de cliques web. Calcule quantos eventos são processados numa janela **tumbling** de 5 minutos.

### Exercício 4
Explique **filter pushdown** e porque é crítico numa consulta federada que junta uma tabela de 10M linhas (Fonte A) com 500 linhas filtradas (Fonte B).

### Exercício 5
Compare arquitecturas Lambda e Kappa para uma empresa que precisa de dashboard near-real-time e relatórios mensais históricos.

### Exercício 6
Dado o mapping:

- ERP: `product_code` (VARCHAR), `unit_price` (DECIMAL, sem IVA)
- E-commerce: `sku` (VARCHAR), `price` (DECIMAL, com IVA 23%)

Defina o schema global `Produto(codigo, preco_sem_iva)` e as transformações necessárias.

### Exercício 7
Um evento tardio chega 10 minutos após o fecho de uma janela tumbling de 5 minutos. Como sistemas como Flink tratam isto (conceito de watermark)?

### Exercício 8
Desenhe o fluxo completo desde um sensor IoT até um dashboard de monitorização, identificando wrappers, streams e pontos de agregação.

---

## Soluções

### Solução 1

**Wrapper API REST:**

- Schema extraction via OpenAPI/Swagger spec
- Query translation: `SELECT * FROM Cliente WHERE id = X` → `GET /customers/X`
- Paginação se lista completa (`GET /customers?page=N`)
- Autenticação (API key, OAuth token refresh)
- Rate limiting e retry com backoff
- Result translation: JSON → tuplos relacionais

**Wrapper SQL:**

- Schema extraction via `INFORMATION_SCHEMA` ou JDBC metadata
- Query translation: SQL global → SQL dialect local
- Connection pooling
- Filter/projection pushdown nativo
- Transacções read-only

Ambos expõem interface comum: `execute(query) → ResultSet`.

### Solução 2

```sql
-- Regra de mapping (pseudocódigo ETL)
data_nascimento_global = CASE
  WHEN fonte = 'A' THEN TO_DATE(data_nascimento, 'DD/MM/YYYY')
  WHEN fonte = 'B' THEN CAST(data_nascimento AS DATE)  -- já ISO
END
```

Validação adicional: rejeitar datas futuras ou anteriores a 1900.

### Solução 3

```
10 000 eventos/seg × 60 seg/min × 5 min = 3 000 000 eventos
```

Três milhões de eventos por janela tumbling de 5 minutos.

### Solução 4

**Filter pushdown:** o predicado `WHERE` é enviado e executado **na fonte**, não no mediator.

Sem pushdown: transferir 10M linhas de A + 500 de B → join de 10M rows no mediator.

Com pushdown: se filtro aplicável em A, transferir apenas linhas relevantes (ex.: 50 000) → join de 50 000 rows.

Reduz **drasticamente** transferência de rede e memória do mediator. Crítico porque rede é o bottleneck em sistemas federados.

### Solução 5

| Aspeto | Lambda | Kappa |
|--------|--------|-------|
| Dashboard near-RT | Speed layer (Flink) | Stream processing directo |
| Relatórios mensais | Batch layer (DW) | Replay Kafka desde início do mês |
| Complexidade | Dois pipelines | Um pipeline |
| Reprocessamento | Re-run batch job | Replay topic com nova lógica |

**Recomendação:** Kappa se equipa pequena e Kafka já existe; Lambda se DW maduro e batch optimizado separadamente.

### Solução 6

```sql
-- Schema global
Produto(codigo VARCHAR, preco_sem_iva DECIMAL)

-- Mapping ERP (directo)
codigo = product_code
preco_sem_iva = unit_price

-- Mapping E-commerce (remover IVA)
codigo = sku
preco_sem_iva = price / 1.23

-- Join/deduplicação por codigo se ambas as fontes alimentam o global
```

Nota: verificar se `product_code` e `sku` usam mesma codificação (padding, case).

### Solução 7

**Watermark:** estimativa do progresso temporal do stream (`now - max_lateness`).

Com watermark de 10 minutos:

- Janela [10:00–10:05) fecha quando watermark ≥ 10:05
- Eventos com timestamp ≤ watermark são considerados "on time"
- Evento tardio (timestamp 10:03, chega 10:15):
  - Se dentro da lateness allowed → actualiza resultado da janela (modo allowed lateness)
  - Se fora → descartado ou enviado para side output

Flink permite configurar `allowedLateness` para reabrir janelas brevemente.

### Solução 8

```
[Sensor IoT]
     │ MQTT/HTTP
     ▼
[Gateway Edge] ── wrapper MQTT → evento canónico
     │
     ▼
[Apache Kafka] ── topic: sensor-readings
     │
     ├──▶ [Flink Stream Job] ── janelas 1 min, agregações
     │         │
     │         ▼
     │    [TimescaleDB / InfluxDB] ── séries temporais
     │         │
     │         ▼
     └──▶ [Batch ETL nocturno] ── histórico longo
               │
               ▼
          [Data Warehouse]
               │
               ▼
          [Dashboard Grafana/Superset]
```

Wrappers: MQTT wrapper no gateway. Streams: Kafka + Flink. Agregação: streaming (1 min) + batch (diário).

---

## Referências

- Garcia-Molina, H. — Database System Implementation (wrappers)
- Kleppmann, M. — *Designing Data-Intensive Applications* (streams)
- Apache Kafka Documentation
- Apache Flink — Windowing and Watermarks

**Próximo módulo:** [04 — ETL, Transformação e Profiling](./04-etl-transformacao-profiling.md)
