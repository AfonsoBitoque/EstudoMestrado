# Módulo 01 — Conceitos Fundamentais de Arquitetura de Software

## Introdução

A arquitetura de software é uma das competências mais estratégicas da engenharia de software moderna. Enquanto a programação concentra-se em resolver problemas concretos com código, a arquitetura estabelece as decisões estruturais de alto nível que determinam como um sistema será organizado, evoluído e operado ao longo de anos. Este módulo introduz os conceitos que sustentam todo o percurso: a distinção entre arquitetura, design e implementação; os atributos de qualidade que orientam decisões; e o papel dos stakeholders no processo arquitetural.

## Arquitetura, Design e Implementação

Estes três termos são frequentemente confundidos, mas representam níveis distintos de abstração e impacto.

**Arquitetura** refere-se às decisões estruturais fundamentais e difíceis de alterar posteriormente. Inclui a escolha de estilos arquiteturais (monolito, microserviços, event-driven), a decomposição do sistema em componentes principais, os mecanismos de comunicação entre eles e as restrições tecnológicas globais. A arquitetura responde a perguntas como: "Como o sistema se divide em partes?", "Quais são os pontos de integração com sistemas externos?" e "Quais tecnologias base serão adotadas?"

**Design** (design de software ou design detalhado) opera num nível intermédio. Traduz a arquitetura em estruturas mais concretas: classes, módulos, interfaces, padrões de projeto (Design Patterns) e algoritmos. O design responde a: "Como implementar este componente?", "Qual a estrutura interna deste serviço?" e "Como garantir baixo acoplamento entre módulos?"

**Implementação** é a materialização do design em código executável. Inclui a escrita de classes, funções, testes unitários, configurações e scripts de deployment. Embora pareça o nível mais tangível, uma má implementação pode comprometer uma boa arquitetura, tal como uma boa implementação não compensa decisões arquiteturais erradas.

A relação entre os três níveis é hierárquica e bidirecional. A arquitetura restringe o design; o design guia a implementação. Por outro lado, descobertas durante a implementação podem revelar limitações arquiteturais e provocar revisões. A regra prática é: quanto mais cedo se tomam decisões arquiteturais, maior o seu impacto e custo de mudança.

## Atributos de Qualidade (Quality Attributes)

Os atributos de qualidade — também designados requisitos não funcionais — são propriedades mensuráveis que caracterizam o comportamento de um sistema além da funcionalidade. São o critério principal para avaliar e comparar arquiteturas alternativas.

**Desempenho (Performance):** capacidade de responder dentro de limites de tempo e throughput aceitáveis. Medido por latência, tempo de resposta e transações por segundo.

**Escalabilidade (Scalability):** habilidade de crescer em carga (utilizadores, dados, transações) sem degradação proporcional. Pode ser vertical (mais recursos num nó) ou horizontal (mais nós).

**Disponibilidade (Availability):** percentagem de tempo em que o sistema está operacional. Expressa-se frequentemente em "nove" (99,9%, 99,99%).

**Confiabilidade (Reliability):** probabilidade de funcionamento correto durante um intervalo de tempo, incluindo tolerância a falhas.

**Segurança (Security):** proteção contra acessos não autorizados, garantia de confidencialidade, integridade e auditabilidade.

**Manutenibilidade (Maintainability):** facilidade de corrigir defeitos, adicionar funcionalidades e compreender o sistema.

**Testabilidade (Testability):** grau em que o sistema permite testes automatizados eficazes.

**Interoperabilidade (Interoperability):** capacidade de comunicar e trocar dados com outros sistemas.

**Usabilidade (Usability):** facilidade de utilização por parte dos utilizadores finais.

**Portabilidade (Portability):** facilidade de migrar o sistema para diferentes ambientes (SO, cloud, hardware).

Estes atributos entram frequentemente em conflito. Maximizar segurança pode reduzir desempenho; maximizar disponibilidade implica custos de infraestrutura. O arquiteto deve priorizar explicitamente, pois "otimizar tudo" é impossível.

## Stakeholders e o Papel do Arquiteto

Stakeholders são todas as partes com interesse legítimo no sistema. Cada grupo traz perspetivas e requisitos distintos:

- **Utilizadores finais** preocupam-se com usabilidade e funcionalidade.
- **Gestores de produto/negócio** focam alinhamento estratégico, time-to-market e custo.
- **Equipas de desenvolvimento** valorizam manutenibilidade, clareza e produtividade.
- **Operações/DevOps/SRE** exigem observabilidade, deployabilidade e resiliência.
- **Segurança e compliance** impõem requisitos regulatórios e de auditoria.
- **Fornecedores e parceiros** necessitam de interfaces estáveis e contratos claros.

O arquitecto de software actua como mediador entre estes interesses. As suas responsabilidades incluem: capturar e priorizar requisitos arquitecturais; propor e documentar decisões; avaliar trade-offs; comunicar a visão técnica; e garantir que a implementação respeita os princípios definidos. Um arquitecto eficaz combina visão técnica profunda com capacidade de comunicação e negociação.

## Decisões Arquiteturais e Documentação

Decisões arquiteturais devem ser explícitas, justificadas e rastreáveis. O custo de uma decisão arquitectural errada cresce exponencialmente com o tempo — refatorar um monolito para microserviços após cinco anos de evolução é ordens de magnitude mais caro do que escolher correctamente no início (ou planear migração incremental).

