# -*- coding: utf-8 -*-
"""Figures de la notion « Limites des fonctions » (Terminale), style des livres.

Compilation : python ../../../outils/figures_livre.py <dossier_notion>
"""

ASY = r"\draw[asymptote]"

FIGURES = {
# ------------------------------------------------------------------ cours
"cours_asymptotes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.4cm, xmin=-4.7, xmax=6.9, ymin=-4.7, ymax=8.7,
  xtick={-4,-2,2,4,6}, ytick={-4,-2,4,6,8}]
  \draw[asymptote] (axis cs:1,-4.7) -- (axis cs:1,8.7);
  \draw[asymptote] (axis cs:-4.7,2) -- (axis cs:6.9,2);
  \addplot[courbe, domain=-4.5:0.53125] {2+3/(x-1)};
  \addplot[courbe, domain=1.46875:6.7] {2+3/(x-1)};
  \node[note,anchor=north west] at (axis cs:1.15,-2.4) {asymptote $x=1$};
  \node[note,anchor=north east] at (axis cs:6.8,1.7) {asymptote $y=2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.6,5.0) {$y=\dfrac{2x+1}{x-1}$};
\end{axis}
\end{tikzpicture}""",

"cours_gendarmes": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=4.4cm, xmin=-0.6, xmax=20.2, ymin=-1, ymax=1.2,
  xtick={6.2832,12.566,18.85}, xticklabels={}, ytick={-0.5,0.5,1}]
  % la courbe passe des deux côtés de l'axe : graduations de x reportées sous le graphique
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:6.2832,-1) {$2\pi$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:12.566,-1) {$4\pi$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:18.85,-1) {$6\pi$};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1.1:19.8] {1/x};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1.1:19.8] {-1/x};
  \addplot[courbe, domain=0.05:19.8] {sin(x)/x};
  \node[anchor=south west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.6,0.45) {$y=\dfrac{1}{x}$};
  \node[anchor=north west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:3.2,-0.42) {$y=-\dfrac{1}{x}$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:11.5,0.3) {$y=\dfrac{\sin x}{x}$};
\end{axis}
\end{tikzpicture}""",

"cours_croissances": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.8cm, xmin=-0.3, xmax=6.3, ymin=-12, ymax=225,
  xtick={1,2,3,4,5}, ytick={50,100,150,200}]
  \addplot[otMuted, line width=1.1pt, domain=0:5.8] {x^2};
  \addplot[courbe2, domain=0:5.6] {x^3};
  \addplot[courbe, domain=0:5.347] {exp(x)};
  \draw[guide] (axis cs:4.5364,0) -- (axis cs:4.5364,93.354);
  \pnt[otOrange]{4.5364}{93.354}
  \node[note,anchor=south west] at (axis cs:4.66,45) {$x\approx 4{,}54$};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:5.15,205) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:5.66,175.6) {$y=x^3$};
  \node[etiq,text=otMuted,anchor=west] at (axis cs:5.86,33.6) {$y=x^2$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- exercice 867 « Asymptotes »
"asym_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.6cm, xmin=-5.6, xmax=9.6, ymin=-7.2, ymax=15.4,
  xtick={-4,2,4,6,8}, xticklabels={$-4$,$2$,$4$,$6$,$8$}, ytick={-5,5,10}]
  \draw[asymptote] (axis cs:2,-7.2) -- (axis cs:2,15.2);
  \draw[asymptote] (axis cs:-5.6,-3.6) -- (axis cs:9.6,11.6);
  \addplot[courbe, domain=-5.4:1.7147] {x+2+3/(x-2)};
  \addplot[courbe, domain=2.2853:9.4] {x+2+3/(x-2)};
  \node[note,anchor=north east] at (axis cs:1.8,15) {$x=2$};
  \node[note,anchor=north east] at (axis cs:9.5,8.2) {$y=x+2$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:3.2,13) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"asym_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.2cm, xmin=-11.2, xmax=6.2, ymin=-7.2, ymax=11.2,
  xtick={-10,-8,-6,-4,-2,2,4}, ytick={-5,5,10}]
  \draw[asymptote] (axis cs:-3,-7.2) -- (axis cs:-3,11.2);
  \draw[asymptote] (axis cs:-11.2,2) -- (axis cs:6.2,2);
  \addplot[courbe, domain=-11:-3.5682] {2-5/(x+3)};
  \addplot[courbe, domain=-2.4318:6] {2-5/(x+3)};
  \node[note,anchor=south east] at (axis cs:-3.15,-7.0) {$x=-3$};
  \node[note,anchor=south east] at (axis cs:6.1,2.3) {$y=2$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-7,4.6) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}""",

"asym_h": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.6cm, xmin=-5.7, xmax=6.7, ymin=-7.2, ymax=9.2,
  xtick={-4,-2,2,4,6}, ytick={-6,-4,4,6,8}]
  \draw[asymptote] (axis cs:1,-7.2) -- (axis cs:1,9.2);
  \draw[asymptote] (axis cs:-5.7,-5.7) -- (axis cs:6.7,6.7);
  \addplot[courbe, domain=-5.5:0.8696] {x+1/(x-1)};
  \addplot[courbe, domain=1.1304:6.5] {x+1/(x-1)};
  \pntv[otGreenDark]{-1}{-1.5}
  \node[note,anchor=south west] at (axis cs:1.15,-7.0) {$x=1$};
  \node[note,anchor=north west] at (axis cs:4.4,3.4) {$y=x$};
  \node[note,anchor=north east,text=otGreenDark] at (axis cs:-1.6,-5.4) {point exclu};
  \draw[otGreenDark,line width=0.5pt,-{Stealth[length=1.6mm]}] (axis cs:-2.0,-5.35) -- (axis cs:-1.12,-1.82);
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.3,7.6) {$\mathcal{C}_h$};
\end{axis}
\end{tikzpicture}""",

