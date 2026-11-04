# -*- coding: utf-8 -*-
"""Figures de la notion « Fonction logarithme népérien » (Terminale), style des livres.

    python ../../../outils/figures_livre.py <ce_dossier_notion> [nom …] [--planche]

Couleurs : fonction étudiée en bleu marine (courbe), seconde fonction en orange
(courbe3) ou seuil orange pointillé, éléments de réponse en vert foncé
(points, ensembles solutions sur l'axe), asymptotes en rouge pointillé.
Toutes les valeurs ont été vérifiées dans verif_logarithme.py.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  courbe3/.style={otOrange!90!black,line width=1.35pt},
  droiteA/.style={otMuted,line width=1pt,dash pattern=on 4pt off 2.5pt},
}
% graduation de l'axe des abscisses placée AU-DESSUS de l'axe, à droite (HD) ou à gauche (HG) du trait
\newcommand{\gradHD}[2]{\node[anchor=south west,xshift=1.5pt,yshift=2pt,font=\otRegular\fontsize{9}{10}\selectfont,
  text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:#1,0) {$#2$};}
\newcommand{\gradHG}[2]{\node[anchor=south east,xshift=-1.5pt,yshift=2pt,font=\otRegular\fontsize{9}{10}\selectfont,
  text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:#1,0) {$#2$};}
"""

FIGURES = {
# =================================================================== cours
"cours_symetrie": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=6.2cm, xmin=-2.6, xmax=4.6, ymin=-2.6, ymax=4.6,
  xtick={-2,-1,1,2,3,4}, xticklabels={}, ytick={-2,-1,1,2,3,4}]
  \addplot[otMuted,line width=0.7pt,dash pattern=on 4pt off 2.5pt, domain=-2.5:4.5] {x};
  \addplot[courbe2, domain=-2.6:1.5] {exp(x)};
  \addplot[courbe, domain=0.075:4.5] {ln(x)};
  \draw[guide] (axis cs:0,1) -- (axis cs:1,0);
  \draw[guide] (axis cs:1,2.71828) -- (axis cs:2.71828,1);
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{1}{2.71828}
  \pnt{1}{0} \pnt{2.71828}{1}
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:1.24,2.62) {$(1\,;e)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.8,0.85) {$(e\,;1)$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.6,4.15) {$y=e^{x}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.2,1.62) {$y=\ln x$};
  \node[etiq,text=otMuted,anchor=north west] at (axis cs:3.95,3.8) {$y=x$};
\end{axis}
\end{tikzpicture}""",

"cours_ln_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.9cm, xmin=-0.4, xmax=7.4, ymin=-3.2, ymax=2.6,
  xtick={1,2,3,4,5,6,7}, xticklabels={}, ytick={-3,-2,-1,1,2}]
  \addplot[otOrange,line width=1.1pt, domain=0.2:3] {x-1};
  \addplot[courbe, domain=0.04:7.2] {ln(x)};
  \pnt{1}{0} \pnt{2.71828}{1}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.8,0.92) {$(e\,;1)$};
  \node[note,anchor=west,text=otOrange!75!black] at (axis cs:3.1,2.08) {tangente $y=x-1$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.6,1.55) {$y=\ln x$};
  \node[note,anchor=west] at (axis cs:0.25,-2.8) {asymptote : l’axe des ordonnées};
\end{axis}
\end{tikzpicture}""",

"cours_croissances": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.7cm, xmin=-0.6, xmax=26, ymin=-1.5, ymax=6.6,
  xtick={5,10,15,20,25}, ytick={2,4,6}]
  \addplot[courbe3, domain=0:6.5] {x};
  \addplot[courbe2, domain=0:25] {sqrt(x)};
  \addplot[courbe, domain=0.23:25] {ln(x)};
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:6.8,6.2) {$y=x$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:25,5.15) {$y=\sqrt{x}$};
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:25,2.9) {$y=\ln x$};
  \node[note,anchor=west] at (axis cs:9.5,1.05) {en $+\infty$ : $\dfrac{\ln x}{x}\to 0$};
