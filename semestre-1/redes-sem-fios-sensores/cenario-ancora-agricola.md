# Cenário Âncora — Monitorização Agrícola no Algarve

Cenário de referência para PLs, discussões e **mini-projeto** de RSFS (Prof. Rui Paulo, 2026/27).

> RSFS cobre a rede **até ao gateway**. Integração cloud/JSON/brokers pertence à UC de IoT.

---

## Contexto

Exploração agrícola no Algarve (ex.: pomar de citrinos ou estufa de morangos) com sensores distribuídos para monitorizar condições que afectam produtividade e consumo de água.

### Motivação regional

- Clima mediterrânico: verões quentes e secos → stress hídrico
- Solos arenosos: drenagem rápida, variabilidade espacial
- Escassez de água → decisões de rega baseadas em dados
- Parcelas de dimensão média (1–5 ha) → alcance e densidade realistas

---

## Requisitos funcionais

| ID | Requisito |
|----|-----------|
| RF1 | Medir humidade do solo a 20 cm de profundidade |
| RF2 | Medir temperatura ambiente e humidade relativa do ar |
| RF3 | Medir luminosidade (PAR simplificado) |
| RF4 | Enviar leituras ao gateway pelo menos a cada 15 min |
| RF5 | Gateway reencaminha dados para sistema central (fora do âmbito RSFS) |

---

## Requisitos não funcionais

| Atributo | Meta | Notas |
|----------|------|-------|
| **Autonomia** | ≥ 2 anos com bateria | Duty cycling agressivo |
| **Alcance nó→gateway** | ≤ 200 m (campo aberto) | Com vegetação: modelar path loss n≈3–4 |
| **Fiabilidade** | PER < 5% em condições normais | Retransmissões limitadas |
| **Latência** | < 60 s aceitável | Não é tempo real crítico |
| **Custo por nó** | < 50 € | Restrição realista |
| **Escalabilidade** | 20–50 nós | Uma parcela |

---

## Topologia proposta (ponto de partida)

```
    [N1]───[N2]───[N3]
      \     |     /
       \    |    /
        [Gateway] ─── (→ rede IP / cloud — IoT UC)
       /    |    \
    [N4]───[N5]───[N6]
         ... (até N20–50)
```

- **Estrela** se LoRaWAN (nós → gateway LoRa)
- **Malha 802.15.4 + RPL** se IEEE 802.15.4 (multi-hop até gateway border router)
- **Híbrida:** sensores LPWAN remotos + cluster 802.15.4 numa zona densa

---

## Parâmetros para link budget (Semana 2)

| Parâmetro | Valor sugerido |
|-----------|----------------|
| Frequência | 868 MHz (LoRa EU) ou 2.4 GHz (802.15.4) |
| P_tx | 14 dBm (LoRa) / 0 dBm (802.15.4) |
| G_antena | 2 dBi (omni) |
| P_sensitivity | -137 dBm (LoRa SF12) / -95 dBm (802.15.4) |
| Path loss model | Log-distância, n = 2.7 (campo com árvores) |
| Margem fading | 15 dB |

### Exercício rápido

Calcula P_rx a 150 m com Friis e log-distância. A ligação é viável?

---

## Tecnologias candidatas (para comparar)

| Tecnologia | Prós no cenário | Contras |
|------------|-----------------|---------|
| **LoRaWAN** | Longo alcance, baixa energia | Downlink limitado, duty cycle regulamentar |
| **802.15.4 + RPL** | Multi-hop flexível, padrão aberto | Alcance curto por salto, complexidade RPL |
| **Wi-Fi (HaLow/802.11ah)** | IP nativo | Pouco disponível, consumo maior |
| **BLE mesh** | Baixo consumo | Escala limitada em campo aberto |
| **NB-IoT** | Cobertura celular | Custo mensal, dependência operador |

---

## Métricas para simulação Cooja (Semanas 8–10)

| Métrica | Como medir |
|---------|------------|
| Pacotes entregues / enviados | Cooja timeline / serial logs |
| Energia estimada | Modelo energético Contiki-NG |
| Latência end-to-end | Timestamp origem vs. gateway |
| Overhead de routing | Contagem pacotes RPL control vs. dados |
| Tráfego agregação | Comparar agregação vs. envio directo (sem. 9) |

---

## Protocolo aplicacional (escopo RSFS)

Para RSFS, analisa **até ao gateway**:

| Opção | Overhead | Adequação |
|-------|----------|-----------|
| **CoAP** | Baixo, UDP, RESTful | Ideal para 6LoWPAN |
| **MQTT-SN** | Médio | Ponte para MQTT no gateway |
| **HTTP** | Alto | Evitar em nós restritos |

A implementação de broker/cliente MQTT completo → UC IoT.

---

## Perguntas para guiões de discussão

1. LoRaWAN estrela vs. malha 802.15.4: qual escolhes e porquê?
2. Agregar 4 leituras num pacote ou enviar 4 pacotes?
3. Que SF LoRa maximiza autonomia sem violar latência de 15 min?
4. Como detectas falha de nó só com métricas de rede?
5. Onde colocas o gateway para minimizar saltos?

---

## Exercícios

1. Completa a tabela de requisitos com 2 RF e 2 RNF adicionais realistas.
2. Calcula link budget LoRa a 300 m com os parâmetros acima.
3. Desenha topologia em estrela e em malha para 12 nós; indica nº de saltos máximo.
4. Justifica CoAP vs. MQTT-SN para este cenário (1 parágrafo cada).
5. Identifica 3 desafios específicos do Algarve (clima, terreno, regulamentação).

## Soluções

1. *Exemplos:* RF6 — detetar geada (temp. < 2 °C); RF7 — alerta bateria baixa; RNF — operar -5 °C a 45 °C; RNF — IP67 na humidade do solo.

2. *LoRa link budget:* PL(300m) ≈ 32.44 + 20·log10(0.868) + 20·log10(0.3) ≈ 32.44 - 1.22 - 10.46 ≈ 20.8 dB (Friis simplificado). P_rx ≈ 14 + 2 + 2 - 20.8 = -2.8 dBm >> -137 dBm. **Viável** com grande margem; SF12 é overkill — SF7 pode bastar.

3. *Estrela:* todos ligados ao gateway (1 salto). *Malha:* layout grid 3×4, gateway no centro, salto máximo ≈ 2–3 dependendo do routing.

4. *CoAP:* RESTful nativo em UDP, baixo overhead, observe para push eficiente. *MQTT-SN:* útil se gateway traduz para MQTT cloud, mas overhead extra de tópicos.

5. *Desafios:* calor extremo (degradação bateria); solos secos (variabilidade humidade); regulamentação ISM 868 MHz duty cycle 1%; vento costeiro (corrosão); sombra de estufas (atenuação).
