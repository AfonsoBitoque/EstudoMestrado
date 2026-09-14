# Módulo 03 — Criptografia de Chave Privada (Simétrica)

**UC:** Criptografia Moderna · **Fase:** 2 — Cifras simétricas e assimétricas

## Objetivos de aprendizagem

- Compreender o funcionamento e aplicações do AES
- Conhecer a evolução histórica do DES até ao AES
- Analisar desafios de gestão de chaves simétricas
- Aplicar boas práticas na geração, armazenamento e rotação de chaves

---

## 1. Criptografia simétrica — conceito

A **mesma chave** cifra e decifra:

```
Alice ── E(K, M) ──→ Bob
Bob  ←── D(K, C) ───
```

**Vantagens:** velocidade, eficiência, baixo overhead  
**Desvantagem principal:** distribuição segura da chave entre partes

---

## 2. DES — Data Encryption Standard

| Aspeto | Detalhe |
|--------|---------|
| Ano | 1977 (NIST) |
| Tamanho bloco | 64 bits |
| Tamanho chave | 64 bits (56 efetivos + 8 paridade) |
| Estrutura | Feistel, 16 rondas |
| Estado | **Obsoleto** — quebrado por força bruta (1998) |

### Evolução

```
DES (56 bits) → 2DES (inseguro) → 3DES (112/168 bits) → AES (substituto)
```

**3DES (Triple-DES):** \( E(K_3, D(K_2, E(K_1, M))) \) — ainda usado em legacy financeiro, mas **descontinuar** (NIST SP 800-131A).

---

## 3. AES — Advanced Encryption Standard

Selecionado em 2001 (Rijndael, Daemen & Rijmen). Substituiu o DES como padrão mundial.

| Parâmetro | Valor |
|-----------|-------|
| Tamanho bloco | **128 bits** (fixo) |
| Tamanhos chave | 128, 192, 256 bits |
| Rondas | 10 (AES-128), 12 (AES-192), 14 (AES-256) |
| Estrutura | Substitution-Permutation Network (SPN) |

### Operações por ronda

1. **SubBytes** — substituição não-linear (S-box)
2. **ShiftRows** — permutação de linhas
3. **MixColumns** — difusão (excepto última ronda)
4. **AddRoundKey** — XOR com chave de ronda

### Segurança actual

- AES-128: seguro com margem ampla
- AES-256: recomendado para dados de longa duração e resistência quântica parcial (Grover → 128 bits efetivos)

### Implementação

- **AES-NI:** instruções CPU Intel/AMD para aceleração hardware
- Modos recomendados: **GCM**, **CTR** (com HMAC se não AEAD)

---

## 4. Outras cifras simétricas

| Algoritmo | Notas |
|-----------|-------|
| **ChaCha20** | Stream cipher, excelente em software, sem AES-NI |
| **Camellia** | Alternativa japonesa, similar ao AES |
| **Blowfish/Twofish** | Legacy, ainda seguros mas menos usados |

---

## 5. Gestão de chaves simétricas

### Desafios

1. **Distribuição inicial** — como partilhar a chave de forma segura?
2. **Escalabilidade** — \( n \) utilizadores requerem \( \frac{n(n-1)}{2} \) chaves únicas
3. **Rotação** — periodicidade de troca de chaves
4. **Revogação** — invalidar chaves comprometidas
5. **Armazenamento** — proteger chaves em repouso

### Soluções

| Mecanismo | Descrição |
|-----------|-----------|
| **KDC (Key Distribution Center)** | Kerberos — centraliza emissão de chaves de sessão |
| **Diffie-Hellman + simétrico** | Troca de chave assimétrica → chave de sessão simétrica (TLS) |
| **HSM / TPM** | Hardware para armazenamento seguro |
| **Envelope encryption** | Chave de dados cifrada com chave mestra (AWS KMS, Azure Key Vault) |
| **Key derivation (KDF)** | HKDF, PBKDF2 — derivar chaves a partir de segredo base |

