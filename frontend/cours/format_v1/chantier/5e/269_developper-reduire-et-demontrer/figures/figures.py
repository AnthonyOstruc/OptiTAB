# -*- coding: utf-8 -*-
"""Figures de la notion 269 (5e : développer, réduire et démontrer), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Modèles d'aire (rectangles découpés) pour la distributivité simple, quadrillage
compté de deux façons, barres pour réduire, triangle (périmètre), programmes de
calcul en schéma, preuve « en barres » de la somme de trois entiers consécutifs.
Convention : énoncé = figure sans la réponse ; corrigé = éléments de réponse en
vert foncé (otGreenDark).
Fonctions aires() et programme() reprises de la notion 4e 255 (même style).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum height=.66cm,inner sep=3.5pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  titreP/.style={text=otNavy,font=\bfseries},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  carreau/.style={draw=otNavy,line width=.6pt},
}
"""

VERT = "otGreenDark"
FILL = {"bleu": "otSky", "orange": "otOrange!16", "vert": "otGreen!16"}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


# ===================================================================== modèle d'aire
def aires(cols, rows, cellules=None, couleurs=None, cell_col="otInk", col_txt=None, row_txt=None,
          x0=0.0, y0=0.0, cell_font=""):
    """Grand rectangle découpé.
    cols = [(largeur_cm, étiquette)] de gauche à droite ; rows = [(hauteur_cm, étiquette)] de haut en bas.
    cellules[i][j] : texte de la case (ligne i, colonne j) ou None.
    col_txt / row_txt : couleur des cotes (vert dans un corrigé)."""
    W = sum(w for w, _ in cols)
    H = sum(h for h, _ in rows)
    L = []
    y = y0 + H
    for i, (h, _) in enumerate(rows):
        x = x0
        for j, (w, _) in enumerate(cols):
            c = couleurs[i][j] if couleurs else "otSky"
            L.append(r"\filldraw[fill=%s,draw=otNavy,line width=.8pt] (%s,%s) rectangle (%s,%s);"
                     % (c, f(x), f(y - h), f(x + w), f(y)))
            if cellules and cellules[i][j]:
                L.append(r"\node[text=%s%s] at (%s,%s) {%s};"
                         % (cell_col, cell_font, f(x + w / 2), f(y - h / 2), cellules[i][j]))
            x += w
        y -= h
    x = x0
    for j, (w, lab) in enumerate(cols):
        col = col_txt[j] if col_txt else "otInk"
        L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x + .04), f(y0 + H + .3), f(x + w - .04), f(y0 + H + .3)))
        L.append(r"\node[anchor=south,text=%s] at (%s,%s) {%s};" % (col, f(x + w / 2), f(y0 + H + .36), lab))
        x += w
    y = y0 + H
    for i, (h, lab) in enumerate(rows):
        col = row_txt[i] if row_txt else "otInk"
        L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 - .3), f(y - .04), f(x0 - .3), f(y - h + .04)))
        L.append(r"\node[anchor=east,text=%s] at (%s,%s) {%s};" % (col, f(x0 - .38), f(y - h / 2), lab))
        y -= h
    return L


DEUX = [[FILL["bleu"], FILL["orange"]]]
TROIS = [[FILL["bleu"], FILL["bleu"], FILL["orange"]]]

FIGURES = {}

# ---------------------------------------------------------------- cours et fiche
FIGURES["c_kab"] = tikz(aires([(3.4, "$a$"), (2.2, "$b$")], [(1.6, "$k$")],
                              [[r"$k \times a$", r"$k \times b$"]], DEUX))
FIGURES["c_exemple"] = tikz(aires([(3.4, "$x$"), (2.4, "$5$")], [(1.5, "$3$")],
                                  [["$3x$", "$15$"]], DEUX, cell_col=VERT))


