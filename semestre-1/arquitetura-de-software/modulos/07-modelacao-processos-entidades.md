# Módulo 07 — Modelação de Processos e Entidades

## Introdução

Modelar processos e entidades de informação é ponte entre o mundo do negócio e a implementação software. **BPMN** (Business Process Model and Notation) permite representar fluxos operacionais; **modelação de entidades** captura a estrutura conceptual da informação empresarial. Este módulo introduz fundamentos de ambas as notações e a sua relação com arquitectura de software.

## BPMN — Fundamentos

**BPMN 2.0** é standard OMG para modelação de processos de negócio, legível por analistas de negócio e developers. Combina diagramas visuais com semantics executáveis (XML para BPMS).

### Elementos Essenciais

**Flow Objects:**
- **Eventos:** algo que acontece. Tipos: Start (círculo fino), Intermediate, End (círculo grosso). Variantes: Message, Timer, Error, Signal.
- **Actividades:** trabalho executado. **Task** (atómica) ou **Sub-process** (composto, colapsável).
- **Gateways:** decisões e paralelismo. **Exclusive (XOR)** — um caminho; **Parallel (AND)** — todos; **Inclusive (OR)** — um ou mais; **Event-based** — baseado em evento.

**Connecting Objects:**
- **Sequence Flow:** ordem de execução (seta sólida).
- **Message Flow:** comunicação entre participantes (seta tracejada).
- **Association:** liga artefactos a elementos.

**Swimlanes:**
- **Pool:** participante (organização, sistema externo). Processo pode ter um ou múltiplos pools.
- **Lane:** subdivisão de pool por role (ex.: "Cliente", "Vendas", "Financeiro").

**Artefactos:**
- **Data Object:** dados manipulados.
- **Annotation:** comentários textuais.

### Padrões Comuns

**Sequência simples:** Start → Task → Task → End.

**Decisão:** Task → Gateway (XOR) → caminhos alternativos → merge → End.

**Paralelismo:** Gateway AND split → tarefas paralelas → Gateway AND join.

**Processo colaborativo:** dois pools (Cliente e Empresa) ligados por Message Flows.

### BPMN e Software

Cada task mapeia potencialmente para: actividade humana (UI, aprovação), serviço automatizado (API call), ou regra de negócio (decision engine). Gateways mapeiam para lógica condicional ou orquestração. Eventos mapeiam para triggers (webhook, timer, message queue). BPMS executam BPMN directamente; em microserviços, engines como Camunda orquestram chamadas a serviços.

Boas práticas: um diagrama por nível de detalhe; evitar "spaghetti"; nomear tasks com verbo + objecto ("Validar Pedido", "Enviar Confirmação"); distinguir processos executáveis de mapas de contexto (qualitative).

## Modelação de Entidades

**Modelação de entidades** descreve tipos de informação significativos para o negócio, os seus atributos e relações — independentemente de implementação física.

### Níveis de Abstração

1. **Conceptual:** entidades de negócio e relações, sem detalhes técnicos. Público: stakeholders de negócio.
2. **Lógico:** atributos, cardinalidades, normalização. Público: arquitectos e analistas.
3. **Físico:** tabelas, colunas, índices, tipos SQL. Público: developers e DBAs.

Arquitectos operam predominantemente nos níveis conceptual e lógico; developers no físico.

### Elementos de um Modelo Entidade-Relação

**Entidade:** concepto de negócio (Cliente, Produto, Encomenda). Representada por rectângulo.

**Atributo:** propriedade da entidade (Nome, Email, Preço). Identificador único (PK) sublinhado.

**Relacionamento:** associação entre entidades (Cliente **faz** Encomenda). Cardinalidades: 1:1, 1:N, N:M.

**Entidade associativa:** resolve N:M com atributos próprios (LinhaEncomenda entre Encomenda e Produto).

### Entidades de Informação Empresariais

No contexto de EA, **entidades de informação** (information entities) são objectos de negócio partilhados entre processos e sistemas — frequentemente alinhados com master data:

- **Party:** pessoa ou organização (Cliente, Fornecedor, Funcionário).
- **Product/Service:** o que a organização vende ou presta.
- **Agreement/Contract:** compromissos formais.
- **Financial:** transacções, facturas, pagamentos.
- **Location:** locais físicos ou lógicos.
- **Event:** ocorrências temporais significativas.

Estas categorias derivam de frameworks como **IBM CIM** ou **TODAF** e facilitam consistência cross-sistema.

### Relação BPMN ↔ Entidades

