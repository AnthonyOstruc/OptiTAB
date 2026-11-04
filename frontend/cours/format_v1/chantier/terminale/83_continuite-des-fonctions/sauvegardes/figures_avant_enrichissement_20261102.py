# -*- coding: utf-8 -*-
"""Figures de la notion 83 « Continuité des fonctions » (Terminale), style des livres.

Compilation : python ../../../../outils/figures_livre.py <dossier_notion> [noms…] [--planche]
"""

FIGURES = {
# ================================================================ cours
"cours_continuite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=3.4cm, height=2.6cm, xmin=-0.4, xmax=4.4, ymin=-0.4, ymax=3.6,
  xtick=\empty, ytick=\empty, grid=none]
  \addplot[courbe, domain=0:4, samples=120] {1.3+0.9*sin(deg(1.3*x))+0.12*x};
  \pnt{0}{1.3} \pnt{4}{0.9853}
  \node[note,anchor=north,align=center,yshift=-0.35cm] at (axis description cs:0.5,0) {continue :\\ tracé sans lever le crayon};
\end{axis}
\begin{axis}[otWeb, at={(4.9cm,0)}, width=3.4cm, height=2.6cm, xmin=-0.4, xmax=4.5, ymin=-0.4, ymax=3.6,
  xtick={1,2,3,4}, ytick={1,2,3}]
  \draw[courbe] (axis cs:0,0) -- (axis cs:1,0);
  \draw[courbe] (axis cs:1,1) -- (axis cs:2,1);
  \draw[courbe] (axis cs:2,2) -- (axis cs:3,2);
  \draw[courbe] (axis cs:3,3) -- (axis cs:4,3);
  \pnt{0}{0} \pnt{1}{1} \pnt{2}{2} \pnt{3}{3}
  \pntv{1}{0} \pntv{2}{1} \pntv{3}{2} \pntv{4}{3}
  \node[note,anchor=north,align=center,yshift=-0.35cm] at (axis description cs:0.5,0) {partie entière $E$ :\\ discontinue en chaque entier};
\end{axis}
\end{tikzpicture}""",

"cours_point_fixe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5cm, xmin=-0.15, xmax=2.6, ymin=-0.15, ymax=2.45,
  xtick={1,2}, xticklabels={}, ytick={1,2}]
  \addplot[otMuted,line width=0.8pt, domain=0:2.45] {x};
  \addplot[courbe, domain=0:2.45] {sqrt(x+2)};
  \draw[otOrange,line width=1pt,line join=round] (axis cs:0,0) -- (axis cs:0,1.41421) -- (axis cs:1.41421,1.41421)
    -- (axis cs:1.41421,1.84776) -- (axis cs:1.84776,1.84776) -- (axis cs:1.84776,1.96157) -- (axis cs:1.96157,1.96157)
    -- (axis cs:1.96157,1.99037) -- (axis cs:1.99037,1.99037);
  \guidev{1.41421}{1.41421} \guidev{1.84776}{1.84776}
  \pnt[otOrange]{0}{0} \pnt[otOrange]{1.41421}{0} \pnt[otOrange]{1.84776}{0}
  \pnt[otGreenDark]{2}{2}
  \node[anchor=north west,inner sep=1.5pt,text=otOrange!75!black] at (axis cs:0.04,-0.05) {$u_0$};
  \node[anchor=north,inner sep=1.5pt,text=otOrange!75!black] at (axis cs:1.41421,-0.05) {$u_1$};
  \node[anchor=north,inner sep=1.5pt,text=otOrange!75!black] at (axis cs:1.84776,-0.05) {$u_2$};
  \node[anchor=south east,inner sep=1.5pt,text=otGreenDark] at (axis cs:1.95,2.05) {$\ell=2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.05,1.85) {$y=\sqrt{x+2}$};
  \node[etiq,text=otMuted,anchor=north west] at (axis cs:2.1,1.95) {$y=x$};
\end{axis}
\end{tikzpicture}""",

