# Módulo 05 — Celular e LPWAN

**UC:** Redes Sem Fios e de Sensores · **Fase:** 2 — Tecnologias

## Objetivos de aprendizagem

- Compreender IoT celular (4G/5G mMTC, NB-IoT, LTE-M)
- Analisar tecnologias LPWAN (LoRaWAN, Sigfox, NB-IoT)
- Comparar trade-offs para aplicações wide-area
- Seleccionar tecnologia por cenário de deployment

---

## 1. IoT celular — visão geral

Redes celulares tradicionais optimizadas para voz/dados móveis. Adaptações para IoT:

| Tecnologia | Standard | Banda | Taxa | Alcance |
|------------|----------|-------|------|---------|
| **NB-IoT** | 3GPP Rel. 13+ | Licenciada (LTE band) | 20–250 kbps | km (indoor excelente) |
| **LTE-M** (eMTC) | 3GPP Rel. 13+ | Licenciada | 100 kbps – 1 Mbps | km |
| **5G mMTC** | 3GPP Rel. 16+ | Licenciada | Variável | km |
| **4G LTE** | 3GPP | Licenciada | Mbit/s | km |

---

## 2. NB-IoT (Narrowband IoT)

### Características

- Bandwidth: 180 kHz (1 PRB LTE)
- Deploy: in-band, guard-band ou standalone
- **Coverage enhancement:** repetitions ( até +20 dB link budget)
- **PSM** (Power Saving Mode) e **eDRX** (extended DRX)
- Sem handover (mobilidade limitada)

### Vantagens

- Cobertura indoor/subterrânea superior
- Espectro licenciado (sem interferência ISM)
- Integração com infraestrutura operador existente
- Segurança SIM/eSIM

### Limitações

- Custo mensal (SIM, dados)
- Dependência de operador
- Latência: segundos (com PSM pode ser minutos)

---

## 3. LTE-M (LTE Cat-M1)

| Aspeto | NB-IoT | LTE-M |
|--------|--------|-------|
| Taxa | 20–250 kbps | 100 kbps – 1 Mbps |
| Latência | Alta | Moderada |
| Mobilidade | Limitada | Handover suportado |
| Voz (VoLTE) | Não | Sim |
| Power | Muito baixo | Baixo |
| Uso | Sensores estáticos | Trackers, wearables |

---

## 4. 5G para IoT

| Serviço | Foco | IoT |
|---------|------|-----|
| **eMBB** | Broadband | Câmaras 4K |
| **URLLC** | Ultra-baixa latência | Industrial, V2X |
| **mMTC** | Massive IoT | Milhões de dispositivos/km² |

5G mMTC evolui NB-IoT/LTE-M com:
- RedCap (Reduced Capability) — dispositivos mid-tier
- Posicionamento integrado
- Network slicing para SLAs diferenciados

---

## 5. LoRaWAN

### Arquitectura

```
End Device (sensor) ←→ Gateway ←→ Network Server ←→ Application Server
     (LoRa PHY)         (IP backhaul)    (gestão)         (dados)
```

### LoRa (PHY) vs. LoRaWAN (MAC/Network)

| Camada | Função |
|--------|--------|
| **LoRa** (Semtech) | Modulação CSS (Chirp Spread Spectrum) |
| **LoRaWAN** (LoRa Alliance) | MAC, routing, join, ADR |

### Classes de dispositivos

| Classe | RX windows | Uso |
|--------|------------|-----|
| **A** | Após TX (2 janelas) | Sensores (mínimo consumo) |
| **B** | + beacons programados | Actuadores com latência definida |
| **C** | RX contínuo (excepto TX) | Actuadores tempo-real |

### Parâmetros

- Banda EU: 868 MHz (duty cycle 1% por canal)
- Spreading Factor (SF7–SF12): trade-off alcance vs. taxa
- Adaptive Data Rate (ADR): rede optimiza SF/potência

### Segurança

- AES-128: NwkSKey (network), AppSKey (application)
- OTAA (Over-The-Air Activation) vs. ABP (Activation By Personalization)

---

## 6. Sigfox

| Aspeto | Sigfox |
|--------|--------|
| Topologia | Proprietária, operador único |
| Banda | Sub-GHz ISM (868/902 MHz) |
| Taxa | 100 bps (ultra-narrowband) |
| Payload | 12 bytes/uplink, 8 downlinks/dia |
| Alcance | 10–50 km (rural) |
| Dispositivos | Ultra-simples, muito baixo custo |

