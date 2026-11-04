# -*- coding: utf-8 -*-
"""Figures du quiz « Fonction exponentielle » (Terminale, notion 85), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>/quiz [nom …] [--planche]

Règles : figure d'énoncé sans la réponse ; figure de correction complétée en vert ;
courbes « choix » (q02_*, q12_*) toutes au même cadrage et à la même taille ;
noms neutres (q02_a…) pour que l'adresse de l'image ne trahisse pas la réponse.
"""

# ------------------------------------------------------------------ cadres communs
# q02 : « laquelle est la courbe de exp ? » — 4 courbes, même repère
CADRE_Q02 = (r"otWeb, width=3.9cm, height=3.6cm, xmin=-3.1, xmax=2.3, ymin=-1.7, ymax=5.3,"
             r" xtick={-2,-1,1,2}, xticklabels={}, ytick={1,2,3,4}")
# q12 : « associer chaque fonction à sa courbe » — 4 courbes, même repère
CADRE_Q12 = (r"otWeb, width=3.9cm, height=3.4cm, xmin=-2.7, xmax=2.7, ymin=-1.0, ymax=3.6,"
             r" xtick={-2,-1,1,2}, xticklabels={}, ytick={1,2,3}")


def courbe_choix(cadre, trace, ylabels="east"):
    """Une courbe « choix » : repère commun, une seule courbe bleue, aucun nom de fonction."""
    if ylabels == "west":
        cadre += r", yticklabel style={anchor=south west,xshift=3.5pt,yshift=1pt}"
    return (r"""
\begin{tikzpicture}
\begin{axis}[""" + cadre + r"""]
""" + trace + r"""
\end{axis}
\end{tikzpicture}""")


FIGURES = {
# =============================================================== q01 : e^x = -2 n'a pas de solution
"q01_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-3.3, xmax=2.4, ymin=-2.6, ymax=5.0,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={-2,-1,1,2,3,4}]
  \draw[seuil] (axis cs:-3.3,-2) -- (axis cs:2.3,-2);
  \addplot[otGreenDark, line width=1.35pt, domain=-3.3:1.55] {exp(x)};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.25,2.4) {$y=e^x$};
  \node[etiq,text=otOrange!80!black,anchor=south east] at (axis cs:2.3,-1.92) {$y=-2$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:-3.25,-1.3) {aucun point commun};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q02 : quatre courbes (choix)
"q02_a": courbe_choix(CADRE_Q02, r"  \addplot[courbe, domain=-1.62:2.3] {exp(-x)};", "west"),     # e^{-x}
"q02_b": courbe_choix(CADRE_Q02, r"  \addplot[courbe, domain=-3.1:1.8] {exp(x)-1};"),             # e^x - 1
"q02_c": courbe_choix(CADRE_Q02, r"  \addplot[courbe, domain=-3.1:1.63] {exp(x)};"),              # e^x (bonne)
"q02_d": courbe_choix(CADRE_Q02, r"  \addplot[courbe, domain=-3.1:1.41] {exp(x)+1};"),            # e^x + 1

