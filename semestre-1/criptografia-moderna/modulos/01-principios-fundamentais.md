# Módulo 01 — Princípios Fundamentais

**UC:** Criptografia Moderna · **Fase:** 1 — Fundamentos

## Objetivos de aprendizagem

- Compreender os objetivos de segurança da tríade CIA e conceitos relacionados
- Aplicar o princípio de Kerckhoffs na análise de sistemas criptográficos
- Distinguir segurança teórica (secrecy perfeita) de segurança prática
- Identificar os componentes básicos de um sistema criptográfico

---

## 1. A tríade CIA

A segurança da informação assenta tradicionalmente em três pilares:

| Pilar | Definição | Exemplo criptográfico |
|-------|-----------|----------------------|
| **Confidencialidade** | Impedir acesso não autorizado à informação | Cifragem AES de um ficheiro |
| **Integridade** | Garantir que os dados não foram alterados | HMAC ou assinatura digital |
| **Disponibilidade** | Garantir acesso aos serviços quando necessário | Redundância, mitigação de DoS |

Além da tríade, em contextos modernos acrescentam-se frequentemente:

- **Autenticidade** — confirmar a identidade de quem comunica (certificados, MACs)
- **Não-repúdio** — impossibilidade de negar uma ação (assinaturas digitais)

> **Nota:** A criptografia resolve sobretudo confidencialidade, integridade e autenticidade. A disponibilidade depende mais de engenharia de sistemas e redes.

---

## 2. Princípio de Kerckhoffs (1883)

> *A segurança de um sistema criptográfico não deve depender do segredo do algoritmo, mas apenas do segredo da chave.*

**Implicações práticas:**

1. Algoritmos devem ser **públicos e analisados** pela comunidade (AES, SHA-256, RSA)
2. Chaves devem ser **geradas aleatoriamente** e **protegidas**
3. Algoritmos proprietários ("security by obscurity") são desaconselhados
4. Permite interoperabilidade e auditoria independente

**Exceção histórica:** Enigma dependia parcialmente do segredo do mecanismo, mas mesmo assim foi quebrado.

---

## 3. Componentes de um sistema criptográfico

```
Mensagem (plaintext) → [Algoritmo + Chave] → Texto cifrado (ciphertext)
Texto cifrado → [Algoritmo + Chave] → Mensagem (plaintext)
```

| Termo | Significado |
|-------|-------------|
| **Plaintext (M)** | Mensagem original |
| **Ciphertext (C)** | Mensagem cifrada |
| **Chave (K)** | Segredo que parametriza o algoritmo |
| **Espaço de chaves** | Conjunto de todas as chaves possíveis |
| **Criptanalista** | Adversário que tenta quebrar o sistema |

---

## 4. Secrecy perfeita (Perfect Secrecy)

Definição de **Shannon (1949):** Um esquema de cifragem tem secrecy perfeita se, observando o ciphertext, o adversário não obtém **nenhuma informação** sobre o plaintext.

Formalmente, para todo o par de mensagens \( m_0, m_1 \) e todo o ciphertext \( c \):

\[
P(M = m_0 \mid C = c) = P(M = m_0)
\]

### One-Time Pad (OTP)

- Chave aleatória \( K \) com o **mesmo tamanho** da mensagem
- Cifragem: \( C = M \oplus K \) (XOR bit a bit)
- **Teorema:** OTP tem secrecy perfeita se a chave for verdadeiramente aleatória, usada **uma única vez** e mantida em segredo

**Limitações do OTP:**

- Distribuição de chaves do tamanho da mensagem (impraticável em larga escala)
- Geração de aleatoriedade verdadeira
- Sem autenticidade (atacante pode alterar bits no ciphertext)

---

## 5. Segurança computacional vs. informação-teórica

| Tipo | Definição | Exemplo |
|------|-----------|---------|
| **Informação-teórica** | Impossível quebrar mesmo com recursos infinitos | OTP |
| **Computacional** | Inviável quebrar com recursos realistas | AES-256, RSA-2048 |

