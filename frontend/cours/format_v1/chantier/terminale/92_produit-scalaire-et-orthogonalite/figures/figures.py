# -*- coding: utf-8 -*-
"""Figures de la notion 92 « Produit scalaire et orthogonalité » (Terminale), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Géométrie dans l'espace : perspective cavalière des livres (otEspace) pour le cube,
projection orthogonale calculée ici pour les tétraèdres ; arêtes cachées en pointillés.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  otEspace/.style={x={(1cm,0cm)},y={(0.42cm,0.34cm)},z={(0cm,1cm)},line join=round,line cap=round},
  otVu/.style={draw=otNavy,line width=0.9pt,line join=round},
  otCache/.style={draw=otNavy!60,line width=0.7pt,dash pattern=on 3pt off 2pt},
  otSommet/.style={font=\normalsize,text=otInk,inner sep=2pt},
  otPt/.style={circle,fill=otNavy,inner sep=0pt,minimum size=4.2pt},
  otPtV/.style={circle,fill=otGreenDark,inner sep=0pt,minimum size=4.6pt},
  otVec/.style={draw=otGreenDark,line width=1.25pt,-{Stealth[length=2.8mm]}},
  otVecC/.style={draw=otGreenDark,line width=1.1pt,dash pattern=on 3.2pt off 2pt,-{Stealth[length=2.8mm]}},
  otVecN/.style={draw=otNavy,line width=1.15pt,-{Stealth[length=2.6mm]}},
  otVecO/.style={draw=otOrange,line width=1.15pt,-{Stealth[length=2.6mm]}},
  otPlan/.style={fill=otSky,draw=otNavy!45,line width=0.6pt},
  otAngle/.style={otNavy,line width=0.6pt},
}
\newcommand{\ptN}[1]{\fill[otNavy] (#1) circle (2.2pt);}
\newcommand{\ptV}[1]{\fill[otGreenDark] (#1) circle (2.4pt);}
\newcommand{\tic}[2]{\path ($(#1)!0.5!(#2)$) coordinate (otm);
  \draw[otNavy,line width=.75pt] ($(otm)!3.6pt!90:(#2)$) -- ($(otm)!3.6pt!-90:(#2)$);}
\newcommand{\ticc}[2]{\path ($(#1)!0.5!(#2)$) coordinate (otm);
  \path ($(otm)!1.5pt!(#2)$) coordinate (otma); \path ($(otm)!-1.5pt!(#2)$) coordinate (otmb);
  \draw[otNavy,line width=.75pt] ($(otma)!3.6pt!90:(#2)$) -- ($(otma)!3.6pt!-90:(#2)$)
    ($(otmb)!3.6pt!90:(#2)$) -- ($(otmb)!3.6pt!-90:(#2)$);}
\newcommand{\otPaveCoord}[3]{%
  \coordinate (A) at (0,0,0); \coordinate (B) at (#1,0,0); \coordinate (C) at (#1,#2,0);
  \coordinate (D) at (0,#2,0); \coordinate (E) at (0,0,#3); \coordinate (F) at (#1,0,#3);
  \coordinate (G) at (#1,#2,#3); \coordinate (H) at (0,#2,#3);}
\newcommand{\otPaveAretes}{%
  \draw[otVu] (A) -- (B) -- (C) -- (G) -- (H) -- (E) -- cycle;
  \draw[otVu] (B) -- (F) -- (E); \draw[otVu] (F) -- (G);
  \draw[otCache] (A) -- (D) -- (C); \draw[otCache] (D) -- (H);}
\newcommand{\otPaveNoms}{%
  \node[otSommet,anchor=north east] at (A) {$A$}; \node[otSommet,anchor=north west] at (B) {$B$};
  \node[otSommet,anchor=west] at (C) {$C$}; \node[otSommet,anchor=south east] at (D) {$D$};
  \node[otSommet,anchor=east] at (E) {$E$}; \node[otSommet,anchor=south east] at (F) {$F$};
  \node[otSommet,anchor=south west] at (G) {$G$}; \node[otSommet,anchor=south east] at (H) {$H$};}
"""


# ------------------------------------------------------------------ projections
def vue(az, el):
    a, e = math.radians(az), math.radians(el)
    w = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
    ex = (-math.sin(a), math.cos(a), 0.0)
    ey = (w[1] * ex[2] - w[2] * ex[1], w[2] * ex[0] - w[0] * ex[2], w[0] * ex[1] - w[1] * ex[0])
    return lambda p: (sum(p[i] * ex[i] for i in range(3)), sum(p[i] * ey[i] for i in range(3)))


def coords(points, proj, s):
    """\\coordinate (nom) at (x,y); pour chaque point 3D projeté (échelle s cm)."""
    out = []
    for nom, p in points.items():
        x, y = proj(p)
        out.append(f"\\coordinate ({nom}) at ({s * x:.3f},{s * y:.3f});")
    return "\n  ".join(out)


def milieu(p, q, t=0.5):
    return tuple(p[i] + t * (q[i] - p[i]) for i in range(3))


