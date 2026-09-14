# Módulo 04 — WLAN, WPAN: Wi-Fi, BLE e ZigBee

**UC:** Redes Sem Fios e de Sensores · **Fase:** 2 — Tecnologias

## Objetivos de aprendizagem

- Comparar IEEE 802.11 (Wi-Fi) e 802.15.x (WPAN)
- Analisar Bluetooth Low Energy (BLE) e aplicações
- Compreender IEEE 802.15.4 e stack ZigBee
- Seleccionar tecnologia adequada por cenário

---

## 1. Classificação IEEE 802

| Grupo | Standard | Nome | Alcance | Taxa |
|-------|----------|------|---------|------|
| WLAN | 802.11 | Wi-Fi | 10–100 m | Mbit/s – Gbit/s |
| WPAN | 802.15.1 | Bluetooth Classic | 10 m | 1–3 Mbit/s |
| WPAN | 802.15.1 (BLE) | Bluetooth LE | 10–100 m | 125 kbps – 2 Mbps |
| WPAN | 802.15.4 | LR-WPAN | 10–100 m | 20–250 kbps |
| WMAN | 802.16 | WiMAX | km | Mbit/s |

---

## 2. Wi-Fi (IEEE 802.11)

### Evolução

| Standard | Banda | Taxa máx. | Notas |
|----------|-------|-----------|-------|
| 802.11n | 2.4/5 GHz | 600 Mbit/s | MIMO, 40 MHz |
| 802.11ac (Wi-Fi 5) | 5 GHz | 3.5 Gbit/s | MU-MIMO, 256-QAM |
| 802.11ax (Wi-Fi 6) | 2.4/5 GHz | 9.6 Gbit/s | OFDMA, TWT |
| 802.11be (Wi-Fi 7) | 2.4/5/6 GHz | ~46 Gbit/s | 320 MHz, MLO |

### Arquitectura

```
Estação (STA) ←→ Access Point (AP) ←→ Rede com fios
                    ou
              STA ←→ STA (Ad-hoc, Wi-Fi Direct)
```

### Funcionalidades chave

- **CSMA/CA** com backoff exponencial
- **MIMO:** múltiplas antenas → throughput e diversidade
- **OFDM/OFDMA:** subportadoras (Wi-Fi 6: multi-user OFDMA)
- **Segurança:** WPA3 (SAE, 192-bit security)
- **Power Save:** PS-Poll, TWT (Target Wake Time — Wi-Fi 6)

### Wi-Fi para IoT

- **Pros:** alto throughput, ubiquidade, IP nativo
- **Contras:** consumo elevado, alcance limitado, congestão 2.4 GHz

---

## 3. Bluetooth Low Energy (BLE)

### Características

| Aspeto | BLE |
|--------|-----|
| Banda | 2.4 GHz (40 canais de 2 MHz) |
| Taxa | 125 kbps – 2 Mbps (BLE 5) |
| Alcance | 10 m (default), até 1 km (BLE 5 Long Range, Coded PHY) |
| Consumo | mA em TX/RX, µA em sleep |
| Topologia | Star (GATT server/client), mesh (BLE Mesh) |

### Stack BLE

```
Aplicação (GATT profiles)
    ├── GAP (Generic Access Profile) — advertising, pairing
    └── GATT (Generic Attribute Profile) — services, characteristics
L2CAP
HCI
Link Layer (LL)
Physical Layer
```

### Modos de operação

| Modo | Descrição |
|------|-----------|
| **Advertising** | Broadcaster envia beacons |
| **Connection** | Central ↔ Peripheral (GATT) |
| **Mesh** | Flooding gerido, relay nodes |

### BLE 5 melhorias

- 2× velocidade (2 Mbps PHY)
- 4× alcance (Coded PHY: S=2, S=8)
- 8× advertising data (255 bytes)
- Advertising extensions, periodic advertising

### Aplicações IoT

- Wearables, beacons, fechaduras, sensores ambientais
- Commissioning (Matter, Thread usa BLE para setup)

---

## 4. IEEE 802.15.4

Standard para **LR-WPAN** (Low-Rate Wireless Personal Area Network).

| Parâmetro | Valor |
|-----------|-------|
| Banda | 868/915 MHz, 2.4 GHz |
| Taxa | 250 kbps (2.4 GHz), 20–100 kbps (sub-GHz) |
| Frame | Max 127 bytes payload |
| Topologia | Star, peer-to-peer, mesh (via upper layer) |
| Segurança | AES-128-CCM* |
| MAC | CSMA/CA ou beacon-enabled (TDMA superframe) |

