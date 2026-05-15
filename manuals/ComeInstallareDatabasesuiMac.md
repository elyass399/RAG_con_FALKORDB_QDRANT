ComeInstallareDatabasesuiMac

Convertito da: ComeInstallareDatabasesuiMac.pdf

COME INSTALLARE “APACHE OPENOFFICE” E FAR FUNZIONARE “DATABASE”
Guida per iMac 🍎
Apache OpenOffice è un prodotto libero, disponibile ufficialmente su Linux, Microsoft
Windows e macOS, che offre funzionalità comparabili con i prodotti commerciali
attualmente dominanti nel settore di produttività personale (ad esempio Microsoft Office).

| In questa breve guida ci concentreremo sul come installare OpenOffice e Java, e fare   |
| -------------------------------------------------------------------------------------- |
| funzionare “Database” su iMac. L'installazione di quest’ultimo, sarà necessaria poiché |
| alcune funzioni, tra cui appunto “Database”, richiedono l'installazione di Java.       |

Sebbene il pacchetto Microsoft Office sia disponibile sull’App Store di iMac, ad un prezzo
di circa 45€, purtroppo, esso comprende solamente Word, Exel e Power Point. Access non
è dunque disponibile per iMac, e ne la Apple dispone sul suo store di una sua versione
alternativa. La soluzione più pratica risulta quindi quella di scaricare il pacchetto
OpenOffice, sul proprio iMac, almeno che non si disponga di una macchina virtuale.
Opzione “Macchina virtuale”
Dall’App Store, e dal sito della Apple è possibile acquistare la licenza di un software che
genera una, o più “macchine virtuali”, sul proprio iMac, nella quale è possibile installare
Windows. Su questa macchina virtuale, una volta impostata e installato il sistema
operativo di Microsoft Windows, sarà possibile scaricare il pacchetto Microsoft Office,
appunto per Windows, e accedere ai contenuti, quali, Word, Exel, Power Point e,
soprattutto, Access.
APACHE OPENOFFICE 🔵
_Come installarlo sul proprio iMac?
Iniziamo scaricando Apache OpenOffice, quindi aprite Safari, o Google Chrome, digitate
“open office mac”, e cliccate sul primo risultato che appare.

Questo vi condurrà direttamente sulla pagina principale per il download di Apache
OpenOffice; cercate il paragrafo “Download” e cliccate su Apache OpenOffice come
evidenziato nella foto.
A questo punto vi apparirà la pagina di preparazione al Download, tramite la quale, sarà
possibile scegliere la versione di OpenOffice e proseguire verso l’ultima fase del
download.

Dopo aver scelto la versione desiderata, cliccate su “Download full installation”.
Dovrebbe aprirsi la pagina della preparazione al download. Atteso il tempo di
preparazione, avrà inizio il download del file. Si prega di fare attenzione all’estensione del
file.
❗ I programmi per iMac hanno come estensione .dmg e NON .exe❗
Una volta che il download sarà giunto al termine aprite il file
Apache_OpenOffice_…OS_x…-…install_it.dmg.
Con molta probabilità vi si aprirà questo avviso, in quanto non avendo scaricato il
programma direttamente dall’App Store, il vostro iMac lo riconoscerà come proveniente da
uno sviluppatore sconosciuto. Non spaventatevi e procedete premendo su “Apri”.

Adesso vi troverete sulla pagina di “Benvenuto” di OpenOffice.
Completate i campi richiesti.
Adesso l’installazione di OpenOffice è terminata.

Si aprirà quindi la pagina principale per la scelta del programma che il pacchetto offre.
Nel nostro caso ci interessa Database, perciò lo apriamo.
❗ Ricorda : Database è la versione di OpenOffice di Access❗
Qualora aveste già installato Java, Database funzionerà correttamente, ed è quindi
consigliata la lettura al paragrafo “Consigli per utilizzare Database”. Altrimenti passate
al paragrafo seguente.
_Come installare Java su iMac?
Se non avete Java sul vostro iMac, al momento dell’apertura di Database vi apparirà
questo avviso:
Quindi (se ancora valido) seguite il seguente indirizzo:
https://www.java.com/en/download/mac_download.jsp

Altrimenti, cercare su Safari (o Google Chrome) “Java for Mac OS X”.
A questo punto, cliccate su “Agree and Start Free Download” per dare inizio al download.
Al termine del Download aprire il file .dmg .
Attendete qualche istante, poi aprite il file di installazione (solitamente denominato come la
versione corrente del programma).
Confermate di voler aprire l’applicazione pur essendo scaricata da internet.

Concedete l’autorizzazione per continuare con l’installazione, e premete su “OK”.
A questo punto, accettate i termini di licenza e premete su “Installa” per dare inizio
all’installazione.
Attendete qualche istante, ed infine al termine dell’installazione, premete su “Chiudi”.

A questo punto, sarà possibile utilizzare Database, perciò riaprite OpenOffice, cliccate su
Database, e buon lavoro!

_Consigli per utilizzare Database
#1 Comprendere che il contenuto di un campo è associato ad un tipo di dato
adeguato, quale: testo, numero, data/ora, si/no.

