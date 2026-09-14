# Módulo 05 — Protocolos de Transferência: MQTT

**UC:** Internet das Coisas · **Parte III** · Tempo sugerido: 6–8 h

---

## Objetivos de aprendizagem

- Explicar o modelo publish/subscribe do MQTT e a sua adequação à IoT
- Configurar tópicos, QoS, retained messages e Last Will Testament
- Operar brokers (Mosquitto) e clientes para telemetria e comandos
- Aplicar boas práticas de segurança e design de tópicos

---

## 1. Introdução ao MQTT

**MQTT (Message Queuing Telemetry Transport)** é um protocolo de mensagens **leve**, **publish/subscribe**, optimizado para redes instáveis e dispositivos com recursos limitados. Standard OASIS, muito usado em IoT.

### 1.1 Porquê MQTT na IoT?

| Característica | Benefício |
|----------------|-----------|
| Binário compacto | Poucos bytes overhead |
| Pub/Sub desacoplado | Dispositivos não conhecem consumidores |
| QoS configurável | Equilíbrio fiabilidade vs. performance |
| Sessões persistentes | Recuperação após disconnect |
| Last Will | Detecção automática de offline |

Funciona sobre **TCP** (porta 1883 plain, **8883 TLS**). MQTT over WebSockets (8083/8084) para browsers.

---

## 2. Modelo Publish/Subscribe

```
┌──────────┐  publish      ┌─────────┐  forward    ┌──────────┐
│ Publisher│──────────────►│  BROKER │────────────►│Subscriber│
│ (sensor) │  topic/data   │Mosquitto│  topic/data │(dashboard│
└──────────┘               └─────────┘             └──────────┘
```

- **Publisher** envia mensagem para um **tópico** — não sabe quem recebe
- **Subscriber** subscreve tópico(s) — recebe todas mensagens publicadas
- **Broker** roteia mensagens; único ponto central (pode cluster)

**Diferença de HTTP:** MQTT é **push** persistente; HTTP é request/response.

---

## 3. Tópicos (Topics)

### 3.1 Estrutura hierárquica

Tópicos são strings UTF-8 separadas por `/`:

```
farm/greenhouse-01/temperature
farm/greenhouse-01/humidity
home/living/light/status
home/living/light/set
```

### 3.2 Wildcards (apenas no subscribe)

| Wildcard | Significado | Exemplo subscribe | Match |
|----------|-------------|-------------------|-------|
| `+` | Um nível | `farm/+/temperature` | `farm/gh01/temperature` |
| `#` | Zero ou mais níveis | `farm/#` | Tudo sob `farm/` |

**Publish nunca usa wildcards** — só subscritores.

### 3.3 Boas práticas de design

```
{site}/{device_id}/{metric}
{tenant}/{location}/{device}/{stream}
```

- Evitar tópico único global (`/data`) — gargalo e ACL difícil
- Separar **telemetry** vs. **commands** vs. **status**
- Não incluir dados variáveis no tópico (usar payload JSON)
- Documentar namespace da organização

---

## 4. Níveis de QoS (Quality of Service)

MQTT define **três níveis** de entrega:

| QoS | Nome | Garantia | Overhead | Uso típico |
|-----|------|----------|----------|------------|
| 0 | At most once | Fire-and-forget | Mínimo | Telemetria frequente tolerante a perda |
| 1 | At least once | Entrega garantida; possíveis duplicados | Médio | Alertas, comandos importantes |
| 2 | Exactly once | Entrega única | Máximo | Billing, transacções (raro em IoT) |

### 4.1 QoS 0 — At most once

Publisher envia; broker entrega se possível; **sem ACK**. Perda silenciosa se rede cair.

### 4.2 QoS 1 — At least once

**PUBACK** confirma recepção. Reenvio se timeout. Subscriber pode receber **duplicados** — consumer deve ser idempotente.

### 4.3 QoS 2 — Exactly once

Handshake de 4 passos (PUBREC, PUBREL, PUBCOMP). Raro em IoT por overhead; usar quando duplicados são inaceitáveis.

### 4.4 QoS publish vs. subscribe

Negociação: effective QoS = **min(publish QoS, subscribe QoS)**.

---

## 5. Brokers

### 5.1 Funções do broker

- Autenticação e autorização (ACL)
- Roteamento por tópico
- Persistência (sessões, QoS 1/2, retained)
- Bridge para outro broker
- Métricas `$SYS/#`

### 5.2 Eclipse Mosquitto

Broker open-source popular:

```bash
# Docker
docker run -d -p 1883:1883 -p 9001:9001 eclipse-mosquitto

# Publicar
mosquitto_pub -h localhost -t "test/topic" -m "hello" -q 1

# Subscrever
mosquitto_sub -h localhost -t "test/#" -v
```

**Ficheiros config:** `mosquitto.conf`, `passwd`, `acl`.

### 5.3 Brokers cloud

HiveMQ Cloud, AWS IoT Core (MQTT), Azure IoT Hub, EMQX — escalabilidade managed.

---

## 6. Retained Messages

Flag **retain** na publish: broker **guarda última mensagem** por tópico.

Novo subscriber recebe **imediatamente** último valor — útil para **estado actual** (luz ON/OFF) sem polling.

```bash
mosquitto_pub -t "home/light/status" -m "ON" -r
```

- Apenas **uma** mensagem retained por tópico
- Publicar payload **vazio com retain** apaga retained message
- Não confundir com persistência de histórico

---

## 7. Last Will and Testament (LWT)

Ao **conectar**, cliente define:

- **will_topic**
- **will_payload**
- **will_qos**
- **will_retain**

Se cliente desconectar **inesperadamente** (sem DISCONNECT), broker publica will message.

**Uso clássico:** `device/esp32-01/status` → `"offline"`

