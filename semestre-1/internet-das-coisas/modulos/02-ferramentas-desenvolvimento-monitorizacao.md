# Módulo 02 — Ferramentas de Desenvolvimento e Monitorização

**UC:** Internet das Coisas · **Parte I** · Tempo sugerido: 4–6 h

---

## Objetivos de aprendizagem

- Conhecer ferramentas essenciais para desenvolvimento IoT (IDE, flash, debug, serial)
- Aplicar estratégias de teste (unitário, integração, hardware-in-the-loop)
- Configurar monitorização de performance e observabilidade em pipelines IoT
- Interpretar métricas, logs e traces para diagnosticar falhas

---

## 1. Ferramentas de desenvolvimento IoT

### 1.1 Ambientes de desenvolvimento (IDE)

| Ferramenta | Plataforma | Uso |
|------------|------------|-----|
| **PlatformIO** | VS Code | Multi-plataforma (ESP32, Arduino, STM32); gestão de dependências |
| **Arduino IDE 2** | Desktop | Rápido para prototipagem; biblioteca vasta |
| **ESP-IDF** | CLI / VS Code | Framework oficial Espressif; controlo total |
| **Thonny** | Desktop | MicroPython em Raspberry Pi Pico / ESP32 |
| **Node-RED** | Browser | Flow-based para gateway e integração |

### 1.2 Programação e flash

- **esptool.py:** gravar firmware em ESP8266/ESP32 via USB-UART
- **OpenOCD / ST-Link:** debug e flash em STM32
- **OTA (Over-The-Air):** actualizar firmware sem cabo — ver módulo extra

**Fluxo típico ESP32:**
```bash
pio run -t upload          # compilar e gravar
pio device monitor -b 115200  # consola serial
```

### 1.3 Debug e consola serial

A **consola serial** (UART, 115200 baud) é a primeira linha de debug em IoT:

```cpp
Serial.printf("[SENSOR] temp=%.1f°C hum=%.1f%%\n", temp, hum);
```

**Ferramentas:** `pio device monitor`, `minicom`, `screen`, Serial Monitor do Arduino IDE.

**Limitações:** impacto em timing real-time; em produção substituir por logs estruturados.

### 1.4 Simuladores e emuladores

- **Wokwi:** simula ESP32/Arduino no browser
- **QEMU:** emulação de CPUs (limitada para periféricos)
- **Docker:** isolar serviços gateway/cloud em dev

### 1.5 Gestão de versões e CI/CD

- **Git** para firmware e infra cloud
- **GitHub Actions / GitLab CI:** build automático, testes, artefactos OTA
- **Semantic versioning** para firmware: `v1.2.3`

---

## 2. Testes em sistemas IoT

### 2.1 Pirâmide de testes adaptada à IoT

```
        ┌─────────────┐
        │  E2E / HIL  │  Poucos — caros, lentos
        ├─────────────┤
        │ Integração  │  MQTT, API, gateway
        ├─────────────┤
        │  Unitários  │  Parsing JSON, lógica, drivers mock
        └─────────────┘
```

### 2.2 Testes unitários

Testam funções isoladas **sem hardware**.

**Exemplo (Python — parsing telemetria):**
```python
def parse_payload(raw: bytes) -> dict:
    return json.loads(raw.decode())

def test_parse_valid():
    assert parse_payload(b'{"temp":22.5}')["temp"] == 22.5
```

**Em C/C++ (Unity, Google Test):** testar conversão ADC→°C, máquinas de estado.

### 2.3 Testes de integração

Validam comunicação entre componentes **com serviços reais ou containers**.

- Publicar em broker MQTT de teste (Mosquitto Docker)
- Mock de API REST com `responses` (Python) ou WireMock
- Verificar que gateway transforma Zigbee → JSON correctamente

### 2.4 Hardware-in-the-Loop (HIL)

Hardware real executa firmware enquanto **ambiente simulado** injecta entradas.

- Sensor físico em câmara climática controlada
- Fonte programável simula bateria
- Útil para validar comportamento antes de deploy em campo

### 2.5 Testes de carga e stress

Simular **N dispositivos** publicando telemetria:

- **MQTT load tools:** `mqtt-stresser`, `emqtt_bench`
- Medir: mensagens/s, latência p99, perda de pacotes
- Identificar gargalos no broker ou na ingestão cloud

---

## 3. Monitorização de performance

### 3.1 Métricas-chave em IoT

