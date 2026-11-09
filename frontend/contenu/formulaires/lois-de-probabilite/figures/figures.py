# -*- coding: utf-8 -*-
"""Figures du formulaire « Lois de probabilité ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/formulaires/lois-de-probabilite --planche --jobs 1
"""
from math import comb, exp, factorial

TITRE = r"title style={font=\otMedium\fontsize{9.5}{11}\selectfont, text=otNavy, yshift=2pt}"


def barres(x, titre, points, ymax, yticks, xticks, couleur="otNavy", largeur=3.7, bar=7):
    """Diagramme en barres d'une loi discrète (petit panneau placé à l'abscisse x)."""
    coords = " ".join(f"({k},{p:.5f})" for k, p in points)
    ytl = ",".join("$" + str(v).replace(".", "{,}") + "$" for v in yticks)
    return rf"""
\begin{{axis}}[otBarres, at={{({x}cm,0)}}, width={largeur}cm, height=3.2cm, bar width={bar}pt, ymax={ymax},
  enlarge x limits=0.08, xtick={{{",".join(map(str, xticks))}}}, ytick={{{",".join(map(str, yticks))}}}, yticklabels={{{ytl}}},
  title={{{titre}}}, {TITRE}]
  \addplot[fill={couleur}!60, draw={couleur}] coordinates {{{coords}}};
\end{{axis}}"""


def figure(*morceaux):
    return r"\begin{tikzpicture}" + "".join(morceaux) + "\n\\end{tikzpicture}"


BERNOULLI_UNIFORME = figure(
    barres(0, r"Bernoulli $\mathcal{B}(0{,}3)$", [(0, 0.7), (1, 0.3)], 0.8, [0.3, 0.7], [0, 1], bar=14),
    barres(4.7, r"Uniforme sur $\{1, \ldots, 6\}$", [(k, 1 / 6) for k in range(1, 7)], 0.25, [0.1, 0.2], [1, 2, 3, 4, 5, 6], "otGreenDark", bar=9),
)

BINOMIALE = figure(
    barres(0, r"$\mathcal{B}(10\,;0{,}3)$", [(k, comb(10, k) * 0.3 ** k * 0.7 ** (10 - k)) for k in range(11)], 0.3, [0.1, 0.2], [0, 2, 4, 6, 8, 10], bar=5),
    barres(4.7, r"$\mathcal{B}(10\,;0{,}5)$", [(k, comb(10, k) * 0.5 ** 10) for k in range(11)], 0.3, [0.1, 0.2], [0, 2, 4, 6, 8, 10], "otGreenDark", bar=5),
)

GEOMETRIQUE = figure(
    barres(0, r"Géométrique $\mathcal{G}(0{,}3)$", [(k, 0.3 * 0.7 ** (k - 1)) for k in range(1, 13)], 0.35, [0.1, 0.2, 0.3], [1, 3, 5, 7, 9, 11], largeur=7, bar=9),
)

POISSON = figure(
    barres(0, r"Poisson $\mathcal{P}(1)$", [(k, exp(-1) / factorial(k)) for k in range(9)], 0.42, [0.1, 0.2, 0.3], [0, 2, 4, 6, 8], bar=6),
    barres(4.7, r"Poisson $\mathcal{P}(4)$", [(k, exp(-4) * 4 ** k / factorial(k)) for k in range(13)], 0.42, [0.1, 0.2, 0.3], [0, 2, 4, 6, 8, 10, 12], "otGreenDark", bar=4),
)

PANNEAU = r"""
\begin{axis}[otWeb, at={(#Xcm,0)}, width=3.7cm, height=3.2cm, xlabel={}, ylabel={}, clip=true, clip mode=individual,
  title={#T}, """ + TITRE + r""", #O]
#C
\end{axis}"""


def panneau(x, titre, options, corps):
    return PANNEAU.replace("#X", str(x)).replace("#T", titre).replace("#O", options).replace("#C", corps)