Processos **manipulam** entidades: task "Criar Encomenda" produz entidade Encomenda; "Actualizar Stock" modifica Produto. Data Objects em BPMN referenciam entidades. Mapeamento processo→entidade→componente software é base da interligação arquitectural (módulo 08).

## UML para Complemento

Além de ER, **UML Class Diagrams** podem modelar entidades com classes, associações, multiplicidades e generalizações (herança). Útil quando entidades evoluem para classes de domínio (DDD). Diferença: ER foca persistência; UML class foca comportamento e estrutura objecto.

## Boas Práticas de Modelação

- Validar modelos com donos de processo e dados.
- Usar glossário de negócio para nomenclatura.
- Manter modelos vivos — actualizar quando processos mudam.
- Não confundir diagrama com documentação completa — complementar com descrições e regras.
- Granularidade adequada: processos de alto nível (value stream) vs. detalhe executável.

## Exercícios

1. Descreva os elementos BPMN: evento, task, gateway exclusivo e pool.

2. Desenhe (em texto) um processo BPMN simples: "Aprovação de Férias" com Start, submissão, aprovação do manager (gateway sim/não), notificação e End.

3. Qual a diferença entre modelo conceptual, lógico e físico de entidades?

4. Modele entidades Cliente, Encomenda e Produto com relacionamentos e cardinalidades.

5. O que é uma entidade associativa? Dê exemplo.

6. Explique a diferença entre Sequence Flow e Message Flow no BPMN.

7. Liste três categorias de entidades de informação empresariais e um exemplo de cada.

8. Como uma task BPMN "Calcular Total da Encomenda" se relaciona com entidades do modelo de dados?

## Soluções

1. **Evento:** ocorrência que afecta processo (início, meio, fim). **Task:** unidade de trabalho atómica. **Gateway exclusivo (XOR):** decisão com exactamente um caminho de saída activo. **Pool:** participante no processo (actor ou sistema), delimita scope e responsabilidade.

2. **Processo Aprovação de Férias:** Start Event → Task "Submeter Pedido de Férias" → Task "Rever Pedido" (Manager) → Gateway XOR "Aprovado?" → [Sim] Task "Notificar Aprovação" → End Event "Férias Aprovadas"; [Não] Task "Notificar Rejeição" → End Event "Pedido Rejeitado". Lane: Funcionário (submissão), Manager (revisão).

3. **Conceptual:** entidades e relações de negócio, sem atributos técnicos — "Cliente faz Encomendas". **Lógico:** atributos detalhados, tipos abstractos, normalização — Cliente(NIF, Nome, Email), cardinalidades precisas. **Físico:** implementação concreta — tabela `customers`, colunas SQL, índices, constraints.

4. **Cliente** (1) — **faz** — (N) **Encomenda**: um cliente tem muitas encomendas; cada encomenda pertence a um cliente. **Encomenda** (1) — **contém** — (N) **LinhaEncomenda** (associativa) — (N) **Produto**: encomenda tem linhas; cada linha referencia um produto; produto aparece em muitas linhas. Atributos: Cliente(NIF, Nome); Encomenda(Data, Estado); Produto(SKU, Nome, Preço); LinhaEncomenda(Quantidade, PreçoUnitário).

5. **Entidade associativa** resolve relacionamento N:M com atributos próprios. Exemplo: **LinhaEncomenda** entre Encomenda e Produto — além das FKs, tem Quantidade e Desconto, que pertencem à relação e não a Encomenda ou Produto isoladamente.

6. **Sequence Flow:** ordem de execução **dentro** do mesmo pool/processo (seta sólida entre elementos). **Message Flow:** comunicação **entre** pools diferentes (seta tracejada) — representa troca de mensagens entre participantes (ex.: Cliente envia pedido → Empresa recebe).

7. **Party:** Cliente, Fornecedor. **Product/Service:** Catálogo de Produtos, Plano de Subscrição. **Financial:** Factura, Pagamento. (Outras válidas: Agreement/Contract — Contrato de Serviço; Location — Armazém; Event — Entrega Realizada.)

8. Task "Calcular Total" **lê** entidades LinhaEncomenda (quantidade, preço unitário) e possivelmente Produto (preço actual, impostos); **aplica** regras de negócio; **actualiza** atributo Total da entidade Encomenda. O mapeamento software: task → serviço `OrderCalculationService` → repositórios de Encomenda/LinhaEncomenda → agregação de domínio. Entidades guiam estrutura de dados que o processo manipula.
