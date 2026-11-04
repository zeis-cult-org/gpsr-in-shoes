# Pubblicazione di `gpsr.in-shoes.it` e HTTPS

> Nulla di quanto segue è stato eseguito. Ogni passo che crea account, pubblica o tocca il DNS richiede approvazione esplicita.
> Il progetto riguarda **solo** il sottodominio `gpsr.in-shoes.it`. Il sito principale `in-shoes.it` / `www.in-shoes.it` e la posta non si toccano.

## 1. Situazione (4/11/2026)

| Voce | Stato |
|---|---|
| Dominio `in-shoes.it` | Acquistato il 3/11/2026 per IN SHOES SRL. |
| DNS | Nameserver `ns81/ns82.domaincontrol.com` = **GoDaddy**. Accesso alla gestione DNS da definire in fase di pubblicazione. |
| `in-shoes.it`, `www.in-shoes.it` | Puntano a indirizzi GoDaddy (`3.33.130.190`, `15.197.148.33`). **Fuori dal progetto.** |
| `gpsr.in-shoes.it` | Nessun record. Da creare. |
| Hosting | **Approvato: GitHub Pages su nuova organizzazione GitHub aziendale.** Non ancora creata. |
| Repository | Pronto in locale, con workflow `.github/workflows/pages.yml` che pubblica solo `public/`. |

## 2. Cosa serve prima di iniziare
- Un'email aziendale per creare l'organizzazione GitHub (meglio una casella condivisa, non personale).
- Nome dell'organizzazione `<ORG>` (es. `in-shoes-srl`; da verificare che sia libero).
- Almeno due proprietari dell'organizzazione con autenticazione a due fattori.
- Una persona con accesso alla gestione DNS di `in-shoes.it` su GoDaddy.

## 3. Passi di pubblicazione

### A. GitHub (nessun effetto sul dominio)
1. Creare l'organizzazione `<ORG>` (piano Free) e invitare il secondo proprietario.
2. Creare il repository **pubblico** `<ORG>/gpsr-in-shoes`, vuoto (senza README). GitHub Pages gratuito richiede un repository pubblico. Il repository conterrà anche `docs/`, che non contiene dati riservati.
3. Collegare il repository locale e fare il push:
   ```bash
   git remote add origin https://github.com/<ORG>/gpsr-in-shoes.git
   ```
   ```bash
   git push -u origin main
   ```
4. Repository → *Settings → Pages → Build and deployment → Source* = **GitHub Actions**.
5. Il workflow parte: esegue i controlli minimi (file, H1, tre link) e pubblica `public/`. Il sito è visibile su `https://<ORG>.github.io/gpsr-in-shoes/`. Provarlo prima di proseguire.

### B. Protezione del dominio (consigliata, prima del CNAME)
6. Organizzazione → *Settings → Pages → Verified domains → Add a domain* → `gpsr.in-shoes.it`. GitHub mostra un record TXT. Verificare il sottodominio, non `in-shoes.it`, così il resto del dominio resta fuori dal progetto. Questo impedisce ad altri account GitHub di usare il sottodominio.

### C. DNS su GoDaddy (solo il sottodominio `gpsr`)
7. Aggiungere esclusivamente questi due record. Non modificare né cancellare nessun record esistente:

   | Tipo  | Nome (host) | Valore | TTL |
   |-------|-------------|--------|-----|
   | TXT   | `_github-pages-challenge-<ORG>.gpsr` | valore fornito da GitHub al passo 6 | 1 ora |
   | CNAME | `gpsr` | `<ORG>.github.io` | 1 ora |

   Il nome esatto del record TXT va copiato da GitHub. In GoDaddy il campo "Nome" si scrive senza `.in-shoes.it` finale. Prima di salvare, fare uno screenshot della zona DNS: serve per il rollback.
8. Tornare al passo 6 e premere **Verify**.

### D. Dominio personalizzato e HTTPS
9. Repository → *Settings → Pages → Custom domain* = `gpsr.in-shoes.it` → Save. Attendere il controllo DNS.
10. Attivare **Enforce HTTPS**. Il certificato Let's Encrypt può richiedere fino a 24 ore.
11. Eseguire la [CHECKLIST_TEST.md](CHECKLIST_TEST.md) completa sul dominio reale.
12. Solo dopo la checklist firmata: generare i QR con `https://gpsr.in-shoes.it/` per tutti e tre i marchi.

## 4. Verifiche dopo la pubblicazione

```powershell
nslookup gpsr.in-shoes.it
curl.exe -I https://gpsr.in-shoes.it/
curl.exe -I http://gpsr.in-shoes.it/
powershell -ExecutionPolicy Bypass -File scripts\verifica.ps1 -SitoUrl https://gpsr.in-shoes.it/
```

Attesi: CNAME verso `<ORG>.github.io`; HTTPS `200`; HTTP reindirizza (`301`) a HTTPS; certificato valido (lucchetto, anche da smartphone); `in-shoes.it` e la posta funzionano come prima.

## 5. Aggiornamenti futuri
Modifica in locale → `scripts/verifica.ps1` → commit → push su `main` (con approvazione) → il workflow ripubblica in pochi minuti. Se qualcosa va storto: [ROLLBACK.md](ROLLBACK.md).

Prima del primo deploy controllare che le versioni delle azioni nel workflow (`checkout`, `configure-pages`, `upload-pages-artifact`, `deploy-pages`) siano ancora le più recenti consigliate da GitHub.

## 6. Anteprima locale

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory public
```

Apri http://localhost:8000/ . Per provarla da smartphone sulla stessa Wi-Fi togli `--bind 127.0.0.1` e apri `http://<IP-del-PC>:8000/` (potrebbe servire consentire Python nel firewall). L'anteprima locale non ha HTTPS: HTTPS si verifica solo sul dominio pubblicato.
