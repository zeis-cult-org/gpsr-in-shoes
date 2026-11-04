# Fase 2 — Migrazione dell'URL storico (SOLO PIANO, NON APPLICATO)

Da `https://lost-95.github.io/cult-milano-gpsr/` a `https://gpsr.in-shoes.it/`.

**Regole confermate (4/11/2026)**
- I vecchi QR sono su scarpe di **tutti e tre i marchi**: la homepage storica deve portare alla **homepage** `https://gpsr.in-shoes.it/`, dove il cliente sceglie CULT, DOCKSTEPS o OXS. **Mai direttamente a CULT.**
- Il redirect riguarda **solo la homepage** (`/cult-milano-gpsr/` e `/cult-milano-gpsr/index.html`).
- I 10 PDF e i loro URL restano invariati e raggiungibili: non è noto se qualche QR punti direttamente a un PDF, quindi si preservano tutti gli indirizzi.

**Prerequisiti obbligatori**: snodo pubblicato, [CHECKLIST_TEST.md](CHECKLIST_TEST.md) completata e approvazione esplicita. Fino ad allora il repository storico non si tocca, non si rinomina, non si trasferisce e i PDF non si cancellano.

## 1. Cosa c'è oggi (rilevato il 4/11/2026)
- Homepage `…/cult-milano-gpsr/` (titolo "Cult Milano | Sicurezza prodotti GPSR") con link a 10 PDF nella stessa cartella e a `ufficiocommerciale@cult-milano.it`.
- Il backup locale `gpsr-cult/gpsr_basic.zip` (30/07/2026) ha `index.html` identico byte per byte a quello online (stesso MD5).
- Tutte le URL testate rispondono 200.

## 2. Verifiche prima di intervenire
1. **Quali URL sono nei QR stampati?** Controllare le etichette di ciascun marchio (e i file di stampa, es. `Etichetta_GPSR_CULT_QR_v1.docx`, i template in `qrcode-etichetta-gpsr-v1/`) decodificando i QR: solo homepage, oppure anche percorsi diretti a PDF o con `index.html` / parametri?
2. **Backup completo**: `git clone` del repository storico in una cartella di archivio + zip datato, con verifica che contenga tutti i PDF e l'`index.html` attuale.

## 3. Opzione proposta: redirect HTML su GitHub Pages
GitHub Pages non permette redirect HTTP lato server. Si sostituisce solo `index.html` del sito storico con una pagina minima:

```html
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GPSR - Informazioni prodotti</title>
  <link rel="canonical" href="https://gpsr.in-shoes.it/">
  <meta http-equiv="refresh" content="0; url=https://gpsr.in-shoes.it/">
</head>
<body>
  <p>Le informazioni GPSR sono disponibili su
    <a href="https://gpsr.in-shoes.it/">gpsr.in-shoes.it</a>.</p>
</body>
</html>
```

- `meta refresh` con ritardo 0: il browser carica la pagina e passa subito allo snodo.
- Link visibile come **fallback accessibile** se il refresh è disattivato.
- Nessun JavaScript necessario.
- **I PDF restano dove sono**: eventuali QR che puntano direttamente a un PDF continuano a funzionare.

### Differenza rispetto a un vero redirect HTTP 301
| | `meta refresh` (GitHub Pages) | HTTP 301 |
|---|---|---|
| Dove avviene | nel browser, dopo aver scaricato la pagina | sul server, prima di qualsiasi contenuto |
| Codice HTTP del vecchio URL | 200 | 301 |
| Riconosciuto come spostamento permanente | parzialmente (motori di ricerca lo trattano in modo simile) | sì |
| Funziona senza HTML/browser (es. strumenti, alcuni lettori QR) | no: mostra la pagina col link | sì |
| Disponibile su `lost-95.github.io` | sì | no |

Per l'utente che inquadra il QR col telefono l'effetto è praticamente identico. Un 301 vero richiederebbe un hosting diverso per `lost-95.github.io`, che non è possibile: quel dominio è di GitHub.

## 4. Sequenza di applicazione (quando approvata)
1. Backup completo (punto 2.2).
2. Commit nel repository storico: solo `index.html` sostituito; PDF invariati.
3. Test immediato da 2 smartphone con un vecchio QR reale per ciascun marchio + verifica che i 10 PDF rispondano 200.
4. Monitoraggio nei giorni successivi.

## 5. Rollback
`git revert` del commit di redirect nel repository storico (oppure ricaricare l'`index.html` dal backup). Tempo di ripristino: pochi minuti. Dettagli in [ROLLBACK.md](ROLLBACK.md).

## 6. Rischio a lungo termine
Il sito storico dipende da un account personale. Se viene chiuso, rinominato, o il repository viene rinominato/reso privato, **i vecchi QR smettono di funzionare** e non esiste rimedio tecnico lato IN SHOES. Raccomandazioni: mantenere l'account e il repository attivi a tempo indeterminato, con credenziali e 2FA documentati e accessibili all'azienda; valutare l'aggiunta di un secondo amministratore. Il trasferimento del repository a un'organizzazione **non** è consigliato: cambierebbe l'URL `lost-95.github.io`.
