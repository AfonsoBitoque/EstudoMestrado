# Módulo 01 — Fundamentos de IoT e Arquitetura

**UC:** Internet das Coisas · **Parte I** · Tempo sugerido: 5–7 h

---

## Objetivos de aprendizagem

Ao concluir este módulo, deverás ser capaz de:

- Definir Internet das Coisas (IoT) e distinguir IoT de sistemas embebidos tradicionais
- Descrever a arquitetura em três camadas (dispositivo, gateway, nuvem)
- Identificar o papel de sensores, atuadores, edge, gateway e cloud
- Escolher componentes adequados para um cenário domótico ou industrial

---

## 1. O que é Internet das Coisas?

A **Internet das Coisas (IoT)** designa a interligação de objetos físicos à Internet de forma que possam **recolher dados**, **comunicar** e **agir** com algum grau de autonomia. Ao contrário de um microcontrolador isolado que executa um programa fixo, um dispositivo IoT participa num **ecossistema distribuído** onde dados fluem entre sensores, processadores locais, gateways e serviços na nuvem.

### Características distintivas da IoT

| Característica | Descrição |
|----------------|-----------|
| **Conectividade** | Ligação persistente ou intermitente (Wi-Fi, Ethernet, LoRa, celular) |
| **Identidade** | Cada dispositivo tem identificador único (MAC, UUID, certificado) |
| **Telemetria** | Envio periódico ou por evento de medições (temperatura, movimento, etc.) |
| **Atuação remota** | Comandos recebidos da nuvem ou de outros sistemas |
| **Escala** | Dezenas a milhões de dispositivos no mesmo sistema |
| **Recursos limitados** | CPU, RAM, energia e largura de banda frequentemente restritos |

### IoT vs. sistemas embebidos clássicos

Um termóstato analógico é embebido mas **não é IoT**. Um termóstato inteligente que reporta temperatura a uma app móvel e recebe comandos via MQTT **é IoT**. A diferença está na **conectividade de rede** e na **integração com serviços externos**.

### Domínios de aplicação

- **Domótica:** iluminação, climatização, segurança
- **Indústria 4.0:** monitorização de máquinas, manutenção preditiva
- **Agricultura inteligente:** humidade do solo, rega automática
- **Saúde:** wearables, monitorização remota de pacientes
- **Cidades inteligentes:** tráfego, iluminação pública, qualidade do ar

---

## 2. Arquitetura em três camadas

A arquitetura IoT mais comum organiza o sistema em **três camadas lógicas**:

```
┌─────────────────────────────────────────────────────────┐
│                    CAMADA CLOUD                          │
│  Armazenamento, analytics, dashboards, ML, APIs        │
└──────────────────────────┬──────────────────────────────┘
                           │ Internet / WAN
┌──────────────────────────▼──────────────────────────────┐
│                   CAMADA GATEWAY                         │
│  Agregação, protocolo, filtragem, conversão de dados     │
└──────────────────────────┬──────────────────────────────┘
                           │ LAN / PAN / Field bus
┌──────────────────────────▼──────────────────────────────┐
│                   CAMADA DISPOSITIVO                     │
│  Sensores, atuadores, microcontroladores, edge local     │
└─────────────────────────────────────────────────────────┘
```

### Camada 1 — Dispositivo (Device / Perception Layer)

É a **camada de perceção e ação**, onde o mundo físico encontra o digital.

**Componentes típicos:**
- Microcontroladores (ESP32, Arduino, STM32)
- Sensores (DHT22, BME280, acelerómetro, câmara)
- Atuadores (relés, servos, LEDs, válvulas)
- Firmware em C/C++, MicroPython ou Rust

**Responsabilidades:**
- Ler sensores em intervalos definidos ou por interrupção
- Executar lógica local simples (debounce, limiares)
- Enviar telemetria para o gateway ou diretamente para a cloud
- Receber e executar comandos (ligar luz, abrir válvula)

