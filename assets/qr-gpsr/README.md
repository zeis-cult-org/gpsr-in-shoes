# QR code ufficiale GPSR — IN SHOES SRL

**URL codificato (esatto):** `https://gpsr.in-shoes.it/`
**Uso:** unico QR per le etichette di CULT, DOCKSTEPS e OXS. QR statico: nessun servizio intermedio, nessuna scadenza.
**Stato:** test digitali superati (34/34) · **in attesa di collaudo su etichetta fisica** prima della produzione.

Questa cartella **non** viene pubblicata sul sito: il workflow pubblica solo `public/`.

## Contenuto

| File | Descrizione |
|---|---|
| `GPSR_IN_SHOES_MASTER.svg` | Master vettoriale, 25 × 25 mm |
| `GPSR_IN_SHOES_STAMPA.pdf` | PDF vettoriale per la stampa, pagina 25 × 25 mm, nero K100 |
| `GPSR_IN_SHOES_PREVIEW.png` | Anteprima 1184 × 1184 px (non per la stampa) |
| `SHA256SUMS.txt` | Impronte SHA-256 dei tre file |
| `SCHEDA_TECNICA_QR.md` | Scheda per la tipografia / fornitore etichette |
| `CHECKLIST_COLLAUDO_FISICO.md` | Collaudo obbligatorio su etichetta reale |
| `REPORT_QA.md` | Esiti dei test digitali e test fisici da fare |
| `MANUTENZIONE.md` | Come mantenere il QR raggiungibile nel tempo |
| `genera_qr.py` | Rigenera i tre file (riproducibile byte per byte) |
| `verifica_qr.py` | Controllo qualità automatico |
| `requirements.txt` | Versioni esatte delle librerie Python |
| `genera_consegna.py` | Crea `CONSEGNA_UFFICIO_ETICHETTE/` (file con nomi chiari + istruzioni PDF) e il relativo ZIP |
| `verifica_consegna.py` | Controlla la consegna: file identici al master, QR leggibili, istruzioni complete, ZIP integro |

## Specifiche
QR versione 3 (29 × 29 moduli), modalità byte, correzione **Q**, maschera 4, quiet zone 4 moduli; 37 moduli su 25,00 mm → modulo 0,676 mm; nero puro su bianco; nessun logo.

## SHA-256

```
f727def629d998a1ecca8531384356202e9cfc0205f0fdfeb24a45c79ef13977  GPSR_IN_SHOES_MASTER.svg
c553c764f0640a75c588175d46b1492c6d5ba8c397dafd234e6269735410e6ad  GPSR_IN_SHOES_STAMPA.pdf
062d02d90940c767f0d53c3be6b94d23ddf0f4e8d3ab5da87dcb3b5360fe2c8b  GPSR_IN_SHOES_PREVIEW.png
```

## Rigenerare e verificare
Vedi [MANUTENZIONE.md](MANUTENZIONE.md#rigenerazione-dei-file-solo-se-necessario). Il QR **non va modificato**: rigenerarlo serve solo a ricostruire file persi, e deve produrre gli stessi SHA-256.
