# Módulo 05 — XML, XPath, XQuery e NoSQL

**UC:** Modelação e Integração de Dados · **Fase 2** · **Tempo sugerido:** 5–7 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Compreender a estrutura e validação de documentos XML
- Escrever consultas básicas em XPath e XQuery
- Diferenciar os quatro tipos principais de bases de dados NoSQL
- Escolher entre SQL e NoSQL consoante requisitos de dados e consultas
- Integrar fontes XML e NoSQL em pipelines de dados

---

## 1. XML — eXtensible Markup Language

### 1.1 Estrutura

XML é uma linguagem de marcação que define regras para codificar documentos legíveis por humanos e máquinas. Combina **dados** com **metadados** (tags).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<biblioteca xmlns="http://exemplo.pt/biblioteca">
  <livro isbn="978-0132350884">
    <titulo>Clean Code</titulo>
    <autor>Robert Martin</autor>
    <preco moeda="EUR">42.50</preco>
    <publicacao ano="2008"/>
  </livro>
</biblioteca>
```

**Componentes:**

| Elemento | Descrição |
|----------|-----------|
| **Element** | `<tag>conteúdo</tag>` |
| **Attribute** | `isbn="..."` — metadado do elemento |
| **Text node** | Conteúdo textual entre tags |
| **Namespace** | `xmlns` — evitar conflitos de nomes |
| **Prolog** | `<?xml version="1.0"?>` |

### 1.2 Documento vs elemento vs atributo

- **Elemento:** unidade estrutural (livro, titulo)
- **Atributo:** propriedade do elemento (isbn, moeda, ano)
- Regra prática: dados que se repetem ou têm estrutura → elementos; metadados simples → atributos

### 1.3 Validação

**DTD (Document Type Definition):** gramática simples

**XSD (XML Schema Definition):** tipos, restrições, namespaces — standard moderno

```xml
<!-- Exemplo XSD simplificado -->
<xs:element name="livro">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="titulo" type="xs:string"/>
      <xs:element name="preco" type="xs:decimal"/>
    </xs:sequence>
    <xs:attribute name="isbn" type="xs:string" use="required"/>
  </xs:complexType>
</xs:element>
```

**Well-formed vs Valid:**

- Well-formed: sintaxe XML correcta
- Valid: conforme XSD/DTD

---

## 2. XPath

### 2.1 Definição

**XPath (XML Path Language)** é uma linguagem para navegar e seleccionar nós num documento XML. Base para XQuery, XSLT e muitas APIs.

### 2.2 Tipos de nós

| Tipo | Exemplo |
|------|---------|
| Root | `/` |
| Element | `livro`, `titulo` |
| Attribute | `@isbn`, `@moeda` |
| Text | texto dentro de `<titulo>` |
| Comment | `<!-- comentário -->` |

### 2.3 Expressões XPath essenciais

| Expressão | Significado |
|-----------|-------------|
| `/biblioteca/livro` | Todos os livros directos |
| `//livro` | Todos os livros em qualquer profundidade |
| `livro[@isbn='978-0132350884']` | Livro com isbn específico |
| `livro/preco/@moeda` | Atributo moeda do preço |
| `livro[preco > 40]` | Livros com preço > 40 |
| `livro[1]` | Primeiro livro |
| `livro[last()]` | Último livro |
| `//autor/text()` | Texto de todos os autores |

### 2.4 Exemplos

Dado o XML da secção 1.1:

```xpath
//livro/titulo                    → "Clean Code"
//livro[@isbn='978-0132350884']/preco  → "42.50"
//livro[preco > 40]/titulo        → títulos de livros caros
count(//livro)                    → 1
```

### 2.5 XPath vs CSS selectors

XPath é mais expressivo (parent, ancestor, preceding-sibling). Usado em XML; CSS selectors dominam HTML web.

---

## 3. XQuery

### 3.1 Definição

**XQuery** é uma linguagem funcional para consultar e transformar coleções de documentos XML. Superset de XPath 2.0.

### 3.2 Estrutura FLWOR

Analogia com SQL:

| XQuery | SQL |
|--------|-----|
| **FOR** | FROM |
| **LET** | variável / WITH |
| **WHERE** | WHERE |
| **ORDER BY** | ORDER BY |
| **RETURN** | SELECT |