def barres():
    """3x + 5x = 8x : huit barres de longueur x, trois bleues puis cinq orange."""
    w, h = .82, .62
    L = []
    for k in range(8):
        c = FILL["bleu"] if k < 3 else FILL["orange"]
        L.append(r"\filldraw[fill=%s,draw=otNavy,line width=.8pt] (%s,0) rectangle (%s,%s);" % (c, f(k * w), f((k + 1) * w), f(h)))
        L.append(r"\node[text=otInk] at (%s,%s) {$x$};" % (f(k * w + w / 2), f(h / 2)))
    # accolades sous les deux groupes, cote au-dessus du total
    L.append(r"\draw[otMuted,line width=.7pt,decorate,decoration={brace,amplitude=5pt,mirror}] (.04,-.14) -- (%s,-.14);" % f(3 * w - .04))
    L.append(r"\draw[otMuted,line width=.7pt,decorate,decoration={brace,amplitude=5pt,mirror}] (%s,-.14) -- (%s,-.14);" % (f(3 * w + .04), f(8 * w - .04)))
    L.append(r"\node[anchor=north,text=otInk] at (%s,-.38) {$3x$};" % f(1.5 * w))
    L.append(r"\node[anchor=north,text=otInk] at (%s,-.38) {$5x$};" % f(5.5 * w))
    L.append(r"\draw[cote] (.04,%s) -- (%s,%s);" % (f(h + .3), f(8 * w - .04), f(h + .3)))
    L.append(r"\node[anchor=south,text=%s] at (%s,%s) {$8x$};" % (VERT, f(4 * w), f(h + .36)))
    return tikz(L)


FIGURES["c_barres"] = barres()


# ===================================================================== programmes de calcul
def programme(etapes, expressions=None, titre=None, x0=0.0, largeur=4.2, nom="p", ecart=.42):
    """Programme vertical : boîtes reliées par des flèches ; expressions (en vert) à droite."""
    L = []
    for k, e in enumerate(etapes):
        if k == 0:
            L.append(r"\node[boite,minimum width=%scm] (%s0) at (%s,0) {%s};" % (f(largeur), nom, f(x0), e))
        else:
            L.append(r"\node[boite,minimum width=%scm,below=%scm of %s%d] (%s%d) {%s};"
                     % (f(largeur), f(ecart), nom, k - 1, nom, k, e))
            L.append(r"\draw[fleche] (%s%d.south) -- (%s%d.north);" % (nom, k - 1, nom, k))
        if expressions and expressions[k]:
            L.append(r"\node[anchor=west,text=%s] at ($(%s%d.east)+(.3,0)$) {%s};" % (VERT, nom, k, expressions[k]))
    if titre:
        L.append(r"\node[titreP,anchor=south] at ($(%s0.north)+(0,.12)$) {%s};" % (nom, titre))
    return L


FIGURES["c_programme"] = tikz(programme(
    ["Choisir un nombre", "Ajouter $5$", "Multiplier par $3$", "Soustraire $15$"],
    ["$x$", "$x + 5$", "$3(x + 5)$", "$3(x + 5) - 15$"], largeur=3.6))

# ---------------------------------------------------------------- 2893 : programmes A et B
ETAPES_A = ["Choisir un nombre", "Multiplier par $3$", "Ajouter $4$", "Multiplier par $2$"]
ETAPES_B = ["Choisir un nombre", "Ajouter $1$", "Multiplier par $6$", "Ajouter $2$"]
FIGURES["ex2893_enonce"] = tikz(programme(ETAPES_A, titre="Programme A", nom="a", largeur=3.5)
                                + programme(ETAPES_B, titre="Programme B", nom="b", x0=4.2, largeur=3.5))
FIGURES["ex2893_A"] = tikz(programme(ETAPES_A, ["$x$", "$3x$", "$3x + 4$", "$2(3x + 4)$"],
                                     titre="Programme A", nom="a", largeur=3.5))
FIGURES["ex2893_B"] = tikz(programme(ETAPES_B, ["$x$", "$x + 1$", "$6(x + 1)$", "$6(x + 1) + 2$"],
                                     titre="Programme B", nom="b", largeur=3.5))


