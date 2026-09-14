# Módulo 02 — Tipos de Cifras

**UC:** Criptografia Moderna · **Fase:** 1 — Fundamentos

## Objetivos de aprendizagem

- Distinguir cifras de fluxo (stream) e cifras de bloco (block)
- Compreender os modos de operação de cifras de bloco e os seus requisitos de segurança
- Identificar quando usar cada tipo de cifra e modo
- Reconhecer erros comuns (reutilização de IV, ECB com padrões)

---

## 1. Cifras de fluxo (Stream Ciphers)

Processam a mensagem **bit a bit** ou **byte a byte**, combinando o plaintext com um **keystream** (sequência pseudoaleatória).

```
Keystream:  k₁ k₂ k₃ k₄ ...
Plaintext:  m₁ m₂ m₃ m₄ ...
Ciphertext: c₁ c₂ c₃ c₄ ...   onde cᵢ = mᵢ ⊕ kᵢ
```

### Características

- Velocidade elevada em hardware e software
- Baixa latência (não esperam bloco completo)
- Requer **nonces/IV únicos** por mensagem (ex.: ChaCha20, Salsa20)
- Vulneráveis se o keystream for reutilizado (two-time pad)

### Exemplos

| Algoritmo | Estado |
|-----------|--------|
| ChaCha20-Poly1305 | ✅ Moderno, usado em TLS e Signal |
| RC4 | ❌ Quebrado, descontinuado |
| One-Time Pad | ✅ Teoricamente perfeito, impraticável |

---

## 2. Cifras de bloco (Block Ciphers)

Cifram **blocos fixos** de dados (tipicamente 128 bits no AES).

```
Bloco plaintext (128 bits) → [E(K, ·)] → Bloco ciphertext (128 bits)
```

### Algoritmos principais

| Algoritmo | Tamanho bloco | Tamanhos chave | Estado |
|-----------|---------------|----------------|--------|
| **AES** | 128 bits | 128, 192, 256 bits | ✅ Padrão atual |
| **DES** | 64 bits | 56 bits efetivos | ❌ Obsoleto |
| **3DES** | 64 bits | 112/168 bits | ⚠️ Legacy, descontinuar |

Uma cifra de bloco sozinha só cifra um bloco. Para mensagens longas, usa-se um **modo de operação**.

---

## 3. Modos de operação — visão geral

### ECB (Electronic Codebook) — ❌ Evitar

Cada bloco é cifrado independentemente: \( C_i = E(K, M_i) \)

**Problema:** Blocos iguais produzem ciphertexts iguais → revela padrões (famoso "Tux penguin").

### CBC (Cipher Block Chaining)

\( C_i = E(K, M_i \oplus C_{i-1}) \), com \( C_0 = IV \)

