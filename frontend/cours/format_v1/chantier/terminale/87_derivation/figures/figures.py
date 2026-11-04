# -*- coding: utf-8 -*-
"""Figures de la notion « Dérivation et convexité » (Terminale), style des livres.

Compilation : python ../../../outils/figures_livre.py <ce dossier de notion>
"""

FIGURES = {
# ------------------------------------------------------------------ cours
"composee_schema": r"""
\begin{tikzpicture}[boite/.style={draw=otNavy,line width=0.8pt,rounded corners=2mm,minimum height=9mm,
  minimum width=16mm,fill=otSky,text=otInk,font=\normalsize}]
  \node[boite] (a) at (0,0) {$x$};
  \node[boite] (b) at (3.1,0) {$u(x)$};
  \node[boite,minimum width=21mm] (c) at (6.5,0) {$v\big(u(x)\big)$};
  \draw[-{Stealth[length=2.4mm]},otNavy,line width=0.9pt] (a) -- (b);
  \draw[-{Stealth[length=2.4mm]},otNavy,line width=0.9pt] (b) -- (c);
  \node[text=otNavy,anchor=south] at (1.55,0.12) {$u$};
  \node[text=otNavy,anchor=south] at (4.6,0.12) {$v$};
  \draw[-{Stealth[length=2.4mm]},otGreenDark,line width=0.9pt,rounded corners=3mm]
    (a.south) -- ++(0,-0.7) -| (c.south);
  \node[text=otGreenDark,anchor=north] at (3.25,-1.25) {$v \circ u$};
  \node[note,anchor=south] at (1.55,0.62) {d'abord $u$};
  \node[note,anchor=south] at (4.6,0.62) {puis $v$};
\end{tikzpicture}""",

"convexe_concave": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=g, width=3.5cm, height=2.7cm, xmin=0, xmax=3.7, ymin=0, ymax=2.35,
  xtick=\empty, ytick=\empty, grid=none]
  \addplot[courbe, domain=0.05:3.4] {0.6*(x-1.7)^2+0.2};
  \draw[otOrange!90!black,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0.3,1.376) -- (axis cs:1.9,0.224);
  \addplot[courbe2, domain=2.05:3.35] {0.8+1.2*(x-2.7)};
  \fill[otNavy] (axis cs:0.3,1.376) circle (1.8pt);
  \fill[otNavy] (axis cs:1.9,0.224) circle (1.8pt);
  \fill[otGreenDark] (axis cs:2.7,0.8) circle (1.8pt);
  \node[etiq,fill=none,anchor=south west] at (axis cs:0.35,1.42) {$A$};
  \node[etiq,fill=none,anchor=south] at (axis cs:1.98,0.3) {$B$};
  \node[note,fill=none,text=otOrange!75!black,anchor=south west] at (axis cs:1.05,0.95) {sécante};
  \node[note,fill=none,text=otGreenDark,anchor=west] at (axis cs:2.75,0.42) {tangente};
\end{axis}
\node[anchor=south,text=otNavy,font=\normalsize] at ($(g.north)+(0,0.25)$) {convexe : $f'' \ge 0$};
\begin{axis}[otWeb, at={(g.east)}, anchor=west, xshift=1.25cm, width=3.5cm, height=2.7cm,
  xmin=0, xmax=3.7, ymin=0, ymax=2.35, xtick=\empty, ytick=\empty, grid=none, name=d]
  \addplot[courbe, domain=0.05:3.4] {2.1-0.6*(x-1.7)^2};
  \draw[otOrange!90!black,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0.3,0.924) -- (axis cs:1.9,2.076);
  \addplot[courbe2, domain=2.05:3.35] {1.5-1.2*(x-2.7)};
  \fill[otNavy] (axis cs:0.3,0.924) circle (1.8pt);
  \fill[otNavy] (axis cs:1.9,2.076) circle (1.8pt);
  \fill[otGreenDark] (axis cs:2.7,1.5) circle (1.8pt);
  \node[etiq,fill=none,anchor=north west] at (axis cs:0.35,0.85) {$A$};
  \node[etiq,fill=none,anchor=north] at (axis cs:1.98,1.95) {$B$};
  \node[note,fill=none,text=otOrange!75!black,anchor=north west] at (axis cs:1.1,1.05) {sécante};
  \node[note,fill=none,text=otGreenDark,anchor=west] at (axis cs:2.75,2.1) {tangente};
