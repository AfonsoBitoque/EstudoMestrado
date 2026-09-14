# Módulo 06 — Limitações, Ameaças e Criptografia Quântica

**UC:** Criptografia Moderna · **Fase:** 3 — Aplicações e ameaças

## Objetivos de aprendizagem

- Identificar limitações práticas da criptografia clássica
- Compreender ataques por side-channel e timing
- Analisar ameaças de computadores quânticos (Shor, Grover)
- Conhecer o panorama de criptografia pós-quântica (PQC)

---

## 1. Limitações da criptografia

A criptografia **não resolve tudo**:

| Problema | Fora do âmbito criptográfico |
|----------|------------------------------|
| Disponibilidade | DoS, redundância |
| Segurança do endpoint | Malware, keyloggers |
| Engenharia social | Phishing |
| Implementação incorrecta | Bugs, configuração |
| Gestão de chaves | Políticas, revogação |

> **Princípio:** "Criptografia é a parte mais forte; o sistema é tão forte quanto o elo mais fraco."

---

## 2. Side-channel attacks

Exploram **informação física** da implementação, não fraquezas matemáticas.

### Tipos

| Canal | Informação vazada | Exemplo |
|-------|-------------------|---------|
| **Timing** | Tempo de execução | RSA square-and-multiply |
| **Power analysis (DPA/SPA)** | Consumo eléctrico | Extração de chave AES |
| **Electromagnetic (EMA)** | Radiação EM | Sniffing a distância |
| **Cache timing** | Acessos à cache | Spectre, Meltdown |
| **Acoustic** | Som do CPU | GnuPG key recovery |
| **Fault injection** | Glitches (voltagem, laser) | Skip instruções |

### Mitigações

- **Constant-time** implementations (sem branches dependentes de segredos)
- **Masking/blinding** em hardware
- **HSMs** e enclaves (TEE, SGX)
- **Padding** e randomização (RSA-OAEP)
- Minimizar superfície de ataque físico

---

## 3. Ataques clássicos relevantes

| Ataque | Alvo | Mitigação |
|--------|------|-----------|
| **Padding oracle** | CBC padding | AEAD, constant-time validation |
| **Bleichenbacher** | RSA PKCS#1 v1.5 | OAEP, não reportar erros distintos |
| **BEAST/CRIME/BREACH** | TLS compression/CBC | TLS 1.3, sem compressão |
| **Downgrade** | Versões TLS fracas | TLS 1.3, no fallback |
| **Replay** | Reenvio de mensagens | Nonces, timestamps, sequence numbers |

---

## 4. Ameaça quântica

### Algoritmo de Shor (1994)

Factoriza inteiros e calcula logaritmos discretos em **tempo polinomial** num computador quântico.

**Impacto:** Quebra **RSA**, **ECC**, **Diffie-Hellman** — toda a PKI actual.

### Algoritmo de Grover (1996)

Acelera busca em \( O(\sqrt{N}) \) — reduz segurança simétrica a metade:

| Algoritmo | Segurança clássica | Pós-Grover |
|-----------|-------------------|------------|
| AES-128 | 128 bits | ~64 bits ❌ |
| AES-256 | 256 bits | ~128 bits ✅ |
| SHA-256 | 256 bits | ~128 bits (colisões: ~85 bits) |

### Timeline estimado

- Computadores quânticos capazes de quebrar RSA-2048: estimativa **2030–2040+** (incerto)
- **Harvest now, decrypt later:** adversários recolhem ciphertext hoje para decifrar no futuro

---

## 5. Criptografia pós-quântica (PQC)

Algoritmos resistentes a ataques clássicos **e** quânticos.

### Famílias (NIST PQC, 2024)

| Família | Algoritmo selecionado | Base matemática | Uso |
|---------|----------------------|-----------------|-----|
| **Lattice (RE)** | **ML-KEM (Kyber)** | Module-LWE | Troca de chaves |
| **Lattice (DS)** | **ML-DSA (Dilithium)** | Module-LWE | Assinaturas |
| **Hash-based** | **SLH-DSA (SPHINCS+)** | Hash trees | Assinaturas (backup) |
| **Code-based** | BIKE, HQC (4.ª ronda) | Decoding | KEM (alternativa) |

### Migração

