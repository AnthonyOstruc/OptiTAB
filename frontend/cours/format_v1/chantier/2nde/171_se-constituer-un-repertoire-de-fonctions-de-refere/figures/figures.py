# -*- coding: utf-8 -*-
"""Figures de la notion « Se constituer un répertoire de fonctions de référence » (Seconde).

Compilées par outils/figures_livre.py (style des livres : quadrillage pâle,
axes gris, courbes bleu marine, éléments de réponse en vert foncé, droites
y = k en orange). Les graduations sont posées à la main (\\gxb, \\gxh, \\gyg,
\\gyd) du côté où la courbe ne passe pas : jamais de texte sur un trait.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  sym/.style={otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt},
  droiteK/.style={otOrange,line width=1.1pt},
  rep/.style={otGreenDark,line width=1.8pt},
  tit/.style={font=\normalsize,text=otNavy},
}
% graduations : x en dessous / au-dessus de l'axe, y à gauche / à droite de l'axe
\newcommand{\gxb}[2]{\node[grad,anchor=north] at ([yshift=-3.5pt]axis cs:#1,0) {$#2$};}
\newcommand{\gxh}[2]{\node[grad,anchor=south] at ([yshift=3.5pt]axis cs:#1,0) {$#2$};}
\newcommand{\gyg}[2]{\node[grad,anchor=east] at ([xshift=-3.5pt]axis cs:0,#1) {$#2$};}
\newcommand{\gyd}[2]{\node[grad,anchor=west] at ([xshift=3.5pt]axis cs:0,#1) {$#2$};}
\newcommand{\gO}{\node[grad,anchor=north east] at ([xshift=-2.5pt,yshift=-2.5pt]axis cs:0,0) {$0$};}
"""

AX = r"otWeb, xticklabels={}, yticklabels={}"

FIGURES = {
# ---------------------------------------------------------------- cours
"cours_carre": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.6cm, height=5.6cm, xmin=-3.5, xmax=3.6, ymin=-0.7, ymax=10.2,
  xtick={-3,-2,-1,1,2,3}, ytick={1,2,3,4,5,6,7,8,9}]
  \addplot[courbe, domain=-3.2:3.2] {x^2};
  \draw[sym] (axis cs:-1,1) -- (axis cs:1,1);
  \draw[sym] (axis cs:-3,9) -- (axis cs:3,9);
  \pnt{-3}{9} \pnt{3}{9} \pnt{-1}{1} \pnt{1}{1} \pnt{-2}{4} \pnt{2}{4}
  \pnt[otGreenDark]{0}{0}
  \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3}
  \gyg{2}{2} \gyg{4}{4} \gyg{6}{6} \gyg{8}{8} \gO
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.55,5.3) {$y=x^2$};\end{axis}
\end{tikzpicture}""",

"cours_carre_equation": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.6cm, height=5cm, xmin=-3.3, xmax=3.4, ymin=-0.6, ymax=6.6,
  xtick={-3,-2,-1,1,2,3}, ytick={1,2,3,4,5,6}]
  \addplot[courbe, domain=-2.55:2.55] {x^2};
  \draw[droiteK] (axis cs:-3.3,4) -- (axis cs:3.3,4);
  \guidev{-2}{4} \guidev{2}{4}
  \sol{-2}{2} \borneF{-2} \borneF{2}
  \pnt[otGreenDark]{-2}{4} \pnt[otGreenDark]{2}{4}
  \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3}
  \gyg{1}{1} \gyg{2}{2} \gyg{3}{3} \gyg{5}{5} \gyg{6}{6}
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:3.3,4.1) {$y=4$};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:-2.6,5.9) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

"cours_inverse": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=6.4cm, xmin=-4.4, xmax=4.4, ymin=-4.4, ymax=4.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-4,-3,-2,-1,1,2,3,4}]
  \addplot[courbe, domain=0.235:4.4] {1/x};
  \addplot[courbe, domain=-4.4:-0.235] {1/x};
  \draw[sym] (axis cs:-2,-0.5) -- (axis cs:2,0.5);
  \pnt{0.5}{2} \pnt{1}{1} \pnt{2}{0.5} \pnt{-0.5}{-2} \pnt{-1}{-1} \pnt{-2}{-0.5}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-1}{-1} \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \gyg{1}{1} \gyg{2}{2} \gyg{3}{3} \gyg{4}{4}
  \gyd{-1}{-1} \gyd{-2}{-2} \gyd{-3}{-3} \gyd{-4}{-4}
  \node[etiq,text=otNavy] at (axis cs:2.6,2.4) {$y=\dfrac{1}{x}$};
  % le centre de symétrie est marqué et nommé sur la figure
  \pnt[otOrange!90!black]{0}{0}
  \node[text=otInk,anchor=north west,inner sep=1pt] at (axis cs:0.1,-0.1) {$O$};
  \node[note,anchor=north west] at (axis cs:0.9,-0.95) {centre de symétrie $O$};
\end{axis}
\end{tikzpicture}""",

