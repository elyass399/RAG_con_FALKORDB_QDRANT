# falkor_ingest_V2.py
import os, json, requests, re, time
from pathlib import Path
from dotenv import load_dotenv
from falkordb import FalkorDB
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pydantic import BaseModel
from typing import List
from collections import defaultdict

load_dotenv()

proxy_string = f"http://{os.getenv('PROXY_USER', '').replace('@', '%40')}:{os.getenv('PROXY_PASS', '')}@{os.getenv('PROXY_HOST', '')}"
PROXIES = {"http": proxy_string, "https": proxy_string}
session         = requests.Session()
session.proxies = PROXIES
session.verify  = False

HEADERS = {
    "Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}",
    "Content-Type":  "application/json",
    "User-Agent":    "Mozilla/5.0"
}

db = FalkorDB(host='localhost', port=6381)

GRAPH_NAME         = "graph_V2"
CONCEPT_COLLECTION = "concepts_V2"

qdrant      = QdrantClient(url="http://localhost:6333")
VECTOR_SIZE = 768

LLM_MODEL            = os.getenv("LITELLM_MODEL", "gemma3:27b")
EMBEDDING_MODEL      = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe:latest")
SIMILARITY_THRESHOLD = 0.97

class Triplet(BaseModel):
    s: str
    r: str
    o: str

class TripletList(BaseModel):
    triplets: List[Triplet]

def call_api(payload, timeout=900):
    url = f"{os.getenv('LITELLM_BASE_URL').rstrip('/')}/chat/completions"
    for attempt in range(2):
        try:
            resp = session.post(url, json=payload, headers=HEADERS, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"   ⚠️ Errore Server ({resp.status_code})")
        except requests.exceptions.ReadTimeout:
            print(f"   ⏳ Timeout. Ritento ({attempt+1}/2)...")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Server non raggiungibile"); return None
        except Exception as e:
            print(f"   ⚠️ {e}")
    return None

def get_embedding(text: str) -> list | None:
    url = f"{os.getenv('LITELLM_BASE_URL').rstrip('/')}/embeddings"
    for attempt in range(3):
        try:
            resp = session.post(url, json={"model": EMBEDDING_MODEL, "input": text},
                                headers=HEADERS, timeout=120)
            if resp.status_code == 200:
                return resp.json()['data'][0]['embedding']
            print(f"   ⚠️ Embedding status {resp.status_code}")
        except requests.exceptions.ReadTimeout:
            print(f"   ⏳ Timeout embedding. Ritento ({attempt+1}/3)...")
            time.sleep(3)
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Server non raggiungibile"); return None
        except Exception as e:
            print(f"   ⚠️ {e}")
    return None