\end{axis}
\node[anchor=south,text=otNavy,font=\normalsize] at ($(d.north)+(0,0.25)$) {concave : $f'' \le 0$};
\end{tikzpicture}""",

"inflexion_x3": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.4cm, xmin=-2.6, xmax=2.7, ymin=-4.6, ymax=5.3,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-4,-2,2,4}]
  \addplot[courbe2, domain=-1.35:1.35] {-3*x};
  \addplot[courbe, domain=-2.22:2.22] {x^3-3*x};
  \fill[otGreenDark] (axis cs:0,0) circle (2.3pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=south west] at (axis cs:0.12,0.2) {$I$};
  \node[note,fill=none,text=otOrange!75!black,anchor=north west] at (axis cs:-2.55,5.25) {concave};
  \node[note,fill=none,text=otNavy,anchor=north east] at (axis cs:2.65,5.25) {convexe};
  \node[etiq,fill=none,text=otNavy,anchor=east] at (axis cs:2.0,3.55) {$y=x^3-3x$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south west] at (axis cs:-1.25,4.05) {$y=-3x$};
\end{axis}
\end{tikzpicture}""",

"lorenz": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.2cm, height=5.2cm, xmin=0, xmax=1.12, ymin=0, ymax=1.12,
  xtick={0.25,0.5,0.75,1}, ytick={0.25,0.5,0.75,1},
  xticklabels={$0{,}25$,$0{,}5$,$0{,}75$,$1$}, yticklabels={$0{,}25$,$0{,}5$,$0{,}75$,$1$}]
  \addplot[fill=otOrange!18, draw=none, domain=0:1] {x} \closedcycle;
  \addplot[fill=white, draw=none, domain=0:1] {x^2} \closedcycle;
  \draw[otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0) -- (axis cs:1,1);
  \addplot[courbe, domain=0:1] {x^2};
  \guides{0.5}{0.25}
  \pnt{0.5}{0.25} \pnt{1}{1}
  \node[note,fill=none,text=otGreenDark,anchor=north west] at (axis cs:0.04,1.1) {droite d'égalité $y=x$};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:0.62,0.33) {$L(x)=x^2$};
\end{axis}
\end{tikzpicture}""",

"inegalites_exp_ln": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5cm, xmin=-2.7, xmax=3.9, ymin=-3.2, ymax=4.6,
  xtick={-2,-1,1,2,3}, ytick={-2,-1,1,2,3,4}]
  \addplot[otNavy!70,line width=1pt,dash pattern=on 4pt off 2.5pt, domain=-2.6:3.4] {x+1};
  \addplot[otGreenDark!80,line width=1pt,dash pattern=on 4pt off 2.5pt, domain=-1.9:3.7] {x-1};
  \addplot[courbe, domain=-2.6:1.45] {exp(x)};
  \addplot[courbe2, domain=0.045:3.7] {ln(x)};
  \pnt{0}{1} \pnt[otGreenDark]{1}{0}
  \node[etiq,fill=none,text=otNavy,anchor=south east] at (axis cs:1.08,3.3) {$y=e^x$};
  \node[etiq,fill=none,text=otNavy,anchor=south east] at (axis cs:3.0,4.35) {$y=x+1$};
  \node[etiq,fill=none,text=otGreenDark,anchor=north west] at (axis cs:2.55,0.85) {$y=\ln x$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south east] at (axis cs:3.75,2.85) {$y=x-1$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------------------- exercices
"ex1257_h": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.8cm, xmin=-3.4, xmax=1.7, ymin=-5.6, ymax=12.4,
  xtick={-2,-1,1}, xticklabels={}, ytick={-4,4,8,12}]
  \addplot[otOrange!85!black, line width=1.35pt, domain=-3.2:-0.8333] {2*x^3+5*x^2-3*x};
  \addplot[courbe, domain=-0.8333:1.32] {2*x^3+5*x^2-3*x};
  \guides{-1.9262}{10.036} \guides{0.2596}{-0.4069}
  \pnt{-1.9262}{10.036} \pnt{0.2596}{-0.4069}
  \fill[otGreenDark] (axis cs:-0.8333,4.8148) circle (2.5pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=west] at (axis cs:-0.62,5.6) {$I$};
  \node[note,fill=none,text=otNavy,anchor=south] at (axis cs:-1.93,10.45) {maximum local};
  \node[note,fill=none,text=otNavy,anchor=north west] at (axis cs:0.36,-0.75) {minimum local};
  \node[note,fill=none,text=otOrange!75!black,anchor=west] at (axis cs:-1.82,2.4) {concave};
  \node[note,fill=none,text=otNavy,anchor=west] at (axis cs:0.1,5.9) {convexe};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:0.55,9.6) {$\mathcal{C}_h$};
\end{axis}
\end{tikzpicture}""",

"ex1253_chaine": r"""
\begin{tikzpicture}[boite/.style={draw=otNavy,line width=0.8pt,rounded corners=2mm,minimum height=11mm,
  minimum width=14mm,fill=otSky,text=otInk,font=\normalsize,inner sep=4pt}]
  \node[boite] (a) at (0,0) {$x$};
  \node[boite] (b) at (3.1,0) {$2x-3$};
  \node[boite] (c) at (6.9,0) {$\dfrac{1}{(2x-3)+1}$};
  \draw[-{Stealth[length=2.4mm]},otNavy,line width=0.9pt] (a) -- (b);
  \draw[-{Stealth[length=2.4mm]},otNavy,line width=0.9pt] (b) -- (c);
  \node[text=otNavy,anchor=south] at ($(a.east)!0.5!(b.west)+(0,0.1)$) {$g$};
  \node[text=otNavy,anchor=south] at ($(b.east)!0.5!(c.west)+(0,0.1)$) {$f$};
  \node[note,fill=none,anchor=south] at ($(b.north)+(0,0.12)$) {$g(x)$};
  \node[note,fill=none,anchor=south] at ($(c.north)+(0,0.12)$) {$f\big(g(x)\big)$};
  \node[text=otGreenDark,anchor=north,align=center,font=\normalsize] at ($(b.south)+(0,-0.15)$)
    {il faut $2x-3 \neq -1$\\ soit $x \neq 1$};
  \node[note,fill=none,anchor=north,align=center] at ($(c.south)+(0,-0.15)$)
    {$f(X)$ existe\\ si $X \neq -1$};
\end{tikzpicture}""",

"ex1261_h": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.6cm, xmin=-0.35, xmax=4.75, ymin=-0.4, ymax=3.25,
  xtick={0.5,1,2,3,4}, xticklabels={}, ytick={1,2,3}]
  \draw[otGreenDark,line width=1.35pt] (axis cs:0.5,0) -- (axis cs:0.5,1.55);
  \addplot[courbe, domain=0.5:4.5, samples=400] {sqrt(2*x-1)};
  \fill[otGreenDark] (axis cs:0.5,0) circle (2.3pt);
  \node[note,fill=none,text=otGreenDark,anchor=south west,align=left] at (axis cs:0.62,2.25) {demi-tangente\\ verticale};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:2.6,1.5) {$y=\sqrt{2x-1}$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- nouveau-1 : lecture sur la courbe de f'
"n1_fprime": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.8cm, xmin=-2.6, xmax=2.75, ymin=-4.6, ymax=4.8,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-4,-3,-2,-1,1,2,3,4}, yticklabels={$-4$,,$-2$,,,$2$,,$4$}]
  \addplot[courbe, domain=-2.2:2.2] {x^3-3*x};
  \node[etiq,fill=none,text=otNavy,anchor=east] at (axis cs:1.95,4.2) {$\mathcal{C}_{f'}$};
\end{axis}
\end{tikzpicture}""",

"n1_fprime_corr": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.8cm, xmin=-2.6, xmax=2.75, ymin=-4.6, ymax=4.8,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-4,-3,-2,-1,1,2,3,4}, yticklabels={$-4$,,$-2$,,,$2$,,$4$}]
  \addplot[otGreenDark, line width=1.6pt, domain=-2.2:-1] {x^3-3*x};
  \addplot[otOrange!85!black, line width=1.6pt, domain=-1:1] {x^3-3*x};
  \addplot[otGreenDark, line width=1.6pt, domain=1:2.2] {x^3-3*x};
  \guidev{-1}{2} \guidev{1}{-2}
  \pnt{-1}{2} \pnt{1}{-2}
  \node[note,fill=none,text=otGreenDark,anchor=north west] at (axis cs:-2.55,4.75) {$f$ convexe};
  \node[note,fill=none,text=otOrange!75!black,anchor=west] at (axis cs:0.08,3.4) {$f$ concave};
  \node[note,fill=none,text=otGreenDark,anchor=east] at (axis cs:2.7,-2.6) {$f$ convexe};
  \node[etiq,fill=none,text=otNavy,anchor=east] at (axis cs:1.95,4.2) {$\mathcal{C}_{f'}$};
\end{axis}
\end{tikzpicture}""",

"n1_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=4.4cm, xmin=-2.95, xmax=3.0, ymin=-2.95, ymax=2.5,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-2,-1,1,2}]
  \addplot[courbe2, domain=0.05:1.8] {-2*x+0.75};
  \addplot[courbe, domain=-2.65:-1] {x^4/4-1.5*x^2};
  \addplot[otOrange!85!black, line width=1.35pt, domain=-1:1] {x^4/4-1.5*x^2};
  \addplot[courbe, domain=1:2.65] {x^4/4-1.5*x^2};
  \fill[otGreenDark] (axis cs:1,-1.25) circle (2.3pt);
  \fill[otGreenDark] (axis cs:-1,-1.25) circle (2.3pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=north east] at (axis cs:0.95,-1.33) {$I$};
  \node[etiq,fill=none,text=otGreenDark,anchor=north west] at (axis cs:-0.95,-1.33) {$J$};
  \node[etiq,fill=none,text=otGreenDark,anchor=west] at (axis cs:1.84,-2.8) {$T$};
  \node[etiq,fill=none,text=otNavy,anchor=north east] at (axis cs:2.95,2.45) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- nouveau-2 : ln x <= x/e
"n2_ln": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.2cm, xmin=-0.5, xmax=8.9, ymin=-2.7, ymax=3.5,
  xtick={1,2.71828,4,6,8}, xticklabels={}, ytick={-2,-1,1,2,3}]
  \addplot[courbe2, domain=0:8.3] {x/exp(1)};
  \addplot[courbe, domain=0.075:8.3, samples=400] {ln(x)};
  \guides{2.71828}{1}
  \fill[otGreenDark] (axis cs:2.71828,1) circle (2.3pt);
  \fill[otGreenDark] (axis cs:0,0) circle (2.1pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=south east] at (axis cs:5.9,2.5) {$T : y=\dfrac{x}{e}$};
  \node[etiq,fill=none,text=otNavy,anchor=north east] at (axis cs:8.3,1.8) {$y=\ln x$};
  \node[etiq,fill=none,text=otGreenDark,anchor=north west] at (axis cs:2.85,0.92) {$(e\,;1)$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south east] at (axis cs:-0.06,0.05) {$O$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- nouveau-3 : propagation (logistique)
"n3_courbe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-0.6, xmax=17.4, ymin=-0.8, ymax=11.6,
  xtick={2,4,6,8,10,12,14,16}, ytick={2,4,6,8,10}, xlabel={$t$}, ylabel={$N$}]
  \addplot[courbe, domain=0:16.5] {10/(1+9*exp(-0.5*x))};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:8.4,7.4) {$\mathcal{C}_N$};
