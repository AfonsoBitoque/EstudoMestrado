# Módulo 08 — Segurança IoT

**UC:** Internet das Coisas · **Parte III** · Tempo sugerido: 5–7 h

---

## Objetivos de aprendizagem

- Identificar vulnerabilidades comuns em dispositivos e ecossistemas IoT
- Implementar identidade de dispositivo, TLS e práticas de autenticação
- Compreender secure boot e cadeia de confiança em firmware
- Aplicar defesa em profundidade numa arquitectura IoT completa

---

## 1. Porquê segurança IoT é crítica

Dispositivos IoT são **alvos atractivos**:

- Deploy massivo — milhões de endpoints
- Firmware desactualizado durante anos
- Credenciais default (`admin/admin`)
- Acesso físico em locais expostos
- Botnets (Mirai, Mozi) — DDoS via câmaras/routers comprometidos

**Impacto:** privacidade (câmaras), safety (industrial, médico), disponibilidade (DDoS), financeiro (ransomware).

---

## 2. Modelo de ameaças STRIDE (aplicado à IoT)

| Ameaça | IoT exemplo |
|--------|-------------|
| **Spoofing** | Dispositivo falso publica telemetria |
| **Tampering** | MITM altera comando "unlock door" |
| **Repudiation** | Negar envio de comando |
| **Information Disclosure** | Sniff MQTT plain text |
| **Denial of Service** | Flood broker; brick devices |
| **Elevation of Privilege** | Exploit firmware → root |

---

## 3. Identidade de dispositivo

Cada dispositivo precisa **identidade única e verificável**.

### 3.1 Identificadores

| Método | Força | Notas |
|--------|-------|-------|
| MAC address | Fraco | Spoofável |
| UUID software | Médio | Clonável se sem hardware root |
| **X.509 certificate** | Forte | mTLS, rotação |
| **TPM / secure element** | Muito forte | Chave nunca exportável |

### 3.2 Provisioning

1. Fábrica injecta certificado único em secure element
2. First boot: device prova identidade ao cloud (EST, AWS Fleet Provisioning)
3. Cloud emite credenciais MQTT scoped (ACL tópicos)

**Nunca** hardcode passwords iguais em todos os dispositivos.

### 3.3 Zero Trust

Não confiar na rede interna. Autenticar **cada** conexão dispositivo-broker-cloud.

---

## 4. TLS e encriptação

### 4.1 TLS em IoT

| Protocolo | Porta | Uso |
|-----------|-------|-----|
| MQTT over TLS | 8883 | Telemetria encriptada |
| HTTPS | 443 | REST API |
| DTLS | 5684 | CoAP seguro |
| WPA3 | — | Wi-Fi link layer |

TLS protege **confidencialidade** e **integridade** em trânsito.

### 4.2 Certificados em dispositivos constrained

- **mbedTLS** / **wolfSSL** — stacks leves
- Cipher suites eficientes: **TLS 1.2+**, evitar RSA pesado — preferir **ECDSA P-256**
- **Certificate pinning** — aceitar só CA da organização
- Rotação antes expiração (monitorar `notAfter`)

### 4.3 Encriptação at-rest

Dados sensíveis em flash:

- **AES-256** com chave em secure element
- Flash encryption (ESP32 feature)
- Encrypted SQLite no gateway

---

## 5. Secure Boot

**Secure boot** garante que dispositivo só executa **firmware autêntico e íntegro**.

### 5.1 Cadeia de confiança

```
ROM bootloader (imutável, chave pública OEM)
    ↓ verifica assinatura
2nd stage bootloader
    ↓ verifica assinatura
Application firmware
    ↓ verifica assinatura (opcional)
OTA updates
```

### 5.2 Mecanismos

| Plataforma | Tecnologia |
|------------|------------|
| ESP32 | Secure Boot V2, flash encryption |
| STM32 | ST secure boot, TrustZone |
| ARM | PSA Certified, TF-M |

Firmware unsigned ou modificado → **refusa boot** — impede malware persistente.

### 5.3 Assinatura OTA

