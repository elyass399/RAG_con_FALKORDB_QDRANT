# check_models.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

proxy_string = f"http://{os.getenv('PROXY_USER','').replace('@','%40')}:{os.getenv('PROXY_PASS','')}@{os.getenv('PROXY_HOST','')}"
PROXIES  = {"http": proxy_string, "https": proxy_string}
HEADERS  = {"Authorization": f"Bearer {os.getenv('LITELLM_API_KEY')}", "Content-Type": "application/json"}
BASE_URL = os.getenv("LITELLM_BASE_URL","").rstrip("/")

session         = requests.Session()
session.proxies = PROXIES
session.verify  = False

def check_models():
    print("\n🔍 Modelli disponibili sul server:\n")
    try:
        resp = session.get(f"{BASE_URL}/models", headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            models = resp.json().get("data", [])
            for m in models:
                print(f"  ✅ {m['id']}")
        else:
            print(f"  ⚠️ Status {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"  ❌ {e}")

def test_models():
    modelli = [
        "gemma4:e4b",
        "gemma4:26b",
        "gemma3:27b",
        "qwen3.6:27b",
        "llama3.2:3b",
        "devstral:24b",
    ]
    print("\n🧪 Test risposta modelli:\n")
    for model in modelli:
        try:
            resp = session.post(f"{BASE_URL}/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": "rispondi solo con 'ok'"}],
                    "temperature": 0
                },
                headers=HEADERS, timeout=60)
            if resp.status_code == 200:
                answer = resp.json()['choices'][0]['message']['content'].strip()
                print(f"  ✅ {model} → {answer[:50]}")
            else:
                print(f"  ❌ {model} → status {resp.status_code}")
        except Exception as e:
            print(f"  ❌ {model} → {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    check_models()
    test_models()