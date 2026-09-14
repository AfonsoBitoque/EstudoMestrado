# Plano Semanal — RSFS (Prof. Rui Paulo)

Plano de aulas **2026/27** adaptado ao formato seminário (turma pequena). Usa este documento como **guia principal de estudo**, em paralelo com os módulos teóricos.

> **Nota:** Este documento resume o plano do docente. O PDF oficial **não** deve ser publicado no repositório.

## Formato das aulas

| Componente | Horário | Formato |
|------------|---------|---------|
| **T** (Teórica) | Seg. 18:00–19:00 + Ter. 16:00–17:00 | *Flipped* ligeiro: lês a secção indicada **antes**; a aula é discussão guiada (15–20 min exposição nos pontos difíceis) |
| **PL** (Prática) | Seg. 19:00–20:00 + Ter. 17:00–18:00 | Bancada acompanhada: guião curto, execução individual/par, docente circula |
| **Bloco segunda** | 18:00–20:00 | Pode ser sessão contínua de 2 h (T+PL) para simulação/projeto |

### Filosofia

- **Não esperes slides completos** — prepara-te com leitura prévia e guiões de discussão.
- **Mini-projeto = espinha dorsal** da 2.ª metade (semanas 6–14).
- **Cenário âncora:** monitorização agrícola no Algarve (usa-o em todas as PLs e no projeto).

### Fronteira com Internet das Coisas (UC 14741088)

| RSFS (esta UC) | IoT (outra UC) |
|----------------|----------------|
| Rede **até ao gateway** | Integração aplicacional |
| Análise/comparação de protocolos (overhead, energia, fiabilidade) | Clientes, brokers, JSON, edge, cloud |
| Wireshark, Cooja, link budget | Implementação full-stack |

---

## Calendário — 14 semanas

### Semana 1 — Enquadramento (Ponto FUC 1)

| | Conteúdo |
|---|----------|
| **T** | Aplicações, requisitos e desafios de redes sem fios, WSN e IoT; contraste com redes cabladas |
| **PL** | Setup: Wireshark, Python, Cooja/Contiki-NG; escolha do **cenário âncora** |
| **Leitura prévia** | Dargie & Poellabauer (D&P), cap. 1 |
| **Módulo** | [01-enquadramento-aplicacoes](./modulos/01-enquadramento-aplicacoes.md) |
| **Checkpoint** | Ambiente funcional + cenário âncora definido por escrito (1 parágrafo) |

