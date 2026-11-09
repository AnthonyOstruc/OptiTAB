# -*- coding: utf-8 -*-
"""Figures du formulaire « Second degré »."""


def panneau(dx, titre, expr, racines, note=None):
    """Petit repère (axe des abscisses seul) avec une parabole tournée vers le haut."""
    lignes = [
        rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2mm]}}] ({dx - 1.3},0) -- ({dx + 1.3},0);",
        rf"  \draw[courbe,domain=-1.15:1.15,samples=80] plot ({{{dx}+\x}},{{{expr}}});",
        rf"  \node[anchor=south] at ({dx},1.8) {{{titre}}};",
    ]
    for x, ancre, tex in racines:
        lignes.append(rf"  \fill[otGreenDark] ({dx + x},0) circle (2.2pt);")
        lignes.append(rf"  \node[anchor={ancre},text=otGreenDark,inner sep=1.5pt] at ({dx + x},-0.06) {{${tex}$}};")
    if note:
        lignes.append(rf"  \node[note,anchor=north,fill=none] at ({dx},-0.12) {{{note}}};")
    return "\n".join(lignes)


TROIS_CAS = "\n".join([
    r"\begin{tikzpicture}",
    panneau(0, r"$\Delta > 0$", r"1.1*\x*\x-0.75", [(-0.826, "north east", "x_1"), (0.826, "north west", "x_2")]),
    panneau(3.0, r"$\Delta = 0$", r"1.1*\x*\x", [(0, "north", "x_0")]),
    panneau(6.0, r"$\Delta < 0$", r"1.1*\x*\x+0.3", [], "aucune racine"),
    r"\end{tikzpicture}",
])

PARABOLE_SOMMET = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-2.4, xmax=4.4, ymin=-2.9, ymax=2.9,
  xtick=\empty, ytick=\empty]
  \draw[seuil] (axis cs:1,-2.9) -- (axis cs:1,2.6);
  \addplot[courbe, domain=-1.75:3.75] {0.5*(x-1)^2-2};
  \pnt{1}{-2}
  \fill[otGreenDark] (axis cs:-1,0) circle (2.3pt);
  \fill[otGreenDark] (axis cs:3,0) circle (2.3pt);
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (axis cs:-1.05,-0.05) {$x_1$};
  \node[anchor=north west,text=otGreenDark,inner sep=1.5pt] at (axis cs:3.05,-0.05) {$x_2$};
  \node[anchor=north,text=otNavy] at (axis cs:1,-2.08) {$S(\alpha\,;\beta)$};
  \node[anchor=west,text=otOrange!75!black] at (axis cs:1.08,2.2) {$x = \alpha$};
  \node[anchor=east,text=otNavy] at (axis cs:-1.7,1.6) {$\mathcal{P}$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"trois_cas": TROIS_CAS, "parabole_sommet": PARABOLE_SOMMET}
