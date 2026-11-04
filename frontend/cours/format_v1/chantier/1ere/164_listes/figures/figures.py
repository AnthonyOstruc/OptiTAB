# -*- coding: utf-8 -*-
"""Figures de la notion « Notion de liste » (Première spécialité), style des livres OptiTAB.

Compilation :  python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

- Schémas de listes (cases bleu marine, indices en Fira Mono) repris de la
  notion Terminale 99 « Listes » ; éléments de réponse en vert.
- Nuages de points, tableaux de valeurs, simulations et sécantes : pgfplots
  (style otWeb / barres sans quadrillage). Toutes les données sont calculées
  ici par du vrai Python (graines fixes pour les simulations) ; le script
  ../verif_listes.py importe ces fonctions et vérifie qu'elles donnent les
  nombres cités dans le cours et les exercices.
"""
from random import randint, seed

PREAMBULE_EXTRA = r"""
\newfontfamily\otMono{FiraMono}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Medium]
\colorlet{otNavyTint}{otNavy!7}
\colorlet{otGreenTint}{otGreen!18}
\tikzset{
  caseL/.style={draw=otNavy,fill=otNavyTint,line width=0.7pt},
  caseV/.style={draw=otGreenDark,fill=otGreenTint,line width=1pt},
  val/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  valV/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otGreenDark},
  idx/.style={font=\otMono\fontsize{9}{10}\selectfont,text=otNavy},
  idxn/.style={font=\otMono\fontsize{9}{10}\selectfont,text=otMuted},
  idxV/.style={font=\otMono\bfseries\fontsize{9}{10}\selectfont,text=otGreenDark},
  lib/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  nomvar/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  code/.style={font=\otMono\fontsize{9}{11}\selectfont,text=otNavy},
  fleche/.style={otMuted,line width=0.7pt,-{Stealth[length=2mm]}},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont,text=otGreenDark,inner sep=1.5pt},
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.5pt},
}
\pgfplotsset{otBarre/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,xshift=4pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,yshift=4pt},
  scale only axis, clip=false, ymin=0,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
"""


# ================================================================ données (vrai Python)
def suite_recurrente(u0, n, f):
    """[u_0, …, u_n] par ajouts successifs."""
    u = [u0]
    for k in range(n):
        u.append(f(u[-1]))
    return u


def simulation_de():
    """Cours : 1 000 lancers d'un dé, graine 1 ; renvoie (R, effectifs)."""
    seed(1)
    R = []
    for k in range(1000):
        R.append(randint(1, 6))
    E = [0, 0, 0, 0, 0, 0]
    for x in R:
        E[x - 1] = E[x - 1] + 1
    return R, E


def simulation_deux_des():
    """Exercice nouveau-2 : 1 000 sommes de deux dés, graine 2 ; renvoie (S, effectifs des sommes 2 à 12)."""
    seed(2)
    S = []
    for k in range(1000):
        a = randint(1, 6)
        b = randint(1, 6)
        S.append(a + b)
    E = [0 for k in range(11)]
    for s in S:
        E[s - 2] = E[s - 2] + 1
    return S, E


def fmt(x):
    """Nombre pour TikZ (point décimal)."""
    return repr(float(x))


def points(xs, ys, couleur="otNavy"):
    return "\n".join(rf"  \pnt[{couleur}]{{{fmt(x)}}}{{{fmt(y)}}}" for x, y in zip(xs, ys))