Na prática, todos os sistemas em uso (TLS, Signal, PGP) baseiam-se em **segurança computacional**.

---

## 6. Modelos de atacante

| Modelo | Capacidades |
|--------|-------------|
| **Ciphertext-only** | Apenas observa ciphertexts |
| **Known-plaintext** | Conhece pares (M, C) |
| **Chosen-plaintext** | Escolhe mensagens e obtém ciphertexts |
| **Chosen-ciphertext** | Escolhe ciphertexts e obtém plaintexts |

Quanto mais poderoso o modelo, mais robusto o esquema deve ser.

---

## Exercícios

### Exercício 1
Enumere os três pilares da tríade CIA e indique um mecanismo criptográfico que suporte cada um.

### Exercício 2
Um empresa desenvolve um algoritmo de cifragem proprietário e afirma que é seguro porque o código fonte é secreto. Explique porque esta abordagem viola Kerckhoffs.

### Exercício 3
No One-Time Pad, a chave tem 1000 bits e a mensagem tem 800 bits. O que se deve fazer com os 200 bits restantes da chave? Justifique.

### Exercício 4
Um ciphertext foi obtido com OTP. O adversário sabe que a mensagem é "SIM" ou "NAO" (3 letras). Porque o OTP deixa de garantir secrecy perfeita neste cenário?

### Exercício 5
Classifique cada situação como violação de confidencialidade, integridade ou disponibilidade:
a) Um atacante altera o valor de uma transferência bancária em trânsito.
b) Um ransomware encripta todos os ficheiros de um servidor.
c) Um atacante envia tráfego massivo para derrubar um site.

### Exercício 6
Qual a diferença entre segurança informação-teórica e segurança computacional? Dê um exemplo de cada.

### Exercício 7
Num ataque chosen-plaintext, o adversário submete a mensagem "AAAA" e recebe o ciphertext. Que tipo de informação pode extrair se o algoritmo for uma cifra de substituição monoalfabética?

---

## Soluções

### Solução 1
- **Confidencialidade:** cifragem simétrica (AES) ou assimétrica (RSA)
- **Integridade:** função hash (SHA-256) ou HMAC
- **Disponibilidade:** não é tipicamente garantida por criptografia; usa-se redundância, load balancing, mitigação de DoS

### Solução 2
Viola Kerckhoffs porque a segurança depende do segredo do algoritmo. Se o algoritmo for descoberto (engenharia inversa, fuga de código), todo o sistema colapsa. Algoritmos públicos permitem auditoria independente; apenas a chave deve ser secreta.

### Solução 3
Os 200 bits restantes **devem ser descartados** e nunca reutilizados. Reutilizar parte da chave de OTP permite ao adversário calcular \( C_1 \oplus C_2 = M_1 \oplus M_2 \), eliminando a proteção da chave e quebrando a secrecy perfeita.

### Solução 4
O espaço de mensagens é **muito pequeno** (apenas 2 opções). O adversário pode cifrar "SIM" e "NAO" com todas as chaves possíveis (ou usar propriedades do XOR) e comparar com o ciphertext observado, identificando a mensagem. Secrecy perfeita exige que todas as mensagens do mesmo tamanho sejam igualmente prováveis dado o ciphertext.

### Solução 5
- a) **Integridade** (e possivelmente confidencialidade se o canal não for cifrado)
- b) **Disponibilidade** e **confidencialidade** (ficheiros inacessíveis)
- c) **Disponibilidade**

### Solução 6
- **Informação-teórica:** quebrar é impossível mesmo com poder computacional infinito (OTP com chave aleatória única)
- **Computacional:** quebrar é inviável em tempo razoável (AES-256 — \(2^{256}\) operações)

### Solução 7
Com "AAAA", a cifra monoalfabética mapeia cada 'A' para a mesma letra cifrada (ex.: "QQQQ"). O adversário identifica a substituição de 'A' e pode aplicar análise de frequência ao resto do ciphertext para recuperar a mensagem.
