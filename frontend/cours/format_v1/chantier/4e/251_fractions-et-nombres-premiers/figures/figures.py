# -*- coding: utf-8 -*-
"""Figures de la notion 251 (4e : fractions et nombres premiers), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Barres et disques partagés, modèles d'aire, droites graduées, arbres de
décomposition, cribles, frise, schémas de partage. Éléments de réponse en
vert foncé dans les corrigés.
"""
from sympy import isprime

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  part/.style={draw=otNavy,line width=.7pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  noeudC/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=1.05cm,minimum height=.62cm,inner sep=2pt,text=otNavy,font=\bfseries},
  noeudP/.style={draw=otOrange!85!black,fill=otOrange!16,line width=.8pt,rounded corners=3pt,
    minimum width=.7cm,minimum height=.62cm,inner sep=2pt,text=otInk,font=\bfseries},
  noeudV/.style={draw=otGreenDark,fill=otGreen!16,line width=.9pt,rounded corners=3pt,
    minimum width=1.05cm,minimum height=.62cm,inner sep=2pt,text=otGreenDark,font=\bfseries},
  noeudQ/.style={draw=otMuted,dash pattern=on 2.5pt off 1.5pt,fill=white,line width=.7pt,rounded corners=3pt,
    minimum width=1.05cm,minimum height=.62cm,inner sep=2pt,text=otMuted},
  branche/.style={otMuted,line width=.7pt},
}
"""


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


BLEU = "otNavy!28"
VERT = "otGreen!55"
ORANGE = "otOrange!55"
GRIS = "otMuted!22"
VERTF = "otGreenDark"
ORF = "otOrange!85!black"


# ================================================================== outils
def disque(cx, cy, r, couleurs):
    """Disque partagé en len(couleurs) secteurs égaux (sens horaire depuis le haut)."""
    n = len(couleurs)
    s = []
    for i, c in enumerate(couleurs):
        a0 = 90 - 360 * i / n
        a1 = 90 - 360 * (i + 1) / n
        s.append(r"\filldraw[fill=%s,part] (%s,%s) -- ++(%s:%s) arc[start angle=%s,end angle=%s,radius=%s] -- cycle;"
                 % (c or "white", f(cx), f(cy), f(a0), f(r), f(a0), f(a1), f(r)))
    return "\n".join(s)


def barre(x, y, w, h, n, couleurs, trait="part"):
    """Barre de n parts égales ; couleurs : liste (None = blanc)."""
    s = []
    d = w / n
    for i in range(n):
        c = couleurs[i] if i < len(couleurs) and couleurs[i] else "white"
        s.append(r"\filldraw[fill=%s,%s] (%s,%s) rectangle (%s,%s);" % (c, trait, f(x + i * d), f(y), f(x + (i + 1) * d), f(y + h)))
    return "\n".join(s)


def accolade_dessous(x0, x1, y, texte, coul="otInk", dy=.12):
    return (r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(x1), f(y - dy), f(x0), f(y - dy))
            + "\n" + r"\node[anchor=north,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y - dy - .2), texte))


def accolade_dessus(x0, x1, y, texte, coul="otInk", dy=.12):
    return (r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(x0), f(y + dy), f(x1), f(y + dy))
            + "\n" + r"\node[anchor=south,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y + dy + .2), texte))


def accolade_gauche(x, y0, y1, texte, coul="otInk", dx=.15):
    """Accolade verticale à gauche (de y0 en bas à y1 en haut), texte à gauche."""
    return (r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(x - dx), f(y0), f(x - dx), f(y1))
            + "\n" + r"\node[anchor=east,text=%s,align=right] at (%s,%s) {%s};" % (coul, f(x - dx - .22), f((y0 + y1) / 2), texte))


def axe(x0, x1, y=0.0, ticks=(), labels=None):
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(x0), f(y), f(x1), f(y))]
    for t in ticks:
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(t), f(y - .08), f(t), f(y + .08)))
    for t, txt in (labels or {}).items():
        s.append(r"\node[gradTexte] at (%s,%s) {%s};" % (f(t), f(y - .2), txt))
    return "\n".join(s)


def point(x, y=0, coul="otNavy"):
    return r"\fill[%s] (%s,%s) circle (2.4pt);" % (coul, f(x), f(y))


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


FIGURES = {}


# ================================================================== crible
def crible(nmax, mode, c=0.8):
    """mode : 'cours' (premiers sur fond bleu), 'enonce' (sans marquage), 'corrige' (premiers en vert)."""
    L = []
    lignes = (nmax + 9) // 10
    for n in range(1, nmax + 1):
        r, k = divmod(n - 1, 10)
        x0, y0 = k * c, -(r + 1) * c
        if isprime(n) and mode != "enonce":
            fond = "otSky" if mode == "cours" else "otGreen!22"
            L.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (fond, f(x0), f(y0), f(x0 + c), f(y0 + c)))
    L.append(r"\draw[otRule,line width=.6pt] (0,%s) grid[step=%s] (%s,0);" % (f(-lignes * c), f(c), f(10 * c)))
    if mode != "enonce":
        bord = "otNavy" if mode == "cours" else VERTF
        for n in range(1, nmax + 1):
            if isprime(n):
                r, k = divmod(n - 1, 10)
                L.append(r"\draw[%s,line width=.9pt] (%s,%s) rectangle (%s,%s);"
                         % (bord, f(k * c), f(-(r + 1) * c), f((k + 1) * c), f(-r * c)))
    for n in range(1, nmax + 1):
        r, k = divmod(n - 1, 10)
        x, y = (k + .5) * c, -(r + .5) * c
        if mode == "enonce":
            L.append(r"\node[text=otInk,font=\otRegular\fontsize{10}{12}\selectfont] at (%s,%s) {%d};" % (f(x), f(y), n))
        elif isprime(n):
            coul = "otNavy" if mode == "cours" else VERTF
            L.append(r"\node[text=%s,font=\otMedium\bfseries\fontsize{10.5}{12}\selectfont] at (%s,%s) {%d};" % (coul, f(x), f(y), n))
        else:
            L.append(r"\node[text=otMuted!70,font=\otRegular\fontsize{10}{12}\selectfont] at (%s,%s) {%d};" % (f(x), f(y), n))
    if mode != "enonce":
        nb = sum(1 for n in range(2, nmax + 1) if isprime(n))
        fond = "otSky" if mode == "cours" else "otGreen!22"
        bord = "otNavy" if mode == "cours" else VERTF
        yl = -lignes * c - .55
        L.append(r"\fill[%s] (0,%s) rectangle (.4,%s);" % (fond, f(yl - .2), f(yl + .2)))
        L.append(r"\draw[%s,line width=.9pt] (0,%s) rectangle (.4,%s);" % (bord, f(yl - .2), f(yl + .2)))
        coul = "otInk" if mode == "cours" else VERTF
        L.append(r"\node[anchor=west,text=%s] at (.55,%s) {nombre premier : il y en a $%d$ inférieurs à $%d$};"
                 % (coul, f(yl), nb, nmax))
    return tikz(L)


FIGURES["crible_50"] = crible(50, "cours")
FIGURES["crible60_enonce"] = crible(60, "enonce")
FIGURES["crible60_corrige"] = crible(60, "corrige")


# ================================================================== arbres
def arbre(n, etapes, resultat="", connus=None, corrige=False, dx=1.08, dy=.95):
    """etapes = [(p, q), …] : n = p × q, puis q = p' × q'…  Les étapes au-delà de
    `connus` sont masquées (« ? ») dans l'énoncé, en vert dans le corrigé."""
    k = len(etapes)
    connus = k if connus is None else connus
    L = [r"\node[noeudC] (c0) at (%s,0) {%d};" % (f(dx), n)]
    for i, (p, q) in enumerate(etapes, start=1):
        dernier = i == k
        if i <= connus:
            sp, sq = "noeudP", ("noeudP" if dernier else "noeudC")
            tp, tq = str(p), str(q)
        elif corrige:
            # même code que l'arbre (orange = facteur premier) ; réponses en vert
            sp = "noeudP,draw=otGreenDark,text=otGreenDark"
            sq = "noeudP,draw=otGreenDark,text=otGreenDark" if dernier else "noeudC,draw=otGreenDark,text=otGreenDark"
            tp, tq = str(p), str(q)
        else:
            sp, sq = "noeudQ,minimum width=.7cm", ("noeudQ,minimum width=.7cm" if dernier else "noeudQ")
            tp, tq = "?", "?"
        L.append(r"\node[%s] (p%d) at (%s,%s) {%s};" % (sp, i, f((i - 1) * dx), f(-i * dy), tp))
        L.append(r"\node[%s] (c%d) at (%s,%s) {%s};" % (sq, i, f((i + 1) * dx), f(-i * dy), tq))
        L.append(r"\draw[branche] (c%d) -- (p%d); \draw[branche] (c%d) -- (c%d);" % (i - 1, i, i - 1, i))
    L.append(r"\node[noeudP,minimum width=.45cm,minimum height=.38cm] (lg) at (%s,0) {};" % f((k + 1) * dx - 2.6))
    L.append(r"\node[anchor=west,text=otInk] at ($(lg.east)+(.12,0)$) {facteur premier};")
    if resultat:
        coul = VERTF if (corrige or connus == k) else "otInk"
        L.append(r"\node[anchor=west,text=%s,font=\large] at (-.35,%s) {$%s$};" % (coul, f(-k * dy - 1.0), resultat))
    return tikz(L)


