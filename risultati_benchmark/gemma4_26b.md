# Benchmark — gemma4:26b

**Data:** 2026-05-07 12:47  
**Modello:** `gemma4:26b`  
**Embedding:** `nomic-embed-text-v2-moe`  
**Grafo:** `graph_V2` · `concepts_V2`  
**GRAPH_DEPTH:** 3  

---

## Q1 — Storia

**chi era Annibale e qual era il suo obiettivo contro Roma?**

*Concept:* `ANNIBALE, MINACCIA_DI_ANNIBALE`  
*Tempo:* 42.4s

### Risposta

Annibale era un abilissimo generale che decise di prendere di sorpresa Roma passando da dove meno si aspettavano un attacco.

---

## Q2 — Calcio

**quali sono le misure del campo per le gare internazionali?**

*Concept:* `GARE_INTERNAZIONALI, ARBITRO_O_GUARDALINEE_NELL_INTERNO_DEL_CAMPO, REGOLAMENTO_DELLA_COMPETIZIONE, CAMPO_DI_CALCIO`  
*Tempo:* 42.5s

### Risposta

Per le gare internazionali, le misure del campo devono essere: lunghezza massima m.110, minima m.100; larghezza massima m.75, minima m.64.

---

## Q3 — Word tesi

**come si imposta l'interlinea in Word per una tesi con caratteri cinesi?**

*Concept:* `TESI_DI_CINESE, INTERLINEA, INTERLINEA_A_ESATTA, SCRITTURA_E_IMPAGINAZIONE_TESI`  
*Tempo:* 43.1s

### Risposta

Per le tesi di cinese, si consiglia di selezionare l'interlinea **ESATTA da 18 a 22 pt**, poiché le righe che contengono caratteri cinesi spesso appaiono più distanziate rispetto a quelle che non ne contengono.

---

## Q4 — Prompt eng.

**cos'è il few-shot prompting e fai un esempio pratico?**

*Concept:* `FEW_SHOT_PROMPTING, SHOT_BASED_PROMPTING, ONE_SHOT_PROMPTING, ZERO_SHOT_PROMPTING`  
*Tempo:* 48.6s

### Risposta

Il few-shot prompting è una tecnica che prevede di fornire al modello alcuni esempi (tipicamente da 2 a 5, chiamati "shot") di coppie input-output che dimostrano il compito che l'IA deve svolgere, prima di presentare la richiesta effettiva. 

Attraverso questi esempi, l'IA "impara" dal pattern mostrato e cerca di replicarlo per il nuovo input. Con due o più esempi, il modello può riconoscere meglio i pattern e gestire compiti più complessi o sfumati, migliorando l'accuratezza e la coerenza delle risposte. Questi esempi aiutano l'IA a comprendere il contesto, il formato atteso e la logica sottostante al compito.

**Esempio pratico (classificazione del sentiment):**

**Istruzione:** Classifica il sentiment del seguente testo come Positivo, Negativo o Neutro.

*   **Testo:** "Questo film è stato fantastico e mi ha emozionato!" | **Sentiment:** Positivo
*   **Testo:** "Non mi è piaciuto per niente, una vera delusione." | **Sentiment:** Negativo
*   **Testo:** "Il servizio al ristorante era accettabile, niente di speciale." | **Sentiment:** Neutro
*   **Testo:** "Adoro questa nuova canzone, mi mette subito di buon umore!" | **L'IA dovrebbe rispondere:** "Positivo"

---

## Q5 — Database Mac

**su Mac posso usare un database invece di Access?**

*Concept:* `OFFICE_2016_PER_MAC, OPEN_OFFICE_MAC, DATABASE, MAC`  
*Tempo:* 48.1s

### Risposta

Access non è disponibile per iMac e Apple non dispone di una versione alternativa nel suo store. La soluzione più pratica è scaricare il pacchetto OpenOffice sul proprio iMac, a meno che non si disponga di una macchina virtuale.

---

## Q6 — AI Act

**cos'è il rischio inaccettabile nell'AI Act e fai un esempio?**

*Concept:* `AI_CHE_COMPORTA_RISCHI_INACCETTABILI, RISCHIO_INACCETTABILE, RISCHI_DELL_AI, AI_ACT`  
*Tempo:* 63.7s

