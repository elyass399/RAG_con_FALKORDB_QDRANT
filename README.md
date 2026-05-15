# GraphRAG: Sistema RAG Ibrido con Knowledge Graph

Un sistema **Retrieval-Augmented Generation (RAG) ibrido** che combina **grafi di conoscenza** (FalkorDB) e **retrieval semantico** (Qdrant) per estrarre risposte accurate e contestualizzate da documentazione tecnica frammentata.

## 🎯 Il Problema

I manuali tecnici sono spesso distribuiti in PDF complessi e frammentati. Trovare una risposta specifica richiede:
- Cercare tra documenti multipli
- Perdere il contesto relazionale
- Informazioni sparse non collegate
- Spreco di tempo e produttività

## ✨ La Soluzione

Un **sistema RAG ibrido** che:
- **Naviga relazioni esplicite** tramite knowledge graph (FalkorDB)
- **Trova concetti semanticamente simili** tramite retrieval vettoriale (Qdrant)
- **Genera risposte complete** con contesto cross-documento
- **Gestisce domini eterogenei** (storia, calcio, AI, database, normative)

## 🏗️ Architettura

```
PDF Documents
    ↓
[pdf_to_md.py] → Markdown conversion (OCR fallback)
    ↓
[semantic_chunking_context.py] → Dynamic Programming + Cosine Similarity
    ↓
[falkor_ingest_V2.py] → LLM triplet extraction + Entity Resolution
    ↓
├─ FalkorDB (graph_V2) → Knowledge graph with relationships
├─ Qdrant (concepts_V2) → Vector embeddings (768-dim)
    ↓
[falkor_chat_V2.py] → Chat pipeline with fallback & graph navigation
    ↓
Answers with context
```

## 📊 Stack Tecnico

| Componente | Tecnologia | Versione/Note |
|---|---|---|
| **Graph DB** | FalkorDB | Property graph, Cypher queries |
| **Vector DB** | Qdrant | HNSW index, cosine similarity |
| **Embedding Model** | nomic-embed-text-v2-moe | 768-dim, Mixture-of-Experts |
| **LLM** | Gemma3:27b | Ingestione (40s/domanda) |
| **LLM** | Gemma4:e4b | Chat (opzionale) |
| **Chunking** | Dynamic Programming | Cosine similarity matrix optimization |
| **Language** | Python 3.9+ | asyncio, LiteLLM proxy |

## 🚀 Quick Start

### Prerequisiti

```bash
# Python 3.9+
python --version

# Docker (per FalkorDB e Qdrant)
docker --version
```

### Installazione

```bash
# Clone repository
git clone https://github.com/elyass399/RAG_con_FALKORDB_QDRANT.git
cd RAG_con_FALKORDB_QDRANT

# Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Startup Services

```bash
# Terminal 1: FalkorDB (port 6381)
docker run -it -p 6381:6381 falkordb/falkordb:latest

# Terminal 2: Qdrant (port 6333)
docker run -it -p 6333:6333 qdrant/qdrant:latest

# Terminal 3: LiteLLM proxy
litellm --model ollama/gemma3:27b --base_url http://localhost:11434
```

### Esecuzione Pipeline

#### 1. **Conversione PDF → Markdown**
```bash
python pdf_to_md.py --input manuals/ --output manuals_md/
```

#### 2. **Semantic Chunking**
```bash
python semantic_chunking_context.py \
    --input manuals_md/ \
    --output output_chunks/ \
    --min_chunk 100 \
    --max_chunk 500
```

#### 3. **Ingestione nel Grafo**
```bash
python falkor_ingest_V2.py \
    --chunks output_chunks/ \
    --llm gemma3:27b \
    --graph_host localhost \
    --graph_port 6381 \
    --qdrant_host localhost \
    --qdrant_port 6333
```

#### 4. **Chat Interattiva**
```bash
python falkor_chat_V2.py \
    --graph_host localhost \
    --graph_port 6381 \
    --qdrant_host localhost \
    --qdrant_port 6333
