# -*- coding: utf-8 -*-
"""Figures de la page « Formulaire de mécanique : prépa et licence ».

    PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/physique-chimie/formulaire-mecanique-prepa --planche --jobs 1

Conventions (rigueur des schémas) : vitesses en bleu marine, forces en orange,
vecteurs de base en gris ; chaque force part de son point d'application ; texte
jamais posé sur un trait. Le graphe d'énergie potentielle effective est tracé en
unités réduites : Ep,eff(r) = -2/r + 1/r², minimum -1 en r = 1 (orbite circulaire).
"""
from math import cos, radians, sin, sqrt

PREAMBULE_EXTRA = r"""
\tikzset{
  leg/.style={font=\otRegular\fontsize{9.5}{11.5}\selectfont,text=otInk,inner sep=1.4pt,align=center},
  legG/.style={leg,text=otMuted},
  legN/.style={leg,text=otNavy},
  legO/.style={leg,text=otOrange!80!black},
  pt/.style={circle,fill=otInk,inner sep=0pt,minimum size=4pt},
  vecN/.style={otNavy,line width=1.2pt,-{Stealth[length=2.6mm]}},
  vecO/.style={otOrange!85!black,line width=1.2pt,-{Stealth[length=2.6mm]}},
  vecG/.style={otMuted,line width=1pt,-{Stealth[length=2.4mm]}},
  axe/.style={otMuted,line width=0.6pt,-{Stealth[length=2.2mm]}},
  trajet/.style={otMuted!80,line width=0.6pt,dash pattern=on 2.5pt off 1.5pt},
  guide/.style={otMuted!70,line width=0.45pt,dash pattern=on 1.5pt off 1.5pt},
}
"""

DEBUT, FIN = "\\begin{tikzpicture}\n", "\\end{tikzpicture}"
FIGURES = {}


def f(x):
    return f"{x:.3f}"


def P(x, y):
    return f"({f(x)},{f(y)})"


def pointe_vers(x, y):
    """Symbole « champ vers le lecteur » (cercle pointé)."""
    return f"\\draw[otNavy!70,line width=0.6pt] {P(x, y)} circle (0.13);\\fill[otNavy!70] {P(x, y)} circle (0.035);\n"


# ====================================================================== 1. coordonnées polaires
def coordonnees_polaires():
    r, th = 3.0, radians(35)
    M = (r * cos(th), r * sin(th))
    ur = (cos(th), sin(th))
    ut = (-sin(th), cos(th))
    s = DEBUT
    s += "\\draw[axe] (-0.3,0) -- (4.3,0) node[legG,anchor=north] {$x$};\n"
    s += "\\draw[axe] (0,-0.3) -- (0,3.0) node[legG,anchor=east] {$y$};\n"
    s += "\\node[legG,anchor=north east] at (-0.05,-0.05) {$O$};\n"
    s += f"\\draw[guide] (0,0) -- {P(*M)};\n"
    s += f"\\node[legG,anchor=south east] at {P(M[0] * 0.55 - 0.05, M[1] * 0.55 + 0.05)} {{$r$}};\n"
    s += f"\\draw[otMuted,line width=0.6pt,-{{Stealth[length=1.8mm]}}] (0.9,0) arc[start angle=0,end angle=35,radius=0.9];\n"
    s += f"\\node[legG] at {P(1.18 * cos(th / 2), 1.18 * sin(th / 2))} {{$\\theta$}};\n"
    s += f"\\node[pt] at {P(*M)} {{}};\n"
    s += f"\\node[leg,anchor=north west] at {P(M[0] + 0.08, M[1] - 0.08)} {{$M$}};\n"
    L = 1.0
    s += f"\\draw[vecN] {P(*M)} -- {P(M[0] + L * ur[0], M[1] + L * ur[1])};\n"
    s += f"\\node[legN,anchor=west] at {P(M[0] + L * ur[0] + 0.05, M[1] + L * ur[1])} {{$\\vec{{u}}_r$}};\n"
    s += f"\\draw[vecO] {P(*M)} -- {P(M[0] + L * ut[0], M[1] + L * ut[1])};\n"
    s += f"\\node[legO,anchor=south] at {P(M[0] + L * ut[0], M[1] + L * ut[1] + 0.05)} {{$\\vec{{u}}_\\theta$}};\n"
    return s + FIN


