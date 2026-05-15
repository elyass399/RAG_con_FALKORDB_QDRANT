# pipeline_graphrag_V2.py
"""
Pipeline GraphRAG V2 — 3 step:
  Step 1: pdf_to_md.py              → manuals/
  Step 2: semantic_chunking_context → output_chunks/
  Step 3: falkor_ingest_V2          → graph_V2 (FalkorDB) + concepts_V2 (Qdrant)

Modelli:
  LLM:       gemma4:e4b
  Embedding: nomic-embed-text-v2-moe:latest (768 dim)
"""

import time
from datetime import datetime
from pdf_to_md import run as run_pdf
from semantic_chunking_context import run_late_chunking_ingestion
from falkor_ingest_V2 import run_ingestion

def run_pipeline():
    start = time.time()
    print("=" * 60)
    print("🚀 PIPELINE GRAPHRAG V2 — AVVIO")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   LLM: gemma4:e4b")
    print(f"   Embedding: nomic-embed-text-v2-moe:latest")
    print(f"   Graph: graph_V2  |  Concepts: concepts_V2")
    print("=" * 60)

    print("\n📄 STEP 1: Conversione PDF → Markdown")
    print("-" * 40)
    run_pdf()

    print("\n✂️  STEP 2: Chunking Semantico → output_chunks/")
    print("-" * 40)
    run_late_chunking_ingestion()

    print("\n🧠 STEP 3: Ingestione → FalkorDB + Qdrant")
    print("-" * 40)
    run_ingestion()

    elapsed = (time.time() - start) / 60
    print("\n" + "=" * 60)
    print(f"🏆 PIPELINE COMPLETATA in {elapsed:.1f} minuti")
    print(f"   Avvia la chat con: python falkor_chat_V2.py")
    print("=" * 60)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run_pipeline()