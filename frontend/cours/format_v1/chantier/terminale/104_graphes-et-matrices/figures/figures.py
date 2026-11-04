# -*- coding: utf-8 -*-
"""Figures de la notion « Graphes et matrices » (Terminale, Mathématiques expertes).

Compilation : python ../../../outils/figures_livre.py <ce dossier de notion>
Graphes : sommets ronds (style « sommet »), arcs à pointe Stealth, poids posés
à côté des arêtes (jamais dessus). Éléments de réponse en vert (otGreenDark).
"""

PREAMBULE_EXTRA = r"""
\usetikzlibrary{matrix,backgrounds}
\tikzset{
  sommet/.style={circle,draw=otNavy,line width=0.9pt,fill=otSky,minimum size=7.6mm,inner sep=0pt,text=otInk,font=\normalsize},
  sommetVert/.style={sommet,draw=otGreenDark,line width=1.3pt},
  petit/.style={circle,draw=otNavy,line width=0.9pt,fill=otSky,minimum size=3.2mm,inner sep=0pt},
  arete/.style={otNavy,line width=1pt},
  areteVerte/.style={otGreenDark,line width=2pt},
  arc/.style={otNavy,line width=1pt,-{Stealth[length=2.7mm,width=2.2mm]},shorten >=0.8pt},
  arcVert/.style={otGreenDark,line width=2pt,-{Stealth[length=3.2mm,width=2.7mm]},shorten >=0.8pt},
  arcPale/.style={otNavy!30,line width=0.9pt,-{Stealth[length=2.5mm,width=2mm]},shorten >=0.8pt},
  poids/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,text=otInk,inner sep=3pt},
  legende/.style={font=\otRegular\fontsize{9}{11}\selectfont,text=otMuted,inner sep=2pt},
  coef/.style={minimum width=6.4mm,minimum height=5.6mm,inner sep=0pt,anchor=center},
}
"""

# ------------------------------------------------------------------ graphes
# Graphe G (non orienté) du cours : « maison » A B C D E.
POS_G = {"A": (0, 0), "B": (3.4, 0), "C": (3.4, 2.6), "D": (0, 2.6), "E": (1.7, 4.1)}
ARETES_G = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E")]


def sommets(pos, style="sommet", echelle=1.0, verts=()):
    return "".join(
        f"  \\node[{'sommetVert' if s in verts else style}] ({s}) at ({x * echelle:.3f},{y * echelle:.3f}) {{${s}$}};\n"
        for s, (x, y) in pos.items())


def graphe_g(echelle=1.0, aretes=ARETES_G, prefixe=""):
    code = sommets(POS_G, echelle=echelle)
    code += "".join(f"  \\draw[arete] ({a}) -- ({b});\n" for a, b in aretes)
    return code


FIGURES = {}

# Graphe G seul
FIGURES["cours_graphe"] = r"""
\begin{tikzpicture}
""" + graphe_g() + r"""
  \node[legende,anchor=north] at (1.7,-0.55) {graphe $G$ : ordre $5$, $7$ arêtes};
\end{tikzpicture}"""

# Graphe pondéré (durées en minutes)
FIGURES["cours_pondere"] = r"""
\begin{tikzpicture}
""" + graphe_g() + r"""
  \path (A) -- (B) node[poids,midway,below] {3};
  \path (A) -- (D) node[poids,midway,left] {7};
  \path (B) -- (C) node[poids,midway,right] {10};
  \path (B) -- (D) node[poids,pos=0.5,anchor=south west] {9};
  \path (C) -- (D) node[poids,midway,above] {15};
  \path (C) -- (E) node[poids,midway,anchor=south west] {5};
  \path (D) -- (E) node[poids,midway,anchor=south east] {12};
\end{tikzpicture}"""

