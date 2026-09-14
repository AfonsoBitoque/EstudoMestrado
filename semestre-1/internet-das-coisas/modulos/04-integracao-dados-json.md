# Módulo 04 — Integração de Dados e JSON

**UC:** Internet das Coisas · **Parte II** · Tempo sugerido: 5–7 h

---

## Objetivos de aprendizagem

- Definir schemas JSON para telemetria IoT interoperável
- Consumir e expor APIs REST para integração multi-plataforma
- Construir pipelines de dados dispositivo → armazenamento → visualização
- Aplicar boas práticas de versionamento, validação e interoperabilidade

---

## 1. JSON na IoT

**JSON (JavaScript Object Notation)** é o formato de intercâmbio dominante em IoT cloud por ser:

- Legível por humanos
- Suportado universalmente (Python, JS, C com cJSON, ArduinoJson)
- Extensível sem schema rígido (trade-off: validação necessária)

**Alternativas:** CBOR (binário compacto), Protocol Buffers, MessagePack — comuns em dispositivos muito constrained ou alta throughput.

---

## 2. Schemas JSON

### 2.1 Estrutura típica de telemetria

```json
{
  "device_id": "esp32-greenhouse-01",
  "timestamp": "2026-09-14T10:30:00.000Z",
  "schema_version": "1.0",
  "readings": {
    "temperature_c": 24.3,
    "humidity_pct": 62.1
  },
  "metadata": {
    "firmware": "2.1.0",
    "rssi": -72
  }
}
```

### 2.2 Campos recomendados

| Campo | Obrigatório? | Descrição |
|-------|--------------|-----------|
| `device_id` | Sim | Identificador único estável |
| `timestamp` | Sim | ISO 8601 UTC |
| `schema_version` | Recomendado | Evolução sem breaking changes |
| Payload de dados | Sim | Leituras ou evento |
| `metadata` | Opcional | Contexto diagnóstico |

### 2.3 JSON Schema para validação

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["device_id", "timestamp", "readings"],
  "properties": {
    "device_id": { "type": "string", "minLength": 1 },
    "timestamp": { "type": "string", "format": "date-time" },
    "schema_version": { "type": "string" },
    "readings": {
      "type": "object",
      "properties": {
        "temperature_c": { "type": "number", "minimum": -40, "maximum": 85 }
      }
    }
  }
}
```

Validar no **gateway ou cloud** — dispositivos constrained podem omitir validação local.

### 2.4 Versionamento de schema

- **Minor (1.0 → 1.1):** campos novos opcionais — retrocompatível
- **Major (1.x → 2.0):** remover/renomear campos — consumers devem migrar

Publicar changelog; suportar N e N-1 em paralelo durante transição.

---

## 3. REST APIs

### 3.1 Princípios REST aplicados à IoT

| Método | Recurso exemplo | Uso |
|--------|-----------------|-----|
| GET | `/devices/{id}/telemetry?from=&to=` | Consultar histórico |
| POST | `/devices/{id}/telemetry` | Ingestão (alternativa a MQTT) |
| GET | `/devices/{id}` | Metadados dispositivo |
| PATCH | `/devices/{id}/config` | Actualizar config remota |
| POST | `/devices/{id}/commands` | Enviar comando (ligar actuador) |

### 3.2 Códigos HTTP

| Código | Significado IoT |
|--------|-----------------|
| 200/201 | Sucesso ingestão ou leitura |
| 400 | JSON inválido ou schema fail |
| 401/403 | Token inválido ou dispositivo não autorizado |
| 404 | Dispositivo desconhecido |
| 429 | Rate limit — dispositivo demasiado frequente |
| 503 | Serviço indisponível — dispositivo deve bufferizar |

### 3.3 Autenticação

- **API Key** no header `X-API-Key` — simples; rotação manual
- **JWT Bearer** — expiração, scopes (`telemetry:write`)
- **Mutual TLS (mTLS)** — certificado por dispositivo — gold standard industrial

### 3.4 Exemplo ingestão

```http
POST /api/v1/telemetry HTTP/1.1
Host: iot.example.com
Authorization: Bearer eyJhbG...
Content-Type: application/json

{"device_id":"d1","timestamp":"2026-09-14T10:00:00Z","readings":{"temp":22.5}}
```

Resposta:
```http
HTTP/1.1 201 Created
Location: /api/v1/telemetry/abc123
```

---

## 4. Pipelines de dados

### 4.1 Arquitectura pipeline clássica

```
Dispositivo → (MQTT/HTTP) → Ingest → Stream/Queue → Process → Store → Visualize
                                ↓
                           Validation
                                ↓
                           Enrichment (geo, device registry)
