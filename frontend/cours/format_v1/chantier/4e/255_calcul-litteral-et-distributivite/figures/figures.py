# -*- coding: utf-8 -*-
"""Figures de la notion 255 (4e : calcul littéral et distributivité), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Modèles d'aire (rectangles découpés), programmes de calcul, allumettes,
piscine, carré magique, boîte, rectangle et carré. Éléments de réponse des
corrigés en vert foncé (otGreenDark).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum height=.66cm,inner sep=3.5pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  titreP/.style={text=otNavy,font=\bfseries},
  allum/.style={otOrange!65!black,line width=2.6pt,line cap=round},
  allumO/.style={otOrange,line width=2.6pt,line cap=round},
  allumV/.style={otGreenDark,line width=2.6pt,line cap=round},
  allumV2/.style={otGreen,line width=2.6pt,line cap=round},
  tete/.style={fill=otRed},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  pli/.style={otMuted,line width=.6pt,dash pattern=on 3pt off 2pt},
}
"""

VERT = "otGreenDark"
FILL = {"bleu": "otSky", "orange": "otOrange!16", "vert": "otGreen!16", "mix": "otSky!40!otOrange!14"}


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


# ===================================================================== modèle d'aire
def aires(cols, rows, cellules=None, couleurs=None, cell_col="otInk", col_txt=None, row_txt=None,
          x0=0.0, y0=0.0, cotes_haut=True, cotes_gauche=True, total=None):
    """Grand rectangle découpé.
    cols = [(largeur_cm, étiquette)] de gauche à droite ; rows = [(hauteur_cm, étiquette)] de haut en bas.
    cellules[i][j] : texte de la case (ligne i, colonne j) ou None.
    total = (étiquette_haut, étiquette_gauche) : une seule cote par côté (énoncé non découpé)."""
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
                L.append(r"\node[text=%s] at (%s,%s) {%s};" % (cell_col, f(x + w / 2), f(y - h / 2), cellules[i][j]))
            x += w
        y -= h
    if total:
        th, tg = total
        if th:
            L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 + .04), f(y0 + H + .3), f(x0 + W - .04), f(y0 + H + .3)))
            L.append(r"\node[anchor=south,text=otInk] at (%s,%s) {%s};" % (f(x0 + W / 2), f(y0 + H + .36), th))
        if tg:
            L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 - .3), f(y0 + H - .04), f(x0 - .3), f(y0 + .04)))
            L.append(r"\node[anchor=east,text=otInk] at (%s,%s) {%s};" % (f(x0 - .38), f(y0 + H / 2), tg))
        return L
    if cotes_haut:
        x = x0
        for j, (w, lab) in enumerate(cols):
            col = col_txt[j] if col_txt else "otInk"
            L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x + .04), f(y0 + H + .3), f(x + w - .04), f(y0 + H + .3)))
            L.append(r"\node[anchor=south,text=%s] at (%s,%s) {%s};" % (col, f(x + w / 2), f(y0 + H + .36), lab))
            x += w
    if cotes_gauche:
        y = y0 + H
        for i, (h, lab) in enumerate(rows):
            col = row_txt[i] if row_txt else "otInk"
            L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 - .3), f(y - .04), f(x0 - .3), f(y - h + .04)))
            L.append(r"\node[anchor=east,text=%s] at (%s,%s) {%s};" % (col, f(x0 - .38), f(y - h / 2), lab))
            y -= h
    return L


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


def rect_cote(x0, y0, W, H, fond, haut, cote_v, nom=None):
    """Rectangle non découpé, avec une cote en haut et une cote verticale à gauche."""
    L = [r"\filldraw[fill=%s,draw=otNavy,line width=.8pt] (%s,%s) rectangle (%s,%s);" % (fond, f(x0), f(y0), f(x0 + W), f(y0 + H)),
         r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 + .04), f(y0 + H + .3), f(x0 + W - .04), f(y0 + H + .3)),
         r"\node[anchor=south,text=otInk] at (%s,%s) {%s};" % (f(x0 + W / 2), f(y0 + H + .36), haut),
         r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 - .3), f(y0 + H - .04), f(x0 - .3), f(y0 + .04)),
         r"\node[anchor=east,text=otInk] at (%s,%s) {%s};" % (f(x0 - .38), f(y0 + H / 2), cote_v)]
    if nom:
        L.append(r"\node[text=otNavy,font=\bfseries] at (%s,%s) {%s};" % (f(x0 + W / 2), f(y0 + H / 2), nom))
    return L


