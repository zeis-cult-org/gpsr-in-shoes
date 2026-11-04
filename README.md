# Portale GPSR IN SHOES — `https://gpsr.in-shoes.it/`

Snodo di link statico gestito da **IN SHOES SRL**. Chi inquadra il QR code su una calzatura arriva qui e sceglie il marchio; ogni pulsante apre la pagina GPSR ufficiale di quel marchio.

| Pulsante  | Destinazione (validata dall'azienda, non modificare) |
|-----------|-------------------------------------------------------|
| CULT      | https://www.cultofficial.com/pages/gpsr               |
| DOCKSTEPS | https://www.docksteps.com/pages/gpsr                  |
| OXS       | https://www.oxs-shoes.it/pages/gpsr                   |

**`https://gpsr.in-shoes.it/` è l'URL unico da stampare nei QR futuri di tutti e tre i marchi.**

**Stato (4/11/2026):** online su `https://gpsr.in-shoes.it/` con HTTPS, pubblicato da `zeis-cult-org/gpsr-in-shoes` tramite GitHub Pages. Collaudo tecnico completato; restano le prove su smartphone reali e la prova di stampa dei QR ([docs/CHECKLIST_TEST.md](docs/CHECKLIST_TEST.md)). Storico interventi: [docs/REGISTRO_OPERAZIONI.md](docs/REGISTRO_OPERAZIONI.md).

## Decisioni confermate (4/11/2026)

| Tema | Decisione |
|---|---|
| Indirizzo ufficiale | `gpsr.in-shoes.it`. Dominio `in-shoes.it` acquistato il 3/11/2026 per IN SHOES SRL. |
| Sito principale | `in-shoes.it` / `www.in-shoes.it` **fuori dal progetto**: non si toccano. Si lavora solo sul sottodominio `gpsr`. |
| Hosting | GitHub Pages con GitHub Actions, sull'**account GitHub esistente di CULT Milano `zeis-cult-org`** (nessuna nuova organizzazione o account), repository `gpsr-in-shoes` separato da quello storico. Un secondo account di continuità verrà aggiunto in futuro. |
| DNS | Nessun record modificato. L'accesso alla gestione DNS si affronta in fase di pubblicazione. |
| Pagina | `public/index.html` è la versione definitiva approvata, inserita senza modifiche (H1 già aggiornato). |
| Vecchi QR | Portano a scarpe di tutti e tre i marchi: in futuro andranno alla **homepage dello snodo**, mai direttamente a CULT. |
| Repository storico | Non modificato. Il futuro redirect riguarderà solo la homepage; i 10 PDF e i loro URL restano. |

## Cosa è (e cosa non è) questo portale

- È **solo uno snodo di link**. Non dichiara IN SHOES SRL fabbricante delle calzature e non le attribuisce la responsabilità GPSR dei tre marchi. Identità e contatti dei fabbricanti stanno nelle pagine ufficiali dei marchi.
- **Non sostituisce** le informazioni obbligatorie sulle etichette fisiche e non è, da solo, prova di conformità.
- Non contiene backend, database, account, cookie, analytics, pixel, font o script esterni.

## Vecchi QR, nuovi QR, snodo, pagine dei marchi

```
VECCHI QR (già sulle scarpe di CULT, DOCKSTEPS, OXS — non modificabili)
   └─► https://lost-95.github.io/cult-milano-gpsr/      (sito storico, account GitHub personale)
          oggi: pagina storica + 10 PDF
          domani (Fase 3, solo dopo approvazione): inoltro allo snodo ─┐
                                                                       │
NUOVI QR (tutti e tre i marchi)                                        │
   └─► https://gpsr.in-shoes.it/   ◄──────────────────────────────────┘
          SNODO (questo progetto, cartella public/)
            ├─► CULT       https://www.cultofficial.com/pages/gpsr
            ├─► DOCKSTEPS  https://www.docksteps.com/pages/gpsr
            └─► OXS        https://www.oxs-shoes.it/pages/gpsr
                 PAGINE DEI MARCHI = contenuto GPSR ufficiale
```

## Struttura

```
gpsr-in-shoes/
├── .github/workflows/
│   └── pages.yml         ← pubblicazione su GitHub Pages (solo public/)
├── assets/qr-gpsr/       ← QR ufficiale: master SVG/PDF/PNG, scheda tipografia, QA, script (NON pubblicato)
├── public/               ← SOLO questa cartella va online
│   └── index.html        ← pagina approvata, definitiva, non modificare
├── docs/
│   ├── ARCHITETTURA.md
│   ├── PUBBLICAZIONE.md
│   ├── CHECKLIST_TEST.md
│   ├── ROLLBACK.md
│   ├── REGISTRO_OPERAZIONI.md     ← interventi su produzione, account e DNS
│   └── MIGRAZIONE_URL_STORICO.md   ← Fase 3: solo piano, non applicato
└── scripts/
    └── verifica.ps1      ← controlli automatici (H1, link, risorse esterne, raggiungibilità)
```

## Anteprima locale

```powershell
python -m http.server 8000 --directory public
```

Poi apri http://localhost:8000/ . Per provarla da smartphone sulla stessa rete Wi-Fi usa `http://<IP-del-PC>:8000/` (IP con `ipconfig`); potrebbe servire consentire Python nel firewall di Windows.

## Verifica automatica

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1
```

Controlla: presenza di `public/index.html`, H1 esatto, presenza dei tre URL, assenza di script/CSS/font esterni, risposta HTTP delle tre pagine dei marchi. Il collaudo completo è in [docs/CHECKLIST_TEST.md](docs/CHECKLIST_TEST.md).

## Regole di lavoro

- Commit Git locali e descrittivi. **Nessun push, deploy, modifica DNS o intervento in produzione senza approvazione esplicita.**
- Non ridisegnare la pagina, non aggiungere funzioni, non cambiare le tre destinazioni.
- Autore dei commit: email aziendale, impostata solo in questo repository (non a livello globale).
- File di testo con fine riga LF (`.gitattributes`), così l'HTML approvato resta identico byte per byte.
- Il repository storico `lost-95/cult-milano-gpsr` non si tocca finché la Fase 3 (redirect dei vecchi QR) non è approvata.