| Métrica | Descrição | Onde medir |
|---------|-----------|------------|
| **Latência end-to-end** | Sensor → dashboard | Timestamps em cada hop |
| **Throughput** | msg/s ou bytes/s | Broker, API gateway |
| **Uptime dispositivo** | % tempo online | Heartbeat MQTT |
| **Packet loss** | Mensagens não entregues | QoS MQTT, logs broker |
| **CPU/RAM dispositivo** | Recursos embebidos | `esp_get_free_heap_size()` |
| **Consumo energético** | mAh/dia | Multímetro ou PMIC |

### 3.2 Heartbeat e last will

Dispositivos publicam periodicamente em `device/{id}/heartbeat`:

```json
{"ts": "2026-09-14T10:00:00Z", "uptime_s": 86400, "rssi": -67}
```

Ausência de heartbeat → alerta de dispositivo offline.

### 3.3 Benchmarking de rede

- **Ping / RTT** até broker
- **Tamanho de payload:** JSON compacto vs. verbose
- **Frequência de publish:** trade-off bateria vs. granularidade

---

## 4. Observabilidade

Observabilidade = capacidade de inferir estado interno a partir de **logs, métricas e traces**.

### 4.1 Logs estruturados

Preferir JSON em produção:

```json
{"level":"info","device":"esp32-01","event":"publish","topic":"farm/temp","latency_ms":45}
```

**Ferramentas:** Loki, Elasticsearch, CloudWatch Logs.

### 4.2 Métricas (time-series)

- **Prometheus** + **Grafana:** padrão de facto
- Exportadores: Mosquitto `$SYS` topics, Node Exporter, custom `/metrics`

**Exemplo Grafana:** painel com taxa de mensagens MQTT, dispositivos activos, latência p95.

### 4.3 Tracing distribuído

**OpenTelemetry** propaga `trace_id` desde dispositivo (se possível) ou gateway até cloud.

Útil para: "Esta leitura demorou 3 s — onde?" → gateway 50 ms, broker 20 ms, Lambda 2.8 s.

### 4.4 Alertas

Regras em Prometheus Alertmanager ou cloud:

- `heartbeat_missing > 5 min`
- `mqtt_messages_rate drop > 50%`
- `gateway_disk_usage > 90%`

---

## 5. Ferramentas práticas recomendadas

| Categoria | Ferramenta | Notas |
|-----------|------------|-------|
| Broker local | Eclipse Mosquitto (Docker) | `$SYS/#` para métricas |
| Flow gateway | Node-RED | Debug nodes, inject |
| Métricas | Prometheus + Grafana | Stack clássica |
| MQTT client test | MQTT Explorer, mosquitto_pub/sub | Debug manual |
| API test | curl, Postman, httpie | REST endpoints |
| Load test | emqtt_bench | Stress broker |

---

## 6. Boas práticas

1. **Separar ambientes:** dev / staging / prod com brokers e credenciais distintos
2. **Versionar tudo:** firmware, configs Node-RED, docker-compose
3. **Nunca debug serial em produção** — usar logs remotos com níveis (DEBUG/INFO/ERROR)
4. **Definir SLOs:** ex. 99% mensagens entregues em < 5 s
5. **Dashboard desde o dia 1** — não adicionar observabilidade só quando algo falha

---

## Exercícios

### Exercício 1
Lista cinco ferramentas que usarias para desenvolver firmware num ESP32 e descreve uma tarefa concreta para cada uma.

### Exercício 2
Escreve um teste unitário (Python ou pseudocódigo) que valida se um payload de telemetria contém campos obrigatórios: `device_id`, `timestamp`, `value`.

### Exercício 3
Desenha um pipeline de CI/CD para firmware ESP32: commit → build → testes → artefacto binário. Que gates de qualidade incluirias?

### Exercício 4
Um dashboard mostra 200 dispositivos "online" mas nenhum dado novo há 2 horas. Lista quatro hipóteses e que logs/métricas consultarias para cada uma.

### Exercício 5
Compara logs textuais (`TEMP: 22.5`) vs. logs JSON estruturados para um sistema com 10 000 dispositivos. Vantagens e desvantagens.

### Exercício 6
Define três alertas Prometheus para um broker Mosquitto em produção, com condição e severidade.

### Exercício 7
Explica como medir latência end-to-end num pipeline sensor → MQTT → InfluxDB → Grafana. Onde colocarias timestamps?