"cours_tvi": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.4cm, xmin=-0.3, xmax=6.3, ymin=-0.35, ymax=3.4,
  xtick={0.8,1.4,3,4.6,5.2}, xticklabels={}, ytick={0.346,1.6,2.854}, yticklabels={$f(a)$,$k$,$f(b)$},
  yticklabel style={font=\large}]
  \draw[seuil] (axis cs:0,1.6) -- (axis cs:6.1,1.6);
  \addplot[courbe, domain=0.8:5.2, samples=160] {1.6+0.25*(x-3)*((x-3)^2-2.56)};
  \guides{0.8}{0.346} \guides{5.2}{2.854}
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 2pt off 1.6pt] (axis cs:1.4,0) -- (axis cs:1.4,1.6);
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 2pt off 1.6pt] (axis cs:3,0) -- (axis cs:3,1.6);
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 2pt off 1.6pt] (axis cs:4.6,0) -- (axis cs:4.6,1.6);
  \pnt{0.8}{0.346} \pnt{5.2}{2.854}
  \pnt[otGreenDark]{1.4}{1.6} \pnt[otGreenDark]{3}{1.6} \pnt[otGreenDark]{4.6}{1.6}
  \node[anchor=north,font=\large,inner sep=1.5pt,text=otMuted,yshift=-2pt] at (axis cs:0.8,0) {$a$};
  \node[anchor=north,font=\large,inner sep=1.5pt,text=otMuted,yshift=-2pt] at (axis cs:5.2,0) {$b$};
  \node[anchor=north,font=\large,inner sep=1.5pt,text=otGreenDark,yshift=-2pt] at (axis cs:1.4,0) {$c_1$};
  \node[anchor=north,font=\large,inner sep=1.5pt,text=otGreenDark,yshift=-2pt] at (axis cs:3,0) {$c_2$};
  \node[anchor=north,font=\large,inner sep=1.5pt,text=otGreenDark,yshift=-2pt] at (axis cs:4.6,0) {$c_3$};
  \node[etiq,font=\large,text=otNavy,anchor=south east] at (axis cs:2.15,2.25) {$y=f(x)$};
\end{axis}
\end{tikzpicture}""",

"cours_unique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6cm, height=4.6cm, xmin=-0.2, xmax=1.45, ymin=-1.35, ymax=1.5,
  xtick={1}, ytick={-1,1}]
  \addplot[pale, domain=-0.2:0] {x^3+x-1};
  \addplot[pale, domain=1:1.12] {x^3+x-1};
  \addplot[courbe, domain=0:1] {x^3+x-1};
  \guides{1}{1}
  \pnt{0}{-1} \pnt{1}{1} \pnt[otGreenDark]{0.6823}{0}
  \node[note,anchor=south east,text=otGreenDark] at (axis cs:0.66,0.04) {$\alpha\approx 0{,}682$};
  \node[note,anchor=north west] at (axis cs:0.06,-1.06) {$f(0)=-1<0$};
  \node[note,anchor=west] at (axis cs:1.05,0.86) {$f(1)=1>0$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.74,-0.38) {$y=x^3+x-1$};
\end{axis}
\end{tikzpicture}""",

"cours_dichotomie": r"""
\begin{tikzpicture}[x=4.5cm,y=0.62cm]
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 3pt off 2pt] (0.6823,0.75) -- (0.6823,-5.45);
  \node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (0.6823,0.75) {$\alpha$};
  \node[anchor=south,font=\otRegular\fontsize{9}{11}\selectfont,text=otNavy] at (-0.2,0.55) {étape};
  \foreach \r/\a/\b/\la/\lb in {0/0/1/0/1, 1/0.5/1/0{,}5/1, 2/0.5/0.75/0{,}5/0{,}75, 3/0.625/0.75/0{,}625/0{,}75,
      4/0.625/0.6875/0{,}625/0{,}6875, 5/0.65625/0.6875/0{,}65625/0{,}6875}{
    \node[anchor=center,font=\otRegular\fontsize{10}{12}\selectfont,text=otNavy] at (-0.2,-\r) {\r};
    \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=east] at (\a-0.012,-\r) {$\la$};
    \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=west] at (\b+0.012,-\r) {$\lb$};
  }
  \foreach \r/\a/\b in {0/0/1, 1/0.5/1, 2/0.5/0.75, 3/0.625/0.75, 4/0.625/0.6875}{
    \draw[otNavy,line width=3.2pt,line cap=butt] (\a,-\r) -- (\b,-\r);}
  \draw[otGreen,line width=3.2pt,line cap=butt] (0.65625,-5) -- (0.6875,-5);
  \foreach \r/\m in {0/0.5, 1/0.75, 2/0.625, 3/0.6875, 4/0.65625}{
    \draw[otOrange,line width=1.3pt] (\m,-\r+0.3) -- (\m,-\r-0.3);}
  \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=south,text=otOrange!75!black,fill=none] at (0.5,0.3) {$m$};
\end{tikzpicture}""",