"cours_racine": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=7.8cm, height=3.6cm, xmin=-0.5, xmax=9.8, ymin=-0.5, ymax=3.6,
  xtick={1,2,3,4,5,6,7,8,9}, ytick={1,2,3}]
  \addplot[courbe, domain=0:9.8, samples=300] {sqrt(x)};
  \guides{1}{1} \guides{4}{2} \guides{9}{3}
  \pnt[otGreenDark]{0}{0} \pnt{1}{1} \pnt{4}{2} \pnt{9}{3}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4} \gxb{5}{5} \gxb{6}{6} \gxb{7}{7} \gxb{8}{8} \gxb{9}{9}
  \gyg{1}{1} \gyg{2}{2} \gyg{3}{3} \gO
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:6.2,2.15) {$y=\sqrt{x}$};
\end{axis}
\end{tikzpicture}""",

"cours_cube": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=5.6cm, height=6.4cm, xmin=-2.4, xmax=2.5, ymin=-9.4, ymax=9.4,
  xtick={-2,-1,1,2}, ytick={-8,-6,-4,-2,2,4,6,8}]
  \addplot[courbe, domain=-2.1:2.1] {x^3};
  \draw[sym] (axis cs:-1,-1) -- (axis cs:1,1);
  \pnt{-2}{-8} \pnt{-1}{-1} \pnt{1}{1} \pnt{2}{8}
  \gxb{1}{1} \gxb{2}{2} \gxh{-1}{-1} \gxh{-2}{-2}
  \gyg{2}{2} \gyg{4}{4} \gyg{6}{6} \gyg{8}{8}
  \gyd{-2}{-2} \gyd{-4}{-4} \gyd{-6}{-6} \gyd{-8}{-8}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.75,6.3) {$y=x^3$};
\end{axis}
\end{tikzpicture}""",

"cours_positions": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.4cm, height=6cm, xmin=-0.12, xmax=1.75, ymin=-0.15, ymax=2.75,
  xtick={0.5,1,1.5}, ytick={0.5,1,1.5,2,2.5}]
  \draw[guide] (axis cs:1,0) -- (axis cs:1,2.42);  % s'arrête sous l'étiquette de y = x^3
  \addplot[courbe, domain=0:1.7] {x};
  \addplot[courbe2, domain=0:1.62] {x^2};
  \addplot[otOrange,line width=1.35pt, domain=0:1.39] {x^3};
  \pnt[otGreenDark]{1}{1} \pnt[otGreenDark]{0}{0}
  \gxb{0.5}{0{,}5} \gxb{1}{1} \gxb{1.5}{1{,}5}
  \gyg{0.5}{0{,}5} \gyg{1}{1} \gyg{1.5}{1{,}5} \gyg{2}{2} \gyg{2.5}{2{,}5}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.72,1.7) {$y=x$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.64,2.62) {$y=x^2$};
  \node[etiq,text=otOrange!85!black,anchor=east] at (axis cs:1.3,2.62) {$y=x^3$};  % fond blanc hors de la courbe
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- fiche
"fiche_repertoire": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", name=A, width=3.3cm, height=2.6cm, xmin=-2.2, xmax=2.3, ymin=-0.7, ymax=4.6,
  xtick={-2,-1,1,2}, ytick={1,2,3,4}, xlabel={}, ylabel={}]
  \addplot[courbe, domain=-2.05:2.05] {x^2};
  \pnt{1}{1} \gxb{1}{1} \gyd{1}{1}
