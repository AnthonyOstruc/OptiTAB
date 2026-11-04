# -*- coding: utf-8 -*-
"""Figures de la notion « Variables et instructions élémentaires (Python) », Seconde.

Compilées par outils/figures_livre.py (style des livres OptiTAB).
- affectation : état de la mémoire après chaque affectation ;
- organigramme_si : instruction conditionnelle if / else ;
- organigramme_tantque : boucle non bornée while (seuil 2^n > 1000).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  instr/.style={fill=otSky,rounded corners=3pt,inner sep=4pt,text=otNavy,
    font=\ttfamily\large},
  memoire/.style={draw=otNavy,line width=0.9pt,rounded corners=2pt,
    minimum width=1.0cm,minimum height=0.85cm,text=otNavy,font=\large},
  memoireNeuve/.style={memoire,draw=otGreenDark,fill=otGreen!15,text=otGreenDark},
  nomVar/.style={font=\ttfamily\large,text=otMuted},
  fleche/.style={otMuted,line width=0.9pt,-{Stealth[length=2.4mm]}},
  bloc/.style={draw=otNavy,fill=otSky,line width=0.9pt,rounded corners=3pt,
    minimum height=0.85cm,inner xsep=8pt,text=otInk,align=center},
  test/.style={draw=otOrange,fill=otOrange!12,line width=0.9pt,diamond,
    aspect=2.3,inner sep=2pt,text=otInk},
  vrai/.style={font=\otMedium\small,text=otGreenDark},
  faux/.style={font=\otMedium\small,text=otRed!85!black},
}
"""

AFFECTATION = r"""
\begin{tikzpicture}
  % état 1
  \node[instr] at (0.5,1.55) {a = 5};
  \node[memoireNeuve] (a1) at (0.5,0) {$5$};
  \node[nomVar,anchor=south] at ($(a1.north)+(0,0.06)$) {a};
  % état 2
  \node[instr] at (3.6,1.55) {b = 2 * a};
  \node[memoire] (a2) at (3.0,0) {$5$};
  \node[memoireNeuve] (b2) at (4.2,0) {$10$};
  \node[nomVar,anchor=south] at ($(a2.north)+(0,0.06)$) {a};
  \node[nomVar,anchor=south] at ($(b2.north)+(0,0.06)$) {b};
  % état 3
  \node[instr] at (7.3,1.55) {a = a + 3};
  \node[memoireNeuve] (a3) at (6.7,0) {$8$};
  \node[memoire] (b3) at (7.9,0) {$10$};
  \node[nomVar,anchor=south] at ($(a3.north)+(0,0.06)$) {a};
  \node[nomVar,anchor=south] at ($(b3.north)+(0,0.06)$) {b};
  \draw[fleche] (1.25,0) -- (2.25,0);
  \draw[fleche] (4.95,0) -- (5.95,0);
\end{tikzpicture}
"""

ORGANIGRAMME_SI = r"""
\begin{tikzpicture}
  \node[bloc] (debut) at (0,2.1) {\texttt{age = 15}};
  \node[test] (t) at (0,0.3) {\texttt{age >= 18} ?};
  \node[bloc,draw=otGreenDark,fill=otGreen!12] (v) at (-2.85,-1.5)
    {afficher « majeur »};
  \node[bloc,draw=otRed!85!black,fill=otRed!8] (f) at (2.85,-1.5)
    {afficher « mineur »};
  \node[bloc] (suite) at (0,-3.2) {suite du programme};
  \draw[fleche] (debut) -- (t);
  \draw[fleche] (t.west) -| (v.north);
  \draw[fleche] (t.east) -| (f.north);
  \draw[fleche] (v.south) |- (suite.west);
  \draw[fleche] (f.south) |- (suite.east);
  \node[vrai,anchor=south east] at ($(t.west)+(-0.1,0.06)$) {Vrai};
  \node[faux,anchor=south west] at ($(t.east)+(0.1,0.06)$) {Faux};
\end{tikzpicture}
"""

