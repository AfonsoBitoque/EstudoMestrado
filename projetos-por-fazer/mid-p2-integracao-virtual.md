# MID — P2: Integração virtual de dados

| Campo | Valor |
|-------|-------|
| **Disciplina** | Modelação e Integração de Dados |
| **Código UC** | 14741095 |
| **Docente** | Paula Ventura Martins |
| **Peso na nota** | **45%** (mínimo 10/20) |
| **Data limite** | **18 janeiro 2027** |
| **Apresentação** | **18–22 janeiro 2027** |
| **Estado** | ⚪ Por iniciar |
| **Tipo** | Grupo (2) + defesa individual |

---

## Resumo

Integrar as fontes do P1 através de **schema global**, wrappers/adapters, **mappings**, transformações e **processamento de queries** sobre o schema integrado. Demonstrar queries simples, intermédias e complexas que combinem dados de **todos** os subtópicos.

---

## O que fazer

### 1. Arquitetura
- [ ] Diagrama da arquitetura e responsabilidades de cada componente
- [ ] Wrappers/adapters para cada fonte local

### 2. Schema global
- [ ] Modelo **conceptual e lógico** global
- [ ] Mappings fonte → global (cada fonte)
- [ ] Transformações de schema e **valores**

### 3. Heterogeneidade (obrigatório documentar)

| Tipo | Exemplos a resolver |
|------|---------------------|
| **Estrutural** | Entidades/atributos diferentes, nesting, relações |
| **Sintática** | Formatos, tipos, encodings, datas |
| **Semântica** | Sinónimos, homónimos, unidades, classificações |

Para cada conflito: elemento origem → regra transformação → representação global.

### 4. Query processing
- [ ] Processar queries sobre schema global
- [ ] Obter resultados das fontes locais
- [ ] Query containment e views (quando aplicável)
- [ ] Validar: resultados esperados, erros, fontes indisponíveis

### 5. Queries globais
- [ ] Simples, intermédias e complexas
- [ ] Incluir queries que combinem **todos** os subtópicos

### 6. Relatório + entrega (≤ 15 páginas corpo)
- [ ] Arquitetura e schema global
- [ ] Fontes e mecanismos de acesso
- [ ] Estratégia de mapping e transformações
- [ ] Query processing + queries implementadas
- [ ] Validação, limitações, melhorias
- [ ] README completo (instalação + demo)

---

## Critérios de avaliação P2

| Critério | Peso |
|----------|------|
| Arquitetura e schema global | 20% |
| Mappings, transformações e heterogeneidade | 25% |
| Implementação e query processing | 25% |
| Validação, reproducibilidade e limitações | 20% |
| Relatório, apresentação e demonstração | 10% |

---

## Entregáveis adicionais vs P1

| Entregável | P2 |
|------------|-----|
| Mappings | Especificação **completa** |
| Queries | **Implementadas** sobre schema global |
| Models | Schema global + locais |
| README | Execução e demonstração **completas** |

---

## Checklist

- [ ] P1 concluído e fontes estáveis
- [ ] Integração funciona com fonte indisponível (teste)
- [ ] Todas queries globais executam com resultado documentado
- [ ] Declaração IA + contribuição
- [ ] Apresentação 18–22 jan

---

## Ligações

- [PROJETOS-P1-P2.md](../semestre-1/modelacao-integracao-dados/PROJETOS-P1-P2.md)
- Módulos: [02](../semestre-1/modelacao-integracao-dados/modulos/02-paradigmas-integracao-dados.md) · [03](../semestre-1/modelacao-integracao-dados/modulos/03-fontes-dados-wrappers-streaming.md) · [04](../semestre-1/modelacao-integracao-dados/modulos/04-etl-transformacao-profiling.md)
