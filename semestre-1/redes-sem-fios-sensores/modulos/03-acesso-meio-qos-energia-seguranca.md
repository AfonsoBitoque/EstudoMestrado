# Módulo 03 — Acesso ao Meio, QoS, Energia e Segurança

**UC:** Redes Sem Fios e de Sensores · **Fase:** 1 — Fundamentos

## Objetivos de aprendizagem

- Comparar protocolos MAC para redes sem fios
- Analisar mecanismos de QoS em ambientes constrained
- Compreender técnicas de eficiência energética
- Identificar desafios e soluções de segurança em WSN/IoT

---

## 1. Acesso ao meio (MAC)

O protocolo MAC regula **quem transmite quando** no meio partilhado.

### Classificação

| Tipo | Mecanismo | Exemplos |
|------|-----------|----------|
| **Contention-based** | Competem pelo canal | CSMA/CA (802.11, 802.15.4) |
| **Schedule-based** | Slots atribuídos | TDMA (802.15.4 beacon mode) |
| **Hybrid** | Combinação | 802.15.4 superframe |

### CSMA/CA (802.11 e 802.15.4)

```
1. Escutar canal (CCA — Clear Channel Assessment)
2. Se livre → transmitir
3. Se ocupado → backoff aleatório → repetir
4. ACK (802.15.4 unicast)
```

**Problemas:** colisões, hidden terminal, exposed terminal.

### Soluções ao hidden terminal

| Protocolo | Mecanismo |
|-----------|-----------|
| **RTS/CTS** (802.11) | Reserva canal antes de dados |
| **802.15.4** | ACK implícito, GTS (guaranteed slots) |

### TDMA

- Slots temporais pré-atribuídos
- **Sem colisões**, previsível, eficiente em energia (sleep entre slots)
- **Desvantagem:** sincronização, inflexível com tráfego variável

### Comparativo CSMA/CA vs. TDMA

| Aspeto | CSMA/CA | TDMA |
|--------|---------|------|
| Colisões | Possíveis | Não |
| Overhead | Backoff, retransmissões | Sincronização |
| Energia | Médio (escuta activa) | Bom (sleep programado) |
| Escalabilidade | Degrada com carga | Fixa por design |
| Latência | Variável | Previsível |

---

## 2. QoS — Quality of Service

Garantir requisitos diferenciados (latência, perda, throughput).

### Mecanismos

| Mecanismo | Descrição | Tecnologia |
|-----------|-----------|------------|
| **Priorização** | Filas por classe | 802.11e (EDCA), 802.15.4 CAP |
| **Reserva** | Bandwidth garantido | 802.11 HCF, GTS |
| **Fragmentação** | Pacotes pequenos | 802.15.4 (127 bytes MTU) |
| **Admission control** | Limitar admissões | 802.11 QoS AP |

### 802.11e — EDCA

4 Access Categories (AC):

| AC | Prioridade | Uso |
|----|------------|-----|
| VO (Voice) | Mais alta | VoIP |
| VI (Video) | Alta | Streaming |
| BE (Best Effort) | Normal | Dados gerais |
| BK (Background) | Baixa | Bulk transfer |

Cada AC tem diferentes parametros de backoff (AIFSN, CW).

### QoS em IoT constrained

- **CoAP CON/NON:** confirmável vs. não-confirmável
- **MQTT QoS 0/1/2:** at-most-once, at-least-once, exactly-once
- **RPL Objective Function:** optimizar por latência, energia ou confiabilidade

---

## 3. Eficiência energética

### Consumo típico (802.15.4)

| Estado | Corrente |
|--------|----------|
| TX | 15–20 mA |
| RX | 15–20 mA |
| Sleep | 0.5–2 µA |

**Ratio TX/sleep:** ~10 000× — minimizar radio ON time é crítico.

### Técnicas

| Técnica | Descrição |
|---------|-----------|
| **Duty cycling** | Radio ON apenas em janelas (1–10%) |
| **Data aggregation** | Comprimir dados no sensor antes de TX |
| **Adaptive sampling** | Reduzir frequência se variância baixa |
| **Sleep scheduling** | TDMA, synchronized wake-up |
| **Energy harvesting** | Solar, vibração, RF harvesting |
| **Power control** | Reduzir \( P_{tx} \) se SNR suficiente |
| **Routing energy-aware** | LEACH, PEGASIS |