ORGANIGRAMME_TANTQUE = r"""
\begin{tikzpicture}
  \node[bloc] (init) at (0,2.2) {\texttt{n = 0}\quad \texttt{p = 1}};
  \node[test] (t) at (0,0.4) {\texttt{p <= 1000} ?};
  \node[bloc] (corps) at (0,-1.6) {\texttt{p = 2 * p}\\\texttt{n = n + 1}};
  \node[bloc,draw=otGreenDark,fill=otGreen!12] (fin) at (4.0,0.4)
    {afficher \texttt{n}};
  \draw[fleche] (init) -- (t);
  \draw[fleche] (t.south) -- (corps.north);
  \draw[fleche] (corps.west) -- ++(-1.2,0) |- (t.west);
  \draw[fleche] (t.east) -- (fin.west);
  \node[vrai,anchor=west] at ($(t.south)+(0.12,-0.42)$) {Vrai};
  \node[faux,anchor=south] at ($(t.east)!0.5!(fin.west)+(0,0.08)$) {Faux};
  \node[note,anchor=east,align=right] at ($(corps.west)+(-1.35,0.95)$)
    {on revient\\au test};
\end{tikzpicture}
"""

FIGURES = {
    "affectation": AFFECTATION,
    "organigramme_si": ORGANIGRAMME_SI,
    "organigramme_tantque": ORGANIGRAMME_TANTQUE,
}

# ================================================================ FINITION 2026-11-02
STY = (r"\tikzset{grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},"
       r"axe/.style={otMuted,line width=.6pt},tic/.style={otMuted,line width=.5pt},"
       r"typeVar/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,inner sep=1pt},"
       r"perdu/.style={font=\ttfamily\large,text=otRed!80!black,inner sep=1pt}}")


def frv(x, dec=None):
    s = f"{x:.{dec}f}" if dec is not None else "%g" % x
    ent, _, d = s.partition(".")
    if len(ent) > 3:
        ent = ent[:-3] + r"\," + ent[-3:]
    return ent + ("{,}" + d if d else "")


def memoire(cases, pas=2.25, largeur=1.6):
    """Cases mémoire : cases = [(nom, valeur, type, ancienne_valeur ou None, neuve)].
    Le nom est au-dessus de la case, le type au-dessous ; une ancienne valeur
    écrasée est écrite barrée à gauche de la nouvelle."""
    L = [r"\begin{tikzpicture}", STY]
    for i, (nom, val, typ, ancien, neuve) in enumerate(cases):
        x = i * pas
        st = "memoireNeuve" if neuve else "memoire"
        if ancien is None:
            L.append(r"\node[%s,minimum width=%.2fcm,font=\ttfamily\large] (c%d) at (%.3f,0) {%s};" % (st, largeur, i, x, val))
        else:
            L.append(r"\node[%s,minimum width=%.2fcm,font=\ttfamily\large] (c%d) at (%.3f,0) {\phantom{%s}};" % (st, largeur, i, x, val))
            L.append(r"\node[anchor=south,inner sep=1pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otRed!80!black] at (%.3f,0.48) {avant : \texttt{%s}};" % (x, ancien))
            L.append(r"\node[font=\ttfamily\large,text=otGreenDark] at (%.3f,0) {%s};" % (x, val))
        haut = 1.05 if ancien is not None else 0.5
        L.append(r"\node[nomVar,anchor=south] at (%.3f,%.3f) {%s};" % (x, haut, nom))
        L.append(r"\node[typeVar,anchor=north] at (%.3f,-0.5) {%s};" % (x, typ))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# 1968 Q2 : quatre variables de quatre types
FIGURES["e1968_types"] = memoire([("a", "7", "int (entier)", None, False),
                                  ("b", "2.0", "float (flottant)", None, False),
                                  ("c", "False", "bool (booléen)", None, False),
                                  ("d", r'"maths"', "str (chaîne)", None, False)], pas=2.3, largeur=1.7)

# 1969 Q3 : l'échange raté (la valeur 4 de a est perdue)
FIGURES["e1969_echange"] = r"""
\begin{tikzpicture}
""" + STY + r"""
  \node[instr] at (0.6,1.75) {b = 9};
  \node[memoire] (a1) at (0,0) {$4$};
  \node[memoireNeuve] (b1) at (1.2,0) {$9$};
  \node[nomVar,anchor=south] at ($(a1.north)+(0,0.06)$) {a};
  \node[nomVar,anchor=south] at ($(b1.north)+(0,0.06)$) {b};
  \node[instr] at (3.75,1.75) {a = b};
  \node[memoireNeuve] (a2) at (3.15,0) {$9$};
  \node[memoire] (b2) at (4.35,0) {$9$};
  \node[nomVar,anchor=south] at ($(a2.north)+(0,0.06)$) {a};
  \node[nomVar,anchor=south] at ($(b2.north)+(0,0.06)$) {b};
  \node[font=\otRegular\fontsize{8.5}{10}\selectfont,text=otRed!80!black,anchor=north,align=center] at (3.15,-0.5) {l’ancienne valeur\\$4$ est perdue};
  \node[instr] at (6.9,1.75) {b = a};
  \node[memoire] (a3) at (6.3,0) {$9$};
  \node[memoireNeuve] (b3) at (7.5,0) {$9$};
  \node[nomVar,anchor=south] at ($(a3.north)+(0,0.06)$) {a};
  \node[nomVar,anchor=south] at ($(b3.north)+(0,0.06)$) {b};
  \draw[fleche] (1.75,0) -- (2.6,0);
  \draw[fleche] (4.9,0) -- (5.75,0);
\end{tikzpicture}"""


