"""Prepara la cartella CONSEGNA_UFFICIO_ETICHETTE e il relativo ZIP.

- copia i file del QR master (identici byte per byte) con nomi chiari
- genera ISTRUZIONI_QR_GPSR.pdf (italiano semplice, QR vettoriale a 25 x 25 mm reali)
- scrive 00_LEGGIMI.txt
- crea CONSEGNA_UFFICIO_ETICHETTE.zip con date fisse (riproducibile)

Uso:  python genera_consegna.py
"""
import shutil
import zipfile
from pathlib import Path

import pymupdf

QUI = Path(__file__).resolve().parent
PROGETTO = QUI.parent.parent
DEST = PROGETTO / "CONSEGNA_UFFICIO_ETICHETTE"
ZIP = PROGETTO / "CONSEGNA_UFFICIO_ETICHETTE.zip"

STAMPA = "1_FILE_PER_LA_STAMPA/QR_GPSR_25x25mm_STAMPA.pdf"
SVG = "2_FILE_DI_SUPPORTO/QR_GPSR_25x25mm_GRAFICA.svg"
PNG = "2_FILE_DI_SUPPORTO/QR_GPSR_ANTEPRIMA.png"
ISTR = "0_ISTRUZIONI_QR_GPSR.pdf"
LEGGIMI = "00_LEGGIMI.txt"
URL = "https://gpsr.in-shoes.it/"
MM = 72 / 25.4

CSS = """
* { font-family: sans-serif; }  /* font integrato: l'indirizzo copiato dal PDF resta esatto */
body { font-size: 10.5pt; line-height: 1.38; color: #1a1a1a; }
h1 { font-size: 19pt; margin: 0 0 4pt 0; }
h2 { font-size: 13pt; margin: 14pt 0 6pt 0; color: #0b3d91; }
p { margin: 0 0 6pt 0; }
.small { font-size: 8.5pt; color: #555555; }
.box { background-color: #eef3fb; border: 1pt solid #b9cbe8; padding: 8pt; margin: 6pt 0 8pt 0; }
.stop { background-color: #fdeeee; border: 1pt solid #e3a6a6; padding: 8pt; margin: 6pt 0; }
.ok { color: #1b7a2e; font-weight: bold; }
.no { color: #b3261e; font-weight: bold; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 6pt 0; }
td, th { border: 0.75pt solid #9aa5b5; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background-color: #e6eaf0; }
ul, ol { margin: 0 0 6pt 0; padding-left: 16pt; }
li { margin-bottom: 3pt; }
.fase { border: 1.2pt solid #0b3d91; padding: 8pt; margin: 6pt 0; }
.firma td { height: 22pt; }
"""

INTESTAZIONE = '<p class="small">IN SHOES SRL · Etichette calzature CULT · DOCKSTEPS · OXS · Versione 1 del 4 novembre 2026</p>'

PAGINA1_INTRO = f"""
{INTESTAZIONE}
<h1>QR code GPSR<br>Istruzioni per l'ufficio etichette</h1>
<div class="box">
<p><b>In breve</b></p>
<ul>
<li>Questo QR va stampato sulle etichette delle calzature <b>CULT, DOCKSTEPS e OXS</b>.
È <b>lo stesso QR per tutti e tre i marchi</b>: non esistono versioni diverse.</li>
<li>Chi lo inquadra con il telefono apre la pagina <b>{URL}</b>, sceglie il marchio
e trova le informazioni di sicurezza del prodotto.</li>
<li>Il QR è <b>definitivo e non scade</b>. Va usato sempre così com'è.</li>
</ul>
</div>
"""

PAGINA1_QR = """
<h2>Il QR in dimensione reale</h2>
<p>Qui a fianco il QR è riprodotto a <b>25 × 25 mm</b>, bordo bianco compreso
(stampando questo foglio al 100%, senza "adatta alla pagina").</p>
<p class="small">Il bordo bianco intorno ai quadratini fa parte del QR.</p>
"""