def extract_triplets(text: str, domain: str) -> list:
    prompt = (
        "Sei un esperto di knowledge graph. Analizza il testo e identifica i CONCETTI CHIAVE "
        "del dominio e le relazioni semantiche tra loro.\n\n"
        "REGOLE SUI CONCETTI:\n"
        "- Usa concetti di dominio specifici, NON parole generiche\n"
        "- Un concetto puo essere composto da piu parole "
        "(es. 'CALCIO_DI_RIGORE', 'GUERRA_PUNICA', 'ZERO_SHOT_PROMPTING')\n"
        "- Preferisci nomi tecnici e specifici del dominio\n"
        "- I NOMI PROPRI sono Concept validi: persone (es. 'ANNIBALE', 'SCIPIONE'), "
        "luoghi (es. 'CARTAGINE', 'ALPI', 'SICILIA'), "
        "eventi (es. 'BATTAGLIA_DI_ZAMA', 'SECONDA_GUERRA_PUNICA')\n\n"
        "REGOLE SULLE RELAZIONI:\n"
        "- Scegli la relazione che descrive ESATTAMENTE il legame reale tra i due concetti\n"
        "- Usa underscore al posto degli spazi (es. E_PARTE_DI, PORTA_A)\n"
        "- Se nessun esempio sotto si adatta, INVENTANE UNA nuova piu precisa\n\n"
        "ESEMPI DI RELAZIONI (non esaustivi):\n"
        "  Gerarchia:    E_UN, E_PARTE_DI, CONTIENE, INCLUDE\n"
        "  Causalita:    CAUSA, PORTA_A, DIPENDE_DA, PROVOCA\n"
        "  Prerequisiti: PREREQUISITO_DI, RICHIEDE, NECESSITA_DI\n"
        "  Esempi:       ESEMPIO_DI, ILLUSTRA, DIMOSTRA\n"
        "  Sinonimi:     SINONIMO_DI, EQUIVALE_A, ANCHE_DETTO\n"
        "  Applicazione: SI_APPLICA_A, USATO_IN, PERMETTE, CONSENTE\n"
        "  Definizione:  DEFINISCE, DESCRIVE, SPECIFICA, CARATTERIZZA\n"
        "  Azione:       ATTRAVERSA, GUIDA, SCONFIGGE, CONQUISTA, COMANDA\n"
        "  Generico:     CORRELATO_A (solo se nessuna altra si adatta)\n\n"
        "IMPORTANTE: ogni tripletta DEVE avere i campi s, r, o — nessuno puo essere vuoto.\n\n"
        f"DOMINIO DEL MANUALE: {domain}\n\n"
        "Rispondi SOLO in JSON con questo schema esatto:\n"
        '{"triplets": [{"s": "CONCETTO_A", "r": "RELAZIONE", "o": "CONCETTO_B"}]}\n'
        "Nessun testo prima o dopo il JSON.\n\n"
        f"TESTO:\n{text[:3000]}"
    )
    data = call_api({"model": LLM_MODEL,
                     "messages": [{"role": "user", "content": prompt}],
                     "temperature": 0})
    if data:
        try:
            content = data['choices'][0]['message']['content']
            content = re.sub(r'^```(?:json)?', '', content.strip(), flags=re.MULTILINE)
            content = re.sub(r'```$', '', content.strip(), flags=re.MULTILINE).strip()
            match   = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                raw = json.loads(match.group())
                raw["triplets"] = [
                    t for t in raw.get("triplets", [])
                    if "s" in t and "r" in t and "o" in t
                    and str(t["s"]).strip() and str(t["r"]).strip() and str(t["o"]).strip()
                ]
                return TripletList(**raw).triplets
        except Exception as e:
            print(f"   ⚠️ Errore parsing: {e}")
    return []

def clean_node_name(text: str) -> str:
    cleaned = re.sub(r'[^A-Z0-9]', '_', str(text).upper().strip())
    return re.sub(r'_+', '_', cleaned).strip('_')

def clean_label(text: str) -> str:
    cleaned = re.sub(r'[^A-Z0-9_]', '', str(text).upper().replace(" ", "_"))
    return re.sub(r'_+', '_', cleaned).strip('_') or "CORRELATO_A"

def concept_to_embedding_text(name: str) -> str:
    # prefisso search_document obbligatorio per nomic-embed-text-v2-moe
    return f"search_document: {name.replace('_', ' ').lower()}"

def write_triplet_to_graph(graph, chunk_id, source, domain, s_name, o_name, r_type):
    query = f"""
        MERGE (c1:Concept {{name: $s_name}})
        ON CREATE SET c1.manual = $domain, c1.source = $source, c1.resolved = false
        ON MATCH SET c1.manual = CASE
            WHEN c1.manual CONTAINS $domain THEN c1.manual
            ELSE c1.manual + '|' + $domain
        END
        MERGE (c2:Concept {{name: $o_name}})
        ON CREATE SET c2.manual = $domain, c2.source = $source, c2.resolved = false
        ON MATCH SET c2.manual = CASE
            WHEN c2.manual CONTAINS $domain THEN c2.manual
            ELSE c2.manual + '|' + $domain
        END
        MERGE (c1)-[:{r_type} {{source: $source}}]->(c2)
        WITH c1, c2
        MATCH (ch:Chunk {{id: $chunk_id}})
        MERGE (ch)-[:CONTIENE]->(c1)
        MERGE (ch)-[:CONTIENE]->(c2)
    """
    graph.query(query, {"s_name": s_name, "o_name": o_name, "source": source,  #query: È la stringa di testo con i comandi Cypher definiti sopra.
                        "domain": domain, "chunk_id": chunk_id})