QUATRE = [[FILL["bleu"], FILL["orange"]], [FILL["vert"], FILL["mix"]]]
DEUX = [[FILL["bleu"], FILL["orange"]]]
UNI4 = [[FILL["bleu"], FILL["bleu"]], [FILL["bleu"], FILL["bleu"]]]
UNI2 = [[FILL["bleu"], FILL["bleu"]]]

FIGURES = {}

# ---------------------------------------------------------------- cours et fiche
FIGURES["c_simple"] = tikz(aires([(3.4, "$a$"), (2.0, "$b$")], [(1.6, "$k$")],
                                 [["$ka$", "$kb$"]], DEUX))
FIGURES["c_double"] = tikz(aires([(3.2, "$c$"), (1.9, "$d$")], [(2.2, "$a$"), (1.3, "$b$")],
                                 [["$ac$", "$ad$"], ["$bc$", "$bd$"]], QUATRE))


# ===================================================================== programmes de calcul
def programme(etapes, expressions=None, titre=None, x0=0.0, largeur=4.2, nom="p", ecart=.42):
    """Programme vertical : boîtes reliées par des flèches de longueur constante ;
    expressions (en vert) à droite de chaque boîte."""
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
    ["Choisir un nombre", "Ajouter $7$", "Multiplier par $2$", r"Soustraire le double\\du nombre de départ"],
    ["$x$", "$x + 7$", "$2(x + 7)$", "$2(x + 7) - 2x$"], largeur=3.6))

# ---------------------------------------------------------------- 2588 : programmes A et B
ETAPES_A = ["Choisir un nombre", "Ajouter $3$", "Multiplier par $2$", "Soustraire $6$"]
ETAPES_B = ["Choisir un nombre", "Multiplier par $4$", r"Soustraire le nombre\\de départ",
            r"Soustraire encore\\le nombre de départ"]
FIGURES["ex2588_enonce"] = tikz(programme(ETAPES_A, titre="Programme A", nom="a", largeur=3.6, ecart=.62)
                                + programme(ETAPES_B, titre="Programme B", nom="b", x0=4.1, largeur=3.6, ecart=.42))
FIGURES["ex2588_A"] = tikz(programme(ETAPES_A, ["$x$", "$x + 3$", "$2(x + 3)$", "$2(x + 3) - 6$"],
                                     titre="Programme A", nom="a", largeur=3.4))
FIGURES["ex2588_B"] = tikz(programme(ETAPES_B, ["$x$", "$4x$", "$4x - x$", "$4x - x - x$"],
                                     titre="Programme B", nom="b", largeur=3.4))

# ---------------------------------------------------------------- 2595 : tour de magie
ETAPES_M = ["Choisir un nombre entier", "Calculer son carré", r"Retirer le carré\\du nombre qui le précède",
            "Annoncer le résultat"]
FIGURES["ex2595_enonce"] = tikz(programme(ETAPES_M, largeur=4.4))
FIGURES["ex2595_corrige"] = tikz(programme(ETAPES_M, ["$n$", "$n^2$", "$n^2 - (n - 1)^2$", "$2n - 1$"], largeur=4.2))

# ---------------------------------------------------------------- 2599 : affirmation 5
ETAPES_V = ["Choisir un nombre", "Multiplier par $4$", "Ajouter $10$", "Diviser par $2$",
            r"Soustraire le nombre\\de départ"]
FIGURES["ex2599_enonce"] = tikz(programme(ETAPES_V, largeur=4.0))
FIGURES["ex2599_corrige"] = tikz(programme(ETAPES_V, ["$x$", "$4x$", "$4x + 10$", "$2x + 5$", "$x + 5$"],
                                           largeur=3.6))


# ===================================================================== 2582 : allumettes
def allumette(x1, y1, x2, y2, style="allum"):
    """Allumette de (x1,y1) à (x2,y2) ; tête rouge à l'arrivée."""
    return [r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x1), f(y1), f(x2), f(y2)),
            r"\fill[tete] (%s,%s) circle (2.3pt);" % (f(x2), f(y2))]


def rangee(nb, s, x0=0.0, styles=None):
    """nb carrés de côté s ; styles = (première verticale, style du carré k).
    Les allumettes s'arrêtent avant les coins (écart g) : les têtes ne se touchent pas."""
    L = []
    g = .13
    st0 = styles[0] if styles else "allum"
    L += allumette(x0, g, x0, s - g, st0)
    for k in range(nb):
        st = styles[1](k) if styles else "allum"
        a, b = x0 + k * s, x0 + (k + 1) * s
        L += allumette(a + g, s, b - g, s, st)
        L += allumette(a + g, 0, b - g, 0, st)
        L += allumette(b, g, b, s - g, st)
    return L


