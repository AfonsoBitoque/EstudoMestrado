# Módulo 01 — Enquadramento e Aplicações

**UC:** Redes Sem Fios e de Sensores · **Semana 1** · **Leitura prévia:** D&P cap. 1

> Segue o [PLANO-SEMANAL](../PLANO-SEMANAL.md). PL desta semana: setup Wireshark, Python, Cooja + escolha do [cenário âncora](../cenario-ancora-agricola.md).

## Objetivos de aprendizagem

- Distinguir WSN, IoT e M2M e as suas relações
- Identificar domínios de aplicação e requisitos típicos
- Analisar restrições de dispositivos restritos (constrained devices)
- Compreender a arquitetura em camadas da IoT

---

## 0. Formato desta UC e fronteira com IoT

### Formato seminário (turma pequena)

- **Teóricas:** lês D&P/G **antes** da aula; a sessão é discussão guiada, não exposição longa
- **PL:** guião curto, execução em bancada, docente circula e faz perguntas
- **Mini-projeto:** espinha dorsal da 2.ª metade (semanas 6–14)

### RSFS vs. Internet das Coisas (UC 14741088)

| RSFS (esta UC) | IoT (outra UC) |
|----------------|----------------|
| Rede **até ao gateway** | Integração aplicacional completa |
| Análise de protocolos (overhead, energia, fiabilidade) | Clientes, brokers, JSON, edge, cloud |
| Wireshark, Cooja, link budget | Implementação full-stack dispositivo→nuvem |

### Cenário âncora do semestre

**Monitorização agrícola no Algarve** — sensores de humidade, temperatura e luminosidade numa parcela rural. Usa este cenário em todas as PLs e no mini-projeto.

Detalhes: [cenario-ancora-agricola.md](../cenario-ancora-agricola.md)

---

## 1. Definições

| Termo | Definição |
|-------|-----------|
| **WSN** (Wireless Sensor Network) | Rede de nós sensores sem fios que colaboram na recolha e transmissão de dados ambientais |
| **IoT** (Internet of Things) | Ecossistema de objectos físicos conectados à Internet com identificação, sensores e actuadores |
| **M2M** (Machine-to-Machine) | Comunicação directa entre dispositivos sem intervenção humana |
| **CPS** (Cyber-Physical Systems) | Integração de computação, rede e processos físicos |

```
WSN ⊂ IoT ⊃ M2M
```

---

## 2. Arquitectura IoT em camadas

```
┌─────────────────────────────────────┐
│  Aplicações (smart city, saúde...)  │
├─────────────────────────────────────┤
│  Processamento / Fog / Edge         │
├─────────────────────────────────────┤
│  Rede (IP, 6LoWPAN, LoRaWAN, 5G)   │
├─────────────────────────────────────┤
│  Dispositivos (sensores, actuadores)│
└─────────────────────────────────────┘
```

### Camadas e protocolos

| Camada | Exemplos |
|--------|----------|
| Percepção | Sensores, RFID, BLE beacons |
| Rede | 802.15.4, Wi-Fi, LoRa, NB-IoT |
| Transporte | TCP, UDP, QUIC |
| Aplicação | MQTT, CoAP, HTTP/REST |

---

## 3. Domínios de aplicação

| Domínio | Exemplos | Requisitos dominantes |
|---------|----------|----------------------|
| **Agricultura inteligente** | Humidade solo, rega automática | Energia, alcance, baixo custo |
| **Saúde** | Monitorização paciente, wearables | Fiabilidade, latência, privacidade |
| **Smart cities** | Iluminação, tráfego, estacionamento | Escalabilidade, interoperabilidade |
| **Indústria 4.0** | Manutenção preditiva, robótica | Latência ultra-baixa, determinismo |
| **Ambiente** | Qualidade ar, incêndios florestais | Autonomia, cobertura remota |
| **Logística** | Rastreamento, cold chain | Mobilidade, cobertura wide-area |
| **Smart home** | Termostatos, câmaras, fechaduras | Usabilidade, interoperabilidade |

---

## 4. Requisitos e trade-offs

Dispositivos IoT/WSN operam sob **restrições severas**:

