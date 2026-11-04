# -*- coding: utf-8 -*-
"""Figures de la notion 272 (5e : repérage et grandeurs en fonction d'une autre), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Courbes et points en bleu marine (seconde série en orange) ; l'énoncé montre la
courbe seule ou un repère vide à compléter ; dans les corrigés, les lectures
(pointillés vers les axes, points lus, valeurs) sont en vert foncé.
Les données (DONNEES) sont relues par verif_272.py : figures et énoncés
utilisent exactement les mêmes valeurs.
"""

PREAMBULE_EXTRA = r"""
\pgfplotsset{gr/.style={otWeb, grid=both,
  major grid style={otRule!80,line width=0.4pt}, minor grid style={otRule!45,line width=0.3pt},
  minor tick length=0pt,
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,xshift=2pt,
    font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis y label/.style={at={(current axis.above origin)},anchor=south west,xshift=-4pt,yshift=1pt,
    font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}}}
\tikzset{
  courbeB/.style={otOrange,line width=1.35pt},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
  ligneB/.style={otOrange,line width=1.35pt,line join=round},
  prolong/.style={otOrange!85!black,line width=0.9pt,dash pattern=on 4pt off 2.5pt},
  lecture/.style={otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt},
  niveau/.style={otGreenDark,line width=0.8pt,dash pattern=on 4pt off 2.5pt},
  vert/.style={note,text=otGreenDark},
  bleu/.style={note,text=otNavy},
  orange/.style={note,text=otOrange!85!black},
  petitG/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  cellule/.style={font=\otRegular\fontsize{9}{11}\selectfont,text=otNavy},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
}
\newcommand{\lirev}[2]{\draw[lecture] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\lirex}[2]{\draw[lecture] (axis cs:#1,#2) -- (axis cs:#1,0);}
\newcommand{\liry}[2]{\draw[lecture] (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\pv}[2]{\fill[otGreenDark] (axis cs:#1,#2) circle (2.3pt);}
\newcommand{\zero}{\node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:0,0) {0};}
"""


def lst(a, b, s):
    """Liste de graduations a, a+s, …, b (sans 0)."""
    v, out = a, []
    while v <= b + 1e-9:
        if abs(v) > 1e-9:
            out.append(("%g" % round(v, 6)))
        v += s
    return "{" + ",".join(out) + "}"


def G(opts, corps, xlab="", ylab="", zero=True):
    o = "gr, " + opts
    if xlab:
        o += ", xlabel={" + xlab + "}"
    if ylab:
        o += ", ylabel={" + ylab + "}"
    return (r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[" + o + "]\n" + corps + "\n"
            + (r"\zero" if zero else "") + "\n\\end{axis}\n\\end{tikzpicture}")


def poly(pts, style="ligne", points=True, couleur="otNavy"):
    s = r"\draw[%s] " % style + " -- ".join("(axis cs:%g,%g)" % p for p in pts) + ";\n"
    if points:
        s += "".join(r"\fill[%s] (axis cs:%g,%g) circle (2.1pt);" % (couleur, x, y) + "\n" for x, y in pts)
    return s


def nuage(pts, couleur="otNavy", r=2.3):
    return "".join(r"\fill[%s] (axis cs:%g,%g) circle (%gpt);" % (couleur, x, y, r) + "\n" for x, y in pts)


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