A documentação arquitectural não precisa ser volumosa, mas deve responder: qual a estrutura do sistema, porquê essa estrutura, quais os riscos conhecidos e como serão mitigados. Diagramas, ADRs (Architecture Decision Records) e descrições de atributos de qualidade são instrumentos essenciais abordados em módulos posteriores.

## Princípios Orientadores

Alguns princípios transversais guiam boas arquitecturas:

- **Separação de preocupações:** cada componente tem uma responsabilidade clara.
- **Baixo acoplamento, alta coesão:** módulos independentes com funções bem definidas.
- **Design for change:** antecipar evolução sem over-engineering.
- **Fail fast, recover gracefully:** detectar falhas cedo e isolar impacto.
- **Simplicidade:** a solução mais simples que satisfaz os requisitos prioritários.

## Exercícios

1. Explique com as suas palavras a diferença entre arquitetura, design e implementação. Dê um exemplo concreto de cada nível num sistema de reservas de hotel.

2. Para um sistema bancário online, liste cinco atributos de qualidade prioritários e justifique a ordem de prioridade.

3. Identifique um conflito entre dois atributos de qualidade num marketplace de e-commerce e proponha uma decisão arquitectural que equilibre ambos.

4. Enumere quatro tipos de stakeholders num projecto de software empresarial e indique uma preocupação típica de cada um.

5. Um gestor de produto pede "microserviços porque é moderno". Como arquitecto, como responderia? Que informação precisaria antes de tomar uma decisão?

6. Descreva uma decisão arquitectural difícil de reverter num sistema que conheça ou imagine. Porque é difícil de alterar?

7. Compare manutenibilidade e desempenho como atributos de qualidade. Quando faria sentido sacrificar um em favor do outro?

8. Redija um parágrafo descrevendo o papel do arquitecto de software numa organização de médio porte durante a fase de concepção de um novo produto.

## Soluções

1. **Arquitetura:** decidir que o sistema será composto por uma API REST, uma base de dados relacional e um frontend SPA — define a estrutura global. **Design:** definir que o módulo de reservas usa o padrão Repository, com entidades `Reserva`, `Quarto` e `Hóspede`, e interfaces entre camadas. **Implementação:** escrever a classe `ReservaRepository` em Java com queries SQL concretas e testes unitários. A arquitectura restringe tecnologias; o design organiza módulos; a implementação é o código.

2. Prioridades típicas para banca online: (1) **Segurança** — dados financeiros e regulamentação; (2) **Disponibilidade** — indisponibilidade gera perda de confiança e receita; (3) **Confiabilidade** — transacções não podem perder-se; (4) **Desempenho** — latência aceitável em pagamentos; (5) **Auditabilidade** (relacionada com segurança/compliance) — rastreio de operações. A ordem reflecte risco regulatório e impacto no negócio.

3. **Conflito:** desempenho vs. segurança — encriptação ponta-a-ponta e validações adicionais aumentam latência. **Equilíbrio:** usar TLS na comunicação, cachear sessões autenticadas com tokens de curta duração, aplicar validação pesada apenas em operações críticas (checkout) e manter catálogo de produtos em CDN com dados públicos. A arquitectura separa caminhos críticos (pagamento) de caminhos de leitura (listagem).

4. **Utilizador final:** experiência simples no checkout. **Gestor de negócio:** lançamento rápido de novas funcionalidades. **Desenvolvedor:** código legível e testável. **Equipa de operações:** monitorização e deploy sem downtime. Cada grupo optimiza métricas diferentes.

5. Resposta profissional: microserviços não são objectivo em si; são meio para atributos como escalabilidade independente e autonomia de equipas. Perguntaria: qual o tamanho da equipa? Qual a carga esperada? Há domínios de negócio claramente separáveis? Qual a maturidade de DevOps? Um monolito modular pode ser mais adequado numa fase inicial. A decisão deve basear-se em requisitos de qualidade e contexto organizacional, não em moda.

6. Exemplo: escolher base de dados relacional vs. NoSQL para o armazenamento principal de transacções. Migrar de MongoDB para PostgreSQL (ou vice-versa) após anos de dados acumulados, queries optimizadas e lógica acoplada ao modelo implica reescrita massiva, migração de dados e risco operacional elevado. Decisões de persistência afectam esquemas, consistência e padrões de acesso em todo o sistema.

7. **Manutenibilidade** favorece-se em sistemas de longa duração com equipas grandes e requisitos em evolução — código limpo, testes e modularidade reduzem custo de mudança. **Desempenho** prioriza-se em sistemas de tempo real (trading, jogos, streaming) onde milissegundos importam. Sacrificar manutenibilidade por desempenho extremo (código optimizado, menos abstracções) só se justifica quando métricas mensuráveis o exigem e o domínio é estável.

8. O arquitecto lidera a definição da visão técnica do produto, trabalhando com negócio para traduzir objectivos em requisitos arquitecturais. Facilita workshops com stakeholders, propõe alternativas com trade-offs explícitos, documenta decisões e estabelece guidelines para equipas de desenvolvimento. Durante a concepção, garante que a solução proposta é viável, alinhada com a estratégia da empresa e equilibrada entre time-to-market, custo e qualidade, sem entrar prematuramente em detalhes de implementação.
