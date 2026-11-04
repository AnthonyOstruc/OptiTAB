# -*- coding: utf-8 -*-
"""Figures de la notion 254 (4e : carrés et racines carrées), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Carrés parfaits en quadrillage, carrés d'aire donnée et leur côté, droites
graduées et encadrements par zooms, carrés construits sur les côtés d'un
triangle (préparation de Pythagore), mosaïques, courbe de chute libre.
Éléments de réponse en vert foncé dans les corrigés.
"""
from math import sqrt, pi

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  bande/.style={line width=3.2pt,line cap=butt},
  zoom/.style={otOrange,line width=.5pt,dash pattern=on 2.5pt off 1.8pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  titre/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,text=otNavy,inner sep=1pt,align=center},
}
"""

VERTF = "otGreenDark"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


def virg(v, k):
    """Nombre décimal écrit à la française pour LaTeX : 4.47 -> 4{,}47."""
    s = ("%." + str(k) + "f") % v
    return s.replace(".", "{,}")


FIGURES = {}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


# ================================================================== carrés en quadrillage
def quadrillage(cotes, u=0.42, gap=0.8, etiquettes=None, coul="otInk", fond="otSky"):
    """Carrés de côté n (en carreaux de u cm), alignés en bas ; étiquettes sous chacun."""
    L, x = [], 0.0
    for i, n in enumerate(cotes):
        c = n * u
        L.append(r"\fill[%s] (%s,0) rectangle (%s,%s);" % (fond, f(x), f(x + c), f(c)))
        for k in range(1, n):
            L.append(r"\draw[otNavy!35,line width=.4pt] (%s,0) -- (%s,%s);" % (f(x + k * u), f(x + k * u), f(c)))
            L.append(r"\draw[otNavy!35,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(k * u), f(x + c), f(k * u)))
        L.append(r"\draw[otNavy,line width=.9pt] (%s,0) rectangle (%s,%s);" % (f(x), f(x + c), f(c)))
        if etiquettes:
            L.append(r"\node[anchor=north,text=%s,align=center] at (%s,-.12) {%s};" % (coul, f(x + c / 2), etiquettes[i]))
        x += c + gap
    return L


FIGURES["quadrillage_cours"] = tikz(quadrillage(
    [1, 2, 3, 4], u=.45, gap=.95,
    etiquettes=[r"$1^2 = 1$", r"$2^2 = 4$", r"$3^2 = 9$", r"$4^2 = 16$"]))

FIGURES["ex2558_enonce"] = tikz(quadrillage(
    [1, 2, 3, 4], u=.45, gap=.95,
    etiquettes=[r"côté $1$", r"côté $2$", r"côté $3$", r"côté $4$"], coul="otMuted"))

FIGURES["ex2558_corrige"] = tikz(quadrillage(
    [1, 2, 3, 4], u=.45, gap=.95,
    etiquettes=[r"$1 \times 1 = 1$", r"$2 \times 2 = 4$", r"$3 \times 3 = 9$", r"$4 \times 4 = 16$"],
    coul=VERTF, fond="otGreen!16"))


# ================================================================== carré d'aire donnée (cote dessous)
def carre(x, c, aire, cote, coul_cote="otInk", fond="otSky", bord="otNavy", titre=None, y=0.0, dessous=False):
    """Carré de côté c (cm de dessin) posé en (x, y) ; aire au centre, cote dessous, titre au-dessus.
    dessous=True : texte de la cote sous la flèche (texte long ou avec un radical, dont la barre
    prolongerait visuellement la flèche)."""
    s = []
    s.append(r"\draw[%s,line width=.9pt,fill=%s] (%s,%s) rectangle (%s,%s);" % (bord, fond, f(x), f(y), f(x + c), f(y + c)))
    if aire:
        s.append(r"\node[text=otNavy,align=center] at (%s,%s) {%s};" % (f(x + c / 2), f(y + c / 2), aire))
    if cote and dessous:
        s.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x), f(y - .3), f(x + c), f(y - .3)))
        s.append(r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
                 % (f(x), f(y - .05), f(x), f(y - .4), f(x + c), f(y - .05), f(x + c), f(y - .4)))
        s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (coul_cote, f(x + c / 2), f(y - .42), cote))
    elif cote:
        s.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x), f(y - .4), f(x + c), f(y - .4)))
        s.append(r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
                 % (f(x), f(y - .05), f(x), f(y - .5), f(x + c), f(y - .05), f(x + c), f(y - .5)))
        s.append(r"\node[coteTexte,text=%s] at (%s,%s) {%s};" % (coul_cote, f(x + c / 2), f(y - .4), cote))
    if titre:
        s.append(r"\node[titre,anchor=south] at (%s,%s) {%s};" % (f(x + c / 2), f(y + c + .12), titre))
    return "\n".join(s)


# cours : aire 25 -> côté 5 ; aire 20 -> côté racine de 20
_k = .62
FIGURES["carres_aire_cours"] = tikz([
    carre(0, 5 * _k, r"aire $25$ cm²", r"$\sqrt{25} = 5$ cm", dessous=True),
    carre(5 * _k + 1.3, sqrt(20) * _k, r"aire $20$ cm²", r"$\sqrt{20}$ cm $\approx 4{,}47$ cm", VERTF, dessous=True),
])

# 2559 : aire 49
FIGURES["ex2559_enonce"] = tikz([carre(0, 3.2, r"aire $49$ cm²", r"côté ?", dessous=True)])
FIGURES["ex2559_corrige"] = tikz([carre(0, 3.2, r"aire $49$ cm²", r"$\sqrt{49} = 7$ cm", VERTF, dessous=True)])

# 2565 : potagers de 196 m² et 200 m²
_k = .2
_x2 = 14 * _k + 1.7
FIGURES["ex2565_enonce"] = tikz([
    carre(0, 14 * _k, r"$196$ m²", r"côté ?", titre="potager de Nadia", dessous=True),
    carre(_x2, sqrt(200) * _k, r"$200$ m²", r"côté ?", titre="potager du voisin", dessous=True),
])
FIGURES["ex2565_corrige"] = tikz([
    carre(0, 14 * _k, r"$196$ m²", r"$14$ m", VERTF, titre="potager de Nadia", dessous=True),
    carre(_x2, sqrt(200) * _k, r"$200$ m²", r"$\sqrt{200}$ m $\approx 14{,}14$ m", VERTF, titre="potager du voisin", dessous=True),
])


# ================================================================== 2560 : trois carrés A, B, C
def trois_carres(corrige):
    k = .33
    donnees = [("A", 8, r"$64$", r"$8$ cm", 0.0),
               ("B", 1.5, r"$2{,}25$", r"$1{,}5$ cm", 3.95),
               ("C", sqrt(30), r"$30$", r"$\sqrt{30}$ cm}\\\textcolor{otGreenDark}{$\approx 5{,}48$ cm", 5.85)]
    L = []
    for nom, cote, aire, rep, xc in donnees:
        c = cote * k
        x0 = xc if nom != "B" else xc - c / 2
        L.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (%s,0) rectangle (%s,%s);" % (f(x0), f(x0 + c), f(c)))
        L.append(r"\node[titre,anchor=south] at (%s,%s) {carré $%s$};" % (f(x0 + c / 2), f(c + .1), nom))
        txt = r"aire %s cm²" % aire
        if corrige:
            txt += r"\\ \textcolor{otGreenDark}{côté %s}" % rep
        L.append(r"\node[anchor=north,text=otInk,align=center] at (%s,-.12) {%s};" % (f(x0 + c / 2), txt))
    return tikz(L)


FIGURES["ex2560_enonce"] = trois_carres(False)
FIGURES["ex2560_corrige"] = trois_carres(True)


# ================================================================== droites graduées
def axe(x0, x1, y=0.0):
    return r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(x0), f(y), f(x1), f(y))


def grad(x, y=0.0, h=.08, texte=None):
    s = r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(x), f(y - h), f(x), f(y + h))
    if texte is not None:
        s += "\n" + r"\node[gradTexte] at (%s,%s) {%s};" % (f(x), f(y - .2), texte)
    return s


def point_haut(x, texte, coul, y=0.0, haut=.15):
    s = [r"\fill[%s] (%s,%s) circle (2.4pt);" % (coul, f(x), f(y))]
    if haut > .3:
        s.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (coul, f(x), f(y + .1), f(x), f(y + haut - .05)))
    s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (coul, f(x), f(y + haut), texte))
    return "\n".join(s)


# 2561 : droite de 0 à 10
def droite_2561(corrige):
    U = .66
    L = [axe(-.3, 10 * U + .5)]
    for k in range(11):
        L.append(grad(k * U, texte="$%d$" % k))
    if corrige:
        for a in (20, 50, 90):
            L.append(point_haut(sqrt(a) * U, r"$\sqrt{%d}$" % a, VERTF))
            L.append(r"\node[anchor=south,text=%s,font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=1pt] at (%s,.62) {$\approx %s$};"
                     % (VERTF, f(sqrt(a) * U), virg(sqrt(a), 2)))
    else:
        L.append(r"\path (0,.95) -- (1,.95);")  # même hauteur que le corrigé
    return tikz(L)


FIGURES["ex2561_enonce"] = droite_2561(False)
FIGURES["ex2561_corrige"] = droite_2561(True)


# cours : encadrement de racine de 20 par zoom
def encadrement_20():
    r20 = sqrt(20)
    U = 1.15
    X1 = lambda v: (v - 2) * U          # ligne 1 : de 2 à 7
    L = [axe(-.3, X1(7) + .5)]
    for k in range(2, 8):
        L.append(grad(X1(k), texte="$%d$" % k))
    L.append(r"\draw[bande,otOrange] (%s,0) -- (%s,0);" % (f(X1(4)), f(X1(5))))
    L.append(point_haut(X1(r20), r"$\sqrt{20}$", "otNavy"))
    Y2, W, x0 = -2.0, 5.75, X1(2)
    X2 = lambda v: x0 + (v - 4) * W
    L.append(r"\draw[zoom] (%s,-.55) -- (%s,%s);" % (f(X1(4)), f(X2(4)), f(Y2 + .55)))
    L.append(r"\draw[zoom] (%s,-.55) -- (%s,%s);" % (f(X1(5)), f(X2(5)), f(Y2 + .55)))
    L.append(r"\draw[otMuted,line width=.6pt] (%s,%s) -- (%s,%s);" % (f(X2(4)), f(Y2), f(X2(5)), f(Y2)))
    for k in range(11):
        v = 4 + k / 10
        h = .12 if k in (0, 10) else .07
        lab = "4" if k == 0 else ("5" if k == 10 else "4{,}%d" % k)
        L.append(grad(X2(v), Y2, h, "$%s$" % lab))
    L.append(r"\draw[bande,otGreen!85] (%s,%s) -- (%s,%s);" % (f(X2(4.4)), f(Y2), f(X2(4.5)), f(Y2)))
    L.append(point_haut(X2(r20), r"$\sqrt{20}$", "otNavy", Y2))
    L.append(r"\node[anchor=north,text=otGreenDark,align=center] at (%s,%s) {$4{,}4^2 = 19{,}36 < 20 < 20{,}25 = 4{,}5^2$\\donc $4{,}4 < \sqrt{20} < 4{,}5$};"
             % (f(X2(4.5)), f(Y2 - .7)))
    return tikz(L)


FIGURES["encadrement_cours"] = encadrement_20()


# 2568 : droite de 2,7 à 3,6 (dixièmes)
def droite_2568():
    U = 7.2
    X = lambda v: (v - 2.7) * U
    L = [axe(-.3, X(3.6) + .5)]
    for k in range(10):
        v = 2.7 + k / 10
        lab = ("%.1f" % v).replace(".", "{,}").replace("{,}0", "")
        L.append(grad(X(v), texte="$%s$" % lab))
    for v in (3.0, 3.2):
        L.append(r"\fill[%s] (%s,0) circle (2.4pt);" % (VERTF, f(X(v))))
    for a, haut in ((8, .15), (10, .15), (12, .15)):
        L.append(point_haut(X(sqrt(a)), r"$\sqrt{%d}$" % a, VERTF, haut=haut))
    L.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.75) {$\sqrt{8} < 3 < \sqrt{10} < 3{,}2 < \sqrt{12}$};" % f(X(3.15)))
    return tikz(L)


FIGURES["ex2568_corrige"] = droite_2568()


# 2569 : encadrements successifs de racine de 2 (trois zooms)
def zooms_racine2():
    r2 = sqrt(2)
    W = 6.8
    niveaux = [(1.0, 0.1, {0: "1", 4: "1{,}4", 5: "1{,}5", 10: "2"}),
               (1.4, 0.01, {0: "1{,}4", 1: "1{,}41", 2: "1{,}42", 10: "1{,}5"}),
               (1.41, 0.001, {0: "1{,}41", 10: "1{,}42"})]
    bandes = [(1.4, 1.5), (1.41, 1.42), (1.414, 1.415)]
    L = []
    for i, (a, pas, labs) in enumerate(niveaux):
        y = -2.1 * i
        X = lambda v, a=a, pas=pas: (v - a) / (10 * pas) * W
        L.append(r"\draw[otMuted,line width=.6pt] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
        for k in range(11):
            h = .12 if k in (0, 10) else .07
            txt = labs[k] if isinstance(labs, list) else labs.get(k)
            L.append(grad(X(a + k * pas), y, h, None if txt is None else "$%s$" % txt))
        b0, b1 = bandes[i]
        L.append(r"\draw[bande,otGreen!85] (%s,%s) -- (%s,%s);" % (f(X(b0)), f(y), f(X(b1)), f(y)))
        L.append(point_haut(X(r2), r"$\sqrt{2}$", "otNavy", y))
        if i == 2:   # graduations voisines : étiquettes écartées de part et d'autre
            L.append(r"\node[gradTexte,anchor=north east] at (%s,%s) {$1{,}414$};" % (f(X(b0) + .1), f(y - .2)))
            L.append(r"\node[gradTexte,anchor=north west] at (%s,%s) {$1{,}415$};" % (f(X(b1) - .1), f(y - .2)))
        if i < 2:
            L.append(r"\draw[zoom] (%s,%s) -- (0,%s);" % (f(X(b0)), f(y - .55), f(y - 2.1 + .9)))
            L.append(r"\draw[zoom] (%s,%s) -- (%s,%s);" % (f(X(b1)), f(y - .55), f(W), f(y - 2.1 + .9)))
        txt = [r"$1{,}4 < \sqrt{2} < 1{,}5$", r"$1{,}41 < \sqrt{2} < 1{,}42$", r"$1{,}414 < \sqrt{2} < 1{,}415$"][i]
        L.append(r"\node[anchor=south east,text=otGreenDark,inner sep=1pt] at (%s,%s) {%s};" % (f(W), f(y + .2), txt))
    return tikz(L)


FIGURES["ex2569_corrige"] = zooms_racine2()


# ================================================================== carrés construits sur les côtés d'un triangle 3-4-5
def pythagore(u=.7):
    A, B, C = (0.0, 0.0), (4 * u, 0.0), (0.0, 3 * u)
    a = 3 * u
    b = 4 * u
    # carré sur [AB] (dessous), sur [AC] (à gauche), sur [BC] (à l'extérieur)
    n = (0.6, 0.8)   # normale unitaire extérieure à [BC]
    h = 5 * u
    B2 = (B[0] + n[0] * h, B[1] + n[1] * h)
    C2 = (C[0] + n[0] * h, C[1] + n[1] * h)
    P = lambda p: "(%s,%s)" % (f(p[0]), f(p[1]))
    L = []
    L.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (0,0) rectangle (%s,%s);" % (f(b), f(-b)))
    L.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (0,0) rectangle (%s,%s);" % (f(-a), f(a)))
    L.append(r"\draw[otGreenDark,line width=1pt,fill=otGreen!18] %s -- %s -- %s -- %s -- cycle;" % (P(B), P(B2), P(C2), P(C)))
    L.append(r"\draw[otNavy,line width=1.1pt,fill=white] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)))
    L.append(r"\coordinate (A) at %s; \coordinate (B) at %s; \coordinate (C) at %s;" % (P(A), P(B), P(C)))
    L.append(r"\angledroit{B}{A}{C}")
    L.append(r"\node[text=otNavy,align=center] at (%s,%s) {aire\\$16$ cm²};" % (f(b / 2), f(-b / 2)))
    L.append(r"\node[text=otNavy,align=center] at (%s,%s) {aire\\$9$ cm²};" % (f(-a / 2), f(a / 2)))
    cx = (B[0] + B2[0] + C[0] + C2[0]) / 4
    cy = (B[1] + B2[1] + C[1] + C2[1]) / 4
    L.append(r"\node[text=otGreenDark,align=center] at (%s,%s) {aire\\$25$ cm²};" % (f(cx), f(cy)))
    # longueurs à l'intérieur du triangle
    L.append(r"\node[text=otInk,inner sep=1pt,anchor=south] at (%s,.07) {$4$ cm};" % f(b * .45))
    L.append(r"\node[text=otInk,inner sep=1pt,anchor=west] at (.1,%s) {$3$ cm};" % f(a * .58))
    L.append(r"\node[text=otInk,inner sep=1pt] at (%s,%s) {$5$ cm};" % (f(b * .40), f(a * .37)))
    return tikz(L)


FIGURES["pythagore"] = pythagore()


# 2575 : énoncé, deux carrés et le grand carré inconnu
def puzzle():
    k = .5
    L = []
    x = 0.0
    for cote, aire in ((3, r"$9$ cm²"), (4, r"$16$ cm²")):
        c = cote * k
        L.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (%s,0) rectangle (%s,%s);" % (f(x), f(x + c), f(c)))
        L.append(r"\node[text=otNavy] at (%s,%s) {%s};" % (f(x + c / 2), f(c / 2), aire))
        x += c
        L.append(r"\node[text=otMuted,font=\Large] at (%s,%s) {%s};" % (f(x + .45), f(1.0), "$+$" if cote == 3 else "$=$"))
        x += .9
    c = 5 * k
    L.append(r"\draw[otOrange!85!black,line width=.9pt,fill=otOrange!14] (%s,0) rectangle (%s,%s);" % (f(x), f(x + c), f(c)))
    L.append(r"\node[text=otInk,align=center] at (%s,%s) {grand\\carré};" % (f(x + c / 2), f(c / 2)))
    L.append(r"\node[anchor=north,text=otMuted] at (%s,-.12) {côté ?};" % f(x + c / 2))
    return tikz(L)


FIGURES["ex2575_enonce"] = puzzle()


# ================================================================== 2566 : rectangle et carré de même aire
def rect_carre(corrige):
    k = .19
    L = []
    w, h = 18 * k, 8 * k
    L.append(r"\draw[otNavy,line width=.9pt,fill=otSky] (0,0) rectangle (%s,%s);" % (f(w), f(h)))
    L.append(r"\node[titre,anchor=south] at (%s,%s) {rectangle};" % (f(w / 2), f(h + .12)))
    if corrige:
        L.append(r"\node[text=otNavy] at (%s,%s) {aire $144$ cm²};" % (f(w / 2), f(h / 2)))
    L.append(r"\draw[cote] (0,-.4) -- (%s,-.4);" % f(w))
    L.append(r"\draw[otMuted!70,line width=.4pt] (0,-.05) -- (0,-.5) (%s,-.05) -- (%s,-.5);" % (f(w), f(w)))
    L.append(r"\node[coteTexte] at (%s,-.4) {$18$ cm};" % f(w / 2))
    L.append(r"\draw[cote] (-.4,0) -- (-.4,%s);" % f(h))
    L.append(r"\draw[otMuted!70,line width=.4pt] (-.05,0) -- (-.5,0) (-.05,%s) -- (-.5,%s);" % (f(h), f(h)))
    L.append(r"\node[coteTexte,anchor=east] at (-.5,%s) {$8$ cm};" % f(h / 2))
    x = w + 1.0
    c = 12 * k
    if corrige:
        L.append(carre(x, c, r"aire\\$144$ cm²", r"$12$ cm", VERTF, fond="otGreen!16", bord=VERTF,
                       titre=r"\textcolor{otGreenDark}{carré de}\\\textcolor{otGreenDark}{même aire}", dessous=True))
    else:
        L.append(carre(x, c, None, r"côté ?", titre=r"carré de\\même aire", fond="white", dessous=True))
        L.append(r"\node[text=otMuted] at (%s,%s) {?};" % (f(x + c / 2), f(c / 2)))
    return tikz(L)


FIGURES["ex2566_enonce"] = rect_carre(False)
FIGURES["ex2566_corrige"] = rect_carre(True)


# ================================================================== 2567 : courbe de chute libre
FIGURES["ex2567_corrige"] = r"""\begin{tikzpicture}
\begin{axis}[otWeb, grid=none, width=6.2cm, height=4.8cm, xmin=0, xmax=5.3, ymin=0, ymax=135,
  xtick={1,2,3,4,5}, ytick={20,40,60,80,100,120},
  xlabel={$t$ (s)}, ylabel={$d$ (m)}]
