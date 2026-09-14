# Matéria Extra — Tópicos Complementares IoT

**UC:** Internet das Coisas · **Contínuo** · Leitura complementar

Este documento cobre tópicos avançados ou sectoriais que enrichcem a formação IoT mas não são núcleo obrigatório dos módulos 01–08.

---

## 1. OPC-UA (Open Platform Communications Unified Architecture)

### 1.1 O que é?

**OPC-UA** é standard industrial (IEC 62541) para **interoperabilidade máquina-a-máquina** em automação industrial, substituindo OPC Classic (COM/DCOM, Windows-only).

### 1.2 Características

| Aspeto | OPC-UA |
|--------|--------|
| Modelo | Cliente-Servidor + PubSub |
| Transporte | TCP binário, HTTPS, MQTT (PubSub) |
| Informação | Modelo de objectos tipados (nodes, references) |
| Segurança | Built-in: signing, encryption, certificates |
| Escalabilidade | Shop floor → IT → cloud |

### 1.3 Modelo de informação

Dados organizados em **Address Space** — árvore de nodes:

- **Objects** — representam equipamento
- **Variables** — valores (temperatura, estado)
- **Methods** — acções invocáveis (start, stop)

Semântica **padronizada** via companion specifications (Packaging, Robotics).

### 1.4 OPC-UA vs. MQTT

| | OPC-UA | MQTT |
|---|--------|------|
| Domínio | Industrial automation | IoT general-purpose |
| Semântica | Rich typed model | Payload livre (JSON) |
| Interop vendor | Nativa | Requer convenção tópicos |
| Overhead | Maior | Menor |

**Convergência:** OPC-UA PubSub sobre MQTT combina semântica industrial com broker MQTT.

### 1.5 Casos de uso

- Integração PLC Siemens ↔ SCADA ↔ MES
- Industry 4.0 digital thread
- Gateway traduz OPC-UA → cloud JSON

---

## 2. LoRaWAN

### 2.1 O que é?

**LoRaWAN** é protocolo **MAC layer** de rede long-range, low-power sobre radio **LoRa** (Semtech chirp spread spectrum).

### 2.2 Arquitectura

```
[End Devices] ──LoRa RF──► [Gateways] ──IP──► [Network Server] ──► [Application Server]
     ↑                           ↑                    ↑
  Sensors                   Sem múltiplos          Join, routing,
  bateria anos              gateways               dedup
```

| Componente | Função |
|------------|--------|
| **End Device** | Sensor/actuador Class A/B/C |
| **Gateway** | Bridge RF ↔ IP (sem lógica app) |
| **Network Server** | Autenticação, ADR, deduplicação |
| **Application Server** | Decrypt payload, integração |

### 2.3 Classes de dispositivos

| Classe | RX windows | Uso |
|--------|------------|-----|
| **A** | 2 slots após TX | Bateria máxima; uplink mostly |
| **B** | Scheduled ping slots | Comandos downlink previsíveis |
| **C** | RX quase contínuo | Alimentado; actuadores |

### 2.4 Características RF

- **Alcance:** 2–15 km rural, 1–3 km urbano
- **Data rate:** 0.3–50 kbps (trade-off range)
- **Payload:** até 51–242 bytes (regional)
- **Frequências:** EU868, US915, etc.

### 2.5 Segurança

- **AES-128** AppSKey / NwkSKey
- **Join procedure:** OTAA (Over-The-Air Activation) preferido vs. ABP
- Payload encriptado end-to-end até Application Server

### 2.6 Quando usar

Agricultura, smart cities, asset tracking — muitos devices, poucos bytes, bateria longa, sem Wi-Fi/celular viável.

---

## 3. Digital Twins (Gémeos Digitais)

### 3.1 Definição

**Digital Twin** é representação virtual **dinâmica** de um activo físico, sincronizada com dados em tempo real, permitindo simulação, monitorização e optimização.

```
[Physical Asset] ◄─── actuators ─── [Control System]
       │                                    ▲
       │ sensors                            │
       ▼                                    │
   [Telemetry] ──► [Digital Twin Model] ───┘
                           │
                           ▼
                    [Simulation / AI / What-if]
```

### 3.2 Componentes

| Componente | Descrição |
|------------|-----------|
| **Physical entity** | Máquina, edifício, cidade |
| **Virtual model** | Geometria, comportamento, regras |
| **Connection** | IoT sync bidireccional |
| **Data** | Histórico + real-time |

### 3.3 Níveis de maturidade

