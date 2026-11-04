# -*- coding: utf-8 -*-
"""Figures de la notion « Fonction exponentielle » (Terminale), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion> [nom …] [--planche]
"""

FIGURES = {
# =============================================================== cours
"cours_exp_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5.6cm, xmin=-3.4, xmax=2.4, ymin=-1.5, ymax=5.6,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={2,3,4,5}]
  \addplot[otGreenDark, line width=1pt, domain=-2.45:2.2] {x+1};
  \addplot[courbe, domain=-3.4:1.68] {exp(x)};
  \guides{1}{2.71828}
  \pnt{0}{1} \pnt{1}{2.71828}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.06,2.71828) {$e$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-0.12,1.12) {$(0\,;1)$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.72,4.3) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.25,1.65) {$y=x+1$};
\end{axis}
\end{tikzpicture}""",

"cours_etude_xexp": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-0.7, xmax=6.6, ymin=-0.95, ymax=0.74,
  xtick={1,2,3,4,5,6}, ytick={0.5}]
  \addplot[courbe, domain=-0.52:6.4] {x*exp(-x)};
  \guides{1}{0.36788} \guidev{2}{0.27067}
  \pnt{1}{0.36788} \pnt[otGreenDark]{2}{0.27067}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1,0.39) {$M$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:2.06,0.29) {$I$};
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,0.36788) {$\frac{1}{e}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.5,0.3) {$y=xe^{-x}$};
\end{axis}
\end{tikzpicture}""",

"cours_condensateur": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-0.6, xmax=13, ymin=-0.7, ymax=6.3,
  xtick={2,4,6,8,10,12}, ytick={1,2,3,5}, xlabel={$t$}, ylabel={$u$}]
  \draw[asymptote] (axis cs:0,5) -- (axis cs:12.7,5);
  \addplot[courbe, domain=0:12.6] {5*(1-exp(-0.5*x))};
  \guides{4}{4.3233}
  \pnt{4}{4.3233}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.08,4.3233) {$4{,}32$};
  \node[note,anchor=south east] at (axis cs:12.7,5.12) {asymptote $y=5$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.6,3.2) {$u(t)=5\left(1-e^{-0{,}5t}\right)$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1212 équations et inéquations
"eq_ex_egal5": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.4cm, xmin=-2.4, xmax=2.5, ymin=-0.7, ymax=7.4,
  xtick={-2,-1,1,1.6094,2}, xticklabels={}, ytick={2,4,6}]
  \draw[seuil] (axis cs:-2.4,5) -- (axis cs:2.45,5);
  \addplot[courbe, domain=-2.4:2.0] {exp(x)};
  \guidev{1.6094}{5}
  \pnt[otGreenDark]{1.6094}{5}
  \node[etiq,text=otOrange!80!black,anchor=north east] at (axis cs:2.45,4.85) {$y=5$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:0.95,3.0) {$y=e^x$};
\end{axis}
\end{tikzpicture}""",

"eq_quad_ln3": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-3.3, xmax=1.7, ymin=-1.5, ymax=4.3,
  xtick={-3,-2,-1,0,1.0986}, xticklabels={}, ytick={-1,1,2,3}]
  \draw[asymptote] (axis cs:-3.3,3) -- (axis cs:-0.4,3);
  \addplot[courbe, domain=-3.3:1.44] {exp(2*x)-4*exp(x)+3};
  \pnt[otGreenDark]{0}{0} \pnt[otGreenDark]{1.0986}{0}
  \node[note,anchor=south west] at (axis cs:-3.25,3.08) {asymptote $y=3$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:-3.2,1.55) {$y=e^{2x}-4e^x+3$};
\end{axis}
\end{tikzpicture}""",

