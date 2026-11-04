# -*- coding: utf-8 -*-
"""Figures de la notion « Représenter algébriquement et graphiquement les fonctions » (Seconde).

Compilées par outils/figures_livre.py (style des livres, repère otWeb) :
courbes en bleu marine, seconde courbe en orange, seuils y = k en pointillés
orange, solutions en vert sur l'axe des abscisses (bornes pleines = comprises,
bornes vides = exclues), repères de lecture en pointillés gris.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  courbeB/.style={otOrange,line width=1.35pt},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
  sym/.style={otOrange!90!black,line width=.7pt,dash pattern=on 3pt off 2pt},
  zone/.style={otGreen!22},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
"""

# Graduations de l'axe des abscisses placées à la main (côté libre de la courbe)
XLAB = {
    "cours_lecture": [(-2, "c", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "h", "2"), (3, "d", "3"), (4, "c", "4")],
    "cours_resolution": [(-2, "c", "-2"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "d", "4"), (5, "c", "5")],
    "ex_table_courbe": [(-3, "c", "-3"), (-2, "g", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "d", "2"), (3, "c", "3")],
    "ex_parite_f": [(-3, "c", "-3"), (-2, "h", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "h", "2"), (3, "c", "3")],
    "ex_parite_h": [(-2, "c", "-2"), (-1, "d", "-1"), (1, "c", "1")],
    "ex_inter_enonce": [(-2, "c", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "ex_inter_points": [(-2, "c", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "ex_inter_sup": [(-2, "c", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "ex_produit_q4": [(-4, "c", "-4"), (-3, "g", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "d", "2"), (3, "c", "3")],
    "ex_produit_q5": [(-4, "c", "-4"), (-3, "g", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "d", "2"), (3, "c", "3")],
    "ex_quotient_q4": [(k, "c", str(k)) for k in (-6, -5, -4, -3, 2, 3, 4, 5)] + [(-1, "g", "-1"), (1, "h", "1")],
    "ex_quotient_q5": [(k, "c", str(k)) for k in (-6, -5, -4, -3, 2, 3, 4, 5)] + [(-1, "g", "-1"), (1, "h", "1")],
    "ex_cubique_enonce": [(-2, "g", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "c", "2")],
    "ex_cubique_q2": [(-2, "h", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2")],
    "ex_cubique_q4": [(-2, "g", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "c", "2")],
    "ex_cubique_q6": [(-1.732, "d", r"-\sqrt{3}"), (1.732, "d", r"\sqrt{3}")],
}
for _poly in ("ex_poly_enonce", "ex_poly_q2", "ex_poly_q3", "ex_poly_q4", "ex_poly_q5"):
    XLAB[_poly] = [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "g", "1"), (2, "c", "2"),
                   (3, "c", "3"), (4, "d", "4"), (5, "c", "5")]

AX = r"\begin{axis}[otWeb, "
FIN = "\n\\end{axis}\n\\end{tikzpicture}"


def fig(opts, corps):
    return "\\begin{tikzpicture}\n" + AX + opts + "]\n" + corps + FIN


# ---------------------------------------------------------------- cours
F1 = "x^2-2*x-3"
cours_base = r"""
  \addplot[courbe, domain=-2.1:4.05] {x^2-2*x-3};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-1.4,3.4) {$\mathcal{C}_f$};
"""

FIGURES = {}

FIGURES["cours_lecture"] = fig(
    r"width=6.6cm, height=6.2cm, xmin=-2.4, xmax=4.7, ymin=-4.7, ymax=6.3, xtick={-2,-1,1,2,3,4}, xticklabels={}, gm, ytick={-4,1,2,3,4,5}, minor ytick={-3,-2,-1,6}",
    cours_base + r"""
  \guides{4}{5}
  \pnt[otGreenDark]{4}{5}
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:2,5.1) {$f(4)=5$};
  \draw[seuil] (axis cs:-2.3,-3) -- (axis cs:4.5,-3);
  \guidev{2}{-3}
  \pnt[otOrange]{0}{-3} \pnt[otOrange]{2}{-3}
  \borneF{0} \borneF{2}
  \node[note,anchor=north west,align=left] at (axis cs:2.35,-3.25) {antécédents\\de $-3$ : $0$ et $2$};
""")

FIGURES["cours_resolution"] = fig(
    r"width=6.6cm, height=6.6cm, xmin=-2.4, xmax=5.3, ymin=-4.7, ymax=6.9, xtick={-2,-1,1,2,3,4,5}, xticklabels={}, gm, ytick={-4,-1,1,2,3,4,5}, minor ytick={-3,-2,6}",
    r"""
  \addplot[courbe, domain=-2.1:4.25] {x^2-2*x-3};
  \addplot[courbeB, domain=-2.3:5.1] {x+1};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-1.4,3.4) {$\mathcal{C}_f$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:4.6,5.2) {$\mathcal{C}_g$};
  \guidev{4}{5}
  \sol{-1}{4} \borneF{-1} \borneF{4}
  \pnt[otRed]{4}{5}
""")

FIGURES["cours_parite"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, gm, name=g, width=3.6cm, height=4.4cm, xmin=-2.1, xmax=2.2, ymin=-5.6, ymax=5.4,
  xtick={-1,1}, ytick={-4,2,4}, minor ytick={-2}, title={\otRegular\fontsize{9}{11}\selectfont\color{otMuted}paire : $g(x)=3x^2-5$},
  title style={yshift=6pt}]
  \addplot[courbe, domain=-1.85:1.85] {3*x^2-5};
  \draw[sym] (axis cs:-1,-2) -- (axis cs:1,-2);
  \pnt[otOrange]{1}{-2} \pnt[otOrange]{-1}{-2}
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:1.05,-2.15) {$M$};
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:-1.05,-2.15) {$M'$};
\end{axis}
\begin{axis}[otWeb, gm, at={(g.east)}, anchor=west, xshift=1.3cm, width=3.6cm, height=4.4cm, xmin=-2.3, xmax=2.4, ymin=-4.3, ymax=4.3,
  xtick={-1,1}, minor xtick={-2,2}, ytick={-2,2}, title={\otRegular\fontsize{9}{11}\selectfont\color{otMuted}impaire : $h(x)=x^3-3x$},
  title style={yshift=6pt}]
  \addplot[courbe, domain=-2.2:2.2] {x^3-3*x};
  \draw[sym] (axis cs:-2,-2) -- (axis cs:2,2);
  \pnt[otOrange]{2}{2} \pnt[otOrange]{-2}{-2} \pnt[otOrange]{0}{0}
  \node[etiq,text=otOrange!85!black,anchor=east] at (axis cs:1.9,2.3) {$N$};
  \node[etiq,text=otOrange!85!black,anchor=west] at (axis cs:-1.9,-2.3) {$N'$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 2035
P35 = r"width=6.4cm, height=6cm, xmin=-1.7, xmax=4.7, ymin=-1.9, ymax=7.1, xtick={-1,1,2,3,4}, gm, ytick={-1,3,4,5,6}, minor ytick={1,2,7}"
B35 = r"""
  \addplot[courbe, domain=-1.33:4.33] {x^2-3*x+1};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:3.7,6.3) {$\mathcal{C}_f$};
"""
FIGURES["ex_appart_enonce"] = fig(P35, B35)
FIGURES["ex_appart_corrige"] = fig(P35, B35 + r"""
  \draw[seuil] (axis cs:-1.6,1) -- (axis cs:4.55,1);
  \node[note,text=otOrange!85!black,anchor=south west] at (axis cs:3.55,1.1) {$y=1$};
  \guidev{3}{1}
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{3}{1}
  \pnt[otGreenDark]{2}{-1} \pnt[otGreenDark]{-1}{5}
  \pntv[otRed]{0}{0}
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:2,-1.12) {$A$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-1.12,5) {$B$};
  \node[etiq,text=otRed,anchor=north east] at (axis cs:-0.05,-0.1) {$C$};
""")

# ---------------------------------------------------------------- 2036
P36 = r"width=6cm, height=6.6cm, xmin=-3.5, xmax=3.6, ymin=-4.6, ymax=5.7, xtick={-3,-2,-1,1,2,3}, ytick={-4,-3,-2,-1,1,2,3,4,5}"
FIGURES["ex_table_repere"] = fig(P36, "")
FIGURES["ex_table_courbe"] = fig(P36.replace("ytick={-4,", "xticklabels={}, gm, minor ytick={-4}, ytick={"), r"""
  \addplot[courbe, domain=-3.12:3.12] {x^2-4};
  \pnt{-3}{5} \pnt{-2}{0} \pnt{-1}{-3} \pnt{0}{-4} \pnt{1}{-3} \pnt{2}{0} \pnt{3}{5}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-2.6,3.9) {$\mathcal{C}_f$};
""")

# ---------------------------------------------------------------- 2040
FIGURES["ex_parite_f"] = fig(
    r"width=5cm, height=4.6cm, xmin=-3.4, xmax=3.6, ymin=-5.7, ymax=5.6, xtick={-3,-2,-1,1,2,3}, xticklabels={}, ytick={-4,-2,2,4}",
    r"""
  \addplot[courbe, domain=-3.2:3.2] {x^2-5};
  \draw[sym] (axis cs:-2.5,1.25) -- (axis cs:2.5,1.25);
  \pnt[otOrange]{2.5}{1.25} \pnt[otOrange]{-2.5}{1.25}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:2.4,3.9) {$y=x^2-5$};
""")
FIGURES["ex_parite_g"] = fig(
    r"width=5cm, height=4.6cm, xmin=-1.9, xmax=2, ymin=-3, ymax=3, xtick={-1,1}, ytick={-2,-1,1,2}",
    r"""
  \addplot[courbe, domain=-1.68:1.68] {x^3-x};
  \draw[sym] (axis cs:-1.5,-1.875) -- (axis cs:1.5,1.875);
  \pnt[otOrange]{1.5}{1.875} \pnt[otOrange]{-1.5}{-1.875} \pnt[otOrange]{0}{0}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.5,2.6) {$y=x^3-x$};
""")
FIGURES["ex_parite_h"] = fig(
    r"width=5cm, height=4.6cm, xmin=-2.1, xmax=1.8, ymin=-3, ymax=3.6, xtick={-2,-1,1}, xticklabels={}, ytick={-2,-1,1,2,3}",
    r"""
  \addplot[courbe, domain=-1.82:1.22] {x^3+x^2};
  \guides{1}{2}
  \pnt[otOrange]{1}{2} \pnt[otOrange]{-1}{0}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.15,-1.0) {$y=x^3+x^2$};
""")

# ---------------------------------------------------------------- 2039
P39 = r"width=6.4cm, height=6cm, xmin=-2.8, xmax=3.4, ymin=-2.6, ymax=6.1, xtick={-2,-1,1,2,3}, xticklabels={}, gm, ytick={-1,1,2,3,4,5}, minor ytick={-2,6}"
B39 = r"""
  \addplot[courbe, domain=-2.75:2.86, name path=f] {x^2-2};
  \addplot[courbeB, domain=-2.6:3.2, name path=g] {x};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-1.6,4.6) {$\mathcal{C}_f$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:3.0,2.6) {$\mathcal{C}_g$};
"""
FIGURES["ex_inter_enonce"] = fig(P39, B39)
FIGURES["ex_inter_points"] = fig(P39, B39 + r"""
  \guidev{2}{2} \guidev{-1}{-1}
  \pnt[otRed]{-1}{-1} \pnt[otRed]{2}{2}
  \borneF{-1} \borneF{2}
  \node[etiq,text=otRed!90!black,anchor=west] at (axis cs:2.15,1.75) {$(2\,;2)$};
""")
FIGURES["ex_inter_sup"] = fig(P39, B39 + r"""
  \guidev{2}{2} \guidev{-1}{-1}
  \sol{-2.75}{-1} \sol{2}{3.3}
  \borneF{-1} \borneF{2}
""")

# ---------------------------------------------------------------- 2038
P38 = r"width=7cm, height=5.2cm, xmin=-3.7, xmax=5.7, ymin=-2.7, ymax=4.9, xtick={-3,-2,-1,1,2,3,4,5}, xticklabels={}, gm, ytick={-2,-1,1,3,4}, minor ytick={2}"
B38 = r"""
  \draw[ligne] (axis cs:-3,1) -- (axis cs:-1,4) -- (axis cs:2,-2) -- (axis cs:5,1);
  \pnt{-3}{1} \pnt{-1}{4} \pnt{2}{-2} \pnt{5}{1}
  \node[etiq,anchor=south east] at (axis cs:-3.05,1.05) {$A$};
  \node[etiq,anchor=south] at (axis cs:-1,4.12) {$B$};
  \node[etiq,anchor=north] at (axis cs:2,-2.12) {$C$};
  \node[etiq,anchor=south west] at (axis cs:5.05,1.05) {$D$};
"""
SEUIL1 = r"""
  \draw[seuil] (axis cs:-3.6,1) -- (axis cs:5.6,1);
"""
FIGURES["ex_poly_enonce"] = fig(P38, B38)
FIGURES["ex_poly_q2"] = fig(P38, B38 + r"""
  \pnt[otRed]{1}{0} \pnt[otRed]{4}{0}
""")
FIGURES["ex_poly_q3"] = fig(P38, SEUIL1 + B38 + r"""
  \guidev{0.5}{1}
  \pnt[otRed]{0.5}{1} \pnt[otRed]{-3}{1} \pnt[otRed]{5}{1}
  \borneF{-3} \borneF{0.5} \borneF{5}
""")
FIGURES["ex_poly_q4"] = fig(P38, SEUIL1 + B38 + r"""
  \guidev{0.5}{1}
  \sol{-3}{0.5} \borneF{-3} \borneF{0.5} \borneF{5}
""")
FIGURES["ex_poly_q5"] = fig(P38, B38 + r"""
  \sol{1}{4} \borneF{1} \borneF{4}
""")

# ---------------------------------------------------------------- 2042
P42 = r"width=6.4cm, height=6cm, xmin=-4.4, xmax=3.6, ymin=-7, ymax=7.8, xtick={-4,-3,-2,-1,1,2,3}, xticklabels={}, gm, ytick={-4,-2,2,4,6}, minor ytick={-6}"
B42 = r"""
  \addplot[courbe, domain=-4.25:3.25] {(x-2)*(x+3)};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-3.55,6.4) {$y=P(x)$};
"""
FIGURES["ex_produit_q4"] = fig(P42, B42 + r"""
  \sol{-3}{2} \borneF{-3} \borneF{2}
""")
FIGURES["ex_produit_q5"] = fig(P42, B42 + r"""
  \sol{-4.3}{-3} \sol{2}{3.5} \borneO{-3} \borneO{2}
""")

# ---------------------------------------------------------------- 2043
P43 = r"width=7cm, height=6cm, xmin=-6.3, xmax=5.6, ymin=-6.3, ymax=8.2, xtick={-6,-5,-4,-3,-2,-1,1,2,3,4,5}, xticklabels={}, gm, ytick={-2,2,4,6}, minor ytick={-6,-4,8}"
B43 = r"""
  \addplot[courbe, domain=-6.2:-1.84, samples=200] {(2*x-3)/(x+1)};
  \addplot[courbe, domain=-0.38:5.5, samples=200] {(2*x-3)/(x+1)};
  \draw[asymptote] (axis cs:-1,-6.3) -- (axis cs:-1,8.2);
  \node[note,text=otRed!90!black,anchor=north east] at (axis cs:-1.15,-4.4) {$x=-1$ interdit};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:3.6,1.6) {$y=Q(x)$};
"""
FIGURES["ex_quotient_q4"] = fig(P43, B43 + r"""
  \sol{-6.2}{-1} \sol{1.5}{5.5} \borneO{-1} \borneF{1.5}
""")
FIGURES["ex_quotient_q5"] = fig(P43, B43 + r"""
  \sol{-1}{1.5} \borneO{-1} \borneO{1.5}
""")

# ---------------------------------------------------------------- 2044
P44 = r"width=6.6cm, height=5.4cm, xmin=0, xmax=10.6, ymin=0, ymax=25.5, xtick={1,2,3,4,5,6,7,8,9,10}, ytick={4,8,12,16,20,24}, xlabel={km}, ylabel={€}"
B44 = r"""
  \addplot[courbe, domain=0:10.5] {2*x+3};
  \addplot[courbeB, domain=0:10.5] {x+8};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:8.6,21.5) {tarif A};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:8.4,15.6) {tarif B};
"""
FIGURES["ex_tarif_q1"] = fig(P44, B44)
FIGURES["ex_tarif_q3"] = fig(P44, B44 + r"""
  \guides{5}{13}
  \pnt[otRed]{5}{13}
  \node[etiq,text=otRed!90!black,anchor=north west] at (axis cs:5.3,12.6) {$(5\,;13)$};
""")
FIGURES["ex_tarif_q4"] = fig(P44, B44 + r"""
  \guidev{5}{13}
  \sol{0}{5} \borneF{0} \borneF{5}
  \node[note,anchor=south west] at (axis cs:0.4,0.8) {tarif A moins cher};
""")
FIGURES["ex_tarif_q5"] = fig(
    r"width=6.6cm, height=5.6cm, xmin=0, xmax=22.5, ymin=0, ymax=47, xtick={5,10,15,20}, ytick={10,20,28,43}, xlabel={km}, ylabel={€}",
    r"""
  \addplot[courbe, domain=0:21.5] {2*x+3};
  \addplot[courbeB, domain=0:21.5] {x+8};
  \guides{20}{43} \guides{20}{28}
  \pnt{20}{43} \pnt[otOrange]{20}{28}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:15.5,38) {tarif A};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:15.5,22.4) {tarif B};
""")

# ---------------------------------------------------------------- nouveau-1
PN1 = r"width=6.8cm, height=5.2cm, xmin=-2.5, xmax=2.6, ymin=-1.7, ymax=2.4, xtick={-2,-1,1,2}, xticklabels={}, ytick={-1,1,2}"
BN1 = r"""
  \addplot[courbe, domain=-2:2] {(x^3-3*x)/2};
  \pnt{-2}{-1} \pnt{2}{1}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-2.45,0.25) {$\mathcal{C}_f$};
"""
FIGURES["ex_cubique_enonce"] = fig(PN1, BN1)
FIGURES["ex_cubique_q2"] = fig(PN1, r"""
  \draw[seuil] (axis cs:-2.4,1) -- (axis cs:2.45,1);
  \draw[seuil] (axis cs:-2.4,-1) -- (axis cs:2.45,-1);
  \node[note,text=otOrange!85!black,anchor=south west] at (axis cs:2.12,1.05) {$y=1$};
  \node[note,text=otOrange!85!black,anchor=north west] at (axis cs:2.12,-1.05) {$y=-1$};
""" + BN1 + r"""
  \guidev{-1}{1} \guidev{2}{1} \guidev{-2}{-1} \guidev{1}{-1}
  \pnt[otRed]{-1}{1} \pnt[otRed]{2}{1} \pnt[otRed]{-2}{-1} \pnt[otRed]{1}{-1}
  \borneF{-2} \borneF{-1} \borneF{1} \borneF{2}
""")
FIGURES["ex_cubique_q4"] = fig(PN1, r"""
  \draw[seuil] (axis cs:-2.4,1) -- (axis cs:2.45,1);
  \node[note,text=otOrange!85!black,anchor=south west] at (axis cs:2.12,1.05) {$y=1$};
""" + BN1 + r"""
  \guidev{-1}{1} \guidev{2}{1}
  \sol{-2}{2} \borneF{-2} \borneO{-1} \borneO{2}
""")
FIGURES["ex_cubique_q6"] = fig(
    r"width=6.8cm, height=5.2cm, xmin=-2.5, xmax=2.6, ymin=-1.7, ymax=2.4, xtick={-1.732,1.732}, xticklabels={}, gm, minor xtick={-2,-1,1,2}, ytick={-1,1,2}",
    BN1 + r"""
  \sol{-1.732}{0} \sol{1.732}{2}
  \borneO{-1.732} \borneO{0} \borneO{1.732} \borneF{2}
""")

# ---------------------------------------------------------------- nouveau-2
FIGURES["ex_enclos_schema"] = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (4.2,0); \coordinate (C) at (4.2,2.4); \coordinate (D) at (0,2.4);
  \fill[otSky] (A) -- (B) -- (C) -- (D) -- cycle;
  \draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;
  \draw[otMuted!70,line width=.4pt] (0,-0.08) -- (0,-0.6) (4.2,-0.08) -- (4.2,-0.6) (4.28,0) -- (4.8,0) (4.28,2.4) -- (4.8,2.4);
  \draw[cote] (0,-0.45) -- (4.2,-0.45);
  \draw[cote] (4.65,0) -- (4.65,2.4);
  \node[anchor=north,text=otInk] at (2.1,-0.55) {$x$};
  \node[anchor=west,text=otInk] at (4.78,1.2) {$10-x$};
  \node[text=otMuted,font=\otRegular\fontsize{9}{11}\selectfont] at (2.1,1.2) {enclos d’aire $A(x)$};
\end{tikzpicture}"""

PN2 = r"width=7cm, height=5.4cm, xmin=0, xmax=10.8, ymin=0, ymax=27.5, xtick={1,2,3,4,5,6,7,8,9,10}, ytick={3,6,9,12,15,18,21,24}"
BN2 = r"""
  \addplot[courbe, domain=0:10] {x*(10-x)};
  \pntv{0}{0} \pntv{10}{0}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:8.3,15.5) {$y=A(x)$};
"""
FIGURES["ex_enclos_courbe"] = fig(PN2, BN2)
FIGURES["ex_enclos_resolution"] = fig(PN2, r"""
  \draw[seuil] (axis cs:0,21) -- (axis cs:10.6,21);
  \node[note,text=otOrange!85!black,anchor=south east] at (axis cs:10.6,21.3) {$y=21$};
""" + BN2 + r"""
  \guidev{3}{21} \guidev{7}{21}
  \pnt[otRed]{3}{21} \pnt[otRed]{7}{21}
  \sol{3}{7} \borneF{3} \borneF{7}
""")

# ---------------------------------------------------------------- finition 2026-11-02
# 2037 : les sept points de la table (aucune courbe : seules ces valeurs sont connues)
P37 = r"width=6cm, height=4.6cm, xmin=-3.6, xmax=3.7, ymin=-1.8, ymax=6, xtick={-3,-2,-1,1,2,3}, ytick={-1,1,2,3,4,5}"
PTS37 = [(-3, 5), (-2, 2), (-1, 0), (0, -1), (1, 0), (2, 2), (3, 5)]
XLAB["ex_table_q4"] = [(-3, "c", "-3"), (-1, "h", "-1"), (1, "h", "1"), (3, "c", "3")]
XLAB["ex_table_q5"] = [(-3, "c", "-3"), (-2, "c", "-2"), (2, "c", "2"), (3, "c", "3")]
FIGURES["ex_table_q4"] = fig(P37 + ", xticklabels={}", r"""
  \draw[seuil] (axis cs:-3.6,2) -- (axis cs:3.6,2);
  \node[note,text=otOrange!85!black,anchor=south east] at (axis cs:3.6,2.15) {$y=2$};
  \guidev{-2}{2} \guidev{2}{2}
""" + "".join(rf"  \pnt{{{a}}}{{{b}}}" + "\n" for a, b in PTS37 if b != 2) + r"""
  \pnt[otGreenDark]{-2}{2} \pnt[otGreenDark]{2}{2}
  \node[note,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-2,0) {$-2$};
  \node[note,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:2,0) {$2$};
""")
FIGURES["ex_table_q5"] = fig(P37 + ", xticklabels={}", r"""
  \fill[otGreen,opacity=0.12] (axis cs:-3.6,0) rectangle (axis cs:3.7,-1.8);
""" + "".join(rf"  \pnt{{{a}}}{{{b}}}" + "\n" for a, b in PTS37 if b > 0) + r"""
  \pnt[otGreenDark]{-1}{0} \pnt[otGreenDark]{0}{-1} \pnt[otGreenDark]{1}{0}
  \node[note,text=otGreenDark,anchor=south,yshift=3.5pt] at (axis cs:-1,0) {$-1$};
  \node[note,text=otGreenDark,anchor=south,yshift=3.5pt] at (axis cs:1,0) {$1$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:1.6,-1.65) {$f(x)\leqslant 0$};
""")

# 2041 : compléter par symétrie (f paire : axe des ordonnées ; g impaire : origine)
FIGURES["ex_parite_table"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=F, width=3.7cm, height=4.6cm, xmin=-3.6, xmax=3.7, ymin=-1.5, ymax=11.5,
  xtick={-3,-2,-1,1,2,3}, xticklabels={}, ytick={4,7,10},
  title={\otRegular\fontsize{9}{11}\selectfont\color{otMuted}$f$ paire}, title style={yshift=6pt}]
  \pnt{0}{1} \pnt{1}{4} \pnt{2}{7} \pnt{3}{10}
  \pnt[otGreenDark]{-1}{4} \pnt[otGreenDark]{-2}{7} \pnt[otGreenDark]{-3}{10}
  \node[note,anchor=north,yshift=-3pt] at (axis cs:-3,0) {$-3$};
  \node[note,anchor=north,yshift=-3.5pt] at (axis cs:3,0) {$3$};
\end{axis}
\begin{axis}[otWeb, at={(F.east)}, anchor=west, xshift=1.2cm, width=3.7cm, height=4.6cm, xmin=-3.6, xmax=3.7, ymin=-10.5, ymax=10.5,
  xtick={-3,-2,-1,1,2,3}, xticklabels={}, ytick={-9,-5,5,9}, yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  title={\otRegular\fontsize{9}{11}\selectfont\color{otMuted}$g$ impaire}, title style={yshift=6pt}]
  \draw[sym] (axis cs:-3,-9) -- (axis cs:3,9);
  \pnt{0}{0} \pnt{1}{2} \pnt{2}{5} \pnt{3}{9}
  \pnt[otGreenDark]{-1}{-2} \pnt[otGreenDark]{-2}{-5} \pnt[otGreenDark]{-3}{-9}
  \node[note,anchor=south,yshift=3.5pt] at (axis cs:-3,0) {$-3$};
  \node[note,anchor=north,yshift=-3.5pt] at (axis cs:3,0) {$3$};
\end{axis}
\end{tikzpicture}"""