PAGINA1_B = f"""
<h2>Quale file usare</h2>
<table>
<tr><th>File</th><th>A cosa serve</th></tr>
<tr><td><b>1_FILE_PER_LA_STAMPA</b><br>QR_GPSR_25x25mm_STAMPA.pdf</td>
<td><span class="ok">✔ IL FILE DA USARE PER LA STAMPA.</span><br>Inseriscilo nel layout dell'etichetta a 25 × 25 mm.</td></tr>
<tr><td>2_FILE_DI_SUPPORTO<br>QR_GPSR_25x25mm_GRAFICA.svg</td>
<td>Solo se il programma di grafica non accetta il PDF. È lo stesso identico QR.</td></tr>
<tr><td>2_FILE_DI_SUPPORTO<br>QR_GPSR_ANTEPRIMA.png</td>
<td>Solo per riconoscere il QR (email, presentazioni).<br><span class="no">✘ Non usarlo per stampare le etichette.</span></td></tr>
</table>
"""

PAGINA2 = f"""
{INTESTAZIONE}
<h2>Regole da rispettare sempre</h2>
<div class="stop">
<ol>
<li><b>Non rigenerare il QR</b> con siti, app o altri programmi, anche se contiene lo stesso indirizzo. Usa solo i file forniti.</li>
<li><b>Non modificarlo</b>: niente loghi, scritte, colori, cornici o effetti sopra o dentro il QR.</li>
<li><b>Non ritagliare il bordo bianco</b>: fa parte del QR e serve al telefono per leggerlo.</li>
<li><b>Non rimpicciolirlo</b> sotto 25 × 25 mm e <b>non deformarlo</b>: deve restare un quadrato perfetto.</li>
<li><b>Non invertire i colori</b>: niente QR bianco su fondo nero o colorato.</li>
<li><b>Non avvicinare altri elementi grafici</b>: lo spazio di 25 × 25 mm è riservato al QR.</li>
</ol>
<p>Se un programma, un collega o la tipografia chiede di cambiare qualcosa del QR, <b>fermati e chiedi al responsabile del progetto GPSR</b>.</p>
</div>
<h2>Specifiche essenziali</h2>
<table>
<tr><td><b>Dimensione</b></td><td>25 × 25 mm, bordo bianco compreso</td></tr>
<tr><td><b>Bordo bianco (margine)</b></td><td>circa 2,7 mm per lato, già compreso nel file: non aggiungere e non togliere</td></tr>
<tr><td><b>Proporzioni</b></td><td>quadrato perfetto (larghezza = altezza)</td></tr>
<tr><td><b>Colore</b></td><td>nero pieno al 100% (solo nero, K100) su fondo bianco</td></tr>
<tr><td><b>Fondo</b></td><td>bianco o molto chiaro, opaco (non lucido, non trasparente)</td></tr>
<tr><td><b>Indirizzo contenuto</b></td><td>{URL} (non modificabile)</td></tr>
<tr><td><b>Marchi</b></td><td>CULT, DOCKSTEPS e OXS: stesso QR per tutti</td></tr>
</table>
<h2>Indicazioni per la stampa</h2>
<ul>
<li>Inserisci il PDF nel layout alla dimensione <b>100%</b> (25 × 25 mm). Non usare "adatta alla pagina" o ridimensionamenti automatici.</li>
<li>Dopo l'inserimento controlla nel programma che il riquadro misuri esattamente 25 × 25 mm.</li>
<li>Se l'etichetta non è bianca, sotto il QR serve un fondo bianco pieno di 25 × 25 mm.</li>
<li>Evita pellicole lucide o riflettenti sopra il QR: possono impedire la lettura.</li>
<li>Se il QR stampato appare con quadratini irregolari, sfocati o "impastati" (succede con alcune stampanti per etichette),
<b>non modificare il file</b>: segnalalo al responsabile, che valuterà con il fornitore della stampante.</li>
</ul>
"""

