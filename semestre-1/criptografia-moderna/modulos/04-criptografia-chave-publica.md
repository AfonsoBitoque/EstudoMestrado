# Módulo 04 — Criptografia de Chave Pública (Assimétrica)

**UC:** Criptografia Moderna · **Fase:** 2 — Cifras simétricas e assimétricas

## Objetivos de aprendizagem

- Compreender o paradigma de chave pública/privada
- Explicar o funcionamento do RSA, ECC e Diffie-Hellman
- Comparar algoritmos assimétricos em termos de segurança e performance
- Identificar aplicações: troca de chaves, assinaturas, cifragem

---

## 1. O problema da chave simétrica

Com cifras simétricas, \( n \) participantes precisam de \( O(n^2) \) chaves. A distribuição inicial é o **problema central**.

**Solução (Diffie-Hellman, 1976; RSA, 1977):** cada entidade tem um par de chaves:

```
Chave pública  (K_pub)  → partilhada livremente
Chave privada  (K_priv) → mantida em segredo
```

---

## 2. Diffie-Hellman (DH) — troca de chaves

Permite que duas partes estabeleçam um **segredo partilhado** sobre um canal inseguro.

### Parâmetros públicos

- Número primo grande \( p \)
- Gerador \( g \) do grupo multiplicativo \( \mathbb{Z}_p^* \)

### Protocolo

```
Alice                          Bob
a ← random                    b ← random
A = g^a mod p                 B = g^b mod p
────── A ──────────────────→
←───── B ────────────────────
s = B^a mod p                 s = A^b mod p
     = g^(ab) mod p                = g^(ab) mod p
```

Ambas obtêm o mesmo segredo \( s = g^{ab} \mod p \).

### Variantes modernas

| Variante | Grupo | Segurança |
|----------|-------|-----------|
| **FFDHE** | \( \mathbb{Z}_p^* \) (primos RFC 7919) | ≥ 2048 bits |
| **ECDH** | Curva elíptica | 256 bits (P-256) ≈ RSA-3072 |
| **X25519** | Curve25519 | Usado em TLS 1.3, Signal |

**Importante:** DH sozinho **não autentica** — vulnerável a MITM. Requer autenticação (certificados, signatures).

---

## 3. RSA

Baseado na dificuldade de factorizar \( n = p \times q \) (inteiros grandes).

### Geração de chaves

1. Escolher primos \( p, q \) grandes
2. \( n = p \times q \), \( \phi(n) = (p-1)(q-1) \)
3. Escolher \( e \) (exponente público, tipicamente 65537)
4. Calcular \( d \equiv e^{-1} \pmod{\phi(n)} \)
5. Chave pública: \( (n, e) \); privada: \( (n, d) \)

### Operações

