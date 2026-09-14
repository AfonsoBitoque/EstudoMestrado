# Matéria Extra — Tópicos Complementares

**UC:** Modelação e Integração de Dados · **Estudo contínuo**

Este documento complementa os 7 módulos principais com tópicos modernos e transversais: data lakes, lakehouse, Apache Spark, data mesh e privacidade de dados (GDPR).

---

## 1. Data Lakes

### 1.1 Definição

Um **data lake** é um repositório centralizado que armazena **dados brutos** em qualquer formato (estruturados, semiestruturados, não estruturados) num sistema de ficheiros distribuído ou object storage, tipicamente com abordagem **schema-on-read**.

```
Fontes diversas → Ingestão → Data Lake (raw zone)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              [Bronze/Raw]    [Silver/Clean]  [Gold/Analytics]
              dados brutos    limpos          agregados prontos
```

### 1.2 Zonas de maturidade (medallion architecture)

| Zona | Conteúdo | Transformação |
|------|----------|---------------|
| **Bronze** | Raw, as-is das fontes | Nenhuma |
| **Silver** | Limpos, deduplicados, tipados | ETL moderado |
| **Gold** | Agregados, modelados para BI | ETL pesado |

### 1.3 Vantagens

- **Flexibilidade:** ingerir qualquer formato sem schema prévio
- **Custo:** object storage (S3, ADLS) muito barato por TB
- **Escala:** petabytes sem reengenharia
- **Data science:** dados brutos disponíveis para ML

### 1.4 Desafios — "Data swamp"

Sem governança, o lake torna-se inutilizável:

- Metadados inexistentes (catalogação)
- Qualidade desconhecida
- Duplicação e obsolescência
- Segurança e compliance negligenciadas

**Solução:** data catalog (Apache Atlas, AWS Glue Catalog), data quality frameworks, políticas de lifecycle.

### 1.5 Data lake vs Data warehouse

| Critério | Data Lake | Data Warehouse |
|----------|-----------|----------------|
| Dados | Raw + processados | Processados, modelados |
| Schema | On-read | On-write |
| Utilizadores | Data scientists, engenheiros | Analistas de BI |
| Performance queries | Variável | Optimizada |
| Custo storage | Baixo | Médio-alto |
| Governança | Desafiante | Madura |

---

## 2. Lakehouse

### 2.1 Definição

**Lakehouse** combina a flexibilidade e custo do data lake com as capacidades de gestão, ACID transactions e performance SQL do data warehouse, tipicamente sobre object storage.

```
Object Storage (S3/ADLS)
        +
Table Format (Delta Lake / Iceberg / Hudi)
        +
Compute Engine (Spark / Trino / Databricks)
        =
Lakehouse
```

### 2.2 Componentes-chave

| Componente | Função |
|------------|--------|
| **Object storage** | Camada de persistência barata (S3) |
| **Table format** | ACID, time travel, schema evolution sobre ficheiros |
| **Compute** | Spark, Trino, Flink para queries e transformações |
| **Catalog** | Unity Catalog, Hive Metastore, AWS Glue |

### 2.3 Table formats

| Format | Destaque |
|--------|----------|
| **Delta Lake** | Databricks, time travel, MERGE |
| **Apache Iceberg** | Netflix, hidden partitioning, multi-engine |
| **Apache Hudi** | Uber, upserts incrementais, CDC |

### 2.4 Vantagens sobre lake puro

- **ACID transactions:** writes concorrentes seguros
- **Time travel:** consultar versões anteriores (`VERSION AS OF`)
- **Schema evolution:** adicionar colunas sem rewrite
- **Performance:** data skipping, Z-ordering, caching
- **Unificação:** elimina silo lake + DW separados

### 2.5 Exemplo Delta Lake

```python
# Escrever com ACID
df.write.format("delta").mode("overwrite").save("/lake/vendas")

# Time travel
spark.read.format("delta").option("versionAsOf", 5).load("/lake/vendas")

# MERGE (upsert)
from delta.tables import DeltaTable
DeltaTable.forPath(spark, "/lake/clientes").merge(
  novos_dados, "target.id = source.id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```

---

## 3. Apache Spark

### 3.1 Definição

**Apache Spark** é um motor de processamento distribuído unificado para big data — batch, streaming, SQL, ML e graph processing numa única plataforma.

### 3.2 Arquitectura

```
Driver Program
     │
     ├── Cluster Manager (YARN, K8s, Standalone)
     │        │
     │   ┌────┴────┐
     │   │ Workers │ (Executors)
     │   │  Tasks  │
     │   └─────────┘
     │
Spark Core (RDD) → Spark SQL → Spark Streaming → MLlib → GraphX
```

### 3.3 Componentes relevantes para integração

