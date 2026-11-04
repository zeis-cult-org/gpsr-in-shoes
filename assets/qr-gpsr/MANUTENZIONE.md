# Manutenzione: tenere raggiungibile il QR nel tempo

Il QR stampato contiene per sempre `https://gpsr.in-shoes.it/`. Non si può aggiornare: deve restare raggiungibile per tutta la vita dei prodotti. Il QR non dipende da servizi di QR dinamici, ma dipende da dominio, DNS, hosting e HTTPS.

## Catena di dipendenze

| Elemento | Dove | Cosa può rompere il QR | Prevenzione |
|---|---|---|---|
| Dominio `in-shoes.it` | GoDaddy, intestato a IN SHOES SRL | Scadenza o mancato rinnovo | **Rinnovo automatico attivo**, metodo di pagamento valido, scadenza segnata in calendario con promemoria 60 giorni prima. Contatti dell'intestatario aggiornati. |
| DNS | GoDaddy, zona `in-shoes.it` | Cancellazione o modifica di `CNAME gpsr` o del TXT di verifica | Non toccare i due record (vedi `docs/REGISTRO_OPERAZIONI.md`). Niente record wildcard `*.in-shoes.it`. Se si aggiungono record CAA, includere `letsencrypt.org`. |
| Hosting | GitHub Pages, account `zeis-cult-org`, repository `gpsr-in-shoes` | Account chiuso o rinominato, repository rinominato, eliminato o reso privato, Pages disattivato | **Non rinominare** account né repository (il CNAME punta a `zeis-cult-org.github.io`). 2FA attiva, codici di recupero conservati in luogo sicuro aziendale. Aggiungere al più presto un secondo amministratore di continuità. |
| HTTPS | Certificato Let's Encrypt gestito da GitHub | Rinnovo bloccato da DNS errato o da CAA restrittivi | Rinnovo automatico. Controllare la scadenza del certificato a ogni verifica periodica. |
| Pagine dei marchi | cultofficial.com, docksteps.com, oxs-shoes.it | Pagina `/pages/gpsr` spostata o rimossa | Avvisare i referenti web: l'indirizzo `/pages/gpsr` va mantenuto. Se cambia, si aggiorna lo snodo (commit approvato); il QR resta valido. |

## Backup
- Repository Git: copia su GitHub e copia locale in OneDrive (`Progetti/gpsr-in-shoes`), con storico completo.
- File master del QR: in `assets/qr-gpsr/` con `SHA256SUMS.txt`. Lo script `genera_qr.py` li rigenera identici, con le versioni di `requirements.txt`.
- Conservare in archivio aziendale anche il PDF inviato alla tipografia e la prova fisica approvata.

## Controlli periodici

| Frequenza | Controllo |
|---|---|
| Mensile | `powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1 -SitoUrl https://gpsr.in-shoes.it/` → esito OK |
| Trimestrale | Lettura di un'etichetta reale con uno smartphone; apertura dei tre marchi. Scadenza del certificato HTTPS oltre 30 giorni. |
| Annuale | Scadenza del dominio e rinnovo automatico; accesso all'account GitHub e 2FA funzionanti; secondo amministratore presente; DNS conforme a `docs/REGISTRO_OPERAZIONI.md`. |
| A ogni nuova tiratura | Il fornitore usa il PDF master (SHA-256 invariato); prova fisica approvata. |

## In caso di problemi
- Il sito non risponde → `docs/ROLLBACK.md`. Se GitHub non fosse più utilizzabile, si pubblica la cartella `public/` su un altro hosting e si sposta il CNAME `gpsr`: **il QR non cambia**.
- **Mai** sostituire il QR stampato con un servizio di QR dinamico o con un URL abbreviato.

## Rigenerazione dei file (solo se necessario)
```powershell
python -m venv C:\venv-qr
C:\venv-qr\Scripts\python -m pip install -r assets\qr-gpsr\requirements.txt
C:\venv-qr\Scripts\python assets\qr-gpsr\genera_qr.py
C:\venv-qr\Scripts\python assets\qr-gpsr\verifica_qr.py
```
Con le stesse versioni delle librerie, gli SHA-256 devono coincidere con quelli registrati. Se cambiano, il codice va ricontrollato con `verifica_qr.py` e collaudato fisicamente prima della stampa.