FIGURES["arbre_360"] = arbre(360, [(2, 180), (2, 90), (2, 45), (3, 15), (3, 5)],
                             resultat=r"360 = 2^3 \times 3^2 \times 5")
FIGURES["arbre504_enonce"] = arbre(504, [(2, 252), (2, 126), (2, 63), (3, 21), (3, 7)], connus=1)
FIGURES["arbre504_corrige"] = arbre(504, [(2, 252), (2, 126), (2, 63), (3, 21), (3, 7)], connus=1, corrige=True,
                                    resultat=r"504 = 2^3 \times 3^2 \times 7")


# ================================================================== droites graduées
def droite(a, b, den, U, pts, labels, y=0.0, dx=0.0, sous=None):
    """Droite de a/den à b/den ; pts = [(q, texte, couleur, hauteur)] ; sous = {q: texte vert sous l'axe}."""
    X = lambda q: dx + U * (q - a) / den
    s = [axe(X(a) - .35, X(b) + .5, y, [X(k) for k in range(a, b + 1)], labels(X))]
    for q, txt, c, haut in pts:
        s.append(point(X(q), y, c))
        if haut > .3:
            s.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (c, f(X(q)), f(y + .1), f(X(q)), f(y + haut - .05)))
        s.append(r"\node[anchor=south,text=%s] at (%s,%s) {%s};" % (c, f(X(q)), f(y + haut), txt))
    for q, txt in (sous or {}).items():
        s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (VERTF, f(X(q)), f(y - .2), txt))
    return "\n".join(s)


