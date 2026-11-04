# -*- coding: utf-8 -*-
"""Figures de la notion « Primitives » (Terminale), style des livres OptiTAB.

    python ../../../outils/figures_livre.py <ce dossier de notion>

- famille : primitives F(x) = x^2 + C de f(x) = 2x ; celle qui passe par (1 ; 3)
  (cours II et fiche I) ;
- lien : f(x) = x^2 - 1 et sa primitive F(x) = x^3/3 - x, signe de f et
  variations de F (cours VI et fiche IV) ;
- ex_famille_cubique : primitives x^3 + 2x + C de 3x^2 + 2, celle qui passe
  par (0 ; 3) en vert (corrigé de l'exercice 1221, question 1).
"""


def parabole(c, style):
    """Courbe y = x^2 + c, coupée à y = 6,2 (haut de la fenêtre)."""
    r = (6.2 - c) ** 0.5
    return rf"  \addplot[{style}, domain={-r:.4f}:{r:.4f}] {{x^2+({c})}};" + "\n"


FAMILLE_PALES = "".join(parabole(c, "pale") for c in (-2, -1, 0, 1, 3, 4))


def cubique(c, style, bas=-3.2, haut=7.2):
    """Courbe y = x^3 + 2x + c (croissante), restreinte à bas <= y <= haut."""
    def racine(cible):
        a, b = -5.0, 5.0
        for _ in range(60):
            m = (a + b) / 2
            if m ** 3 + 2 * m + c < cible:
                a = m
            else:
                b = m
        return (a + b) / 2
    return rf"  \addplot[{style}, domain={racine(bas):.4f}:{racine(haut):.4f}] {{x^3+2*x+({c})}};" + "\n"


CUBIQUES_PALES = "".join(cubique(c, "pale") for c in (-1, 1, 5))

# graduation de l'axe des abscisses placée à la main : \gradx{valeur}{ancre}
PREAMBULE_EXTRA = r"""
\newcommand{\gradx}[2]{\node[anchor=#2,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,
  inner sep=1.3pt,yshift=-2pt] at (axis cs:#1,0) {$#1$};}
\tikzset{signe/.style={font=\Large\bfseries,inner sep=1pt}}
"""

LIEN = r"""
\begin{tikzpicture}
% panneau du haut : f(x) = x^2 - 1, signe de f
\begin{axis}[otWeb, name=haut, width=7.4cm, height=3.1cm, xmin=-2.45, xmax=2.6, ymin=-1.45, ymax=3.75,
  axis y line=none, xtick={-2,-1,1,2}, xticklabels={}, ytick=\empty, ylabel={}, grid=none]
  \addplot[draw=none, fill=otGreen!22, domain=-2.1:-1] {x^2-1} \closedcycle;
  \addplot[draw=none, fill=otOrange!28, domain=-1:1] {x^2-1} \closedcycle;
  \addplot[draw=none, fill=otGreen!22, domain=1:2.1] {x^2-1} \closedcycle;
  \addplot[otGreenDark, line width=1.35pt, domain=-2.1:2.1] {x^2-1};
  \node[signe,text=otGreenDark] at (axis cs:-1.62,0.6) {$+$};
  \node[signe,text=otGreenDark] at (axis cs:1.62,0.6) {$+$};
  \node[signe,text=otOrange!75!black] at (axis cs:0,-0.48) {$-$};
  \gradx{-2}{north} \gradx{-1}{north east} \gradx{1}{north west} \gradx{2}{north}
  \coordinate (h1) at (axis cs:-1,3.6);
  \coordinate (h2) at (axis cs:1,3.6);
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:0,1.75) {$y=f(x)=x^2-1$};
\end{axis}
% panneau du bas : F(x) = x^3/3 - x, variations de F
\begin{axis}[otWeb, at={(haut.south)}, anchor=north, yshift=-0.55cm, width=7.4cm, height=3.1cm,
  xmin=-2.45, xmax=2.6, ymin=-1.3, ymax=1.75,
  axis y line=none, xtick={-2,-1,1,2}, xticklabels={}, ytick=\empty, ylabel={}, grid=none]
  \addplot[courbe, domain=-2.1:-1] {x^3/3-x};
  \addplot[otOrange!85!black, line width=1.35pt, domain=-1:1] {x^3/3-x};
  \addplot[courbe, domain=1:2.1] {x^3/3-x};
  \pnt{-1}{0.6667} \pnt{1}{-0.6667}
  \gradx{-2}{north east} \gradx{-1}{north east} \gradx{1}{north west} \gradx{2}{north west}
  \coordinate (b1) at (axis cs:-1,-1.25);
  \coordinate (b2) at (axis cs:1,-1.25);
  \node[note,anchor=south east] at (axis cs:-1.06,0.72) {max $\displaystyle\frac{2}{3}$};
  \node[note,anchor=north west] at (axis cs:1.06,-0.74) {min $\displaystyle-\frac{2}{3}$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.17,0.75) {$y=F(x)$};
  \node[note,anchor=south] at (axis cs:-1.85,1.3) {croissante};
  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:0,1.3) {décroissante};
  \node[note,anchor=south] at (axis cs:1.85,1.3) {croissante};
\end{axis}
\draw[guide] (h1) -- (b1);
\draw[guide] (h2) -- (b2);
\end{tikzpicture}"""

