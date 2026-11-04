# -*- coding: utf-8 -*-
"""Figures de la notion « Dérivation et étude de fonctions » (Première
spécialité), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <ce dossier de notion>
"""

NOTE = r"\otRegular\fontsize{8.5}{10}\selectfont"


def lecture_g(corrige):
    """Exercice 1366 : g(x) = x^2/2 + 3, tangente en 2 : y = 2x + 1 par (2;5) et (4;9)."""
    code = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=6.4cm, xmin=-0.6, xmax=5.6, ymin=-0.8, ymax=13.2,
  xtick={1,2,3,4,5}, ytick={1,3,5,7,9,11}, extra y ticks={}, minor y tick num=0]
  \addplot[otGreenDark!80!otNavy, line width=1pt, domain=-0.5:5.6] {2*x+1};
  \addplot[courbe, domain=-0.5:4.3] {x^2/2+3};
"""
    if corrige:
        code += r"""  \draw[otGreenDark, line width=1pt, dash pattern=on 4pt off 2pt] (axis cs:2,5) -- (axis cs:4,5) -- (axis cs:4,9);
  \node[anchor=north, text=otGreenDark] at (axis cs:3,4.85) {$+2$};
  \node[anchor=west, text=otGreenDark] at (axis cs:4.08,7) {$+4$};
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:4.2,4.4) {pente\\$4 \div 2 = 2$};
"""
    code += r"""  \pnt{2}{5} \pnt{4}{9}
  \node[etiq, fill=none, anchor=north west] at (axis cs:2.08,4.75) {$A$};
  \node[etiq, fill=none, anchor=north west] at (axis cs:4.1,8.75) {$B$};
  \node[etiq, fill=none, text=otNavy, anchor=east] at (axis cs:3.95,12.4) {$\mathcal{C}_g$};
  \node[etiq, fill=none, text=otGreenDark, anchor=west] at (axis cs:5.0,10.2) {$T$};
\end{axis}
\end{tikzpicture}"""
    return code


def lecture_f(corrige):
    """Exercice 1365 : courbe passant par C(-1;2) et D(2;0), tangentes par (1;0) et (0;-1)."""
    f = r"5*x^3/54+x^2/9-19*x/18+25/27"
    # corrigé : la graduation 2 tomberait sous le pointillé vertical (D est nommé)
    xlab = r", xticklabels={$-2$,$-1$,$1$,,$3$}" if corrige else ""
    code = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=8.2cm, height=6.2cm, xmin=-2.7, xmax=3.6, ymin=-1.9, ymax=3.4,
  xtick={{-2,-1,1,2,3}}, ytick={{-1,1,2,3}}, yticklabels={{$-1$,,$2$,$3$}}{xlab}]
  \addplot[otOrange!85!black, line width=1pt, domain=-2.6:1.9] {{-x+1}};
  \addplot[otGreenDark, line width=1pt, domain=-0.6:3.5] {{x/2-1}};
  \addplot[courbe, domain=-2.6:3.25] {{{f}}};
"""
    if corrige:
        code += r"""  \draw[otOrange!80!black, line width=1pt, dash pattern=on 4pt off 2pt] (axis cs:-1,2) -- (axis cs:1,2) -- (axis cs:1,0);
  \node[anchor=south, text=otOrange!80!black] at (axis cs:0.5,2.05) {$+2$};
  \node[anchor=west, text=otOrange!80!black] at (axis cs:1.06,1.15) {$-2$};
  \draw[otGreenDark, line width=1pt, dash pattern=on 4pt off 2pt] (axis cs:0,-1) -- (axis cs:2,-1) -- (axis cs:2,0);
  \node[anchor=north, text=otGreenDark] at (axis cs:1,-1.05) {$+2$};
  \node[anchor=west, text=otGreenDark] at (axis cs:2.1,-0.6) {$+1$};
"""
    code += r"""  \pnt{-1}{2} \pnt{2}{0}
  \pnt[otMuted]{1}{0} \pnt[otMuted]{0}{-1}
  \node[etiq, fill=none, anchor=south west] at (axis cs:-0.95,2.12) {$C$};
  \node[etiq, fill=none, anchor=south east] at (axis cs:1.92,0.1) {$D$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:3.0,2.0) {$\mathcal{C}_f$};
  \node[etiq, fill=none, text=otOrange!80!black, anchor=west] at (axis cs:-1.95,3.2) {$T_C$};
  \node[etiq, fill=none, text=otGreenDark, anchor=north] at (axis cs:3.3,0.55) {$T_D$};
\end{axis}
\end{tikzpicture}"""
    return code