\addplot[courbe, domain=0:5.1] {4.9*x^2};
\draw[guide] (axis cs:3,0) -- (axis cs:3,44.1) -- (axis cs:0,44.1);
\draw[guide] (axis cs:4.2426,0) -- (axis cs:4.2426,88.2) -- (axis cs:0,88.2);
\fill[otGreenDark] (axis cs:3,44.1) circle (2.4pt);
\fill[otGreenDark] (axis cs:4.2426,88.2) circle (2.4pt);
\node[anchor=south east,text=otGreenDark,inner sep=1pt] at (axis cs:2.92,47) {$(3\,;\,44{,}1)$};
\node[anchor=south east,text=otGreenDark,inner sep=1pt] at (axis cs:4.15,91) {$(4{,}24\,;\,88{,}2)$};
\node[anchor=east,text=otNavy,inner sep=1pt] at (axis cs:3.4,121) {$d = 4{,}9 \times t^2$};
\end{axis}
\end{tikzpicture}"""


# ================================================================== 2570 : carré ABCD et carré BDEF sur la diagonale
def menon(corrige):
    s = .75
    pts = {"A": (0, 0), "B": (4, 0), "C": (4, 4), "D": (0, 4), "E": (4, 8), "F": (8, 4)}
    P = lambda n: "(%s,%s)" % (f(pts[n][0] * s), f(pts[n][1] * s))
    L = []
    if corrige:
        L.append(r"\fill[otGreen!18] %s -- %s -- %s -- %s -- cycle;" % (P("B"), P("D"), P("E"), P("F")))
    L.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P("A"), P("B"), P("D")))
    if not corrige:
        L.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P("B"), P("C"), P("D")))
    L.append(r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle;" % (P("A"), P("B"), P("C"), P("D")))
    L.append(r"\draw[otNavy,line width=.75pt,dash pattern=on 3pt off 2pt] %s -- %s;" % (P("B"), P("D")))
    if corrige:
        L.append(r"\draw[otGreenDark,line width=1.1pt,line join=round] %s -- %s -- %s -- %s -- cycle;" % (P("B"), P("D"), P("E"), P("F")))
        L.append(r"\draw[geoAide] %s -- %s %s -- %s;" % (P("C"), P("E"), P("C"), P("F")))
        for (cx, cy) in ((8 / 3, 8 / 3), (8 / 3, 16 / 3), (16 / 3, 16 / 3), (16 / 3, 8 / 3)):
            L.append(r"\node[text=otGreenDark] at (%s,%s) {$8$ cm²};" % (f(cx * s), f(cy * s)))
        L.append(r"\node[anchor=south,text=otGreenDark] at (%s,%s) {aire de $BDEF$ : $4 \times 8 = 32$ cm²};" % (f(4 * s), f(8 * s + .35)))
    L.append(r"\coordinate (A) at %s; \coordinate (B) at %s; \coordinate (D) at %s;" % (P("A"), P("B"), P("D")))
    L.append(r"\angledroit{B}{A}{D}")
    L.append(r"\draw[cote] (0,-.4) -- (%s,-.4);" % f(4 * s))
    L.append(r"\draw[otMuted!70,line width=.4pt] (0,-.05) -- (0,-.5) (%s,-.05) -- (%s,-.5);" % (f(4 * s), f(4 * s)))
    L.append(r"\node[coteTexte] at (%s,-.4) {$4$ cm};" % f(2 * s))
    L.append(r"\node[anchor=north east,inner sep=1.5pt] at %s {$A$};" % P("A"))
    L.append(r"\node[anchor=north west,inner sep=1.5pt] at %s {$B$};" % P("B"))
    L.append(r"\node[anchor=east,inner sep=2pt] at %s {$D$};" % P("D"))
    if corrige:
        L.append(r"\node[anchor=south west,inner sep=1.5pt] at %s {$C$};" % P("C"))
        L.append(r"\node[anchor=south,inner sep=2pt] at %s {$E$};" % P("E"))
        L.append(r"\node[anchor=west,inner sep=2pt] at %s {$F$};" % P("F"))
        for n in "ABCDEF":
            L.append(r"\fill[otNavy] %s circle (1.5pt);" % P(n))
    else:
        L.append(r"\node[anchor=south west,inner sep=1.5pt] at %s {$C$};" % P("C"))
        for n in "ABCD":
            L.append(r"\fill[otNavy] %s circle (1.5pt);" % P(n))
    return tikz(L)


FIGURES["ex2570_enonce"] = menon(False)
FIGURES["ex2570_corrige"] = menon(True)


# ================================================================== 2572 : terrain et allée
def allee(corrige):
    S, w = 4.2, .42
    L = []
    if corrige:
        cols = ["otGreen!45", "otGreen!22", "otGreen!45", "otGreen!22"]
        rects = [(0, 0, S - w, w), (S - w, 0, S, S - w), (w, S - w, S, S), (0, w, w, S)]
        for c, (x0, y0, x1, y1) in zip(cols, rects):
            L.append(r"\filldraw[fill=%s,draw=otGreenDark,line width=.6pt] (%s,%s) rectangle (%s,%s);" % (c, f(x0), f(y0), f(x1), f(y1)))
    else:
        L.append(r"\fill[otOrange!22] (0,0) rectangle (%s,%s);" % (f(S), f(S)))
    L.append(r"\filldraw[fill=otGreen!10,draw=otNavy,line width=.6pt] (%s,%s) rectangle (%s,%s);" % (f(w), f(w), f(S - w), f(S - w)))
    L.append(r"\draw[otNavy,line width=1pt] (0,0) rectangle (%s,%s);" % (f(S), f(S)))
    if corrige:
        L.append(r"\node[text=otNavy,align=center] at (%s,%s) {pelouse\\$43^2 = 1\,849$ m²};" % (f(S / 2), f(S / 2 + .45)))
        y = S / 2 - .55
        L.append(r"\draw[cote,otGreenDark] (%s,%s) -- (%s,%s);" % (f(w), f(y), f(S - w), f(y)))
        L.append(r"\node[anchor=south,text=otGreenDark,inner sep=1pt] at (%s,%s) {$43$ m};" % (f(S / 2), f(y + .06)))
        L.append(r"\node[anchor=west,text=otGreenDark,align=left] at (%s,%s) {allée : $4$ rectangles\\de $44$ m sur $1$ m\\$4 \times 44 = 176$ m²};" % (f(S + .3), f(S / 2)))
    else:
        L.append(r"\node[text=otNavy] at (%s,%s) {pelouse};" % (f(S / 2), f(S / 2)))
        L.append(r"\draw[otMuted,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(S - w / 2), f(S * .7), f(S + .45), f(S * .7)))
        L.append(r"\node[anchor=west,text=otInk,align=left] at (%s,%s) {allée de $1$ m\\de large};" % (f(S + .5), f(S * .7)))
        L.append(r"\node[titre,anchor=south] at (%s,%s) {terrain carré : aire $2\,025$ m²};" % (f(S / 2), f(S + .12)))
    L.append(r"\draw[cote] (0,-.4) -- (%s,-.4);" % f(S))
    L.append(r"\draw[otMuted!70,line width=.4pt] (0,-.05) -- (0,-.5) (%s,-.05) -- (%s,-.5);" % (f(S), f(S)))
    L.append(r"\node[coteTexte,text=%s] at (%s,-.4) {%s};" % (VERTF if corrige else "otInk", f(S / 2), r"$45$ m" if corrige else r"côté ?"))
    return tikz(L)


FIGURES["ex2572_enonce"] = allee(False)
FIGURES["ex2572_corrige"] = allee(True)


# ================================================================== 2573 : photo 6 cm et photo 12 cm
def photos():
    k = .27
    L = [carre(0, 6 * k, None, r"$6$ cm", titre="photo")]
    L.append(r"\node[text=otNavy,align=center] at (%s,%s) {$36$\\cm²};" % (f(3 * k), f(3 * k)))
    x = 6 * k + 1.1
    c = 12 * k
    L.append(carre(x, c, None, r"$12$ cm", VERTF, fond="otGreen!12", bord=VERTF, titre=r"\textcolor{otGreenDark}{côté doublé}"))
    L.append(r"\draw[otGreenDark,line width=.6pt,dash pattern=on 3pt off 2pt] (%s,0) -- (%s,%s) (%s,%s) -- (%s,%s);"
             % (f(x + c / 2), f(x + c / 2), f(c), f(x), f(c / 2), f(x + c), f(c / 2)))
    for i in (0, 1):
        for j in (0, 1):
            L.append(r"\node[text=otGreenDark,align=center] at (%s,%s) {$36$\\cm²};" % (f(x + c / 4 + i * c / 2), f(c / 4 + j * c / 2)))
    L.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.82) {aire : $4 \times 36 = 144$ cm²};" % f(x + c / 2))
    return tikz(L)


FIGURES["ex2573_corrige"] = photos()


# ================================================================== 2574 : mosaïques
def mosaique(n, x0=0.0, t=.42, couleur=None, legende=None, coul_leg="otMuted"):
    """Mosaïque n × n ; couleur(i, j) -> remplissage (i colonne, j rangée depuis le bas)."""
    L = []
    for i in range(n):
        for j in range(n):
            c = couleur(i, j) if couleur else "otNavy!30"
            L.append(r"\filldraw[fill=%s,draw=white,line width=1.2pt] (%s,%s) rectangle (%s,%s);"
                     % (c, f(x0 + i * t), f(j * t), f(x0 + (i + 1) * t), f((j + 1) * t)))
    if legende:
        L.append(r"\node[anchor=north,text=%s,align=center] at (%s,-.12) {%s};" % (coul_leg, f(x0 + n * t / 2), legende))
    return L


_t = .42
FIGURES["ex2574_enonce"] = tikz(mosaique(4, 0, _t, legende=r"côté $4$ : $16$ carreaux")
                                + mosaique(5, 4 * _t + 1.6, _t, legende=r"côté $5$ : ? carreaux"))

FIGURES["ex2574_corrige_L"] = tikz(mosaique(
    5, 0, .5, couleur=lambda i, j: "otGreen!70" if (i == 4 or j == 4) else "otNavy!30",
    legende=r"$4 + 4 + 1 = 9$ carreaux ajoutés\\$5^2 - 4^2 = 25 - 16 = 9$", coul_leg=VERTF)
    + [r"\node[anchor=west,text=otNavy,align=left] at (2.75,.95) {côté $4$ :\\$16$ carreaux};",
       r"\node[anchor=west,text=otGreenDark,align=left] at (2.75,2.25) {une colonne,\\une rangée\\et le coin};"])

FIGURES["ex2574_corrige_bord"] = tikz(mosaique(
    6, 0, .42, couleur=lambda i, j: "otGreen!70" if (i in (0, 5) or j in (0, 5)) else "otNavy!30",
    legende=r"bord : $6^2 - 4^2 = 36 - 16 = 20$ carreaux\\ou $4 \times 6 - 4 = 20$ carreaux", coul_leg=VERTF))


# ================================================================== 2576 : la pièce carrelée
def piece():
    n, t = 15, .24
    S = n * t
    L = []
    L.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(S), f(S)))
    L.append(r"\fill[otGreen!45] (0,%s) rectangle (%s,%s);" % (f(S - t), f(S), f(S)))
    for k in range(1, n):
        L.append(r"\draw[otNavy!40,line width=.35pt] (%s,0) -- (%s,%s);" % (f(k * t), f(k * t), f(S)))
        L.append(r"\draw[otNavy!40,line width=.35pt] (0,%s) -- (%s,%s);" % (f(k * t), f(S), f(k * t)))
    L.append(r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%s,%s);" % (f(S), f(S)))
    L.append(r"\draw[accol] (0,%s) -- (%s,%s);" % (f(S + .12), f(S), f(S + .12)))
    L.append(r"\node[anchor=south,text=otGreenDark] at (%s,%s) {$15$ carreaux de $30$ cm par rangée};" % (f(S / 2), f(S + .35)))
    L.append(r"\draw[accol] (%s,%s) -- (%s,0);" % (f(S + .12), f(S), f(S + .12)))
    L.append(r"\node[anchor=west,text=otGreenDark,align=left] at (%s,%s) {$15$ rangées\\$15^2 = 225$\\carreaux};" % (f(S + .4), f(S / 2)))
    L.append(r"\draw[cote] (0,-.4) -- (%s,-.4);" % f(S))
    L.append(r"\draw[otMuted!70,line width=.4pt] (0,-.05) -- (0,-.5) (%s,-.05) -- (%s,-.5);" % (f(S), f(S)))
    L.append(r"\node[coteTexte] at (%s,-.4) {$4{,}5$ m};" % f(S / 2))
    return tikz(L)


FIGURES["ex2576_corrige"] = piece()


# ================================================================== 2578 : les pizzas
def pizzas():
    k = .08
    R1, R2 = 15 * k, 10 * k
    L = []

    def disque(cx, r, coul, fond, legende):
        s = [r"\draw[%s,line width=1pt,fill=%s] (%s,%s) circle (%s);" % (coul, fond, f(cx), f(R1), f(r))]
        s.append(r"\draw[%s,line width=.6pt,dash pattern=on 3pt off 2pt] (%s,%s) -- (%s,%s);" % (coul, f(cx - r), f(R1), f(cx + r), f(R1)))
        s.append(r"\node[anchor=north,text=otInk] at (%s,%s) {%s};" % (f(cx), f(R1 - r - .12), legende))
        return s

    c1 = R1
    L += disque(c1, R1, "otOrange!85!black", "otOrange!16", r"diamètre $30$ cm")
    L.append(r"\node[titre,anchor=south] at (%s,%s) {une grande : $14$ €};" % (f(c1), f(2 * R1 + .15)))
    c2 = 2 * R1 + .9 + R2
    c3 = c2 + 2 * R2 + .5
    L += disque(c2, R2, "otNavy", "otSky", r"$20$ cm")
    L += disque(c3, R2, "otNavy", "otSky", r"$20$ cm")
    L.append(r"\node[titre,anchor=south] at (%s,%s) {deux moyennes\\$9$ € chacune};" % (f((c2 + c3) / 2), f(2 * R1 + .15)))
    return tikz(L)


FIGURES["ex2578_enonce"] = pizzas()