_d1 = droite(-12, 0, 12, 5.4,
             [(-10, r"$-\dfrac{5}{6}$", "otNavy", .2), (-9, r"$-\dfrac{3}{4}$", "otNavy", 1.15)],
             lambda X: {X(-12): "$-1$", X(0): "$0$"})
_d2 = droite(0, 12, 12, 5.4,
             [(8, r"$\dfrac{2}{3}$", "otNavy", .2), (9, r"$\dfrac{3}{4}$", "otNavy", 1.15)],
             lambda X: {X(0): "$0$", X(12): "$1$"}, y=-2.6)
FIGURES["comparer_cours"] = tikz([_d1, _d2])

FIGURES["ranger_corrige"] = tikz([droite(
    12, 20, 24, 23.0,
    [(14, r"$\dfrac{7}{12}$", "otNavy", .2), (15, r"$\dfrac{5}{8}$", "otNavy", .2),
     (16, r"$\dfrac{2}{3}$", "otNavy", .2), (17, r"$\dfrac{17}{24}$", VERTF, .2),
     (18, r"$\dfrac{3}{4}$", "otNavy", .2)],
    lambda X: {X(12): r"$\dfrac{1}{2}$"},
    sous={q: r"$\dfrac{%d}{24}$" % q for q in range(14, 19)})])


