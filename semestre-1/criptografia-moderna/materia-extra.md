# Matéria Extra — Criptografia Moderna

Conteúdo complementar para aprofundamento além do programa base.

---

## 1. Provas de conhecimento zero (Zero-Knowledge Proofs)

### Conceito

Um provador convence um verificador de que uma afirmação é verdadeira **sem revelar nenhuma informação** além da validade da afirmação.

```
Propriedades:
  - Completude: afirmação verdadeira → verificador aceita
  - Solidez: afirmação falsa → verificador rejeita (com alta probabilidade)
  - Zero-knowledge: verificador não aprende nada além da validade
```

### Exemplo clássico: caveira de Ali Baba

Alice prova que conhece a palavra secreta da caveira sem a revelar, repetindo um protocolo de desafio-resposta.

### zk-SNARKs e zk-STARKs

| Tipo | Características |
|------|-----------------|
| **zk-SNARK** | Provas curtas, verificação rápida; setup confiável (cerimónia); usado em Zcash, blockchains |
| **zk-STARK** | Sem setup confiável; provas maiores; resistente a quantum |

### Aplicações

- Privacidade em blockchain (Zcash, rollups Ethereum)
- Autenticação sem revelar credenciais
- Verificação de computação off-chain
- Compliance (provar elegibilidade sem revelar dados)

---

## 2. Criptografia homomórfica (introdução)

### Conceito

Permite **operar sobre dados cifrados** sem decifrar:

```
E(m₁) ⊕ E(m₂) = E(m₁ + m₂)     (homomorfismo aditivo)
E(m₁) ⊗ E(m₂) = E(m₁ × m₂)     (homomorfismo multiplicativo)
```

### Tipos

| Tipo | Operações | Exemplo |
|------|-----------|---------|
| **Parcial (PHE)** | Só adição OU só multiplicação | Paillier, RSA (mult.) |
| **Somewhat (SHE)** | N operações limitadas | BGV (limitado) |
| **Fully (FHE)** | Adição + multiplicação ilimitadas | CKKS, BFV, TFHE |

### Aplicações

- Computação em cloud sem expor dados (votação, ML privado)
- Análise de dados médicos/financeiros encriptados
- Filtragem de spam encriptada

### Limitações actuais

- Performance: FHE é **1000–10⁶× mais lento** que computação clara
- Tamanho de ciphertext expandido
- Em maturação para produção (2025: casos de uso específicos)

---

## 3. Protocolo Signal

Protocolo de mensagens end-to-end (E2EE) usado por Signal, WhatsApp e Messenger (opt-in).

### Componentes

| Componente | Função |
|------------|--------|
| **X3DH** | Extended Triple Diffie-Hellman — estabelecimento inicial de sessão |
| **Double Ratchet** | Actualização contínua de chaves (forward secrecy + break-in recovery) |
| **Sesame** | Gestão de sessões multi-dispositivo |

### X3DH (simplificado)

```
Alice (offline)                    Bob (online)
  Identity Key (IK_A)               Identity Key (IK_B)
  Signed Prekey (SPK_A)             Signed Prekey (SPK_B)
  One-time Prekeys (OPK)            One-time Prekeys (OPK)

Alice obtém bundle de Bob do servidor
Calcula 4 DH shared secrets → combina com KDF → root key + chain keys
```

### Double Ratchet

```
Cada mensagem:
  1. DH ratchet: novo par ephemeral → nova root key
  2. Symmetric ratchet: chain key → message key (one-time)
  3. Cifragem: AES-256 / ChaCha20 + HMAC/Poly1305
```

**Propriedades:**

- **Forward secrecy:** chaves passadas não comprometem futuro
- **Break-in recovery:** após compromisso temporário, sessão recupera-se
- **Deniability:** assinaturas não transferíveis (MACs simétricos)

### Comparação com TLS

| | TLS | Signal |
|--|-----|--------|
| Modelo | Cliente-servidor | Peer-to-peer |
| E2EE | Não (servidor vê plaintext) | Sim |
| Forward secrecy | Sim (TLS 1.3) | Sim (por mensagem) |
| Metadata | Visível ao servidor | Minimizada (Sealed Sender) |

---

## Exercícios complementares

### Exercício 1
Explique porque uma prova zero-knowledge de "conheço a password" é preferível a enviar a password hashada.

### Exercício 2
Num esquema homomórfico aditivo, o servidor calcula a soma de salários cifrados. Que informação o servidor **não** consegue obter?

### Exercício 3
Descreva o papel do Double Ratchet na forward secrecy do Signal.

### Exercício 4
Compare zk-SNARKs e zk-STARKs quanto ao setup e resistência quântica.

---

## Soluções

### Solução 1
Enviar hash permite ataque offline (rainbow tables, brute-force). ZK proof demonstra conhecimento sem revelar hash ou password — verificador aceita sem obter material reutilizável.

### Solução 2
Não obtém salários individuais — apenas o resultado cifrado da soma. Sem chave privada, não decifra nem valores parciais nem totais (dependendo do esquema e se tem a chave).

### Solução 3
Cada mensagem deriva nova message key de chain key actualizada; DH ratchet periodicamente renova root key com novo ECDH ephemeral. Compromisso de chave actual não expõe mensagens anteriores (forward secrecy) nem futuras após novo ratchet (break-in recovery).

### Solução 4
- **zk-SNARK:** requer setup confiável (cerimónia MPC); provas pequenas; curvas elípticas → vulnerável a Shor
- **zk-STARK:** sem trusted setup; provas maiores; baseado em hash → mais resistente a quantum