\end{axis}
\end{tikzpicture}""",

"n3_inflexion": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-0.6, xmax=17.4, ymin=-0.8, ymax=11.6,
  xtick={2,4,6,8,10,12,14,16}, ytick={1,5,10}, xlabel={$t$}, ylabel={$N$}]
  \draw[asymptote] (axis cs:0,10) -- (axis cs:17,10);
  \addplot[courbe2, domain=1.2:7.6] {1.25*(x-4.3944)+5};
  \addplot[courbe, domain=0:16.5] {10/(1+9*exp(-0.5*x))};
  \guides{4.3944}{5}
  \pnt{0}{1}
  \fill[otGreenDark] (axis cs:4.3944,5) circle (2.3pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=north west] at (axis cs:4.55,4.85) {$I$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south east] at (axis cs:7.5,9.1) {$T$};
  \node[note,fill=none,text=otRed!85!black,anchor=south east] at (axis cs:17,10.15) {$N=10$};
  \node[note,fill=none,text=otNavy,anchor=west] at (axis cs:0.4,5.75) {convexe};
  \node[note,fill=none,text=otOrange!75!black,anchor=west] at (axis cs:8.7,6.4) {concave};
\end{axis}
\end{tikzpicture}""",

"ex1256_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.4cm, xmin=-1.6, xmax=3.7, ymin=-0.05, ymax=1.38,
  xtick={0.2929,1,1.7071}, xticklabels={$x_1$,$1$,$x_2$}, ytick={0.6065,1}, yticklabels={$e^{-\frac12}$,$1$}]
  \fill[otOrange!12] (axis cs:0.2929,0) rectangle (axis cs:1.7071,1.38);
  \addplot[courbe, domain=-1.55:3.55] {exp(-(x-1)^2)};
  \draw[guide] (axis cs:0,0.6065) -- (axis cs:1.7071,0.6065);
  \guidev{0.2929}{0.6065} \guidev{1.7071}{0.6065} \guidev{1}{1}
  \pnt{1}{1}
  \fill[otGreenDark] (axis cs:0.2929,0.6065) circle (2.3pt);
  \fill[otGreenDark] (axis cs:1.7071,0.6065) circle (2.3pt);
  \node[note,fill=none,text=otOrange!75!black,anchor=south] at (axis cs:1,1.08) {concave};
  \node[note,fill=none,text=otNavy,anchor=south] at (axis cs:-0.75,0.3) {convexe};
  \node[note,fill=none,text=otNavy,anchor=south] at (axis cs:2.75,0.3) {convexe};
  \node[etiq,fill=none,text=otNavy,anchor=south west] at (axis cs:1.95,0.8) {$y=g(x)$};
