# -*- coding: utf-8 -*-
"""Figures de la table « Cercle trigonométrique » : cercle complet, signes par quart."""
from fractions import Fraction

R = 3.0
DEGRES = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def radian(d):
    f = Fraction(d, 180)
    if f == 0:
        return "0"
    num = "" if f.numerator == 1 else str(f.numerator)
    if f.denominator == 1:
        return num + r"\pi"
    return rf"\dfrac{{{num}\pi}}{{{f.denominator}}}"


def axes(r):
    return "\n".join([
        rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] ({-r - 0.5},0) -- ({r + 0.6},0);",
        rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] (0,{-r - 0.5}) -- (0,{r + 0.6});",
        rf"  \draw[otNavy,line width=1.1pt] (0,0) circle ({r});",
        r"  \fill[otInk] (0,0) circle (1.3pt);",
    ])


# étiquettes posées sur un axe : décalées pour ne pas couper le trait
SPECIAUX = {
    0: "anchor=south west,xshift=3pt,yshift=1pt",
    90: "anchor=south west,xshift=3pt,yshift=1pt",
    180: "anchor=south east,xshift=-3pt,yshift=1pt",
    270: "anchor=north west,xshift=3pt,yshift=-1pt",
}
SPECIAUX_DEG = {
    0: "anchor=north east,xshift=-3pt,yshift=-2pt",
    90: "anchor=north east,xshift=-3pt,yshift=-3pt",
    180: "anchor=north west,xshift=3pt,yshift=-2pt",
    270: "anchor=south east,xshift=-3pt,yshift=3pt",
}


def cercle():
    l = [r"\begin{tikzpicture}", axes(R)]
    for d in DEGRES:
        l.append(rf"  \fill[otNavy] ({d}:{R}) circle (2.3pt);")
        if d in SPECIAUX:
            l.append(rf"  \node[{SPECIAUX[d]},text=otNavy,font=\large] at ({d}:{R}) {{${radian(d)}$}};")
            l.append(rf"  \node[{SPECIAUX_DEG[d]},text=otMuted!85!black] at ({d}:{R}) {{${d}^\circ$}};")
        else:
            l.append(rf"  \node[anchor={d + 180},text=otNavy,font=\large,inner sep=2pt] at ({d}:{R + 0.1}) {{${radian(d)}$}};")
            l.append(rf"  \node[anchor={d},text=otMuted!85!black,inner sep=1.5pt] at ({d}:{R - 0.12}) {{${d}^\circ$}};")
    l.append(r"  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (0,0) {$O$};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


R2 = 2.0
SIGNES = r"""
\begin{tikzpicture}
  \fill[otGreen!20] (0,0) -- (#R,0) arc (0:90:#R) -- cycle;
  \fill[otOrange!22] (0,0) -- (0,#R) arc (90:180:#R) -- cycle;
  \fill[otRed!14] (0,0) -- (-#R,0) arc (180:270:#R) -- cycle;
  \fill[otSky] (0,0) -- (0,-#R) arc (270:360:#R) -- cycle;
#AXES
  \node[align=center,text=otInk] at (45:1.15) {$\cos > 0$\\$\sin > 0$};
  \node[align=center,text=otInk] at (135:1.15) {$\cos < 0$\\$\sin > 0$};
  \node[align=center,text=otInk] at (225:1.15) {$\cos < 0$\\$\sin < 0$};
  \node[align=center,text=otInk] at (315:1.15) {$\cos > 0$\\$\sin < 0$};
  \node[anchor=north west,text=otMuted,font=\small] at (#R+0.15,-0.05) {cos};
  \node[anchor=south east,text=otMuted,font=\small] at (-0.05,#R+0.15) {sin};
\end{tikzpicture}"""

FIGURES = {
    "cercle_complet": cercle(),
    "signes_quarts": SIGNES.replace("#AXES", axes(R2)).replace("#R", str(R2)),
}