"ineq_ex_7": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.4cm, xmin=-2.4, xmax=2.7, ymin=-0.8, ymax=9.2,
  xtick={-2,-1,1,1.9459}, xticklabels={}, ytick={2,4,6,8}]
  \draw[seuil] (axis cs:-2.4,7) -- (axis cs:2.65,7);
  \addplot[courbe, domain=-2.4:2.2] {exp(x)};
  \guidev{1.9459}{7}
  \sol{1.9459}{2.65} \borneF{1.9459}
  \pnt[otGreenDark]{1.9459}{7}
  \node[etiq,text=otOrange!80!black,anchor=north east] at (axis cs:2.65,6.85) {$y=7$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:0.95,3.0) {$y=e^x$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1217 croissances comparées
"cc_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.4cm, xmin=-2.8, xmax=2.4, ymin=-0.6, ymax=5.6,
  xtick={-2,-1,1,2}, ytick={2,3,4,5}]
  \addplot[courbe, domain=-2.7:1.95] {exp(x)-x};
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=north west] at (axis cs:0.1,0.88) {minimum $1$ en $0$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-2.7,3.05) {$y=e^x-x$};
\end{axis}
\end{tikzpicture}""",

"cc_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-0.4, xmax=3.6, ymin=-0.8, ymax=9.4,
  xtick={1,2,3}, ytick={4,6,8}]
  \addplot[courbe, domain=0.125:3.32] {exp(x)/x};
  \guides{1}{2.71828}
  \pnt[otGreenDark]{1}{2.71828}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,2.71828) {$e$};
  \node[etiq,text=otNavy] at (axis cs:1.55,6.3) {$y=\dfrac{e^x}{x}$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1213 x e^x
"xex_min": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-5.4, xmax=1.4, ymin=-0.85, ymax=2.7,
  xtick={-5,-4,-3,-2,-1,1}, xticklabels={}, ytick={1,2}]
  \addplot[courbe, domain=-5.3:0.96] {x*exp(x)};
  \guides{-1}{-0.36788}
  \pnt[otGreenDark]{-1}{-0.36788}
  \node[etiq,anchor=west,text=otMuted] at (axis cs:0.05,-0.36788) {$-\frac{1}{e}$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.98,1.5) {$y=xe^x$};
\end{axis}
\end{tikzpicture}""",

"xex_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-2.7, xmax=1.5, ymin=-1.3, ymax=2.7,
  xtick={-2,-1,1}, xticklabels={}, ytick={1,2}]
  \addplot[otGreenDark, line width=1.1pt, domain=-1.25:1.3] {x};
  \addplot[courbe, domain=-2.7:0.96] {x*exp(x)};
  \pnt[otGreenDark]{0}{0}
  \node[etiq,text=otMuted,anchor=south east] at (axis cs:-0.06,0.06) {$O$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.36,1.3) {$T : y=x$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.05,2.6) {$y=xe^x$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1216 équations et inéquations avancées
"av_zeros": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.2cm, xmin=-0.65, xmax=1.65, ymin=-0.75, ymax=4,
  xtick={0.6931,1.0986}, xticklabels={}, ytick={1,3}]
  \addplot[courbe, domain=-0.6:1.5] {exp(2*x)-5*exp(x)+6};
  \pnt[otGreenDark]{0.6931}{0} \pnt[otGreenDark]{1.0986}{0}
  \node[etiq,text=otNavy,anchor=north] at (axis cs:0.72,3.1) {$y=e^{2x}-5e^x+6$};
\end{axis}
\end{tikzpicture}""",

"av_ineq": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4cm, xmin=-1.7, xmax=1.3, ymin=-0.65, ymax=2.7,
  xtick={0,0.6931}, xticklabels={}, ytick={1,2}]
  \addplot[draw=none, domain=-1.7:1.15, name path=c] {exp(2*x)-3*exp(x)+2};
  \path[name path=a] (axis cs:-1.7,0) -- (axis cs:1.3,0);
  \addplot[otGreen!30] fill between[of=c and a, soft clip={domain=0:0.6931}];
  \addplot[courbe, domain=-1.7:1.15] {exp(2*x)-3*exp(x)+2};
  \sol{0}{0.6931} \borneF{0} \borneF{0.6931}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-1.65,1.75) {$y=e^{2x}-3e^x+2$};
\end{axis}
\end{tikzpicture}""",

"av_e2_sup": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.2cm, xmin=-3.1, xmax=2.4, ymin=-0.6, ymax=6.8,
  xtick={-3,-2,-1,1,2}, ytick={4,6}]
  \addplot[courbe2, domain=-3.1:2.15] {2*exp(x-1)};
  \addplot[courbe, domain=-3.1:0.85] {exp(x+1)};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-0.15,2.5) {$y=e^{x+1}$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.15,2.0) {$y=2e^{x-1}$};
