# Checklist collaudo fisico del QR GPSR

Il QR è **pronto per la produzione industriale solo dopo questo collaudo** su un'etichetta reale (stesso materiale, stampante e formato della produzione).

Data: ________  Fornitore: ________________  Materiale etichetta: ________________  Stampante / tecnologia: ________________ dpi: ______

## A. Misure e aspetto (righello o calibro)
- [ ] Lato del QR, margine bianco incluso: **25,0 mm** (±0,2 mm). Misurato: ______ mm
- [ ] Forma quadrata, non deformata (stessa misura in orizzontale e in verticale)
- [ ] Margine bianco di circa 2,7 mm su tutti e quattro i lati, senza altri elementi grafici
- [ ] Nero pieno e uniforme, fondo bianco; nessuna sbavatura, nessun modulo mancante o unito ai vicini
- [ ] Supporto opaco; nessun riflesso che impedisca la lettura

## B. Lettura con smartphone
Fotocamera nativa, senza app dedicate. Ogni lettura deve mostrare **gpsr.in-shoes.it** e aprire il portale con i tre marchi.

| Telefono | Sistema | 10–15 cm | 25–30 cm | Luce scarsa | Inclinato ~30° | Esito |
|---|---|---|---|---|---|---|
| | iPhone / iOS | ☐ | ☐ | ☐ | ☐ | |
| | Android | ☐ | ☐ | ☐ | ☐ | |
| | (terzo, se disponibile) | ☐ | ☐ | ☐ | ☐ | |

- [ ] Lettura immediata (entro 2 secondi) in condizioni normali
- [ ] L'anteprima del telefono mostra il dominio `gpsr.in-shoes.it` con HTTPS, senza avvisi di sicurezza
- [ ] Dal portale, i pulsanti CULT, DOCKSTEPS e OXS aprono la pagina GPSR corretta
- [ ] Prova anche con rete mobile (Wi-Fi spento)

## C. Etichetta applicata
- [ ] Lettura riuscita con l'etichetta applicata nella posizione reale (scatola o calzatura)
- [ ] Lettura riuscita anche su superficie leggermente curva, se prevista
- [ ] Facoltativo: dopo strofinamento leggero / prova di resistenza prevista dal capitolato

## D. Coerenza dei file
- [ ] Il fornitore ha usato `GPSR_IN_SHOES_STAMPA.pdf` (SHA-256 `c553c764…0e6ad`) senza rigenerarlo
- [ ] Stesso QR per CULT, DOCKSTEPS e OXS (nessuna variante per marchio)

## Esito
- [ ] **Approvato per la produzione** — Nome: ______________ Firma: ______________ Data: ________
- [ ] Non approvato — Motivo e azione correttiva: ________________________________

Conservare la prova fisica approvata e una foto della lettura nel fascicolo del progetto.