"asym_k": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.4cm, xmin=-6.7, xmax=5.7, ymin=-7.2, ymax=8.2,
  xtick={-6,-4,2,4}, ytick={2,4,6}]
  \draw[asymptote] (axis cs:-1,-7.2) -- (axis cs:-1,8.2);
  \draw[asymptote] (axis cs:-6.7,-5.7) -- (axis cs:5.7,6.7);
  \addplot[courbe, domain=-6.5:-1.1262] {x+1-1/(x+1)};
  \addplot[courbe, domain=-0.856:5.5] {x+1-1/(x+1)};
  \node[note,anchor=south east] at (axis cs:-1.15,-7.0) {$x=-1$};
  \node[note,anchor=south east] at (axis cs:5.5,7.0) {$y=x+1$};
  \node[etiq,text=otNavy,anchor=center] at (axis cs:-3.2,3.6) {$\mathcal{C}_k$};
\end{axis}
\end{tikzpicture}""",

"asym_m": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.8cm, xmin=-8.6, xmax=8.6, ymin=-4.9, ymax=2.3,
  xtick={-8,-6,-4,-2,2,4,6,8}, xticklabels={}, ytick={-4,-3,-2,-1,1}, yticklabels={}]
  \draw[asymptote] (axis cs:-8.6,1) -- (axis cs:8.6,1);
  \addplot[courbe, domain=-8.4:8.4, samples=300] {1-5/(x^2+1)};
  \pnt{0}{-4}
  \node[note,anchor=north west] at (axis cs:0.25,-4.15) {minimum $-4$};
  \node[note,anchor=south east] at (axis cs:8.5,1.15) {$y=1$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.5,-2.8) {$\mathcal{C}_m$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- exercice 1197 « DS »
"ds_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.4cm, xmin=-5.7, xmax=7.7, ymin=-6.2, ymax=12.2,
  xtick={-4,-2,2,4,6}, ytick={-5,5,10}]
  \draw[asymptote] (axis cs:1,-6.2) -- (axis cs:1,12.2);
  \draw[asymptote] (axis cs:-5.7,3) -- (axis cs:7.7,3);
  \addplot[courbe, domain=-5.5:0.4318] {3+5/(x-1)};
  \addplot[courbe, domain=1.5682:7.5] {3+5/(x-1)};
  \node[note,anchor=south west] at (axis cs:1.15,-6.0) {$x=1$};
  \node[note,anchor=north east] at (axis cs:7.6,2.7) {$y=3$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.7,8.5) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"ds_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=5.6cm, xmin=-9.6, xmax=5.6, ymin=-15.4, ymax=7.2,
  xtick={-8,-6,-4,2,4}, xticklabels={$-8$,$-6$,$-4$,$2$,$4$}, ytick={-10,-5,5}]
  \draw[asymptote] (axis cs:-2,-15.4) -- (axis cs:-2,7.2);
  \draw[asymptote] (axis cs:-9.6,-11.6) -- (axis cs:5.6,3.6);
  \addplot[courbe, domain=-9.4:-2.2853] {x-2+3/(x+2)};
  \addplot[courbe, domain=-1.7147:5.4] {x-2+3/(x+2)};
  \node[note,anchor=north east] at (axis cs:-2.15,7.0) {$x=-2$};
  \node[note,anchor=south east] at (axis cs:-6.0,-7.4) {$y=x-2$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.0,5.4) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- exercice 1195 « gauche / droite »
"abs_sur_x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=3.2cm, xmin=-3.6, xmax=3.6, ymin=-1.8, ymax=1.8,
  xtick={-3,-2,-1,1,2,3}, ytick={-1,1}, yticklabels={}]
  \draw[courbe] (axis cs:-3.4,-1) -- (axis cs:-0.07,-1);
  \draw[courbe] (axis cs:0.07,1) -- (axis cs:3.4,1);
  \pntv{0}{1} \pntv{0}{-1}
  \node[anchor=east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt] at (axis cs:-0.2,1) {$1$};
  \node[anchor=west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt] at (axis cs:0.2,-1) {$-1$};
  \node[note,anchor=south,text=otGreenDark] at (axis cs:1.9,1.15) {limite à droite : $1$};
  \node[note,anchor=north,text=otGreenDark] at (axis cs:-1.9,-1.15) {limite à gauche : $-1$};
  \node[etiq,text=otNavy,anchor=center] at (axis cs:-2.1,0.85) {$y=\dfrac{|x|}{x}$};
\end{axis}
\end{tikzpicture}""",