### Exercício 8
Propõe uma estratégia de teste (unitário, integração, HIL) para validar que um relé só activa quando temperatura > 30°C **e** utilizador autorizou via app.

---

## Soluções

### Solução 1

| Ferramenta | Tarefa |
|------------|--------|
| PlatformIO | Compilar projecto multi-ficheiro com dependências (`lib_deps`) |
| esptool.py | Gravar firmware `.bin` na flash do ESP32 |
| Serial Monitor | Ver output de boot e debug UART |
| Logic Analyzer (PulseView) | Verificar timing I2C/SPI com sensor BME280 |
| Git | Versionar código e tags de release (`v1.0.0`) |

### Solução 2

```python
import json

REQUIRED = {"device_id", "timestamp", "value"}

def validate_payload(raw: str) -> bool:
    data = json.loads(raw)
    return REQUIRED.issubset(data.keys())

def test_valid():
    assert validate_payload('{"device_id":"d1","timestamp":"2026-01-01T00:00:00Z","value":22.5}')

def test_missing_value():
    assert not validate_payload('{"device_id":"d1","timestamp":"2026-01-01T00:00:00Z"}')

def test_invalid_json():
    try:
        validate_payload('not json')
        assert False
    except json.JSONDecodeError:
        pass
```

### Solução 3

```
git push → GitHub Actions:
  1. Checkout
  2. Setup PlatformIO
  3. pio run (build) — GATE: zero erros compilação
  4. pio test (unitários host) — GATE: 100% pass
  5. Lint (clang-tidy) — GATE: zero warnings críticos
  6. Upload firmware.bin como artefacto
  7. (Opcional) Deploy OTA staging com aprovação manual
```

Gates: build OK, testes passam, tamanho flash < partição, semver tag presente em release.

### Solução 4

| Hipótese | Evidência a consultar |
|----------|----------------------|
| Dispositivos publicam mas broker não recebe | Logs broker, `$SYS/broker/messages/received` |
| Broker recebe mas consumer cloud parado | Logs Lambda/consumer, lag Kafka |
| Heartbeat OK mas sensor avariado | Payload telemetria — só heartbeat, sem dados sensor |
| Relógio/dispositivos stuck (watchdog não reiniciou) | `uptime_s` constante nos heartbeats |
| Tópico ou ACL MQTT incorrectos pós-deploy | Logs auth Mosquitto, `mosquitto_sub -t '#' -v` |

### Solução 5

**Textuais:** legíveis humanamente; difíceis de parsear automaticamente; regex frágil; sem campos padronizados.

**JSON estruturado:** parse automático; filtros no Loki/Elasticsearch (`device_id="x"`); correlação; indexing eficiente.

**Desvantagem JSON:** maior overhead bytes em dispositivos muito constrained — compromisso: JSON compacto ou CBOR no wire, JSON no gateway.

### Solução 6

1. **BrokerDown** — `up{job="mosquitto"} == 0` for 1 min → **critical**
2. **HighConnectionCount** — `mosquitto_clients_connected > 5000` for 5 min → **warning** (possível ataque ou flash crowd)
3. **MessageRateDrop** — `rate(mosquitto_messages_received[5m]) < 0.5 * avg_over_time(...[1d])` → **warning**

### Solução 7

| Ponto | Timestamp |
|-------|-----------|
| ESP32 após leitura sensor | `t0` em payload `sensor_ts` |
| Gateway ao receber | `t1_ingress` header/metadata |
| Broker ao persistir (QoS1) | `t2_broker` (log broker) |
| Consumer ao escrever InfluxDB | `t3_write` |
| Query Grafana | `t4_display` (now) |

**Latência E2E** ≈ `t3_write - t0`. Usar NTP sync nos dispositivos para precisão absoluta.

### Solução 8

| Nível | O quê |
|-------|-------|
| **Unitário** | Função `should_activate(temp, authorized)` com casos limite (29.9, 30.0, 30.1) |
| **Integração** | Mock MQTT: publicar temp 31°C + flag auth true → verificar mensagem no tópico `relay/command` |
| **HIL** | ESP32 real com sensor simulado (fonte resistiva) e relé com LED; app staging envia auth; medir tempo de resposta |

Teste negativo em cada nível: temp alta sem auth → relé permanece OFF.

---

## Referências

- Andy King — *Programming the Internet of Things* (Ch. ferramentas e testes)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [PlatformIO Docs](https://docs.platformio.org/)
- [ROADMAP da UC](../ROADMAP.md)
