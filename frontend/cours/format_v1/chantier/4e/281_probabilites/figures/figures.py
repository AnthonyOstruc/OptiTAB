# -*- coding: utf-8 -*-
"""Figures de la notion 281 (4e : probabilités), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>

Énoncé : situation seule (urne, dé, roue, cartes, échelle, diagramme, script).
Corrigé : même figure, issues favorables en vert (contour vert épais, les autres
estompées quand les couleurs ont un sens ; fond vert sinon).
Moteurs d'arbre et de courbe de fréquences repris de la notion 3e 243 ; blocs Scratch
dessinés par scratch.py (copie du module de la notion 3e 248, non modifié).
Toutes les valeurs sont relues par ../verif_281.py (données DONNEES ci-dessous).
"""
import math
import random
from fractions import Fraction as Fr

from scratch import *  # noqa: F401,F403
from scratch import PREAMBULE_SCRATCH

PREAMBULE_EXTRA = PREAMBULE_SCRATCH + r"""
\definecolor{otYellow}{HTML}{F2C230}
\definecolor{otBlue}{HTML}{3F7AD6}
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\normalsize, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  titreCol/.style={font=\otRegular\fontsize{8.5}{10}\selectfont, text=otMuted, anchor=south},
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  legende/.style={font=\normalsize, text=otInk, inner sep=1.5pt},
}
\pgfplotsset{otLoi/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  xticklabel style={yshift=-1pt},
  ymajorgrids, grid style={otRule!75,line width=0.35pt},
  every axis x label/.style={at={(current axis.south)},anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,yshift=-16pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,yshift=4pt,xshift=-8pt},
  scale only axis, clip=false,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
"""

FIGURES = {}
TOLERE = {}
TEXTE_BLOC = ("textes blancs écrits sur le fond coloré des blocs Scratch : aucun trait sous le texte "
              "(contrôlé par controle_scratch.py sur une version à fonds blancs)")

# Données partagées avec verif_281.py
DONNEES = {
    "urne_cours": [("rouge", 5), ("bleue", 3), ("jaune", 2)],
    "urne_3125": [("rouge", 6), ("bleue", 4), ("jaune", 2)],
    "roue_cours": [180, 120, 60],
    "roue_3127": {1: "rouge", 2: "bleu", 3: "rouge", 4: "jaune", 5: "blanc", 6: "rouge", 7: "bleu", 8: "jaune"},
    "roue_3135": [180, 90, 60, 30],
    "roue_3139": {1: 5, 4: 2, 7: 2, 10: 2},          # secteurs gagnants (sur 12) : gain en euros
    "echelle_3129": {"C": Fr(0), "B": Fr(1, 6), "A": Fr(1, 2), "F": Fr(3, 4), "E": Fr(5, 6), "D": Fr(1)},
    "pile_3133": [(10, 7), (100, 56), (1000, 512), (10000, 4985)],
    "punaise_3137": [(20, 14), (50, 27), (100, 63), (200, 118), (500, 309), (1000, 612)],
    "urnes_3140": {"A": (3, 2), "B": (5, 4), "C": (8, 7)},
    "de_3142": [60, 65, 70, 75, 80, 150],
    "distributeur_3144": [("rouge", 12), ("jaune", 9), ("bleue", 6), ("blanche", 3)],
    "bande_3141": {"rouges": 3, "bleues": 4, "jaunes": 5},   # parts sur 12 (1 part = 2 boules)
}

COUL = {"rouge": "otRed", "bleue": "otBlue", "bleu": "otBlue", "jaune": "otYellow", "blanche": "white",
        "blanc": "white", "noire": "otInk"}
PLURIEL = {"rouge": "rouges", "bleue": "bleues", "jaune": "jaunes", "blanche": "blanches", "noire": "noires"}


