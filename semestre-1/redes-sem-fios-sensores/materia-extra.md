# Matéria Extra — Redes Sem Fios e de Sensores

Conteúdo complementar para aprofundamento além do programa base.

---

## 1. Wi-Fi 6 (802.11ax) e Wi-Fi 7 (802.11be)

### Wi-Fi 6 (802.11ax) — 2019

| Inovação | Descrição | Benefício IoT |
|----------|-----------|---------------|
| **OFDMA** | Múltiplos utilizadores por canal simultaneamente | Eficiência com muitos dispositivos |
| **TWT** | Target Wake Time — agendar wake-up | Redução consumo IoT |
| **BSS Coloring** | Identificar BSS em ambientes densos | Menos interferência |
| **1024-QAM** | Maior taxa por subportadora | Throughput |
| **MU-MIMO** | Downlink e uplink | Densidade |

### Wi-Fi 7 (802.11be) — 2024

| Inovação | Descrição |
|----------|-----------|
| **320 MHz channels** | Largura canal dupla vs. Wi-Fi 6 |
| **Multi-Link Operation (MLO)** | Agregar 2.4 + 5 + 6 GHz simultaneamente |
| **4096-QAM** | Maior eficiência espectral |
| **Preamble puncturing** | Usar banda parcial se interferida |
| **Taxa teórica** | ~46 Gbit/s |

### Implicações IoT

- Wi-Fi 6/7 tornam Wi-Fi viável para **massive IoT** (centenas de dispositivos por AP)
- TWT essencial para sensores alimentados por bateria
- Matter sobre Wi-Fi beneficia de OFDMA e TWT
- Wi-Fi 7 MLO: redundância e latência ultra-baixa para industrial

---

## 2. Matter (Project CHIP)

### Conceito

Standard de interoperabilidade smart home liderado pela **Connectivity Standards Alliance** (Apple, Google, Amazon, Samsung, etc.).

### Objectivo

Um protocolo unificado — dispositivos de diferentes vendors comunicam nativamente.

### Arquitectura

```
┌─────────────────────────────────────┐
│ Matter Application Layer (clusters) │
├─────────────────────────────────────┤
│ Matter Interaction Model            │
├─────────────────────────────────────┤
│ Matter Data Model                   │
├─────────────────────────────────────┤
│ Secure Channel (CASE/PASE)          │
├─────────────────────────────────────┤
│ Transport: IPv6                     │
├─────────────────────────────────────┤
│ Radio: Wi-Fi | Thread | Ethernet    │
└─────────────────────────────────────┘
```

### Transportes

| Transporte | Uso |
|------------|-----|
| **Thread** | Dispositivos constrained (802.15.4) |
| **Wi-Fi** | Dispositivos com mais recursos |
| **Ethernet** | Gateways, hubs |

### Commissioning

1. Dispositivo anuncia via **BLE** (commissioning)
2. QR code / manual code para pairing
3. Credenciais Thread/Wi-Fi transferidas via BLE
4. Dispositivo junta-se à fabric mesh/IP

### Segurança

- **PASE** (Password-Authenticated Session Establishment) — commissioning
- **CASE** (Certificate Authenticated Session Establishment) — operação
- Certificados DAC (Device Attestation Certificate)
- AES-CCM para mensagens

### Clusters Matter

Modelo de dados unificado: OnOff, LevelControl, TemperatureMeasurement, DoorLock, etc.

---

## 3. IoT Satélite

### Motivação

Cobertura global onde celular/LPWAN terrestre não chega: oceanos, florestas remotas, logística marítima, agricultura extensiva.

### Opções (2025)

| Serviço | Tipo | Banda | Taxa | Latência |
|---------|------|-------|------|----------|
| **Starlink IoT** (planeado) | LEO | — | — | Baixa |
| **Iridium Certus** | LEO | L-band | 88–704 kbps | ~1 s |
| **Inmarsat IDP** | GEO | L-band | 2.4–10 kbps | ~20 s |
| **Myriota** | LEO | VHF | 1 kbps | Horas |
| **Astrocast** | LEO | L-band | 1 kbps | Minutos |
| **Sateliot (3GPP NB-IoT)** | LEO | S-band | NB-IoT standard | ~10 s |

### Arquitecturas

```
Dispositivo IoT → Satélite → Gateway terrestre → Cloud
                  (direct-to-satellite)
```

vs.

```
Dispositivo → LPWAN gateway → Backhaul satélite → Cloud
```

### Desafios

| Desafio | Descrição |
|---------|-----------|
| **Custo terminal** | Módulos satélite > LPWAN terrestre |
| **Consumo energia** | TX satélite requer potência (100 mW – 2 W) |
| **Latência** | GEO: 500+ ms; LEO: 20–50 ms |
| **Regulação** | Espectro licenciado, autorizações |
| **Antena** | Patch vs. omnidireccional, pointing (GEO) |

### Direct-to-Satellite IoT (emergente)

- **3GPP Release 17+:** NTN (Non-Terrestrial Networks) — NB-IoT/LTE-M via satélite
- Apple/S Globalstar: SOS via satélite (consumidor)
- Qualcomm Snapdragon Satellite
- Integração com eSIM e roaming espacial

### Casos de uso

- Rastreamento gado em áreas remotas
- Monitorização ambiental (Amazónia, Ártico)
- Containers marítimos
- Estações meteorológicas oceânicas
- Backup connectivity para LPWAN gateways

---

## Exercícios complementares

### Exercício 1
Explique como TWT em Wi-Fi 6 beneficia um sensor de temperatura com bateria.

### Exercício 2
Porque Matter usa BLE para commissioning mas Thread para operação?

### Exercício 3
Compare IoT satélite LEO vs. GEO para sensores ambientais com 1 leitura/hora.

### Exercício 4
Descreva o fluxo de commissioning Matter com QR code.

---

## Soluções

### Solução 1
TWT permite ao sensor negociar com o AP janelas específicas de wake-up → dorme entre janelas → reduz consumo de escuta (RX) de always-on para scheduled → prolonga vida da bateria significativamente.

### Solução 2
- **BLE commissioning:** curto alcance, baixo consumo, ubiquidade em smartphones para setup inicial
- **Thread operação:** IPv6 mesh, multi-hop, escalável, adequado para automação contínua
- BLE não escala para mesh operacional; Thread não está em todos os phones para setup

### Solução 3
- **LEO:** latência ~ms, cobertura global com constellation, terminal mais simples (sem pointing), melhor para dados frequentes
- **GEO:** latência ~500 ms, terminal com antena direccional ou mais potência, adequado para 1 leitura/hora (duty cycle baixo tolera latência), custo terminal menor em alguns casos
- Para 1 leitura/hora ambiental: **LEO direct-to-satellite** (Myriota, Sateliot) ou **GEO store-and-forward** viáveis

### Solução 4
1. Utilizador abre app Matter, scan QR code no dispositivo
2. App extrai setup code (passcode, discriminator, certificate)
3. App estabelece BLE com dispositivo
4. PASE handshake autenticado com passcode
5. App envia credenciais Thread/Wi-Fi via BLE
6. Dispositivo junta-se à rede Matter; CASE para comunicação segura contínua
