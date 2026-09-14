# Módulo 03 — Simulação, Emulação e Dados

**UC:** Internet das Coisas · **Parte II** · Tempo sugerido: 5–7 h

---

## Objetivos de aprendizagem

- Distinguir simulação de dados, emulação de hardware e sensores virtuais
- Criar geradores de telemetria realista para desenvolvimento sem hardware
- Avaliar trade-offs entre fidelidade, custo e velocidade de iteração
- Integrar dados simulados em pipelines MQTT/REST

---

## 1. Porquê simular?

Desenvolver IoT **só com hardware físico** é lento e frágil:

- Sensores podem avariar ou estar indisponíveis
- Condições ambientais difíceis de reproduzir (geada, vibração extrema)
- Escalar a 1000 dispositivos fisicamente é impossível em dev
- CI/CD precisa de testes automatizados **sem bancada**

**Simulação e emulação** permitem iterar rapidamente na lógica de software, integração cloud e dashboards antes do deploy em campo.

---

## 2. Simulação vs. emulação vs. sensores virtuais

| Conceito | O que modela | Fidelidade | Exemplo |
|----------|--------------|------------|---------|
| **Simulação de dados** | Apenas valores de telemetria | Baixa a média | Script Python gera `{temp: 22.5}` |
| **Emulação de hardware** | Comportamento do MCU + periféricos | Média a alta | Wokwi simula ESP32 e GPIO |
| **Sensor virtual** | Interface de sensor com backend simulado | Média | Driver lê de ficheiro/API em vez de I2C |

### 2.1 Simulação de dados

Gera **streams de dados** que imitam padrões reais sem modelar física nem firmware.

**Técnicas:**
- Valores aleatórios uniformes ou normais
- Random walk (sucesso de valor anterior + delta)
- Séries temporais com sazonalidade (sinusoide + ruído)
- Replay de datasets históricos (CSV → MQTT)

```python
import random, time, json

def simulate_temp(base=20.0):
    return base + random.gauss(0, 0.5)  # °C com ruído gaussiano

while True:
    payload = {"temp": round(simulate_temp(), 2), "ts": time.time()}
    print(json.dumps(payload))
    time.sleep(5)
```

### 2.2 Emulação de hardware

Reproduz **execução de firmware** em ambiente virtual, incluindo timers, interrupções e pinos GPIO (limitado).

**Wokwi:** ESP32, Arduino, sensores virtuais ligados por wiring no browser.

**QEMU + ESP-IDF:** emulação parcial de CPU; periféricos específicos podem faltar.

**Vantagem:** testar código C/C++ real sem gravar flash.

**Limitação:** timing, RF e consumo energético não são fiéis.

### 2.3 Sensores virtuais

Abstração onde o **código aplicacional** chama `read_temperature()` e o backend pode ser:

- Hardware real (BME280 via I2C)
- Ficheiro JSON actualizado por script
- Servidor HTTP que devolve leitura simulada

**Padrão Strategy / HAL (Hardware Abstraction Layer):**

```cpp
#ifdef SIMULATION
  float read_temperature() { return simulated_temp; }
#else
  float read_temperature() { return bme280.readTemperature(); }
#endif
```

Permite **mesmo código de negócio** em dev e produção.

---

## 3. Modelos de dados simulados

### 3.1 Ruído e realismo

Dados constantes (`temp: 20.0` sempre) não testam alertas nem gráficos. Introduzir:

- **Ruído gaussiano** em sensores analógicos
- **Outliers ocasionais** (1% leituras inválidas) para testar filtros
- **Deriva lenta** (simular envelhecimento ou mudança ambiental)
- **Eventos discretos** (porta aberta → pico movimento)

### 3.2 Cenários de falha

Simular comportamentos de campo:

| Cenário | Simulação |
|---------|-----------|
| Perda de rede | Parar publish MQTT por N minutos |
| Sensor stuck | Repetir mesmo valor 1000 vezes |
| Bateria baixa | Decrementar `battery_pct` linearmente |
| Spike | Temperatura salta para 85°C instantaneamente |

