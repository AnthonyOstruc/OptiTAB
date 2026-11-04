# -*- coding: utf-8 -*-
"""Figures de la notion 102 « Nombres complexes » (style des livres OptiTAB).

Compilation : python ../../../outils/figures_livre.py <dossier_notion> [noms…] [--planche]
Plan complexe : grille légère, axes otMuted, points et vecteurs otNavy / otGreen,
angles otOrange ; éléments de réponse en vert (otGreenDark).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  grille/.style={otRule!75,line width=0.35pt,step=1},
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.2pt},
  lab/.style={font=\normalsize,inner sep=1.5pt,text=otInk},
  vec/.style={line width=1.1pt,-{Stealth[length=2.4mm]}},
  ang/.style={otOrange,line width=0.9pt,-{Stealth[length=1.7mm]}},
  pointille/.style={otMuted,line width=0.5pt,dash pattern=on 2pt off 1.6pt},
}
\newcommand{\pz}[2][otNavy]{\fill[#1] (#2) circle (2.2pt);}
\newcommand{\pzv}[2][otNavy]{\draw[#1,fill=white,line width=0.9pt] (#2) circle (2.4pt);}
"""


def repere(xmin, xmax, ymin, ymax, unite, grille=None, tx=(), ty=(), O=True):
    """Début d'un plan complexe : grille, axes, graduations (tx, ty : (valeur, texte, ancre))."""
    s = rf"\begin{{tikzpicture}}[x={unite}cm,y={unite}cm,line cap=round,line join=round]" + "\n"
    if grille:
        gx0, gy0, gx1, gy1 = grille
        s += rf"\draw[grille] ({gx0},{gy0}) grid ({gx1},{gy1});" + "\n"
    s += rf"\draw[axe] ({xmin},0) -- ({xmax},0);" + "\n"
    s += rf"\draw[axe] (0,{ymin}) -- (0,{ymax});" + "\n"
    if O:
        s += r"\node[lab,text=otMuted,anchor=north east] at (-0.02,-0.02) {$O$};" + "\n"
    for v, t, a in tx:
        s += rf"\draw[otMuted,line width=0.5pt] ({v},0) ++(0,-2pt) -- ++(0,4pt);" + "\n"
        s += rf"\node[grad,anchor={a or 'north'}] at ({v},0) [yshift=-2.5pt] {{$\displaystyle {t}$}};" + "\n"
    for v, t, a in ty:
        s += rf"\draw[otMuted,line width=0.5pt] (0,{v}) ++(-2pt,0) -- ++(4pt,0);" + "\n"
        s += rf"\node[grad,anchor={a or 'east'}] at (0,{v}) [xshift=-2.5pt] {{$\displaystyle {t}$}};" + "\n"
    return s


FIN = "\\end{tikzpicture}"

FIGURES = {}

# =============================================================== COURS
FIGURES["c_affixe"] = repere(-1.2, 4.6, -2.7, 3.0, 1, grille=(-1, -2, 4, 2.6), O=True) + r"""
\draw[pointille] (3,0) -- (3,2) -- (0,2);
\draw[pointille] (3,0) -- (3,-2) -- (0,-2);
\draw[vec,otGreen] (0,0) -- (3,2);
\draw[vec,otNavy] (0,0) -- (1,0);
\draw[vec,otNavy] (0,0) -- (0,1);
\node[lab,text=otNavy,anchor=north] at (0.5,-0.06) {$\vec{u}$};
\node[lab,text=otNavy,anchor=east] at (-0.06,0.55) {$\vec{v}$};
\pz{3,2} \pz[otGreenDark]{3,-2}
\node[lab,text=otNavy,anchor=south west] at (3.04,2.04) {$M(z)$};
\node[lab,text=otGreenDark,anchor=north west] at (3.04,-2.04) {$M'(\overline{z})$};
\node[lab,text=otMuted,anchor=south west] at (3.05,0.05) {$x$};
\node[lab,text=otMuted,anchor=east] at (-0.06,2) {$y$};
\node[lab,text=otMuted,anchor=east] at (-0.06,-2) {$-y$};
\node[note,anchor=north east] at (4.55,-0.1) {axe réel};
\node[note,anchor=north west] at (0.12,2.95) {axe imaginaire};
""" + FIN

FIGURES["c_module_argument"] = repere(-0.6, 4.5, -0.6, 3.0, 1, grille=(-0.5, -0.5, 4, 2.6)) + r"""
\draw[pointille] (3.2,0) -- (3.2,2.1) -- (0,2.1);
\draw[vec,otNavy] (0,0) -- (3.2,2.1);
\draw[ang] (1,0) arc (0:33.27:1);
\node[lab,text=otOrange!80!black] at (16.6:1.33) {$\theta$};
\pz{3.2,2.1}
\node[lab,text=otNavy,anchor=south west] at (3.24,2.14) {$M(z)$};
\node[lab,text=otNavy,anchor=south east] at (1.5,1.1) {$r = |z|$};
\node[lab,text=otMuted,anchor=north] at (3.2,-0.08) {$x = r\cos\theta$};
\node[lab,text=otMuted,anchor=east] at (-0.08,2.1) {$y = r\sin\theta$};
""" + FIN

