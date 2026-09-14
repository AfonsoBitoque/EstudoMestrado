# Módulo 04 — ETL, Transformação, Profiling e Deduplicação

**UC:** Modelação e Integração de Dados · **Fase 2** · **Tempo sugerido:** 6–8 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Descrever as fases Extract, Transform e Load de um pipeline ETL
- Definir regras de transformação para limpeza e harmonização
- Aplicar técnicas de data profiling para avaliar qualidade
- Implementar estratégias de deduplicação de registos
- Identificar métricas e ferramentas de qualidade de dados

---

## 1. Pipeline ETL

### 1.1 Visão geral

**ETL (Extract, Transform, Load)** é o processo de mover dados de fontes operacionais para um repositório analítico (DW, data lake, data mart).

```
┌─────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ Fontes  │───▶│   Extract   │───▶│  Transform   │───▶│    Load     │
│ (OLTP)  │    │             │    │              │    │  (DW/Lake)  │
└─────────┘    └─────────────┘    └──────────────┘    └─────────────┘
                      │                  │                    │
                      ▼                  ▼                    ▼
                 Staging Area      Regras negócio      Tabelas finais
                 (raw copy)        Limpeza             Índices
                                   Enriquecimento
```

### 1.2 Extract (Extração)

**Objectivo:** obter dados das fontes com mínimo impacto nos sistemas operacionais.

| Modo | Descrição | Quando usar |
|------|-----------|-------------|
| **Full extract** | Copiar tabela completa | Tabelas pequenas, dimensões |
| **Incremental** | Apenas registos alterados desde último extract | Tabelas grandes (factos) |
| **CDC** | Change Data Capture em tempo real | Near-real-time |
| **API polling** | Consultar API periodicamente | Fontes SaaS |

**Técnicas incrementais:**

- Coluna `updated_at` com timestamp
- Log tables / triggers
- Debezium (binlog MySQL, WAL PostgreSQL)
- Hash comparison de linhas

**Staging area:** área intermédia onde dados brutos são depositados antes de transformação — permite reprocessamento sem re-extract.

### 1.3 Transform (Transformação)

**Objectivo:** limpar, harmonizar, enriquecer e modelar dados segundo regras de negócio.

Categorias de transformação:

| Categoria | Exemplos |
|-----------|----------|
| **Limpeza** | Trim strings, corrigir encoding, remover nulos |
| **Normalização** | Formatos de data, moeda, telefone |
| **Derivação** | Calcular margem, idade, categorias |
| **Lookup** | Resolver FKs, mapear códigos |
| **Agregação** | Sumarizar linhas de detalhe |
| **Deduplicação** | Identificar e fundir duplicados |
| **SCD** | Gerir histórico dimensional |

### 1.4 Load (Carga)

**Objectivo:** inserir dados transformados no destino.

| Estratégia | Descrição |
|------------|-----------|
| **Full load** | Truncar e recarregar (dimensões pequenas) |
| **Incremental load** | Append de novos/alterados |
| **Upsert (MERGE)** | Insert or update por chave |
| **Partition swap** | Carregar partição nova, trocar atomicamente |

**Boas práticas:**

- Transacções para atomicidade
- Logging de linhas rejeitadas (dead letter)
- Validação pós-carga (row counts, checksums)
- Idempotência (re-run seguro)

### 1.5 ETL vs ELT

| ETL | ELT |
|-----|-----|
| Transform antes de load | Load raw, transform no destino |
| Staging + servidor ETL | Destino faz transform (SQL, dbt) |
| Pentaho, Informatica | Snowflake + dbt, BigQuery |
| Controlo fino pré-carga | Aproveita poder do DW cloud |

---

## 2. Regras de transformação

### 2.1 Tipos de regras

**Regras de validação:**

```
SE email NOT MATCH regex '^[^@]+@[^@]+\.[^@]+$' ENTÃO rejeitar linha
SE idade < 0 OU idade > 150 ENTÃO marcar como inválido
SE nif NOT NULL ENTÃO validar dígito de controlo
```

**Regras de derivação:**

```
margem = preco_venda - preco_custo
nome_completo = TRIM(nome) || ' ' || TRIM(apelido)
faixa_etaria = CASE WHEN idade < 18 THEN 'Menor' WHEN idade < 65 THEN 'Adulto' ELSE 'Sénior' END
```