\end{axis}
\end{tikzpicture}""",

"ex1260_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=3.6cm, xmin=-8, xmax=4.2, ymin=-0.6, ymax=6.3,
  xtick={-7,-5,-3,-1,1,3}, ytick={2,4}]
  \addplot[courbe, domain=-7.6:-3, samples=400] {sqrt(max(x^2+4*x+3,0))};
  \addplot[courbe, domain=-1:3.6, samples=400] {sqrt(max(x^2+4*x+3,0))};
  \pnt{-3}{0} \pnt{-1}{0}
  \node[etiq,fill=none,text=otNavy,anchor=east] at (axis cs:1.7,4.0) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"ex1259_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=3.8cm, xmin=-7.3, xmax=7.6, ymin=-0.45, ymax=4.1,
  xtick={-6,-4,-2,2,4,6}, xticklabels={}, ytick={1,2,3}]
  \draw[asymptote] (axis cs:-2,-0.4) -- (axis cs:-2,4.05);
  \draw[asymptote] (axis cs:2,-0.4) -- (axis cs:2,4.05);
  \addplot[courbe, domain=-7.1:-2.035, samples=300] {ln((x^2+1)/(x^2-4))};
  \addplot[courbe, domain=2.035:7.1, samples=300] {ln((x^2+1)/(x^2-4))};
  \node[note,fill=none,text=otRed!85!black,anchor=north east] at (axis cs:-2.15,4.05) {$x=-2$};
  \node[note,fill=none,text=otRed!85!black,anchor=north west] at (axis cs:2.15,4.05) {$x=2$};
  \node[etiq,fill=none,text=otNavy,anchor=south west] at (axis cs:3.3,1.0) {$\mathcal{C}_f$};
  \node[note,fill=none,anchor=south] at (axis cs:-5.4,0.62) {asymptote $y=0$};
\end{axis}
\end{tikzpicture}""",