FIGURES["c_lieux"] = r"""\begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
\draw[otGreenDark,line width=1.2pt] (1.5,1.5) circle (1.2);
\draw[otMuted,line width=0.8pt] (1.5,1.5) -- (2.539,2.1);
\pz{1.5,1.5} \pz{0.729,2.419}
\node[lab,text=otNavy,anchor=north] at (1.5,1.42) {$\Omega$};
\node[lab,text=otMuted,anchor=south east] at (2.0,1.84) {$r$};
\node[lab,text=otNavy,anchor=south east] at (0.69,2.46) {$M$};
\node[lab,text=otNavy,anchor=north] at (1.5,-0.25) {$|z - \omega| = r$};
\begin{scope}[xshift=4.3cm]
\draw[otGreenDark,line width=1.2pt] (2.0,-0.2) -- (0.884,2.477);
\draw[otNavy,line width=0.9pt] (0.3,0.5) -- (2.7,1.5);
\draw[pointille] (1.057,2.062) -- (0.3,0.5) (1.057,2.062) -- (2.7,1.5);
\coordinate (A) at (0.3,0.5); \coordinate (B) at (2.7,1.5); \coordinate (I) at (1.5,1.0); \coordinate (M) at (1.057,2.062);
\angledroit{B}{I}{M}
\codage{A}{I} \codage{I}{B}
\codage[2]{M}{A} \codage[2]{M}{B}
\pz{0.3,0.5} \pz{2.7,1.5} \pz{1.057,2.062}
\node[lab,text=otNavy,anchor=north east] at (0.27,0.47) {$A$};
\node[lab,text=otNavy,anchor=west] at (2.78,1.5) {$B$};
\node[lab,text=otNavy,anchor=south west] at (1.12,2.12) {$M$};
\node[lab,text=otNavy,anchor=north] at (1.5,-0.25) {$|z - a| = |z - b|$};
\end{scope}
""" + FIN

FIGURES["c_addition"] = r"""\begin{tikzpicture}[x=2.2cm,y=2.2cm,line cap=round,line join=round]
\draw[axe] (-1.25,0) -- (1.4,0);
\draw[axe] (0,-1.2) -- (0,1.38);
\draw[otMuted,line width=0.7pt] (0,0) circle (1);
\draw[vec,otNavy] (0,0) -- (25:1);
\draw[vec,otGreen] (0,0) -- (80:1);
\draw[ang] (0.42,0) arc (0:25:0.42);
\draw[otGreenDark,line width=0.9pt,-{Stealth[length=1.7mm]}] (25:0.3) arc (25:80:0.3);
\node[lab,text=otOrange!80!black] at (12.5:0.62) {$a$};
\node[lab,text=otGreenDark] at (52.5:0.5) {$b - a$};
\pz{25:1} \pz[otGreenDark]{80:1}
\node[lab,text=otNavy,anchor=west] at ($(25:1)+(0.04,0)$) {$A(\cos a\,;\sin a)$};
\node[lab,text=otGreenDark,anchor=south west] at ($(80:1)+(0.04,0.05)$) {$B(\cos b\,;\sin b)$};
\node[lab,text=otMuted,anchor=north east] at (-0.01,-0.01) {$O$};
""" + FIN

FIGURES["c_produit"] = repere(-0.5, 2.5, -0.4, 4.6, 1.15, grille=(-0.4, -0.3, 2.4, 4.4)) + r"""
\draw[otOrange,line width=1.5pt,-{Stealth[length=2.6mm]}] (0,0) -- (0,4);
\draw[vec,otNavy] (0,0) -- (1.732,1);
\draw[vec,otGreen] (0,0) -- (1,1.732);
\draw[otNavy,line width=0.9pt] (0.7,0) arc (0:30:0.7);
\draw[otGreenDark,line width=0.9pt,-{Stealth[length=1.7mm]}] (30:0.7) arc (30:90:0.7);
\node[lab,text=otNavy] at (14:1.2) {$\frac{\pi}{6}$};
\node[lab,text=otGreenDark] at (76:1.2) {$\frac{\pi}{3}$};
\pz{1.732,1} \pz[otGreenDark]{1,1.732} \pz[otOrange]{0,4}
\node[lab,text=otNavy,anchor=west] at (1.8,1) {$z = \sqrt{3} + \mathrm{i}$};
\node[lab,text=otGreenDark,anchor=west] at (1.07,1.76) {$z' = 1 + \mathrm{i}\sqrt{3}$};
\node[lab,text=otOrange!80!black,anchor=west] at (0.08,4.05) {$zz' = 4\mathrm{i}$};
\node[note,anchor=west] at (0.45,3.35) {modules : $2 \times 2 = 4$};
\node[note,anchor=west] at (0.45,2.9) {arguments : $\frac{\pi}{6} + \frac{\pi}{3} = \frac{\pi}{2}$};
""" + FIN

FIGURES["c_racines_p"] = repere(-0.7, 2.5, -1.55, 1.6, 1.1, grille=(-0.5, -1.4, 2.3, 1.4),
                                ty=((1, "1", None), (-1, "-1", None))) + r"""
\draw[pointille] (1,1) -- (1,-1);
\pz{1,0} \pz[otGreenDark]{1,1} \pz[otGreenDark]{1,-1}
\node[lab,text=otNavy,anchor=south west] at (1.05,0.04) {$1$};
\node[lab,text=otGreenDark,anchor=west] at (1.08,1) {$1 + \mathrm{i}$};
\node[lab,text=otGreenDark,anchor=west] at (1.08,-1) {$1 - \mathrm{i}$};
""" + FIN