**Regras de lookup:**

```
pais_id = SELECT id FROM dim_pais WHERE codigo_iso = fonte.pais_cod
produto_sk = SELECT surrogate_key FROM dim_produto WHERE codigo_natural = fonte.prod_id AND is_current = true
```

**Regras de harmonização:**

```
-- Unificar moedas para EUR
valor_eur = CASE moeda
  WHEN 'USD' THEN valor * taxa_cambio_usd
  WHEN 'GBP' THEN valor * taxa_cambio_gbp
  ELSE valor
END
```

### 2.2 Tratamento de valores nulos

| Estratégia | Quando |
|----------|--------|
| Rejeitar linha | Campo obrigatório (PK, FK) |
| Valor default | `pais = 'Desconhecido'` |
| Imputação | Média/mediana para numéricos |
| Flag `is_missing` | Preservar informação de ausência |

### 2.3 Slowly Changing Dimensions (preview)

Tratadas em detalhe no Módulo 06 — na fase Transform aplicam-se regras SCD Type 1/2/3.

---

## 3. Data profiling

### 3.1 Definição

**Data profiling** é o processo sistemático de examinar dados de origem para compreender estrutura, conteúdo, relações e qualidade **antes** de desenhar transformações.

### 3.2 Dimensões de profiling

| Dimensão | Métricas |
|----------|----------|
| **Structure** | Tipos, comprimentos, nullable |
| **Content** | Min, max, média, desvio padrão |
| **Uniqueness** | Cardinalidade, duplicados |
| **Completeness** | % nulos por coluna |
| **Validity** | % valores dentro de domínio esperado |
| **Consistency** | Cross-column rules |
| **Timeliness** | Frescura, gaps temporais |

### 3.3 Exemplo de relatório de profiling

```
Coluna: email (tabela clientes_fonte)
├── Tipo detectado: VARCHAR(255)
├── Completude: 87,3% (12,7% NULL)
├── Unicidade: 94,1% unique (5,9% duplicados)
├── Padrão dominante: 91,2% match regex email
├── Valores inválidos: 234 registos (ex: "nao tem", "N/A")
├── Comprimento: min=0, max=89, média=24,3
└── Top valores: gmail.com (42%), sapo.pt (18%), ...
```

### 3.4 Ferramentas

| Ferramenta | Tipo |
|------------|------|
| OpenRefine | Profiling + limpeza interactiva |
| Great Expectations | Testes de qualidade como código |
| Apache Griffin | Profiling distribuído |
| SQL analítico | `COUNT`, `GROUP BY`, histogramas |
| pandas-profiling (ydata) | Relatórios automáticos Python |

### 3.5 Workflow recomendado

1. **Profile** fontes antes de modelar
2. **Documentar** anomalias e regras de negócio
3. **Definir** regras de transformação baseadas em findings
4. **Validar** pós-ETL com mesmas métricas
5. **Monitorizar** continuamente (data quality dashboards)

---

## 4. Deduplicação

### 4.1 Problema

Registos duplicados surgem por:

- Imports múltiplos sem controlo
- Cliente regista-se duas vezes com emails diferentes
- Merge de bases após aquisição
- Erros de digitação (João Silva vs Joao Silva)

### 4.2 Tipos de duplicados

| Tipo | Descrição |
|------|-----------|
| **Exact duplicate** | Todas as colunas iguais |
| **Partial duplicate** | Mesma chave natural, dados diferentes |
| **Fuzzy duplicate** | Registos similares mas não idênticos |

### 4.3 Estratégias

**1. Exact matching:**

```sql
SELECT *, COUNT(*) OVER (PARTITION BY nif) AS cnt
FROM clientes
HAVING cnt > 1
```

**2. Blocking + fuzzy matching:**

- **Blocking:** agrupar candidatos por prefixo (primeiras 3 letras do apelido + código postal)
- **Scoring:** similaridade Jaro-Winkler, Levenshtein, Soundex
- **Threshold:** score > 0,85 → provável duplicado

**3. Survivorship rules:**

Quando duplicados são identificados, qual registo "sobrevive"?

| Regra | Descrição |
|-------|-----------|
| **Most recent** | Mantém registo com `updated_at` mais recente |
| **Most complete** | Mantém registo com menos NULLs |
| **Master source** | CRM prevalece sobre Excel |
| **Merge** | Combinar campos não-nulos de ambos |

