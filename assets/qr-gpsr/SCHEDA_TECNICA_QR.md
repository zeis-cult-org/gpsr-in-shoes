# Scheda tecnica QR GPSR — per la tipografia / fornitore etichette

**Committente:** IN SHOES SRL · **Uso:** etichette calzature CULT, DOCKSTEPS, OXS · **Versione master:** 04/11/2026

## 1. File da usare

| File | Uso | SHA-256 |
|---|---|---|
| `GPSR_IN_SHOES_STAMPA.pdf` | **File di stampa** (vettoriale) | `c553c764f0640a75c588175d46b1492c6d5ba8c397dafd234e6269735410e6ad` |
| `GPSR_IN_SHOES_MASTER.svg` | Alternativa vettoriale per impaginazione | `f727def629d998a1ecca8531384356202e9cfc0205f0fdfeb24a45c79ef13977` |
| `GPSR_IN_SHOES_PREVIEW.png` | Solo anteprima, **non per la stampa** | `062d02d90940c767f0d53c3be6b94d23ddf0f4e8d3ab5da87dcb3b5360fe2c8b` |

Non rigenerare il QR con altri strumenti o servizi: usare questi file. Per controllare l'integrità, confrontare l'SHA-256 (Windows: `certutil -hashfile GPSR_IN_SHOES_STAMPA.pdf SHA256`).

## 2. Specifiche del codice

| Voce | Valore |
|---|---|
| Contenuto | `https://gpsr.in-shoes.it/` (esatto, minuscolo, con `/` finale) |
| Tipo | QR Code (ISO/IEC 18004), statico, versione 3 (29 × 29 moduli), modalità byte |
| Correzione errori | Livello **Q** (circa 25%) |
| Quiet zone | 4 moduli per lato (2,70 mm), **inclusa** nel formato |
| Formato totale | **25,00 × 25,00 mm**, margine bianco incluso |
| Modulo (X-dimension) | **0,676 mm** (25 mm / 37 moduli) |
| Colore | Nero pieno **K100** (C0 M0 Y0 K100) su bianco. Nessun nero composto (rich black). |
| Elementi sovrapposti | Nessuno: niente logo, testo, cornici o retini dentro i 25 × 25 mm |

## 3. Regole di stampa
1. Stampare a **100%**, senza adattare alla pagina. Il lato misurato deve essere 25,0 mm (tolleranza ±0,2 mm).
2. Non deformare: il rapporto deve restare 1:1. Non ruotare di angoli diversi da 0°, 90°, 180° o 270°.
3. Non invertire i colori (niente bianco su nero) e non usare colori diversi dal nero.
4. Il supporto sotto il QR deve essere bianco o molto chiaro e opaco. Se l'etichetta non è bianca, stampare un fondo bianco pieno di 25 × 25 mm.
5. Nessun altro elemento grafico deve entrare nella quiet zone: i 25 × 25 mm sono riservati al QR.
6. Evitare superfici lucide o riflettenti sopra il QR; meglio un supporto opaco.
7. **Stampanti a trasferimento termico o a getto**: con risoluzioni basse, un modulo da 0,676 mm non corrisponde a un numero intero di punti (ad esempio 5,4 punti a 203 dpi), e questo crea moduli irregolari. Comunicare la risoluzione della stampante: se serve, si adatta la dimensione a un numero intero di punti per modulo (per esempio 300 dpi → 8 punti = 25,06 mm; 203 dpi → 6 punti = 27,8 mm) **e si ripete il collaudo**.
8. Offset e flexo: applicare la consueta compensazione dell'ingrossamento del punto, così che i moduli neri non si allarghino.

## 4. Riduzioni e varianti
- **Non ridurre sotto 25 mm** senza un nuovo collaudo fisico. Ingrandire è consentito, purché proporzionale.
- Qualsiasi variante di dimensione o di supporto richiede una prova di stampa approvata da IN SHOES SRL.

## 5. Prova richiesta prima della tiratura
Inviare a IN SHOES SRL almeno una **prova su etichetta reale**, con lo stesso materiale, la stessa stampante e lo stesso formato della produzione. La tiratura parte solo dopo l'approvazione scritta, secondo la [checklist di collaudo fisico](CHECKLIST_COLLAUDO_FISICO.md).

Facoltativo, se il fornitore ha un verificatore di codici: grado di qualità ISO/IEC 15415 pari a **C (1,5)** o superiore.

## Contatto tecnico
IN SHOES SRL — riferimento progetto GPSR: ______________________ (email/telefono)