FIGURES = {
"famille": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=6.4cm, xmin=-2.75, xmax=2.95, ymin=-2.6, ymax=6.75,
  xtick={-2,-1,1,2}, ytick={-2,-1,1,2,3,4,5,6},
  yticklabel style={anchor=north east,inner sep=1.2pt,xshift=-1.5pt,yshift=-1.5pt}]
""" + FAMILLE_PALES + parabole(2, "courbe") + r"""
  \guides{1}{3}
  \pnt[otGreenDark]{1}{3}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-2.05,6.25) {$y=x^2+2$};
  \node[note,anchor=south] at (axis cs:2.1,6.3) {$y=x^2+C$};
\end{axis}
\end{tikzpicture}""",

"lien": LIEN,

"ex_famille_cubique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=6cm, xmin=-1.75, xmax=1.95, ymin=-3.4, ymax=7.6,
  xtick={-1,1}, xticklabels={}, ytick={-2,2,4,6},
  yticklabel style={anchor=east,inner sep=1.2pt,xshift=-2pt,yshift=0pt}]
""" + CUBIQUES_PALES + cubique(3, "otGreenDark, line width=1.5pt") + r"""
  \pnt[otGreenDark]{0}{3}
  \node[anchor=south east,text=otGreenDark,font=\otRegular\bfseries\fontsize{9}{10}\selectfont,inner sep=1.2pt] at (axis cs:-0.04,3.02) {3};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:1.12,7.3) {$y=F(x)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------- 1223, question 3 : -1/2 cos(2x) + C
"ex1223_cos": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=4.6cm, xmin=-3.75, xmax=3.85, ymin=-1.0, ymax=1.45,
  xtick={-3.14159,-1.5708,1.5708,3.14159}, xticklabels={}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}]
  \addplot[otNavy!70, line width=1.2pt, domain=-3.4:3.4] {-0.5*cos(2*x)};
  \addplot[otGreenDark, line width=1.5pt, domain=-3.4:3.4] {0.5-0.5*cos(2*x)};
  \draw[-{Stealth[length=2.2mm]},otGreenDark,line width=0.9pt] (axis cs:1.5708,0.54) -- (axis cs:1.5708,0.95);
  \node[note,fill=none,text=otGreenDark,anchor=south west] at (axis cs:1.95,1.08) {$+\dfrac{1}{2}$ vers le haut};
  \fill[otNavy] (axis cs:0,-0.5) circle (2.1pt);
  \fill[otGreenDark] (axis cs:0,0) circle (2.3pt);
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:0.06,-0.55) {$-\frac{1}{2}$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south] at (axis cs:-1.5708,1.06) {$y=F(x)$};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:-3.72,-0.6) {$y=-\frac{1}{2}\cos(2x)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------- 1224, question 1 : ln(-x) sur ]-oo ; 0[
"ex1224_ln": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4cm, xmin=-4.8, xmax=4.9, ymin=-2.7, ymax=2.0,
  xtick={-4,-2,-1,1,2,4}, xticklabels={}, ytick={-2,-1,1}, yticklabels={,,$1$}]
  \addplot[pale, domain=0.075:4.5, samples=300] {ln(x)};
  \addplot[courbe, domain=-4.5:-0.075, samples=300] {ln(-x)};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:-4.55,0.92) {$y=\ln(-x)$};
  \node[etiq,fill=none,text=otMuted,anchor=north east] at (axis cs:4.55,0.92) {$y=\ln x$};
  \node[etiq,fill=none,text=otGreenDark,anchor=north west,align=left] at (axis cs:-4.55,-0.6)
    {$f(x)=\dfrac{1}{x}<0$\\ $F$ décroissante};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------- nouveau-1 : reconnaître la courbe d'une primitive
"n1_courbes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5cm, xmin=-1.6, xmax=3.9, ymin=-1.9, ymax=4.7,
  xtick={-1,1,2,3}, xticklabels={}, ytick={-1,1,2,3,4}, yticklabels={$-1$,,$2$,$3$,$4$}]
  \addplot[courbe, domain=-1.3:3.3] {x^2-2*x};
  \addplot[courbe2, domain=-1.3:3.3] {x^3/3-x^2+1};
  \node[etiq,fill=none,text=otNavy,anchor=west] at (axis cs:3.33,4.29) {$\mathcal{C}_1$};
  \node[etiq,fill=none,text=otGreenDark,anchor=west] at (axis cs:3.33,2.09) {$\mathcal{C}_2$};
  \node[anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.2pt] at (axis cs:0.03,1.03) {$1$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.2pt] at (axis cs:2,-0.42) {$2$};
\end{axis}
\end{tikzpicture}""",

