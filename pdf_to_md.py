# pdf_to_md.py
"""
pdf_to_md.py — Convertitore PDF → Markdown
Legge da ./pdfs/  |  Scrive in ./manuals/
"""

import os, re, sys, subprocess
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("❌ pip install pdfplumber")
try:
    import fitz
except ImportError:
    sys.exit("❌ pip install pymupdf")

def _check_ocr() -> bool:  #Verifica se tesseract installato. Ritorna True/False. Usata una volta sola all'avvio per decidere se abilitare OCR.
    try:
        import pytesseract
        from PIL import Image
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False

OCR_AVAILABLE = _check_ocr()
if OCR_AVAILABLE:
    import pytesseract
    from PIL import Image
    import io

INPUT_DIR  = Path("./pdfs")
OUTPUT_DIR = Path("./manuals")

BULLET_PATTERNS = [
    r"^[\u2022\-\u2013\u2014\*]\s+",  #• - – — * simboli comuni per elenchi puntati
    r"^[>\u27a4\u25ba\u25b6\u2713\u2714\u2192]\s+", #> ➤ ► ▶ ✓ ✔ → simboli che a volte appaiono come "finti" bullet
    r"^\d+[\.\)]\s+",  #1. 2) 3. ecc. numerazione comune
    r"^[a-zA-Z][\.\)]\s+",  #a. b) c. ecc. lettere usate come bullet o sub-bullet
    r"^\([a-zA-Z0-9]+\)\s+",  #(1) (a) (i) ecc. numeri o lettere tra parentesi
]
BULLET_RE = re.compile("|".join(BULLET_PATTERNS))  #unisce tutto in una regex sola con | (OR). Più veloce che 5 check separati.

def is_bullet(line): return bool(BULLET_RE.match(line.strip()))  #Controlla se riga è un punto elenco. Usa regex (BULLET_RE) su simboli tipo •, -, 1., a). Ritorna True/False.

def normalize_bullet(line):  # Trasforma una riga che è un bullet in formato Markdown. Esempio: "1. Item" → "1. Item", "a) Subitem" → "- Subitem", "• Point" → "- Point". Rimuove simboli di bullet e aggiunge "-" per sub-bullet.
    stripped = line.strip()
    if re.match(r"^\d+[\.\)]\s+", stripped):
        num  = re.match(r"^(\d+)[\.\)]\s+", stripped).group(1)
        rest = re.sub(r"^\d+[\.\)]\s+", "", stripped)
        return f"{num}. {rest}"
    if re.match(r"^[a-zA-Z][\.\)]\s+", stripped):
        rest = re.sub(r"^[a-zA-Z][\.\)]\s+", "", stripped)
        return f"- {rest}"
    return f"- {BULLET_RE.sub('', stripped)}"

def clean_text(text):  #Pulisce il testo rimuovendo spazi extra, caratteri non stampabili e unendo parole spezzate da trattini. Ritorna testo pulito.
    if not text: return ""
    text = re.sub(r" {2,}", " ", text)  #sostituisce più spazi con uno solo
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text) #rimuove caratteri non stampabili
    text = re.sub(r"-\n([a-z])", r"\1", text) #unisce parole spezzate da trattini alla fine di una riga (es. "esempi-\nficio" → "esempioficio")
    return text.strip()

def table_to_markdown(table):  #Converte una tabella (lista di liste) in formato Markdown. Calcola larghezza colonne, pulisce testo e formatta con | e -. Ritorna stringa Markdown della tabella.
    if not table or not table[0]: return ""
    cleaned = [[str(c).replace("\n"," ").strip() if c else "" for c in row] for row in table]  #pulisce ogni cella: converte in stringa, rimuove nuove linee, spazi extra e sostituisce None con stringa vuota
    max_cols   = max(len(r) for r in cleaned) #trova il numero massimo di colonne in qualsiasi riga (per tabelle irregolari)
    cleaned    = [r + [""]*(max_cols-len(r)) for r in cleaned] #aggiunge celle vuote alle righe che hanno meno colonne, in modo che tutte abbiano lo stesso numero di colonne (necessario per il formato Markdown)
    col_widths = [max(max(len(r[i]) for r in cleaned), 3) for i in range(max_cols)] #calcola la larghezza massima di ogni colonna, considerando anche un minimo di 3 caratteri per evitare colonne troppo strette
    def fmt(row): return "| " + " | ".join(c.ljust(col_widths[i]) for i,c in enumerate(row)) + " |" #funzione interna per formattare una riga in Markdown, allineando il testo a sinistra e aggiungendo spazi per raggiungere la larghezza della colonna
    sep = "| " + " | ".join("-"*w for w in col_widths) + " |"  #riga di separazione tra header e corpo della tabella in Markdown, composta da trattini che corrispondono alla larghezza di ogni colonna
    return "\n".join([fmt(cleaned[0]), sep] + [fmt(r) for r in cleaned[1:]])   

