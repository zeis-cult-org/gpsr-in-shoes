"""Prepara la cartella CONSEGNA_UFFICIO_ETICHETTE e il relativo ZIP.

- copia i file del QR master (identici byte per byte) con nomi chiari
- genera 0_ISTRUZIONI_QR_GPSR.pdf (2 pagine, italiano semplice, QR vettoriale a 25 x 25 mm reali)
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
.stop { background-color: #fdeeee; border: 1pt solid #e3a6a6; padding: 8pt; margin: 8pt 0; }
.ok { color: #1b7a2e; font-weight: bold; }
.no { color: #b3261e; font-weight: bold; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 6pt 0; }
td, th { border: 0.75pt solid #9aa5b5; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background-color: #e6eaf0; }
ul { margin: 0 0 6pt 0; padding-left: 16pt; }
li { margin-bottom: 3pt; }
.fase { border: 1.2pt solid #0b3d91; padding: 8pt; margin: 6pt 0; }
"""

INTESTAZIONE = '<p class="small">IN SHOES SRL · Etichette calzature CULT · DOCKSTEPS · OXS · Versione 1 del 4 novembre 2026</p>'

PAGINA1_INTRO = f"""
{INTESTAZIONE}
<h1>QR code GPSR<br>Istruzioni per l'ufficio etichette</h1>
<div class="box">
<ul>
<li>È <b>lo stesso QR per CULT, DOCKSTEPS e OXS</b>: non esistono versioni diverse.</li>
<li>Inquadrandolo con il telefono si apre <b>{URL}</b>, dove si sceglie il marchio.</li>
<li>Il QR è <b>definitivo e non scade</b>: va usato sempre così com'è.</li>
</ul>
</div>
"""

PAGINA1_QR = """
<h2>File da usare</h2>
<p><span class="ok">✔ Per la stampa:</span> <b>1_FILE_PER_LA_STAMPA / QR_GPSR_25x25mm_STAMPA.pdf</b></p>
<p>Nella cartella 2_FILE_DI_SUPPORTO: il file <b>.svg</b> solo se il programma di grafica non accetta il PDF;
il file <b>.png</b> solo come anteprima <span class="no">(non per stampare)</span>.</p>
<p class="small">A fianco il QR in dimensione reale: 25 × 25 mm stampando questo foglio al 100%.</p>
"""

PAGINA1_REGOLE = """
<h2>Come va stampato</h2>
<table>
<tr><td><b>Dimensione</b></td><td>25 × 25 mm al 100% (no "adatta alla pagina"), bordo bianco di circa 2,7 mm per lato già compreso:
non ridurlo e non ritagliarlo</td></tr>
<tr><td><b>Forma</b></td><td>quadrato perfetto, non deformato</td></tr>
<tr><td><b>Colore</b></td><td>nero pieno al 100% (K100) su fondo bianco opaco; mai colori invertiti</td></tr>
<tr><td><b>Spazio</b></td><td>nessun altro elemento grafico dentro i 25 × 25 mm; niente pellicole lucide sopra il QR</td></tr>
</table>
<div class="stop">
<p><b>Non rigenerare il QR</b> con siti, app o altri programmi. <b>Non modificarlo</b>: niente loghi, scritte, colori o effetti.</p>
<p>Se qualcuno chiede di cambiarlo, o il QR stampato esce irregolare o sfocato, non toccare il file:
<b>avvisa il responsabile del progetto GPSR</b>.</p>
</div>
"""