# Graphes complets K4 et K5
FIGURES["cours_complets"] = r"""
\begin{tikzpicture}
  \foreach \i in {1,...,4} { \node[petit] (k\i) at ({45+90*\i}:1.35) {}; }
  \foreach \i/\j in {1/2,1/3,1/4,2/3,2/4,3/4} { \draw[arete] (k\i) -- (k\j); }
  \node[legende,anchor=north] at (0,-1.45) {$K_4$ : $6$ arêtes};
  \begin{scope}[xshift=4.6cm]
  \foreach \i in {1,...,5} { \node[petit] (p\i) at ({90+72*\i}:1.5) {}; }
  \foreach \i/\j in {1/2,1/3,1/4,1/5,2/3,2/4,2/5,3/4,3/5,4/5} { \draw[arete] (p\i) -- (p\j); }
  \node[legende,anchor=north] at (0,-1.45) {$K_5$ : $10$ arêtes};
  \end{scope}
\end{tikzpicture}"""

# Connexe / non connexe
FIGURES["cours_connexe"] = r"""
\begin{tikzpicture}
""" + graphe_g(0.72) + r"""
  \node[legende,anchor=north] at (1.224,-0.5) {connexe};
  \begin{scope}[xshift=4.4cm]
""" + sommets(POS_G, echelle=0.72).replace("(A)", "(A2)").replace("(B)", "(B2)").replace("(C)", "(C2)").replace("(D)", "(D2)").replace("(E)", "(E2)") + r"""
  \draw[arete] (A2) -- (B2); \draw[arete] (A2) -- (D2); \draw[arete] (B2) -- (C2);
  \draw[arete] (B2) -- (D2); \draw[arete] (C2) -- (D2);
  \node[legende,anchor=north] at (1.224,-0.5) {non connexe : $E$ est isolé};
  \end{scope}
\end{tikzpicture}"""

# Graphe orienté H : triangle A, B, C et D au centre
POS_H = {"A": (0, 3.1), "B": (2.7, 0), "C": (-2.7, 0), "D": (0, 1.25)}


def graphe_h(verts=(), arcs_verts=()):
    arcs = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D"), ("C", "D"), ("D", "B")]
    code = sommets(POS_H, verts=verts)
    for a, b in arcs:
        st = "arcVert" if (a, b) in arcs_verts else ("arcPale" if arcs_verts else "arc")
        code += f"  \\draw[{st}] ({a}) -- ({b});\n"
    return code


FIGURES["cours_oriente"] = r"""
\begin{tikzpicture}
""" + graphe_h() + r"""
  \node[legende,anchor=north] at (0,-0.55) {graphe orienté $H$};
\end{tikzpicture}"""

FIGURES["cours_chemins"] = r"""
\begin{tikzpicture}
""" + graphe_h(verts=("C", "B"), arcs_verts=(("C", "A"), ("A", "B"), ("C", "D"), ("D", "B"))) + r"""
  \node[legende,anchor=north,text=otGreenDark] at (0,-0.55) {$C\to A\to B$ et $C\to D\to B$ : $(M^2)_{CB}=2$};
\end{tikzpicture}"""

# ------------------------------------------------------------- Markov
FIGURES["cours_markov2"] = r"""
\begin{tikzpicture}
  \node[sommet] (A) at (0,0) {$A$};
  \node[sommet] (B) at (3.8,0) {$B$};
  \draw[arc] (A) to[bend left=28] node[poids,midway,above] {0,2} (B);
  \draw[arc] (B) to[bend left=28] node[poids,midway,below] {0,3} (A);
  \draw[arc] (A.150) to[out=160,in=200,looseness=6] node[poids,midway,left] {0,8} (A.210);
  \draw[arc] (B.30) to[out=20,in=-20,looseness=6] node[poids,midway,right] {0,7} (B.-30);
\end{tikzpicture}"""

