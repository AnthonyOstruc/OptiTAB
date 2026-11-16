# -*- coding: utf-8 -*-
"""Figures de « Calculer une durée » : méthode des sauts sur une ligne du temps."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fig_commun import PREAMBULE_EXTRA, f, tikz, carte  # noqa: E402,F401

FIGURES = {}


def hm(m):
    return "%d\\,\\mathrm{h}\\,%02d" % (m // 60, m % 60)


def duree(m):
    h, mn = divmod(m, 60)
    if not h:
        return "%d min" % mn
    return "%d h" % h + (" %d min" % mn if mn else "")


def sauts(reperes, x_de, total=True, haut=.75):
    """Ligne du temps : repères (minutes) placés en x_de(m), sauts verts entre eux."""
    L = []
    x0, x1 = x_de(reperes[0]), x_de(reperes[-1])
    L.append(r"\draw[otMuted,line width=.8pt] (%s,0) -- (%s,0);" % (f(x0 - .3), f(x1 + .3)))
    for m in reperes:
        x = x_de(m)
        L.append(r"\draw[otNavy,line width=.9pt] (%s,-.12) -- (%s,.12);" % (f(x), f(x)))
        L.append(r"\node[grad,anchor=north] at (%s,-.18) {$%s$};" % (f(x), hm(m)))
    for a, b in zip(reperes, reperes[1:]):
        xa, xb = x_de(a), x_de(b)
        L.append(r"\draw[saut] (%s,.18) to[bend left=40] (%s,.18);" % (f(xa + .04), f(xb - .04)))
        L.append(r"\node[etiq,anchor=south,text=otGreenDark] at (%s,%s) {%s};" % (f((xa + xb) / 2), f(.18 + haut * min(1, (xb - xa) / 3) + .12), duree(b - a)))
    if total:
        d = reperes[-1] - reperes[0]
        L.append(r"\node[etiq,anchor=north,text=otGreenDark] at (%s,-.85) {total : %s};" % (f((x0 + x1) / 2), duree(d)))
    return L


# 8 h 45 → 9 h 00 → 11 h 00 → 11 h 20 : 15 min + 2 h + 20 min = 2 h 35 min.
R = [8 * 60 + 45, 9 * 60, 11 * 60, 11 * 60 + 20]
assert R[-1] - R[0] == 155
# Échelle non proportionnelle (lisible) : positions choisies à la main.
POS = {R[0]: 0.0, R[1]: 1.6, R[2]: 5.0, R[3]: 6.6}
FIGURES["duree_sauts"] = tikz(sauts(R, POS.get))

# Aperçu de la carte.
FIGURES["carte_duree"] = carte(sauts(R, {R[0]: 0.0, R[1]: 1.25, R[2]: 3.75, R[3]: 5.0}.get))
