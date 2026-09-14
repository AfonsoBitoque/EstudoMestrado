# Módulo 02 — Fundamentos de Comunicação Sem Fios

**UC:** Redes Sem Fios e de Sensores · **Fase:** 1 — Fundamentos

## Objetivos de aprendizagem

- Compreender modelos de propagação e path loss
- Calcular SNR e capacidade de canal
- Distinguir tipos de fading e mitigações
- Analisar espectro, bandas ISM e interferência

---

## 1. Espectro radio e bandas ISM

| Banda | Frequência | Uso típico |
|-------|------------|------------|
| Sub-GHz | 868 MHz (EU), 915 MHz (US) | LoRa, ZigBee, Sigfox |
| 2.4 GHz ISM | 2.400–2.483 GHz | Wi-Fi, BLE, ZigBee, Thread |
| 5 GHz | 5.150–5.850 GHz | Wi-Fi 5/6 |
| Celular | 700 MHz – 3.5 GHz | 4G/5G, NB-IoT |

**ISM:** bandas de uso livre (sujeitas a regulamentação de potência e duty cycle).

---

## 2. Modelos de path loss

Path loss quantifica a atenuação do sinal com a distância.

### Free Space Path Loss (FSPL)

\[
FSPL_{dB} = 20 \log_{10}(d) + 20 \log_{10}(f) + 20 \log_{10}\left(\frac{4\pi}{c}\right)
\]

Aproximação (distância em km, frequência em MHz):

\[
FSPL_{dB} \approx 32.44 + 20 \log_{10}(d_{km}) + 20 \log_{10}(f_{MHz})
\]

### Log-distance model

\[
PL(d) = PL(d_0) + 10 \cdot n \cdot \log_{10}\left(\frac{d}{d_0}\right)
\]

| Ambiente | Expoente \( n \) |
|----------|-----------------|
| Espaço livre | 2 |
| Urbano | 2.7 – 3.5 |
| Indoor | 2 – 4 |
| Obstruído (dense) | 4 – 6 |

### Modelos adicionais

- **Okumura-Hata:** celular, 150 MHz – 1.5 GHz
- **COST-231:** extensão Hata para 2 GHz
- **ITU-R P.1238:** indoor

---

## 3. SNR — Signal-to-Noise Ratio

\[
SNR_{dB} = P_{rx} - N_{floor}
\]

Onde:
- \( P_{rx} = P_{tx} - PL \) (potência recebida)
- \( N_{floor} \) = ruído térmico ≈ \(-174 \text{ dBm/Hz} + 10\log_{10}(BW)\)

**Exemplo:** BW = 1 MHz → \( N \approx -114 \text{ dBm} \)

| SNR | Qualidade |
|-----|-----------|
| > 20 dB | Excelente |
| 10–20 dB | Boa |
| 5–10 dB | Marginal |
| < 5 dB | Inaceitável (BER alto) |

---

## 4. Fading

Variação rápida da amplitude do sinal devido a multi-percurso.

### Tipos

| Tipo | Escala temporal | Causa |
|------|-----------------|-------|
| **Large-scale** | Distância, obstáculos | Path loss, shadowing |
| **Small-scale (fast)** | λ/2 (cm–m) | Multi-percurso construtivo/destrutivo |
| **Shadowing** | Metros | Obstáculos grandes (log-normal) |

### Efeito multi-percurso

Sinal directo + reflexões chegam com fases diferentes → construtiva ou destrutiva.

### Mitigações

| Técnica | Descrição |
|---------|-----------|
| **Diversidade** | Múltiplas antenas (MIMO) |
| **Frequency hopping** | BLE, alguns WPAN |
| **OFDM** | Wi-Fi, LTE — divide em subportadoras |
| **Equalização** | Compensar distorção de canal |
| **Coding (FEC)** | Corrigir erros de bit |
| **Interleaving** | Distribuir erros burst |

---

## 5. Capacidade de canal (Shannon)

\[
C = B \cdot \log_2\left(1 + \frac{S}{N}\right) \text{ bits/s}
\]