FIGURES["cours_markov3"] = r"""
\begin{tikzpicture}
  \node[sommet] (A) at (0,0) {$A$};
  \node[sommet] (B) at (2.8,0) {$B$};
  \node[sommet] (C) at (5.6,0) {$C$};
  \draw[arc] (A) to[bend left=28] node[poids,midway,above] {0,5} (B);
  \draw[arc] (B) to[bend left=28] node[poids,midway,below] {0,25} (A);
  \draw[arc] (B) to[bend left=28] node[poids,midway,above] {0,25} (C);
  \draw[arc] (C) to[bend left=28] node[poids,midway,below] {0,5} (B);
  \draw[arc] (A.150) to[out=160,in=200,looseness=6] node[poids,midway,left] {0,5} (A.210);
  \draw[arc] (C.30) to[out=20,in=-20,looseness=6] node[poids,midway,right] {0,5} (C.-30);
  \draw[arc] (B.120) to[out=110,in=70,looseness=6] node[poids,midway,above] {0,5} (B.60);
\end{tikzpicture}"""

FIGURES["cours_convergence"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=3.6cm, xmin=-0.4, xmax=11, ymin=-0.08, ymax=1.18,
  xtick={2,4,6,8,10}, ytick={0.6,1}, yticklabels={$0{,}6$,$1$}, xlabel={$n$}, ylabel={$a_n$}]
  \draw[seuil] (axis cs:0,0.6) -- (axis cs:10.6,0.6);
  \addplot[only marks, mark=*, mark size=1.9pt, otNavy, samples at={0,...,10}] {0.6+0.4*0.5^x};
  \addplot[only marks, mark=*, mark size=1.9pt, otGreenDark, samples at={0,...,10}] {0.6-0.6*0.5^x};
  \node[note,anchor=west,text=otNavy] at (axis cs:1.25,1.0) {départ en $A$ : $a_0=1$};
  \node[note,anchor=west,text=otGreenDark] at (axis cs:1.35,0.12) {départ en $B$ : $a_0=0$};
\end{axis}
\end{tikzpicture}"""

# ------------------------------------------------------------- matrices
FIGURES["cours_produit"] = r"""
\begin{tikzpicture}
  \matrix (A) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=)] {1 & 2 & 3\\ 4 & 5 & 6\\};
  \node (fois) [right=3mm of A] {$\times$};
  \matrix (B) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=), right=3mm of fois] {1 & 0\\ -1 & 2\\ 2 & 1\\};
  \node (egal) [right=3mm of B] {$=$};
  \matrix (C) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=), right=3mm of egal] {5 & 7\\ 11 & 16\\};
  \begin{scope}[on background layer]
    \fill[otSky,rounded corners=2pt] ($(A-2-1.north west)+(-0.5mm,0.3mm)$) rectangle ($(A-2-3.south east)+(0.5mm,-0.3mm)$);
    \fill[otGreen!25,rounded corners=2pt] ($(B-1-1.north west)+(-0.3mm,0.5mm)$) rectangle ($(B-3-1.south east)+(0.3mm,-0.5mm)$);
    \fill[otOrange!35,rounded corners=2pt] ($(C-2-1.north west)+(-0.3mm,0.3mm)$) rectangle ($(C-2-1.south east)+(0.3mm,-0.3mm)$);
  \end{scope}
  \node[legende,anchor=north,text=otNavy] at (A.south |- B.south) {ligne $2$ de $A$};
  \node[legende,anchor=north,text=otGreenDark] at (B.south) {colonne $1$ de $B$};
  \node[legende,anchor=north,text=otOrange!80!black] at (C.south |- B.south) {$(AB)_{21}$};
  \node[anchor=north,inner sep=0pt] at ($(B.south)+(0,-6.5mm)$) {$(AB)_{21}=4\times1+5\times(-1)+6\times2=11$};
