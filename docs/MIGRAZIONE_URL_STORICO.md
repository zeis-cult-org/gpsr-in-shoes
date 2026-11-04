# Fase 3 — Migrazione dell'URL storico: piano operativo definitivo

Da `https://lost-95.github.io/cult-milano-gpsr/` a `https://gpsr.in-shoes.it/`.
**Stato: ✅ APPLICATA E COLLAUDATA il 04/11/2026** (commit `f3c2ae1` su `lost-95/cult-milano-gpsr`, online alle 15:52). Esito in §8. Rollback in §7, sempre disponibile.

## 1. Regole
- I vecchi QR sono su scarpe di **tutti e tre i marchi**: la homepage storica porta alla **homepage** dello snodo, dove il cliente sceglie CULT, DOCKSTEPS o OXS. **Mai direttamente a CULT.**
- Si modifica **un solo file**: `index.html` del repository `lost-95/cult-milano-gpsr`.
- I 10 PDF e i loro URL restano **invariati e raggiungibili**. Non si rinomina, non si trasferisce e non si cancella nulla.

## 2. Analisi (04/11/2026)

| Verifica | Risultato |
|---|---|
| URL contenuto nei vecchi QR | Decodificati i QR presenti nei file etichetta (Word dell'etichetta GPSR, sua copia nel pacchetto template, modello Avery 3489 in Excel): **tutti** `https://lost-95.github.io/cult-milano-gpsr/`, solo homepage. Nessun QR verso un PDF. I PDF si conservano comunque, perché potrebbero esistere altre tirature. |
| Sito storico | Repository pubblico, ramo `main`, ultimo commit `432f167` (30/07/2026), pubblicato direttamente dal ramo (nessun workflow). 11 file: `index.html` + 10 PDF. |
| Homepage online vs repository | Identiche (MD5 `2b4ec01e…`). |
| PDF online vs repository | 10/10 identici (SHA-256). |
| Varianti dell'URL | `/cult-milano-gpsr` → 301 → `/cult-milano-gpsr/`; `/`, `/index.html`, `/?parametri` → 200; HTTP → 301 → HTTPS. Le varianti servono tutte lo stesso `index.html`, quindi il redirect le copre tutte. |
| Cache | `Cache-Control: max-age=600`: modifica e rollback diventano visibili a tutti entro circa 10 minuti. |
| Contenuti equivalenti | Le pagine GPSR di CULT, DOCKSTEPS e OXS pubblicano gli stessi 10 PDF, **identici byte per byte** (30/30) a quelli storici. Dopo il redirect nessuna informazione va persa. |

## 3. Soluzione: pagina di redirect

File preparato: [`migrazione-storico/index.html`](../migrazione-storico/index.html). Sostituisce solo la homepage storica.

Tre meccanismi, in ordine di intervento:
1. `location.replace(...)` in JavaScript: reindirizza subito e **non lascia la pagina nella cronologia**, così il tasto Indietro non rimbalza.
2. `<meta http-equiv="refresh" content="0; url=https://gpsr.in-shoes.it/">`: funziona anche con JavaScript disattivato.
3. Link visibile "gpsr.in-shoes.it": fallback accessibile se entrambi fossero bloccati.

Più `<link rel="canonical">` verso lo snodo. Nessuna risorsa esterna, nessun cookie. Il testo è neutro e non indica alcun fabbricante.

**Perché non un 301:** `lost-95.github.io` è un dominio di GitHub e GitHub Pages non permette redirect HTTP lato server. Per chi inquadra il QR l'effetto è lo stesso: il passaggio è immediato.

## 4. Test già eseguiti in locale (04/11/2026)
Copia del sito storico (nuovo `index.html` + 10 PDF originali) servita in locale su `/cult-milano-gpsr/`:

| Test | Esito |
|---|---|
| `scripts/verifica-storico.ps1 -Fase prima` sul sito reale | ✅ homepage originale, 10 PDF invariati |
| `scripts/verifica-storico.ps1 -Fase dopo` sulla copia locale | ✅ redirect su `/`, `/index.html`, `/?src=qr`; 10 PDF invariati; destinazione 200 |
| Browser desktop: homepage locale → `https://gpsr.in-shoes.it/` | ✅ |
| Solo meta refresh (senza JavaScript) → `https://gpsr.in-shoes.it/` | ✅ |
| Vista smartphone 375 px → snodo, nessuno scorrimento orizzontale | ✅ |
| Tasto Indietro: torna alla pagina precedente, nessun loop | ✅ |
| HTML ben formato | ✅ |

## 5. Backup (già fatto)
- Copia **mirror** completa del repository storico (tutti i rami e la storia) + copia di lavoro, nell'archivio Backups aziendale, cartella `cult-milano-gpsr_backup_2026-11-04`.
- Backup precedente: zip del 30/07/2026, identico al sito online.
- Impronte di riferimento dei 10 PDF e della homepage dentro `scripts/verifica-storico.ps1`.

## 6. Procedura di applicazione (dopo approvazione)

| # | Passo | Chi |
|---|---|---|
| 1 | Aggiorna il backup (`git fetch` sul mirror) e conferma che `main` sia ancora `432f167` | Claude |
| 2 | `verifica-storico.ps1 -Fase prima` sul sito reale → OK | Claude |
| 3 | Verifica che `https://gpsr.in-shoes.it/` sia online e collaudato (`verifica.ps1 -SitoUrl`) | Claude |
| 4 | Nella copia di lavoro: sostituisce `index.html` con `migrazione-storico/index.html` (copia byte per byte), commit "Homepage: redirect verso https://gpsr.in-shoes.it/ (PDF invariati)" | Claude |
| 5 | Push su `lost-95/cult-milano-gpsr`. Richiede l'accesso dell'account **lost-95**: Git aprirà il browser dove sei collegato come lost-95, e l'autorizzazione la confermi tu | Claude + tu |
| 6 | Attesa della pubblicazione GitHub Pages (1–2 minuti) e della cache (fino a 10 minuti) | — |
| 7 | `verifica-storico.ps1 -Fase dopo` sul sito reale → OK | Claude |
| 8 | Browser desktop e smartphone: URL storico → snodo → CULT / DOCKSTEPS / OXS | Claude |
| 9 | Simulazione del vecchio QR: decodifica dell'immagine QR dell'etichetta storica e apertura dell'URL letto | Claude |
| 10 | **Prova fisica**: inquadrare con un telefono un'etichetta vecchia già stampata (CULT, DOCKSTEPS, OXS) | Tu |
| 11 | Registro operazioni aggiornato, commit nel progetto | Claude |

Finestra consigliata: orario di basso traffico. La modifica è reversibile in pochi minuti.

## 7. Rollback immediato
Condizioni: lo snodo non risponde, il redirect non funziona su qualche dispositivo, o un PDF non è più raggiungibile.

```bash
git -C <copia-di-lavoro-storico> revert --no-edit HEAD
git -C <copia-di-lavoro-storico> push origin main
```
In alternativa: ripubblicare l'`index.html` del backup (commit `432f167`), anche dall'editor web di GitHub. Visibile a tutti entro circa 10 minuti (cache). I PDF non vengono mai toccati, quindi restano disponibili in ogni caso. Dopo il rollback: `verifica-storico.ps1 -Fase prima` → OK.

## 8. Esito dell'applicazione (04/11/2026)

| Verifica | Esito |
|---|---|
| Push autorizzato dall'account `lost-95` (codice dispositivo), `432f167..f3c2ae1` | ✅ |
| Homepage online identica al file testato (MD5 `e4aaa8f3…`) | ✅ |
| `verifica-storico.ps1 -Fase dopo`: redirect su `/`, `/index.html`, `/?src=qr`; 10 PDF 200 con SHA-256 invariati; destinazione 200 | ✅ |
| Varianti: senza barra finale, `http://`, parametri → stessa pagina di redirect | ✅ |
| Browser desktop: URL storico → `https://gpsr.in-shoes.it/` (nuovo H1); tasto Indietro senza loop | ✅ |
| Smartphone (emulazione Android 375 px) → snodo, nessuno scorrimento orizzontale | ✅ |
| Senza JavaScript (pagina online con lo script rimosso) → snodo tramite meta refresh | ✅ |
| Simulazione scansione: QR decodificati dall'etichetta Word e dal modello Avery → URL storico → redirect → snodo 200 (MD5 pagina approvata) | ✅ |
| **Scansione di etichette fisiche già stampate**, eseguita dall'utente | ✅ reindirizzamento confermato |

## 9. Rischi residui
- **Dipendenza dallo snodo:** dopo la migrazione anche i vecchi QR dipendono da `gpsr.in-shoes.it` (dominio, DNS, GitHub). Mitigazione: [assets/qr-gpsr/MANUTENZIONE.md](../assets/qr-gpsr/MANUTENZIONE.md).
- **Account personale lost-95:** il sito storico resta necessario per sempre, perché i vecchi QR puntano lì. Se l'account o il repository venissero chiusi, rinominati o resi privati, i vecchi QR smetterebbero di funzionare. Mantenere account e repository attivi, con 2FA e codici di recupero conservati. **Non trasferire** il repository: cambierebbe l'URL.
- **Cache fino a 10 minuti** dopo la modifica: in quella finestra alcuni utenti vedono ancora la vecchia pagina, che resta valida.
- **Percorsi sconosciuti** (es. errori di battitura) restano 404 come oggi. Facoltativo, da valutare a parte: un `404.html` che rimandi allo snodo.