- **Cifragem:** \( C = M^e \mod n \)
- **Decifragem:** \( M = C^d \mod n \)
- **Assinatura:** \( S = H(M)^d \mod n \)
- **Verificação:** \( H(M \stackrel{?}{=} S^e \mod n \)

### Padding obrigatório

| Uso | Padding |
|-----|---------|
| Cifragem | **OAEP** (RSAES-OAEP) |
| Assinatura | **PSS** (RSASSA-PSS) |

**Nunca** usar RSA "textbook" (sem padding) — determinístico e inseguro.

### Tamanhos recomendados (2025)

| Uso | Mínimo |
|-----|--------|
| RSA cifragem/assinatura | 2048 bits |
| Longo prazo | 3072 ou 4096 bits |

---

## 4. ECC — Criptografia de Curvas Elípticas

Opera no grupo de pontos de uma **curva elíptica** sobre corpo finito.

### Vantagens sobre RSA

| Aspeto | RSA-3072 | ECDSA P-256 |
|--------|----------|-------------|
| Segurança equivalente | ~128 bits | ~128 bits |
| Tamanho chave | 3072 bits | 256 bits |
| Velocidade | Mais lento | Mais rápido |
| Assinatura | ~384 bytes | ~64 bytes |

### Curvas comuns

| Curva | Uso |
|-------|-----|
| **P-256 (secp256r1)** | Certificados, TLS |
| **Curve25519 / X25519** | ECDH moderno |
| **Ed25519** | Assinaturas (EdDSA) |

### ECDSA vs. Ed25519

- **ECDSA:** requer nonce aleatório único por assinatura — falhas de implementação são catastróficas (Sony PS3)
- **Ed25519:** determinístico, mais robusto, preferido em sistemas novos

---

## 5. Comparação e aplicações

| Algoritmo | Cifragem | Assinatura | Troca chaves | Performance |
|-----------|----------|------------|--------------|-------------|
| RSA | ✅ (lenta) | ✅ | ❌ | Lenta |
| ECDH | ❌ | ❌ | ✅ | Rápida |
| ECDSA/Ed25519 | ❌ | ✅ | ❌ | Rápida |
| ElGamal | ✅ | ❌ | ❌ | Média |

**Padrão moderno (TLS 1.3):**

```
ECDH (X25519) → chave de sessão simétrica → AES-GCM / ChaCha20
Certificado ECDSA/Ed25519 → autenticação do servidor
```

---

## 6. Híbrido simétrico + assimétrico

A cifragem assimétrica é **~1000× mais lenta** que simétrica. Na prática:

1. Troca de chaves assimétrica (ECDH) → chave de sessão
2. Dados cifrados com simétrico (AES-GCM)
3. Assinatura assimétrica para autenticidade

---

## Exercícios

### Exercício 1
Alice e Bob usam Diffie-Hellman sem autenticação. Descreva um ataque MITM.

### Exercício 2
RSA com \( n = 143 = 11 \times 13 \), \( e = 7 \). Calcule \( \phi(n) \) e o expoente privado \( d \).

### Exercício 3
Porque RSA "textbook" (sem OAEP) é inseguro para cifragem?

### Exercício 4
Compare o tamanho de chave RSA-3072 e ECDSA P-256 para ~128 bits de segurança. Qual a implicação em dispositivos IoT?

### Exercício 5
Num sistema híbrido TLS, qual o papel de ECDH e AES-GCM?

### Exercício 6
Explique porque reutilizar o nonce \( k \) em ECDSA permite recuperar a chave privada.

### Exercício 7
\( g = 2 \), \( p = 23 \). Alice envia \( A = 8 \), Bob envia \( B = 19 \). Calcule o segredo partilhado (dado \( a = 3 \), \( b = 14 \)).

### Exercício 8
Quais as três operações principais que RSA suporta e que padding deve ser usado em cada?

---

## Soluções

### Solução 1
Mallory intercepta: recebe \( A \) de Alice, envia \( M_A = g^{m_1} \) a Bob; recebe \( B \) de Bob, envia \( M_B = g^{m_2} \) a Alice. Mallory calcula segredos separados com cada um. Alice e Bob pensam comunicar entre si, mas Mallory decifra/reencripta todo o tráfego.

### Solução 2
\( \phi(n) = (11-1)(13-1) = 10 \times 12 = 120 \).  
\( d = e^{-1} \mod 120 \): \( 7 \times 103 = 721 = 6 \times 120 + 1 \), logo **\( d = 103 \)**.

### Solução 3
Textbook RSA é **determinístico**: mesma mensagem → mesmo ciphertext. Permite ataques de chosen-plaintext, multiplicative ( \( E(m_1) \cdot E(m_2) = E(m_1 \cdot m_2) \) ) e não tem proteção semântica (IND-CPA). OAEP adiciona randomização e prova de segurança.

### Solução 4
RSA-3072: chave pública ~384 bytes; P-256: ~32 bytes. Em IoT (memória/banda limitada), ECC reduz overhead de certificados, assinaturas e consumo energético na handshake.

### Solução 5
- **ECDH:** troca segura da chave de sessão simétrica (confidencialidade futura se ephemeral)
- **AES-GCM:** cifragem autenticada dos dados em volume (velocidade + AEAD)

### Solução 6
ECDSA: \( s = k^{-1}(H(m) + r \cdot d) \mod n \). Duas assinaturas com mesmo \( k \) permitem eliminar \( k \) e resolver para \( d \). Por isso \( k \) deve ser único e imprevisível (Ed25519 evita isto).

### Solução 7
Verificação: \( 2^3 \mod 23 = 8 = A \) ✓; \( 2^{14} \mod 23 = 19 = B \) ✓.  
Segredo: \( s = 8^{14} \mod 23 = 19^3 \mod 23 \).  
\( 8^{14} = (2^3)^{14} = 2^{42} \mod 23 \). Por Fermat: \( 2^{22} \equiv 1 \), \( 2^{42} = 2^{20} = 1048576 \mod 23 \).  
\( 1048576 / 23 = 45590 \) resto **2**. Segredo = **2** (equivalentemente \( 19^3 = 6859 \mod 23 = 2 \)).

### Solução 8
1. **Cifragem** → RSAES-OAEP  
2. **Assinatura** → RSASSA-PSS  
3. **Verificação de assinatura** → RSASSA-PSS (lado público, sem padding adicional)
