# Módulo 08 — Planeamento, Simulação e Mini-Projeto

**UC:** Redes Sem Fios e de Sensores · **Docente:** Rui Paulo · **Semanas:** 6–14

> Alinhado com o [PLANO-SEMANAL](../PLANO-SEMANAL.md) e o [cenário âncora agrícola](../cenario-ancora-agricola.md).

## Objetivos de aprendizagem

- Planear deployment de redes WSN/IoT (link budget, densidade, cobertura)
- Utilizar ferramentas de simulação (Cooja, NS-3, OMNeT++)
- Definir métricas e cenários de avaliação
- Elaborar mini-projeto fundamentado com resultados reproducíveis

---

## 1. Planeamento de rede

### Passos

1. **Requisitos:** alcance, taxa, energia, fiabilidade, nº dispositivos
2. **Selecção tecnologia:** Wi-Fi, BLE, 802.15.4, LoRaWAN, NB-IoT
3. **Link budget:** verificar viabilidade de cada link
4. **Densidade e topologia:** nós/gateway, mesh vs. star
5. **Backend:** cloud, protocolo (MQTT/CoAP), segurança
6. **Deployment:** instalação, provisioning, monitorização

### Link budget (checklist)

```
□ P_tx, G_tx, G_rx conhecidos
□ Path loss model seleccionado (indoor/outdoor, n)
□ Margem fading (10–20 dB)
□ P_sensitivity do receptor
□ P_rx > P_sensitivity? → Link OK
```

### Densidade de gateways LoRaWAN

Regra empírica: 1 gateway urbano cobre 2–5 km; rural 5–15 km.  
Planeamento: usar tools (Radio Mobile, Semtech LoRa calculator).

---

## 2. Ferramentas de simulação

### Cooja (Contiki/Contiki-NG)

| Aspeto | Detalhe |
|--------|---------|
| Foco | 802.15.4, 6LoWPAN, RPL, CoAP |
| Emulação | Compila firmware real para motes virtuais |
| Motas | Z1, Sky, Cooja mote |
| Visualização | Topologia, radio range, energia |
| Ideal para | Protocolos IoT constrained, RPL, MAC 802.15.4 |

```bash
# Exemplo: iniciar Cooja com Contiki-NG
cd contiki-ng/tools/cooja
./cooja
```

### NS-3

| Aspeto | Detalhe |
|--------|---------|
| Foco | Wi-Fi, LTE, LoRa, redes genéricas |
| Tipo | Simulador discrete-event (C++/Python) |
| Módulos | lr-wpan (802.15.4), Wi-Fi, LoRaWAN, LTE |
| Ideal para | Performance analysis, comparação tecnologias |

```python
# NS-3: exemplo conceptual
# helper = LrWpanHelper()
# helper.SetChannel(channel)
# devices = helper.Install(nodes)
```

### OMNeT++ / INET

| Aspeto | Detalhe |
|--------|---------|
| Foco | Redes genéricas, wired + wireless |
| Tipo | Framework modular (C++) |
| Ideal para | Cenários complexos, integração multi-tecnologia |

### Comparação

| Ferramenta | IoT constrained | Wi-Fi/LTE | Curva aprendizagem |
|------------|-----------------|-----------|-------------------|
| Cooja | ★★★★★ | ★ | Média |
| NS-3 | ★★★ | ★★★★★ | Alta |
| OMNeT++ | ★★★ | ★★★★ | Alta |

---

## 3. Definição de cenários

### Parâmetros a variar

| Parâmetro | Exemplo |
|-----------|---------|
| Nº nós | 10, 50, 100 |
| Área | 100×100 m, 1×1 km |
| Taxa de dados | 1 pkt/min, 1 pkt/s |
| Modelo energia | Bateria 2000 mAh |
| Mobility | Estático, random walk |
| Falhas | 5% nós morrem ao fim de 1h |

### Métricas

