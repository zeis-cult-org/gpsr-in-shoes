# Checklist di collaudo — da completare PRIMA di stampare i nuovi QR

Data: ____________  Collaudatore: ____________  Commit pubblicato: ____________

## A. File (in locale)
- [ ] `scripts/verifica.ps1` termina con esito OK.
- [ ] `public/index.html` è identico alla versione approvata (MD5 `31fd181b644cfd32f92359a367611751`, verificabile con `certutil -hashfile public\index.html MD5`). Se la pagina viene riapprovata in futuro, aggiornare qui l'MD5.
- [ ] H1 esatto: `GPSR - Sicurezza dei prodotti.<br>Informazioni sempre accessibili.`
- [ ] Nessun riferimento a IN SHOES SRL come fabbricante o responsabile GPSR dei marchi.
- [ ] Nessuno script, font, CSS, analytics, pixel o cookie esterno.

## B. Collegamenti
- [ ] CULT apre esattamente `https://www.cultofficial.com/pages/gpsr`
- [ ] DOCKSTEPS apre esattamente `https://www.docksteps.com/pages/gpsr`
- [ ] OXS apre esattamente `https://www.oxs-shoes.it/pages/gpsr`
- [ ] Ognuna delle tre pagine mostra contenuto GPSR corretto e aggiornato (verifica a cura dell'azienda).

## C. Dominio e HTTPS (sul sito pubblicato)
- [ ] `https://gpsr.in-shoes.it/` risponde 200 con certificato valido (lucchetto, nessun avviso).
- [ ] `http://gpsr.in-shoes.it/` reindirizza a HTTPS.
- [ ] Funziona anche con rete mobile 4G/5G (non solo Wi-Fi aziendale).
- [ ] I record DNS esistenti di `in-shoes.it` (sito principale, posta) funzionano come prima.

## D. Smartphone
- [ ] iPhone (Safari) e Android (Chrome): layout corretto, testo leggibile, nessuno scorrimento orizzontale.
- [ ] Pulsanti facili da toccare; ognuno apre la pagina corretta.
- [ ] Rotazione verticale/orizzontale ok.
- [ ] Modalità scura del telefono: testo ancora leggibile.

## E. QR code
- [ ] Il QR codifica esattamente `https://gpsr.in-shoes.it/` (con `https://`, senza parametri).
- [ ] Lo stesso identico URL è usato sulle etichette di CULT, DOCKSTEPS e OXS (nessun URL diverso per marchio).
- [ ] Prova di stampa al formato reale dell'etichetta, letta con almeno 2 telefoni diversi (fotocamera nativa), a distanza normale e con luce scarsa.
- [ ] Anteprima URL mostrata dal telefono = `gpsr.in-shoes.it`.

## F. Comportamento in caso di guasto
- [ ] Simulazione: se una pagina di marchio non risponde, lo snodo resta raggiungibile e gli altri due pulsanti funzionano (il guasto è limitato a quel marchio).
- [ ] È chiaro chi avvisare e come intervenire: vedi [ROLLBACK.md](ROLLBACK.md).
- [ ] Il sito storico `https://lost-95.github.io/cult-milano-gpsr/` e i suoi PDF rispondono ancora 200 (non deve essere stato toccato).

## Esito
- [ ] **Approvato per la stampa dei nuovi QR** — Firma: ____________
