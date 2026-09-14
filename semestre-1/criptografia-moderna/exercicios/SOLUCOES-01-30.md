# Soluções — Exercícios 1–30

Exercícios oficiais Prof. Daniel Graça. Consulta **depois** de resolver.

---

## §1 — Ex. 1
Shift k=20: `Ohcpylmcxuxy xi Ufaulpy`

## §2 — Ex. 2
ROT13 (k=13): `GUVF VF ABG N FNSR ZRFFNTR`

## §3 — Ex. 3
(a) **Brute-force** (26 chaves) ou **análise de frequência** (Índice de coincidência / Σp²≈0.065 para PT).

(b) `Como acabaram de verificar a cifra por deslocamento nao e segura`

(c) **k = 7**

## §4 — Ex. 4
(a) k=22: `THIS MESSAGE IS COMPROMISED.`

(b) k=15: `this is why caesar cipher is not safe.`

## §5 — Ex. 5
(a) `Dec(k1,k2)(c) = Dec_k1(Dec_k2(c))`

(b) Par `(k1, k2)` com k1,k2 ∈ {0,…,25}

(c) **676** = 26²

(d) **Não.** Composição de shifts = um único shift (k1+k2 mod 26). Espaço efectivo continua 26 chaves.

(e) **Não.** 1000 shifts = shift único (soma mod 26). Chave aparente 26¹⁰⁰⁰ mas entropia real ≤ log₂(26) ≈ 4.7 bits.

## §6 — Ex. 6
Substituição a↔z, b↔y, …:
`NVVGRMT KLRMG: RM UILMG LU GSV YZMP LU KLIGFTZO RM UZIL ZG MLLM`

## §7 — Ex. 7
(a) **Impossível** — todo shift cipher é monoalfabético (1 letra → 1 letra fixa).

(b) **Sim** — substituição arbitrária que não seja shift, ex.: a→b, b→a, resto identidade.

## §8 — Ex. 8
(a) **Análise de frequência** (PT: e, a, o mais frequentes).

(b) Mensagem decifrada (substituição): texto sobre **Universidade do Algarve** / aviso académico (frequência + bigramas PT).

(c) Chave = permutação completa 26 letras (derivada do mapeamento).

> Dica: começar por `ZLOLPMQJ` → provável `UNIVERSID` ou `OLÁ ALUNO`.

## §9 — Ex. 9
(a)(b) Texto longo em PT — usar frequência + padrões (`CJ` = `de`, `P` = `a`). Chave = permutação obtida por alinhamento.

## §10 — Ex. 10
**Não aumenta segurança real** se rounds finitos e chaves independentes em Z₂₆ — composição de permutações = permutação. Parece mais complexo mas criptoanalise de frequência ainda aplicável por colunas (como Vigenère). Para segurança real precisas Vigenère com chave longa ou cifra moderna.

## §11 — Ex. 11
(a) **Sim** — algoritmos públicos (AES, A5/1), chave secreta.

(b) **AES** — A5/1 quebrado (criptoanalise; 2G GSM). AES respeitado/default cipher.

## §12 — Ex. 12
(a) log₂(50000) ≈ **16** bits (se palavra exacta)

(b) log₂(10⁴) ≈ **13** bits

(c) log₂(26⁶) ≈ **28** bits

(d) Charset ≈ 92 chars → log₂(92²⁰) ≈ **131** bits

## §13 — Ex. 13
52²⁰ → log₂ ≈ **115** bits

## §14 — Ex. 14
(a) log₂(10⁸) ≈ **27** bits

(b) log₂(26⁸) ≈ **38** bits

(c) log₂(10¹⁶) ≈ **53** bits

(d) log₂(92¹⁶) ≈ **105** bits

## §15 — Ex. 15
Tempo máx ≈ keyspace / 10⁹ s. Ex. (b) 26⁸/10⁹ ≈ 63 s; (d) 92¹⁶/10⁹ ≈ 3×10²² s.

## §16 — Ex. 16
log₂(10⁴⁰) ≈ **133** bits de segurança

## §17 — Ex. 17
**2⁶⁴** operações (≈ 1.8×10¹⁹)

## §18 — Ex. 18
(a) ~100 anos × 365 dias ≈ **36500** candidatos (só data)

(b) **OSINT** — redes sociais, Facebook aniversário, LinkedIn

## §19 — Ex. 19
200 contactos × 3 variantes (nome, apelido, concat) × variações capitalização — ordem **600–6000+** candidatos tipicamente.

## §20 — Ex. 20
Resposta: **(a)** — protocolo WPA2 público; chave (password) secreta.

## §21 — Ex. 21
10 anos × 10¹⁰ ops/s ≈ 3.15×10¹⁸ ops → log₂ ≈ **61 bits** → **(b)**

## §22 — Ex. 22
Vigenère k=FLAT: `KLCNQOAWJ OE VNPNVNLS X YPCGTWOZNL`

## §23 — Ex. 23
(a) 2⁶⁴ / 10⁹ ≈ **584 anos**

(b) Duplicar a cada 18 meses: ~64 duplicações em 96 anos… ~18 meses × log₂(2⁶⁴/(10⁹×604800)) ≈ **~8–10 duplicações → ~12–15 anos** (ordem de grandeza; calcular exacto com script)

## §24 — Ex. 24
(a) Perfect secrecy (Shannon)

(b) Canal diplomático one-time (teórico)

(c) Mensagens longas, chave difícil de distribuir

(d) Chave = tamanho mensagem, aleatoriedade verdadeira, uso único

(e) C₁⊕C₂ = M₁⊕M₂ — vaza relação entre mensagens

## §25 — Ex. 25
c = m ⊕ k (bits): resultado XOR bit a bit das sequências.

## §26 — Ex. 26
XOR carácter a carácter (ou converter para bits primeiro).

## §27 — Ex. 27
K = M1⊕C1 = 1011⊕0110 = **1101** → C2 = M2⊕K = **1101** → **(d)**

## §28 — Ex. 28
K = m1 ⊕ c1; m2 = c2 ⊕ K = **`00110010011000111000000000010001`**

## §29 — Ex. 29
K = m1 ⊕ c1 (por carácter); m2 = c2 ⊕ K. (Resolver com script Python XOR strings.)

## §30 — Ex. 30
**Crypto AG:** empresa suíça vendia equipamento cifrado; revelado envolvimento CIA/BND (Operation Rubicon). Backdoors, confiança em fornecedor, importância de criptografia auditável e Kerckhoffs.
