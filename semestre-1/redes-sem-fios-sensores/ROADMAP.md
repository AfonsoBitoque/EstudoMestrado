# Roadmap — Redes Sem Fios e de Sensores

**UC:** 14741087 · **ECTS:** 6 · **Língua:** EN ou PT  
**Pré-requisitos recomendados:** Redes de Computadores, Programação

## Objetivos de aprendizagem (resumo)

1. Explicar princípios de redes sem fios e sensores (propagação, MAC, interferência, mobilidade)
2. Comparar Wi-Fi, Bluetooth/BLE, IEEE 802.15.4, ZigBee, celular, LPWAN
3. Analisar arquiteturas de redes de sensores e IoT
4. Avaliar trade-offs: energia, escalabilidade, QoS, fiabilidade, segurança
5. Interpretar artigos, normas e documentação técnica
6. Propor soluções com simulação ou estudo de casos

## Percurso de estudo (8–10 semanas)

### Fase 1 — Fundamentos (Semanas 1–2)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 1 | [01-enquadramento-aplicacoes](./modulos/01-enquadramento-aplicacoes.md) | Enquadramento IoT/WSN | 3–5 h |
| 2 | [02-fundamentos-comunicacao-sem-fios](./modulos/02-fundamentos-comunicacao-sem-fios.md) | Propagação, métricas | 6–8 h |
| 3 | [03-acesso-meio-qos-energia-seguranca](./modulos/03-acesso-meio-qos-energia-seguranca.md) | MAC, QoS, energia | 5–7 h |

**Checkpoint:** Calcular path loss e SNR para cenário indoor; comparar CSMA/CA vs TDMA.

### Fase 2 — Tecnologias (Semanas 3–5)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 4 | [04-wlan-wpan-wifi-ble-zigbee](./modulos/04-wlan-wpan-wifi-ble-zigbee.md) | WLAN, WPAN, 802.15.4 | 6–8 h |
| 5 | [05-celular-lpwan](./modulos/05-celular-lpwan.md) | Celular, LoRaWAN, NB-IoT | 5–7 h |

**Checkpoint:** Tabela comparativa de 4 tecnologias para smart agriculture.

### Fase 3 — Redes de sensores e protocolos IoT (Semanas 6–8)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 6 | [06-redes-sensores-topologias-roteamento](./modulos/06-redes-sensores-topologias-roteamento.md) | WSN | 6–8 h |
| 7 | [07-protocolos-iot-6lowpan-rpl-coap-mqtt](./modulos/07-protocolos-iot-6lowpan-rpl-coap-mqtt.md) | Protocolos restritos | 6–8 h |

### Fase 4 — Projeto e avaliação (Semanas 9–10)

| Ordem | Módulo | Conteúdo FUC | Tempo sugerido |
|-------|--------|--------------|----------------|
| 8 | [08-planeamento-simulacao-mini-projeto](./modulos/08-planeamento-simulacao-mini-projeto.md) | Simulação, casos | 6–10 h |
| — | [materia-extra.md](./materia-extra.md) | Complementar | Contínuo |

**Checkpoint final:** Mini-projeto com simulação (Cooja/NS-3/OMNeT++) ou estudo de caso fundamentado.

## Avaliação (referência)

- **50%** — Componente escrita (teste/exame)
- **50%** — Componente prática (mini-projeto, simulação, etc.)
- Mínimo **7** na prática para admissão ao exame
- Aprovação com ≥ **9,5**

## Ferramentas de simulação

| Ferramenta | Uso |
|------------|-----|
| Cooja (Contiki) | 802.15.4, RPL |
| NS-3 | Wi-Fi, LTE, LoRa |
| OMNeT++ / INET | Redes genéricas |
| Wireshark | Análise de tráfego |

## Ligações úteis

- [IEEE 802.15.4](https://standards.ieee.org/standard/802_15_4-2020.html)
- [LoRa Alliance](https://lora-alliance.org/)
- [IETF RPL RFC 6550](https://datatracker.ietf.org/doc/html/rfc6550)
