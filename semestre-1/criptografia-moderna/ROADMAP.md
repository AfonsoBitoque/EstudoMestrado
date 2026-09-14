# Roadmap — Criptografia Moderna

**UC:** 14741103 · **ECTS:** 6 · **Docente:** Daniel Graça · **Ano:** 2026/27  
**Pré-requisitos:** Nenhum formal

> **Guia principal:** [GUIA-MATERIAIS.md](./GUIA-MATERIAIS.md) — Course notes, Slides, Exercises, Project (PDFs locais)

---

## Materiais do professor

| Material | Uso | Guia |
|----------|-----|------|
| **Course notes.pdf** | Texto de referência (69 p.) | Capítulos 1–7 abaixo |
| **Slides.pdf** | Aulas (129 slides) | Diagramas, definições |
| **Exercises.pdf** | 76 exercícios oficiais | [exercicios/INDICE.md](./exercicios/INDICE.md) |
| **Project.pdf** | Trabalho 70% | [PROJETO.md](./PROJETO.md) |

---

## Percurso alinhado com Course notes

### Cap. 1 — Introduction (Semanas 1–2)

| Ordem | Módulo | Course notes | Exercícios | Slides |
|-------|--------|--------------|------------|--------|
| 1 | [01-principios-fundamentais](./modulos/01-principios-fundamentais.md) | §1.1–1.2 Kerckhoffs | 11–21, 20 | p.1–35 |
| 2 | [02-tipos-cifras](./modulos/02-tipos-cifras.md) | §1.1 história, §1.3 OTP | 1–10, 22–29 | Caesar, Vigenère, OTP |

**Checkpoint:** Explicar Kerckhoffs + decifrar shift cipher (ex. 3–4).

### Cap. 2 — Symmetric encryption (Semanas 3–4)

| Ordem | Módulo | Course notes | Exercícios |
|-------|--------|--------------|------------|
| 3 | [03-criptografia-chave-privada](./modulos/03-criptografia-chave-privada.md) | §2.2 DES/AES, §2.2.3 modes | 31–50 |

**Checkpoint:** AES CBC com Python (ex. 39–41) + explicar porquê não ECB.

### Cap. 3–4 — Hashes & MACs (Semana 5)

| Ordem | Módulo | Course notes | Exercícios |
|-------|--------|--------------|------------|
| 4 | [05-funcoes-dispersao](./modulos/05-funcoes-dispersao.md) | Cap. 3–4 | 51–65 |

**Checkpoint:** Calcular SHA-256 (ex. 55) + explicar HMAC.

### Cap. 5 — Asymmetric (Semana 6)

| Ordem | Módulo | Course notes | Exercícios |
|-------|--------|--------------|------------|
| 5 | [04-criptografia-chave-publica](./modulos/04-criptografia-chave-publica.md) | Cap. 5 RSA/DH/ECC | 66–70, 75 |

**Checkpoint:** Exemplo numérico RSA (ex. 68) e DH (ex. 69).

### Cap. 6–7 — Quantum & PKI (Semanas 7–8)

| Ordem | Módulo | Course notes | Exercícios |
|-------|--------|--------------|------------|
| 6 | [06-limitacoes-ameacas-quantica](./modulos/06-limitacoes-ameacas-quantica.md) | Cap. 6 | 71–72, 76 |
| 7 | [07-distribuicao-chaves-assinaturas](./modulos/07-distribuicao-chaves-assinaturas.md) | Cap. 7 PKI | 73–74 |
| — | [PROJETO.md](./PROJETO.md) | — | Trabalho 70% |
| — | [materia-extra.md](./materia-extra.md) | — | Complementar |

**Checkpoint final:** Explicar MITM + implicações quânticas (ex. 75–76).

---

## Exercícios oficiais — soluções

| Ficheiro | Exercícios |
|----------|------------|
| [SOLUCOES-01-30.md](./exercicios/SOLUCOES-01-30.md) | Clássicas, OTP, key space |
| [SOLUCOES-31-50.md](./exercicios/SOLUCOES-31-50.md) | Simétrico, AES, modos |
| [SOLUCOES-51-76.md](./exercicios/SOLUCOES-51-76.md) | Hash, MAC, assimétrico, quantum |

---

## Avaliação

| Componente | Peso |
|------------|------|
| Teste individual | **30%** |
| Projeto + defesa | **70%** |
| Exame (opcional) | 30% + 70% projeto |

- Dispensa exame: ≥ **9,5** contínua
- **IA proibida** em testes/exames

---

## Ferramentas

```bash
pip install cryptography
python3 semestre-1/criptografia-moderna/scripts/aes_exercicios.py
openssl dgst -sha256 file
```

- OpenSSL CLI · Python `cryptography` · Wireshark (TLS)