def allumettes_enonce():
    s = .9
    L = []
    x = 0.0
    for nb, lab in ((1, "1 carré"), (2, "2 carrés"), (3, "3 carrés")):
        L += rangee(nb, s, x)
        L.append(r"\node[petit,anchor=north] at (%s,-.25) {%s};" % (f(x + nb * s / 2), lab))
        x += nb * s + 1.0
    return tikz(L)


def allumettes_corrige():
    s = 1.25
    L = rangee(3, s, 0.0, ("allumO", lambda k: "allumV" if k % 2 == 0 else "allumV2"))
    L.append(r"\node[text=otOrange!85!black,anchor=east] at (-.22,%s) {$1$};" % f(s / 2))
    for k in range(3):
        L.append(r"\node[text=%s,anchor=north] at (%s,-.22) {$3$};" % (VERT, f((k + .5) * s)))
    L.append(r"\node[text=%s,anchor=north] at (%s,-.95) {$1 + 3 \times 3 = 10$ allumettes};" % (VERT, f(1.5 * s)))
    return tikz(L)


FIGURES["ex2582_enonce"] = allumettes_enonce()
FIGURES["ex2582_corrige"] = allumettes_corrige()

# ===================================================================== modèles d'aire des exercices
# 2583 : 3(x + 4)
FIGURES["ex2583_enonce"] = tikz(aires([(3.4, "$x$"), (2.0, "$4$")], [(1.6, "$3$")], couleurs=UNI2))
FIGURES["ex2583_corrige"] = tikz(aires([(3.4, "$x$"), (2.0, "$4$")], [(1.6, "$3$")],
                                       [["$3x$", "$12$"]], DEUX, cell_col=VERT))
# 2584 : 5x + 15 = 5(x + 3)
FIGURES["ex2584_enonce"] = tikz(aires([(3.4, "?"), (1.7, "?")], [(1.6, "$5$")],
                                      [["$5x$", "$15$"]], DEUX))
FIGURES["ex2584_corrige"] = tikz(aires([(3.4, "$x$"), (1.7, "$3$")], [(1.6, "$5$")],
                                       [["$5x$", "$15$"]], DEUX, col_txt=[VERT, VERT]))
# 2586 : (x + 3)(x + 2)
FIGURES["ex2586_enonce"] = tikz(aires([(3.0, "$x$"), (1.6, "$3$")], [(3.0, "$x$"), (1.1, "$2$")], couleurs=UNI4))
FIGURES["ex2586_corrige"] = tikz(aires([(3.0, "$x$"), (1.6, "$3$")], [(3.0, "$x$"), (1.1, "$2$")],
                                       [["$x^2$", "$3x$"], ["$2x$", "$6$"]], QUATRE, cell_col=VERT))
# 2587 : rectangle 2x + 3 sur x
FIGURES["ex2587_enonce"] = tikz(rect_cote(0, 0, 5.0, 1.8, "otSky", "$2x + 3$", "$x$"))
FIGURES["ex2587_corrige"] = tikz(aires([(3.6, "$2x$"), (1.4, "$3$")], [(1.8, "$x$")],
                                       [["$2x^2$", "$3x$"]], DEUX, cell_col=VERT))
# 2589 : (x + 4)(x + 1)
FIGURES["ex2589_corrige"] = tikz(aires([(3.0, "$x$"), (1.9, "$4$")], [(3.0, "$x$"), (0.8, "$1$")],
                                       [["$x^2$", "$4x$"], ["$x$", "$4$"]], QUATRE, cell_col=VERT))
# 2596 : 21 × 32 = (20 + 1)(30 + 2)
FIGURES["ex2596_corrige"] = tikz(aires([(3.6, "$30$"), (1.1, "$2$")], [(2.3, "$20$"), (0.8, "$1$")],
                                       [["$600$", "$40$"], ["$30$", "$2$"]], QUATRE, cell_col=VERT))


# ---------------------------------------------------------------- 2598 : rectangle A et carré B
def deux_figures():
    """Énoncé : rectangle A (x + 5 sur x + 1) et carré B (côté x + 3), à la même échelle."""
    X, u = 1.15, .4                     # x en cm, une unité en cm
    xB = X + 5 * u + 1.45
    S = X + 3 * u
    L = rect_cote(0, 0, X + 5 * u, X + u, "otSky", "$x + 5$", "$x + 1$", "$A$")
    L += rect_cote(xB, 0, S, S, "otOrange!16", "$x + 3$", "$x + 3$", "$B$")
    return tikz(L)


FIGURES["ex2598_enonce"] = deux_figures()