\end{axis}
\node[tit,anchor=south] at ([yshift=4pt]A.north) {$x\mapsto x^2$ \ (parabole)};
\begin{axis}[""" + AX + r""", name=B, at={(A.east)}, anchor=west, xshift=1.3cm, width=3.3cm, height=2.6cm,
  xmin=-2.6, xmax=2.7, ymin=-2.8, ymax=2.9, xtick={-2,-1,1,2}, ytick={-2,-1,1,2}, xlabel={}, ylabel={}]
  \addplot[courbe, domain=0.36:2.6] {1/x};
  \addplot[courbe, domain=-2.6:-0.36] {1/x};
  \pnt{1}{1} \gxb{1}{1} \gyg{1}{1}
\end{axis}
\node[tit,anchor=south] at ([yshift=4pt]B.north) {$x\mapsto \dfrac{1}{x}$ \ (hyperbole)};
\begin{axis}[""" + AX + r""", name=C, at={(A.south)}, anchor=north, yshift=-1.75cm, width=3.3cm, height=2.6cm,
  xmin=-0.6, xmax=5.3, ymin=-0.5, ymax=2.5, xtick={1,2,3,4,5}, ytick={1,2}, xlabel={}, ylabel={}]
  \addplot[courbe, domain=0:5.2, samples=300] {sqrt(x)};
  \pnt{1}{1} \gxb{1}{1} \gyg{1}{1}
\end{axis}
\node[tit,anchor=south] at ([yshift=4pt]C.north) {$x\mapsto \sqrt{x}$};
\begin{axis}[""" + AX + r""", name=D, at={(B.south)}, anchor=north, yshift=-1.75cm, width=3.3cm, height=2.6cm,
  xmin=-1.8, xmax=1.9, ymin=-4.2, ymax=4.3, xtick={-1,1}, ytick={-4,-2,2,4}, xlabel={}, ylabel={}]
  \addplot[courbe, domain=-1.6:1.6] {x^3};
  \pnt{1}{1} \gxb{1}{1} \gyg{2}{2}
\end{axis}
\node[tit,anchor=south] at ([yshift=4pt]D.north) {$x\mapsto x^3$};
\end{tikzpicture}""",

# ---------------------------------------------------------------- exercices
"ex_carre_9": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.6cm, height=5cm, xmin=-4.3, xmax=4.4, ymin=-1, ymax=12.6,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={2,4,6,8,10,12}]
  \addplot[courbe, domain=-3.5:3.5] {x^2};
  \draw[droiteK] (axis cs:-4.3,9) -- (axis cs:4.3,9);
  \guidev{-3}{9} \guidev{3}{9}
  \sol{-3}{3} \borneO{-3} \borneO{3}
  \pnt[otGreenDark]{-3}{9} \pnt[otGreenDark]{3}{9}
  \gxb{-4}{-4} \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gyg{2}{2} \gyg{4}{4} \gyg{6}{6} \gyg{12}{12}
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:4.3,8.8) {$y=9$};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:-3.55,11.6) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

"ex_racine_droite": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=7.4cm, height=5cm, xmin=-0.6, xmax=6.6, ymin=-2.6, ymax=3.3,
  xtick={1,2,3,4,5,6}, ytick={-2,-1,1,2,3}]
  \addplot[courbe, domain=0:6.5, samples=300] {sqrt(x)};
  \addplot[courbe2, domain=-0.5:5.2] {x-2};
  \draw[guide] (axis cs:1,-1) -- (axis cs:1,1);
  \guides{4}{2}
  \pntv[otOrange]{1}{1} \pntv[otOrange]{1}{-1}
  \pnt[otGreenDark]{4}{2}
  \gxb{1}{1} \gxb{3}{3} \gxb{4}{4} \gxb{5}{5} \gxb{6}{6}
  \gyg{-1}{-1} \gyg{1}{1} \gyg{2}{2} \gyg{3}{3}
  \node[etiq,text=otNavy,anchor=north] at (axis cs:5.7,2.12) {$y=\sqrt{x}$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:5.3,3.2) {$y=x-2$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:3.9,2.1) {$(4\,;2)$};
\end{axis}
\end{tikzpicture}""",