FIGURES["c_quotient"] = repere(-1.8, 3.9, -0.5, 5.8, 0.72, grille=(-1.5, -0.4, 3.6, 5.6),
                               tx=((1, "1", None),), ty=((1, "1", None),)) + r"""
\coordinate (A) at (1,1); \coordinate (B) at (3,2); \coordinate (C) at (-1,5);
\draw[otMuted,line width=0.6pt] (B) -- (C);
\draw[vec,otNavy] (A) -- (B);
\draw[vec,otGreen] (A) -- (C);
\angledroit{B}{A}{C}
\draw[ang] ($(A)+(26.57:0.75)$) arc (26.57:116.57:0.75);
\node[lab,text=otOrange!80!black] at ($(A)+(71.57:1.2)$) {$\frac{\pi}{2}$};
\pz{1,1} \pz{3,2} \pz[otGreenDark]{-1,5}
\node[lab,text=otNavy,anchor=north west] at (1.06,0.94) {$A$};
\node[lab,text=otNavy,anchor=west] at (3.08,2) {$B$};
\node[lab,text=otGreenDark,anchor=south east] at (-1.04,5.04) {$C$};
\node[note,anchor=west] at (1.4,4.6) {$AC = 2AB$};
""" + FIN


def polygone(n, etiquettes, titre, couleur="otNavy"):
    pts = " -- ".join(f"({360 * k / n:.4f}:1)" for k in range(n))
    s = rf"\fill[otSky] {pts} -- cycle;" + "\n"
    s += r"\draw[axe] (-1.25,0) -- (1.32,0); \draw[axe] (0,-1.25) -- (0,1.38);" + "\n"
    s += r"\draw[otMuted,line width=0.6pt] (0,0) circle (1);" + "\n"
    s += rf"\draw[{couleur},line width=1.1pt] {pts} -- cycle;" + "\n"
    for k in range(n):
        s += rf"\fill[{couleur}] ({360 * k / n:.4f}:1) circle (2.2pt);" + "\n"
    for ang, texte, ancre, dx, dy in etiquettes:
        s += rf"\node[lab,text={couleur},anchor={ancre}] at ($({ang}:1)+({dx},{dy})$) {{{texte}}};" + "\n"
    s += rf"\node[lab,text=otInk,anchor=north] at (0,-1.38) {{{titre}}};" + "\n"
    return s


FIGURES["c_racines_unite"] = r"""\begin{tikzpicture}[x=1.0cm,y=1.0cm,line cap=round,line join=round]
""" + polygone(3, [(0, "$1$", "south west", 0.03, 0.03), (120, "$j$", "south east", -0.02, 0.03),
                   (240, "$j^2$", "north east", -0.02, -0.03)], "$n = 3$") + r"""
\begin{scope}[xshift=3.22cm]
""" + polygone(4, [(0, "$1$", "south west", 0.03, 0.03), (90, r"$\mathrm{i}$", "south west", 0.04, 0.03),
                   (180, "$-1$", "south east", -0.03, 0.03), (270, r"$-\mathrm{i}$", "north west", 0.04, -0.03)],
               "$n = 4$") + r"""
\end{scope}
\begin{scope}[xshift=6.44cm]
""" + polygone(6, [(0, "$1$", "south west", 0.03, 0.03), (60, r"$\mathrm{e}^{\mathrm{i}\frac{\pi}{3}}$", "south west", 0.02, 0.02)],
               "$n = 6$") + r"""
\end{scope}
""" + FIN

# =============================================================== EXERCICE 1133 (DS transformation)
FIGURES["ds_points"] = repere(-2.8, 2.9, -0.6, 3.8, 0.95, grille=(-2.5, -0.5, 2.5, 3.5),
                              tx=((-2, "-2", None), (-1, "-1", None), (1, "1", None), (2, "2", None)),
                              ty=((1, "1", None), (2, "2", None), (3, "3", None))) + r"""
\pz{0,1} \pz{2,1} \pz{-1,3}
\pz[otGreenDark]{-0.3333,0} \pz[otGreenDark]{1.6667,0} \pz[otGreenDark]{-2,0}
\node[lab,text=otNavy,anchor=south west] at (0.06,1.06) {$A$};
\node[lab,text=otNavy,anchor=south west] at (2.04,1.04) {$B$};
\node[lab,text=otNavy,anchor=south west] at (-0.96,3.04) {$C$};
\node[lab,text=otGreenDark,anchor=south east] at (-0.38,0.06) {$A'$};
\node[lab,text=otGreenDark,anchor=south] at (1.6667,0.08) {$B'$};
\node[lab,text=otGreenDark,anchor=south] at (-2,0.08) {$C'$};
""" + FIN

