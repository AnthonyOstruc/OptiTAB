# -*- coding: utf-8 -*-
"""Figures du formulaire « Formules de physique-chimie du brevet ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/formules-physique-chimie-brevet --planche
"""

NOM = r"\node[anchor=north,font=\otMedium\fontsize{10.5}{12}\selectfont,text=otMuted] at (#1) {#2};"


def nom(x, y, texte):
    return NOM.replace("#1", f"{x},{y}").replace("#2", texte)


# ---------------------------------------------------------------- triangles
# Le « triangle » : on cache la grandeur cherchée, ce qui reste donne le calcul.
def triangle(x0, haut, gauche, droite, titre, formule):
    l, h, mi = 2.8, 2.4, 1.05
    xm = x0 + l / 2
    xg = x0 + (l / 2) * mi / h
    xd = x0 + l - (l / 2) * mi / h
    return (
        rf"""
  \fill[otSky] ({x0},0) -- ({x0 + l},0) -- ({xm},{h}) -- cycle;
  \fill[otGreen!14] ({x0},0) -- ({x0 + l},0) -- ({xd},{mi}) -- ({xg},{mi}) -- cycle;
  \draw[geoTrait] ({x0},0) -- ({x0 + l},0) -- ({xm},{h}) -- cycle;
  \draw[geoTrait] ({xg},{mi}) -- ({xd},{mi});
  \draw[geoTrait] ({xm},0) -- ({xm},{mi});
  \node[font=\LARGE,text=otNavy] at ({xm},1.53) {{${haut}$}};
  \node[font=\LARGE,text=otGreenDark] at ({x0 + 0.86},0.47) {{${gauche}$}};
  \node[font=\LARGE,text=otGreenDark] at ({x0 + l - 0.86},0.47) {{${droite}$}};
"""
        + nom(xm, -0.22, titre)
        + rf"""
  \node[anchor=north,text=otInk] at ({xm},-0.72) {{${formule}$}};"""
    )


TRIANGLES_FORMULES = (
    r"""
\begin{tikzpicture}"""
    + triangle(0, "d", "v", "t", "Vitesse", r"d = v \times t")
    + triangle(3.9, "U", "R", "I", "Loi d’Ohm", r"U = R \times I")
    + triangle(7.8, "E", "P", "t", "Énergie", r"E = P \times t")
    + r"""
\end{tikzpicture}"""
)


# ---------------------------------------------------------------- circuits
# Symboles normalisés du collège : pile (grand trait = borne +), lampe (cercle
# barré d'une croix), points de jonction. Les fils s'arrêtent au bord des symboles.
R_LAMPE = 0.27


def fil(*points):
    return r"  \draw[otInk,line width=0.9pt] " + " -- ".join(f"({x},{y})" for x, y in points) + ";\n"


def lampe(x, y, etiquette, cote="above"):
    d = R_LAMPE * 0.7071
    pos = {"above": (0, R_LAMPE + 0.08, "south"), "below": (0, -R_LAMPE - 0.08, "north"),
           "right": (R_LAMPE + 0.1, 0, "west"), "left": (-R_LAMPE - 0.1, 0, "east")}[cote]
    return (
        rf"""  \draw[otInk,line width=0.9pt,fill=white] ({x},{y}) circle ({R_LAMPE});
  \draw[otInk,line width=0.75pt] ({x - d},{y - d}) -- ({x + d},{y + d});
  \draw[otInk,line width=0.75pt] ({x - d},{y + d}) -- ({x + d},{y - d});
  \node[anchor={pos[2]},text=otInk,font=\large] at ({x + pos[0]},{y + pos[1]}) {{$\mathrm{{{etiquette}}}$}};
"""
    )


def pile_verticale(x, y):
    """Pile sur un fil vertical : grand trait fin (+) en haut, petit trait épais (−) en bas."""
    return (
        rf"""  \draw[otInk,line width=0.9pt] ({x - 0.32},{y + 0.09}) -- ({x + 0.32},{y + 0.09});
  \draw[otInk,line width=2.4pt] ({x - 0.15},{y - 0.09}) -- ({x + 0.15},{y - 0.09});
  \node[anchor=east,text=otInk,font=\small] at ({x - 0.36},{y + 0.27}) {{$+$}};
"""
    )


def jonction(x, y):
    return rf"  \fill[otInk] ({x},{y}) circle (2pt);" + "\n"


def courant(x, y, sens, etiquette, cote):
    """Flèche du sens du courant sur un fil, avec son nom à côté."""
    dx, dy = {"droite": (0.18, 0), "gauche": (-0.18, 0), "bas": (0, -0.18), "haut": (0, 0.18)}[sens]
    ancre, ex, ey = {"above": ("south", 0, 0.14), "below": ("north", 0, -0.14),
                     "right": ("west", 0.16, 0), "left": ("east", -0.16, 0)}[cote]
    return (
        rf"""  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] ({x - dx},{y - dy}) -- ({x + dx},{y + dy});
  \node[anchor={ancre},text=otOrange!75!black,font=\large] at ({x + ex},{y + ey}) {{${etiquette}$}};
"""
    )