\end{axis}
\end{tikzpicture}""",

"cours_demivie": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.7cm, xmin=0, xmax=21000, ymin=0, ymax=112,
  xtick={5730,11460}, ytick={25,50,100}, yticklabels={$25\,\%$,$50\,\%$,$100\,\%$}, scaled x ticks=false,
  xlabel={$t$}, ylabel={}]
  \addplot[courbe, domain=0:20500, samples=120] {100*exp(-0.000120968*x)};
  \guides{5730}{50} \guides{11460}{25}
  \pnt[otGreenDark]{5730}{50} \pnt[otGreenDark]{11460}{25}
  \node[note,anchor=south west] at (axis cs:5950,52) {demi-vie $T$ : il reste $50\,\%$};
  \node[note,anchor=south west] at (axis cs:11700,27) {après $2T$ : $25\,\%$};
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:20500,105) {$N(t)=N_0\,e^{-\lambda t}$};
  \node[note,anchor=north east] at (axis cs:20500,-14) {$t$ en années};
\end{axis}
\end{tikzpicture}""",

# ================================================ 1247 équations
"eq_q1": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-2.4, xmax=6.5, ymin=-2.7, ymax=3.25,
  xtick={-2,-1,1.5,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:-2,-2.7) -- (axis cs:-2,3.1);
  \draw[asymptote] (axis cs:0.3333,-2.7) -- (axis cs:0.3333,3.1);
  \addplot[courbe, domain=-1.93:6.3] {ln(x+2)};
  \addplot[courbe3, domain=0.36:6.3] {ln(3*x-1)};
  \guidev{1.5}{1.2528}
  \pnt[otGreenDark]{1.5}{1.2528}
  \node[etiq,text=otOrange!75!black,anchor=south east] at (axis cs:4.0,2.75) {$y=\ln(3x-1)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.5,1.3) {$y=\ln(x+2)$};
\end{axis}
\end{tikzpicture}""",

"eq_q2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-0.4, xmax=9.4, ymin=-2.3, ymax=2.9,
  xtick={2,4,6,7.389,9}, xticklabels={}, ytick={-2,-1,1,2}]
  \draw[seuil] (axis cs:0,2) -- (axis cs:9.1,2);
  \addplot[courbe, domain=0.1:9.1] {ln(x)};
  \guidev{7.389}{2}
  \pnt[otGreenDark]{7.389}{2}
  \node[etiq,text=otOrange!75!black,anchor=south west] at (axis cs:0.4,2.08) {$y=2$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.2,1.0) {$y=\ln x$};
\end{axis}
\end{tikzpicture}""",

"eq_q3": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-2.3, xmax=8.4, ymin=-1.7, ymax=2.8,
  xtick={0.71828,2,4,6,8}, xticklabels={}, ytick={-1,1,2}]
  \addplot[pale, domain=-1.82:2] {ln(x+2)};
  \draw[seuil] (axis cs:0,1) -- (axis cs:8.2,1);
  \addplot[courbe, domain=2:8.2] {ln(x+2)};
  \draw[guide,otRed] (axis cs:0.71828,0) -- (axis cs:0.71828,1);
  \pntv[otRed]{0.71828}{1}
  \pntv{2}{1.3863}
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:8.3,1) {$y=1$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.3,1.6) {$y=\ln(x+2)$};
  \node[note,anchor=south west,text=otRed!85!black] at (axis cs:2.3,2.38) {$e-2$ n’est pas dans $]2\,;+\infty[$};
\end{axis}
\end{tikzpicture}""",

"eq_q4": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.4, xmax=6.4, ymin=-2.7, ymax=3.8,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:1,-2.7) -- (axis cs:1,3.7);
  \draw[seuil] (axis cs:0,2.0794) -- (axis cs:6.2,2.0794);
  \addplot[courbe, domain=1.035:6.2] {ln(x^2-1)};
  \guidev{3}{2.0794}
  \pnt[otGreenDark]{3}{2.0794}
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:6.25,2.0794) {$y=\ln 8$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.3,1.6) {$y=\ln(x+1)+\ln(x-1)$};
\end{axis}
\end{tikzpicture}""",

