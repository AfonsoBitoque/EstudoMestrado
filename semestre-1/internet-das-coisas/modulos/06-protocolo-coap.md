# Módulo 06 — Protocolo CoAP

**UC:** Internet das Coisas · **Parte III** · Tempo sugerido: 4–6 h

---

## Objetivos de aprendizagem

- Descrever CoAP como protocolo RESTful para dispositivos constrained
- Comparar CoAP com MQTT e HTTP no contexto IoT
- Explicar observe, block transfer e mecanismos de fiabilidade UDP
- Identificar cenários adequados para deploy CoAP

---

## 1. Introdução ao CoAP

**CoAP (Constrained Application Protocol)** — RFC 7252 — é um protocolo **application-layer** optimizado para dispositivos com **recursos severamente limitados** (RAM de KB, duty cycle radio baixo).

### Características principais

| Aspeto | CoAP |
|--------|------|
| Transporte | **UDP** (puerto 5683) — também DTLS |
| Modelo | **Request/Response** RESTful |
| Overhead | Cabeçalho mínimo 4 bytes |
| Formato dados | JSON, CBOR, plain text |
| Multicast | Suportado (UDP) |
| Proxy | CoAP-to-HTTP bridging |

CoAP traz semântica **web** (URI, métodos) ao mundo constrained sem overhead de HTTP completo.

---

## 2. Modelo RESTful

CoAP usa métodos análogos a HTTP:

| Método | Função | Exemplo |
|--------|--------|---------|
| GET | Ler recurso | `GET coap://[fd00::1]/sensors/temp` |
| POST | Criar / actuar | POST comando |
| PUT | Actualizar recurso | PUT configuração |
| DELETE | Remover | DELETE registo |

### 2.1 URIs e recursos

Recursos identificados por **URI**:

```
coap://sensor.local/temperature
coap://sensor.local/actuators/relay1
```

Dispositivo expõe **recursos** — servidor CoAP embebido no sensor.

### 2.2 Códigos de resposta

Similar HTTP:

| Código | Significado |
|--------|-------------|
| 2.05 Content | GET sucesso com payload |
| 2.04 Changed | PUT/POST sucesso |
| 4.04 Not Found | Recurso inexistente |
| 4.00 Bad Request | Payload inválido |
| 5.00 Internal Server Error | Erro dispositivo |

Formato `class.detail` (ex.: 2.05 = success + 05).

---

## 3. CoAP vs. MQTT vs. HTTP

| Critério | CoAP | MQTT | HTTP/1.1 |
|----------|------|------|----------|
| Transporte | UDP | TCP | TCP |
| Padrão | Request/Response | Pub/Sub | Request/Response |
| Overhead | Muito baixo | Baixo | Alto |
| Multicast | Sim | Não | Não |
| Push servidor | Observe (RFC 7641) | Native pub/sub | WebSocket/SSE |
| NAT traversal | Desafiante (UDP) | TCP mais fácil | TCP mais fácil |

**Quando CoAP:**
- Rede mesh IPv6 (6LoWPAN)
- Dispositivos que **servem** recursos (sensor consultável)
- Multicast descoberta de serviços
- 802.15.4 com frames pequenos

**Quando MQTT:**
- Telemetria push contínua para cloud
- Muitos publishers → poucos subscribers
- Infraestrutura TCP estável

---

## 4. Fiabilidade sobre UDP

UDP não garante entrega. CoAP inclui:

### 4.1 Confirmable (CON) vs. Non-confirmable (NON)

- **CON:** requer ACK do destinatário; retransmissão exponencial backoff se timeout
- **NON:** fire-and-forget como QoS 0 MQTT

### 4.2 Message IDs

Correlacionar requests/responses e detectar duplicados.

### 4.3 Separación mensagem vs. request

Camada CoAP distingue **empty ACK** (mensagem recebida) de **response** (resultado da operação) — permite respostas lentas (sensor demora a ler).

---

## 5. Observe (RFC 7641)

**Problema:** GET polling desperdiça energia e bandwidth.

**Solução Observe:** cliente envia GET com opção `Observe: 0`; servidor **notifica** quando recurso muda.

```
Client ──GET /temp [Observe:0]──► Server
Client ◄──2.05 Content (22°C)──── Server
Client ◄──2.05 Content (23°C)──── Server  (push)
Client ◄──2.05 Content (23.5°C)── Server
```

Similar a **MQTT subscribe** mas sobre modelo REST de recursos.

Cancelar: GET com `Observe: 1` ou timeout.

---

## 6. Block Transfer (RFC 7959)

Payloads grandes (firmware, logs) não cabem num único datagrama UDP (~ MTU 1200 bytes em 6LoWPAN).

**Block-wise transfer:** troca de blocos numerados até transferência completa.

```
GET /logs [Block2: 0] → block 0/N
GET /logs [Block2: 1] → block 1/N
...
```

Essencial para **OTA firmware** e dumps de diagnóstico em CoAP.

---

## 7. Segurança — DTLS

CoAP usa **DTLS** (TLS sobre UDP) — porto 5684.

- Pre-shared key (PSK) — comum em dispositivos simples
- Raw public key
- Certificados (como TLS MQTT)

Sem DTLS, CoAP é **texto claro** — inaceitável em produção externa.

---

## 8. CoAP proxy e HTTP mapping

**CoAP-HTTP proxy** traduz:

