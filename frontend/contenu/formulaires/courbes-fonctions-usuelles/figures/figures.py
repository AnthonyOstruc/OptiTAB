# -*- coding: utf-8 -*-
"""Figures du formulaire « Courbes des fonctions usuelles ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/formulaires/courbes-fonctions-usuelles --planche --jobs 1
"""

PI = 3.14159265


def panneau(x, titre, fenetre, ticks, corps):
    """Un petit repère (3,7 cm × 3,4 cm) placé à l'abscisse x (en cm)."""
    xmin, xmax, ymin, ymax = fenetre
    return rf"""
\begin{{axis}}[otWeb, at={{({x}cm,0)}}, width=3.7cm, height=3.4cm,
  xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}, xlabel={{}}, ylabel={{}},
  clip=true, clip mode=individual, {ticks},
  title={{{titre}}}, title style={{font=\otMedium\fontsize{{9.5}}{{11}}\selectfont, text=otNavy, yshift=3pt}}]
{corps}
\end{{axis}}"""


GRAD = r"font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt"
POS = {"b": "anchor=north,yshift=-2.5pt", "h": "anchor=south,yshift=2.5pt",
       "g": "anchor=east,xshift=-2pt", "d": "anchor=west,xshift=2pt"}


def gx(x, cote, tex):
    """Graduation de l'axe des abscisses : « b » dessous, « h » dessus."""
    return rf"  \node[{GRAD},{POS[cote]}] at (axis cs:{x},0) {{${tex}$}};" + "\n"


def gy(y, cote, tex):
    """Graduation de l'axe des ordonnées : « g » à gauche, « d » à droite."""
    return rf"  \node[{GRAD},{POS[cote]}] at (axis cs:0,{y}) {{${tex}$}};" + "\n"


def figure(*panneaux):
    return r"\begin{tikzpicture}" + "".join(panneaux) + "\n\\end{tikzpicture}"


CARRE_CUBE = figure(
    panneau(0, "Fonction carré", (-2.3, 2.3, -0.9, 4.6), "xtick={-2,-1,1,2}, ytick={1,2,3,4}", r"""
  \addplot[courbe, domain=-2.14:2.14] {x^2};
  \pnt{1}{1} \pnt{-1}{1}"""),
    panneau(4.8, "Fonction cube", (-1.9, 1.9, -4.6, 4.6), "xtick={-1,1}, ytick={-4,-2,2,4}, xticklabels={}, yticklabels={}", r"""
  \addplot[courbe, domain=-1.66:1.66] {x^3};
  \pnt{1}{1} \pnt{-1}{-1}
""" + gx(-1, "h", "-1") + gx(1, "b", "1") + gy(2, "g", "2") + gy(4, "g", "4") + gy(-2, "d", "-2") + gy(-4, "d", "-4")),
)

INVERSE_RACINE = figure(
    panneau(0, "Fonction inverse", (-3.3, 3.3, -3.3, 3.3), "xtick={-2,-1,1,2}, ytick={-2,-1,1,2}, xticklabels={}, yticklabels={}", gx(-2, "h", "-2") + gx(-1, "h", "-1") + gx(1, "b", "1") + gx(2, "b", "2")
    + gy(1, "g", "1") + gy(2, "g", "2") + gy(-1, "d", "-1") + gy(-2, "d", "-2") + r"""
  \addplot[courbe, domain=-3.3:-0.3, samples=120] {1/x};
  \addplot[courbe, domain=0.3:3.3, samples=120] {1/x};
  \pnt{1}{1} \pnt{-1}{-1}"""),
    panneau(4.8, "Fonction racine carrée", (-0.7, 4.7, -0.5, 2.6), "xtick={1,2,3,4}, ytick={1,2}", r"""
  \addplot[courbe, domain=0:4.6, samples=200] {sqrt(x)};
  \pnt{0}{0} \pnt{1}{1} \pnt{4}{2}"""),
)