# ===================================================================== 2875 : quadrillage compté de deux façons
def quadrillage(corrige=False):
    """4 rangées de 6 carreaux bleus et 3 carreaux orange (carreaux de 0,5 cm)."""
    s, n_r, n_b, n_o = .5, 4, 6, 3
    L = []
    for i in range(n_r):
        for j in range(n_b + n_o):
            c = FILL["bleu"] if j < n_b else FILL["orange"]
            L.append(r"\filldraw[fill=%s,carreau] (%s,%s) rectangle (%s,%s);" % (c, f(j * s), f(i * s), f((j + 1) * s), f((i + 1) * s)))
    L.append(r"\draw[otNavy,line width=1.6pt] (%s,0) -- (%s,%s);" % (f(n_b * s), f(n_b * s), f(n_r * s)))
    L.append(r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%s,%s);" % (f((n_b + n_o) * s), f(n_r * s)))
    if corrige:
        L.append(r"\node[anchor=north,text=%s] at (%s,-.18) {$4 \times 6 = 24$};" % (VERT, f(n_b * s / 2)))
        L.append(r"\node[anchor=north,text=%s] at (%s,-.18) {$4 \times 3 = 12$};" % (VERT, f(n_b * s + n_o * s / 2 + .25)))
        L.append(r"\draw[cote] (.04,%s) -- (%s,%s);" % (f(n_r * s + .3), f((n_b + n_o) * s - .04), f(n_r * s + .3)))
        L.append(r"\node[anchor=south,text=%s] at (%s,%s) {$6 + 3 = 9$ carreaux};" % (VERT, f((n_b + n_o) * s / 2), f(n_r * s + .36)))
        L.append(r"\draw[cote] (-.3,%s) -- (-.3,.04);" % f(n_r * s - .04))
        L.append(r"\node[anchor=east,text=%s] at (-.38,%s) {$4$};" % (VERT, f(n_r * s / 2)))
    return tikz(L)


FIGURES["ex2875_enonce"] = quadrillage(False)
FIGURES["ex2875_corrige"] = quadrillage(True)


# ===================================================================== 2877 : triangle (périmètre)
def triangle(corrige=False):
    A, B, C = (0, 0), (5.2, 0), (1.5, 2.6)
    col = VERT if corrige else "otInk"
    L = [r"\filldraw[fill=otSky,draw=otNavy,line width=.9pt,line join=round] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
         % (A + B + C)]
    L.append(r"\node[anchor=north,text=%s] at (2.6,-.12) {$2x$};" % col)
    L.append(r"\node[anchor=south east,text=%s] at (.68,1.36) {$x$};" % col)
    L.append(r"\node[anchor=south west,text=%s] at (3.42,1.36) {$x + 3$};" % col)
    if corrige:
        L.append(r"\node[anchor=north,text=%s] at (2.6,-.72) {$P = x + 2x + x + 3 = 4x + 3$};" % VERT)
    return tikz(L)


FIGURES["ex2877_enonce"] = triangle(False)
FIGURES["ex2877_corrige"] = triangle(True)

# ===================================================================== modèles d'aire des exercices
# 2873 : 4(x + 3)
FIGURES["ex2873_enonce"] = tikz(aires([(3.6, "$x$"), (2.2, "$3$")], [(1.6, "$4$")], couleurs=DEUX))
FIGURES["ex2873_corrige"] = tikz(aires([(3.6, "$x$"), (2.2, "$3$")], [(1.6, "$4$")],
                                       [["$4x$", "$12$"]], DEUX, cell_col=VERT))
# 2882 : 6x + 18 = 6(x + 3)
FIGURES["ex2882_enonce"] = tikz(aires([(3.6, "?"), (2.0, "?")], [(1.6, "$6$")],
                                      [["$6x$", "$18$"]], DEUX))
