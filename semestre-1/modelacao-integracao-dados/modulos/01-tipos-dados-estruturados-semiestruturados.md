# Módulo 01 — Tipos de Dados: Estruturados, Semiestruturados e Não Estruturados

**UC:** Modelação e Integração de Dados · **Fase 1** · **Tempo sugerido:** 4–6 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverá ser capaz de:

- Diferenciar dados estruturados, semiestruturados e não estruturados
- Compreender os formatos JSON, XML e CSV e as suas características
- Escolher o formato e o tipo de armazenamento adequados a cada cenário
- Identificar desafios de integração associados a cada categoria

---

## 1. Introdução

Os sistemas de informação modernos recolhem dados de fontes heterogéneas: bases de dados relacionais, APIs REST, ficheiros de log, imagens, sensores IoT, e-mails, documentos PDF, entre outros. Antes de integrar ou modelar estes dados, é fundamental classificá-los quanto ao **grau de estrutura**, pois isso determina as ferramentas de processamento, o custo de armazenamento e a complexidade das consultas.

---

## 2. Dados estruturados

### 2.1 Definição

Dados **estruturados** seguem um esquema fixo e predefinido. Cada registo tem o mesmo conjunto de campos, com tipos de dados bem definidos (inteiro, decimal, data, texto com comprimento fixo, etc.). A estrutura é conhecida **antes** da inserção dos dados.

### 2.2 Características

| Característica | Descrição |
|----------------|-----------|
| Esquema rígido | Colunas e tipos definidos à priori |
| Consultas eficientes | SQL, índices B-tree, joins otimizados |
| Integridade | Constraints (PK, FK, NOT NULL, CHECK) |
| Escalabilidade vertical | Tradicionalmente limitada a um servidor |

### 2.3 Exemplos

- Tabelas em bases de dados relacionais (PostgreSQL, MySQL, Oracle)
- Ficheiros CSV com cabeçalho fixo e colunas consistentes
- Folhas de cálculo com colunas tipadas de forma uniforme
- Registos de transações bancárias (conta, valor, data, tipo)

### 2.4 Formato CSV (Comma-Separated Values)

O **CSV** é um formato tabular simples em texto plano:

```csv
id,nome,idade,cidade
1,Ana Silva,28,Lisboa
2,Bruno Costa,35,Porto
3,Carla Mendes,42,Coimbra
```

**Vantagens:** universal, legível, compatível com Excel e ferramentas ETL.  
**Desvantagens:** sem tipos nativos, sem relações, problemas com vírgulas dentro de campos, sem metadados.

**Quando usar CSV:** troca de dados entre sistemas, exportações de relatórios, datasets pequenos/médios para análise, integração com ferramentas de BI.

---

## 3. Dados semiestruturados

### 3.1 Definição

Dados **semiestruturados** possuem alguma estrutura, mas **não obedecem a um esquema rígido**. Podem ter campos opcionais, listas de comprimento variável, estruturas aninhadas ou tags que auto-descrevem o conteúdo. O esquema pode evoluir sem migração formal.

### 3.2 Características

| Característica | Descrição |
|----------------|-----------|
| Esquema flexível | Campos podem variar entre documentos |
| Auto-descritivo | Tags/chaves identificam o significado |
| Aninhamento | Objetos dentro de objetos, arrays |
| Consultas especializadas | XPath, XQuery, JSONPath, operadores NoSQL |

### 3.3 Formato JSON (JavaScript Object Notation)

```json
{
  "id": 1001,
  "cliente": {
    "nome": "Ana Silva",
    "contactos": ["ana@email.pt", "+351912345678"]
  },
  "encomendas": [
    {"produto": "Laptop", "valor": 899.99},
    {"produto": "Rato", "valor": 29.99}
  ],
  "ativo": true
}
```

**Vantagens:** leve, nativo em APIs REST, fácil parsing em todas as linguagens.  
**Desvantagens:** sem comentários nativos, sem schema enforcement (salvo JSON Schema), joins complexos.

**Quando usar JSON:** APIs web, configurações de aplicações, logs estruturados, bases de dados documentais (MongoDB), mensagens em filas (Kafka).

### 3.4 Formato XML (eXtensible Markup Language)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cliente id="1001">
  <nome>Ana Silva</nome>
  <contactos>
    <email>ana@email.pt</email>
    <telefone>+351912345678</telefone>
  </contactos>
  <encomendas>
    <encomenda produto="Laptop" valor="899.99"/>
    <encomenda produto="Rato" valor="29.99"/>
  </encomendas>