### Métricas

- **Lifetime:** tempo até primeiro nó morrer
- **Energy per bit:** J/bit transmitido
- **Duty cycle:** % tempo radio activo

---

## 4. Segurança em WSN/IoT

### Ameaças

| Ameaça | Descrição |
|--------|-----------|
| Eavesdropping | Interceptar comunicações |
| Injection | Inserir pacotes falsos |
| Replay | Reenviar pacotes capturados |
| Sybil | Múltiplas identidades falsas |
| Sinkhole | Atrair tráfego para nó malicioso |
| DoS | Inundar canal ou esgotar bateria |

### Serviços de segurança

| Serviço | Mecanismo |
|---------|-----------|
| Confidencialidade | AES-128-CCM (802.15.4 security) |
| Integridade | MIC (Message Integrity Code) |
| Autenticação | Pre-shared keys, certificates |
| Disponibilidade | Rate limiting, jamming detection |

### 802.15.4 Security

- **AES-128-CCM*:** cifragem + autenticação
- Key sizes: 128 bits
- Frame counter anti-replay

### Desafios IoT

- Dispositivos Classe 0: criptografia pesada
- Key management em escala (milhares de nós)
- OTA updates seguros
- Side-channels em hardware barato

---

## Exercícios

### Exercício 1
Explique o problema do hidden terminal e como RTS/CTS o mitiga.

### Exercício 2
Compare CSMA/CA e TDMA para uma WSN com 100 sensores e tráfego periódico baixo.

### Exercício 3
Um nó 802.15.4 tem duty cycle de 2%. TX consome 18 mA, sleep 1 µA. Estime corrente média.

### Exercício 4
Descreva as diferenças entre MQTT QoS 0, 1 e 2.

### Exercício 5
Identifique três ataques específicos a WSN e uma contramedida para cada.

### Exercício 6
Porque data aggregation melhora eficiência energética?

### Exercício 7
Explique o papel do frame counter em 802.15.4 security.

### Exercício 8
Num cenário com tráfego de voz e dados, como 802.11e EDCA prioriza voz?

---

## Soluções

### Solução 1
Hidden terminal: A e C não se ouvem, ambos transmitem para B → colisão. RTS/CTS: A envia RTS a B; B responde CTS (ouvido por C); C adia transmissão ao detectar CTS.

### Solução 2
**TDMA preferível:** tráfego periódico previsível, sem colisões, nós dormem fora do slot → máxima eficiência energética. CSMA/CA: colisões aumentam com 100 nós, backoff desperdiça energia, escuta activa constante.

### Solução 3
\( I_{avg} = 0.02 \times 18 + 0.98 \times 0.001 = 0.36 + 0.00098 \approx \mathbf{0.36 \text{ mA}} \)

### Solução 4
- **QoS 0:** fire-and-forget, sem ACK — at-most-once, mais rápido
- **QoS 1:** PUBACK confirmado — at-least-once (possível duplicado)
- **QoS 2:** handshake 4-way — exactly-once, mais overhead

### Solução 5
1. **Sybil** → autenticação centralizada, certificados
2. **Sinkhole** → roteamento multi-path, detecção de anomalias
3. **Replay** → frame counter monotónico + nonce
4. **DoS** → rate limiting, duty cycle regulation

### Solução 6
Agregar N leituras num pacote reduz transmissões de N para 1. Como TX domina consumo, reduz energia ~N× (menos overhead MAC, menos ACKs).

### Solução 7
Contador monotónico por chave em cada frame seguro. Receptor rejeita frames com contador ≤ último aceite → impede replay de pacotes capturados anteriormente.

### Solução 8
EDCA atribui AC_VO (voz) parâmetros agressivos: AIFSN menor (escuta menos), CW menor (backoff mais curto) → voz acede ao canal preferencialmente sobre BE/BK.