# tétraèdre régulier d'arête 1 : base BCD horizontale, C devant, sommet A
PHI = math.radians(12)
R = 1 / math.sqrt(3)
TETRA = {
    "B": (R * math.cos(math.radians(150) + PHI), R * math.sin(math.radians(150) + PHI), 0.0),
    "C": (R * math.cos(math.radians(270) + PHI), R * math.sin(math.radians(270) + PHI), 0.0),
    "D": (R * math.cos(math.radians(30) + PHI), R * math.sin(math.radians(30) + PHI), 0.0),
    "A": (0.0, 0.0, math.sqrt(2 / 3)),
}
TETRA["I"] = milieu(TETRA["A"], TETRA["B"])
TETRA["J"] = milieu(TETRA["A"], TETRA["C"])
TETRA["K"] = milieu(TETRA["A"], TETRA["D"])
COORD_TETRA = coords(TETRA, vue(-90, 22), 4.6)


def tetra(extra, milieux="IJK", labels_milieux=None):
    """Tétraèdre régulier ABCD (arête [BD] cachée) + éléments supplémentaires."""
    lab = {"I": "south east", "J": "west", "K": "south west"}
    lab.update(labels_milieux or {})
    pts = "".join(f"  \\ptN{{{m}}} \\node[otSommet,anchor={lab[m]}] at ({m}) {{${m}$}};\n"
                  for m in milieux)
    return (r"""\begin{tikzpicture}[line join=round,line cap=round]
  """ + COORD_TETRA + r"""
  \draw[otCache] (B) -- (D);
  \draw[otVu] (A) -- (B) -- (C) -- (D) -- cycle; \draw[otVu] (A) -- (C);
""" + extra + pts + r"""  \node[otSommet,anchor=south] at (A) {$A$}; \node[otSommet,anchor=east] at (B) {$B$};
  \node[otSommet,anchor=north] at (C) {$C$}; \node[otSommet,anchor=west] at (D) {$D$};
\end{tikzpicture}""")


# tétraèdre OABC trirectangle (exercice 1108) : vue calculée pour que l'angle AMO soit lisible
TRI = {"O": (0, 0, 0), "A": (1, 0, 0), "B": (0, 1, 0), "C": (0, 0, 1)}
TRI["M"] = (0, 0.6, 0.4)
TRI["I"] = (0, 0.5, 0.5)
TRI["oa"] = (0.12, 0, 0)
TRI["ob"] = (0, 0.12, 0)
TRI["oc"] = (0, 0, 0.12)
TRI["oab"] = (0.12, 0.12, 0)
TRI["obc"] = (0, 0.12, 0.12)
TRI["oac"] = (0.12, 0, 0.12)
COORD_TRI = coords(TRI, vue(320, 35), 4.8)


def trirect(extra, m="M", lab_m="south"):
    return (r"""\begin{tikzpicture}[line join=round,line cap=round]
  """ + COORD_TRI + r"""
  \draw[otCache] (O) -- (B);
  \draw[otMuted,line width=0.5pt] (oa) -- (oac) -- (oc);
  \draw[otMuted,line width=0.5pt,dash pattern=on 1.6pt off 1.2pt] (oa) -- (oab) -- (ob) (ob) -- (obc) -- (oc);
  \draw[otVu] (A) -- (B) -- (C) -- cycle; \draw[otVu] (O) -- (A) (O) -- (C);
""" + extra + f"  \\ptV{{{m}}} \\node[otSommet,anchor={lab_m}] at ({m}) {{$M$}};\n" + r"""  \node[otSommet,anchor=east] at (O) {$O$}; \node[otSommet,anchor=north west] at (A) {$A$};
  \node[otSommet,anchor=west] at (B) {$B$}; \node[otSommet,anchor=south] at (C) {$C$};
\end{tikzpicture}""")