ABS_ENTIERE = figure(
    panneau(0, "Valeur absolue", (-2.7, 2.7, -0.8, 2.8), "xtick={-2,-1,1,2}, ytick={1,2}", r"""
  \addplot[courbe, domain=-2.7:2.7, samples=3] {abs(x)};
  \pnt{0}{0}"""),
    panneau(4.8, "Partie entière", (-2.5, 3.5, -2.7, 2.7), "xtick={-2,-1,1,2,3}, ytick={-2,-1,1,2}, yticklabels={}", gy(1, "g", "1") + gy(2, "g", "2") + r"""
  \draw[courbe] (axis cs:-2,-2) -- (axis cs:-1,-2);
  \draw[courbe] (axis cs:-1,-1) -- (axis cs:0,-1);
  \draw[courbe] (axis cs:0,0) -- (axis cs:1,0);
  \draw[courbe] (axis cs:1,1) -- (axis cs:2,1);
  \draw[courbe] (axis cs:2,2) -- (axis cs:3,2);
  \pnt{-2}{-2} \pnt{-1}{-1} \pnt{0}{0} \pnt{1}{1} \pnt{2}{2}
  \pntv{-1}{-2} \pntv{0}{-1} \pntv{1}{0} \pntv{2}{1} \pntv{3}{2}"""),
)

EXP_LN = figure(
    panneau(0, "Exponentielle", (-3.2, 2.2, -0.7, 6.4), "xtick={-2,-1,1}, ytick={1,2,3,4,5,6}", r"""
  \addplot[courbe, domain=-3.2:1.85, samples=160] {exp(x)};
  \pnt{0}{1} \pnt{1}{2.71828}"""),
    panneau(4.8, "Logarithme népérien", (-0.7, 6.6, -2.9, 2.4), r"xtick={1,2.71828,4,5,6}, xticklabels={$1$,$\mathrm{e}$,$4$,$5$,$6$}, ytick={-2,-1,1,2}", r"""
  \addplot[courbe2, domain=0.055:6.6, samples=200] {ln(x)};
  \pnt[otGreenDark]{1}{0} \pnt[otGreenDark]{2.71828}{1}"""),
)

SIN_COS = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.2cm, height=3.1cm, xmin=-6.9, xmax=7.3, ymin=-1.6, ymax=1.95,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$},
  minor xtick={-4.7124,-1.5708,1.5708,4.7124}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-1,1}]
  \addplot[courbe2, domain=-6.9:7.1] {cos(x)};
  \addplot[courbe, domain=-6.9:7.1] {sin(x)};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.12) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:-3.1416,1.12) {$y=\cos x$};
  \draw[otMuted,line width=0.6pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:0,-1.36) -- (axis cs:6.2832,-1.36)
    node[note,midway,below=2pt,fill=none] {période $2\pi$};
\end{axis}
\end{tikzpicture}"""

TANGENTE = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=4.2cm, xmin=-4.9, xmax=4.9, ymin=-4.2, ymax=4.2,
  xtick={-4.7124,-1.5708,1.5708,4.7124}, xticklabels={}, ytick={-3,3},
  clip=true, clip mode=individual]
  \draw[asymptote] (axis cs:-4.7124,-4.2) -- (axis cs:-4.7124,4.2);
  \draw[asymptote] (axis cs:-1.5708,-4.2) -- (axis cs:-1.5708,4.2);
  \draw[asymptote] (axis cs:1.5708,-4.2) -- (axis cs:1.5708,4.2);
  \draw[asymptote] (axis cs:4.7124,-4.2) -- (axis cs:4.7124,4.2);
  \addplot[courbe, domain=-4.475:-1.808, samples=200] {tan(x)};
  \addplot[courbe, domain=-1.333:1.333, samples=200] {tan(x)};
  \addplot[courbe, domain=1.808:4.475, samples=200] {tan(x)};
  \pnt{0}{0} \pnt{0.7854}{1}
\end{axis}
\end{tikzpicture}"""

ARCSIN_ARCCOS = figure(
    panneau(0, "Arcsinus", (-1.7, 1.7, -2.0, 2.0), "xtick={-1,1}, ytick={-1.5708,1.5708}, xticklabels={}, yticklabels={}", gx(-1, "h", "-1") + gx(1, "b", "1")
    + gy(1.5708, "g", r"\frac{\pi}{2}") + gy(-1.5708, "d", r"-\frac{\pi}{2}") + r"""
  \draw[guide] (axis cs:1,0) -- (axis cs:1,1.5708);
  \draw[guide] (axis cs:-1,0) -- (axis cs:-1,-1.5708);
  \addplot[courbe, domain=-1:1, samples=300] {asin(x)*pi/180};
  \pnt{-1}{-1.5708} \pnt{1}{1.5708} \pnt{0}{0}"""),
    panneau(4.8, "Arccosinus", (-1.7, 1.7, -0.6, 3.5), "xtick={-1,1}, ytick={1.5708,3.1416}, yticklabels={$$,$\\pi$}", r"""
  \draw[guide] (axis cs:-1,0) -- (axis cs:-1,3.1416);
  \addplot[courbe2, domain=-1:1, samples=300] {acos(x)*pi/180};
  \pnt[otGreenDark]{-1}{3.1416} \pnt[otGreenDark]{1}{0} \pnt[otGreenDark]{0}{1.5708}"""),
)

