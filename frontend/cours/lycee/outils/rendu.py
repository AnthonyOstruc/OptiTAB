# -*- coding: utf-8 -*-
"""Rendu PDF (Chrome sans interface + MathJax) d'un cours ou d'une fiche, pour relecture visuelle.

Usage : python outils/rendu.py <slug> cours|fiche
Les images existantes en base sont lues via images/existantes.json ({"cours_<id>": {"1": "url"}}).
"""
import json
import re
import subprocess
import sys

from lycee_commun import RACINE, SORTIE, IMAGES, charger_spec

CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>window.MathJax = {{tex: {{inlineMath: [['$','$']]}}, svg: {{fontCache: 'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>
<style>body{{max-width:860px;margin:20px auto;font-family:Arial,sans-serif}} img{{max-width:100%;display:block;margin:12px auto}}</style>
</head><body>{corps}</body></html>"""


def rendre(slug, quoi):
    sp = charger_spec(slug)
    html = (SORTIE / f"{slug}_{quoi}.html").read_text(encoding="utf-8")
    images = {}
    if quoi == "cours":
        ex = json.loads((IMAGES / "existantes.json").read_text(encoding="utf-8")).get(f"cours_{sp.COURS_ID}", {})
        images.update({int(k): v for k, v in ex.items()})
        n0 = max(images) if images else 0
        for k, fig in enumerate(sp.FIGURES, n0 + 1):
            images[k] = (IMAGES / fig["fichier"]).as_uri()
    else:
        for k, f in enumerate(sp.FICHE_IMAGES, 1):
            images[k] = (IMAGES / f).as_uri()
    html = re.sub(r"\[IMAGE_(\d+)\]", lambda m: f'<img src="{images.get(int(m.group(1)), "")}">', html)
    page = RACINE / "rendus" / f"{slug}_{quoi}.html"
    page.write_text(PAGE.format(corps=html), encoding="utf-8")
    pdf = RACINE / "rendus" / f"{slug}_{quoi}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", page.as_uri()],
                   check=True, capture_output=True)
    print(pdf)


if __name__ == "__main__":
    rendre(sys.argv[1], sys.argv[2])