| Requisito | Descrição | Impacto |
|-----------|-----------|---------|
| **Energia** | Bateria ou energy harvesting | Limita radio duty cycle, computação |
| **Custo** | Centenas/milhares de nós | Hardware simplificado |
| **Alcance** | Metros a quilómetros | Escolha de tecnologia |
| **Taxa de dados** | bits/s a Mbit/s | Protocolo e radio |
| **Latência** | ms a horas | Tempo-real vs. event-driven |
| **Fiabilidade** | Perda tolerável ou crítica | Retransmissões, redundância |
| **Segurança** | Autenticação, cifragem | Overhead computacional |
| **Escalabilidade** | 10²–10⁶ dispositivos | Endereçamento, roteamento |

### Triângulo de trade-offs

```
        Energia
         /\
        /  \
       /    \
  Alcance ── Taxa de dados
```

Não é possível optimizar os três simultaneamente.

---

## 5. Classificação de dispositivos (RFC 7228)

| Classe | Memória (RAM/Flash) | Exemplo |
|--------|---------------------|---------|
| 0 | << 10 KB / 100 KB | Sensor simples 802.15.4 |
| 1 | ~10 KB / ~250 KB | Contiki, RIOT |
| 2 | ~50 KB / ~250 KB | IoT gateway, ESP32 |

---

## 6. Padrões e organizações

| Organização | Área |
|-------------|------|
| IEEE | 802.11, 802.15.4, 802.15.1 (BLE) |
| IETF | 6LoWPAN, CoAP, RPL, CORE |
| 3GPP | NB-IoT, LTE-M, 5G mMTC |
| LoRa Alliance | LoRaWAN |
| CSA | Matter (smart home) |

---

## Exercícios

### Exercício 1
Diferencie WSN e IoT. Toda a WSN é IoT? Toda a IoT é WSN?

### Exercício 2
Para monitorização de incêndios florestais com sensores alimentados por bateria e solar, identifique os três requisitos mais críticos.

### Exercício 3
Explique o trade-off entre alcance e taxa de dados numa rede LPWAN.

### Exercício 4
Classifique os dispositivos: (a) ESP32 com 520 KB SRAM, (b) sensor 802.15.4 com 8 KB RAM, (c) gateway industrial com 512 MB RAM.

### Exercício 5
Compare requisitos de smart agriculture vs. telemedicina em termos de latência e fiabilidade.

### Exercício 6
Descreva a arquitectura em camadas IoT e indique um protocolo por camada.

### Exercício 7
Porque é a energia frequentemente o requisito dominante em WSN?

### Exercício 8
Uma cidade quer deployar 50 000 sensores de estacionamento. Que desafios de escalabilidade existem?

---

## Soluções

### Solução 1
- **WSN:** foco em sensores colaborativos, frequentemente sem IP, multi-hop
- **IoT:** conceito mais amplo, inclui actuadores, gateways, cloud, IP
- Nem toda WSN é IoT (pode operar isolada); nem toda IoT é WSN (ex.: smart TV, câmara Wi-Fi)

### Solução 2
1. **Autonomia energética** (bateria + solar, duty cycle baixo)
2. **Alcance/cobertura** (áreas remotas, floresta)
3. **Fiabilidade** (detecção crítica — falsos negativos perigosos)

### Solução 3
LPWAN optimiza alcance (km) com taxas baixas (kbps) usando modulação robusta (CSS em LoRa) e bandwidth estreita. Aumentar taxa exige mais SNR → menor alcance ou mais potência → menos autonomia.

### Solução 4
- (a) ESP32 → **Classe 2**
- (b) Sensor 802.15.4 → **Classe 0**
- (c) Gateway 512 MB → **Classe 2+** (não constrained; nó gateway)

### Solução 5
- **Agricultura:** latência tolerante (minutos/horas), fiabilidade moderada (dados não críticos)
- **Telemedicina:** latência crítica (segundos), fiabilidade alta (vida do paciente), privacidade obrigatória

### Solução 6
Percepção (sensores) → Rede (802.15.4, LoRaWAN) → Transporte (UDP/TCP) → Aplicação (MQTT, CoAP) → Processamento (cloud/fog)

### Solução 7
Radio TX/RX consome ordens de magnitude mais energia que computação. Nós com bateria limitada devem minimizar transmissões (duty cycle < 1%), usar sleep modes, e optimizar protocolos MAC/roteamento para energia.

### Solução 8
Endereçamento IP, gestão de chaves, provisioning, manutenção OTA, backend para 50k dispositivos, cobrança de rede celular/LPWAN, interferência mútua, actualizações de firmware, monitorização de saúde da rede.