### Hierarquia de chaves

```
Chave mestra (HSM)
    ├── Chave de cifragem de dados (DEK) — rotacionada frequentemente
    ├── Chave de cifragem de chaves (KEK) — protege DEKs
    └── Chave de autenticação (MAC key)
```

---

## 6. Boas práticas

1. Usar **AES-256-GCM** ou **ChaCha20-Poly1305** (AEAD)
2. Gerar chaves com **CSPRNG** (`/dev/urandom`, `secrets` em Python)
3. **Nunca** hardcodar chaves no código fonte
4. Rotacionar chaves conforme política (ex.: 90 dias)
5. Usar **KDF** para derivar chaves de passwords (nunca usar password directamente como chave)
6. Separar chaves por **propósito** (encryption vs. MAC — evitar reutilização)

---

## Exercícios

### Exercício 1
Quantas chaves simétricas únicas são necessárias para 10 utilizadores comunicarem par-a-par de forma segura?

### Exercício 2
Porque o DES foi substituído? Quantas operações de força bruta são necessárias no pior caso?

### Exercício 3
Compare AES-128 e AES-256 em termos de rondas, segurança e impacto do algoritmo de Grover (ameaça quântica).

### Exercício 4
Explique o conceito de "envelope encryption" e porque é útil em serviços cloud.

### Exercício 5
Uma empresa usa a mesma chave AES para cifrar dados e calcular HMAC. Porque é isto problemático?

### Exercício 6
Descreva o papel do Kerberos como KDC na gestão de chaves.

### Exercício 7
Qual a diferença entre 3DES EDE (Encrypt-Decrypt-Encrypt) e EEE (Encrypt-Encrypt-Encrypt)? Qual é usado na prática?

### Exercício 8
Uma aplicação deriva a chave AES directamente da password do utilizador (sem KDF). Identifique dois problemas de segurança.

---

## Soluções

### Solução 1
\( \frac{n(n-1)}{2} = \frac{10 \times 9}{2} = \mathbf{45} \) chaves.

### Solução 2
Chave efectiva de 56 bits → \( 2^{56} \approx 7{,}2 \times 10^{16} \) tentativas. Quebrado por força bruta em horas (1998, EFF Deep Crack). Espaço de chaves demasiado pequeno para padrões actuais.

### Solução 3
- **AES-128:** 10 rondas, 128 bits de segurança; Grover reduz para ~64 bits efetivos
- **AES-256:** 14 rondas, 256 bits; Grover reduz para ~128 bits efetivos
- AES-256 recomendado para dados com vida útil longa pós-quantum

### Solução 4
Envelope encryption: a chave de dados (DEK) cifra os dados; a DEK é cifrada com uma chave mestra (KEK) no HSM/KMS. Permite rotacionar DEKs sem alterar KEK, auditar acessos centralizados e cumprir requisitos de compliance.

### Solução 5
Viola o princípio de **separação de chaves**. Ataques de related-key e composição incorrecta podem permitir forjar MACs ou recuperar chaves. Devem existir chaves independentes para cifragem e autenticação.

### Solução 6
Kerberos: utilizador autentica-se no KDC (TGT); KDC emite **tickets** com chaves de sessão temporárias para comunicação par-a-par. Evita \( n^2 \) chaves permanentes — cada par usa chave de sessão efémera.

### Solução 7
- **EDE:** \( E(K_3, D(K_2, E(K_1, M))) \) — padrão 3DES; retrocompatível com DES (\( K_1=K_2=K_3 \) → DES)
- **EEE:** três cifragens — mais seguro teoricamente mas sem retrocompatibilidade
- Na prática usa-se **EDE** (ANSI X9.52, SP 800-67)

### Solução 8
1. Passwords têm **entropia baixa** → chave fraca, vulnerável a dicionário
2. Sem **salt** nem iterações (KDF) → mesma password gera mesma chave; ataques rainbow table
3. Solução: PBKDF2, scrypt ou Argon2 para derivar chave de 256 bits