"ex_inverse_enonce": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.6cm, xmin=-4.4, xmax=4.4, ymin=-3.4, ymax=3.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe, domain=0.3:4.4] {1/x};
  \addplot[courbe, domain=-4.4:-0.3] {1/x};
  \draw[droiteK] (axis cs:-4.4,2) -- (axis cs:4.4,2);
  \draw[droiteK] (axis cs:-4.4,-1) -- (axis cs:4.4,-1);
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-1}{-1} \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \gyg{1}{1} \gyg{3}{3} \gyd{-2}{-2} \gyd{-3}{-3}
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:4.4,2.1) {$y=2$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:-4.4,-1.1) {$y=-1$};
  \node[etiq,text=otNavy] at (axis cs:2.9,1.1) {$\mathcal{C}$};
\end{axis}
\end{tikzpicture}""",

"ex_inverse_sup2": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.6cm, xmin=-4.4, xmax=4.4, ymin=-3.4, ymax=3.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe, domain=0.3:4.4] {1/x};
  \addplot[courbe, domain=-4.4:-0.3] {1/x};
  \draw[droiteK] (axis cs:-4.4,2) -- (axis cs:4.4,2);
  \addplot[rep, domain=0.295:0.5] {1/x};
  \guidev{0.5}{2}
  \sol{0}{0.5} \borneO{0} \borneO{0.5}
  \pnt[otGreenDark]{0.5}{2}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-1}{-1} \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \gyg{1}{1} \gyg{3}{3} \gyd{-1}{-1} \gyd{-2}{-2} \gyd{-3}{-3}
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:0.5,0) {$0{,}5$};
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:4.4,2.1) {$y=2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:0.75,2.75) {$\dfrac{1}{x}>2$};
\end{axis}
\end{tikzpicture}""",