- Build server assina `.bin` com chave privada (HSM)
- Dispositivo verifica com chave pública em eFuse
- Rollback protection — anti-downgrade para versão vulnerável

---

## 6. Vulnerabilidades comuns IoT

### 6.1 OWASP IoT Top 10 (resumo)

1. Passwords fracos/default
2. Insecure network services
3. Insecure ecosystem interfaces
4. Lack of secure update mechanism
5. Use of insecure/outdated components
6. Insufficient privacy protection
7. Insecure data transfer/storage
8. Lack of device management
9. Insecure default settings
10. Lack of physical hardening

### 6.2 Casos reais

| Incidente | Lição |
|-----------|-------|
| **Mirai (2016)** | Telnet default creds → botnet |
| **Ring cameras** | Credenciais vazadas, acesso não autorizado |
| **Stuxnet** | Air-gap bypass via USB — industrial |
| **Verkada (2021)** | Super admin credentials expostas |

### 6.3 Superfície de ataque expandida

```
[Device firmware] ← USB, UART debug, JTAG
[Radio: Wi-Fi, BLE, Zigbee]
[Cloud API]
[Mobile app]
[Supply chain — dependências]
[Physical — extrair flash]
```

---

## 7. Defesa em profundidade

```
┌─────────────────────────────────────────────────────────┐
│ Camada 1: Hardware — TPM, secure boot, flash encryption │
├─────────────────────────────────────────────────────────┤
│ Camada 2: Firmware — signed OTA, no debug prod          │
├─────────────────────────────────────────────────────────┤
│ Camada 3: Rede — TLS, VLAN, firewall, no port forward    │
├─────────────────────────────────────────────────────────┤
│ Camada 4: Aplicação — ACL MQTT, input validation        │
├─────────────────────────────────────────────────────────┤
│ Camada 5: Cloud — IAM, audit logs, anomaly detection    │
└─────────────────────────────────────────────────────────┘
```

### 7.1 Hardening prático

- Desactivar UART debug em produção (`CONFIG_ESP_CONSOLE_NONE`)
- ACL broker: device X só publica `devices/X/#`
- Rate limiting ingestão
- Segregação rede IoT (VLAN separada)
- Monitorização: tentativas auth falhadas
- SBOM (Software Bill of Materials) para CVE tracking

---

## 8. Autenticação MQTT segura

```conf
# mosquitto.conf
listener 8883
cafile /etc/mosquitto/ca.crt
certfile /etc/mosquitto/server.crt
keyfile /etc/mosquitto/server.key
require_certificate true
use_identity_as_username true
```

Dispositivo apresenta certificado client; broker usa CN como username; ACL por CN.

---

## 9. Resposta a incidentes IoT

1. **Isolar** dispositivo (revogar cert MQTT)
2. **Analisar** logs broker/cloud
3. **Patch** OTA fleet ou recall físico
4. **Rotacionar** credenciais/chaves comprometidas
5. **Post-mortem** — actualizar threat model

---

## 10. Compliance e regulamentação

- **GDPR** — dados pessoais, consentimento, DPIA
- **NIS2** — infra crítica EU
- **FDA** — dispositivos médicos IoT
- **IEC 62443** — segurança industrial

---

## Exercícios

### Exercício 1
Explica por que Mirai teve sucesso massivo e três medidas que o teriam mitigado.

### Exercício 2
Compara autenticação MQTT username/password vs. mTLS para fleet de 50 000 dispositivos.

### Exercício 3
Descreve fluxo secure boot desde power-on até application running no ESP32.

### Exercício 4
Atacante com acesso físico ao ESP32. Que vectores de ataque existem e contramedidas?

### Exercício 5
Desenha ACL MQTT para tenant multi-tenant SaaS: tenant A não vê dados tenant B.

### Exercício 6
Lista cinco checks de security review antes de deploy OTA firmware v2.0.

### Exercício 7
Diferencia encriptação in-transit vs. at-rest com exemplo IoT cada.

### Exercício 8
Propõe arquitectura zero-trust para smart hospital: sensores paciente → nurse station → cloud.

---

## Soluções