# 1970 Q6 : 200 minutes = 3 × 60 + 20
def duree_1970():
    u = 0.034  # cm par minute
    L = [r"\begin{tikzpicture}", STY]
    for k in range(3):
        L.append(r"\draw[otNavy,line width=.8pt,fill=otSky] (%.3f,0) rectangle (%.3f,0.7);" % (k * 60 * u, (k + 1) * 60 * u))
        L.append(r"\node[font=\normalsize,text=otNavy] at (%.3f,0.35) {$60$ min};" % ((k + 0.5) * 60 * u))
    L.append(r"\draw[otGreenDark,line width=.8pt,fill=otGreen!20] (%.3f,0) rectangle (%.3f,0.7);" % (180 * u, 200 * u))
    L.append(r"\node[text=otGreenDark,anchor=south,inner sep=1.5pt] at (%.3f,0.75) {$20$};" % (190 * u))
    L.append(r"\draw[decorate,decoration={brace,mirror,amplitude=5pt},otNavy,line width=.7pt] (0,-0.12) -- (%.3f,-0.12);" % (180 * u))
    L.append(r"\node[anchor=north,text=otNavy,inner sep=2pt,align=center] at (%.3f,-0.35) {\texttt{t // 60} vaut $3$ : $3$ heures};" % (90 * u))
    L.append(r"\node[anchor=north west,text=otGreenDark,inner sep=2pt,align=left] at (%.3f,-0.1) {\texttt{t \%% 60}\\vaut $20$};" % (180 * u + 0.1))
    L.append(r"\node[grad,anchor=south west] at (0,0.75) {\texttt{t = 200} minutes};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e1970_duree"] = duree_1970()

# 1971 Q1 : organigramme du if / elif / else, chemin suivi pour note = 14 en vert
FIGURES["e1971_organigramme"] = r"""
\begin{tikzpicture}
  \tikzset{chemin/.style={otGreenDark,line width=1.4pt,-{Stealth[length=2.6mm]}},
    blocV/.style={bloc,draw=otGreenDark,fill=otGreen!15,line width=1.2pt}}
  \node[bloc] (d) at (0,2.2) {\texttt{note = 14}};
  \node[test] (t1) at (0,0.65) {\texttt{note >= 16} ?};
  \node[test,draw=otGreenDark,fill=otGreen!10,line width=1.2pt] (t2) at (0,-1.2) {\texttt{note >= 12} ?};
  \node[test] (t3) at (0,-3.05) {\texttt{note >= 10} ?};
  \node[bloc] (a1) at (4.3,0.65) {afficher \texttt{Très bien}};
  \node[blocV] (a2) at (4.3,-1.2) {afficher \texttt{Bien}};
  \node[bloc] (a3) at (4.3,-3.05) {afficher \texttt{Passable}};
  \node[bloc] (a4) at (0,-4.75) {afficher \texttt{Insuffisant}};
  \draw[chemin] (d) -- (t1);
  \draw[chemin] (t1) -- (t2);
  \draw[fleche] (t2) -- (t3);
  \draw[fleche] (t3) -- (a4);
  \draw[fleche] (t1.east) -- (a1.west);
  \draw[chemin] (t2.east) -- (a2.west);
  \draw[fleche] (t3.east) -- (a3.west);
  \node[vrai,anchor=south] at ($(t1.east)!0.5!(a1.west)+(0,0.05)$) {Vrai};
  \node[vrai,anchor=south] at ($(t2.east)!0.5!(a2.west)+(0,0.05)$) {Vrai};
  \node[vrai,anchor=south] at ($(t3.east)!0.5!(a3.west)+(0,0.05)$) {Vrai};
  \node[faux,anchor=west] at ($(t1.south)!0.5!(t2.north)+(0.1,0)$) {Faux};
  \node[faux,anchor=west] at ($(t2.south)!0.5!(t3.north)+(0.1,0)$) {Faux};
  \node[faux,anchor=west] at ($(t3.south)!0.5!(a4.north)+(0.1,0)$) {Faux};
\end{tikzpicture}"""