\end{axis}
\end{tikzpicture}""",

"av_ineq_trinome": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.2cm, xmin=-0.6, xmax=4.4, ymin=-0.6, ymax=4.5,
  xtick={1,2,3,4}, ytick={2,3,4}]
  \draw[seuil] (axis cs:-0.6,1) -- (axis cs:4.3,1);
  \addplot[courbe, domain=0.44:3.56] {exp(x^2-4*x+3)};
  \guidev{1}{1} \guidev{3}{1}
  \sol{-0.6}{1} \sol{3}{4.35} \borneF{1} \borneF{3}
  \pnt[otGreenDark]{1}{1} \pnt[otGreenDark]{3}{1}
  \node[etiq,text=otOrange!80!black,anchor=north east] at (axis cs:4.3,0.92) {$y=1$};
  \node[etiq,text=otNavy] at (axis cs:2,2.7) {$y=e^{x^2-4x+3}$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1218 logarithme
"log_eq_domaine": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.4cm, xmin=-0.4, xmax=4.5, ymin=-2.7, ymax=3.1,
  xtick={1,2,3,4}, xticklabels={}, ytick={-2,-1,1,2}]
  \draw[asymptote] (axis cs:1,-2.7) -- (axis cs:1,3.0);
  \addplot[pale, domain=0:1] {ln(x+1)};
  \addplot[courbe, domain=1:4.35] {ln(x+1)};
  \addplot[courbe2, domain=1.034:4.35] {ln(x^2-1)};
  \guidev{2}{1.0986}
  \pnt[otGreenDark]{2}{1.0986}
  \node[note,anchor=north east] at (axis cs:0.9,-2.0) {$x=1$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:2.75,2.05) {$y=\ln\left(x^2-1\right)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.8,1.0) {$y=\ln(x+1)$};
\end{axis}
\end{tikzpicture}""",

"log_ineq": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.4cm, xmin=-0.4, xmax=3.9, ymin=-2.7, ymax=3.8,
  xtick={1.3133,2,3}, xticklabels={}, ytick={-2,-1,2,3}]
  \draw[seuil] (axis cs:-0.4,1) -- (axis cs:3.8,1);
  \addplot[courbe, domain=0.075:3.62] {ln(exp(x)-1)};
  \guidev{1.3133}{1}
  \sol{1.3133}{3.85} \borneF{1.3133}
  \pnt[otGreenDark]{1.3133}{1}
  \node[etiq,text=otOrange!80!black,anchor=north east] at (axis cs:3.8,0.92) {$y=1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.72,2.0) {$y=\ln\left(e^x-1\right)$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1211 étude complète
"etude_complete": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-4.3, xmax=1.5, ymin=-0.75, ymax=3.3,
  xtick={-4,-3,-2,-1,0.4055}, xticklabels={}, ytick={1,2,3}]
  \draw[asymptote] (axis cs:-4.3,2) -- (axis cs:-0.35,2);
  \addplot[courbe, domain=-4.3:1.2] {exp(2*x)-3*exp(x)+2};
  \guidev{0.4055}{-0.25}
  \pnt[otGreenDark]{0.4055}{-0.25}
  \node[note,anchor=west] at (axis cs:0.52,-0.5) {minimum $-0{,}25$};
  \node[note,anchor=south west] at (axis cs:-4.25,2.06) {asymptote $y=2$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:-4.2,1.62) {$y=f(x)$};
\end{axis}
\end{tikzpicture}""",

"etude_signe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4cm, xmin=-1.7, xmax=1.3, ymin=-0.65, ymax=2.7,
  xtick={0,0.6931}, xticklabels={}, ytick={1,2}]
  \addplot[courbe, domain=-1.7:1.15] {exp(2*x)-3*exp(x)+2};
  \sol{-1.7}{0} \sol{0.6931}{1.28} \borneF{0} \borneF{0.6931}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-1.65,1.75) {$y=e^{2x}-3e^x+2$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1220 courbe en cloche
"cloche_inflexion": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.4cm, xmin=-3.2, xmax=3.4, ymin=-0.25, ymax=1.35,
  xtick={-2,-0.70711,0.70711,2}, xticklabels={}, ytick=\empty]
  \addplot[otOrange, line width=0.9pt, domain=0.2:1.25] {0.60653-0.85776*(x-0.70711)};
  \addplot[otOrange, line width=0.9pt, domain=-1.25:-0.2] {0.60653+0.85776*(x+0.70711)};
  \addplot[courbe, domain=-3.2:3.2] {exp(-x^2)};
  \guidev{-0.70711}{0.60653} \guidev{0.70711}{0.60653}
  \pnt[otGreenDark]{-0.70711}{0.60653} \pnt[otGreenDark]{0.70711}{0.60653}
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:-0.8,0.66) {$I$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:0.8,0.66) {$J$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:1.45,0.38) {$y=e^{-x^2}$};
\end{axis}
\end{tikzpicture}""",