- IV deve ser **imprevisível** (idealmente aleatório)
- Erro num bloco afeta dois blocos na descifragem
- Requer padding (PKCS#7)

### CTR (Counter)

\( C_i = M_i \oplus E(K, \text{nonce} \| \text{counter}_i) \)

- Converte cifra de bloco em stream cipher
- Paralelizável (cifragem e decifragem)
- **Nonce único** por chave — reutilização é catastrófica

### GCM (Galois/Counter Mode) — ✅ Recomendado

- CTR + autenticação integrada (AEAD)
- Produz ciphertext **e** tag de autenticação
- Padrão em TLS 1.3: AES-GCM, ChaCha20-Poly1305

```
┌─────────┐    ┌──────────┐    ┌────────────┐
│ Plaintext│ → │ AES-GCM  │ → │ Ciphertext │
│    + AAD │    │  + Key   │    │  + Tag   │
└─────────┘    └──────────┘    └────────────┘
```

---

## 4. AEAD (Authenticated Encryption with Associated Data)

Combina **confidencialidade** e **integridade/autenticidade** numa única operação.

| Modo | Algoritmo base | Uso |
|------|----------------|-----|
| GCM | AES | TLS, VPNs, disco encriptado |
| Poly1305-ChaCha20 | ChaCha20 | TLS, Signal, WireGuard |
| CCM | AES | IEEE 802.15.4, ZigBee |

**Regra de ouro:** Nunca usar cifragem sem autenticação (encrypt-then-MAC ou AEAD).

---

## 5. Comparação stream vs. block

| Aspeto | Stream | Block (+ modo) |
|--------|--------|----------------|
| Unidade | Bit/byte | Bloco (128 bits) |
| Paralelismo | Limitado | CTR/GCM: sim |
| Padding | Não necessário | CBC: sim |
| Autenticação | Externa (Poly1305) | Integrada (GCM) |
| Exemplos | ChaCha20 | AES-GCM |

---

## 6. Padding (PKCS#7)

Para CBC, mensagens devem ter tamanho múltiplo do bloco. PKCS#7 adiciona \( n \) bytes com valor \( n \):

```
Mensagem: "HELLO" (5 bytes)
Bloco 16 bytes → padding: 11 bytes com valor 0x0B
```

---

## Exercícios

### Exercício 1
Explique porque o modo ECB não deve ser usado para cifrar imagens ou ficheiros com padrões repetitivos.

### Exercício 2
Uma aplicação usa AES-CTR com o mesmo nonce para duas mensagens diferentes. Que vulnerabilidade surge?

### Exercício 3
Qual a diferença entre CBC e CTR quanto ao paralelismo e necessidade de padding?

### Exercício 4
Porque é preferível AES-GCM em vez de AES-CBC + HMAC separado?

### Exercício 5
Uma mensagem de 34 bytes é cifrada com AES (bloco 16 bytes) em modo CBC. Quantos bytes de padding PKCS#7 são adicionados?

### Exercício 6
Classifique como cifra de fluxo ou bloco: (a) ChaCha20, (b) AES, (c) RC4, (d) 3DES.

### Exercício 7
Descreva o papel do IV/nonce nos modos CBC e CTR. O IV deve ser mantido em segredo?

### Exercício 8
Um sistema usa AES-ECB para cifrar bases de dados com muitos registos idênticos. Que ataque passivo é possível?

---

## Soluções

### Solução 1
ECB cifra cada bloco independentemente. Blocos de plaintext iguais (ex.: áreas brancas numa imagem) produzem ciphertexts idênticos, revelando a estrutura visual. O padrão do plaintext fica visível no ciphertext.

### Solução 2
Reutilizar nonce em CTR é equivalente a reutilizar keystream (two-time pad): \( C_1 \oplus C_2 = M_1 \oplus M_2 \). Se o adversário conhecer uma mensagem, recupera a outra.

### Solução 3
- **CBC:** encadeamento sequencial → cifragem não paralelizável; decifragem parcialmente paralelizável; **requer padding**
- **CTR:** contador incrementado → **cifragem e decifragem paralelizáveis**; **sem padding** (XOR com keystream)

### Solução 4
GCM (AEAD) garante atomicamente confidencialidade e integridade, evitando erros de composição (MAC-then-encrypt vs. encrypt-then-MAC). É mais eficiente (hardware AES-NI + GHASH) e menos propenso a implementações incorretas.

### Solução 5
34 bytes ocupam 3 blocos (48 bytes). Padding = 48 − 34 = **14 bytes**, cada um com valor 0x0E.

### Solução 6
- (a) ChaCha20 → **fluxo**
- (b) AES → **bloco** (requer modo de operação)
- (c) RC4 → **fluxo**
- (d) 3DES → **bloco**

### Solução 7
- **CBC:** IV aleatório imprevisível no primeiro bloco; garante que mensagens iguais produzem ciphertexts diferentes. **Não precisa ser secreto**, mas deve ser único e imprevisível.
- **CTR:** nonce + contador inicializam o keystream. **Nonce deve ser único por chave**; não precisa ser secreto, mas repetição compromete toda a segurança.

### Solução 8
**Análise de frequência de blocos:** o adversário identifica quais registos têm blocos iguais, inferindo igualdade de campos sem descifrar. Pode correlacionar registos e extrair metadados sensíveis.
