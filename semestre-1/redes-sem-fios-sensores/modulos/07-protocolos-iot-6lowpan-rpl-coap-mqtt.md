# Módulo 07 — Protocolos IoT: 6LoWPAN, RPL, CoAP e MQTT

**UC:** Redes Sem Fios e de Sensores · **Fase:** 3 — Redes de sensores e protocolos IoT

## Objetivos de aprendizagem

- Compreender adaptação IPv6 para redes constrained (6LoWPAN)
- Analisar roteamento RPL em LLNs
- Comparar CoAP e MQTT para aplicações IoT
- Implementar arquitecturas IP em dispositivos restritos

---

## 1. Motivação: IP everywhere

IoT beneficia de **IPv6 nativo**:
- Endereçamento escalável (2¹²⁸ endereços)
- Interoperabilidade com Internet
- Ferramentas standard (ping, routing, firewalls)
- Evolução independente de vendor

**Desafio:** IPv6 (1280 bytes MTU) + 802.15.4 (127 bytes frame) → **6LoWPAN**

---

## 2. 6LoWPAN (IPv6 over Low-Power Wireless Personal Area Networks)

RFC 4944, 6282, 6775.

### Funções

| Função | Mecanismo |
|--------|-----------|
| **Header compression** | HC1/HC6/IPv6 (IPHC) — 40 bytes → 2–3 bytes |
| **Fragmentation** | Divide pacotes IPv6 em frames 802.15.4 |
| **Mesh forwarding** | Mesh header (RFC 4944) ou RPL |
| **Neighbor discovery** | 6LoWPAN-ND (RFC 6775) — substitui IPv6 ND |

### Header compression (IPHC)

```
IPv6 header (40 bytes):
  Version, TC, FL, PL, NH, HL, Src, Dst

Comprimido (2-3 bytes):
  TF (Traffic Class, Flow Label) — inline ou elided
  NH (Next Header) — elided se UDP comprimido
  HL (Hop Limit) — inline ou elided
  SA/DA — elided, 16-bit, ou 64-bit inline
```

Endereço IPv6 derivado de EUI-64 do 802.15.4.

### Adaptation layer

```
┌──────────────────────────────┐
│ IPv6 + UDP + CoAP payload    │
├──────────────────────────────┤
│ 6LoWPAN adaptation (frag)    │
├──────────────────────────────┤
│ 802.15.4 MAC frame (≤127 B)  │
└──────────────────────────────┘
```

---

## 3. RPL (IPv6 Routing Protocol for LLNs)

RFC 6550 — routing para redes com perda, baixa potência, topologia dinâmica.

### Conceitos

| Conceito | Descrição |
|----------|-----------|
| **DODAG** | Destination-Oriented Directed Acyclic Graph |
| **Root (DODAG root)** | Sink/border router |
| **Rank** | Distância ao root (via Objective Function) |
| **DAO/DIO** | DODAG Advertisement / Destination Advertisement Object |

### Modos de operação

| Modo | Tráfego | Uso |
|------|---------|-----|
| **No-Downward** | Só upstream (sensores → root) | Monitorização |
| **Storing** | Downstream via intermediate routers | Actuadores |
| **Non-storing** | Downstream via root (source routing) | Memória limitada |

### Objective Functions

| OF | Métrica | Uso |
|----|---------|-----|
| **OF0** (RFC 6552) | Hop count | Simples |
| **MRHOF** (RFC 6719) | ETX (Expected Transmission Count) | Fiabilidade |

### Trickle timer

Controla frequência de DIO (proactive maintenance) — adapta a estabilidade da rede.

---

## 4. CoAP (Constrained Application Protocol)

RFC 7252 — protocolo de aplicação RESTful para dispositivos constrained.

### Características

| Aspeto | CoAP | HTTP |
|--------|------|------|
| Transporte | UDP | TCP |
| Header | 4 bytes | ~200+ bytes |
| Métodos | GET, POST, PUT, DELETE | Idem + PATCH, etc. |
| Formato | Binary | Text |
| Observação | Nativa (observe option) | WebSocket/SSE |

### Message types

| Tipo | Descrição |
|------|-----------|
| **CON** | Confirmable — requer ACK |
| **NON** | Non-confirmable — fire-and-forget |
| **ACK** | Acknowledgement |
| **RST** | Reset |

### URI e recursos

```
coap://[2001:db8::1]/temperature
coap://sensor.local/.well-known/core  (discovery)
```

### CoAP sobre 6LoWPAN

```
CoAP (UDP port 5683)
  → UDP (comprimido)
    → IPv6 (comprimido)
      → 6LoWPAN
        → 802.15.4
```

### Segurança: DTLS

DTLS (Datagram TLS) protege CoAP — perfil constrained (RFC 7925).

---

