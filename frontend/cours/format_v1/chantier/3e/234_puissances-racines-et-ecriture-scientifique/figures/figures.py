# -*- coding: utf-8 -*-
"""Figures de la notion « Puissances, racines et écriture scientifique » (3e), style des livres.

Compilées par outils/figures_livre.py : axe des ordres de grandeur, carrés et
racines carrées, encadrement d'une racine par zooms. Réponses en vert foncé.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  bande/.style={line width=3.2pt,line cap=butt},
  objet/.style={font=\otRegular\fontsize{9}{11}\selectfont,anchor=south,inner sep=1pt,align=center},
}
"""


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


# ------------------------------------------------------------------ axe des puissances de 10
def axe_puissances(n0, n1, pas, objets, coul="otNavy", titre=None):
    """Axe VERTICAL gradué en puissances de 10 de 10^n0 (bas) à 10^n1 (haut) ; objets : [(exposant, nom)]."""
    Y = lambda n: (n - n0) * pas
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[axe] (0,-.3) -- (0,%s);" % f(Y(n1) + .5))
    for n in range(n0, n1 + 1):
        s.append(r"\draw[grad] (-.08,%s) -- (.08,%s);" % (f(Y(n)), f(Y(n))))
        s.append(r"\node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=east,inner sep=1pt] at (-.15,%s) {$10^{%d}$};" % (f(Y(n)), n))
    for n, nom in objets:
        s.append(r"\fill[%s] (0,%s) circle (2.4pt);" % (coul, f(Y(n))))
        s.append(r"\draw[%s,line width=.4pt] (.1,%s) -- (.4,%s);" % (coul, f(Y(n)), f(Y(n))))
        s.append(r"\node[anchor=west,text=%s,inner sep=1pt] at (.45,%s) {%s};" % (coul, f(Y(n)), nom))
    if titre:
        s.append(r"\node[anchor=south,text=otMuted,font=\otRegular\fontsize{8.5}{10}\selectfont] at (0,%s) {%s};"
                 % (f(Y(n1) + .6), titre))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES = {}
FIGURES["ordres_cours"] = axe_puissances(-8, 8, .5, [
    (-7, "virus"), (-5, "cellule"), (-3, "fourmi"), (0, "humain"),
    (2, "tour Eiffel"), (4, "Everest"), (7, "diamètre de la Terre")], titre="longueurs en mètres")

FIGURES["ex_ordres_enonce"] = axe_puissances(-8, 6, .5, [], titre="longueurs en mètres")
FIGURES["ex_ordres_corrige"] = axe_puissances(-8, 6, .5, [
    (-7, "virus"), (-6, "bactérie"), (-4, "cheveu"), (2, "terrain"),
    (5, "Paris – Lyon")], coul="otGreenDark", titre="longueurs en mètres")


# ------------------------------------------------------------------ carrés : aire et côté
def carre(c, aire, cote, coul_cote="otInk", x=0.0):
    """Carré de côté c (cm de dessin), aire écrite au centre, cote dessous."""
    s = []
    s.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (%s,0) rectangle (%s,%s);" % (f(x), f(x + c), f(c)))
    s.append(r"\node[text=otNavy,fill=otSky,inner sep=1pt] at (%s,%s) {%s};" % (f(x + c / 2), f(c / 2), aire))
    s.append(r"\draw[cote] (%s,-.4) -- (%s,-.4);" % (f(x), f(x + c)))
    s.append(r"\draw[otMuted!70,line width=.4pt] (%s,-.05) -- (%s,-.5) (%s,-.05) -- (%s,-.5);" % (f(x), f(x), f(x + c), f(x + c)))
    s.append(r"\node[coteTexte,text=%s] at (%s,-.4) {%s};" % (coul_cote, f(x + c / 2), cote))
    return "\n".join(s)


_s = [r"\begin{tikzpicture}"]
_s.append(carre(3.0, r"aire $25$ cm²", r"$5$ cm"))
_s.append(carre(4.025, r"aire $45$ cm²", r"$\sqrt{45}$ cm $\approx 6{,}71$ cm", "otGreenDark", x=4.0))
_s.append(r"\end{tikzpicture}")
FIGURES["carre_racine"] = "\n".join(_s)

FIGURES["ex_carre169_enonce"] = "\n".join([r"\begin{tikzpicture}", carre(3.9, r"aire $169$ cm²", r"côté ?"), r"\end{tikzpicture}"])
FIGURES["ex_carre169_corrige"] = "\n".join([r"\begin{tikzpicture}", carre(3.9, r"aire $169$ cm²", r"$\sqrt{169} = 13$ cm", "otGreenDark"), r"\end{tikzpicture}"])
FIGURES["ex_dalle_enonce"] = "\n".join([r"\begin{tikzpicture}", carre(3.6, r"aire $2$ m²", r"côté ?"), r"\end{tikzpicture}"])
FIGURES["ex_dalle_corrige"] = "\n".join([r"\begin{tikzpicture}", carre(3.6, r"aire $2$ m²", r"$\sqrt{2}$ m $\approx 1{,}414$ m", "otGreenDark"), r"\end{tikzpicture}"])

# ------------------------------------------------------------------ encadrement de racine de 37 (zooms)
r37 = 37 ** .5
_s = [r"\begin{tikzpicture}"]
U = 2.0
X1 = lambda v: (v - 5) * U          # ligne 1 : de 5 à 8
_s.append(r"\draw[axe] (-.3,0) -- (%s,0);" % f(X1(8) + .5))
for k in range(5, 9):
    _s.append(r"\draw[grad] (%s,-.08) -- (%s,.08);" % (f(X1(k)), f(X1(k))))
    _s.append(r"\node[gradTexte] at (%s,-.2) {$%d$};" % (f(X1(k)), k))
