# -*- coding: utf-8 -*-
"""Planche-contact des figures d'un chapitre (relecture visuelle).
Usage : python planche.py <prefixe> <sortie.png> [colonnes]   ex. : python planche.py relatifs_4e out.png 3
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

FRONT = Path(__file__).resolve().parents[4]
pref, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
files = sorted((FRONT / "cours/cours_optitab/4e/images").glob(pref + "*.png")) + \
        sorted((FRONT / "exercices/4e/images").glob(pref + "*.png"))
W = 560
tiles = []
for f in files:
    im = Image.open(f).convert("RGB")
    im.thumbnail((W, 420))
    t = Image.new("RGB", (W, 450), "white")
    t.paste(im, ((W - im.width) // 2, 24))
    ImageDraw.Draw(t).text((6, 4), f.name, fill=(200, 0, 0))
    tiles.append(t)
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * 450), (230, 230, 230))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * W, (i // cols) * 450))
sheet.save(out)
print(len(tiles), "figures ->", out)
