run_ingestion()
│
├─ BLOCCO 1️⃣: SETUP
│  ├─ Leggi file da ./output_chunks
│  ├─ Connettiti a FalkorDB
│  └─ Conta nodi esistenti
│
├─ BLOCCO 2️⃣: INIT
│  ├─ Se prima volta: ricrea Qdrant
│  └─ Se incrementale: riusa Qdrant
│
├─ BLOCCO 3️⃣: ORGANIZE
│  ├─ Raggruppa chunk per dominio
│  └─ Output: {STORIA: [...], CALCIO: [...]}
│
├─ BLOCCO 4️⃣: PROCESS (il più lungo)
│  └─ Per ogni chunk in ogni dominio:
│     ├─ Crea nodo Chunk
│     ├─ Chiama LLM → extract_triplets()
│     ├─ write_triplet_to_graph()
│     └─ save_concept_embedding() in Qdrant
│
└─ BLOCCO 5️⃣: FINALIZE
   ├─ resolve_entities() → trova sinonimi
   └─ Print statistiche