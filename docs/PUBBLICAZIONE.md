# Pubblicazione di `gpsr.in-shoes.it` e HTTPS

> Ogni passo che pubblica (push, attivazione Pages) o tocca il DNS richiede approvazione esplicita.
> Il progetto riguarda **solo** il sottodominio `gpsr.in-shoes.it`. Il sito principale `in-shoes.it` / `www.in-shoes.it`, la posta e gli altri record DNS non si toccano. Il repository storico `lost-95/cult-milano-gpsr` non si tocca.

## 1. Decisioni (aggiornate al 4/11/2026)

| Voce | Decisione / stato |
|---|---|
| Account GitHub | **`zeis-cult-org`** (https://github.com/zeis-cult-org), account esistente di CULT Milano. È un account *utente*, non un'organizzazione GitHub nonostante il nome: valgono i percorsi delle impostazioni del profilo. Nessuna nuova organizzazione o account. |
| Amministratore | Un solo amministratore e sviluppatore. Un secondo account di continuità verrà aggiunto in futuro. |
| Repository | https://github.com/zeis-cult-org/gpsr-in-shoes, **pubblico**, separato dal repository storico. ✅ Creato e allineato il 4/11/2026. |
| Hosting | GitHub Pages con sorgente **GitHub Actions** (`.github/workflows/pages.yml`). ✅ Attivo dal 4/11/2026. |
| URL provvisorio | https://zeis-cult-org.github.io/gpsr-in-shoes/ ✅ Online e collaudato il 4/11/2026. |
| Dominio | `https://gpsr.in-shoes.it/`, dominio di IN SHOES SRL. ✅ Online con HTTPS (Let's Encrypt, rinnovo automatico) ed Enforce HTTPS dal 4/11/2026. |
| DNS | Nameserver GoDaddy (`ns81/ns82.domaincontrol.com`). ✅ 4/11/2026: aggiunti solo TXT `_github-pages-challenge-zeis-cult-org.gpsr` e CNAME `gpsr → zeis-cult-org.github.io`. Stato precedente e rollback in [REGISTRO_OPERAZIONI.md](REGISTRO_OPERAZIONI.md). |
| Verifica dominio | ✅ `gpsr.in-shoes.it` verificato sull'account `zeis-cult-org` il 4/11/2026. Il record TXT va lasciato nel DNS. |
| Autore commit | `l.santarelli@cult-milano.it` (solo in questo repository). |

## 2. Procedura ufficiale GitHub (verificata sulla documentazione il 4/11/2026)

Fonti: docs.github.com → Pages → *Verifying your custom domain*, *Managing a custom domain*, *Using custom workflows*, *Securing your site with HTTPS*.

- **CNAME del sottodominio**: deve puntare a `zeis-cult-org.github.io`, **senza** nome del repository e senza il dominio `*.pages.github.io` mostrato nelle impostazioni.
- **Ordine**: GitHub raccomanda di *verificare* il dominio, poi di *aggiungerlo* nelle impostazioni Pages del repository, e **solo dopo** creare il CNAME. Creare il CNAME prima espone al rischio che un altro account usi il sottodominio.
- **Verifica dominio (account personale)**: foto profilo → *Settings* → *Pages* (impostazioni del profilo, non del repository) → *Add a domain*. GitHub mostra il record TXT da creare, nella forma `_github-pages-challenge-zeis-cult-org.<dominio>`. Il valore esatto si copia da GitHub. Il TXT va lasciato nel DNS anche dopo la verifica.
  - Verificare un dominio protegge anche i suoi sottodomini immediati. La documentazione non dice esplicitamente se si può verificare direttamente il sottodominio `gpsr.in-shoes.it`. Si prova prima con `gpsr.in-shoes.it`; se GitHub non lo accetta si verifica `in-shoes.it`. Anche in quel caso si aggiunge solo un nuovo record TXT con nome `_github-pages-challenge-…`, che non tocca il sito principale né la posta.
- **Workflow personalizzato**: il file `CNAME` non serve ed è ignorato. Il dominio si imposta in *Settings → Pages → Custom domain*.
- **Permessi minimi** per `deploy-pages`: `pages: write` e `id-token: write`; più `contents: read` per leggere il codice. Ambiente predefinito: `github-pages`.
- **HTTPS**: dopo il salvataggio del dominio GitHub controlla il DNS e richiede un certificato Let's Encrypt. Di solito serve meno di un'ora; l'opzione *Enforce HTTPS* può comparire fino a 24 ore dopo.
- **Da evitare**: record wildcard (`*.in-shoes.it`), rischio di takeover. Se in futuro si aggiungono record CAA al dominio, uno deve autorizzare `letsencrypt.org`.

## 3. Controllo del workflow (`.github/workflows/pages.yml`)

| Requisito | Esito |
|---|---|
| Pubblica solo `public/` | ✅ `upload-pages-artifact` con `path: public`. Documentazione e script non vengono pubblicati. |
| Permessi minimi | ✅ `contents: read`, `pages: write`, `id-token: write`. Nessun altro permesso. |
| Credenziali | ✅ `checkout` con `persist-credentials: false`. |
| Quando parte | Push su `main` o avvio manuale. Un solo deploy alla volta (`concurrency`). |
| Controlli prima del deploy | ✅ File presente, MD5 della pagina approvata, H1 esatto, tre link presenti. Se falliscono, non pubblica. |
| Versioni azioni | `checkout@v7`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`: ultime versioni al 4/11/2026, su Node 24. Le versioni precedenti funzionavano ma GitHub segnalava che usavano Node 20, ormai deprecato. |
| Verifica sul sito pubblicato | ✅ Pagina servita identica (MD5); `README.md`, `docs/`, `scripts/`, `.github/` rispondono 404; HTTP reindirizza a HTTPS. |

## 4. Passi di pubblicazione

Prima di ogni passo DNS: screenshot della zona DNS di `in-shoes.it` su GoDaddy (serve per il rollback).

### A. Repository e push
1. **(Tu, nel browser)** Accedi con l'account `zeis-cult-org` → *New repository* → nome `gpsr-in-shoes`, **Public**, **senza** README, .gitignore o licenza → *Create repository*.
2. **(Io, con la tua approvazione)** Collego il repository e faccio il push:
   ```bash
   git remote add origin https://github.com/zeis-cult-org/gpsr-in-shoes.git
   ```
   ```bash
   git push -u origin main
   ```
   Al primo push Git Credential Manager apre il browser per l'accesso a GitHub: lo completi tu. Nessuna password passa da me.

### B. GitHub Pages e URL provvisorio
3. **(Tu, con me)** Repository → *Settings → Pages → Build and deployment → Source* = **GitHub Actions**.
4. Il workflow parte (scheda *Actions*), oppure si avvia a mano con *Run workflow*.
5. **(Io)** Verifico `https://zeis-cult-org.github.io/gpsr-in-shoes/` con `scripts/verifica.ps1 -SitoUrl …` e in anteprima desktop e smartphone.

### C. Verifica del dominio (TXT)
6. **(Tu)** *Settings del profilo → Pages → Add a domain* → `gpsr.in-shoes.it`. Copia nome e valore del TXT esattamente come li mostra GitHub.
7. **(Tu su GoDaddy, con la mia approvazione)** Aggiungi **solo** quel record TXT. Il campo "Nome" va scritto senza `.in-shoes.it` finale.
8. Controllo:
   ```powershell
   Resolve-DnsName -Type TXT _github-pages-challenge-zeis-cult-org.gpsr.in-shoes.it
   ```
   Poi su GitHub: menu ⋯ accanto al dominio → *Continue verifying* → *Verify*.

### D. Dominio personalizzato e CNAME
9. **(Tu)** Repository → *Settings → Pages → Custom domain* = `gpsr.in-shoes.it` → *Save*. Il controllo DNS risulterà in errore finché non c'è il CNAME: è normale.
10. **(Tu su GoDaddy, con la mia approvazione)** Aggiungi **solo**:

    | Tipo  | Nome  | Valore | TTL |
    |-------|-------|--------|-----|
    | CNAME | `gpsr` | `zeis-cult-org.github.io` | 1 ora |

11. Controllo:
    ```powershell
    Resolve-DnsName -Type CNAME gpsr.in-shoes.it
    ```

### E. HTTPS e collaudo
12. Quando GitHub mostra il controllo DNS riuscito e il certificato pronto: *Enforce HTTPS*. Se dopo qualche minuto il certificato non parte: *Remove*, reinserisci il dominio e *Save*.
13. **(Io)** Verifiche finali:
    ```powershell
    curl.exe -I https://gpsr.in-shoes.it/
    curl.exe -I http://gpsr.in-shoes.it/
    powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1 -SitoUrl https://gpsr.in-shoes.it/
    ```
    Attesi: HTTPS `200`, HTTP reindirizza (`301`) a HTTPS, certificato valido; `in-shoes.it` e la posta funzionano come prima.
14. [CHECKLIST_TEST.md](CHECKLIST_TEST.md) completa, compresi CULT, DOCKSTEPS e OXS da desktop e da smartphone reali. Solo dopo: Fase 3 (redirect storico e nuovi QR).

## 5. Aggiornamenti futuri
Modifica autorizzata → `scripts/verifica.ps1` → commit → push su `main` (con approvazione) → il workflow ripubblica in pochi minuti. Problemi: [ROLLBACK.md](ROLLBACK.md).

Account Git su questo PC: Git Credential Manager conserva due account GitHub. Ogni repository indica il proprio nell'indirizzo di push:
- `gpsr-in-shoes` → `https://zeis-cult-org@github.com/zeis-cult-org/gpsr-in-shoes.git`
- sito storico `cult-milano-gpsr` (copia di lavoro nell'archivio Backups) → `https://lost-95@github.com/lost-95/cult-milano-gpsr.git`
Su un altro PC, al primo push si autorizza l'account corretto con il codice dispositivo (`https://github.com/login/device`).

## 6. Anteprima locale

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory public
```

Apri http://localhost:8000/ . Da smartphone sulla stessa Wi-Fi togli `--bind 127.0.0.1` e apri `http://<IP-del-PC>:8000/`. HTTPS si verifica solo sul dominio pubblicato.
