# Módulo 06 — Modelo Multidimensional e Data Warehouse

**UC:** Modelação e Integração de Dados · **Fase 3** · **Tempo sugerido:** 6–8 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Compreender o modelo multidimensional (cubos OLAP)
- Diferenciar esquemas estrela (star) e floco de neve (snowflake)
- Identificar tabelas de factos e dimensões
- Aplicar tipos de Slowly Changing Dimensions (SCD)
- Desenhar um data warehouse dimensional para um caso de negócio

---

## 1. Data Warehouse — revisão

Um **Data Warehouse (DW)** é um repositório de dados integrados, orientado a subject areas, variante no tempo e não volátil, optimizado para **consultas analíticas (OLAP)** e não para transacções (OLTP).

```
OLTP (normalizado)          DW (dimensional)
├── Muitas tabelas          ├── Poucas tabelas largas
├── Writes frequentes       ├── Reads pesados
├── 3NF                     ├── Star/Snowflake
└── Dados actuais           └── Histórico
```

---

## 2. Modelo multidimensional

### 2.1 Conceito

Os dados são organizados como um **cubo multidimensional** onde:

- **Dimensões** são eixos de análise (tempo, produto, cliente, loja)
- **Medidas (measures)** são valores numéricos agregáveis (vendas, quantidade, margem)
- **Factos** são eventos de negócio registados nas intersecções das dimensões

```
                    Produto
                       │
          ┌────────────┼────────────┐
          │            │            │
       Tempo ──────── VENDAS ────── Loja
          │         (facto)         │
          └────────────┼────────────┘
                       │
                    Cliente
```

### 2.2 Operadores mentais

Analistas "fatiam" o cubo:

- Por **tempo:** vendas em Q1 2024
- Por **produto:** vendas de laptops
- Por **loja + tempo:** vendas do Porto em Junho

---

## 3. Tabelas de factos

### 3.1 Definição

A **tabela de factos** regista eventos de negócio ao nível de granularidade mais baixo (fine-grained). Contém:

- **Chaves estrangeiras** para dimensões (surrogate keys)
- **Medidas** numéricas (additive, semi-additive, non-additive)
- Opcionalmente **degenerate dimensions** (número de encomenda, linha)

### 3.2 Exemplo: fact_vendas

```sql
CREATE TABLE fact_vendas (
  venda_sk        BIGINT PRIMARY KEY,  -- surrogate key
  data_sk         INT NOT NULL,        -- FK → dim_data
  produto_sk      INT NOT NULL,        -- FK → dim_produto
  cliente_sk      INT NOT NULL,        -- FK → dim_cliente
  loja_sk         INT NOT NULL,        -- FK → dim_loja
  -- Medidas
  quantidade      INT NOT NULL,
  valor_venda     DECIMAL(12,2) NOT NULL,
  valor_custo     DECIMAL(12,2) NOT NULL,
  margem          DECIMAL(12,2) NOT NULL,
  -- Degenerate
  num_encomenda   VARCHAR(20)
);
```

### 3.3 Tipos de medidas

| Tipo | Descrição | Exemplo | Agregável com SUM? |
|------|-----------|---------|-------------------|
| **Additive** | Soma em todas as dimensões | quantidade, valor | Sim |
| **Semi-additive** | Soma em algumas dimensões | saldo stock (não somar tempo) | Parcial |
| **Non-additive** | Não somável | rácio margem %, preço unitário | Não (média ponderada) |

### 3.4 Tipos de factos

| Tipo | Granularidade | Exemplo |
|------|---------------|---------|
| **Transaction** | Uma linha por evento | fact_vendas (linha de venda) |
| **Periodic snapshot** | Uma linha por período | fact_stock_diario |
| **Accumulating snapshot** | Milestones de processo | fact_encomenda (pedido→envio→entrega) |
| **Factless** | Sem medida numérica | fact_presencas (evento ocorreu sim/não) |

### 3.5 Granularidade

A **granularidade** define o que cada linha representa:

- "Uma linha por linha de venda" → SUM(valor) = total vendas ✓
- "Uma linha por dia/produto/loja (pré-agregado)" → perde detalhe de cliente

**Regra:** definir granularidade antes de tudo; é a decisão mais importante do DW.

---

## 4. Tabelas de dimensões

### 4.1 Definição

**Dimensões** descrevem o contexto dos factos — respondem a "quem, o quê, onde, quando, como". Contêm atributos descritivos para filtrar, agrupar e rotular.