| Métrica | Unidade | Ferramenta |
|---------|---------|------------|
| PDR (Packet Delivery Ratio) | % | Todas |
| Latência end-to-end | ms/s | Todas |
| Consumo energético | mJ/pacote, J total | Cooja, NS-3 |
| Network lifetime | horas/dias | Cooja |
| Overhead routing | pacotes contr./dados | Cooja, NS-3 |
| Throughput | kbps | NS-3 |

---

## 4. Metodologia experimental

```
1. Hipótese (ex.: "RPL MRHOF reduz PDR vs. OF0 com 20% perda")
2. Cenário base (fixar parâmetros comuns)
3. Variável independente (OF0 vs. MRHOF)
4. N ≥ 30 runs com seeds diferentes
5. Intervalos de confiança (95%)
6. Análise e conclusão
```

### Boas práticas

- Documentar versão simulator e firmware
- Scripts reproducíveis (Python/bash)
- Gráficos com barras de erro
- Comparar com resultados da literatura
- Validar modelo (sanity checks)

---

## 5. Mini-projeto — enunciado oficial (Prof. Rui Paulo)

### Enunciado

> Projetar e avaliar (por simulação em **Cooja** ou análise fundamentada) uma rede de sensores para o **cenário âncora** (monitorização agrícola no Algarve), justificando:
> - tecnologia de acesso
> - topologia
> - protocolo de encaminhamento
> - protocolo aplicacional
>
> Com análise de compromissos **energia / latência / fiabilidade**.

**Âmbito RSFS:** rede até ao gateway. Integração cloud/broker/JSON → UC IoT.

### Marcos

| Marco | Semana | Entregável |
|-------|--------|------------|
| Lançamento | 6 | Leitura do enunciado + ideias iniciais |
| **Proposta** | **8** | Documento 2–3 págs.: tecnologia, topologia, protocolos, métricas |
| Acompanhamento | 9–13 | Progresso nas PL (Cooja, resultados parciais) |
| **Entrega final** | **14** | Relatório + apresentação/discussão |

Realização **individual ou em pares** (a confirmar após 3.ª fase).

### Grelha de avaliação (35% da nota final)

| Critério | Peso |
|----------|------|
| Fundamentação técnica | **40%** |
| Resultados / análise | **30%** |
| Relatório | **20%** |
| Apresentação / discussão | **10%** |

### Estrutura sugerida da proposta (Semana 8)

1. Descrição do cenário e requisitos (RF/RNF)
2. Tecnologia de acesso escolhida + alternativas descartadas
3. Topologia (diagrama) e nº de nós
4. Protocolo de encaminhamento (ex.: RPL, flooding, estrela LoRaWAN)
5. Protocolo aplicacional até ao gateway (CoAP, MQTT-SN, etc.)
6. Métricas a medir e hipóteses
7. Plano de simulação Cooja (ou metodologia analítica)

### Estrutura sugerida do relatório final

1. **Introdução** — problema, objectivos, contribuição
2. **Estado da arte** — tecnologias/protocolos relevantes (D&P, RFCs)
3. **Cenário** — topologia, parâmetros, ferramenta
4. **Implementação** — configuração Cooja, desafios
5. **Resultados** — gráficos PDR, energia, latência, overhead
6. **Análise de trade-offs** — energia vs. latência vs. fiabilidade
7. **Conclusão** — respostas às questões, limitações
8. **Referências** — IEEE, IETF RFCs, artigos

### Exemplos de abordagens válidas

| Abordagem | Ferramenta | Foco |
|-----------|----------|------|
| Malha 802.15.4 + RPL vs. estrela | Cooja | PDR, energia, saltos |
| Agregação vs. envio directo | Cooja | Tráfego, lifetime |
| LoRaWAN SF7 vs. SF12 | Análise + calculadora | Airtime, bateria, alcance |
| CoAP vs. MQTT-SN no gateway | Wireshark + análise | Overhead, latência |