# ================================================================ schémas de listes
def schema_indices(nom, valeurs, pas_mm=10, idx_vert=False, negatifs=True, lib_largeur=None):
    """Une liste en cases, indices au-dessus (en vert si idx_vert), indices négatifs dessous."""
    n = len(valeurs)
    lignes = [rf"\begin{{tikzpicture}}[x={pas_mm}mm,y=10mm]"]
    for i, v in enumerate(valeurs):
        lignes.append(rf"  \draw[caseL] ({i},0) rectangle ++(1,0.8);")
        lignes.append(rf"  \node[val] at ({i}+0.5,0.4) {{{v}}};")
        lignes.append(rf"  \node[{'idxV' if idx_vert else 'idx'}] at ({i}+0.5,1.12) {{{i}}};")
        if negatifs:
            lignes.append(rf"  \node[idxn] at ({i}+0.5,-0.33) {{{i - n}}};")
    lignes.append(rf"  \node[nomvar,anchor=east] at (-0.12,0.4) {{{nom} =}};")
    lignes.append(r"  \node[lib,anchor=east] at (-0.12,1.12) {indice};")
    if negatifs:
        lignes.append(r"  \node[lib,anchor=east] at (-0.12,-0.33) {indice négatif};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def schema_ajouts(etats, libelles, note=None):
    """Liste qui grandit : une ligne par état ; la case ajoutée est verte, une flèche
    part du dernier élément de la ligne précédente (u[-1]) vers le nouvel élément."""
    dy = 1.25
    L = [r"\begin{tikzpicture}[x=10mm,y=10mm]"]
    for r, (etat, lib) in enumerate(zip(etats, libelles)):
        y = -r * dy
        for i, v in enumerate(etat):
            nouveau = r > 0 and i == len(etat) - 1
            L.append(rf"  \draw[{'caseV' if nouveau else 'caseL'}] ({i},{y}) rectangle ++(1,0.8);")
            L.append(rf"  \node[{'valV' if nouveau else 'val'}] at ({i}+0.5,{y}+0.4) {{{v}}};")
        L.append(rf"  \node[code,anchor=east] at (-0.2,{y}+0.4) {{{lib}}};")
        if r > 0:
            i = len(etat) - 1
            L.append(rf"  \draw[fleche] ({i - 1}+0.62,{y + dy}-0.06) -- ({i}+0.38,{y}+0.86);")
    if note:
        y = -(len(etats) - 1) * dy - 0.45
        L.append(rf"  \node[code,anchor=north west,inner sep=1pt] at (0,{y}) {{{note}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


LISTE_INDICES = schema_indices("notes", [12, 15, 9, 14, 10])

U_COURS = suite_recurrente(1, 4, lambda x: 2 * x + 1)          # [1, 3, 7, 15, 31]
LISTE_APPEND = schema_ajouts(
    [U_COURS[:k + 1] for k in range(5)],
    ["u = [1]", "k = 0", "k = 1", "k = 2", "k = 3"],
    note=r"u.append(2*u[-1] + 1)",
)

EX1063_INDICES = schema_indices("T", [14, 17, 12, 19, 16, 11, 15], pas_mm=8.5, idx_vert=True)


def ex1064_liste():
    L = [3]
    etats = [list(L)]
    for k in range(4):
        L.append(L[-1] + 2 * k)
        etats.append(list(L))
    return etats


EX1064_APPEND = schema_ajouts(
    ex1064_liste(),
    ["L = [3]", "k = 0", "k = 1", "k = 2", "k = 3"],
    note=r"L.append(L[-1] + 2*k)",
)

# ================================================================ cours : suite et nuage
U_NUAGE = suite_recurrente(1, 8, lambda x: 0.5 * x + 2)        # u_0 … u_8
SUITE_NUAGE = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=6.2cm, height=3.9cm, xmin=-0.3, xmax=8.7, ymin=-0.3, ymax=4.7,
  xtick={{1,2,...,8}}, ytick={{1,2,3,4}}, xlabel={{$n$}}, ylabel={{$u_n$}}]
  \draw[seuil] (axis cs:-0.3,4) -- (axis cs:8.7,4);
  \node[legende,text=otOrange!85!black,anchor=west] at (axis cs:8.95,4) {{$y=4$}};
{points(range(9), U_NUAGE)}
\end{{axis}}
\end{{tikzpicture}}"""

# ================================================================ cours : simulation d'un dé
_R1, E_DE = simulation_de()
F_DE = [e / 1000 for e in E_DE]
SIMULATION_HISTO = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otBarre, ybar, bar width=15pt, width=5.6cm, height=3.8cm,
  xmin=0.4, xmax=6.6, ymax=0.215, xtick={{1,...,6}},
  ytick={{0.05,0.1,0.15,0.2}}, yticklabels={{0{{,}}05,0{{,}}10,0{{,}}15,0{{,}}20}},
  xlabel={{face}}, ylabel={{fréquence}}, axis x line*=bottom]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {{{" ".join(f"({k + 1},{fmt(f)})" for k, f in enumerate(F_DE))}}};
  \draw[seuil] (axis cs:0.4,{1 / 6:.6f}) -- (axis cs:6.6,{1 / 6:.6f});
  \node[text=otOrange!85!black,anchor=west,inner sep=1.5pt] at (axis cs:6.7,{1 / 6:.6f}) {{$1/6$}};
\end{{axis}}
\end{{tikzpicture}}"""

# ================================================================ cours : sécante
SECANTE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.2cm, height=4.6cm, xmin=-0.9, xmax=2.7, ymin=-0.9, ymax=4.9,
  xtick={1,2}, ytick={1,2,3,4}]
  \addplot[courbe, domain=-0.9:2.2] {x^2};
  \addplot[otGreenDark, line width=1pt, dash pattern=on 4pt off 2.5pt, domain=0.05:2.7] {2*x-1};
  \addplot[otOrange!90!black, line width=1.1pt, domain=0.37:2.3] {3*x-2};
  \draw[guide] (axis cs:1,1) -- (axis cs:2,1) -- (axis cs:2,4);
  \draw[otMuted,line width=.55pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] (axis cs:1,0.72) -- (axis cs:2,0.72);
  \draw[otMuted,line width=.55pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] (axis cs:2.12,1) -- (axis cs:2.12,4);
  \node[text=otInk,anchor=north,inner sep=1.5pt] at (axis cs:1.5,0.64) {$h$};
  \node[text=otInk,anchor=west,inner sep=1.5pt] at (axis cs:2.17,2.5) {$f(1+h)-f(1)$};
  \pnt{1}{1} \pnt{2}{4}
  \node[anchor=south east,inner sep=2pt] at (axis cs:0.97,1.03) {$A$};
  \node[anchor=south east,inner sep=2pt] at (axis cs:1.97,4.03) {$M$};
  \node[legende,text=otOrange!85!black,anchor=west] at (axis cs:0.55,-0.72) {sécante $(AM)$};
  \node[legende,text=otGreenDark,anchor=west] at (axis cs:2.74,4.4) {tangente en $A$};
  \node[text=otNavy,anchor=east,inner sep=1.5pt] at (axis cs:-0.62,0.25) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}"""

# ================================================================ exercice 1066 : u_{n+1} = 2u_n - 3
U_1066 = suite_recurrente(5, 5, lambda x: 2 * x - 3)            # [5, 7, 11, 19, 35, 67]


def repere_1066(corrige):
    pts = points(range(6), U_1066, "otGreenDark") if corrige else ""
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=5.8cm, height=4.8cm, xmin=-0.3, xmax=5.6, ymin=-4, ymax=74,
  xtick={{1,...,5}}, ytick={{10,20,...,70}}, xlabel={{$n$}}, ylabel={{$u_n$}}]
{pts}
\end{{axis}}
\end{{tikzpicture}}"""


