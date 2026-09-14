# Roadmap — Criptografia Moderna

**UC:** 14741103 · **ECTS:** 6 · **Língua:** PT ou EN (conforme turma)  
**Pré-requisitos:** Nenhum formal

## Objetivos de aprendizagem (resumo)

- Conhecer sistemas criptográficos: sequenciais, por blocos, simétricos e assimétricos
- Utilizar sistemas criptográficos na prática
- Reconhecer limitações e ameaças (incl. criptografia quântica)
- Compreender distribuição de chaves e aplicações (TLS, assinaturas, etc.)

## Percurso de estudo (6–8 semanas)

### Fase 1 — Fundamentos (Semanas 1–2)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 1 | [01-principios-fundamentais](./modulos/01-principios-fundamentais.md) | Princípios e conceitos | 4–6 h |
| 2 | [02-tipos-cifras](./modulos/02-tipos-cifras.md) | Tipos de cifras | 5–7 h |

**Checkpoint:** Distinguir confidencialidade, integridade, autenticidade e não-repúdio com exemplos.

### Fase 2 — Cifras simétricas e assimétricas (Semanas 3–5)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 3 | [03-criptografia-chave-privada](./modulos/03-criptografia-chave-privada.md) | Criptografia simétrica | 6–8 h |
| 4 | [04-criptografia-chave-publica](./modulos/04-criptografia-chave-publica.md) | Criptografia assimétrica | 6–8 h |
| 5 | [05-funcoes-dispersao](./modulos/05-funcoes-dispersao.md) | Hash functions | 4–6 h |

**Checkpoint:** Implementar AES-GCM e RSA-OAEP com biblioteca (OpenSSL/Python cryptography).

### Fase 3 — Aplicações e ameaças (Semanas 6–8)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 6 | [06-limitacoes-ameacas-quantica](./modulos/06-limitacoes-ameacas-quantica.md) | Limitações e ameaças | 4–6 h |
| 7 | [07-distribuicao-chaves-assinaturas](./modulos/07-distribuicao-chaves-assinaturas.md) | PKI, assinaturas, aplicações | 6–8 h |
| — | [materia-extra.md](./materia-extra.md) | Complementar | Contínuo |

**Checkpoint final:** Explicar handshake TLS 1.3 e verificar assinatura digital de um documento.

## Avaliação (referência)

- **30%** — Teste individual
- **70%** — Projeto/trabalho com defesa individual
- Dispensa exame com ≥ 9,5 na avaliação contínua
- **IA proibida** em testes/exames; permitida como apoio ao estudo

## Ferramentas práticas

- OpenSSL CLI
- Python `cryptography` library
- Wireshark (TLS analysis)
- GnuPG (PGP)

## Ligações úteis

- [Cryptopals Challenges](https://cryptopals.com/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
