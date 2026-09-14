# Módulo 06 — Redes de Sensores: Topologias e Roteamento

**UC:** Redes Sem Fios e de Sensores · **Fase:** 3 — Redes de sensores e protocolos IoT

## Objetivos de aprendizagem

- Comparar topologias WSN (star, tree, mesh, cluster)
- Analisar protocolos de roteamento energy-aware
- Compreender LEACH e variantes de clustering
- Avaliar trade-offs de roteamento em WSN

---

## 1. Arquitectura WSN

```
        [Sink / Base Station]
           /    |    \
        [SN]  [SN]  [SN]     ← Sensor Nodes
        /  \         |
      [SN] [SN]     [SN]     ← Multi-hop
```

### Tipos de nós

| Nó | Função | Recursos |
|----|--------|----------|
| **Sensor Node (SN)** | Recolha + forward | Limitados |
| **Cluster Head (CH)** | Agregação + relay | Moderados |
| **Sink/Base Station** | Destino final | Abundantes |

---

## 2. Topologias

### Star

```
    [Sink]
   /  |  \
 [SN][SN][SN]
```

- Todos comunicam directamente com sink
- **Pros:** simples, sem roteamento
- **Contras:** alcance limitado, single point, hotspot no sink

### Tree (hierárquica)

```
       [Sink]
       /    \
    [CH1]  [CH2]
    / \      |
  [SN][SN] [SN]
```

- Roteamento parent-child
- **Pros:** escalável, agregação
- **Contras:** fragilidade (parent failure), desequilíbrio energético

### Mesh

```
[SN]─[SN]─[SN]
  \   |   /
   [SN]─[SN]─[Sink]
```

- Multi-hop arbitrário
- **Pros:** robustez, auto-healing
- **Contras:** overhead routing, complexidade

### Cluster (hierárquica plana)

- Rede dividida em clusters
- CH agrega e transmite ao sink
- Rotação de CH para equilibrar energia

---

## 3. Classificação de protocolos de roteamento

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| **Flat** | Todos nós iguais | Flooding, SPIN, Directed Diffusion |
| **Hierarchical** | Clusters | LEACH, PEGASIS, TEEN |
| **Location-based** | Usam coordenadas GPS | GAF, GEAR |
| **QoS-aware** | Garantias de QoS | SAR, SPEED |

### Data-centric vs. address-centric

- **Data-centric:** interesse em dados (tipo, região) — Directed Diffusion
- **Address-centric:** destino por ID/endereço — AODV, DSR

---

## 4. LEACH (Low-Energy Adaptive Clustering Hierarchy)

Protocolo clássico de clustering energy-aware.

### Funcionamento

1. **Setup phase:** nós auto-elegem-se CH com probabilidade \( P = \frac{k}{N} \)
2. **CH** anuncia, nós não-CH juntam-se ao CH mais próximo
3. **Steady-state:** nós enviam dados ao CH; CH agrega e envia ao sink
4. **Rotação:** novo conjunto de CHs cada round

### Objectivos

- Distribuir consumo energético
- Agregação reduz transmissões ao sink
- Descentralizado (sem routing global)

### Limitações

- Assume rádio com potência ajustável
- CH distante do sink consome muito (transmissão directa)
- Não adapta a densidade heterogénea

### Variantes

| Variante | Melhoria |
|----------|----------|
| **LEACH-C** | Sink selecciona CHs (centralizado) |
| **LEACH-F** | CH fixo se poucos nós |
| **HEED** | CH por residual energy + comunicação cost |
| **PEGASIS** | Chain topology, leader rota |

---

## 5. Outros protocolos relevantes

### AODV (Ad hoc On-Demand Distance Vector)

- Route discovery on-demand (RREQ/RREP)
- Sequence numbers evitam loops
- Usado em ZigBee, adaptações WSN

### RPL (IPv6 Routing Protocol for LLNs)

- Standard IETF (RFC 6550) para 6LoWPAN
- DODAG (Destination-Oriented DAG)
- Objective Function: OF0 (hop count), MRHOF (ETX)
- Ver módulo 07

### Directed Diffusion

- Sink envia **interests** (queries)
- Gradientes de dados estabelecidos
- In-network aggregation e caching

### Flooding / Gossiping

- **Flooding:** broadcast total — simples, alto overhead
- **Gossiping:** forward probabilístico — reduz overhead

---

## 6. Métricas de roteamento WSN

| Métrica | Descrição |
|---------|-----------|
| **Energy efficiency** | Total/consumed energy per round |
| **Network lifetime** | Tempo até primeiro nó morrer |
| **Latency** | End-to-end delay |
| **Delivery ratio** | Pacotes recebidos / enviados |
| **Overhead** | Pacotes de controlo / pacotes de dados |

---

## 7. Desafios

| Desafio | Impacto |
|---------|---------|
| Energia limitada | Protocolo deve minimizar TX/RX |
| Topologia dinâmica | Nós morrem, links mudam |
| Escala | Milhares de nós |
| Dados correlacionados | Oportunidade de agregação |
| Heterogeneidade | Nós com capacidades diferentes |

---

## Exercícios

### Exercício 1
Compare topologias star e mesh para 200 sensores numa área de 1 km² com sink central.

### Exercício 2
Descreva as fases setup e steady-state do LEACH.

### Exercício 3
Porque a rotação de Cluster Head é importante em LEACH?

### Exercício 4
Rede com 100 nós, desejamos 5 CHs. Qual a probabilidade \( P \) de auto-eleição no LEACH?

### Exercício 5
Compare LEACH e PEGASIS em termos de topologia intra-cluster.

### Exercício 6
Explique a diferença entre roteamento proactivo (table-driven) e reactivo (on-demand) em WSN.

### Exercício 7
Um nó sensor detecta dados redundantes com vizinhos. Que técnica de roteamento data-centric aproveita isto?

### Exercício 8
Identifique três desvantagens de flooding como protocolo de roteamento WSN.

---

## Soluções

### Solução 1
- **Star:** 200 links directos ao sink — muitos fora de alcance, energia alta nos nós distantes, não viável
- **Mesh:** multi-hop — viável, distribui carga, auto-healing, mais overhead de routing
- **Mesh preferível** para área grande

### Solução 2
- **Setup:** nós auto-elegem CH (probabilidade P); CHs anunciam; nós associam-se ao CH mais próximo (por RSSI)
- **Steady-state:** nós enviam TDMA/CSMA ao CH; CH agrega e transmite ao sink; dura até próximo round

### Solução 3
Sem rotação, os mesmos nós seriam CH repetidamente → esgotam bateria antes dos restantes → buracos na rede. Rotação distribui carga energética, maximiza network lifetime.

### Solução 4
\( P = k/N = 5/100 = \mathbf{0.05} \) (5% por round)

### Solução 5
- **LEACH:** star intra-cluster (nós → CH → sink)
- **PEGASIS:** chain (nós formam corrente, leader envia ao sink) — elimina CHs, reduz overhead, mas latência na chain

### Solução 6
- **Proactivo:** mantém tabelas de routing actualizadas (periodicamente) — baixa latência, alto overhead
- **Reactivo:** descobre rota quando necessário (AODV) — baixo overhead, latência de discovery

### Solução 7
**Directed Diffusion:** sink envia interests; nós agregam dados correlacionados in-network; gradientes evitam envio de dados redundantes.

### Solução 8
1. **Implosion:** pacotes duplicados por múltiplos caminhos
2. **Overlap:** vizinhos recebem informação redundante
3. **Overhead energético** proporcional a nós × hops
4. Não escala com densidade