**Limitações:** downlink muito restrito, vendor lock-in, taxa mínima.

---

## 7. Tabela comparativa LPWAN

| Critério | LoRaWAN | Sigfox | NB-IoT | LTE-M |
|----------|---------|--------|--------|-------|
| Espectro | ISM (gratuito) | ISM | Licenciado | Licenciado |
| Taxa | 0.3–50 kbps | 0.1 kbps | 20–250 kbps | 100k–1M bps |
| Alcance | 2–15 km | 10–50 km | 1–10 km | 1–10 km |
| Custo rede | Privada/pública | Subscrição | SIM/mês | SIM/mês |
| Mobilidade | Não | Não | Limitada | Sim |
| Downlink | Moderado | Muito limitado | Sim | Sim |
| Deployment | DIY gateways | Operador | Operador | Operador |
| Privacidade | Rede privada possível | Cloud Sigfox | Operador | Operador |

---

## 8. Selecção por cenário

| Cenário | Tecnologia recomendada | Justificação |
|---------|----------------------|--------------|
| Smart metering urbano | NB-IoT | Cobertura indoor, operador |
| Agricultura remota (privado) | LoRaWAN | Rede privada, longo alcance |
| Rastreamento activos móveis | LTE-M | Handover, mobilidade |
| Botão de pânico ultra-simples | Sigfox | Custo mínimo, uplink esporádico |
| Industrial tempo-real | 5G URLLC | Latência < 10 ms |

---

## Exercícios

### Exercício 1
Compare NB-IoT e LoRaWAN para smart metering num edifício urbano.

### Exercício 2
Explique o trade-off Spreading Factor vs. taxa de dados em LoRa.

### Exercício 3
Descreva PSM e eDRX e o impacto na latência de NB-IoT.

### Exercício 4
Porque Sigfox limita downlinks a 8/dia?

### Exercício 5
Um tracker GPS precisa de mobilidade e 1 update/minuto. NB-IoT ou LTE-M?

### Exercício 6
Calcule duty cycle LoRa: SF10, payload 20 bytes, tempo ar ~400 ms, intervalo TX = 5 min.

### Exercício 7
Compare custos de deployment: rede LoRaWAN privada vs. NB-IoT via operador.

### Exercício 8
Descreva OTAA vs. ABP em LoRaWAN. Qual é mais seguro?

---

## Soluções

### Solução 1
- **NB-IoT:** cobertura indoor excelente (penetração edifícios), sem instalar gateways, billing integrado, espectro licenciado
- **LoRaWAN:** requer gateways no edifício, ISM pode interferir, mais controlo/privacidade, sem custo mensal por SIM
- Urbano com cobertura operador → **NB-IoT**; edifício isolado/privado → **LoRaWAN**

### Solução 2
SF maior (SF12) → chirp mais longo → mais processamento gain → **maior alcance**, **menor taxa** (bps). SF7: rápido, curto alcance; SF12: lento, longo alcance. ADR ajusta automaticamente.

### Solução 3
- **PSM:** dispositivo dorme profundamente entre transmissões; acorda periodicamente (timer) → latência downlink de minutos/horas
- **eDRX:** ciclos DRX alargados (até 40 min) → menor consumo que always-on, latência intermédia
- Trade-off: autonomia vs. responsividade a comandos downlink

### Solução 4
Sigfox optimiza para uplink-only IoT (sensores). Downlink ultra-limitado reduz consumo nos dispositivos (sem RX contínuo), simplifica rede, e maximiza capacidade uplink no ultra-narrowband.

### Solução 5
**LTE-M:** suporta handover entre células (mobilidade), taxa suficiente para GPS + 1 msg/min, latência aceitável. NB-IoT: sem handover confiável, latência alta com PSM.

### Solução 6
Duty cycle = 400 ms / 300000 ms = **0.13%** (bem abaixo do limite 1% EU 868 MHz)

### Solução 7
- **LoRaWAN privada:** CAPEX gateways + servidores; OPEX manutenção; sem fee/SIM; ideal >1000 nós área definida
- **NB-IoT:** OPEX SIM (~1-5€/mês/dispositivo); zero infra; ideal deployment rápido, cobertura existente
- Break-even depende de escala e duração

### Solução 8
- **OTAA:** join procedure com AppKey, gera session keys dinamicamente → keys únicas por sessão, revogáveis
- **ABP:** keys pré-configuradas → risco se dispositivo clonado, sem re-keying
- **OTAA mais seguro** (recomendado para produção)
