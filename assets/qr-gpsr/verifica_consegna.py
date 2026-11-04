"""Controllo della cartella CONSEGNA_UFFICIO_ETICHETTE e del suo ZIP (solo lettura)."""
import hashlib
import re
import unicodedata
import sys
import zipfile
from pathlib import Path

import numpy as np
import pymupdf
import zxingcpp
from PIL import Image

QUI = Path(__file__).resolve().parent
PROGETTO = QUI.parent.parent
DEST = PROGETTO / "CONSEGNA_UFFICIO_ETICHETTE"
ZIP = PROGETTO / "CONSEGNA_UFFICIO_ETICHETTE.zip"
URL = "https://gpsr.in-shoes.it/"
esiti = []


def check(nome, ok, det=""):
    esiti.append(ok)
    print(f"[{'OK' if ok else 'ERRORE'}] {nome}" + (f" — {det}" if det else ""))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leggi(gray):
    r = zxingcpp.read_barcodes(gray, formats=zxingcpp.BarcodeFormat.QRCode)
    return r[0].text if r else None


def render(doc_or_path, dpi, clip=None, pagina=0):
    doc = pymupdf.open(str(doc_or_path)) if not isinstance(doc_or_path, pymupdf.Document) else doc_or_path
    pix = doc[pagina].get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY, clip=clip)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width).copy()


attesi = {
    "1_FILE_PER_LA_STAMPA/QR_GPSR_25x25mm_STAMPA.pdf": "GPSR_IN_SHOES_STAMPA.pdf",
    "2_FILE_DI_SUPPORTO/QR_GPSR_25x25mm_GRAFICA.svg": "GPSR_IN_SHOES_MASTER.svg",
    "2_FILE_DI_SUPPORTO/QR_GPSR_ANTEPRIMA.png": "GPSR_IN_SHOES_PREVIEW.png",
}
presenti = sorted(p.relative_to(DEST).as_posix() for p in DEST.rglob("*") if p.is_file())
check("Cartella con i soli 5 file previsti", presenti == sorted(list(attesi) + ["00_LEGGIMI.txt", "0_ISTRUZIONI_QR_GPSR.pdf"]), str(presenti))

for rel, master in attesi.items():
    check(f"{rel} identico al master {master}", sha(DEST / rel) == sha(QUI / master))

for rel in ("1_FILE_PER_LA_STAMPA/QR_GPSR_25x25mm_STAMPA.pdf", "2_FILE_DI_SUPPORTO/QR_GPSR_25x25mm_GRAFICA.svg"):
    t = leggi(render(DEST / rel, 300))
    check(f"QR leggibile in {rel.split('/')[-1]}", t == URL, repr(t))
t = leggi(np.array(Image.open(DEST / "2_FILE_DI_SUPPORTO/QR_GPSR_ANTEPRIMA.png").convert("L")))
check("QR leggibile nell'anteprima PNG", t == URL, repr(t))
d = pymupdf.open(str(DEST / "1_FILE_PER_LA_STAMPA/QR_GPSR_25x25mm_STAMPA.pdf"))
check("File di stampa: 25,0 x 25,0 mm, vettoriale",
      abs(d[0].rect.width / 72 * 25.4 - 25) < 0.001 and abs(d[0].rect.height / 72 * 25.4 - 25) < 0.001 and not d[0].get_images())

# Istruzioni
ist = pymupdf.open(str(DEST / "0_ISTRUZIONI_QR_GPSR.pdf"))
check("Istruzioni: 3 pagine A4", len(ist) == 3 and all(round(p.rect.width) == 595 and round(p.rect.height) == 842 for p in ist))
check("Istruzioni: nessuna immagine raster (QR vettoriale)", all(not p.get_images() for p in ist))
testo = "\n".join(p.get_text() for p in ist)
# L'indirizzo deve comparire esatto (copiabile); le legature tipografiche fi/fl si normalizzano.
check("Istruzioni: indirizzo copiabile esatto, senza caratteri alterati", URL in testo)
testo = unicodedata.normalize("NFKC", testo).replace("\xa0", " ")
for frase in ("CULT, DOCKSTEPS e OXS", "lo stesso QR per tutti e tre i marchi", URL, "25 × 25 mm", "Non rigenerare il QR",
              "Non ritagliare il bordo bianco", "Non modificarlo", "FASE 1", "FASE 2", "approvazione scritta",
              "QR_GPSR_25x25mm_STAMPA.pdf", "IL FILE DA USARE PER LA STAMPA", "K100"):
    check(f"Istruzioni contengono: {frase}", frase.replace("\n", " ") in testo.replace("\n", " "))
tecnici = re.findall(r"(?i)\b(github|git|dns|hosting|server|script|python|sha-?256|repository|deploy|html|css)\b", testo)
check("Istruzioni senza termini tecnici di programmazione o infrastruttura", not tecnici, str(sorted(set(tecnici))))
# QR stampato nelle istruzioni: deve misurare 25 mm e leggersi
blocchi = [b for b in ist[0].get_drawings() if abs(b["rect"].width - 25 * 72 / 25.4) < 0.5 and abs(b["rect"].height - 25 * 72 / 25.4) < 0.5]
check("Pagina 1: QR inserito a 25 x 25 mm reali", bool(blocchi), f"{len(blocchi)} riquadri da 25 mm")
if blocchi:
    t = leggi(render(ist, 300, clip=blocchi[0]["rect"] + (-10, -10, 10, 10)))
    check("Pagina 1: QR in dimensione reale leggibile", t == URL, repr(t))

# LEGGIMI
leg = (DEST / "00_LEGGIMI.txt").read_text(encoding="utf-8")
check("00_LEGGIMI.txt indica file di stampa, URL e approvazione", "QR_GPSR_25x25mm_STAMPA.pdf" in leg and URL in leg and "approvazione" in leg)

# ZIP
with zipfile.ZipFile(ZIP) as z:
    check("ZIP integro", z.testzip() is None)
    nomi = sorted(n for n in z.namelist())
    check("ZIP contiene esattamente la cartella di consegna", nomi == sorted(f"CONSEGNA_UFFICIO_ETICHETTE/{p}" for p in presenti))
    check("ZIP: file identici a quelli della cartella",
          all(hashlib.sha256(z.read(f"CONSEGNA_UFFICIO_ETICHETTE/{p}")).hexdigest() == sha(DEST / p) for p in presenti))

print(f"\nESITO: {'OK' if all(esiti) else 'ERRORI'} ({sum(esiti)}/{len(esiti)})")
sys.exit(0 if all(esiti) else 1)