- \( B \) = bandwidth (Hz)
- \( S/N \) = razão sinal-ruído linear

**Implicação:** aumentar SNR ou bandwidth aumenta capacidade, mas com rendimentos decrescentes.

---

## 6. Link budget

```
P_rx = P_tx + G_tx + G_rx - PL - L_margins

Margens: fading (10-20 dB), interferência, cabos, polarização
```

Se \( P_{rx} > P_{sensitivity} \) → link viável.

---

## 7. Interferência

| Tipo | Descrição |
|------|-----------|
| **Co-channel** | Mesma frequência, redes diferentes |
| **Adjacent-channel** | Canais vizinhos |
| **Inter-tecnologia** | Wi-Fi vs. ZigBee (2.4 GHz) |

**CSMA/CA** (Wi-Fi, 802.15.4): escuta antes de transmitir; backoff se canal ocupado.

---

## Exercícios

### Exercício 1
Calcule FSPL a 100 m em 2.4 GHz (espaço livre). \( P_{tx} = 10 \text{ dBm} \), \( G_{tx} = G_{rx} = 0 \text{ dBi} \). Qual \( P_{rx} \)?

### Exercício 2
Com \( P_{rx} = -85 \text{ dBm} \) e BW = 250 kHz, calcule SNR (assuma ruído térmico).

### Exercício 3
Explique a diferença entre path loss (large-scale) e fading (small-scale).

### Exercício 4
Ambiente indoor com expoente \( n = 3 \). A 10 m, PL = 60 dB. Estime PL a 30 m (log-distance, \( d_0 = 10 \text{ m} \)).

### Exercício 5
Porque Wi-Fi e ZigBee interferem mutuamente apesar de usarem canais diferentes?

### Exercício 6
Calcule a capacidade de Shannon para B = 20 MHz, SNR = 15 dB (linear: 31.6).

### Exercício 7
Descreva três técnicas para combater fading multi-percurso.

### Exercício 8
Um link LoRa tem sensitivity = -137 dBm, \( P_{tx} = 14 \text{ dBm} \), margem fading = 15 dB. Qual o path loss máximo admissível?

---

## Soluções

### Solução 1
\( FSPL = 32.44 + 20\log(0.1) + 20\log(2400) = 32.44 - 20 + 67.6 = 80.0 \text{ dB} \)  
\( P_{rx} = 10 - 80 = \mathbf{-70 \text{ dBm}} \)

### Solução 2
\( N = -174 + 10\log(250000) = -174 + 54 = -120 \text{ dBm} \)  
\( SNR = -85 - (-120) = \mathbf{35 \text{ dB}} \)

### Solução 3
- **Path loss:** atenuação média com distância/obstáculos (large-scale, previsível)
- **Fading:** variação rápida da amplitude por multi-percurso (small-scale, posição-dependent)

### Solução 4
\( PL(30) = 60 + 10 \times 3 \times \log_{10}(30/10) = 60 + 30 \times 0.477 = 60 + 14.3 = \mathbf{74.3 \text{ dB}} \)

### Solução 5
Ambos operam em 2.4 GHz ISM. Canais ZigBee (2 MHz) sobrepõem-se parcialmente a canais Wi-Fi (20 MHz). Spectral overlap causa interferência co-canal e adjacente mesmo com numeração de canais diferente.

### Solução 6
\( C = 20 \times 10^6 \times \log_2(1 + 31.6) = 20 \times 10^6 \times 5.02 \approx \mathbf{100 \text{ Mbit/s}} \)

### Solução 7
1. **OFDM** — divide sinal em subportadoras resistentes a selective fading
2. **Diversidade** (MIMO, antenna switching) — múltiplos caminhos independentes
3. **Frequency hopping** — evita frequências em fade profundo

### Solução 8
\( PL_{max} = P_{tx} - P_{sensitivity} - \text{margin} = 14 - (-137) - 15 = 14 + 137 - 15 = \mathbf{136 \text{ dB}} \)