### Risposta

L'AI che comporta rischi inaccettabili (capitolo 2, art. 5) è semplicemente vietata. Il contesto fornito non riporta un esempio specifico per questa categoria di rischio.

---

## Q7 — Cross-manuale

**In Word 2016 per Mac, come si accede agli strumenti per gestire le revisioni di una tesi che include caratteri cinesi?**

*Concept:* `WORD_2016_PER_MAC, WORD_2016_FOR_MAC, OFFICE_2016_PER_MAC, MANUALE_WORD_TESI_UPDATE_MAG23`  
*Tempo:* 59.9s

### Risposta

Il contesto non specifica come accedere agli strumenti di revisione per la versione "Word 2016 per Mac". 

Tuttavia, nel documento `MANUALE_WORD_TESI_UPDATE_MAG23`, viene indicato che è possibile utilizzare la **Scheda Revisione** per gestire i commenti (tramite il pulsante "Nuovo commento") e per verificare di aver accettato o rifiutato le revisioni tramite i pulsanti **Accetta** e **Rifiuta**. Il medesimo documento riporta un esempio di nota che include caratteri cinesi.

---

## Q8 — Ragionamento

**Quali errori commise Annibale che permisero a Roma di riorganizzarsi e vincere la seconda guerra punica?**

*Concept:* `ANNIBALE, SECONDA_GUERRA_PUNICA, MINACCIA_DI_ANNIBALE, PRIMA_GUERRA_PUNICA`  
*Tempo:* 46.1s

### Risposta

L'errore commesso da Annibale fu che, invece di attaccare subito Roma senza darle il tempo di riorganizzarsi, si ritirò per un lungo periodo con il suo esercito a Capua (in Campania) per far riposare i suoi soldati, convinto che la vittoria fosse vicina. Questo permise al Senato di Roma di approfittarne per riorganizzarsi, raccogliere gli uomini rimasti e allestire un esercito affidato al console Scipione.

---

## Q9 — Precisione

**quali furono esattamente le conseguenze della resa di Cartagine dopo la battaglia di Zama — territori persi e condizioni imposte da Roma?**

*Concept:* `SCONTRO_TRA_ROMA_E_CARTAGINE, BATTAGLIA_DI_ZAMA, CONQUISTA_DI_TERRITORI_DA_CARTAGINE, CARTAGINE`  
*Tempo:* 46.2s

### Risposta

Dopo la battaglia di Zama, Roma impose una resa durissima a Cartagine con le seguenti conseguenze:

*   **Territori persi:** Cartagine perse le sue colonie in Spagna e in Africa.
*   **Condizioni imposte:** Roma impose un controllo totale, stabilendo che Cartagine non avrebbe potuto dichiarare guerra a nessuno senza aver prima ricevuto il permesso da Roma.

---

## Q10 — Cross+ragionamento

**Un sistema di IA che analizza i caratteri cinesi di uno studente per valutarne le capacità cognitive rientra nei sistemi vietati dall'AI Act? Perché?**

*Concept:* `SISTEMI_DI_IA_VIETATI, ARTIFICIAL_INTELLIGENCE_ACT, SISTEMA_DI_AI, SISTEMI_DI_AI`  
*Tempo:* 51.7s

### Risposta

Non è possibile determinare se il sistema descritto rientri tra i sistemi vietati basandosi esclusivamente sulle informazioni fornite.

Il contesto specifica che l'AI che comporta "rischi inaccettabili" (capitolo 2, art. 5) è vietata, ma non elenca le casistiche specifiche che rientrano in questa categoria di rischio. Il testo menziona invece che i sistemi di AI vengono considerati ad "alto rischio" quando prevedono una profilazione degli individui (utilizzando dati personali per valutare aspetti come la salute o il rendimento lavorativo), ma non specifica se l'analisi dei caratteri cinesi per la valutazione delle capacità cognitive rientri tra i sistemi vietati o tra quelli ad alto rischio.

---

## Sommario

| Metrica | Valore |
|---|---|
| Domande totali | 10 |
| ✅ Risposte complete | 8 | q10 - q7
| ⚠️ Risposte incomplete | 2 |
| Tempo totale | 492s |
| Tempo medio per domanda | 49.2s |