**Restrições:** memória de KB a poucos MB, consumo energético crítico em dispositivos a bateria, protocolos leves (MQTT, CoAP).

### Camada 2 — Gateway (Network / Edge Gateway Layer)

O **gateway** atua como **ponte** entre dispositivos com recursos limitados e a infraestrutura cloud.

**Funções principais:**
- **Agregação:** receber dados de múltiplos sensores e consolidar
- **Conversão de protocolo:** Zigbee/Bluetooth → MQTT/HTTPS
- **Filtragem e pré-processamento:** descartar leituras inválidas, calcular médias
- **Buffer offline:** armazenar dados quando a ligação à cloud falha
- **Segurança:** terminação TLS, autenticação de dispositivos

**Exemplos:** Raspberry Pi com Mosquitto, AWS IoT Greengrass, Azure IoT Edge, routers industriais.

### Camada 3 — Cloud (Application Layer)

A **nuvem** fornece escala, persistência e valor de negócio.

**Serviços típicos:**
- **Ingestão de dados:** AWS IoT Core, Azure IoT Hub, Google Cloud IoT
- **Armazenamento:** InfluxDB, TimescaleDB, S3, Cosmos DB
- **Processamento:** stream processing (Kafka, Kinesis), regras (Node-RED cloud)
- **Visualização:** Grafana, dashboards customizados
- **Machine Learning:** deteção de anomalias, previsão de falhas

---

## 3. Sensores e atuadores

### Sensores

Um **sensor** converte uma grandeza física num sinal elétrico digital ou analógico.

| Tipo | Grandeza medida | Exemplos |
|------|-----------------|----------|
| Ambiental | Temperatura, humidade, pressão | DHT22, BME280 |
| Movimento | Aceleração, rotação, presença | MPU6050, PIR |
| Luz | Intensidade luminosa | LDR, BH1750 |
| Distância | Proximidade | HC-SR04 (ultrassom) |
| Elétrico | Corrente, tensão | ACS712, INA219 |
| Químico | Gases, pH | MQ-135, sensor pH |

**Conceitos importantes:**
- **Precisão vs. exatidão:** precisão = repetibilidade; exatidão = proximidade ao valor real
- **Taxa de amostragem:** frequência de leitura (Hz); trade-off com consumo e tráfego de rede
- **Calibração:** ajuste de offset e ganho para valores corretos

### Atuadores

Um **atuador** converte um sinal elétrico numa ação física.

| Tipo | Ação | Exemplos |
|------|------|----------|
| Digital | ON/OFF | Relé, MOSFET, LED |
| Analógico | Valor contínuo | Servo, motor DC com PWM, DAC |
| Mecânico | Movimento | Stepper, solenoide |
| Térmico | Aquecimento/arrefecimento | Resistência, Peltier |

### Fluxo sensor → atuador (loop de controlo)

```
Sensor → ADC/Leitura → Processamento → Decisão → Atuador → Mundo físico
                ↑                                    │
                └──────── feedback (opcional) ───────┘
```

Em IoT, este loop pode ser **local** (edge) ou **remoto** (comando da cloud com latência).

---

## 4. Edge, Gateway e Cloud — papéis e fronteiras

### Edge computing (no dispositivo ou gateway)

Processamento **próximo da fonte de dados**, reduzindo latência e tráfego.

- **Edge no dispositivo:** filtrar leituras, detetar eventos (queda, movimento)
- **Edge no gateway:** agregação, regras complexas, inferência ML leve

### Gateway

Nem todo gateway faz edge computing, mas muitos gateways modernos incluem capacidade de processamento local (ex.: AWS Greengrass, Azure IoT Edge).

### Cloud

Ideal para:
- Armazenamento histórico de longo prazo
- Analytics sobre milhões de dispositivos
- Treino de modelos ML
- Integração com ERP, CRM, sistemas empresariais

**Regra prática:** processa no edge o que precisa de resposta rápida; envia para a cloud o que precisa de escala e histórico.

---

## 5. Padrões arquiteturais comuns