```

Domande di esempio:
```
> cos'è il rischio inaccettabile nell'AI Act?
> misure del campo per gare internazionali di calcio?
> quale il ruolo in comune tra un prompt e l'arbitro di calcio?
```

## 📈 Benchmark

### Setup
- **Domande:** 10 (storia, calcio, Word, AI Act, database, cross-manuale)
- **Modelli testati:** Gemma3:27b, Gemma4:26b, Gemma4:e4b, Qwen3.6:27b
- **Embedding fisso:** nomic-embed-text-v2-moe
- **Graph depth:** 3 (navigazione bidirezionale)

### Risultati

| Metrica | Gemma3:27b | Gemma4:26b | Gemma4:e4b | Qwen3.6:27b |
|---|---|---|---|---|
| ✅ Risposte complete | 10/10 | 8/10 | 9/10 | 9/10 |
| ⚠️ Incomplete | 0 | 2 | 1 | 1 |
| ⏱️ Tempo totale | 403s | 492s | 984s | 1082s |
| ⚡ Tempo medio | 40.3s | 49.2s | 98.4s | 108.2s |

**Conclusione:** Gemma3:27b è il modello ottimale per questo use case (modello denso vs. MoE overhead).

## 🔑 Componenti Principali

### `pdf_to_md.py`
Converte PDF in Markdown strutturato con OCR fallback.
```python
python pdf_to_md.py --input doc.pdf --output doc.md
```

### `semantic_chunking_context.py`
Segmenta testo usando **Dynamic Programming** su matrice cosine similarity.
- Sottomatrici 2-8 frasi
- Score cumulativo = somma medie similarità
- Massimizza coerenza semantica

### `falkor_ingest_V2.py`
Estrae triplet (soggetto-relazione-oggetto) con LLM e li carica nel grafo.
```
Esempio: ANNIBALE -[ATTRAVERSA]-> ALPI
         ANNIBALE -[SCONFIGGE]-> ROMANI
```

**Entity Resolution:** Evita duplicati nel grafo (soglia 0.97 similarità coseno).

### `falkor_chat_V2.py`
Pipeline chat a 7 step:
1. Embedding query vettoriale
2. Ricerca Qdrant (TOP_K=8, threshold=0.40)
3. **Fallback Keyword** se score basso
4. **Navigazione Grafo Bidirezionale** (depth=3)
5. Recupero chunk associati
6. Costruzione contesto (chunk + triplet + note cross-manuale)
7. LLM genera risposta finale

## 📚 Dataset

7 manuali eterogenei per testare flessibilità:

**Omogenei (Informatica):**
- Manuale WORD (tesi)
- WORD 2016 FOR MAC Quick Start Guide
- Come Installare Database su Mac

**Eterogenei (Domini diversi):**
- AI Act (normativa EU)
- Prompt Engineering (AI/ML)
- Le 17 Regole del Calcio (sport)
- Storia: Le Guerre Puniche (storia)

## 🛠️ Configurazione

Crea `.env` nella root:
```env
# LiteLLM
LITELLM_API_KEY=your_key_here
LITELLM_API_BASE=https://llm.padova.zucchettitest.it/v1

# FalkorDB
FALKOR_HOST=localhost
FALKOR_PORT=6381

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Modelli
LLM_INGEST=gemma3:27b
LLM_CHAT=gemma4:e4b
EMBEDDING_MODEL=nomic-embed-text-v2-moe

# Graph
GRAPH_DEPTH=3
SIMILARITY_THRESHOLD=0.40
TOP_K_VECTORS=8
```

## 📖 Documentazione Tecnica

### Late Chunking vs. Nostro Approccio

**Late Chunking (Jina AI, 2024):**
- Embedding dell'intero documento PRIMA del chunking
- Risolve pronomi a distanza (es. "sua" → "Padova")
- **Svantaggio:** GPU potente, embedding model 8k+ token, lentezza

**Nostro Approccio (Grafo + DP):**
```
Chunk 8: "Annibale attraversò le Alpi"
         → ANNIBALE [COMANDA] ESERCITO

Chunk 9: "Con il suo esercito..."
         → ESERCITO [SCONFIGGE] ROMANI