# 1972 Q4 : valeurs prises par i dans range(2, 8, 2)
def range_1972():
    u = 0.8
    L = [r"\begin{tikzpicture}", STY]
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (9 * u + 0.35))
    for k in range(10):
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (k * u, k * u))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.14) {%d};" % (k * u, k))
    for a in (2, 4, 6):
        L.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2mm]}] (%.3f,0.15) .. controls (%.3f,0.85) and (%.3f,0.85) .. (%.3f,0.15);" % (a * u + 0.05, a * u + 0.4, (a + 2) * u - 0.4, (a + 2) * u - 0.05))
        L.append(r"\node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (%.3f,0.72) {$+2$};" % ((a + 1) * u))
    for a in (2, 4, 6):
        L.append(r"\fill[otNavy] (%.3f,0) circle (3pt);" % (a * u))
    L.append(r"\draw[otOrange!90!black,line width=1pt,fill=white] (%.3f,0) circle (3pt);" % (8 * u))
    L.append(r"\node[anchor=north,text=otNavy,inner sep=1.5pt,align=center] at (%.3f,-0.5) {départ\\$2$};" % (2 * u))
    L.append(r"\node[anchor=north,text=otOrange!90!black,inner sep=1.5pt,align=center] at (%.3f,-0.5) {$8$ exclu :\\on s’arrête};" % (8 * u))
    L.append(r"\node[anchor=north,text=otNavy,inner sep=1.5pt] at (%.3f,-1.55) {\texttt{i} prend les valeurs $2$, $4$, $6$};" % (5 * u))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e1972_range"] = range_1972()


# 1973 Q5 : capital au bout de k années (placement à 3 %)
def capital_1973():
    dx, uy = 0.265, 0.0032
    L = [r"\begin{tikzpicture}", STY]
    xr = 26 * dx
    for v in (200, 400, 600, 800, 1000, 1200):
        if v != 1000:
            L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, xr, v * uy))
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (v * uy, frv(v)))
    c = 500.0
    for k in range(26):
        X = (k + 0.5) * dx
        col = "otGreen!75" if k == 24 else ("otNavy!45" if c <= 1000 else "otNavy!20")
        L.append(r"\fill[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (col, X - 0.1, X + 0.1, c * uy))
        if k % 4 == 0:
            L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%d};" % (X, k))
        c *= 1.03
    L.append(r"\draw[seuil] (0,%.3f) -- (%.3f,%.3f);" % (1000 * uy, xr, 1000 * uy))
    X24 = 24.5 * dx
    L.append(r"\draw[otGreenDark,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X24, 1016.4 * uy + 0.05, X24 - 0.6, 1300 * uy))
    L.append(r"\node[anchor=east,text=otGreenDark,inner sep=1.5pt] at (%.3f,%.3f) {$24$ ans : $1\,016{,}40$ €};" % (X24 - 0.6, 1300 * uy))
    L.append(r"\node[anchor=west,text=otOrange!90!black,inner sep=1.5pt] at (%.3f,%.3f) {$1\,000$};" % (xr + 0.05, 1000 * uy))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (1300 * uy + 0.35))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % xr)
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {capital (€)};" % (1300 * uy + 0.38))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {années};" % xr)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e1973_capital"] = capital_1973()

