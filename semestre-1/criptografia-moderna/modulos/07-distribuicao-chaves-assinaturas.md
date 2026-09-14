# Módulo 07 — Distribuição de Chaves, Assinaturas e TLS

**UC:** Criptografia Moderna · **Fase:** 3 — Aplicações e ameaças

## Objetivos de aprendizagem

- Compreender PKI e certificados X.509
- Explicar assinaturas digitais e o seu processo
- Analisar o handshake TLS 1.3
- Aplicar conceitos a cenários reais (HTTPS, email, código)

---

## 1. O problema da confiança

Num sistema de chave pública, como verificar que uma chave pública pertence realmente a quem diz ser?

**Solução:** Infraestrutura de Chave Pública (**PKI**)

```
Entidade → CSR → CA (Certificate Authority) → Certificado X.509
Utilizador → verifica cadeia → confia na chave pública
```

---

## 2. Certificados X.509

Estrutura de um certificado:

| Campo | Conteúdo |
|-------|----------|
| **Version** | v3 |
| **Serial Number** | Identificador único |
| **Subject** | CN=example.com, O=Org, C=PT |
| **Issuer** | CA que assinou |
| **Validity** | Not Before / Not After |
| **Subject Public Key Info** | Algoritmo + chave pública |
| **Extensions** | SAN, Key Usage, Basic Constraints |
| **Signature** | Assinatura da CA sobre o certificado |

### Cadeia de confiança

```
Root CA (auto-assinado, no trust store)
    └── Intermediate CA
            └── Certificado servidor (leaf)
```

Browsers/OS incluem **trust stores** com Root CAs confiáveis (Mozilla, Microsoft, Apple).

### Validação

1. Verificar assinatura de cada certificado na cadeia
2. Verificar validade temporal
3. Verificar revogação (CRL ou OCSP)
4. Verificar hostname (CN/SAN match)
5. Verificar Key Usage / Extended Key Usage

---

## 3. Assinaturas digitais

Garantem **autenticidade**, **integridade** e **não-repúdio**.

### Processo

```
Assinatura:
  1. h = Hash(M)
  2. S = Sign(K_priv, h)     // RSA-PSS, ECDSA, Ed25519

Verificação:
  1. h' = Hash(M)
  2. Verify(K_pub, S, h') → true/false
```

### Propriedades

- Alterar **1 bit** de M invalida a assinatura
- Apenas detentor de \( K_{priv} \) pode assinar
- Qualquer um com \( K_{pub} \) pode verificar

### Aplicações

| Aplicação | Esquema |
|-----------|---------|
| TLS/HTTPS | Certificado do servidor |
| Email | S/MIME, PGP |
| Código | Authenticode, codesign (macOS, Android) |
| Documentos | PDF signing, DocuSign |
| Blockchain | ECDSA/secp256k1 (Bitcoin) |

---

## 4. TLS 1.3 — visão geral

Protocolo que protege comunicações na Internet (HTTPS).

### Objetivos

- **Confidencialidade** — cifragem simétrica
- **Integridade** — AEAD
- **Autenticidade** — certificado do servidor (e opcionalmente cliente)

### Handshake simplificado (1-RTT)

```
Cliente                                    Servidor
  │ ClientHello                             │
  │  + key_share (X25519 pub)               │
  │  + supported_groups                     │
  │  + cipher_suites                        │
  ├────────────────────────────────────────→│
  │                                         │ ServerHello
  │←────────────────────────────────────────┤  + key_share (X25519 pub)
  │                                         │  + certificate
  │                                         │  + certificate_verify
  │                                         │  + finished
  │  [Derivação: shared_secret = ECDH]      │
  │  [HKDF → handshake keys + app keys]     │
  │                                         │
  │ Finished                                │
  ├────────────────────────────────────────→│
  │                                         │
  │══════ Dados cifrados (AES-GCM) ═════════│
```

### Melhorias vs. TLS 1.2

- Handshake mais rápido (1-RTT, 0-RTT resumption)
- Apenas cipher suites seguros (sem RSA key transport, sem CBC, sem 3DES)
- **Forward secrecy** obrigatório (ephemeral DH)
- Negociação de versão segura

### Cipher suites TLS 1.3

```
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_GCM_SHA256
```

---

## 5. Revogação de certificados