def cube(corrige):
    """Exercice nouveau-1 : courbe de la fonction cube, point A(1;1) (énoncé) ; + tangente (corrigé)."""
    code = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=7.0cm, xmin=-2.7, xmax=2.3, ymin=-10, ymax=6.4,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-8,-6,-4,-2,2,4}]
"""
    if corrige:
        code += r"""  \addplot[otGreenDark, line width=1.2pt, domain=-2.45:2.25] {3*x-2};
  \guides{1}{1} \guidev{-2}{-8}
  \pnt{-2}{-8}
"""
    code += r"""  \addplot[courbe, domain=-2.13:1.82] {x^3};
  \pnt{1}{1}
  \node[etiq, fill=none, anchor=south east] at (axis cs:0.95,1.25) {$A$};
  \node[etiq, fill=none, text=otNavy, anchor=south] at (axis cs:1.6,6.0) {$\mathcal{C}_f$};
"""
    if corrige:
        code += r"""  \node[etiq, fill=none, text=otGreenDark, anchor=west] at (axis cs:2.05,3.0) {$T$};
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:-2.65,5.9) {$\mathcal{C}_f$ au-dessus\\de $T$ sur\\$[-2\,;+\infty[$};
"""
    code += r"""\end{axis}
\end{tikzpicture}"""
    return code


# graduations placées du côté libre des pointillés de lecture
XLAB = {
    "cours_variations": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2")],
    "tangente_cube": [(-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2")],
    "cube_enonce": [(-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2")],
    "ds1_tangentes": [(1, "h", "1"), (2, "h", "2"), (3, "h", "3"), (4, "c", "4")],
    "ds1_variations": [(-1, "h", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "ds2_tangentes": [(2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "ds2_variations": [(-1, "c", "-1"), (1, "c", "1"), (2, "h", "2")],
    "calc_tangente_horiz": [(2, "h", "2"), (4, "c", "4")],
    "etude_carre": [(-1.7320508, "c", r"-\sqrt{3}"), (-1, "c", "-1"), (1, "c", "1"), (1.7320508, "c", r"\sqrt{3}")],
    "examA_tangente": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "examA_volume": [(2, "c", "2"), (4, "c", "4"), (6.6666667, "c", r"\frac{20}{3}"), (8, "c", "8"), (10, "c", "10")],
    "examB_tangente": [(1, "c", "1")],
    "examB_aire": [(2, "c", "2"), (4.3012701, "c", "r_0"), (6, "c", "6"), (8, "c", "8")],
    "derivee_signe": [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "c", "4")],
    "cours_optimisation": [(2, "c", "2"), (5, "c", "5"), (8, "c", "8"), (10, "c", "10")],
    "cours_inegalite": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "optim_aire": [(5, "c", "5"), (10, "c", "10"), (15, "c", "15"), (20, "c", "20")],
    "optim_cout": [(5, "c", "5"), (10, "c", "10"), (15, "c", "15")],
    "optim_mobile": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6"), (7, "c", "7")],
    "encadrement": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
}

# ---------------------------------------------------------------- finition 2026-11-02
VERT = r"otGreenDark"
NOUVELLES = {
# 1369 B : f(x) = 2x² − 8x + 5, tangente en 3 et tangente horizontale en 2
"ds1_tangentes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=6.4cm, xmin=-0.6, xmax=4.9, ymin=-4.4, ymax=6.4,
  xtick={1,2,3,4}, xticklabels={}, ytick={-3,-2,-1,1,2,3}, yticklabels={$-3$,,$-1$,$1$,,$3$}]
  \addplot[otGreenDark, line width=1.2pt, domain=2.17:4.85] {4*x-13};
  \draw[otGreenDark, line width=1.2pt] (axis cs:1,-3) -- (axis cs:3,-3);
  \addplot[courbe, domain=-0.1:4.1] {2*x^2-8*x+5};
  \guidev{3}{-1} \guidev{2}{-3}
  \pnt{3}{-1} \pnt{2}{-3}
  \node[etiq, fill=none, anchor=north west] at (axis cs:3.08,-1.05) {$A$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:0.3,5.0) {$\mathcal{C}_f$};
  \node[etiq, fill=none, text=otGreenDark, anchor=west] at (axis cs:4.95,5.3) {$T$};
  \node[note, fill=none, text=otGreenDark, anchor=west] at (axis cs:3.05,-3) {$y = -3$};
\end{axis}
\end{tikzpicture}""",

# 1369 C : g(x) = −x³ + 3x² + 9x − 5
"ds1_variations": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=6.6cm, xmin=-2.7, xmax=5.0, ymin=-18, ymax=27,
  xtick={-1,1,2,3,4}, xticklabels={}, ytick={-15,-10,-5,5,10,15,20}, yticklabels={,,$-5$,$5$,$10$,$15$,$20$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:-1.8,-10) -- (axis cs:-0.2,-10);
  \draw[otGreenDark, line width=1.2pt] (axis cs:2.2,22) -- (axis cs:3.8,22);
  \addplot[courbe, domain=-2.4:4.9] {-x^3+3*x^2+9*x-5};
  \guidev{-1}{-10} \guidev{3}{22}
  \pnt{-1}{-10} \pnt{3}{22}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:3,22.6) {maximum local $22$};
  \node[note, fill=none, anchor=north, text=otGreenDark, align=center] at (axis cs:-1,-10.8) {minimum\\local $-10$};
  \node[etiq, fill=none, text=otNavy, anchor=south] at (axis cs:-2.35,5.4) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}""",

# 1371 B : f(x) = −x² + 6x − 5, tangente en 1 : y = 4x − 4 ; tangente horizontale y = 4
"ds2_tangentes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=6.4cm, xmin=-0.5, xmax=6.0, ymin=-4.3, ymax=6.6,
  xtick={1,2,3,4,5}, xticklabels={}, ytick={-3,-2,-1,1,2,3,4,5}, yticklabels={$-3$,,$-1$,$1$,,$3$,,$5$}]
  \addplot[otGreenDark, line width=1.2pt, domain=0.08:2.6] {4*x-4};
  \draw[otGreenDark, line width=1.2pt] (axis cs:2,4) -- (axis cs:4,4);
  \addplot[courbe, domain=0.3:5.7] {-x^2+6*x-5};
  \guidev{3}{4}
  \pnt{1}{0} \pnt{3}{4}
  \node[note, fill=none, anchor=south east] at (axis cs:0.95,0.12) {$(1\,;0)$};
  \node[note, fill=none, anchor=south] at (axis cs:3,4.15) {$(3\,;4)$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:4.75,2.6) {$\mathcal{C}_f$};
  \node[etiq, fill=none, text=otGreenDark, anchor=east] at (axis cs:2.4,6.2) {$T$};
  \node[note, fill=none, text=otGreenDark, anchor=west] at (axis cs:4.05,4.05) {$y = 4$};
\end{axis}
\end{tikzpicture}""",

