# -*- coding: utf-8 -*-
"""Figures de la notion 241 (3e : fonctions linéaires et affines), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Droites en bleu marine, seconde droite en orange ; dans les corrigés, les
lectures (ordonnée à l'origine, « +1 » puis « +a », points, intersections)
sont en vert.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  courbeB/.style={otOrange,line width=1.35pt},
  lecture/.style={otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt},
  niveau/.style={otGreenDark,line width=0.8pt,dash pattern=on 4pt off 2.5pt},
  pas/.style={otGreenDark,line width=1.1pt,-{Stealth[length=2mm]}},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
\newcommand{\lirev}[2]{\draw[lecture] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
"""

AX = r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, gm, "
FIN = "\n\\end{axis}\n\\end{tikzpicture}"


def fig(opts, corps):
    return AX + opts + "]\n" + corps + FIN


FIGURES = {}
XLAB = {}

# ------------------------------------------------------------ cours et fiche : g(x) = 2x - 3
PC = (r"width=6.2cm, height=7.4cm, xmin=-1.6, xmax=4.4, ymin=-4.6, ymax=5.6, "
      r"xtick={-1,1,2,3,4}, xticklabels={}, ytick={-4,-3,-2,-1,1,2,3,4,5}, "
      r"yticklabels={,,$-2$,$-1$,$1$,$2$,$3$,$4$,$5$}")
FIGURES["cours_affine"] = fig(PC, r"""
  \addplot[courbe, domain=-0.75:4.25] {2*x-3};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:3.55,3.4) {$\mathcal{D}$};
  \pnt[otGreenDark]{0}{-3}
  \node[note,text=otGreenDark,anchor=south east] at (axis cs:-0.12,-2.85) {$b = -3$};
  \draw[pas] (axis cs:2,1) -- (axis cs:3,1);
  \draw[pas] (axis cs:3,1) -- (axis cs:3,3);
  \node[note,text=otGreenDark,anchor=north] at (axis cs:2.5,0.88) {$+1$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:3.08,1.9) {$+2 = a$};
  \pnt{2}{1} \pnt{3}{3}
""")
XLAB["cours_affine"] = [(-1, "c", "-1"), (1, "c", "1"), (2, "h", "2"), (3, "c", "3"), (4, "c", "4")]

# ------------------------------------------------------------ 2299 : f(x) = 1,5x (corrigé)
P99 = (r"width=6.2cm, height=7cm, xmin=-0.9, xmax=4.8, ymin=-0.9, ymax=7.2, "
       r"xtick={1,2,3,4}, ytick={1,2,3,4,5,6,7}")
FIGURES["lineaire_2299_corrige"] = fig(P99, r"""
  \addplot[courbe, domain=-0.5:4.5] {1.5*x};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:3.6,4.9) {$\mathcal{D}_f$};
  \pnt[otGreenDark]{0}{0} \pnt[otGreenDark]{2}{3} \pnt[otGreenDark]{4}{6}
  \node[note,text=otGreenDark,anchor=east] at (axis cs:1.85,3.25) {$A(2\ ;\ 3)$};
  \node[note,text=otGreenDark,anchor=east] at (axis cs:3.85,6.25) {$B(4\ ;\ 6)$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:0.05,-0.05) {$O$};
""")

# ------------------------------------------------------------ 2300 : g(x) = -x + 4 (corrigé)
P00 = (r"width=6.2cm, height=6.4cm, xmin=-0.9, xmax=5.4, ymin=-0.9, ymax=5.4, "
       r"xtick={1,2,3,4,5}, ytick={1,2,3,4,5}, yticklabels={$1$,$2$,$3$,,$5$}")
FIGURES["affine_2300_corrige"] = fig(P00, r"""
  \addplot[courbe, domain=-0.6:4.8] {-x+4};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.6,1.9) {$\mathcal{D}_g$};
  \pnt[otGreenDark]{0}{4} \pnt[otGreenDark]{4}{0} \pnt[otGreenDark]{1}{3}
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:0.3,4.45) {$(0\ ;\ 4)$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:4.05,0.15) {$(4\ ;\ 0)$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:1.12,3.1) {$(1\ ;\ 3)$};
""")

# ------------------------------------------------------------ 2301 : proportionnalité (corrigé)
P01 = (r"width=6.6cm, height=5.4cm, xmin=0, xmax=46, ymin=0, ymax=92, "
       r"xtick={10,20,30,40}, ytick={20,40,60,80}, xlabel={$x$ (L)}, ylabel={prix (\texteuro)}")
FIGURES["proportion_2301_corrige"] = fig(P01, r"""
  \addplot[courbe, domain=0:44] {1.9*x};
  \pnt[otGreenDark]{10}{19} \pnt[otGreenDark]{25}{47.5} \pnt[otGreenDark]{40}{76}
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:25.8,46.5) {$(25\ ;\ 47{,}5)$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:40.6,75) {$(40\ ;\ 76)$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:10.8,18) {$(10\ ;\ 19)$};
""")

# ------------------------------------------------------------ 2306 : lire f(x) = -2x + 3
P06 = (r"width=6.2cm, height=7.2cm, xmin=-1.6, xmax=3.4, ymin=-3.6, ymax=5.6, "
       r"xtick={-1,1,2,3}, xticklabels={}, ytick={-3,-2,-1,1,2,3,4,5}, "
       r"yticklabels={$-3$,$-2$,$-1$,$1$,$2$,,$4$,$5$}")