FIGURES["ds_construction"] = r"""\begin{tikzpicture}[x=0.9cm,y=0.9cm,line cap=round,line join=round]
\draw[grille] (-1.5,-1) grid (4,3.4);
\draw[otGreen,line width=3.2pt,opacity=0.6] (-1.6,0) -- (4.2,0);
\draw[axe] (-1.7,0) -- (4.6,0);
\draw[axe] (0,-1.1) -- (0,3.7);
\node[lab,text=otMuted,anchor=north east] at (-0.02,-0.02) {$O$};
\draw[otMuted,line width=0.5pt] (1,0) ++(0,-2pt) -- ++(0,4pt);
\node[grad,anchor=north] at (1,0) [yshift=-2.5pt] {$1$};
\draw[otMuted,line width=0.5pt] (0,1) ++(-2pt,0) -- ++(4pt,0);
\node[grad,anchor=east] at (0,1) [xshift=-2.5pt] {$1$};
\draw[vec,otOrange] (0,0) -- (1,3);
\node[lab,text=otOrange!80!black,anchor=east] at (0.4,1.65) {$\vec{w}$};
\draw[otNavy,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (2.0833,-0.75) -- (3.2,2.6);
\draw[otGreenDark,line width=1pt,-{Stealth[length=2.2mm]}] (3,2) -- (2.4,0.2);
\pz{3,2} \pz[otGreenDark]{2.3333,0}
\node[lab,text=otNavy,anchor=west] at (3.08,2) {$N$};
\node[lab,text=otGreenDark,anchor=north west] at (2.42,-0.08) {$N'$};
\node[lab,text=otGreenDark,anchor=south east] at (4.25,0.1) {$\mathscr{D}$};
""" + FIN

# =============================================================== EXERCICE 963 (ensembles de points)
FIGURES["lieux_e1"] = repere(-2.6, 6.8, -1.6, 7.8, 0.5, grille=(-2.5, -1.5, 6.5, 7.5), O=False,
                             tx=((1, "1", None),), ty=((1, "1", None),)) + r"""
\draw[otGreenDark,line width=1.3pt] (2,3) circle (4);
\draw[otMuted,line width=0.8pt] (2,3) -- (6,3);
\pz{2,3}
\node[lab,text=otNavy,anchor=north] at (2,2.9) {$\Omega$};
\node[lab,text=otMuted,anchor=south] at (4,3.08) {$4$};
\node[lab,text=otGreenDark,anchor=south west] at (4.9,5.9) {$\mathcal{E}_1$};
""" + FIN

FIGURES["lieux_e2"] = repere(-2.7, 2.3, -1.9, 2.9, 0.85, grille=(-2.5, -1.8, 2, 2.6), O=False,
                             tx=((1, "1", None),), ty=((1, "1", None),)) + r"""
\coordinate (A) at (1,-1); \coordinate (B) at (-2,1); \coordinate (I) at (-0.5,0); \coordinate (P) at (0.0547,0.832);
\draw[otGreenDark,line width=1.3pt] (-1.6,-1.65) -- (1.15,2.475);
\draw[otNavy,line width=0.8pt] (A) -- (B);
\angledroit{A}{I}{P}
\codage{A}{I} \codage{I}{B}
\pz{1,-1} \pz{-2,1}
\node[lab,text=otNavy,anchor=west] at (1.08,-1) {$A$};
\node[lab,text=otNavy,anchor=east] at (-2.08,1) {$B$};
\node[lab,text=otGreenDark,anchor=west] at (1.22,2.42) {$\mathcal{E}_2$};
""" + FIN

FIGURES["lieux_e3"] = repere(-1.2, 3.3, -0.6, 4.1, 0.9, grille=(-1, -0.5, 3, 3.9),
                             tx=((1, "1", None),)) + r"""
\draw[pointille] (0,1) -- (1.5,1);
\draw[otGreenDark,line width=1.3pt] (0,1) -- (2.8,3.8);
\draw[ang] (0.7,1) arc (0:45:0.7);
\node[lab,text=otOrange!80!black] at ($(0,1)+(22.5:1.2)$) {$\frac{\pi}{4}$};
\pzv[otGreenDark]{0,1}
\node[lab,text=otNavy,anchor=east] at (-0.1,1) {$\Omega$};
\node[lab,text=otGreenDark,anchor=north west] at (2.15,2.9) {$\mathcal{E}_3$};
""" + FIN

FIGURES["lieux_e5"] = repere(-0.7, 2.6, -1.35, 1.45, 1.2, grille=(-0.5, -1.2, 2.4, 1.3),
                             tx=((2, "2", "north west"),)) + r"""
\draw[otGreenDark,line width=1.3pt] (1,0) circle (1);
\draw[otMuted,line width=0.8pt] (1,0) -- (1.5,0.866);
\pz{1,0}
\node[lab,text=otNavy,anchor=north] at (1,-0.06) {$\Omega'$};
\node[lab,text=otMuted,anchor=south east] at (1.2,0.46) {$1$};
\node[lab,text=otGreenDark,anchor=south west] at (1.74,0.74) {$\mathcal{E}_5$};
""" + FIN

# =============================================================== EXERCICE 958 (second degré)
FIGURES["second_degre_sol"] = repere(-3.0, 3.6, -3.6, 3.8, 0.7, grille=(-3, -3.5, 3.5, 3.5),
                                     ty=((1, "1", None),)) + r"""
% graduation 1 de l'axe réel : décalée à gauche du pointillé vertical x = 1
\draw[otMuted,line width=0.5pt] (1,0) ++(0,-2pt) -- ++(0,4pt);
\node[grad,anchor=north east] at (1,0) [xshift=-3.5pt,yshift=-2.5pt] {$1$};
\draw[pointille] (1,2) -- (1,-2) (-2,3) -- (-2,-3) (1.5,0.5) -- (1.5,-0.5);
\pz{1,2} \pz{1,-2}
\pz[otGreenDark]{-2,3} \pz[otGreenDark]{-2,-3}
\pz[otOrange]{1.5,0.5} \pz[otOrange]{1.5,-0.5}
\node[lab,text=otNavy,anchor=west] at (1.1,2) {$1 + 2\mathrm{i}$};
\node[lab,text=otNavy,anchor=west] at (1.1,-2) {$1 - 2\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=east] at (-2.1,3) {$-2 + 3\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=east] at (-2.1,-3) {$-2 - 3\mathrm{i}$};
\node[lab,text=otOrange!80!black,anchor=west] at (1.6,0.55) {$\frac{3}{2} + \frac{1}{2}\mathrm{i}$};
\node[lab,text=otOrange!80!black,anchor=west] at (1.6,-0.55) {$\frac{3}{2} - \frac{1}{2}\mathrm{i}$};
""" + FIN

