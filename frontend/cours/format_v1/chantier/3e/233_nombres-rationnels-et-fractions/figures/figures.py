# -*- coding: utf-8 -*-
"""Figures de la notion « Nombres rationnels et fractions » (3e), style des livres.

Compilées par outils/figures_livre.py. Parts de disques et de barres, droites
graduées, schémas de partage. Éléments de réponse en vert foncé.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  part/.style={draw=otNavy,line width=.7pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
}
"""


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


BLEU = "otNavy!30"
VERT = "otGreen!55"
ORANGE = "otOrange!55"
GRIS = "otMuted!12"


def disque(cx, cy, r, n, k, coul=BLEU):
    """Disque partagé en n secteurs égaux, les k premiers colorés (sens horaire depuis le haut)."""
    s = []
    for i in range(n):
        a0 = 90 - 360 * i / n
        a1 = 90 - 360 * (i + 1) / n
        fill = coul if i < k else "white"
        s.append(r"\filldraw[fill=%s,part] (%s,%s) -- ++(%s:%s) arc[start angle=%s,end angle=%s,radius=%s] -- cycle;"
                 % (fill, f(cx), f(cy), f(a0), f(r), f(a0), f(a1), f(r)))
    return "\n".join(s)


def barre(x, y, w, h, n, couleurs):
    """Barre de n parts égales ; couleurs : liste de n couleurs (None = blanc)."""
    s = []
    d = w / n
    for i in range(n):
        c = couleurs[i] if i < len(couleurs) and couleurs[i] else "white"
        s.append(r"\filldraw[fill=%s,part] (%s,%s) rectangle (%s,%s);" % (c, f(x + i * d), f(y), f(x + (i + 1) * d), f(y + h)))
    return "\n".join(s)


def accolade_dessous(x0, x1, y, texte, coul="otInk", dy=.12):
    return (r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(x1), f(y - dy), f(x0), f(y - dy))
            + "\n" + r"\node[anchor=north,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y - dy - .2), texte))


def accolade_dessus(x0, x1, y, texte, coul="otInk", dy=.12):
    return (r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(x0), f(y + dy), f(x1), f(y + dy))
            + "\n" + r"\node[anchor=south,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y + dy + .2), texte))


def axe(x0, x1, y=0.0, ticks=(), labels=None):
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(x0), f(y), f(x1), f(y))]
    for t in ticks:
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(t), f(y - .08), f(t), f(y + .08)))
    for t, txt in (labels or {}).items():
        s.append(r"\node[gradTexte] at (%s,%s) {%s};" % (f(t), f(y - .2), txt))
    return "\n".join(s)


def point(x, y=0, coul="otNavy"):
    return r"\fill[%s] (%s,%s) circle (2.4pt);" % (coul, f(x), f(y))


FIGURES = {}

# ------------------------------------------------------------------ cours 1
# Trois représentations de 3/4
_s = [r"\begin{tikzpicture}"]
_s.append(disque(1.1, 0, 1, 4, 3))
_s.append(r"\node[anchor=north,text=otNavy] at (1.1,-1.15) {$\dfrac{3}{4}$ du disque};")
_s.append(barre(3.2, -.35, 5.2, .7, 4, [BLEU] * 3))
_s.append(r"\node[anchor=north,text=otNavy] at (5.8,-.5) {$\dfrac{3}{4}$ de la barre};")
U, X0, Y = 3.6, 1.1, -3.1
_tk = [X0 + U * k / 4 for k in range(9)]
_s.append(axe(X0 - .4, X0 + 2 * U + .5, Y, _tk, {X0: "$0$", X0 + U: "$1$", X0 + 2 * U: "$2$"}))
_s.append(point(X0 + .75 * U, Y))
_s.append(r"\node[anchor=south,text=otNavy] at (%s,%s) {$\dfrac{3}{4}$};" % (f(X0 + .75 * U), f(Y + .15)))
_s.append(r"\node[anchor=south west,text=otMuted,font=\otRegular\fontsize{8.5}{10}\selectfont] at (%s,%s) {unité partagée en 4};"
          % (f(X0 + U + .2), f(Y + .2)))
_s.append(r"\end{tikzpicture}")
FIGURES["representations"] = "\n".join(_s)