| Componente | Uso |
|------------|-----|
| **Spark SQL** | Queries SQL sobre DataFrames |
| **Structured Streaming** | Processamento de streams (micro-batch) |
| **Spark Connect** | Client-server API desacoplada |

### 3.4 Exemplo ETL com Spark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("ETL Vendas").getOrCreate()

# Extract
vendas = spark.read.json("s3://lake/bronze/vendas/")
clientes = spark.read.parquet("s3://lake/silver/clientes/")

# Transform
vendas_clean = vendas \
  .filter(col("valor") > 0) \
  .withColumn("moeda_eur",
    when(col("moeda") == "USD", col("valor") * 0.92)
    .otherwise(col("valor")))

resultado = vendas_clean.join(clientes, "cliente_id") \
  .groupBy("regiao", "categoria") \
  .sum("moeda_eur")

# Load
resultado.write.format("delta").mode("overwrite") \
  .save("s3://lake/gold/vendas_por_regiao/")
```

### 3.5 Spark vs MapReduce vs Flink

| Critério | MapReduce | Spark | Flink |
|----------|-----------|-------|-------|
| Modelo | Batch, disco | Batch + micro-batch, memória | Stream nativo |
| Latência | Alta (min) | Média (seg) | Baixa (ms) |
| Iterações (ML) | Lento | Rápido (in-memory) | Rápido |
| Maturidade | Legado | Muito alta | Alta |

### 3.6 Quando usar Spark

- ETL de grandes volumes (>100 GB) para lake/lakehouse
- Transformações complexas com joins multi-fonte
- Pipeline unificado batch + streaming
- ML feature engineering em escala

---

## 4. Data Mesh

### 4.1 Definição

**Data mesh** é um paradigma **socio-técnico** proposto por Zhamak Dehghani (ThoughtWorks, 2019) que descentraliza a propriedade e gestão de dados, tratando-os como **produtos** fornecidos por domínios de negócio.

### 4.2 Quatro princípios

| Princípio | Descrição |
|-----------|-----------|
| **Domain ownership** | Cada domínio (vendas, logística) é dono dos seus dados |
| **Data as a product** | Dados expostos com SLAs, documentação, qualidade |
| **Self-serve platform** | Plataforma que facilita criar/consumir produtos de dados |
| **Federated governance** | Standards globais (formato, segurança) com autonomia local |

### 4.3 Arquitectura conceptual

```
┌─────────────────────────────────────────────────────┐
│           Self-Serve Data Platform                   │
│  (infra, catálogo, pipelines, qualidade, segurança) │
└──────────┬──────────────┬──────────────┬─────────────┘
           │              │              │
    ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Domínio     │ │ Domínio   │ │ Domínio   │
    │ Vendas      │ │ Logística │ │ Marketing │
    │ (data       │ │ (data     │ │ (data     │
    │  products)  │ │  products)│ │  products)│
    └─────────────┘ └───────────┘ └───────────┘
```

### 4.4 Data product

Um **produto de dados** inclui:

- Dados (datasets, APIs, streams)
- Metadados (schema, lineage, owner)
- SLAs (freshness, availability, quality)
- Documentação e contratos de interface
- Políticas de acesso

### 4.5 Data mesh vs Data warehouse centralizado

| Aspeto | DW Centralizado | Data Mesh |
|--------|-----------------|-----------|
| Propriedade | Equipa central de dados | Domínios de negócio |
| Escalabilidade organizacional | Bottleneck central | Distribuída |
| Agilidade | Lenta (fila central) | Rápida (autonomia) |
| Consistência | Alta (modelo único) | Desafiante (federada) |
| Complexidade | Técnica | Organizacional + técnica |

### 4.6 Quando adoptar

- Organização grande com múltiplos domínios independentes
- Equipa central de dados sobrecarregada (bottleneck)
- Necessidade de time-to-market rápido por domínio
- Maturidade organizacional para governança federada

**Não adoptar** se: organização pequena, domínio único, ou falta de plataforma self-serve.

---

## 5. GDPR e Privacidade de Dados

### 5.1 Contexto

O **Regulamento Geral sobre a Proteção de Dados (RGPD/GDPR)** é regulamento europeu (2018) que define regras para recolha, processamento e armazenamento de dados pessoais.

Aplica-se a qualquer organização que processe dados de residentes na UE, independentemente da localização.

### 5.2 Princípios fundamentais (Art. 5)

| Princípio | Implicação para integração |
|-----------|---------------------------|
| **Licitude, lealdade, transparência** | Base legal para processamento; informar titulares |
| **Limitação de finalidades** | Dados só para fins declarados |
| **Minimização** | Recolher apenas o necessário |
| **Exactidão** | Dados correctos e actualizados |
| **Limitação de conservação** | Não reter além do necessário |
| **Integridade e confidencialidade** | Segurança técnica e organizacional |
| **Responsabilização** | Demonstrar compliance |

### 5.3 Bases legais para processamento (Art. 6)

- Consentimento do titular
- Execução de contrato
- Obrigação legal
- Interesses vitais
- Interesse público
- **Interesse legítimo** (com teste de balanceamento)

### 5.4 Direitos dos titulares

| Direito | Impacto no DW/Lake |
|---------|-------------------|
| **Acesso** (Art. 15) | Exportar todos os dados de um titular |
| **Rectificação** (Art. 16) | Corrigir dados incorrectos em todas as cópias |
| **Apagamento** (Art. 17) | "Direito ao esquecimento" — eliminar de todos os sistemas |
| **Portabilidade** (Art. 20) | Fornecer dados em formato estruturado |
| **Oposição** (Art. 21) | Cessar processamento para marketing |

### 5.5 Implicações para pipelines de dados

**Pseudonimização vs Anonimização:**

| Técnica | Reversível? | GDPR aplica? |
|---------|-------------|--------------|
| Pseudonimização | Sim (com chave) | Sim — dados pessoais |
| Anonimização | Não | Não — fora do scope |

**Técnicas:**

```
Identificação directa:  nome, email, NIF, telefone
Identificação indirecta: IP, cookies, combinações de atributos