def save_concept_embedding(concept_name, domain, qdrant_id) -> bool:
    # usa concept_to_embedding_text che include già il prefisso search_document
    vector = get_embedding(concept_to_embedding_text(concept_name))  #trasforma BATTAGLIA_DI_ZAMA in search_document: battaglia di zama
    if not vector: return False
    try:
        qdrant.upsert(
            collection_name=CONCEPT_COLLECTION,
            points=[PointStruct(id=qdrant_id, vector=vector,  #id: identificatore univoco del concetto, vector: embedding del concetto(lista dei 768 numeri)
                                payload={"name": concept_name, "domain": domain})] #metadati
        )
        return True
    except Exception as e:
        print(f"   ⚠️ {e}"); return False

def is_resolvable(name: str) -> bool:
    if len(name) < 6: return False  #ROMA (4 lettere) o DNA (3 lettere) restituiscono False. Sono troppo brevi per una ricerca semantica affidabile in questo contesto.
    tokens = name.split('_')
    meaningful = [t for t in tokens if len(t) > 2] 
    if len(meaningful) < 2: return False #La regola dice: Devono esserci almeno 2 parole pesanti. || CALCIO_DI_RIGORE: Ha 2 parole significative (CALCIO, RIGORE). OK. || IL_CALCIO: Ha solo 1 parola significativa (CALCIO). SCARTATO.
    single_char_tokens = [t for t in tokens if len(t) == 1]
    if single_char_tokens: return False  #Se c'è anche solo un token di una singola lettera, restituisce False. || GUERRA_PUNICA: Non ha token di una sola lettera. OK. || GUERRA_PUNICA_X: Ha un token di una sola lettera (X). SCARTATO.
    return True

def resolve_entities(graph):
    print("\n🔗 Entity Resolution in corso...")
    try:
        res        = graph.query("MATCH (c:Concept {resolved: false}) RETURN c.name, c.manual") #resolved = false significa che quel concetto non è ancora passato per l'entity resolution — non è ancora stato confrontato con gli altri per trovare sinonimi.
        unresolved = [(row[0], row[1]) for row in res.result_set if row[0]]
    except Exception as e:
        print(f"   ⚠️ {e}"); return

    if not unresolved:
        print("   ✅ Nessun Concept nuovo da risolvere."); return

    print(f"   📊 Concept da risolvere: {len(unresolved)}")
    processati = [n for n, _ in unresolved if is_resolvable(n)]
    filtrati   = [n for n, _ in unresolved if not is_resolvable(n)]
    print(f"   🔍 Processati: {len(processati)} | Filtrati: {len(filtrati)}")
    found = 0

    for name, domain in unresolved:
        if not is_resolvable(name): continue
        vector = get_embedding(concept_to_embedding_text(name))
        if not vector: continue
        try:
            results = qdrant.query_points(
                collection_name=CONCEPT_COLLECTION,
                query=vector, limit=5,
                score_threshold=SIMILARITY_THRESHOLD
            ).points
        except Exception:
            continue
        for hit in results:
            candidate = hit.payload.get("name")
            if candidate == name: continue
            if not is_resolvable(candidate): continue
            try:
                graph.query(
                    "MATCH (c1:Concept {name: $n1}), (c2:Concept {name: $n2}) "
                    "MERGE (c1)-[:SINONIMO_DI]->(c2)",
                    {"n1": name, "n2": candidate}    # se la similarita supera la soglia (in questo caso 0.97), si crea relazione di sinonimia tra i due concetti nel grafo
                )
                print(f"   🔗 {name} ↔ {candidate}")
                found += 1
            except Exception as e:
                print(f"   ⚠️ {e}")

    try:
        graph.query("MATCH (c:Concept {resolved: false}) SET c.resolved = true")  #l'ultima vrifica ; segna i concetti gia controllati come resolved per non essere ritrattati nella prossima ingestion
    except Exception as e:
        print(f"   ⚠️ {e}")

    print(f"   ✅ Entity resolution: {found} sinonimi trovati.")

