# Aula 01 — Introdução e revisão SQL

**Docente:** Paula Cristina Negrão Ventura Martins · **UC:** 14741095 · **Ano:** 2026/27

> Resumo dos slides da aula 1 (class1). PDF oficial não publicado no repositório.

---

## Informação da UC

| | |
|---|---|
| **Contacto** | pventura@ualg.pt · Gabinete B1-2.69 |
| **Antes da próxima aula** | Confirmar Moodle + software; rever BD relacionais |
| **Bibliografia** | Doan, Halevy & Ives — *Principles of Data Integration*; Lemahieu et al. — *Principles of Database Management* |

---

## Percurso de aprendizagem (6 blocos)

1. **Data foundations** — estruturados, semi-estruturados, não estruturados
2. **Integration paradigms** — virtual, mediação, materialização
3. **Sources and schemas** — streams, XML, mediators, wrappers, mapping
4. **ETL and quality** — extração, transformação, profiling, duplicados
5. **Extended stores** — XML e NoSQL
6. **Analytics** — data warehouses, OLAP, MDX, reporting

---

## Objetivos de aprendizagem

- Escolher SQL ou NoSQL adequado ao problema
- Filtrar, agregar e extrair dados heterogéneos em escala
- Distinguir OLTP vs OLAP
- Desenhar e implementar data warehouse pequeno/médio
- Integrar dados transacionais em DW (ETL)
- Explicar mediação, mashups e reporting

---

## Avaliação

| Componente | Peso | Condição |
|------------|------|----------|
| **P1** | 45% | Mín. 10/20 |
| **P2** | 45% | Mín. 10/20 |
| **Exercícios PL** | 10% | Média 0–5 |

```
Nota final = Média(P1, P2) × 90% + Exer × 10%
```

- Grupo de **2**; defesa **individual** (até 4 perguntas)
- **Sem exame final**
- IA: permitida com declaração; proibida na discussão individual

Ver: [PROJETOS-P1-P2.md](../PROJETOS-P1-P2.md) · [projetos-por-fazer](../../../projetos-por-fazer/README.md)

---

## Revisão SQL — roadmap da aula

```
Modelo E-R  →  Tabelas/PK/FK  →  CREATE  →  INSERT  →  SELECT
```

Cada statement SQL deve ser rastreável a uma decisão de modelação.

---

## Modelação conceptual (exemplo seguros)

**Entidades:** PERSON, CAR, ACCIDENT, INSURANCE_COMPANY

**Relações:**
- owns (1:N) PERSON → CAR
- involved in (M:N) PERSON, CAR, ACCIDENT
- insures (N:1) → INSURANCE_COMPANY

**Pergunta-chave:** que factos pertencem a uma entidade vs. a uma relação?

---

## Regras de mapeamento E-R → relacional

| Regra | Exemplo |
|-------|---------|
| Entidade → tabela | PERSON(nr_id PK, name, …) |
| Multivalor → tabela | PERSON_EMAIL(nr_id, email) |
| 1:N → FK no N | CAR.owner_id → PERSON |
| M:N → tabela junção | INVOLVEMENT(person_id, plate_nr, acc_id) |

---

## Schema relacional resultante

```
PERSON(nr_id PK, name, birth_dt, street, city, zip_code)
PERSON_EMAIL(nr_id FK, email PK)
CAR(plate_nr PK, model, manufacturer, owner_id FK)
ACCIDENT(acc_id PK, location, description)
INVOLVEMENT(person_id FK, plate_nr FK, acc_id FK, event_date)
INSURANCE_PLAN(plan_id PK, company_id FK, premium)
```

---

## Exemplo music database (usado na aula)

```
ARTIST(artist_id, artist_name)
  1:N
ALBUM(album_id, title, artist_id FK)
  1:N
TRACK(track_id, title, duration, album_id FK)
  1:N
PLAY_EVENT(played_at, track_id FK)
```

---

## Famílias SQL

| Família | Comandos | Propósito |
|---------|----------|-----------|
| **DDL** | CREATE, ALTER, DROP | Estrutura |
| **DML** | INSERT, UPDATE, DELETE | Dados |
| **DQL** | SELECT | Consultas |
| **TCL/DCL** | COMMIT, ROLLBACK, GRANT | Controlo |

JOIN é operador dentro de SELECT, não comando de criação.

---

## Workflow MySQL prático

```sql
CREATE DATABASE IF NOT EXISTS music;
USE music;

CREATE TABLE artist (
  artist_id   INTEGER      PRIMARY KEY,
  artist_name VARCHAR(120) NOT NULL
);

CREATE TABLE album (
  album_id  INTEGER      PRIMARY KEY,
  title     VARCHAR(160) NOT NULL,
  artist_id INTEGER      NOT NULL,
  FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);
```

Comandos úteis: `SHOW DATABASES;` · `SHOW TABLES;` · `DESCRIBE table_name;`

---

## Tipos de dados (escolher por significado)

| Família | Tipos | Uso |
|---------|-------|-----|
| Caracteres | CHAR, VARCHAR, TEXT | Nomes, descrições |
| Numérico exacto | INTEGER, DECIMAL(p,s) | IDs, dinheiro |
| Numérico aproximado | FLOAT, DOUBLE | Medições |
| Data/hora | DATE, TIME, TIMESTAMP | Eventos |
| Lógico/binário | BOOLEAN, BLOB | Flags, binário |

**Não uses FLOAT para dinheiro** — preferir DECIMAL(p,s).

---

## Constraints

| Constraint | Propósito |
|------------|-----------|
| PRIMARY KEY | Identificador único |
| FOREIGN KEY | Integridade referencial |
| UNIQUE | Candidato alternativo |
| NOT NULL | Valor obrigatório |
| DEFAULT | Valor por omissão |
| CHECK | Regra de domínio |

---

## DML e consultas (tópicos da aula)

- INSERT com integridade referencial (ordem: artist → album → track)
- SELECT com WHERE, ORDER BY, LIKE
- JOINs (INNER, LEFT) para relacionar tabelas
- Agregações (COUNT, SUM, GROUP BY, HAVING)

---

## Sistemas geridos (referência)

PostgreSQL · MySQL · SQL Server · Oracle · SQLite

SQL core é portável; tipos e funções administrativas variam.

---

## Ligação aos projetos

A modelação E-R → SQL desta aula é base directa do **P1** (modelos por fonte) e do **P2** (schema global + mappings).

- [Proposta — 21 set](../../../projetos-por-fazer/mid-proposta-projeto.md)
- [P1 — 16 nov](../../../projetos-por-fazer/mid-p1-fontes-heterogeneas.md)

---

## Exercícios de consolidação

1. Desenha E-R para biblioteca (livros, autores, empréstimos, leitores).
2. Mapeia para schema relacional com PK/FK.
3. Escreve CREATE TABLE + INSERT para 3 registos.
4. Query: livros emprestados por leitor (JOIN + GROUP BY).
5. Identifica que parte do P1 corresponde a cada passo acima.

## Soluções (esboço)

5. Domínio/requisitos → proposta; modelos E-R/SQL por fonte → P1; integração → P2.