# ------------------------------------------------------------------ sommes en barres
def somme_barres(lignes, n, w=4.8):
    """lignes : [(étiquette, [couleurs])] ; barres de n parts alignées."""
    s = [r"\begin{tikzpicture}"]
    for i, (lab, cs) in enumerate(lignes):
        y = -1.0 * i
        s.append(barre(0, y, w, .6, n, cs))
        s.append(r"\node[anchor=east,text=otInk] at (-.2,%s) {%s};" % (f(y + .3), lab))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["somme_cours"] = somme_barres([
    (r"$\dfrac{1}{2} = \dfrac{3}{6}$", [BLEU] * 3),
    (r"$\dfrac{1}{3} = \dfrac{2}{6}$", [ORANGE] * 2),
    (r"$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{5}{6}$", [BLEU] * 3 + [ORANGE] * 2),
], 6)

FIGURES["ex_somme"] = somme_barres([
    (r"$\dfrac{2}{3} = \dfrac{4}{6}$", [BLEU] * 4),
    (r"$\dfrac{1}{6}$", [ORANGE]),
    (r"\textcolor{otGreenDark}{$\dfrac{2}{3} + \dfrac{1}{6} = \dfrac{5}{6}$}", [BLEU] * 4 + [ORANGE]),
], 6)

# ------------------------------------------------------------------ exercice 2099 : fractions égales
_s = [r"\begin{tikzpicture}"]
W = 6.0
for i, (lab, n, k) in enumerate([(r"$\dfrac{3}{4}$", 4, 3), (r"$\dfrac{6}{8}$", 8, 6), (r"$\dfrac{9}{12}$", 12, 9)]):
    y = -1.0 * i
    _s.append(barre(0, y, W, .6, n, [VERT] * k))
    _s.append(r"\node[anchor=east,text=otGreenDark] at (-.2,%s) {%s};" % (f(y + .3), lab))
_s.append(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt] (4.5,.85) -- (4.5,-2.25);")
_s.append(r"\node[anchor=north,text=otGreenDark] at (4.5,-2.3) {même longueur coloriée};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_egales"] = "\n".join(_s)


# ------------------------------------------------------------------ exercice 2181 : lire des fractions
def parts(corrige):
    s = [r"\begin{tikzpicture}"]
    yb = -3.6
    s.append(disque(1.1, 0, 1, 8, 3))
    s.append(disque(1.1, yb, 1, 6, 5))
    s.append(barre(3.2, -.35, 5.5, .7, 5, [BLEU] * 2))
    s.append(barre(3.2, yb - .35, 5.5, .7, 12, [BLEU] * 9))
    for lab, (x, y) in {"A": (-.15, .95), "C": (-.15, yb + .95)}.items():
        s.append(r"\node[text=otNavy,font=\bfseries] at (%s,%s) {%s};" % (f(x), f(y), lab))
    for lab, (x, y) in {"B": (3.2, .45), "D": (3.2, yb + .45)}.items():
        s.append(r"\node[anchor=south west,text=otNavy,font=\bfseries,inner sep=1pt] at (%s,%s) {%s};" % (f(x), f(y), lab))
    if corrige:
        for (x, y, t) in [(1.1, -1.15, r"$\dfrac{3}{8}$"), (1.1, yb - 1.15, r"$\dfrac{5}{6}$"),
                          (5.95, -.5, r"$\dfrac{2}{5}$"), (5.95, yb - .5, r"$\dfrac{9}{12} = \dfrac{3}{4}$")]:
            s.append(r"\node[anchor=north,text=otGreenDark] at (%s,%s) {%s};" % (f(x), f(y), t))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_parts_enonce"] = parts(False)
FIGURES["ex_parts_corrige"] = parts(True)