```
HTTP GET https://gateway/sensors/temp
    → CoAP GET coap://[ipv6]/temp
    → resposta mapeada para HTTP 200
```

Permite integração com sistemas web existentes sem MQTT.

**libcoap**, **aiocoap** (Python), **Californium** (Java) — implementações populares.

---

## 9. Arquitectura típica CoAP

```
┌─────────────┐  6LoWPAN   ┌─────────────┐  HTTPS   ┌───────┐
│ CoAP sensors│◄──────────►│ Border Router│◄────────►│ Cloud │
│ (UDP 5683)  │            │ + CoAP proxy │          │       │
└─────────────┘            └─────────────┘          └───────┘
```

Border router (contiki-ng, OpenThread) faz routing IPv6 e proxy.

---

## 10. Exemplo aiocoap (Python)

```python
import asyncio
from aiocoap import Context, Message, GET

async def read_temp():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://[::1]/temperature')
    response = await protocol.request(request).response
    print(response.payload.decode())

asyncio.run(read_temp())
```

---

## Exercícios

### Exercício 1
Explica porque CoAP usa UDP em vez de TCP para dispositivos 802.15.4.

### Exercício 2
Compara Observe CoAP com subscrição MQTT. Semelhanças e diferenças.

### Exercício 3
Um sensor envia payload de 4 KB mas MTU é 1280 bytes. Que mecanismo CoAP usas?

### Exercício 4
Para alarme de inundação em cave (1 leitura/min, bateria 5 anos, IPv6 mesh), CoAP ou MQTT? Justifica.

### Exercício 5
Descreve handshake CON com retransmissão quando ACK se perde.

### Exercício 6
Mapeia operação "ligar relé" para método CoAP, URI e payload JSON.

### Exercício 7
Quais desafios de NAT/firewall com CoAP UDP e como mitigar?

### Exercício 8
Desenha arquitectura com 20 sensores CoAP, border router e cloud HTTP.

---

## Soluções

### Solução 1

802.15.4 tem frames **máx. 127 bytes** — TCP overhead (headers, state, retransmissões) é pesado. UDP permite datagramas pequenos alinhados com radio. CoAP CON fornece fiabilidade **selectiva** só quando necessário, poupando energia vs. TCP always-on. Dispositivos sleeping frequentemente acordam, enviam NON/CON, voltam a dormir — TCP manteria conexão cara.

### Solução 2

| | CoAP Observe | MQTT Subscribe |
|---|--------------|----------------|
| Modelo | Recurso REST `/temp` | Tópico `sensor/temp` |
| Transporte | UDP + CON notifications | TCP persistente |
| Broker | Direct device (ou proxy) | Broker central obrigatório |
| Filtros | Por recurso URI | Wildcards tópicos |
| Estado | GET inicial + updates | Retained opcional |

Semelhança: push assíncrono de mudanças. Diferença: CoAP server-centric REST; MQTT broker-centric pub/sub.

### Solução 3

**Block Transfer (RFC 7959)** — Block2 para response em blocos de ≤ MTU-safe size até 4 KB completos.

### Solução 4

**CoAP** preferível:
- Mesh IPv6 6LoWPAN típico em building automation
- 1 leitura/min → request/response ou Observe eficiente
- UDP + sleep alinha com bateria longa
- Multicast descoberta na instalação

MQTT sobre TCP manteria conexões caras; overhead broker pode estar na border router como proxy se necessário.

### Solução 5

1. Client envia CON GET `/temp` (MID=1234)
2. Timeout sem resposta → retransmite CON GET MID=1234 (backoff)
3. Server recebe (pode ser duplicado) → responde ACK MID=1234
4. Server processa → envia CON response 2.05 payload (MID=5678)
5. Client ACK MID=5678
Se ACK passo 3 perdido, client retransmite; server deduplica por MID.

### Solução 6

```
Method: PUT ou POST
URI: coap://device/actuators/relay1
Payload: {"state":"ON"}
Content-Format: application/json
Response esperada: 2.04 Changed
```

PUT idempotente se relay1 é recurso com estado definido.

### Solução 7

**Desafios:** UDP não atravessa NAT stateful facilmente; firewalls bloqueiam 5683; endereços IPv6 mesh não routáveis na Internet.

**Mitigações:**
- Border router com túnel IPv6 ou CoAP-HTTP proxy na rede edge
- DTLS + PSK
- MQTT/HTTP na border como uplink (híbrido)
- NAT traversal limitado — evitar CoAP direct-to-Internet de behind NAT residencial

### Solução 8

```
[20× CoAP sensors] ──6LoWPAN mesh──► [Border Router]
                                         │
                         CoAP proxy + DTLS termination
                                         │
                         HTTPS REST ────► [Cloud API]
                                         │
                         Observe notifications agregadas
                                         ▼
                                    [TimescaleDB / Grafana]
```

Sensors expõem `/temp`, `/battery`. Border router subscreve Observe ou faz polling agregado; cloud só vê HTTP/JSON.

---

## Referências

- [RFC 7252 — CoAP](https://datatracker.ietf.org/doc/html/rfc7252)
- [RFC 7641 — Observe](https://datatracker.ietf.org/doc/html/rfc7641)
- [RFC 7959 — Block Transfer](https://datatracker.ietf.org/doc/html/rfc7959)
- [aiocoap](https://aiocoap.readthedocs.io/)
- [ROADMAP da UC](../ROADMAP.md)