# =============================================================== EXERCICE 961 (forme exponentielle)
FIGURES["expo_z1"] = repere(-2.5, 2.6, -0.5, 2.5, 1.0, grille=(-2.4, -0.4, 2.4, 2.4),
                            tx=((-1, "-1", None), (2, "2", "north west")), O=True) + r"""
\draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] (2,0) arc (0:180:2);
\draw[pointille] (-1,0) -- (-1,1.732) -- (0,1.732);
\draw[vec,otNavy] (0,0) -- (-1,1.732);
\draw[ang] (0.6,0) arc (0:120:0.6);
\node[lab,text=otOrange!80!black] at (52:1.02) {$\frac{2\pi}{3}$};
\pz{-1,1.732}
\node[lab,text=otNavy,anchor=south east] at (-1.1,1.8) {$z_1$};
\node[lab,text=otNavy,anchor=north east] at (-0.58,0.8) {$2$};
\node[lab,text=otMuted,anchor=west] at (0.08,1.732) {$\sqrt{3}$};
""" + FIN

# =============================================================== EXERCICE 956 (forme trigonométrique)
FIGURES["trigo_z1z2"] = r"""\begin{tikzpicture}[x=1.15cm,y=1.15cm,line cap=round,line join=round]
\draw[grille] (-0.3,-0.3) grid (1.6,1.5);
\draw[axe] (-0.4,0) -- (1.75,0); \draw[axe] (0,-0.4) -- (0,1.65);
\node[lab,text=otMuted,anchor=north east] at (-0.02,-0.02) {$O$};
\draw[pointille] (1,0) -- (1,1) -- (0,1);
\draw[vec,otNavy] (0,0) -- (1,1);
\draw[ang] (0.5,0) arc (0:45:0.5);
\node[lab,text=otOrange!80!black] at (22:0.88) {$\frac{\pi}{4}$};
\pz{1,1}
\node[lab,text=otNavy,anchor=south west] at (1.04,1.04) {$z_1 = 1 + \mathrm{i}$};
\node[lab,text=otNavy,anchor=south east] at (0.42,0.5) {$\sqrt{2}$};
\node[grad,anchor=north] at (1,-0.06) {$1$};
\node[grad,anchor=east] at (-0.06,1) {$1$};
\begin{scope}[xshift=3.6cm]
\draw[grille] (-0.3,-0.3) grid (2.1,1.5);
\draw[axe] (-0.4,0) -- (2.25,0); \draw[axe] (0,-0.4) -- (0,1.65);
\node[lab,text=otMuted,anchor=north east] at (-0.02,-0.02) {$O$};
\draw[pointille] (1.732,0) -- (1.732,1) -- (0,1);
\draw[vec,otNavy] (0,0) -- (1.732,1);
\draw[ang] (0.6,0) arc (0:30:0.6);
\node[lab,text=otOrange!80!black] at (14:1.08) {$\frac{\pi}{6}$};
\pz{1.732,1}
\node[lab,text=otNavy,anchor=south west] at (1.77,1.04) {$z_2 = \sqrt{3} + \mathrm{i}$};
\node[lab,text=otNavy,anchor=south east] at (0.82,0.52) {$2$};
\node[grad,anchor=north] at (1.732,-0.06) {$\sqrt{3}$};
\node[grad,anchor=east] at (-0.06,1) {$1$};
\end{scope}
""" + FIN

FIGURES["trigo_z3z4"] = r"""\begin{tikzpicture}[x=0.95cm,y=0.95cm,line cap=round,line join=round]
\draw[grille] (-2.4,-0.3) grid (0.7,2.5);
\draw[axe] (-2.5,0) -- (0.9,0); \draw[axe] (0,-0.4) -- (0,2.65);
\node[lab,text=otMuted,anchor=north west] at (0.02,-0.02) {$O$};
\draw[pointille] (-2,0) -- (-2,2) -- (0,2);
\draw[vec,otNavy] (0,0) -- (-2,2);
\draw[ang] (0.55,0) arc (0:135:0.55);
\node[lab,text=otOrange!80!black] at (58:1.0) {$\frac{3\pi}{4}$};
\pz{-2,2}
\node[lab,text=otNavy,anchor=south east] at (-2.04,2.04) {$z_3$};
\node[lab,text=otNavy,anchor=north east] at (-1.08,0.92) {$2\sqrt{2}$};
\node[grad,anchor=north] at (-2,-0.06) {$-2$};
\node[grad,anchor=west] at (0.06,2) {$2$};
\begin{scope}[xshift=4.3cm]
\draw[grille] (-2.2,-0.3) grid (0.7,1.6);
\draw[axe] (-2.3,0) -- (0.9,0); \draw[axe] (0,-0.4) -- (0,1.8);
\node[lab,text=otMuted,anchor=north west] at (0.02,-0.02) {$O$};
\draw[pointille] (-1.732,0) -- (-1.732,1) -- (0,1);
\draw[vec,otNavy] (0,0) -- (-1.732,1);
\draw[ang] (0.55,0) arc (0:150:0.55);
\node[lab,text=otOrange!80!black] at (55:1.0) {$\frac{5\pi}{6}$};
\pz{-1.732,1}
\node[lab,text=otNavy,anchor=south east] at (-1.77,1.04) {$z_4$};
\node[lab,text=otNavy,anchor=north east] at (-0.95,0.42) {$2$};
\node[grad,anchor=north] at (-1.732,-0.06) {$-\sqrt{3}$};
\node[grad,anchor=west] at (0.06,1) {$1$};
\end{scope}
""" + FIN