# ===================================================================== feuilles de tableur
def tableur(colonnes, lignes, largeurs, active=None, barre=None, vert=None, orange=None, surligne=None, h=.52):
    """Feuille de tableur (même dessin que la notion 268).
    lignes : la 1re = en-têtes (ligne 1) ; active = (ligne, colonne) ; barre = (nom, formule) ;
    vert / orange = ensembles de (ligne, colonne) écrits en couleur ; surligne = ligne surlignée en vert."""
    L = []
    wn = .55
    xs = [0.0, wn]
    for w in largeurs:
        xs.append(xs[-1] + w)
    R = len(lignes) + 1
    top = 0.0
    if barre:
        nomc, formule = barre
        yb = .2 + h
        L.append(r"\filldraw[fill=white,draw=otMuted!70,line width=.5pt] (0,%s) rectangle (%s,%s);" % (f(.2), f(xs[-1]), f(yb)))
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(1.05), f(.2), f(1.05), f(yb)))
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f(.525), f(.2 + h / 2), nomc))
        L.append(r"\node[petit,text=otMuted,font=\itshape] at (%s,%s) {fx};" % (f(1.35), f(.2 + h / 2)))
        if formule:
            coul = "otGreenDark" if vert and "barre" in vert else "otInk"
            L.append(r"\node[anchor=west,font=\otRegular\fontsize{9.5}{11}\selectfont,text=%s] at (%s,%s) {%s};"
                     % (coul, f(1.62), f(.2 + h / 2), formule))
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[-1]), f(top - h)))
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[1]), f(top - R * h)))
    if surligne:
        y0 = top - surligne * h
        L.append(r"\fill[otGreen!18] (%s,%s) rectangle (%s,%s);" % (f(xs[1]), f(y0), f(xs[-1]), f(y0 - h)))
    for k, c in enumerate(colonnes):
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f((xs[k + 1] + xs[k + 2]) / 2), f(top - h / 2), c))
    for r, ligne in enumerate(lignes):
        y = top - (r + 1) * h - h / 2
        L.append(r"\node[cellule] at (%s,%s) {%d};" % (f(wn / 2), f(y), r + 1))
        for k, v in enumerate(ligne):
            if not v:
                continue
            coul = "otInk"
            if vert and (r + 1, k) in vert:
                coul = "otGreenDark"
            if orange and (r + 1, k) in orange:
                coul = "otOrange!85!black"
            L.append(r"\node[text=%s] at (%s,%s) {%s};" % (coul, f((xs[k + 1] + xs[k + 2]) / 2), f(y), v))
    for r in range(R + 1):
        L.append(r"\draw[otMuted!70,line width=.5pt] (0,%s) -- (%s,%s);" % (f(top - r * h), f(xs[-1]), f(top - r * h)))
    for x in xs:
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x), f(top), f(x), f(top - R * h)))
    if active:
        r, k = active
        L.append(r"\draw[otNavy,line width=1.4pt] (%s,%s) rectangle (%s,%s);"
                 % (f(xs[k + 1]), f(top - r * h), f(xs[k + 2]), f(top - (r + 1) * h)))
    return L


FIGURES = {}
DONNEES = {}

# =============================================================== COURS
# Ascenseur panoramique : hauteur (m) en fonction du temps (s)
DONNEES["ascenseur"] = [(0, 0), (20, 30), (35, 30), (55, 60), (70, 60), (110, 0)]
FIGURES["cours_ascenseur"] = G(
    r"width=6.6cm, height=4.6cm, xmin=0, xmax=118, ymin=0, ymax=72, xtick=" + lst(10, 110, 10)
    + r", xticklabels={10,20,30,40,50,60,70,80,90,100,}, ytick=" + lst(10, 70, 10) + r", minor y tick num=1",
    poly(DONNEES["ascenseur"], points=False) + r"""
  \lirev{10}{15} \pv{10}{15}
  \draw[niveau] (axis cs:0,45) -- (axis cs:80,45);
  \lirex{45}{45} \lirex{80}{45} \pv{45}{45} \pv{80}{45}
  \draw[otGreenDark,line width=2.6pt] (axis cs:55,60) -- (axis cs:70,60);
  \node[vert,anchor=south] at (axis cs:62.5,61.5) {maximum : $60$ m};
""", "temps (s)", "hauteur (m)")

# Ressort : L = 12 + 3m (L en cm, m en kg)
DONNEES["ressort"] = [(m, 12 + 3 * m) for m in range(0, 5)]
FIGURES["cours_ressort"] = G(
    r"width=5.4cm, height=5.2cm, xmin=0, xmax=5.3, ymin=0, ymax=29.5, xtick=" + lst(1, 5, 1)
    + r", minor x tick num=1, ytick=" + lst(3, 27, 3),
    r"""
  \addplot[courbe, domain=0:4.6] {12+3*x};
""" + nuage(DONNEES["ressort"], "otGreenDark") + r"""
  \node[bleu,anchor=north west] at (axis cs:2.3,14.5) {$L = 12 + 3m$};
""", "masse $m$ (kg)", "longueur $L$ (cm)")

# Tableur du ressort
_res = [["Masse (kg)", "Longueur (cm)"]] + [["$%d$" % m, "$%d$" % L] for m, L in DONNEES["ressort"]]
FIGURES["cours_tableur"] = tikz(tableur(["A", "B"], _res, [2.3, 2.7], active=(2, 1), barre=("B2", "=12+3*A2")))


