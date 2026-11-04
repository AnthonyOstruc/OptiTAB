# -*- coding: utf-8 -*-
"""Planche-contact des figures d'un préfixe : python outils/planche.py <prefixe>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[1]
fs = sorted((R / "images").glob(sys.argv[1] + "*.png"))
W, tiles = 620, []
for f in fs:
    im = Image.open(f).convert("RGB"); im.thumbnail((W, 470))
    t = Image.new("RGB", (W, 500), "white"); t.paste(im, ((W - im.width) // 2, 26))
    ImageDraw.Draw(t).text((6, 4), f.name, fill=(200, 0, 0)); tiles.append(t)
sh = Image.new("RGB", (3 * W, ((len(tiles) + 2) // 3) * 500), (230, 230, 230))
for i, t in enumerate(tiles):
    sh.paste(t, ((i % 3) * W, (i // 3) * 500))
out = R / "rendus" / f"planche_{sys.argv[1]}.png"; sh.save(out); print(out)