"ex_inverse_supm1": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.6cm, xmin=-4.4, xmax=4.4, ymin=-3.4, ymax=3.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe, domain=-1:-0.3] {1/x};
  \addplot[rep, domain=0.3:4.4] {1/x};
  \addplot[rep, domain=-4.4:-1] {1/x};
  \draw[droiteK] (axis cs:-4.4,-1) -- (axis cs:4.4,-1);
  \guidev{-1}{-1}
  \sol{-4.4}{-1} \sol{0}{4.4} \borneF{-1} \borneO{0}
  \pnt[otGreenDark]{-1}{-1}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \node[grad,text=otGreenDark,anchor=south] at ([yshift=3.5pt]axis cs:-1,0) {$-1$};
  \gyg{1}{1} \gyg{2}{2} \gyg{3}{3} \gyd{-2}{-2} \gyd{-3}{-3}
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:4.4,-1.1) {$y=-1$};
\end{axis}
\end{tikzpicture}""",

"ex_encadrement": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.4cm, height=5.4cm, xmin=-3.8, xmax=3.2, ymin=-1, ymax=11,
  xtick={-3,-2,-1,1,2,3}, ytick={1,2,3,4,5,6,7,8,9,10}]
  \addplot[courbe, domain=-3.3:3.1] {x^2};
  \addplot[rep, domain=-3:2] {x^2};
  \draw[guide] (axis cs:-3,0) -- (axis cs:-3,9) -- (axis cs:0,9);
  \draw[guide] (axis cs:2,0) -- (axis cs:2,4) -- (axis cs:0,4);
  \sol{-3}{2} \borneF{-3} \borneF{2}
  \draw[otGreen,line width=3pt,opacity=0.9] (axis cs:0,0) -- (axis cs:0,9);
  \pnt[otGreenDark]{-3}{9} \pnt[otGreenDark]{2}{4} \pnt[otGreenDark]{0}{0}
  \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3}
  \gyd{9}{9} \gyg{4}{4} \gyg{2}{2} \gyg{6}{6}
  \node[etiq,text=otNavy] at (axis cs:-1.25,7) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- finition 2026-11-02
# cours I : f(x) = -2x + 3 < 7  <=>  x > -2
"cours_affine": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.4cm, height=5.6cm, xmin=-3.4, xmax=3.4, ymin=-3.6, ymax=10,
  xtick={-3,-2,-1,1,2,3}, ytick={-2,2,4,6,8}]
  \addplot[courbe, domain=-3.2:3.2] {-2*x+3};
  \draw[droiteK] (axis cs:-3.4,7) -- (axis cs:3.4,7);
  \addplot[rep, domain=-2:3.2] {-2*x+3};
  \guidev{-2}{7}
  \sol{-2}{3.4} \borneO{-2}
  \pnt[otGreenDark]{-2}{7}
  \gxb{-3}{-3} \gxb{-1}{-1} \gxb{1}{1} \gxh{2}{2} \gxh{3}{3}
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:-2,0) {$-2$};
  \gyd{4}{4} \gyd{6}{6} \gyd{8}{8} \gyg{2}{2} \gyg{-2}{-2}
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:3.4,7.15) {$y=7$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-2.3,9.3) {$y=-2x+3$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:0.9,3.6) {$f(x)<7$};
\end{axis}
\end{tikzpicture}""",

# cours III : 1/x < 2  <=>  x < 0 ou x > 0,5
"cours_inverse_ineq": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.6cm, xmin=-4.4, xmax=4.4, ymin=-3.4, ymax=3.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe, domain=0.3:0.5] {1/x};
  \addplot[rep, domain=0.5:4.4] {1/x};
  \addplot[rep, domain=-4.4:-0.3] {1/x};
  \draw[droiteK] (axis cs:-4.4,2) -- (axis cs:4.4,2);
  \guidev{0.5}{2}
  \sol{-4.4}{0} \sol{0.5}{4.4} \borneO{0} \borneO{0.5}
  \pnt[otGreenDark]{0.5}{2}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-1}{-1} \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \node[grad,text=otGreenDark,anchor=north west] at ([xshift=1pt,yshift=-3.5pt]axis cs:0.5,0) {$0{,}5$};
  \gyg{1}{1} \gyg{3}{3} \gyd{-1}{-1} \gyd{-2}{-2} \gyd{-3}{-3}
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:4.4,2.1) {$y=2$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.75,2.75) {$y=\dfrac{1}{x}$};
\end{axis}
\end{tikzpicture}""",

# cours VIII et exercice 3745 : balayage de x^2 entre 1,1 et 1,5
"balayage_racine2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7cm, height=5.2cm, xmin=1.02, xmax=1.58, ymin=1.05, ymax=2.45,
  xtick={1.1,1.2,1.3,1.4,1.5}, ytick={1.2,1.4,1.6,1.8,2,2.2,2.4},
  xticklabel style={anchor=north,yshift=-2pt,fill=none}, yticklabel style={anchor=east,xshift=-2pt,yshift=0pt,fill=none},
  xlabel={}, ylabel={}]
  \addplot[courbe, domain=1.05:1.555] {x^2};
  \draw[droiteK] (axis cs:1.02,2) -- (axis cs:1.58,2);
  \draw[guide] (axis cs:1.1,1.05) -- (axis cs:1.1,1.21);
  \draw[guide] (axis cs:1.2,1.05) -- (axis cs:1.2,1.44);
  \draw[guide] (axis cs:1.3,1.05) -- (axis cs:1.3,1.69);
  \draw[guide] (axis cs:1.4,1.05) -- (axis cs:1.4,1.96);
  \draw[guide] (axis cs:1.5,1.05) -- (axis cs:1.5,2.25);
  \draw[otGreen,line width=3.4pt,opacity=0.9] (axis cs:1.4,1.05) -- (axis cs:1.5,1.05);
  \pnt{1.1}{1.21} \pnt{1.2}{1.44} \pnt{1.3}{1.69}
  \pnt[otGreenDark]{1.4}{1.96} \pnt[otGreenDark]{1.5}{2.25}
  \pntv[otOrange!90!black]{1.41421}{2}
  \node[etiq,text=otOrange!85!black,anchor=south east,inner sep=1pt] at (axis cs:1.4,2.03) {$\sqrt{2}$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:1.025,1.98) {$y=2$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.16,1.62) {$y=x^2$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:1.505,1.07) {$1{,}4<\sqrt{2}<1{,}5$};
\end{axis}
\end{tikzpicture}""",