# ------------------------------------------------------------------ exercice 2098 : droite graduée en quarts
def droite_quarts(corrige):
    U, X0 = 3.8, .5
    X = lambda q: X0 + U * q / 4
    s = [r"\begin{tikzpicture}"]
    s.append(axe(X0 - .4, X(8) + .55, 0, [X(k) for k in range(9)], {X(0): "$0$", X(4): "$1$", X(8): "$2$"}))
    pts = [("A", 3, "otNavy"), ("B", 6, "otNavy"), ("C", 7, "otNavy")]
    if corrige:
        pts += [("D", 2, "otGreenDark"), ("E", 5, "otGreenDark")]
    for nom, q, c in pts:
        s.append(point(X(q), 0, c))
        s.append(r"\node[anchor=south,text=%s] at (%s,.14) {$%s$};" % (c, f(X(q)), nom))
        if corrige:
            fr = {3: r"\dfrac{3}{4}", 6: r"\dfrac{6}{4}", 7: r"\dfrac{7}{4}", 2: r"\dfrac{2}{4}", 5: r"\dfrac{5}{4}"}[q]
            s.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.22) {$%s$};" % (f(X(q)), fr))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_droite_enonce"] = droite_quarts(False)
FIGURES["ex_droite_corrige"] = droite_quarts(True)


# ------------------------------------------------------------------ exercice 2183 : 2/3 de 3/4 (carré unité)
def carre_produit(corrige):
    c = 3.6
    s = [r"\begin{tikzpicture}"]
    h = c / 4
    for j in range(4):
        y0 = c - (j + 1) * h
        s.append(r"\fill[%s] (0,%s) rectangle (%s,%s);" % (BLEU if j < 3 else "white", f(y0), f(c), f(y0 + h)))
    if corrige:
        s.append(r"\fill[otGreen!70] (0,%s) rectangle (%s,%s);" % (f(h), f(2 * c / 3), f(c)))
    for j in range(1, 4):
        s.append(r"\draw[otNavy,line width=.6pt] (0,%s) -- (%s,%s);" % (f(j * h), f(c), f(j * h)))
    if corrige:
        for i in (1, 2):
            s.append(r"\draw[otGreenDark,line width=.6pt,dash pattern=on 3pt off 2pt] (%s,0) -- (%s,%s);" % (f(i * c / 3), f(i * c / 3), f(c)))
    s.append(r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%s,%s);" % (f(c), f(c)))
    s.append(r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(c + .15), f(c), f(c + .15), f(h)))
    s.append(r"\node[anchor=west,text=otNavy] at (%s,%s) {$\dfrac{3}{4}$};" % (f(c + .4), f((c + h) / 2)))
    if corrige:
        s.append(r"\draw[accol] (0,%s) -- (%s,%s);" % (f(c + .15), f(2 * c / 3), f(c + .15)))
        s.append(r"\node[anchor=south,text=otGreenDark] at (%s,%s) {$\dfrac{2}{3}$ de la largeur};" % (f(c / 3), f(c + .4)))
        s.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.2) {$6$ cases sur $12$ : $\dfrac{6}{12} = \dfrac{1}{2}$};" % f(c / 2))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_produit_enonce"] = carre_produit(False)
FIGURES["ex_produit_corrige"] = carre_produit(True)

# ------------------------------------------------------------------ cours 3 / exercice 2103 : 3/5 de 40
_s = [r"\begin{tikzpicture}"]
w = 1.5
_s.append(barre(0, 0, 5 * w, .7, 5, [VERT] * 3))
for i in range(5):
    _s.append(r"\node[text=otInk] at (%s,.35) {$8$};" % f(w * i + w / 2))
_s.append(accolade_dessus(0, 5 * w, .7, r"$40$"))
_s.append(accolade_dessous(0, 3 * w, 0, r"$\dfrac{3}{5}$ de $40$ : $3 \times 8 = 24$", "otGreenDark"))
_s.append(r"\end{tikzpicture}")
FIGURES["quantite"] = "\n".join(_s)


# ------------------------------------------------------------------ droites en douzièmes
def corps_douziemes(a, b, U, pts, labels, y=0.0, dx=0.0):
    """Corps TikZ d'une droite de a à b (en douzièmes), U cm par unité, à la hauteur y."""
    X = lambda q: dx + U * q / 12
    s = [axe(X(a) - .35, X(b) + .5, y, [X(k) for k in range(a, b + 1)], labels(X))]
    for q, txt, c, haut in pts:
        s.append(point(X(q), y, c))
        if haut > .3:
            s.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (c, f(X(q)), f(y + .1), f(X(q)), f(y + haut - .05)))
        s.append(r"\node[anchor=south,text=%s] at (%s,%s) {%s};" % (c, f(X(q)), f(y + haut), txt))
    return "\n".join(s), X


