# semantic_chunking_context.py
import os, json, requests, re, time
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
proxy_string = f"http://{os.getenv('PROXY_USER', '').replace('@', '%40')}:{os.getenv('PROXY_PASS', '')}@{os.getenv('PROXY_HOST', '')}"
PROXIES = {"http": proxy_string, "https": proxy_string}
HEADERS = {"Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}", "Content-Type": "application/json"}
BASE_URL = os.getenv("LITELLM_BASE_URL", "").rstrip("/")

def call_api(endpoint, payload, timeout=120):
    try:
        resp = requests.post(f"{BASE_URL}/{endpoint}", json=payload, headers=HEADERS,
                             proxies=PROXIES, timeout=timeout, verify=False)
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None

def get_embedding(text, retries=3, delay=3) -> np.ndarray | None:
    for attempt in range(retries):
        data = call_api("embeddings",
                        {"model": os.getenv("EMBEDDING_MODEL", "nomic-embed-text-v2-moe:latest"),
                         "input": text},
                        timeout=120)
        if data and 'data' in data:
            return np.array(data['data'][0]['embedding'])
        if attempt < retries - 1:
            print(f"   ⏳ Embedding fallito, ritento ({attempt+1}/{retries})...")
            time.sleep(delay)
    return None

def get_clean_sentences(text):
    text = re.sub(r'((?:\|.*\n)+)', lambda m: m.group(0).replace('\n', ' [TAB_NL] '), text)
    text = re.sub(r'\b([a-zA-Z0-9]{1,3})\.(?!\s+[A-Z])', r'\1#DOT#', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    segments = re.split(r'\.\s+(?=[A-Z])', text)
    return [s.replace('#DOT#', '.').replace(' [TAB_NL] ', '\n').strip() + "."
            for s in segments if len(s.strip()) > 15]

def global_optimal_chunking(matrix, min_sents=2, max_sents=8):
    n = len(matrix)
    dp = [-float('inf')] * (n + 1); dp[0] = 0; path = [0] * (n + 1)
    for i in range(1, n + 1):
        for size in range(min_sents, max_sents + 1):
            j = i - size
            if j < 0: continue
            reward = np.mean(matrix[j:i, j:i])
            if dp[j] + reward > dp[i]:
                dp[i] = dp[j] + reward; path[i] = j
    splits = []; curr = n
    while curr > 0:
        splits.append((path[curr], curr)); curr = path[curr]
    return sorted(splits)

def run_late_chunking_ingestion():
    INPUT_DIR  = Path("./manuals")
    OUTPUT_DIR = Path("./output_chunks")
    OUTPUT_DIR.mkdir(exist_ok=True)

    manuals = sorted(INPUT_DIR.glob("*.md"))
    if not manuals:
        print("⚠️  Nessun .md trovato in ./manuals/")
        return

    ok, skipped = 0, 0

    for manual in manuals:
        manual_out = OUTPUT_DIR / manual.stem

        if manual_out.exists() and any(manual_out.iterdir()):
            print(f"  ⏭️  {manual.name} → chunks già presenti, salto.")
            skipped += 1
            continue

        print(f"\n🚀 Elaborazione: {manual.name}")
        content   = manual.read_text(encoding="utf-8", errors="replace")
        sentences = get_clean_sentences(content)

        if not sentences:
            print(f"   ⚠️ Nessuna frase estratta, salto.")
            continue

        print(f"   🧠 Vettorizzazione di {len(sentences)} frasi...")
        embs = [get_embedding(s) for s in sentences]
        embs = [e for e in embs if e is not None]

        if len(embs) < 2:
            print(f"   ⚠️ Embedding insufficienti, salto.")
            continue

        matrix         = cosine_similarity(np.array(embs))
        optimal_splits = global_optimal_chunking(matrix)

        manual_out.mkdir(parents=True, exist_ok=True)
        saved          = 0
        skipped_chunks = 0

        for idx, (start, end) in enumerate(optimal_splits, 1):
            chunk_text = " ".join(sentences[start:end])
            vec = get_embedding(chunk_text)
            if vec is None:
                print(f"   ❌ Chunk {idx} fallito dopo tutti i tentativi, salto.")
                skipped_chunks += 1
                continue

            chunk_data = {
                "id":     f"{manual.stem}_{idx:03d}",
                "vector": vec.tolist(),
                "text":   chunk_text,
                "source": manual.name
            }
            with open(manual_out / f"{manual.stem}_{idx:03d}.json", "w", encoding="utf-8") as f:
                json.dump(chunk_data, f, ensure_ascii=False, indent=4)
            saved += 1

        print(f"   ✅ {saved} chunk salvati in {manual_out}/")
        if skipped_chunks > 0:
            print(f"   ⚠️ {skipped_chunks} chunk saltati dopo tutti i retry.")
        ok += 1

    print(f"\n{'='*50}")
    print(f"Elaborati: {ok} | Saltati: {skipped}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run_late_chunking_ingestion()