### 4.2 Exemplo: dim_produto

```sql
CREATE TABLE dim_produto (
  produto_sk      INT PRIMARY KEY,       -- surrogate key
  produto_id      VARCHAR(20) NOT NULL,  -- natural key (negócio)
  nome            VARCHAR(100) NOT NULL,
  categoria       VARCHAR(50),
  subcategoria    VARCHAR(50),
  marca           VARCHAR(50),
  preco_lista     DECIMAL(10,2),
  -- SCD Type 2
  valid_from      DATE NOT NULL,
  valid_to        DATE,                  -- NULL = actual
  is_current      BOOLEAN DEFAULT true
);
```

### 4.3 Surrogate keys vs natural keys

| Aspeto | Surrogate key (SK) | Natural key (NK) |
|--------|-------------------|------------------|
| Tipo | Inteiro auto-increment | Código de negócio |
| Mudanças | Imutável | Pode mudar (SCD) |
| Performance | Joins inteiros, compactos | Strings, compostas |
| Fontes múltiplas | Unifica IDs diferentes | Conflitos possíveis |

**Best practice:** usar surrogate keys nas dimensões; manter natural key como atributo.

### 4.4 Dimensões comuns

| Dimensão | Atributos típicos |
|----------|-------------------|
| **Tempo (dim_data)** | dia, mês, trimestre, ano, feriado, fim_semana |
| **Produto** | nome, categoria, marca, preço |
| **Cliente** | nome, segmento, cidade, país |
| **Loja** | nome, região, tipo, m² |
| **Funcionário** | nome, departamento, cargo |

### 4.5 Dimensão conformada (conformed dimension)

Mesma dimensão partilhada por múltiplos fact tables ou data marts — garante consistência ("Cliente" significa o mesmo em vendas e reclamações).

### 4.6 Role-playing dimensions

A mesma dimensão usada com papéis diferentes:

- `dim_data` como **data_pedido** e **data_entrega** no mesmo fact table
- Solução: views ou aliases (`dim_data_pedido`, `dim_data_entrega`)

### 4.7 Junk dimensions

Agrupar flags/indicadores booleanos de baixa cardinalidade numa dimensão artificial:

```sql
dim_indicadores_venda (ind_sk, promo_flag, online_flag, devolucao_flag)
-- Combinações: 2×2×2 = 8 linhas
```

---

## 5. Star schema vs Snowflake schema

### 5.1 Star schema (esquema estrela)

Fact table central rodeada por dimensões **desnormalizadas** (flat).

```
                    dim_produto
                         │
dim_cliente ──── fact_vendas ──── dim_loja
                         │
                    dim_data
```

**Vantagens:**

- Queries simples (menos joins)
- Performance superior (menos joins)
- Intuitivo para utilizadores de BI

**Desvantagens:**

- Redundância de dados nas dimensões
- Actualização de atributos afecta mais linhas

### 5.2 Snowflake schema (floco de neve)

Dimensões **normalizadas** em sub-dimensões hierárquicas.

```
dim_produto → dim_categoria → dim_familia
     │
fact_vendas
     │
dim_loja → dim_regiao → dim_pais
```

**Vantagens:**

- Menos redundância
- Integridade referencial
- Dimensões hierárquicas claras

**Desvantagens:**

- Mais joins → queries mais complexas
- Performance inferior (mais tabelas)

### 5.3 Comparação

| Critério | Star | Snowflake |
|----------|------|-----------|
| Joins | Poucos | Muitos |
| Redundância | Alta | Baixa |
| Performance BI | Superior | Inferior |
| Manutenção dimensões | Simples | Normalizada |
| Uso típico | Kimball, BI self-service | Inmon, dimensões muito grandes |

**Regra Kimball:** preferir star; snowflake apenas quando dimensão é enorme e hierarquia profunda.

---

## 6. Slowly Changing Dimensions (SCD)

Dimensões mudam ao longo do tempo (cliente muda de cidade, produto muda de categoria). SCD define **como** registar essas mudanças.

### 6.1 SCD Type 0 — Retain original

Atributo **nunca muda** após carga inicial.

```
data_nascimento → imutável
```

### 6.2 SCD Type 1 — Overwrite

Actualiza valor **in-place**, perde histórico.