"eq_q5": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.3, xmax=6.4, ymin=-3.3, ymax=4.0,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={-3,-2,-1,1,2,3}]
  \addplot[courbe3, domain=0:6.2] {ln(x^2+3)};
  \addplot[courbe, domain=0.2:6.2] {2*ln(x)};
  \node[etiq,text=otOrange!75!black,anchor=south west] at (axis cs:0.3,2.4) {$y=\ln(x^2+3)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.6,1.2) {$y=2\ln x$};
  \node[note,anchor=west,text=otGreenDark] at (axis cs:2.4,-1.6) {aucun point commun : $S=\varnothing$};
\end{axis}
\end{tikzpicture}""",

# ================================================ 1248 inéquations
"ineq_q1": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-0.4, xmax=6.4, ymin=-2.4, ymax=2.8,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2}]
  \addplot[courbe3, domain=0:6.2] {ln(x+1)};
  \addplot[courbe, domain=0.05:6.2] {ln(2*x)};
  \guidev{1}{0.6931}
  \sol{1}{6.2} \borneO{1}
  \pnt{1}{0.6931}
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:3.0,2.0) {$y=\ln(2x)$};
  \node[etiq,text=otOrange!75!black,anchor=north west] at (axis cs:3.2,0.95) {$y=\ln(x+1)$};
\end{axis}
\end{tikzpicture}""",

"ineq_q2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-0.4, xmax=6.4, ymin=-2.7, ymax=2.3,
  xtick={0.36788,1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2}]
  \draw[seuil] (axis cs:0,-1) -- (axis cs:6.2,-1);
  \addplot[courbe, domain=0.07:6.2] {ln(x)};
  \guidev{0.36788}{-1}
  \sol{0.36788}{6.2} \borneF{0.36788}
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:6.25,-1) {$y=-1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:5.0,1.85) {$y=\ln x$};
\end{axis}
\end{tikzpicture}""",

"ineq_q3": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-2.2, xmax=3.4, ymin=-2.6, ymax=2.4,
  xtick={-1.5,-1,1,2,3}, xticklabels={}, ytick={-2,-1,2}]
  \draw[asymptote] (axis cs:-1.5,-2.6) -- (axis cs:-1.5,2.3);
  \addplot[courbe, domain=-1.46:3.2] {ln(2*x+3)};
  \sol{-1.5}{-1} \borneO{-1.5} \borneF{-1}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.0,1.2) {$y=\ln(2x+3)$};
\end{axis}
\end{tikzpicture}""",

"ineq_q4": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-5.4, xmax=5.4, ymin=-2.7, ymax=3.6,
  xtick={-4,-2,-1,1,2,4}, xticklabels={}, ytick={-2,2,3}]
  \draw[asymptote] (axis cs:-1,-2.7) -- (axis cs:-1,3.5);
  \draw[asymptote] (axis cs:1,-2.7) -- (axis cs:1,3.5);
  \draw[seuil] (axis cs:-5.2,1.0986) -- (axis cs:5.2,1.0986);
  \addplot[courbe, domain=1.035:5.2] {ln(x^2-1)};
  \addplot[courbe, domain=-5.2:-1.035] {ln(x^2-1)};
  \guidev{2}{1.0986} \guidev{-2}{1.0986}
  \pnt{2}{1.0986} \pnt{-2}{1.0986}
  \sol{-5.2}{-2} \sol{2}{5.2} \borneO{-2} \borneO{2}
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:5.25,1.0986) {$y=\ln 3$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.3,-0.7) {$y=\ln(x^2-1)$};
\end{axis}
\end{tikzpicture}""",

"ineq_q5": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.4, xmax=6.6, ymin=-2.7, ymax=3.6,
  xtick={1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:2,-2.7) -- (axis cs:2,3.5);
  \draw[seuil] (axis cs:0,2.0794) -- (axis cs:6.4,2.0794);
  \addplot[courbe, domain=2.035:6.4] {ln(x^2-2*x)};
  \guidev{4}{2.0794}
  \pnt{4}{2.0794}
  \sol{2}{4} \borneO{2} \borneF{4}
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:6.45,2.0794) {$y=\ln 8$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.1,-0.7) {$y=\ln x+\ln(x-2)$};
\end{axis}
\end{tikzpicture}""",