Grafo connette: ANNIBALE → ESERCITO → ROMANI
Query "esercito di Annibale" → naviga grafo → chunk 9 recuperato
```

### Triplet Extraction: LLM vs. mREBEL vs. spaCy

| Metodo | Accuracy | Speed | Domain-aware |
|---|---|---|---|
| **LLM (Gemma3)** | ✅ 4/4 | 5-15s/chunk | ✅ Sì |
| **mREBEL** | ❌ 1/5 | Fast | ❌ Schemi rigidi |
| **spaCy** | ❌ Grezzo | Very fast | ❌ No |

**Scelto:** LLM per accuratezza semantica.

## 🎓 Concetti Chiave

### Modello Denso vs. MoE

**Gemma3 (Denso):**
- Tutti i parametri attivi ad ogni inferenza
- Forward pass singolo
- 40s/domanda

**Gemma4 (MoE):**
- Routing interno seleziona esperti
- Thinking mode (chain-of-thought interno)
- 98s/domanda (3x più lento, no vantaggio qualitativo)

**Nel vostro RAG:** Il grafo già fa da "filtro intelligente" → Gemma3 denso è sufficiente.

### Dynamic Programming Chunking

```
Frasi vettorizzate → Matrice cosine similarity (NxN)
                  ↓
DP esamina sottomatrici 2-8 frasi
                  ↓
Score cumulativo = somma medie similarità
                  ↓
Seleziona divisione che massimizza score totale
                  ↓
Frasi semanticamente correlate nello stesso chunk
```

## 🔍 Risoluzione di Problemi

### FalkorDB non connette
```bash
# Verifica porta
netstat -an | grep 6381

# Restart
docker stop falkordb && docker run -p 6381:6381 falkordb/falkordb:latest
```

### Qdrant connection timeout
```bash
# Check status
curl http://localhost:6333/health

# Rebuild index
python -c "from qdrant_client import QdrantClient; c = QdrantClient('localhost', 6333); c.recreate_collection('concepts_V2', ...)"
```

### LLM timeout durante ingestione
```bash
# Aumenta timeout in falkor_ingest_V2.py
request_timeout = 60  # default 30s

# O usa batching
python falkor_ingest_V2.py --batch_size 5 --chunks output_chunks/
```

## 📝 File Structure

```
RAG_con_FALKORDB_QDRANT/
├── pdf_to_md.py                      # PDF → Markdown
├── semantic_chunking_context.py      # DP chunking
├── falkor_ingest_V2.py              # LLM extraction + graph insert
├── falkor_chat_V2.py                # Chat pipeline
├── manuals/                         # Input PDF documents
├── output_chunks/                   # Semantic chunks
├── output_raptor/                   # RAPTOR layers (optional)
├── .env                             # Environment config
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🤝 Contribuzione

Segnalazioni di bug, feature request, o miglioramenti sono benvenuti.

```bash
git checkout -b feature/tua-feature
git commit -am 'Add feature'
git push origin feature/tua-feature
```

## 📄 Licenza

Progetto di stage Zucchetti S.p.A. — 2024-2026

## 🙋 Autori

- **Elyass** — Sviluppatore, Zucchetti S.p.A.

## 🔗 Riferimenti

- [FalkorDB Documentation](https://www.falkordb.com/)
- [Qdrant Vector Database](https://qdrant.tech/)
- [Nomic Embeddings](https://www.nomic.ai/)
- [Gemma LLM](https://ai.google.dev/gemma/)
- [RAG Best Practices](https://arxiv.org/abs/2312.10997)

## ⭐ Vale la pena?

**Sì.**

Il sistema dimostra che combinare grafi di conoscenza con retrieval semantico produce risposte accurate su domini eterogenei, senza richiedere un LLM particolarmente potente.

L'approccio scala bene su dataset eterogenei e gestisce correttamente le relazioni cross-documento — il limite principale dei RAG tradizionali.

Il costo computazionale reale è nella fase di ingestione, non nel retrieval — una volta costruito il grafo, il sistema è veloce e preciso.
