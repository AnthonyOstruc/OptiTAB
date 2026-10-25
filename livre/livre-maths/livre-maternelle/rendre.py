"""Rend les pages d’un cahier en planches pour la relecture : python rendre.py ps [dpi] [par_planche] [premiere-derniere]"""
from pathlib import Path
import subprocess, sys
from PIL import Image

RACINE = Path(__file__).resolve().parent

def rendre(cle, dpi=50, par=6, plage=None):
    sortie = RACINE / 'build' / 'rendu' / cle
    sortie.mkdir(parents=True, exist_ok=True)
    for p in sortie.glob('*.png'):
        p.unlink()
    cmd = ['pdftoppm', '-r', str(dpi), '-png']
    if plage:
        a, b = plage.split('-')
        cmd += ['-f', a, '-l', b]
    subprocess.run(cmd + [str(RACINE / cle / 'main.pdf'), str(sortie / 'p')], check=True)
    pages = sorted(sortie.glob('p-*.png'))
    w, h = Image.open(pages[0]).size
    cols = 3 if par <= 6 else 4
    lignes = (par + cols - 1) // cols
    for k in range(0, len(pages), par):
        planche = Image.new('RGB', (cols * (w + 8) + 8, lignes * (h + 8) + 8), (120, 120, 120))
        for i, p in enumerate(pages[k:k + par]):
            planche.paste(Image.open(p), (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
        planche.save(sortie / f'planche-{k // par + 1:02d}.png')
    print(len(pages), 'pages,', (len(pages) + par - 1) // par, 'planches dans', sortie)

if __name__ == '__main__':
    a = sys.argv[1:]
    rendre(a[0], int(a[1]) if len(a) > 1 else 50, int(a[2]) if len(a) > 2 else 6, a[3] if len(a) > 3 else None)