def droite_douziemes(a, b, U, pts, labels, extra=None):
    """Droite de a à b (en douzièmes, entiers), U cm par unité."""
    corps, X = corps_douziemes(a, b, U, pts, labels)
    s = [r"\begin{tikzpicture}", corps]
    if extra:
        s.append(extra(X))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_comparer"] = droite_douziemes(
    -12, 0, 6.6,
    [(-10, r"$-\dfrac{5}{6}$", "otNavy", .2), (-9, r"$-\dfrac{3}{4}$", "otNavy", 1.15),
     (-8, r"$-\dfrac{2}{3}$", "otGreenDark", .2), (-7, r"$-\dfrac{7}{12}$", "otNavy", 1.15)],
    lambda X: {X(-12): "$-1$", X(0): "$0$"})

_c1, _ = corps_douziemes(
    -12, 0, 6.6,
    [(-10, r"$-\dfrac{5}{6}$", "otNavy", .2), (-9, r"$-\dfrac{3}{4}$", "otNavy", 1.15)],
    lambda X: {X(-12): "$-1$", X(0): "$0$"}, y=0.0, dx=6.6)
_c2, _ = corps_douziemes(
    0, 12, 6.6,
    [(8, r"$\dfrac{2}{3}$", "otNavy", .2), (9, r"$\dfrac{3}{4}$", "otNavy", 1.15)],
    lambda X: {X(0): "$0$", X(12): "$1$"}, y=-2.6)
FIGURES["comparer_cours"] = "\n".join([r"\begin{tikzpicture}", _c1, _c2, r"\end{tikzpicture}"])


def _enc_extra(X):
    s = []
    for q, t in ((8, r"\dfrac{2}{3}"), (15, r"\dfrac{5}{4}")):
        s.append(r"\draw[otOrange!85!black,fill=white,line width=1pt] (%s,0) circle (2.6pt);" % f(X(q)))
        s.append(r"\node[anchor=south,text=otOrange!85!black] at (%s,.2) {$%s$};" % (f(X(q)), t))
    return "\n".join(s)


FIGURES["ex_encadrement"] = droite_douziemes(
    7, 16, 10.0,
    [(q, "", "otGreenDark", .2) for q in range(9, 15)],
    lambda X: {X(q): r"$\dfrac{%d}{12}$" % q for q in range(7, 17)},
    _enc_extra)

# ------------------------------------------------------------------ exercice 2111 : lecture
_s = [r"\begin{tikzpicture}"]
w = 1.7
_s.append(barre(0, 0, 5 * w, .7, 5, [BLEU, BLEU, VERT, None, None]))
for i in range(5):
    _s.append(r"\node[text=otInk] at (%s,.35) {$54$};" % f(w * i + w / 2))
_s.append(accolade_dessus(0, 5 * w, .7, r"livre : $270$ pages"))
_s.append(accolade_dessous(0, 2 * w, 0, r"lundi\\$\dfrac{2}{5}$ : $108$ pages", "otNavy"))
_s.append(accolade_dessous(2 * w, 3 * w, 0, r"mardi\\$\dfrac{1}{5}$ : $54$"))
_s.append(accolade_dessous(3 * w, 5 * w, 0, r"reste\\$\dfrac{2}{5}$ : $108$ pages", "otGreenDark"))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_lecture"] = "\n".join(_s)

# ------------------------------------------------------------------ exercice 2112 : cuve
_s = [r"\begin{tikzpicture}"]
h = .7
for j in range(8):
    c = BLEU if j < 5 else (VERT if j == 5 else "white")
    _s.append(r"\filldraw[fill=%s,draw=otNavy!50,line width=.4pt] (0,%s) rectangle (2,%s);" % (c, f(j * h), f((j + 1) * h)))
