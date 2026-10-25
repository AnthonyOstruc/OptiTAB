# -*- coding: utf-8 -*-
"""Génère evaluations/fig-folium-niveaux.tex : lignes de niveau de
f(x, y) = x^3 + y^3 - 3xy (examen de fin d'année, exercice 3).
Le niveau 0 (folium de Descartes) est tracé à part, par son paramétrage."""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BS = chr(92)
xs = np.linspace(-2.0, 2.5, 700)
ys = np.linspace(-2.0, 2.5, 700)
Xg, Yg = np.meshgrid(xs, ys)
F = Xg**3 + Yg**3 - 3*Xg*Yg
niveaux = [-0.8, -0.45, 0.7, 2.0]
couleurs = {-0.8: "otGreenDark!80", -0.45: "otGreenDark!55", 0.7: "otNavy!45", 2.0: "otNavy!30"}
cs = plt.contour(Xg, Yg, F, levels=niveaux)
lignes = []
for lev, segs in zip(cs.levels, cs.allsegs):
    for s in segs:
        if len(s) < 8:
            continue
        ferme = np.hypot(*(s[0] - s[-1])) < 1e-3
        s = s[::5] if not ferme else s[::5]
        pts = " -- ".join("(%.3f,%.3f)" % (p[0], p[1]) for p in s)
        fin = " -- cycle;" if ferme else ";"
        lignes.append(BS + "draw[%s,line width=0.6pt] " % couleurs[float(round(lev, 2))] + pts + fin)
sortie = os.path.join(os.path.dirname(__file__), "..", "evaluations", "fig-folium-niveaux.tex")
with io.open(sortie, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("% Fichier généré par verifications/fig_folium.py — ne pas éditer\n")
    fh.write("\n".join(lignes) + "\n")
print("ecrit :", os.path.normpath(sortie), len(lignes), "courbes")
