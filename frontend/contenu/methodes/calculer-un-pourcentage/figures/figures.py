# -*- coding: utf-8 -*-
"""Figures de « Calculer un pourcentage » (valeurs recalculées et vérifiées)."""
from fractions import Fraction as Fr

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,line width=.8pt,rounded corners=3pt,fill=otSky,minimum height=.8cm,minimum width=1.7cm,inner sep=4pt,font=\fontsize{12}{14}\selectfont},
  fleche/.style={otGreenDark,line width=1pt,-{Stealth[length=2.4mm]}},
  coef/.style={font=\fontsize{10.5}{12}\selectfont,text=otGreenDark,inner sep=2pt},
  note/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,inner sep=1pt},
}
"""


def f(v):
    return ("%.4f" % float(v)).rstrip("0").rstrip(".")


def nombre(x):
    """Fraction -> écriture française « 1{,}15 »."""
    s = f(x)
    return s.replace(".", "{,}")


def grille(n_colorees, c=.36, x0=0.0, y0=0.0):
    """Carré de 100 cases, les n premières colorées (ligne par ligne, depuis le haut)."""
    L = []
    for k in range(100):
        i, j = k % 10, k // 10
        x, y = x0 + i * c, y0 - (j + 1) * c
        coul = "otGreen!70" if k < n_colorees else "white"
        L.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (coul, f(x), f(y), f(x + c), f(y + c)))
    for i in range(11):
        L.append(r"\draw[otMuted!60,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x0 + i * c), f(y0), f(x0 + i * c), f(y0 - 10 * c)))
        L.append(r"\draw[otMuted!60,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x0), f(y0 - i * c), f(x0 + 10 * c), f(y0 - i * c)))
    L.append(r"\draw[otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x0 + 10 * c), f(y0 - 10 * c)))
    return L


def tikz(L):
    return "\\begin{tikzpicture}\n" + "\n".join(L) + "\n\\end{tikzpicture}"


FIGURES = {}

# 15 % : 15 cases sur 100.
L = grille(15)
L.append(r"\node[anchor=west,text=otGreenDark,font=\fontsize{12}{14}\selectfont] at (4.0,-1.1) {$15\,\%=\dfrac{15}{100}=0{,}15$};")
L.append(r"\node[anchor=west,note,align=left] at (4.0,-2.35) {15 cases colorées\\sur 100 cases};")
FIGURES["pourcentage_grille"] = tikz(L)


def chaine(valeurs, coefs, unite="€", ecart=3.4):
    """Valeurs reliées par des flèches « × coefficient » (le calcul est vérifié)."""
    for a, k, b in zip(valeurs, coefs, valeurs[1:]):
        assert Fr(a) * Fr(k) == Fr(b), (a, k, b)
    L = []
    for i, v in enumerate(valeurs):
        L.append(r"\node[boite] (v%d) at (%s,0) {$%s$ %s};" % (i, f(i * ecart), nombre(Fr(v)), unite))
    for i, k in enumerate(coefs):
        L.append(r"\draw[fleche] (v%d.east) -- (v%d.west);" % (i, i + 1))
        L.append(r"\node[coef,anchor=south] at (%s,.5) {$\times %s$};" % (f(i * ecart + ecart / 2), nombre(Fr(k))))
    return L


# Hausse de 15 % (× 1,15) et baisse de 30 % (× 0,7).
L = chaine(["80", "92"], ["1.15"])
L.append(r"\node[note,anchor=north] at (1.7,-.65) {hausse de 15\,\%};")
L2 = chaine(["60", "42"], ["0.7"])
L += [r"\begin{scope}[yshift=-2.1cm]"] + L2 + [r"\node[note,anchor=north] at (1.7,-.65) {baisse de 30\,\%};", r"\end{scope}"]
FIGURES["pourcentage_coefficient"] = tikz(L)

# Aperçu de la carte (cadre fixe 6 × 3,75 cm, commun aux méthodes).
L = [r"\begin{scope}[local bounding box=F]"] + grille(15, c=.3) + [
    r"\node[anchor=west,text=otGreenDark,font=\fontsize{20}{22}\selectfont\bfseries] at (3.4,-1.5) {15\,\%};",
    r"\end{scope}", r"\pgfresetboundingbox",
    r"\path ($(F.center)+(-3,-1.875)$) rectangle ($(F.center)+(3,1.875)$);"]
FIGURES["carte_pourcentage"] = tikz(L)