1. **Descriptive** — visualização 3D + telemetria
2. **Informative** — analytics, alertas
3. **Predictive** — ML previsão falhas
4. **Comprehensive** — simulação what-if
5. **Autonomous** — twin controla físico automaticamente

### 3.4 Tecnologias

- **Azure Digital Twins** — DTDL modeling language
- **AWS IoT TwinMaker**
- **GE Predix**, **Siemens MindSphere**
- **Unity/Unreal** — visualização 3D

### 3.5 Casos de uso

- Manutenção preditiva turbina — simular desgaste
- Smart building — optimizar HVAC em twin antes aplicar
- Supply chain — twin de armazém

---

## 4. Plataformas Cloud IoT — AWS e Azure

### 4.1 AWS IoT Core

**Serviço managed MQTT/HTTP** para fleet de dispositivos.

| Funcionalidade | Serviço |
|----------------|---------|
| Ingestão MQTT | IoT Core |
| Regras routing | IoT Rules → Lambda, S3, DynamoDB |
| Device registry | Thing + certificates |
| Shadow | Estado desired/reported |
| Edge | Greengrass |
| Analytics | IoT Analytics |
| Fleet provisioning | Just-in-time certs |

**Device Shadow exemplo:**
```json
{
  "state": {
    "desired": { "temperature_setpoint": 22 },
    "reported": { "temperature_setpoint": 22, "current_temp": 24.1 }
  }
}
```

App escreve desired; device sync reported.

### 4.2 Azure IoT Hub

Hub central bidireccional para dispositivos.

| Funcionalidade | Serviço |
|----------------|---------|
| Ingestão | IoT Hub (MQTT, AMQP, HTTP) |
| Device twins | Sync estado cloud-device |
| Edge computing | IoT Edge modules |
| Provisioning | DPS (Device Provisioning Service) |
| Digital twins | Azure Digital Twins |
| Time-series | Azure Data Explorer, TSI |

### 4.3 Comparação rápida

| | AWS IoT Core | Azure IoT Hub |
|---|--------------|---------------|
| Protocolo dominante | MQTT | MQTT, AMQP |
| Edge | Greengrass | IoT Edge (Docker) |
| Twin concept | Device Shadow | Device Twin |
| Digital Twin | TwinMaker | Digital Twins (DTDL) |
| Integração | Lambda, AWS ecosystem | Azure Functions, AD |

### 4.4 Padrão arquitectura cloud

```
[Devices] → [IoT Hub/Core] → [Stream processing] → [Storage] → [Dashboard]
                  ↓
            [Rules / Functions]
                  ↓
            [Alerts, integrations]
```

---

## 5. OTA Updates (Over-The-Air)

### 5.1 Importância

Dispositivos IoT em campo **anos** sem USB — segurança e features exigem **actualização remota de firmware**.

### 5.2 Arquitectura OTA

```
[Build CI] → sign firmware.bin → [OTA Server / S3 / IoT Job]
                                        │
                              notify device (MQTT)
                                        ▼
                              [Device downloads chunks]
                                        ▼
                              [Verify signature]
                                        ▼
                              [Swap partition / flash]
                                        ▼
                              [Reboot → new firmware]
```

### 5.3 Requisitos de segurança

- **Assinatura criptográfica** verificada (secure boot chain)
- **HTTPS/MQTT TLS** download
- **Anti-rollback** — versão mínima
- **Dual partition (A/B)** — rollback se boot fail
- **Staged rollout** — canary subset primeiro

### 5.4 Protocolos e ferramentas

| Plataforma | Mecanismo |
|------------|-----------|
| ESP32 | esp_https_ota, ESP-IDF OTA API |
| AWS | IoT Jobs + S3 presigned URL |
| Azure | IoT Hub Device Management |
| MCUboot | Open source bootloader A/B |
| Mender | Open source OTA platform |

### 5.5 Boas práticas

1. Delta updates (bsdiff) para poupar bandwidth
2. Confirmar boot success antes commit partition
3. Monitorizar taxa falha OTA fleet-wide
4. Nunca plaintext firmware download
5. Testar em hardware representativo antes fleet push

### 5.6 Fluxo ESP-IDF simplificado

```c
esp_https_ota_config_t ota_config = {
    .url = "https://ota.example.com/firmware.bin",
    .cert_pem = server_cert,
};
esp_https_ota(&ota_config);  // download + verify + set boot partition
esp_restart();
```

---

## Exercícios

### Exercício 1
Compara OPC-UA e MQTT para integrar PLC industrial com dashboard cloud. Quando escolher cada um?

### Exercício 2
Calcula: sensor LoRa envia 20 bytes a cada 15 min. Quantos MB/mês por dispositivo? E 5000 dispositivos?