### 4.4 Algoritmo simplificado

```
1. Normalizar campos (lower, trim, remover acentos)
2. Calcular hash exacto → eliminar duplicados exactos
3. Blocking por chave fraca (nome + data_nascimento)
4. Para cada par no bloco: calcular score de similaridade
5. Score > threshold → marcar como duplicado
6. Aplicar survivorship → registo golden
7. Manter mapping duplicado → golden para auditoria
```

### 4.5 MDM (Master Data Management)

Abordagem enterprise para manter **golden record** por entidade (cliente, produto). Ferramentas: Informatica MDM, Talend MDM, open-source: dedupe.io.

---

## 5. Qualidade de dados — dimensões

Framework **TDQM (Total Data Quality Management):**

| Dimensão | Pergunta |
|----------|----------|
| **Accuracy** | Os valores reflectem a realidade? |
| **Completeness** | Todos os campos obrigatórios preenchidos? |
| **Consistency** | Coerente entre sistemas? |
| **Timeliness** | Actualizados a tempo? |
| **Uniqueness** | Sem duplicados indevidos? |
| **Validity** | Dentro do domínio/formato esperado? |

---

## 6. Pipeline completo — exemplo

```
Extract:
  - PostgreSQL vendas (incremental por updated_at)
  - CSV fornecedores (full diário)
  - API REST taxas câmbio (polling horário)

Transform:
  - Normalizar datas para ISO
  - Converter moedas para EUR (lookup taxas)
  - Validar NIF português
  - Deduplicar fornecedores (fuzzy por nome + NIF)
  - Derivar margem_bruta
  - Resolver FKs dimensionais

Load:
  - fact_vendas (incremental append)
  - dim_fornecedor (SCD Type 2)
  - Rejeitados → tabela erros_etl com motivo
```

---

## Exercícios

### Exercício 1
Uma tabela `pedidos` tem 50M linhas e coluna `updated_at`. O ETL corre de hora a hora. Descreva a estratégia de extract incremental e uma query SQL de exemplo.

### Exercício 2
Dados de profiling mostram que a coluna `telefone` tem 34% NULL, 12% com formato inválido e comprimentos entre 0 e 25 caracteres. Proponha três regras de transformação.

### Exercício 3
Dois registos de clientes:

| id | nome | email | nif |
|----|------|-------|-----|
| 101 | João Silva | joao@gmail.com | 123456789 |
| 205 | Joao Silva | joao.silva@gmail.com | 123456789 |

São duplicados? Que técnica usar e qual registo sobreviveria com regra "most complete"?

### Exercício 4
Calcule a completude global de um dataset com 3 colunas obrigatórias:

- Coluna A: 95% preenchida (10 000 registos)
- Coluna B: 88% preenchida
- Coluna C: 92% preenchida

Assuma independência e estime % de registos com **todas** as colunas preenchidas.

### Exercício 5
Escreva pseudocódigo para validar NIF português (9 dígitos, algoritmo de checksum mod 11).

### Exercício 6
Compare ETL tradicional com ELT moderno (dbt + Snowflake) para uma startup que carrega 100 GB/dia de logs JSON.

### Exercício 7
Um pipeline ETL processou 1M linhas; 15 000 foram rejeitadas; 850 000 carregadas; restantes?

### Exercício 8
Desenhe o fluxo de deduplicação para integrar duas bases de clientes (CRM e ERP) num golden record, incluindo blocking key e survivorship rule "CRM prevalece".

---

## Soluções

### Solução 1

**Estratégia:** incremental extract baseado em `updated_at` com watermark.

```sql
-- Guardar último watermark: 2024-06-15 14:00:00
SELECT *
FROM pedidos
WHERE updated_at > '2024-06-15 14:00:00'
  AND updated_at <= CURRENT_TIMESTAMP
ORDER BY updated_at;
```

Após extract bem-sucedido, actualizar watermark. Tratar:

- Registos com mesmo `updated_at` (usar id como desempate)
- Deletes (CDC ou flag `is_deleted`)
- Overlap window (extrair com margem de 5 min para late updates)

### Solução 2

