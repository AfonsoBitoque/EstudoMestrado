# Módulo 08 — Planeamento, Simulação e Mini-Projeto

**UC:** Redes Sem Fios e de Sensores · **Fase:** 4 — Projeto e avaliação

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

## 5. Mini-projeto — directrizes

### Estrutura sugerida (relatório)

1. **Introdução** — problema, objectivos, contribuição
2. **Estado da arte** — tecnologias/protocolos relevantes
3. **Cenário** — topologia, parâmetros, ferramenta
4. **Implementação** — configuração, código, desafios
5. **Resultados** — gráficos, tabelas, análise
6. **Conclusão** — respostas às questões, limitações
7. **Referências** — IEEE, IETF RFCs, artigos

### Exemplos de temas

| Tema | Ferramenta |
|------|------------|
| Comparação RPL OF0 vs. MRHOF em WSN | Cooja |
| LoRaWAN ADR vs. SF fixo — alcance e energia | NS-3 |
| Wi-Fi vs. 802.15.4 para smart building | NS-3 |
| Impacto duty cycle em lifetime WSN | Cooja |
| NB-IoT vs. LoRaWAN — estudo de caso agriculture | Analítico + NS-3 |
| BLE mesh vs. ZigBee — latência e overhead | OMNeT++ / prática |

### Critérios de avaliação (referência)

| Critério | Peso |
|----------|------|
| Fundamentação técnica | 30% |
| Metodologia e rigor | 25% |
| Resultados e análise | 25% |
| Apresentação e clareza | 10% |
| Defesa oral | 10% |

---

## 6. Estudo de caso: smart agriculture

### Requisitos

- 50 sensores humidade/temperatura, 500 m × 500 m
- Leitura a cada 15 min, bateria 2 anos
- Gateway com backhaul 4G

### Análise

1. **Link budget:** LoRa SF10 → alcance ~5 km ✓
2. **Energia:** duty cycle 0.1% → lifetime > 2 anos ✓
3. **Backend:** LoRaWAN → MQTT → cloud dashboard
4. **Alternativa:** NB-IoT se cobertura operador disponível

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