---

## 6. Estudo de caso: cenário âncora agrícola (Algarve)

Ver documento completo: [cenario-ancora-agricola.md](../cenario-ancora-agricola.md)

### Resumo

- 20–50 nós: humidade solo, temperatura, luminosidade
- Leitura a cada 15 min, autonomia ≥ 2 anos
- Parcela 1–5 ha, alcance nó→gateway ≤ 200 m
- Gateway como border router (6LoWPAN) ou LoRaWAN concentrador

### Análise rápida

1. **Link budget:** validar com Python (sem. 2) antes de simular
2. **Topologia:** malha RPL se 802.15.4; estrela se LoRaWAN
3. **Agregação:** 4 leituras/pacote reduz tráfego ~75% (testar sem. 9)
4. **Backend:** fora do âmbito RSFS — referir apenas interface no gateway

---

## Exercícios

### Exercício 1
Liste os 5 passos de planeamento de uma rede IoT e indique entregáveis de cada.

### Exercício 2
Compare Cooja e NS-3 para simular RPL em 802.15.4. Qual preferir?

### Exercício 3
Defina um cenário experimental para comparar LEACH vs. flooding em lifetime de rede.

### Exercício 4
Uma simulação reporta PDR = 100% com 100 nós e 0% perda de link. Identifique dois problemas metodológicos possíveis.

### Exercício 5
Calcule: 50 sensores, 1 pkt/15 min, 50 bytes/pkt, energia TX = 0.1 mJ/pkt. Consumo diário total?

### Exercício 6
Descreva a estrutura mínima de um relatório de mini-projeto.

### Exercício 7
Para smart agriculture (caso acima), justifique LoRaWAN vs. Wi-Fi.

### Exercício 8
Porque executar N ≥ 30 runs com seeds diferentes numa simulação?

---

## Soluções

### Solução 1
1. **Requisitos** → documento de requisitos
2. **Selecção tecnologia** → matriz comparativa
3. **Link budget** → cálculos, mapa cobertura
4. **Topologia** → diagrama rede, BOM (bill of materials)
5. **Backend/deployment** → arquitectura cloud, plano instalação

### Solução 2
**Cooja preferível:** emula firmware Contiki-NG real, suporte nativo 6LoWPAN/RPL/802.15.4, visualização energia, curva aprendizagem menor para IoT constrained. NS-3: mais flexível mas configuração lr-wpan/RPL mais complexa.

### Solução 3
- **Cenário:** 50 nós, área 100×100 m, sink central, energia inicial 2 J
- **Variável:** protocolo (LEACH vs. flooding)
- **Métrica:** network lifetime (primeiro nó morto), PDR, energia total
- **Runs:** 30 seeds, intervalo confiança 95%
- **Ferramenta:** Cooja com Contiki-NG

### Solução 4
1. **Perda de link 0%** irreal — sem modelo de canal/fading
2. **PDR 100%** pode indicar simulação sem contenção/colisões
3. Falta de variabilidade estatística (1 run apenas)
4. Buffer sizes ilimitados

### Solução 5
Pkts/dia = 50 × (24×60/15) = 50 × 96 = 4800 pkts  
Energia = 4800 × 0.1 mJ = **480 mJ/dia** (0.48 J/dia)

### Solução 6
Introdução, estado da arte, cenário, implementação, resultados (gráficos/tabelas), conclusão, referências. Opcional: apêndice com código/configs.

### Solução 7
- **LoRaWAN:** alcance 500 m área sem AP, bateria 2 anos, baixo custo/nó
- **Wi-Fi:** requer AP + energia, alcance limitado outdoor, overkill em taxa, consumo alto
- **LoRaWAN** adequado para sensores esparsos em campo

### Solução 8
Simulações têm componente aleatória (backoff, perdas, posições). N ≥ 30 runs permite calcular média e intervalo de confiança estatisticamente válido, evitando conclusões baseadas num outlier.
