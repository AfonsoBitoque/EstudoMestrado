# Soluções — Exercícios 51–76

---

## §51 — Ex. 51
| | AES | SHA-256 |
|---|-----|---------|
| Tipo | Cifra simétrica reversível | Hash unidireccional |
| Chave | Sim | Não (ou HMAC) |
| Output | Mesmo tamanho bloco | 256 bits fixo |

## §52 — Ex. 52
(a) **Preimage:** dado h(x), achar x

(b) **2nd preimage:** dado x, achar y≠x com h(x)=h(y)

(c) **Collision:** achar quaisquer x≠y com h(x)=h(y)

## §53 — Ex. 53
Paradoxo aniversário: ~2^(n/2) tentativas para colisão em n-bit hash. Ataque certificados MD5, assinaturas fracas.

## §54 — Ex. 54
**Merkle-Damgård** (SHA-2), **Sponge** (SHA-3), compressão iterativa por blocos.

## §55 — Ex. 55
Mensagem = 125 bytes zero (1000 bits):
```
MD5:     38397588c4d02f8b95c263852e9aee7a
SHA-256: 42d699d9e89e439804c0981f96b1a3fa7dbe42c6be1dbca6211c6faa4e0e2463
SHA-512: e46b5c1865b53513bb10be9e3a2c2a54ee9e88f83e8802e85e728a2364ab649ecd4af605b41d7583688f8a78d1b49e36f1ef5b8824ab89885578eed8ebdbfd15
SHA3-256:463ee12af80481cf70bfd385bfce4987d3e54f28f9057aeb5c12a8fd6fde3d9e
```

## §56 — Ex. 56
Primeiro bit = 1 (byte0 = 0x80):
```
SHA-256: b63bc2dbfc7e40b2bdc5dd65f529df02bd17d3af93ed5a52d137384aba18bbef
```
(Outros: recalcular com OpenSSL/Python)

## §57 — Ex. 57
Alternativa caso SHA-2 quebrado; concurso NIST 2007–2012; construção sponge diferente.

## §58 — Ex. 58
Resposta: **(b)** — determinístico.

## §59 — Ex. 59
**Assinaturas digitais** — atacante não pode substituir documento mantendo hash válido (2nd preimage).

## §60 — Ex. 60
MAC usa **chave secreta** — impossível verificar sem chave. TLS record MAC, API auth tokens.

## §61 — Ex. 61
Forgery permite **mensagens falsas autênticas** — transferências, comandos IoT.

## §62 — Ex. 62
HMAC(k,m) = H((k⊕opad) || H((k⊕ipad) || m))

## §63 — Ex. 63
CMAC = CBC-MAC sobre AES com chave derivada, tag truncada.

## §64 — Ex. 64
(a) Atacante **reordena/blocos** CBC sem detecção (só confidencialidade).

(b) **Encrypt-then-MAC** ou **AEAD** (GCM, ChaCha20-Poly1305).

## §65 — Ex. 65
PRF ≈ MAC para segurança; PRF mais forte (pseudorandom); MAC focado autenticidade.

## §66 — Ex. 66
Chaves **diferentes** encriptação/desencriptação (assimétrico) vs **iguais** (simétrico).

## §67 — Ex. 67
**Parcialmente** — chaves públicas distribuíveis; mas autenticidade chaves (PKI) e forward secrecy ainda desafios.

## §68 — Ex. 68
Exemplo mínimo: p=3, q=11, n=33, φ=20, e=3, d=7. Enc(m=5)=5³ mod 33=26. Dec(26)=26⁷ mod 33=5.

## §69 — Ex. 69
p=23, g=5. Alice a=6, Bob b=15. A=8, B=19. s=19⁶ mod 23=19=8¹⁵ mod 23.

## §70 — Ex. 70
Mesma segurança com **chaves menores** (256-bit ECC ≈ 3072-bit RSA), mais rápido, menos bandwidth.

## §71 — Ex. 71
Grover reduz simétrico n-bit → **n/2** efectivo. AES-128 → ~64 bits. Usar **AES-256** para margem pós-quântica.

## §72 — Ex. 72
Shor quebra **RSA, DH, ECC**. Migrar para **PQC** (Kyber, Dilithium).

## §73 — Ex. 73
Root CA → Intermediate CA → Entity certificates. Cadeia de confiança até anchor.

## §74 — Ex. 74
AES-256 dá **128 bits** pós-Grover (256/2). **Sim** atingível com AES-256.

## §75 — Ex. 75
Atacante **intercepta** A↔B, fala com ambos separadamente, reencaminha/modifica (sem certificados/autenticação).

## §76 — Ex. 76
(a) Segurança n → ~n/2 (Grover)

(b) Dobrar tamanho chave simétrica (AES-256)

(c) RSA/ECC/DH **quebrados** por Shor

(d) Adoptar **criptografia pós-quântica** (NIST PQC 2024)
