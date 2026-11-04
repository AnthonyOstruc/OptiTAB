# -*- coding: utf-8 -*-
"""Figures de la notion 236 (3e : calcul littéral), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=3.3cm,minimum height=.62cm,inner sep=3pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
}
"""

COULEURS = ["otSky", "otGreen!16", "otOrange!16", "otSky!60!otGreen!20"]


def f(x):
    """Nombre décimal pour TikZ (point décimal, 3 chiffres)."""
    return f"{x:.3f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------ rectangles d'aires
def aires(cols, rows, cellules=None, couleurs=None, cell_col="otInk"):
    """Grand rectangle découpé : cols = [(largeur_cm, étiquette)], rows = [(hauteur_cm, étiquette)]
    (de haut en bas). cellules[i][j] = texte de la case (ligne i, colonne j) ou None."""
    W = sum(w for w, _ in cols)
    H = sum(h for h, _ in rows)
    L = [r"\begin{tikzpicture}"]
    y = H
    for i, (h, _) in enumerate(rows):
        x = 0.0
        for j, (w, _) in enumerate(cols):
            c = couleurs[i][j] if couleurs else COULEURS[(i + j) % 2]
            L.append(rf"\filldraw[fill={c},draw=otNavy,line width=.8pt] ({f(x)},{f(y-h)}) rectangle ({f(x+w)},{f(y)});")
            if cellules and cellules[i][j]:
                L.append(rf"\node[text={cell_col}] at ({f(x+w/2)},{f(y-h/2)}) {{{cellules[i][j]}}};")
            x += w
        y -= h
    # cotes horizontales (au-dessus)
    x = 0.0
    for (w, lab) in cols:
        L.append(rf"\draw[cote] ({f(x+0.04)},{f(H+0.3)}) -- ({f(x+w-0.04)},{f(H+0.3)});")
        L.append(rf"\node[anchor=south,text=otInk] at ({f(x+w/2)},{f(H+0.36)}) {{{lab}}};")
        x += w
    # cotes verticales (à gauche)
    y = H
    for (h, lab) in rows:
        L.append(rf"\draw[cote] (-0.3,{f(y-0.04)}) -- (-0.3,{f(y-h+0.04)});")
        L.append(rf"\node[anchor=east,text=otInk] at (-0.38,{f(y-h/2)}) {{{lab}}};")
        y -= h
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ programmes de calcul
def programme(titre, etapes, expressions=None, x0=0.0):
    """Programme vertical : boîtes reliées par des flèches ; expressions (en vert) à droite."""
    L = []
    L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(x0)},0.15) {{{titre}}};")
    dy = 1.05
    for k, e in enumerate(etapes):
        L.append(rf"\node[boite] (b{titre[-1]}{k}) at ({f(x0)},{f(-k*dy)}) {{{e}}};")
        if k:
            L.append(rf"\draw[fleche] (b{titre[-1]}{k-1}.south) -- (b{titre[-1]}{k}.north);")
        if expressions and expressions[k]:
            L.append(rf"\node[anchor=west,text=otGreenDark] at ($(b{titre[-1]}{k}.east)+(.25,0)$) {{{expressions[k]}}};")
    return L