# --------------------------------------------- exercice 1191 « gendarmes »
"gend_x2sin": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.2cm, height=4.4cm, xmin=-0.37, xmax=0.37, ymin=-0.142, ymax=0.142,
  xtick=\empty, ytick=\empty]
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=-0.36:0.36, samples=100] {x^2};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=-0.36:0.36, samples=100] {-x^2};
  \addplot[courbe, line width=1pt, domain=0.003:0.36, samples=1500] {x^2*sin(1/x)};
  \addplot[courbe, line width=1pt, domain=-0.36:-0.003, samples=1500] {x^2*sin(1/x)};
  \node[anchor=south west,inner sep=1.5pt,text=otOrange!70!black] at (axis cs:-0.25,0.074) {$y=x^2$};
  \node[anchor=north west,inner sep=1.5pt,text=otOrange!70!black] at (axis cs:-0.25,-0.074) {$y=-x^2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.03,0.075) {$y=x^2\sin\!\left(\dfrac{1}{x}\right)$};
\end{axis}
\end{tikzpicture}""",

"conj_sqrt": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=3.2cm, xmin=-0.5, xmax=10.6, ymin=-0.12, ymax=0.72,
  xtick={2,4,6,8,10}, ytick={0.5}, yticklabels={$\dfrac12$}]
  \draw[asymptote] (axis cs:0,0.5) -- (axis cs:10.5,0.5);
  \addplot[courbe, domain=0:10.4, samples=400] {sqrt(x^2+x)-x};
  \node[anchor=south east,text=otMuted,inner sep=1.5pt] at (axis cs:10.4,0.53) {asymptote $y=\dfrac{1}{2}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3,0.4) {$y=\sqrt{x^2+x}-x$};
\end{axis}
\end{tikzpicture}""",
}