# ================================================================ exercice 868
"ex868_trou": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-1.4, xmax=4.4, ymin=-0.6, ymax=6.6,
  xtick={1,2,3}, ytick={2,4,6}]
  \addplot[courbe, domain=-1.2:1.93] {x+2};
  \addplot[courbe, domain=2.07:4.2] {x+2};
  \guides{2}{4}
  \pntv{2}{4}
  \node[note,anchor=south east] at (axis cs:1.9,4.3) {trou en $(2\,;4)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.6,4.1) {$y=f(x)$};
\end{axis}
\end{tikzpicture}""",

"ex868_raccord": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-1.8, xmax=2.9, ymin=-0.6, ymax=4.4,
  xtick={-1,1,2}, ytick={1,2,3,4}]
  \addplot[courbe, domain=-1.75:1] {x^2};
  \addplot[courbe2, domain=1:2.6] {2*x-1};
  \guides{1}{1}
  \pnt[otGreenDark]{1}{1}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-1.2,2.7) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:2.05,2.8) {$y=2x-1$};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:1.12,0.95) {raccord en $(1\,;1)$};
\end{axis}
\end{tikzpicture}""",

"ex868_sinx": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=3cm, xmin=-9.9, xmax=10.3, ymin=-0.45, ymax=1.4,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$}, ytick={1}]
  \addplot[courbe, domain=-9.6:-0.06] {sin(x)/x};
  \addplot[courbe, domain=0.06:9.6] {sin(x)/x};
  \pntv{0}{1}
  \node[note,anchor=south west] at (axis cs:0.35,1.03) {trou en $(0\,;1)$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:4.2,0.3) {$y=\dfrac{\sin x}{x}$};
\end{axis}
\end{tikzpicture}""",

"ex868_abs": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=3.6cm, xmin=-0.4, xmax=6.6, ymin=-0.5, ymax=3.6,
  xtick={1,2,3,4,5,6}, ytick={1,2,3}]
  \addplot[courbe, domain=0:6, samples=3] {abs(x-3)};
  \pnt[otGreenDark]{3}{0}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:3,2.2) {$y=|x-3|$};
\end{axis}
\end{tikzpicture}""",

# ================================================================ exercice 870
"ex870_inverse": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-2.4, xmax=4.4, ymin=-5.3, ymax=5.5,
  xtick={-2,-1,2,3,4}, xticklabels={}, ytick={-4,-2,2,4}]
  \addplot[courbe, domain=-2.2:0.81, samples=200] {1/(x-1)};
  \addplot[courbe, domain=1.19:4.2, samples=200] {1/(x-1)};
  \draw[asymptote] (axis cs:1,-5.3) -- (axis cs:1,5.4);
  \node[note,anchor=south west] at (axis cs:1.12,-5.1) {asymptote $x=1$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.3,1.0) {$y=\dfrac{1}{x-1}$};
\end{axis}
\end{tikzpicture}""",

"ex870_saut2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-2.7, xmax=2.9, ymin=-2.9, ymax=2.9,
  xtick={-2,-1,1,2}, xticklabels={}, ytick={-2,-1,1,2}]
  \addplot[courbe, domain=-2.5:0] {x+1};
  \addplot[courbe2, domain=0:2.5] {x-1};
  \pntv{0}{1} \pnt[otGreenDark]{0}{-1}
  \node[note,anchor=west,text=otOrange!75!black] at (axis cs:0.14,1) {saut de $2$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-1.35,0.25) {$y=x+1$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.6,-0.9) {$y=x-1$};
\end{axis}
\end{tikzpicture}""",