FIGURES = {
# =================================================================== COURS
# I. rappel : AB.AC = AB.AH (H projeté orthogonal de C sur (AB))
"cours_projection": r"""
\begin{tikzpicture}[line join=round]
  \fill[otSky] (-0.7,-0.75) -- (5.0,-0.75) -- (6.3,2.6) -- (0.6,2.6) -- cycle;
  \draw[otNavy!45,line width=0.6pt] (-0.7,-0.75) -- (5.0,-0.75) -- (6.3,2.6) -- (0.6,2.6) -- cycle;
  \coordinate (A) at (0.3,0); \coordinate (B) at (4.6,0.35); \coordinate (C) at (3.0,2.05);
  \coordinate (H) at ($(A)!(C)!(B)$);
  \draw[otMuted,line width=0.7pt,dash pattern=on 3pt off 2pt] (C) -- (H);
  \draw[otGreenDark,line width=3.2pt,opacity=0.35] (A) -- (H);
  \draw[otVecN] (A) -- (B);
  \draw[otVec] (A) -- (C);
  \angledroit[0.22]{C}{H}{B}
  \ptN{H}
  \node[otSommet,anchor=north east] at (A) {$A$}; \node[otSommet,anchor=north west] at (B) {$B$};
  \node[otSommet,anchor=south] at (C) {$C$}; \node[otSommet,anchor=north] at ($(H)+(0,-0.16)$) {$H$};
  \node[otSommet,text=otNavy] at (-0.05,-0.45) {$\mathcal{P}$};
\end{tikzpicture}""",

# II. droites orthogonales non sécantes
"cours_orthogonales": r"""
\begin{tikzpicture}[otEspace,scale=4.4]
  \otPaveCoord{1}{1}{1}
  \otPaveAretes
  \draw[otGreenDark,line width=2.2pt] (A) -- (E);
  \draw[otOrange,line width=2.2pt] (H) -- (G);
  \otPaveNoms
\end{tikzpicture}""",

# II. (AG) orthogonale au plan (BDE)
"cours_cube_bde": r"""
\begin{tikzpicture}[otEspace,scale=4.4]
  \otPaveCoord{1}{1}{1}
  \coordinate (K) at (1/3,1/3,1/3);
  \fill[otGreen,opacity=0.2] (B) -- (D) -- (E) -- cycle;
  \otPaveAretes
  \draw[otGreenDark,line width=1pt] (B) -- (E);
  \draw[otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt] (B) -- (D) -- (E);
  \draw[otOrange,line width=1.1pt,dash pattern=on 3.5pt off 2pt] (A) -- (K);
  \draw[otOrange,line width=1.1pt,dash pattern=on 3.5pt off 2pt] (K) -- (G);
  \node[geoPoint,fill=otOrange] at (K) {};
  \node[otSommet,inner sep=1pt,anchor=north west,text=otOrange!70!black] at ($(K)+(0.035,0,-0.02)$) {$K$};
  \node[otSommet,anchor=north east] at (A) {$A$}; \node[otSommet,anchor=north west] at (B) {$B$};
  \node[otSommet,anchor=west] at (C) {$C$}; \node[otSommet,anchor=east] at ($(D)+(-0.02,0,0.02)$) {$D$};
  \node[otSommet,anchor=east] at (E) {$E$}; \node[otSommet,anchor=south east] at (F) {$F$};
  \node[otSommet,anchor=south west] at (G) {$G$}; \node[otSommet,anchor=south east] at (H) {$H$};
\end{tikzpicture}""",

# III. vecteur normal
"cours_normal": r"""
\begin{tikzpicture}[line join=round]
  \fill[otSky] (-0.8,-0.8) -- (4.3,-0.8) -- (5.5,1.75) -- (0.4,1.75) -- cycle;
  \draw[otNavy!45,line width=0.6pt] (-0.8,-0.8) -- (4.3,-0.8) -- (5.5,1.75) -- (0.4,1.75) -- cycle;
  \coordinate (A) at (1.4,0.35); \coordinate (M) at (3.7,0.95); \coordinate (N) at (1.4,2.9);
  \draw[otVecN] (A) -- (M);
  \draw[otVec] (A) -- (N);
  \angledroit[0.24]{N}{A}{M}
  \ptN{A} \ptN{M}
  \node[otSommet,anchor=north east] at (A) {$A$}; \node[otSommet,anchor=north west] at (M) {$M$};
  \node[otSommet,anchor=east,text=otGreenDark] at ($(N)+(-0.05,-0.15)$) {$\vec{n}$};
  \node[otSommet,text=otNavy] at (0.05,-0.45) {$\mathcal{P}$};
\end{tikzpicture}""",

# IV. projeté orthogonal sur un plan
"cours_projete": r"""
\begin{tikzpicture}[line join=round]
  \fill[otSky] (-0.8,-0.8) -- (4.3,-0.8) -- (5.5,1.75) -- (0.4,1.75) -- cycle;
  \draw[otNavy!45,line width=0.6pt] (-0.8,-0.8) -- (4.3,-0.8) -- (5.5,1.75) -- (0.4,1.75) -- cycle;
  \coordinate (H) at (1.6,0.45); \coordinate (M) at (1.6,3.0); \coordinate (Q) at (3.9,0.15);
  \draw[otMuted,line width=0.8pt] (M) -- (Q) -- (H);
  \draw[otGreenDark,line width=1.3pt] (M) -- (H);
  \angledroit[0.24]{M}{H}{Q}
  \ptN{M} \ptV{H} \ptN{Q}
  \node[otSommet,anchor=south] at (M) {$M$}; \node[otSommet,anchor=north east] at (H) {$H$};
  \node[otSommet,anchor=north west] at (Q) {$Q$};
  \node[otSommet,text=otNavy] at (0.05,-0.45) {$\mathcal{P}$};
\end{tikzpicture}""",

# ========================================================= EXERCICE 979
"ex979_rectangle": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, x=1.05cm, y=1.05cm, xmin=-0.8, xmax=4.4, ymin=-0.8, ymax=4.9,
  xtick={1,2,3,4}, ytick={1,2,3}]
  \fill[otSky] (axis cs:0,0) rectangle (axis cs:3,4);
  \draw[otOrange,line width=1pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0) -- (axis cs:3,4);
  \draw[geoTrait] (axis cs:0,0) -- (axis cs:3,0) -- (axis cs:3,4) -- (axis cs:0,4) -- cycle;
  \draw[geoTrait] (axis cs:3,0) -- (axis cs:0,4);
  \draw[otNavy,line width=.6pt] (axis cs:0.28,0) -- (axis cs:0.28,0.28) -- (axis cs:0,0.28);
  \pnt{0}{0} \pnt{3}{0} \pnt{0}{4} \pnt{3}{4}
  \node[otSommet,anchor=north east] at (axis cs:-0.05,-0.05) {$A$};
  \node[otSommet,anchor=south west] at (axis cs:3.03,0.03) {$B$};
  \node[otSommet,anchor=south east] at (axis cs:-0.03,4.03) {$C$};
  \node[otSommet,anchor=south west] at (axis cs:3.03,4.03) {$D$};