# 2025 Q2 : droite y = 2x + 3 et les images calculées
"ex_affine_f": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6cm, height=6.2cm, xmin=-2.8, xmax=4.6, ymin=-2.4, ymax=12.4,
  xtick={-2,-1,1,2,3,4}, ytick={-1,1,2,3,4,5,6,7,8,9,10,11,12}]
  \addplot[courbe, domain=-2.6:4.4] {2*x+3};
  \guides{3}{9} \guides{4}{11}
  \draw[guide] (axis cs:-2,0) -- (axis cs:-2,-1) -- (axis cs:0,-1);
  \pnt{-2}{-1} \pnt{3}{9} \pnt{4}{11} \pnt[otGreenDark]{0}{3} \pnt[otGreenDark]{-1.5}{0}
  \gxh{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gyd{-1}{-1} \gyg{3}{3} \gyg{6}{6} \gyg{9}{9} \gyg{11}{11}
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:-1.6,0.15) {$-1{,}5$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.6,3.6) {$y=2x+3$};
\end{axis}
\end{tikzpicture}""",

# 2025 Q5 : g(x) = -3x + 1 <= -8  <=>  x >= 3
"ex_affine_g": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6cm, height=6.2cm, xmin=-1.8, xmax=4.8, ymin=-12, ymax=5.6,
  xtick={-1,1,2,3,4}, ytick={-10,-8,-6,-4,-2,2,4}]
  \addplot[courbe, domain=-1.45:3] {-3*x+1};
  \addplot[rep, domain=3:4.3] {-3*x+1};
  \draw[droiteK] (axis cs:-1.8,-8) -- (axis cs:4.8,-8);
  \guidev{3}{-8}
  \sol{3}{4.8} \borneF{3}
  \pnt[otGreenDark]{3}{-8}
  \gxb{-1}{-1} \gxh{1}{1} \gxh{2}{2} \gxh{4}{4}
  \node[grad,text=otGreenDark,anchor=south] at ([yshift=3.5pt]axis cs:3,0) {$3$};
  \gyd{2}{2} \gyd{4}{4} \gyg{-2}{-2} \gyg{-4}{-4} \gyg{-6}{-6} \gyg{-10}{-10}
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:-1.8,-8.25) {$y=-8$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.6,3.6) {$y=-3x+1$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:3.55,-6.6) {$g(x)\leqslant -8$};
\end{axis}
\end{tikzpicture}""",

# 2026 Q2 : symétrie de la parabole, points d'abscisses -5 et 5
"ex_carre_sym": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.6cm, height=5.4cm, xmin=-7, xmax=7, ymin=-3, ymax=29,
  xtick={-5,-4,-3,-2,-1,1,2,3,4,5}, ytick={5,10,15,20,25}]
  \addplot[courbe, domain=-5.15:5.15] {x^2};
  \draw[sym] (axis cs:-5,25) -- (axis cs:5,25);
  \guidev{-5}{25} \guidev{5}{25}
  \pnt[otGreenDark]{-5}{25} \pnt[otGreenDark]{5}{25}
  \gxb{-5}{-5} \gxb{-3}{-3} \gxb{-1}{-1} \gxb{1}{1} \gxb{3}{3} \gxb{5}{5}
  \gyg{5}{5} \gyg{10}{10} \gyg{15}{15} \gyg{20}{20}
  \node[etiq,text=otGreenDark,anchor=north east] at (axis cs:-5.15,24.4) {$(-5\,;25)$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:5.15,24.4) {$(5\,;25)$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:3.2,3.2) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