B06 = r"""
  \addplot[courbe, domain=-1.2:3.2] {-2*x+3};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:-0.95,5.0) {$\mathcal{D}$};
"""
FIGURES["lecture_2306_enonce"] = fig(P06, B06)
FIGURES["lecture_2306_corrige"] = fig(P06, B06 + r"""
  \pnt[otGreenDark]{0}{3}
  \node[note,text=otGreenDark,anchor=north east] at (axis cs:-0.1,2.85) {$b = 3$};
  \draw[pas] (axis cs:0,3) -- (axis cs:1,3);
  \draw[pas] (axis cs:1,3) -- (axis cs:1,1);
  \node[note,text=otGreenDark,anchor=south] at (axis cs:0.5,3.08) {$+1$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:1.08,2.1) {$-2 = a$};
  \pnt{1}{1}
  \pnt[otGreenDark]{1.5}{0}
  \node[note,text=otGreenDark,anchor=north east] at (axis cs:1.42,-0.2) {$1{,}5$};
""")
XLAB["lecture_2306_enonce"] = [(-1, "c", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3")]
XLAB["lecture_2306_corrige"] = [(-1, "c", "-1"), (2, "c", "2"), (3, "c", "3")]

# ------------------------------------------------------------ 2307 : droites parallèles (corrigé)
P07 = (r"width=6.0cm, height=7.4cm, xmin=-2.1, xmax=1.9, ymin=-8.6, ymax=11.6, "
       r"xtick={-2,-1,1}, xticklabels={}, ytick={-8,-6,-4,-2,2,4,6,8,10}, yticklabels={$-8$,$-6$,$-4$,,$2$,$4$,$6$,$8$,$10$}")
FIGURES["paralleles_2307_corrige"] = fig(P07, r"""
  \addplot[courbe, domain=-1.85:1.4] {4*x-1};
  \addplot[courbeB, domain=-2.0:1.35] {4*x+6};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.15,2.6) {$\mathcal{D}_f$};
  \node[etiq,text=otOrange!85!black,anchor=east] at (axis cs:0.85,10.6) {$\mathcal{D}_g$};
  \draw[otGreenDark,line width=1pt,{Stealth[length=2mm]}-{Stealth[length=2mm]}] (axis cs:0.75,2.2) -- (axis cs:0.75,8.8);
  \node[note,text=otGreenDark,anchor=west] at (axis cs:0.82,6.0) {$+7$};
""")
XLAB["paralleles_2307_corrige"] = [(-2, "c", "-2"), (-1, "c", "-1"), (1, "c", "1")]

# ------------------------------------------------------------ 2308 : pourcentages
P08 = (r"width=6.6cm, height=6.2cm, xmin=0, xmax=112, ymin=0, ymax=132, "
       r"xtick={20,40,60,80,100}, ytick={20,40,60,80,100,120}, xlabel={$x$}, ylabel={}")
FIGURES["pourcentages_2308_corrige"] = fig(P08, r"""
  \addplot[courbe, domain=0:105] {1.2*x};
  \addplot[courbeB, domain=0:105] {0.85*x};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:95,118) {$f(x) = 1{,}2x$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:83,62) {$g(x) = 0{,}85x$};
  \lirev{50}{60}
  \pnt[otGreenDark]{50}{60}
  \lirev{80}{68}
  \pnt[otGreenDark]{80}{68}
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:51,58) {$60$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:81,69) {$68$};
""")

# ------------------------------------------------------------ 2310 : deux abonnements (corrigé)
P10 = (r"width=6.8cm, height=6.2cm, xmin=0, xmax=11.2, ymin=0, ymax=64, "
       r"xtick={2,4,6,8,10}, ytick={10,20,30,40,50,60}, xlabel={$n$}, ylabel={prix (\texteuro)}")
FIGURES["abonnements_2310_corrige"] = fig(P10, r"""
  \addplot[courbe, domain=0:10.5] {20+3*x};
  \addplot[courbeB, domain=0:10.5] {8+5*x};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:8.6,44) {A};
  \node[etiq,text=otOrange!85!black,anchor=south east] at (axis cs:9.3,58) {B};
  \lirev{6}{38}
  \pnt[otGreenDark]{6}{38}
  \node[note,text=otGreenDark,anchor=south east] at (axis cs:5.8,39.5) {$(6\ ;\ 38)$};
""")

# ------------------------------------------------------------ 2316 : vélos, type brevet
P16 = (r"width=6.8cm, height=6.4cm, xmin=0, xmax=9.6, ymin=0, ymax=40, "
       r"xtick={1,2,3,4,5,6,7,8,9}, ytick={5,10,15,20,25,30,35}, xlabel={$h$}, ylabel={coût (\texteuro)}")
B16 = r"""
  \addplot[courbe, domain=0:9] {4*x};
  \addplot[courbeB, domain=0:9] {10+2*x};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:7.6,33.5) {Libre};
  \node[etiq,text=otOrange!85!black,anchor=south] at (axis cs:1.0,13.6) {Pass};
"""
FIGURES["velos_2316_enonce"] = fig(P16, B16)
FIGURES["velos_2316_corrige"] = fig(P16, B16 + r"""
  \lirev{5}{20}
  \pnt[otGreenDark]{5}{20}
  \draw[niveau] (axis cs:0,22) -- (axis cs:9.2,22);
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:0.1,22.3) {budget $22$};
  \draw[lecture] (axis cs:6,22) -- (axis cs:6,0);
  \pnt[otGreenDark]{6}{22} \pnt[otGreenDark]{5.5}{22}
""")
