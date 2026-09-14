# Módulo 07 — Edge Computing

**UC:** Internet das Coisas · **Parte III** · Tempo sugerido: 5–7 h

---

## Objetivos de aprendizagem

- Distinguir cloud, fog e edge computing no contexto IoT
- Identificar workloads adequados para processamento local
- Quantificar benefícios de latência, bandwidth e privacidade
- Desenhar arquitecturas híbridas edge-cloud com exemplos práticos

---

## 1. De cloud-only para edge

Arquitectura **cloud-only** envia **toda** telemetria bruta para a nuvem. Funciona com poucos dispositivos; com escala revela problemas:

| Problema | Impacto |
|----------|---------|
| Latência | 100–500 ms+ round-trip inviável para controlo em tempo real |
| Bandwidth | MB/dia × 10 000 devices = custos elevados |
| Privacidade | Vídeo/áudio/voz não podem sair do edifício (GDPR, HIPAA) |
| Disponibilidade | Internet down → sistema parado |
| Custo cloud | Ingress + storage + compute de dados redundantes |

**Edge computing** move processamento **para perto da fonte** — dispositivo, gateway ou servidor local.

---

## 2. Terminologia: edge vs. fog vs. cloud

```
┌─────────────────────────────────────────────────────────────┐
│                         CLOUD                                │
│              Regiões geográficas distantes                   │
└────────────────────────────┬────────────────────────────────┘
                             │ WAN
┌────────────────────────────▼────────────────────────────────┐
│                    FOG / EDGE GATEWAY                        │
│         Fábrica, edifício, base station — processamento      │
└────────────────────────────┬────────────────────────────────┘
                             │ LAN / PAN
┌────────────────────────────▼────────────────────────────────┐
│                    EDGE DEVICE                               │
│         Microcontrolador com inferência ML local             │
└─────────────────────────────────────────────────────────────┘
```

| Termo | Localização | Exemplos |
|-------|-------------|----------|
| **Edge (device)** | No sensor/actuador | ESP32-S3 com TFLite Micro |
| **Edge (gateway)** | Raspberry Pi, industrial PC | Node-RED, Azure IoT Edge |
| **Fog** | Rede local próxima | Servidor fábrica, 5G MEC |
| **Cloud** | Data center remoto | AWS, Azure, GCP |

**Fog** (Cisco) enfatiza camada intermédia na **rede**; **edge** enfatiza **proximidade física** aos dados. Na prática usam-se intercambiavelmente.

---

## 3. O que processar no edge?

### 3.1 Critérios de decisão

| Processar no edge se… | Enviar para cloud se… |
|-----------------------|----------------------|
| Latência < 50 ms crítica | Analytics histórico longo prazo |
| Dados volumosos (vídeo) | Treino ML pesado |
| Offline must-work | Correlação multi-site global |
| Dados sensíveis | Escalabilidade elástica |
| Agregação reduz 99% tráfego | Integração ERP/BI enterprise |

### 3.2 Workloads típicos no edge

- **Filtragem:** descartar leituras dentro de normalidade
- **Agregação:** média/min, max/min por janela
- **Detecção de eventos:** queda, intrusão, vibração anómala
- **Controlo em loop fechado:** PID motor, PID climatização
- **Inferência ML:** classificação imagem, anomaly detection leve
- **Protocol translation:** Modbus → MQTT
- **Buffer/store-and-forward** quando uplink falha

---

## 4. Redução de latência

### 4.1 Exemplo ilustrativo

**Cloud-only:** sensor → MQTT → cloud (200 ms) → regra → comando → dispositivo (200 ms) = **400 ms+**

**Edge:** sensor → gateway local (5 ms) → decisão → actuador = **< 20 ms**

Crítico para: robots industriais, veículos autónomos, proteção de pessoas.

### 4.2 Content Delivery analogy

Edge IoT é CDN invertido — compute vai para os dados, não dados para o compute.

---

## 5. Redução de bandwidth

Câmara 1080p @ 2 Mbps contínua = **~21 GB/dia**.

