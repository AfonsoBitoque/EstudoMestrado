# MID — P1: Fontes de dados heterogéneas

| Campo | Valor |
|-------|-------|
| **Disciplina** | Modelação e Integração de Dados |
| **Código UC** | 14741095 |
| **Docente** | Paula Ventura Martins |
| **Peso na nota** | **45%** (mínimo 10/20) |
| **Data limite** | **16 novembro 2026** |
| **Estado** | ⚪ Por iniciar |
| **Tipo** | Grupo (2) + defesa individual |
| **Entrega** | Moodle (ZIP/repo) + apresentação nov–dez |

---

## Resumo

Implementar **4 fontes de dados heterogéneas** (2 por estudante) num domínio comum, com modelos conceptual/lógico/físico, dados populados, análise de qualidade e **12 queries** representativas. Base para o P2 (integração virtual).

---

## O que fazer (por ordem)

### 1. Domínio e requisitos
- [ ] Escolher domínio e problema
- [ ] Identificar stakeholders
- [ ] Requisitos funcionais e não-funcionais + casos de uso
- [ ] Glossário de conceitos

### 2. Fontes de dados (4 total)
Cada membro: **2 fontes** do seu subtópico.

| Tipo permitido | Exemplos |
|----------------|----------|
| Relacional | PostgreSQL, MySQL |
| NoSQL | MongoDB, Redis |
| Semi-estruturado | XML, JSON, CSV |
| Externo | Web API, formulários web |

- [ ] ≥ **2 tecnologias** diferentes no grupo
- [ ] Justificar cada fonte no relatório
- [ ] Modelos **conceptual, lógico e físico** por fonte
- [ ] Scripts criação + carga de dados
- [ ] Análise de **qualidade** e heterogeneidade (prepara P2)

### 3. Queries (12 total)

| Tipo | Quantidade | Quem |
|------|------------|------|
| Por subtópico | 2 × 2 = **4** | Cada estudante |
| Cross-subtopic | **8** | Grupo |
| **Total** | **12** | 4 simples + 4 intermédias + 4 complexas |

Queries devem incluir: filtragem, agregação, relações entre entidades, combinação entre fontes/subtópicos.

### 4. Relatório PDF (≤ 15 páginas corpo)
- [ ] Domínio, objetivos, stakeholders, requisitos
- [ ] Glossário e constraints
- [ ] 4 fontes + responsável de cada uma
- [ ] Modelos + processo de recolha/geração de dados
- [ ] Queries com resultados esperados
- [ ] Instruções instalação/execução
- [ ] Declaração de contribuição + IA (se usada)

### 5. Repositório / pacote

```
report/     → PDF final
src/        → código
data/       → dados ou scripts aquisição
database/   → scripts DDL + load
models/     → diagramas, schemas
queries/    → SQL + resultados esperados
README.md   → instalação e demo
```

---

## Critérios de avaliação P1

| Critério | Peso |
|----------|------|
| Domínio, stakeholders e requisitos | 20% |
| Seleção de fontes, heterogeneidade e justificação | 20% |
| Modelos conceptual, lógico e físico | 25% |
| Implementação, população e qualidade dos dados | 20% |
| Queries, relatório, apresentação e demonstração | 15% |

**Defesa individual:** até 4 perguntas; falha numa pergunta = −25% da nota do projeto.

---

## Checklist final

- [ ] Proposta aprovada (21 set)
- [ ] 4 fontes funcionais com dados coerentes
- [ ] 12 queries executáveis com resultados documentados
- [ ] README reproduz instalação completa
- [ ] Sem credenciais/secrets no repo
- [ ] Dados externos citados (origem, licença, data)
- [ ] Apresentação oral preparada

---

## Ligações

- [PROJETOS-P1-P2.md](../semestre-1/modelacao-integracao-dados/PROJETOS-P1-P2.md)
- Módulos: [01](../semestre-1/modelacao-integracao-dados/modulos/01-tipos-dados-estruturados-semiestruturados.md) · [02](../semestre-1/modelacao-integracao-dados/modulos/02-paradigmas-integracao-dados.md) · [05](../semestre-1/modelacao-integracao-dados/modulos/05-xml-nosql.md)
- [Próximo: P2](./mid-p2-integracao-virtual.md)
