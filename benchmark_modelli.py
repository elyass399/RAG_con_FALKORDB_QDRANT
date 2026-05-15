# benchmark_modelli.py
import os, time, re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from falkor_chat_V2 import (
    find_relevant_concepts,
    navigate_graph,
    get_chunks_text,
    session,
    HEADERS,
    BASE_URL,
)

MODELLI = [
    "gemma4:e4b",
    "gemma4:26b",
    "gemma3:27b",
    "qwen3.6:27b",
]

DOMANDE = [
    # 1 — Storia
    "chi era Annibale e qual era il suo obiettivo contro Roma?",
    # 2 — Calcio
    "quali sono le misure del campo per le gare internazionali?",
    # 3 — Word tesi
    "come si imposta l'interlinea in Word per una tesi con caratteri cinesi?",
    # 4 — Prompt engineering
    "cos'è il few-shot prompting e fai un esempio pratico?",
    # 5 — Database Mac
    "su Mac posso usare un database invece di Access?",
    # 6 — AI Act
    "cos'è il rischio inaccettabile nell'AI Act e fai un esempio?",
    # 7 — Cross-manuale: Word 2016 + Word tesi
    "In Word 2016 per Mac, come si accede agli strumenti per gestire le revisioni di una tesi che include caratteri cinesi?",
    # 8 — Ragionamento
    "Quali errori commise Annibale che permisero a Roma di riorganizzarsi e vincere la seconda guerra punica?",
    # 9 — Precisione dettagli
    "quali furono esattamente le conseguenze della resa di Cartagine dopo la battaglia di Zama — territori persi e condizioni imposte da Roma?",
    # 10 — Cross + ragionamento
    "Un sistema di IA che analizza i caratteri cinesi di uno studente per valutarne le capacità cognitive rientra nei sistemi vietati dall'AI Act? Perché?",
]

def call_api_model(model: str, system: str, user: str, timeout=180) -> str:
    url = f"{BASE_URL}/chat/completions"
    for attempt in range(2):
        try:
            resp = session.post(url, json={
                "model":       model,
                "messages":    [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ],
                "temperature": 0
            }, headers=HEADERS, timeout=timeout)
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
                return re.sub(r'</?end_of_turn>', '', content).strip()
            else:
                return f"[ERRORE SERVER {resp.status_code}]"
        except requests.exceptions.Timeout:
            if attempt == 0:
                print(f"      ⏳ Timeout, ritento...")
                continue
            return "[TIMEOUT]"
        except Exception as e:
            return f"[ERRORE: {e}]"
    return "[ERRORE]"

def ask(question: str, model: str) -> dict:
    start = time.time()

    concepts = find_relevant_concepts(question)
    if not concepts:
        return {"risposta": "Nessun concetto trovato.", "tempo": 0, "concepts": []}

    facts, chunk_ids = navigate_graph(concepts)
    chunks = get_chunks_text(chunk_ids)
    if not chunks:
        return {"risposta": "Informazione non presente nei manuali.", "tempo": 0, "concepts": concepts}

    docs_txt  = "\n\n".join(chunks)
    graph_txt = "\n".join(f"- {f}" for f in facts)

    sys_prompt = (
        "Sei l'assistente RAG di Zucchetti. "
        "Rispondi usando SOLO le informazioni nel CONTESTO e nelle RELAZIONI fornite. "
        "Se l'informazione non è presente, dillo chiaramente."
    )
    user_prompt = (
        f"CONTESTO:\n{docs_txt}\n\n"
        f"RELAZIONI:\n{graph_txt}\n\n"
        f"DOMANDA: {question}"
    )

    risposta = call_api_model(model, sys_prompt, user_prompt, timeout=180)
    elapsed  = round(time.time() - start, 1)

    return {"risposta": risposta, "tempo": elapsed, "concepts": concepts}

def run():
    import requests as req_module
    globals()['requests'] = req_module

    output_dir = Path("./risultati_benchmark")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"\n🚀 BENCHMARK — {timestamp}")
    print(f"   {len(MODELLI)} modelli × {len(DOMANDE)} domande = {len(MODELLI)*len(DOMANDE)} risposte\n")

    for model in MODELLI:
        model_safe = model.replace(":", "_").replace("/", "_")
        out_path   = output_dir / f"{model_safe}.md"

        print(f"\n📋 {model}")
        print("-" * 55)

        lines = [
            f"# Benchmark — {model}",
            f"",
            f"**Data:** {timestamp}  ",
            f"**Modello:** `{model}`  ",
            f"**Embedding:** `nomic-embed-text-v2-moe`  ",
            f"**Grafo:** `graph_V2` · `concepts_V2`  ",
            f"**GRAPH_DEPTH:** 3  ",
            f"",
            f"---",
            f"",
        ]

        total_time, errori = 0, 0

        for i, domanda in enumerate(DOMANDE, 1):
            categoria = [
                "Storia", "Calcio", "Word tesi", "Prompt eng.",
                "Database Mac", "AI Act", "Cross-manuale",
                "Ragionamento", "Precisione", "Cross+ragionamento"
            ][i-1]

            print(f"   [{i:02d}/10] [{categoria}] {domanda[:45]}...", end=" ", flush=True)

            result   = ask(domanda, model)
            risposta = result["risposta"]
            tempo    = result["tempo"]
            concepts = result["concepts"]
            total_time += tempo

            is_error = (risposta.startswith("[") or
                        "non è possibile" in risposta.lower() or
                        "non presente" in risposta.lower() or
                        "non specifica" in risposta.lower())
            if is_error: errori += 1

            status = "✅" if not is_error else "⚠️"
            print(f"{status} ({tempo}s)")

            lines += [
                f"## Q{i} — {categoria}",
                f"",
                f"**{domanda}**",
                f"",
                f"*Concept:* `{', '.join(concepts[:4])}`  ",
                f"*Tempo:* {tempo}s",
                f"",
                f"### Risposta",
                f"",
                risposta,
                f"",
                f"---",
                f"",
            ]

        # Sommario
        lines += [
            f"## Sommario",
            f"",
            f"| Metrica | Valore |",
            f"|---|---|",
            f"| Domande totali | {len(DOMANDE)} |",
            f"| ✅ Risposte complete | {len(DOMANDE) - errori} |",
            f"| ⚠️ Risposte incomplete | {errori} |",
            f"| Tempo totale | {total_time:.0f}s |",
            f"| Tempo medio per domanda | {total_time/len(DOMANDE):.1f}s |",
            f"",
        ]

        out_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"   💾 {out_path.name} — {len(DOMANDE)-errori}/{len(DOMANDE)} ok — {total_time:.0f}s totali")

    print(f"\n✅ BENCHMARK COMPLETATO → ./risultati_benchmark/")

if __name__ == "__main__":
    import urllib3, requests
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run()