"n1_lecture": r"""
\begin{tikzpicture}
% panneau du haut : C1 = courbe de f, signe de f
\begin{axis}[otWeb, name=haut, width=7cm, height=3cm, xmin=-1.45, xmax=3.6, ymin=-1.45, ymax=3.75,
  axis y line=none, xtick={-1,1,2,3}, xticklabels={}, ytick=\empty, ylabel={}, grid=none]
  \addplot[draw=none, fill=otGreen!22, domain=-1.1:0] {x^2-2*x} \closedcycle;
  \addplot[draw=none, fill=otOrange!28, domain=0:2] {x^2-2*x} \closedcycle;
  \addplot[draw=none, fill=otGreen!22, domain=2:3.1] {x^2-2*x} \closedcycle;
  \addplot[courbe, domain=-1.1:3.1] {x^2-2*x};
  \node[signe,text=otGreenDark] at (axis cs:-0.62,0.7) {$+$};
  \node[signe,text=otGreenDark] at (axis cs:2.62,0.7) {$+$};
  \node[signe,text=otOrange!75!black] at (axis cs:1,-0.62) {$-$};
  \gradx{-1}{north} \gradx{0}{north east} \gradx{2}{north west} \gradx{3}{north}
  \coordinate (h1) at (axis cs:0,3.6);
  \coordinate (h2) at (axis cs:2,3.6);
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:3.12,3.1) {$\mathcal{C}_1 = \mathcal{C}_f$};
\end{axis}
% panneau du bas : C2 = courbe de F, variations de F
\begin{axis}[otWeb, at={(haut.south)}, anchor=north, yshift=-0.55cm, width=7cm, height=3cm,
  xmin=-1.45, xmax=3.6, ymin=-0.95, ymax=1.75,
  axis y line=none, xtick={-1,1,2,3}, xticklabels={}, ytick=\empty, ylabel={}, grid=none]
  \addplot[otGreenDark, line width=1.35pt, domain=-1.1:0] {x^3/3-x^2+1};
  \addplot[otOrange!85!black, line width=1.35pt, domain=0:2] {x^3/3-x^2+1};
  \addplot[otGreenDark, line width=1.35pt, domain=2:3.1] {x^3/3-x^2+1};
  \pnt{0}{1} \pnt{2}{-0.3333}
  \gradx{1}{north} \gradx{3}{north}
  \coordinate (b1) at (axis cs:0,-0.9);
  \coordinate (b2) at (axis cs:2,-0.9);
  \node[note,anchor=south] at (axis cs:-0.75,1.3) {croissante};
  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:1,1.3) {décroissante};
  \node[note,anchor=south] at (axis cs:2.75,1.3) {croissante};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:3.12,1.1) {$\mathcal{C}_2 = \mathcal{C}_F$};
\end{axis}
\draw[guide] (h1) -- (b1);
\draw[guide] (h2) -- (b2);
\end{tikzpicture}""",

