# Módulo 05 — Funções de Dispersão (Hash)

**UC:** Criptografia Moderna · **Fase:** 2 — Cifras simétricas e assimétricas

## Objetivos de aprendizagem

- Compreender propriedades de funções hash criptográficas
- Distinguir hash, HMAC e funções de password
- Conhecer SHA-256 e família SHA-2/SHA-3
- Aplicar bcrypt, scrypt e Argon2 para armazenamento de passwords

---

## 1. Funções hash criptográficas

Mapeiam entrada de tamanho arbitrário para **digest fixo**:

```
H: {0,1}* → {0,1}^n     (ex.: n = 256 para SHA-256)
```

### Propriedades exigidas

| Propriedade | Definição |
|-------------|-----------|
| **Resistência à pré-imagem** | Dado \( h \), inviável encontrar \( m \) tal que \( H(m) = h \) |
| **Resistência à segunda pré-imagem** | Dado \( m \), inviável encontrar \( m' \neq m \) com \( H(m) = H(m') \) |
| **Resistência a colisões** | Inviável encontrar quaisquer \( m, m' \) com \( H(m) = H(m') \) |

### Aplicações

- Integridade de ficheiros (checksums)
- Assinaturas digitais (hash-then-sign)
- Merkle trees (blockchain, certificados)
- Derivação de chaves (HKDF)
- Armazenamento de passwords (com funções dedicadas)

---

## 2. SHA-256 e família SHA

### SHA-2 (NIST)

| Algoritmo | Digest | Estado |
|-----------|--------|--------|
| SHA-256 | 256 bits | ✅ Padrão |
| SHA-384 | 384 bits | ✅ |
| SHA-512 | 512 bits | ✅ |

**Construção:** Merkle-Damgård (SHA-256) — blocos de 512 bits, 64 rondas.

### SHA-3 (Keccak, 2015)

- Construção **sponge** (diferente de SHA-2)
- Alternativa se SHA-2 for comprometido
- Variantes: SHA3-256, SHAKE128/256 (XOF — extensible output)

### Algoritmos obsoletos — ❌ Nunca usar

| Algoritmo | Problema |
|-----------|----------|
| MD5 | Colisões práticas (2004) |
| SHA-1 | Colisões práticas (SHAttered, 2017) |

---

## 3. HMAC — Hash-based Message Authentication Code

Combina hash com chave secreta para **autenticidade + integridade**:

```
HMAC(K, M) = H( (K' ⊕ opad) || H( (K' ⊕ ipad) || M ) )
```

### Características

- Requer chave secreta partilhada
- Seguro mesmo se H tiver vulnerabilidades menores (desde que resistente a colisões)
- Usado em: TLS (legacy), API authentication, JWT (HS256)

### HMAC vs. hash simples

| | Hash (SHA-256) | HMAC-SHA256 |
|--|----------------|-------------|
| Chave | Não | Sim |
| Autenticidade | Não | Sim |
| Uso | Integridade (canal confiável) | Integridade + autenticação |

---

## 4. Password hashing

Passwords têm **baixa entropia** — hash rápido (SHA-256) permite milhões de tentativas/segundo.

### Requisitos de password hashing

1. **Lento** (ou memory-hard) — aumenta custo do atacante
2. **Salt único** por password — impede rainbow tables
3. **Parâmetros ajustáveis** — adaptar a hardware futuro

### bcrypt

- Baseado em Blowfish
- **Cost factor** (work factor): \( 2^{cost} \) iterações
- Salt de 128 bits incluído no output
- Limite de 72 bytes na password
- Cost recomendado: **12–14** (2025)

```
$2b$12$<22-char salt><31-char hash>
```

### scrypt

- **Memory-hard:** requer \( O(n) \) memória além de CPU
- Parâmetros: N, r, p
- Resiste a ASICs/GPUs melhor que bcrypt

### Argon2 — ✅ Recomendado (PHC winner, 2015)

| Variante | Uso |
|----------|-----|
| **Argon2id** | Password hashing (híbrido, default) |
| Argon2i | Resistente a side-channels |
| Argon2d | Resistente a GPU (não side-channel) |