"ex870_inverse_carre": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-3.3, xmax=3.5, ymin=-0.5, ymax=6.6,
  xtick={-3,-2,-1,1,2,3}, ytick={2,4,6}]
  \addplot[courbe, domain=-3.1:-0.405, samples=200] {1/x^2};
  \addplot[courbe, domain=0.405:3.1, samples=200] {1/x^2};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:1.05,1.6) {$y=\dfrac{1}{x^2}$};
  \node[note,anchor=north east,align=right] at (axis cs:-0.65,6.4) {asymptote verticale :\\ l'axe des ordonnées};
\end{axis}
\end{tikzpicture}""",

"ex870_sin_inv": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.2cm, height=3.6cm, xmin=-1.6, xmax=1.55, ymin=-1.5, ymax=1.6,
  xtick={-1,1}, ytick={-1,1}, yticklabels={}, grid=none]
  \draw[seuil] (axis cs:-1.2,1) -- (axis cs:1.45,1);
  \draw[seuil] (axis cs:-1.2,-1) -- (axis cs:1.45,-1);
  \node[note,anchor=east] at (axis cs:-1.33,1) {$1$};
  \node[note,anchor=east] at (axis cs:-1.33,-1) {$-1$};
  \addplot[courbe, line width=0.8pt, domain=0.72:70, samples=3000] ({1/x},{sin(x)});
  \addplot[courbe, line width=0.8pt, domain=0.72:70, samples=3000] ({-1/x},{-sin(x)});
  \pnt[otGreenDark]{0}{0}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.75,-0.35) {$y=\sin\left(\dfrac{1}{x}\right)$};
\end{axis}
\end{tikzpicture}""",

"ex870_saut1": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-1.8, xmax=3.3, ymin=-0.5, ymax=4.4,
  xtick={-1,1,2,3}, ytick={1,2,3,4}]
  \addplot[courbe, domain=-1.75:1] {x^2};
  \addplot[courbe2, domain=1:3.1] {x+1};
  \guidev{1}{1}
  \pntv{1}{1} \pnt[otGreenDark]{1}{2}
  \draw[otOrange,line width=0.8pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:1.35,1) -- (axis cs:1.35,2);
  \node[note,anchor=west,text=otOrange!75!black] at (axis cs:1.42,1.28) {saut de $1$};
  \draw[otOrange!60,line width=0.5pt,dash pattern=on 1.5pt off 1.5pt] (axis cs:1,1) -- (axis cs:1.35,1) (axis cs:1,2) -- (axis cs:1.35,2);
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-1.2,2.7) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:2.3,3.45) {$y=x+1$};
\end{axis}
\end{tikzpicture}""",

# ================================================================ exercice 872
"ex872_cube": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.6cm, xmin=-3.8, xmax=3.2, ymin=-1.2, ymax=17.5,
  xtick={-3,-2,-1,1,2}, ytick={4,8,12,16}]
  \addplot[courbe, domain=-3.4:2.55] {x^2+2*x+4};
  \guides{2}{12}
  \pnt[otGreenDark]{2}{12}
  \node[note,anchor=west,text=otGreenDark] at (axis cs:2.12,11.2) {$\tilde f(2)=12$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-2.75,9.3) {$y=\tilde f(x)$};
\end{axis}
\end{tikzpicture}""",

"ex872_sin2x": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=3.4cm, xmin=-7.2, xmax=7.6, ymin=-0.75, ymax=2.45,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$}, ytick={1,2}]
  \addplot[courbe, domain=-7:-0.02, samples=300] {sin(2*x)/x};
  \addplot[courbe, domain=0.02:7, samples=300] {sin(2*x)/x};
  \pnt[otGreenDark]{0}{2}
  \node[note,anchor=south west,text=otGreenDark] at (axis cs:0.25,2.02) {$\tilde g(0)=2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.5,0.55) {$y=\dfrac{\sin(2x)}{x}$};
\end{axis}
\end{tikzpicture}""",

"ex872_ln": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4cm, xmin=-1.5, xmax=6.4, ymin=-0.35, ymax=3.3,
  xtick={-1,1,2,3,4,5,6}, ytick={1,2,3}, yticklabels={,$2$,$3$}]
  \addplot[courbe, domain=-0.93:-0.01, samples=200] {ln(1+x)/x};
  \addplot[courbe, domain=0.01:6.1, samples=200] {ln(1+x)/x};
  \draw[asymptote] (axis cs:-1,0) -- (axis cs:-1,3.25);
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=south west,text=otGreenDark] at (axis cs:0.12,1.08) {$\tilde h(0)=1$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.6,0.65) {$y=\dfrac{\ln(1+x)}{x}$};
\end{axis}
\end{tikzpicture}""",

