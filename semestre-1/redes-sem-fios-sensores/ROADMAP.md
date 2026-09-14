# Roadmap — Redes Sem Fios e de Sensores

**UC:** 14741087 · **ECTS:** 6 · **Docente:** Rui Paulo · **Ano:** 2026/27  
**Pré-requisitos recomendados:** Redes de Computadores, Programação

> **Guia principal:** segue o [PLANO-SEMANAL.md](./PLANO-SEMANAL.md) do professor — 14 semanas, formato seminário, leitura prévia + discussão + PL em bancada.

---

## Como estudar nesta UC

```
Leitura prévia (D&P / Goldsmith / RFC)
        ↓
Módulo teórico (modulos/*.md) + exercícios
        ↓
PL semanal (Wireshark, Python, Cooja)
        ↓
Mini-projeto (semanas 6–14, cenário agrícola Algarve)
```

| Documento | Função |
|-----------|--------|
| [PLANO-SEMANAL.md](./PLANO-SEMANAL.md) | Calendário real das aulas (T + PL) |
| [cenario-ancora-agricola.md](./cenario-ancora-agricola.md) | Cenário para PLs e mini-projeto |
| `modulos/` | Teoria aprofundada + exercícios com soluções |
| [materia-extra.md](./materia-extra.md) | Wi-Fi 6/7, Matter, IoT satélite |

---

## Formato das aulas (turma seminário)

| Tipo | Formato |
|------|---------|
| **Teórica** | *Flipped* ligeiro: lês D&P/G antes; aula = discussão guiada |
| **PL** | Guião curto, execução individual/par, docente circula |
| **2.ª metade** | Mini-projeto como espinha dorsal |

**Horários:** Seg. 18:00–20:00 (T+PL contíguos) · Ter. 16:00–18:00 (T+PL)

---

## Percurso alinhado com as 14 semanas

| Sem. | Ponto FUC | Foco | Módulo(s) | PL |
|------|-----------|------|-----------|-----|
| 1 | Enquadramento | WSN/IoT vs. cabladas | [01](./modulos/01-enquadramento-aplicacoes.md) | Setup Wireshark, Python, Cooja |
| 2 | Fundamentos | Propagação, SNR | [02 §1–3](./modulos/02-fundamentos-comunicacao-sem-fios.md) | Link budget Python |
| 3 | Fundamentos | Interferência, métricas | [02 §4–6](./modulos/02-fundamentos-comunicacao-sem-fios.md) | RSSI Wi-Fi real |
| 4 | Acesso | ALOHA, CSMA/CA, TDMA | [03 §1–3](./modulos/03-acesso-meio-qos-energia-seguranca.md) | Wireshark 802.11 |
| 5 | Acesso | QoS, energia, S-MAC | [03 §4–6](./modulos/03-acesso-meio-qos-energia-seguranca.md) | CSMA vs. TDMA |
| 6 | Tecnologias | Wi-Fi vs. BLE | [04 §1–2](./modulos/04-wlan-wpan-wifi-ble-zigbee.md) | BLE + **início mini-projeto** |
| 7 | Tecnologias | 802.15.4, LPWAN | [04 §3](./modulos/04-wlan-wpan-wifi-ble-zigbee.md), [05](./modulos/05-celular-lpwan.md) | Airtime LoRa |
| 8 | WSN | Topologias, nós | [06 §1–3](./modulos/06-redes-sensores-topologias-roteamento.md) | Cooja multi-hop + **proposta** |
| 9 | WSN | Agregação, sync | [06 §4–5](./modulos/06-redes-sensores-topologias-roteamento.md) | Cooja agregação |
| 10 | WSN | Routing, energia | [06 §6–7](./modulos/06-redes-sensores-topologias-roteamento.md) | Cooja RPL/DODAG |
| 11 | IoT | 6LoWPAN, RPL | [07 §1–3](./modulos/07-protocolos-iot-6lowpan-rpl-coap-mqtt.md) | Wireshark 6LoWPAN |
| 12 | IoT | CoAP vs. MQTT | [07 §4–6](./modulos/07-protocolos-iot-6lowpan-rpl-coap-mqtt.md) | Dissecção protocolos |
| 13 | Planeamento | Comparação, artigo | [08](./modulos/08-planeamento-simulacao-mini-projeto.md) | Trabalho mini-projeto |
| 14 | Síntese | Revisão teste | Revisão global | **Apresentação projeto** |

---

## Mini-projeto (35% da nota)

Cenário: [monitorização agrícola no Algarve](./cenario-ancora-agricola.md)

| Marco | Semana |
|-------|--------|
| Lançamento | 6 |
| Proposta | 8 |
| Acompanhamento | 9–13 |
| Entrega + apresentação | 14 |

Detalhes: [módulo 08 — Mini-projeto](./modulos/08-planeamento-simulacao-mini-projeto.md)

---

## Avaliação

| Componente | Peso |
|------------|------|
| Prova escrita (teste/exame) | **50%** |
| Mini-projeto | **35%** |
| Guiões PL (sem. 2, 5, 9, 10) | **15%** |

- Aprovação: nota final ≥ **9,50**
- Mínimo na prática para admissão ao exame

---

## Bibliografia (plano do docente)

| Sigla | Referência |
|-------|------------|
| **D&P** | Dargie & Poellabauer — *Fundamentals of Wireless Sensor Networks* |
| **G** | Goldsmith — *Wireless Communications* |
| **Normas** | IEEE 802.11, 802.15.4; RFC 6282, 6550, 7252 |

---

## Fronteira RSFS ↔ IoT

| RSFS (14741087) | IoT (14741088) |
|-----------------|----------------|
| Rede até ao **gateway** | Clientes, brokers, JSON, edge, cloud |
| Análise de protocolos | Implementação full-stack |

---

## Ferramentas

| Ferramenta | Semanas |
|------------|---------|
| Wireshark | 1, 4, 11, 12 |
| Python (link budget) | 2, 3 |
| Cooja / Contiki-NG | 8, 9, 10 + projeto |
| Calculadora LoRa | 7 |

---

## Ligações úteis

- [Contiki-NG](https://github.com/contiki-ng/contiki-ng)
- [RFC 6550 — RPL](https://datatracker.ietf.org/doc/html/rfc6550)
- [RFC 7252 — CoAP](https://datatracker.ietf.org/doc/html/rfc7252)
- [LoRa Alliance](https://lora-alliance.org/)