```
Fase 1: Inventário de sistemas criptográficos
Fase 2: Priorizar dados de longa duração
Fase 3: Híbrido clássico + PQC (ex.: X25519 + Kyber)
Fase 4: Deprecar RSA/ECC quando PQC maduro
```

**TLS híbrido (2024+):** X25519Kyber768 em Chrome, Cloudflare.

---

## 6. QKD — Quantum Key Distribution

Usa propriedades quânticas (incerteza, no-cloning) para distribuir chaves.

- **BB84:** protocolo fundamental
- Detecta escuta (perturbação quântica)
- **Limitação:** requer fibra dedicada; não substitui PQC em Internet

---

## 7. Recomendações práticas (2025)

1. Migrar para **AES-256**, **SHA-384/512**, **Ed25519/X25519**
2. Descontinuar RSA < 2048, SHA-1, MD5, 3DES
3. Planear inventário **crypto-agility**
4. Monitorizar standardização NIST PQC
5. Implementações **constant-time** e auditadas
6. TLS 1.3 everywhere

---

## Exercícios

### Exercício 1
Diferencie um ataque criptanalítico de um ataque por side-channel. Dê um exemplo de cada.

### Exercício 2
Porque AES-128 pode ser insuficiente num cenário pós-quântico, mas AES-256 permanece adequado?

### Exercício 3
Explique o ataque "harvest now, decrypt later" e que tipos de dados estão mais em risco.

### Exercício 4
Que algoritmos da infraestrutura actual (TLS, certificados) são vulneráveis ao algoritmo de Shor?

### Exercício 5
Descreva três mitigações contra timing attacks em implementações criptográficas.

### Exercício 6
Compare ML-KEM (Kyber) e QKD (BB84) como soluções para distribuição de chaves quântica-resistente.

### Exercício 7
Um sistema TLS usa RSA-1024 e AES-128-CBC. Identifique quatro problemas de segurança.

### Exercício 8
O que é "crypto-agility" e porque é importante na migração PQC?

---

## Soluções

### Solução 1
- **Criptanalítico:** explora fraqueza matemática (ex.: colisão MD5, factorização RSA)
- **Side-channel:** explora implementação física (ex.: DPA para extrair chave AES medindo consumo eléctrico durante cifragem)

### Solução 2
Grover reduz segurança simétrica a metade: AES-128 → ~64 bits (inseguro); AES-256 → ~128 bits (ainda seguro). Dobrar tamanho da chave compensa Grover.

### Solução 3
Adversário (ex.: estado-nation) armazena ciphertext interceptado hoje. Quando computadores quânticos quebrarem RSA/ECC, descifra retroactivamente. **Mais em risco:** segredos com valor de longo prazo (diplomáticos, médicos, propriedade intelectual, dados pessoais).

### Solução 4
Vulneráveis a Shor: **RSA** (cifragem, assinaturas), **ECDSA/EdDSA** (se baseado em ECDLP — na verdade Ed25519 também), **ECDH**, **DSA**, **Diffie-Hellman**. Não afectados: **AES**, **SHA-256** (com margem reduzida), **HMAC**.

### Solução 5
1. Implementações **constant-time** (sem branches/lookup tables dependentes de segredos)
2. **Blinding** em RSA (multiplicar por factor aleatório)
3. Usar **AEAD** em vez de CBC+padding
4. **HSM/TEE** para isolar operações sensíveis
5. Desactivar compressão em TLS

### Solução 6
- **ML-KEM (Kyber):** software, funciona sobre IP/Internet, baseado em retículos, híbrido com clássico, escalável
- **QKD (BB84):** requer canal quântico dedicado (fibra), distâncias limitadas, detecta escuta fisicamente, caro, complementar (não substituto universal)

### Solução 7
1. RSA-1024 — quebrável hoje (NIST proíbe desde 2013)
2. AES-128 — margem reduzida pós-Grover
3. CBC — vulnerável a padding oracle; sem autenticação
4. Sem AEAD — falta integridade/autenticidade
5. Possível versão TLS antiga

### Solução 8
Crypto-agility: capacidade de **substituir algoritmos** sem reescrever toda a aplicação (APIs abstractas, negociação de algoritmos, gestão de chaves flexível). Crucial para migração gradual RSA → PQC híbrido → PQC puro.
