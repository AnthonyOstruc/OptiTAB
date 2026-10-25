"""Agrandit une zone d'une page du PDF pour vérifier un détail.

python zoom_pdf.py <page PDF> <x0> <y0> <x1> <y1> [dpi]   (coordonnées en points PDF, origine en haut à gauche)
"""
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parent
n, x0, y0, x1, y1 = (float(a) for a in sys.argv[1:6])
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 300
doc = fitz.open(ROOT / 'main.pdf')
pix = doc[int(n) - 1].get_pixmap(dpi=dpi, clip=fitz.Rect(x0, y0, x1, y1))
sortie = ROOT / 'build' / 'qa' / 'pages' / f'zoom-{int(n):03d}.png'
sortie.parent.mkdir(parents=True, exist_ok=True)
pix.save(sortie)
print(sortie.name, pix.width, pix.height)