| Mecanismo | Descrição | Limitação |
|-----------|-----------|-----------|
| **CRL** | Lista de certificados revogados | Tamanho, latência |
| **OCSP** | Consulta online por certificado | Privacidade, disponibilidade |
| **OCSP Stapling** | Servidor inclui resposta OCSP | Melhor performance |
| **CRLite** | Bloom filters compactos | Emergente |

---

## 6. PGP/GPG — web of trust

Alternativa descentralizada à PKI hierárquica:

- Utilizadores assinam chaves uns dos outros
- Rede de confiança (web of trust)
- Usado em email, ficheiros, git signing

---

## 7. Verificação prática

```bash
# Ver certificado de um site
openssl s_client -connect example.com:443 -brief

# Verificar assinatura de ficheiro (GPG)
gpg --verify documento.pdf.sig documento.pdf

# Inspecionar certificado
openssl x509 -in cert.pem -text -noout
```

---

## Exercícios

### Exercício 1
Descreva o papel de uma CA numa PKI. O que acontece se uma Root CA for comprometida?

### Exercício 2
Quais campos de um certificado X.509 são essenciais para validar que `https://banco.pt` é autêntico?

### Exercício 3
Explique porque TLS 1.3 exige forward secrecy e como ECDH ephemeral o garante.

### Exercício 4
Diferencie CRL e OCSP. Porque OCSP stapling melhora performance e privacidade?

### Exercício 5
Descreva o processo completo de assinatura e verificação de um documento PDF.

### Exercício 6
Um certificado tem SAN: `example.com, *.example.com`. O certificado é válido para `api.example.com`? E para `other.net`?

### Exercício 7
Liste três melhorias de TLS 1.3 sobre TLS 1.2 do ponto de vista criptográfico.

### Exercício 8
Compare PKI hierárquica (X.509) com web of trust (PGP). Quando preferir cada uma?

---

## Soluções

### Solução 1
CA emite certificados ligando identidade a chave pública, assinando com a sua chave privada. Se Root CA comprometida: atacante emite certificados falsos para qualquer domínio → browsers confiam → MITM global. Mitigação: revogar root, actualizar trust stores, Certificate Transparency.

### Solução 2
- **Subject/SAN:** deve conter `banco.pt` (match exacto ou wildcard)
- **Validity:** datas actuais dentro do intervalo
- **Signature:** verificável pela cadeia até Root CA confiável
- **Key Usage / EKU:** serverAuth
- **Revogação:** não revogado (OCSP/CRL)

### Solução 3
Forward secrecy: compromisso da chave privada do servidor **não** permite decifrar sessões passadas. ECDH ephemeral gera par de chaves temporário por sessão; chave simétrica derivada do segredo efémero é descartada — sem chave privada estática do servidor no key exchange.

### Solução 4
- **CRL:** lista completa descarregada periodicamente — grande, desactualizada
- **OCSP:** consulta em tempo real — expõe browsing a CA, latência
- **Stapling:** servidor anexa resposta OCSP pré-obtida no handshake — cliente não contacta CA, mais rápido, mais privado

### Solução 5
1. Calcular hash do PDF (SHA-256)
2. Assinar hash com chave privada do signatário (RSA-PSS/ECDSA)
3. Incorporar assinatura + certificado no PDF
4. Verificador: extrai certificado, verifica cadeia PKI, recalcula hash, verifica assinatura com chave pública

### Solução 6
- `api.example.com` → **Sim** (wildcard `*.example.com` cobre subdomínios de um nível)
- `other.net` → **Não** (domínio não incluído no SAN/CN)

### Solução 7
1. Apenas AEAD cipher suites (sem CBC, MAC-then-encrypt)
2. Forward secrecy obrigatório (sem RSA key transport)
3. Handshake encriptado mais cedo (Certificate encrypted)
4. Remoção de algoritmos fracos (3DES, RC4, MD5, SHA-1)
5. 0-RTT com cautela (replay protection)

### Solução 8
- **PKI (X.509):** centralizada, escalável, ideal para web/TLS, empresas — confiança delegada a CAs
- **PGP (web of trust):** descentralizada, ideal para email pessoal, comunidades técnicas, git signing — confiança distribuída entre pares
- Preferir PKI para serviços públicos; PGP para comunicação peer-to-peer sem CA central