# ================================================================== sommes en barres
def somme_barres(lignes, n, w=4.8):
    """lignes : [(étiquette, [couleurs])] ; barres de n parts alignées, étiquettes à gauche."""
    s = []
    for i, (lab, cs) in enumerate(lignes):
        y = -1.0 * i
        s.append(barre(0, y, w, .6, n, cs))
        s.append(r"\node[anchor=east,text=otInk] at (-.2,%s) {%s};" % (f(y + .3), lab))
    return tikz(s)


FIGURES["somme_cours"] = somme_barres([
    (r"$\dfrac{1}{2} = \dfrac{3}{6}$", [BLEU] * 3),
    (r"$\dfrac{1}{3} = \dfrac{2}{6}$", [ORANGE] * 2),
    (r"$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{5}{6}$", [BLEU] * 3 + [ORANGE] * 2),
], 6)

_s = []
_s.append(barre(0, 0, 4.8, .6, 2, [BLEU]))
_s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {$\dfrac{1}{2}$};")
_s.append(barre(0, -1, 4.8, .6, 3, [ORANGE]))
_s.append(r"\node[anchor=east,text=otInk] at (-.2,-.7) {$\dfrac{1}{3}$};")
FIGURES["somme_enonce"] = tikz(_s)

FIGURES["somme_corrige"] = somme_barres([
    (r"$\dfrac{1}{2} = \dfrac{3}{6}$", [BLEU] * 3),
    (r"$\dfrac{1}{3} = \dfrac{2}{6}$", [ORANGE] * 2),
    (r"\textcolor{otGreenDark}{$\dfrac{1}{2} + \dfrac{1}{3} = \dfrac{5}{6}$}", [VERT] * 5),
], 6)


# ================================================================== modèles d'aire
def aire(cols, lignes, kc, kl, c=.9, mode="cours"):
    """Rectangle unité cols × lignes ; kc colonnes en bleu ; kl lignes (du bas) de cette partie :
    hachurées (énoncé), en vert (corrigé, cours)."""
    W, H = cols * c, lignes * c
    s = []
    s.append(r"\fill[%s] (0,0) rectangle (%s,%s);" % (BLEU, f(kc * c), f(H)))
    if mode == "enonce":
        s.append(r"\fill[pattern=north east lines,pattern color=otOrange] (0,0) rectangle (%s,%s);" % (f(kc * c), f(kl * c)))
    else:
        s.append(r"\fill[%s] (0,0) rectangle (%s,%s);" % (VERT, f(kc * c), f(kl * c)))
    for i in range(1, cols):
        s.append(r"\draw[otNavy!45,line width=.5pt] (%s,0) -- (%s,%s);" % (f(i * c), f(i * c), f(H)))
    for j in range(1, lignes):
        s.append(r"\draw[otNavy!45,line width=.5pt] (0,%s) -- (%s,%s);" % (f(j * c), f(W), f(j * c)))
    if mode == "enonce":
        s.append(r"\draw[%s,line width=1pt] (0,0) rectangle (%s,%s);" % (ORF, f(kc * c), f(kl * c)))
    s.append(r"\draw[otNavy,line width=1pt] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
    return s, W, H, c


# cours : 2/3 × 4/5 = 8/15
_s, W, H, c = aire(5, 3, 4, 2)
_s.append(accolade_dessus(0, 4 * c, H, r"$\dfrac{4}{5}$ de la largeur", "otNavy"))
_s.append(accolade_gauche(0, 0, 2 * c, r"$\dfrac{2}{3}$", VERTF))
_s.append(r"\node[anchor=north,text=%s] at (%s,-.2) {$8$ cases sur $15$ : $\dfrac{2}{3} \times \dfrac{4}{5} = \dfrac{8}{15}$};"
          % (VERTF, f(W / 2)))
FIGURES["aire_cours"] = tikz(_s)

# exercice 2510 : 2/3 de 3/4
_s, W, H, c = aire(4, 3, 3, 2, mode="enonce")
_s.append(accolade_dessus(0, 3 * c, H, r"$\dfrac{3}{4}$ du rectangle", "otNavy"))
_s.append(accolade_gauche(0, 0, 2 * c, r"$\dfrac{2}{3}$", ORF))
FIGURES["aire_enonce"] = tikz(_s)

_s, W, H, c = aire(4, 3, 3, 2, mode="corrige")
_s.append(accolade_dessus(0, 3 * c, H, r"$\dfrac{3}{4}$ du rectangle", "otNavy"))
_s.append(accolade_gauche(0, 0, 2 * c, r"$\dfrac{2}{3}$", VERTF))
_s.append(r"\node[anchor=north,text=%s] at (%s,-.2) {$6$ cases sur $12$ : $\dfrac{6}{12} = \dfrac{1}{2}$};" % (VERTF, f(W / 2)))
FIGURES["aire_corrige"] = tikz(_s)


# ================================================================== fraction d'une quantité (cours)
_s = []
w = 1.6
_s.append(barre(0, 0, 4 * w, .7, 4, [VERT] * 3))
for i in range(4):
    _s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.1) {$7$};" % f(w * i + w / 2))