FIGURES["coordonnees_polaires"] = coordonnees_polaires()


# ====================================================================== 2. énergie potentielle effective
def racines(Em):
    """r tels que -2/r + 1/r² = Em (Em r² + 2 r - 1 = 0)."""
    if Em == 0:
        return [0.5]
    d = sqrt(4 + 4 * Em)
    return sorted(x for x in ((-2 + d) / (2 * Em), (-2 - d) / (2 * Em)) if x > 0)


E_LIE, E_DIFF = -0.6, 0.3
R1, R2 = racines(E_LIE)
(R3,) = racines(E_DIFF)
assert abs(R1 - 0.6127) < 1e-3 and abs(R2 - 2.7206) < 1e-3 and abs(R3 - 0.4673) < 1e-3


def energie_potentielle_effective():
    s = DEBUT
    s += r"""\begin{axis}[otWeb, width=7.2cm, height=5.4cm, xmin=0, xmax=4, ymin=-1.45, ymax=1.3,
  axis lines=left, xtick=\empty, ytick={0}, yticklabels={$0$}, clip=false,
  xlabel={$r$}, ylabel={$E$},
  every axis x label/.style={at={(current axis.right of origin)},anchor=north west,text=otMuted},
  every axis y label/.style={at={(current axis.north west)},anchor=south,text=otMuted}]
"""
    s += "\\addplot[otMuted!60,line width=0.4pt,domain=0:4] {0};\n"
    s += "\\addplot[otNavy,line width=1.3pt,domain=0.40:4,samples=220] {-2/x + 1/x^2};\n"
    s += "\\node[legN,anchor=west] at (axis cs:0.55,1.05) {$E_{p,\\mathrm{eff}}(r)$};\n"
    # état lié : mouvement entre r_min et r_max
    s += f"\\addplot[otOrange!85!black,line width=1.1pt,dash pattern=on 3pt off 1.5pt] coordinates {{({f(R1)},{E_LIE}) ({f(R2)},{E_LIE})}};\n"
    s += f"\\draw[guide] (axis cs:{f(R1)},{E_LIE}) -- (axis cs:{f(R1)},-1.45);\n"
    s += f"\\draw[guide] (axis cs:{f(R2)},{E_LIE}) -- (axis cs:{f(R2)},-1.45);\n"
    s += f"\\node[legG,anchor=north] at (axis cs:{f(R1)},-1.47) {{$r_{{\\min}}$}};\n"
    s += f"\\node[legG,anchor=north] at (axis cs:{f(R2)},-1.47) {{$r_{{\\max}}$}};\n"
    s += f"\\node[legO,anchor=north west,align=left] at (axis cs:{f(R2 + 0.08)},{E_LIE - 0.04}) {{$E_m < 0$ :\\\\état lié}};\n"
    # état de diffusion
    s += f"\\addplot[otGreenDark,line width=1.1pt,dash pattern=on 3pt off 1.5pt] coordinates {{({f(R3)},{E_DIFF}) (4,{E_DIFF})}};\n"
    s += f"\\node[leg,text=otGreenDark,anchor=south east] at (axis cs:4,{E_DIFF + 0.04}) {{$E_m > 0$ : état de diffusion}};\n"
    # minimum : orbite circulaire
    s += "\\fill[otInk] (axis cs:1,-1) circle (2.2pt);\n"
    s += "\\node[leg,anchor=north west] at (axis cs:1.08,-1.06) {orbite circulaire};\n"
    s += "\\end{axis}\n"
    return s + FIN


FIGURES["energie_potentielle_effective"] = energie_potentielle_effective()