# Proportionnalité : deux petits graphiques
def petit(x0, titre, coul, corps, conclusion, ccoul, xl, yl, opts):
    return (r"\begin{axis}[gr, at={(%gcm,0cm)}, width=3.0cm, height=3.1cm, " % x0 + opts
            + r", title={%s}, title style={font=\otMedium\fontsize{9}{10}\selectfont,text=%s,yshift=10pt}" % (titre, coul)
            + r", xlabel={%s}, ylabel={%s}]" % (xl, yl) + "\n" + corps + "\n" + r"\zero" + "\n"
            + r"\node[anchor=north,font=\otMedium\fontsize{9}{11}\selectfont,text=%s,align=center] at (axis cs:2,-9) {%s};" % (ccoul, conclusion)
            + "\n" + r"\end{axis}" + "\n")


DONNEES["pommes"] = [(m, 2 * m) for m in range(0, 5)]
FIGURES["cours_proportionnalite"] = (r"\begin{tikzpicture}" + "\n"
    + petit(0, "Prix des pommes", "otNavy",
            r"\addplot[courbe, domain=0:4.4] {2*x};" + "\n" + nuage(DONNEES["pommes"], "otNavy", 2.1),
            r"proportionnelles\\(droite par $O$)", "otGreenDark", "kg", "€",
            r"xmin=0, xmax=4.8, ymin=0, ymax=30, xtick={1,2,3,4}, ytick={6,12,18,24}")
    + petit(4.9, "Longueur du ressort", "otNavy",
            r"\addplot[courbe, domain=0:4.4] {12+3*x};" + "\n" + nuage(DONNEES["ressort"], "otNavy", 2.1),
            r"non proportionnelles\\(ne passe pas par $O$)", "otOrange!85!black", "kg", "cm",
            r"xmin=0, xmax=4.8, ymin=0, ymax=30, xtick={1,2,3,4}, ytick={6,12,18,24}")
    + r"\end{tikzpicture}")

# =============================================================== 2940 cuve : V = 2,5 t
DONNEES["cuve"] = lambda t: 2.5 * t
P40 = (r"width=6.2cm, height=5.0cm, xmin=0, xmax=13, ymin=0, ymax=33.5, xtick=" + lst(2, 12, 2)
       + r", ytick=" + lst(5, 30, 5))
B40 = r"""
  \addplot[courbe, domain=0:12] {2.5*x};
"""
FIGURES["ex2940_enonce"] = G(P40, B40, "temps (min)", "volume d'eau (L)")
FIGURES["ex2940_corrige"] = G(P40, B40 + r"""
  \lirev{4}{10} \pv{4}{10}
  \lirev{10}{25} \pv{10}{25}
  \liry{6}{15} \lirex{6}{15} \pv{6}{15}
  \node[vert,anchor=north west,align=left] at (axis cs:0.5,32.5) {$4$ min : $10$ L\\$10$ min : $25$ L\\$15$ L : $6$ min};
""", "temps (min)", "volume d'eau (L)")

# =============================================================== 2938 température
DONNEES["temperature"] = [(0, 6), (2, 5), (4, 4), (6, 3), (8, 5), (10, 9), (12, 13), (14, 16),
                          (16, 15), (18, 12), (20, 9), (22, 8), (24, 7)]
P38 = (r"width=6.7cm, height=4.9cm, xmin=0, xmax=25.6, ymin=0, ymax=19, xtick=" + lst(2, 24, 2)
       + r", ytick=" + lst(2, 18, 2) + r", minor y tick num=1")
B38 = poly(DONNEES["temperature"])
FIGURES["ex2938_enonce"] = G(P38, B38, "heure (h)", "température (°C)")
FIGURES["ex2938_corrige"] = G(P38, B38 + r"""
  \lirev{18}{12} \pv{18}{12}
  \draw[niveau] (axis cs:0,9) -- (axis cs:20,9);
  \lirex{10}{9} \lirex{20}{9} \pv{10}{9} \pv{20}{9}
  \pv{14}{16} \pv{6}{3}
  \node[vert,anchor=south west] at (axis cs:14.3,16.2) {maximum : $16$ °C};
  \node[vert,anchor=north] at (axis cs:4.8,2.5) {minimum : $3$ °C};
""", "heure (h)", "température (°C)")

