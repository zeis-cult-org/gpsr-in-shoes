# Pubblicazione di `gpsr.in-shoes.it` e HTTPS

> Nulla di quanto segue è stato eseguito. Ogni passo richiede approvazione esplicita.

## 1. Situazione rilevata (4/11/2026, via DNS pubblico)

| Voce | Risultato | Stato |
|---|---|---|
| Nameserver di `in-shoes.it` | `ns81.domaincontrol.com`, `ns82.domaincontrol.com` | **DNS gestito da GoDaddy** (domaincontrol.com / jomax.net sono server GoDaddy) |
| `in-shoes.it` e `www.in-shoes.it` | A → `3.33.130.190`, `15.197.148.33` | Indirizzi usati da GoDaddy (parcheggio/inoltro/Website Builder). **Da confermare** chi gestisce il sito principale. |
| `gpsr.in-shoes.it` | nessun record | Libero, da creare |
| Hosting dello snodo | — | **Non ancora scelto** |

Da confermare: chi ha l'accesso all'account GoDaddy intestato a IN SHOES SRL, e che il dominio non sia gestito anche da un altro fornitore (es. Shopify o un'agenzia).

## 2. Hosting consigliato: GitHub Pages su un'organizzazione IN SHOES

Motivi: gratuito, statico, HTTPS automatico (Let's Encrypt), stessa tecnologia del sito storico, nessun server da mantenere.

Condizione essenziale: **non** usare l'account personale `lost-95`. Creare un'organizzazione GitHub di proprietà aziendale (es. `in-shoes-srl`, nome da decidere) con almeno due proprietari che usano email aziendali.

Alternative equivalenti se preferite: Cloudflare Pages o Netlify (piano gratuito, stessi principi: si pubblica la cartella `public/`, record CNAME sul sottodominio).

## 3. Passi (GitHub Pages) — da eseguire solo dopo approvazione

1. Creare l'organizzazione aziendale `<ORG>` e il repository `gpsr-in-shoes`.
2. Collegare questo repository locale e fare il push (**richiede approvazione**).
3. Pubblicare la cartella `public/` con il workflow ufficiale GitHub Actions "Static HTML" (`actions/upload-pages-artifact` con `path: public`, poi `actions/deploy-pages`). Il workflow verrà aggiunto al repository solo a hosting confermato.
4. Verificare il dominio sull'organizzazione (protegge da takeover del sottodominio): *Settings dell'organizzazione → Pages → Add a domain → `in-shoes.it`*. GitHub fornisce un record TXT da inserire in GoDaddy.
5. In GoDaddy, DNS di `in-shoes.it`, aggiungere:

   | Tipo  | Nome (host) | Valore | TTL |
   |-------|-------------|--------|-----|
   | TXT   | `_github-pages-challenge-<ORG>` | valore fornito da GitHub al passo 4 | 1 ora |
   | CNAME | `gpsr` | `<ORG>.github.io` | 1 ora |

   I valori `<ORG>` e il TXT sono noti solo dopo il passo 1 e 4: **non inserirli prima**. Non toccare gli altri record esistenti (A, MX, ecc.).
6. Nel repository: *Settings → Pages → Custom domain* = `gpsr.in-shoes.it`, attendere il controllo DNS, poi attivare **Enforce HTTPS** (il certificato può richiedere fino a 24 ore).
7. Eseguire [CHECKLIST_TEST.md](CHECKLIST_TEST.md) sul dominio reale.

## 4. Verifiche dopo la pubblicazione

```powershell
nslookup gpsr.in-shoes.it
curl.exe -I https://gpsr.in-shoes.it/
curl.exe -I http://gpsr.in-shoes.it/
```

Attesi: CNAME verso `<ORG>.github.io`; HTTPS risponde `200`; HTTP reindirizza (`301`) a HTTPS; certificato valido per `gpsr.in-shoes.it` (lucchetto nel browser, anche da smartphone).

## 5. Anteprima locale

```powershell
python -m http.server 8000 --directory public
```

Apri http://localhost:8000/ ; da smartphone sulla stessa Wi-Fi `http://<IP-del-PC>:8000/`. L'anteprima locale non ha HTTPS: HTTPS si verifica solo sul dominio pubblicato.