# =============================================================== EXERCICE 960 (racines de l'unité)
FIGURES["unite_n3"] = r"""\begin{tikzpicture}[x=1.6cm,y=1.6cm,line cap=round,line join=round]
\fill[otSky] (0:1) -- (120:1) -- (240:1) -- cycle;
\draw[axe] (-1.3,0) -- (1.42,0); \draw[axe] (0,-1.3) -- (0,1.42);
\draw[otMuted,line width=0.6pt] (0,0) circle (1);
\draw[otNavy,line width=1.1pt] (0:1) -- (120:1) -- (240:1) -- cycle;
\fill[otNavy] (0:1) circle (2.2pt); \fill[otGreenDark] (120:1) circle (2.2pt); \fill[otGreenDark] (240:1) circle (2.2pt);
\node[lab,text=otNavy,anchor=south west] at (1.03,0.03) {$1$};
\node[lab,text=otGreenDark,anchor=south east] at ($(120:1)+(-0.03,0.03)$) {$j = -\frac{1}{2} + \frac{\sqrt{3}}{2}\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=north east] at ($(240:1)+(-0.03,-0.03)$) {$j^2 = -\frac{1}{2} - \frac{\sqrt{3}}{2}\mathrm{i}$};
\node[grad,anchor=north east] at (-0.53,-0.03) {$-\frac{1}{2}$};
""" + FIN

FIGURES["unite_n4"] = r"""\begin{tikzpicture}[x=1.6cm,y=1.6cm,line cap=round,line join=round]
\fill[otSky] (0:1) -- (90:1) -- (180:1) -- (270:1) -- cycle;
\draw[axe] (-1.35,0) -- (1.42,0); \draw[axe] (0,-1.35) -- (0,1.42);
\draw[otMuted,line width=0.6pt] (0,0) circle (1);
\draw[otNavy,line width=1.1pt] (0:1) -- (90:1) -- (180:1) -- (270:1) -- cycle;
\foreach \a in {0,90,180,270} {\fill[otNavy] (\a:1) circle (2.2pt);}
\node[lab,text=otNavy,anchor=south west] at (1.03,0.03) {$1$};
\node[lab,text=otNavy,anchor=south west] at (0.04,1.03) {$\mathrm{i}$};
\node[lab,text=otNavy,anchor=south east] at (-1.03,0.03) {$-1$};
\node[lab,text=otNavy,anchor=north west] at (0.04,-1.03) {$-\mathrm{i}$};
""" + FIN

FIGURES["cubique_moins8"] = repere(-2.7, 2.8, -2.4, 2.5, 0.85, grille=None,
                                   tx=((2, "2", "north west"),)) + r"""
\fill[otGreen!18] (60:2) -- (180:2) -- (300:2) -- cycle;
\draw[otMuted,line width=0.6pt] (0,0) circle (2);
\draw[otGreenDark,line width=1.1pt] (60:2) -- (180:2) -- (300:2) -- cycle;
\pz[otGreenDark]{60:2} \pz[otGreenDark]{180:2} \pz[otGreenDark]{300:2}
\node[lab,text=otGreenDark,anchor=south west] at ($(60:2)+(0.04,0.04)$) {$1 + \mathrm{i}\sqrt{3}$};
\node[lab,text=otGreenDark,anchor=south east] at (-2.04,0.04) {$-2$};
\node[lab,text=otGreenDark,anchor=north west] at ($(300:2)+(0.04,-0.04)$) {$1 - \mathrm{i}\sqrt{3}$};
""" + FIN

# =============================================================== EXERCICE 962 (angles orientés)
FIGURES["angles_abc"] = r"""\begin{tikzpicture}[x=1.7cm,y=1.7cm,line cap=round,line join=round]
\coordinate (A) at (1,0); \coordinate (B) at (0,1); \coordinate (C) at (0,-1);
\fill[otSky] (A) -- (B) -- (C) -- cycle;
\draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] (0,0) circle (1);
\draw[axe] (-1.3,0) -- (1.5,0); \draw[axe] (0,-1.3) -- (0,1.45);
\draw[otNavy,line width=1.1pt] (A) -- (B) -- (C) -- cycle;
\angledroit{B}{A}{C}
\codage{A}{B} \codage{A}{C}
\draw[ang] ($(A)+(225:0.34)$) arc (225:135:0.34);
\node[lab,text=otOrange!80!black,anchor=south] at (0.42,0.06) {$-\frac{\pi}{2}$};
\pz{1,0} \pz{0,1} \pz{0,-1}
\node[lab,text=otNavy,anchor=south west] at (1.03,0.03) {$A$};
\node[lab,text=otNavy,anchor=south west] at (0.05,1.06) {$B$};
\node[lab,text=otNavy,anchor=north west] at (0.05,-1.06) {$C$};
""" + FIN