def circuit_serie(x0):
    L, H, yp = 3.4, 2.3, 1.15
    s = ""
    # côté gauche : pile
    s += fil((x0, yp - 0.09), (x0, 0), (x0 + L, 0), (x0 + L, H), (x0 + 2.4 + R_LAMPE, H))
    s += fil((x0 + 2.4 - R_LAMPE, H), (x0 + 1.1 + R_LAMPE, H))
    s += fil((x0 + 1.1 - R_LAMPE, H), (x0, H), (x0, yp + 0.09))
    s += pile_verticale(x0, yp)
    s += lampe(x0 + 1.1, H, "L_1")
    s += lampe(x0 + 2.4, H, "L_2")
    s += courant(x0 + 1.7, 0, "gauche", "I", "below")
    s += courant(x0 + L, 1.15, "bas", "I", "right")
    s += nom(x0 + L / 2, -0.62, "En série")
    return s


def circuit_derivation(x0):
    L, xm, H, yp = 4.0, 2.1, 2.3, 1.15
    s = ""
    s += fil((x0, yp - 0.09), (x0, 0), (x0 + L, 0), (x0 + L, yp - R_LAMPE))
    s += fil((x0 + L, yp + R_LAMPE), (x0 + L, H), (x0, H), (x0, yp + 0.09))
    s += fil((x0 + xm, 0), (x0 + xm, yp - R_LAMPE))
    s += fil((x0 + xm, yp + R_LAMPE), (x0 + xm, H))
    s += pile_verticale(x0, yp)
    s += lampe(x0 + xm, yp, "L_1", "left")
    s += lampe(x0 + L, yp, "L_2", "right")
    s += jonction(x0 + xm, H) + jonction(x0 + xm, 0)
    s += courant(x0 + 1.0, H, "droite", "I", "above")
    s += courant(x0 + xm, 1.85, "bas", "I_1", "right")
    s += courant(x0 + L, 1.85, "bas", "I_2", "left")
    s += nom(x0 + L / 2, -0.62, "En dérivation")
    return s


CIRCUITS = (
    r"""
\begin{tikzpicture}
"""
    + circuit_serie(0)
    + circuit_derivation(5.1)
    + r"""\end{tikzpicture}"""
)


# ---------------------------------------------------------------- échelle de pH
U = 0.72  # largeur d'une unité de pH (cm)


def graduations():
    s = ""
    for k in range(15):
        x = round(k * U, 3)
        s += rf"  \draw[otInk,line width=0.6pt] ({x},0) -- ({x},-0.12);" + "\n"
        s += rf"  \node[anchor=north,font=\otRegular\fontsize{{10}}{{11}}\selectfont,text=otInk] at ({x},-0.14) {{{k}}};" + "\n"
    return s


def exemple(ph, texte):
    x = round(ph * U, 3)
    return (
        rf"""  \draw[otMuted,line width=0.6pt,-{{Stealth[length=1.6mm]}}] ({x},-1.02) -- ({x},-0.62);
  \node[anchor=north,align=center,font=\otRegular\fontsize{{10}}{{11.5}}\selectfont,text=otMuted] at ({x},-1.06) {{{texte}}};
"""
    )


ECHELLE_PH = (
    r"""
\begin{tikzpicture}
  \shade[left color=otRed!80, right color=otOrange!60] (0,0) rectangle (""" + f"{7 * U - 0.02}" + r""",0.42);
  \fill[otGreen!70] (""" + f"{7 * U - 0.06}" + r""",0) rectangle (""" + f"{7 * U + 0.06}" + r""",0.42);
  \shade[left color=otSky, right color=otNavy!75] (""" + f"{7 * U + 0.02}" + r""",0) rectangle (""" + f"{14 * U}" + r""",0.42);
  \draw[otInk,line width=0.6pt] (0,0) rectangle (""" + f"{14 * U}" + r""",0.42);
"""
    + graduations()
    + rf"""  \draw[decorate,decoration={{brace,amplitude=4pt}},otRed!80!black,line width=0.8pt] (0.05,0.56) -- ({7 * U - 0.12},0.56);
  \node[anchor=south,align=center,text=otRed!80!black,font=\otMedium\fontsize{{11}}{{13}}\selectfont] at ({3.5 * U},0.74) {{Solution acide\\[1pt]\otRegular\fontsize{{9.5}}{{11}}\selectfont ions $\mathrm{{H^+}}$ majoritaires}};
  \node[anchor=south,text=otGreenDark,font=\otMedium\fontsize{{11}}{{13}}\selectfont] at ({7 * U},1.62) {{Neutre}};
  \draw[otGreenDark,line width=0.7pt] ({7 * U},0.5) -- ({7 * U},1.58);
  \draw[decorate,decoration={{brace,amplitude=4pt}},otNavy,line width=0.8pt] ({7 * U + 0.12},0.56) -- ({14 * U - 0.05},0.56);
  \node[anchor=south,align=center,text=otNavy,font=\otMedium\fontsize{{11}}{{13}}\selectfont] at ({10.5 * U},0.74) {{Solution basique\\[1pt]\otRegular\fontsize{{9.5}}{{11}}\selectfont ions $\mathrm{{OH^-}}$ majoritaires}};
"""
    + exemple(2, r"jus de\\citron")
    + exemple(7, r"eau\\pure")
    + exemple(12, r"eau de\\Javel")
    + r"""\end{tikzpicture}"""
)


FIGURES = {
    "triangles_formules": TRIANGLES_FORMULES,
    "circuits_serie_derivation": CIRCUITS,
    "echelle_ph": ECHELLE_PH,
}