# 2026 Q5 : f(-4) > f(-1) (décroissante sur ]-inf ; 0])
"ex_carre_compare": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6cm, height=5.4cm, xmin=-5, xmax=2.6, ymin=-2, ymax=19,
  xtick={-4,-3,-2,-1,1,2}, ytick={2,4,6,8,10,12,14,16,18}]
  \addplot[courbe, domain=-4.3:2.3] {x^2};
  \guides{-4}{16} \guides{-1}{1}
  \pnt[otGreenDark]{-4}{16} \pnt[otGreenDark]{-1}{1}
  \gxb{-4}{-4} \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2}
  \node[grad,text=otGreenDark,anchor=west] at ([xshift=3.5pt]axis cs:0,16) {$16$};
  \node[grad,text=otGreenDark,anchor=west] at ([xshift=3.5pt]axis cs:0,1.35) {$1$};
  \gyd{4}{4} \gyd{8}{8} \gyd{12}{12}
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:-3.85,16.3) {$f(-4)$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-1.6,0.95) {$f(-1)$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.2,7) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

# 2029 Q5 : x^3 >= 8  <=>  x >= 2
"ex_cube_8": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=5.6cm, height=6.2cm, xmin=-2.5, xmax=2.9, ymin=-10.5, ymax=14.5,
  xtick={-2,-1,1,2}, ytick={-8,-4,4,8,12}]
  \addplot[courbe, domain=-2.15:2] {x^3};
  \addplot[rep, domain=2:2.4] {x^3};
  \draw[droiteK] (axis cs:-2.5,8) -- (axis cs:2.9,8);
  \guidev{2}{8}
  \sol{2}{2.9} \borneF{2}
  \pnt[otGreenDark]{2}{8}
  \gxb{1}{1} \gxh{-1}{-1} \gxh{-2}{-2}
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:2,0) {$2$};
  \gyg{4}{4} \gyg{12}{12} \gyd{-4}{-4} \gyd{-8}{-8}
  \node[etiq,text=otOrange!85!black,anchor=south west] at (axis cs:-2.5,8.2) {$y=8$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.55,-6) {$y=x^3$};
\end{axis}
\end{tikzpicture}""",

# 2027 Q5 : points (3 ; 1/3) et (-3 ; -1/3) symétriques par rapport à O
"ex_inverse_sym3": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.4cm, xmin=-4.4, xmax=4.4, ymin=-3.4, ymax=3.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe, domain=0.3:4.4] {1/x};
  \addplot[courbe, domain=-4.4:-0.3] {1/x};
  \draw[sym] (axis cs:-3,-1/3) -- (axis cs:3,1/3);
  \pnt[otGreenDark]{3}{1/3} \pnt[otGreenDark]{-3}{-1/3}
  \pnt[otOrange!90!black]{0}{0}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4}
  \gxh{-1}{-1} \gxh{-2}{-2} \gxh{-3}{-3} \gxh{-4}{-4}
  \gyg{1}{1} \gyg{2}{2} \gyg{3}{3} \gyd{-1}{-1} \gyd{-2}{-2} \gyd{-3}{-3}
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:3,0.75) {$\left(3\,;\frac{1}{3}\right)$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:-3,-0.75) {$\left(-3\,;-\frac{1}{3}\right)$};
  \node[text=otInk,anchor=north west,inner sep=1pt] at (axis cs:0.12,-0.45) {$O$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.75,2.6) {$y=\dfrac{1}{x}$};
\end{axis}
\end{tikzpicture}""",