FIGURES["angles_abm"] = r"""\begin{tikzpicture}[x=1.7cm,y=1.7cm,line cap=round,line join=round]
\coordinate (A) at (1,0); \coordinate (B) at (0,1); \coordinate (M) at (-0.366,-0.366);
\fill[otGreen!15] (A) -- (B) -- (M) -- cycle;
\draw[axe] (-1.0,0) -- (1.5,0); \draw[axe] (0,-0.9) -- (0,1.45);
\draw[otNavy,line width=1.1pt] (A) -- (B);
\draw[otGreenDark,line width=1.1pt] (B) -- (M) -- (A);
\codage{A}{B} \codage{B}{M} \codage{M}{A}
\draw[ang] ($(A)+(135:0.4)$) arc (135:195:0.4);
\node[lab,text=otOrange!80!black] at ($(A)+(152:0.8)$) {$\frac{\pi}{3}$};
\pz{1,0} \pz{0,1} \pz[otGreenDark]{-0.366,-0.366}
\node[lab,text=otNavy,anchor=south west] at (1.03,0.03) {$A$};
\node[lab,text=otNavy,anchor=south west] at (0.05,1.04) {$B$};
\node[lab,text=otGreenDark,anchor=north east] at (-0.4,-0.4) {$M$};
""" + FIN

# =============================================================== EXERCICE 959 (cercle, médiatrice, parallélogramme)
FIGURES["transfo_cercle_med"] = repere(-2.6, 5.7, -1.8, 5.8, 0.55, grille=(-2.5, -1.5, 5.5, 5.5),
                                       ty=((1, "1", None),)) + r"""
% graduation 1 de l'axe réel : au-dessus de l'axe (la droite Δ passe juste en dessous)
\draw[otMuted,line width=0.5pt] (1,0) ++(0,-2pt) -- ++(0,4pt);
\node[grad,anchor=south east] at (1,0) [xshift=-1.5pt,yshift=2pt] {$1$};
\coordinate (A) at (1,2); \coordinate (B) at (3,-1); \coordinate (I) at (2,0.5); \coordinate (P) at (2.832,1.055);
\draw[otGreenDark,line width=1.3pt] (A) circle (3);
\draw[otOrange,line width=1.3pt] (-1,-1.5) -- (5.3,2.7);
\draw[otNavy,line width=0.8pt] (A) -- (B);
\draw[otMuted,line width=0.8pt] (A) -- (1,5);
\angledroit{B}{I}{P}
\codage{A}{I} \codage{I}{B}
\pz{1,2} \pz{3,-1}
\node[lab,text=otNavy,anchor=north east] at (0.92,1.92) {$A$};
\node[lab,text=otNavy,anchor=west] at (3.1,-1) {$B$};
\node[lab,text=otMuted,anchor=west] at (1.06,3.6) {$3$};
\node[lab,text=otGreenDark,anchor=south east] at (-1.2,4.2) {$\mathcal{C}$};
\node[lab,text=otOrange!80!black,anchor=north west] at (4.6,2.1) {$\Delta$};
""" + FIN

FIGURES["transfo_parallelogramme"] = repere(-4.7, 3.9, -1.6, 6.8, 0.55, grille=(-4.5, -1.5, 3.5, 6.5),
                                            tx=((1, "1", None),), ty=((1, "1", None),)) + r"""
\fill[otSky,opacity=0.85] (1,2) -- (3,-1) -- (-2,3) -- (-4,6) -- cycle;
\draw[otNavy,line width=0.9pt] (1,2) -- (3,-1) -- (-2,3) -- (-4,6) -- cycle;
\draw[vec,otGreenDark] (1,2) -- (3,-1);
\draw[vec,otGreenDark] (-4,6) -- (-2,3);
\pz{1,2} \pz{3,-1} \pz{-2,3} \pz[otGreenDark]{-4,6}
\node[lab,text=otNavy,anchor=west] at (1.12,2.05) {$A$};
\node[lab,text=otNavy,anchor=north west] at (3.06,-1.04) {$B$};
\node[lab,text=otNavy,anchor=north east] at (-2.08,2.9) {$C$};
\node[lab,text=otGreenDark,anchor=south east] at (-4.06,6.04) {$D$};
""" + FIN

# =============================================================== FINITION 2026-11-02
# EXERCICE 955 : module = distance OM (corrigé Q1) ; conjugués = symétriques (corrigé Q2)
FIGURES["ex955_module"] = repere(-0.8, 4.1, -2.6, 4.8, 0.85, grille=(-0.5, -2.5, 3.6, 4.5),
                                 tx=((3, "3", "north west"),), ty=((4, "4", None), (-2, "-2", None))) + r"""
\draw[pointille] (3,0) -- (3,4) -- (0,4);
\draw[pointille] (1,0) -- (1,-2) -- (0,-2);
\draw[vec,otGreenDark] (0,0) -- (3,4);
\draw[vec,otNavy] (0,0) -- (1,-2);
\pz[otGreenDark]{3,4} \pz{1,-2}
\node[lab,text=otGreenDark,anchor=south west] at (3.04,4.04) {$z_1$};
\node[lab,text=otNavy,anchor=north west] at (1.06,-2.04) {$z_2$};
\node[lab,text=otGreenDark,anchor=south east] at (1.45,2.3) {$|z_1| = 5$};
\node[lab,text=otNavy,anchor=west] at (1.12,-1.05) {$|z_2| = \sqrt{5}$};
""" + FIN