### Endereçamento

- Short address: 16 bits
- Extended address: 64 bits (EUI-64)

---

## 5. ZigBee (sobre 802.15.4)

Stack completa para redes mesh de sensores.

### Camadas

```
ZigBee Application Layer (ZCL — ZigBee Cluster Library)
ZigBee Network Layer (NWK) — mesh routing
IEEE 802.15.4 MAC + PHY
```

### Topologias

| Tipo | Descrição |
|------|-----------|
| **Star** | End devices → coordinator |
| **Tree** | Hierárquica com routers |
| **Mesh** | Multi-hop, auto- healing |

### Tipos de nós

| Nó | Função |
|----|--------|
| **Coordinator** | Um por rede, forma PAN |
| **Router** | Relay, permite filhos |
| **End Device** | Sensor/actuador, pode sleep (RFD) |

### ZigBee vs. alternativas

| | ZigBee | Thread | BLE Mesh |
|--|--------|--------|----------|
| Base | 802.15.4 | 802.15.4 | BLE |
| Routing | AODV-like (ZigBee PRO) | RPL (IPv6) | Flooding managed |
| IP | Não (proprietário) | Sim (6LoWPAN) | Não |
| Interop | ZigBee 3.0 | Matter | Limitada |

---

## 6. Tabela comparativa

| Critério | Wi-Fi 6 | BLE 5 | ZigBee (802.15.4) |
|----------|---------|-------|-------------------|
| Taxa | Gbit/s | 2 Mbps | 250 kbps |
| Alcance | 50 m | 100 m+ (coded) | 100 m |
| Energia | Alta | Muito baixa | Baixa |
| Topologia | Star (AP) | Star/Mesh | Mesh |
| IP nativo | Sim | Não (gateway) | Não (gateway) |
| Custo nó | Médio | Baixo | Baixo |
| IoT fit | Gateway, câmaras | Wearables, beacons | Sensores mesh |

---

## Exercícios

### Exercício 1
Compare Wi-Fi e 802.15.4 para sensores de humidade numa estufa de 200 m².

### Exercício 2
Explique o papel do GATT no BLE e a diferença entre Central e Peripheral.

### Exercício 3
Porque o MTU de 802.15.4 (127 bytes) influencia protocolos superiores?

### Exercício 4
Descreva a topologia mesh ZigBee e o papel dos routers.

### Exercício 5
Um beacon BLE transmite a cada 100 ms. Estime duty cycle se TX dura 1 ms.

### Exercício 6
Compare ZigBee e Thread. Porque Thread é preferido para Matter?

### Exercício 7
Wi-Fi 6 introduz TWT (Target Wake Time). Como beneficia dispositivos IoT?

### Exercício 8
Identifique três fontes de interferência entre Wi-Fi e ZigBee em 2.4 GHz.

---

## Soluções

### Solução 1
**802.15.4/ZigBee preferível:** baixo consumo (bateria), mesh sem infraestrutura AP, custo baixo por nó, 250 kbps suficiente para humidade. Wi-Fi: consumo alto, overkill em taxa, requer AP.

### Solução 2
GATT define services/characteristics (dados estruturados). **Central** inicia conexão e lê/escreve; **Peripheral** anuncia services e responde. Ex.: smartphone (Central) ↔ sensor (Peripheral).

### Solução 3
Payload pequeno força fragmentação IP (6LoWPAN), compressão de headers, mensagens CoAP compactas, e aggregation. Overhead MAC/security proporcionalmente alto → optimizar tamanho de pacote.

### Solução 4
Mesh: end devices comunicam via routers multi-hop ao coordinator. Routers relay frames, mantêm tabela de routing, permitem filhos (end devices ou routers). Auto-healing: rotas alternativas se router falhar.

### Solução 5
Duty cycle = 1 ms / 100 ms = **1%** (ideal; na prática inclui RX windows e overhead advertising).

### Solução 6
- **ZigBee:** stack proprietária, sem IP nativo
- **Thread:** IPv6 nativo (6LoWPAN), RPL, aberto (Thread Group)
- **Matter** requer IP (Thread ou Wi-Fi) para interoperabilidade universal → Thread preferido em WPAN

### Solução 7
TWT negocia janelas de wake-up entre AP e STA → dispositivo dorme até slot acordado → reduz consumo e contensão no canal.

### Solução 8
1. Overlap espectral (canais Wi-Fi 20 MHz vs. ZigBee 2 MHz)
2. Transmissões Wi-Fi de alta potência em canais adjacentes
3. Coexistência no mesmo AP/router com ZigBee coordinator