PAGINA3 = f"""
{INTESTAZIONE}
<h2>Prima della produzione: prova di stampa obbligatoria</h2>
<div class="fase">
<p><b>FASE 1 — Prova di stampa (adesso)</b></p>
<p>Stampa alcune etichette di prova con <b>lo stesso materiale, la stessa stampante e lo stesso formato</b> della produzione.
Esegui la checklist qui sotto e consegna le prove al responsabile del progetto GPSR.</p>
</div>
<div class="fase">
<p><b>FASE 2 — Produzione definitiva (solo dopo l'approvazione)</b></p>
<p>La produzione delle etichette può partire <b>solo dopo l'approvazione scritta del responsabile del progetto GPSR</b>.
<span class="no">Senza approvazione, non avviare la produzione.</span></p>
</div>
<h2>Checklist della prova di stampa</h2>
<table>
<tr><th style="width:24pt">✔</th><th>Controllo</th></tr>
<tr><td>☐</td><td>Il QR misura <b>25 × 25 mm</b> con un righello, bordo bianco compreso. Misurato: ______ mm</td></tr>
<tr><td>☐</td><td>È quadrato e non deformato</td></tr>
<tr><td>☐</td><td>Nero pieno e netto su fondo bianco, senza sbavature, macchie o quadratini mancanti</td></tr>
<tr><td>☐</td><td>Il bordo bianco è libero su tutti e quattro i lati</td></tr>
<tr><td>☐</td><td>Letto con un <b>iPhone</b> (fotocamera normale): si apre <b>gpsr.in-shoes.it</b></td></tr>
<tr><td>☐</td><td>Letto con un telefono <b>Android</b> (fotocamera normale): si apre <b>gpsr.in-shoes.it</b></td></tr>
<tr><td>☐</td><td>La pagina mostra i tre marchi CULT, DOCKSTEPS e OXS e ogni pulsante apre la pagina giusta</td></tr>
<tr><td>☐</td><td>La lettura riesce anche da 25–30 cm e con poca luce</td></tr>
<tr><td>☐</td><td>La lettura riesce con l'etichetta già applicata sulla scatola o sulla calzatura</td></tr>
</table>
<div class="fase">
<p>Prova eseguita da: ________________________________ &#160;&#160; Data: ______________</p>
<p>Esito: ☐ positivo &#160;&#160; ☐ negativo &#160;&#160; Note: ____________________________________________</p>
<p><b>Approvazione della produzione</b> (responsabile del progetto GPSR):</p>
<p>Firma: ________________________________ &#160;&#160; Data: ______________</p>
</div>
<p class="small">Responsabile del progetto GPSR: ________________________________ (nome e contatto).
Conserva la prova approvata insieme a queste istruzioni.</p>
"""

LEGGIMI_TXT = f"""QR CODE GPSR - CONSEGNA PER L'UFFICIO ETICHETTE
IN SHOES SRL - versione 1 del 4 novembre 2026

Il QR e' UNICO per le calzature CULT, DOCKSTEPS e OXS.
Inquadrandolo si apre: {URL}

COSA C'E' IN QUESTA CARTELLA
  0_ISTRUZIONI_QR_GPSR.pdf   -> LEGGERE PRIMA: istruzioni, regole e checklist
  1_FILE_PER_LA_STAMPA\\QR_GPSR_25x25mm_STAMPA.pdf   -> IL FILE DA USARE PER LA STAMPA
  2_FILE_DI_SUPPORTO\\QR_GPSR_25x25mm_GRAFICA.svg    -> solo per programmi di grafica che non accettano il PDF
  2_FILE_DI_SUPPORTO\\QR_GPSR_ANTEPRIMA.png          -> solo anteprima, NON per la stampa

REGOLE
  - Dimensione 25 x 25 mm, bordo bianco compreso. Nero pieno su fondo bianco.
  - Non rigenerare, modificare, ritagliare, ridurre o deformare il QR.
  - Prima della produzione: prova di stampa e checklist (vedi istruzioni).
  - La produzione definitiva parte solo dopo l'approvazione scritta
    del responsabile del progetto GPSR.
"""