# ================================================ 1246 études
"etude_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-0.6, xmax=6.4, ymin=-2.7, ymax=2.8,
  xtick={0.5,1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,1,2}]
  \draw[asymptote] (axis cs:0.5,-2.7) -- (axis cs:0.5,2.7);
  \addplot[courbe, domain=0.54:6.2] {ln(2*x-1)};
  \pnt{1}{0}
  \node[note,anchor=south west] at (axis cs:0.6,2.2) {asymptote $x=\frac{1}{2}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.0,1.2) {$y=\ln(2x-1)$};
\end{axis}
\end{tikzpicture}""",

"etude_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-0.2, xmax=2.45, ymin=-0.7, ymax=2.25,
  xtick={0.36788,1,2}, xticklabels={}, ytick={1,2}]
  \addplot[courbe, domain=0.001:2.4] {x*ln(x)};
  \guides{0.36788}{-0.36788}
  \pntv{0}{0}
  \pnt[otGreenDark]{0.36788}{-0.36788}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.03,-0.36788) {$-\frac{1}{e}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.5,0.55) {$y=x\ln x$};
\end{axis}
\end{tikzpicture}""",

"etude_h": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-2.4, xmax=5.4, ymin=-2.7, ymax=3.2,
  xtick={-2,-1,1,2,3,4,5}, xticklabels={}, ytick={-2,-1,1,2},
  yticklabel style={anchor=south west,xshift=1pt,yshift=1pt}]
  \draw[asymptote] (axis cs:1,-2.7) -- (axis cs:1,3.1);
  \draw[asymptote] (axis cs:2,-2.7) -- (axis cs:2,3.1);
  \addplot[courbe, domain=-2.2:0.93] {ln(x^2-3*x+2)};
  \addplot[courbe, domain=2.07:5.2] {ln(x^2-3*x+2)};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.7,-1.0) {$y=\ln(x^2-3x+2)$};
\end{axis}
\end{tikzpicture}""",

"etude_k": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-0.3, xmax=7.4, ymin=-1.25, ymax=0.45,
  xtick={1,1.6487,3,4,5,6,7}, xticklabels={}, ytick={-1,-0.5}]
  \addplot[courbe, domain=0.632:7.2] {ln(x)/x^2};
  \guides{1.6487}{0.18394}
  \pnt[otGreenDark]{1.6487}{0.18394}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.03,0.18394) {$\frac{1}{2e}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.5,-0.15) {$y=\dfrac{\ln x}{x^2}$};
\end{axis}
\end{tikzpicture}""",

"etude_m": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-5.4, xmax=5.4, ymin=-3.3, ymax=3.3,
  xtick={-4,-2,-1,1,2,4}, xticklabels={}, ytick={-3,-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:-1,-3.3) -- (axis cs:-1,3.2);
  \draw[asymptote] (axis cs:1,-3.3) -- (axis cs:1,3.2);
  \addplot[courbe, domain=1.087:5.2] {ln((x+1)/(x-1))};
  \addplot[courbe, domain=-5.2:-1.087] {ln((x+1)/(x-1))};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.0,1.6) {$y=\ln\left(\dfrac{x+1}{x-1}\right)$};
\end{axis}
\end{tikzpicture}""",

# ================================================ 1251 synthèse 1
"synth1_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.9cm, xmin=-2.4, xmax=6.4, ymin=-2.7, ymax=3.4,
  xtick={-2,-1,1,2,3,4,5,6}, xticklabels={}, ytick={-2,-1,2,3}]
  \draw[asymptote] (axis cs:1,-2.7) -- (axis cs:1,3.2);
  \draw[asymptote] (axis cs:3,-2.7) -- (axis cs:3,3.2);
  \draw[guide] (axis cs:2,-2.7) -- (axis cs:2,2.9);
  \addplot[courbe, domain=-2.2:0.9635] {ln(x^2-4*x+3)};
  \addplot[courbe, domain=3.0365:6.2] {ln(x^2-4*x+3)};
  \gradHD{1}{1} \gradHG{3}{3}
  \node[note,anchor=south] at (axis cs:2,2.95) {axe $x=2$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.5,-0.9) {$y=\ln(x^2-4x+3)$};
\end{axis}
\end{tikzpicture}""",

