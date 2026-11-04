"""Genera il QR code ufficiale GPSR di IN SHOES SRL.

Contenuto codificato (esatto): https://gpsr.in-shoes.it/
Uscite, nella stessa cartella dello script:
  GPSR_IN_SHOES_MASTER.svg   vettoriale, 25 x 25 mm
  GPSR_IN_SHOES_STAMPA.pdf   vettoriale, pagina 25 x 25 mm, nero K100 (CMYK)
  GPSR_IN_SHOES_PREVIEW.png  anteprima 1184 x 1184 px (32 px per modulo, 25 mm a 1203 dpi)
  SHA256SUMS.txt             impronte dei tre file

Nessuna data o dato variabile nei file: a parità di versioni delle librerie
(requirements.txt) l'uscita è identica byte per byte.

Uso:  python genera_qr.py
"""
import hashlib
from pathlib import Path

import segno
from PIL import Image

URL = "https://gpsr.in-shoes.it/"
ERRORE = "q"            # correzione errori livello Q (~25%)
MARGINE = 4             # quiet zone in moduli per lato
LATO_MM = 25.0          # lato totale, margine incluso
PX_MODULO = 32          # risoluzione dell'anteprima PNG

QUI = Path(__file__).resolve().parent
SVG = QUI / "GPSR_IN_SHOES_MASTER.svg"
PDF = QUI / "GPSR_IN_SHOES_STAMPA.pdf"
PNG = QUI / "GPSR_IN_SHOES_PREVIEW.png"
SUMS = QUI / "SHA256SUMS.txt"


def crea_qr():
    qr = segno.make(URL, error=ERRORE, mode="byte", boost_error=False, micro=False)
    assert qr.designator == "3-Q", qr.designator
    return qr


def matrice_con_margine(qr):
    """Lista di righe di 0/1 (1 = modulo nero), quiet zone inclusa."""
    return [[1 if v else 0 for v in riga] for riga in qr.matrix_iter(scale=1, border=MARGINE)]


def tratti(m):
    """Tratti orizzontali neri: (riga, colonna_iniziale, lunghezza)."""
    out = []
    for y, riga in enumerate(m):
        x = 0
        while x < len(riga):
            if riga[x]:
                x0 = x
                while x < len(riga) and riga[x]:
                    x += 1
                out.append((y, x0, x - x0))
            else:
                x += 1
    return out


def scrivi_svg(m):
    n = len(m)
    d = "".join(f"M{x} {y}h{w}v1h-{w}z" for y, x, w in tratti(m))
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
        f'width="{LATO_MM:g}mm" height="{LATO_MM:g}mm" viewBox="0 0 {n} {n}" '
        'shape-rendering="crispEdges">\n'
        f"<title>QR GPSR IN SHOES SRL - {URL}</title>\n"
        f'<rect width="{n}" height="{n}" fill="#FFFFFF"/>\n'
        f'<path fill="#000000" d="{d}"/>\n'
        "</svg>\n"
    )
    SVG.write_bytes(svg.encode("utf-8"))


def scrivi_pdf(m):
    n = len(m)
    lato_pt = LATO_MM / 25.4 * 72          # 70.866142 pt
    lp = f"{lato_pt:.6f}"
    s = f"{lato_pt / n:.8f}"
    righe = [
        "q",
        f"0 0 0 0 k 0 0 {lp} {lp} re f",     # fondo bianco (nessun inchiostro)
        f"{s} 0 0 -{s} 0 {lp} cm",          # coordinate in moduli, origine in alto a sinistra
        "0 0 0 1 k",                        # nero solo K100
    ]
    righe += [f"{x} {y} {w} 1 re" for y, x, w in tratti(m)]
    righe += ["f", "Q"]
    contenuto = ("\n".join(righe) + "\n").encode("ascii")

    oggetti = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {lp} {lp}] /TrimBox [0 0 {lp} {lp}] "
         f"/Resources << >> /Contents 4 0 R >>").encode("ascii"),
        f"<< /Length {len(contenuto)} >>\nstream\n".encode("ascii") + contenuto + b"endstream",
        (f"<< /Title (QR GPSR IN SHOES SRL - {URL}) /Subject (QR 3-Q, 25 x 25 mm, quiet zone 4 moduli) "
         f"/Producer (genera_qr.py, segno {segno.__version__}) >>").encode("ascii"),
    ]
    dati = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offset = []
    for i, corpo in enumerate(oggetti, start=1):
        offset.append(len(dati))
        dati += f"{i} 0 obj\n".encode("ascii") + corpo + b"\nendobj\n"
    xref = len(dati)
    dati += f"xref\n0 {len(oggetti) + 1}\n0000000000 65535 f \n".encode("ascii")
    for o in offset:
        dati += f"{o:010d} 00000 n \n".encode("ascii")
    dati += (f"trailer\n<< /Size {len(oggetti) + 1} /Root 1 0 R /Info 5 0 R >>\n"
             f"startxref\n{xref}\n%%EOF\n").encode("ascii")
    PDF.write_bytes(bytes(dati))


def scrivi_png(m):
    n = len(m)
    img = Image.new("L", (n, n), 255)
    img.putdata([0 if v else 255 for riga in m for v in riga])
    img = img.resize((n * PX_MODULO, n * PX_MODULO), Image.NEAREST)
    # pHYs in pixel per metro scelto in modo che il lato valga esattamente 25 mm.
    ppm = round(n * PX_MODULO / (LATO_MM / 1000))
    dpi = ppm * 0.0254
    img.save(PNG, dpi=(dpi, dpi), optimize=False)


def scrivi_checksum():
    righe = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}" for p in (SVG, PDF, PNG)]
    SUMS.write_text("\n".join(righe) + "\n", encoding="ascii", newline="\n")
    return righe


def main():
    qr = crea_qr()
    m = matrice_con_margine(qr)
    scrivi_svg(m)
    scrivi_pdf(m)
    scrivi_png(m)
    print(f"URL: {URL}")
    print(f"QR: {qr.designator} (versione {qr.version}, errore {qr.error}, maschera {qr.mask}), "
          f"{len(m) - 2 * MARGINE} moduli + {MARGINE} di margine = {len(m)} moduli, "
          f"modulo {LATO_MM / len(m):.4f} mm")
    for r in scrivi_checksum():
        print(r)


if __name__ == "__main__":
    main()