def ocr_page(fitz_page):  #Esegue OCR su una pagina di fitz (PyMuPDF). Renderizza la pagina come immagine, la converte in un oggetto PIL e poi usa pytesseract per estrarre il testo. Ritorna il testo estratto.
    mat = fitz.Matrix(2, 2)  #aumenta la risoluzione dell'immagine per migliorare l'accuratezza dell'OCR (2x in questo caso)
    pix = fitz_page.get_pixmap(matrix=mat)  #renderizza la pagina come immagine raster (pixmap) usando la matrice di trasformazione per aumentare la risoluzione
    img = Image.open(io.BytesIO(pix.tobytes("png")))   #converte la pixmap in un oggetto PIL Image, prima convertendo i dati in byte e poi aprendo l'immagine da questi byte
    return pytesseract.image_to_string(img, lang="ita+eng")  #esegue OCR sull'immagine usando pytesseract, specificando le lingue italiana e inglese per migliorare il riconoscimento del testo. Ritorna il testo estratto come stringa.

def convert_pdf(pdf_path):  #Converte un PDF in Markdown. Per ogni pagina, estrae il testo e le tabelle, identifica i bullet point e li formatta in Markdown. Se la pagina è vuota ma OCR è disponibile, tenta di estrarre testo dalle immagini. Ritorna il contenuto Markdown completo del PDF.
    print(f"  📄 {pdf_path.name}")
    md_pages = []
    fitz_doc = fitz.open(str(pdf_path))  #apre il PDF con PyMuPDF (fitz) per poter accedere alle pagine come oggetti fitz, necessari per l'OCR. Questo è fatto all'inizio per evitare di dover riaprire il PDF ogni volta che serve fare OCR su una pagina.

    with pdfplumber.open(str(pdf_path)) as pdf:  #apre il PDF con pdfplumber per estrarre testo, parole e tabelle in modo più strutturato. pdfplumber è usato principalmente per l'estrazione del testo e delle tabelle, mentre fitz è usato solo per l'OCR quando necessario. Questo approccio combinato sfrutta i punti di forza di entrambi i tool.
        for page_num, page in enumerate(pdf.pages):  #itera su ogni pagina del PDF usando pdfplumber, che fornisce un'interfaccia più ricca per l'estrazione di testo e tabelle. page_num è l'indice della pagina (0-based) e page è l'oggetto che rappresenta la pagina corrente.
            raw_text = page.extract_text() or ""  #estrae il testo grezzo dalla pagina usando pdfplumber. Se la pagina è vuota o non contiene testo, raw_text sarà una stringa vuota. Questo testo viene usato per determinare se è necessario eseguire l'OCR.

            if len(raw_text.strip()) < 20:   #  se il testo estratto è molto breve (meno di 20 caratteri), si assume che la pagina sia principalmente composta da immagini o che l'estrazione del testo sia fallita. In questo caso, se l'OCR è disponibile, si tenta di estrarre testo dalle immagini della pagina. Se l'OCR non è disponibile, si salta la pagina.
                if OCR_AVAILABLE:  # controlla se l'OCR è disponibile (tesseract installato e funzionante). Se sì, procede con l'OCR; altrimenti, stampa un messaggio informativo e salta la pagina.
                    print(f"   🔍 Pagina {page_num+1} — OCR...")
                    ocr_text = ocr_page(fitz_doc[page_num])  #esegue OCR sulla pagina corrente usando la funzione ocr_page, che renderizza la pagina come immagine e usa pytesseract per estrarre il testo. Il testo estratto viene memorizzato in ocr_text.
                    if ocr_text.strip(): md_pages.append(ocr_text.strip())  #se il testo estratto tramite OCR non è vuoto, lo aggiunge alla lista md_pages, che conterrà il contenuto Markdown di tutte le pagine. Se il testo OCR è vuoto, non viene aggiunto nulla e si passa alla pagina successiva.
                else:
                    print(f"   ℹ️  Pagina {page_num+1} — solo immagini, salto.")
                continue

            found_tables = page.find_tables({   #usa pdfplumber per trovare tabelle nella pagina, con parametri che aiutano a identificare meglio le linee che formano le tabelle. Questi parametri indicano di cercare linee verticali e orizzontali, con tolleranze specifiche per unire linee vicine e ignorare linee troppo corte. Il risultato è una lista di oggetti che rappresentano le tabelle trovate nella pagina.
                "vertical_strategy":   "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance":      3,
                "join_tolerance":      3,
                "edge_min_length":     10,
            })

            tables_with_pos = []   #crea una lista per memorizzare le tabelle trovate insieme alla loro posizione verticale (y1, y2) e alla loro rappresentazione in Markdown. Questo è utile per inserire le tabelle nel punto giusto del testo estratto, mantenendo l'ordine originale del documento.
            for ft in found_tables:  #itera su ogni tabella trovata (ft è un oggetto che rappresenta una tabella trovata da pdfplumber). Per ogni tabella, estrae i dati in formato lista di liste usando ft.extract(), e se la tabella contiene dati, aggiunge una tupla alla lista tables_with_pos che contiene la posizione verticale della tabella (ft.bbox[1] è la coordinata y1 superiore, ft.bbox[3] è la coordinata y2 inferiore) e la rappresentazione Markdown della tabella ottenuta con table_to_markdown(tbl_data). Questo permette di mantenere l'ordine delle tabelle rispetto al testo quando si costruisce il Markdown finale.
                tbl_data = ft.extract()
                if tbl_data:
                    tables_with_pos.append((ft.bbox[1], ft.bbox[3], table_to_markdown(tbl_data)))  #aggiunge una tupla alla lista tables_with_pos che contiene la posizione verticale della tabella (y1, y2) e la rappresentazione Markdown della tabella. ft.bbox è una tupla che rappresenta il bounding box della tabella, dove ft.bbox[1] è la coordinata y1 (superiore) e ft.bbox[3] è la coordinata y2 (inferiore). table_to_markdown(tbl_data) converte i dati della tabella in formato Markdown. Questa struttura permette di inserire le tabelle nel punto giusto del testo quando si costruisce il Markdown finale.

            table_y_ranges = [(y1, y2) for y1, y2, _ in tables_with_pos]  #crea una lista di tuple che rappresentano gli intervalli verticali occupati dalle tabelle nella pagina. Ogni tupla contiene la coordinata y1 (superiore) e y2 (inferiore) di una tabella. Questa lista viene usata per verificare se una riga di testo si trova all'interno dell'area di una tabella, in modo da evitare di includere testo che fa parte della tabella nel flusso principale del Markdown, poiché quel testo sarà già rappresentato nella tabella stessa.
            def is_in_table(y):
                return any(y1 <= y <= y2 for y1, y2 in table_y_ranges)  #funzione che verifica se una coordinata y si trova all'interno di uno degli intervalli verticali delle tabelle. Restituisce True se y è compreso tra y1 e y2 per almeno una delle tabelle, altrimenti restituisce False. Questo è usato per escludere righe di testo che si trovano all'interno dell'area di una tabella, poiché quel testo sarà già rappresentato nella tabella stessa e non dovrebbe essere duplicato nel flusso principale del Markdown.

            words = page.extract_words(keep_blank_chars=False, use_text_flow=True)   #estrae le parole dalla pagina usando pdfplumber, con opzioni che rimuovono gli spazi vuoti e cercano di mantenere il flusso del testo. Il risultato è una lista di dizionari, dove ogni dizionario rappresenta una parola con informazioni sulla sua posizione (x0, y0, x1, y1) e il testo della parola stessa. Queste informazioni sono utili per raggruppare le parole in linee e per determinare se una parola si trova all'interno di una tabella.
            if not words: continue

            lines_grouped = []
            current_line  = []
            current_y     = None
            for w in words:  # itera su ogni parola estratta (w è un dizionario che rappresenta una parola con informazioni sulla sua posizione e testo). Raggruppa le parole in linee basandosi sulla coordinata y (w["top"]). Se la coordinata y di una parola è vicina a quella della parola precedente (differenza <= 3), si considera che appartengano alla stessa linea. Altrimenti, si inizia una nuova linea. Questo processo crea una lista di linee, dove ogni linea è una lista di parole che si trovano approssimativamente alla stessa altezza nella pagina.
                if current_y is None or abs(w["top"] - current_y) <= 3:  #  controlla se la coordinata y della parola corrente (w["top"]) è vicina a quella della parola precedente (current_y). Se current_y è None (prima parola) o se la differenza tra w["top"] e current_y è minore o uguale a 3, si considera che la parola appartiene alla stessa linea. In questo caso, la parola viene aggiunta alla current_line e current_y viene aggiornata alla coordinata y della parola corrente. Se la differenza è maggiore di 3, significa che la parola appartiene a una nuova linea, quindi la current_line viene aggiunta alla lista lines_grouped (se non è vuota), e si inizia una nuova current_line con la parola corrente, aggiornando current_y di conseguenza.
                    current_line.append(w); current_y = w["top"]
                else:
                    if current_line: lines_grouped.append(current_line)   #  se la parola corrente appartiene a una nuova linea, si verifica se current_line contiene parole (non è vuota). Se sì, current_line viene aggiunta alla lista lines_grouped, che contiene tutte le linee raggruppate. Questo assicura che la linea precedente venga salvata prima di iniziare a costruire la nuova linea.
                    current_line = [w]; current_y = w["top"]   #  si inizia una nuova linea con la parola corrente (current_line = [w]) e si aggiorna current_y alla coordinata y della parola corrente. Questo prepara il processo per raggruppare le parole successive che appartengono a questa nuova linea.
            if current_line: lines_grouped.append(current_line)   # dopo aver iterato su tutte le parole, si verifica se current_line contiene ancora parole (l'ultima linea potrebbe non essere stata aggiunta a lines_grouped). Se current_line non è vuota, viene aggiunta a lines_grouped. A questo punto, lines_grouped contiene tutte le linee della pagina, dove ogni linea è una lista di parole che si trovano approssimativamente alla stessa altezza.

            md_lines        = []
            prev_was_bullet = False
            tables_queue    = sorted(tables_with_pos, key=lambda x: x[0])
            inserted_tables = set()

            for line_words in lines_grouped:
                line_top  = line_words[0]["top"]
                line_text = clean_text(" ".join(w["text"] for w in line_words))
                if not line_text or is_in_table(line_top): continue

                for i, (ty, _, tmd) in enumerate(tables_queue):
                    if i not in inserted_tables and ty < line_top:
                        md_lines.extend(["", tmd, ""]); inserted_tables.add(i)

                if is_bullet(line_text):
                    md_lines.append(normalize_bullet(line_text)); prev_was_bullet = True
                else:
                    if prev_was_bullet: md_lines.append("")
                    md_lines.append(line_text); prev_was_bullet = False

            for i, (_, _, tmd) in enumerate(tables_queue):
                if i not in inserted_tables:
                    md_lines.extend(["", tmd, ""])

            page_md = re.sub(r"\n{3,}", "\n\n", "\n".join(md_lines))
            if page_md.strip(): md_pages.append(page_md)

    fitz_doc.close()
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(md_pages)).strip()