# 1371 C : g(x) = 2x³ − 3x² − 12x + 7
"ds2_variations": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=6.6cm, xmin=-2.8, xmax=3.9, ymin=-21, ymax=22,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-15,-10,-5,5,10,15}, yticklabels={,$-10$,$-5$,,$10$,},
  yticklabel style={anchor=south west, xshift=1pt, yshift=1pt}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:-1.7,14) -- (axis cs:-0.3,14);
  \draw[otGreenDark, line width=1.2pt] (axis cs:1.3,-13) -- (axis cs:2.7,-13);
  \addplot[courbe, domain=-2.4:3.45] {2*x^3-3*x^2-12*x+7};
  \guidev{-1}{14} \guidev{2}{-13}
  \pnt{-1}{14} \pnt{2}{-13}
  \node[note, fill=none, anchor=south, text=otGreenDark, align=center] at (axis cs:-1,14.6) {maximum\\local $14$};
  \node[note, fill=none, anchor=north, text=otGreenDark, align=center] at (axis cs:2,-13.6) {minimum\\local $-13$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:3.45,12) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}""",

# 1373 énoncé : rectangle de périmètre 40 m
"optim_rectangle": r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (4.6,0); \coordinate (C) at (4.6,2.6); \coordinate (D) at (0,2.6);
  \draw[geoTrait, geoRemplissage] (A) -- (B) -- (C) -- (D) -- cycle;
  \cote[0.45]{B}{A}{$x$}
  \cote[0.45]{C}{B}{$y$}
  \node[text=otMuted, font=\otRegular\fontsize{9}{10}\selectfont, align=center] at (2.3,1.3) {périmètre : $40$ m};
\end{tikzpicture}""",

# 1373 Q1 : A(x) = 20x − x², maximum 100 en 10
"optim_aire": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-1.2, xmax=22, ymin=-10, ymax=122,
  xtick={5,10,15,20}, xticklabels={}, ytick={20,40,60,80,100}, xlabel={$x$}, ylabel={$A$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:6.5,100) -- (axis cs:13.5,100);
  \addplot[courbe, domain=0:20] {20*x-x^2};
  \guides{10}{100}
  \pnt{10}{100}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:10,102) {aire maximale : $100$ m²};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:18.4,44) {$\mathcal{C}_A$};