_s.append(accolade_dessus(0, 4 * w, .7, r"la classe : $28$ élèves"))
_s.append(accolade_dessous(0, 3 * w, -.5, r"$\dfrac{3}{4}$ de $28$ : $3 \times 7 = 21$ élèves", VERTF))
FIGURES["quantite_cours"] = tikz(_s)


# ================================================================== 2511 : verres de 1/8 L
_s = []
w = .82
_s.append(barre(0, 0, 8 * w, .7, 8, [VERT] * 6))
_s.append(r"\node[anchor=east,text=otInk] at (-.2,.35) {$1$ L};")
for i in range(6):
    _s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,-.1) {$\dfrac{1}{8}$};" % (VERTF, f(w * i + w / 2)))
_s.append(accolade_dessus(0, 6 * w, .7, r"la bouteille : $\dfrac{3}{4}$ L $= \dfrac{6}{8}$ L", "otNavy"))
_s.append(accolade_dessous(0, 6 * w, -.85, r"$6$ verres de $\dfrac{1}{8}$ L", VERTF))
FIGURES["verres_corrige"] = tikz(_s)


# ================================================================== 2513 : gâteau
_s = []
R = 1.55
cols = [BLEU] * 3 + [ORANGE] * 4 + [GRIS] * 2 + [VERT] * 3
_s.append(disque(0, 0, R, cols))
leg = [(BLEU, r"Léa : $\dfrac{3}{12} = \dfrac{1}{4}$", "otInk"),
       (ORANGE, r"Tom : $\dfrac{4}{12} = \dfrac{1}{3}$", "otInk"),
       (GRIS, r"Inès : $\dfrac{2}{12} = \dfrac{1}{6}$", "otInk"),
       (VERT, r"reste : $\dfrac{3}{12} = \dfrac{1}{4}$", VERTF)]
for i, (cc, t, tc) in enumerate(leg):
    y = 1.3 - .87 * i
    _s.append(r"\filldraw[fill=%s,part] (2.1,%s) rectangle (2.5,%s);" % (cc, f(y - .2), f(y + .2)))
    _s.append(r"\node[anchor=west,text=%s] at (2.65,%s) {%s};" % (tc, f(y), t))
FIGURES["gateau_corrige"] = tikz(_s)


# ================================================================== 2514 : la classe
_s = []
w = 1.6
_s.append(barre(0, 0, 4 * w, .7, 4, [VERT, VERT, BLEU, None]))
for i in range(4):
    _s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.1) {$7$};" % f(w * i + w / 2))
