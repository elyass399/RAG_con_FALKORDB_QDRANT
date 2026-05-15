# debug_q2.py
import os, requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

proxy_string = f"http://{os.getenv('PROXY_USER','').replace('@','%40')}:{os.getenv('PROXY_PASS','')}@{os.getenv('PROXY_HOST','')}"
session         = requests.Session()
session.proxies = {"http": proxy_string, "https": proxy_string}
session.verify  = False

HEADERS  = {"Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}", "Content-Type": "application/json"}
BASE_URL = os.getenv("LITELLM_BASE_URL","").rstrip("/")

qdrant = QdrantClient(url="http://localhost:6333")

def get_embedding(text):
    resp = session.post(f"{BASE_URL}/embeddings",
        json={"model": "nomic-embed-text-v2-moe:latest", "input": text},
        headers=HEADERS, timeout=120)
    return resp.json()['data'][0]['embedding']

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Test con prefisso corretto
query = "search_query: quali sono le misure del campo per le gare internazionali?"
vector = get_embedding(query)

results = qdrant.query_points(
    collection_name="concepts_V2",
    query=vector,
    limit=15,
    score_threshold=0.0  # nessun filtro — voglio vedere tutto
).points

print("TOP 15 risultati per 'misure campo gare internazionali':\n")
for h in results:
    print(f"  {h.score:.4f}  {h.payload.get('name')}  [{h.payload.get('domain')}]")

# Cerca direttamente GARE_INTERNAZIONALI in Qdrant
print("\n\nCerca GARE_INTERNAZIONALI direttamente:")
from qdrant_client.models import Filter, FieldCondition, MatchValue
res = qdrant.scroll(
    collection_name="concepts_V2",
    scroll_filter=Filter(must=[
        FieldCondition(key="name", match=MatchValue(value="GARE_INTERNAZIONALI"))
    ]),
    limit=5,
    with_vectors=False
)
for p in res[0]:
    print(f"  id={p.id} name={p.payload.get('name')} domain={p.payload.get('domain')}")