Pseudonimização:  hash(NIF) → identificador irreversível sem chave
Generalização:    idade 34 → faixa "30-40"
Supressão:        remover colunas identificadoras
Tokenização:      substituir por token reversível (vault)
```

### 5.6 Privacy by Design (Art. 25)

Integrar privacidade desde a concepção:

1. **Data minimization:** ETL não copia campos desnecessários para o DW
2. **Masking:** `email → a***@email.pt` em ambientes de dev/test
3. **Encryption:** at-rest (AES-256) e in-transit (TLS)
4. **Access control:** RBAC, row-level security por departamento
5. **Audit logging:** quem acedeu a que dados pessoais
6. **Retention policies:** purge automático após período legal

### 5.7 DPIA — Data Protection Impact Assessment

Obrigatória quando processamento pode causar **alto risco** (Art. 35):

- Profiling sistemático
- Dados sensíveis em larga escala (saúde, origem racial)
- Monitorização sistemática de área pública

### 5.8 Transferências internacionais

Dados pessoais só podem ser transferidos para países com **decisão de adequação** ou com **garantias** (Standard Contractual Clauses, Binding Corporate Rules).

Impacto: cloud providers (AWS US, GCP) requerem SCCs ou regiões EU.

### 5.9 Multas

Até **20 M€** ou **4% do volume de negócios global** (o que for maior).

Exemplos: Meta (1,2 B€, 2023), Amazon (746 M€, 2021).

---

## Exercícios

### Exercício 1
Uma empresa armazena logs JSON brutos (500 TB), relatórios BI agregados e PDFs de contratos no mesmo S3 bucket sem catalogação. Identifique três problemas e classifique o repositório (lake, swamp, warehouse).

### Exercício 2
Compare data lake, data warehouse e lakehouse para uma startup que processa 50 GB/dia de eventos JSON e precisa de dashboards SQL e notebooks ML.

### Exercício 3
Explique como Delta Lake resolve o problema de concurrent writes num data lake baseado em Parquet puro.

### Exercício 4
Um pipeline Spark processa 200 GB de vendas diárias. O job demora 45 minutos. Identifique três optimizações Spark possíveis.

### Exercício 5
Numa organização com domínios de Vendas, RH e Financeiro, cada um quer autonomia sobre os seus dados mas o CFO precisa de um relatório consolidado. Como data mesh resolve isto?

### Exercício 6
Um cliente exerce o direito ao apagamento (Art. 17). Liste os sistemas que devem ser actualizados numa arquitectura com OLTP, DW, data lake e backups.

### Exercício 7
Diferencie pseudonimização e anonimização. O hash SHA-256 do email de um cliente é pseudonimização ou anonimização? Justifique.

### Exercício 8
Proponha uma política de retenção para dados pessoais num DW de retalho, considerando: transacções (obrigação fiscal 10 anos), dados de marketing (consentimento revogável), logs de acesso (auditoria).

---

## Soluções

### Solução 1

**Classificação: Data Swamp** (lake sem governança).

Problemas:

1. **Sem catalogação:** impossível descobrir que datasets existem e o que contêm
2. **Mistura de zonas:** raw, agregados e PDFs no mesmo bucket — sem separação bronze/silver/gold
3. **Sem controlo de qualidade:** PDFs não estruturados sem metadados; logs JSON sem schema enforcement
4. **Segurança:** contratos (dados sensíveis) acessíveis no mesmo bucket que logs

Remediação: medallion architecture, data catalog, políticas de acesso por zona.

### Solução 2

**Lakehouse recomendado:**

| Requisito | Solução |
|-----------|---------|
| 50 GB/dia JSON | Ingestão para object storage (bronze) |
| Dashboards SQL | Gold layer com Delta/Iceberg + Trino/Spark SQL |
| Notebooks ML | Acesso directo ao lake (silver/bronze) via Spark |
| Custo startup | Object storage barato vs DW enterprise |

DW puro seria rígido para ML; lake puro não daria SQL performante. Lakehouse unifica ambos.

### Solução 3

Parquet puro não suporta **ACID transactions** — writes concorrentes corrompem ficheiros.

Delta Lake adiciona:

- **_delta_log:** transaction log (JSON) que regista cada operação
- **Optimistic concurrency control:** verificar conflitos antes de commit
- **Atomic writes:** write visible only after commit
- **Time travel:** versões anteriores consultáveis

Dois jobs escrevendo simultaneamente: Delta detecta conflito e retry/fail gracefully.

### Solução 4

1. **Partitioning:** particionar por data (`/vendas/ano=2024/mes=06/`) — partition pruning
2. **Broadcast join:** se dim_cliente < 10 MB, broadcast em vez de shuffle join
3. **Cache/Persist:** reutilizar DataFrames intermediários se usados múltiplas vezes
4. **Formato columnar:** converter JSON para Parquet/Delta (leitura columnar 10x mais rápida)
5. **Aumentar executors:** mais paralelismo (se cluster permitir)
6. **Predicate pushdown:** filtrar cedo (`filter` antes de `join`)

### Solução 5

**Data mesh:**

- Cada domínio (Vendas, RH, Financeiro) expõe **data products** com contratos definidos
- CFO consome produtos de dados de cada domínio via **self-serve platform**
- Relatório consolidado: join de data products (não DW monolítico central)
- **Federated governance:** standards comuns (formato, nomenclatura, segurança) garantem interoperabilidade
- Domínio Financeiro pode criar produto "consolidado financeiro" que agrega inputs dos outros

Autonomia local + interoperabilidade global.

### Solução 6

Sistemas a actualizar para apagamento completo:

1. **OLTP:** DELETE do registo (ou anonymize)
2. **Data Warehouse:** DELETE/UPDATE em dim_cliente + fact tables associados
3. **Data Lake:** DELETE ficheiros/partições ou overwrite com dados redigidos
4. **Backups:** purge ou anonymize em backups activos (retention policy)
5. **Caches:** invalidar Redis/Memcached
6. **Search indexes:** Elasticsearch DELETE by query
7. **Logs:** se contêm PII, redigir ou purge conforme retention
8. **Réplicas/CDC:** garantir que delete propaga via Kafka/Debezium
9. **Third-party:** notificar processadores subcontratados (Art. 28)

Documentar prova de apagamento (audit trail).

### Solução 7

**SHA-256(email) é pseudonimização**, não anonimização.

Justificação:

- **Pseudonimização (Art. 4(5)):** dados que não podem ser atribuídos a titular **sem informação adicional** (chave de re-identificação). Hash com salt secreto é reversível com rainbow tables ou se o universo de emails é conhecido.
- **Anonimização:** irreversível — impossível re-identificar titular por qualquer meio razoável.

Para anonimização real: generalização + supressão + k-anonymity (k≥5).

### Solução 8

| Tipo de dado | Retenção | Base legal | Acção após período |
|--------------|----------|------------|-------------------|
| Transacções | 10 anos | Obrigação fiscal (Art. 6(1)(c)) | Anonymize (manter totais, remover PII) |
| Marketing (consentimento) | Até revogação ou 2 anos inactividade | Consentimento (Art. 6(1)(a)) | DELETE imediato se revogado |
| Logs de acesso | 1 ano | Interesse legítimo (segurança) | Purge automático |
| Dimensão cliente (DW) | Alinhada com transacções | Obrigação fiscal | SCD Type 1 anonymize após 10 anos |

Implementar: job ETL de purge mensal, audit log de eliminações, DPIA documentada.

---

## Referências

- Dehghani, Z. — *Data Mesh* (O'Reilly, 2022)
- Databricks — Lakehouse Architecture Whitepaper
- Apache Spark Documentation — https://spark.apache.org
- Delta Lake — https://delta.io
- Regulamento (UE) 2016/679 (RGPD) — https://gdpr.eu
- CNPD (Portugal) — https://www.cnpd.pt
- Kleppmann, M. — *Designing Data-Intensive Applications*

---

## Mapa de ligação aos módulos principais

| Tópico extra | Módulos relacionados |
|--------------|---------------------|
| Data lakes | 01 (tipos), 04 (ETL) |
| Lakehouse | 02 (paradigmas), 04 (ETL/ELT) |
| Apache Spark | 03 (streaming), 04 (ETL) |
| Data mesh | 02 (paradigmas integração) |
| GDPR | 04 (profiling), 06 (DW — PII em dimensões) |