**Preparação antes da aula:**
- [ ] Instalar Wireshark (+ permissões capture no Linux)
- [ ] Clonar [Contiki-NG](https://github.com/contiki-ng/contiki-ng) e testar Cooja
- [ ] Ler D&P cap. 1 e anotar 3 perguntas para discussão

---

### Semana 2 — Fundamentos: propagação (Ponto FUC 2)

| | Conteúdo |
|---|----------|
| **T** | Propagação, atenuação, modelos path loss (espaço livre, log-distância), ruído, SNR |
| **PL** | Link budget em **Python**: Friis, sensibilidade, margem; gráficos alcance vs. frequência |
| **Leitura prévia** | Goldsmith (G), cap. 2 (selecção) |
| **Módulo** | [02-fundamentos-comunicacao-sem-fios](./modulos/02-fundamentos-comunicacao-sem-fios.md) (§1–3) |
| **Checkpoint** | Script Python que calcula P_rx e margem para o cenário âncora |

**Fórmulas-chave:**
```
Friis:  P_rx = P_tx + G_tx + G_rx - PL(d)
Log-dist: PL(d) = PL(d0) + 10·n·log10(d/d0)
SNR = P_rx - N (dBm)
```

---

### Semana 3 — Fundamentos: interferência e métricas (Ponto FUC 2)

| | Conteúdo |
|---|----------|
| **T** | Interferência, desvanecimento, mobilidade; métricas: débito, latência, PER, energia/bit |
| **PL** | Medições **reais** Wi-Fi do portátil: RSSI vs. distância; comparar com modelos da sem. 2 |
| **Leitura prévia** | G, cap. 3 (selecção) |
| **Módulo** | [02-fundamentos-comunicacao-sem-fios](./modulos/02-fundamentos-comunicacao-sem-fios.md) (§4–6) |
| **Checkpoint** | Gráfico RSSI medido vs. modelado + análise de desvio |

---

### Semana 4 — Acesso ao meio (Ponto FUC 3)

| | Conteúdo |
|---|----------|
| **T** | Meio partilhado; ALOHA, CSMA/CA, TDMA; nó escondido/exposto |
| **PL** | Wireshark modo monitor: tramas 802.11, RTS/CTS, retransmissões |
| **Leitura prévia** | D&P, cap. 5 |
| **Módulo** | [03-acesso-meio-qos-energia-seguranca](./modulos/03-acesso-meio-qos-energia-seguranca.md) (§1–3) |
| **Checkpoint** | Captura Wireshark com identificação de retransmissão e tipo MAC |

> Reaproveia material CCNA (meio partilhado, tramas).

---

### Semana 5 — QoS, fiabilidade, energia (Ponto FUC 3)

| | Conteúdo |
|---|----------|
| **T** | QoS, fiabilidade, segurança no acesso; duty cycling; eficiência energética (S-MAC) |
| **PL** | Simulação CSMA vs. TDMA (script fornecido); colisões vs. carga |
| **Leitura prévia** | D&P, cap. 6 |
| **Módulo** | [03-acesso-meio-qos-energia-seguranca](./modulos/03-acesso-meio-qos-energia-seguranca.md) (§4–6) |
| **Checkpoint** | Relatório curto: quando TDMA vence CSMA no cenário âncora? |

> **Guião PL avaliável** (conta para os 15% da componente prática).

---

### Semana 6 — Tecnologias: Wi-Fi vs BLE (Ponto FUC 4)

| | Conteúdo |
|---|----------|
| **T** | Wi-Fi (802.11) vs. BLE: arquitetura, alcance, débito, energia |
| **PL** | Captura e análise BLE; **lançamento do mini-projeto** (proposta na sem. 8) |
| **Leitura prévia** | Excertos 802.11 |
| **Módulo** | [04-wlan-wpan-wifi-ble-zigbee](./modulos/04-wlan-wpan-wifi-ble-zigbee.md) (§1–2) |
| **Checkpoint** | Tabela comparativa Wi-Fi vs. BLE para o cenário âncora |

---

### Semana 7 — Tecnologias: 802.15.4, LPWAN (Ponto FUC 4)

| | Conteúdo |
|---|----------|
| **T** | IEEE 802.15.4/ZigBee; LPWAN: LoRaWAN e NB-IoT; tabela de trade-offs |
| **PL** | Calculadora airtime LoRa; dimensionamento LPWAN para cenário âncora |
| **Leitura prévia** | Excertos 802.15.4 |
| **Módulo** | [04-wlan-wpan-wifi-ble-zigbee](./modulos/04-wlan-wpan-wifi-ble-zigbee.md) (§3) + [05-celular-lpwan](./modulos/05-celular-lpwan.md) |
| **Checkpoint** | Dimensionamento LoRa: SF, BW, payload, airtime, bateria estimada |

---

### Semana 8 — WSN: arquitetura e topologias (Ponto FUC 5)

| | Conteúdo |
|---|----------|
| **T** | Arquitetura do nó sensor, gateways, topologias (estrela, malha, cluster) |
| **PL** | Cooja: **primeira rede multi-hop**; **entrega da proposta de mini-projeto** |
| **Leitura prévia** | D&P, cap. 2–3 |
| **Módulo** | [06-redes-sensores-topologias-roteamento](./modulos/06-redes-sensores-topologias-roteamento.md) (§1–3) |
| **Checkpoint** | Proposta de mini-projeto entregue (ver [08-planeamento](./modulos/08-planeamento-simulacao-mini-projeto.md)) |

**Marco do mini-projeto:** proposta formal com tecnologia, topologia, protocolos e métricas.

---

### Semana 9 — WSN: agregação e sincronização (Ponto FUC 5)

| | Conteúdo |
|---|----------|
| **T** | Recolha e agregação de dados; sincronização e localização (conceitos) |
| **PL** | Cooja: agregação vs. envio direto — medir tráfego e energia |
| **Leitura prévia** | D&P, cap. 7 e 9 (selecção) |
| **Módulo** | [06-redes-sensores-topologias-roteamento](./modulos/06-redes-sensores-topologias-roteamento.md) (§4–5) |
| **Checkpoint** | Gráfico tráfego/energia: agregação vs. directo |

> **Guião PL avaliável** (semanas 2, 5, 9, 10 são referidas pelo docente).

---

### Semana 10 — WSN: encaminhamento e energia (Ponto FUC 5)

| | Conteúdo |
|---|----------|
| **T** | Encaminhamento em WSN; gestão de energia do nó |
| **PL** | Cooja: **RPL** em funcionamento; construção do DODAG e reparação |
| **Leitura prévia** | D&P, cap. 8 |
| **Módulo** | [06-redes-sensores-topologias-roteamento](./modulos/06-redes-sensores-topologias-roteamento.md) (§6–7) |
| **Checkpoint** | Captura/screenshot DODAG + explicação de rank e parent |

> **Guião PL avaliável.**

---

### Semana 11 — IoT: 6LoWPAN e RPL (Ponto FUC 6)

| | Conteúdo |
|---|----------|
| **T** | Endereçamento, 6LoWPAN, RPL (visão IETF); pilha para redes restritas |
| **PL** | 6LoWPAN e RPL no Wireshark (rede da sem. 10); captura MQTT de broker local (só como tráfego) |
| **Leitura prévia** | RFC 6282, RFC 6550 (excertos) |
| **Módulo** | [07-protocolos-iot-6lowpan-rpl-coap-mqtt](./modulos/07-protocolos-iot-6lowpan-rpl-coap-mqtt.md) (§1–3) |
| **Checkpoint** | Identificar compressão de cabeçalho IPv6→6LoWPAN numa captura |

---

### Semana 12 — IoT: CoAP vs MQTT (Ponto FUC 6)

| | Conteúdo |
|---|----------|
| **T** | CoAP vs. MQTT; segurança em redes restritas (DTLS, chaves, ameaças) |
| **PL** | Wireshark: dissecção CoAP vs. MQTT vs. HTTP — overhead, perdas, impacto energético |
| **Leitura prévia** | RFC 7252 (excertos) |
| **Módulo** | [07-protocolos-iot-6lowpan-rpl-coap-mqtt](./modulos/07-protocolos-iot-6lowpan-rpl-coap-mqtt.md) (§4–6) |
| **Checkpoint** | Tabela overhead CoAP vs. MQTT para o cenário âncora |

---

### Semana 13 — Planeamento e artigo (Ponto FUC 7)

| | Conteúdo |
|---|----------|
| **T** | Metodologia de comparação e seleção de soluções; discussão de artigo à escolha |
| **PL** | Sessão inteira de **trabalho no mini-projeto** com acompanhamento |
| **Leitura prévia** | Artigo científico escolhido pelo aluno |
| **Módulo** | [08-planeamento-simulacao-mini-projeto](./modulos/08-planeamento-simulacao-mini-projeto.md) |
| **Checkpoint** | Rascunho do relatório (≥ 50%) + lista de resultados |

---

### Semana 14 — Síntese e apresentação (Ponto FUC 8)

| | Conteúdo |
|---|----------|
| **T** | Revisão orientada para o teste; síntese trade-offs energia/desempenho/custo |
| **PL** | **Apresentação e discussão do mini-projeto** |
| **Módulo** | Revisão global + [materia-extra.md](./materia-extra.md) |
| **Checkpoint** | Projeto entregue + apresentação |

---

## Mini-projeto (35% da nota final)

**Enunciado-tipo (Prof. Rui Paulo):**

> Projetar e avaliar (por simulação em Cooja ou análise fundamentada) uma rede de sensores para o **cenário âncora**, justificando tecnologia de acesso, topologia, protocolo de encaminhamento e protocolo aplicacional, com análise de compromissos **energia / latência / fiabilidade**.

| Marco | Semana |
|-------|--------|
| Lançamento | 6 |
| Proposta entregue | 8 |
| Acompanhamento PL | 9–13 |
| Relatório + apresentação | 14 |

### Grelha de avaliação

| Critério | Peso |
|----------|------|
| Fundamentação técnica | 40% |
| Resultados / análise | 30% |
| Relatório | 20% |
| Apresentação / discussão | 10% |

Realização **individual ou em pares** (a fixar após 3.ª fase de candidaturas).

Detalhes completos: [módulo 08 — Mini-projeto](./modulos/08-planeamento-simulacao-mini-projeto.md).

---

## Avaliação global

| Componente | Peso |
|------------|------|
| Prova individual escrita (teste/exame) | **50%** |
| Mini-projeto | **35%** |
| Guiões PL selecionados (sem. 2, 5, 9, 10) | **15%** |
| **Total prática** | **50%** |

- Nota final ≥ **9,50** para aprovação
- Mínimo na componente prática para admissão ao exame (conforme regulamento)

---

## Bibliografia principal

| Sigla | Obra |
|-------|------|
| **D&P** | Christian Dargie & Christian Poellabauer — *Fundamentals of Wireless Sensor Networks* |
| **G** | Andrea Goldsmith — *Wireless Communications* |
| **Normas** | IEEE 802.11, 802.15.4; IETF RFC 6282 (6LoWPAN), RFC 6550 (RPL), RFC 7252 (CoAP) |

---

## Setup recomendado (Semana 1)

```bash
# Wireshark
sudo apt install wireshark

# Python para link budget
pip install numpy matplotlib

# Contiki-NG + Cooja
git clone https://github.com/contiki-ng/contiki-ng.git
cd contiki-ng
# Seguir README para Cooja (requer Java)
```

Consulta também: [cenario-ancora-agricola.md](./cenario-ancora-agricola.md)