# =============================================================== 2937 parcours : P = 2n + 3
DONNEES["parcours"] = [(n, 2 * n + 3) for n in range(0, 7)]
P37 = (r"width=5.6cm, height=5.4cm, xmin=0, xmax=6.8, ymin=0, ymax=17, xtick=" + lst(1, 6, 1)
       + r", ytick=" + lst(2, 16, 2) + r", minor y tick num=1")
FIGURES["ex2937_enonce"] = G(P37, "", "activités", "prix (€)")
FIGURES["ex2937_corrige"] = G(P37, nuage(DONNEES["parcours"], "otGreenDark", 2.6) + r"""
  \draw[otOrange!85!black,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,12) -- (axis cs:6.5,12);
  \node[orange,anchor=south east] at (axis cs:3.85,12.25) {budget : $12$ €};
  \draw[otGreenDark,line width=1pt] (axis cs:4,11) circle (5pt);
""", "activités", "prix (€)")

# =============================================================== 2946 carré : A = c²
DONNEES["carre"] = [(c, c * c) for c in range(0, 6)]
P46 = (r"width=5.4cm, height=5.8cm, xmin=0, xmax=5.6, ymin=0, ymax=27.5, xtick=" + lst(1, 5, 1)
       + r", minor x tick num=1, ytick=" + lst(2, 26, 2))
FIGURES["ex2946_enonce"] = G(P46, "", "côté (cm)", "aire (cm²)")
FIGURES["ex2946_corrige"] = G(P46, r"""
  \addplot[courbe, domain=0:5.1, samples=120] {x^2};
""" + nuage(DONNEES["carre"], "otNavy") + r"""
  \lirev{2.5}{6.25} \pv{2.5}{6.25}
  \liry{4.4721}{20} \lirex{4.4721}{20} \pv{4.4721}{20}
  \node[vert,anchor=north west,align=left] at (axis cs:0.3,26.6) {$2{,}5$ cm : environ $6$ cm²\\$20$ cm² : environ $4{,}5$ cm};
""", "côté (cm)", "aire (cm²)")

# =============================================================== 2949 sortie à vélo (distance parcourue)
DONNEES["velo"] = [(0, 0), (20, 6), (30, 6), (60, 12)]
P49 = (r"width=6.2cm, height=4.8cm, xmin=0, xmax=66, ymin=0, ymax=14.2, xtick=" + lst(10, 60, 10)
       + r", minor x tick num=1, ytick=" + lst(2, 14, 2) + r", minor y tick num=1")
B49 = poly(DONNEES["velo"])
FIGURES["ex2949_enonce"] = G(P49, B49, "temps (min)", "distance parcourue (km)")
FIGURES["ex2949_corrige"] = G(P49, B49 + r"""
  \lirev{10}{3} \pv{10}{3}
  \lirev{50}{10} \pv{50}{10}
  \liry{45}{9} \lirex{45}{9} \pv{45}{9}
  \draw[otGreenDark,line width=2.6pt] (axis cs:20,6) -- (axis cs:30,6);
  \node[vert,anchor=south] at (axis cs:25,6.4) {pause};
""", "temps (min)", "distance parcourue (km)")

# =============================================================== 2944 tableur du périmètre : P = 2L + 6
DONNEES["perimetre"] = [(L, 2 * L + 6) for L in range(3, 9)]
_pe = [["Longueur (cm)", "Périmètre (cm)"]] + [["$%d$" % L, ""] for L, P in DONNEES["perimetre"]]
FIGURES["ex2944_enonce"] = tikz(tableur(["A", "B"], _pe, [2.6, 2.7], active=(2, 1), barre=("B2", "")))
_pc = [["Longueur (cm)", "Périmètre (cm)"]] + [["$%d$" % L, "$%d$" % P] for L, P in DONNEES["perimetre"]]
FIGURES["ex2944_corrige"] = tikz(tableur(["A", "B"], _pc, [2.6, 2.7], active=(2, 1), barre=("B2", "=2*A2+6"),
                                         vert={(r, 1) for r in range(2, 8)} | {"barre"}, surligne=6))
P44 = (r"width=5.6cm, height=5.2cm, xmin=0, xmax=9.3, ymin=0, ymax=25, xtick=" + lst(1, 9, 1)
       + r", ytick=" + lst(2, 24, 2))