def frac(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else rf"\dfrac{{{x.numerator}}}{{{x.denominator}}}"


# ================================================================ boules et urnes
def boule(x, y, couleur, r=0.2, etat="normal"):
    """etat : normal, favorable (contour vert), pale (estompée)."""
    c = COUL[couleur]
    op = ",opacity=0.28" if etat == "pale" else ""
    L = []
    bord = "otMuted" if c == "white" else c + "!70!black"
    L.append(rf"\filldraw[fill={c},draw={bord},line width=0.5pt{op}] ({x:.3f},{y:.3f}) circle ({r:.3f});")
    if etat != "pale" and c != "white":
        L.append(rf"\fill[white,opacity=.5] ({x - 0.35 * r:.3f},{y + 0.35 * r:.3f}) circle ({0.28 * r:.3f});")
    if etat == "favorable":
        L.append(rf"\draw[otGreenDark,line width=1.5pt] ({x:.3f},{y:.3f}) circle ({r + 0.06:.3f});")
    return L


def positions_grille(n, cols, s=0.56, r=0.2, y0=0.1):
    pos = []
    rows = (n + cols - 1) // cols
    for k in range(n):
        i, j = divmod(k, cols)
        nb = min(cols, n - i * cols)
        x = (j - (nb - 1) / 2) * s
        pos.append((x, y0 + r + 0.06 + i * s))
    return pos, rows


def bocal(W, H):
    return (rf"\fill[otSky!70] (-{W},{H}) -- (-{W},0.22) to[out=-90,in=180] (-{W - 0.22:.2f},0) -- "
            rf"({W - 0.22:.2f},0) to[out=0,in=-90] ({W},0.22) -- ({W},{H}) -- cycle;"
            "\n"
            rf"\draw[otNavy,line width=1pt,line cap=round] (-{W},{H}) -- (-{W},0.22) to[out=-90,in=180] "
            rf"(-{W - 0.22:.2f},0) -- ({W - 0.22:.2f},0) to[out=0,in=-90] ({W},0.22) -- ({W},{H});")


def urne(boules, cols=4, favorables=(), legende=True, titre=None, dx=0.0, s=0.56):
    """boules : liste de (couleur, nombre) ; favorables : couleurs mises en évidence (corrigé)."""
    seq = [c for c, n in boules for _ in range(n)]
    pos, rows = positions_grille(len(seq), cols, s=s)
    W = cols * s / 2 + 0.22
    H = 0.1 + rows * s + 0.45
    L = [rf"\begin{{scope}}[xshift={dx}cm]", bocal(W, H)]
    for (x, y), c in zip(pos, seq):
        etat = "normal" if not favorables else ("favorable" if c in favorables else "pale")
        L += boule(x, y, c, etat=etat)
    y = -0.45
    if titre:
        L.append(rf"\node[evt,font=\otMedium\fontsize{{10}}{{12}}\selectfont] at (0,{y:.2f}) {{{titre}}};")
        y -= 0.5
    if legende:
        for c, n in boules:
            v = c in favorables
            L += boule(-W + 0.25, y, c, r=0.14, etat="normal")
            sty = "legende,text=otGreenDark" if v else "legende"
            L.append(rf"\node[{sty},anchor=west] at ({-W + 0.48:.2f},{y:.2f}) {{${n}$ boules {PLURIEL[c]}}};")
            y -= 0.48
    L.append(r"\end{scope}")
    return "\n".join(L)


def fig(*parties):
    return "\n".join([r"\begin{tikzpicture}[x=1cm,y=1cm]"] + list(parties) + [r"\end{tikzpicture}"])


FIGURES["urne_cours"] = fig(urne(DONNEES["urne_cours"]))
FIGURES["urne_3125"] = fig(urne(DONNEES["urne_3125"]))
FIGURES["urne_3125_rouges"] = fig(urne(DONNEES["urne_3125"], favorables=("rouge",)))


def trois_urnes(favorables=()):
    parts = []
    for k, (nom, (r, n)) in enumerate(DONNEES["urnes_3140"].items()):
        bs = [("rouge", r), ("noire", n)]
        cols = {"A": 3, "B": 3, "C": 4}[nom]
        titre = rf"urne {nom}"
        parts.append(urne(bs, cols=cols, favorables=favorables, legende=False, titre=titre, dx=k * 2.55, s=0.5))
    return fig(*parts)


FIGURES["urnes_3140"] = trois_urnes()
FIGURES["urnes_3140_rouges"] = trois_urnes(favorables=("rouge",))


# ================================================================ dé
PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
        6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def faces(verts=()):
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    c, e = 0.95, 0.42
    for k in range(1, 7):
        x = (k - 1) * (c + 0.32)
        v = k in verts
        fond, bord, pip, lw = ("otGreen!30", "otGreenDark", "otGreenDark", "1.5pt") if v else ("white", "otNavy", "otNavy", "0.9pt")
        L.append(rf"\draw[fill={fond},draw={bord},line width={lw},rounded corners=2.5pt] ({x:.2f},0) rectangle ({x + c:.2f},{c:.2f});")
        for a, b in PIPS[k]:
            L.append(rf"\fill[{pip}] ({x + c / 2 + a * 0.26:.3f},{c / 2 + b * 0.26:.3f}) circle (0.085);")
        L.append(rf"\node[grad,text={'otGreenDark' if v else 'otMuted'}] at ({x + c / 2:.3f},-0.28) {{{k}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["de_faces"] = faces()
FIGURES["de_faces_pairs"] = faces(verts=(2, 4, 6))


# ================================================================ roues
def roue(secteurs, R=1.7, contour_vert=(), pales=(), interieur=0.62, exterieur=None, fl=True):
    """secteurs : liste de dict(angle, fond, txt, txt_ext, vert) en partant du haut, sens horaire.
    contour_vert : indices (1…n) entourés d'un trait vert épais ; pales : indices estompés."""
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    a = 90.0
    geo = []
    for k, s in enumerate(secteurs, start=1):
        b = a - s["angle"]
        geo.append((k, a, b, s))
        a = b
    for k, a, b, s in geo:
        op = ",opacity=0.3" if k in pales else ""
        L.append(r"\fill[%s%s] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;"
                 % (s["fond"], op, a, R, a, b, R))
    for k, a, b, s in geo:
        L.append(r"\draw[otNavy,line width=.8pt] (0,0) -- (%.2f:%.2f);" % (a, R))
    L.append(r"\draw[otNavy,line width=1pt] (0,0) circle (%.2f);" % R)
    for k, a, b, s in geo:
        if k in contour_vert:
            L.append(r"\draw[otGreenDark,line width=2.2pt,line join=round] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;"
                     % (a, R - 0.04, a, b, R - 0.04))
    for k, a, b, s in geo:
        m = (a + b) / 2
        if s.get("txt"):
            col = s.get("col", "otInk")
            L.append(r"\node[text=%s,font=\large,inner sep=1pt] at (%.2f:%.2f) {%s};" % (col, m, interieur * R, s["txt"]))
        if s.get("txt_ext"):
            col = s.get("col_ext", "otNavy")
            L.append(r"\node[text=%s,font=\large,inner sep=1pt] at (%.2f:%.2f) {%s};" % (col, m, R + (exterieur or 0.36), s["txt_ext"]))
    L.append(r"\fill[otNavy] (0,0) circle (1.8pt);")
    if fl:
        L.append(r"\fill[otOrange] (0,%.2f) -- (-0.18,%.2f) -- (0.18,%.2f) -- cycle;" % (R + 0.04, R + 0.42, R + 0.42))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# --- cours : 3 secteurs inégaux
FIGURES["roue_cours"] = roue([
    {"angle": 180, "fond": "otSky", "txt": r"$1$\\[-1pt]{\normalsize\color{otMuted}$180°$}"},
    {"angle": 120, "fond": "otYellow!35", "txt": r"$2$\\[-1pt]{\normalsize\color{otMuted}$120°$}"},
    {"angle": 60, "fond": "white", "txt": r"$3$\\[-1pt]{\normalsize\color{otMuted}$60°$}"},
], interieur=0.55).replace(r"font=\large,inner sep=1pt]", r"font=\large,inner sep=1pt,align=center]")


# --- 3127 : 8 secteurs égaux colorés, numéros à l'extérieur
def roue_couleurs(verts=()):
    fonds = {"rouge": "otRed", "bleu": "otBlue", "jaune": "otYellow", "blanc": "white"}
    sect = []
    for k in range(1, 9):
        v = k in verts
        sect.append({"angle": 45, "fond": fonds[DONNEES["roue_3127"][k]], "txt_ext": rf"${k}$",
                     "col_ext": "otGreenDark" if v else "otNavy"})
    pales = tuple(k for k in range(1, 9) if verts and k not in verts)
    return roue(sect, R=1.6, contour_vert=verts, pales=pales, exterieur=0.34)


FIGURES["roue_3127"] = roue_couleurs()
FIGURES["roue_3127_rouge_ou_pair"] = roue_couleurs(verts=(1, 2, 3, 4, 6, 8))


# --- 3135 : 4 secteurs inégaux numérotés, angles à l'extérieur
def roue_angles(verts=()):
    fonds = ["otSky", "white", "otSky", "white"]
    sect = []
    for k, ang in enumerate(DONNEES["roue_3135"], start=1):
        v = k in verts
        sect.append({"angle": ang, "fond": "otGreen!35" if v else fonds[k - 1], "txt": rf"${k}$",
                     "col": "otGreenDark" if v else "otInk", "txt_ext": rf"${ang}°$",
                     "col_ext": "otGreenDark" if v else "otMuted"})
    return roue(sect, R=1.6, exterieur=0.42)


FIGURES["roue_3135"] = roue_angles()
FIGURES["roue_3135_pairs"] = roue_angles(verts=(2, 4))


# --- 3138 : 8 secteurs égaux numérotés (jeu 3)
def roue_8(ana=(), ben=()):
    sect = []
    for k in range(1, 9):
        if k in ana:
            fond, col = "otGreen!35", "otGreenDark"
        elif k in ben:
            fond, col = "otOrange!40", "otOrange!70!black"
        else:
            fond, col = ("otSky" if k % 2 else "white"), "otNavy"
        sect.append({"angle": 45, "fond": fond, "txt": rf"${k}$", "col": col})
    code = roue(sect, R=1.6, interieur=0.66)
    if ana or ben:
        leg = (r"\begin{tikzpicture}[x=1cm,y=1cm]" "\n"
               r"\fill[otGreen!35,draw=otGreenDark] (2.3,0.45) rectangle (2.6,0.75);"
               r"\node[legende,anchor=west,text=otGreenDark] at (2.7,0.6) {Ana : $3$ et $6$};"
               r"\fill[otOrange!40,draw=otOrange!70!black] (2.3,-0.45) rectangle (2.6,-0.15);"
               r"\node[legende,anchor=west,text=otOrange!70!black] at (2.7,-0.3) {Ben : $4$ et $8$};")
        code = code.replace(r"\begin{tikzpicture}[x=1cm,y=1cm]", leg, 1)
    return code


FIGURES["roue_3138"] = roue_8()
FIGURES["roue_3138_jeu3"] = roue_8(ana=(3, 6), ben=(4, 8))


# --- 3139 : roue de la kermesse (12 secteurs)
def roue_kermesse(verts=False):
    sect = []
    for k in range(1, 13):
        g = DONNEES["roue_3139"].get(k)
        if g:
            fond = "otGreen!35" if verts else "otYellow!45"
            sect.append({"angle": 30, "fond": fond, "txt": rf"${g}$\,€", "col": "otGreenDark" if verts else "otInk"})
        else:
            sect.append({"angle": 30, "fond": "white" if k % 2 else "otSky"})
    return roue(sect, R=1.9, interieur=0.7).replace(r"font=\large,", r"font=\normalsize,")


FIGURES["roue_3139"] = roue_kermesse()
FIGURES["roue_3139_gagnants"] = roue_kermesse(verts=True)


# ================================================================ cartes
SUITS = [(r"\spadesuit", "otInk", "pique"), (r"\varheartsuit", "otRed", "cœur"),
         (r"\vardiamondsuit", "otRed", "carreau"), (r"\clubsuit", "otInk", "trèfle")]
VALEURS = ["7", "8", "9", "10", "V", "D", "R", "A"]


def carte(x, y, w, h, haut, bas=None, col="otInk", vert=False):
    fond, bord, lw = ("otGreen!30", "otGreenDark", "1.4pt") if vert else ("white", "otNavy!70", "0.7pt")
    L = [rf"\draw[fill={fond},draw={bord},line width={lw},rounded corners=2pt] ({x:.3f},{y:.3f}) rectangle ({x + w:.3f},{y + h:.3f});"]
    if bas is None:
        L.append(rf"\node[text={'otGreenDark' if vert else 'otInk'},inner sep=0pt] at ({x + w / 2:.3f},{y + h / 2:.3f}) {{${haut}$}};")
    else:
        L.append(rf"\node[text={'otGreenDark' if vert else 'otInk'},inner sep=0pt] at ({x + w / 2:.3f},{y + h * 0.69:.3f}) {{$\mathrm{{{haut}}}$}};")
        L.append(rf"\node[text={col},inner sep=0pt,font=\large] at ({x + w / 2:.3f},{y + h * 0.3:.3f}) {{${bas}$}};")
    return L


def jeu32(favorable=lambda v, s: False):
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    w, h, g = 0.82, 1.08, 0.12
    for i, (sym, col, nom) in enumerate(SUITS):
        for j, v in enumerate(VALEURS):
            L += carte(j * (w + g), -i * (h + g), w, h, v, sym, col, favorable(v, nom))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["cartes_32"] = jeu32()
FIGURES["cartes_32_figures"] = jeu32(lambda v, s: v in ("V", "D", "R"))

PREMIERS_20 = [n for n in range(2, 21) if all(n % d for d in range(2, n))]


def cartes20(verts=()):
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    w, h, g = 0.7, 0.9, 0.11
    for n in range(1, 21):
        i, j = divmod(n - 1, 10)
        L += carte(j * (w + g), -i * (h + g), w, h, str(n), vert=n in verts)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["cartes_20"] = cartes20()
FIGURES["cartes_20_premiers"] = cartes20(verts=PREMIERS_20)


# ================================================================ échelle des probabilités
def echelle(points=None, mots=True, fleche=False, pas=0.25, L=7.5):
    T = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    T.append(rf"\fill[otSky] (0,-0.09) rectangle ({L},0.09);")
    T.append(rf"\draw[otNavy,line width=0.8pt] (0,-0.09) rectangle ({L},0.09);")
    n = round(1 / pas)
    for k in range(n + 1):
        x = k * pas * L
        majeur = abs(k * pas * 4 - round(k * pas * 4)) < 1e-9
        T.append(rf"\draw[otNavy,line width={'0.8pt' if majeur else '0.5pt'}] ({x:.3f},{-0.2 if majeur else -0.15}) -- ({x:.3f},{0.2 if majeur else 0.15});")
        v = Fr(k, n)
        if majeur or pas >= 0.25:
            txt = f"{float(v):g}".replace(".", "{,}")
            T.append(rf"\node[grad,anchor=north] at ({x:.3f},-0.24) {{${txt}$}};")
        elif pas < 0.25:
            txt = f"{float(v):g}".replace(".", "{,}")
            T.append(rf"\node[grad,anchor=north] at ({x:.3f},-0.24) {{${txt}$}};")
    if mots:
        for v, t in [(0, "impossible"), (0.5, "une chance sur deux"), (1, "certain")]:
            T.append(rf"\node[legende,anchor=north,text=otNavy] at ({v * L:.3f},-0.68) {{{t}}};")
    if fleche:
        T.append(rf"\draw[otMuted,line width=0.7pt,-{{Stealth[length=2.2mm]}}] (0.6,0.62) -- ({L - 0.6},0.62);")
        T.append(rf"\node[grad,anchor=south] at ({L / 2},0.68) {{de plus en plus probable}};")
    if points:
        for nom, v in points.items():
            x = float(v) * L
            T.append(rf"\fill[otGreenDark] ({x:.3f},0) circle (2.6pt);")
            T.append(rf"\node[text=otGreenDark,font=\large,anchor=south] at ({x:.3f},0.24) {{${nom}$}};")
    T.append(r"\end{tikzpicture}")
    return "\n".join(T)


FIGURES["echelle_cours"] = echelle(fleche=True)
FIGURES["echelle_3129"] = echelle(pas=0.1, mots=True)
FIGURES["echelle_3129_placee"] = echelle(pas=0.1, mots=True, points=DONNEES["echelle_3129"])


# ================================================================ arbre (dénombrement, notion 243)
def N(nom, *enfants, vert=False, droite=None):
    return {"nom": nom, "p": None, "enfants": list(enfants), "vert": vert, "droite": droite}


def _vert(n):
    if not n["enfants"]:
        return n["vert"]
    n["vert"] = n["vert"] or any([_vert(c) for c in n["enfants"]])
    return n["vert"]


def _placer(n, prof, y, dy, ecarts, Lx):
    n["x"] = prof * Lx
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for k, c in enumerate(n["enfants"]):
        if k and c["enfants"]:
            y -= ecarts.get(prof + 1, 0)
        y = _placer(c, prof + 1, y, dy, ecarts, Lx)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def _tous_y(n):
    ys = [n["y"]]
    for c in n["enfants"]:
        ys += _tous_y(c)
    return ys


def arbre(enfants, mode="corrige", Lx=2.0, dy=0.85, ecarts=None, titres=None):
    racine = {"nom": None, "p": None, "enfants": enfants, "droite": None, "vert": False}
    if mode == "corrige":
        _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, Lx)
    noeuds, aretes, droites = [], [], []
    k = [0]

    def visiter(n, parent_ref):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            v = mode == "corrige" and c["vert"]
            noeuds.append(rf"\node[{'evt,text=otGreenDark' if v else 'evt'}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if v else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            if not c["enfants"] and mode == "corrige" and c["droite"]:
                si = "issueV" if c["vert"] else "issue"
                droites.append(rf"\node[{si}] at ([xshift=6pt]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)")

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)")
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += droites
    if titres:
        haut = max(_tous_y(racine)) + 0.45
        for i, t in enumerate(titres, start=1):
            lignes.append(rf"\node[titreCol] at ({i * Lx:.3f},{haut:.3f}) {{{t}}};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def pieces(verts=()):
    return [N(a, *[N(b, vert=(a + b) in verts, droite=f"${a}{b}$") for b in "PF"]) for a in "PF"]


TP = [r"1\textsuperscript{re} pièce", r"2\textsuperscript{e} pièce"]
FIGURES["arbre_pieces_enonce"] = arbre(pieces(), "enonce", ecarts={1: 0.25}, titres=TP)
FIGURES["arbre_pieces"] = arbre(pieces({"PF", "FP"}), "corrige", ecarts={1: 0.25}, titres=TP)


# ================================================================ courbes de fréquences
def simulation(p, n, graine, pas=10):
    r = random.Random(graine)
    s, pts = 0, []
    for k in range(1, n + 1):
        s += r.random() < p
        if k % pas == 0:
            pts.append((k, s / k))
    return pts


DONNEES["sim_cours"] = simulation(1 / 6, 2000, 117)


def courbe_frequence(points, cible, cible_tex, xmax, yticks, ymin, ymax, ylabel):
    coords = " ".join(f"({x},{y:.4f})" for x, y in points)
    yt = ",".join(str(v) for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width=6.4cm, height=3.8cm, xmin=0, xmax={xmax}, ymin={ymin}, ymax={ymax},
  scaled x ticks=false, scaled y ticks=false,
  xtick={{0,500,1000,1500,2000}}, xticklabels={{$0$,$500$,$1\,000$,$1\,500$,$2\,000$}},
  ytick={{{yt}}}, yticklabels={{{ytl}}},
  xlabel={{nombre de lancers}}, ylabel={{{ylabel}}}]
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,{cible}) -- (axis cs:{xmax},{cible});
\node[anchor=west, legendeV, font=\normalsize] at (axis cs:{xmax},{cible}) {{{cible_tex}}};
\addplot[courbe, line width=1pt] coordinates {{{coords}}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["frequences_6"] = courbe_frequence(DONNEES["sim_cours"], 1 / 6, r"$\dfrac{1}{6}$", 2000,
                                           [(0, "0"), (0.1, "0{,}1"), (0.2, "0{,}2"), (0.3, "0{,}3"), (0.4, "0{,}4")],
                                           0, 0.42, "fréquence du $6$")


def nuage_categories(series, cible, cible_tex, ymin, ymax, yticks, ylabel, largeur=6.4):
    n = len(series)
    coords = " ".join(f"({k},{Fr(s, e) * 1.0:.4f})" for k, (e, s) in enumerate(series, start=1))
    xt = ",".join(str(k) for k in range(1, n + 1))
    xtl = ",".join("{$" + f"{e:,}".replace(",", r"\,") + "$}" for e, _ in series)
    yt = ",".join(str(v) for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width={largeur}cm, height=3.8cm, xmin=0.5, xmax={n + 0.5}, ymin={ymin}, ymax={ymax},
  xtick={{{xt}}}, xticklabels={{{xtl}}}, ytick={{{yt}}}, yticklabels={{{ytl}}},
  scaled y ticks=false, xlabel={{nombre de lancers}}, ylabel={{{ylabel}}}]
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0.5,{cible}) -- (axis cs:{n + 0.5},{cible});
\node[anchor=west, legendeV, font=\normalsize] at (axis cs:{n + 0.5},{cible}) {{{cible_tex}}};
\addplot[courbe, line width=1pt, mark=*, mark size=2.2pt, mark options={{fill=otNavy}}] coordinates {{{coords}}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["frequences_3133"] = nuage_categories(DONNEES["pile_3133"], 0.5, r"$0{,}5$", 0.4, 0.75,
                                              [(0.4, "0{,}4"), (0.5, "0{,}5"), (0.6, "0{,}6"), (0.7, "0{,}7")],
                                              "fréquence de « pile »", largeur=5.6)
FIGURES["frequences_3137"] = nuage_categories(DONNEES["punaise_3137"], 0.612, r"$\approx 0{,}61$", 0.5, 0.75,
                                              [(0.5, "0{,}5"), (0.6, "0{,}6"), (0.7, "0{,}7")],
                                              "fréquence de « pointe en haut »")


# ================================================================ diagramme du dé truqué
def barres_de(attendu=False):
    eff = DONNEES["de_3142"]
    coords = " ".join(f"({k},{e})" for k, e in enumerate(eff, start=1))
    nn = "" if attendu else ", nodes near coords"
    ligne = ""
    if attendu:
        m = 500 / 6
        ligne = (rf"\draw[otGreenDark, line width=1pt, dash pattern=on 4pt off 2.5pt] (axis cs:0.4,{m:.3f}) -- (axis cs:6.6,{m:.3f});" "\n"
                 rf"\node[anchor=west, legendeV, font=\normalsize, align=left] at (axis cs:6.6,{m:.3f}) {{dé équilibré :\\$\approx 83$}};")
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otBarres, width=5.7cm, height=4.2cm, ymax=170, xmin=0.4, xmax=6.6, enlarge x limits=false,
  xtick={{1,2,3,4,5,6}}, ytick={{0,20,40,60,80,100,120,140,160}}, bar width=17pt,
  xlabel={{face}}, ylabel={{effectif}}, clip=false{nn}]
\addplot[fill=otNavy!55, draw=otNavy] coordinates {{{coords}}};
{ligne}
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["barres_3142"] = barres_de()
FIGURES["barres_3142_attendu"] = barres_de(attendu=True)


# ================================================================ bande des fractions (3141)
def bande():
    w, h = 0.7, 0.7
    grp = [("rouges", 3, "otRed!30", r"\frac{1}{4}"), ("bleues", 4, "otBlue!25", r"\frac{1}{3}"),
           ("jaunes", 5, "otYellow!55", r"\frac{5}{12}")]
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    x = 0
    for nom, n, fond, f in grp:
        for i in range(n):
            vj = nom == "jaunes"
            L.append(rf"\draw[fill={fond},draw=otNavy,line width=0.7pt] ({x + i * w:.2f},0) rectangle ({x + (i + 1) * w:.2f},{h});")
            L.append(rf"\node[text=otGreenDark,inner sep=0pt] at ({x + (i + 0.5) * w:.2f},{h / 2}) {{$2$}};")
        L.append(rf"\draw[otMuted,line width=0.7pt,decorate,decoration={{brace,amplitude=4pt}}] ({x + 0.05:.2f},{h + 0.12}) -- ({x + n * w - 0.05:.2f},{h + 0.12});")
        L.append(rf"\node[legende,anchor=south] at ({x + n * w / 2:.2f},{h + 0.3}) {{{nom} : ${f}$}};")
        x += n * w
    xj = 7 * w
    L.append(rf"\draw[otGreenDark,line width=0.9pt,decorate,decoration={{brace,amplitude=4pt,mirror}}] ({xj + 0.05:.2f},-0.12) -- ({x - 0.05:.2f},-0.12);")
    L.append(rf"\node[legende,text=otGreenDark,anchor=north] at ({(xj + x) / 2:.2f},-0.3) {{$5$ parts $= 10$ boules}};")
    L.append(rf"\node[legende,text=otGreenDark,anchor=north] at ({3.5 * w:.2f},-0.3) {{$1$ part $= 2$ boules}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["bande_3141"] = bande()


# ================================================================ distributeur (3144)
def distributeur(favorables=()):
    R, r = 1.85, 0.17
    pos = []
    dx, dy = 0.43, 0.38
    for i in range(-12, 13):
        for j in range(-8, 8):
            x = j * dx + (dx / 2 if i % 2 else 0)
            y = i * dy
            if math.hypot(x, y) <= R - r - 0.07:
                pos.append((x, y))
    pos.sort(key=lambda p: (round(p[1], 3), p[0]))
    pos = pos[:30]
    seq = [c for c, n in DONNEES["distributeur_3144"] for _ in range(n)]
    random.Random(4).shuffle(seq)
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    L.append(r"\fill[otNavy!80] (-0.85,-1.5) -- (0.85,-1.5) -- (1.15,-3.0) -- (-1.15,-3.0) -- cycle;")
    L.append(r"\fill[white] (-0.32,-2.55) rectangle (0.32,-2.85);")
    L.append(r"\filldraw[fill=otOrange,draw=otOrange!70!black,line width=0.6pt] (0,-2.05) circle (0.26);")
    L.append(r"\fill[otOrange!70!black] (-0.05,-2.27) rectangle (0.05,-1.83);")
    L.append(rf"\filldraw[fill=otSky!60,draw=otNavy,line width=1pt] (0,0) circle ({R});")
    L.append(r"\fill[otNavy!80] (-0.45,%.2f) rectangle (0.45,%.2f);" % (R - 0.05, R + 0.22))
    for (x, y), c in zip(pos, seq):
        etat = "normal" if not favorables else ("favorable" if c in favorables else "pale")
        L += boule(x, y, c, r=r, etat=etat)
    y = 0.95
    for c, n in DONNEES["distributeur_3144"]:
        v = c in favorables
        L += boule(2.35, y, c, r=0.15)
        L.append(rf"\node[legende,anchor=west{',text=otGreenDark' if v else ''}] at (2.6,{y:.2f}) {{${n}$ {PLURIEL[c]}}};")
        y -= 0.55
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["distributeur_3144"] = distributeur()
FIGURES["distributeur_3144_rouges"] = distributeur(favorables=("rouge",))


# ================================================================ cible (3145)
def cible(zone=None):
    """zone : None (énoncé), "centre" ou "couronne" (corrigé, zone en vert)."""
    g = "otGreen!40"
    grand = g if zone == "couronne" else "otSky"
    petit = g if zone == "centre" else ("white" if zone == "couronne" else "otNavy!18")
    L = [r"\begin{tikzpicture}[x=1.2cm,y=1.2cm]"]
    L.append(r"\draw[otNavy,line width=1pt,fill=white] (0,0) rectangle (4,4);")
    L.append(rf"\filldraw[fill={grand},draw=otNavy,line width=0.9pt] (2,2) circle (2);")
    L.append(rf"\filldraw[fill={petit},draw=otNavy,line width=0.9pt] (2,2) circle (1);")
    L.append(r"\fill[otNavy] (2,2) circle (1.6pt);")
    L.append(r"\draw[otInk,line width=0.7pt] (2,2) -- (3,2);")
    L.append(r"\node[coteTexte,fill=none,anchor=south] at (2.48,2.05) {$10$ cm};")
    L.append(r"\draw[otInk,line width=0.7pt] (2,2) -- (2,0);")
    L.append(r"\node[coteTexte,fill=none,anchor=west] at (2.06,0.5) {$20$ cm};")
    L.append(r"\coordinate (Q1) at (4,0); \coordinate (Q0) at (0,0); \cote[0.45]{Q1}{Q0}{$40$ cm}")
    if zone:
        t = "petit disque" if zone == "centre" else "couronne"
        L.append(rf"\node[legende,text=otGreenDark,anchor=north] at (2,-0.85) {{zone favorable : {t}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["cible_3145"] = cible()
FIGURES["cible_3145_centre"] = cible("centre")
FIGURES["cible_3145_couronne"] = cible("couronne")


# ================================================================ scripts Scratch
SCRIPTS = {
    "cours": [Drapeau(), Mettre("succès", 0),
              Repeter(1000, [Mettre("dé", Alea(1, 6)), Si(Cmp(V("dé"), "=", 6), [Ajouter("succès", 1)])]),
              Dire(Op(V("succès"), "/", 1000))],
    "3132": [Drapeau(), Mettre("succès", 0),
             Repeter(600, [Mettre("dé", Alea(1, 6)), Si(Cmp(V("dé"), "=", 6), [Ajouter("succès", 1)])]),
             Dire(Op(V("succès"), "/", 600))],
    "3132_6000": [Drapeau(), Mettre("succès", 0),
                  Repeter(Trou("A", 6000), [Mettre("dé", Alea(1, 6)), Si(Cmp(V("dé"), "=", 6), [Ajouter("succès", 1)])]),
                  Dire(Op(V("succès"), "/", Trou("B", 6000)))],
}


def scripts_fig(nom, pile, corrige=False):
    FIGURES[nom] = figure_scripts([("", pile)], corrige=corrige)
    TOLERE[nom] = TEXTE_BLOC


scripts_fig("scratch_cours", SCRIPTS["cours"])
scripts_fig("scratch_3132", SCRIPTS["3132"])
scripts_fig("scratch_3132_6000", SCRIPTS["3132_6000"], corrige=True)
