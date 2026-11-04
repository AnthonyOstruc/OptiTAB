# -*- coding: utf-8 -*-
"""Figures de la notion « Échantillonnage » (Seconde).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Toutes les données sont produites par des simulations à graine fixe
(module random de Python) : les mêmes fonctions sont rejouées par
../verif_echantillonnage.py, qui vérifie chaque nombre cité dans le texte.
"""
import random

PREAMBULE_EXTRA = r"""
\tikzset{
  bande/.style={fill=otGreen!16, draw=none},
  bord/.style={otGreenDark, line width=0.8pt},
  lab/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  labV/.style={font=\normalsize, text=otGreenDark, inner sep=1.5pt},
  labO/.style={font=\normalsize, text=otOrange!85!black, inner sep=1.5pt},
}
"""


# ---------------------------------------------------------------- données
def echantillon(rng, n, p):
    """Nombre de succès dans un échantillon de taille n."""
    k = 0
    for _ in range(n):
        if rng.random() < p:
            k += 1
    return k


def serie(graine, N, n, p):
    """Liste des nombres de succès de N échantillons de taille n."""
    rng = random.Random(graine)
    return [echantillon(rng, n, p) for _ in range(N)]


def cumul(graine, n_max, p):
    """Fréquences cumulées f_1, …, f_{n_max} d'une suite de lancers."""
    rng = random.Random(graine)
    k, fr = 0, []
    for i in range(1, n_max + 1):
        if rng.random() < p:
            k += 1
        fr.append(k / i)
    return fr


GRAINES_STAB = (2, 8, 17)         # trois suites de 1000 lancers d'une pièce
GRAINE_COURS = 197                # 100 échantillons de taille 100, p = 0,5
GRAINE_N2 = 1132                  # 50 échantillons de taille 100, p = 0,4


def hors_bande(ks, n, p):
    """Indices des échantillons tels que |f - p| > 1/sqrt(n) (en entiers :
    |k - n p| > sqrt(n), n carré parfait)."""
    r = int(round(n ** 0.5))
    np_ = int(round(n * p))
    return [i for i, k in enumerate(ks) if abs(k - np_) > r]


# ---------------------------------------------------------------- outils TikZ
def _points(ks, n, hors, couleur_hors="otNavy", r="1.55pt"):
    lignes = []
    for i, k in enumerate(ks):
        c = couleur_hors if i in hors else "otNavy"
        lignes.append(rf"  \fill[{c}] (axis cs:{i + 1},{k / n:.2f}) circle ({r});")
    return "\n".join(lignes)


def nuage(ks, n, p, N, surligner, etiquettes=True):
    """etiquettes=False (figure d'énoncé) : ni la droite y = p ni les valeurs écrites
    à droite, que l'élève doit calculer lui-même (question 1 de l'exercice 3753)."""
    e = 1 / n ** 0.5
    bas, haut = p - e, p + e
    hors = set(hors_bande(ks, n, p)) if surligner else set()
    ymin, ymax = round(p - 2.5 * e, 2), round(p + 2.5 * e, 2)
    yt = ",".join(f"{p + j * e:.2f}" for j in (-2, -1, 0, 1, 2))
    pas = 20 if N == 100 else 10
    def fr(x):
        return f"{x:.1f}".replace(".", "{,}")
    if not etiquettes:
        return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, axis lines=left, width=6.2cm, height=4.6cm,
  xmin=0, xmax={N + 1}, ymin={ymin}, ymax={ymax},
  xtick={{0,{pas},...,{N}}}, ytick={{{yt}}},
  yticklabel style={{/pgf/number format/fixed,/pgf/number format/precision=1,anchor=east,xshift=-1pt,yshift=0pt}},
  xlabel={{échantillon}}, ylabel={{$f$}},
  every axis x label/.style={{at={{(current axis.right of origin)}},anchor=west,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted,xshift=2pt}},
  every axis y label/.style={{at={{(current axis.above origin)}},anchor=south,font=\normalsize,text=otMuted,yshift=2pt}}]
  \fill[bande] (axis cs:0,{bas:.2f}) rectangle (axis cs:{N + 1},{haut:.2f});
  \draw[bord] (axis cs:0,{bas:.2f}) -- (axis cs:{N + 1},{bas:.2f});
  \draw[bord] (axis cs:0,{haut:.2f}) -- (axis cs:{N + 1},{haut:.2f});
{_points(ks, n, hors, "otOrange")}
\end{{axis}}
\end{{tikzpicture}}"""
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, axis lines=left, width=6.2cm, height=4.6cm,
  xmin=0, xmax={N + 1}, ymin={ymin}, ymax={ymax},
  xtick={{0,{pas},...,{N}}}, ytick={{{yt}}},
  yticklabel style={{/pgf/number format/fixed,/pgf/number format/precision=1,anchor=east,xshift=-1pt,yshift=0pt}},
  xlabel={{échantillon}}, ylabel={{$f$}},
  every axis x label/.style={{at={{(current axis.right of origin)}},anchor=west,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted,xshift=2pt}},
  every axis y label/.style={{at={{(current axis.above origin)}},anchor=south,font=\normalsize,text=otMuted,yshift=2pt}}]
  \fill[bande] (axis cs:0,{bas:.2f}) rectangle (axis cs:{N + 1},{haut:.2f});
  \draw[bord] (axis cs:0,{bas:.2f}) -- (axis cs:{N + 1},{bas:.2f});
  \draw[bord] (axis cs:0,{haut:.2f}) -- (axis cs:{N + 1},{haut:.2f});
  \draw[seuil] (axis cs:0,{p:.2f}) -- (axis cs:{N + 1},{p:.2f});
{_points(ks, n, hors, "otOrange")}
  \node[labV, anchor=west] at (axis cs:{N + 1},{haut:.2f}) {{$p+\frac{{1}}{{\sqrt{{n}}}}={fr(haut)}$}};
  \node[labO, anchor=west] at (axis cs:{N + 1},{p:.2f}) {{$p={fr(p)}$}};
  \node[labV, anchor=west] at (axis cs:{N + 1},{bas:.2f}) {{$p-\frac{{1}}{{\sqrt{{n}}}}={fr(bas)}$}};
\end{{axis}}
\end{{tikzpicture}}"""