## 5. MQTT (Message Queuing Telemetry Transport)

Protocolo publish/subscribe sobre TCP (ou TLS).

### Arquitectura

```
Publisher → [Broker] → Subscriber
              ↑
         (tópicos)
```

### Características

| Aspeto | MQTT |
|--------|------|
| Transporte | TCP/TLS (porta 1883/8883) |
| Modelo | Publish/Subscribe |
| QoS | 0 (at-most-once), 1 (at-least-once), 2 (exactly-once) |
| Overhead | ~2 bytes header mínimo |
| Last Will | Mensagem automática se disconnect |

### MQTT vs. CoAP

| Critério | CoAP | MQTT |
|----------|------|------|
| Paradigma | REST (request/response) | Pub/Sub |
| Transporte | UDP | TCP |
| Overhead | Muito baixo | Baixo |
| Broker | Opcional (direct) | Necessário |
| Constrained | Nativo | MQTT-SN para constrained |
| Observação | CoAP observe | Subscrição tópico |
| Firewalls/NAT | Difícil (UDP) | Fácil (TCP) |

### MQTT-SN (Sensor Networks)

Adaptação MQTT para UDP/802.15.4 — gateway MQTT-SN ↔ MQTT.

---

## 6. Stack completa IoT constrained

```
┌─────────────────────────────────┐
│ Aplicação (CoAP/MQTT-SN)        │
├─────────────────────────────────┤
│ Transporte (UDP/TCP)            │
├─────────────────────────────────┤
│ Rede (IPv6 + RPL + 6LoWPAN)    │
├─────────────────────────────────┤
│ MAC/PHY (802.15.4)              │
└─────────────────────────────────┘
         ↕ Border Router
┌─────────────────────────────────┐
│ IPv6 Internet / Cloud           │
│ (MQTT broker, HTTP API)          │
└─────────────────────────────────┘
```

**Border Router:** traduz 6LoWPAN ↔ Ethernet/Wi-Fi (Contiki-NG, OpenThread).

---

## Exercícios

### Exercício 1
Porque 6LoWPAN é necessário para usar IPv6 sobre 802.15.4?

### Exercício 2
Explique header compression IPHC e quantos bytes poupa tipicamente.

### Exercício 3
Descreva a formação de um DODAG em RPL quando um novo nó junta-se à rede.

### Exercício 4
Compare CoAP CON e NON. Quando usar cada um?

### Exercício 5
Um sensor publica temperatura a cada 10 s. CoAP observe ou MQTT subscribe — qual preferir e porquê?

### Exercício 6
Explique a diferença entre RPL storing e non-storing mode.

### Exercício 7
Calcule overhead: frame 802.15.4 = 127 bytes, MAC+sec = 25 bytes, 6LoWPAN frag header = 5 bytes. Qual o payload IPv6 máximo por fragmento?

### Exercício 8
Descreva o papel do border router numa rede Thread/6LoWPAN.

---

## Soluções

### Solução 1
802.15.4 frame = 127 bytes max; IPv6 header = 40 bytes + UDP 8 + payload → não cabe. 6LoWPAN comprime headers e fragmenta pacotes IPv6 em múltiplos frames 802.15.4.

### Solução 2
IPHC comprime endereços (elided se derivados de MAC), flow label, hop limit, next header. Típico: 40 bytes → **2–3 bytes** (poupança ~37 bytes), crítico em frames de 127 bytes.

### Solução 3
1. Nó envia multicast DIO (DODAG Information Object)
2. Nó pai responde com rank e métricas (ETX)
3. Nó selecciona pai (menor rank via OF)
4. Nó envia DAO (Destination Advertisement) ao root via pai
5. Root/registos conhecem rota downstream

### Solução 4
- **CON:** dados críticos, requer confirmação (ACK) — sensores alarme, actuadores
- **NON:** dados periódicos tolerantes a perda — leituras ambientais frequentes, menor overhead

### Solução 5
**CoAP observe** se rede constrained (6LoWPAN nativo, sem broker). **MQTT subscribe** se gateway/broker já existe na cloud. CoAP: menos infra, directo; MQTT: melhor integração cloud, QoS, histórico.

### Solução 6
- **Storing:** routers intermediários mantêm tabelas de routing downstream — tráfego downstream local, mais memória
- **Non-storing:** root mantém rotas, encapsula source routing header — routers stateless, menos memória nos nós

### Solução 7
127 − 25 − 5 = **97 bytes** payload por fragmento (approx.; depende de headers adicionais)

### Solução 8
Border router: interface 802.15.4 (6LoWPAN mesh) + interface IP (Ethernet/Wi-Fi). Faz prefix delegation IPv6, routing entre mesh e Internet, pode hospedar DODAG root (RPL), traduz para MQTT/HTTP na cloud.