\end{axis}
\end{tikzpicture}""",

# ========================================================= EXERCICE 976
"ex976_points": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, x=0.56cm, y=0.56cm, xmin=-4.3, xmax=6.6, ymin=-2.2, ymax=7.4,
  xtick={-2,2,4}, ytick={-1,2,4,6}]
  \coordinate (A) at (axis cs:1,2); \coordinate (B) at (axis cs:4,6);
  \coordinate (C) at (axis cs:-3,5); \coordinate (D) at (axis cs:5,-1);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \fill[otGreen!14] (A) -- (B) -- (D) -- cycle;
  \draw[geoTrait] (C) -- (D) (A) -- (B) (B) -- (C) (B) -- (D);
  \angledroit[0.2]{B}{A}{C} \angledroit[0.2]{D}{A}{B}
  \tic{A}{B} \tic{A}{C} \tic{A}{D}
  \ptN{A} \ptN{B} \ptN{C} \ptN{D}
  \node[otSommet,anchor=north east] at (A) {$A$}; \node[otSommet,anchor=south] at (B) {$B$};
  \node[otSommet,anchor=south east] at (C) {$C$}; \node[otSommet,anchor=north west] at (D) {$D$};
\end{axis}
\end{tikzpicture}""",

# ========================================================= EXERCICE 982
"ex982_droites": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, x=0.62cm, y=0.62cm, xmin=-0.8, xmax=7.8, ymin=-2.3, ymax=5.6,
  xtick={2,4,6}, ytick={-2,2,4}]
  \coordinate (A) at (axis cs:2,-1); \coordinate (B) at (axis cs:6,3); \coordinate (M) at (axis cs:4,1);
  \coordinate (D) at (axis cs:5,0); \coordinate (P) at (axis cs:3,2);
  \draw[geoTrait] (axis cs:0.9,-2.1) -- (axis cs:7.5,4.5);
  \draw[otOrange,line width=1.1pt] (axis cs:-0.5,5.5) -- (axis cs:7.2,-2.2);
  \angledroit[0.2]{B}{M}{P}
  \ticc{A}{M} \ticc{M}{B}
  \draw[otGreenDark,line width=0.7pt,-{Stealth[length=1.8mm]}] ($(D)!0.45cm!(B)$) arc[start angle=71.57, end angle=198.43, radius=0.45cm];
  \draw[otVec] (D) -- (B); \draw[otVec] (D) -- (A);
  \ptN{A} \ptN{B} \ptN{M} \ptV{D}
  \node[otSommet,anchor=north west] at (A) {$A$}; \node[otSommet,anchor=north west] at (B) {$B$};
  \node[otSommet,anchor=east] at (axis cs:3.88,1) {$M$};
  \node[otSommet,anchor=north] at (axis cs:5,-0.12) {$D$};
  \node[otSommet,text=otNavy,anchor=north west] at (axis cs:7.0,3.6) {$(AB)$};
  \node[otSommet,text=otOrange!75!black,anchor=south west] at (axis cs:0.25,5.0) {$(d)$};
\end{axis}
\end{tikzpicture}""",

"ex982_triangles": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, x=0.62cm, y=0.62cm, xmin=-0.8, xmax=7.6, ymin=-2.1, ymax=5.6,
  xtick={4,6}, ytick={2,4}]
  \coordinate (A) at (axis cs:2,-1); \coordinate (B) at (axis cs:6,3); \coordinate (C) at (axis cs:2,3);
  \coordinate (E) at (axis cs:0.5359,4.4641);
  \draw[otOrange,line width=1.1pt] (axis cs:-0.5,5.5) -- (axis cs:7.1,-2.1);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \draw[geoTrait] (A) -- (B) -- (C) -- cycle;
  \draw[otGreenDark,line width=1.2pt] (A) -- (E) -- (B);
  \angledroit[0.2]{A}{C}{B}
  \ptN{A} \ptN{B} \ptN{C} \ptV{E}
  \node[otSommet,anchor=north] at (A) {$A$}; \node[otSommet,anchor=west] at (B) {$B$};
  \node[otSommet,anchor=south west] at (C) {$C$}; \node[otSommet,anchor=south west] at (E) {$E$};
  \node[otSommet,text=otOrange!75!black,anchor=south west] at (axis cs:6.35,-1.05) {$(d)$};
\end{axis}
\end{tikzpicture}""",

# ========================================================= EXERCICE 1105 (cube)
"ex1105_cube": r"""
\begin{tikzpicture}[otEspace,scale=4.4]
  \otPaveCoord{1}{1}{1}
  \otPaveAretes
  \draw[otVecC] (A) -- (C);
  \draw[otVecC] (A) -- (G);
  \otPaveNoms
\end{tikzpicture}""",

"ex1105_triangle": r"""
\begin{tikzpicture}[otEspace,scale=4.4]
  \otPaveCoord{1}{1}{1}
  \fill[otGreen,opacity=0.16] (A) -- (C) -- (G) -- cycle;
  \otPaveAretes
  \draw[otGreenDark,line width=1.2pt,dash pattern=on 3.2pt off 2pt] (A) -- (C) (A) -- (G);
  \draw[otGreenDark,line width=1.4pt] (C) -- (G);
  \draw[otGreenDark,line width=.6pt] ($(C)!0.075!(A)$) -- ($($(C)!0.075!(A)$)+(0,0,0.11)$) -- (1,1,0.11);
  \otPaveNoms
\end{tikzpicture}""",

