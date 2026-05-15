# falkor_chat_V2_history_test.py
"""
Test della chat history con sliding window embedding.
File indipendente — non tocca falkor_chat_V2.py.
"""
import os, requests, re
from dotenv import load_dotenv
from falkordb import FalkorDB
from qdrant_client import QdrantClient
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

load_dotenv()
proxy_string = f"http://{os.getenv('PROXY_USER', '').replace('@', '%40')}:{os.getenv('PROXY_PASS', '')}@{os.getenv('PROXY_HOST', '')}"
PROXIES = {"http": proxy_string, "https": proxy_string}

BASE_URL = os.getenv("LITELLM_BASE_URL", "").rstrip("/")
HEADERS  = {
    "Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}",
    "Content-Type":  "application/json",
    "User-Agent":    "Mozilla/5.0"
}

session         = requests.Session()
session.proxies = PROXIES
session.verify  = False

GRAPH_NAME         = "graph_V2"
CONCEPT_COLLECTION = "concepts_V2"

db    = FalkorDB(host='localhost', port=6381)
graph = db.select_graph(GRAPH_NAME)
qdrant = QdrantClient(url="http://localhost:6333")

LLM_MODEL       = os.getenv("LITELLM_MODEL", "gemma3:27b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe:latest")

TOP_CONCEPTS        = 8
GRAPH_DEPTH         = 3
SCORE_MIN_RELEVANT  = 0.40
MAX_HISTORY         = 3
FOLLOWUP_THRESHOLD  = 0.85  # soglia similarity per rilevare followup

# ── SLIDING WINDOW ────────────────────────────────────────────────────────────
history_embeddings = []  # lista di (query_text, vector)

def update_history_embedding(query: str, vector: list):
    history_embeddings.append((query, vector))
    if len(history_embeddings) > MAX_HISTORY:
        history_embeddings.pop(0)
    print(f"   📚 History embeddings: {len(history_embeddings)} — {[h[0][:30] for h in history_embeddings]}")

def detect_followup(query_vector: list) -> tuple[bool, str]:
    """
    Confronta il vettore della nuova domanda con l'ultimo in history.
    Ritorna (is_followup, prev_query).
    """
    if not history_embeddings:
        print(f"   🔗 History vuota — no followup check")
        return False, ""

    last_query, last_vector = history_embeddings[-1]
    sim = cos_sim([query_vector], [last_vector])[0][0]
    is_f = sim >= FOLLOWUP_THRESHOLD

    print(f"   🔗 Similarity con '{last_query[:40]}': {sim:.4f} "
          f"{'→ FOLLOWUP ✅' if is_f else '→ nuovo argomento ✅'}")

    return is_f, last_query if is_f else ""

def build_search_query(user_input: str, query_vector: list) -> str:
    """
    Se followup → arricchisce la query con la domanda precedente.
    Se no → usa la query originale.
    """
    is_f, prev_query = detect_followup(query_vector)
    if is_f:
        enriched = f"{prev_query} {user_input}"
        print(f"   ✏️  Query arricchita: '{enriched}'")
        return enriched
    return user_input

# ── API ───────────────────────────────────────────────────────────────────────
def call_api(payload, timeout=300):
    url = f"{BASE_URL}/chat/completions"
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
            print(f"   ⚠️ Errore: {e}")
    return None

def get_embedding(text: str) -> list | None:
    text = f"search_query: {text}"
    url  = f"{BASE_URL}/embeddings"
    for attempt in range(2):
        try:
            resp = session.post(url,
                json={"model": EMBEDDING_MODEL, "input": text},
                headers=HEADERS, timeout=120)
            if resp.status_code == 200:
                return resp.json()['data'][0]['embedding']
        except requests.exceptions.ReadTimeout:
            print(f"   ⏳ Timeout embedding. Ritento ({attempt+1}/2)...")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Server non raggiungibile"); return None
        except Exception as e:
            print(f"   ⚠️ {e}")
    return None

# ── RETRIEVAL ─────────────────────────────────────────────────────────────────
def find_concepts_by_keyword(query: str) -> list[str]:
    words  = re.findall(r'[a-zA-ZÀ-ù]{4,}', query.upper())
    found, seen = [], set()
    for word in words:
        try:
            res = graph.query(
                "MATCH (c:Concept) WHERE c.name CONTAINS $word "
                "RETURN c.name LIMIT 5",
                {"word": word}
            )
            for row in res.result_set:
                name = row[0]
                if name and name not in seen:
                    seen.add(name); found.append(name)
        except Exception:
            pass
    return found[:8]