UNIFORME_EXPONENTIELLE = figure(
    panneau(0, r"Uniforme sur $[1\,;3]$", r"xmin=-0.4, xmax=4.2, ymin=-0.08, ymax=0.75, xtick={1,3}, ytick={0.5}, yticklabels={$\frac{1}{2}$}", r"""
  \fill[otSky] (axis cs:1,0) rectangle (axis cs:3,0.5);
  \draw[courbe] (axis cs:-0.4,0) -- (axis cs:1,0);
  \draw[courbe] (axis cs:1,0.5) -- (axis cs:3,0.5);
  \draw[courbe] (axis cs:3,0) -- (axis cs:4.2,0);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,0.5);
  \draw[guide] (axis cs:3,0) -- (axis cs:3,0.5);"""),
    panneau(4.8, r"Exponentielle $\mathcal{E}(1)$", r"xmin=-0.4, xmax=4.4, ymin=-0.08, ymax=1.15, xtick={1,2,3,4}, ytick={1}", r"""
  \addplot[fill=otSky, draw=none, domain=0:1, samples=60] {exp(-x)} \closedcycle;
  \addplot[courbe2, domain=0:4.4, samples=120] {exp(-x)};
  \draw[otGreen,line width=1.35pt] (axis cs:-0.4,0) -- (axis cs:0,0);
  \node[text=otNavy,inner sep=1pt] at (axis cs:0.45,0.2) {\small$63\,\%$};"""),
)

NORMALES = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.6cm, xmin=-5.2, xmax=5.2, ymin=0, ymax=0.85,
  xtick={-4,-2,2,4}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \addplot[otGreenDark, line width=1.2pt, domain=-5.2:5.2, samples=220] {exp(-x^2/(2*0.25))/(0.5*sqrt(2*pi))};
  \addplot[courbe, domain=-5.2:5.2, samples=220] {exp(-x^2/2)/sqrt(2*pi)};
  \addplot[otOrange!85!black, line width=1.2pt, domain=-5.2:5.2, samples=220] {exp(-x^2/8)/(2*sqrt(2*pi))};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:0.55,0.72) {$\sigma = 0{,}5$};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:1.35,0.3) {$\sigma = 1$};
  \node[anchor=west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.75,0.14) {$\sigma = 2$};
\end{axis}
\end{tikzpicture}"""

CENTREE_REDUITE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.6cm, xmin=-3.8, xmax=3.8, ymin=0, ymax=0.46,
  xtick={-1.96,0,1.96}, xticklabels={}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \addplot[fill=otSky, draw=none, domain=-1.96:1.96, samples=160] {exp(-x^2/2)/sqrt(2*pi)} \closedcycle;
  \addplot[fill=otOrange!25, draw=none, domain=-3.8:-1.96, samples=80] {exp(-x^2/2)/sqrt(2*pi)} \closedcycle;
  \addplot[fill=otOrange!25, draw=none, domain=1.96:3.8, samples=80] {exp(-x^2/2)/sqrt(2*pi)} \closedcycle;
  \draw[otNavy!50,line width=0.5pt] (axis cs:-1.96,0) -- (axis cs:-1.96,0.0584);
  \draw[otNavy!50,line width=0.5pt] (axis cs:1.96,0) -- (axis cs:1.96,0.0584);
  \addplot[courbe, domain=-3.8:3.8, samples=200] {exp(-x^2/2)/sqrt(2*pi)};
  \node[text=otNavy] at (axis cs:0,0.13) {$0{,}95$};
  \node[anchor=south,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:-2.75,0.03) {$0{,}025$};
  \node[anchor=south,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.75,0.03) {$0{,}025$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {
    "bernoulli_uniforme": BERNOULLI_UNIFORME,
    "binomiales": BINOMIALE,
    "geometrique": GEOMETRIQUE,
    "poisson": POISSON,
    "uniforme_exponentielle": UNIFORME_EXPONENTIELLE,
    "normales": NORMALES,
    "centree_reduite": CENTREE_REDUITE,
}

XLAB = {
    "centree_reduite": [(-1.96, "c", r"-1{,}96"), (0, "c", r"0"), (1.96, "c", r"1{,}96")],
}
