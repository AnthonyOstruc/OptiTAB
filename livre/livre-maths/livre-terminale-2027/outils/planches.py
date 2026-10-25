"""Rend toutes les pages du PDF en planches PNG (contrôle visuel).

Usage : python -I -X utf8 outils/planches.py [pdf] [dossier] [pages_par_planche] [dpi]
Par défaut : main.pdf, build/qa, 18 pages par planche (6 x 3), 40 dpi. Chaque page porte son numéro.
"""
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

R = Path(__file__).resolve().parent.parent
pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else R / "main.pdf"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else R / "build" / "qa"
par = int(sys.argv[3]) if len(sys.argv) > 3 else 18
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 40
cols = 6 if par >= 12 else 4
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("planche-*.png"):
    old.unlink()
doc = fitz.open(pdf)
for start in range(0, doc.page_count, par):
    ims = []
    for i in range(start, min(start + par, doc.page_count)):
        pix = doc[i].get_pixmap(dpi=dpi)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 34, 14], fill=(255, 230, 0))
        d.text((3, 1), str(i + 1), fill=(0, 0, 0))
        ims.append(im)
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), (120, 120, 120))
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * (w + 6), (k // cols) * (h + 6)))
    sheet.save(out / f"planche-{start + 1:03d}-{min(start + par, doc.page_count):03d}.png")
print(doc.page_count, "pages rendues dans", out)