\end{tikzpicture}"""


def sarrus(entrees, couleur, diagonales, signe):
    """Tableau 3 × 5 (deux premières colonnes recopiées) et trois diagonales."""
    lignes = []
    for r in entrees:
        lignes.append(" & ".join(r + r[:2]) + r"\\")
    code = (r"\matrix (S) [matrix of math nodes, nodes={circle,minimum size=6.4mm,inner sep=0pt}, "
            r"column sep=2.2mm, row sep=1.2mm] {" + " ".join(lignes) + "};\n")
    code += r"  \draw[otMuted,line width=0.8pt] ($(S-1-1.north west)+(-0.6mm,1mm)$) -- ($(S-3-1.south west)+(-0.6mm,-1mm)$);" + "\n"
    code += r"  \draw[otMuted,line width=0.8pt] ($(S-1-3.north east)+(1.1mm,1mm)$) -- ($(S-3-3.south east)+(1.1mm,-1mm)$);" + "\n"
    for chemin in diagonales:
        code += "".join(f"  \\draw[{couleur},line width=0.8pt] (S-{i}-{j}) circle (3.2mm);\n" for i, j in chemin)
        code += f"  \\draw[{couleur},line width=1.1pt] " + " -- ".join(f"(S-{i}-{j})" for i, j in chemin) + ";\n"
    code += f"  \\node[legende,anchor=north,text={couleur}] at ($(S.south)+(0,-1mm)$) {{{signe}}};\n"
    return code


DESC = [[(1, 1), (2, 2), (3, 3)], [(1, 2), (2, 3), (3, 4)], [(1, 3), (2, 4), (3, 5)]]
MONT = [[(3, 1), (2, 2), (1, 3)], [(3, 2), (2, 3), (1, 4)], [(3, 3), (2, 4), (1, 5)]]


def figure_sarrus(entrees, texte_plus, texte_moins):
    return (r"""
\begin{tikzpicture}
  \begin{scope}
  """ + sarrus(entrees, "otGreenDark", DESC, texte_plus) + r"""  \end{scope}
  \begin{scope}[xshift=4.6cm]
  """ + sarrus(entrees, "otOrange!85!black", MONT, texte_moins) + r"""  \end{scope}
\end{tikzpicture}""")


FIGURES["cours_sarrus"] = figure_sarrus([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]],
                                        r"$+\,(aei+bfg+cdh)$", r"$-\,(ceg+afh+bdi)$")

# ------------------------------------------------------------- transformations
FIGURES["cours_rotation"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=3.9cm, xmin=-2.3, xmax=3.0, ymin=-0.55, ymax=2.8,
  xtick={-2,-1,1,2}, ytick={1,2}, yticklabels={$1$,{}}]
  \draw[otNavy,line width=0.9pt] (axis cs:0,0) -- (axis cs:2,1);
  \draw[otGreenDark,line width=0.9pt] (axis cs:0,0) -- (axis cs:-1,2);
  \draw[otMuted,line width=0.8pt,dash pattern=on 3pt off 2pt,-{Stealth[length=2mm]}] (axis cs:2,1) arc[start angle=26.565, end angle=116.565, radius=2.236];
  \draw[otMuted,line width=0.6pt] (axis cs:0.179,0.089) -- (axis cs:0.089,0.268) -- (axis cs:-0.089,0.179);
  \pnt{2}{1} \pnt[otGreenDark]{-1}{2}
  \node[anchor=west] at (axis cs:2.08,1.0) {$M$};
  \node[anchor=east,text=otGreenDark] at (axis cs:-1.1,2.05) {$M'$};
  \node[anchor=north east] at (axis cs:-0.03,-0.03) {$O$};
\end{axis}
\end{tikzpicture}"""

