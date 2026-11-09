# -*- coding: utf-8 -*-
"""Figures du formulaire « Aires, périmètres et volumes ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/formulaires/aires-perimetres-volumes --planche
"""

NOM = r"\node[anchor=south,font=\otMedium\fontsize{9}{10}\selectfont,text=otMuted] at (#1) {#2};"


def nom(x, y, texte):
    return NOM.replace("#1", f"{x},{y}").replace("#2", texte)


CARRE_RECTANGLE_DISQUE = r"""
\begin{tikzpicture}
  % carré
  \fill[otSky] (0,0) rectangle (1.8,1.8); \draw[geoTrait] (0,0) rectangle (1.8,1.8);
  \node[anchor=north,yshift=-2pt] at (0.9,0) {$c$};
""" + nom(0.9, 2.05, "Carré") + r"""
  % rectangle
  \fill[otSky] (2.7,0) rectangle (5.5,1.8); \draw[geoTrait] (2.7,0) rectangle (5.5,1.8);
  \node[anchor=north,yshift=-2pt] at (4.1,0) {$L$};
  \node[anchor=west,xshift=2pt] at (5.5,0.9) {$\ell$};
""" + nom(4.1, 2.05, "Rectangle") + r"""
  % disque
  \fill[otSky] (7.35,0.9) circle (0.95); \draw[geoTrait] (7.35,0.9) circle (0.95);
  \draw[otGreenDark,line width=0.9pt] (7.35,0.9) -- (8.3,0.9);
  \fill[otInk] (7.35,0.9) circle (1.3pt);
  \node[anchor=south,yshift=1pt,text=otGreenDark] at (7.83,0.9) {$r$};
  \node[anchor=north,yshift=-1pt] at (7.35,0.9) {$O$};
""" + nom(7.35, 2.05, "Disque") + r"""
\end{tikzpicture}"""

TRIANGLE_PARALLELOGRAMME = r"""
\begin{tikzpicture}
  % triangle
  \coordinate (A) at (0,0); \coordinate (B) at (3.1,0); \coordinate (C) at (1.0,2.0); \coordinate (H) at (1.0,0);
  \fill[otSky] (A) -- (B) -- (C) -- cycle; \draw[geoTrait] (A) -- (B) -- (C) -- cycle;
  \draw[geoAide] (C) -- (H);
  \angledroit[0.18]{C}{H}{B}
  \node[anchor=north,yshift=-2pt] at (2.05,0) {$b$};
  \node[anchor=west,xshift=1pt,text=otGreenDark] at (1.0,0.75) {$h$};
""" + nom(1.55, 2.25, "Triangle") + r"""
  % parallélogramme
  \coordinate (P) at (4.1,0); \coordinate (Q) at (6.9,0); \coordinate (R) at (7.7,2.0); \coordinate (S) at (4.9,2.0); \coordinate (K) at (4.9,0);
  \fill[otSky] (P) -- (Q) -- (R) -- (S) -- cycle; \draw[geoTrait] (P) -- (Q) -- (R) -- (S) -- cycle;
  \draw[geoAide] (S) -- (K);
  \angledroit[0.18]{S}{K}{Q}
  \node[anchor=north,yshift=-2pt] at (5.9,0) {$b$};
  \node[anchor=west,xshift=1pt,text=otGreenDark] at (4.9,0.75) {$h$};
""" + nom(5.9, 2.25, "Parallélogramme") + r"""
\end{tikzpicture}"""