def filter_by_domain(concept_names: list[str], top_domains: set) -> list[str]:
    if not concept_names or not top_domains:
        return concept_names
    try:
        res = graph.query(
            "MATCH (c:Concept) WHERE c.name IN $names RETURN c.name, c.manual",
            {"names": concept_names}
        )
        filtered = []
        for row in res.result_set:
            name   = row[0]
            manual = row[1] or ''
            if any(d in manual for d in top_domains):
                filtered.append(name)
        return filtered if filtered else concept_names
    except Exception:
        return concept_names

def find_relevant_concepts(query: str, query_vector: list) -> list[str]:
    """Usa il vettore già calcolato — zero embedding extra."""
    try:
        results = qdrant.query_points(
            collection_name=CONCEPT_COLLECTION,
            query=query_vector,
            limit=TOP_CONCEPTS,
            score_threshold=0.25
        ).points

        print(f"   🔍 Score results: {[(h.payload.get('name'), round(h.score,4)) for h in results]}")

        seen, concepts, max_score = set(), [], 0.0
        for h in results:
            name = h.payload.get("name")
            if name and name not in seen:
                seen.add(name); concepts.append(name)
            if h.score > max_score:
                max_score = h.score

        if round(max_score, 2) < SCORE_MIN_RELEVANT:
            print(f"   ⚠️ Score basso ({max_score:.3f}) — attivo fallback keyword...")
            top_domains = set()
            for h in results[:3]:
                d = h.payload.get('domain') or h.payload.get('manual') or ''
                if d: top_domains.add(d)
            keyword_concepts = find_concepts_by_keyword(query)
            if keyword_concepts:
                keyword_filtered = filter_by_domain(keyword_concepts, top_domains)
                print(f"   🔎 Fallback keyword filtrato: {keyword_filtered}")
                merged, ms = [], set()
                for c in keyword_filtered + concepts:
                    if c not in ms:
                        ms.add(c); merged.append(c)
                concepts = merged[:TOP_CONCEPTS]

        print(f"   🎯 Concept trovati: {concepts}")
        return concepts

    except Exception as e:
        print(f"   ⚠️ Qdrant: {e}")
        return find_concepts_by_keyword(query)

def navigate_graph(concepts: list[str]) -> tuple[list[str], list[str]]:
    if not concepts:
        return [], []
    facts, seen_facts, chunk_ids = [], set(), set()
    for concept in concepts:
        try:
            res = graph.query(
                f"MATCH (c:Concept {{name: $name}})-[r*1..{GRAPH_DEPTH}]->(m:Concept) "
                "RETURN c.name, type(r[0]), m.name, c.manual, m.manual LIMIT 15",
                {"name": concept}
            )
            for row in res.result_set:
                rel = row[1].replace('_', ' ') if row[1] else ""
                f   = f"{row[0]} {rel} {row[2]}"
                if row[3] and row[4] and row[3] != row[4]:
                    f += f"  [cross: {row[3]} → {row[4]}]"
                if f not in seen_facts:
                    facts.append(f); seen_facts.add(f)
        except Exception:
            pass
        try:
            res = graph.query(
                f"MATCH (m:Concept)-[r*1..{GRAPH_DEPTH}]->(c:Concept {{name: $name}}) "
                "RETURN m.name, type(r[0]), c.name, m.manual, c.manual LIMIT 10",
                {"name": concept}
            )
            for row in res.result_set:
                rel = row[1].replace('_', ' ') if row[1] else ""
                f   = f"{row[0]} {rel} {row[2]}"
                if row[3] and row[4] and row[3] != row[4]:
                    f += f"  [cross: {row[3]} → {row[4]}]"
                if f not in seen_facts:
                    facts.append(f); seen_facts.add(f)
        except Exception:
            pass
        try:
            res = graph.query(
                "MATCH (ch:Chunk)-[:CONTIENE]->(c:Concept {name: $name}) "
                "RETURN ch.id LIMIT 12",
                {"name": concept}
            )
            for row in res.result_set:
                if row[0]: chunk_ids.add(row[0])
        except Exception:
            pass
    return facts[:30], list(chunk_ids)

