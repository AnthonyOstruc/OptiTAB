# -*- coding: utf-8 -*-
"""Figures de la notion « Étudier les variations et les extremums d'une fonction » (Seconde).

Compilées par outils/figures_livre.py (style des livres : repère otWeb,
courbes bleu marine, maximum en vert foncé, minimum en orange, seuils en
pointillés orange). Les courbes « lues » (cours, exercice 2012) sont des
splines de Hermite monotones par morceaux : les nœuds donnés ci-dessous sont
exactement les valeurs du texte (vérifiées par verif_173.py).
"""

XLAB = {
    "cours_courbe": [(-3, "c", "-3"), (-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1"),
                     (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5")],
    "ex_courbe_corrige": [(-4, "c", "-4"), (-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"),
                          (1, "h", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
}

# ------------------------------------------------------------ outils
# nœuds (x, y, pente) ; pente nulle aux extremums
COURBE_COURS = [(-3, 2, -3.2), (-1, -2, 0), (2, 3, 0), (5, 0, -2.2)]
COURBE_EX = [(-4, 1, 1.5), (-2, 3, 0), (1, -2, 0), (4, 2, 2)]


def hermite_val(pts, t):
    for (x0, y0, s0), (x1, y1, s1) in zip(pts, pts[1:]):
        if x0 <= t <= x1:
            h = x1 - x0
            s = (t - x0) / h
            h00 = 2 * s**3 - 3 * s**2 + 1
            h10 = s**3 - 2 * s**2 + s
            h01 = -2 * s**3 + 3 * s**2
            h11 = s**3 - s**2
            return h00 * y0 + h10 * h * s0 + h01 * y1 + h11 * h * s1
    raise ValueError(t)


def trace(pts, style="courbe", n=240):
    a, b = pts[0][0], pts[-1][0]
    c = " ".join("(%.4f,%.4f)" % (a + (b - a) * k / n, hermite_val(pts, a + (b - a) * k / n))
                 for k in range(n + 1))
    return r"\addplot[%s] coordinates {%s};" % (style, c)


PREAMBULE_EXTRA = r"""
\tikzset{
  noteV/.style={font=\otRegular\fontsize{8.5}{10.5}\selectfont,text=otGreenDark,align=center,inner sep=1.2pt},
  noteO/.style={font=\otRegular\fontsize{8.5}{10.5}\selectfont,text=otOrange!80!black,align=center,inner sep=1.2pt},
  gradY/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.2pt,xshift=1pt,yshift=-1pt},
  titreF/.style={font=\otMedium\fontsize{8.5}{10.5}\selectfont,align=center,inner sep=1pt},
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  rep/.style={otGreenDark,line width=2pt},
}
% graduations posées à la main : x dessous / dessus, y à gauche / à droite
\newcommand{\gxb}[2]{\node[grad,anchor=north,yshift=-3.5pt] at (axis cs:#1,0) {$#2$};}
\newcommand{\gxh}[2]{\node[grad,anchor=south,yshift=3.5pt] at (axis cs:#1,0) {$#2$};}
\newcommand{\gyg}[2]{\node[grad,anchor=east,xshift=-3.5pt] at (axis cs:0,#1) {$#2$};}
\newcommand{\gyd}[2]{\node[grad,anchor=west,xshift=3.5pt] at (axis cs:0,#1) {$#2$};}
"""

# petit repère sans quadrillage (cours : sens de variation)
SENS = r"""
\begin{axis}[otWeb, name=%(nom)s, %(pos)s width=3.1cm, height=2.9cm, xmin=0, xmax=4.1, ymin=0, ymax=4.1,
  grid=none, xtick={1.2,3}, xticklabels={$u$,$v$}, ytick={%(yt)s}, yticklabels={%(yl)s},
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt}]
  \addplot[%(st)s, domain=0.3:3.8] {%(f)s};
  \draw[guide] (axis cs:1.2,0) -- (axis cs:1.2,%(fu)s) -- (axis cs:0,%(fu)s);
  \draw[guide] (axis cs:3,0) -- (axis cs:3,%(fv)s) -- (axis cs:0,%(fv)s);
  \pnt[%(c)s]{1.2}{%(fu)s} \pnt[%(c)s]{3}{%(fv)s}
\end{axis}
\node[titreF,text=%(tc)s,anchor=south] at ([yshift=12pt]%(nom)s.north) {%(titre)s};
\node[anchor=north,font=\small] at ([yshift=-20pt]%(nom)s.south) {%(regle)s};
"""


def sens():
    f1, f2 = "0.6+0.2*x^2", "3.6-0.2*x^2"
    g1 = lambda t: 0.6 + 0.2 * t * t
    g2 = lambda t: 3.6 - 0.2 * t * t
    a = SENS % dict(nom="A", pos="", f=f1, st="courbe", c="otNavy", tc="otNavy",
                    fu="%.3f" % g1(1.2), fv="%.3f" % g1(3), yt="%.3f,%.3f" % (g1(1.2), g1(3)),
                    yl="$f(u)$,$f(v)$", titre="croissante :\\\\ l'ordre est conservé",
                    regle=r"$u<v \Rightarrow f(u)\le f(v)$")
    b = SENS % dict(nom="B", pos="at={(4.6cm,0)},", f=f2, st="courbe2", c="otGreenDark", tc="otGreenDark",
                    fu="%.3f" % g2(1.2), fv="%.3f" % g2(3), yt="%.3f,%.3f" % (g2(3), g2(1.2)),
                    yl="$f(v)$,$f(u)$", titre="décroissante :\\\\ l'ordre est inversé",
                    regle=r"$u<v \Rightarrow f(u)\ge f(v)$")
    return "\\begin{tikzpicture}\n" + a + b + "\\end{tikzpicture}"


FIGURES = {
"cours_sens": sens(),

"cours_courbe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=8.2cm, height=5.2cm, xmin=-3.7, xmax=5.6, ymin=-3.3, ymax=4.1,
  xtick={-3,-2,-1,1,2,3,4,5}, xticklabels={}, ytick={-2,-1,1,2,3}, yticklabels={$-2$,,$1$,$2$,$3$}]
  \guides{2}{3} \guidev{-1}{-2}
  \node[gradY,anchor=north west] at (axis cs:0,-1) {$-1$};
  """ + trace(COURBE_COURS) + r"""
  \pnt{-3}{2} \pnt{5}{0}
  \pnt[otGreenDark]{2}{3} \pnt[otOrange]{-1}{-2}
  \node[noteV,anchor=south] at (axis cs:2.75,3.12) {maximum $3$\\ atteint en $x=2$};
  \node[noteO,anchor=north] at (axis cs:-1.9,-2.25) {minimum $-2$\\ atteint en $x=-1$};
  \node[text=otNavy,anchor=south west] at (axis cs:4.25,1.25) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------ exercice 2012 (lecture graphique)
"ex_courbe_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.8cm, height=5.4cm, xmin=-4.6, xmax=4.7, ymin=-2.7, ymax=3.8,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-2,-1,1,2,3}, yticklabels={$-2$,,$1$,$2$,$3$}]
  \node[gradY,anchor=north east,xshift=-2pt] at (axis cs:0,-1) {$-1$};
  """ + trace(COURBE_EX) + r"""
  \pnt{-4}{1} \pnt{4}{2}
  \node[text=otNavy,anchor=south east] at (axis cs:-2.9,3.05) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"ex_courbe_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.8cm, height=5.4cm, xmin=-4.6, xmax=4.7, ymin=-3.4, ymax=4.3,
  xtick={-4,-3,-2,-1,1,2,3,4}, xticklabels={}, ytick={-2,-1,1,2,3}, yticklabels={$-2$,,$1$,$2$,$3$}]
  \node[gradY,anchor=north east,xshift=-2pt] at (axis cs:0,-1) {$-1$};
  \draw[guide] (axis cs:-2,0) -- (axis cs:-2,3) -- (axis cs:0,3);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,-2) -- (axis cs:0,-2);
  """ + trace(COURBE_EX) + r"""
  \pnt{-4}{1} \pnt{4}{2}
  \pnt[otGreenDark]{-2}{3} \pnt[otOrange]{1}{-2}
  \node[noteV,anchor=south] at (axis cs:-2,3.12) {maximum $3$};
  \node[noteO,anchor=north] at (axis cs:1.6,-2.2) {minimum $-2$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------ exercice 2024 (balayage)
"balayage": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-0.4, xmax=4.7, ymin=-0.6, ymax=7.9,
  xtick={1,2,3,4}, ytick={2,4,6}]
  \addplot[courbe, domain=0:4] {x*(5-x)};
  \pnt{0}{0} \pnt{1}{4} \pnt{2}{6} \pnt{3}{6} \pnt{4}{4}
  \pnt[otGreenDark]{2.5}{6.25}
  \node[noteV,anchor=south] at (axis cs:2.5,6.4) {maximum réel $6{,}25$ en $x=2{,}5$};
  \node[text=otNavy,anchor=north west] at (axis cs:3.75,2.9) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------ exercice 2022 (inéquation par la courbe)
"parabole_2022": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=5.6cm, xmin=-1.6, xmax=6.7, ymin=-12, ymax=7.2,
  xtick={-1,1,2,3,4,5,6}, ytick={-10,-8,-6,-4,-2,2,4}]
  \draw[seuil] (axis cs:-1.4,1) -- (axis cs:6.3,1);
  \sol{0}{4} \borneF{0} \borneF{4}
  \guidev{4}{1}
  \addplot[courbe, domain=-1:6] {-(x-2)^2+5};
  \pnt{-1}{-4} \pnt{6}{-11}
  \pnt[otGreenDark]{2}{5} \pnt[otOrange]{0}{1} \pnt[otOrange]{4}{1}
  \node[noteV,anchor=south] at (axis cs:2,5.3) {maximum $5$};
  \node[noteO,anchor=south west] at (axis cs:4.9,1.25) {$y=1$};
  \node[text=otNavy,anchor=east] at (axis cs:5.45,-10) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------ exercice 2023 (rectangle)
"rectangle_2023": r"""
\begin{tikzpicture}
\coordinate (A) at (0,0); \coordinate (B) at (5,0); \coordinate (C) at (5,2.3); \coordinate (D) at (0,2.3);
\fill[geoRemplissage] (A) -- (B) -- (C) -- (D) -- cycle;
\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;
\cote{B}{A}{$x$}
\cote[0.8]{C}{B}{$10-x$}
\node[text=otInk] at (2.5,1.15) {aire $A(x)$};
\end{tikzpicture}""",

"aire_2023": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.8cm, height=5cm, xmin=-0.6, xmax=11, ymin=-2.5, ymax=30,
  xtick={1,2,3,4,5,6,7,8,9,10}, ytick={5,10,15,20,25}, ylabel={$A$}]
  \draw[seuil] (axis cs:0,21) -- (axis cs:10.3,21);
  \draw[guide] (axis cs:5,0) -- (axis cs:5,25) -- (axis cs:0,25);
  \sol{3}{7} \borneF{3} \borneF{7}
  \guidev{3}{21} \guidev{7}{21}
  \addplot[courbe, domain=0:10] {x*(10-x)};
  \pntv{0}{0} \pntv{10}{0}
  \pnt[otGreenDark]{5}{25} \pnt[otOrange]{3}{21} \pnt[otOrange]{7}{21}
  \node[noteV,anchor=south] at (axis cs:5,25.6) {maximum $25$};
  \node[noteO,anchor=south] at (axis cs:9.4,21.4) {$y=21$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------ nouveau-2 (droites)
"droites_n2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=6.6cm, xmin=-3.5, xmax=3.5, ymin=-2.5, ymax=4.5,
  xtick={-3,-2,-1,1,2,3}, ytick={-2,-1,1,2,3,4}, yticklabels={$-2$,$-1$,$1$,$2$,,$4$}]
  \node[gradY,anchor=south west,yshift=4pt] at (axis cs:0,3) {$3$};
  \addplot[courbe, domain=-3.5:3.5] {0.5*x+1};
  \addplot[courbe2, domain=-0.7:2.7] {-2*x+3};
  \node[text=otNavy,anchor=south east] at (axis cs:3.3,2.75) {$\mathcal{D}_f$};
  \node[text=otGreenDark,anchor=south west] at (axis cs:0.5,2.45) {$\mathcal{D}_g$};
\end{axis}
\end{tikzpicture}""",
}

# ====================================================== finition 2026-11-02
AXN = r"otWeb, xticklabels={}, yticklabels={}"


def gx(f, xs, seuil):
    """Graduations de l'axe des abscisses du côté libre : dessous si la courbe
    est au-dessus de l'axe (ou loin dessous), dessus sinon."""
    out = []
    for t in xs:
        y = f(t)
        lab = ("%g" % t).replace("-", "-").replace(".", "{,}")
        out.append((r"\gxb{%s}{%s}" if (y > 0 or y < -seuil) else r"\gxh{%s}{%s}") % (t, lab))
    return " ".join(out)


def fig(opts, corps):
    return "\\begin{tikzpicture}\n\\begin{axis}[" + AXN + ", " + opts + "]\n" + corps + "\n\\end{axis}\n\\end{tikzpicture}"


# 2018 : une courbe compatible avec le tableau (décroît de 2 à -4, croît jusqu'à 3, constante sur [4 ; 5])
COURBE_2018 = [(-3, 2, -1.5), (1, -4, 0), (4, 3, 0)]
f2018 = lambda t: hermite_val(COURBE_2018, t) if t <= 4 else 3
FIGURES["ex_tableau_2018"] = fig(
    r"width=7cm, height=5.2cm, xmin=-3.6, xmax=5.7, ymin=-5.6, ymax=4.6, xtick={-3,-2,-1,1,2,3,4,5}, ytick={-4,-3,-2,-1,1,2,3,4}",
    trace(COURBE_2018) + r"""
  \draw[rep] (axis cs:4,3) -- (axis cs:5,3);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,-4) -- (axis cs:0,-4);
  \draw[guide] (axis cs:4,0) -- (axis cs:4,3);
  \draw[guide] (axis cs:5,0) -- (axis cs:5,3);
  \pnt{-3}{2} \pnt[otOrange]{1}{-4} \pnt[otGreenDark]{4}{3} \pnt[otGreenDark]{5}{3}
  """ + gx(f2018, [-3, -1, 1, 2, 3, 4, 5], 1.4) + r"""
  \gyg{2}{2} \gyg{3}{3} \gyd{-2}{-2}
  \node[noteV,anchor=south] at (axis cs:4.5,3.15) {maximum $3$};
  \node[noteO,anchor=north west] at (axis cs:1.15,-4.2) {minimum $-4$ en $x=1$};
""")

# 2015 : r(x) = sqrt(5 - 2x) sur [-2 ; 5/2], r(x) >= 2 <=> x <= 1/2
FIGURES["ex_racine_2015"] = fig(
    r"width=6.8cm, height=4.4cm, xmin=-2.7, xmax=3.3, ymin=-0.7, ymax=3.7, xtick={-2,-1,1,2}, ytick={1,2,3}",
    r"""
  \draw[seuil] (axis cs:-2.6,2) -- (axis cs:3.2,2);
  \addplot[courbe, domain=-2:2.5, samples=300] {sqrt(5-2*x)};
  \guidev{0.5}{2}
  \sol{-2}{0.5} \borneF{-2} \borneF{0.5}
  \pnt[otGreenDark]{-2}{3} \pnt[otOrange]{2.5}{0} \pnt[otOrange]{0.5}{2}
  \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2}
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-2,0) {$-2$};
  \node[grad,text=otGreenDark,anchor=north west,xshift=1pt,yshift=-3.5pt] at (axis cs:0.5,0) {$\frac{1}{2}$};
  \node[grad,anchor=north,yshift=-3.5pt] at (axis cs:2.5,0) {$\frac{5}{2}$};
  \gyd{1}{1} \gyd{3}{3}
  \node[noteO,anchor=south east] at (axis cs:3.2,2.1) {$y=2$};
  \node[noteV,anchor=west] at (axis cs:-1.85,3.15) {maximum $3$};
  \node[text=otNavy,anchor=south west] at (axis cs:1.5,1.45) {$y=r(x)$};
""")

# 2021 : p(x) = -3x + 7 sur [-2 ; 5], taux d'accroissement -3
FIGURES["ex_affine_2021"] = fig(
    r"width=6.2cm, height=6.4cm, xmin=-2.8, xmax=5.8, ymin=-9.6, ymax=15.2, xtick={-2,-1,1,2,3,4,5}, ytick={-8,-4,4,8,12}",
    r"""
  \addplot[courbe, domain=-2:5] {-3*x+7};
  \draw[seuil] (axis cs:1,4) -- (axis cs:2,4);
  \draw[otOrange!85!black,line width=1.1pt,-{Stealth[length=2mm]}] (axis cs:2,4) -- (axis cs:2,1.15);
  \pnt{1}{4} \pnt{2}{1}
  \node[noteO,anchor=south] at (axis cs:1.5,4.15) {$+1$};
  \node[noteO,anchor=west] at (axis cs:2.08,2.6) {$-3$};
  \draw[guide] (axis cs:-2,0) -- (axis cs:-2,13) -- (axis cs:0,13);
  \draw[guide] (axis cs:5,0) -- (axis cs:5,-8) -- (axis cs:0,-8);
  \pnt[otGreenDark]{-2}{13} \pnt[otOrange]{5}{-8}
  \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxh{3}{3} \gxh{4}{4}
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-2,0) {$-2$};
  \node[grad,text=otOrange!80!black,anchor=south,yshift=3.5pt] at (axis cs:5,0) {$5$};
  \gyd{4}{4} \gyg{-4}{-4}
  \node[grad,text=otGreenDark,anchor=west,xshift=3.5pt] at (axis cs:0,13) {$13$};
  \node[grad,text=otOrange!80!black,anchor=east,xshift=-3.5pt] at (axis cs:0,-8) {$-8$};
  \node[noteV,anchor=east] at (axis cs:-2.2,13) {maximum};
  \node[noteO,anchor=north east] at (axis cs:4.9,-8.4) {minimum};
""")

# 2020 Q1 : fonction carré sur [-3 ; 2]
FIGURES["ex_carre_2020"] = fig(
    r"width=5.8cm, height=5.2cm, xmin=-3.7, xmax=2.8, ymin=-0.9, ymax=10.4, xtick={-3,-2,-1,1,2}, ytick={1,2,3,4,5,6,7,8,9,10}",
    r"""
  \addplot[courbe, domain=-3:2] {x^2};
  \draw[guide] (axis cs:-3,0) -- (axis cs:-3,9) -- (axis cs:0,9);
  \draw[guide] (axis cs:2,0) -- (axis cs:2,4) -- (axis cs:0,4);
  \pnt[otGreenDark]{-3}{9} \pnt[otOrange]{0}{0} \pnt{2}{4}
  \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2}
  \gyd{9}{9} \gyd{4}{4} \gyd{2}{2} \gyd{6}{6}
  \node[noteV,anchor=south] at (axis cs:-3,9.2) {maximum $9$};
  \node[noteO,anchor=north] at (axis cs:0,-1.35) {minimum $0$ en $x=0$};
  \node[text=otNavy,anchor=west] at (axis cs:-1.45,6.2) {$y=x^2$};
""")

# 2019 : f(x) = 4 - 3x sur [-2 ; 2], f(x) >= 1 <=> x <= 1
FIGURES["ex_affine_2019"] = fig(
    r"width=5.8cm, height=5.8cm, xmin=-2.8, xmax=2.9, ymin=-3.2, ymax=11.6, xtick={-2,-1,1,2}, ytick={-2,2,4,6,8,10}",
    r"""
  \draw[seuil] (axis cs:-2.7,1) -- (axis cs:2.8,1);
  \addplot[courbe, domain=-2:2] {4-3*x};
  \guidev{1}{1}
  \sol{-2}{1} \borneF{-2} \borneF{1}
  \pnt[otGreenDark]{-2}{10} \pnt[otOrange]{2}{-2} \pnt[otOrange]{1}{1}
  \draw[guide] (axis cs:-2,1) -- (axis cs:-2,10) -- (axis cs:0,10);
  \draw[guide] (axis cs:2,0) -- (axis cs:2,-2) -- (axis cs:0,-2);
  \gxb{-1}{-1}
  \node[grad,anchor=north west,xshift=1.5pt,yshift=-3.5pt] at (axis cs:2,0) {$2$};
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-2,0) {$-2$};
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:1,0) {$1$};
  \gyd{10}{10} \gyd{6}{6} \gyd{8}{8} \gyg{-2}{-2}
  \node[noteO,anchor=south east] at (axis cs:2.8,1.15) {$y=1$};
  \node[noteV,anchor=east] at (axis cs:-2.2,10) {maximum};
  \node[noteO,anchor=west] at (axis cs:2.2,-2) {minimum};
""")

# 2014 : g(x) = -2(x - 3)^2 + 7 sur [0 ; 5] ; sur [4 ; 5] : max 5, min -1
FIGURES["ex_parabole_2014"] = fig(
    r"width=6.2cm, height=6.2cm, xmin=-0.6, xmax=5.9, ymin=-12.5, ymax=9.6, xtick={1,2,3,4,5}, ytick={-10,-8,-6,-4,-2,2,4,6,8}",
    r"""
  \addplot[courbe, domain=0:5] {-2*(x-3)^2+7};
  \addplot[rep, domain=4:5] {-2*(x-3)^2+7};
  \draw[guide] (axis cs:3,0) -- (axis cs:3,7) -- (axis cs:0,7);
  \draw[guide] (axis cs:4,0) -- (axis cs:4,5);
  \pnt{0}{-11} \pnt{3}{7}
  \pnt[otGreenDark]{4}{5} \pnt[otOrange]{5}{-1}
  \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gyg{7}{7} \gyg{-11}{-11} \gyg{-4}{-4} \gyg{4}{4}
  \node[noteV,anchor=west] at (axis cs:4.12,5.3) {max. $5$};
  \node[noteO,anchor=north] at (axis cs:5,-1.5) {min. $-1$};
  \node[text=otNavy,anchor=west] at (axis cs:1.0,-8) {$y=g(x)$};
""")

# 2013 : f(x) = (x + 3)^2 - 1 sur [-6 ; 2], f(x) <= 8 <=> x dans [-6 ; 0]
FIGURES["ex_parabole_2013"] = fig(
    r"width=6.4cm, height=6.4cm, xmin=-6.8, xmax=2.8, ymin=-5.2, ymax=26.5, xtick={-6,-5,-4,-3,-2,-1,1,2}, ytick={4,8,12,16,20,24}",
    r"""
  \draw[seuil] (axis cs:-6.7,8) -- (axis cs:2.7,8);
  \addplot[courbe, domain=-6:2] {(x+3)^2-1};
  \addplot[rep, domain=-6:0] {(x+3)^2-1};
  \draw[guide] (axis cs:-3,0) -- (axis cs:-3,-1);
  \draw[guide] (axis cs:2,0) -- (axis cs:2,24) -- (axis cs:0,24);
  \guidev{-6}{8}
  \sol{-6}{0} \borneF{-6} \borneF{0}
  \pnt[otOrange]{-6}{8} \pnt[otOrange]{0}{8} \pnt[otOrange]{-3}{-1} \pnt{2}{24}
  \gxb{-5}{-5} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2}
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-6,0) {$-6$};
  \node[grad,anchor=south,yshift=3.5pt] at (axis cs:-3,0) {$-3$};
  \gyg{4}{4} \gyg{12}{12} \gyg{16}{16} \gyg{24}{24}
  \node[noteO,anchor=south west] at (axis cs:-6.7,8.4) {$y=8$};
  \node[noteO,anchor=north] at (axis cs:-3,-1.9) {minimum $-1$};
  \node[text=otNavy,anchor=west] at (axis cs:0.9,13) {$y=f(x)$};
""")

# 2016 : h(x) = |x - 2| + 1 sur [-1 ; 6], h(x) <= 4 <=> x dans [-1 ; 5]
FIGURES["ex_abs_2016"] = fig(
    r"width=6.6cm, height=4.6cm, xmin=-1.7, xmax=6.8, ymin=-0.9, ymax=6, xtick={-1,1,2,3,4,5,6}, ytick={1,2,3,4,5}",
    r"""
  \draw[seuil] (axis cs:-1.6,4) -- (axis cs:6.7,4);
  \draw[courbe] (axis cs:-1,4) -- (axis cs:2,1) -- (axis cs:6,5);
  \draw[rep] (axis cs:-1,4) -- (axis cs:2,1) -- (axis cs:5,4);
  \guidev{5}{4} \guidev{2}{1}
  \sol{-1}{5} \borneF{-1} \borneF{5}
  \pnt[otOrange]{-1}{4} \pnt[otOrange]{5}{4} \pnt[otOrange!90!black]{2}{1} \pnt{6}{5}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4} \gxb{6}{6}
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:-1,0) {$-1$};
  \node[grad,text=otGreenDark,anchor=north,yshift=-3.5pt] at (axis cs:5,0) {$5$};
  \gyg{1}{1} \gyg{2}{2} \gyg{5}{5}
  \node[noteO,anchor=south west] at (axis cs:-1.65,4.2) {$y=4$};
  \node[noteO,anchor=north west] at (axis cs:2.15,0.9) {minimum $1$};
  \node[text=otNavy,anchor=south] at (axis cs:3.6,5.05) {$y=h(x)$};
""")

# 2017 : f(x) = 1/(x^2 + 1) sur [-3 ; 3]
FIGURES["ex_cloche_2017"] = fig(
    r"width=7.4cm, height=3.8cm, xmin=-3.7, xmax=3.8, ymin=-0.22, ymax=1.38, xtick={-3,-2,-1,1,2,3}, ytick={0.5,1}",
    r"""
  \addplot[courbe, domain=-3:3, samples=300] {1/(x^2+1)};
  \guidev{-3}{0.1} \guidev{3}{0.1}
  \pnt[otGreenDark]{0}{1} \pnt[otOrange]{-3}{0.1} \pnt[otOrange]{3}{0.1}
  \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3}
  \gyg{0.5}{0{,}5}
  \node[noteV,anchor=south west] at (axis cs:0.15,1.04) {maximum $1$ en $x=0$};
  \node[noteO,anchor=south] at (axis cs:-3,0.22) {$\frac{1}{10}$};
  \node[noteO,anchor=south] at (axis cs:3,0.22) {$\frac{1}{10}$};
  \node[text=otNavy,anchor=south west] at (axis cs:1.15,0.55) {$y=\dfrac{1}{x^2+1}$};
""")

# 3746 Q4 : f(x) = x^2 + 4x, croissante sur [-2 ; +inf[ mais pas sur R
FIGURES["ex_contre_3746"] = fig(
    r"width=6.2cm, height=5.4cm, xmin=-5.7, xmax=1.8, ymin=-5.4, ymax=6.4, xtick={-5,-4,-3,-2,-1,1}, ytick={-4,-3,-2,-1,1,2,3,4,5}",
    r"""
  \addplot[courbe, domain=-5.2:-2] {x^2+4*x};
  \addplot[rep, domain=-2:1.15] {x^2+4*x};
  \draw[guide] (axis cs:-3,0) -- (axis cs:-3,-3) -- (axis cs:0,-3);
  \draw[guide] (axis cs:-2,0) -- (axis cs:-2,-4) -- (axis cs:0,-4);
  \pnt[otOrange]{-4}{0} \pnt[otOrange]{-3}{-3} \pnt{-2}{-4}
  \gxh{-3}{-3} \gxh{-2}{-2} \gxh{-1}{-1} \gxb{1}{1}
  \gyd{-3}{-3} \gyd{-4}{-4} \gyg{2}{2} \gyg{4}{4}
  \node[noteO,anchor=north east] at (axis cs:-4.1,-0.3) {$f(-4)=0$};
  \node[noteO,anchor=north east] at (axis cs:-3.15,-3.1) {$f(-3)=-3$};
  \node[noteV,anchor=north west] at (axis cs:-4.3,6.3) {croissante sur $[-2\,;+\infty[$};
""")

# cours III : f(x) = -2x + 5 sur [0 ; 3]
FIGURES["cours_affine_173"] = fig(
    r"width=5.6cm, height=5cm, xmin=-0.8, xmax=4.2, ymin=-2.2, ymax=6.6, xtick={1,2,3,4}, ytick={-1,1,2,3,4,5,6}",
    r"""
  \addplot[pale, domain=-0.5:3.35] {-2*x+5};
  \addplot[courbe, domain=0:3] {-2*x+5};
  \draw[guide] (axis cs:3,0) -- (axis cs:3,-1) -- (axis cs:0,-1);
  \pnt[otGreenDark]{0}{5} \pnt[otOrange]{3}{-1}
  \gxb{1}{1} \gxb{2}{2} \gxh{3}{3} \gxh{4}{4}
  \gyg{1}{1} \gyg{3}{3} \gyg{-1}{-1}
  \node[grad,text=otGreenDark,anchor=east,xshift=-3.5pt] at (axis cs:0,5) {$5$};
  \node[noteV,anchor=west] at (axis cs:0.15,5.35) {maximum $5$ en $x=0$};
  \node[noteO,anchor=north east] at (axis cs:2.9,-1.2) {minimum $-1$ en $x=3$};
  \node[text=otNavy,anchor=south west] at (axis cs:1.6,2.1) {$y=-2x+5$};
""")