### 3.3 Exemplos

```xquery
(: Listar títulos de livros caros :)
for $livro in //livro
where $livro/preco > 40
return $livro/titulo/text()

(: Construir novo XML :)
for $livro in //livro
where $livro/publicacao/@ano > 2000
return
  <livro-recente isbn="{$livro/@isbn}">
    <nome>{ $livro/titulo/text() }</nome>
    <preco-eur>{ $livro/preco/text() }</preco-eur>
  </livro-recente>

(: Agregação :)
let $livros := //livro
return
  <estatisticas>
    <total>{ count($livros) }</total>
    <preco-medio>{ avg($livros/preco) }</preco-medio>
  </estatisticas>
```

### 3.4 XQuery vs SQL

| Aspeto | XQuery | SQL |
|--------|--------|-----|
| Modelo | Hierárquico (XML) | Relacional (tabelas) |
| Schema | Flexível | Fixo |
| Joins | Descendentes, FLWOR | JOIN explícito |
| Output | XML, texto, JSON | Tabelas |

---

## 4. Transformações XSLT (referência)

**XSLT (Extensible Stylesheet Language Transformations)** transforma XML → XML, HTML ou texto. Usado em integração B2B e publicação.

```xml
<xsl:template match="livro">
  <tr>
    <td><xsl:value-of select="titulo"/></td>
    <td><xsl:value-of select="preco"/></td>
  </tr>
</xsl:template>
```

---

## 5. Bases de dados NoSQL

### 5.1 Motivação

Limitações do modelo relacional para certos casos:

- Esquema rígido dificulta evolução rápida
- Joins caros em escala horizontal (sharding)
- Dados semi-estruturados mal adaptados a normalização
- Latência ultra-baixa para acesso por chave

**Teorema CAP:** num sistema distribuído, só se podem garantir 2 de 3: **C**onsistency, **A**vailability, **P**artition tolerance.

### 5.2 Taxonomia — 4 tipos principais

```
NoSQL
├── Document stores
├── Key-value stores
├── Column-family stores
└── Graph databases
```

---

## 6. Document stores

### 6.1 Modelo

Documentos auto-contidos (JSON, BSON, XML) agrupados em **collections**. Esquema flexível — documentos na mesma collection podem ter campos diferentes.

### 6.2 Exemplo (MongoDB)

```javascript
// Collection: clientes
{
  "_id": ObjectId("..."),
  "nome": "Ana Silva",
  "email": "ana@email.pt",
  "morada": {
    "rua": "Rua das Flores, 12",
    "cidade": "Lisboa"
  },
  "tags": ["premium", "newsletter"]
}
```

### 6.3 Consultas

```javascript
db.clientes.find({ "morada.cidade": "Lisboa", "tags": "premium" })
db.clientes.aggregate([
  { $match: { "morada.cidade": "Lisboa" } },
  { $group: { _id: "$tags", count: { $sum: 1 } } }
])
```

### 6.4 Quando usar

- Conteúdo com estrutura variável (catálogos, perfis)
- Desenvolvimento ágil (schema evolution)
- APIs que devolvem JSON nativamente
- **Exemplos:** MongoDB, CouchDB, Firestore

### 6.5 Limitações

- Joins limitados ($lookup caro)
- Transacções multi-documento (suporte recente, com custo)
- Consistência eventual em clusters

---

## 7. Key-value stores

### 7.1 Modelo

Mapa simples: **chave → valor** opaco. Sem esquema, sem consultas complexas — apenas get/put/delete por chave.

### 7.2 Exemplo (Redis)

```
SET user:1001 '{"nome":"Ana","idade":28}'
GET user:1001
EXPIRE session:abc123 3600
INCR pageviews:homepage
```

### 7.3 Quando usar

- Cache de sessões e resultados
- Contadores em tempo real
- Filas simples (LIST, STREAM)
- Feature flags, rate limiting
- **Exemplos:** Redis, DynamoDB (modo KV), Riak, etcd

### 7.4 Limitações

- Sem queries secundárias (sem índice = sem busca)
- Valor opaco — lógica no cliente
- Modelação de relações complexa

