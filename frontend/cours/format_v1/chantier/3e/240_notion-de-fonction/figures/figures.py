# -*- coding: utf-8 -*-
"""Figures de la notion 240 (3e : notion de fonction), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Courbes en bleu marine, seconde courbe en orange ; dans les corrigés, les
lectures graphiques (pointillés, points, valeurs lues) sont en vert.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  courbeB/.style={otOrange,line width=1.35pt},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
  lecture/.style={otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt},
  niveau/.style={otGreenDark,line width=0.8pt,dash pattern=on 4pt off 2.5pt},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=3.3cm,minimum height=.62cm,inner sep=3pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
\newcommand{\lirev}[2]{\draw[lecture] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\lirex}[2]{\draw[lecture] (axis cs:#1,#2) -- (axis cs:#1,0);}
"""

AX = r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, gm, "
FIN = "\n\\end{axis}\n\\end{tikzpicture}"


def fig(opts, corps):
    return AX + opts + "]\n" + corps + FIN


FIGURES = {}
XLAB = {}

# ------------------------------------------------------------ schéma x -> f(x)
def machine(entree, nom, regle, sortie, legende, haut=("nombre $x$", "fonction $f$", "image $f(x)$")):
    return r"""
\begin{tikzpicture}[font=\normalsize]
  \node[draw=otNavy,fill=otSky,line width=0.9pt,rounded corners=3pt,
        minimum width=1.1cm,minimum height=0.95cm,text=otNavy] (a) at (0,0) {%s};
  \node[fill=otNavy,rounded corners=4pt,minimum width=2.4cm,minimum height=1.3cm,
        text=white,align=center] (f) at (2.6,0) {%s\\[2pt]%s};
  \node[draw=otGreenDark,fill=otGreen!15,line width=0.9pt,rounded corners=3pt,
        minimum width=1.1cm,minimum height=0.95cm,text=otGreenDark] (r) at (5.2,0) {%s};
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (a.east) -- (f.west);
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (f.east) -- (r.west);
  \node[note,text=otNavy,anchor=south] at ($(a.north)+(0,0.12)$) {%s};
  \node[note,text=otNavy,anchor=south] at ($(f.north)+(0,0.12)$) {%s};
  \node[note,text=otGreenDark,anchor=south] at ($(r.north)+(0,0.12)$) {%s};
  \node[anchor=north,text=otInk] at ($(f.south)+(0,-0.22)$) {%s};
\end{tikzpicture}
""" % (entree, nom, regle, sortie, haut[0], haut[1], haut[2], legende)


FIGURES["machine_cours"] = machine("$3$", "$f$", r"$\times 2$, puis $+\,1$", "$7$",
                                   r"$f : x \longmapsto 2x + 1$ \quad et \quad $f(3) = 7$")