FIGURES["ex1139_rotation"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=3.8cm, xmin=-3.8, xmax=2.9, ymin=-0.55, ymax=3.6,
  xtick={-3,-2,-1,1,2}, ytick={1,2,3}]
  \draw[otNavy,line width=0.9pt] (axis cs:0,0) -- (axis cs:2,3);
  \draw[otGreenDark,line width=0.9pt] (axis cs:0,0) -- (axis cs:-3,2);
  \draw[otMuted,line width=0.8pt,dash pattern=on 3pt off 2pt,-{Stealth[length=2mm]}] (axis cs:2,3) arc[start angle=56.31, end angle=146.31, radius=3.606];
  \draw[otMuted,line width=0.6pt] (axis cs:0.139,0.208) -- (axis cs:-0.069,0.347) -- (axis cs:-0.208,0.139);
  \pnt{2}{3} \pnt[otGreenDark]{-3}{2}
  \node[anchor=west] at (axis cs:2.08,3.0) {$M$};
  \node[anchor=north,text=otGreenDark] at (axis cs:-3,1.88) {$M'$};
  \node[anchor=north east] at (axis cs:-0.03,-0.03) {$O$};
\end{axis}
\end{tikzpicture}"""

FIGURES["ex1139_composee"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=3.6cm, height=7.2cm, xmin=-0.9, xmax=4.0, ymin=-2.7, ymax=7.0,
  xtick={2,3}, ytick={-2,-1,1,2,3,4,5,6}]
  \draw[guide] (axis cs:1,-2) -- (axis cs:1,2);
  % graduation 1 de l'axe des abscisses : à gauche du pointillé vertical x = 1
  \draw[otMuted,line width=0.5pt] ([yshift=-1.5pt]axis cs:1,0) -- ([yshift=1.5pt]axis cs:1,0);
  \node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt] at (axis cs:1,0) [xshift=-2pt,yshift=-2.5pt] {$1$};
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:0,0) -- (axis cs:3,6);
  \pnt{1}{-2} \pnt{1}{2} \pnt[otGreenDark]{3}{6}
  \node[anchor=west] at (axis cs:1.12,-2) {$N$};
  \node[anchor=north west] at (axis cs:1.1,1.9) {$N_1$};
  \node[anchor=west,text=otGreenDark] at (axis cs:3.1,6) {$N'$};
\end{axis}
\end{tikzpicture}"""

# ------------------------------------------------------------- systèmes (1136)
FIGURES["ex1136_q1"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.8cm, xmin=-0.7, xmax=5.6, ymin=-0.85, ymax=3.0,
  xtick={1,2,3}, ytick={1,2}]
  \addplot[courbe, domain=0:4.6] {(7-2*x)/3};
  \addplot[courbe2, domain=0:5.4] {(4-x)/2};
  \guides{2}{1}
  \pnt[otGreenDark]{2}{1}
  \node[anchor=south west,text=otGreenDark] at (axis cs:2.05,1.05) {$(2\,;1)$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.75,2.05) {$2x+3y=7$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:3.7,0.42) {$x+2y=4$};
\end{axis}
\end{tikzpicture}"""

FIGURES["ex1136_q2"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=4.4cm, height=5.2cm, xmin=-0.6, xmax=3.3, ymin=-5.6, ymax=4.6,
  xtick={1,2,3}, ytick={-4,-2,2,4}]
  \addplot[courbe, domain=0.2:3.1] {3*x-5};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.25,2.6) {$y=3x-5$};
\end{axis}
\end{tikzpicture}"""

FIGURES["ex1136_q3"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.4cm, xmin=-0.4, xmax=4.4, ymin=-0.3, ymax=2.4,
  xtick={1,2}, ytick={1,2}]
  \addplot[courbe, domain=0:3.5] {(3-x)/2};
  \addplot[courbe2, domain=0:4.0] {(7-2*x)/4};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:1.6,1.05) {$2x+4y=7$};
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:1.75,0.55) {$x+2y=3$};
\end{axis}
\end{tikzpicture}"""

# ------------------------------------------------------------- exercice 1142
POS_42 = {"A": (0, 3.3), "B": (-2.8, 0), "C": (0, 1.25), "D": (2.8, 0)}
ARCS_42 = [("A", "B"), ("B", "D"), ("D", "A"), ("B", "C"), ("C", "D")]


def graphe_42(arcs_verts=(), verts=()):
    code = sommets(POS_42, verts=verts)
    for a, b in ARCS_42:
        st = "arcVert" if (a, b) in arcs_verts else ("arcPale" if arcs_verts else "arc")
        code += f"  \\draw[{st}] ({a}) -- ({b});\n"
    for a, b in (("A", "C"), ("C", "A")):
        st = "arcVert" if (a, b) in arcs_verts else ("arcPale" if arcs_verts else "arc")
        code += f"  \\draw[{st}] ({a}) to[bend left=22] ({b});\n"
    return code


FIGURES["ex1142_graphe"] = r"""
\begin{tikzpicture}
""" + graphe_42() + r"""
\end{tikzpicture}"""

FIGURES["ex1142_chemins"] = r"""
\begin{tikzpicture}
""" + graphe_42(arcs_verts=(("A", "B"), ("B", "D"), ("A", "C"), ("C", "D")), verts=("A", "D")) + r"""
  \node[legende,anchor=north,text=otGreenDark] at (0,-0.55) {$A\to B\to D$ et $A\to C\to D$};
