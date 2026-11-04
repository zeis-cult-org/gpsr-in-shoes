"""Controllo qualità digitale del QR GPSR (solo lettura, non modifica i file).

Verifica: contenuto decodificato, identità modulo per modulo tra SVG/PDF/PNG e la
matrice di riferimento, dimensioni fisiche, contenuto vettoriale del PDF, colori,
quiet zone, orientamento, leggibilità a diverse risoluzioni, sfocatura e rotazione,
checksum SHA-256.

Uso:  python verifica_qr.py      (esce con codice 1 se un controllo fallisce)
"""
import hashlib
import re
import sys
from pathlib import Path

import cv2
import pymupdf as fitz
import numpy as np
import segno
import zxingcpp
from PIL import Image

URL = "https://gpsr.in-shoes.it/"
MARGINE = 4
LATO_MM = 25.0
QUI = Path(__file__).resolve().parent
SVG = QUI / "GPSR_IN_SHOES_MASTER.svg"
PDF = QUI / "GPSR_IN_SHOES_STAMPA.pdf"
PNG = QUI / "GPSR_IN_SHOES_PREVIEW.png"
SUMS = QUI / "SHA256SUMS.txt"

esiti = []


def check(nome, ok, dettaglio=""):
    esiti.append(ok)
    print(f"[{'OK' if ok else 'ERRORE'}] {nome}" + (f" — {dettaglio}" if dettaglio else ""))


def riferimento():
    qr = segno.make(URL, error="q", mode="byte", boost_error=False, micro=False)
    m = np.array([[1 if v else 0 for v in r] for r in qr.matrix_iter(scale=1, border=MARGINE)], dtype=np.uint8)
    return qr, m


def campiona(gray, n):
    """Matrice n x n (1 = nero) leggendo il centro di ogni modulo."""
    h, w = gray.shape
    ys = ((np.arange(n) + 0.5) * h / n).astype(int)
    xs = ((np.arange(n) + 0.5) * w / n).astype(int)
    return (gray[np.ix_(ys, xs)] < 128).astype(np.uint8)


def decodifica(gray):
    """Testo letto da ZXing-C++ e da OpenCV (None se non letto)."""
    z = zxingcpp.read_barcodes(gray, formats=zxingcpp.BarcodeFormat.QRCode)
    t_z = z[0].text if z else None
    info_z = (z[0].symbology_identifier, str(z[0].ec_level), z[0].orientation) if z else None
    t_cv, _, _ = cv2.QRCodeDetector().detectAndDecode(gray)
    return t_z, (t_cv or None), info_z


def render(path, dpi):
    doc = fitz.open(str(path))
    pix = doc[0].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()


