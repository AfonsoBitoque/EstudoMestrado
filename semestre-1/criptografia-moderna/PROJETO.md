# Projeto — Criptografia Moderna (70%)

**Docente:** Daniel Graça · Enunciado base: Project.pdf (local, não publicar)

## Formato

| Entregável | Detalhe |
|------------|---------|
| **Relatório escrito** | ~20–30 páginas |
| **Apresentação** | Defesa individual (validação da nota) |
| **Nota** | Individual — depende da discussão oral |

---

## O relatório deve cobrir

1. **Relevância** — porquê o tema importa hoje
2. **Explicação técnica** — como funciona (primitivas, protocolos)
3. **Uso da criptografia** — onde e como é aplicada
4. **Como a segurança é alcançada** — ameaças modeladas, garantias
5. **Vantagens** — benefícios da abordagem
6. **Falhas e ataques** — vulnerabilidades conhecidas, casos reais
7. **Considerações práticas** — deployment, performance, UX, regulamentação

---

## Temas sugeridos (escolher 1)

| # | Tema | Módulos de apoio |
|---|------|------------------|
| 1 | Criptografia no local de trabalho | 07 |
| 2 | Blockchain | 04, 05, materia-extra |
| 3 | Cartões de pagamento (EMV, 3DS) | 03, 04, 07 |
| 4 | Criptografia em Wi-Fi (WPA2/WPA3) | 03, 07 |
| 5 | Cloud computing | 03, 06, 07 |
| 6 | Identificação eletrónica (eID, eIDAS) | 04, 07 |
| 7 | Segurança IoT | 03, 06 |
| 8 | Lightweight cryptography | 03, materia-extra |
| 9 | Homomorphic encryption | materia-extra |
| 10 | Post-quantum algorithms (Kyber, Dilithium…) | [06](./modulos/06-limitacoes-ameacas-quantica.md) |
| 11 | Web browsers (TLS, certificados) | [07](./modulos/07-distribuicao-chaves-assinaturas.md) |
| 12 | Redes móveis 4G/5G | 03, 04 |
| 13 | E2E encryption (Signal, WhatsApp) | 04, 07, materia-extra |
| 14 | Hardware cryptography (HSM, TPM, Secure Enclave) | 03, 07 |
| 15 | Zero-knowledge proofs | materia-extra |
| 16 | Kerberos | 07 |
| 17 | **Tema próprio** (validar com docente) | — |

---

## Estrutura sugerida do relatório

```
1. Introdução e motivação
2. Contexto e estado da arte
3. Fundamentos criptográficos (primitivas usadas)
4. Arquitetura / protocolo em detalhe
5. Modelo de ameaças e garantias de segurança
6. Ataques conhecidos e mitigações
7. Casos de estudo ou implementação (opcional)
8. Considerações práticas e limitações
9. Conclusão
10. Referências (NIST, RFCs, papers)
Apêndice: declaração de uso de IA (se aplicável)
```

---

## Preparação para a defesa

O docente pode colocar questões sobre **qualquer parte** do relatório. Prepara:

- Explicar primitivas usadas (simétrico, assimétrico, hash, MAC, assinatura)
- Descrever 1–2 ataques reais e como são mitigados
- Comparar com alternativas (ex.: RSA vs ECC, AES-GCM vs CBC+HMAC)
- Implicações quânticas (se relevante)
- Limitações honestas do teu tema

---

## Checklist antes de entregar

- [ ] Todas as 7 secções obrigatórias do enunciado
- [ ] Diagramas de protocolo (Alice/Bob/Eve ou equivalente)
- [ ] Referências académicas/técnicas (RFC, NIST, papers)
- [ ] Ataques e falhas **concretos** (não genéricos)
- [ ] Declaração de IA se usaste ferramentas no relatório
- [ ] Slides de apresentação alinhados com o relatório
- [ ] Ensaiar defesa individual (15–20 min + perguntas)
