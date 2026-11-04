# -*- coding: utf-8 -*-
"""Harmonise les tableaux HTML des cours et fiches de 3ème (gabarit OptiTAB, bordures nettes).

- conteneur défilant (overflow-x:auto) pour les petits écrans ;
- bordure extérieure bleue de 2 px, grille intérieure de 1 px bien visible ;
- en-tête bleu à texte blanc ; lignes alternées ;
- tableau sans en-tête : la première colonne sert d'en-tête de ligne.

Usage : python outils/tableaux_3e.py [--test fichier.html]
"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
FRONT = ICI.parents[3]
FICHIERS = sorted((FRONT / "cours/cours_optitab/3e").glob("*.txt")) + \
    sorted((FRONT / "cours/resume/3e").glob("*.txt"))

GRILLE = "#b6c8da"
TABLE = ("width:100%; min-width:300px; border-collapse:collapse; margin:0; "
         "border:2px solid #3498db; background:#ffffff;")
TH = ("border:1px solid #2b7bb9; padding:10px 12px; text-align:center; vertical-align:middle; "
      "background:#3498db; color:#ffffff; font-weight:700;")
TD = (f"border:1px solid {GRILLE}; padding:10px 12px; text-align:center; vertical-align:middle; "
      "color:#2c3e50;")
TD_TETE = (f"border:1px solid {GRILLE}; padding:10px 12px; text-align:center; "
           "vertical-align:middle; background:#eaf3fb; color:#2c3e50; font-weight:700;")
FONDS = ["#ffffff", "#f4f8fc"]
OUVRE = '<div style="overflow-x:auto; margin:15px 0;">'


def restyle(tab):
    sans_entete = "<th" not in tab
    tab = re.sub(r"<table[^>]*>", f'<table style="{TABLE}">', tab, count=1)
    tab = re.sub(r"<th\b[^>]*>", f'<th style="{TH}">', tab)
    rangs = []

    def tr(m):
        i = len(rangs)
        rangs.append(m.group(0))
        corps = m.group(0)
        if "<th" in corps:
            return re.sub(r"<tr\b[^>]*>", '<tr style="background:#3498db;">', corps, count=1)
        corps = re.sub(r"<tr\b[^>]*>", f'<tr style="background:{FONDS[i % 2]};">', corps, count=1)
        cellules = [0]

        def td(mm):
            cellules[0] += 1
            return f'<td style="{TD_TETE if (sans_entete and cellules[0] == 1) else TD}">'
        return re.sub(r"<td\b[^>]*>", td, corps)
    return re.sub(r"<tr\b.*?</tr>", tr, tab, flags=re.S)


def traiter(txt):
    def rep(m):
        avant = txt[max(0, m.start() - 80):m.start()]
        tab = restyle(m.group(0))
        if "overflow-x:auto" in avant:
            return tab
        return f"{OUVRE}\n{tab}\n</div>"
    return re.sub(r"<table\b.*?</table>", rep, txt, flags=re.S)


def main():
    if "--test" in sys.argv:
        src = (FRONT / "cours/cours_optitab/3e/cours_transformations_3e.txt").read_text(encoding="utf-8")
        tab = re.search(r"<table\b.*?</table>", src, re.S).group(0)
        src2 = (FRONT / "cours/cours_optitab/3e/cours_raisonner_3e.txt").read_text(encoding="utf-8")
        tab2 = re.search(r"<table\b.*?</table>", src2, re.S).group(0)
        page = ("<!doctype html><html><head><meta charset='utf-8'>"
                "<script>window.MathJax={tex:{inlineMath:[['$','$']]}};</script>"
                "<script src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js'></script>"
                "</head><body style='font-family:Arial;padding:16px;background:#f9f9f9'>"
                f"<h3>Avant</h3>{tab}<h3>Après</h3>{traiter(tab)}<h3>Sans en-tête (après)</h3>"
                f"{traiter(tab2)}</body></html>")
        Path(sys.argv[sys.argv.index("--test") + 1]).write_text(page, encoding="utf-8")
        return
    n = 0
    for f in FICHIERS:
        t = f.read_text(encoding="utf-8")
        t2 = traiter(t)
        if t2 != t:
            f.write_text(t2, encoding="utf-8")
            n += 1
            print("restylé :", f.name)
    print(f"{n} fichier(s) modifié(s)")


if __name__ == "__main__":
    main()