\end{tikzpicture}"""

# ------------------------------------------------------------- exercice 1138
POS_38 = {"A": (0, 3.2), "E": (3.6, 3.2), "D": (3.6, 0), "C": (0, 0), "B": (1.35, 1.6)}
ARCS_38 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A"), ("A", "C"), ("B", "D")]


def graphe_38(arcs_verts=(), verts=()):
    code = sommets(POS_38, verts=verts)
    for a, b in ARCS_38:
        st = "arcVert" if (a, b) in arcs_verts else ("arcPale" if arcs_verts else "arc")
        code += f"  \\draw[{st}] ({a}) -- ({b});\n"
    return code


FIGURES["ex1138_graphe"] = r"""
\begin{tikzpicture}
""" + graphe_38() + r"""
\end{tikzpicture}"""

FIGURES["ex1138_chemins"] = r"""
\begin{tikzpicture}
""" + graphe_38(arcs_verts=(("A", "B"), ("B", "D"), ("A", "C"), ("C", "D"), ("D", "E")), verts=("A", "E")) + r"""
  \node[legende,anchor=north,text=otGreenDark] at (1.8,-0.55) {$A\to B\to D\to E$ et $A\to C\to D\to E$};
\end{tikzpicture}"""


# ============================================================= FINITION 2026-11-02
# ------------------------------------------------------------- exercice 1134 : produit ligne × colonne
FIGURES["ex1134_produit"] = r"""
\begin{tikzpicture}
  \matrix (A) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=)] {2 & 3\\ 1 & 4\\};
  \node (fois) [right=3mm of A] {$\times$};
  \matrix (B) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=), right=3mm of fois] {1 & -1\\ 2 & 3\\};
  \node (egal) [right=3mm of B] {$=$};
  \matrix (C) [matrix of math nodes, nodes={coef}, left delimiter=(, right delimiter=), right=3mm of egal] {8 & 7\\ 9 & 11\\};
  \begin{scope}[on background layer]
    \fill[otSky,rounded corners=2pt] ($(A-1-1.north west)+(-0.5mm,0.3mm)$) rectangle ($(A-1-2.south east)+(0.5mm,-0.3mm)$);
    \fill[otGreen!25,rounded corners=2pt] ($(B-1-1.north west)+(-0.3mm,0.5mm)$) rectangle ($(B-2-1.south east)+(0.3mm,-0.5mm)$);
    \fill[otOrange!35,rounded corners=2pt] ($(C-1-1.north west)+(-0.3mm,0.3mm)$) rectangle ($(C-1-1.south east)+(0.3mm,-0.3mm)$);
  \end{scope}
  \node[legende,anchor=north,text=otNavy] at (A.south |- B.south) {ligne $1$ de $A$};
  \node[legende,anchor=north,text=otGreenDark] at (B.south) {colonne $1$ de $B$};
  \node[legende,anchor=north,text=otOrange!80!black] at (C.south |- B.south) {$(AB)_{11}$};
  \node[anchor=north,inner sep=0pt] at ($(B.south)+(0,-6.5mm)$) {$(AB)_{11}=2\times1+3\times2=8$};