def post_process(md):
    lines = md.split("\n")
    cleaned = []
    for line in lines:
        s = line.strip()
        if re.match(r"^\d{1,4}$", s): continue
        if re.match(r"^[-_=]{5,}$", s): continue
        cleaned.append(line)
    result = "\n".join(cleaned)
    result = re.sub(r"(^- .+)\n([^-\n\|>])", r"\1 \2", result, flags=re.MULTILINE)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result

def run():
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir(parents=True)
        print(f"📁 Creata '{INPUT_DIR}/' — inserisci i PDF e rilancia.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(INPUT_DIR.glob("*.pdf"))

    if not pdfs:
        print(f"⚠️  Nessun .pdf trovato in '{INPUT_DIR}/'")
        return

    print(f"\n🚀 PDF trovati: {len(pdfs)}")
    print(f"   OCR disponibile: {OCR_AVAILABLE}\n")
    ok, skipped, errors = 0, 0, []

    for pdf_path in pdfs:
        out_path = OUTPUT_DIR / (pdf_path.stem + ".md")
        if out_path.exists():
            print(f"  ⏭️  {pdf_path.name} → già convertito, salto.")
            skipped += 1; continue
        try:
            md       = convert_pdf(pdf_path)
            md       = post_process(md)
            title    = pdf_path.stem.replace("_"," ").replace("-"," ")
            final_md = f"{title}\n\nConvertito da: {pdf_path.name}\n\n{md}"
            out_path.write_text(final_md, encoding="utf-8")
            kb = out_path.stat().st_size // 1024
            print(f"  ✅ {pdf_path.name} → {out_path.name} ({kb} KB)")
            ok += 1
        except Exception as e:
            print(f"  ❌ {pdf_path.name} → {e}")
            errors.append((pdf_path.name, str(e)))

    print(f"\n{'='*50}")
    print(f"Convertiti: {ok} | Saltati: {skipped} | Errori: {len(errors)}")
    if errors:
        for name, err in errors:
            print(f"  - {name}: {err}")

if __name__ == "__main__":
    run()