```sql
UPDATE dim_cliente
SET cidade = 'Porto', updated_at = NOW()
WHERE cliente_id = 'C001' AND is_current = true;
```

**Quando:** correções de erros, atributos sem valor histórico (email actual).

### 6.3 SCD Type 2 — Add new row (mais comum)

Nova linha com novo surrogate key; linha anterior fechada.

```sql
-- Antes
| cliente_sk | cliente_id | cidade  | valid_from | valid_to   | is_current |
| 101        | C001       | Lisboa  | 2020-01-01 | NULL       | true       |

-- Cliente muda para Porto (2024-06-01)
-- Step 1: fechar linha actual
UPDATE dim_cliente SET valid_to = '2024-05-31', is_current = false
WHERE cliente_sk = 101;

-- Step 2: inserir nova linha
INSERT INTO dim_cliente (cliente_sk, cliente_id, cidade, valid_from, valid_to, is_current)
VALUES (102, 'C001', 'Porto', '2024-06-01', NULL, true);
```

**Quando:** histórico completo necessário (auditoria, análise temporal).

Fact table mantém FK para SK correcto → vendas antigas apontam para Lisboa, novas para Porto.

### 6.4 SCD Type 3 — Add new column

Mantém valor **actual** e **anterior** em colunas separadas.

```sql
| cliente_sk | cidade_actual | cidade_anterior | data_mudanca |
| 101        | Porto         | Lisboa          | 2024-06-01   |
```

**Quando:** apenas última mudança importa (limitado a 1 versão anterior).

### 6.5 SCD Type 4 — Mini-dimension

Atributos voláteis (ex.: preço) movidos para mini-dimension separada com histórico, mantendo dimensão principal estável.

### 6.6 SCD Type 6 — Hybrid (1+2+3)

Combina overwrite de atributos actuais com histórico completo — complexo, raro.

### 6.7 Resumo

| Tipo | Histórico | Complexidade | Uso |
|------|-----------|--------------|-----|
| 0 | Não | Mínima | Imutável |
| 1 | Não | Baixa | Overwrite |
| 2 | Completo | Alta | **Mais comum** |
| 3 | 1 versão | Média | Actual + anterior |
| 4 | Mini-dim | Média | Atributos voláteis |

---

## 7. Processo de desenho dimensional

### 7.1 Metodologia Kimball (4 passos)

1. **Seleccionar processo de negócio** (vendas, inventário, RH)
2. **Declarar granularidade** (linha de venda, snapshot diário)
3. **Identificar dimensões** (quem, o quê, onde, quando)
4. **Identificar factos/medidas** (quanto, quantos)

### 7.2 Exemplo: processo de vendas

```
1. Processo: registo de venda
2. Granularidade: uma linha por item de linha de venda
3. Dimensões: data, produto, cliente, loja, vendedor, promoção
4. Factos: quantidade, valor_venda, valor_custo, margem, desconto
```

---

## 8. Data marts

Subconjunto do DW focado numa área de negócio:

- **Dependente:** extrai do DW enterprise (Inmon)
- **Independente:** construído directamente das fontes (Kimball)

Kimball recomenda **data marts dimensionais** como blocos de construção do DW.

---

## Exercícios

### Exercício 1
Identifique dimensões, medidas e granularidade para um fact table de **reclamações de clientes**.

### Exercício 2
Desenhe um star schema (tabelas e FKs) para vendas de uma cadeia de retalho com: lojas, produtos, clientes, datas e promoções.

### Exercício 3
Uma medida `taxa_margem = margem / valor_venda` está num fact table. É additive, semi-additive ou non-additive? Como agregar correctamente por região?

### Exercício 4
Cliente C001 muda de segmento "Standard" para "Premium" a 2024-03-15. Implemente SCD Type 2 mostrando estado antes e depois.

### Exercício 5
Compare star e snowflake para uma dim_produto com 2M linhas, hierarquia família→categoria→produto, e 50 queries BI diárias.

### Exercício 6
O que é uma dimensão conformada? Dê exemplo com dim_tempo partilhada por fact_vendas e fact_inventario.

### Exercício 7
fact_stock_diario regista stock à meia-noite. A medida `stock_unidades` é additive? Justifique.

### Exercício 8
Uma empresa quer saber "vendas por categoria de produto **tal como era categorizado na data da venda**". Que tipo SCD é necessário na dim_produto e porquê?

---

## Soluções

### Solução 1