def une_figure(nom, cols, rows, cellules):
    """Corrigé de 2598 : une figure découpée par question (plus lisible sur téléphone)."""
    L = aires(cols, rows, cellules, QUATRE, cell_col=VERT)
    W = sum(w for w, _ in cols)
    L.append(r"\node[titreP,anchor=north] at (%s,-.18) {%s};" % (f(W / 2), nom))
    return tikz(L)


XC, UC = 2.0, .6
FIGURES["ex2598_A"] = une_figure("Rectangle $A$", [(XC, "$x$"), (5 * UC, "$5$")], [(XC, "$x$"), (UC, "$1$")],
                                 [["$x^2$", "$5x$"], ["$x$", "$5$"]])
FIGURES["ex2598_B"] = une_figure("Carré $B$", [(XC, "$x$"), (3 * UC, "$3$")], [(XC, "$x$"), (3 * UC, "$3$")],
                                 [["$x^2$", "$3x$"], ["$3x$", "$9$"]])


# ===================================================================== 2593 : piscine
def piscine(corrige):
    m, Lb, lb = .7, 3.9, 1.95           # margelle, longueur 2x, largeur x (cm)
    W, H = Lb + 2 * m, lb + 2 * m
    L = []
    if corrige:
        for (x, y) in ((0, 0), (m + Lb, 0), (0, m + lb), (m + Lb, m + lb)):
            L.append(r"\filldraw[fill=otOrange!22,draw=otOrange!85!black,line width=.7pt] (%s,%s) rectangle (%s,%s);"
                     % (f(x), f(y), f(x + m), f(y + m)))
            L.append(r"\node[text=otOrange!75!black] at (%s,%s) {$1$};" % (f(x + m / 2), f(y + m / 2)))
        for (x, y, w, h, lab) in ((m, 0, Lb, m, "$2x$"), (m, m + lb, Lb, m, "$2x$"),
                                  (0, m, m, lb, "$x$"), (m + Lb, m, m, lb, "$x$")):
            L.append(r"\filldraw[fill=otGreen!18,draw=otGreenDark,line width=.7pt] (%s,%s) rectangle (%s,%s);"
                     % (f(x), f(y), f(x + w), f(y + h)))
            L.append(r"\node[text=%s] at (%s,%s) {%s};" % (VERT, f(x + w / 2), f(y + h / 2), lab))
        L.append(r"\filldraw[fill=otSky,draw=otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(m), f(m), f(m + Lb), f(m + lb)))
        L.append(r"\node[text=otNavy,align=center] at (%s,%s) {bassin};" % (f(W / 2), f(H / 2 + .3)))
        L.append(r"\node[text=%s,align=center] at (%s,%s) {$6x + 4$};" % (VERT, f(W / 2), f(H / 2 - .3)))
    else:
        L.append(r"\filldraw[fill=otOrange!16,draw=otOrange!85!black,line width=.9pt] (0,0) rectangle (%s,%s);" % (f(W), f(H)))
        L.append(r"\filldraw[fill=otSky,draw=otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(m), f(m), f(m + Lb), f(m + lb)))
        L.append(r"\node[text=otNavy] at (%s,%s) {bassin};" % (f(W / 2), f(H / 2)))
        L.append(r"\node[text=otOrange!75!black] at (%s,%s) {margelle};" % (f(W / 2), f(m / 2)))
    # cotes extérieures : 2x (en haut, sur la longueur du bassin), x (à gauche), 1 m (à droite)
    L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(m), f(H + .3), f(m + Lb), f(H + .3)))
    L.append(r"\draw[guide] (%s,%s) -- (%s,%s);" % (f(m), f(m + lb), f(m), f(H + .42)))
    L.append(r"\draw[guide] (%s,%s) -- (%s,%s);" % (f(m + Lb), f(m + lb), f(m + Lb), f(H + .42)))
    L.append(r"\node[anchor=south,text=otInk] at (%s,%s) {$2x$};" % (f(m + Lb / 2), f(H + .36)))
    L.append(r"\draw[cote] (-.3,%s) -- (-.3,%s);" % (f(m), f(m + lb)))
    L.append(r"\draw[guide] (%s,%s) -- (-.42,%s);" % (f(m), f(m), f(m)))
    L.append(r"\draw[guide] (%s,%s) -- (-.42,%s);" % (f(m), f(m + lb), f(m + lb)))
    L.append(r"\node[anchor=east,text=otInk] at (-.38,%s) {$x$};" % f(m + lb / 2))
    L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(W + .3), f(0), f(W + .3), f(m)))
    L.append(r"\node[anchor=west,text=otInk] at (%s,%s) {$1$ m};" % (f(W + .38), f(m / 2)))
    return tikz(L)