---

## 8. Column-family stores (wide-column)

### 8.1 Modelo

Dados organizados por **row key** com **column families** — milhões de colunas sparse por linha. Optimizado para writes distribuídos e leituras por row key ou range scan.

### 8.2 Exemplo (Cassandra)

```sql
CREATE TABLE sensor_readings (
  sensor_id UUID,
  timestamp TIMESTAMP,
  temperature DOUBLE,
  humidity DOUBLE,
  PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

Cada `(sensor_id, timestamp)` é uma row; colunas temperature/humidity pertencem à family default.

### 8.3 Quando usar

- Time-series (IoT, métricas, logs)
- Write-heavy workloads distribuídos
- Dados sparse com muitas colunas possíveis
- **Exemplos:** Apache Cassandra, HBase, ScyllaDB

### 8.4 Limitações

- Modelagem query-driven (desenhar tabelas pelas queries)
- Joins inexistentes
- Eventual consistency por defeito

---

## 9. Graph databases

### 9.1 Modelo

**Nós** (entidades) e **arestas** (relações) com propriedades. Optimizado para traversals — "amigos de amigos", caminhos mais curtos, detecção de comunidades.

### 9.2 Exemplo (Neo4j — Cypher)

```cypher
CREATE (a:Pessoa {nome: 'Ana'})-[:CONHECE {desde: 2020}]->(b:Pessoa {nome: 'Bruno'})
CREATE (b)-[:TRABALHA_EM]->(e:Empresa {nome: 'TechCorp'})

MATCH (p:Pessoa {nome: 'Ana'})-[:CONHECE*1..2]-(outro)
RETURN outro.nome
```

### 9.3 Quando usar

- Redes sociais, recomendações
- Detecção de fraude (grafos de transacções)
- Knowledge graphs, ontologias
- IT dependency mapping
- **Exemplos:** Neo4j, Amazon Neptune, ArangoDB

### 9.4 Limitações

- Não optimizado para agregações tabulares massivas
- Escala horizontal mais complexa que KV/column
- Curva de aprendizagem (modelação de grafos)

---

## 10. SQL vs NoSQL — decisão

| Critério | SQL (RDBMS) | NoSQL |
|----------|-------------|-------|
| Esquema | Fixo, normalizado | Flexível |
| Escala | Vertical (+ read replicas) | Horizontal (sharding nativo) |
| Transacções ACID | Completas | Variável (document: sim; KV: limitado) |
| Joins | Nativos, optimizados | Limitados ou inexistentes |
| Consultas ad-hoc | SQL expressivo | Query-driven design |
| Consistência | Forte | Eventual (muitos) |

**Regra prática:** SQL para dados transaccionais com relações complexas; NoSQL para escala, flexibilidade de esquema ou padrões de acesso específicos (KV lookup, time-series, graph traversal).

---

## Exercícios

### Exercício 1
Escreva expressões XPath para o XML da secção 1.1:

a) Seleccionar todos os ISBNs  
b) Livros publicados após 2005  
c) Valor textual do título do livro com isbn 978-0132350884  

### Exercício 2
Escreva uma query XQuery FLWOR que devolva XML com título e preço de todos os livros com preço inferior a 50 EUR.

### Exercício 3
Classifique cada caso de uso com o tipo NoSQL mais adequado (document, key-value, column, graph):

a) Cache de sessões web com TTL  
b) Perfil de utilizador com campos opcionais  
c) Rede de conexões LinkedIn  
d) Métricas de sensores IoT (1M writes/seg)  

### Exercício 4
Uma aplicação e-commerce tem produtos (relacional), carrinho (sessão) e recomendações ("quem comprou X também comprou Y"). Proponha tecnologia SQL/NoSQL para cada componente.

### Exercício 5
Explique porque column-family stores são adequadas para time-series mas inadequadas para queries ad-hoc com múltiplos filtros arbitrários.

### Exercício 6
Converta o seguinte JSON para XML equivalente:

```json
{
  "encomenda": {
    "id": "E001",
    "itens": [
      {"produto": "Teclado", "qtd": 2},
      {"produto": "Rato", "qtd": 1}
    ]
  }
}
```

### Exercício 7
MongoDB e PostgreSQL JSONB ambos armazenam JSON. Compare-os em: esquema, joins, transacções e casos de uso.

### Exercício 8
Num sistema CAP, durante uma partition de rede, uma base Cassandra escolhe AP (availability + partition tolerance). O que acontece à consistência? Dê um exemplo concreto.

---

## Soluções

### Solução 1

```xpath
a) //livro/@isbn
b) //livro[publicacao/@ano > 2005]
c) //livro[@isbn='978-0132350884']/titulo/text()
```

### Solução 2

```xquery
for $livro in //livro
where $livro/preco < 50
return
  <livro-barato isbn="{$livro/@isbn}">
    <titulo>{ $livro/titulo/text() }</titulo>
    <preco>{ $livro/preco/text() }</preco>
  </livro-barato>