| Elemento | Valor |
|----------|-------|
| **Granularidade** | Uma linha por reclamação individual |
| **Dimensões** | data (abertura/resolução), cliente, produto, loja, tipo_reclamação, canal, agente |
| **Medidas** | tempo_resolucao_horas (non-additive avg), valor_compensacao (additive), num_reclamacoes (additive count) |
| **Degenerate** | num_ticket |

### Solução 2

```sql
-- Dimensões
dim_data (data_sk, data, dia, mes, trimestre, ano, feriado)
dim_produto (produto_sk, produto_id, nome, categoria, marca)
dim_cliente (cliente_sk, cliente_id, nome, segmento, cidade)
dim_loja (loja_sk, loja_id, nome, regiao, tipo)
dim_promocao (promo_sk, promo_id, descricao, desconto_pct)

-- Fact
fact_vendas (
  venda_sk, data_sk, produto_sk, cliente_sk, loja_sk, promo_sk,
  quantidade, valor_venda, valor_custo, margem, desconto
)

-- FKs: fact_vendas.data_sk → dim_data.data_sk (etc.)
```

Star schema: fact central, 5 dimensões desnormalizadas.

### Solução 3

**Non-additive** — rácio não se soma meaningfully.

Agregação correcta por região:

```sql
SELECT regiao,
       SUM(margem) / SUM(valor_venda) AS taxa_margem
FROM fact_vendas f
JOIN dim_loja l ON f.loja_sk = l.loja_sk
GROUP BY regiao;
```

Média das taxas individuais seria incorrecta (média de médias).

### Solução 4

**Antes:**

| cliente_sk | cliente_id | segmento | valid_from | valid_to | is_current |
|------------|------------|----------|------------|----------|------------|
| 50 | C001 | Standard | 2022-01-01 | NULL | true |

**Depois (SCD Type 2):**

| cliente_sk | cliente_id | segmento | valid_from | valid_to | is_current |
|------------|------------|----------|------------|----------|------------|
| 50 | C001 | Standard | 2022-01-01 | 2024-03-14 | false |
| 51 | C001 | Premium | 2024-03-15 | NULL | true |

Vendas antes de 15/03 → FK cliente_sk=50. Vendas após → FK cliente_sk=51.

### Solução 5

**Star schema recomendado** porque:

- 50 queries BI/dia beneficiam de menos joins
- 2M linhas é gerível desnormalizado (categoria inline)
- Hierarquia família→categoria→produto pode ser atributos flat (familia, categoria, produto_nome)
- Snowflake só se categoria/família forem partilhadas por muitas dimensões e redundância for problemática

Snowflake se: família/categoria mudam frequentemente e normalização reduz storage significativamente.

### Solução 6

**Dimensão conformada:** mesma tabela `dim_data` (mesmos surrogate keys, mesmos atributos) referenciada por múltiplos fact tables.

```
fact_vendas.data_sk ──→ dim_data ←── fact_inventario.data_sk
```

Benefício: "Q1 2024" significa exactamente o mesmo período em vendas e inventário; joins cross-fact possíveis.

### Solução 7

**Semi-additive.**

- SUM por produto ou loja: **sim** (stock total de todos os produtos numa loja)
- SUM por tempo: **não** (somar stock de 30 dias ≠ stock actual)
- Agregação temporal correcta: último valor do período ou média

```sql
-- Stock total actual por loja (último snapshot)
SELECT loja_sk, stock_unidades
FROM fact_stock_diario
WHERE data_sk = (SELECT MAX(data_sk) FROM fact_stock_diario);
```

### Solução 8

**SCD Type 2** na dim_produto.

Motivo: categoria muda ao longo do tempo (produto reclassificado). Para analisar vendas históricas com categorização **da época**, cada versão da dimensão deve reflectir categoria vigente na data.

Fact table mantém FK para produto_sk correcto → venda de 2023 aponta para SK com categoria antiga; venda de 2024 aponta para SK com categoria nova.

SCD Type 1 perderia histórico; Type 3 só guarda 1 versão anterior (insuficiente).

---

## Referências

- Kimball, R. & Ross, M. — *The Data Warehouse Toolkit* (3rd ed.)
- Inmon, W.H. — *Building the Data Warehouse*
- Kimball Group — Dimensional Modeling Techniques

**Próximo módulo:** [07 — OLAP, ETL DW e MDX](./07-olap-etl-dw-mdx.md)