_s.append(r"\node[anchor=east,text=otInk,align=right] at (-.2,.35) {classe :\\$28$ élèves};")
_s.append(accolade_dessus(0, 3 * w, .7, r"demi-pensionnaires : $\dfrac{3}{4}$ de $28 = 21$", "otNavy"))
_s.append(accolade_dessous(0, 2 * w, -.5, r"dessert : $\dfrac{2}{3}$ de $21 = 14$\\soit $\dfrac{1}{2}$ de la classe", VERTF))
_s.append(accolade_dessous(2 * w, 3 * w, -.5, r"sans\\dessert", "otNavy"))
_s.append(accolade_dessous(3 * w, 4 * w, -.5, r"externes", "otMuted"))
FIGURES["classe_corrige"] = tikz(_s)


# ================================================================== 2517 : réservoir
def reservoir(corrige):
    s = []
    L, h = 2.2, .8
    s.append(r"\fill[%s] (0,0) rectangle (%s,%s);" % (BLEU, f(L), f(3 * h)))
    if corrige:
        for j in range(1, 5):
            s.append(r"\draw[%s,line width=.6pt,dash pattern=on 3pt off 2pt] (0,%s) -- (%s,%s);" % (VERTF, f(j * h), f(L), f(j * h)))
        for j in range(5):
            s.append(r"\node[anchor=west,text=%s] at (%s,%s) {$12$ L};" % (VERTF, f(L + .25), f(j * h + h / 2)))
        s.append(r"\node[anchor=south,text=%s] at (%s,%s) {capacité : $5 \times 12 = 60$ L};" % (VERTF, f(L / 2), f(5 * h + .15)))
    else:
        for j in range(1, 5):
            s.append(r"\draw[otNavy,line width=.6pt] (%s,%s) -- (%s,%s);" % (f(L - .25), f(j * h), f(L), f(j * h)))
    s.append(r"\draw[otNavy,line width=1.1pt] (0,%s) -- (0,0) -- (%s,0) -- (%s,%s) -- cycle;" % (f(5 * h), f(L), f(L), f(5 * h)))
    s.append(accolade_gauche(0, 0, 3 * h, r"$\dfrac{3}{5}$ :\\$36$ L", "otNavy"))
    return tikz(s)


FIGURES["reservoir_enonce"] = reservoir(False)
FIGURES["reservoir_corrige"] = reservoir(True)