### 3.3 Escala — múltiplos dispositivos

```python
import asyncio
import aiomqtt  # ou paho-mqtt

async def device_sim(device_id: str):
    async with aiomqtt.Client("localhost") as client:
        while True:
            payload = {"id": device_id, "temp": 20 + random.random()}
            await client.publish(f"farm/{device_id}/temp", json.dumps(payload))
            await asyncio.sleep(10)

async def main():
    await asyncio.gather(*[device_sim(f"node-{i}") for i in range(100)])
```

---

## 4. Ferramentas e abordagens

| Ferramenta | Tipo | Uso |
|------------|------|-----|
| **Python scripts** | Simulação dados | Prototipagem rápida, CI |
| **Node-RED inject** | Simulação + flow | Demo e gateway |
| **Wokwi** | Emulação HW | Firmware sem placa |
| **Renode** | Emulação HW | STM32, nRF — mais avançado |
| **MQTT.fx / MQTTX** | Cliente manual | Publicar payloads teste |
| **Locust / custom** | Carga | Stress test broker |

### Node-RED — nós úteis

- **inject:** timestamp + payload fixo ou aleatório
- **function:** gerar JSON customizado
- **mqtt out:** publicar no broker

---

## 5. Integração no pipeline de desenvolvimento

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ Simulador    │────►│ MQTT Broker │────►│ Node-RED /   │
│ (100 devices)│     │ (Mosquitto) │     │ Cloud ingest │
└──────────────┘     └─────────────┘     └──────────────┘
```

**Workflow recomendado:**

1. **Fase 1:** Simulador Python → validar schema JSON e dashboard
2. **Fase 2:** Wokwi ou placa real → validar firmware
3. **Fase 3:** HIL com sensor real + resto simulado
4. **Fase 4:** Piloto em campo com subset de dispositivos

---

## 6. Validação de simuladores

Um simulador útil deve permitir verificar:

- [ ] Schema JSON aceite pelo consumer
- [ ] Frequência de publish dentro dos limites do broker
- [ ] Alertas disparam com valores limite
- [ ] Sistema recupera após simulação de outage
- [ ] IDs de dispositivo únicos e consistentes

---

## 7. Limitações — quando não chega simulação

- Comportamento RF (interferência, alcance LoRa)
- Consumo energético real em duty cycle complexo
- EMI e ruído eléctrico em ambiente industrial
- Latência de rede móvel variable

**Conclusão:** simulação acelera dev; **sempre** validar com hardware representativo antes de produção.

---

## Exercícios

### Exercício 1
Define com precisão a diferença entre simulação de dados, emulação de hardware e sensor virtual. Dá um exemplo de cada no contexto de monitorização de qualidade do ar.

### Exercício 2
Escreve um script Python que gera leituras de humidade (% RH) com random walk: valor inicial 50, cada step ±0.5, clamp entre 20 e 80.

### Exercício 3
Como testarias no CI (sem hardware) que o firmware publica MQTT no tópico correcto quando temperatura > 40°C?

### Exercício 4
Desenha uma arquitectura HAL em pseudocódigo C que permita compilar o mesmo projecto para `SIMULATION` e `PRODUCTION`.

### Exercício 5
Lista quatro propriedades estatísticas que telemetria simulada de temperatura ambiente deveria reproduzir para ser credível.

### Exercício 6
Simulas 500 dispositivos MQTT. Que problemas de infraestrutura podem surgir no broker e como os detectarias?

### Exercício 7
Compara usar **replay de CSV histórico** vs. **gerador estocástico** para testar algoritmo de manutenção preditiva.

### Exercício 8
Propõe cenário de teste que combine simulação de dados com inject Node-RED para demonstrar falha de gateway (buffer offline).

---

## Soluções

### Solução 1

| Conceito | Definição | Exemplo qualidade ar |
|----------|-----------|----------------------|
| Simulação dados | Gera valores numéricos sem firmware | Script produz CO₂ ppm com média 800 + ruído |
| Emulação HW | Executa código em MCU virtual | Wokwi corre sketch que lê sensor MQ135 virtual |
| Sensor virtual | API idêntica ao driver real, backend substituível | `read_co2()` lê de REST `/sim/co2` em dev |

### Solução 2

```python
import random