"ex1105_repere": r"""
\begin{tikzpicture}[otEspace,scale=4.4]
  \otPaveCoord{1}{1}{1}
  \otPaveAretes
  \draw[otVecN] (A) -- (B); \draw[otVecN,dash pattern=on 3pt off 2pt] (A) -- (D); \draw[otVecN] (A) -- (E);
  \draw[otVecC] (A) -- (C);
  \draw[otVecC] (A) -- (G);
  \node[otSommet,anchor=north east] at (A) {$A(0\,;0\,;0)$};
  \node[otSommet,anchor=north west] at (B) {$B$};
  \node[otSommet,anchor=west,text=otGreenDark] at (C) {$C(1\,;1\,;0)$};
  \node[otSommet,anchor=south east] at (D) {$D$};
  \node[otSommet,anchor=east] at (E) {$E$}; \node[otSommet,anchor=south east] at (F) {$F$};
  \node[otSommet,anchor=south west,text=otGreenDark] at (G) {$G(1\,;1\,;1)$};
  \node[otSommet,anchor=south east] at (H) {$H$};
\end{tikzpicture}""",

# ========================================================= EXERCICE 1106 (tétraèdre régulier)
"ex1106_tetra": tetra(""),
"ex1106_q1": tetra(r"""  \draw[otVec] (A) -- (B); \draw[otVec] (A) -- (C);
""", milieux=""),
"ex1106_q2": tetra(r"""  \draw[otVec] (B) -- (I); \draw[otVec] (A) -- (J);
""", milieux="IJ"),
"ex1106_q3": tetra(r"""  \draw[otVec] (I) -- (J); \draw[otVecO] (A) -- (D);
""", milieux="IJ"),
"ex1106_q4": tetra(r"""  \draw[otVec] (I) -- (K); \draw[otVecO] (J) -- (K);
""", milieux="IJK"),

# ========================================================= EXERCICE 1108 (tétraèdre trirectangle)
"ex1108_tetra": trirect(r"""  \draw[otGreenDark,line width=1.2pt] (A) -- (M);
  \draw[otGreenDark,line width=1.1pt,dash pattern=on 3.2pt off 2pt] (M) -- (O);
  \draw[otGreenDark,line width=0.7pt] ($(M)!0.42cm!(A)$) to[bend left=30] ($(M)!0.42cm!(O)$);
  \node[otSommet,text=otGreenDark] at ($(M)!0.82cm!($(A)!0.5!(O)$)$) {$\theta$};
"""),
"ex1108_milieu": trirect(r"""  \fill[otGreen,opacity=0.18] (A) -- (B) -- (I) -- cycle;
  \draw[otGreenDark,line width=1.2pt] (A) -- (I);
  \draw[otGreenDark,line width=.6pt] ($(I)!0.22cm!(A)$) -- ($($(I)!0.22cm!(A)$)+($(I)!0.22cm!(B)$)-(I)$) -- ($(I)!0.22cm!(B)$);
  \tic{B}{I} \tic{I}{C}
""", m="I"),

"ex1108_courbe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=6.4cm, height=3.6cm, xmin=0, xmax=1.12, ymin=40, ymax=58.5,
  xtick={0.5,1}, xticklabels={$\frac{1}{2}$,$1$}, ytick={45,50,54.74}, yticklabels={$45°$,$50°$,$54{,}7°$},
  xlabel={$x$}, ylabel={$\theta(x)$ en degrés},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(current axis.north west)},anchor=south west,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  yticklabel style={anchor=east,yshift=0pt}]
  \addplot[courbe, domain=0:1] {acos(sqrt((2*x^2-2*x+1)/(2*x^2-2*x+2)))};
  \draw[guide] (axis cs:0.5,40) -- (axis cs:0.5,54.74) -- (axis cs:0,54.74);
  \pnt{0}{45} \pnt{1}{45} \pnt[otGreenDark]{0.5}{54.74}
  \node[note,anchor=south] at (axis cs:0.5,55.3) {maximum en $x=\frac{1}{2}$};