FIGURES["ex955_conjugues"] = repere(-3.2, 4.6, -5.8, 6.0, 0.62, grille=(-3, -5.5, 4, 5.5),
                                    tx=(), ty=()) + r"""
\draw[pointille] (3,4) -- (3,-4) (1,2) -- (1,-2) (-2,5) -- (-2,-5);
\pz{3,4} \pz{1,-2} \pz{-2,5}
\pz[otGreenDark]{3,-4} \pz[otGreenDark]{1,2} \pz[otGreenDark]{-2,-5}
\node[lab,text=otNavy,anchor=west] at (3.12,4) {$z_1 = 3 + 4\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=west] at (3.12,-4) {$\overline{z_1} = 3 - 4\mathrm{i}$};
\node[lab,text=otNavy,anchor=west] at (1.12,-2) {$z_2$};
\node[lab,text=otGreenDark,anchor=west] at (1.12,2) {$\overline{z_2}$};
\node[lab,text=otNavy,anchor=east] at (-2.12,5) {$z_3 = -2 + 5\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=east] at (-2.12,-5) {$\overline{z_3} = -2 - 5\mathrm{i}$};
""" + FIN

# EXERCICE 954 : somme = règle du parallélogramme (corrigé Q1) ; parties réelle et imaginaire (Q4)
FIGURES["ex954_somme"] = repere(-1.9, 2.9, -0.7, 7.8, 0.72, grille=(-1.5, -0.5, 2.5, 7.5),
                                tx=((-1, "-1", None), (1, "1", "north west"), (2, "2", None)),
                                ty=((3, "3", None), (7, "7", None))) + r"""
\draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] (2,3) -- (1,7) -- (-1,4);
\draw[vec,otNavy] (0,0) -- (2,3);
\draw[vec,otNavy] (0,0) -- (-1,4);
\draw[vec,otGreenDark] (0,0) -- (1,7);
\pz{2,3} \pz{-1,4} \pz[otGreenDark]{1,7}
\node[lab,text=otNavy,anchor=west] at (2.1,3) {$z_1$};
\node[lab,text=otNavy,anchor=east] at (-1.1,4) {$z_2$};
\node[lab,text=otGreenDark,anchor=south west] at (1.06,7.02) {$z_1 + z_2 = 1 + 7\mathrm{i}$};
""" + FIN

FIGURES["ex954_parties"] = repere(-0.9, 3.4, -0.7, 4.1, 0.95, grille=(-0.5, -0.5, 3, 3.6),
                                  tx=(), ty=()) + r"""
\draw[pointille] (2,0) -- (2,3);
\draw[pointille] (0.12,3) -- (2,3);
\draw[otGreenDark,line width=3pt,line cap=butt,opacity=0.9] (0,0) -- (2,0);
\draw[otOrange,line width=3pt,line cap=butt,opacity=0.9] (0,0) -- (0,3);
\pz{2,3} \pz[otOrange]{0,3}
\node[lab,text=otNavy,anchor=south west] at (2.04,3.04) {$z_1 = 2 + 3\mathrm{i}$};
\node[lab,text=otOrange!80!black,anchor=south east] at (-0.06,3.06) {$z_4 = 3\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=north] at (1,-0.12) {$\mathrm{Re}(z_1) = 2$};
\node[lab,text=otOrange!80!black,anchor=east] at (-0.12,1.5) {$3$};
\node[note,anchor=west] at (0.2,1.5) {$\mathrm{Im}(z_1) = \mathrm{Im}(z_4) = 3$};
""" + FIN

# EXERCICE 957 : puissances successives de 1 + i (corrigé Q2)
FIGURES["ex957_puissances"] = repere(-4.8, 1.9, -0.6, 2.75, 1.0, grille=(-4.5, -0.5, 1.5, 2.5),
                                     tx=((-4, "-4", "north"), (-2, "-2", "north"), (1, "1", "north")),
                                     ty=()) + r"""
\draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] (1,1) -- (0,2) -- (-2,2) -- (-4,0);
\draw[vec,otNavy] (0,0) -- (1,1);
\draw[vec,otNavy] (0,0) -- (0,2);
\draw[vec,otNavy] (0,0) -- (-2,2);
\draw[vec,otGreenDark] (0,0) -- (-4,0);
\pz{1,1} \pz{0,2} \pz{-2,2} \pz[otGreenDark]{-4,0}
\node[lab,text=otNavy,anchor=west] at (1.08,1) {$z_1 = 1 + \mathrm{i}$};
\node[lab,text=otNavy,anchor=south west] at (0.05,2.04) {$z_1^2 = 2\mathrm{i}$};
\node[lab,text=otNavy,anchor=south east] at (-2.04,2.04) {$z_1^3 = -2 + 2\mathrm{i}$};
\node[lab,text=otGreenDark,anchor=south east] at (-4.08,0.1) {$z_1^4 = -4$};
\node[note,anchor=north] at (-1.45,-0.62) {à chaque étape : module $\times \sqrt{2}$, argument $+\frac{\pi}{4}$};
""" + FIN