def main():
    qr, ref = riferimento()
    n = ref.shape[0]
    print(f"Riferimento: {qr.designator}, maschera {qr.mask}, {n} x {n} moduli con quiet zone\n")

    # --- Struttura del riferimento: quiet zone e pattern di posizione
    check("Quiet zone di 4 moduli bianchi su ogni lato",
          not ref[:MARGINE].any() and not ref[-MARGINE:].any() and not ref[:, :MARGINE].any() and not ref[:, -MARGINE:].any())
    finder = np.ones((7, 7), np.uint8); finder[1:6, 1:6] = 0; finder[2:5, 2:5] = 1
    a, b = MARGINE, n - MARGINE - 7
    check("Orientamento: pattern di posizione in alto a sinistra, alto a destra, basso a sinistra",
          (ref[a:a+7, a:a+7] == finder).all() and (ref[a:a+7, b:b+7] == finder).all()
          and (ref[b:b+7, a:a+7] == finder).all() and not (ref[b:b+7, b:b+7] == finder).all())

    # --- SVG
    s = SVG.read_text(encoding="utf-8")
    check("SVG: dimensioni 25 x 25 mm e viewBox 37 x 37",
          'width="25mm"' in s and 'height="25mm"' in s and f'viewBox="0 0 {n} {n}"' in s)
    colori = set(re.findall(r'fill="([^"]+)"', s))
    check("SVG: solo nero puro #000000 su bianco #FFFFFF", colori == {"#000000", "#FFFFFF"}, str(sorted(colori)))
    check("SVG: nessuna immagine raster, testo visibile, link o script",
          not re.search(r"<(image|text|a|script|use|filter)\b", s))
    m_svg = np.zeros_like(ref)
    for x, y, w in re.findall(r"M(\d+) (\d+)h(\d+)v1h-\d+z", s):
        m_svg[int(y), int(x):int(x) + int(w)] = 1
    check("SVG: moduli identici alla matrice di riferimento", (m_svg == ref).all())
    g = render(SVG, 600)
    check("SVG renderizzato (600 dpi): moduli identici", (campiona(g, n) == ref).all())
    tz, tcv, _ = decodifica(g)
    check("SVG renderizzato: decodifica ZXing e OpenCV = URL esatto", tz == URL and tcv == URL, f"ZXing={tz!r} OpenCV={tcv!r}")

    # --- PDF
    doc = fitz.open(str(PDF))
    p = doc[0]
    w_mm, h_mm = p.rect.width / 72 * 25.4, p.rect.height / 72 * 25.4
    check("PDF: struttura valida (aperto senza riparazioni)", not doc.is_repaired)
    check("PDF: una pagina di 25,000 x 25,000 mm (MediaBox)",
          len(doc) == 1 and abs(w_mm - 25) < 0.001 and abs(h_mm - 25) < 0.001, f"{w_mm:.4f} x {h_mm:.4f} mm")
    check("PDF: TrimBox uguale a MediaBox", p.trimbox == p.mediabox)
    check("PDF: contenuto vettoriale, nessuna immagine raster",
          len(p.get_images()) == 0 and len(p.get_drawings()) > 0, f"{len(p.get_drawings())} gruppi vettoriali, {len(p.get_images())} immagini")
    check("PDF: nessun testo sovrapposto", p.get_text().strip() == "")
    cs = PDF.read_bytes().decode("latin-1")
    col = set(re.findall(r"([\d.]+ [\d.]+ [\d.]+ [\d.]+) k", cs))
    check("PDF: colori CMYK solo bianco (0 0 0 0) e nero K100 (0 0 0 1)",
          col == {"0 0 0 0", "0 0 0 1"} and " rg" not in cs and " g\n" not in cs, str(sorted(col)))
    g = render(PDF, 600)
    check("PDF renderizzato (600 dpi): moduli identici", (campiona(g, n) == ref).all())
    tz, tcv, info = decodifica(g)
    check("PDF renderizzato: decodifica ZXing e OpenCV = URL esatto", tz == URL and tcv == URL, f"ZXing={tz!r} OpenCV={tcv!r}")
    check("Livello di correzione letto dal decodificatore = Q", info is not None and info[1] == "Q", f"{info}")

    # --- PNG
    im = Image.open(PNG)
    dpi = im.info.get("dpi", (0, 0))[0]
    lato_png_mm = im.width / dpi * 25.4 if dpi else 0
    check("PNG: 1184 x 1184 px, scala di grigi, lato 25 mm dai metadati",
          im.size == (1184, 1184) and im.mode == "L" and abs(lato_png_mm - 25) < 0.01, f"{im.size}, {im.mode}, {dpi:.1f} dpi = {lato_png_mm:.3f} mm")
    a = np.array(im)
    check("PNG: solo valori 0 (nero) e 255 (bianco), contrasto 21:1", set(np.unique(a).tolist()) == {0, 255})
    check("PNG: moduli identici", (campiona(a, n) == ref).all())
    tz, tcv, _ = decodifica(a)
    check("PNG: decodifica ZXing e OpenCV = URL esatto", tz == URL and tcv == URL, f"ZXing={tz!r} OpenCV={tcv!r}")
    check("Proporzioni 1:1 in SVG, PDF e PNG", im.width == im.height and p.rect.width == p.rect.height)

    # --- Leggibilità a diverse risoluzioni (PDF renderizzato a 25 mm)
    print("\nLeggibilità digitale (25 mm renderizzati a varie risoluzioni):")
    for d in (72, 100, 150, 200, 300, 600):
        g = render(PDF, d)
        tz, tcv, _ = decodifica(g)
        px_mod = g.shape[0] / n
        check(f"  {d:>3} dpi ({g.shape[0]} px, {px_mod:.1f} px/modulo)", tz == URL, f"ZXing={'OK' if tz == URL else tz} OpenCV={'OK' if tcv == URL else tcv}")
    g = render(PDF, 300)
    tz, _, _ = decodifica(cv2.GaussianBlur(g, (0, 0), 3))
    check("  300 dpi con sfocatura gaussiana (sigma 3 px)", tz == URL)
    big = cv2.copyMakeBorder(g, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=255)
    c = (big.shape[1] / 2, big.shape[0] / 2)
    rot = cv2.warpAffine(big, cv2.getRotationMatrix2D(c, 20, 1), (big.shape[1], big.shape[0]), borderValue=255)
    tz, _, _ = decodifica(rot)
    check("  300 dpi ruotato di 20 gradi", tz == URL)
    tz, _, _ = decodifica(np.ascontiguousarray(cv2.rotate(g, cv2.ROTATE_180)))
    check("  300 dpi capovolto (180 gradi)", tz == URL)

    # --- Checksum
    attese = dict(reversed(r.split("  ")) for r in SUMS.read_text(encoding="ascii").split("\n") if r)
    for f in (SVG, PDF, PNG):
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        check(f"SHA-256 {f.name}", attese.get(f.name) == h, h)

    print(f"\nESITO: {'OK' if all(esiti) else 'ERRORI'} ({sum(esiti)}/{len(esiti)} controlli superati)")
    return 0 if all(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
