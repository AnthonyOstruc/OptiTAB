# -*- coding: utf-8 -*-
"""Figures de la notion 279 (5e : hasard et probabilités), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>

Énoncé : situation seule (dé, urne, sacs, roue, cartes, échelle vide, courbes).
Corrigé : même figure, issues favorables en vert (contour vert épais, les autres
estompées quand les couleurs ont un sens ; fond vert sinon).
Moteurs (boules, urnes, faces de dé, roues, cartes, échelle, courbes de fréquences)
repris de la notion 4e 281 et adaptés. Toutes les valeurs sont relues par
../verif_279.py (données DONNEES ci-dessous).
"""
import random
from fractions import Fraction as Fr

PREAMBULE_EXTRA = r"""
\definecolor{otYellow}{HTML}{F2C230}
\definecolor{otBlue}{HTML}{3F7AD6}
\tikzset{
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},
  legende/.style={font=\normalsize, text=otInk, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  titreFig/.style={font=\otMedium\fontsize{10}{12}\selectfont, text=otNavy, inner sep=1.5pt},
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

# Données partagées avec verif_279.py
DONNEES = {
    "sac_cours": [("rouge", 5), ("bleu", 2), ("vert", 1)],
    "roue_cours": [("bleu", 180), ("jaune", 120), ("rouge", 60)],
    "echelle_sac": {"jaune": Fr(0), "vert": Fr(1, 8), "bleu": Fr(1, 4), "rouge": Fr(5, 8), "certain": Fr(1)},
    "urne_3087": [("rouge", 3), ("bleue", 1)],
    "echelle_3087": {"D": Fr(0), "B": Fr(1, 6), "A": Fr(1, 2), "C": Fr(3, 4), "E": Fr(1)},
    "urne_3083": [("rouge", 6), ("bleue", 3), ("jaune", 1)],
    "evenements_3084": {"A": (2, 4, 6), "B": (3, 6), "C": (1, 2)},
    "cartes_3096": {"A": (2, 4, 6, 8, 10, 12), "C": (1, 2, 3, 4, 6, 12)},
    "roue1_3103": ["rouge", "bleu", "rouge", "jaune", "blanc", "bleu", "rouge", "jaune"],
    "roue2_3103": [("rouge", 180), ("bleu", 90), ("jaune", 90)],
    "barres_3089": [("Inès", 20, 8), ("classe", 500, 243)],
    "sacs_3101": {"A": (3, 5), "B": (7, 9), "C": (5, 5)},       # (jaunes, bleus)
    "des_3094": {"Malik": (68, [1, 1, 1, 1, 1, 1]), "Nora": (3, [14, 14, 14, 14, 14, 30])},
    "gagnants_3092": (4, 8, 12),
    "echelle_3092": {"B": Fr(3, 20), "A": Fr(1, 4), "C": Fr(1, 3)},
    "regle2_3102": {"Zoé": (1, 2, 5), "Yanis": (3, 4, 6)},
    "echelle_3102": {"Zoé1": Fr(1, 3), "Yanis1": Fr(2, 3), "regle2": Fr(1, 2)},
}

COUL = {"rouge": "otRed", "bleue": "otBlue", "bleu": "otBlue", "jaune": "otYellow", "blanche": "white",
        "blanc": "white", "vert": "otGreen", "verte": "otGreen"}


# ================================================================ boules, jetons, urnes
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
    return (rf"\fill[otSky!70] (-{W:.2f},{H:.2f}) -- (-{W:.2f},0.22) to[out=-90,in=180] (-{W - 0.22:.2f},0) -- "
            rf"({W - 0.22:.2f},0) to[out=0,in=-90] ({W:.2f},0.22) -- ({W:.2f},{H:.2f}) -- cycle;"
            "\n"
            rf"\draw[otNavy,line width=1pt,line cap=round] (-{W:.2f},{H:.2f}) -- (-{W:.2f},0.22) to[out=-90,in=180] "
            rf"(-{W - 0.22:.2f},0) -- ({W - 0.22:.2f},0) to[out=0,in=-90] ({W:.2f},0.22) -- ({W:.2f},{H:.2f});")


def urne(objets, nom="boule", cols=4, favorables=(), legende=True, titre=None, dx=0.0, s=0.56, H=None):
    """objets : liste de (couleur, nombre) ; favorables : couleurs mises en évidence (corrigé)."""
    seq = [c for c, n in objets for _ in range(n)]
    pos, rows = positions_grille(len(seq), cols, s=s)
    W = cols * s / 2 + 0.22
    H = H if H is not None else 0.1 + rows * s + 0.45
    L = [rf"\begin{{scope}}[xshift={dx}cm]", bocal(W, H)]
    for (x, y), c in zip(pos, seq):
        etat = "normal" if not favorables else ("favorable" if c in favorables else "pale")
        L += boule(x, y, c, etat=etat)
    y = -0.45
    if titre:
        L.append(rf"\node[titreFig] at (0,{y:.2f}) {{{titre}}};")
        y -= 0.5
    if legende:
        for c, n in objets:
            v = c in favorables
            L += boule(-W + 0.25, y, c, r=0.14, etat="normal")
            sty = "legende,text=otGreenDark" if v else "legende"
            mot = nom + ("s" if n > 1 else "")
            coul = c if n == 1 else (c + "s")
            L.append(rf"\node[{sty},anchor=west] at ({-W + 0.48:.2f},{y:.2f}) {{${n}$ {mot} {coul}}};")
            y -= 0.48
    L.append(r"\end{scope}")
    return "\n".join(L)


def fig(*parties):
    return "\n".join([r"\begin{tikzpicture}[x=1cm,y=1cm]"] + list(parties) + [r"\end{tikzpicture}"])


FIGURES["urne_cours"] = fig(urne(DONNEES["sac_cours"], nom="jeton"))
FIGURES["urne_3087"] = fig(urne(DONNEES["urne_3087"], cols=2))
FIGURES["urne_3083"] = fig(urne(DONNEES["urne_3083"], cols=4))
FIGURES["urne_3083_rouges"] = fig(urne(DONNEES["urne_3083"], cols=4, favorables=("rouge",)))


def trois_sacs(favorables=()):
    parts = []
    for k, (nom, (j, b)) in enumerate(DONNEES["sacs_3101"].items()):
        objets = [("jaune", j), ("bleu", b)]
        parts.append(urne(objets, cols=4, favorables=favorables, legende=False, titre=rf"sac {nom}",
                          dx=k * 2.75, s=0.5, H=0.1 + 4 * 0.5 + 0.45))
    return fig(*parts)


FIGURES["sacs_3101"] = trois_sacs()
FIGURES["sacs_3101_gagnants"] = trois_sacs(favorables=("jaune",))


# ================================================================ dé
PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
        6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def rangee_faces(y=0.0, verts=(), oranges=(), x0=0.0, numeros=True):
    L = []
    c = 0.95
    for k in range(1, 7):
        x = x0 + (k - 1) * (c + 0.32)
        if k in verts:
            fond, bord, pip, lw, num = "otGreen!30", "otGreenDark", "otGreenDark", "1.5pt", "otGreenDark"
        elif k in oranges:
            fond, bord, pip, lw, num = "otOrange!35", "otOrange!80!black", "otOrange!80!black", "1.5pt", "otOrange!80!black"
        elif verts or oranges:
            fond, bord, pip, lw, num = "white", "otNavy!45", "otNavy!45", "0.9pt", "otMuted"
        else:
            fond, bord, pip, lw, num = "white", "otNavy", "otNavy", "0.9pt", "otMuted"
        L.append(rf"\draw[fill={fond},draw={bord},line width={lw},rounded corners=2.5pt] ({x:.2f},{y:.2f}) rectangle ({x + c:.2f},{y + c:.2f});")
        for a, b in PIPS[k]:
            L.append(rf"\fill[{pip}] ({x + c / 2 + a * 0.26:.3f},{y + c / 2 + b * 0.26:.3f}) circle (0.085);")
        if numeros:
            L.append(rf"\node[grad,text={num}] at ({x + c / 2:.3f},{y - 0.28:.3f}) {{{k}}};")
    return L


FIGURES["de_faces"] = fig(*rangee_faces())


def de_evenements():
    L = []
    for i, (nom, verts) in enumerate(DONNEES["evenements_3084"].items()):
        y = -i * 1.55
        L.append(rf"\node[text=otNavy,font=\large,anchor=east] at (-0.2,{y + 0.475:.3f}) {{${nom}$}};")
        L += rangee_faces(y=y, verts=verts)
    return fig(*L)


FIGURES["de_evenements_3084"] = de_evenements()


def de_regle2():
    z, y = DONNEES["regle2_3102"]["Zoé"], DONNEES["regle2_3102"]["Yanis"]
    L = rangee_faces(verts=z, oranges=y)
    L.append(r"\fill[otGreen!30,draw=otGreenDark,line width=0.8pt] (0.3,-0.95) rectangle (0.6,-0.65);")
    L.append(r"\node[legende,anchor=west,text=otGreenDark] at (0.7,-0.8) {Zoé : $1$, $2$, $5$};")
    L.append(r"\fill[otOrange!35,draw=otOrange!80!black,line width=0.8pt] (4.1,-0.95) rectangle (4.4,-0.65);")
    L.append(r"\node[legende,anchor=west,text=otOrange!80!black] at (4.5,-0.8) {Yanis : $3$, $4$, $6$};")
    return fig(*L)


FIGURES["de_3102_regle2"] = de_regle2()


# ================================================================ roues
def roue(secteurs, R=1.7, contour_vert=(), pales=(), fl=True, partage=None, styles_partage="otMuted,line width=0.8pt,dash pattern=on 3pt off 2pt",
         cx=0.0, cy=0.0, envelopper=True):
    """secteurs : liste de dict(angle, fond, txt, col, pos) en partant du haut, sens horaire.
    pos : (angle, rayon relatif) de l'étiquette ; par défaut milieu du secteur, 0,62 R.
    partage : angles (en degrés) des rayons en pointillés qui partagent la roue en secteurs égaux."""
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"] if envelopper else []
    L.append(rf"\begin{{scope}}[shift={{({cx},{cy})}}]")
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
    if partage:
        for t in partage:
            L.append(r"\draw[%s] (0,0) -- (%.2f:%.2f);" % (styles_partage, t, R))
    for k, a, b, s in geo:
        L.append(r"\draw[otNavy,line width=.8pt] (0,0) -- (%.2f:%.2f);" % (a, R))
    L.append(r"\draw[otNavy,line width=1pt] (0,0) circle (%.2f);" % R)
    for k, a, b, s in geo:
        if k in contour_vert:
            L.append(r"\draw[otGreenDark,line width=2.2pt,line join=round] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;"
                     % (a, R - 0.04, a, b, R - 0.04))
    for k, a, b, s in geo:
        if s.get("txt"):
            ang, rr = s.get("pos", ((a + b) / 2, 0.62))
            col = s.get("col", "otInk")
            L.append(r"\node[text=%s,font=%s,inner sep=1pt,align=center] at (%.2f:%.2f) {%s};"
                     % (col, s.get("font", r"\large"), ang, rr * R, s["txt"]))
    L.append(r"\fill[otNavy] (0,0) circle (1.8pt);")
    if fl:
        L.append(r"\fill[otOrange] (0,%.2f) -- (-0.18,%.2f) -- (0.18,%.2f) -- cycle;" % (R + 0.04, R + 0.42, R + 0.42))
    L.append(r"\end{scope}")
    if envelopper:
        L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FOND = {"rouge": "otRed!75", "bleu": "otBlue!70", "jaune": "otYellow", "blanc": "white"}


# --- cours : bleu 180°, jaune 120°, rouge 60° ; partage en 6 secteurs de 60°
def roue_cours():
    sect = []
    for nom, ang in DONNEES["roue_cours"]:
        sect.append({"angle": ang, "fond": FOND[nom], "txt": rf"${ang}°$", "col": "otNavy"})
    # étiquettes d'angle à l'extérieur de la roue (pas de texte sur les aplats colorés)
    R = 1.75
    for s, ang in zip(sect, (0, -150, 120)):
        s["pos"] = (ang, (R + 0.45) / R)
    return roue(sect, R=R, partage=(30, -30, -150))


FIGURES["roue_cours"] = roue_cours()


# --- 3103 : roue 1 (8 secteurs égaux colorés) et roue 2 (180°, 90°, 90°)
def secteurs_roue1(verts=False):
    sect = []
    for k, c in enumerate(DONNEES["roue1_3103"], start=1):
        sect.append({"angle": 45, "fond": FOND[c]})
    if verts:
        rouges = tuple(k for k, c in enumerate(DONNEES["roue1_3103"], start=1) if c == "rouge")
        pales = tuple(k for k in range(1, 9) if k not in rouges)
        return sect, rouges, pales
    return sect, (), ()


def secteurs_roue2(quarts=False):
    sect = []
    for nom, ang in DONNEES["roue2_3103"]:
        sect.append({"angle": ang, "fond": FOND[nom], "txt": "" if quarts else rf"${ang}°$", "col": "otNavy"})
    for s, ang in zip(sect, (0, -135, 135)):
        s["pos"] = (ang, (1.45 + 0.42) / 1.45)
    return sect


def roues_3103():
    s1, _, _ = secteurs_roue1()
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    L.append(roue(s1, R=1.45, envelopper=False))
    L.append(r"\node[titreFig] at (0,-1.85) {roue 1};")
    L.append(roue(secteurs_roue2(), R=1.45, cx=3.75, envelopper=False))
    L.append(r"\node[titreFig] at (3.75,-1.85) {roue 2};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["roues_3103"] = roues_3103()


def roue1_rouges():
    s1, rouges, pales = secteurs_roue1(verts=True)
    code = roue(s1, R=1.6, contour_vert=rouges, pales=pales)
    leg = r"\node[legende,anchor=west,text=otGreenDark] at (2.0,0) {$3$ secteurs rouges sur $8$};"
    return code.replace(r"\end{tikzpicture}", leg + "\n" + r"\end{tikzpicture}")


FIGURES["roue1_3103_rouges"] = roue1_rouges()


def roue2_quarts():
    sect = secteurs_roue2(quarts=True)
    code = roue(sect, R=1.6, partage=(0,), styles_partage="otGreenDark,line width=1.3pt,dash pattern=on 4pt off 2.5pt")
    q = r"$\dfrac{1}{4}$"
    noeuds = []
    for ang in (45, -45, -135, 135):
        noeuds.append(r"\node[text=otGreenDark,inner sep=1pt] at (%d:2.08) {%s};" % (ang, q))
    noeuds.append(r"\node[legende,anchor=west,text=otGreenDark,align=left] at (2.35,0) {rouge : $2$ quarts\\bleu : $1$ quart\\jaune : $1$ quart};")
    return code.replace(r"\end{tikzpicture}", "\n".join(noeuds) + "\n" + r"\end{tikzpicture}")


FIGURES["roue2_3103_quarts"] = roue2_quarts()


# --- 3092 : roue de 12 secteurs numérotés
def roue_12(verts=()):
    sect = []
    for k in range(1, 13):
        v = k in verts
        fond = "otGreen!35" if v else ("otSky" if k % 2 else "white")
        sect.append({"angle": 30, "fond": fond, "txt": rf"${k}$", "col": "otGreenDark" if v else "otInk",
                     "pos": (90 - 30 * (k - 1) - 15, 0.72)})
    return roue(sect, R=1.8, contour_vert=verts)


FIGURES["roue_3092"] = roue_12()
FIGURES["roue_3092_gagnants"] = roue_12(verts=DONNEES["gagnants_3092"])


# ================================================================ cartes
def carte(x, y, w, h, texte, vert=False, pale=False):
    if vert:
        fond, bord, lw, col = "otGreen!30", "otGreenDark", "1.4pt", "otGreenDark"
    elif pale:
        fond, bord, lw, col = "white", "otNavy!40", "0.7pt", "otMuted"
    else:
        fond, bord, lw, col = "white", "otNavy!70", "0.7pt", "otInk"
    return [rf"\draw[fill={fond},draw={bord},line width={lw},rounded corners=2pt] ({x:.3f},{y:.3f}) rectangle ({x + w:.3f},{y + h:.3f});",
            rf"\node[text={col},inner sep=0pt,font=\large] at ({x + w / 2:.3f},{y + h / 2:.3f}) {{${texte}$}};"]


def paquet(n, par_ligne, verts=None, y0=0.0, x0=0.0, w=0.72, h=0.95, g=0.13):
    L = []
    for k in range(1, n + 1):
        i, j = divmod(k - 1, par_ligne)
        v = verts is not None and k in verts
        p = verts is not None and k not in verts
        L += carte(x0 + j * (w + g), y0 - i * (h + g), w, h, str(k), vert=v, pale=p)
    return L


FIGURES["cartes_10_impairs"] = fig(*paquet(10, 5, verts=(1, 3, 5, 7, 9)))
FIGURES["cartes_12"] = fig(*paquet(12, 6))


def cartes_A_C():
    L = []
    for i, nom in enumerate(("A", "C")):
        y = -i * 2.75
        L.append(rf"\node[text=otNavy,font=\large,anchor=east] at (-0.2,{y + 0.475 - 0.54:.3f}) {{${nom}$}};")
        L += paquet(12, 6, verts=DONNEES["cartes_3096"][nom], y0=y)
    return fig(*L)


FIGURES["cartes_12_A_C"] = cartes_A_C()


# ================================================================ échelle des probabilités
def dec(v, chiffres=3):
    t = f"{float(v):.{chiffres}f}".rstrip("0").rstrip(".")
    return t.replace(".", "{,}")


def echelle(points=(), pas=Fr(1, 4), L=6.6, mots=False, fleche=False, y=0.0, titre=None, valeurs=True):
    """points : liste de (valeur, étiquette, niveau, couleur, ancre) ; niveau 1 ou 2 (au-dessus de la barre)."""
    T = []
    T.append(rf"\fill[otSky] (0,{y - 0.09:.2f}) rectangle ({L},{y + 0.09:.2f});")
    T.append(rf"\draw[otNavy,line width=0.8pt] (0,{y - 0.09:.2f}) rectangle ({L},{y + 0.09:.2f});")
    n = int(1 / pas)
    for k in range(n + 1):
        x = float(k * pas) * L
        T.append(rf"\draw[otNavy,line width=0.7pt] ({x:.3f},{y - 0.2:.2f}) -- ({x:.3f},{y + 0.2:.2f});")
        if valeurs:
            T.append(rf"\node[grad,anchor=north] at ({x:.3f},{y - 0.24:.2f}) {{${dec(k * pas)}$}};")
    if mots:
        for v, t, h in [(0, "impossible", 0.7), (Fr(1, 4), "peu probable", 1.2), (Fr(1, 2), "une chance sur deux", 0.7),
                        (Fr(3, 4), "très probable", 1.2), (1, "certain", 0.7)]:
            T.append(rf"\node[legende,anchor=north,text=otNavy] at ({float(v) * L:.3f},{y - h:.2f}) {{{t}}};")
    if fleche:
        T.append(rf"\draw[otMuted,line width=0.7pt,-{{Stealth[length=2.2mm]}}] (0.6,{y + 0.55:.2f}) -- ({L - 0.6},{y + 0.55:.2f});")
        T.append(rf"\node[grad,anchor=south] at ({L / 2},{y + 0.62:.2f}) {{de plus en plus probable}};")
    for v, txt, niveau, col, ancre in points:
        x = float(v) * L
        T.append(rf"\fill[{col}] ({x:.3f},{y:.2f}) circle (2.7pt);")
        if niveau == 1:
            T.append(rf"\node[text={col},font=\large,anchor={ancre},inner sep=1.5pt] at ({x:.3f},{y + 0.24:.2f}) {{{txt}}};")
        else:
            T.append(rf"\draw[{col},line width=0.6pt] ({x:.3f},{y + 0.12:.2f}) -- ({x:.3f},{y + 0.78:.2f});")
            T.append(rf"\node[text={col},font=\large,anchor={ancre},inner sep=1.5pt] at ({x:.3f},{y + 0.82:.2f}) {{{txt}}};")
    if titre:
        T.append(rf"\node[titreFig,anchor=south west] at (0,{y + 0.8:.2f}) {{{titre}}};")
    return T


FIGURES["echelle_cours"] = fig(*echelle(pas=Fr(1, 4), mots=True, fleche=True, L=6.0))

V = "otGreenDark"
FIGURES["echelle_sac"] = fig(*echelle(pas=Fr(1, 4), points=[
    (0, "jaune", 1, V, "south"), (Fr(1, 8), "vert", 2, V, "south"), (Fr(1, 4), "bleu", 1, V, "south"),
    (Fr(5, 8), "rouge", 1, V, "south"), (1, "rouge, bleu ou vert", 2, V, "south east")]))

FIGURES["echelle_3087"] = fig(*echelle(pas=Fr(1, 10)))
FIGURES["echelle_3087_placee"] = fig(*echelle(pas=Fr(1, 10), points=[
    (p, rf"${nom}$", 1, V, "south") for nom, p in DONNEES["echelle_3087"].items()]))

FIGURES["echelle_3092"] = fig(*echelle(pas=Fr(1, 10), points=[
    (p, rf"${nom}$", 1, V, "south") for nom, p in DONNEES["echelle_3092"].items()]))


def echelle_3102():
    e = DONNEES["echelle_3102"]
    T = echelle(pas=Fr(1, 10), y=2.0, titre="règle 1", points=[
        (e["Zoé1"], "Zoé", 1, V, "south"), (e["Yanis1"], "Yanis", 1, V, "south")])
    T += echelle(pas=Fr(1, 10), y=0.0, titre="règle 2", points=[(e["regle2"], "Zoé et Yanis", 1, V, "south")])
    return fig(*T)


FIGURES["echelle_3102"] = echelle_3102()


# ================================================================ courbes de fréquences
def simulation_bernoulli(p, n, graine):
    r = random.Random(graine)
    s, pts = 0, []
    for k in range(1, n + 1):
        s += r.random() < p
        pts.append((k, s / k))
    return pts


def lancers(graine, n, poids):
    return random.Random(graine).choices([1, 2, 3, 4, 5, 6], weights=poids, k=n)


DONNEES["sim_cours"] = simulation_bernoulli(5 / 8, 1000, 214)
for nom, (g, poids) in list(DONNEES["des_3094"].items()):
    DONNEES[f"lancers_{nom}"] = lancers(g, 600, poids)


def freq_six(seq):
    pts, s = [], 0
    for k, x in enumerate(seq, start=1):
        s += x == 6
        pts.append((k, s / k))
    return pts


def coords(pts, debut=1, pas_apres=None, seuil=60):
    garde = [(x, y) for x, y in pts if x >= debut and (pas_apres is None or x <= seuil or x % pas_apres == 0)]
    return " ".join(f"({x},{y:.4f})" for x, y in garde)


def courbe_cours():
    c = coords(DONNEES["sim_cours"], pas_apres=5, seuil=100)
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width=5.8cm, height=3.9cm, xmin=0, xmax=1000, ymin=0.4, ymax=1.05,
  scaled x ticks=false, scaled y ticks=false,
  xtick={{0,200,400,600,800,1000}}, xticklabels={{$0$,$200$,$400$,$600$,$800$,$1\,000$}},
  ytick={{0.4,0.5,0.6,0.7,0.8,0.9,1}}, yticklabels={{$0{{,}}4$,$0{{,}}5$,$0{{,}}6$,$0{{,}}7$,$0{{,}}8$,$0{{,}}9$,$1$}},
  xlabel={{nombre de tirages}}, ylabel={{fréquence du rouge}}]
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,0.625) -- (axis cs:1000,0.625);
\node[anchor=west, legendeV, font=\normalsize] at (axis cs:1000,0.625) {{$0{{,}}625$}};
\addplot[courbe, line width=1pt] coordinates {{{c}}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["frequences_cours"] = courbe_cours()


def courbes_3094(corrige=False):
    m = coords(freq_six(DONNEES["lancers_Malik"]), debut=2, pas_apres=3, seuil=60)
    n = coords(freq_six(DONNEES["lancers_Nora"]), debut=2, pas_apres=3, seuil=60)
    ligne = ""
    if corrige:
        ligne = (r"\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,0.16667) -- (axis cs:600,0.16667);" "\n"
                 r"\node[anchor=west, legendeV, font=\normalsize] at (axis cs:600,0.16667) {$\dfrac{1}{6} \approx 0{,}17$};" "\n"
                 r"\node[anchor=west, legendeV, font=\normalsize] at (axis cs:600,0.302) {$\approx 0{,}3$};")
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width=5.4cm, height=4.2cm, xmin=0, xmax=600, ymin=0, ymax=0.6,
  scaled x ticks=false, scaled y ticks=false,
  xtick={{0,100,200,300,400,500,600}},
  ytick={{0,0.1,0.2,0.3,0.4,0.5,0.6}}, yticklabels={{$0$,$0{{,}}1$,$0{{,}}2$,$0{{,}}3$,$0{{,}}4$,$0{{,}}5$,$0{{,}}6$}},
  xlabel={{nombre de lancers}}, ylabel={{fréquence du $6$}}]
{ligne}
\addplot[otOrange!85!black, line width=1pt] coordinates {{{n}}};
\addplot[courbe, line width=1pt] coordinates {{{m}}};
\node[anchor=south, font=\normalsize, text=otOrange!85!black, inner sep=1.5pt] at (axis cs:420,0.37) {{dé de Nora}};
\node[anchor=north, font=\normalsize, text=otNavy, inner sep=1.5pt] at (axis cs:420,0.115) {{dé de Malik}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["frequences_3094"] = courbes_3094()
FIGURES["frequences_3094_corrige"] = courbes_3094(corrige=True)


# ================================================================ barres (3089)
def barres_3089():
    W, H = 4.9, 3.2     # largeur et hauteur du cadre (y = 0 → 0 ; y = H → 0,6)
    k = H / 0.6
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for i in range(0, 7):
        v = i / 10
        L.append(rf"\draw[otRule!75,line width=0.35pt] (0,{v * k:.3f}) -- ({W},{v * k:.3f});")
        L.append(rf"\node[grad,anchor=east] at (-0.08,{v * k:.3f}) {{${dec(Fr(i, 10))}$}};")
    L.append(rf"\draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] (0,0) -- (0,{H + 0.35:.2f});")
    L.append(rf"\draw[otMuted,line width=0.6pt] (0,0) -- ({W},0);")
    L.append(rf"\node[grad,anchor=south west] at (-0.3,{H + 0.42:.2f}) {{fréquence de « pile »}};")
    for j, (nom, n, p) in enumerate(DONNEES["barres_3089"]):
        f = Fr(p, n)
        x = 0.8 + j * 2.0
        L.append(rf"\fill[otNavy!55,draw=otNavy,line width=0.6pt] ({x:.2f},0) rectangle ({x + 0.9:.2f},{float(f) * k:.3f});")
        L.append(rf"\node[legende,anchor=north,align=center] at ({x + 0.45:.2f},-0.12) {{{nom}\\[-2pt]{{\small ${n}$ lancers}}}};")
        L.append(rf"\node[legende,anchor=north west,text=otNavy] at ({x + 0.95:.2f},{float(f) * k - 0.04:.3f}) {{${dec(f)}$}};")
    L.append(rf"\draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (0,{0.5 * k:.3f}) -- ({W},{0.5 * k:.3f});")
    L.append(rf"\node[legendeV,anchor=west,font=\normalsize,align=left] at ({W + 0.05},{0.5 * k:.3f}) {{probabilité\\$0{{,}}5$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["barres_3089"] = barres_3089()