1. **Normalização:** `REGEXP_REPLACE(telefone, '[^0-9+]', '')` — remover espaços, hífens
2. **Validação:** rejeitar se comprimento NOT IN (9, 13) para PT (+351XXXXXXXXX)
3. **Default:** se NULL e email válido → flag `telefone_ausente = true`; se inválido → NULL + log warning

Regra adicional: prefixar `+351` se 9 dígitos sem indicativo.

### Solução 3

**Sim, provável duplicado:**

- NIF idêntico (123456789) — match exacto forte
- Nome similar (João/Joao — diferença de acento)
- Email similar (joao@gmail.com vs joao.silva@gmail.com — mesmo domínio, prefixo relacionado)

**Técnica:** blocking por NIF → exact match confirma duplicado. Fuzzy no nome como reforço.

**Survivorship "most complete":**

| Campo | 101 | 205 |
|-------|-----|-----|
| nome | João Silva (com acento) | Joao Silva |
| email | joao@gmail.com | joao.silva@gmail.com |
| nif | 123456789 | 123456789 |

Registo **101** sobrevive (nome com acento correcto). Email: preferir o mais completo → `joao.silva@gmail.com` de 205 (merge rule).

Golden record: `{id: 101, nome: 'João Silva', email: 'joao.silva@gmail.com', nif: '123456789'}`

### Solução 4

Assumindo independência:

```
P(A ∧ B ∧ C) = 0,95 × 0,88 × 0,92 = 0,769 ≈ 76,9%
```

Registos completos: ~7 690 de 10 000.

Nota: na prática, NULLs correlacionam (registo incompleto tende a ter múltiplos NULLs), logo completude real seria **menor**.

### Solução 5

```
FUNÇÃO validar_nif(nif: string) → boolean:
  SE length(nif) ≠ 9 OU NOT is_numeric(nif) → RETORNAR false
  
  check_digit = int(nif[8])
  sum = 0
  PARA i = 0 ATÉ 7:
    sum += int(nif[i]) × (9 - i)
  
  remainder = sum MOD 11
  SE remainder == 0 OU remainder == 1:
    expected = 0
  SENÃO:
    expected = 11 - remainder
  
  RETORNAR check_digit == expected
```

### Solução 6

| Critério | ETL tradicional | ELT (dbt + Snowflake) |
|----------|-----------------|----------------------|
| Volume JSON | Parser externo necessário | VARIANT type nativo, parse in-warehouse |
| Flexibilidade schema | Pipeline rígido | Schema-on-read, iterar SQL |
| Custo compute | Servidor ETL dedicado | Pay-per-query Snowflake |
| Equipa | Especialistas ETL | Analistas SQL + dbt |
| Time-to-value | Semanas | Dias |

**Recomendação ELT** para startup: load raw JSON para Snowflake, transformar com dbt, sem infra ETL separada.

### Solução 7

```
1 000 000 - 15 000 (rejeitadas) - 850 000 (carregadas) = 135 000 linhas
```

As 135 000 restantes provavelmente são:

- Duplicados ignorados (já existiam no destino)
- Registos filtrados por regra de negócio (ex.: status = 'cancelado' excluído)
- Updates que não alteraram contagem (upsert)

Investigar logs ETL para categorizar.

### Solução 8

```
[CRM clientes] ──┐
                 ├──▶ [Staging unificado]
[ERP clientes] ──┘           │
                             ▼
                    [Normalização]
                    - lower(trim(nome))
                    - remover acentos
                    - pad NIF com zeros
                             │
                             ▼
                    [Blocking]
                    Key: primeiras 3 letras apelido + NIF
                             │
                             ▼
                    [Fuzzy matching]
                    Score Jaro-Winkler(nome) + exact(NIF)
                    Threshold: 0.85
                             │
                             ▼
                    [Survivorship: CRM prevalece]
                    Para cada cluster de duplicados:
                      - Base: registo CRM
                      - Preencher NULLs com valores ERP
                      - Manter CRM.id como golden_id
                             │
                             ▼
                    [Golden Record + Mapping Table]
                    golden_cliente / cliente_xref(crm_id, erp_id, golden_id)
```

---

## Referências

- Kimball, R. — *The Data Warehouse ETL Toolkit*
- Redman, T. — *Data Quality: The Field Guide*
- Great Expectations — https://greatexpectations.io
- OpenRefine — https://openrefine.org

**Próximo módulo:** [05 — XML e NoSQL](./05-xml-nosql.md)