_s.append(r"\draw[otNavy,line width=1pt] (0,%s) -- (0,0) -- (2,0) -- (2,%s);" % (f(8 * h), f(8 * h)))
_s.append(r"\draw[otOrange!85!black,line width=.9pt,dash pattern=on 3pt off 2pt] (-.25,%s) -- (2.25,%s);" % (f(7 * h), f(7 * h)))
_s.append(r"\node[anchor=west,text=otOrange!85!black] at (2.4,%s) {départ : $\dfrac{7}{8}$};" % f(7 * h))
_s.append(r"\node[anchor=west,text=otGreenDark] at (2.4,%s) {$+30$ L $= \dfrac{1}{8}$};" % f(5.5 * h))
_s.append(r"\node[anchor=west,text=otNavy] at (2.4,%s) {après consommation : $\dfrac{5}{8}$};" % f(2.5 * h))
_s.append(r"\node[anchor=east,text=otMuted,font=\otRegular\fontsize{8.5}{10}\selectfont] at (-.3,%s) {$\dfrac{3}{4}$};" % f(6 * h))
_s.append(r"\draw[otMuted,line width=.5pt] (-.25,%s) -- (0,%s);" % (f(6 * h), f(6 * h)))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_cuve"] = "\n".join(_s)

# ------------------------------------------------------------------ exercice 2113 : trajet
_s = [r"\begin{tikzpicture}"]
w = .36
_s.append(barre(0, 0, 24 * w, .6, 24, [BLEU] * 9 + [ORANGE] * 10 + [VERT] * 5))
_s.append(accolade_dessous(0, 9 * w, 0, r"matin\\$\dfrac{9}{24}$", "otNavy"))
_s.append(accolade_dessous(9 * w, 19 * w, 0, r"après-midi\\$\dfrac{10}{24}$", "otOrange!85!black"))
_s.append(accolade_dessous(19 * w, 24 * w, 0, r"soir\\$\dfrac{5}{24}$", "otGreenDark"))
_s.append(accolade_dessus(19 * w, 24 * w, .6, r"$15$ km", "otGreenDark"))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_trajet"] = "\n".join(_s)

# ------------------------------------------------------------------ exercice 2114 : votes
_s = [r"\begin{tikzpicture}"]
w = 1.4
_s.append(barre(0, 0, 6 * w, .7, 6, [GRIS, BLEU, BLEU, BLEU, ORANGE, ORANGE]))
for i in range(6):
    _s.append(r"\node[text=otInk] at (%s,.35) {$5$};" % f(w * i + w / 2))
_s.append(accolade_dessus(w, 6 * w, .7, r"présents : $\dfrac{5}{6}$ de la classe, $25$ élèves"))
_s.append(accolade_dessous(0, w, 0, r"absents\\$5$", "otMuted"))
_s.append(accolade_dessous(w, 4 * w, 0, r"projet A : $\dfrac{3}{5}$ des présents\\$15$ voix", "otNavy"))
_s.append(accolade_dessous(4 * w, 6 * w, 0, r"projet B\\$10$ voix", "otGreenDark"))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_votes"] = "\n".join(_s)

# ------------------------------------------------------------------ exercice 2116 : robinets
_s = [r"\begin{tikzpicture}"]
w = 1.3
_s.append(barre(0, 0, 6 * w, .7, 6, [BLEU, BLEU, ORANGE]))
_s.append(accolade_dessus(0, 6 * w, .7, r"le bassin"))
_s.append(accolade_dessous(0, 2 * w, 0, r"A en 1 h\\$\dfrac{1}{3} = \dfrac{2}{6}$", "otNavy"))
_s.append(accolade_dessous(2 * w, 3 * w, 0, r"B en 1 h\\$\dfrac{1}{6}$", "otOrange!85!black"))
_s.append(r"\node[anchor=north,text=otGreenDark] at (%s,-1.65) {ensemble en 1 h : $\dfrac{3}{6} = \dfrac{1}{2}$ du bassin};" % f(3 * w))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_robinets"] = "\n".join(_s)

TOLERE = {
    "quantite": "nombres écrits au centre des parts coloriées : fond de couleur, aucun trait sous le texte",
    "ex_lecture": "nombres écrits au centre des parts coloriées : fond de couleur, aucun trait sous le texte",
    "ex_votes": "nombres écrits au centre des parts coloriées : fond de couleur, aucun trait sous le texte",
}
