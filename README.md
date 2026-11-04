# Portale GPSR IN SHOES — `https://gpsr.in-shoes.it/`

Snodo di link statico gestito da **IN SHOES SRL**. Chi inquadra il QR code su una calzatura arriva qui e sceglie il marchio; ogni pulsante apre la pagina GPSR ufficiale di quel marchio.

| Pulsante  | Destinazione (validata dall'azienda, non modificare) |
|-----------|-------------------------------------------------------|
| CULT      | https://www.cultofficial.com/pages/gpsr               |
| DOCKSTEPS | https://www.docksteps.com/pages/gpsr                  |
| OXS       | https://www.oxs-shoes.it/pages/gpsr                   |

## Cosa è (e cosa non è) questo portale

- È **solo uno snodo di link**. Non dichiara IN SHOES SRL fabbricante delle calzature e non le attribuisce la responsabilità GPSR dei tre marchi. Identità e contatti dei fabbricanti stanno nelle pagine ufficiali dei marchi.
- **Non sostituisce** le informazioni obbligatorie sulle etichette fisiche e non è, da solo, prova di conformità.
- Non contiene backend, database, account, cookie, analytics, pixel, font o script esterni.

## Vecchi QR, nuovi QR, snodo, pagine dei marchi

```
VECCHI QR (già sulle scarpe di CULT, DOCKSTEPS, OXS — non modificabili)
   └─► https://lost-95.github.io/cult-milano-gpsr/      (sito storico, account GitHub personale)
          oggi: pagina storica + 10 PDF
          domani (Fase 2, solo dopo approvazione): inoltro allo snodo ─┐
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
├── public/               ← SOLO questa cartella va online
│   └── index.html        ← pagina approvata (unica modifica ammessa: l'H1)
├── docs/
│   ├── ARCHITETTURA.md
│   ├── PUBBLICAZIONE.md
│   ├── CHECKLIST_TEST.md
│   ├── ROLLBACK.md
│   └── MIGRAZIONE_URL_STORICO.md   ← Fase 2: solo piano, non applicato
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
- Il repository storico `lost-95/cult-milano-gpsr` non si tocca finché la Fase 2 non è approvata.