\end{axis}
\end{tikzpicture}""",

# 1373 Q2 : C(x) = x² − 10x + 50 sur [0 ; 15], minimum 25 en 5
"optim_cout": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-0.9, xmax=16.4, ymin=-12, ymax=140,
  xtick={5,10,15}, xticklabels={}, ytick={25,50,75,100,125}, xlabel={$x$}, ylabel={$C$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:3,25) -- (axis cs:7,25);
  \addplot[courbe, domain=0:15] {x^2-10*x+50};
  \guides{5}{25}
  \pnt{5}{25} \pnt{0}{50} \pnt{15}{125}
  \node[note, fill=none, anchor=west, text=otGreenDark] at (axis cs:6.9,13) {coût minimal : $25$};
  \node[etiq, fill=none, text=otNavy, anchor=east] at (axis cs:12.6,100) {$\mathcal{C}_C$};
\end{axis}
\end{tikzpicture}""",

# 1373 Q3 : s(t) = −t² + 6t + 2, arrêt à t = 3, position maximale 11
"optim_mobile": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-0.5, xmax=7.6, ymin=-6.2, ymax=14.6,
  xtick={1,2,3,4,5,6,7}, xticklabels={}, ytick={-4,-2,2,4,6,8,10,12}, yticklabels={$-4$,,$2$,,$6$,,$10$,},
  xlabel={$t$}, ylabel={$s$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:1.8,11) -- (axis cs:4.2,11);
  \addplot[courbe, domain=0:7] {-x^2+6*x+2};
  \guides{3}{11}
  \pnt{3}{11} \pnt{0}{2}
  \node[note, fill=none, anchor=south, text=otGreenDark, align=center] at (axis cs:3,11.4) {$v(3) = 0$ : position maximale $11$ m};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:0.25,7.0) {$\mathcal{C}_s$};
\end{axis}
\end{tikzpicture}""",

# 1367 Q2 : f(x) = x² − 4x + 3, tangente horizontale y = −1 en 2
"calc_tangente_horiz": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5.6cm, xmin=-0.6, xmax=4.7, ymin=-2.1, ymax=4.6,
  xtick={1,2,3,4}, xticklabels={}, ytick={-1,1,2,3,4}, yticklabels={$-1$,$1$,,$3$,}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:0.7,-1) -- (axis cs:3.3,-1);
  \addplot[courbe, domain=-0.08:4.08] {x^2-4*x+3};
  \guidev{2}{-1}
  \pnt{2}{-1}
  \node[note, fill=none, anchor=west, text=otGreenDark] at (axis cs:3.35,-1) {$y = -1$};
  \node[note, fill=none, anchor=north, text=otGreenDark] at (axis cs:2,-1.2) {tangente horizontale};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:4.1,3.6) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# 1372 Q3 : f(x) = (x² − 3)²
"etude_carre": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-2.8, xmax=2.9, ymin=-1.4, ymax=11.2,
  xtick={-1,1}, xticklabels={}, ytick={2,4,6}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:-0.75,9) -- (axis cs:0.75,9);
  \draw[otGreenDark, line width=2pt] (axis cs:-2.25,0) -- (axis cs:-1.21,0);
  \draw[otGreenDark, line width=2pt] (axis cs:1.21,0) -- (axis cs:2.25,0);
  \addplot[courbe, domain=-2.45:2.45] {(x^2-3)^2};
  \pnt{0}{9} \pnt{-1.7320508}{0} \pnt{1.7320508}{0}
  \node[note, fill=none, anchor=south west, text=otGreenDark] at (axis cs:0.12,9.25) {maximum local $9$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:2.47,9.4) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# 1370 B : f(x) = x³ − 6x² + 12x − 3 = (x − 2)³ + 5
"examA_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=6.4cm, xmin=-0.6, xmax=4.5, ymin=-4.2, ymax=14.2,
  xtick={1,2,3,4}, xticklabels={}, ytick={-2,2,4,6,8,10,12}, yticklabels={$-2$,$2$,,$6$,,$10$,}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:0.75,5) -- (axis cs:3.25,5);
  \addplot[courbe, domain=0:4] {(x-2)^3+5};
  \guides{2}{5}
  \pnt{2}{5}
  \node[note, fill=none, anchor=south east] at (axis cs:1.92,5.35) {$(2\,;5)$};
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:2.25,3.6) {tangente horizontale\\mais pas d’extremum};
  \node[etiq, fill=none, text=otNavy, anchor=east] at (axis cs:3.75,12.6) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# 1370 énoncé C : boîte sans couvercle, base carrée de côté x, hauteur 10 − x
"examA_boite": r"""
\begin{tikzpicture}[line join=round]
  \def\a{3.0} \def\h{2.2} \def\dx{1.25} \def\dy{0.75}
  \coordinate (A) at (0,0); \coordinate (B) at (\a,0); \coordinate (C) at (\a+\dx,\dy); \coordinate (D) at (\dx,\dy);
  \coordinate (E) at (0,\h); \coordinate (F) at (\a,\h); \coordinate (G) at (\a+\dx,\h+\dy); \coordinate (H) at (\dx,\h+\dy);
  \fill[otSky] (A) -- (B) -- (C) -- (G) -- (H) -- (E) -- cycle;
  \draw[otNavy!55, line width=.7pt, dash pattern=on 3pt off 2pt] (A) -- (D) -- (C) (D) -- (H);
  \draw[geoTrait] (A) -- (B) -- (C) -- (G) -- (F) -- (B) (A) -- (E) -- (F) (E) -- (H) -- (G);
  \cote[0.4]{B}{A}{$x$}
  \cote[0.35]{C}{B}{$x$}
  \cote[0.4]{A}{E}{$10 - x$}
  \node[note, fill=none, anchor=south] at ($(H)!0.5!(G)+(0,0.12)$) {sans couvercle};