def pagina(doc, html, top=50, height=742):
    p = doc.new_page(width=595, height=842)
    p.insert_htmlbox(pymupdf.Rect(50, top, 545, top + height), html, css=CSS)
    return p


def blocco(p, x0, y0, x1, html, max_h=700):
    """Inserisce html dal punto y0 e restituisce la y dove finisce."""
    spare, _ = p.insert_htmlbox(pymupdf.Rect(x0, y0, x1, y0 + max_h), html, css=CSS)
    return y0 + max_h - spare


def crea_istruzioni(path):
    doc = pymupdf.open()
    qr = pymupdf.open(QUI / "GPSR_IN_SHOES_STAMPA.pdf")
    p1 = doc.new_page(width=595, height=842)
    y = blocco(p1, 50, 50, 545, PAGINA1_INTRO)
    # Colonna di testo stretta a sinistra, QR vettoriale a dimensione reale (25 x 25 mm) a destra
    lato = 25 * MM
    x = 545 - lato - 20
    y_testo = blocco(p1, 50, y, x - 25, PAGINA1_QR)
    r = pymupdf.Rect(x, y + 14, x + lato, y + 14 + lato)
    p1.draw_rect(r + (-0.6, -0.6, 0.6, 0.6), color=(0.6, 0.6, 0.6), width=0.4)  # contorno di riferimento, esterno al QR
    p1.show_pdf_page(r, qr, 0)
    y_qr = blocco(p1, x - 30, r.y1 + 3, r.x1 + 30, '<p class="small" style="text-align:center">25 × 25 mm reali</p>', 30)
    blocco(p1, 50, max(y_testo, y_qr) + 6, 545, PAGINA1_B)
    pagina(doc, PAGINA2)
    pagina(doc, PAGINA3)
    for i, p in enumerate(doc, start=1):
        p.insert_htmlbox(pymupdf.Rect(50, 805, 545, 825),
                         f'<p class="small" style="text-align:right">QR GPSR · Istruzioni ufficio etichette · pagina {i} di {len(doc)}</p>', css=CSS)
    doc.set_metadata({"title": "QR code GPSR - Istruzioni per l'ufficio etichette", "author": "IN SHOES SRL",
                      "subject": f"QR unico CULT, DOCKSTEPS, OXS - {URL}", "creator": "genera_consegna.py",
                      "producer": "", "creationDate": "", "modDate": ""})
    doc.save(path, garbage=4, deflate=True, no_new_id=True)


def main():
    # Sovrascrive i file al loro posto (OneDrive può bloccare la cancellazione delle cartelle) e
    # rimuove eventuali file estranei, così la cartella contiene solo i file previsti.
    previsti = {STAMPA, SVG, PNG, ISTR, LEGGIMI}
    if DEST.exists():
        for f in DEST.rglob("*"):
            if f.is_file() and f.relative_to(DEST).as_posix() not in previsti:
                f.unlink()
    for rel, src in ((STAMPA, "GPSR_IN_SHOES_STAMPA.pdf"), (SVG, "GPSR_IN_SHOES_MASTER.svg"), (PNG, "GPSR_IN_SHOES_PREVIEW.png")):
        (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(QUI / src, DEST / rel)
    crea_istruzioni(DEST / ISTR)
    (DEST / LEGGIMI).write_bytes(LEGGIMI_TXT.replace("\n", "\r\n").encode("utf-8"))
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in DEST.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"CONSEGNA_UFFICIO_ETICHETTE/{f.relative_to(DEST).as_posix()}", (2026, 11, 4, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, f.read_bytes())
    print("Cartella:", DEST)
    print("ZIP:", ZIP)


if __name__ == "__main__":
    main()
