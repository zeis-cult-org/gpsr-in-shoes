# Architettura

## Obiettivo
Un indirizzo stabile, di proprietà aziendale (`https://gpsr.in-shoes.it/`), da stampare nei QR di tutti e tre i marchi, che smista verso le pagine GPSR ufficiali. Se in futuro una pagina di marchio cambia indirizzo, si aggiorna lo snodo e i QR stampati restano validi.

## Componenti

| Componente | Indirizzo | Chi lo controlla | Ruolo |
|---|---|---|---|
| Vecchi QR | `https://lost-95.github.io/cult-milano-gpsr/` | account GitHub personale `lost-95` | Già stampati su scarpe CULT, DOCKSTEPS, OXS. Non modificabili. |
| Sito storico | stesso indirizzo + 10 PDF (`ballerina.pdf`, `mocassino.pdf`, `mule.pdf`, `sandalo.pdf`, `scarpa_con_tacco.pdf`, `slides.pdf`, `sneaker.pdf`, `stivale.pdf`, `stivaletto.pdf`, `stringata.pdf`) | `lost-95` | Resta online invariato fino alla Fase 3. |
| Snodo | `https://gpsr.in-shoes.it/` | IN SHOES SRL | Pagina statica con 3 pulsanti. Destinazione dei nuovi QR. |
| Pagine marchi | `cultofficial.com`, `docksteps.com`, `oxs-shoes.it` → `/pages/gpsr` | i rispettivi marchi | Contenuto GPSR ufficiale (fabbricante, contatti, avvertenze). |

## Ambito
Solo il sottodominio `gpsr.in-shoes.it`. Il sito principale `in-shoes.it` / `www.in-shoes.it` e la posta del dominio sono fuori dal progetto.

## Scelte tecniche
- **Hosting**: GitHub Pages sull'account GitHub esistente usato per CULT Milano, repository `gpsr-in-shoes` separato dal repository storico (decisione del 4/11/2026: nessuna nuova organizzazione o account). Pubblicazione tramite `.github/workflows/pages.yml`.
- **Statico puro**: un solo file `public/index.html` con CSS incorporato, versione definitiva approvata. Nessun framework, build, backend, database, cookie, tracciamento, CDN o font esterni.
- **Separazione pubblicato / interno**: online va solo `public/`. Documentazione e script restano fuori, così non vengono pubblicati per errore.
- **HTTPS obbligatorio** tramite certificato gestito dall'hosting (vedi [PUBBLICAZIONE.md](PUBBLICAZIONE.md)).
- **Link esterni** aperti con normali `<a href>`: se una pagina di marchio non risponde, il problema è circoscritto a quel marchio; lo snodo resta su. Mitigazione: controllo periodico con `scripts/verifica.ps1` e procedura in [ROLLBACK.md](ROLLBACK.md).

## Vincoli di contenuto
- Lo snodo non si presenta come fabbricante e non attribuisce a IN SHOES SRL la responsabilità GPSR dei marchi.
- Non sostituisce l'etichetta fisica obbligatoria e non è prova di conformità.

## Estensione futura: Digital Product Passport (NON implementato)
Oggi non esiste alcun DPP. Per non bloccare il futuro:
- la **radice** `https://gpsr.in-shoes.it/` resta per sempre lo snodo (i QR stampati la usano);
- eventuali percorsi futuri vanno aggiunti **sotto** la radice senza cambiarla, per esempio `/dpp/…` o uno schema compatibile con GS1 Digital Link (`/01/<GTIN>`), da decidere quando la normativa delegata sul DPP calzature sarà definita;
- un DPP richiederà probabilmente dati per prodotto e quindi un'architettura diversa (non solo statica): andrà progettato a parte, con una nuova approvazione.