"n1_famille": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5.2cm, xmin=-1.6, xmax=3.95, ymin=-1.9, ymax=4.6,
  xtick={-1,1,2,3}, xticklabels={}, ytick={-1,1,2,3,4}, yticklabels={$-1$,,,$3$,$4$}]
  \addplot[pale, domain=-1.3:3.3, restrict y to domain=-1.85:4.4] {x^3/3-x^2-1};
  \addplot[pale, domain=-1.3:3.3, restrict y to domain=-1.85:4.4] {x^3/3-x^2};
  \addplot[courbe, domain=-1.3:3.3] {x^3/3-x^2+1};
  \addplot[otGreenDark, line width=1.5pt, domain=-1.3:3.3] {x^3/3-x^2+2};
  \draw[-{Stealth[length=2.2mm]},otGreenDark,line width=0.9pt] (axis cs:1.6,-0.04) -- (axis cs:1.6,0.92);
  \node[etiq,fill=none,text=otGreenDark,anchor=west,inner sep=1pt] at (axis cs:1.64,0.47) {$+1$};
  \pnt{0}{1}
  \fill[otGreenDark] (axis cs:3,2) circle (2.3pt);
  \node[etiq,fill=none,text=otNavy,anchor=north east] at (axis cs:-0.05,0.95) {$A$};
  \node[etiq,fill=none,text=otGreenDark,anchor=south east] at (axis cs:2.95,2.05) {$B$};
  \node[etiq,fill=none,text=otNavy,anchor=west] at (axis cs:3.33,2.09) {$\mathcal{C}_F$};
  \node[etiq,fill=none,text=otGreenDark,anchor=west] at (axis cs:3.33,3.09) {$\mathcal{C}_G$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------- nouveau-2 : remplissage d'une cuve
"n2_debit": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.9cm, xmin=-1.5, xmax=44.5, ymin=-4, ymax=47,
  xtick={10,20,30,40}, ytick={10,20,30,40}, xlabel={$t$}, ylabel={$q$}]
  \addplot[courbe, domain=0:41] {40*exp(-0.1*x)};
  \pnt{0}{40}
  \node[etiq,fill=none,text=otNavy,anchor=south west] at (axis cs:12,15) {$\mathcal{C}_q$};
\end{axis}
\end{tikzpicture}""",

"n2_volume": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-1.5, xmax=44.5, ymin=-30, ymax=580,
  xtick={13.8629,20,30,40}, xticklabels={}, ytick={100,200,300,400,500}, xlabel={$t$}, ylabel={$V$}]
  \draw[asymptote] (axis cs:0,500) -- (axis cs:43,500);
  \addplot[courbe, domain=0:41] {500-400*exp(-0.1*x)};
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 3pt off 2pt] (axis cs:0,400) -- (axis cs:13.8629,400) -- (axis cs:13.8629,0);
  \pnt{0}{100}
  \fill[otGreenDark] (axis cs:13.8629,400) circle (2.3pt);
  \node[note,fill=none,text=otRed!85!black,anchor=south east] at (axis cs:43,505) {$V=500$};
  \node[etiq,fill=none,text=otNavy,anchor=north west] at (axis cs:24,440) {$\mathcal{C}_V$};
\end{axis}
\end{tikzpicture}""",
}

# graduations x placées à la main (côté libre de la courbe)
XLAB = {
    "ex_famille_cubique": [(-1, "d", "-1"), (1, "c", "1")],
    "ex1223_cos": [(-3.14159, "c", r"-\pi"), (-1.5708, "c", r"-\frac{\pi}{2}"),
                   (1.5708, "c", r"\frac{\pi}{2}"), (3.14159, "c", r"\pi")],
    "ex1224_ln": [(-4, "c", "-4"), (-2, "c", "-2"), (-1, "g", "-1"), (1, "d", "1"), (2, "c", "2"), (4, "c", "4")],
    "n1_courbes": [(1, "c", "1"), (3, "c", "3")],
    "n1_famille": [(1, "c", "1"), (3, "c", "3")],
    "n2_volume": [(13.8629, "c", r"10\ln 4"), (20, "c", "20"), (30, "c", "30"), (40, "c", "40")],
}
