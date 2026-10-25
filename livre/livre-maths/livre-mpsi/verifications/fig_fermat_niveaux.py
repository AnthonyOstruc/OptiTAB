# -*- coding: utf-8 -*-
"""Génère chapitres/defis/fig-fermat-niveaux.tex : lignes de niveau de
f(M) = MA + MB + MC pour A(-1,0), B(1,0), C(0,2) (défi du chapitre 20)."""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BS = chr(92)
A, B, C = (-1, 0), (1, 0), (0, 2)
xs = np.linspace(-2.2, 2.2, 500)
ys = np.linspace(-1.3, 3.2, 500)
Xg, Yg = np.meshgrid(xs, ys)
F = sum(np.hypot(Xg - p[0], Yg - p[1]) for p in (A, B, C))
niveaux = [3.85, 4.2, 4.8, 5.6, 6.6]
cs = plt.contour(Xg, Yg, F, levels=niveaux)
lignes = []
for lev, segs in zip(cs.levels, cs.allsegs):
    for s in segs:
        s = s[::6]
        pts = " -- ".join("(%.3f,%.3f)" % (p[0], p[1]) for p in s)
        lignes.append(BS + "draw[otNavy!45,line width=0.5pt] " + pts + " -- cycle;")
sortie = os.path.join(os.path.dirname(__file__), "..", "chapitres", "defis", "fig-fermat-niveaux.tex")
with io.open(sortie, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("% Fichier généré par verifications/fig_fermat_niveaux.py — ne pas éditer\n")
    fh.write("\n".join(lignes) + "\n")
print("ecrit :", os.path.normpath(sortie), len(lignes), "lignes de niveau")