"ex872_exp": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4cm, xmin=-4.4, xmax=2.6, ymin=-0.35, ymax=4.1,
  xtick={-4,-3,-2,-1,1,2}, ytick={1,2,3,4}]
  \addplot[courbe, domain=-4.2:-0.01, samples=200] {(exp(x)-1)/x};
  \addplot[courbe, domain=0.01:2.2, samples=200] {(exp(x)-1)/x};
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:0.1,0.92) {$\tilde k(0)=1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-1.0,1.3) {$y=\dfrac{e^x-1}{x}$};
\end{axis}
\end{tikzpicture}""",

"ex872_racine": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.6cm, xmin=-1.5, xmax=6.5, ymin=-0.12, ymax=1.25,
  xtick={-1,1,2,3,4,5,6}, ytick={1}]
  \addplot[courbe, domain=-1:-0.01, samples=200] {(sqrt(x+1)-1)/x};
  \addplot[courbe, domain=0.01:6.2, samples=200] {(sqrt(x+1)-1)/x};
  \pnt{-1}{1}
  \pnt[otGreenDark]{0}{0.5}
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:0.15,0.53) {$\tilde m(0)=\dfrac{1}{2}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.2,0.38) {$y=\dfrac{\sqrt{x+1}-1}{x}$};
\end{axis}
\end{tikzpicture}""",

# ================================================================ exercice 869
"ex869_cubique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6cm, height=4.8cm, xmin=-0.45, xmax=2.5, ymin=-1.7, ymax=5.4,
  xtick={1,2}, xticklabels={}, ytick={-1,1,3}]
  \addplot[courbe, domain=0:2.2] {x^3-3*x+1};
  \guides{1}{-1} \guides{2}{3}
  \pnt{0}{1} \pnt{1}{-1} \pnt{2}{3}
  \pnt[otGreenDark]{0.3473}{0} \pnt[otGreenDark]{1.5321}{0}
  \node[note,anchor=north east,text=otGreenDark] at (axis cs:0.33,-0.05) {$c_1$};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:1.56,-0.05) {$c_2$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.75,3.3) {$y=x^3-3x+1$};
\end{axis}
\end{tikzpicture}""",

"ex869_exp_2x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.6cm, xmin=-0.75, xmax=1.85, ymin=-1.3, ymax=5.4,
  xtick={0.5,1,1.5}, ytick={1,2,3,4,5}]
  \addplot[courbe2, domain=-0.6:1.65] {2*x};
  \addplot[courbe, domain=-0.6:1.65] {exp(x)};
  \draw[otOrange,line width=0.9pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] (axis cs:0.6931,1.42) -- (axis cs:0.6931,1.96);
  \node[note,anchor=north west,align=left,text=otOrange!75!black,fill=none] at (axis cs:0.78,1.3) {écart minimal\\$\approx 0{,}61$ en $\ln 2$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:0.95,2.9) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.3,2.35) {$y=2x$};
\end{axis}
\end{tikzpicture}""",

"ex869_ln": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-0.35, xmax=3.6, ymin=-1.8, ymax=2.5,
  xtick={1,2,3}, xticklabels={}, ytick={-1,1,2}]
  \addplot[courbe, domain=0.17:3.4, samples=200] {ln(x)};
  \addplot[courbe2, domain=0:3.4] {2-x};
  \guidev{1.5571}{0.4429}
  \pnt[otRed]{1.5571}{0.4429}
  \node[note,anchor=north,text=otRed!85!black] at (axis cs:1.5571,-0.05) {$\alpha$};
  \node[anchor=south east,text=otNavy,inner sep=1.5pt] at (axis cs:3.3,1.3) {$y=\ln x$};
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:0.25,1.9) {$y=2-x$};
\end{axis}
\end{tikzpicture}""",

"ex869_cos": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=6cm, height=4.4cm, xmin=-0.25, xmax=1.95, ymin=-0.3, ymax=1.75,
  xtick={1.5708}, xticklabels={$\frac{\pi}{2}$}, ytick={1}]
  \addplot[courbe2, domain=0:1.7] {x};
  \addplot[courbe, domain=0:1.5708] {cos(x)};
  \guidev{0.7391}{0.7391}
  \pnt[otRed]{0.7391}{0.7391}
  \node[note,anchor=north,text=otRed!85!black] at (axis cs:0.7391,-0.04) {$c\approx 0{,}739$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.12,1.08) {$y=\cos x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.38,1.25) {$y=x$};
\end{axis}
\end{tikzpicture}""",

