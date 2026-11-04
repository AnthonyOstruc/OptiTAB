# -*- coding: utf-8 -*-
"""Chaîne « de zéro » des cours et fiches de lycée (format OptiTAB 3ème/4ème).

Usage :
  python v2/v2.py construire <slug> [--rendu]   contrôle + sortie/<slug>_cours.html et _fiche.html (+ PDF)
Fichiers source :
  v2/cours/<slug>.txt  : « === titre », « Images: a.png, b.png », « Titre: … », puis le HTML
  v2/fiches/<slug>.txt : « Images: … », « Titre: Résumé : … », puis le HTML
Dans le HTML, les formules s'écrivent $...$ ; \\displaystyle est ajouté automatiquement.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V2 = Path(__file__).resolve().parent
RACINE = V2.parent
IMAGES = RACINE / "images"
SORTIE = V2 / "sortie"
VERIF_MJ = RACINE.parent / "cours_optitab" / "4e" / "outils" / "verifier_mathjax.cjs"
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>window.MathJax = {{tex: {{inlineMath: [['$','$']]}}, svg: {{fontCache: 'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>
<style>body{{max-width:860px;margin:20px auto;font-family:Arial,sans-serif}} img{{max-width:100%;display:block;margin:12px auto}}</style>
</head><body>{corps}</body></html>"""


def lire(chemin):
    brut = chemin.read_text(encoding="utf-8")
    champ = lambda n: (re.search(rf"^{n}:\s*(.*)$", brut, re.M) or [None, ""])[1].strip()  # noqa: E731
    images = [s.strip() for s in champ("Images").split(",") if s.strip()]
    html = brut[brut.index("<div"):].strip()
    return champ("Titre"), images, html


def displaystyle(html):
    return re.sub(r"\$(?!\\displaystyle)([^$]+?)\$", r"$\\displaystyle \1$", html)


def controler(html, images, nom):
    err = []
    if len(re.findall(r"<div\b", html)) != html.count("</div>"):
        err.append("<div> non équilibrés")
    for k, ligne in enumerate(html.splitlines(), 1):
        if ligne.count("$") % 2:
            err.append(f"ligne {k} : nombre impair de $")
    hors_maths = re.sub(r"\$[^$]*\$", "", html)
    if "*" in re.sub(r"<[^>]+>", "", hors_maths):
        err.append("astérisque hors formule (rendu en italique sur le site)")
    marques = [int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", html)]
    if sorted(marques) != list(range(1, len(images) + 1)):
        err.append(f"marqueurs {sorted(marques)} ≠ images 1..{len(images)}")
    for f in images:
        if not (IMAGES / f).exists():
            err.append(f"image absente : {f}")
    for e in err:
        print(f"  [ERREUR] {nom} : {e}")
    return not err


def rendre(slug, quoi, html, images):
    corps = re.sub(r"\[IMAGE_(\d+)\]", lambda m: f'<img src="{(IMAGES / images[int(m.group(1)) - 1]).as_uri()}">',
                   html)
    page = SORTIE / f"{slug}_{quoi}_rendu.html"
    page.write_text(PAGE.format(corps=corps), encoding="utf-8")
    pdf = RACINE / "rendus" / f"{slug}_{quoi}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", page.as_uri()],
                   check=True, capture_output=True)
    return pdf


def construire(slug, rendu=False):
    ok = True
    sorties = []
    for quoi, dossier in (("cours", "cours"), ("fiche", "fiches")):
        titre, images, html = lire(V2 / dossier / f"{slug}.txt")
        html = displaystyle(html)
        ok &= controler(html, images, f"{slug} ({quoi})")
        out = SORTIE / f"{slug}_{quoi}.html"
        out.write_text(html, encoding="utf-8")
        sorties.append(out)
        print(f"[{slug}] {quoi} : « {titre} », {len(html)} car., {len(images)} image(s)")
        if rendu:
            print("   rendu :", rendre(slug, quoi, html, images))
    r = subprocess.run(["node", str(VERIF_MJ)] + [str(s) for s in sorties], capture_output=True, text=True,
                       encoding="utf-8")
    print("  ", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-400:])
    ok &= r.returncode == 0 and "0 erreur" in r.stdout
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "construire":
        sys.exit(0 if construire(sys.argv[2], "--rendu" in sys.argv) else 1)