XLAB = {
    "asym_f": [(-4, "c", "-4"), (2, "d", "2"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8")],
    "asym_m": [(-8, "c", "-8"), (-6, "c", "-6"), (-4, "c", "-4"), (-2, "g", "-2"),
               (2, "d", "2"), (4, "c", "4"), (6, "c", "6"), (8, "c", "8")],
    "ds_g": [(-8, "c", "-8"), (-6, "c", "-6"), (-4, "c", "-4"), (2, "d", "2"), (4, "c", "4")],
    "tangente_sin_pi": [(1.5708, "c", r"\frac{\pi}{2}"), (3.1416, "g", r"\pi"), (4.7124, "c", r"\frac{3\pi}{2}"),
                        (6.2832, "d", r"2\pi")],
    # la branche gauche passe sous l'axe : graduations négatives au-dessus
    "asym_1moinsx": [(-4, "h", "-4"), (-2, "h", "-2"), (2, "c", "2"), (4, "c", "4"), (6, "c", "6")],
}

# =================================================================== finition 2026-11-02
# Figures ajoutées dans les corrigés (éléments de réponse en vert).
FIGURES.update({
# 1188 Q5 : e^x tend vers 0 en -infini, l'axe des abscisses est asymptote
"exp_asym": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4cm, xmin=-5.4, xmax=2.4, ymin=-1, ymax=5.3,
  xtick={1}, ytick={1,2,3,4}]
  \draw[otGreenDark,line width=2pt,line cap=butt,opacity=0.85] (axis cs:-5.3,0) -- (axis cs:-0.3,0);
  \addplot[courbe, domain=-5.2:1.6] {exp(x)};
  \pnt{0}{1}
  \node[anchor=north west,text=otGreenDark,font=\otRegular\fontsize{9}{11}\selectfont,inner sep=1.5pt] at (axis cs:-5.3,-0.15)
    {asymptote $y=0$ en $-\infty$};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:1.6,3.2) {$y=e^x$};
\end{axis}
\end{tikzpicture}""",

# 1189 Q1 : 1/x + 3 et son asymptote horizontale y = 3
"inv_plus3": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4cm, xmin=-0.6, xmax=10.8, ymin=-0.6, ymax=8.2,
  xtick={2,4,6,8,10}, ytick={1,2,3,4,5,6,7}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,3) -- (axis cs:10.6,3);
  \addplot[courbe, domain=0.2:10.4, samples=200] {1/x+3};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (axis cs:10.6,2.8) {asymptote $y=3$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:1.6,5.3) {$y=\dfrac{1}{x}+3$};
\end{axis}
\end{tikzpicture}""",

# 1190 Q1 : (x^2 - 1)/(x - 1) : la droite y = x + 1 privée du point (1 ; 2)
"trou_x1": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=4.2cm, xmin=-1.6, xmax=3.6, ymin=-0.8, ymax=4.6,
  xtick={1,2,3}, ytick={1,2,3,4}]
  \addplot[courbe, domain=-1.5:0.93] {x+1};
  \addplot[courbe, domain=1.07:3.4] {x+1};
  \draw[guide,otGreenDark] (axis cs:1,0) -- (axis cs:1,2) -- (axis cs:0,2);
  \pntv{1}{2}
  \node[anchor=south east,text=otGreenDark,font=\otRegular\fontsize{9}{11}\selectfont,inner sep=1.5pt] at (axis cs:0.85,2.35)
    {limite $2$ en $1$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:1.9,2.6) {$y=\dfrac{x^2-1}{x-1}$};
\end{axis}
\end{tikzpicture}""",

# 1192 Q4 : la limite de sin x/(x - pi) en pi est la pente -1 de la tangente en (pi ; 0)
"tangente_sin_pi": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.2cm, height=4.4cm, xmin=-0.3, xmax=7.1, ymin=-1.8, ymax=1.75,
  xtick={1.5708,3.1416,4.7124,6.2832}, xticklabels={}, ytick={-1,1}]
  \addplot[courbe, domain=0:6.6, samples=200] {sin(x)};
  \addplot[courbe2, domain=1.55:4.74] {3.14159-x};
  \pnt[otGreenDark]{3.14159}{0}
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:0.3,-1.15) {$y=\sin x$};
  \node[anchor=north west,align=left,text=otGreenDark,inner sep=1.5pt] at (axis cs:4.9,-1.12)
    {tangente en $\pi$\\pente $-1$};
\end{axis}
\end{tikzpicture}""",

# 1193 Q4 : ln x / x tend vers 0 en +infini (maximum 1/e en e)
"lnx_sur_x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=4cm, xmin=-0.8, xmax=26, ymin=-0.62, ymax=0.56,
  xtick={5,10,15,20,25}, ytick={-0.4,-0.2,0.2,0.4}]
  \addplot[courbe, domain=0.62:25, samples=300] {ln(x)/x};
  \pnt{2.71828}{0.36788}
  \node[anchor=south west,font=\otRegular\fontsize{9}{11}\selectfont,text=otMuted,inner sep=1.5pt] at (axis cs:3.2,0.38)
    {maximum $\dfrac{1}{e}$ en $x=e$};
  \node[anchor=north east,text=otGreenDark,font=\otRegular\fontsize{9}{11}\selectfont,inner sep=1.5pt] at (axis cs:25,-0.2)
    {$\dfrac{\ln x}{x}\to 0$ en $+\infty$ : asymptote $y=0$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:17,0.19) {$y=\dfrac{\ln x}{x}$};