"ex869_double": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.4cm, xmin=-2.5, xmax=2.6, ymin=-0.9, ymax=10.2,
  xtick={-2,-1,1,2}, ytick={3,6,9}]
  \addplot[courbe, domain=-2.04:2.04] {(x^2-1)^2};
  \guides{2}{9} \guides{-2}{9}
  \pnt{-2}{9} \pnt{2}{9}
  \pnt[otGreenDark]{-1}{0} \pnt[otGreenDark]{1}{0}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.12,6.3) {$y=(x^2-1)^2$};
\end{axis}
\end{tikzpicture}""",

# ================================================================ exercice 871
"ex871_heron": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=5.4cm, xmin=-0.12, xmax=2.45, ymin=-0.12, ymax=2.45,
  xtick={1,1.5}, xticklabels={}, ytick={1,2}]
  \addplot[otMuted,line width=0.8pt, domain=0:2.35] {x};
  \addplot[courbe, domain=0.52:2.35, samples=200] {(x+2/x)/2};
  \draw[otGreenDark,line width=1.1pt,line join=round] (axis cs:1,0) -- (axis cs:1,1.5) -- (axis cs:1.5,1.5)
    -- (axis cs:1.5,1.41667) -- (axis cs:1.41667,1.41667) -- (axis cs:1.41667,1.41422);
  \draw[guide] (axis cs:1.5,1.5) -- (axis cs:1.5,0);
  \pnt[otGreenDark]{1}{0}
  \pnt[otGreenDark]{1.41421}{1.41421}
  \node[anchor=north,yshift=-2pt] at (axis cs:1,0) {$u_0$};
  \node[anchor=north,yshift=-2pt] at (axis cs:1.5,0) {$u_1$};
  \node[anchor=north west,text=otGreenDark,inner sep=1.5pt] at (axis cs:1.57,1.3) {$\ell=\sqrt{2}$};
  \node[anchor=south west,text=otMuted,inner sep=1.5pt] at (axis cs:2.35,2.35) {$y=x$};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:2.37,1.62) {$y=h(x)$};
\end{axis}
\end{tikzpicture}""",

"ex871_dicho": r"""
\begin{tikzpicture}[x=4.5cm,y=0.6cm]
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 3pt off 2pt] (0.14619,0.75) -- (0.14619,-7.45);
  \node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (0.14619,0.75) {$\beta$};
  \node[anchor=south,font=\otRegular\fontsize{9}{11}\selectfont,text=otNavy] at (-0.36,0.55) {étape};
  \foreach \r/\a/\b/\la/\lb in {0/0/1/1/2, 1/0/0.5/1/1{,}5, 2/0/0.25/1/1{,}25, 3/0.125/0.25/1{,}125/1{,}25,
      4/0.125/0.1875/1{,}125/1{,}1875, 5/0.125/0.15625/1{,}125/1{,}15625, 6/0.140625/0.15625/1{,}140625/1{,}15625,
      7/0.140625/0.1484375/1{,}140625/1{,}1484375}{
    \node[anchor=center,font=\otRegular\fontsize{10}{12}\selectfont,text=otNavy] at (-0.36,-\r) {\r};
    \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=east] at (\a-0.012,-\r) {$\la$};
    \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=west] at (\b+0.012,-\r) {$\lb$};
  }
  \foreach \r/\a/\b in {0/0/1, 1/0/0.5, 2/0/0.25, 3/0.125/0.25, 4/0.125/0.1875, 5/0.125/0.15625, 6/0.140625/0.15625}{
    \draw[otNavy,line width=3.2pt,line cap=butt] (\a,-\r) -- (\b,-\r);}
  \draw[otGreen,line width=3.2pt,line cap=butt] (0.140625,-7) -- (0.1484375,-7);
  \foreach \r/\m in {0/0.5, 1/0.25, 2/0.125, 3/0.1875, 4/0.15625, 5/0.140625, 6/0.1484375}{
    \draw[otOrange,line width=1.3pt] (\m,-\r+0.3) -- (\m,-\r-0.3);}
  \node[note,font=\fontsize{10.5}{12}\selectfont,anchor=south,text=otOrange!75!black,fill=none] at (0.5,0.3) {$m$};
\end{tikzpicture}""",