Parâmetros: memória (m), iterações (t), paralelismo (p).  
Exemplo: Argon2id, m=64MB, t=3, p=4.

### Comparação

| Função | CPU | Memória | Recomendação |
|--------|-----|---------|--------------|
| SHA-256 | Rápido | Baixa | ❌ Passwords |
| bcrypt | Lento | Baixa | ✅ Legacy OK |
| scrypt | Lento | Alta | ✅ |
| Argon2id | Lento | Alta | ✅ **Preferido** |

---

## 5. Derivação de chaves (KDF)

| KDF | Uso |
|-----|-----|
| **PBKDF2** | Derivar chave de password (NIST, FIPS) — 600k+ iterações SHA-256 |
| **HKDF** | Expandir segredo partilhado (TLS, Signal) |
| **Argon2** | Password → chave criptográfica |

---

## 6. Length extension attack

Em hashes Merkle-Damgård (SHA-256, MD5), conhecendo \( H(M) \), é possível calcular \( H(M \| \text{padding} \| M') \) **sem conhecer M**.

**Mitigação:** usar HMAC em vez de \( H(k \| m) \); preferir SHA-3 ou construções AEAD.

---

## Exercícios

### Exercício 1
Explique a diferença entre resistência à pré-imagem e resistência a colisões. Qual é mais forte?

### Exercício 2
Porque MD5 e SHA-1 não devem ser usados para assinaturas digitais?

### Exercício 3
Descreva o propósito do salt no armazenamento de passwords.

### Exercício 4
Compare bcrypt e Argon2id. Porque Argon2id é preferido em novos sistemas?

### Exercício 5
Um developer armazena passwords como `SHA-256(password)`. Identifique três problemas.

### Exercício 6
Qual a diferença entre HMAC-SHA256 e SHA-256(m || key)? Porque HMAC é preferível?

### Exercício 7
Um sistema usa bcrypt com cost=4. Está adequado para 2025? Justifique.

### Exercício 8
Explique o length extension attack e como HMAC o previne.

---

## Soluções

### Solução 1
- **Pré-imagem:** dado hash, encontrar *qualquer* input que o produza
- **Colisão:** encontrar *dois* inputs distintos com o mesmo hash
- Colisão é mais fácil (birthday attack: \( O(2^{n/2}) \) vs. \( O(2^n) \) para pré-imagem). Resistência a colisões implica segunda pré-imagem, mas não necessariamente pré-imagem completa.

### Solução 2
Colisões práticas permitem construir dois documentos com a mesma assinatura (ataque ao hash, não à chave privada). SHAttered (2017) demonstrou colisão SHA-1; MD5 colisões desde 2004.

### Solução 3
Salt garante que passwords iguais produzem hashes diferentes; impede **rainbow tables** (tabelas pré-computadas); força atacante a atacar cada password individualmente.

### Solução 4
- **bcrypt:** CPU-bound, limite 72 bytes, sem parâmetro de memória
- **Argon2id:** memory-hard (resiste GPU/ASIC), híbrido side-channel/data-dependent, vencedor PHC, parâmetros flexíveis (memória, tempo, paralelismo)
- Argon2id preferido: mais robusto contra hardware especializado e side channels

### Solução 5
1. SHA-256 é **rápido** → brute-force viável (milhões/seg)
2. Sem **salt** → rainbow tables
3. Sem **work factor** → custo de ataque constante e baixo
4. Mesma password → mesmo hash (vazamento de igualdade)

### Solução 6
HMAC usa construção aninhada com pads (ipad/opad) provavelmente segura. \( H(m \| key) \) é vulnerável a **length extension** em Merkle-Damgård. HMAC é standard (RFC 2104, FIPS 198-1).

### Solução 7
**Não.** Cost=4 → \( 2^4 = 16 \) iterações — trivialmente rápido em GPU moderna. Recomendado cost **12–14** (bcrypt), calibrando para ~250–500 ms por hash no servidor.

### Solução 8
Merkle-Damgård: estado interno após \( H(M) \) permite continuar hashing sem M. HMAC encapsula o hash em construção com chave secreta desconhecida do atacante, impossibilitando estender a mensagem autenticada.