### Solução 1

**Sucesso Mirai:** scanning massivo IPs; credenciais default telnet/SSH (`admin/admin`, `root/root`); dispositivos expostos Internet; sem rate limit; firmware nunca actualizado.

**Mitigações:**
1. Proibir credenciais default — forced password change first boot
2. Fechar telnet; só SSH com keys ou desactivar admin remoto
3. Firewall/ACL — dispositivos não routáveis publicamente
4. (Bonus) mTLS + network segmentation

### Solução 2

| | Username/Password | mTLS |
|---|-----------------|------|
| Segurança | Média — secret em flash clonável | Alta — chave privada protegida |
| Escala 50k | Rotação passwords nightmare | PKI + auto-provisioning |
| Revogação | Mudar password OTA | CRL/OCSP revogar cert |
| Overhead | Baixo | CPU TLS maior |
| Gestão | Simples inicial | Complexo but automatable |

**50k devices:** mTLS + Fleet Provisioning (AWS/Azure) — password único por device inviável manualmente.

### Solução 3

1. Power-on → ROM bootloader (eFuse secure boot enable)
2. ROM verifica assinatura RSA/ECDSA 2nd stage bootloader
3. 2nd stage verifica assinatura partition table + app
4. Se qualquer verificação falha → halt / reset
5. App inicia; flash encryption decrypt on-the-fly
6. OTA update verifica assinatura antes swap partition

### Solução 4

| Ataque | Contramedida |
|--------|--------------|
| UART console root | Disable console prod; secure boot |
| Flash dump SPI | Flash encryption; epoxy encapsulation |
| Glitching fault injection | Secure element; sensors |
| JTAG debug | Blow fuses disable JTAG |
| Replacing flash chip | Secure boot signature mismatch |

Defesa: secure boot + flash encryption + disable debug + tamper-evident enclosure.

### Solução 5

```
# Estrutura tópicos
tenants/{tenant_id}/devices/{device_id}/telemetry
tenants/{tenant_id}/devices/{device_id}/commands

# ACL user device-tenantA-001
topic write tenants/tenantA/devices/device-tenantA-001/#
topic read tenants/tenantA/devices/device-tenantA-001/commands/#

# ACL user dashboard-tenantA
topic read tenants/tenantA/#
topic write tenants/tenantA/+/commands/#  # com validação server-side

# Broker rejeita cross-tenant por prefix match
```

Cloud API também filtra por tenant_id do JWT — defesa dupla.

### Solução 6

1. Firmware assinado criptograficamente verificado em CI
2. Testes regressão + rollback partition disponível
3. Staged rollout — 5% fleet canary antes 100%
4. Sem credenciais hardcoded novas no diff
5. Changelog CVE dependências (SBOM scan)
6. (Bonus) Version >= minimum anti-rollback eFuse

### Solução 7

**In-transit:** MQTT TLS 8883 entre ESP32 e broker — sniff Wi-Fi não revela payload `{patient_id, heart_rate}`.

**At-rest:** histórico health data encriptado AES-256 em PostgreSQL/cloud storage — backup disk stolen não legível sem KMS key.

### Solução 8

```
[Patient sensors] ──BLE encrypted──► [Bedside gateway/nurse station]
         mTLS device cert              │ local HL7/FHIR buffer
         no direct Internet             │ VLAN isolada hospital
                                        ▼
                              [Hospital IoT broker — on-prem]
                                        │ mTLS + private link
                                        ▼
                              [Cloud — anonymized aggregates only]
```

Princípios: identidade por dispositivo; micro-segmentation VLAN; dados identificáveis ficam on-prem edge; cloud analytics só com pseudonymization; audit log imutável; revogação cert instantânea por paciente alta.

---

## Referências

- [OWASP IoT Project](https://owasp.org/www-project-internet-of-things/)
- [NISTIR 8259 — IoT Device Cybersecurity](https://csrc.nist.gov/publications/detail/nistir/8259/final)
- [ESP32 Secure Boot](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/secure-boot-v2.html)
- [ROADMAP da UC](../ROADMAP.md)