FIGURES["ex2593_enonce"] = piscine(False)
FIGURES["ex2593_corrige"] = piscine(True)


# ===================================================================== 2594 : carré magique
def carre_magique(cases, couleur):
    w, h = 1.65, .95
    L = []
    for i, ligne in enumerate(cases):
        for j, t in enumerate(ligne):
            L.append(r"\filldraw[fill=%s,draw=otNavy,line width=.8pt] (%s,%s) rectangle (%s,%s);"
                     % ("otSky" if (i + j) % 2 == 0 else "white", f(j * w), f(-i * h), f((j + 1) * w), f(-(i + 1) * h)))
            L.append(r"\node[text=%s] at (%s,%s) {%s};" % (couleur, f((j + .5) * w), f(-(i + .5) * h), t))
    L.append(r"\draw[otNavy,line width=1.3pt] (0,0) rectangle (%s,%s);" % (f(3 * w), f(-3 * h)))
    return tikz(L)


FIGURES["ex2594_enonce"] = carre_magique([["$x - 3$", "$x + 2$", "$x + 1$"],
                                          ["$x + 4$", "$x$", "$x - 4$"],
                                          ["$x - 1$", "$x - 2$", "$x + 3$"]], "otInk")
FIGURES["ex2594_corrige"] = carre_magique([["$2$", "$7$", "$6$"], ["$9$", "$5$", "$1$"], ["$4$", "$3$", "$8$"]], VERT)


# ===================================================================== 2597 : boîte sans couvercle
def boite(corrige):
    u = .2                               # 1 cm réel = 0,2 cm
    W, H, c = 30 * u, 20 * u, 3 * u
    L = [r"\filldraw[fill=otSky!60,draw=otNavy,line width=.9pt] (0,0) rectangle (%s,%s);" % (f(W), f(H))]
    for (x, y) in ((0, 0), (W - c, 0), (0, H - c), (W - c, H - c)):
        L.append(r"\filldraw[fill=otOrange!22,draw=otOrange!85!black,line width=.7pt] (%s,%s) rectangle (%s,%s);"
                 % (f(x), f(y), f(x + c), f(y + c)))
    # plis (contour du fond)
    L.append(r"\draw[pli] (%s,%s) rectangle (%s,%s);" % (f(c), f(c), f(W - c), f(H - c)))
    L.append(r"\node[text=otNavy] at (%s,%s) {fond};" % (f(W / 2), f(H / 2)))
    # côté x d'un carré découpé (en haut à gauche)
    L.append(r"\draw[cote] (.03,%s) -- (%s,%s);" % (f(H + .3), f(c - .03), f(H + .3)))
    L.append(r"\node[anchor=south,text=otOrange!75!black] at (%s,%s) {$x$};" % (f(c / 2), f(H + .36)))
    if corrige:
        L.append(r"\draw[cote] (%s,-.32) -- (%s,-.32);" % (f(c + .03), f(W - c - .03)))
        L.append(r"\draw[guide] (%s,%s) -- (%s,-.44);" % (f(c), f(c), f(c)))
        L.append(r"\draw[guide] (%s,%s) -- (%s,-.44);" % (f(W - c), f(c), f(W - c)))
        L.append(r"\node[anchor=north,text=%s] at (%s,-.38) {$30 - 2x$};" % (VERT, f(W / 2)))
        L.append(r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(W + .32), f(c + .03), f(W + .32), f(H - c - .03)))
        L.append(r"\draw[guide] (%s,%s) -- (%s,%s);" % (f(W - c), f(c), f(W + .44), f(c)))
        L.append(r"\draw[guide] (%s,%s) -- (%s,%s);" % (f(W - c), f(H - c), f(W + .44), f(H - c)))
        L.append(r"\node[anchor=west,text=%s] at (%s,%s) {$20 - 2x$};" % (VERT, f(W + .4), f(H / 2)))
    else:
        L.append(r"\draw[cote] (.03,-.32) -- (%s,-.32);" % f(W - .03))
        L.append(r"\node[anchor=north,text=otInk] at (%s,-.38) {$30$ cm};" % f(W / 2))
        L.append(r"\draw[cote] (%s,.03) -- (%s,%s);" % (f(W + .32), f(W + .32), f(H - .03)))
        L.append(r"\node[anchor=west,text=otInk] at (%s,%s) {$20$ cm};" % (f(W + .4), f(H / 2)))
    return tikz(L)


FIGURES["ex2597_enonce"] = boite(False)
FIGURES["ex2597_corrige"] = boite(True)