# 3757 : prix des deux tarifs selon le nombre de séances
FIGURES["e3757_tarifs"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=6.6cm, height=4.6cm,
  xmin=0, xmax=16.5, ymin=0, ymax=140, xtick={0,2,...,16}, ytick={20,40,...,120},
  xlabel={$n$}, ylabel={prix (€)},
  every axis y label/.style={at={(current axis.above origin)},anchor=south,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,yshift=2pt}]
  \fill[otGreen!18] (axis cs:10.5,0) rectangle (axis cs:16.5,140);
  \addplot[only marks, mark=*, mark size=1.6pt, otNavy] coordinates {(0,0) (1,8) (2,16) (3,24) (4,32) (5,40) (6,48) (7,56) (8,64) (9,72) (10,80) (11,88) (12,96) (13,104) (14,112) (15,120) (16,128)};
  \addplot[only marks, mark=square*, mark size=1.5pt, otOrange!90!black] coordinates {(0,50) (1,53) (2,56) (3,59) (4,62) (5,65) (6,68) (7,71) (8,74) (9,77) (10,80) (11,83) (12,86) (13,89) (14,92) (15,95) (16,98)};
  \draw[guide] (axis cs:10,0) -- (axis cs:10,80);
  \node[anchor=south east,text=otNavy,inner sep=1.5pt] at (axis cs:12.6,104) {tarif A : $8n$};
  \node[anchor=south,text=otOrange!90!black,inner sep=1.5pt] at (axis cs:4,72) {tarif B : $50 + 3n$};
  \node[anchor=north,text=otGreenDark,inner sep=1.5pt,align=center] at (axis cs:13.5,52) {B moins cher\\dès $n = 11$};
\end{axis}
\end{tikzpicture}"""

# nouveau-1 : cases mémoire du programme de caisse (après exécution)
FIGURES["n1_memoire"] = memoire([("prix", "12.5", "float", None, False),
                                 ("n", "3", "int", None, False),
                                 ("total", "32.5", "float", "37.5", True),
                                 ("cher", "True", "bool", None, False)], pas=2.2, largeur=1.55)


# nouveau-2 : hauteurs atteintes après chaque rebond, seuil de 10 cm
def rebonds():
    hs = [160, 80, 40, 20, 10, 5]
    dx, uy = 1.1, 0.026
    L = [r"\begin{tikzpicture}", STY]
    xr = (len(hs) + 0.2) * dx
    for v in (40, 80, 120, 160):
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, xr, v * uy))
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%d};" % (v * uy, v))
    for k, h in enumerate(hs):
        X = (k + 0.65) * dx
        col = "otOrange!80" if h < 10 else "otNavy!45"
        L.append(r"\fill[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (col, X - 0.22, X + 0.22, h * uy))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (X, "départ" if k == 0 else str(k)))
        L.append(r"\node[anchor=south,inner sep=1.2pt,text=%s] at (%.3f,%.3f) {$%d$};" % ("otOrange!90!black" if h < 10 else "otInk", X, max(h * uy, 10 * uy) + 0.06, h))
    L.append(r"\draw[seuil] (0,%.3f) -- (%.3f,%.3f);" % (10 * uy, xr, 10 * uy))
    L.append(r"\node[anchor=south east,text=otOrange!90!black,inner sep=1.5pt] at (%.3f,%.3f) {seuil : $10$ cm};" % (xr, 10 * uy + 0.5))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (160 * uy + 0.4))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % xr)
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {hauteur $h$ (cm)};" % (160 * uy + 0.42))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {rebond n°};" % xr)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["n2_rebonds"] = rebonds()


# nouveau-3 : le vol de 6 (valeurs successives de u)
def syracuse(u0=6):
    vals = [u0]
    while vals[-1] != 1:
        u = vals[-1]
        vals.append(u // 2 if u % 2 == 0 else 3 * u + 1)
    dx, uy = 0.85, 0.19
    L = [r"\begin{tikzpicture}", STY]
    xr = (len(vals) - 1) * dx + 0.75
    for v in (4, 8, 12, 16):
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, xr, v * uy))
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%d};" % (v * uy, v))
    pts = [(0.35 + k * dx, v * uy) for k, v in enumerate(vals)]
    L.append(r"\draw[otNavy,line width=1pt] " + " -- ".join("(%.3f,%.3f)" % p for p in pts) + ";")
    for k, (x, y) in enumerate(pts):
        v = vals[k]
        col = "otGreenDark" if v == max(vals) else "otNavy"
        L.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, x, y))
        monte = k + 1 < len(vals) and vals[k + 1] > v
        anc = "north" if (k > 0 and vals[k - 1] > v and monte) else "south"
        dy = -0.12 if anc == "north" else 0.1
        L.append(r"\node[anchor=%s,inner sep=1.2pt,text=%s] at (%.3f,%.3f) {$%d$};" % (anc, col, x, y + dy, v))
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (x, x))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%d};" % (x, k))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (16 * uy + 0.5))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % xr)
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {valeur de \texttt{u}};" % (16 * uy + 0.52))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {étape};" % xr)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["n3_syracuse"] = syracuse(6)