"synth1_ineg": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4cm, xmin=-1.5, xmax=3.7, ymin=-2.7, ymax=3.5,
  xtick={-1,1,2,3}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:-1,-2.7) -- (axis cs:-1,3.4);
  \addplot[courbe3, domain=-1.3:3.3] {x};
  \addplot[courbe, domain=-0.925:3.5] {ln(1+x)};
  \pnt[otGreenDark]{0}{0}
  \node[etiq,text=otOrange!75!black,anchor=south east] at (axis cs:3.0,3.1) {$y=x$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.6,0.8) {$y=\ln(1+x)$};
\end{axis}
\end{tikzpicture}""",

"synth1_ax": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.4, xmax=9.4, ymin=-2.9, ymax=3.6,
  xtick={2,2.71828,4,6,8}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \addplot[droiteA, domain=0:5.4] {-0.5*x};
  \addplot[courbe3, line width=1.1pt, domain=0:9.2] {0.3*x};
  \addplot[courbe2, line width=1.1pt, domain=0:8.6] {x/2.71828};
  \addplot[courbe, domain=0.06:9.2] {ln(x)};
  \guidev{2.71828}{1}
  \pnt{0.7035}{-0.35175}
  \pnt{1.63134}{0.4894} \pnt{5.93779}{1.78134}
  \pnt[otGreenDark]{2.71828}{1}
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:8.6,3.2) {$a=\frac{1}{e}$};
  \node[etiq,text=otOrange!75!black,anchor=west] at (axis cs:9.3,2.76) {$a=0{,}3$};
  \node[etiq,text=otMuted,anchor=west] at (axis cs:5.5,-2.7) {$a=-0{,}5$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.6,1.45) {$y=\ln x$};
\end{axis}
\end{tikzpicture}""",

# ================================================ 1252 synthèse 2
"synth2_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.6cm, xmin=-0.3, xmax=5.4, ymin=-2.8, ymax=1.6,
  xtick={0.15859,1,2,3.14619,4,5}, xticklabels={}, ytick={-2,-1,1}]
  \addplot[courbe, domain=0.009:5.3] {ln(x)-x+2};
  \guides{1}{1}
  \pnt[otGreenDark]{1}{1}
  \pnt[otGreenDark]{0.15859}{0} \pnt[otGreenDark]{3.14619}{0}
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:5.2,-1.75) {$y=\ln x-x+2$};
\end{axis}
\end{tikzpicture}""",

"synth2_ineq": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.3, xmax=5.4, ymin=-3.1, ymax=3.4,
  xtick={0.15859,1,2,3.14619,4,5}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \addplot[courbe, domain=0.045:5.2] {ln(x)};
  \addplot[courbe3, domain=0:5.3] {x-2};
  \guidev{0.15859}{-1.84141} \guidev{3.14619}{1.14619}
  \sol{0.15859}{3.14619} \borneF{0.15859} \borneF{3.14619}
  \pnt{0.15859}{-1.84141} \pnt{3.14619}{1.14619}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.7,1.05) {$y=\ln x$};
  \node[etiq,text=otOrange!75!black,anchor=south east] at (axis cs:4.6,2.75) {$y=x-2$};
\end{axis}
\end{tikzpicture}""",
}