\end{axis}
\end{tikzpicture}""",

# 1196 Q1 : x + sin x reste au-dessus de la droite y = x - 1
"x_plus_sin": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=4.6cm, xmin=-0.6, xmax=13.6, ymin=-1.6, ymax=14.6,
  xtick={5,10}, ytick={5,10}]
  \addplot[otNavy!40,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=0:13] {x+1};
  \addplot[courbe2, domain=0.4:13] {x-1};
  \addplot[courbe, domain=0:13, samples=300] {x+sin(x)};
  \node[anchor=south east,text=otMuted,inner sep=1.5pt] at (axis cs:11.4,12.6) {$y=x+1$};
  \node[anchor=north west,text=otGreenDark,inner sep=1.5pt] at (axis cs:9.6,7.9) {minorante $y=x-1$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:0.6,8.5) {$y=x+\sin x$};
\end{axis}
\end{tikzpicture}""",

# 1195 Q5 : g(x) = (2x + 1)/(1 - x), asymptote verticale x = 1
"asym_1moinsx": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5cm, xmin=-5.6, xmax=6.6, ymin=-12.5, ymax=8.6,
  xtick={-4,-2,2,4,6}, xticklabels={}, ytick={-10,-5,5}]
  \draw[asymptote] (axis cs:1,-12.5) -- (axis cs:1,8.6);
  \draw[asymptote] (axis cs:-5.6,-2) -- (axis cs:6.6,-2);
  \addplot[courbe, domain=-5.4:0.7, samples=200] {(2*x+1)/(1-x)};
  \addplot[courbe, domain=1.26:6.4, samples=200] {(2*x+1)/(1-x)};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (axis cs:-0.35,8.4) {$x\to1^-$ : $+\infty$};
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:1.75,-12.3) {$x\to1^+$ : $-\infty$};
  \node[note,anchor=south west] at (axis cs:1.15,4.6) {$x=1$};
  \node[note,anchor=north west] at (axis cs:-5.5,-2.35) {$y=-2$};
\end{axis}
\end{tikzpicture}""",

# 1197 C1 : (2x + sin x)/(x + 1) entre (2x - 1)/(x + 1) et (2x + 1)/(x + 1)
"ds_gend_x": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=4.4cm, xmin=-0.8, xmax=31, ymin=-1.15, ymax=2.5,
  xtick={5,10,15,20,25,30}, ytick={-1,1,2}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,2) -- (axis cs:30.5,2);
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=0:30] {(2*x+1)/(x+1)};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=0:30] {(2*x-1)/(x+1)};
  \addplot[courbe, domain=0:30, samples=300] {(2*x+sin(x))/(x+1)};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:30.5,2.05) {asymptote $y=2$};
  \node[anchor=north east,align=right,inner sep=1.5pt] at (axis cs:30.5,1.6)
    {\textcolor{otOrange!80!black}{gendarmes : $\dfrac{2x-1}{x+1}$ et $\dfrac{2x+1}{x+1}$}\\[2pt]
     \textcolor{otNavy}{$y=\dfrac{2x+\sin x}{x+1}$}};
\end{axis}
\end{tikzpicture}""",
})
