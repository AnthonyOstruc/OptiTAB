"""Ajuste les portions de droite des courbes de titrage conductimétrique et calcule les volumes équivalents.

Lancer : python -I -X utf8 verifications/droites_conductimetrie.py
"""
from pathlib import Path
import numpy as np

DONNEES = Path(__file__).resolve().parent.parent / 'figures' / 'donnees'


def segments(nom, bornes, colonne=1):
    data = np.loadtxt(DONNEES / f'{nom}.dat', skiprows=1)
    v, s = data[:, 0], data[:, colonne]
    droites = []
    for a, b in bornes:
        m = (v >= a) & (v <= b)
        p, q = np.polyfit(v[m], s[m], 1)
        droites.append((p, q))
    inters = []
    for (p1, q1), (p2, q2) in zip(droites, droites[1:]):
        x = (q2 - q1) / (p1 - p2)
        inters.append(x)
    texte = ' ; '.join(f'droite {i + 1}: y = {p:.5f} x + {q:.5f}' for i, (p, q) in enumerate(droites))
    print(f'{nom} [col {colonne}] : {texte} ; intersections : {[round(x, 3) for x in inters]}')
    return droites, inters


if __name__ == '__main__':
    segments('03-hcl-naoh-sigma', [(0, 1.75), (2.25, 4)])
    segments('03-naoh-hcl-sigma', [(0, 7), (9, 16)])
    segments('03-chlorure-sigma', [(0, 5.5), (7, 12)])
    segments('03-melange-sigma', [(0, 2.5), (6, 13), (15, 20)])
    segments('03-dilution-sigma', [(0, 9), (11, 20)], colonne=2)
    segments('03-dilution-sigma', [(0, 4), (16, 20)], colonne=1)