# ====================================================================== 3. particule chargée dans un champ magnétique
def particule_champ_magnetique():
    R = 1.6
    s = DEBUT
    s += f"\\draw[trajet] (0,0) circle ({R});\n"
    s += "\\node[pt] at (0,0) {};\n\\node[legG,anchor=south east] at (-0.06,0.06) {$C$};\n"
    a = radians(235)
    s += f"\\draw[guide] (0,0) -- {P(R * cos(a), R * sin(a))};\n"
    s += f"\\node[legG,anchor=north west] at {P(R * cos(a) * 0.5 + 0.06, R * sin(a) * 0.5 - 0.06)} {{$R$}};\n"
    # champ vers le lecteur
    for x, y in [(-2.6, 1.9), (2.6, 1.9), (-2.6, -2.15), (2.6, -2.15), (2.6, 0.15), (-2.6, 0.15)]:
        s += pointe_vers(x, y)
    s += "\\node[legN,anchor=west] at (-2.4,-2.15) {$\\vec{B}$ vers le lecteur};\n"
    # charge positive au sommet : vitesse vers la droite, force q v ∧ B vers le centre (sens horaire)
    s += f"\\node[pt] at (0,{R}) {{}};\n"
    s += f"\\node[leg,anchor=south east] at (-0.08,{R + 0.06}) {{$q > 0$}};\n"
    s += f"\\draw[vecN] (0,{R}) -- (1.25,{R});\n\\node[legN,anchor=south] at (1.0,{R + 0.04}) {{$\\vec{{v}}$}};\n"
    s += f"\\draw[vecO] (0,{R}) -- (0,{R - 0.95});\n\\node[legO,anchor=west] at (0.08,{R - 0.62}) {{$\\vec{{F}}$}};\n"
    # sens de parcours (horaire)
    s += f"\\draw[otMuted,line width=0.6pt,-{{Stealth[length=2mm]}}] (20:{R + 0.3}) arc[start angle=20,end angle=-20,radius={R + 0.3}];\n"
    return s + FIN


FIGURES["particule_champ_magnetique"] = particule_champ_magnetique()


# ====================================================================== 4. pendule pesant
def pendule_pesant():
    th = radians(28)
    L, d = 3.0, 1.9
    u = (sin(th), -cos(th))                  # direction de la tige, depuis O
    G = (d * u[0], d * u[1])
    B = (L * u[0], L * u[1])
    n = (cos(th), sin(th))                   # normale à la tige
    s = DEBUT
    s += pointe_vers(0, 0)
    s += "\\node[legN,anchor=south] at (0,0.18) {axe $\\Delta$};\n"
    s += "\\node[legG,anchor=east] at (-0.2,0) {$O$};\n"
    s += f"\\draw[guide] (0,-0.15) -- (0,{-L - 0.2});\n"
    # le solide : une plaque allongée autour de la tige
    w = 0.12
    c = [(0.15 * u[0] + w * n[0], 0.15 * u[1] + w * n[1]), (B[0] + w * n[0], B[1] + w * n[1]),
         (B[0] - w * n[0], B[1] - w * n[1]), (0.15 * u[0] - w * n[0], 0.15 * u[1] - w * n[1])]
    s += f"\\draw[otNavy!60,line width=0.9pt,rounded corners=2pt] {' -- '.join(P(*p) for p in c)} -- cycle;\n"
    s += f"\\draw[otMuted,line width=0.6pt,-{{Stealth[length=1.8mm]}}] (0,-1.0) arc[start angle=-90,end angle={-90 + 28},radius=1.0];\n"
    s += f"\\node[legG] at {P(1.32 * sin(th / 2), -1.32 * cos(th / 2))} {{$\\theta$}};\n"
    # distance OG, à côté de la plaque
    off = 0.55
    s += f"\\draw[otMuted,line width=0.55pt,{{Stealth[length=1.6mm]}}-{{Stealth[length=1.6mm]}}] {P(off * n[0], off * n[1])} -- {P(G[0] + off * n[0], G[1] + off * n[1])};\n"
    s += f"\\node[legG,anchor=south west] at {P(G[0] / 2 + (off + 0.05) * n[0], G[1] / 2 + (off + 0.05) * n[1])} {{$d$}};\n"
    # centre de gravité et poids
    s += f"\\node[pt] at {P(*G)} {{}};\n"
    s += f"\\node[leg,anchor=east] at {P(G[0] - 0.36, G[1] + 0.05)} {{$G$}};\n"
    s += f"\\draw[vecO] {P(*G)} -- {P(G[0], G[1] - 1.15)};\n"
    s += f"\\node[legO,anchor=east] at {P(G[0] - 0.08, G[1] - 1.0)} {{$\\vec{{P}}$}};\n"
    return s + FIN


FIGURES["pendule_pesant"] = pendule_pesant()
