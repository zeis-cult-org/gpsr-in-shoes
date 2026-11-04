# Rollback

Principio: i QR già stampati devono funzionare sempre. Nel dubbio si torna all'ultima versione funzionante, poi si analizza.

## 1. Lo snodo pubblica una versione errata
1. Individuare l'ultimo commit buono: `git log --oneline`.
2. `git revert <commit-errato>` (non riscrive la storia), poi push sul repository di pubblicazione (**con approvazione**).
3. GitHub Pages ripubblica in pochi minuti. Verificare con `scripts/verifica.ps1` e da smartphone.

## 2. `gpsr.in-shoes.it` non risponde (DNS, hosting o certificato)
- I **vecchi QR non sono coinvolti** finché la Fase 3 non è applicata: puntano ancora al sito storico.
- Controllare: record CNAME `gpsr` in GoDaddy, stato GitHub Pages (*Settings → Pages*), stato del certificato.
- Errore DNS: ripristinare il valore precedente del record (annotarlo sempre prima di ogni modifica).
- Hosting indisponibile a lungo: pubblicare la stessa cartella `public/` su un hosting alternativo (Cloudflare Pages / Netlify) e spostare il CNAME `gpsr` lì. Il QR non cambia.

## 3. Una pagina di marchio non è raggiungibile
- Non dipende dallo snodo: avvisare il responsabile web del marchio.
- Non cambiare la destinazione senza una nuova validazione aziendale. Se l'azienda approva un indirizzo sostitutivo temporaneo, aggiornare solo quel link, con commit dedicato, e ripristinarlo appena possibile.

## 4. Dopo la Fase 3 (redirect del sito storico attivo)
- Se lo snodo o i link non funzionano: nel repository storico `lost-95/cult-milano-gpsr` ripristinare l'`index.html` originale con `git revert` del commit di redirect (o ricaricando il file dal backup). I PDF non vengono mai rimossi, quindi restano disponibili in ogni caso.
- Backup disponibili: copia locale `gpsr-cult/gpsr_basic.zip` (30/07/2026, verificata identica al sito online il 4/11/2026) e il backup completo da eseguire prima della Fase 3 (vedi [MIGRAZIONE_URL_STORICO.md](MIGRAZIONE_URL_STORICO.md)).

## Contatti (da compilare)
| Ruolo | Nome | Contatto |
|---|---|---|
| Responsabile snodo e account GitHub `<ACCOUNT>` | | |
| Accesso DNS GoDaddy | | |
| Titolare account `lost-95` (sito storico) | | |
| Web CULT / DOCKSTEPS / OXS | | |