"q02_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-3.3, xmax=2.4, ymin=-1.0, ymax=5.3,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={2,3,4,5}]
  \addplot[otGreenDark, line width=1.35pt, domain=-3.3:1.64] {exp(x)};
  \guides{1}{2.71828}
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{1}{2.71828}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.06,2.71828) {$e$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:-0.1,1.1) {$(0\,;1)$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.08,2.55) {$(1\,;e)$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.6,4.6) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:-2.95,0.55) {$e^x>0$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q04 : tangente en 0
"q04_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-3.3, xmax=2.4, ymin=-1.5, ymax=5.0,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={1,2,3,4}]
  \addplot[otOrange, line width=1.1pt, domain=-2.45:2.2] {x+1};
  \addplot[courbe, domain=-3.3:1.6] {exp(x)};
  \pnt{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.3,4.2) {$y=e^x$};
  \node[etiq,text=otOrange!80!black,anchor=north west] at (axis cs:1.55,2.4) {$T$};
\end{axis}
\end{tikzpicture}""",

"q04_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.6cm, xmin=-3.3, xmax=2.4, ymin=-1.5, ymax=5.0,
  xtick={-3,-2,-1,1,2}, xticklabels={}, ytick={2,3,4}]
  \addplot[otGreenDark, line width=1.1pt, domain=-2.45:2.2] {x+1};
  \addplot[courbe, domain=-3.3:1.6] {exp(x)};
  \draw[otGreenDark, line width=0.7pt, dash pattern=on 2.5pt off 1.6pt] (axis cs:0,1) -- (axis cs:1,1) -- (axis cs:1,2);
  \pnt[otGreenDark]{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.3,4.2) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.5,2.2) {$T : y=x+1$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:-0.12,1.15) {$(0\,;1)$};
  \node[note,text=otGreenDark,anchor=north] at (axis cs:0.5,0.93) {$+1$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:1.04,1.4) {$+1$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q06 : e^{-2x+1} décroissante
"q06_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.4cm, xmin=-0.9, xmax=2.6, ymin=-0.6, ymax=4.6,
  xtick={1,2}, ytick={1,2,3,4}, yticklabels={$1$,$2$,,}]
  \addplot[otGreenDark, line width=1.35pt, domain=-0.24:2.45] {exp(-2*x+1)};
  \pnt[otGreenDark]{0}{2.71828}
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:0.12,2.72) {$(0\,;e)$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:0.75,1.25) {$y=e^{-2x+1}$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:1.0,0.95) {décroissante : $u'=-2<0$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q10 : ensemble des solutions x < 3
"q10_corrige": r"""
\begin{tikzpicture}[x=0.95cm]
  \draw[otMuted, line width=0.6pt, -{Stealth[length=2.3mm]}] (-1.6,0) -- (5.2,0);
  \draw[otGreen, line width=3pt, line cap=butt, opacity=0.9] (-1.6,0) -- (3,0);
  \foreach \k in {-1,0,1,2,4} {\draw[otMuted, line width=0.5pt] (\k,-0.07) -- (\k,0.07);}
  \draw[otGreenDark, line width=1.2pt] (3.14,0.2) -- (3,0.2) -- (3,-0.2) -- (3.14,-0.2);
  \node[font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, anchor=north] at (0,-0.26) {0};
  \node[font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, anchor=north] at (1,-0.26) {1};
  \node[font=\otRegular\fontsize{9}{10}\selectfont, text=otGreenDark, anchor=north] at (3,-0.26) {3};
  \node[text=otGreenDark, anchor=south] at (0.7,0.24) {$S=\left]-\infty\,;3\right[$};
  \node[note, anchor=north] at (4.3,-0.26) {$3$ exclu};
\end{tikzpicture}""",

# =============================================================== q12 : associer fonctions et courbes
"q12_a": courbe_choix(CADRE_Q12, r"  \addplot[courbe, domain=-1.2:2.7] {exp(-x)};", "west"),        # e^{-x}
"q12_b": courbe_choix(CADRE_Q12, r"  \addplot[courbe, domain=-2.7:2.7] {exp(-x^2)};"),             # e^{-x^2}
"q12_c": courbe_choix(CADRE_Q12, r"  \addplot[courbe, domain=-1.1:1.1] {exp(x^2)};"),              # e^{x^2}
"q12_d": courbe_choix(CADRE_Q12, r"  \addplot[courbe, domain=-2.7:1.08] {x*exp(x)};"),             # x e^x

# =============================================================== q13 : suite géométrique e^{-0,5n}
"q13_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.8cm, xmin=-0.6, xmax=8.8, ymin=-0.18, ymax=1.32,
  xtick={1,2,3,4,5,6,7,8}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}, xlabel={$n$}, ylabel={$u_n$}]
  \addplot[otGreen!45, line width=0.6pt, dash pattern=on 2pt off 1.6pt, domain=0:8.3] {exp(-0.5*x)};
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{1}{0.60653} \pnt[otGreenDark]{2}{0.36788}
  \pnt[otGreenDark]{3}{0.22313} \pnt[otGreenDark]{4}{0.13534} \pnt[otGreenDark]{5}{0.08208}
  \pnt[otGreenDark]{6}{0.04979} \pnt[otGreenDark]{7}{0.03020} \pnt[otGreenDark]{8}{0.01832}
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:2.6,0.62) {$u_{n+1}=e^{-0{,}5}\times u_n$};
  \node[note,anchor=south west] at (axis cs:2.6,0.36) {raison $e^{-0{,}5}\approx 0{,}61$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q14 : maximum de x e^{-x}
"q14_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4cm, xmin=-0.7, xmax=6.6, ymin=-0.95, ymax=0.74,
  xtick={1,2,3,4,5,6}, ytick={0.5}, yticklabels={$0{,}5$}]
  \addplot[courbe, domain=-0.52:6.4] {x*exp(-x)};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.5,0.3) {$y=xe^{-x}$};
\end{axis}
\end{tikzpicture}""",

"q14_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4cm, xmin=-0.7, xmax=6.6, ymin=-0.95, ymax=0.74,
  xtick={1,2,3,4,5,6}, ytick={0.5}, yticklabels={$0{,}5$}]
  \addplot[courbe, domain=-0.52:6.4] {x*exp(-x)};
  \guides{1}{0.36788}
  \pnt[otGreenDark]{1}{0.36788}
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:1,0.4) {maximum};
  \node[etiq,anchor=east,text=otGreenDark] at (axis cs:-0.05,0.36788) {$\frac{1}{e}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.5,0.3) {$y=xe^{-x}$};