"ex1255_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=4.4cm, xmin=-0.5, xmax=4.6, ymin=-0.9, ymax=7.2,
  xtick={1,2,3,4}, ytick={1,3,5}]
  \addplot[courbe2, domain=-0.1:2.1] {5};
  \addplot[courbe, domain=-0.15:4.13] {x^3-6*x^2+9*x+1};
  \guides{2}{3} \guides{3}{1} \guidev{1}{5}
  \pnt{1}{5} \pnt{3}{1}
  \fill[otGreenDark] (axis cs:2,3) circle (2.3pt);
  \node[etiq,fill=none,text=otGreenDark,anchor=south west] at (axis cs:2.08,3.1) {$I$};
  \node[etiq,fill=none,text=otGreenDark,anchor=west] at (axis cs:2.15,5) {$y=5$};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:3.45,6.6) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"ex1258_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.6cm, xmin=-6.3, xmax=6.6, ymin=-5.8, ymax=7.8,
  xtick={-5,-3,-1,3,5}, xticklabels={}, ytick={-4,2,4,6}]
  \draw[asymptote] (axis cs:1,-5.8) -- (axis cs:1,7.7);
  \draw[asymptote] (axis cs:-6.3,1) -- (axis cs:6.5,1);
  \addplot[courbe, domain=-6.2:0.333, samples=300] {(x+3)/(x-1)};
  \addplot[courbe, domain=1.667:6.4, samples=300] {(x+3)/(x-1)};
  \pntv{-1}{-1}
  \node[note,fill=none,text=otRed!85!black,anchor=north west] at (axis cs:1.15,7.7) {$x=1$};
  \node[note,fill=none,text=otRed!85!black,anchor=south west] at (axis cs:-6.2,1.15) {$y=1$};
  \node[note,fill=none,anchor=north east] at (axis cs:-1.15,-1.3) {trou en $(-1\,;-1)$};
  \node[etiq,fill=none,text=otNavy,anchor=west] at (axis cs:2.35,5.2) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",
}

XLAB = {
    "inflexion_x3": [(-2, "g", "-2"), (-1, "g", "-1"), (1, "d", "1"), (2, "c", "2")],
    "ex1257_h": [(-2, "c", "-2"), (-1, "c", "-1"), (1, "h", "1")],
    "ex1261_h": [(0.5, "c", "0{,}5"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "n1_fprime": [(-2, "g", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2")],
    "n1_fprime_corr": [(-2, "g", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2")],
    "n1_f": [(-2, "c", "-2"), (-1, "h", "-1"), (1, "h", "1"), (2, "c", "2")],
    "n2_ln": [(1, "d", "1"), (2.71828, "c", "e"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8")],
    "ex1256_g": [(0.2929, "c", "x_1"), (1, "c", "1"), (1.7071, "c", "x_2")],
    "ex1259_f": [(-6, "c", "-6"), (-4, "c", "-4"), (-2, "g", "-2"), (2, "d", "2"), (4, "c", "4"), (6, "c", "6")],
    "ex1258_f": [(-5, "c", "-5"), (-3, "c", "-3"), (-1, "h", "-1"), (3, "c", "3"), (5, "c", "5")],
}