# ================================================================ exercice nouveau-1 : f(x) = x² − 4x + 3
X_N1 = [0.5 * k for k in range(9)]


def f_n1(x):
    return x**2 - 4 * x + 3


Y_N1 = [f_n1(x) for x in X_N1]


def repere_n1(corrige):
    # quadrillage aux demi-unités en x (un \foreach s'évaluerait trop tard dans l'axe)
    demi = "\n".join(rf"  \draw[otRule!75,line width=0.35pt] (axis cs:{a},-1.6) -- (axis cs:{a},3.7);"
                     for a in (0.5, 1.5, 2.5, 3.5))
    # ligne y = 3 du quadrillage (graduation 3 non écrite : le point (0 ; 3) est sur l'axe)
    demi += "\n" + r"  \draw[otRule!75,line width=0.35pt] (axis cs:-0.4,3) -- (axis cs:4.6,3);"
    corps = ""
    if corrige:
        neg = [(x, y) for x, y in zip(X_N1, Y_N1) if y < 0]
        autres = [(x, y) for x, y in zip(X_N1, Y_N1) if y >= 0]
        corps = (r"  \addplot[pale, dash pattern=on 3pt off 2pt, domain=-0.12:4.12] {x^2-4*x+3};" + "\n"
                 + points([p[0] for p in autres], [p[1] for p in autres]) + "\n"
                 + points([p[0] for p in neg], [p[1] for p in neg], "otGreenDark"))
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=5.8cm, height=4.6cm, xmin=-0.4, xmax=4.6, ymin=-1.6, ymax=3.7,
  xtick={{1,2,3,4}}, ytick={{-1,1,2}}]
{demi}
{corps}
\end{{axis}}
\end{{tikzpicture}}"""


# ================================================================ exercice nouveau-2 : deux dés
_S2, E_2DES = simulation_deux_des()
F_2DES = [e / 1000 for e in E_2DES]
P_2DES = [(6 - abs(s - 7)) / 36 for s in range(2, 13)]
EX_N2_HISTO = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otBarre, ybar, bar width=8.5pt, width=5.6cm, height=4.2cm,
  xmin=1.3, xmax=12.7, ymax=0.2, xtick={{2,...,12}},
  ytick={{0.05,0.1,0.15}}, yticklabels={{0{{,}}05,0{{,}}10,0{{,}}15}},
  xlabel={{somme}}, ylabel={{fréquence}}, axis x line*=bottom]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {{{" ".join(f"({s},{fmt(F_2DES[s - 2])})" for s in range(2, 13) if s != 7)}}};
  \addplot[fill=otGreen!70,draw=otGreenDark] coordinates {{(7,{fmt(F_2DES[5])})}};
  \addplot[only marks, mark=-, mark size=7pt, mark options={{otOrange!90!black, line width=1.6pt}}]
    coordinates {{{" ".join(f"({s},{P_2DES[s - 2]:.6f})" for s in range(2, 13))}}};
\end{{axis}}
  \fill[otNavy!55,draw=otNavy] (0.2,-0.95) rectangle ++(0.3,0.22);
  \node[legende,anchor=west] at (0.55,-0.84) {{fréquence observée}};
  \draw[otOrange!90!black,line width=1.6pt] (4.15,-0.84) -- ++(0.42,0);
  \node[legende,anchor=west] at (4.62,-0.84) {{probabilité}};
\end{{tikzpicture}}"""