def run_ingestion():
    #BLOC 1 : SETUP E lettura file 
    INPUT_DIR = Path("./output_chunks")
    files     = sorted(list(INPUT_DIR.rglob("*.json")))

    if not files:
        print("❌ Nessun file trovato in ./output_chunks"); return

    graph = db.select_graph(GRAPH_NAME)

    try:
        nodi_exist = graph.query("MATCH (n) RETURN count(n) AS tot").result_set[0][0]   #usata per contare i nodi esistenti nel grafo , [0]prima riga[0]prima colonna , se il grafo non esiste ancora, viene sollevata un'eccezione e nodi_exist viene impostato a 0, indicando che è la prima esecuzione e che il grafo deve essere inizializzato. 
    except Exception:
        nodi_exist = 0
    #BLOC 2 : inizializzazione collezione Qdrant e struttura dati per i manuali
    if nodi_exist == 0:
        print(f"🆕 Prima esecuzione — inizializzazione {GRAPH_NAME} + {CONCEPT_COLLECTION}...")
        try:
            qdrant.delete_collection(CONCEPT_COLLECTION)
        except Exception:
            pass
        qdrant.create_collection(
            collection_name=CONCEPT_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
    else:
        print(f"🔄 Modalità incrementale — {nodi_exist} nodi esistenti.")
        try:
            qdrant.get_collection(CONCEPT_COLLECTION)
        except Exception:
            qdrant.create_collection(
                collection_name=CONCEPT_COLLECTION,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
            )

    manuals: dict         = defaultdict(list)
    domain_counters: dict = defaultdict(int)
    #BLOC 3: organizzazione dei manuali per dominio e assegnazione ID chunk
    for f_path in files:
        with open(f_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        source = data.get('source', 'Unknown')
        domain = re.sub(r'[^A-Z0-9_]', '_', Path(source).stem.upper().replace("-", "_"))
        domain = re.sub(r'_+', '_', domain).strip('_')
        domain_counters[domain] += 1
        chunk_id = f"chunk_{domain}_{domain_counters[domain]:03d}"
        manuals[domain].append((chunk_id, data))

    print(f"📚 Manuali: {list(manuals.keys())}")
    print(f"📊 Grafo: {GRAPH_NAME}\n")

    try:
        qdrant_concept_id = qdrant.get_collection(CONCEPT_COLLECTION).points_count + 1
    except Exception:
        qdrant_concept_id = 1
    #BLOC 4: estrazione e salvataggio triplette, popolamento grafo e collezione Qdrant
    seen_concepts: dict[str, int] = {}

    for domain, chunk_list in manuals.items():
        print(f"\n📖 [{domain}] — {len(chunk_list)} chunk")

        for chunk_id, data in chunk_list:
            text   = data.get('text', '')
            source = data.get('source', 'Unknown')

            try:
                if graph.query("MATCH (ch:Chunk {id: $id}) RETURN ch LIMIT 1",
                               {"id": chunk_id}).result_set:
                    print(f"   ⏭️  {chunk_id} — già presente, salto.")
                    continue  #saltiamo il chunk se esiste gia
            except Exception:
                pass

            graph.query(
                "CREATE (:Chunk {id: $id, content: $content, source: $source, domain: $domain})",  # crea un nodo chunk con questi 4 campi
                {"id": chunk_id, "content": str(text), "source": source, "domain": domain}
            )

            print(f"   🧠 {chunk_id}...")
            start_t  = time.time()
            triplets = extract_triplets(text, domain)  #Chiama l'LLM (extract_triplets) per farsi dire quali relazioni ci sono in quel testo.
            print(f"   📄 {len(triplets)} relazioni ({time.time() - start_t:.1f}s)")

            for t in triplets:
                s_name = clean_node_name(t.s)
                o_name = clean_node_name(t.o)
                r_type = clean_label(t.r)
                if not s_name or not o_name: continue
                try:
                    write_triplet_to_graph(graph, chunk_id, source, domain,
                                           s_name, o_name, r_type)  #scrive la tripla nel grafo, creando i nodi concetto se non esistono già e collegandoli al nodo chunk
                    for cname in [s_name, o_name]:
                        if cname not in seen_concepts:
                            if save_concept_embedding(cname, domain, qdrant_concept_id):
                                seen_concepts[cname] = qdrant_concept_id
                                qdrant_concept_id += 1
                except Exception as e:
                    print(f"      ❌ [{s_name} -[{r_type}]-> {o_name}]: {e}")

            time.sleep(0.5)

        print(f"✅ [{domain}] completato.")
    #
    resolve_entities(graph)  #dopo aver inserito tutte le triple, si esegue l'entity resolution per trovare i sinonimi tra i concetti usando gli embedding e creare le relazioni di sinonimia nel grafo

    print(f"\n🏆 {GRAPH_NAME} COMPLETATO!")
    print(f"   Qdrant: {qdrant_concept_id-1} Concept in '{CONCEPT_COLLECTION}'")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run_ingestion()