"cloche_convexite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.4cm, xmin=-3.2, xmax=3.4, ymin=-0.25, ymax=1.35,
  xtick={-2,-0.70711,0.70711,2}, xticklabels={}, ytick=\empty]
  \addplot[courbe, domain=-3.2:-0.70711] {exp(-x^2)};
  \addplot[courbe, domain=0.70711:3.2] {exp(-x^2)};
  \addplot[otOrange, line width=1.35pt, domain=-0.70711:0.70711] {exp(-x^2)};
  \guidev{-0.70711}{0.60653} \guidev{0.70711}{0.60653}
  \pnt[otGreenDark]{-0.70711}{0.60653} \pnt[otGreenDark]{0.70711}{0.60653}
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:-0.8,0.66) {$I$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:0.8,0.66) {$J$};
  \node[note,text=otNavy,anchor=south] at (axis cs:-2.1,0.32) {convexe};
  \node[note,text=otNavy,anchor=south] at (axis cs:2.1,0.32) {convexe};
  \node[note,text=otOrange!80!black,anchor=south west] at (axis cs:0.12,1.04) {concave};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1214 composée
"compo_min": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.4cm, xmin=-1.2, xmax=3.2, ymin=-0.45, ymax=4.6,
  xtick={-1,1,2,3}, ytick={2,3,4}]
  \draw[guide] (axis cs:1,0) -- (axis cs:1,4.15);
  \draw[guide] (axis cs:1,0.36788) -- (axis cs:0,0.36788);
  \addplot[courbe, domain=-0.56:2.56] {exp(x^2-2*x)};
  \pnt[otGreenDark]{1}{0.36788}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,0.36788) {$\frac{1}{e}$};
  \node[note,anchor=south] at (axis cs:1,4.2) {axe $x=1$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.62,3.0) {$y=e^{x^2-2x}$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1219 bactéries
"bacteries": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-6, xmax=134, ymin=-900, ymax=12600,
  xtick={34.657,50,100,115.13}, xticklabels={}, ytick={2000,4000,6000,8000,10000},
  scaled y ticks=false, xlabel={$t$}, ylabel={$N$}]
  \addplot[courbe, domain=0:124] {1000*exp(0.02*x)};
  \guides{34.657}{2000} \guides{115.13}{10000}
  \pnt{0}{1000}
  \pnt[otGreenDark]{34.657}{2000} \pnt[otGreenDark]{115.13}{10000}
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:72,6000) {$N(t)=1\,000\,e^{0{,}02t}$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== 1215 optimisation
"optim_max": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-0.5, xmax=10.6, ymin=-0.1, ymax=0.75,
  xtick={2,4,6,8,10}, ytick={0.2}, yticklabels={$0{,}2$}]
  \addplot[courbe, domain=0:10.3] {x^2*exp(-x)};
  \guides{2}{0.54134}
  \pnt[otGreenDark]{2}{0.54134}
  \node[etiq,anchor=east,text=otGreenDark] at (axis cs:-0.08,0.54134) {$\dfrac{4}{e^2}$};
  \node[note,anchor=south west] at (axis cs:2.15,0.56) {maximum en $x=2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:4.6,0.3) {$y=x^2e^{-x}$};
\end{axis}
\end{tikzpicture}""",
}

# ======================================================== finition 2026-11-02 : figures ajoutées
FIGURES.update({
# cours (II. 3) et fiche : croissances comparées
"cours_croissances": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=4.6cm, xmin=-0.4, xmax=6.4, ymin=-14, ymax=215,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={50,100,150,200}, scaled y ticks=false]
  \addplot[courbe2, domain=0:5.89] {x^3};
  \addplot[courbe, domain=-0.4:5.33] {exp(x)};
  \guidev{4.5364}{93.354}
  \pnt[otGreenDark]{4.5364}{93.354}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:4.95,182) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:5.92,195) {$y=x^3$};
  \node[note,anchor=south east] at (axis cs:4.3,118) {$e^x > x^3$ dès $x > 4{,}54$};
\end{axis}
\end{tikzpicture}""",

# 1209 Q1-Q2 : comparaison avec la tangente et asymptote en -inf
"ex1209_limites": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-4.4, xmax=2.4, ymin=-1.1, ymax=6.2,
  xtick={-4,-3,-2,-1,1,2}, xticklabels={}, ytick={1,2,3,4,5}]
  \addplot[otGreenDark, line width=1.1pt, domain=-2.05:2.2] {x+1};
  \addplot[courbe, domain=-4.4:1.79] {exp(x)};
  \pnt{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.45,5.3) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.2,1.75) {$y=x+1$};
  \node[note,anchor=south west] at (axis cs:-4.3,0.7) {asymptote $y=0$ en $-\infty$};
