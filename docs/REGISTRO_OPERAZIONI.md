# Registro operazioni

Operazioni su produzione, account e DNS. Una riga per intervento, la più recente in fondo.

| Data | Operazione | Esito | Note |
|---|---|---|---|
| 04/11/2026 | Creato repository pubblico `zeis-cult-org/gpsr-in-shoes` (vuoto, senza README/licenza) | ✅ | Primo tentativo fallito per disservizio GitHub (errore 504), secondo riuscito. |
| 04/11/2026 | Primo push di `main` (4 commit, fino a `d1847cb`) | ✅ | Accesso Git con codice dispositivo autorizzato dall'account `zeis-cult-org`. Annullato un accesso via browser che puntava per errore a `lost-95`. |
| 04/11/2026 | Primo workflow automatico | ❌ atteso | Fermo a `configure-pages`: Pages non ancora attivo. Nessuna pubblicazione. |
| 04/11/2026 | GitHub Pages attivato, sorgente "GitHub Actions"; workflow rilanciato | ✅ | Sito su https://zeis-cult-org.github.io/gpsr-in-shoes/ |
| 04/11/2026 | Collaudo URL provvisorio | ✅ | MD5 identico all'approvato; solo `public/` online; HTTP→HTTPS 301; `verifica.ps1` OK; CULT, DOCKSTEPS, OXS aperti con clic reali su desktop e vista smartphone. |

## Zona DNS `in-shoes.it` prima delle modifiche (GoDaddy, 04/11/2026)

Riferimento per il rollback: questi 7 record **non vanno modificati**.

| Tipo | Nome | Dati | TTL |
|---|---|---|---|
| A | `@` | Parked | 600 secondi |
| NS | `@` | `ns81.domaincontrol.com.` | 1 ora |
| NS | `@` | `ns82.domaincontrol.com.` | 1 ora |
| CNAME | `www` | `in-shoes.it.` | 1 ora |
| CNAME | `_domainconnect` | `_domainconnect.gd.domaincontrol.com.` | 1 ora |
| SOA | `@` | Nameserver primario: `ns81.domaincontrol.com.` | 1 ora |
| TXT | `_dmarc` | `v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;` | 1 ora |

Record da aggiungere (gli unici):

| Tipo | Nome | Dati | TTL |
|---|---|---|---|
| TXT | `_github-pages-challenge-zeis-cult-org.gpsr` | `a9b3a544417a9bb9c57ee922cfc66b` | 1 ora |
| CNAME | `gpsr` | `zeis-cult-org.github.io` | 1 ora |

Rollback DNS: eliminare solo questi due record.

## Dominio definitivo