PAGINA2 = f"""
{INTESTAZIONE}
<h2>Prova di stampa, poi produzione</h2>
<div class="fase">
<p><b>FASE 1 — Prova di stampa:</b> stampa alcune etichette di prova con lo stesso materiale, la stessa stampante
e lo stesso formato della produzione, compila la checklist e consegna le prove al responsabile.</p>
</div>
<div class="fase">
<p><b>FASE 2 — Produzione definitiva:</b> solo dopo l'<b>approvazione scritta</b> del responsabile del progetto GPSR.
<span class="no">Senza approvazione, non avviare la produzione.</span></p>
</div>
<h2>Checklist della prova</h2>
<table>
<tr><td style="width:24pt">☐</td><td>Misura 25 × 25 mm con il righello, è quadrato e il bordo bianco è libero. Misurato: ______ mm</td></tr>
<tr><td>☐</td><td>Nero netto, senza sbavature, macchie o quadratini mancanti</td></tr>
<tr><td>☐</td><td>Con un <b>iPhone</b> (fotocamera normale) si apre <b>gpsr.in-shoes.it</b></td></tr>
<tr><td>☐</td><td>Con un telefono <b>Android</b> (fotocamera normale) si apre <b>gpsr.in-shoes.it</b></td></tr>
<tr><td>☐</td><td>I pulsanti CULT, DOCKSTEPS e OXS aprono la pagina giusta</td></tr>
<tr><td>☐</td><td>La lettura riesce da 25–30 cm, con poca luce e con l'etichetta applicata sulla scatola o calzatura</td></tr>
</table>
<div class="fase">
<p>Prova eseguita da: ________________________________ &#160;&#160; Data: ______________</p>
<p>Esito: ☐ positivo &#160;&#160; ☐ negativo &#160;&#160; Note: ____________________________________________</p>
<p><b>Approvazione della produzione</b> (responsabile del progetto GPSR)</p>
<p>Nome: ______________________ &#160; Firma: ______________________ &#160; Data: ____________</p>
</div>
"""


def blocco(p, x0, y0, x1, html, max_h=700):
    """Inserisce html dal punto y0 e restituisce la y dove finisce."""
    spare, _ = p.insert_htmlbox(pymupdf.Rect(x0, y0, x1, y0 + max_h), html, css=CSS)
    return y0 + max_h - spare


def crea_istruzioni(path):
    doc = pymupdf.open()
    qr = pymupdf.open(QUI / "GPSR_IN_SHOES_STAMPA.pdf")
    p1 = doc.new_page(width=595, height=842)
    y = blocco(p1, 50, 50, 545, PAGINA1_INTRO)
    # Colonna di testo a sinistra, QR vettoriale a dimensione reale (25 x 25 mm) a destra
    lato = 25 * MM
    x = 545 - lato - 20
    y_testo = blocco(p1, 50, y, x - 25, PAGINA1_QR)
    r = pymupdf.Rect(x, y + 14, x + lato, y + 14 + lato)
    p1.draw_rect(r + (-0.6, -0.6, 0.6, 0.6), color=(0.6, 0.6, 0.6), width=0.4)  # contorno di riferimento, esterno al QR
    p1.show_pdf_page(r, qr, 0)
    y_qr = blocco(p1, x - 30, r.y1 + 3, r.x1 + 30, '<p class="small" style="text-align:center">25 × 25 mm reali</p>', 30)
    blocco(p1, 50, max(y_testo, y_qr) + 4, 545, PAGINA1_REGOLE)
    p2 = doc.new_page(width=595, height=842)
    blocco(p2, 50, 50, 545, PAGINA2)
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
    previsti = {STAMPA, SVG, PNG, ISTR}
    if DEST.exists():
        for f in DEST.rglob("*"):
            if f.is_file() and f.relative_to(DEST).as_posix() not in previsti:
                f.unlink()
    for rel, src in ((STAMPA, "GPSR_IN_SHOES_STAMPA.pdf"), (SVG, "GPSR_IN_SHOES_MASTER.svg"), (PNG, "GPSR_IN_SHOES_PREVIEW.png")):
        (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(QUI / src, DEST / rel)
    crea_istruzioni(DEST / ISTR)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in DEST.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"CONSEGNA_UFFICIO_ETICHETTE/{f.relative_to(DEST).as_posix()}", (2026, 11, 4, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, f.read_bytes())
    print("Cartella:", DEST)
    print("ZIP:", ZIP)


if __name__ == "__main__":
    main()