# ================================================================ exercice nouveau-3 : g(x) = x² − 3x en a = 2
EX_N3_ENONCE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=4.4cm, xmin=-0.6, xmax=4.4, ymin=-2.9, ymax=2.3,
  xtick={1,2,3}, xticklabels={}, ytick={-2,-1,1,2}]
  \addplot[courbe, domain=-0.55:3.6] {x^2-3*x};
  \addplot[otOrange!90!black, line width=1.1pt, domain=1.55:3.9] {2*x-6};
  \draw[guide] (axis cs:2,-2) -- (axis cs:3,-2) -- (axis cs:3,0);
  \draw[otMuted,line width=.55pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] (axis cs:2,-2.3) -- (axis cs:3,-2.3);
  \node[text=otInk,anchor=north,inner sep=1.5pt] at (axis cs:2.5,-2.36) {$h$};
  \node[text=otInk,anchor=west,inner sep=1.5pt] at (axis cs:3.08,-1.05) {$g(2+h)-g(2)$};
  \pnt{2}{-2} \pnt{3}{0}
  \node[anchor=south east,inner sep=2pt] at (axis cs:1.93,-1.93) {$A$};
  \node[anchor=south east,inner sep=2pt] at (axis cs:2.97,0.05) {$M$};
  \node[text=otNavy,anchor=west,inner sep=1.5pt] at (axis cs:0.12,1.6) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}"""

EX_N3_SECANTES = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=4.4cm, xmin=-0.6, xmax=4.4, ymin=-2.9, ymax=2.3,
  xtick={1,2,3}, xticklabels={}, ytick={-2,-1,1,2}]
  \addplot[courbe, domain=-0.55:3.6] {x^2-3*x};
  \addplot[otOrange!90!black, line width=1pt, domain=1.55:3.9] {2*x-6};
  \addplot[otOrange!60, line width=1pt, domain=1.3:2.85] {1.5*x-5};
  \addplot[otGreenDark, line width=1.2pt, domain=1.1:3.75] {x-4};
  \pnt{2}{-2} \pnt{3}{0} \pnt{2.5}{-1.25}
  \node[anchor=north,inner sep=2pt] at (axis cs:2.05,-2.12) {$A$};
  \node[anchor=south east,inner sep=2pt] at (axis cs:2.97,0.05) {$M_1$};
  \node[anchor=south east,inner sep=2pt] at (axis cs:2.47,-1.2) {$M_2$};
  \node[legendeV,anchor=west] at (axis cs:3.8,-0.52) {tangente};
  \node[legendeV,anchor=north west] at (axis cs:3.8,-0.72) {pente $1$};
  \node[text=otNavy,anchor=west,inner sep=1.5pt] at (axis cs:0.12,1.6) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}"""

# ================================================================ exercice nouveau-4 : u_n = n² − 7n + 1
U_N4 = [n**2 - 7 * n + 1 for n in range(9)]
EX_N4_NUAGE = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=6cm, height=4.8cm, xmin=-0.3, xmax=8.7, ymin=-13, ymax=11,
  xtick={{1,...,8}}, ytick={{-10,-5,5,10}}, xlabel={{$n$}}, ylabel={{$u_n$}}]
{points([n for n in range(9) if n not in (3, 4)], [u for n, u in enumerate(U_N4) if n not in (3, 4)])}
{points([3, 4], [U_N4[3], U_N4[4]], "otGreenDark")}
  \node[legendeV,anchor=north] at (axis cs:3.5,-11.6) {{$u_3=u_4=-11$}};