**Edge:** inferência detecta "pessoa na zona" → envia evento JSON 200 bytes = **~17 KB/dia** (99.99% redução).

---

## 6. Plataformas edge

| Plataforma | Descrição |
|------------|-----------|
| **AWS IoT Greengrass** | Lambda, ML, sync com cloud |
| **Azure IoT Edge** | Módulos Docker, offline |
| **Google Distributed Cloud** | Edge GKE |
| **Node-RED** | Low-code flows em gateway |
| **K3s / MicroK8s** | Kubernetes leve em edge server |
| **EdgeX Foundry** | Open source IoT edge framework |

### 6.1 Modelo de módulos (Azure IoT Edge exemplo)

```
┌─────────────────────────────────────┐
│  Edge Device (Raspberry Pi / IPC) │
│  ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │ Modbus  │ │ ML      │ │ MQTT  │ │
│  │ module  │→│ module  │→│ bridge│ │
│  └─────────┘ └─────────┘ └───────┘ │
└─────────────────────────────────────┘
         ▲ cloud deploy / monitor
```

Cloud define desired state; edge executa offline com sync periódico.

---

## 7. ML no edge

### 7.1 TensorFlow Lite Micro

Modelos quantizados (INT8) em KB de flash:

- Keyword spotting ("Hey device")
- Vibração normal vs. falha
- Classificação imagem simples

### 7.2 Trade-offs

| | Cloud ML | Edge ML |
|---|----------|---------|
| Modelo | GB, GPU | KB–MB |
| Actualização | Instant | OTA necessário |
| Dados | Todos centralizados | Privacidade local |
| Latência | Alta | Baixa |

**Padrão híbrido:** inferência edge; retreino cloud com features agregadas (não raw).

---

## 8. Sincronização edge-cloud

- **Config pull:** cloud push desired config; edge aplica
- **Telemetry push:** edge envia agregados + alertas
- **Digital twin sync:** estado edge reflectido na cloud (ver matéria extra)
- **Conflict resolution:** edge authoritative para controlo local; cloud para policy

### 8.1 Offline-first

Edge deve operar **autonomamente** horas/dias sem cloud:

- Regras locais em SQLite
- Buffer telemetria em disco
- UI local (HMI) para operador fábrica

---

## 9. Casos de estudo

### 9.1 Fábrica — predictive maintenance

```
Sensores vibração → FFT no IPC edge → score anomalia
  → se score > threshold: parar máquina LOCAL (< 10 ms)
  → enviar features hourly para cloud ML retraining
```

### 9.2 Smart building

```
Câmaras → edge NVR com detecção presença
  → HVAC ajuste local
  → cloud recebe ocupação agregada por zona (não vídeo)
```

### 9.3 Agricultura

```
Estação sol edge agrega 50 sensores LoRa
  → decisão rega local baseada em previsão + humidade
  → sync config de quotas water com cloud 1×/dia
```

---

## 10. Desafios do edge

| Desafio | Mitigação |
|---------|-----------|
| Hardware heterogéneo | Containers, abstrações (Docker) |
| Gestão remota | OTA, IoT Device Management |
| Segurança física | TPM, secure boot (módulo 08) |
| Observabilidade | Agentes métricas locais + sync |
| Actualização modelos ML | Versionamento + rollback OTA |

---

## Exercícios

### Exercício 1
Define edge computing e fog computing com um exemplo cada.

### Exercício 2
Para sistema de travagem de emergência em AGV (Automated Guided Vehicle), onde processas o sinal de obstacle detection? Justifica latência.

### Exercício 3
Uma câmara gera 1 GB/h. Que processamento edge reduz para 10 MB/h mantendo detecção de intrusão?

### Exercício 4
Compara Node-RED num Raspberry Pi vs. AWS Greengrass para gateway domótico com 30 dispositivos.

### Exercício 5
Lista cinco dados que **não** deveriam sair do edge por GDPR/privacidade.