FIGURES["ex2944_graphique"] = G(P44, r"""
  \draw[prolong] (axis cs:0,6) -- (axis cs:3,12);
  \addplot[courbe, domain=3:8] {2*x+6};
""" + nuage(DONNEES["perimetre"], "otGreenDark", 2.4) + r"""
  \fill[otOrange!85!black] (axis cs:0,6) circle (2.1pt);
  \node[orange,anchor=north west,align=left] at (axis cs:0.6,5.3) {ne passe pas\\par l'origine};
""", "longueur (cm)", "périmètre (cm)")

# =============================================================== 2954 location de kayak
DONNEES["kayakA"] = lambda t: 6 * t
DONNEES["kayakB"] = lambda t: 10 + 4 * t
P54 = (r"width=6.4cm, height=6cm, xmin=0, xmax=8.7, ymin=0, ymax=54, xtick=" + lst(1, 8, 1)
       + r", ytick=" + lst(6, 48, 6))
B54 = r"""
  \addplot[courbe, domain=0:8] {10+4*x};
  \addplot[courbeB, domain=0:8] {6*x};
  \node[bleu,anchor=south east] at (axis cs:1.6,19.5) {$(d_1)$};
  \node[orange,anchor=east] at (axis cs:7,47) {$(d_2)$};
"""
FIGURES["ex2954_enonce"] = G(P54, B54, "durée (h)", "prix (€)")
FIGURES["ex2954_corrige"] = G(P54, B54 + r"""
  \lirex{2}{18} \liry{2}{18} \liry{2}{12} \pv{2}{18} \pv{2}{12}
  \lirev{5}{30} \pv{5}{30}
  \draw[niveau] (axis cs:0,42) -- (axis cs:8,42);
  \lirex{7}{42} \lirex{8}{42} \pv{7}{42} \pv{8}{42}
  \node[vert,anchor=east] at (axis cs:4.75,32.5) {$5$ h : $30$ €};
""", "durée (h)", "prix (€)")

# =============================================================== 2956 trajet de Tom
SITUATIONS = [
    ("Graphique 1", r"\draw[ligne] (axis cs:0,0) -- (axis cs:2,2) -- (axis cs:4,0) -- (axis cs:5,0) -- (axis cs:9,4);", "c"),
    ("Graphique 2", r"\draw[ligne] (axis cs:0,0) -- (axis cs:9,4);", "a"),
    ("Graphique 3", r"\draw[ligne] (axis cs:0,4) -- (axis cs:9,0);", "d"),
    ("Graphique 4", r"\draw[ligne] (axis cs:0,0) -- (axis cs:3,2) -- (axis cs:5,2) -- (axis cs:8,4);", "b"),
]


def mini(x0, y0, titre, corps):
    return (r"\begin{axis}[otWeb, grid=none, at={(%gcm,%gcm)}, width=2.9cm, height=1.9cm, " % (x0, y0)
            + r"xmin=0, xmax=10, ymin=0, ymax=4.8, xtick=\empty, ytick=\empty, "
            + r"xlabel={temps}, ylabel={distance}, "
            + r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-2pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}, "
            + r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,xshift=-4pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}, "
            + r"title={%s}, title style={font=\otMedium\fontsize{9}{10}\selectfont,text=otNavy,yshift=14pt}]" % titre
            + "\n" + corps + "\n" + r"\end{axis}" + "\n")


def situations(corrige=False):
    s = r"\begin{tikzpicture}" + "\n"
    pos = [(0, 3.9), (4.4, 3.9), (0, 0), (4.4, 0)]
    for k, (t, c, lettre) in enumerate(SITUATIONS):
        titre = t + (r" : \textcolor{otGreenDark}{situation %s}" % lettre if corrige else "")
        s += mini(pos[k][0], pos[k][1], titre, c)
    return s + r"\end{tikzpicture}"


FIGURES["ex2956_situations"] = situations()
FIGURES["ex2956_situations_corrige"] = situations(True)

DONNEES["tom"] = [(0, 0), (4, 400), (8, 0), (10, 0), (22, 1200)]
P56 = (r"width=5.9cm, height=5cm, xmin=0, xmax=23.8, ymin=0, ymax=1330, xtick=" + lst(2, 22, 2)
       + r", ytick=" + lst(200, 1200, 200) + r", minor y tick num=1")