\end{tikzpicture}""",

# 1370 C : V(x) = 10x² − x³ sur [0 ; 10]
"examA_volume": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-0.7, xmax=11.2, ymin=-16, ymax=182,
  xtick={2,4,6.6666667,8,10}, xticklabels={}, ytick={50,100,150}, xlabel={$x$}, ylabel={$V$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:5.2,148.148) -- (axis cs:8.1,148.148);
  \addplot[courbe, domain=0:10] {10*x^2-x^3};
  \guidev{6.6666667}{148.148}
  \pnt{6.6666667}{148.148}
  \pnt[otOrange!85!black]{2}{32} \pnt[otOrange!85!black]{8}{128}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:6.67,152) {volume maximal $\approx 148{,}1$ cm³};
  \node[note, fill=none, anchor=north west, text=otOrange!80!black] at (axis cs:2.2,30) {$V(2) = 32$};
  \node[note, fill=none, anchor=west, text=otOrange!80!black] at (axis cs:8.25,128) {$V(8) = 128$};
\end{axis}
\end{tikzpicture}""",

# 1374 C : f(x) = x³ − 3x² + 4, tangente en 1 : y = −3x + 5
"examB_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=6.2cm, xmin=-1.7, xmax=3.6, ymin=-2.2, ymax=6.8,
  xtick={-1,1,2,3}, xticklabels={}, ytick={2,4,6}, yticklabels={$2$,,$6$}]
  \addplot[otGreenDark, line width=1.2pt, domain=0.1:2.3] {-3*x+5};
  \addplot[courbe, domain=-1.15:3.2] {x^3-3*x^2+4};
  \guides{1}{2}
  \pnt{1}{2} \pnt{0}{4} \pnt{2}{0}
  \node[etiq, fill=none, text=otGreenDark, anchor=south west] at (axis cs:0.4,4.55) {$T : y = -3x + 5$};
  \node[note, fill=none, anchor=south east, align=center] at (axis cs:-0.12,4.15) {maximum\\local $4$};
  \node[note, fill=none, anchor=north west, align=left] at (axis cs:2.35,-0.2) {minimum\\local $0$};
  \node[etiq, fill=none, text=otNavy, anchor=east] at (axis cs:3.05,5.9) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# 1374 énoncé D : boîte cylindrique de rayon r et de hauteur h
"examB_cylindre": r"""
\begin{tikzpicture}[line join=round]
  \def\r{1.5} \def\e{0.42} \def\h{3.0}
  \fill[otSky] (-\r,0) arc[start angle=180, end angle=360, x radius=\r, y radius=\e] -- (\r,\h)
     arc[start angle=0, end angle=-180, x radius=\r, y radius=\e] -- cycle;
  \draw[otNavy!55, line width=.7pt, dash pattern=on 3pt off 2pt] (\r,0) arc[start angle=0, end angle=180, x radius=\r, y radius=\e];
  \draw[geoTrait] (-\r,0) arc[start angle=180, end angle=360, x radius=\r, y radius=\e];
  \draw[geoTrait] (0,\h) ellipse[x radius=\r, y radius=\e];
  \draw[geoTrait] (-\r,0) -- (-\r,\h) (\r,0) -- (\r,\h);
  \draw[otNavy, line width=.8pt] (0,\h) -- (\r,\h);
  \fill[otNavy] (0,\h) circle (1.6pt);
  \node[anchor=south, inner sep=2pt] at (0.75,\h+0.03) {$r$};
  \draw[cote] (\r+0.45,0) -- (\r+0.45,\h) node[midway, coteTexte] {$h$};
  \draw[otMuted!70, line width=.4pt] (\r+0.08,0) -- (\r+0.55,0) (\r+0.08,\h) -- (\r+0.55,\h);
\end{tikzpicture}""",