### Exercício 6
Desenha arquitectura híbrida: edge faz agregação 1 min; cloud faz ML diário. Indica fluxos.

### Exercício 7
Internet falha 8 horas. Que funcionalidades edge **devem** continuar numa smart factory?

### Exercício 8
Calcula bandwidth: 1000 sensores × 500 bytes × 1 msg/s cloud-only vs. edge agrega 1 msg/min de 2 KB por gateway (10 gateways).

---

## Soluções

### Solução 1

**Edge computing:** processamento na proximidade imediata dos dispositivos IoT. Exemplo: ESP32-CAM corre TinyML para detecção movimento sem enviar vídeo.

**Fog computing:** camada intermédia entre dispositivos e cloud, tipicamente na infraestrutura de rede local. Exemplo: servidor na fábrica corre agregação e regras SCADA para toda a linha de produção.

### Solução 2

**No próprio AGV (edge device)** — sensores LiDAR/câmara → MCU/SoC embebido → travagem.

Latência máxima tolerável: **< 50 ms** (often < 20 ms). Cloud round-trip 200 ms+ causa colisão. Controlo safety-critical nunca depende de WAN.

### Solução 3

1. **Detecção movimento** (background subtraction) — descartar frames estáticos
2. **Object detection** (MobileNet) — só frames com movimento
3. **Enviar clip/evento** 10 s @ 720p reduzido ou snapshot + bbox JSON
4. Opcional: gravar localmente NVR; cloud recebe alerta metadata only

De 1 GB/h vídeo bruto → eventos + thumbnails ≈ 10 MB/h.

### Solução 4

| | Node-RED | Greengrass |
|---|----------|------------|
| Complexidade | Baixa, visual | Média-alta |
| Custo | Grátis (hardware only) | AWS fees + hardware |
| Offline | Sim (flows locais) | Sim (Lambda local) |
| Integração cloud | Manual MQTT/REST | Nativa AWS IoT |
| Escala 30 devices | Excelente | Overkill unless AWS stack |

**Domótica 30 devices:** Node-RED suficiente e simples. Greengrass se ecossistema AWS enterprise.

### Solução 5

1. Streams de vídeo com rostos identificáveis
2. Gravações áudio em casa
3. Dados biométricos wearables (ECG, SpO2 raw)
4. Localização GPS contínua interior detalhada
5. Conversas captadas por assistentes vocais

Enviar apenas agregados anonimizados ou eventos.

### Solução 6

```
[Sensors] → [Edge Gateway]
              │ agregação 1 min (avg, max, count)
              │ detecção anomalia local instant
              ▼
         [Cloud Storage]
              │ batch diário
              ▼
         [ML Training Job]
              │ novo modelo
              ▼
         [OTA deploy] → Edge Gateway (inferência actualizada)
```

Fluxos: telemetria agregada uplink; modelos downlink; alertas críticos uplink imediato.

### Solução 7

**Devem continuar:**
1. Controlo máquinas safety (paragens emergência)
2. Loop PID temperatura/pressão linha produção
3. Registo local auditoria (compliance)
4. HMI operadores — visualização e override manual
5. Detecção anomalia vibração com paragem automática
6. Buffer telemetria para sync posterior

**Podem pausar:** dashboards cloud, relatórios BI, sync multi-fábrica.

### Solução 8

**Cloud-only:**
1000 × 500 B × 1/s = 500 000 B/s ≈ **488 KB/s** ≈ **42 GB/dia**

**Edge com 10 gateways:**
Cada gateway agrega 100 sensores → 1 msg/min × 2 KB = 2 KB/min/gateway
10 × 2 KB/min = 20 KB/min ≈ **0.33 KB/s** ≈ **29 MB/dia**

Redução ~99.9% bandwidth.

---

## Referências

- Perry Lea — *IoT and Edge Computing for Architects*
- [AWS IoT Greengrass](https://docs.aws.amazon.com/greengrass/)
- [Azure IoT Edge](https://learn.microsoft.com/azure/iot-edge/)
- [ROADMAP da UC](../ROADMAP.md)