### Star (estrela) via gateway

Todos os dispositivos comunicam com um gateway central. Simples de gerir; gateway é ponto único de falha.

### Mesh (malha)

Dispositivos encaminham dados uns para os outros (Zigbee, Thread). Resiliente; mais complexo.

### Direct-to-cloud

Dispositivo com Wi-Fi/celular liga diretamente à cloud (ESP32 + MQTT). Sem gateway; cada dispositivo precisa de stack TCP/IP completo.

---

## 6. Considerações de design

| Fator | Questão a responder |
|-------|---------------------|
| Energia | Bateria ou alimentação fixa? Duty cycle? |
| Latência | Resposta em ms (edge) ou segundos (cloud)? |
| Largura de banda | Quanto dados por dia? |
| Segurança | Dados sensíveis? Regulamentação (GDPR)? |
| Fiabilidade | O que acontece offline? |
| Custo | CAPEX/OPEX por dispositivo |

---

## Exercícios

### Exercício 1 — Definição
Define IoT com as tuas palavras e dá dois exemplos de objetos que **não** são IoT e dois que **são**.

### Exercício 2 — Camadas
Para um sistema de rega automática em estufa, identifica pelo menos um componente de cada camada (dispositivo, gateway, cloud) e a sua função.

### Exercício 3 — Sensores
Uma fábrica quer detetar vibração anormal num motor. Que tipo de sensor recomendarias? Justifica precisão, taxa de amostragem e onde processar o sinal (edge vs. cloud).

### Exercício 4 — Arquitetura
Desenha (texto ou ASCII) uma arquitetura de 3 camadas para um sistema domótico com: 5 sensores de temperatura, 3 relés de iluminação, 1 câmara e app móvel. Indica protocolos plausíveis entre camadas.

### Exercício 5 — Gateway
Explica três funções que um gateway desempenha que um ESP32 sozinho não consegue fazer eficientemente numa instalação com 50 sensores Zigbee.

### Exercício 6 — Trade-offs
Compara arquitetura **direct-to-cloud** vs. **gateway centralizado** para 200 sensores de humidade do solo em campo agrícola (sem Wi-Fi, bateria de 2 anos). Qual preferes e porquê?

### Exercício 7 — Loop de controlo
Descreve o percurso completo de um comando "ligar AC" enviado de uma app móvel até o relé fechar, passando por todas as camadas.

### Exercício 8 — Design
Lista cinco requisitos não-funcionais (NFR) para um sistema IoT de monitorização de idosos em casa e indica em que camada cada um é mais crítico.

---

## Soluções

### Solução 1 — Definição

**Definição:** IoT é a rede de objetos físicos equipados com sensores, software e conectividade que permitem recolher, trocar e actuar sobre dados através da Internet, integrando o mundo físico com sistemas digitais.

**Não IoT:**
- Relógio de parede analógico (sem conectividade nem dados digitais)
- Calculadora de bolso (embebido isolado, sem rede)

**IoT:**
- Termóstato Nest (telemetria + comandos remotos via cloud)
- Pulseira Fitbit (sensores + sync com app/servidor)

### Solução 2 — Camadas

| Camada | Componente | Função |
|--------|------------|--------|
| Dispositivo | Sensor de humidade do solo (capacitivo) | Medir % humidade a cada 30 min |
| Dispositivo | Válvula solenoide + driver | Abrir/fechar rega conforme comando |
| Gateway | Raspberry Pi com LoRa concentrator | Agregar leituras de múltiplos sensores de campo, converter LoRa → MQTT |
| Cloud | AWS IoT Core + Lambda + DynamoDB | Regras de rega, histórico, alertas por email |

### Solução 3 — Sensores

**Sensor recomendado:** acelerómetro piezoelétrico ou MEMS triaxial (ex.: ADXL345, sensor de vibração industrial IEPE).

