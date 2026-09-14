# Guia de Materiais — Criptografia Moderna

**Docente:** Daniel Graça · **Ano:** 2026/27 · **UAlg FCT**

Materiais oficialmente disponibilizados pelo professor (PDFs locais — **não publicar** no repositório):

| Ficheiro | Conteúdo | Páginas |
|----------|----------|---------|
| **Course notes.pdf** | Apontamentos completos (texto de referência) | 69 |
| **Slides.pdf** | Apresentações das aulas | 129 |
| **Exercises.pdf** | Lista de exercícios (1–76) | 12 |
| **Project.pdf** | Enunciado do projeto/trabalho | 1 |

---

## Como estudar (ordem recomendada)

```
1. Slides (aula)  →  visão geral + diagramas
2. Course notes   →  aprofundamento + definições formais
3. Módulos repo   →  resumo PT + exercícios extra
4. Exercises.pdf  →  exercícios oficiais (INDICE abaixo)
5. Soluções       →  exercicios/SOLUCOES-*.md (depois de tentar!)
6. Projeto        →  PROJETO.md
```

---

## Course notes — estrutura (capítulos)

| Cap. | Título | Módulo repo | Slides (aprox.) | Exercícios |
|------|--------|-------------|-----------------|------------|
| 1 | Introduction (história, Kerckhoffs, OTP, segurança) | [01](./modulos/01-principios-fundamentais.md), [02](./modulos/02-tipos-cifras.md) | p.1–35 | 1–30 |
| 2 | Symmetric encryption (block, stream, DES, AES, modes) | [03](./modulos/03-criptografia-chave-privada.md) | p.36–58 | 31–50 |
| 3 | Hash functions | [05](./modulos/05-funcoes-dispersao.md) | p.59–67 | 51–59 |
| 4 | MACs (HMAC, CMAC, AEAD) | [05](./modulos/05-funcoes-dispersao.md) §MAC | p.68–74 | 60–65 |
| 5 | Asymmetric encryption (RSA, DH, ECC) | [04](./modulos/04-criptografia-chave-publica.md) | p.75–90 | 66–70 |
| 6 | Post-quantum cryptography | [06](./modulos/06-limitacoes-ameacas-quantica.md) | p.91–125 | 71–72, 76 |
| 7 | Public-Key Infrastructure | [07](./modulos/07-distribuicao-chaves-assinaturas.md) | p.126–129 | 73–75 |

---

## Slides — tópicos principais

| Tema | Conteúdo-chave |
|------|----------------|
| Objetivos UC | Termos, primitivas, garantias de segurança, uso prático |
| Cifras históricas | Caesar, shift, substituição, Vigenère, Kasiski, coincidência |
| OTP & Shannon | XOR, perfect secrecy, \|K\|≥\|M\|, computational security |
| n-bit security | ~2^n operações; segurança ≠ tamanho da chave (RSA) |
| Attack models | Ciphertext-only → chosen-ciphertext; side-channels |
| Kerckhoffs | Inimigo conhece o sistema; chave secreta |
| Taxonomia Martin | Unstudied → Broken → Respected → Default ciphers |
| Block ciphers | Rounds, SPN vs Feistel, DES, AES (SubBytes, ShiftRows…) |
| Modes | **ECB (não usar!)**, CBC, OFB, CFB, CTR |
| Ataques | Codebook, meet-in-the-middle, padding oracle |
| Stream ciphers | Keystream, RC4/A5/1 quebrados, ChaCha |
| Hashes | Preimage, 2nd preimage, collision; MD/SHA/SHA-3 |
| MACs | HMAC, CMAC, encrypt-then-MAC |
| RSA, DH, ECDH | Math + protocolos |
| Post-quantum | LWE/Kyber, Dilithium, hash-based (MSS) |
| PKI | Hierárquica, certificados X.509 |

---

## Exercícios oficiais (76)

Índice completo com ligação às soluções: [exercicios/INDICE.md](./exercicios/INDICE.md)

| Bloco | Exercícios | Tema |
|-------|------------|------|
| A | 1–10 | Cifras clássicas (shift, substituição, Vigenère) |
| B | 11–21 | Kerckhoffs, key space, segurança em bits, WPA2 |
| C | 22–30 | Vigenère, OTP, Crypto AG |
| D | 31–38 | Simétrico vs assimétrico, DES, 3DES, Feistel, S-box |
| E | 39–50 | AES (Python), modos, ataques, stream vs block |
| F | 51–65 | Hashes, birthday, HMAC, CMAC, MAC vs encrypt |
| G | 66–76 | RSA, DH, ECC, quantum, PKI, MITM |

Soluções: [exercicios/SOLUCOES-01-30.md](./exercicios/SOLUCOES-01-30.md), [31-50](./exercicios/SOLUCOES-31-50.md), [51-76](./exercicios/SOLUCOES-51-76.md)

---

## Avaliação

| Componente | Peso |
|------------|------|
| Teste individual | **30%** |
| Projeto + defesa individual | **70%** |
| Exame (se não dispensado) | 30% exame + 70% projeto |

- Dispensa exame com ≥ **9,5** na avaliação contínua
- **IA proibida** em testes/exames; permitida como apoio ao estudo (com declaração no projeto)

Detalhes do projeto: [PROJETO.md](./PROJETO.md)

---

## Ferramentas (mencionadas nos exercícios)

```bash
# Python cryptography (ex. 39–41)
pip install cryptography

# OpenSSL (hashes ex. 55–56)
echo -n ... | openssl dgst -sha256

# Exemplo AES ECB
python3 semestre-1/criptografia-moderna/scripts/aes_exercicios.py
```

---

## Pré-requisitos (slides)

- Módulo, números primos, probabilidade básica
- Representação bits/bytes (texto, imagens)
- Mentalidade atacante/defensor

---

## Política de IA (UC)

- Testes/exames: **sem IA**
- Estudo: IA permitida como apoio
- Projeto: IA só para tarefas que **não substituam** raciocínio humano (figuras, gramática); **declarar** uso