### Exercício 3
Explica diferença entre Device Shadow (AWS) e Device Twin (Azure) com exemplo termóstato.

### Exercício 4
Desenha arquitectura LoRaWAN completa para monitorização humidade solo em 10 km² com 200 sensores.

### Exercício 5
Que nível de digital twin (1–5) corresponde a: (a) modelo 3D estático, (b) ML preditivo falhas, (c) controlo autónomo?

### Exercício 6
Lista cinco riscos de OTA mal implementado e mitigação para cada.

### Exercício 7
Propõe pipeline AWS: ESP32 → IoT Core → Lambda → DynamoDB → alerta SNS.

### Exercício 8
Como combinarias OPC-UA shop floor com LoRaWAN sensores campo numa fábrica agroalimentar?

---

## Soluções

### Solução 1

**OPC-UA** quando:
- PLCs Siemens/Allen-Bradley com servers OPC nativos
- Semântica tipada crítica (interlocks safety)
- Integração SCADA/MES existente

**MQTT** quando:
- Cloud-native greenfield
- Dispositivos diversos sem OPC
- Fan-out analytics, mobile apps

**Híbrido:** OPC-UA gateway na linha produção traduz para MQTT cloud para analytics; OPC mantém-se local real-time.

### Solução 2

Por device:
20 B × (60/15) × 24 × 30 = 20 × 4 × 720 = **57 600 B/mês ≈ 56 KB/mês**

5000 devices: 57 600 × 5000 = 288 000 000 B ≈ **275 MB/mês** uplink total

Extremamente eficiente vs. celular/Wi-Fi contínuo.

### Solução 3

**Device Shadow / Twin** mantém estado **desired** (cloud/app) vs **reported** (device).

Termóstato:
```json
"desired": { "target_temp": 21 },
"reported": { "target_temp": 21, "current_temp": 23, "heater": "ON" }
```

App altera desired para 19 → device recebe sync → ajusta → actualiza reported. Funcionam similarmente; diferenças na API e DTDL tags (Azure).

### Solução 4

```
[200× LoRa soil sensors] ──RF868──► [3–4 Gateways multichannel]
                                           │ IP backhaul (4G/fiber)
                                           ▼
                                    [LoRaWAN Network Server]
                                    (TTN / ChirpStack / private)
                                           │
                                           ▼
                                    [Application Server]
                                           │ MQTT/HTTP
                                           ▼
                                    [Cloud: rules rega + dashboard]
```

Gateway placement: cobertura 10 km² rural ~ 3 gateways elevados. ADR optimiza SF/data rate. OTAA provisioning por sensor.

### Solução 5

(a) Nível 1 — Descriptive (3D + dados estáticos)  
(b) Nível 3 — Predictive  
(c) Nível 5 — Autonomous  

### Solução 6

| Risco | Mitigação |
|-------|-----------|
| Firmware malicioso inject | Assinatura + secure boot |
| Brick device mid-flash | Dual partition A/B |
| Downgrade attack | Anti-rollback eFuse |
| Download MITM | TLS + cert pinning |
| Fleet-wide bad update | Canary 5% + auto halt on error rate |

### Solução 7

```
ESP32 ──MQTT TLS──► AWS IoT Core (topic devices/esp32-01/telemetry)
                         │
                    IoT Rule SQL:
                    SELECT * FROM 'devices/+/telemetry' WHERE temp > 40
                         │
                         ▼
                    AWS Lambda (process alert, enrich)
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
         DynamoDB               SNS → email/SMS
    (telemetry history)      "High temp device X"
```

IoT Core regista Thing + cert; Lambda idempotente com message_id.

### Solução 8

```
Shop floor (OPC-UA):
  PLCs packaging ──OPC-UA──► Edge gateway OPC ──MQTT──► Cloud MES

Campo (LoRaWAN):
  Solo humidade ──LoRa──► LoRa gateway ──► Application Server ──MQTT──► Cloud

Cloud correlaciona:
  humidade baixa (LoRa) + linha produção alta (OPC-UA) → ajuste rega + log batch produção
```

OPC-UA permanece on-prem real-time; LoRaWAN para assets geográficos dispersos; cloud agrega business intelligence.

---

## Referências

- [OPC Foundation](https://opcfoundation.org/)
- [LoRa Alliance](https://lora-alliance.org/)
- [AWS IoT Documentation](https://docs.aws.amazon.com/iot/)
- [Azure IoT Documentation](https://learn.microsoft.com/azure/iot/)
- [ESP-IDF OTA Updates](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html)
- [ROADMAP da UC](../ROADMAP.md)