| TIPO DI CAMPO            | CARATTERISTICHE E UTILIZZO DEL CONTENUTO                                                                                                                                                                                                                                               |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Immagine [LONGVARBINARY] | Dato costituito da un flusso di bit; la sua lunghezza non è fissa, dipende dalla sorgente dei dati.                                                                                                                                                                                    |
| Memo [LONGVARCHAR]       | Dato di tipo testuale senza limiti di lunghezza.                                                                                                                                                                                                                                       |
| Numero [NUMERIC]         | Dato di tipo numerico; permette l’uso di decimali.                                                                                                                                                                                                                                     |
| Decimal [DECIMAL]        | Dato di tipo numerico; permette l’uso di decimali di cui deve essere indicato il numero massimo di cifre.                                                                                                                                                                              |
| Intero [INTEGER]         | Dato di tipo numerico che occupa 4 byte; permette l’uso di soli valori interi. Questo campo può anche essere a incremento automatico, quindi può essere utilizzato come chiave primaria di un archivio.                                                                                |
| Testo [VARCHAR]          | Dato di tipo testuale (oppure testo e numeri, o numeri non suscettibili di calcoli come per esempio CAP, P.IVA ecc.); non occupa uno spazio fisso su disco; anche se si dichiara un numero massimo di caratteri, lo spazio occupato corrisponderà alla quantità di caratteri digitali. |
| Si/No [BOOLEAN]          | Dato che può assumere solo due valori: Si oppure No.                                                                                                                                                                                                                                   |
| Data [DATE]              | Dato di tipo data.                                                                                                                                                                                                                                                                     |
| Ora [TIME]               | Dato di tipo ora.                                                                                                                                                                                                                                                                      |
| Altro [OTHER]            | Dati di altro genere.                                                                                                                                                                                                                                                                  |

#2 Aggiungere criteri ad una query utilizzando i seguenti operatori: = (uguale a), <>
(diverso), < (minore di), <= (minore di o uguale a), > (maggiore di), >= (maggiore di o
uguale a)

| Campo (esempio di campi) | Tipo di dato presente nel campo | Criterio da digitare | Risultato della query (esempio di risultati) |
| ------------------------ | ------------------------------- | -------------------- | -------------------------------------------- |
| Costo                    | Decimale [DECIMAL]              | >250                 | Valori superiori a 250                       |
| Costo                    | Decimale [DECIMAL]              | >=250                | Valori uguale o superiore a 250              |
| Costo                    | Decimale [DECIMAL]              | <>225                | Valori diversi da 225                        |
| Libro di testo           | Si/No [BOOLEAN]                 | 1                    | Si                                           |
| Libro di testo           | Si/No [BOOLEAN]                 | 0                    | No                                           |
| Data inizio              | Data [DATE]                     | >=01/09/2018         | Ciò che inizia dal 01/09/2018 compreso       |
| Data fine                | Data [DATE]                     | <18/12/2017          | Ciò che termina prima del 18/12/2017         |

❗ Il criterio o l'operatore Like può essere usato in una query per trovare dati
corrispondenti ad un modello specifico❗
#3 Utilizzare un carattere jolly in una query: *, %, ? o _.

| Carattere Jolly | Descrizione                                        |
| --------------- | -------------------------------------------------- |
| *               | Corrispondono ad un numero qualsiasi di caratteri. |
| %               |                                                    |
| ?               | Corrispondono a qualsiasi singolo carattere.       |
| _               |                                                    |

| Campo (esempio di campi) | Tipo di dato presente nel campo | Criterio da digitare                | Risultato della query (esempio di risultati)       |
| ------------------------ | ------------------------------- | ----------------------------------- | -------------------------------------------------- |
| Cognome                  | Testo [VARCHAR]                 | LIKE C* oppure LIKE C%              | Persone il cui cognome inizia con la lettera C.    |
| ID Corso                 | Testo [VARCHAR]                 | LIKE *1 oppure LIKE %1              | Persone iscritte a qualsiasi corso del primo anno. |
| Nome                     | Testo [VARCHAR]                 | LIKE ‘Gianni?’ oppure LIKE ‘Giann_’ | Persone che si chiamano Gianni o Gianna            |

#4 Aggiungere criteri ad una query utilizzando uno o più dei seguenti operatori
logici: AND, OR, NOT

| Campo (esempio di campi) | Tipo di dato presente nel campo | Criterio da digitare              | Risultato della query (esempio di risultati) |
| ------------------------ | ------------------------------- | --------------------------------- | -------------------------------------------- |
| Città                    | Testo [VARCHAR]                 | Pisa OR Livorno                   | Persone che risiedono a Pisa e a Livorno.    |
| Data di nascita          | Data [DATE]                     | >=01/01/1998 AND <=01/01/1998     | Persone nate nel 1998.                       |
| ID Corso                 | Testo [VARCHAR]                 | NOT LIKE CF02                     | Persone non iscritte al corso CF02.          |
| Data di nascita          | Data [DATE]                     | BETWEEN 01/01/1997 AND 31/12/1997 | Persone nate nell’anno 1997.                 |

#5 Relazioni
Per creare relazioni con Database, bisogna cercare l’opzione “Relazioni”, nella barra
superiore, nella sezione “Strumenti”.