\end{{axis}}
\end{{tikzpicture}}"""

# ================================================================ enrichissement du 2026-11-03
# ---- nouveau-1 (figures exn5_…) : série de notes, deux listes X (notes) et N (effectifs)
X_N5 = [8, 10, 12, 14, 16]
N_N5 = [1, 4, 7, 5, 3]


def liste_notes_n5():
    L = []
    for i in range(len(X_N5)):
        for k in range(N_N5[i]):
            L.append(X_N5[i])
    return L


L_N5 = liste_notes_n5()


def schema_deux_lignes(nom, valeurs, verts, par_ligne=10, pas_mm=7.6):
    """Longue liste sur deux lignes de cases (indices au-dessus) ; cases « verts » en vert."""
    dy = 1.75
    L = [rf"\begin{{tikzpicture}}[x={pas_mm}mm,y=10mm]"]
    for i, v in enumerate(valeurs):
        r, c = divmod(i, par_ligne)
        y = -r * dy
        vert = i in verts
        L.append(rf"  \draw[{'caseV' if vert else 'caseL'}] ({c},{y}) rectangle ++(1,0.8);")
        L.append(rf"  \node[{'valV' if vert else 'val'}] at ({c}+0.5,{y}+0.4) {{{v}}};")
        L.append(rf"  \node[{'idxV' if vert else 'idx'}] at ({c}+0.5,{y}+1.12) {{{i}}};")
    L.append(rf"  \node[nomvar,anchor=east] at (-0.15,0.4) {{{nom} =}};")
    L.append(rf"  \node[lib,anchor=east] at (-0.15,1.12) {{indice}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


EX_N5_LISTE = schema_deux_lignes("L", L_N5, verts={9, 10})

M_N5 = sum(L_N5) / len(L_N5)                                    # 12,5
S_N5 = (sum((x - M_N5) ** 2 for x in L_N5) / len(L_N5)) ** 0.5  # √4,75 ≈ 2,18
BORNES_N5 = (M_N5 - 2 * S_N5, M_N5 + 2 * S_N5)                  # ≈ 8,14 et 16,86


def batons_n5():
    dedans = [(x, n) for x, n in zip(X_N5, N_N5) if BORNES_N5[0] <= x <= BORNES_N5[1]]
    dehors = [(x, n) for x, n in zip(X_N5, N_N5) if not BORNES_N5[0] <= x <= BORNES_N5[1]]
    bat = lambda pts, st: "\n".join(rf"  \draw[{st}] (axis cs:{x},0) -- (axis cs:{x},{n});" for x, n in pts)
    a, b = BORNES_N5
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otBarre, width=6.2cm, height=3.6cm, xmin=6.3, xmax=18.2, ymax=9.6,
  xtick={{8,10,12,14,16}}, ytick={{2,4,6,8}}, xlabel={{note}}, ylabel={{effectif}},
  axis x line*=bottom]
{bat(dehors, "otNavy,line width=5pt")}
{bat(dedans, "otGreen!80!black,line width=5pt")}
  \draw[otGreenDark,line width=0.9pt,{{Bar[width=2.2mm]}}-{{Bar[width=2.2mm]}}] (axis cs:{a:.4f},8.3) -- (axis cs:{b:.4f},8.3);
  \node[legendeV,anchor=south] at (axis cs:{(a + b) / 2:.4f},8.55) {{$[m-2s\,;\,m+2s]$}};
  \draw[seuil] (axis cs:{M_N5},0) -- (axis cs:{M_N5},7.6);
  \node[text=otOrange!85!black,anchor=north west,inner sep=1.5pt] at (axis cs:{M_N5 + 0.08},7.55) {{$m$}};
\end{{axis}}
\end{{tikzpicture}}"""


EX_N5_BATONS = batons_n5()


# ---- nouveau-2 (figure exn6_…) : suite de Syracuse
def suivant_syracuse(u):
    if u % 2 == 0:
        return u // 2
    return 3 * u + 1


def vol_syracuse(n):
    L = [n]
    while L[-1] != 1:
        L.append(suivant_syracuse(L[-1]))
    return L