_s.append(r"\draw[bande,otOrange] (%s,0) -- (%s,0);" % (f(X1(6)), f(X1(7))))
_s.append(r"\fill[otNavy] (%s,0) circle (2.4pt);" % f(X1(r37)))
_s.append(r"\node[anchor=south,text=otNavy] at (%s,.15) {$\sqrt{37}$};" % f(X1(r37)))
_s.append(r"\node[anchor=south,text=otMuted] at (%s,.15) {$6^2 = 36 < 37 < 49 = 7^2$};" % f(X1(7.4)))
Y2, W, x0 = -2.0, 6.0, X1(5)
X2 = lambda v: x0 + (v - 6) * W
_s.append(r"\draw[otOrange,line width=.5pt,dash pattern=on 2.5pt off 1.8pt] (%s,-.55) -- (%s,%s);" % (f(X1(6)), f(X2(6)), f(Y2 + .55)))
_s.append(r"\draw[otOrange,line width=.5pt,dash pattern=on 2.5pt off 1.8pt] (%s,-.55) -- (%s,%s);" % (f(X1(7)), f(X2(7)), f(Y2 + .55)))
_s.append(r"\draw[otMuted,line width=.6pt] (%s,%s) -- (%s,%s);" % (f(X2(6)), f(Y2), f(X2(7)), f(Y2)))
for k in range(11):
    v = 6 + k / 10
    h = .12 if k in (0, 10) else .07
    _s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X2(v)), f(Y2 - h), f(X2(v)), f(Y2 + h)))
    lab = "6" if k == 0 else ("7" if k == 10 else "6{,}%d" % k)
    _s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X2(v)), f(Y2 - .2), lab))
_s.append(r"\draw[bande,otGreen!85] (%s,%s) -- (%s,%s);" % (f(X2(6)), f(Y2), f(X2(6.1)), f(Y2)))
_s.append(r"\fill[otNavy] (%s,%s) circle (2.4pt);" % (f(X2(r37)), f(Y2)))
_s.append(r"\node[anchor=south,text=otNavy] at (%s,%s) {$\sqrt{37}$};" % (f(X2(r37)), f(Y2 + .15)))
_s.append(r"\node[anchor=north,text=otGreenDark] at (%s,%s) {$6{,}0^2 = 36 < 37 < 37{,}21 = 6{,}1^2$, donc $6{,}0 < \sqrt{37} < 6{,}1$};" % (f(X2(6.5)), f(Y2 - .75)))
_s.append(r"\end{tikzpicture}")
FIGURES["encadrement"] = "\n".join(_s)

# ------------------------------------------------------------------ exercice 2138 : carré construit sur la diagonale
_s = [r"\begin{tikzpicture}"]
_s.append(r"\coordinate (A) at (0,0); \coordinate (B) at (3,0); \coordinate (C) at (3,3); \coordinate (D) at (0,3);")
_s.append(r"\coordinate (E) at (6,0); \coordinate (F) at (3,-3);")
_s.append(r"\fill[otGreen!25] (A) -- (C) -- (E) -- (F) -- cycle;")
_s.append(r"\draw[otGreenDark,line width=1pt] (A) -- (C) -- (E) -- (F) -- cycle;")
_s.append(r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;")
_s.append(r"\angledroit{A}{B}{C}")
for p, a in [("A", "west"), ("B", "north west"), ("C", "south"), ("D", "south east"), ("E", "west"), ("F", "north")]:
    _s.append(r"\fill[otNavy] (%s) circle (1.6pt);" % p)
_s.append(r"\node[anchor=east] at (A) {$A$};")
_s.append(r"\node[anchor=north east,xshift=-1pt] at (B) {$B$};")
_s.append(r"\node[anchor=south] at (C) {$C$};")
_s.append(r"\node[anchor=south east] at (D) {$D$};")
_s.append(r"\node[anchor=west] at (E) {$E$};")
_s.append(r"\node[anchor=north] at (F) {$F$};")
_s.append(r"\draw[cote] (-.45,0) -- (-.45,3);")
_s.append(r"\node[coteTexte,anchor=east] at (-.55,1.5) {$5$ cm};")
_s.append(r"\node[text=otNavy] at (1.0,2.0) {$25$ cm²};")
_s.append(r"\node[text=otGreenDark,fill=otGreen!25,inner sep=1pt] at (3,-1.25) {aire $50$ cm²};")
_s.append(r"\node[anchor=south west,text=otGreenDark] at (4.6,1.55) {$CE = AC = \sqrt{50}$ cm};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_double"] = "\n".join(_s)

TOLERE = {
    "carre_racine": "aire écrite au centre du carré, sur son fond bleu pâle : aucun trait sous le texte",
    "ex_carre169_enonce": "aire écrite au centre du carré, sur son fond bleu pâle : aucun trait sous le texte",
    "ex_carre169_corrige": "aire écrite au centre du carré, sur son fond bleu pâle : aucun trait sous le texte",
    "ex_dalle_enonce": "aire écrite au centre du carré, sur son fond bleu pâle : aucun trait sous le texte",
    "ex_dalle_corrige": "aire écrite au centre du carré, sur son fond bleu pâle : aucun trait sous le texte",
    "ex_double": "aires écrites à l’intérieur des carrés, sur leur fond coloré : aucun trait sous le texte",
}