**Justificação:**
- **Precisão:** repetibilidade alta para comparar assinaturas de vibração ao longo do tempo
- **Taxa de amostragem:** 1–10 kHz para capturar frequências de defeito mecânico (rolamentos); amostragem contínua ou por janelas de FFT
- **Processamento:** **edge no gateway** — calcular RMS, FFT e detetar anomalias localmente (latência baixa, evita enviar MB/s para cloud); cloud recebe apenas features agregadas e alertas

### Solução 4 — Arquitetura domótica

```
[5× DHT22] ──I2C/1-Wire──► [ESP32 hub] ──Wi-Fi/MQTT──► [Raspberry Pi Gateway]
[3× Relé]  ◄──GPIO────────  [ESP32 hub]                    │ Mosquitto + Node-RED
                                                            │ TLS
[Câmara RTSP] ──Wi-Fi──────────────────────────────────────►│
                                                            ▼
                                              [Cloud: Home Assistant / AWS]
                                                            │
                                                            ▼
                                              [App móvel — HTTPS REST/MQTT over WebSocket]
```

- Dispositivo → Gateway: MQTT ou HTTP local
- Gateway → Cloud: MQTT over TLS ou HTTPS
- App → Cloud: REST API ou WebSocket

### Solução 5 — Funções do gateway

1. **Conversão de protocolo:** 50 sensores Zigbee usam stack leve; gateway traduz para MQTT/HTTPS que a cloud entende — ESP32 individual não geriria 50 radios Zigbee eficientemente.
2. **Agregação e batching:** gateway consolida 50 leituras num único payload JSON a cada minuto, reduzindo conexões TLS e custos cloud — ESP32 enviaria 50 mensagens separadas.
3. **Buffer offline:** se Internet cair, gateway armazena em SQLite/SD e reenvia — ESP32 com RAM limitada não bufferiza dias de dados de 50 sensores.

### Solução 6 — Trade-offs

**Recomendação: gateway centralizado** (ou LoRaWAN gateway + network server).

| Critério | Direct-to-cloud | Gateway |
|----------|-----------------|---------|
| Wi-Fi | Inexistente no campo | LoRa/Zigbee até gateway com backhaul |
| Bateria | Celular/Wi-Fi consome muito | LoRa: anos de bateria |
| Custo | 200 módulos celulares caros | 1–2 gateways + sensores baratos |
| Escala | 200 conexões cloud | 1 conexão cloud |

Direct-to-cloud exigiria modem celular por sensor — inviável para 2 anos de bateria e custo. Gateway com LoRaWAN concentra tráfego e estende autonomia.

### Solução 7 — Comando "ligar AC"

1. **App móvel:** utilizador toca "Ligar AC" → HTTPS POST para API cloud
2. **Cloud:** valida token OAuth, publica mensagem MQTT `home/living/ac/set` payload `{"state":"ON"}` no broker
3. **Gateway (se existir):** subscreve tópico, reencaminha para rede local, ou dispositivo subscreve directamente
4. **ESP32/dispositivo:** recebe MQTT, parse JSON, activa GPIO ligado ao relé
5. **Atuador:** relé fecha circuito → AC liga
6. **Feedback (opcional):** dispositivo publica `home/living/ac/status` → cloud → app actualiza UI

### Solução 8 — Requisitos não-funcionais

| NFR | Camada crítica | Motivo |
|-----|----------------|--------|
| Latência < 2 s em emergência (queda) | Edge/dispositivo | Detecção local; cloud demasiado lenta |
| Disponibilidade 99.9% | Cloud + gateway | Alertas a familiares/médicos |
| Privacidade (GDPR) | Cloud + dispositivo | Dados de saúde encriptados, consentimento |
| Autonomia 6 meses (wearable) | Dispositivo | Optimização firmware e duty cycle |
| Usabilidade (app simples) | Cloud (API/UI) | Familiares não-técnicos |

---

## Referências

- Andy King — *Programming the Internet of Things*
- Perry Lea — *IoT and Edge Computing for Architects*
- [ROADMAP da UC](../ROADMAP.md)