\end{axis}
\end{tikzpicture}""",
}

TOLERE = {}

# =================================================================== FINITION 2026-11-02
# Outil commun espace.py (parties cachées calculées, étiquettes placées hors des traits).
import espace as es  # noqa: E402

PREAMBULE_EXTRA += es.STYLES

# exercices réécrits (géométrie plane de Première remplacée par des exercices dans l'espace) :
# leurs anciennes figures ne servent plus
for _nom in ("ex979_rectangle", "ex976_points", "ex982_droites", "ex982_triangles"):
    FIGURES.pop(_nom, None)


def nom_pave(f, S, pref=None):
    centre = tuple(sum(S[k][i] for k in "ABCDEFGH") / 8 for i in range(3))
    cx, cy = f.p(centre)
    for k in "ABCDEFGH":
        x, y = f.p(S[k])
        pr = (pref or {}).get(k, math.degrees(math.atan2(y - cy, x - cx)))
        f.label(S[k], f"${k}$", pref=pr)


# ---------------------------------------------------------------- COURS (refaites)
# I. AB.AC = AB.AH (H projeté orthogonal de C sur (AB))
f = es.Fig(1.0)
cadre = [(-0.7, -0.75), (5.0, -0.75), (6.3, 2.6), (0.6, 2.6)]
f.fill(cadre, "ePlanB"); f.ligne(cadre, "eBordB", ferme=True)
A_, B_, C_ = (0.4, 0.05), (4.6, 0.4), (3.0, 2.05)
ab = es.sub(B_, A_)
H_ = es.add(A_, es.mul(es.dot(es.sub(C_, A_), ab) / es.dot(ab, ab), ab))
f.ligne([C_, H_], "eGuide")
f.ligne([A_, H_], "otGreenDark,line width=3.4pt,opacity=0.3", compte=False)
f.vec(A_, B_); f.vec(A_, C_, "eVecV")
f.angle_droit(H_, C_, B_, 0.22)
f.point(H_)
f.label(A_, "$A$", pref=200); f.label(B_, "$B$", pref=-20); f.label(C_, "$C$", pref=90); f.label(H_, "$H$", pref=-90)
f.texte((5.5, 2.25), r"$\mathcal{P}$", style="eLblN", anchor="north east")
FIGURES["cours_projection"] = f.tikz()

# II. (AG) orthogonale au plan (BDE), qu'elle coupe en K
S1 = es.sommets_pave(1, 1, 1)
f = es.Fig(4.4, uy=(0.32, 0.42))          # vue un peu plus plongeante : K se détache de (DH)
f.fill([S1["B"], S1["D"], S1["E"]], "ePlanV")
es.pave(f, S1, noms=False)
f.ligne([S1["B"], S1["E"]], "eRep", dessus=True)
f.ligne([S1["E"], S1["D"]], "eRepC", dessus=True); f.ligne([S1["D"], S1["B"]], "eRepC", dessus=True)
K1 = (1 / 3, 1 / 3, 1 / 3)
f.ligne([S1["A"], S1["G"]], "otOrange,line width=1.1pt,dash pattern=on 3.5pt off 2pt", dessus=True)
f.point(K1, "ptO")
nom_pave(f, S1, pref={"D": 180})
f.label(K1, "$K$", style="eLblO", pref=120, dirs=range(90, 171, 10))
FIGURES["cours_cube_bde"] = f.tikz()


# IV. projeté orthogonal d'un point sur une droite (cours) et exercice 978
def fig_projete_droite(nA, nB, tH, vert_bh=False):
    f = es.Fig(1.0)
    B = (0.6, 0.55)
    u = (1.0, 0.38)
    nu = math.hypot(*u)
    uu = (u[0] / nu, u[1] / nu)
    H = (B[0] + tH * uu[0], B[1] + tH * uu[1])
    A = (H[0] - 1.55 * uu[1], H[1] + 1.55 * uu[0])
    d0, d1 = (B[0] - 0.75 * uu[0], B[1] - 0.75 * uu[1]), (B[0] + 5.2 * uu[0], B[1] + 5.2 * uu[1])
    f.ligne([d0, d1], "eDroite")
    f.ligne([A, B], "eFin")
    f.vec(B, (B[0] + 0.95 * uu[0], B[1] + 0.95 * uu[1]), "eVec")
    f.ligne([A, H], "eRep")
    f.angle_droit(H, A, d1, 0.22, "eAngleV")
    f.point(B); f.point(A); f.point(H, "ptV")
    f.label(B, f"${nB}$", pref=-100)
    f.label((B[0] + 0.55 * uu[0], B[1] + 0.55 * uu[1]), r"$\vec{u}$", h=0.5, pref=-80, r=0.05)
    f.label(A, f"${nA}$", pref=90)
    f.label(H, "$H$", style="eLblV", pref=-70)
    f.label(d1, "$d$", style="eLblN", pref=30)
    return f.tikz()


FIGURES["cours_projete_droite"] = fig_projete_droite("M", "B", 3.0)
FIGURES["n978_projete"] = fig_projete_droite("A", "B", 2.1)


# III. plan médiateur (cours) et exercice 982
def fig_mediateur(avec_cd):
    f = es.Fig(1.0)
    A, B = (0.0, 1.0, 1.15), (4.2, 1.0, 1.15)
    I = es.mil(A, B)
    plan = [(2.1, -0.4, -0.55), (2.1, 2.9, -0.55), (2.1, 2.9, 2.75), (2.1, -0.4, 2.75)]
    f.opaque(plan)
    f.fill(plan, "ePlanV")
    f.ligne(plan, "eBordV", ferme=True)
    f.seg(A, B, "eDroite", "eDroiteC")
    f.codage(A, I, 2); f.codage(I, B, 2)
    D = (2.1, 0.35, 0.05)
    f.angle_droit(I, B, D if avec_cd else (2.1, 1.0, 0.0), 0.2, "eAngleV")
    f.point(A); f.point(B); f.point(I)
    f.label(A, "$A$", pref=180); f.label(B, "$B$", pref=0); f.label(I, "$I$", pref=120)
    if avec_cd:
        C = (2.1, 2.3, 1.65)
        f.seg(D, A, "eRep", "eRepC"); f.seg(D, B, "eRep", "eRepC")
        f.ligne([D, I], "eGuide")
        f.point(D, "ptV"); f.point(C, "ptV")
        f.label(D, "$D$", style="eLblV", pref=-90); f.label(C, "$C$", style="eLblV", pref=90)
    else:
        M = (2.1, 0.35, 2.2)
        f.seg(M, A, "eFin", "eGuide"); f.seg(M, B, "eFin", "eGuide")
        f.point(M, "ptV"); f.label(M, "$M$", style="eLblV", pref=90)
    f.label((2.1, 2.75, 2.45), r"$\mathcal{P}$", style="eLblV", pref=200)
    return f.tikz()


FIGURES["cours_plan_mediateur"] = fig_mediateur(False)
FIGURES["n982_mediateur"] = fig_mediateur(True)

# ---------------------------------------------------------------- 974 : pavé 4 × 2 × 3
SP = es.sommets_pave(4, 2, 3)
f = es.Fig(1.2)
es.pave(f, SP, leger=True, noms=False)
f.vec(SP["A"], (1, 0, 0)); f.vec(SP["A"], (0, 1, 0), "eVecC"); f.vec(SP["A"], (0, 0, 1))
nom_pave(f, SP)
f.label((0.55, 0, 0), r"$\vec{\imath}$", h=0.5, pref=-90, r=0.05, dirs=range(-120, -59, 10))
f.label((0, 0.8, 0), r"$\vec{\jmath}$", h=0.55, pref=-10, r=0.1, dirs=range(-40, 11, 10))
f.label((0, 0, 0.55), r"$\vec{k}$", h=0.5, pref=180, r=0.05, dirs=range(150, 211, 10))
f.label(es.mil(SP["A"], SP["B"], 0.6), "$4$", style="eLblM", pref=-90, r=0.05)
f.label(es.mil(SP["B"], SP["C"]), "$2$", style="eLblM", pref=-20, r=0.05)
f.label(es.mil(SP["A"], SP["E"], 0.7), "$3$", style="eLblM", pref=180, r=0.05)
FIGURES["n974_pave"] = f.tikz()

f = es.Fig(1.0)
f.fill([SP["A"], SP["F"], SP["H"]], "ePlanV")
f.opaque([SP[k] for k in "ABFE"], [SP[k] for k in "BCGF"], [SP[k] for k in "EFGH"])
es.pave(f, SP, leger=True, noms=False)
f.seg(SP["A"], SP["F"], "eRep", "eRepC"); f.seg(SP["F"], SP["H"], "eRep", "eRepC"); f.seg(SP["A"], SP["H"], "eRep", "eRepC")
pa = f.arc(SP["A"], SP["F"], SP["H"], 1.1)
nom_pave(f, SP)
f.label(pa, r"$\approx 60{,}1°$", n=6, style="eLblV", pref=60, r=0.1)
FIGURES["n974_angle"] = f.tikz()

# ---------------------------------------------------------------- 981 : hauteur issue de B, pied hors de [AC]
f = es.Fig(1.15)
A, C = (1.3, 0.3), (3.3, 0.3)
B = (1.3 - 1.0, 0.3 + 2 * math.sqrt(2))
H = (0.3, 0.3)
f.fill([A, B, C], "ePlanB")
f.ligne([(-0.4, 0.3), A], "eGuide")
f.ligne([A, B, C], "eArete", ferme=True)
f.ligne([B, H], "eRep")
f.angle_droit(H, B, A, 0.2, "eAngleV")
for q, nom, pr in ((A, "A", -60), (B, "B", 90), (C, "C", 0)):
    f.point(q); f.label(q, f"${nom}$", pref=pr)
f.point(H, "ptV"); f.label(H, "$H$", style="eLblV", pref=-120)
f.label(es.mil(A, C), "$2$", style="eLblM", pref=-90, r=0.06)
f.label(es.mil(A, B), "$3$", style="eLblM", pref=20, r=0.06)
f.label(es.mil(H, A), "$1$", style="eLblM", pref=-90, r=0.06)
pa = f.arc(A, C, B, 0.42, "eArc")
f.label(pa, r"$\approx 109{,}5°$", n=7, style="eLblV", pref=40, r=0.05)
FIGURES["n981_hauteur"] = f.tikz()

# ---------------------------------------------------------------- 979 : rectangle ABDC (AB = 3, AC = 6)
f = es.Fig(0.85)
A, B, C = (0, 0, 0), (3, 0, 0), (0, 6, 0)
D = (3, 6, 0)
f.fill([A, B, D, C], "ePlanB")
f.ligne([A, B, D, C], "eArete", ferme=True)
f.ligne([B, D], "eRep"); f.ligne([C, D], "eRep")
f.ligne([A, D], "otOrange,line width=1.1pt"); f.ligne([B, C], "otOrange,line width=1.1pt")
f.angle_droit(A, B, C, 0.55)
for q, nom, st in ((A, "A", "eLbl"), (B, "B", "eLbl"), (C, "C", "eLbl"), (D, "D", "eLblV")):
    f.point(q, "ptV" if nom == "D" else "ptN"); f.label(q, f"${nom}$", style=st)
f.label(es.mil(A, B), "$3$", style="eLblM", pref=-90, r=0.06)
f.label(es.mil(A, C), "$6$", style="eLblM", pref=160, r=0.06)
FIGURES["n979_rectangle"] = f.tikz()

# ---------------------------------------------------------------- 976 : projeté de M sur le plan P
f = es.Fig(1.0)
X, Y = 5.2, 3.2
cadre = [(0, 0, 0), (X, 0, 0), (X, Y, 0), (0, Y, 0)]
es.plan(f, cadre)
Ap, Bp, Hp = (0.9, 0.7, 0), (3.9, 0.9, 0), (2.2, 2.0, 0)
Mp = (2.2, 2.0, 2.45)
f.seg(Mp, Bp, "eFin", "eGuide")
f.ligne([Hp, Bp], "eGuide")
f.seg(Hp, Mp, "eRep", "eRepC")
f.angle_droit(Hp, Mp, Bp, 0.3, "eAngleV")
f.point(Ap); f.point(Bp); f.point(Mp); f.point(Hp, "ptV")
f.label(Ap, "$A$", pref=200); f.label(Bp, "$B$", pref=-30); f.label(Mp, "$M$", pref=90); f.label(Hp, "$H$", style="eLblV", pref=200)
f.label(es.mil(Hp, Mp), "$7$", style="eLblV", pref=180, r=0.08)
f.texte((X - 0.15, 0.12, 0), r"$\mathcal{P}$", style="eLblN", anchor="south east")
FIGURES["n976_projete"] = f.tikz()

# ---------------------------------------------------------------- 975 : plan dirigé par u et v, vecteur normal n
f = es.Fig(1.15)
cadre = [(0, 0, 0), (4.8, 0, 0), (4.8, 3.2, 0), (0, 3.2, 0)]
es.plan(f, cadre)
O = (1.6, 1.0, 0)
u, v, n, w = (1.6, 0, 0), (0, 1.6, 0), (0, 0, 1.7), (-1.15, 0.2, 1.0)
f.vec(O, es.add(O, u)); f.vec(O, es.add(O, v))
f.vec(O, es.add(O, n), "eVecV")
f.vec(O, es.add(O, w), "eVecO")
f.angle_droit(O, es.add(O, u), es.add(O, n), 0.28, "eAngleV")
f.angle_droit(O, es.add(O, v), es.add(O, n), 0.28, "eAngleV")
f.point(O); f.label(O, "$O$", pref=220)
f.label(es.add(O, u), r"$\vec{u}$", h=0.5, pref=-60)
f.label(es.add(O, v), r"$\vec{v}$", h=0.5, pref=60)
f.label(es.add(O, n), r"$\vec{n}$", h=0.5, style="eLblV", pref=90)
f.label(es.add(O, w), r"$\vec{w}$", h=0.5, style="eLblO", pref=150)
f.texte((4.65, 0.12, 0), r"$\mathcal{P}$", style="eLblN", anchor="south east")
FIGURES["n975_normal"] = f.tikz()

# ---------------------------------------------------------------- 1107 : vecteur normal au plan (ABC)
f = es.Fig(1.0)
cadre = [(0, 0, 0), (5.0, 0, 0), (5.0, 3.2, 0), (0, 3.2, 0)]
es.plan(f, cadre)
A, B, C = (1.4, 0.8, 0), (3.7, 0.9, 0), (2.5, 2.5, 0)
f.fill([A, B, C], "ePlanV")
f.ligne([A, B, C], "eArete", ferme=True)
N = (1.4, 0.8, 1.9)
f.vec(A, N, "eVecV")
f.angle_droit(A, B, N, 0.3, "eAngleV"); f.angle_droit(A, C, N, 0.3, "eAngleV")
for q, nom in ((A, "A"), (B, "B"), (C, "C")):
    f.point(q); f.label(q, f"${nom}$")
f.label(N, r"$\vec{n}$", h=0.5, style="eLblV", pref=90)
f.label((5.0, 3.2, 0), r"$(ABC)$", n=4, style="eLblN", pref=0)
FIGURES["n1107_normal"] = f.tikz()


# ---------------------------------------------------------------- 1108 : étiquettes refaites (M hors des arêtes)
def trirect2(vert, m=(0, 0.6, 0.4), nom_m="M", theta=True):
    pr = vue(320, 35)
    P = lambda q: tuple(4.8 * c for c in pr(q))
    O, A, B, C, M = (P(q) for q in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), m))
    f = es.Fig(1.0)
    if vert == "abm":
        f.fill([A, B, M], "ePlanV")
    f.ligne([O, B], "eCachee")
    for a, b in ((A, B), (B, C), (C, A), (O, A), (O, C)):
        f.ligne([a, b], "eArete")
    # angles droits en O (traits fins), dans les faces OAB, OBC, OAC
    q = 0.12
    for a, b, st in (((q, 0, 0), (0, q, 0), "eGuide"), ((0, q, 0), (0, 0, q), "eGuide"), ((q, 0, 0), (0, 0, q), "eFin")):
        f.ligne([P(a), P(es.add(a, b)), P(b)], st)
    if vert == "theta":
        f.ligne([A, M], "eRep"); f.ligne([M, O], "eRepC")
        pa = f.arc(M, A, O, 0.42)
        f.label(pa, r"$\theta$", style="eLblV", pref=-90, r=0.05)
    else:
        f.ligne([A, M], "eRep")
        f.angle_droit(M, A, B, 0.22, "eAngleV")
        f.codage(B, M, 1); f.codage(M, C, 1)
    f.point(M, "ptV")
    f.label(M, f"${nom_m}$", style="eLblV", pref=60)
    for q_, nom in ((O, "O"), (A, "A"), (B, "B"), (C, "C")):
        f.label(q_, f"${nom}$")
    return f.tikz()


FIGURES["ex1108_tetra"] = trirect2("theta")
FIGURES["ex1108_milieu"] = trirect2("abm", m=(0, 0.5, 0.5))

# 1105 : repère, un peu moins large (≤ 900 px)
FIGURES["ex1105_repere"] = FIGURES["ex1105_repere"].replace("scale=4.4", "scale=4.0")