# ================================================================== 2521 : jardin
def jardin(corrige):
    k = .36
    W, H = 18 * k, 12 * k
    s = []
    if not corrige:
        s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
    else:
        b = W / 8
        zones = ["otOrange!70"] + ["otOrange!28"] * 2 + [BLEU] * 2 + ["otGreen!35"] * 3
        for i, c in enumerate(zones):
            s.append(r"\fill[%s] (%s,0) rectangle (%s,%s);" % (c, f(i * b), f((i + 1) * b), f(H)))
        for i in range(1, 8):
            fort = i in (3, 5)
            s.append(r"\draw[%s,line width=%spt] (%s,0) -- (%s,%s);"
                     % ("otNavy" if fort else "otNavy!40", ".8" if fort else ".4", f(i * b), f(i * b), f(H)))
        s.append(accolade_dessous(0, 3 * b, 0, r"potager\\$\dfrac{3}{8}$\\$81$ m²", VERTF))
        s.append(accolade_dessous(3 * b, 5 * b, 0, r"fleurs\\$\dfrac{1}{4}$\\$54$ m²", VERTF))
        s.append(accolade_dessous(5 * b, 8 * b, 0, r"pelouse\\$\dfrac{3}{8}$\\$81$ m²", VERTF))
        s.append(r"\draw[accol] (0,%s) -- (%s,%s);" % (f(H + .12), f(b), f(H + .12)))
        s.append(r"\node[anchor=south west,text=%s,inner sep=1pt] at (0,%s) {tomates : $\dfrac{1}{8}$ du jardin, $27$ m²};"
                 % (VERTF, f(H + .38)))
    s.append(r"\draw[otNavy,line width=1pt] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
    s.append(r"\draw[cote] (-.35,0) -- (-.35,%s);" % f(H))
    s.append(r"\node[anchor=east,text=otInk] at (-.45,%s) {$12$ m};" % f(H / 2))
    if not corrige:
        s.append(r"\draw[cote] (0,-.35) -- (%s,-.35);" % f(W))
        s.append(r"\node[anchor=north,text=otInk] at (%s,-.45) {$18$ m};" % f(W / 2))
    return tikz(s)


FIGURES["jardin_enonce"] = jardin(False)
FIGURES["jardin_corrige"] = jardin(True)


# ================================================================== 2522 : chameaux
_s = []
pas, gap, r = .39, .36, .16
groupes = [(9, "otNavy!70", r"aîné\\$9$", "otNavy"),
           (6, "otOrange", r"2\textsuperscript{e} fils\\$6$", ORF),
           (2, "otGreen", r"3\textsuperscript{e} fils\\$2$", VERTF)]
x = 0.0
for nb, coul, lab, tc in groupes:
    x0 = x
    for i in range(nb):
        _s.append(r"\fill[%s] (%s,0) circle (%spt);" % (coul, f(x), f(r * 28.35)))
        x += pas
    x1 = x - pas
    _s.append(accolade_dessous(x0 - r, x1 + r, -r, lab, tc, dy=.1))
    x += gap
_s.append(r"\draw[otMuted,line width=1pt,fill=white] (%s,0) circle (%spt);" % (f(x), f(r * 28.35)))
_s.append(r"\node[anchor=south,text=otMuted,align=center] at (%s,%s) {chameau\\du sage};" % (f(x), f(r + .12)))
_s.append(r"\node[anchor=north west,text=%s,align=left] at (%s,-1.75) {$9 + 6 + 2 = 17$ chameaux distribués :\\le sage reprend le sien.};"
          % (VERTF, f(-r)))
FIGURES["chameaux_corrige"] = tikz(_s)


# ================================================================== 2523 : phares
_s = []
sc, T = .11, 72
yA, yB = 1.0, .5
for t in (0, 36, 72):
    _s.append(r"\draw[%s,line width=.8pt,dash pattern=on 2.5pt off 1.8pt] (%s,0) -- (%s,%s);" % (VERTF, f(t * sc), f(t * sc), f(yA + .3)))
_s.append(r"\draw[otMuted,line width=.7pt,-{Stealth[length=2.3mm]}] (0,0) -- (%s,0);" % f(T * sc + .45))
_s.append(r"\node[anchor=west,text=otMuted] at (%s,0) {s};" % f(T * sc + .5))
for t in range(0, T + 1, 6):
    _s.append(r"\draw[otMuted,line width=.5pt] (%s,-.06) -- (%s,.06);" % (f(t * sc), f(t * sc)))
for t in (0, 12, 18, 24, 36, 48, 54, 60, 72):
    if t in (0, 36, 72):
        _s.append(r"\node[anchor=north,text=%s,font=\otMedium\bfseries\fontsize{9.5}{11}\selectfont] at (%s,-.14) {%d};" % (VERTF, f(t * sc), t))
    else:
        _s.append(r"\node[anchor=north,text=otMuted,font=\otRegular\fontsize{9}{11}\selectfont] at (%s,-.14) {%d};" % (f(t * sc), t))
for t in range(0, T + 1, 12):
    _s.append(r"\fill[otNavy] (%s,%s) circle (2.6pt);" % (f(t * sc), f(yA)))
for t in range(0, T + 1, 18):
    _s.append(r"\fill[otOrange] (%s,%s) circle (2.6pt);" % (f(t * sc), f(yB)))
_s.append(r"\fill[otNavy] (.1,2.35) circle (2.6pt);")
_s.append(r"\node[anchor=west,text=otInk] at (.25,2.35) {phare 1 : un éclair toutes les $12$ s};")
_s.append(r"\fill[otOrange] (.1,1.85) circle (2.6pt);")
_s.append(r"\node[anchor=west,text=otInk] at (.25,1.85) {phare 2 : un éclair toutes les $18$ s};")
_s.append(r"\node[anchor=north,text=%s] at (%s,-.62) {éclairs simultanés : toutes les $36$ s};" % (VERTF, f(36 * sc)))
FIGURES["phares_corrige"] = tikz(_s)


# ================================================================== 2525 : robinets
_s = []
w, n, hb = 6.0, 12, .55
d = w / n
lignes = [
    (r"$A$ en $1$ h : $\dfrac{1}{6} = \dfrac{2}{12}$ du bassin", "otNavy", [BLEU] * 2, 0),
    (r"$B$ en $1$ h : $\dfrac{1}{3} = \dfrac{4}{12}$ du bassin", "otNavy", [ORANGE] * 4, 0),
    (r"$A$ et $B$ ensemble : $\dfrac{6}{12} = \dfrac{1}{2}$ du bassin", VERTF, [VERT] * 6, 0),
    (r"avec la vidange : $\dfrac{6}{12} - \dfrac{3}{12} = \dfrac{1}{4}$ du bassin", VERTF, [VERT] * 3, 3),
]
y = 0.0
for lab, tc, cs, hach in lignes:
    _s.append(barre(0, y, w, hb, n, cs))
    if hach:
        k0 = len(cs)
        _s.append(r"\fill[pattern=north east lines,pattern color=otRed] (%s,%s) rectangle (%s,%s);"
                  % (f(k0 * d), f(y), f((k0 + hach) * d), f(y + hb)))
        _s.append(r"\draw[otRed,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(k0 * d), f(y), f((k0 + hach) * d), f(y + hb)))
    _s.append(r"\node[anchor=south west,text=%s,inner sep=1pt] at (0,%s) {%s};" % (tc, f(y + hb + .12), lab))
    y -= 1.75
_s.append(r"\fill[pattern=north east lines,pattern color=otRed] (0,%s) rectangle (.45,%s);" % (f(y + .9), f(y + 1.2)))
_s.append(r"\draw[otRed,line width=.9pt] (0,%s) rectangle (.45,%s);" % (f(y + .9), f(y + 1.2)))
_s.append(r"\node[anchor=west,text=otInk] at (.6,%s) {vidé par $V$ en $1$ h : $\dfrac{1}{4} = \dfrac{3}{12}$};" % f(y + 1.05))
FIGURES["robinets_corrige"] = tikz(_s)


# ================================================================== 2526 : carrelage
def piece(corrige):
    k = 5.6 / 420
    W, H = 420 * k, 300 * k
    s = []
    if corrige:
        d = 60 * k
        s.append(r"\fill[otGreen!14] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
        for i in range(1, 7):
            s.append(r"\draw[%s,line width=.6pt] (%s,0) -- (%s,%s);" % (VERTF, f(i * d), f(i * d), f(H)))
        for j in range(1, 5):
            s.append(r"\draw[%s,line width=.6pt] (0,%s) -- (%s,%s);" % (VERTF, f(j * d), f(W), f(j * d)))
        s.append(r"\fill[otGreen!45] (0,%s) rectangle (%s,%s);" % (f(H - d), f(d), f(H)))
        s.append(r"\draw[%s,line width=.6pt] (0,%s) rectangle (%s,%s);" % (VERTF, f(H - d), f(d), f(H)))
    else:
        s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
    s.append(r"\draw[otNavy,line width=1pt] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
    s.append(r"\draw[cote] (0,-.35) -- (%s,-.35);" % f(W))
    s.append(r"\node[anchor=north,text=otInk] at (%s,-.45) {$4{,}20$ m};" % f(W / 2))
    s.append(r"\draw[cote] (-.35,0) -- (-.35,%s);" % f(H))
    s.append(r"\node[anchor=east,text=otInk] at (-.45,%s) {$3$ m};" % f(H / 2))
    if corrige:
        d = 60 * k
        s.append(r"\draw[cote,%s] (0,%s) -- (%s,%s);" % (VERTF, f(H + .3), f(d), f(H + .3)))
        s.append(r"\node[anchor=south,text=%s] at (%s,%s) {$60$ cm};" % (VERTF, f(d / 2), f(H + .38)))
        s.append(r"\node[anchor=south east,text=%s] at (%s,%s) {$7 \times 5 = 35$ carreaux};" % (VERTF, f(W), f(H + .38)))
    return tikz(s)


FIGURES["piece_enonce"] = piece(False)
FIGURES["piece_corrige"] = piece(True)