# 1374 D : S(r) = 2πr² + 1000/r, minimum en r0 ≈ 4,30
"examB_aire": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.8cm, xmin=-0.5, xmax=9.4, ymin=-50, ymax=720,
  xtick={2,4.3012701,6,8}, xticklabels={}, ytick={100,200,300,400,500,600}, xlabel={$r$}, ylabel={$S$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:3.2,348.73) -- (axis cs:5.4,348.73);
  \addplot[courbe, domain=1.6:8.6] {2*pi*x^2+1000/x};
  \guidev{4.3012701}{348.73}
  \pnt{4.3012701}{348.73}
  \node[note, fill=none, anchor=north east, text=otGreenDark, align=right] at (axis cs:4.05,315) {aire\\minimale};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:8.0,640) {$\mathcal{C}_S$};
\end{axis}
\end{tikzpicture}""",

# nouveau-3 corrigé : signe de f' lu sur sa courbe
"derivee_signe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=6.0cm, xmin=-3.5, xmax=4.6, ymin=-3.1, ymax=4.7,
  xtick={-3,-2,-1,1,2,3,4}, xticklabels={}, ytick={-1,1,2,3,4}, yticklabels={$-1$,$1$,,,},
  yticklabel style={anchor=north east, xshift=-1pt, yshift=-1pt}]
  \sol{-3}{-1} \sol{3}{4}
  \draw[otOrange,line width=3pt,line cap=butt,opacity=0.9] (axis cs:-1,0) -- (axis cs:3,0);
  \addplot[otGreenDark, line width=1.35pt, domain=-3:-1] {(x+1)*(x-3)/3};
  \addplot[otGreenDark, line width=1.35pt, domain=3:4] {(x+1)*(x-3)/3};
  \addplot[otOrange!85!black, line width=1.35pt, domain=-1:3] {(x+1)*(x-3)/3};
  \pnt[otNavy]{-1}{0} \pnt[otNavy]{3}{0}
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:-2.0,4.45) {$f'(x) > 0$\\$f$ croissante};
  \node[note, fill=none, anchor=north west, text=otOrange!80!black, align=left] at (axis cs:0.25,-1.55) {$f'(x) < 0$\\$f$ décroissante};
\end{axis}
\end{tikzpicture}""",

# nouveau-2 Q1 : f(x) = x + 4/x sur [1 ; 6], encadrement 4 ≤ f(x) ≤ 20/3
"encadrement": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.6cm, xmin=-0.4, xmax=6.8, ymin=-0.7, ymax=8.2,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={2,4,5,6.6666667}, yticklabels={$2$,$4$,$5$,$\displaystyle\frac{20}{3}$}]
  \draw[otGreenDark, line width=0.8pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,4) -- (axis cs:6.3,4);
  \draw[otGreenDark, line width=0.8pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,6.6666667) -- (axis cs:6.3,6.6666667);
  \addplot[courbe, domain=1:6] {x+4/x};
  \guidev{1}{5} \guidev{6}{6.6666667}
  \pnt{1}{5} \pnt{2}{4} \pnt{6}{6.6666667}
  \node[note, fill=none, anchor=north, text=otGreenDark] at (axis cs:3.6,3.85) {minimum $4$};
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:3.4,6.8) {maximum $\dfrac{20}{3}$};
  \node[etiq, fill=none, text=otNavy, anchor=south east] at (axis cs:4.0,5.7) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# cours : optimisation, enclos le long d'un mur, A(x) = 20x − 2x²
"cours_optimisation": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=5.6cm, xmin=-0.6, xmax=11.0, ymin=-6, ymax=62,
  xtick={2,4,5,8,10}, xticklabels={}, ytick={10,20,30,40,50}, xlabel={$x$}, ylabel={$A$}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:3.4,50) -- (axis cs:6.6,50);
  \addplot[courbe, domain=0:10] {20*x-2*x^2};
  \guides{5}{50}
  \pnt{5}{50}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:5,51.2) {aire maximale : $50$ m²};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:9.15,24) {$\mathcal{C}_A$};
\end{axis}
\end{tikzpicture}""",

# cours : x + 1/x ≥ 2 sur ]0 ; +∞[
"cours_inegalite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=5.4cm, xmin=-0.4, xmax=4.7, ymin=-0.5, ymax=5.2,
  xtick={1,2,3,4}, xticklabels={}, ytick={1,2,3,4}]
  \addplot[otGreenDark, line width=1.1pt, domain=0:4.4] {2};
  \addplot[courbe, domain=0.24:4.4] {x+1/x};
  \guidev{1}{2}
  \pnt{1}{2}
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:0.32,4.7) {$y = x + \frac{1}{x}$};
  \node[etiq, fill=none, text=otGreenDark, anchor=north] at (axis cs:3.4,1.9) {$y = 2$};
\end{axis}
\end{tikzpicture}""",
}

