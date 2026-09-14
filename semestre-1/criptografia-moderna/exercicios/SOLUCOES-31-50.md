# Soluções — Exercícios 31–50

---

## §31 — Ex. 31
(a) Simétrico: **n(n−1)/2 = 49 995 000** chaves (10000 pessoas)

(b) Assimétrico: **n = 10 000** pares de chaves (cada um publica chave pública)

## §32 — Ex. 32
Assimétrico permitiu **distribuição de chaves** e novas apps (assinaturas, SSL). Simétrico **não obsoleto** — muito mais rápido; híbrido (TLS: DH/RSA + AES).

## §33 — Ex. 33
2³² blocos × 32 bits ≈ 16 GB codebook — **viável** hoje; **inviável** para AES 128-bit.

## §34 — Ex. 34
Chave **56 bits** curta (brute-force 1999); design envelhecido; substituído por AES.

## §35 — Ex. 35
(a) Meet-in-the-middle: ~2⁵⁶+2⁵⁶ = 2⁵⁷ ops, não 2¹¹². Segurança efectiva **~112 bits** (2-key 3DES) ou **80 bits** (3-key variantes).

(b)(i) **EDE com Dec middle** permite Dec(k1,Dec(k2,Enc(k1,m))) = Enc(k1,m) — compatibilidade **single-DES** quando k1=k2=k3.

(ii) `Dec_k = Enc_k1(Dec_k2(Enc_k3(c)))`

## §36 — Ex. 36
**Não** — Feistel usa F **não** necessariamente invertível; inversão via estrutura (swap + subkeys inversos).

## §37 — Ex. 37
**f deve ser permutação** (bijecção) sobre {0,1}⁸ — cada input mapeia para output único.

## §38 — Ex. 38
**Não** — 2¹²⁸ entradas impossível armazenar.

## §39 — Ex. 39
AES-256-ECB, 16 bytes `0x41`×16 (32 hex 'A' = 16 bytes):
```
7e0e7577ef9c30a6bf0b25e0621e827e
```
Script: `scripts/aes_exercicios.py`

## §40 — Ex. 40
128 bytes 'A' ECB — cada bloco 16 bytes idêntico → **mesmo ciphertext** repetido:
```
7e0e7577ef9c30a6bf0b25e0621e827e (×8 blocos)
```

## §41 — Ex. 41
CBC, IV = 16 bytes 0x88, 128 bytes 'A':
Primeiro bloco ciphertext:
```
3b898b73e2c8f937d6dd19c138217ba9
```

## §42 — Ex. 42
Password tem **entropia baixa** e tamanho variável. AES precisa chave **128/192/256 bits** fixa. Usar **KDF** (PBKDF2, Argon2, scrypt) para derivar chave.

## §43 — Ex. 43
Bloco 8 bits → tabela 2⁸×2⁸ = **65536 entradas** por bloco — codebook attack trivial (128 KB).

## §44 — Ex. 44
1000 bits = 7 blocos completos + 8 bits restantes → **padding** (PKCS#7) + CBC/CTR encadear blocos.

## §45 — Ex. 45
Blocos iguais → ciphertext igual; vaza padrões; manipulação blocos; sem IV.

## §46 — Ex. 46
**SPN** (AES): substituição + permutação cada round. **Feistel** (DES): metade processada por F, swap.

## §47 — Ex. 47
Double encryption E_k2(E_k1(P)): calcular e armazenar E_k1(P) para todo k1; calcular D_k2(C) para todo k2; procurar colisão — **2⁵⁶+2⁵⁶** em vez de 2¹¹².

## §48 — Ex. 48
Servidor revela **padding válido/inválido** (tempo ou erro). Atacante modifica ciphertext byte a byte até padding OK → decifra bloco a bloco.

## §49 — Ex. 49
**Encrypt-then-MAC**, **AES-GCM**, validar padding em tempo constante, não revelar erros distintos, usar **authenticated encryption**.

## §50 — Ex. 50
| | Block | Stream |
|---|-------|--------|
| Unidade | Bloco fixo | Bit/byte stream |
| Erro | Propaga bloco | Propaga bit |
| Vantagem stream | Baixa latência, telecom histórico |
| Menos popular | Modos block (CTR), RC4/A5 quebrados, block mais versátil (MAC, hash) |