</cliente>
```

**Vantagens:** validação por XSD/DTD, namespaces, transformações XSLT, padrão em sistemas empresariais (SOAP, RSS, configurações Java).  
**Desvantagens:** verboso, parsing mais pesado que JSON.

**Quando usar XML:** integração B2B, documentos com validação formal, sistemas legados, feeds RSS/Atom, ficheiros de configuração empresariais.

### 3.5 Comparação JSON vs XML vs CSV

| Critério | CSV | JSON | XML |
|----------|-----|------|-----|
| Legibilidade humana | Alta | Alta | Média |
| Estruturas aninhadas | Não | Sim | Sim |
| Esquema/validação | Não | JSON Schema | XSD/DTD |
| Tamanho típico | Pequeno | Médio | Grande |
| Uso em APIs modernas | Raro | Dominante | Declínio |
| Dados tabulares | Excelente | Possível | Possível |

---

## 4. Dados não estruturados

### 4.1 Definição

Dados **não estruturados** não possuem um esquema predefinido nem organização interna que facilite consultas automáticas. O conteúdo semântico está embutido no formato nativo (texto livre, pixels, amostras de áudio).

### 4.2 Exemplos

- Documentos de texto livre (PDF, Word, e-mails)
- Imagens e vídeos (JPEG, PNG, MP4)
- Áudio (WAV, MP3)
- Posts em redes sociais
- Logs em texto plano sem parsing
- Dados de sensores em formato binário bruto

### 4.3 Desafios

- **Extração:** requer OCR, NLP, visão computacional
- **Armazenamento:** object storage (S3, MinIO), file systems distribuídos (HDFS)
- **Metadados:** essenciais para catalogação (data, autor, tags)
- **Volume:** representam ~80–90% dos dados gerados globalmente

### 4.4 Abordagens de valorização

| Abordagem | Descrição |
|-----------|-----------|
| Metadados | Indexar atributos extraídos (autor, data, tipo) |
| Text mining | Extrair entidades, sentimento, tópicos |
| Data lakes | Armazenar raw + processar sob demanda |
| Embeddings | Representações vectoriais para pesquisa semântica |

---

## 5. Quando usar cada tipo e formato

### 5.1 Árvore de decisão simplificada

```
Os dados têm esquema fixo e relacional?
├── Sim → Estruturado (SQL, CSV para troca)
└── Não
    ├── Têm tags/chaves auto-descritivas?
    │   ├── Sim → Semiestruturado
    │   │   ├── API moderna / web → JSON
    │   │   ├── Validação formal / legado → XML
    │   │   └── Tabela simples sem relações → CSV
    │   └── Não → Não estruturado (object storage + metadados)
