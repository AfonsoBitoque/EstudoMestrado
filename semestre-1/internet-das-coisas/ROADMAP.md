# Roadmap — Internet das Coisas (IoT)

**UC:** 14741088 · **ECTS:** 6 · **Língua:** Inglês  
**Pré-requisitos recomendados:** Redes de Computadores  
**Bibliografia de referência:** Andy King — *Programming the Internet of Things*; Perry Lea — *IoT and Edge Computing for Architects*

## Objetivos de aprendizagem (resumo)

1. Projetar e construir solução IoT **full-stack** (dispositivo → nuvem)
2. Enfrentar desafios de integração na implementação
3. Conhecer protocolos para dispositivos com recursos limitados, gateways e serviços
4. Criar dados em JSON utilizáveis em várias plataformas
5. Utilizar serviços na nuvem para valor comercial

## Percurso de estudo (10 etapas alinhadas com avaliação prática)

### Part I — Introdução e arquitetura (Semanas 1–3)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 1 | [01-fundamentos-iot-arquitetura](./modulos/01-fundamentos-iot-arquitetura.md) | Part I — conceitos e arquitetura | 5–7 h |
| 2 | [02-ferramentas-desenvolvimento-monitorizacao](./modulos/02-ferramentas-desenvolvimento-monitorizacao.md) | Part I — ferramentas e performance | 4–6 h |

**Checkpoint:** Desenhar arquitetura em 3 camadas (edge, gateway, cloud) para cenário domótico.

### Part II — Estratégias de dados (Semanas 4–6)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 3 | [03-simulacao-emulacao-dados](./modulos/03-simulacao-emulacao-dados.md) | Part II — simulação e emulação | 5–7 h |
| 4 | [04-integracao-dados-json](./modulos/04-integracao-dados-json.md) | Part II — integração de dados | 5–7 h |

**Checkpoint:** Publicar telemetria simulada em JSON via API REST ou broker MQTT.

### Part III — Conectividade e edge (Semanas 7–10)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 5 | [05-protocolos-transferencia-mqtt](./modulos/05-protocolos-transferencia-mqtt.md) | Part III — MQTT | 6–8 h |
| 6 | [06-protocolo-coap](./modulos/06-protocolo-coap.md) | Part III — CoAP | 4–6 h |
| 7 | [07-edge-computing](./modulos/07-edge-computing.md) | Part III — Edge | 5–7 h |
| 8 | [08-seguranca-iot](./modulos/08-seguranca-iot.md) | Part III — Segurança | 5–7 h |
| — | [materia-extra.md](./materia-extra.md) | Complementar | Contínuo |

**Checkpoint final:** Pipeline completo sensor → MQTT → processamento edge/cloud → dashboard.

## Avaliação (referência)

- **10 etapas** de implementação em sala, peso igual cada uma
- Sem exame na época — conclusão obrigatória de todas as etapas
- **IA generativa não permitida** nesta UC

## Stack sugerida para prática

| Camada | Tecnologias |
|--------|-------------|
| Dispositivo | ESP32/Arduino, Python (simulação) |
| Protocolos | MQTT (Mosquitto), CoAP (aiocoap) |
| Edge | Node-RED, Docker |
| Cloud | AWS IoT Core, Azure IoT Hub, ou HiveMQ Cloud (free tier) |
| Dados | JSON, InfluxDB/TimescaleDB |

## Ligações úteis

- [MQTT Specification](https://mqtt.org/)
- [CoAP RFC 7252](https://datatracker.ietf.org/doc/html/rfc7252)
- [Eclipse Mosquitto](https://mosquitto.org/)