B56 = poly(DONNEES["tom"])
FIGURES["ex2956_trajet"] = G(P56, B56, "temps (min)", "distance à la maison (m)")
FIGURES["ex2956_trajet_corrige"] = G(P56, B56 + r"""
  \draw[niveau] (axis cs:0,200) -- (axis cs:12,200);
  \lirex{2}{200} \lirex{6}{200} \lirex{12}{200} \pv{2}{200} \pv{6}{200} \pv{12}{200}
  \liry{4}{400} \pv{4}{400}
  \draw[otGreenDark,line width=2.6pt] (axis cs:8,0) -- (axis cs:10,0);
  \lirev{22}{1200} \pv{22}{1200}
  \node[vert,anchor=north west,align=left] at (axis cs:4.6,1110) {demi-tour à $400$ m\\maison : de $8$ à $10$ min};
""", "temps (min)", "distance à la maison (m)")

# =============================================================== 2945 bougie : h = 15 - 2t
DONNEES["bougie"] = [(0, 15), (1, 13), (2, 11), (3, 9), (4, 7)]
P45 = (r"width=6cm, height=5.2cm, xmin=0, xmax=8.6, ymin=0, ymax=17, xtick=" + lst(1, 8, 1)
       + r", minor x tick num=1, ytick=" + lst(2, 16, 2) + r", minor y tick num=1")
FIGURES["ex2945_enonce"] = G(P45, "", "temps (h)", "hauteur (cm)")
FIGURES["ex2945_corrige"] = G(P45, r"""
  \addplot[courbe, domain=0:7.5] {15-2*x};
""" + nuage(DONNEES["bougie"], "otNavy", 2.4) + r"""
  \lirev{2.5}{10} \pv{2.5}{10}
  \liry{5}{5} \lirex{5}{5} \pv{5}{5}
  \pv{7.5}{0}
  \node[vert,anchor=south west] at (axis cs:7.45,0.35) {$7{,}5$ h};
  \node[vert,anchor=north west,align=left] at (axis cs:4.6,16.3) {$2{,}5$ h : $10$ cm\\$5$ cm : $5$ h};
""", "temps (h)", "hauteur (cm)")
_bt = [["Temps (h)", "Hauteur (cm)"]] + [["$%d$" % t, ""] for t in range(0, 9)]
FIGURES["ex2945_tableur"] = tikz(tableur(["A", "B"], _bt, [2.3, 2.5], active=(2, 1), barre=("B2", "=15-2*A2")))
_bc = [["Temps (h)", "Hauteur (cm)"]] + [["$%d$" % t, "$%d$" % (15 - 2 * t)] for t in range(0, 9)]
FIGURES["ex2945_tableur_corrige"] = tikz(tableur(["A", "B"], _bc, [2.3, 2.5], active=(2, 1), barre=("B2", "=15-2*A2"),
                                                 vert={(r, 1) for r in range(2, 10)}, orange={(10, 1)}))

# =============================================================== 2952 randonnée : profil
DONNEES["profil"] = [(0, 1200), (1, 1300), (2, 1400), (3, 1600), (4, 1750), (5, 1850),
                     (6, 1800), (7, 1600), (8, 1500), (9, 1500), (10, 1400)]
P52 = (r"width=5.8cm, height=5.2cm, xmin=0, xmax=10.8, ymin=1100, ymax=1960, xtick=" + lst(1, 10, 1)
       + r", ytick={1100,1200,1300,1400,1500,1600,1700,1800,1900}, minor y tick num=1, axis lines=left"
       + r", every axis x label/.style={at={(axis description cs:1,0)},anchor=west,xshift=2pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}"
       + r", every axis y label/.style={at={(axis description cs:0,1)},anchor=south west,xshift=-4pt,yshift=1pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")
B52 = poly(DONNEES["profil"])
FIGURES["ex2952_enonce"] = G(P52, B52, "distance (km)", "altitude (m)", zero=False)
FIGURES["ex2952_corrige"] = G(P52, B52 + r"""
  \draw[niveau] (axis cs:0,1600) -- (axis cs:7,1600);
  \draw[lecture] (axis cs:3,1600) -- (axis cs:3,1100);
  \draw[lecture] (axis cs:7,1600) -- (axis cs:7,1100);
  \pv{3}{1600} \pv{7}{1600} \pv{5}{1850}
  \draw[otGreenDark,line width=2.6pt] (axis cs:8,1500) -- (axis cs:9,1500);
  \node[vert,anchor=south] at (axis cs:5,1870) {sommet : $1\,850$ m};
  \node[vert,anchor=north] at (axis cs:8.5,1480) {plat};
""", "distance (km)", "altitude (m)", zero=False)