```

### 5.2 Cenários práticos

| Cenário | Tipo | Formato / Tecnologia |
|---------|------|----------------------|
| ERP com vendas diárias | Estruturado | PostgreSQL |
| API de e-commerce | Semiestruturado | JSON via REST |
| Faturas entre empresas | Semiestruturado | XML (UBL, Factur-X) |
| Exportação para Excel | Estruturado | CSV |
| Arquivo de contratos | Não estruturado | PDF + metadados |
| Feed de sensores IoT | Semiestruturado | JSON ou Avro |
| Catálogo de produtos B2B | Semiestruturado | XML com XSD |

---

## 6. Implicações para integração de dados

- **Estruturados:** joins, ETL clássico, mapeamento directo para data warehouse
- **Semiestruturados:** flattening (normalização), schema-on-read, parsers específicos
- **Não estruturados:** pipelines de extração, enriquecimento com metadados, integração tardia

A escolha incorrecta de formato aumenta custos de transformação, reduz qualidade e dificulta governança. A regra geral é: **use o formato mais simples que satisfaça os requisitos** — CSV para tabelas planas, JSON para APIs, XML quando a validação formal é obrigatória.

---

## Exercícios

### Exercício 1
Classifique cada fonte de dados como estruturada (E), semiestruturada (S) ou não estruturada (N):

a) Tabela `funcionarios` numa base MySQL  
b) Resposta JSON de uma API do GitHub  
c) Fotografia de um documento de identificação  
d) Ficheiro CSV exportado de uma folha Google Sheets  
e) E-mail com corpo em HTML e anexos PDF  
f) Stream de eventos Kafka em formato Avro  

### Exercício 2
Uma empresa precisa de trocar diariamente uma lista de preços com 500 produtos (ID, nome, preço, categoria) com um parceiro que usa Excel. Qual formato recomendaria e porquê?

### Exercício 3
Compare JSON e XML para uma API REST moderna de reservas hoteleiras. Liste três vantagens de JSON e duas situações em que XML seria preferível.

### Exercício 4
O seguinte registo CSV contém um erro comum. Identifique-o e proponha uma solução:

```csv
id,nome,morada,cidade
1,João Santos,"Rua das Flores, 12",Lisboa
2,Maria Oliveira,Rua do Comércio 5,Porto
```

### Exercício 5
Um sistema IoT envia leituras de sensores com estrutura variável: alguns sensores reportam temperatura e humidade, outros apenas temperatura, e alguns incluem coordenadas GPS. Justifique porque estes dados são semiestruturados e indique o formato mais adequado.

### Exercício 6
Calcule a taxa de compressão aproximada: um documento XML de 45 KB representa os mesmos dados que um JSON de 28 KB. Qual formato é mais eficiente em termos de tamanho? Em que cenário o formato maior poderia ainda ser preferível?

### Exercício 7
Uma organização tem 2 TB de PDFs (contratos), 50 GB de dados transaccionais em Oracle e 200 GB de logs JSON. Proponha uma estratégia de armazenamento diferenciada por tipo.

### Exercício 8
Converta mentalmente (ou escreva) a seguinte estrutura JSON para XML equivalente:

```json
{
  "livro": {
    "isbn": "978-0132350884",
    "titulo": "Clean Code",
    "autores": ["Robert Martin"]
  }
}
```

---

## Soluções

### Solução 1

| Fonte | Classificação | Justificação |
|-------|---------------|--------------|
| a) Tabela MySQL | **E** | Esquema fixo com tipos definidos |
| b) API GitHub JSON | **S** | Estrutura com chaves, mas flexível entre endpoints |
| c) Fotografia | **N** | Imagem sem esquema consultável |
| d) CSV Google Sheets | **E** | Formato tabular com colunas fixas |
| e) E-mail HTML + PDF | **N** (corpo S parcial) | Conteúdo principal não estruturado; classificar globalmente como **N** |
| f) Kafka Avro | **S** | Schema registry com evolução, mas estrutura auto-descritiva |

### Solução 2

**CSV** é a escolha recomendada porque:

- Dados tabulares simples (4 colunas fixas)
- Volume modesto (500 linhas)
- Compatibilidade directa com Excel
- Sem necessidade de aninhamento ou validação XSD
- Fácil de gerar a partir de qualquer base de dados (COPY, SELECT INTO OUTFILE)

Alternativa: XLSX se forem necessários múltiplos separadores ou formatação.

### Solução 3

**Vantagens de JSON para API REST:**

1. Parsing nativo em JavaScript (frontend)
2. Menor overhead de rede (~40% menor que XML equivalente)
3. Ecossistema moderno (OpenAPI, ferramentas de teste)

**Situações preferíveis para XML:**

1. Integração com sistemas legados que exigem SOAP/XSD
2. Quando validação formal contra XSD é requisito contratual
3. Documentos que serão assinados digitalmente (XML-DSig)

### Solução 4

**Problema:** O campo `morada` de João Santos contém vírgula (`Rua das Flores, 12`). Sem aspas de encapsulamento correcto, o parser interpretaria 5 colunas em vez de 4.

**Solução:** Encapsular campos com vírgulas entre aspas duplas (como já feito na linha 1). Regra RFC 4180: campos com vírgulas, aspas ou quebras de linha devem ser quoted; aspas internas duplicadas (`""`).

### Solução 5

Dados **semiestruturados** porque:

- Existe estrutura (timestamp, sensor_id, leituras)
- Campos variam entre sensores (schema flexível)
- Não obedecem a um esquema relacional fixo

**Formato recomendado:** **JSON** (ou Avro/Protobuf com schema registry para evolução controlada). JSON pela simplicidade; Avro se o volume for muito elevado e a evolução de schema precisar de ser versionada.

### Solução 6

JSON é **~38% mais compacto** (28/45 ≈ 0,62). XML seria preferível se:

- Fosse necessária validação XSD contra um standard sectorial
- O parceiro exigisse XML por contrato
- Fossem necessárias transformações XSLT no pipeline

### Solução 7

| Tipo | Volume | Armazenamento |
|------|--------|---------------|
| PDFs (N) | 2 TB | Object storage (S3/MinIO) + índice de metadados (Elasticsearch) |
| Oracle (E) | 50 GB | Manter em RDBMS; réplicas para DW |
| Logs JSON (S) | 200 GB | Data lake (Parquet particionado) ou Elasticsearch para pesquisa |

Estratégia: **armazenamento poliglota** — cada tipo no sistema optimizado para o seu perfil de acesso.

### Solução 8

```xml
<?xml version="1.0" encoding="UTF-8"?>
<livro>
  <isbn>978-0132350884</isbn>
  <titulo>Clean Code</titulo>
  <autores>
    <autor>Robert Martin</autor>
  </autores>
</livro>
```

Nota: arrays JSON convertem-se tipicamente em elementos repetidos em XML.

---

## Referências

- RFC 4180 — Common Format and MIME Type for CSV Files
- JSON Schema — https://json-schema.org
- W3C XML Recommendation
- Gartner — Unstructured Data Growth Statistics

**Próximo módulo:** [02 — Paradigmas de Integração de Dados](./02-paradigmas-integracao-dados.md)