# Graduations de l'axe des abscisses placées à la main, du côté libre des courbes :
# « g » sous l'axe à gauche du trait, « d » à droite, « c » centrée, « h » au-dessus.
XLAB = {
    "cours_symetrie": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "d", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "cours_ln_tangente": [(1, "d", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6"),
                          (7, "c", "7")],
    "eq_q1": [(-2, "g", "-2"), (-1, "d", "-1"), (1.5, "c", r"\frac{3}{2}"), (3, "c", "3"), (4, "c", "4"),
              (5, "c", "5"), (6, "c", "6")],
    "eq_q2": [(2, "c", "2"), (4, "c", "4"), (6, "c", "6"), (7.389, "c", "e^2"), (9, "c", "9")],
    "eq_q3": [(0.71828, "c", "e-2"), (2, "c", "2"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8")],
    "eq_q4": [(1, "g", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
    "eq_q5": [(1, "d", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
    "ineq_q1": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
    "ineq_q2": [(0.36788, "g", r"\frac{1}{e}"), (1, "d", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"),
                (5, "c", "5"), (6, "c", "6")],
    "ineq_q3": [(-1.5, "g", r"-\frac{3}{2}"), (-1, "d", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "ineq_q4": [(-4, "c", "-4"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "g", "1"), (2, "c", "2"), (4, "c", "4")],
    "ineq_q5": [(1, "c", "1"), (2, "g", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
    "etude_f": [(0.5, "g", r"\frac{1}{2}"), (1, "d", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"),
                (6, "c", "6")],
    "etude_g": [(0.36788, "h", r"\frac{1}{e}"), (1, "d", "1"), (2, "c", "2")],
    "etude_h": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "g", "1"), (2, "d", "2"), (3, "c", "3"), (4, "c", "4"),
                (5, "c", "5")],
    "etude_k": [(1, "d", "1"), (1.6487, "c", r"\sqrt{e}"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"),
                (6, "c", "6"), (7, "c", "7")],
    "etude_m": [(-4, "h", "-4"), (-2, "h", "-2"), (-1, "g", "-1"), (1, "d", "1"), (2, "c", "2"), (4, "c", "4")],
    "synth1_f": [(-2, "c", "-2"), (-1, "c", "-1"), (2, "d", "2"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")],
    "synth1_ineg": [(-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "synth1_ax": [(2, "c", "2"), (2.71828, "c", "e"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8")],
    "synth2_f": [(0.15859, "d", r"\alpha"), (1, "c", "1"), (2, "c", "2"), (3.14619, "g", r"\beta"), (4, "c", "4"),
                 (5, "c", "5")],
    "synth2_ineq": [(0.15859, "h", r"\alpha"), (1, "d", "1"), (2, "d", "2"), (3.14619, "c", r"\beta"), (4, "c", "4"),
                    (5, "c", "5")],
}

# ======================================================== finition 2026-11-02 : figures ajoutées
FIGURES.update({
# 1245 Q2 : ensemble de définition de ln(x^2 - 4), deux branches
"ex1245_domaine": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-5.9, xmax=6.1, ymin=-3.2, ymax=3.9,
  xtick={-4,-2,2,4}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \draw[asymptote] (axis cs:-2,-3.2) -- (axis cs:-2,3.7);
  \draw[asymptote] (axis cs:2,-3.2) -- (axis cs:2,3.7);
  \addplot[courbe, domain=-5.5:-2.0125, samples=200] {ln(x^2-4)};
  \addplot[courbe, domain=2.0125:5.5, samples=200] {ln(x^2-4)};
  \sol{-5.85}{-2} \sol{2}{5.95} \borneO{-2} \borneO{2}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.6,-1.4) {$y=\ln\left(x^2-4\right)$};
\end{axis}
\end{tikzpicture}""",

# 1249 Q1 : x ln x en 0+
"ex1249_xlnx": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.8cm, xmin=-0.12, xmax=1.75, ymin=-0.55, ymax=0.95,
  xtick={0.36788,1,1.5}, xticklabels={}, ytick={0.5}, yticklabels={$0{,}5$}]
  \addplot[courbe, domain=0.0005:1.6, samples=300] {x*ln(x)};
  \pntv[otGreenDark]{0}{0}
  \node[note,anchor=south west,text=otGreenDark] at (axis cs:0.05,0.42) {limite $0$ en $0^+$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.45,0.55) {$y=x\ln x$};
\end{axis}
\end{tikzpicture}""",

# 1249 Q2 : ln x / x en +inf
"ex1249_lnx_x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.9cm, xmin=-0.8, xmax=21.2, ymin=-0.95, ymax=0.75,
  xtick={2.71828,5,10,15,20}, xticklabels={}, ytick={-0.5,0.36788}, yticklabels={$-0{,}5$,$\dfrac{1}{e}$}]
  \addplot[courbe, domain=0.6:20.6, samples=300] {ln(x)/x};
  \guides{2.71828}{0.36788}
  \pnt{2.71828}{0.36788}
  \node[note,anchor=south east,text=otGreenDark] at (axis cs:20.5,0.28) {tend vers $0$ en $+\infty$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.6,-0.25) {$y=\dfrac{\ln x}{x}$};
\end{axis}
\end{tikzpicture}""",

# 1249 Q3 : ln(1+x) et sa tangente y = x en 0
"ex1249_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-1.5, xmax=3.4, ymin=-2.6, ymax=2.5,
  xtick={1,2,3}, xticklabels={}, ytick={-2,-1,1,2}]
  \draw[asymptote] (axis cs:-1,-2.6) -- (axis cs:-1,2.4);
  \addplot[otGreenDark, line width=1.1pt, domain=-1.3:2.3] {x};
  \addplot[courbe, domain=-0.909:3.2, samples=300] {ln(1+x)};
  \pnt[otGreenDark]{0}{0}
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:2.2,2.25) {$y=x$};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:0.6,-0.9) {tangente en $0$ : pente $1$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.15,1.05) {$y=\ln(1+x)$};
  \node[note,anchor=north east] at (axis cs:-1.05,-2.0) {$x=-1$};
\end{axis}
\end{tikzpicture}""",

# 1250 Q3 : refroidissement de Newton
"ex1250_newton": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-2.5, xmax=64, ymin=-8, ymax=112,
  xtick={10,20,30,40,50,60}, ytick={20,40,60,80,100}, xlabel={$t$}, ylabel={$T$}]
  \draw[asymptote] (axis cs:0,20) -- (axis cs:62,20);
  \addplot[courbe, domain=0:60] {20+80*exp(-ln(2)/10*x)};
  \guides{10}{60}
  \pnt{0}{100} \pnt[otGreenDark]{10}{60}
  \node[note,anchor=north east] at (axis cs:62,18.5) {température ambiante $20$ °C};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:14,62) {$T(t)=20+80\,e^{-kt}$};
\end{axis}
\end{tikzpicture}""",

# 1250 Q5 : seuil C_n < 5
"ex1250_seuil": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-0.6, xmax=16.4, ymin=-4, ymax=56,
  xtick={2,4,6,8,11,14,16}, xticklabels={}, ytick={10,20,30,40,50}, xlabel={$n$}, ylabel={},
  xmajorgrids=false, ymajorgrids=true]
  \draw[seuil] (axis cs:0,5) -- (axis cs:16.2,5);
  \draw[guide] (axis cs:11,0) -- (axis cs:11,3.6);
  \addplot[only marks, mark=*, mark size=1.8pt, otNavy, samples at={0,1,...,10}] {50*0.8^x};
  \addplot[only marks, mark=*, mark size=1.8pt, otGreenDark, samples at={11,12,...,16}] {50*0.8^x};
  \node[etiq,text=otOrange!80!black,anchor=south west] at (axis cs:0.4,5.6) {seuil $5$ mg/L};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.2,30) {$C_n=50\times 0{,}8^n$};
  \node[note,anchor=north east,text=otNavy,align=right] at (axis cs:16.2,55) {$C_{10}\approx 5{,}37$ : encore au-dessus};
  \node[note,anchor=north east,text=otGreenDark,align=right] at (axis cs:16.2,47) {$C_{11}\approx 4{,}29$ : sous le seuil};
\end{axis}
\end{tikzpicture}""",
})

XLAB.update({
    "ex1245_domaine": [(-4, "c", "-4"), (-2, "d", "-2"), (2, "g", "2"), (4, "c", "4")],
    "ex1249_xlnx": [(0.36788, "h", r"\frac{1}{e}"), (1, "d", "1"), (1.5, "c", r"1{,}5")],
    "ex1249_lnx_x": [(2.71828, "c", "e"), (5, "c", "5"), (10, "c", "10"), (15, "c", "15"), (20, "c", "20")],
    "ex1249_tangente": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3")],
    "ex1250_seuil": [(2, "c", "2"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8"), (11, "c", r"\mathbf{11}"),
                     (14, "c", "14"), (16, "c", "16")],
})

# Graduations placées à la main (XLAB) : les étiquettes automatiques de l'axe des abscisses
# sont vides ; sans fond, elles ne laissent plus de petit carré blanc sur la grille ou une courbe.
for _nom in XLAB:
    FIGURES[_nom] = FIGURES[_nom].replace(r"\begin{axis}[", r"\begin{axis}[xticklabel style={fill=none}, ", 1)
