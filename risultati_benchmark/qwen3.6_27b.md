# Benchmark — qwen3.6:27b

**Data:** 2026-05-07 12:47  
**Modello:** `qwen3.6:27b`  
**Embedding:** `nomic-embed-text-v2-moe`  
**Grafo:** `graph_V2` · `concepts_V2`  
**GRAPH_DEPTH:** 3  

---

## Q1 — Storia

**chi era Annibale e qual era il suo obiettivo contro Roma?**

*Concept:* `ANNIBALE, MINACCIA_DI_ANNIBALE`  
*Tempo:* 63.4s

### Risposta

In base al contesto fornito:

* **Chi era Annibale:** viene descritto esclusivamente come un `"abilissimo generale"`. Il testo non riporta ulteriori dettagli sulla sua identità, nazionalità o cariche ufficiali.
* **Qual era il suo obiettivo contro Roma:** il suo scopo era prendere Roma di sorpresa, attaccandola da una direzione inaspettata (attraversando le Alpi con un vasto esercito) per colpire la città prima che il Senato romano potesse riorganizzarsi e vincere la guerra. 

Qualsiasi altra informazione non è presente nel materiale fornito.

---

## Q2 — Calcio

**quali sono le misure del campo per le gare internazionali?**

*Concept:* `GARE_INTERNAZIONALI, ARBITRO_O_GUARDALINEE_NELL_INTERNO_DEL_CAMPO, REGOLAMENTO_DELLA_COMPETIZIONE, CAMPO_DI_CALCIO`  
*Tempo:* 56.0s

### Risposta

Secondo il contesto fornito, per le gare internazionali le misure del campo devono essere:
- **Lunghezza:** minima 100 m, massima 110 m
- **Larghezza:** minima 64 m, massima 75 m

---

## Q3 — Word tesi

**come si imposta l'interlinea in Word per una tesi con caratteri cinesi?**

*Concept:* `TESI_DI_CINESE, INTERLINEA, INTERLINEA_A_ESATTA, SCRITTURA_E_IMPAGINAZIONE_TESI`  
*Tempo:* 82.2s

### Risposta

In base al manuale fornito, per impostare correttamente l'interlinea in una tesi che contiene caratteri cinesi si consiglia di:

1. Andare su **Formato** > **Paragrafo**.
2. Nella sezione **Spaziatura (interlinea)**, selezionare l'opzione **ESATTA**.
3. Impostare il valore tra **18 e 22 pt**.

Questa configurazione è raccomandata perché le righe che contengono caratteri cinesi tendono ad apparire più distanziate rispetto a quelle che non ne contengono. 

Il manuale suggerisce inoltre, nella stessa finestra di dialogo, di impostare:
* `Prima: 0 pt`
* `Dopo: 0 pt`
* Spuntare l'opzione `“Non aggiungere spazio tra paragrafi dello stesso stile”`

---

## Q4 — Prompt eng.

**cos'è il few-shot prompting e fai un esempio pratico?**

*Concept:* `FEW_SHOT_PROMPTING, SHOT_BASED_PROMPTING, ONE_SHOT_PROMPTING, ZERO_SHOT_PROMPTING`  
*Tempo:* 208.4s

### Risposta

Il **Few-shot Prompting** è una tecnica di prompt engineering che consiste nel fornire al modello linguistico alcuni esempi (tipicamente da 2 a 5, chiamati "shot") di coppie input-output che dimostrano il compito da svolgere, prima di presentare la richiesta effettiva. L'IA "impara" dal pattern mostrato negli esempi e cerca di replicarlo per il nuovo input. Questa tecnica è consigliata per compiti complessi, nuovi o quando è necessario specificare formati o stili esatti, poiché permette al modello di riconoscere meglio i pattern, migliorando l'accuratezza e la coerenza delle risposte.

**Esempio pratico (classificazione del sentiment):**
Istruzione: Classifica il sentiment del seguente testo come Positivo, Negativo o Neutro.
- Testo: `"Questo film è stato fantastico e mi ha emozionato!"` → Sentiment: `Positivo`
- Testo: `"Non mi è piaciuto per niente, una vera delusione."` → Sentiment: `Negativo`
- Testo: `"Il servizio al ristorante era accettabile, niente di speciale."` → Sentiment: `Neutro`
- Testo: `"Adoro questa nuova canzone, mi mette subito di buon umore!"` → Sentiment: `[L'IA dovrebbe rispondere "Positivo"]`

Questi esempi (shot) aiutano l'IA a comprendere il contesto, il formato atteso e la logica sottostante al compito.

---

## Q5 — Database Mac

**su Mac posso usare un database invece di Access?**

*Concept:* `OFFICE_2016_PER_MAC, OPEN_OFFICE_MAC, DATABASE, MAC`  
*Tempo:* 107.9s

### Risposta

Sì. Secondo le informazioni fornite, Microsoft Access non è disponibile per Mac e Apple non offre un'alternativa nativa sul suo store. La soluzione più pratica indicata è scaricare e installare il pacchetto **Apache OpenOffice** sul proprio Mac, che include il modulo Database. In alternativa, è possibile fare ricorso a una macchina virtuale.

---

## Q6 — AI Act

**cos'è il rischio inaccettabile nell'AI Act e fai un esempio?**

*Concept:* `AI_CHE_COMPORTA_RISCHI_INACCETTABILI, RISCHIO_INACCETTABILE, RISCHI_DELL_AI, AI_ACT`  
*Tempo:* 103.7s

### Risposta