"ex871_quintique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=4.8cm, xmin=-2.05, xmax=2.05, ymin=-5.3, ymax=6.6,
  xtick={-1,1}, xticklabels={}, ytick={-3,5}]
  \addplot[courbe, domain=-1.7:1.62] {x*x*x*x*x-5*x+1};
  \guides{-1}{5} \guides{1}{-3}
  \pnt{-1}{5} \pnt{1}{-3}
  \pnt[otGreenDark]{-1.5417}{0} \pnt[otGreenDark]{0.2001}{0} \pnt[otGreenDark]{1.4405}{0}
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:-1.5,-0.1) {$\alpha_1$};
  \node[note,anchor=south west,text=otGreenDark] at (axis cs:0.25,0.12) {$\alpha_2$};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:1.47,-0.1) {$\alpha_3$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.15,-3.7) {$y=x^5-5x+1$};
\end{axis}
\end{tikzpicture}""",

"ex871_raccord_ab": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.8cm, xmin=-1.9, xmax=2.6, ymin=-3.9, ymax=5.6,
  xtick={-1,1,2}, ytick={2,4}]
  \addplot[courbe2, domain=-1.45:1] {2*x-1};
  \addplot[otOrange, line width=1.35pt, domain=-1.75:1] {1};
  \addplot[courbe, domain=1:2.33] {x^2};
  \guidev{1}{1}
  \pnt{1}{1}
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.85,4.0) {$y=x^2$};
  \node[note,text=otGreenDark,anchor=south east] at (axis cs:-1.5,-3.6) {$a=2$, $b=-1$};
  \node[note,text=otOrange!75!black,anchor=south west] at (axis cs:-1.8,1.1) {$a=0$, $b=1$};
  \node[note,anchor=north west] at (axis cs:1.1,0.85) {$(1\,;1)$};
\end{axis}
\end{tikzpicture}""",

"ex871_exp_droite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-3.4, xmax=2.2, ymin=-1.1, ymax=5.4,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={1,2,3,4,5}]
  \addplot[courbe2, domain=-3.2:2] {x+2};
  \addplot[courbe, domain=-3.2:1.65] {exp(x)};
  \guidev{-1.8414}{0.1586} \guidev{1.1462}{3.1462}
  \pnt[otRed]{-1.8414}{0.1586} \pnt[otRed]{1.1462}{3.1462}
  \node[note,anchor=north west,text=otRed!85!black] at (axis cs:-1.8,-0.05) {$\alpha$};
  \node[note,anchor=north west,text=otRed!85!black] at (axis cs:1.17,-0.05) {$\beta$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.05,4.0) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.3,3.0) {$y=x+2$};
\end{axis}
\end{tikzpicture}""",
}

P2 = r"\frac{\pi}{2}"
XLAB = {
    "cours_point_fixe": [(1, "c", "1"), (2, "d", "2")],
    "ex868_sinx": [(-6.2832, "g", r"-2\pi"), (-3.1416, "d", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "ex872_sin2x": [(-6.2832, "g", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "d", r"\pi"), (6.2832, "d", r"2\pi")],
    "ex869_cos": [(1.5708, "c", P2)],
    "ex869_cubique": [(1, "h", "1"), (2, "c", "2")],
    "ex869_ln": [(1, "d", "1"), (2, "c", "2"), (3, "c", "3")],
    "ex870_inverse": [(-2, "h", "-2"), (-1, "h", "-1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4")],
    "ex870_saut2": [(-2, "c", "-2"), (-1, "d", "-1"), (1, "d", "1"), (2, "c", "2")],
    "ex871_quintique": [(-1, "c", "-1"), (1, "h", "1")],
    "ex871_exp_droite": [(-3, "c", "-3"), (-1, "c", "-1"), (1, "c", "1"), (2, "c", "2")],
}