FIGURES["ex2882_corrige"] = tikz(aires([(3.6, "$x$"), (2.0, "$3$")], [(1.6, "$6$")],
                                       [["$6x$", "$18$"]], DEUX, col_txt=[VERT, VERT]))
# 2881 : 7 × 102 = 7 × 100 + 7 × 2 et 37 × 6 + 37 × 4 = 37 × 10
FIGURES["ex2881_102"] = tikz(aires([(4.6, "$100$"), (1.1, "$2$")], [(1.5, "$7$")],
                                   [["$700$", "$14$"]], DEUX, cell_col=VERT))
FIGURES["ex2881_37"] = tikz(aires([(3.3, "$6$"), (2.2, "$4$")], [(1.5, "$37$")],
                                  [[r"$37 \times 6$", r"$37 \times 4$"]], DEUX)
                            + [r"\draw[cote] (.04,-.3) -- (5.46,-.3);",
                               r"\node[anchor=north,text=%s] at (2.75,-.36) {$6 + 4 = 10$};" % VERT])
# 2888 : jardin 5(2x + 3)
FIGURES["ex2888_enonce"] = tikz(aires([(2.6, "$x$"), (2.6, "$x$"), (1.8, "$3$")], [(1.7, "$5$")],
                                      [["A", "B", "C"]], TROIS, cell_col="otNavy", cell_font=r",font=\bfseries"))
FIGURES["ex2888_corrige"] = tikz(aires([(2.6, "$x$"), (2.6, "$x$"), (1.8, "$3$")], [(1.7, "$5$")],
                                       [["$5x$", "$5x$", "$15$"]], TROIS, cell_col=VERT))


# ===================================================================== 2887 : trois entiers consécutifs
def consecutifs():
    """Avant : barres n, n + 1, n + 2 ; après : on déplace un carré unité (vert) -> trois fois n + 1."""
    w, hn, u, gap = .74, 1.5, .4, .3
    L = []

    def barre(x, nb_unites, vert_haut=False, vert_ajout=False, lab=""):
        L.append(r"\filldraw[fill=otSky,draw=otNavy,line width=.8pt] (%s,0) rectangle (%s,%s);" % (f(x), f(x + w), f(hn)))
        L.append(r"\node[text=otInk] at (%s,%s) {$n$};" % (f(x + w / 2), f(hn / 2)))
        for k in range(nb_unites):
            vert = (vert_haut and k == nb_unites - 1) or (vert_ajout and k == nb_unites - 1)
            fill = "otGreen!35" if vert else FILL["orange"]
            draw = VERT if vert else "otNavy"
            y = hn + k * u
            L.append(r"\filldraw[fill=%s,draw=%s,line width=.8pt] (%s,%s) rectangle (%s,%s);"
                     % (fill, draw, f(x + (w - u) / 2), f(y), f(x + (w + u) / 2), f(y + u)))
        L.append(r"\node[anchor=north,text=otInk] at (%s,-.12) {%s};" % (f(x + w / 2), lab))

    barre(0, 0, lab="$n$")
    barre(w + gap, 1, lab="$n + 1$")
    barre(2 * (w + gap), 2, vert_haut=True, lab="$n + 2$")
    x1 = 3 * w + 2 * gap
    L.append(r"\draw[fleche] (%s,%s) -- (%s,%s);" % (f(x1 + .3), f(hn / 2), f(x1 + 1.0), f(hn / 2)))
    xd = x1 + 1.3
    barre(xd, 1, vert_ajout=True, lab="$n + 1$")
    barre(xd + w + gap, 1, lab="$n + 1$")
    barre(xd + 2 * (w + gap), 1, lab="$n + 1$")
    ytitre = hn + 2 * u + .15
    L.append(r"\node[titreP,anchor=south] at (%s,%s) {Avant};" % (f(x1 / 2), f(ytitre)))
    L.append(r"\node[titreP,anchor=south] at (%s,%s) {Après};" % (f(xd + x1 / 2), f(ytitre)))
    return tikz(L)


FIGURES["ex2887_corrige"] = consecutifs()