ARCTAN = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.4cm, xmin=-5.6, xmax=5.6, ymin=-2.1, ymax=2.1,
  xtick={-4,-2,2,4}, ytick=\empty, xlabel={$x$}, ylabel={$y$}]
  \draw[asymptote] (axis cs:-5.6,1.5708) -- (axis cs:5.6,1.5708);
  \draw[asymptote] (axis cs:-5.6,-1.5708) -- (axis cs:5.6,-1.5708);
  \addplot[courbe, domain=-5.6:5.6, samples=200] {atan(x)*pi/180};
  \pnt{0}{0} \pnt{1}{0.7854}
  \node[anchor=south west,text=otRed!85!black,inner sep=1.5pt] at (axis cs:-5.5,1.62) {$y=\frac{\pi}{2}$};
  \node[anchor=north east,text=otRed!85!black,inner sep=1.5pt] at (axis cs:5.5,-1.62) {$y=-\frac{\pi}{2}$};
\end{axis}
\end{tikzpicture}"""

HYPERBOLIQUES = figure(
    panneau(0, "ch et sh", (-2.6, 2.6, -4.3, 4.3), "xtick={-2,-1,1,2}, ytick={-3,3}, xticklabels={}, yticklabels={}", gx(-2, "h", "-2") + gx(-1, "h", "-1") + gx(1, "b", "1") + gx(2, "b", "2")
    + gy(3, "g", "3") + gy(-3, "d", "-3") + r"""
  \addplot[courbe, domain=-2.15:2.15] {cosh(x)};
  \addplot[courbe2, domain=-2.15:2.15] {sinh(x)};
  \pnt{0}{1} \pnt[otGreenDark]{0}{0}
  \node[anchor=east,text=otNavy,inner sep=1.5pt] at (axis cs:-1.75,3.0) {$\operatorname{ch}$};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:-1.45,-2.9) {$\operatorname{sh}$};"""),
    panneau(4.8, "th", (-3.3, 3.3, -1.6, 1.6), "xtick={-2,-1,1,2}, ytick={-1,1}, yticklabels={}", r"""
  \node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt,anchor=south east] at (axis cs:-0.05,1.04) {$1$};
  \node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt,anchor=north west] at (axis cs:0.05,-1.04) {$-1$};
  \draw[asymptote] (axis cs:-3.3,1) -- (axis cs:3.3,1);
  \draw[asymptote] (axis cs:-3.3,-1) -- (axis cs:3.3,-1);
  \addplot[courbe, domain=-3.3:3.3, samples=160] {tanh(x)};
  \pnt{0}{0}"""),
)

PUISSANCES = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=4.6cm, xmin=-0.3, xmax=3.3, ymin=-0.3, ymax=3.3,
  xtick={1,2,3}, ytick={1,2,3}, clip=true, clip mode=individual]
  \addplot[otOrange!85!black, line width=1.2pt, domain=0:1.78, samples=120] {x^2};
  \addplot[otMuted, line width=1pt, domain=0:3.2] {x};
  \addplot[courbe2, domain=0:3.2, samples=200] {sqrt(x)};
  \addplot[courbe, domain=0.31:3.2, samples=160] {1/x};
  \pnt[otInk]{1}{1}
  \node[anchor=west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:1.82,3.15) {$\alpha = 2$};
  \node[anchor=west,text=otMuted!70!black,inner sep=1.5pt] at (axis cs:3.3,3.2) {$\alpha = 1$};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:3.3,1.79) {$\alpha = \frac{1}{2}$};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:3.3,0.31) {$\alpha = -1$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {
    "carre_cube": CARRE_CUBE,
    "inverse_racine": INVERSE_RACINE,
    "abs_entiere": ABS_ENTIERE,
    "exp_ln": EXP_LN,
    "sin_cos": SIN_COS,
    "tangente": TANGENTE,
    "arcsin_arccos": ARCSIN_ARCCOS,
    "arctan": ARCTAN,
    "hyperboliques": HYPERBOLIQUES,
    "puissances": PUISSANCES,
}

XLAB = {
    "sin_cos": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "tangente": [(-4.7124, "g", r"-\frac{3\pi}{2}"), (-1.5708, "g", r"-\frac{\pi}{2}"),
                 (1.5708, "g", r"\frac{\pi}{2}"), (4.7124, "g", r"\frac{3\pi}{2}")],
}