humidity = 50.0

while True:
    humidity += random.uniform(-0.5, 0.5)
    humidity = max(20.0, min(80.0, humidity))
    print(f"humidity={humidity:.2f}")
    # time.sleep(1)  # opcional
```

### Solução 3

1. Compilar firmware com flag `SIMULATION` e função `get_temp()` injectável
2. Teste host-side (PlatformIO Unity): mock `get_temp()` retorna 41.0 → verificar que `mqtt_publish` foi chamado com tópico `alert/high_temp`
3. Alternativa integração: simulador Python publica no broker; consumer cloud testa regra — não testa firmware directamente mas testa pipeline

Combinação ideal: unitário no firmware + integração no broker.

### Solução 4

```c
// sensor_hal.h
float hal_read_temperature(void);
void hal_init(void);

// sensor_hal_sim.c  (#ifdef SIMULATION)
static float sim_temp = 22.0;
float hal_read_temperature(void) { return sim_temp; }
void hal_set_sim_temp(float t) { sim_temp = t; }  // testes

// sensor_hal_bme280.c  (#else)
float hal_read_temperature(void) { return bme280_read_temp(); }

// main.c — idêntico em ambos
void loop() {
    float t = hal_read_temperature();
    if (t > 40) mqtt_publish_alert(t);
}
```

Build: `gcc -DSIMULATION` vs. `pio run -e production`.

### Solução 5

1. **Média** próxima da temperatura ambiente real (~20–25°C interior)
2. **Variância** pequena but não zero (±0.5–2°C)
3. **Autocorrelação** — valores consecutivos correlacionados (não i.i.d.)
4. **Sazonalidade diária** — ciclo lento 24 h (opcional mas credível)
5. (Bonus) **Outliers raros** para testar robustez

### Solução 6

| Problema | Detecção |
|----------|----------|
| Limite conexões MQTT | `$SYS/broker/clients/max`, rejeições |
| CPU/RAM broker saturados | `top`, métricas container |
| Rate limiting / throttling cloud | HTTP 429, lag consumer |
| Colisão client IDs | Logs disconnect "already connected" |
| Disco cheio (persistência QoS) | Espaço disco, `$SYS/broker/store/messages/count` |

Mitigação: connection pooling, shared subscriptions, batching, broker cluster.

### Solução 7

| Abordagem | Prós | Contras |
|-----------|------|---------|
| Replay CSV | Dados reais; reproduz incidentes históricos | Não gera cenários novos; pode overfit |
| Estocástico | Infinitos cenários; stress edge cases | Pode não reflectir física real |

**Manutenção preditiva:** combinar — treinar/validar com histórico real; stress test com simulador estocástico que injecta falhas sintéticas.

### Solução 8

**Cenário buffer offline:**

1. Simulador Python publica 10 msg/min em `factory/line1/#`
2. Node-RED gateway flow persiste em SQLite se cloud unreachable
3. **Inject Node-RED** simula outage: `function` node bloqueia HTTP forward por 15 min (`global.set('cloud_down', true)`)
4. Durante outage, verificar SQLite row count aumenta
5. Inject restaura cloud → verificar flush batch para API
6. Dashboard Grafana mostra gap zero após flush (dados contínuos)

---

## Referências

- Andy King — *Programming the Internet of Things* (Part II)
- [Wokwi Documentation](https://docs.wokwi.com/)
- [ROADMAP da UC](../ROADMAP.md)