```

### 4.2 Componentes

| Etapa | Tecnologias | Função |
|-------|-------------|--------|
| Ingest | AWS IoT Rules, Azure IoT Hub, Node-RED | Receber dados brutos |
| Validate | JSON Schema, Lambda | Rejeitar lixo |
| Enrich | Join com registry | Adicionar `site`, `owner` |
| Process | Kafka Streams, Flink | Agregações, janelas |
| Store | InfluxDB, TimescaleDB, S3 | Time-series ou data lake |
| Visualize | Grafana, Power BI | Dashboards |

### 4.3 MQTT + JSON vs. REST

| Aspecto | MQTT + JSON | REST |
|---------|-------------|------|
| Padrão | Push pub/sub | Request/response |
| Escala fan-out | Excelente | Polling ineficiente |
| Fire-and-forget | Sim (QoS 0) | POST idempotente necessário |
| Dispositivos constrained | MQTT preferido | HTTP possível |

Muitos sistemas usam **MQTT device-to-cloud** e **REST cloud-to-app**.

### 4.4 Idempotência

Dispositivos reenviam em falha de rede. Usar **`message_id` UUID** ou `(device_id, timestamp, sequence)` para deduplicar no consumer.

---

## 5. Interoperabilidade

### 5.1 Padrões sectoriais

| Padrão | Domínio | Notas |
|--------|---------|-------|
| **WoT Thing Description** | W3C Web of Things | JSON-LD descreve capacidades |
| **Sparkplug B** | Industria MQTT | Payload protobuf sobre MQTT |
| **LWM2M** | Dispositivos celulares | Objetos normalizados |
| **Digital Twin Definition Language (DTDL)** | Azure | Modelo digital gémeo |

### 5.2 Normalização multi-vendor

Gateway traduz formatos proprietários → **canonical model** interno:

```
Vendor A JSON ──┐
Vendor B CSV  ──┼──► Normalizer ──► {"metric":"temp","value":22.5,"unit":"C"}
Vendor C MQTT ──┘
```

### 5.3 Unidades e nomenclatura

- Temperatura sempre em **°C** ou **K** — documentar
- Usar SI quando possível
- Nomes de campos: `snake_case` consistente (`temperature_c` não `TempC` num sítio e `temp` noutro)

---

## 6. Boas práticas

1. **Timestamps UTC** com timezone explícito (`Z`)
2. **Limitar tamanho payload** — ESP32: manter < 1 KB se possível
3. **Validar na entrada** — garbage in, garbage out
4. **Contract-first** — acordar schema antes de implementar firmware e cloud
5. **OpenAPI/Swagger** para APIs REST documentadas
6. **Compressão** gzip em HTTP para batches grandes

---

## 7. Exemplo pipeline Node-RED → InfluxDB

```
[mqtt in] → [json validate] → [function: add tags] → [influxdb out]
```

Function node:
```javascript
msg.payload = {
    measurement: "environment",
    tags: { device_id: msg.payload.device_id },
    fields: msg.payload.readings,
    timestamp: new Date(msg.payload.timestamp)
};
return msg;
```

---

## Exercícios

### Exercício 1
Cria um schema JSON (informal ou JSON Schema) para evento de porta aberta: `device_id`, `timestamp`, `event_type`, `door_id`, `duration_s` opcional.

### Exercício 2
Desenha endpoints REST completos (método, path, body, resposta) para: (a) ingestão telemetria, (b) consulta últimas 24 h, (c) envio comando.

### Exercício 3
Um dispositivo envia `{"temp": 9999}`. Onde deves validar e que acção tomar em cada camada (device, gateway, cloud)?

### Exercício 4
Explica como garantir idempotência quando o mesmo POST é reenviado 3 vezes devido a timeout.

### Exercício 5
Compara JSON vs. CBOR para ESP32 que publica a cada 10 s em rede LoRa (50 bytes payload máx.). Quantifica trade-offs.

### Exercício 6
Propõe estratégia de migração de `schema_version` 1.0 para 2.0 quando `readings.temp` passa a `readings.temperature_c`.

### Exercício 7
Desenha pipeline que ingere MQTT e REST, normaliza para modelo canónico e escreve TimescaleDB.

### Exercício 8
Escreve exemplo curl para POST telemetria e GET consulta com filtros `from`, `to`, `device_id`.

---

## Soluções

### Solução 1

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["device_id", "timestamp", "event_type", "door_id"],
  "properties": {
    "device_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "event_type": { "type": "string", "enum": ["door_open", "door_close"] },
    "door_id": { "type": "string" },
    "duration_s": { "type": "number", "minimum": 0 }
  }
}
```