Secondo il contesto fornito, nell'AI Act i sistemi di intelligenza artificiale che comportano **rischi inaccettabili** (disciplinati al capitolo 2, articolo 5) sono **semplicemente vietati**.

Tra gli esempi di sistemi associati a queste categorie di rischio citati nel testo figurano:
- Sistemi di *social scoring* che categorizzano e discriminano gli individui in base a comportamenti o caratteristiche personali (quali etnia, opinioni politiche, orientamento sessuale, ecc.);
- Sistemi di identificazione biometrica negli spazi pubblici e di riconoscimento facciale basati sulla raccolta indiscriminata di immagini.

*(La risposta si basa esclusivamente sulle informazioni presenti nel contesto fornito.)*

---

## Q7 — Cross-manuale

**In Word 2016 per Mac, come si accede agli strumenti per gestire le revisioni di una tesi che include caratteri cinesi?**

*Concept:* `WORD_2016_PER_MAC, WORD_2016_FOR_MAC, OFFICE_2016_PER_MAC, MANUALE_WORD_TESI_UPDATE_MAG23`  
*Tempo:* 119.3s

### Risposta

In base al contesto fornito, gli strumenti per gestire le revisioni si trovano nella **Scheda Revisione**. Da questa scheda è possibile:
- Attivare o disattivare il tracciamento delle modifiche (`ATTIVO-NON ATTIVO`)
- Inserire un `Nuovo commento`
- Scegliere cosa visualizzare (`Tutti i commenti` o `Documento originale`)
- Verificare e confermare le modifiche tramite i pulsanti `Accetta` e `Rifiuta`

Tuttavia, il contesto **non contiene informazioni specifiche** su come accedere o configurare questi strumenti per una tesi che include caratteri cinesi. L'unico riferimento ai caratteri cinesi presente nei documenti è un esempio di nota bibliografica, che non è correlato alla gestione delle revisioni. Se ti servono indicazioni specifiche sulla gestione di caratteri cinesi durante il tracciamento delle modifiche, tali informazioni non sono presenti nel materiale fornito.

---

## Q8 — Ragionamento

**Quali errori commise Annibale che permisero a Roma di riorganizzarsi e vincere la seconda guerra punica?**

*Concept:* `ANNIBALE, SECONDA_GUERRA_PUNICA, MINACCIA_DI_ANNIBALE, PRIMA_GUERRA_PUNICA`  
*Tempo:* 105.3s

### Risposta

In base al contesto fornito, Annibale commise un errore decisivo durante la seconda guerra punica: **invece di attaccare subito Roma per non darle il tempo di riorganizzarsi, si ritirò per un lungo periodo con il suo esercito a Capua (in Campania) per far riposare i soldati**, convinto che la vittoria fosse ormai vicina.

Questa scelta permise al Senato romano di:
- Riorganizzarsi e raccogliere gli uomini rimasti;
- Allestire un nuovo esercito affidato al console Scipione;
- Far sì che Scipione utilizzasse uno stratagemma, spostando il teatro della guerra direttamente in Africa e minacciando Cartagine. La città, preoccupata, fu costretta a richiamare Annibale e il suo esercito in patria, permettendo a Roma di salvarsi e vincere la guerra.

---

## Q9 — Precisione

**quali furono esattamente le conseguenze della resa di Cartagine dopo la battaglia di Zama — territori persi e condizioni imposte da Roma?**

*Concept:* `SCONTRO_TRA_ROMA_E_CARTAGINE, BATTAGLIA_DI_ZAMA, CONQUISTA_DI_TERRITORI_DA_CARTAGINE, CARTAGINE`  
*Tempo:* 92.7s

### Risposta

In base al contesto fornito, dopo la battaglia di Zama Roma impose a Cartagine una **resa durissima** con le seguenti conseguenze:

* **Territori persi:** Cartagine perse le sue colonie in **Spagna** e in **Africa**.
* **Condizioni imposte:** Roma stabilì un **controllo totale** sulla città, imponendo che Cartagine **non potesse dichiarare guerra a nessuno senza aver prima ricevuto il permesso da Roma**.

---

## Q10 — Cross+ragionamento

**Un sistema di IA che analizza i caratteri cinesi di uno studente per valutarne le capacità cognitive rientra nei sistemi vietati dall'AI Act? Perché?**

*Concept:* `SISTEMI_DI_IA_VIETATI, ARTIFICIAL_INTELLIGENCE_ACT, SISTEMA_DI_AI, SISTEMI_DI_AI`  
*Tempo:* 143.5s

### Risposta

In base al contesto fornito, **non è possibile determinare** se il sistema descritto rientri tra quelli vietati dall'AI Act. 

Il testo indica che:
- L'AI che comporta **rischi inaccettabili** (capitolo 2, art. 5) è **semplicemente vietata**.
- I sistemi sono considerati **ad alto rischio** quando prevedono una **profilazione degli individui**, ovvero quando utilizzano dati personali per valutare aspetti della vita di una persona come il rendimento lavorativo, la situazione economica o la salute.

Tuttavia, il contesto **non contiene informazioni specifiche** riguardo all'analisi di caratteri cinesi o alla valutazione delle capacità cognitive di studenti, né chiarisce se tale applicazione rientri tra i rischi inaccettabili vietati o in un'altra categoria di rischio. Pertanto, con le informazioni disponibili, non posso stabilire se il sistema descritto sia vietato.

---

## Sommario

| Metrica | Valore |
|---|---|
| Domande totali | 10 |
| ✅ Risposte complete | 9 | q10
| ⚠️ Risposte incomplete | 1 | 
| Tempo totale | 1082s |
| Tempo medio per domanda | 108.2s |
