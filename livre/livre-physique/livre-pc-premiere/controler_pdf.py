"""Rend les pages du PDF pour la relecture visuelle.

python controler_pdf.py            -> planches de 6 pages dans build/qa/planches
python controler_pdf.py 12 13 14   -> pages isolées (numérotation du PDF, 1 = couverture) dans build/qa/pages
"""
import sys
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent
PDF = ROOT / 'main.pdf'
QA = ROOT / 'build' / 'qa'


def rendre(page, dpi):
    pix = page.get_pixmap(dpi=dpi)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def planches(doc, par_planche=6, dpi=55):
    dossier = QA / 'planches'
    dossier.mkdir(parents=True, exist_ok=True)
    for f in dossier.glob('*.png'):
        f.unlink()
    for debut in range(0, len(doc), par_planche):
        images = [rendre(doc[i], dpi) for i in range(debut, min(debut + par_planche, len(doc)))]
        w, h = images[0].size
        planche = Image.new('RGB', (3 * w + 40, 2 * h + 30), 'white')
        for k, im in enumerate(images):
            planche.paste(im, (10 + (k % 3) * (w + 10), 10 + (k // 3) * (h + 10)))
        nom = dossier / f'planche-{debut + 1:03d}-{debut + len(images):03d}.png'
        planche.save(nom)
        print(nom.name)


def pages(doc, numeros, dpi=110):
    dossier = QA / 'pages'
    dossier.mkdir(parents=True, exist_ok=True)
    for n in numeros:
        nom = dossier / f'page-{n:03d}.png'
        rendre(doc[n - 1], dpi).save(nom)
        print(nom.name)


if __name__ == '__main__':
    doc = fitz.open(PDF)
    print(len(doc), 'pages')
    if len(sys.argv) > 1:
        pages(doc, [int(a) for a in sys.argv[1:]])
    else:
        planches(doc)