# ------------------------------------------------------------ programmes de calcul (2282)
def programme(etapes, expressions=None):
    L = [r"\begin{tikzpicture}"]
    dy = 1.05
    for k, e in enumerate(etapes):
        L.append(rf"\node[boite] (b{k}) at (0,{-k*dy:.2f}) {{{e}}};")
        if k:
            L.append(rf"\draw[fleche] (b{k-1}.south) -- (b{k}.north);")
        if expressions and expressions[k]:
            L.append(rf"\node[anchor=west,text=otGreenDark] at ($(b{k}.east)+(.25,0)$) {{{expressions[k]}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


ETAPES_2282 = ["Choisir un nombre", "Ajouter $3$", "Élever le résultat au carré"]
FIGURES["programme_enonce"] = programme(ETAPES_2282)
FIGURES["programme_corrige"] = programme(ETAPES_2282, ["$x$", "$x + 3$", "$(x + 3)^2$"])

# ------------------------------------------------------------ cours : lecture graphique
# f(x) = x^2 - 4x + 1 : f(5) = 6 ; antécédents de -2 : 1 et 3
FIGURES["cours_lecture"] = fig(
    r"width=7cm, height=7cm, xmin=-1.4, xmax=5.7, ymin=-3.9, ymax=7.4, "
    r"xtick={-1,1,2,3,4,5}, xticklabels={}, ytick={-3,-2,-1,1,2,3,4,5,6,7}, yticklabels={$-3$,$-2$,$-1$,,,,$4$,$5$,$6$,$7$}",
    r"""
  \addplot[courbe, domain=-0.75:5.15, samples=80] {x^2-4*x+1};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:3.9,3.3) {$\mathcal{C}_f$};
  \lirev{5}{6}
  \pnt[otGreenDark]{5}{6}
  \node[note,text=otGreenDark,anchor=east,align=right] at (axis cs:3.9,6.6) {image de $5$ : $f(5) = 6$};
  \draw[niveau] (axis cs:-1.3,-2) -- (axis cs:5.6,-2);
  \lirex{1}{-2} \lirex{3}{-2}
  \pnt[otGreenDark]{1}{-2} \pnt[otGreenDark]{3}{-2}
  \node[note,text=otGreenDark,anchor=north west,align=left] at (axis cs:3.45,-2.3) {antécédents\\de $-2$ : $1$ et $3$};
""")
XLAB["cours_lecture"] = [(-1, "c", "-1"), (1, "h", "1"), (2, "c", "2"), (3, "h", "3"), (4, "c", "4"), (5, "c", "5")]

# ------------------------------------------------------------ 2280 : f(x) = -x^2 + 2x + 3 sur [-2 ; 4]
P80 = (r"width=6.8cm, height=7.2cm, xmin=-2.6, xmax=4.7, ymin=-5.8, ymax=5.2, "
       r"xtick={-2,-1,1,2,3,4}, xticklabels={}, ytick={-5,-4,-3,-2,-1,1,2,3,4,5}, yticklabels={$-5$,$-4$,$-3$,$-2$,$-1$,$1$,,,$4$,$5$}")
B80 = r"""
  \addplot[courbe, domain=-2:4, samples=80] {-x^2+2*x+3};
  \pnt{-2}{-5} \pnt{4}{-5}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.6,3.6) {$\mathcal{C}_f$};
"""
FIGURES["lecture_2280_enonce"] = fig(P80, B80)
FIGURES["lecture_2280_corrige"] = fig(P80, B80 + r"""
  \lirev{4}{-5}
  \pnt[otGreenDark]{4}{-5}
  \draw[niveau] (axis cs:-2.5,3) -- (axis cs:2.9,3);
  \lirex{0}{3} \lirex{2}{3}
  \pnt[otGreenDark]{0}{3} \pnt[otGreenDark]{2}{3}
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:-2.5,3.15) {$y = 3$};
""")
XLAB["lecture_2280_enonce"] = [(-2, "h", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "h", "4")]
XLAB["lecture_2280_corrige"] = XLAB["lecture_2280_enonce"]

# ------------------------------------------------------------ 2283 : ligne brisée
P83 = (r"width=7.4cm, height=5.6cm, xmin=-4.8, xmax=3.8, ymin=-1.9, ymax=4.6, "
       r"xtick={-4,-3,-2,-1,1,2,3}, xticklabels={}, ytick={-1,1,2,3,4}, yticklabels={$-1$,,$2$,$3$,$4$}")
B83 = r"""
  \draw[ligne] (axis cs:-4,0) -- (axis cs:-1,3) -- (axis cs:1,-1) -- (axis cs:3,1);
  \pnt{-4}{0} \pnt{-1}{3} \pnt{1}{-1} \pnt{3}{1}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-2.9,2.1) {$\mathcal{C}_f$};
"""
FIGURES["brisee_enonce"] = fig(P83, B83)
FIGURES["brisee_corrige"] = fig(P83, B83 + r"""
  \draw[niveau] (axis cs:-4.7,1) -- (axis cs:3.7,1);
  \lirex{-3}{1} \lirex{3}{1}
  \pnt[otGreenDark]{-3}{1} \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{3}{1}
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:1.5,1.15) {$y = 1$};
""")
XLAB["brisee_enonce"] = [(-4, "g", "-4"), (-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2"), (3, "c", "3")]
XLAB["brisee_corrige"] = [(-4, "g", "-4"), (-3, "c", "-3"), (-2, "c", "-2"), (-1, "c", "-1"), (1, "h", "1"), (2, "c", "2"), (3, "c", "3")]

# ------------------------------------------------------------ 2285 : deux droites f(x) = x + 2, g(x) = 2x - 1
P85 = (r"width=6.8cm, height=7.4cm, xmin=-1.6, xmax=6.4, ymin=-1.7, ymax=11.2, "
       r"xtick={-1,1,2,3,4,5,6}, xticklabels={}, ytick={-1,1,2,3,4,5,6,7,8,9,10,11}, "
       r"yticklabels={,,$2$,,$4$,,$6$,,$8$,,$10$,}")
B85 = r"""
  \addplot[courbe, domain=-1.5:6.3] {x+2};
  \addplot[courbeB, domain=-0.3:6.05] {2*x-1};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:5.2,7.0) {$\mathcal{C}_f$};
  \node[etiq,text=otOrange!85!black,anchor=east] at (axis cs:4.95,10.3) {$\mathcal{C}_g$};
"""
FIGURES["droites_enonce"] = fig(P85, B85)
FIGURES["droites_corrige"] = fig(P85, B85 + r"""
  \lirev{3}{5}
  \pnt[otGreenDark]{3}{5}
  \node[note,text=otGreenDark,anchor=west] at (axis cs:3.25,4.7) {$(3\ ;\ 5)$};
""")
XLAB["droites_enonce"] = [(-1, "c", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "c", "6")]
XLAB["droites_corrige"] = XLAB["droites_enonce"]

# ------------------------------------------------------------ 2286 : tableau -> courbe, f(x) = 4 - x^2
P86 = (r"width=6.4cm, height=7cm, xmin=-3.6, xmax=3.6, ymin=-5.8, ymax=5.0, "
       r"xtick={-3,-2,-1,1,2,3}, xticklabels={}, ytick={-5,-4,-3,-2,-1,1,2,3,4}, yticklabels={$-5$,$-4$,$-3$,$-2$,$-1$,$1$,$2$,$3$,}")
FIGURES["tableau_courbe_corrige"] = fig(P86, r"""
  \addplot[courbe, domain=-3:3, samples=80] {4-x^2};
  \pnt[otGreenDark]{-3}{-5} \pnt[otGreenDark]{-2}{0} \pnt[otGreenDark]{-1}{3} \pnt[otGreenDark]{0}{4}
  \pnt[otGreenDark]{1}{3} \pnt[otGreenDark]{2}{0} \pnt[otGreenDark]{3}{-5}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.6,2.6) {$\mathcal{C}_f$};
""")
XLAB["tableau_courbe_corrige"] = [(-3, "c", "-3"), (-2, "h", "-2"), (-1, "c", "-1"), (1, "c", "1"), (2, "h", "2"), (3, "c", "3")]

# ------------------------------------------------------------ 2288 : f(x) = x^2 - 2x - 3 sur [-2 ; 4]
P88 = (r"width=6.8cm, height=7.2cm, xmin=-2.7, xmax=4.7, ymin=-5.2, ymax=6.0, "
       r"xtick={-2,-1,1,2,3,4}, xticklabels={}, ytick={-5,-4,-3,-2,-1,1,2,3,4,5}, yticklabels={$-5$,$-4$,,,$-1$,$1$,$2$,$3$,$4$,$5$}")
B88 = r"""
  \addplot[courbe, domain=-2:4, samples=80] {x^2-2*x-3};
  \pnt{-2}{5} \pnt{4}{5}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:3.25,3.6) {$\mathcal{C}_f$};
"""
FIGURES["courbe_2288_enonce"] = fig(P88, B88)
FIGURES["courbe_2288_corrige"] = fig(P88, B88 + r"""
  \lirev{4}{5}
  \pnt[otGreenDark]{4}{5}
  \draw[niveau] (axis cs:-2.6,-3) -- (axis cs:4.6,-3);
  \lirex{0}{-3} \lirex{2}{-3}
  \pnt[otGreenDark]{0}{-3} \pnt[otGreenDark]{2}{-3}
  \pnt[otGreenDark]{-1}{0} \pnt[otGreenDark]{3}{0}
  \node[note,text=otGreenDark,anchor=north east] at (axis cs:4.6,-3.15) {$y = -3$};
""")
XLAB["courbe_2288_enonce"] = [(-2, "c", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "c", "4")]
XLAB["courbe_2288_corrige"] = XLAB["courbe_2288_enonce"]

# ------------------------------------------------------------ 2292 : distance au départ en fonction du temps
P92 = (r"width=7.2cm, height=5.2cm, xmin=0, xmax=29.5, ymin=0, ymax=690, "
       r"xtick={5,10,15,20,25}, ytick={100,200,300,400,500,600}, "
       r"xlabel={$t$ (min)}, ylabel={$d$ (m)}")
B92 = r"""
  \draw[ligne] (axis cs:0,0) -- (axis cs:10,600) -- (axis cs:15,600) -- (axis cs:27,0);
  \pnt{0}{0} \pnt{10}{600} \pnt{15}{600} \pnt{27}{0}
"""
FIGURES["promenade_enonce"] = fig(P92, B92)
FIGURES["promenade_corrige"] = fig(P92, B92 + r"""
  \node[note,text=otGreenDark,anchor=west,align=left] at (axis cs:6.6,140) {aller\\$60$ m/min};
  \node[note,text=otGreenDark,anchor=north] at (axis cs:12.5,560) {pause};
  \node[note,text=otGreenDark,anchor=east,align=right] at (axis cs:19.6,140) {retour\\$50$ m/min};
  \draw[otGreenDark,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,300) -- (axis cs:24,300);
  \draw[otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt] (axis cs:5,300) -- (axis cs:5,0);
  \draw[otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt] (axis cs:21,300) -- (axis cs:21,0);
  \fill[otGreenDark] (axis cs:5,300) circle (2.1pt);
  \fill[otGreenDark] (axis cs:21,300) circle (2.1pt);
  \node[note,text=otGreenDark,anchor=south] at (axis cs:13,305) {$d = 300$};
""")