\end{axis}
\end{tikzpicture}""",

# 1209 Q3 : taux d'accroissement en 0 et tangente de pente 1
"ex1209_taux": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-1.4, xmax=1.9, ymin=-0.35, ymax=3.5,
  xtick={-1,1}, xticklabels={}, ytick={1,2,3}]
  \addplot[otOrange, line width=0.9pt, dash pattern=on 4pt off 2.5pt, domain=-0.55:1.45] {1+1.71828*x};
  \addplot[otGreenDark, line width=1.1pt, domain=-1.1:1.6] {x+1};
  \addplot[courbe, domain=-1.4:1.2] {exp(x)};
  \guides{1}{2.71828}
  \pnt{0}{1} \pnt[otOrange]{1}{2.71828}
  \node[etiq,text=otInk,anchor=north west] at (axis cs:0.07,0.93) {$A$};
  \node[etiq,text=otOrange!80!black,anchor=north west] at (axis cs:1.06,2.66) {$M$};
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.06,2.71828) {$e$};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:0.55,1.35) {tangente : pente $1$};
\end{axis}
\end{tikzpicture}""",

# 1210 Q3 : signe de la dérivée et sens de variation
"ex1210_variations": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-1.1, xmax=1.6, ymin=-0.5, ymax=5.6,
  xtick={-1,1}, ytick={1,2}]
  \addplot[courbe, domain=-1.1:0.57] {exp(3*x)};
  \addplot[courbe2, domain=-0.33:1.5] {exp(-2*x+1)};
  \pnt{0}{1} \pnt[otGreenDark]{0}{2.71828}
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:0.03,2.71828) {$e$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.6,5.2) {$y=e^{3x}$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:0.55,1.3) {$y=e^{-2x+1}$};
\end{axis}
\end{tikzpicture}""",
})

XLAB_AJOUT = {
    "cours_croissances": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (4.5364, "d", r"4{,}54"), (6, "c", "6")],
    "ex1209_limites": [(-4, "c", "-4"), (-3, "c", "-3"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "c", "1"), (2, "c", "2")],
    "ex1209_taux": [(-1, "c", "-1"), (1, "c", "1")],
}

# Graduations de l'axe des abscisses placées à la main (côté libre de la courbe) :
# « g » sous l'axe à gauche, « d » à droite, « c » centrée dessous, « h » au-dessus.
SR2 = r"\frac{\sqrt{2}}{2}"
XLAB = {
    "cours_exp_tangente": [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "c", "1"), (2, "c", "2")],
    "eq_ex_egal5": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (1.6094, "c", r"\ln 5"), (2, "d", "2")],
    "eq_quad_ln3": [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (0, "g", "0"), (1.0986, "d", r"\ln 3")],
    "ineq_ex_7": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (1.9459, "c", r"\ln 7")],
    "xex_min": [(-5, "h", "-5"), (-4, "h", "-4"), (-3, "h", "-3"), (-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1")],
    "xex_tangente": [(-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1")],
    "av_zeros": [(0.6931, "g", r"\ln 2"), (1.0986, "d", r"\ln 3")],
    "av_ineq": [(0, "g", "0"), (0.6931, "d", r"\ln 2")],
    "log_eq_domaine": [(1, "g", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "log_ineq": [(1.3133, "c", r"\ln(e+1)"), (2, "c", "2"), (3, "c", "3")],
    "etude_complete": [(-4, "c", "-4"), (-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"),
                       (0.4055, "h", r"\ln\frac{3}{2}")],
    "etude_signe": [(0, "g", "0"), (0.6931, "d", r"\ln 2")],
    "cloche_inflexion": [(-2, "c", "-2"), (-0.70711, "c", "-" + SR2), (0.70711, "c", SR2), (2, "c", "2")],
    "cloche_convexite": [(-2, "c", "-2"), (-0.70711, "c", "-" + SR2), (0.70711, "c", SR2), (2, "c", "2")],
    "bacteries": [(34.657, "c", r"34{,}7"), (50, "c", "50"), (100, "c", "100"), (115.13, "c", r"115{,}1")],
}

XLAB.update(XLAB_AJOUT)

# Graduations placées à la main (XLAB) : les étiquettes automatiques de l'axe des abscisses
# sont vides ; sans fond, elles ne laissent plus de petit carré blanc sur la grille ou une courbe.
for _nom in XLAB:
    FIGURES[_nom] = FIGURES[_nom].replace(r"\begin{axis}[", r"\begin{axis}[xticklabel style={fill=none}, ", 1)
