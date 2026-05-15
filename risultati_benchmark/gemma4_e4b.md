# Benchmark — gemma4:e4b

**Data:** 2026-05-07 12:47  
**Modello:** `gemma4:e4b`  
**Embedding:** `nomic-embed-text-v2-moe`  
**Grafo:** `graph_V2` · `concepts_V2`  
**GRAPH_DEPTH:** 3  

---

## Q1 — Storia

**chi era Annibale e qual era il suo obiettivo contro Roma?**

*Concept:* `ANNIBALE, MINACCIA_DI_ANNIBALE`  
*Tempo:* 82.8s

### Risposta

Annibale era un "abilissimo generale".

Il suo obiettivo contro Roma era quello di prendere la città di sorpresa, attraversando le Alpi e puntando verso il sud Italia.

---

## Q2 — Calcio

**quali sono le misure del campo per le gare internazionali?**

*Concept:* `GARE_INTERNAZIONALI, ARBITRO_O_GUARDALINEE_NELL_INTERNO_DEL_CAMPO, REGOLAMENTO_DELLA_COMPETIZIONE, CAMPO_DI_CALCIO`  
*Tempo:* 120.0s

### Risposta

Per le gare internazionali, le misure del campo devono essere:

*   **Lunghezza:** massima m.110 e minima m.100.
*   **Larghezza:** massima m.75 e minima m.64.

---

## Q3 — Word tesi

**come si imposta l'interlinea in Word per una tesi con caratteri cinesi?**

*Concept:* `TESI_DI_CINESE, INTERLINEA, INTERLINEA_A_ESATTA, SCRITTURA_E_IMPAGINAZIONE_TESI`  
*Tempo:* 206.7s

### Risposta

Per una tesi con caratteri cinesi, si consiglia di selezionare l'interlinea **ESATTA** con un valore compreso tra **18 e 22 pt**.

Questo perché le righe che contengono caratteri cinesi tendono ad apparire più distanziate rispetto a quelle che non li contengono.

*Nota: È importante impostare anche Prima: 0 pt e Dopo: 0 pt, e di mettere la spunta su “Non aggiungere spazio tra paragrafi dello stesso stile”.*

---

## Q4 — Prompt eng.

**cos'è il few-shot prompting e fai un esempio pratico?**

*Concept:* `FEW_SHOT_PROMPTING, SHOT_BASED_PROMPTING, ONE_SHOT_PROMPTING, ZERO_SHOT_PROMPTING`  
*Tempo:* 102.4s

### Risposta

Il Few-shot Prompting è una tecnica che consiste nel fornire al modello linguistico di grandi dimensioni (LLM) **diversi esempi** (tipicamente da 2 a 5, chiamati "shot") di coppie input-output.

**Come funziona:**
Questa tecnica serve a dimostrare al modello il compito che deve svolgere, in modo che l'IA possa "imparare" dal pattern mostrato negli esempi e cercare di replicarlo per il nuovo input che verrà fornito.

**Quando usarlo:**
È particolarmente utile quando i compiti sono complessi, nuovi, o quando è necessario specificare un formato o uno stile molto preciso per la risposta.

***

### Esempio Pratico (Classificazione di Sentiment)

Un esempio pratico è la classificazione del sentiment, dove vengono forniti diversi esempi di testo e del loro sentiment associato, prima di chiedere all'IA di classificare un testo finale:

**Istruzione:** Classifica il sentiment del seguente testo come Positivo, Negativo o Neutro.