\end{tikzpicture}"""


# ------------------------------------------------------------- graphes probabilistes
def markov_chaine3(etats, p, verts=()):
    """Trois états alignés ; p[(i, j)] = probabilité de transition (boucles comprises)."""
    a, b, c = etats
    code = (rf"  \node[{'sommetVert' if a in verts else 'sommet'}] ({a}) at (0,0) {{${a}$}};" + "\n"
            rf"  \node[{'sommetVert' if b in verts else 'sommet'}] ({b}) at (2.5,0) {{${b}$}};" + "\n"
            rf"  \node[{'sommetVert' if c in verts else 'sommet'}] ({c}) at (5.0,0) {{${c}$}};" + "\n")
    code += rf"  \draw[arc] ({a}) to[bend left=28] node[poids,midway,above] {{{p[(a, b)]}}} ({b});" + "\n"
    code += rf"  \draw[arc] ({b}) to[bend left=28] node[poids,midway,below] {{{p[(b, a)]}}} ({a});" + "\n"
    code += rf"  \draw[arc] ({b}) to[bend left=28] node[poids,midway,above] {{{p[(b, c)]}}} ({c});" + "\n"
    code += rf"  \draw[arc] ({c}) to[bend left=28] node[poids,midway,below] {{{p[(c, b)]}}} ({b});" + "\n"
    code += rf"  \draw[arc] ({a}.150) to[out=160,in=200,looseness=6] node[poids,midway,left] {{{p[(a, a)]}}} ({a}.210);" + "\n"
    code += rf"  \draw[arc] ({c}.30) to[out=20,in=-20,looseness=6] node[poids,midway,right] {{{p[(c, c)]}}} ({c}.-30);" + "\n"
    code += rf"  \draw[arc] ({b}.120) to[out=110,in=70,looseness=6] node[poids,midway,above] {{{p[(b, b)]}}} ({b}.60);" + "\n"
    return code


# exercice 1140 (réécrit) : refuges A, B, C
P40 = {("A", "A"): "0,7", ("A", "B"): "0,3", ("B", "A"): "0,2", ("B", "B"): "0,3", ("B", "C"): "0,5",
       ("C", "B"): "0,3", ("C", "C"): "0,7"}
FIGURES["ex1140_graphe"] = r"""
\begin{tikzpicture}
""" + markov_chaine3("ABC", P40) + r"""
\end{tikzpicture}"""


def distributions(P, pi0, n):
    res = [pi0]
    for _ in range(n):
        pi = res[-1]
        res.append([sum(pi[i] * P[i][j] for i in range(len(P))) for j in range(len(P))])
    return res


_D40 = distributions([[0.7, 0.3, 0], [0.2, 0.3, 0.5], [0, 0.3, 0.7]], [1, 0, 0], 12)


def nuage(valeurs, couleur):
    pts = " ".join(f"({k},{v:.5f})" for k, v in enumerate(valeurs))
    return rf"  \addplot[only marks, mark=*, mark size=1.9pt, {couleur}] coordinates {{{pts}}};" + "\n"


FIGURES["ex1140_convergence"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.0cm, height=4.4cm, xmin=-0.4, xmax=12.9, ymin=-0.06, ymax=1.12,
  xtick={2,4,6,8,10,12}, ytick={0.2,0.3,0.5,1}, yticklabels={$0{,}2$,$0{,}3$,$0{,}5$,$1$}, xlabel={$n$}, ylabel={}]
  \draw[seuil] (axis cs:0,0.5) -- (axis cs:12.3,0.5);
  \draw[seuil] (axis cs:0,0.3) -- (axis cs:12.3,0.3);
  \draw[seuil] (axis cs:0,0.2) -- (axis cs:12.3,0.2);
""" + nuage([d[0] for d in _D40], "otNavy") + nuage([d[1] for d in _D40], "otOrange!90!black") + nuage([d[2] for d in _D40], "otGreenDark") + r"""
  \node[note,anchor=west,text=otMuted] at (axis cs:1.3,0.95) {le randonneur part du refuge $A$};
  \node[note,anchor=west,text=otNavy] at (axis cs:12.6,0.2) {$P(X_n = A)$};
  \node[note,anchor=west,text=otGreenDark] at (axis cs:12.6,0.5) {$P(X_n = C)$};
  \node[note,anchor=west,text=otOrange!80!black] at (axis cs:12.6,0.3) {$P(X_n = B)$};
\end{axis}
\end{tikzpicture}"""