def get_chunks_text(chunk_ids: list[str]) -> list[str]:
    texts = []
    for chunk_id in chunk_ids[:10]:
        try:
            res = graph.query(
                "MATCH (ch:Chunk {id: $id}) RETURN ch.content, ch.domain",
                {"id": chunk_id}
            )
            if res.result_set:
                content = res.result_set[0][0]
                domain  = res.result_set[0][1]
                texts.append(f"[{domain}]\n{content}")
        except Exception:
            pass
    return texts

# ── CHAT ──────────────────────────────────────────────────────────────────────
def start_chat():
    print("\n🚀 ZUCCHETTI — GRAPHRAG CHAT V2 [HISTORY TEST]")
    print(f"   {GRAPH_NAME} · {CONCEPT_COLLECTION}")
    print(f"   FOLLOWUP_THRESHOLD={FOLLOWUP_THRESHOLD} | MAX_HISTORY={MAX_HISTORY}\n")
    print("   Domande suggerite per il test:")
    print("   1. quali sono le misure del campo per le gare internazionali?")
    print("   2. e per le gare normali?                    ← followup atteso")
    print("   3. cos'è il few-shot prompting?")
    print("   4. su Mac posso usare un database?           ← NON followup atteso")
    print("   5. quale errore commise Annibale?")
    print()

    try:
        res = graph.query("MATCH (n) RETURN count(n) AS tot")
        tot = res.result_set[0][0]
        if tot == 0:
            print("❌ Grafo vuoto"); return
        print(f"📊 FalkorDB: {tot} nodi  |  Qdrant: {CONCEPT_COLLECTION}")
    except Exception:
        print("❌ Grafo non trovato"); return

    while True:
        user_input = input("\ndomanda : ").strip()
        if user_input.lower() in ["esci", "quit", "exit"]:
            history_embeddings.clear()
            break
        if not user_input:
            continue

        print(f"\n{'─'*55}")

        # Step 1 — embedding della domanda (usato sia per followup che per Qdrant)
        query_vector = get_embedding(user_input)
        if not query_vector:
            print("risposta ai : Errore embedding."); continue

        # Step 2 — detecta followup e costruisce search_query
        search_query = build_search_query(user_input, query_vector)

        # Step 3 — se followup, ricalcola il vettore per la search_query arricchita
        if search_query != user_input:
            search_vector = get_embedding(search_query)
            if not search_vector:
                search_vector = query_vector
        else:
            search_vector = query_vector

        # Step 4 — retrieval con search_vector
        concepts = find_relevant_concepts(search_query, search_vector)
        if not concepts:
            print("risposta ai : Nessun concetto trovato."); continue

        facts, chunk_ids = navigate_graph(concepts)
        chunks = get_chunks_text(chunk_ids)
        if not chunks:
            print("risposta ai : Informazione non presente."); continue

        domains_used = set()
        for c in chunks:
            match = re.match(r'\[([^\]]+)\]', c)
            if match: domains_used.add(match.group(1))
        if len(domains_used) > 1:
            print(f"   🌐 Cross-manuale: {domains_used}")

        graph_txt = "\n".join(f"- {f}" for f in facts)
        docs_txt  = "\n\n".join(chunks)
        cross_note = (
            "\nLa risposta richiede informazioni da piu manuali.\n"
            if len(domains_used) > 1 else ""
        )

        sys_prompt = (
            "Sei l'assistente RAG di Zucchetti. "
            "Rispondi usando SOLO le informazioni nel CONTESTO e nelle RELAZIONI fornite. "
            f"{cross_note}"
            "Se l'informazione non e presente, dillo chiaramente."
        )
        user_prompt = (
            f"CONTESTO:\n{docs_txt}\n\n"
            f"RELAZIONI:\n{graph_txt}\n\n"
            f"DOMANDA: {user_input}"
        )

        res = call_api({
            "model":       LLM_MODEL,
            "messages":    [
                {"role": "system", "content": sys_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            "temperature": 0
        })

        if res and 'choices' in res:
            answer = re.sub(r'</?end_of_turn>', '',
                            res['choices'][0]['message']['content']).strip()
            print(f"\nrisposta ai : {answer}")

            # Step 5 — aggiorna sliding window con vettore originale
            update_history_embedding(user_input, query_vector)
        else:
            print("risposta ai : Errore di connessione.")

        print(f"{'─'*55}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    start_chat()