TRAPEZE_LOSANGE = r"""
\begin{tikzpicture}
  % trapèze
  \coordinate (A) at (0,0); \coordinate (B) at (3.4,0); \coordinate (C) at (2.6,1.9); \coordinate (D) at (0.8,1.9); \coordinate (H) at (0.8,0);
  \fill[otSky] (A) -- (B) -- (C) -- (D) -- cycle; \draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;
  \draw[geoAide] (D) -- (H);
  \angledroit[0.18]{D}{H}{B}
  \node[anchor=north,yshift=-2pt] at (1.7,0) {$B$};
  \node[anchor=south,yshift=2pt] at (1.7,1.9) {$b$};
  \node[anchor=west,xshift=1pt,text=otGreenDark] at (0.8,0.75) {$h$};
""" + nom(1.7, 2.45, "Trapèze") + r"""
  % losange
  \coordinate (E) at (4.4,1.0); \coordinate (F) at (5.9,0); \coordinate (G) at (7.4,1.0); \coordinate (I) at (5.9,2.0);
  \fill[otSky] (E) -- (F) -- (G) -- (I) -- cycle; \draw[geoTrait] (E) -- (F) -- (G) -- (I) -- cycle;
  \draw[geoAide] (E) -- (G); \draw[geoAide] (F) -- (I);
  \node[anchor=south,yshift=1pt,text=otGreenDark] at (5.15,1.0) {$D$};
  \node[anchor=west,xshift=2pt,text=otGreenDark] at (5.9,0.45) {$d$};
""" + nom(5.9, 2.45, "Losange") + r"""
\end{tikzpicture}"""

PAVE_CYLINDRE = r"""
\begin{tikzpicture}
  % pavé droit
  \fill[otSky] (0,0) rectangle (2.4,1.5);
  \fill[otSky!70] (0,1.5) -- (0.9,2.1) -- (3.3,2.1) -- (2.4,1.5) -- cycle;
  \fill[otSky!85!otNavy!8] (2.4,0) -- (3.3,0.6) -- (3.3,2.1) -- (2.4,1.5) -- cycle;
  \draw[geoAide,otMuted] (0,0) -- (0.9,0.6) -- (3.3,0.6); \draw[geoAide,otMuted] (0.9,0.6) -- (0.9,2.1);
  \draw[geoTrait] (0,0) rectangle (2.4,1.5);
  \draw[geoTrait] (0,1.5) -- (0.9,2.1) -- (3.3,2.1) -- (2.4,1.5);
  \draw[geoTrait] (2.4,0) -- (3.3,0.6) -- (3.3,2.1);
  \node[anchor=north,yshift=-2pt] at (1.2,0) {$L$};
  \node[anchor=north west,xshift=1pt] at (2.85,0.3) {$\ell$};
  \node[anchor=east,xshift=-2pt,text=otGreenDark] at (0,0.75) {$h$};
""" + nom(1.65, 2.35, "Pavé droit") + r"""
  % cylindre
  \fill[otSky] (5.0,0) -- (5.0,2.0) arc (180:360:1.0 and 0.42) -- (7.0,0) arc (0:-180:1.0 and 0.42);
  \fill[otSky!70] (6.0,2.0) ellipse (1.0 and 0.42);
  \draw[geoAide,otMuted] (7.0,0) arc (0:180:1.0 and 0.42);
  \draw[geoTrait] (5.0,0) arc (180:360:1.0 and 0.42);
  \draw[geoTrait] (5.0,0) -- (5.0,2.0); \draw[geoTrait] (7.0,0) -- (7.0,2.0);
  \draw[geoTrait] (6.0,2.0) ellipse (1.0 and 0.42);
  \draw[otGreenDark,line width=0.9pt] (6.0,2.0) -- (7.0,2.0);
  \fill[otInk] (6.0,2.0) circle (1.2pt);
  \node[anchor=south,yshift=0.5pt,inner sep=0.8pt,text=otGreenDark] at (6.55,2.0) {$r$};
  \node[anchor=west,xshift=2pt,text=otGreenDark] at (7.0,1.0) {$h$};
""" + nom(6.0, 2.55, "Cylindre") + r"""
\end{tikzpicture}"""