# nouveau-1 : météo à deux états B (beau) et M (mauvais)
FIGURES["n1_graphe"] = r"""
\begin{tikzpicture}
  \node[sommet] (B) at (0,0) {$B$};
  \node[sommet] (M) at (3.8,0) {$M$};
  \draw[arc] (B) to[bend left=28] node[poids,midway,above] {0,1} (M);
  \draw[arc] (M) to[bend left=28] node[poids,midway,below] {0,4} (B);
  \draw[arc] (B.150) to[out=160,in=200,looseness=6] node[poids,midway,left] {0,9} (B.210);
  \draw[arc] (M.30) to[out=20,in=-20,looseness=6] node[poids,midway,right] {0,6} (M.-30);
\end{tikzpicture}"""

# nouveau-2 : graphe non orienté à cinq sommets
POS_N2 = {"A": (0, 1.5), "B": (1.7, 3.0), "C": (1.7, 0), "D": (3.4, 1.5), "E": (5.3, 1.5)}
ARETES_N2 = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("D", "E")]


def graphe_n2(vertes=(), verts=()):
    code = sommets(POS_N2, verts=verts)
    for a, b in ARETES_N2:
        st = "areteVerte" if (a, b) in vertes else ("arete,otNavy!30" if vertes else "arete")
        code += f"  \\draw[{st}] ({a}) -- ({b});\n"
    return code


FIGURES["n2_graphe"] = r"""
\begin{tikzpicture}
""" + graphe_n2() + r"""
\end{tikzpicture}"""

FIGURES["n2_chaines"] = r"""
\begin{tikzpicture}
""" + graphe_n2(vertes=(("A", "B"), ("B", "D"), ("A", "C"), ("C", "D"), ("D", "E")), verts=("A", "E")) + r"""
  \node[legende,anchor=north,text=otGreenDark] at (2.65,-0.55) {$A - B - D - E$ et $A - C - D - E$};
\end{tikzpicture}"""

# nouveau-3 : adhérents des deux antennes (en centaines), U(n+1) = A U(n) + C
_AN = [30 - 15 * 0.8 ** n - 5 * 0.4 ** n for n in range(16)]
_BN = [20 - 15 * 0.8 ** n + 5 * 0.4 ** n for n in range(16)]
FIGURES["n3_convergence"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.8cm, height=4.4cm, xmin=-0.4, xmax=16.2, ymin=0, ymax=34,
  xtick={2,4,6,8,10,12,14}, ytick={10,20,30}, xlabel={$n$}, ylabel={}]
  \draw[seuil] (axis cs:0,30) -- (axis cs:15.4,30);
  \draw[seuil] (axis cs:0,20) -- (axis cs:15.4,20);
""" + nuage(_AN, "otNavy") + nuage(_BN, "otGreenDark") + r"""
  \node[note,anchor=north west,text=otNavy] at (axis cs:9,25.2) {$a_n$ (Lyon)};
  \node[note,anchor=north west,text=otGreenDark] at (axis cs:9,16.2) {$b_n$ (Lille)};
\end{axis}
\end{tikzpicture}"""