FIGURES = {
# ------------------------------------------------------------------ cours
"cours_secantes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=6.4cm, xmin=-0.7, xmax=4.3, ymin=-0.8, ymax=6.6,
  xtick={1}, xticklabels={$a$}, ytick=\empty]
  \addplot[otOrange!85!black, line width=0.8pt, domain=-0.35:3.35] {2*(x-1)+1.5};
  \addplot[otOrange!85!black, line width=0.8pt, domain=-0.35:3.6] {1.6*(x-1)+1.5};
  \addplot[otOrange!85!black, line width=0.8pt, domain=-0.35:3.9] {1.3*(x-1)+1.5};
  \addplot[otGreenDark, line width=1.3pt, domain=-0.35:4.2] {x+0.5};
  \addplot[courbe, domain=-0.6:3.25] {0.5*x^2+1};
  \guidev{1}{1.5}
  \pnt{1}{1.5}
  \pnt[otOrange!85!black]{3}{5.5} \pnt[otOrange!85!black]{2.2}{3.42} \pnt[otOrange!85!black]{1.6}{2.28}
  \node[etiq, fill=none, anchor=north west] at (axis cs:1.1,1.45) {$A$};
  \node[etiq, fill=none, anchor=east, text=otOrange!80!black] at (axis cs:2.85,5.6) {$M$};
  \node[note, fill=none, anchor=north west, text=otOrange!80!black, align=left] at (axis cs:2.0,1.3) {$M$ se rapproche de $A$ :\\$h$ tend vers $0$};
  \node[etiq, fill=none, text=otNavy, anchor=south] at (axis cs:3.25,6.35) {$\mathcal{C}_f$};
  \node[note, fill=none, anchor=west, text=otGreenDark, align=left] at (axis cs:4.25,4.75) {tangente\\pente $f'(a)$};
  \node[note, fill=none, anchor=west, text=otOrange!80!black, align=left] at (axis cs:3.95,3.0) {sécantes\\$(AM)$};
\end{axis}
\end{tikzpicture}""",

"cours_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=6.4cm, xmin=-2.4, xmax=3.3, ymin=-1.6, ymax=5.4,
  xtick={-2,-1,1,2,3}, ytick={-1,1,2,3,4,5}]
  \addplot[otGreenDark, line width=1.2pt, domain=-0.25:3.15] {2*x-1};
  \addplot[courbe, domain=-2.25:2.3] {x^2};
  \draw[otOrange!85!black, line width=1pt, dash pattern=on 4pt off 2pt] (axis cs:1,1) -- (axis cs:2,1) -- (axis cs:2,3);
  \node[anchor=north, text=otOrange!80!black] at (axis cs:1.5,0.95) {$1$};
  \node[anchor=west, text=otOrange!80!black] at (axis cs:2.06,1.75) {$f'(1) = 2$};
  \pnt{1}{1}
  \node[etiq, fill=none, anchor=south east] at (axis cs:0.92,1.1) {$A$};
  \node[etiq, fill=none, text=otNavy, anchor=north west] at (axis cs:0.15,5.35) {$y = x^2$};
  \node[etiq, fill=none, text=otGreenDark, anchor=north] at (axis cs:2.1,-0.62) {$T : y = 2x - 1$};
\end{axis}
\end{tikzpicture}""",

"cours_variations": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=6.2cm, xmin=-2.6, xmax=2.7, ymin=-3.4, ymax=3.6,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-2,-1,1,2}, yticklabels={$-2$,$-1$,$1$,}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:-1.75,2) -- (axis cs:-0.25,2);
  \draw[otGreenDark, line width=1.2pt] (axis cs:0.25,-2) -- (axis cs:1.75,-2);
  \addplot[courbe, domain=-2.15:2.15] {x^3-3*x};
  \guides{-1}{2} \guides{1}{-2}
  \pnt{-1}{2} \pnt{1}{-2}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:-1,2.1) {maximum local $2$};
  \node[note, fill=none, anchor=north, text=otGreenDark] at (axis cs:1,-2.1) {minimum local $-2$};
  \node[etiq, fill=none, text=otNavy, anchor=north west] at (axis cs:-2.55,3.5) {$y = x^3 - 3x$};