Exemplo payload:
```json
{"device_id":"hub-01","timestamp":"2026-09-14T08:00:00Z","event_type":"door_open","door_id":"front","duration_s":null}
```

### Solução 2

**(a) Ingestão**
```http
POST /api/v1/devices/{device_id}/telemetry
Body: { "timestamp": "...", "readings": {...} }
→ 201 Created { "id": "msg-uuid" }
→ 400 se schema inválido
```

**(b) Consulta 24 h**
```http
GET /api/v1/devices/{device_id}/telemetry?from=2026-09-13T10:00:00Z&to=2026-09-14T10:00:00Z
→ 200 { "data": [ {...}, ... ], "count": 1440 }
```

**(c) Comando**
```http
POST /api/v1/devices/{device_id}/commands
Body: { "command": "set_relay", "params": { "channel": 1, "state": "ON" } }
→ 202 Accepted { "command_id": "cmd-uuid", "status": "pending" }
```

### Solução 3

| Camada | Acção |
|--------|-------|
| Device | Plausibility check firmware (range -40..85°C) — **não enviar** 9999 |
| Gateway | JSON Schema validation; rejeitar ou clamp; log alerta `invalid_reading` |
| Cloud | Schema validation; descartar registo; métrica `validation_errors++`; opcional dead-letter queue para análise |

Defesa em profundidade — não confiar só na cloud.

### Solução 4

1. Cliente inclui header `Idempotency-Key: uuid-v4` ou campo `message_id` no body
2. Servidor mantém cache/DB de keys processadas (TTL 24–48 h)
3. 1.º POST → processa → 201 + armazena key
4. 2.º e 3.º POST mesma key → 200/201 com mesmo `id` resposta, **sem reprocessar**
5. Alternativa: unique constraint DB em `(device_id, sequence)`

### Solução 5

| | JSON | CBOR |
|---|------|------|
| Payload exemplo `{"t":24.3,"h":60}` | ~20 bytes | ~12 bytes |
| Parse ESP32 | ArduinoJson ~10–20 ms | tinycbor ~5 ms |
| Debug | Fácil mosquitto_sub | Binário — precisa decoder |
| LoRa 50 B | Cabe poucas leituras verbose | Mais métricas no mesmo frame |

**Recomendação LoRa:** CBOR ou formato binário custom; JSON no gateway após recepção se backhaul permitir.

### Solução 6

1. Publicar spec 2.0 com changelog
2. Gateway/cloud aceita **ambos** formatos durante janela (detector: presença de `readings.temp` vs `readings.temperature_c`)
3. Normalizer mapeia v1 → canonical v2 internamente
4. Firmware novo envia só 2.0; firmware legado continua 1.0
5. Após 90 dias ou 100% fleet upgraded, deprecar 1.0 (HTTP 400 com mensagem migrate)

### Solução 7

```
                    ┌─── MQTT subscriber ───┐
                    │                       ▼
[Devices] ──MQTT──► │              [Normalizer service]
                    │                       ▲
                    └─── REST POST ──────────┘
                                            │
                    Canonical: {device_id, ts, metrics[{name,value,unit}]}
                                            ▼
                                    [TimescaleDB hypertable]
                                    metrics(device_id, ts, name, value)
```

Normalizer: parse source, validate, map fields, insert UPSERT com idempotency key.

### Solução 8

```bash
# POST telemetria
curl -X POST https://iot.example.com/api/v1/devices/esp32-01/telemetry \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2026-09-14T10:00:00Z","readings":{"temperature_c":22.5,"humidity_pct":55}}'

# GET consulta
curl -G https://iot.example.com/api/v1/telemetry \
  -H "Authorization: Bearer TOKEN" \
  --data-urlencode "device_id=esp32-01" \
  --data-urlencode "from=2026-09-13T10:00:00Z" \
  --data-urlencode "to=2026-09-14T10:00:00Z"
```

---

## Referências

- [JSON Schema](https://json-schema.org/)
- [OpenAPI Specification](https://swagger.io/specification/)
- W3C Web of Things — Thing Description
- [ROADMAP da UC](../ROADMAP.md)