def programmes_AB():
    L = [r"\begin{tikzpicture}"]
    L += programme("Programme A", ["Choisir un nombre", "Ajouter $5$", "Multiplier par $4$", "Soustraire $8$"], x0=0)
    L += programme("Programme B", ["Choisir un nombre", "Multiplier par $4$", "Ajouter $12$"], x0=4.1)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def programme_cours():
    L = [r"\begin{tikzpicture}"]
    L += programme("Programme de calcul",["Choisir un nombre", "Ajouter $4$", "Multiplier par $3$",
                                   "Retirer le triple\\\\du nombre de départ"],
                   ["$x$", "$x + 4$", "$3(x + 4)$", "$3(x + 4) - 3x$"])
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ bordure (exercice 2175)
def bordure(corrige):
    b, c = 0.8, 2.8               # largeur de la bordure, côté du petit carré (cm)
    T = c + 2 * b
    L = [r"\begin{tikzpicture}"]
    if corrige:
        # coins (orange) et bandes (vert)
        for (x, y) in ((0, 0), (b + c, 0), (0, b + c), (b + c, b + c)):
            L.append(rf"\filldraw[fill=otOrange!22,draw=otOrange!85!black,line width=.7pt] ({f(x)},{f(y)}) rectangle ({f(x+b)},{f(y+b)});")
        for (x, y, w, h) in ((b, 0, c, b), (b, b + c, c, b), (0, b, b, c), (b + c, b, b, c)):
            L.append(rf"\filldraw[fill=otGreen!18,draw=otGreenDark,line width=.7pt] ({f(x)},{f(y)}) rectangle ({f(x+w)},{f(y+h)});")
        L.append(rf"\node[text=otGreenDark] at ({f(b+c/2)},{f(b/2)}) {{$2x$}};")
        L.append(rf"\node[text=otGreenDark] at ({f(b+c/2)},{f(T-b/2)}) {{$2x$}};")
        L.append(rf"\node[text=otGreenDark] at ({f(b/2)},{f(b+c/2)}) {{$2x$}};")
        L.append(rf"\node[text=otGreenDark] at ({f(T-b/2)},{f(b+c/2)}) {{$2x$}};")
        for (x, y) in ((0, 0), (b + c, 0), (0, b + c), (b + c, b + c)):
            L.append(rf"\node[text=otOrange!75!black] at ({f(x+b/2)},{f(y+b/2)}) {{$4$}};")
        L.append(rf"\fill[white] ({f(b)},{f(b)}) rectangle ({f(b+c)},{f(b+c)});")
        L.append(rf"\draw[otNavy,line width=.9pt] ({f(b)},{f(b)}) rectangle ({f(b+c)},{f(b+c)});")
        L.append(rf"\node[text=otGreenDark,align=center] at ({f(T/2)},{f(T/2)}) {{$4 \times 2x + 4 \times 4$\\$= 8x + 16$}};")
    else:
        L.append(rf"\filldraw[fill=otOrange!16,draw=otOrange!85!black,line width=.9pt] (0,0) rectangle ({f(T)},{f(T)});")
        L.append(rf"\filldraw[fill=otSky,draw=otNavy,line width=.9pt] ({f(b)},{f(b)}) rectangle ({f(b+c)},{f(b+c)});")
        L.append(rf"\node[text=otOrange!75!black] at ({f(T/2)},{f(b/2)}) {{bordure}};")
    # cotes : x (sous le petit carré, dans la bordure ? non : à l'extérieur, en bas) et 2 cm (à droite)
    L.append(rf"\draw[cote] ({f(b)},-0.3) -- ({f(b+c)},-0.3);")
    L.append(rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(b)},-0.4) -- ({f(b)},{f(b)});")
    L.append(rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(b+c)},-0.4) -- ({f(b+c)},{f(b)});")
    L.append(rf"\node[anchor=north,text=otInk] at ({f(b+c/2)},-0.36) {{$x$}};")
    L.append(rf"\draw[cote] ({f(T+0.3)},{f(b+c)}) -- ({f(T+0.3)},{f(T)});")
    L.append(rf"\node[anchor=west,text=otInk] at ({f(T+0.38)},{f(b+c+b/2)}) {{$2$ cm}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES = {
    # cours : k(a + b) = ka + kb
    "distributivite_simple": aires([(3.4, "$a$"), (2.0, "$b$")], [(1.6, "$k$")],
                                   [["$k \\times a$", "$k \\times b$"]],
                                   couleurs=[["otSky", "otOrange!16"]]),
    # cours et fiche : (a + b)(c + d)
    "double_distributivite": aires([(3.2, "$a$"), (1.9, "$b$")], [(2.2, "$c$"), (1.3, "$d$")],
                                   [["$ac$", "$bc$"], ["$ad$", "$bd$"]],
                                   couleurs=[["otSky", "otOrange!16"], ["otGreen!16", "otSky!40!otOrange!14"]]),
    # cours : (a + b)^2
    "carre_somme": aires([(3.0, "$a$"), (1.5, "$b$")], [(3.0, "$a$"), (1.5, "$b$")],
                         [["$a^2$", "$ab$"], ["$ab$", "$b^2$"]],
                         couleurs=[["otSky", "otOrange!16"], ["otOrange!16", "otGreen!16"]]),
    "programme_cours": programme_cours(),
    # exercice 2198 : (x + 6)^2
    "carre_x6": aires([(3.0, "$x$"), (1.8, "$6$")], [(3.0, "$x$"), (1.8, "$6$")],
                      [["$x^2$", "$6x$"], ["$6x$", "$36$"]],
                      couleurs=[["otSky", "otGreen!16"], ["otGreen!16", "otOrange!16"]],
                      cell_col="otGreenDark"),
    # exercice 2199 : (2x + 3)(x + 5)
    "rectangle_enonce": aires([(3.6, "$2x$"), (1.5, "$3$")], [(1.8, "$x$"), (2.3, "$5$")],
                              couleurs=[["otSky", "otSky"], ["otSky", "otSky"]]),
    "rectangle_corrige": aires([(3.6, "$2x$"), (1.5, "$3$")], [(1.8, "$x$"), (2.3, "$5$")],
                               [["$2x^2$", "$3x$"], ["$10x$", "$15$"]],
                               couleurs=[["otSky", "otOrange!16"], ["otGreen!16", "otSky!40!otOrange!14"]],
                               cell_col="otGreenDark"),
    "programmes_AB": programmes_AB(),
    "bordure_enonce": bordure(False),
    "bordure_corrige": bordure(True),
}
