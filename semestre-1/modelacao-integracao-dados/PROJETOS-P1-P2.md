# Projetos P1 e P2 — Integração Virtual de Dados

**UC:** 14741095 · **Docente:** Paula Ventura Martins · **2026/27**

> Resumo do enunciado oficial (DMI_Projects_2026_2027.pdf). PDF não publicado no repositório.

Painel de prazos: [projetos-por-fazer](../../projetos-por-fazer/README.md)

---

## Visão geral

P1 e P2 formam um **trabalho contínuo** sobre integração virtual de dados:

| | P1 | P2 |
|---|----|----|
| **Pergunta** | Que dados são necessários e como representar cada fonte? | Como aceder às fontes através de uma representação coerente? |
| **Output** | Fontes locais implementadas e populadas | Sistema de integração + queries globais |
| **Peso** | 45% | 45% |
| **Mínimo** | 10/20 | 10/20 |

**Grupo:** 2 estudantes. Cada um trata um **subtópico distinto** mas complementar no mesmo domínio.

---

## Calendário

| Marco | Data | Conteúdo |
|-------|------|----------|
| **Proposta** | **21 set 2026** | Domínio, grupo, requisitos, fontes, plano (formativo) |
| **P1 entrega** | **16 nov 2026** | Relatório, fontes, modelos, scripts, queries, README |
| **P1 apresentação** | nov–dez 2026 | Oral + discussão individual |
| **P2 entrega** | **18 jan 2027** | Integração, mappings, queries globais, validação |
| **P2 apresentação** | **18–22 jan 2027** | Oral + discussão individual |

*Datas finais confirmadas no Moodle.*

---

## P1 — Fontes heterogéneas

### Tarefas do grupo

1. Selecionar domínio e definir problema
2. Identificar stakeholders e requisitos (idealmente com peritos)
3. Especificar necessidades como queries representativas
4. **Cada membro:** desenhar, implementar e popular **2 fontes heterogéneas** (4 total)
5. Usar ≥ **2 tecnologias** de gestão de dados diferentes
6. Analisar qualidade e documentar heterogeneidade para P2

### Tipos de fonte permitidos

Relacional · NoSQL · XML · CSV/JSON · Web APIs · Formulários web

### Queries (12 total)

| | Quantidade |
|---|------------|
| Por estudante (subtópico) | 2 + 2 = 4 |
| Cross-subtopic (grupo) | 8 |
| **Total** | **12** (4 simples + 4 intermédias + 4 complexas) |

Incluir: filtragem, agregação, relações, combinação entre fontes.

### Relatório P1

- Domínio, objetivos, stakeholders, requisitos
- Glossário e constraints
- Requisitos funcionais/não-funcionais + casos de uso
- 4 fontes + responsável de cada
- Modelos conceptual, lógico, físico
- Recolha/geração de dados + qualidade
- Queries com resultados esperados
- Instruções instalação/execução

---

## P2 — Integração virtual

### Requisitos de integração

1. Arquitetura e responsabilidades dos componentes
2. Schema global (conceptual + lógico)
3. Wrappers/adapters para fontes locais
4. Mappings fonte → global
5. Transformações de schema e valores
6. Processamento de queries sobre schema global
7. Query containment e views (se aplicável)
8. Validação: resultados, erros, fontes indisponíveis

### Heterogeneidade (documentar resolução)

| Tipo | Exemplos |
|------|----------|
| Estrutural | Entidades, atributos, nesting, relações |
| Sintática | Formatos, tipos, encodings, datas |
| Semântica | Sinónimos, homónimos, unidades, significados |

### Relatório P2

- Arquitetura e schema global
- Fontes e mecanismos de acesso
- Mappings e transformações
- Query processing + queries globais
- Validação, limitações, melhorias
- Instalação, execução, demonstração

---

## Entregáveis técnicos

| Pasta/ficheiro | P1 | P2 |
|----------------|----|----|
| `report/` PDF | ✓ | ✓ |
| `src/` | ✓ | ✓ |
| `data/` | ✓ | ✓ |
| `database/` scripts | ✓ | actualizado |
| `models/` | schemas locais | global + locais |
| `queries/` | requisitos + esperados | implementadas |
| `README.md` | setup fontes | demo completa |
| Declaração IA | se usada | se usada |
| Declaração contribuição | ✓ | ✓ |

Relatório: **≤ 15 páginas** (corpo); anexos para schemas extensos, código, logs.

---

## Avaliação detalhada

### Nota final
```
Média(P1, P2) × 90% + Exer × 10%
```
Mínimo 10 em P1, P2 e nota final. Sem exame.

### Critérios P1

| Critério | % |
|----------|---|
| Domínio, stakeholders, requisitos | 20 |
| Fontes, heterogeneidade, justificação | 20 |
| Modelos conceptual/lógico/físico | 25 |
| Implementação, população, qualidade | 20 |
| Queries, relatório, apresentação | 15 |

### Critérios P2

| Critério | % |
|----------|---|
| Arquitetura e schema global | 20 |
| Mappings, transformações, heterogeneidade | 25 |
| Implementação e query processing | 25 |
| Validação, reproducibilidade, limitações | 20 |
| Relatório, apresentação | 10 |

### Discussão individual
- Até **4 perguntas** com peso igual
- Falha numa pergunta → deduz **25%** da nota do projeto
- Notas podem diferir dentro do grupo

---

## Requisitos de dados

- Dados suficientes para todas as queries
- Dados sintéticos OK (documentar geração)
- Dados externos: origem, licença, data acesso
- Sem credenciais/secrets na submissão
- Reprodutibilidade total via README

---

## Uso de IA generativa

Permitida para: clarificar conceitos, exemplos, debug, documentação, alternativas.

Obrigatório: declarar ferramenta, propósito, extensão; verificar outputs; responsabilidade do grupo.

**Proibida** na discussão individual.

---

## Checklist submissão

- [ ] Artefactos abrem e executam
- [ ] README completo
- [ ] Queries retornam resultados documentados
- [ ] Nomes consistentes (report + repo)
- [ ] Citações e licenças
- [ ] Contribuição + IA
- [ ] Sem secrets