| Testo: "Questo film è stato fantastico e mi ha emozionato!" | Sentiment: Positivo |
| :--- | :--- |
| Testo: "Non mi è piaciuto per niente, una vera delusione." | Sentiment: Negativo |
| Testo: "Il servizio al ristorante era accettabile, niente di speciale." | Sentiment: Neutro |
| Testo: "Adoro questa nuova canzone, mi mette subito di buon umore!" | Sentiment: Positivo |
| **Testo: "..."** | **Sentiment: [L'IA dovrebbe rispondere]** |

---

## Q5 — Database Mac

**su Mac posso usare un database invece di Access?**

*Concept:* `OFFICE_2016_PER_MAC, OPEN_OFFICE_MAC, DATABASE, MAC`  
*Tempo:* 130.8s

### Risposta

Sì, secondo le informazioni fornite, Access non è disponibile per iMac.

La soluzione più pratica è scaricare il pacchetto **OpenOffice** sul proprio iMac. Una volta installato, sarà possibile utilizzare la funzione **Database** all'interno di OpenOffice.

*Nota: Se non si dispone di Java sul proprio iMac, al momento dell'apertura di Database potrebbe apparire un avviso, e potrebbe essere necessario seguire le istruzioni per l'installazione di Java.*

---

## Q6 — AI Act

**cos'è il rischio inaccettabile nell'AI Act e fai un esempio?**

*Concept:* `AI_CHE_COMPORTA_RISCHI_INACCETTABILI, RISCHIO_INACCETTABILE, RISCHI_DELL_AI, AI_ACT`  
*Tempo:* 65.0s

### Risposta

L'AI che comporta rischi inaccettabili è semplicemente vietata (capitolo 2, art. 5).

Esempi di sistemi che rientrano in questa categoria includono:

*   Sistemi di social scoring, che categorizzano e discriminano gli individui in base a comportamenti o a caratteristiche personali (come l’etnia, le opinioni politiche, l’orientamento sessuale, ecc.).
*   Sistemi di identificazione biometrica negli spazi pubblici e di riconoscimento facciale attraverso la raccolta indiscriminata di immagini.

---

## Q7 — Cross-manuale

**In Word 2016 per Mac, come si accede agli strumenti per gestire le revisioni di una tesi che include caratteri cinesi?**

*Concept:* `WORD_2016_PER_MAC, WORD_2016_FOR_MAC, OFFICE_2016_PER_MAC, MANUALE_WORD_TESI_UPDATE_MAG23`  
*Tempo:* 48.0s

### Risposta

Per gestire le revisioni di un documento, il relatore può utilizzare la **Scheda Revisione**.

Gli strumenti disponibili includono:
*   **ATTIVO-NON ATTIVO**
*   **Nuovo commento** (per aggiungere un commento/spiegazione per chi leggerà)
*   **Visualizza:** che permette di selezionare tra "Tutti i commenti" o "Documento originale".

È inoltre possibile verificare di aver accettato o rifiutato tutte le revisioni utilizzando i pulsanti **Accetta** e **Rifiuta**.

---

## Q8 — Ragionamento

**Quali errori commise Annibale che permisero a Roma di riorganizzarsi e vincere la seconda guerra punica?**

*Concept:* `ANNIBALE, SECONDA_GUERRA_PUNICA, MINACCIA_DI_ANNIBALE, PRIMA_GUERRA_PUNICA`  
*Tempo:* 111.4s

### Risposta

Annibale commise l'errore di non attaccare subito Roma, senza darle il tempo di riorganizzarsi. Invece, si ritirò per un lungo periodo con il suo esercito a Capua (in Campania) per far riposare i suoi soldati, convinto che la vittoria fosse vicina.

Questo ritardo permise al Senato di Roma di approfittarne per riorganizzarsi, raccogliendo gli uomini rimasti e allestendo un esercito affidato al console Scipione, che usò uno stratagemma.

---

## Q9 — Precisione

**quali furono esattamente le conseguenze della resa di Cartagine dopo la battaglia di Zama — territori persi e condizioni imposte da Roma?**

*Concept:* `SCONTRO_TRA_ROMA_E_CARTAGINE, BATTAGLIA_DI_ZAMA, CONQUISTA_DI_TERRITORI_DA_CARTAGINE, CARTAGINE`  
*Tempo:* 56.6s

### Risposta

Dopo la battaglia di Zama, i romani imposero una resa durissima a Cartagine. Le conseguenze furono:

*   **Territori persi:** Cartagine perse le sue colonie in Spagna e in Africa.
*   **Condizioni imposte da Roma:** I romani imposero un controllo totale, in modo che Cartagine non potesse dichiarare guerra a nessuno senza aver prima ricevuto il permesso da Roma.

---

## Q10 — Cross+ragionamento

**Un sistema di IA che analizza i caratteri cinesi di uno studente per valutarne le capacità cognitive rientra nei sistemi vietati dall'AI Act? Perché?**

*Concept:* `SISTEMI_DI_IA_VIETATI, ARTIFICIAL_INTELLIGENCE_ACT, SISTEMA_DI_AI, SISTEMI_DI_AI`  
*Tempo:* 60.2s

### Risposta

Sulla base delle informazioni fornite, non è possibile determinare con certezza se un sistema di IA che analizza i caratteri cinesi di uno studente per valutarne le capacità cognitive rientri nei sistemi vietati dall'AI Act.

Tuttavia, il CONTESTO fornisce i seguenti elementi di riferimento per la classificazione del rischio:

1.  **Rischio Inaccettabile:** L'AI che comporta rischi inaccettabili è semplicemente vietata.
2.  **Rischio Elevato (Alto Rischio):** I sistemi di AI vengono considerati ad alto rischio quando prevedono una **profilazione degli individui**, ovvero quando utilizzano dati personali per valutare vari aspetti della vita di una persona (come il rendimento lavorativo, la situazione economica o la salute).

Il testo non specifica se l'analisi dei caratteri cinesi per la valutazione cognitiva costituisca un rischio inaccettabile o se rientri nelle casistiche di profilazione descritte.

---

## Sommario

| Metrica | Valore |
|---|---|
| Domande totali | 10 |
| ✅ Risposte complete | 9 | q10
| ⚠️ Risposte incomplete | 1 |
| Tempo totale | 984s |
| Tempo medio per domanda | 98.4s |