Combinar com heartbeat periódico `"online"` para estado completo.

```python
# Pseudocódigo Paho
client.will_set("device/esp32-01/status", payload="offline", qos=1, retain=True)
client.connect("broker", 1883)
client.publish("device/esp32-01/status", "online", retain=True)
```

---

## 8. Sessões e Clean Session

- **Clean Session = true:** broker descarta subscrições e filas QoS ao disconnect
- **Clean Session = false:** sessão persistente; mensagens QoS 1/2 em fila enquanto offline (dentro limites)

MQTT 5.0 introduz **Session Expiry** mais granular.

---

## 9. Segurança MQTT (resumo)

| Mecanismo | Descrição |
|-----------|-----------|
| TLS | Encriptação transporte (8883) |
| Username/password | Autenticação básica |
| Client certificates | mTLS por dispositivo |
| ACL | Restringir publish/subscribe por tópico |

Nunca MQTT plain em produção na Internet pública.

---

## 10. Exemplo telemetria + comando

```
# Telemetria (QoS 0, sem retain)
Topic: factory/line1/temp
Payload: {"value":72.3,"unit":"C","ts":"2026-09-14T10:00:00Z"}

# Comando (QoS 1)
Topic: factory/line1/relay/set
Payload: {"channel":2,"state":"ON"}

# ACK estado (retain)
Topic: factory/line1/relay/status
Payload: {"channel":2,"state":"ON"}
```

---

## Exercícios

### Exercício 1
Explica pub/sub MQTT comparando com HTTP REST para 500 sensores a publicar a cada 5 s.

### Exercício 2
Dado namespace `building/floor/room/device/metric`, propõe tópicos para temperatura, comando HVAC e LWT offline.

### Exercício 3
Que QoS escolhes para: (a) heartbeat 1/min, (b) alarme incêndio, (c) leitura temp cada 10 s? Justifica.

### Exercício 4
Um subscriber liga-se com QoS 2 mas publisher usa QoS 0. Qual effective QoS?

### Exercício 5
Descreve cenário onde retained message causa comportamento incorrecto e como evitar.

### Exercício 6
Configura LWT + retained online para dispositivo `sensor-42`. Escreve tópicos, payloads e sequência connect/disconnect.

### Exercício 7
Como detectarias no broker que 100 dispositivos publicam com mesmo `client_id`?

### Exercício 8
Desenha ACL Mosquitto: dispositivo `esp32-01` só publica em `farm/esp32-01/#` e subscreve `farm/esp32-01/commands/#`.

---

## Soluções

### Solução 1

**MQTT:** sensores publicam fire-and-forget; cloud subscreve `sensors/#`; zero polling; conexão persistente multiplexada; escala com fan-out nativo.

**HTTP REST:** 500 POST/5s = 100 req/s contínuos; cada sensor precisa resolver DNS, TLS handshake frequente se sem keep-alive; cloud expõe endpoint por dispositivo ou batch complexo; ineficiente energeticamente.

MQTT adequado para telemetria push contínua; REST melhor para queries ad-hoc e integração com sistemas request/response.

### Solução 2

| Finalidade | Tópico |
|------------|--------|
| Temperatura | `building/2/office-A/sensor-01/temperature` |
| Comando HVAC | `building/2/office-A/hvac/set` |
| LWT offline | `building/2/office-A/sensor-01/status` → `"offline"` |
| Online (retain) | mesmo tópico status → `"online"` |

### Solução 3

| Caso | QoS | Motivo |
|------|-----|--------|
| Heartbeat | 0 | Perda ocasional OK; próximo em 1 min; mínimo overhead |
| Alarme incêndio | 1 ou 2 | Crítico entregar; 1 suficiente se consumer idempotente |
| Temp 10 s | 0 | Alta frequência; perda isolada irrelevante; histórico contínuo |

### Solução 4

**Effective QoS = min(0, 2) = 0.** Entrega at-most-once apesar do subscriber preferir QoS 2.

### Solução 5

**Cenário:** retained `home/alarm/status = "TRIGGERED"` de teste. Novo subscriber (app) mostra alarme activo mesmo após alarme resolvido se ninguém publicou retain `"CLEAR"`.

**Evitar:** sempre publicar estado actual com retain após clear; ou não usar retain em eventos transientes; usar retain só para estado steady (ON/OFF).

### Solução 6

```
will_topic: device/sensor-42/status
will_payload: {"state":"offline"}
will_qos: 1
will_retain: true

Sequência:
1. CONNECT com will configurado
2. PUBLISH retain QoS1 device/sensor-42/status {"state":"online"}
3. Operar normalmente — heartbeat opcional
4. Disconnect inesperado (queda energia)
5. Broker publica will → status offline (retained)
6. Reconnect → passo 2 restaura online
```

### Solução 7

- Logs Mosquitto: `"Socket error on client X, disconnecting"` e reconnections frequentes
- Dois clientes mesmo ID: broker **desconecta** sessão anterior (MQTT 3.1.1)
- Métrica `$SYS/broker/clients/connected` flutua
- `mosquitto_sub -t '$SYS/broker/log/#' -v` se logging activo
- Auditar provisioning — client_id deve ser único por dispositivo (MAC, UUID)

### Solução 8

```
# aclfile exemplo Mosquitto
user esp32-01
topic write farm/esp32-01/#
topic read farm/esp32-01/commands/#

# Proibir write noutros tópicos — default deny se configurado
```

Complementar autenticação `password_file` e listener TLS na porta 8883.

---

## Referências

- [MQTT.org](https://mqtt.org/)
- [OASIS MQTT Version 3.1.1](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)
- [Eclipse Mosquitto](https://mosquitto.org/man/mosquitto-conf-5.html)
- [ROADMAP da UC](../ROADMAP.md)