\end{axis}
\end{tikzpicture}""",

"cours_nonderivable": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=g, width=3.4cm, height=3.6cm, xmin=-1.6, xmax=1.7, ymin=-0.3, ymax=1.75,
  xtick={-1,1}, ytick={1}, grid=none, ylabel={}]
  \addplot[courbe, domain=-1.45:1.45, samples=3] {abs(x)};
  \pnt{0}{0}
  \node[note, fill=none, anchor=north east, text=otGreenDark] at (axis cs:-0.62,0.48) {pente $-1$};
  \node[note, fill=none, anchor=north west, text=otGreenDark] at (axis cs:0.62,0.48) {pente $1$};
\end{axis}
\node[anchor=south, text=otNavy] at ($(g.north)+(0,0.08)$) {$y = |x|$};
\begin{axis}[otWeb, at={(g.east)}, anchor=west, xshift=1.4cm, name=d, width=3.4cm, height=3.6cm,
  xmin=-0.3, xmax=2.2, ymin=-0.3, ymax=1.75, xtick={1,2}, ytick={1}, grid=none, ylabel={}]
  \draw[otGreenDark, line width=0.9pt, dash pattern=on 3pt off 2pt] (axis cs:0,0) -- (axis cs:1.05,1.05);
  \draw[otGreenDark, line width=0.9pt, dash pattern=on 3pt off 2pt] (axis cs:0,0) -- (axis cs:0.39,1.56);
  \addplot[courbe, domain=0:2.1, samples=200] {sqrt(x)};
  \pnt{0}{0} \pnt[otGreenDark]{1}{1} \pnt[otGreenDark]{0.0625}{0.25}
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:1.05,0.82) {pentes\\$1/\sqrt{h}$};
\end{axis}
\node[anchor=south, text=otNavy] at ($(d.north)+(0,0.08)$) {$y = \sqrt{x}$};
\end{tikzpicture}""",

# ------------------------------------------------------------------ exercices
"lecture_g": lecture_g(False),
"lecture_g_corrige": lecture_g(True),
"lecture_f": lecture_f(False),
"lecture_f_corrige": lecture_f(True),

"etude_1368": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=6.0cm, xmin=-0.6, xmax=4.7, ymin=-1.6, ymax=7.4,
  xtick={1,2,3,4}, ytick={1,2,3,4,5,6}]
  \draw[otGreenDark, line width=1.2pt] (axis cs:0.35,5) -- (axis cs:1.65,5);
  \draw[otGreenDark, line width=1.2pt] (axis cs:2.35,1) -- (axis cs:3.65,1);
  \addplot[courbe, domain=-0.22:4.3] {x^3-6*x^2+9*x+1};
  \guides{1}{5} \guidev{3}{1}
  \pnt{1}{5} \pnt{3}{1}
  \node[note, fill=none, anchor=south, text=otGreenDark] at (axis cs:1,5.1) {maximum local $5$};
  \node[note, fill=none, anchor=north, text=otGreenDark] at (axis cs:3,0.9) {minimum local $1$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:4.3,5.6) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"tangente_cube": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=7.0cm, xmin=-2.7, xmax=2.3, ymin=-10, ymax=6.4,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-8,-6,-4,-2,2,4}]
  \addplot[otGreenDark, line width=1.2pt, domain=-2.45:2.25] {3*x-2};
  \addplot[courbe, domain=-2.13:1.82] {x^3};
  \guides{1}{1} \guidev{-2}{-8}
  \pnt{1}{1} \pnt{-2}{-8}
  \node[etiq, fill=none, anchor=south east] at (axis cs:0.95,1.25) {$A$};
  \node[etiq, fill=none, text=otNavy, anchor=south] at (axis cs:1.6,6.0) {$\mathcal{C}_f$};
  \node[etiq, fill=none, text=otGreenDark, anchor=west] at (axis cs:2.05,3.0) {$T$};
  \node[note, fill=none, anchor=north west, text=otGreenDark, align=left] at (axis cs:-2.65,5.9) {$\mathcal{C}_f$ au-dessus\\de $T$ sur\\$[-2\,;+\infty[$};
\end{axis}
\end{tikzpicture}""",

"courbe_derivee": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=6.0cm, xmin=-3.5, xmax=4.6, ymin=-2.2, ymax=4.7,
  xtick={-3,-2,-1,1,2,3,4}, ytick={-2,-1,1,2,3,4},
  yticklabel style={anchor=north east, xshift=-1pt, yshift=-1pt}]
  \addplot[courbe2, domain=-3:4] {(x+1)*(x-3)/3};
  \pnt[otGreenDark]{-3}{4} \pnt[otGreenDark]{4}{1.6667}
  \node[etiq, fill=none, text=otGreenDark, anchor=west] at (axis cs:3.55,3.0) {courbe de $f'$};
\end{axis}
\end{tikzpicture}""",
"cube_enonce": cube(False),
}
FIGURES.update(NOUVELLES)