\end{axis}
\end{tikzpicture}""",

# =============================================================== q15 : condensateur
"q15_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.8cm, xmin=-0.6, xmax=13, ymin=-0.7, ymax=6.3,
  xtick={2,4,6,8,10,12}, ytick={1,2,3,4,5}, xlabel={$t$}, ylabel={$u$}]
  \addplot[courbe, domain=0:12.6] {5*(1-exp(-0.5*x))};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.6,3.2) {$u(t)=5\left(1-e^{-0{,}5t}\right)$};
\end{axis}
\end{tikzpicture}""",

"q15_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.8cm, xmin=-0.6, xmax=13, ymin=-0.7, ymax=6.3,
  xtick={2,4,6,8,10,12}, ytick={1,2,3,5}, xlabel={$t$}, ylabel={$u$}]
  \draw[asymptote] (axis cs:0,5) -- (axis cs:12.7,5);
  \addplot[courbe, domain=0:12.6] {5*(1-exp(-0.5*x))};
  \guides{4}{4.3233}
  \pnt[otGreenDark]{4}{4.3233}
  \node[etiq,anchor=east,text=otGreenDark] at (axis cs:-0.08,4.3233) {$4{,}32$};
  \node[note,anchor=south east] at (axis cs:12.7,5.12) {asymptote $y=5$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.6,3.2) {$u(t)=5\left(1-e^{-0{,}5t}\right)$};
\end{axis}
\end{tikzpicture}""",
}

# Graduations de l'axe des abscisses placées à la main, du côté libre de la courbe :
# « g » sous l'axe à gauche du trait, « d » à droite, « c » centrée dessous, « h » au-dessus.
_X3 = [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "c", "2")]
_X2 = [(-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "c", "2")]
_X2H = [(-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1"), (2, "c", "2")]
XLAB = {
    "q01_corrige": _X3,
    "q02_a": _X2, "q02_b": _X2H, "q02_c": _X2, "q02_d": _X2,
    "q02_corrige": _X3,
    "q04_enonce": [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "c", "1"), (2, "c", "2")],
    "q04_corrige": [(-3, "c", "-3"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "c", "1"), (2, "c", "2")],
    "q12_a": _X2, "q12_b": _X2, "q12_c": _X2, "q12_d": _X2H,
}

# Graduations placées à la main : étiquettes automatiques vides, sans fond blanc.
for _nom in XLAB:
    FIGURES[_nom] = FIGURES[_nom].replace(r"\begin{axis}[", r"\begin{axis}[xticklabel style={fill=none}, ", 1)