# 2028 Q5 : sqrt(x) < 3  <=>  0 <= x < 9
"ex_racine_3": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=7.8cm, height=3.8cm, xmin=-0.6, xmax=12.6, ymin=-0.7, ymax=4.1,
  xtick={1,2,3,4,5,6,7,8,9,10,11,12}, ytick={1,2,3,4}]
  \addplot[rep, domain=0:9, samples=300] {sqrt(x)};
  \addplot[courbe, domain=9:12.6] {sqrt(x)};
  \draw[droiteK] (axis cs:-0.6,3) -- (axis cs:12.6,3);
  \guidev{9}{3}
  \sol{0}{9} \borneF{0} \borneO{9}
  \pntv[otGreenDark]{9}{3}
  \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{4}{4} \gxb{5}{5} \gxb{6}{6} \gxb{7}{7} \gxb{8}{8}
  \gxb{10}{10} \gxb{11}{11} \gxb{12}{12}
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:9,0) {$9$};
  \gyg{1}{1} \gyg{2}{2} \gyg{4}{4}
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:12.6,2.88) {$y=3$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:2.6,1.45) {$y=\sqrt{x}$};
\end{axis}
\end{tikzpicture}""",

# 2030 Q6 : 1/(-2) < 0 < 1/3
"ex_inverse_compare": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.8cm, height=5.4cm, xmin=-4.4, xmax=4.4, ymin=-2.6, ymax=2.6,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={-2,-1,1,2}]
  \addplot[courbe, domain=0.385:4.4] {1/x};
  \addplot[courbe, domain=-4.4:-0.385] {1/x};
  \guides{-2}{-0.5} \guides{3}{1/3}
  \pnt[otGreenDark]{-2}{-0.5} \pnt[otGreenDark]{3}{1/3}
  \gxb{1}{1} \gxb{2}{2} \gxb{4}{4} \gxh{-1}{-1} \gxh{-3}{-3} \gxh{-4}{-4}
  \node[grad,text=otGreenDark,anchor=south] at ([yshift=3.5pt]axis cs:-2,0) {$-2$};
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:3,0) {$3$};
  \gyg{1}{1} \gyg{2}{2} \gyd{-1}{-1} \gyd{-2}{-2}
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:-2.3,-0.85) {$\dfrac{1}{-2}=-0{,}5$};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:3,0.7) {$\dfrac{1}{3}\approx 0{,}33$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.75,2.1) {$y=\dfrac{1}{x}$};
\end{axis}
\end{tikzpicture}""",

# 2031 Q2 et Q6 : x^2 = 16 (deux solutions) et x^2 = -4 (aucune)
"ex_carre_16": r"""
\begin{tikzpicture}
\begin{axis}[""" + AX + r""", width=6.6cm, height=5.8cm, xmin=-6.6, xmax=6.6, ymin=-7, ymax=21,
  xtick={-5,-4,-3,-2,-1,1,2,3,4,5}, ytick={-4,4,8,12,16,20}]
  \addplot[courbe, domain=-4.55:4.55] {x^2};
  \draw[droiteK] (axis cs:-6.6,16) -- (axis cs:6.6,16);
  \draw[droiteK] (axis cs:-6.6,-4) -- (axis cs:6.6,-4);
  \guidev{-4}{16} \guidev{4}{16}
  \pnt[otGreenDark]{-4}{16} \pnt[otGreenDark]{4}{16}
  \gxb{-5}{-5} \gxb{-3}{-3} \gxb{-2}{-2} \gxb{-1}{-1} \gxb{1}{1} \gxb{2}{2} \gxb{3}{3} \gxb{5}{5}
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:-4,0) {$-4$};
  \node[grad,text=otGreenDark,anchor=north] at ([yshift=-3.5pt]axis cs:4,0) {$4$};
  \gyd{4}{4} \gyd{8}{8} \gyd{12}{12} \gyd{20}{20}
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:6.6,15.4) {$y=16$};
  \node[etiq,text=otOrange!85!black,anchor=north east] at (axis cs:6.6,-4.5) {$y=-4$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-2.6,9) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",
}