def courbes_stabilisation():
    couleurs = ("otNavy", "otGreenDark", "otRed!85!black")
    indices = list(range(10, 101)) + list(range(104, 301, 4)) + list(range(310, 1001, 10))
    plots = []
    for g, c in zip(GRAINES_STAB, couleurs):
        fr = cumul(g, 1000, 0.5)
        coords = " ".join(f"({i},{fr[i - 1]:.4f})" for i in indices)
        plots.append(rf"  \addplot[{c}, line width=0.9pt, line join=round] coordinates {{{coords}}};")
    plots = "\n".join(plots)
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=7.0cm, height=4.4cm,
  xmin=0, xmax=1000, ymin=0, ymax=1,
  xtick={{200,400,600,800,1000}}, ytick={{0.25,0.5,0.75,1}},
  yticklabel style={{/pgf/number format/fixed,/pgf/number format/precision=2,anchor=east,xshift=-1pt,yshift=0pt}},
  xlabel={{$n$}}, ylabel={{$f$}}]
  \draw[seuil] (axis cs:0,0.5) -- (axis cs:1000,0.5);
{plots}
  \node[labO, anchor=west] at (axis cs:1020,0.5) {{$p=0{{,}}5$}};
\end{{axis}}
\end{{tikzpicture}}"""


def intervalles_2011():
    """Exercice 2011 : intervalles [p - e ; p + e] des séries A et B."""
    sx = 15.0  # 1 unité de fréquence = 15 cm  (0,25 -> 0,75 : 7,5 cm)
    def X(v):
        return (v - 0.25) * sx
    def fr(v):
        return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", "{,}")
    l = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for nom, y, a, b, f, coul in (("A", 1.6, 0.3, 0.7, 0.64, "otGreenDark"),
                                  ("B", 0.0, 0.45, 0.55, 0.59, "otOrange!90!black")):
        l.append(rf"\draw[otMuted, line width=0.6pt] ({X(0.25):.2f},{y}) -- ({X(0.75):.2f},{y});")
        l.append(rf"\node[lab, anchor=east] at ({X(0.25) - 0.15:.2f},{y}) {{Série {nom}}};")
        l.append(rf"\draw[otNavy, line width=3pt, opacity=0.35] ({X(a):.2f},{y}) -- ({X(b):.2f},{y});")
        for v in (a, b):
            l.append(rf"\draw[otNavy, line width=0.9pt] ({X(v):.2f},{y - 0.14}) -- ({X(v):.2f},{y + 0.14});")
            l.append(rf"\node[lab, anchor=north] at ({X(v):.2f},{y - 0.18}) {{${fr(v)}$}};")
        l.append(rf"\draw[otOrange, line width=0.7pt, dash pattern=on 2pt off 1.5pt] ({X(0.5):.2f},{y - 0.1}) -- ({X(0.5):.2f},{y + 0.1});")
        l.append(rf"\fill[{coul}] ({X(f):.2f},{y}) circle (2.6pt);")
        l.append(rf"\node[font=\normalsize, text={coul}, anchor=south, inner sep=1.5pt] at ({X(f):.2f},{y + 0.22}) {{$f_{nom}={fr(f)}$}};")
    l.append(rf"\node[labO, anchor=south] at ({X(0.5):.2f},{1.6 + 0.16}) {{$p=0{{,}}5$}};")
    l.append(rf"\node[labO, anchor=south] at ({X(0.5):.2f},{0.16}) {{$p$}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {}
# Cours et fiche
FIGURES["cours_stabilisation"] = courbes_stabilisation()
FIGURES["cours_fluctuation"] = nuage(serie(GRAINE_COURS, 100, 100, 0.5), 100, 0.5, 100, True)
# Exercice nouveau-2 (3753) : nuage à lire (énoncé, sans les valeurs à calculer) et corrigé
FIGURES["n2_nuage"] = nuage(serie(GRAINE_N2, 50, 100, 0.4), 100, 0.4, 50, False, etiquettes=False)
FIGURES["n2_nuage_corrige"] = nuage(serie(GRAINE_N2, 50, 100, 0.4), 100, 0.4, 50, True)
# Exercice 2011 : comparaison des deux séries
FIGURES["e2011_intervalles"] = intervalles_2011()


# ================================================================ FINITION 2026-11-02
STY = (r"\tikzset{grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},"
       r"axe/.style={otMuted,line width=.6pt},tic/.style={otMuted,line width=.5pt}}")


def frv(x, dec=None):
    s = f"{x:.{dec}f}" if dec is not None else "%g" % x
    ent, _, d = s.partition(".")
    if len(ent.lstrip("-")) > 3:
        ent = ent[:-3] + r"\," + ent[-3:]
    return ent + ("{,}" + d if d else "")


TIRAGES_2009 = [0.12, 0.77, 0.05, 0.31, 0.29, 0.90, 0.18, 0.33, 0.02, 0.60]


def seuil_2009():
    """2009 : les dix nombres renvoyés par random() sur [0 ; 1[ ; succès si < 0,3."""
    u = 8.4
    X = lambda v: v * u
    L = [r"\begin{tikzpicture}", STY]
    L.append(r"\fill[otGreen!20] (0,-0.12) rectangle (%.3f,0.5);" % X(0.3))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (X(1) + 0.4))
    for k in range(11):
        v = k / 10
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (X(v), X(v)))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.16) {%s};" % (X(v), frv(v)))
    L.append(r"\node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (%.3f,0.5) {$[0\,;0{,}3[$ : succès};" % X(0.15))
    for v in TIRAGES_2009:
        col = "otGreenDark" if v < 0.3 else "otNavy!60"
        L.append(r"\fill[%s] (%.3f,0.25) circle (2.3pt);" % (col, X(v)))
    L.append(r"\node[anchor=south,text=otNavy,inner sep=1.5pt] at (%.3f,0.5) {$[0{,}3\,;1[$ : échecs};" % X(0.65))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def lignes_intervalles(rangs, a, b, u, pas, marque=None, legende=None, larg_nom=1.9):
    """Intervalles sur des axes parallèles ; rangs = [(nom, bas, haut, f, dedans)], de haut en bas.
    marque = (valeur, texte) : droite verticale orange (valeur testée)."""
    X = lambda v: larg_nom + (v - a) * u
    L = [r"\begin{tikzpicture}", STY]
    k = len(rangs)
    for j, (nom, bas, haut, f, dedans) in enumerate(rangs):
        y = (k - j) * 0.75
        L.append(r"\node[grad,anchor=east,font=\otRegular\fontsize{9}{10}\selectfont] at (%.3f,%.3f) {%s};" % (larg_nom - 0.15, y, nom))
        L.append(r"\draw[otRule,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X(a), y, X(b), y))
        L.append(r"\draw[otNavy!45,line width=4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X(bas), y, X(haut), y))
        for v in (bas, haut):
            L.append(r"\draw[otNavy,line width=.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X(v), y - 0.14, X(v), y + 0.14))
        col = "otGreenDark" if dedans else "otOrange!90!black"
        L.append(r"\fill[%s] (%.3f,%.3f) circle (2.6pt);" % (col, X(f), y))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (%.3f,0) -- (%.3f,0);" % (X(a), X(b) + 0.35))
    v = a
    while v <= b + 1e-9:
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (X(v), X(v)))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.14) {%s};" % (X(v), frv(round(v, 2))))
        v += pas
    if marque:
        val, txt = marque
        L.append(r"\draw[otOrange!90!black,line width=.8pt,dash pattern=on 3pt off 2pt] (%.3f,-0.05) -- (%.3f,%.3f);" % (X(val), X(val), k * 0.75 + 0.45))
        L.append(r"\node[anchor=south,text=otOrange!90!black,inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (X(val), k * 0.75 + 0.48, txt))
    if legende:
        L.append(r"\node[anchor=north,text=otMuted,inner sep=1pt] at (%.3f,-0.6) {%s};" % ((X(a) + X(b)) / 2, legende))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# 2007 : intervalles d'estimation des quatre échantillons, et la valeur p = 0,20 annoncée
FIGURES["e2007_intervalles"] = lignes_intervalles(
    [(r"$n = 100$", 0.32, 0.52, 0.42, True), (r"$n = 900$", 0.486, 0.554, 0.52, True),
     (r"$n = 25$", 0.0, 0.28, 0.08, True), (r"$n = 1\,600$", 0.135, 0.185, 0.16, True)],
    0, 0.6, 11.0, 0.1, marque=(0.20, r"$p = 0{,}20$ ?"),
    legende=r"point : fréquence $f$ ; barre : intervalle d’estimation")


def normalises_2006():
    """2006 : chaque intervalle [p - e ; p + e] dessiné à la même longueur ; f placé à (f - p)/e."""
    cas = [("0{,}45", "0{,}55", "0{,}5", 0.58, 0.5, 0.05), ("0{,}2", "0{,}4", "0{,}3", 0.39, 0.3, 0.1),
           ("0{,}10", "0{,}14", "0{,}12", 0.15, 0.12, 0.02), (r"0{,}583", r"0{,}717", "0{,}65", 0.60, 0.65, 1 / 15),
           ("0{,}6", "1", "0{,}8", 0.55, 0.8, 0.2)]
    E = 1.9          # longueur d'un demi-intervalle (cm)
    x0 = 4.3         # abscisse de p
    L = [r"\begin{tikzpicture}", STY]
    for j, (gb, gh, gp, f, p, e) in enumerate(cas):
        y = -j * 1.05
        L.append(r"\node[grad,anchor=west] at (0,%.3f) {Q%d};" % (y, j + 1))
        L.append(r"\draw[otRule,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0 - 3.4, y, x0 + 3.4, y))
        L.append(r"\draw[otNavy!45,line width=4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0 - E, y, x0 + E, y))
        for xx in (x0 - E, x0 + E):
            L.append(r"\draw[otNavy,line width=.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (xx, y - 0.14, xx, y + 0.14))
        L.append(r"\draw[otOrange!90!black,line width=.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, y - 0.1, x0, y + 0.1))
        L.append(r"\node[grad,anchor=north] at (%.3f,%.3f) {$%s$};" % (x0 - E, y - 0.17, gb))
        L.append(r"\node[grad,anchor=north] at (%.3f,%.3f) {$%s$};" % (x0 + E, y - 0.17, gh))
        L.append(r"\node[grad,anchor=north,text=otOrange!90!black] at (%.3f,%.3f) {$p = %s$};" % (x0, y - 0.17, gp))
        xf = x0 + (f - p) / e * E
        dedans = abs(f - p) <= e + 1e-12
        col = "otGreenDark" if dedans else "otOrange!90!black"
        L.append(r"\fill[%s] (%.3f,%.3f) circle (2.7pt);" % (col, xf, y))
        L.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%.3f,%.3f) {$f = %s$};" % (col, xf, y + 0.14, frv(f, 2)))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e2006_bilan"] = normalises_2006()


def ecarts_2005():
    """2005 : écart observé |f - p| (bleu ou orange) et seuil 1/racine(n) (vert) pour les quatre situations."""
    cas = [("pièces", 0.03, 0.05, "0{,}03", "0{,}05"), ("dé", 35 / 900, 1 / 30, r"0{,}039", r"0{,}033"),
           ("jury", 0.22, 0.1, "0{,}22", "0{,}1"), ("pièce", 0.016, 0.02, "0{,}016", "0{,}02")]
    u = 26.0
    x0 = 1.55
    L = [r"\begin{tikzpicture}", STY]
    for j, (nom, ec, s, tec, ts) in enumerate(cas):
        y = -j * 1.15
        col = "otNavy!60" if ec <= s else "otOrange!85"
        L.append(r"\node[grad,anchor=east] at (%.3f,%.3f) {%s};" % (x0 - 0.12, y - 0.05, nom))
        L.append(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, x0, y, x0 + ec * u, y + 0.26))
        L.append(r"\fill[otGreen!75] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, y - 0.36, x0 + s * u, y - 0.1))
        L.append(r"\node[anchor=west,inner sep=1.5pt,text=%s] at (%.3f,%.3f) {$|f - p| = %s$};" % ("otNavy" if ec <= s else "otOrange!90!black", x0 + ec * u + 0.05, y + 0.13, tec))
        L.append(r"\node[anchor=west,inner sep=1.5pt,text=otGreenDark] at (%.3f,%.3f) {$1/\sqrt{n} = %s$};" % (x0 + s * u + 0.05, y - 0.23, ts))
    L.append(r"\draw[axe] (%.3f,0.35) -- (%.3f,%.3f);" % (x0, x0, -3 * 1.15 - 0.5))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e2005_ecarts"] = ecarts_2005()

# 2008 : la courbe de n -> 1/racine(n) et les tailles minimales
FIGURES["e2008_courbe"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7.0cm, height=4.6cm,
  xmin=0, xmax=1250, ymin=0, ymax=0.2, domain=25:1250, samples=300,
  xtick={0,200,400,600,800,1000,1200}, ytick={0.05,0.1,0.15,0.2},
  yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2,anchor=east,xshift=-1pt,yshift=0pt},
  xlabel={$n$}, ylabel={$\frac{1}{\sqrt{n}}$},
  every axis y label/.style={at={(current axis.above origin)},anchor=south,font=\normalsize,text=otMuted,yshift=2pt}]
  \addplot[courbe] {1/sqrt(x)};
  \draw[seuil] (axis cs:0,0.1) -- (axis cs:1250,0.1);
  \draw[seuil] (axis cs:0,0.05) -- (axis cs:1250,0.05);
  \draw[seuil] (axis cs:0,0.03) -- (axis cs:1250,0.03);
  \draw[guide] (axis cs:100,0) -- (axis cs:100,0.1);
  \draw[guide] (axis cs:400,0) -- (axis cs:400,0.05);
  \draw[guide] (axis cs:1112,0) -- (axis cs:1112,0.03);
  \fill[otGreenDark] (axis cs:100,0.1) circle (2.3pt);
  \fill[otGreenDark] (axis cs:400,0.05) circle (2.3pt);
  \fill[otGreenDark] (axis cs:1112,0.029987) circle (2.3pt);
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:105,0.1) {$n = 100$};
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:405,0.05) {$n = 400$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:1100,0.002) {$n = 1\,112$};
  \node[anchor=west,text=otOrange!90!black,inner sep=1.5pt] at (axis cs:1255,0.03) {$e = 0{,}03$};
\end{axis}
\end{tikzpicture}"""

# nouveau-1 (3752) : la fréquence se stabilise (abscisses non proportionnelles)
PALIERS_3752 = [10, 50, 100, 500, 1000, 5000, 10000]
SUCCES_3752 = [9, 37, 66, 321, 642, 3099, 6196]


def stabilisation_3752():
    dx, uy, y0 = 1.05, 10.0, 0.55
    Y = lambda f: (f - y0) * uy
    L = [r"\begin{tikzpicture}", STY]
    xr = (len(PALIERS_3752) + 0.2) * dx
    for v in (0.6, 0.7, 0.8, 0.9):
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (Y(v), xr, Y(v)))
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (Y(v), Y(v)))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (Y(v), frv(v)))
    pts = []
    for i, (n, k) in enumerate(zip(PALIERS_3752, SUCCES_3752)):
        X = (i + 0.6) * dx
        pts.append((X, Y(k / n)))
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (X, X))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (X, frv(n)))
    L.append(r"\draw[otNavy,line width=1pt] " + " -- ".join("(%.3f,%.3f)" % p for p in pts) + ";")
    for X, yv in pts:
        L.append(r"\fill[otNavy] (%.3f,%.3f) circle (2.3pt);" % (X, yv))
    L.append(r"\draw[seuil] (0,%.3f) -- (%.3f,%.3f);" % (Y(0.62), xr, Y(0.62)))
    L.append(r"\node[anchor=south east,text=otOrange!90!black,inner sep=1.5pt] at (%.3f,%.3f) {$f \approx 0{,}62$};" % (xr, Y(0.62) + 0.04))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (Y(0.95) + 0.3))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % xr)
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {fréquence $f$};" % (Y(0.95) + 0.3))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {nombre $n$ de lancers (échelle non proportionnelle)};" % xr)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e2009_seuil"] = seuil_2009()
FIGURES["e3752_stabilisation"] = stabilisation_3752()