```

### Solução 3

| Caso | Tipo NoSQL |
|------|------------|
| a) Cache sessões TTL | **Key-value** (Redis) |
| b) Perfil campos opcionais | **Document** (MongoDB) |
| c) Rede LinkedIn | **Graph** (Neo4j) |
| d) Métricas IoT 1M/s | **Column-family** (Cassandra) |

### Solução 4

| Componente | Tecnologia | Justificação |
|------------|------------|--------------|
| Produtos | **PostgreSQL** | Relacional, transacções, stock, preços |
| Carrinho | **Redis** (KV) | Sessão efémera, TTL, alta velocidade |
| Recomendações | **Neo4j** (graph) ou **Redis** (pre-computed) | Graph para calcular relações; cache KV para servir |

Arquitectura poliglota — cada store optimizado para o padrão de acesso.

### Solução 5

Column-family stores organizam dados por **row key** com acesso optimizado por essa chave (+ clustering columns). Leitura eficiente: `WHERE sensor_id = X AND timestamp BETWEEN A AND B`.

Queries ad-hoc com filtros arbitrários (ex.: `WHERE humidity > 80 AND city = 'Porto'`) requerem **secondary indexes** ou **full scan** — ambos caros em escala.

Modelagem é **query-driven:** criar tabela por padrão de acesso. Sem joins, sem flexibilidade ad-hoc — trade-off consciente por write throughput.

### Solução 6

```xml
<?xml version="1.0" encoding="UTF-8"?>
<encomenda id="E001">
  <itens>
    <item>
      <produto>Teclado</produto>
      <qtd>2</qtd>
    </item>
    <item>
      <produto>Rato</produto>
      <qtd>1</qtd>
    </item>
  </itens>
</encomenda>
```

### Solução 7

| Critério | MongoDB | PostgreSQL JSONB |
|----------|---------|------------------|
| Esquema | Flexível por documento | JSONB em tabela relacional fixa |
| Joins | $lookup (limitado, caro) | JOIN nativo com tabelas relacionais |
| Transacções | Multi-doc (desde v4.0) | ACID completo |
| Casos de uso | App-centric, escala horizontal | Dados híbridos relacional + JSON, analytics SQL |

Escolher PostgreSQL JSONB quando JSON é parte de um modelo maior com relações; MongoDB quando documento é a unidade fundamental.

### Solução 8

Com **AP**, durante partition:

- Sistema continua **disponível** (accepts reads/writes)
- **Consistência** degradada → **consistência eventual**

Exemplo concreto:

1. Cliente A escreve `saldo = 100` no nó Lisboa
2. Partition isola Lisboa de Porto
3. Cliente B lê no nó Porto → obtém `saldo = 80` (valor stale)
4. Partition curada → **gossip protocol** reconcilia (last-write-wins ou vector clocks)

Risco: leituras de dados desactualizados até reconciliação — aceitável para métricas IoT, problemático para saldos bancários.

---

## Referências

- W3C XPath 3.1 / XQuery 3.1 Specifications
- MongoDB Manual — Data Modeling
- Kleppmann, M. — *Designing Data-Intensive Applications* (Cap. CAP, NoSQL)
- Neo4j Graph Academy

**Próximo módulo:** [06 — Modelo Multidimensional e Data Warehouse](./06-modelo-multidimensional-dw.md)
