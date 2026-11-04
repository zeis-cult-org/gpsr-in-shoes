# Report controllo qualità — QR GPSR IN SHOES

Data: 04/11/2026 · Script: `verifica_qr.py` · Esito digitale: **34/34 controlli superati**
Stato: **pronto per la prova di stampa**. Non ancora approvato per la produzione: manca il collaudo fisico.

## 1. Verifica preliminare del sito (04/11/2026)

| Controllo | Esito |
|---|---|
| `https://gpsr.in-shoes.it/` risponde 200, certificato valido (Let's Encrypt, CN `gpsr.in-shoes.it`, scade 02/02/2027) | ✅ |
| `http://gpsr.in-shoes.it/` → 301 → `https://gpsr.in-shoes.it/` (un solo reindirizzamento) | ✅ |
| Pagina servita identica a quella approvata (MD5 `31fd181b…`) | ✅ |
| CULT, DOCKSTEPS, OXS `/pages/gpsr` rispondono 200 | ✅ |

## 2. Test digitali (eseguiti)

| Area | Controllo | Esito |
|---|---|---|
| Contenuto | Decodifica con **ZXing-C++** e **OpenCV** (motori indipendenti) di SVG, PDF e PNG = `https://gpsr.in-shoes.it/` esatto | ✅ |
| Contenuto | Livello di correzione letto dal decodificatore = **Q**; simbologia `]Q1` (QR modello 2) | ✅ |
| Identità | SVG (sorgente e renderizzato), PDF renderizzato e PNG identici **modulo per modulo** alla matrice di riferimento (37 × 37 con quiet zone) | ✅ |
| Struttura | Versione 3-Q, maschera 4, modalità byte, nessun aumento automatico del livello di correzione | ✅ |
| Margini | Quiet zone di 4 moduli bianchi su ogni lato (2,70 mm) | ✅ |
| Orientamento | Pattern di posizione in alto a sinistra, alto a destra e basso a sinistra | ✅ |
| Proporzioni | 1:1 in tutti i formati | ✅ |
| Contrasto | SVG solo `#000000`/`#FFFFFF`; PNG solo 0/255 (contrasto 21:1); PDF solo CMYK 0/0/0/0 e 0/0/0/100 | ✅ |
| PDF | Struttura valida; una pagina **25,000 × 25,000 mm** (MediaBox = TrimBox); solo vettoriale (0 immagini raster); nessun testo | ✅ |
| SVG | `width="25mm" height="25mm"`; nessuna immagine, testo visibile, link o script | ✅ |
| PNG | 1184 × 1184 px, 32 px per modulo, metadati 1202,9 dpi = 25,000 mm | ✅ |
| Leggibilità | 25 mm renderizzati a 72, 100, 150, 200, 300 e 600 dpi: letto da ZXing a tutte le risoluzioni; da OpenCV da 100 dpi in su (a 72 dpi = 1,9 px/modulo, sotto il limite di OpenCV) | ✅ |
| Robustezza | Letto con sfocatura gaussiana forte, rotazione di 20° e capovolgimento | ✅ |
| Riproducibilità | Due generazioni consecutive danno file identici byte per byte | ✅ |
| Integrità | SHA-256 dei tre file uguali a `SHA256SUMS.txt` | ✅ |
| Controllo visivo | Anteprima esaminata: tre pattern d'angolo corretti, margine uniforme, nessun elemento sovrapposto | ✅ |

## 3. Test che richiedono una stampa fisica (da eseguire)

I test digitali non possono verificare questi aspetti; vanno fatti con la [checklist di collaudo fisico](CHECKLIST_COLLAUDO_FISICO.md):

- dimensione reale stampata (25,0 mm) e assenza di deformazioni;
- resa del nero e del supporto: ingrossamento del punto, sbavature, riflessi, opacità;
- compatibilità della dimensione del modulo con la risoluzione della stampante (stampa termica: vedi scheda tecnica, punto 3.7);
- lettura con smartphone reali (iOS e Android), a distanze, luci e inclinazioni diverse;
- lettura con etichetta applicata sul prodotto o sulla scatola;
- facoltativo: grado ISO/IEC 15415 con verificatore professionale.

## 4. Ambiente usato
Python 3.14.6; segno 1.6.6, Pillow 13.0.0, PyMuPDF 2.1, zxing-cpp 3.1.1, opencv-python-headless 5.0.0.93, numpy 2.5.4 (`requirements.txt`). Nessun servizio online usato per generare o leggere il codice.