| Data | Operazione | Esito | Note |
|---|---|---|---|
| 04/11/2026 | Push `43ef148` (azioni su Node 24, controllo MD5 nel workflow) | ✅ | Ripubblicazione riuscita, pagina invariata, avviso Node 20 risolto. |
| 04/11/2026 | Dominio `gpsr.in-shoes.it` aggiunto ai domini verificati dell'account `zeis-cult-org` | ✅ | GitHub accetta direttamente il sottodominio. |
| 04/11/2026 | Custom domain `gpsr.in-shoes.it` impostato nel repository (prima del CNAME, come da documentazione GitHub) | ✅ | L'URL provvisorio da qui rimanda al dominio definitivo. |
| 04/11/2026 | Inseriti su GoDaddy (dall'utente) i 2 record TXT e CNAME sopra indicati | ✅ | Visibili da DNS pubblico (8.8.8.8). Altri record verificati invariati, `_dmarc` compreso. |
| 04/11/2026 | Verifica dominio su GitHub | ✅ | "Successfully verified gpsr.in-shoes.it". |
| 04/11/2026 | `http://gpsr.in-shoes.it/` | ✅ | Serve la pagina approvata (MD5 identico). |
| 04/11/2026 | Certificato HTTPS | ✅ | Let's Encrypt (YR1), CN e SAN `gpsr.in-shoes.it`, valido dal 04/11/2026 al 02/02/2027. Rinnovo automatico gestito da GitHub. |
| 04/11/2026 | Enforce HTTPS attivato | ✅ | GitHub: "DNS check successful", "Your site is live at https://gpsr.in-shoes.it/". |
| 04/11/2026 | Collaudo dominio definitivo | ✅ | MD5 della pagina servita identico all'approvato; `verifica.ps1 -SitoUrl https://gpsr.in-shoes.it/` OK; file interni 404; URL provvisorio → 301 verso `https://gpsr.in-shoes.it/`; `http://gpsr.in-shoes.it/` → 301 verso HTTPS (attivo dopo circa 10 minuti di cache CDN); nessuna richiesta esterna né cookie; CULT, DOCKSTEPS, OXS aperti con clic reali su desktop e vista smartphone (375 px, nessuno scorrimento orizzontale). |
| 04/11/2026 | Controlli di non regressione | ✅ | `in-shoes.it` risponde come prima; sito storico `lost-95.github.io/cult-milano-gpsr/` e PDF rispondono 200; record DNS esistenti invariati. |
| 04/11/2026 | Revisione autorizzata della pagina: H1 ridotto a "GPSR - Sicurezza dei prodotti." (tolto "Informazioni sempre accessibili.") e dimensione H1 da clamp(2.3rem,6.5vw,4.6rem) a clamp(1.6rem,4vw,2.6rem) | ✅ | Nuovo MD5 `3744f3a5888a95dbccb14a9249328a0d`, aggiornato in `verifica.ps1` e nel workflow. Pubblicato con il push fino a `5e9551b`. |
| 04/11/2026 | Push di 4 commit (QR, fix H1, manutenzione, piano Fase 3) fino a `5e9551b` | ✅ | Deploy riuscito; nuovo H1 online (MD5 approvato); `verifica.ps1` OK; CULT, DOCKSTEPS, OXS con clic reali; file QR e migrazione non pubblicati (404); QR master decodificato → `https://gpsr.in-shoes.it/` → pagina nuova. |
| 04/11/2026 | Fase 3 preparata: backup mirror aggiornato (`main` = `432f167`), `verifica-storico.ps1 -Fase prima` OK, commit locale `f3c2ae1` nel repository storico (solo `index.html`, diff in `migrazione-storico/index.html.diff`) | ✅ | Autorizzato dall'utente. |
| 04/11/2026 | **Fase 3 applicata**: push `432f167..f3c2ae1` su `lost-95/cult-milano-gpsr` (account `lost-95`, codice dispositivo) | ✅ | Online alle 15:52. `verifica-storico.ps1 -Fase dopo` OK (redirect + 10 PDF invariati); desktop, smartphone, senza JavaScript e simulazione QR storici → `https://gpsr.in-shoes.it/`. Rollback: `git revert f3c2ae1` + push (vedi `docs/MIGRAZIONE_URL_STORICO.md` §7). |
| 04/11/2026 | Collaudo fisico dei QR storici: scansione di etichette vecchie già stampate, eseguita dall'utente | ✅ | Reindirizzamento a `https://gpsr.in-shoes.it/` confermato. **Fase 3 completata e collaudata.** |
| 04/11/2026 | Preparata `CONSEGNA_UFFICIO_ETICHETTE/` + ZIP per l'addetta etichette | ✅ | File di stampa identico al master (SHA-256 `c553c764…`); istruzioni PDF in italiano semplice (QR vettoriale a 25 mm reali, regole, specifiche, prova di stampa vs produzione, checklist); `verifica_consegna.py` 31/31 OK; ZIP riproducibile. Revisione: rimosso `00_LEGGIMI.txt`; istruzioni ridotte a una pagina (file, QR reale, come va stampato), senza riquadro regole, prova di stampa e firme. |
| — | Collaudo fisico del nuovo QR 25 × 25 mm su etichetta reale | ⏳ | Da coordinare direttamente con l'ufficio etichette (non più descritto nelle istruzioni); produzione solo dopo approvazione del responsabile GPSR. |

Da completare a cura dell'azienda: prova da smartphone reali (iPhone e Android, rete mobile) e prova di stampa dei QR, come da [CHECKLIST_TEST.md](CHECKLIST_TEST.md). Fase 3 completata e collaudata il 04/11/2026. Resta il collaudo fisico del nuovo QR 25 × 25 mm prima della produzione industriale (`CONSEGNA_UFFICIO_ETICHETTE/`).