VOL7 = vol_syracuse(7)          # 17 termes, maximum 52 au rang 5
_R7 = max(range(len(VOL7)), key=lambda i: VOL7[i])
EX_N6_VOL = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=6.6cm, height=4.4cm, xmin=-0.6, xmax=17.4, ymin=-4, ymax=60,
  xtick={{2,4,...,16}}, ytick={{10,20,...,50}}, xlabel={{$n$}}, ylabel={{$u_n$}}]
  \addplot[pale, line width=0.7pt] coordinates {{{" ".join(f"({i},{v})" for i, v in enumerate(VOL7))}}};
{points([i for i in range(len(VOL7)) if i != _R7], [v for i, v in enumerate(VOL7) if i != _R7])}
{points([_R7], [VOL7[_R7]], "otGreenDark")}
  \node[legendeV,anchor=west] at (axis cs:{_R7 + 0.45},{VOL7[_R7] + 1.5}) {{$u_5=52$}};
  \node[legende,anchor=south] at (axis cs:16.3,4.6) {{$u_{{16}}=1$}};
\end{{axis}}
\end{{tikzpicture}}"""

# ---- nouveau-3 (figure exn7_…) : deux placements
A_N7 = [1000 + 60 * n for n in range(31)]
B_N7 = [1000]
for _n in range(30):
    B_N7.append(B_N7[-1] * 1.04)
_C7 = next(n for n in range(31) if B_N7[n] > A_N7[n])   # 21
EX_N7_PLACEMENTS = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=6.6cm, height=4.6cm, xmin=-0.8, xmax=31.5, ymin=0, ymax=3600,
  xtick={{5,10,...,30}}, ytick={{1000,2000,3000}}, xlabel={{$n$}}, ylabel={{capital (€)}},
  every axis y label/.style={{at={{(current axis.above origin)}},anchor=south,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted}},
  /pgf/number format/1000 sep={{\,}}]
  \draw[otGreenDark,line width=0.8pt,dash pattern=on 3pt off 2pt] (axis cs:{_C7},0) -- (axis cs:{_C7},3350);
  \node[legendeV,anchor=south] at (axis cs:{_C7},3370) {{$n=21$}};
{chr(10).join(rf"  \fill[otNavy] (axis cs:{n},{a}) circle (1.5pt);" for n, a in enumerate(A_N7) if n != _C7)}
{chr(10).join(rf"  \fill[otOrange!90!black] (axis cs:{n},{b:.2f}) circle (1.5pt);" for n, b in enumerate(B_N7) if n != _C7)}
  \fill[otGreenDark] (axis cs:{_C7},{A_N7[_C7]}) circle (1.9pt);
  \fill[otGreenDark] (axis cs:{_C7},{B_N7[_C7]:.2f}) circle (1.9pt);
  \node[text=otNavy,anchor=west,inner sep=1.5pt] at (axis cs:30.6,{A_N7[30]}) {{$a_n$}};
  \node[text=otOrange!85!black,anchor=west,inner sep=1.5pt] at (axis cs:30.6,{B_N7[30]:.2f}) {{$b_n$}};
\end{{axis}}
\end{{tikzpicture}}"""

# graduations de l'axe des abscisses placées à la main : « 3 » à droite du trait,
# pour ne pas passer sous le point M (3 ; 0)
XLAB = {
    "exn3_enonce": [(1, "c", "1"), (2, "c", "2"), (3, "d", "3")],
    "exn3_secantes": [(1, "c", "1"), (2, "c", "2"), (3, "d", "3")],
}

FIGURES = {
    "liste_indices": LISTE_INDICES,
    "liste_append": LISTE_APPEND,
    "suite_nuage": SUITE_NUAGE,
    "simulation_histo": SIMULATION_HISTO,
    "secante": SECANTE,
    "ex1063_indices": EX1063_INDICES,
    "ex1064_append": EX1064_APPEND,
    "ex1066_repere": repere_1066(False),
    "ex1066_nuage": repere_1066(True),
    "exn1_repere": repere_n1(False),
    "exn1_points": repere_n1(True),
    "exn2_histo": EX_N2_HISTO,
    "exn3_enonce": EX_N3_ENONCE,
    "exn3_secantes": EX_N3_SECANTES,
    "exn4_nuage": EX_N4_NUAGE,
    "exn5_liste": EX_N5_LISTE,
    "exn5_batons": EX_N5_BATONS,
    "exn6_vol": EX_N6_VOL,
    "exn7_placements": EX_N7_PLACEMENTS,
}