PYRAMIDE_CONE = r"""
\begin{tikzpicture}
  % pyramide à base carrée
  \coordinate (A) at (0,0); \coordinate (B) at (2.2,0); \coordinate (C) at (3.0,0.6); \coordinate (D) at (0.8,0.6);
  \coordinate (O) at (1.5,0.3); \coordinate (S) at (1.5,2.5);
  \fill[otSky] (A) -- (B) -- (S) -- cycle; \fill[otSky!80] (B) -- (C) -- (S) -- cycle;
  \draw[geoAide,otMuted] (A) -- (D) -- (C); \draw[geoAide,otMuted] (D) -- (S);
  \draw[geoAide] (S) -- (O);
  \draw[geoTrait] (A) -- (B) -- (C); \draw[geoTrait] (S) -- (A); \draw[geoTrait] (S) -- (B); \draw[geoTrait] (S) -- (C);
  \node[anchor=west,xshift=1pt,text=otGreenDark] at (1.5,1.0) {$h$};
""" + nom(1.5, 2.75, "Pyramide") + r"""
  % cône
  \coordinate (T) at (5.8,2.5);
  \fill[otSky] (4.85,0) -- (T) -- (6.75,0) arc (0:-180:0.95 and 0.32);
  \draw[geoAide,otMuted] (6.75,0) arc (0:180:0.95 and 0.32);
  \draw[geoTrait] (4.85,0) arc (180:360:0.95 and 0.32);
  \draw[geoTrait] (4.85,0) -- (T) -- (6.75,0);
  \draw[geoAide] (T) -- (5.8,0);
  \draw[otGreenDark,line width=0.9pt] (5.8,0) -- (6.75,0);
  \fill[otInk] (5.8,0) circle (1.2pt);
  \node[anchor=south,yshift=0.5pt,inner sep=0.8pt,text=otGreenDark] at (6.3,0) {$r$};
  \node[anchor=east,xshift=-1pt,text=otGreenDark] at (5.8,1.0) {$h$};
""" + nom(5.8, 2.75, "Cône") + r"""
\end{tikzpicture}"""

PRISME_BOULE = r"""
\begin{tikzpicture}
  % prisme droit à base triangulaire
  \coordinate (P1) at (0,0); \coordinate (P2) at (2.0,0); \coordinate (P3) at (1.3,0.6);
  \coordinate (Q1) at (0,1.8); \coordinate (Q2) at (2.0,1.8); \coordinate (Q3) at (1.3,2.4);
  \fill[otSky] (P1) -- (P2) -- (Q2) -- (Q1) -- cycle; \fill[otSky!70] (Q1) -- (Q2) -- (Q3) -- cycle;
  \draw[geoAide,otMuted] (P1) -- (P3) -- (P2); \draw[geoAide,otMuted] (P3) -- (Q3);
  \draw[geoTrait] (P1) -- (P2) -- (Q2) -- (Q1) -- cycle; \draw[geoTrait] (Q1) -- (Q3) -- (Q2);
  \node[anchor=east,xshift=-2pt,text=otGreenDark] at (0,0.9) {$h$};
""" + nom(1.0, 2.65, "Prisme droit") + r"""
  % boule
  \fill[otSky] (5.0,1.15) circle (1.15);
  \draw[geoAide,otMuted] (6.15,1.15) arc (0:180:1.15 and 0.32);
  \draw[geoTrait] (3.85,1.15) arc (180:360:1.15 and 0.32);
  \draw[geoTrait] (5.0,1.15) circle (1.15);
  \draw[otGreenDark,line width=0.9pt] (5.0,1.15) -- (6.15,1.15);
  \fill[otInk] (5.0,1.15) circle (1.2pt);
  \node[anchor=south,yshift=0.5pt,inner sep=0.8pt,text=otGreenDark] at (5.6,1.15) {$r$};
""" + nom(5.0, 2.55, "Boule") + r"""
\end{tikzpicture}"""

FIGURES = {
    "carre_rectangle_disque": CARRE_RECTANGLE_DISQUE,
    "triangle_parallelogramme": TRIANGLE_PARALLELOGRAMME,
    "trapeze_losange": TRAPEZE_LOSANGE,
    "pave_cylindre": PAVE_CYLINDRE,
    "pyramide_cone": PYRAMIDE_CONE,
    "prisme_boule": PRISME_BOULE,
}
