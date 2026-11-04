# -*- coding: utf-8 -*-
"""Figures de la notion 271 « Proportionnalité et pourcentages » (5e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = contre-exemple ou élément d'alerte.
Toutes les figures restent étroites (≤ 7,5 cm environ) pour rester lisibles sur
téléphone sans réduction.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  fl/.style={otNavy,line width=.85pt,-{Stealth[length=2.2mm]}},
  flV/.style={otGreenDark,line width=.85pt,-{Stealth[length=2.2mm]}},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
  accolV/.style={decorate,decoration={brace,amplitude=5pt},otGreenDark,line width=.8pt},
  accolN/.style={decorate,decoration={brace,amplitude=5pt},otNavy,line width=.8pt},
  coteV/.style={otGreenDark,line width=.6pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}},
}
"""

FIGURES = {}


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def f(x):
    """Nombre au format TikZ."""
    return "%.3f" % x


# ================================================================== TABLEAU DE PROPORTIONNALITÉ
def tableau(entetes, l1, l2, coef=None, coef_vert=False, w0=2.3, w=1.15, vertes=(),
            haut=(), bas=(), note=None, note_vert=True):
    """Tableau à deux lignes, style des livres.

    haut / bas : flèches courbes entre colonnes (i, j, étiquette, vert?) au-dessus de
    la 1re ligne / au-dessous de la 2de ligne. coef : flèche latérale « × coef ».
    vertes : cases (ligne, colonne) écrites en vert (réponses).
    """
    h = .75
    s = []
    n = len(l1)
    W = w0 + n * w
    for r, (ent, ligne) in enumerate(((entetes[0], l1), (entetes[1], l2))):
        y = -r * h
        s.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(y), f(w0), f(y - h)))
        s.append(r"\node[txt,text=otNavy] at (%s,%s) {%s};" % (f(w0 / 2), f(y - h / 2), ent))
        for k, v in enumerate(ligne):
            c = "otGreenDark" if (r, k) in vertes else "otInk"
            s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(w0 + (k + .5) * w), f(y - h / 2), v))
    s += [r"\draw[otNavy,line width=.7pt] (0,0) rectangle (%s,%s);" % (f(W), f(-2 * h)),
          r"\draw[otNavy,line width=.7pt] (0,%s) -- (%s,%s);" % (f(-h), f(W), f(-h))]
    for k in range(n):
        s.append(r"\draw[otNavy,line width=.7pt] (%s,0) -- (%s,%s);" % (f(w0 + k * w), f(w0 + k * w), f(-2 * h)))

    def arc(i, j, lab, vert, dessus):
        xi, xj = w0 + (i + .5) * w, w0 + (j + .5) * w
        st, col = ("flV", "otGreenDark") if vert else ("fl", "otNavy")
        if dessus:
            y0, yc, sens, anc = .08, .62, 1, "south"
        else:
            y0, yc, sens, anc = -2 * h - .08, -2 * h - .62, -1, "north"
        xa, xb = xi + .12 * (1 if xj > xi else -1), xj - .12 * (1 if xj > xi else -1)
        s.append(r"\draw[%s] (%s,%s) .. controls (%s,%s) and (%s,%s) .. (%s,%s);"
                 % (st, f(xa), f(y0), f(xa), f(yc), f(xb), f(yc), f(xb), f(y0)))
        pic = y0 + .75 * (yc - y0)
        s.append(r"\node[text=%s,anchor=%s,inner sep=1pt] at (%s,%s) {$%s$};"
                 % (col, anc, f((xi + xj) / 2), f(pic + sens * .07), lab))

    for a in haut:
        arc(a[0], a[1], a[2], a[3] if len(a) > 3 else False, True)
    for a in bas:
        arc(a[0], a[1], a[2], a[3] if len(a) > 3 else False, False)
    if coef is not None:
        st, c = ("flV", "otGreenDark") if coef_vert else ("fl", "otNavy")
        s += [r"\draw[%s] (%s,%s) to[out=0,in=0,looseness=1.6] (%s,%s);" % (st, f(W + .1), f(-h / 2), f(W + .1), f(-1.5 * h)),
              r"\node[text=%s,anchor=west] at (%s,%s) {$\times %s$};" % (c, f(W + .62), f(-h), coef)]
    if note:
        yb = -2 * h - (.95 if bas else .25)
        col = "otGreenDark" if note_vert else "otInk"
        s.append(r"\node[text=%s,anchor=north west] at (0,%s) {%s};" % (col, f(yb), note))
    return figure(s)


# Cours : le tissu à 6 € le mètre
FIGURES["cours_tableau"] = tableau(("longueur (m)", "prix (€)"), ("1", "2", "3{,}5", "5"),
                                   ("6", "12", "21", "30"), coef="6", w0=2.45, w=.95)

# Cours / fiche : 5 baguettes pour 4,50 € — passage par l'unité
FIGURES["cours_unite"] = tableau(("baguettes", "prix (€)"), ("5", "1", "8"), ("4{,}50", "0{,}90", "7{,}20"),
                                 coef="0{,}9", w0=1.95, w=1.15,
                                 haut=[(0, 1, r"\div 5"), (1, 2, r"\times 8")],
                                 bas=[(0, 1, r"\div 5"), (1, 2, r"\times 8")])

# 2921 : la recette de crêpes (corrigé)
FIGURES["ex2921_corrige"] = tableau(("personnes", "farine (g)"), ("4", "1", "6", "10"),
                                    ("250", "62{,}5", "375", "625"), coef="62{,}5", coef_vert=True,
                                    w0=2.0, w=.95, vertes={(1, 1), (1, 2), (1, 3)},
                                    haut=[(0, 1, r"\div 4"), (1, 2, r"\times 6")])

# 2915 : le gazole (corrigé)
FIGURES["ex2915_corrige"] = tableau(("volume (L)", "prix (€)"), ("5", "10", "20", "25"),
                                    ("9", "18", "36", "45"), coef="1{,}8", coef_vert=True,
                                    w0=2.05, w=.98, vertes={(1, 0), (1, 2), (1, 3)},
                                    haut=[(1, 0, r"\div 2"), (1, 2, r"\times 2")],
                                    bas=[(1, 0, r"\div 2", True), (1, 2, r"\times 2", True)],
                                    note=r"$25 = 5 + 20$, donc $9 + 36 = 45$ €")

# 2935 : le goûter (corrigé)
FIGURES["ex2935_corrige"] = tableau(("personnes", "fruits (g)"), ("8", "1", "20", "16"),
                                    ("600", "75", r"1\,500", r"1\,200"), coef="75", coef_vert=True,
                                    w0=2.0, w=1.02, vertes={(1, 1), (1, 2), (1, 3)},
                                    haut=[(0, 1, r"\div 8"), (1, 2, r"\times 20")])


# ================================================================== BARRE DE POURCENTAGE
def barre(total, part, k, unite, titre_part, reste=None, L=6.6, H=.75):
    """Barre de 10 cases = 100 % ; k cases en vert.

    total : texte de la quantité totale ; part : valeur d'une case (10 %) ;
    titre_part : texte vert sous les k cases ; reste : texte navy sous les autres cases.
    """
    n = 10
    u = L / n
    s = [r"\fill[otGreen!35] (0,0) rectangle (%s,%s);" % (f(k * u), f(H)),
         r"\fill[otSky] (%s,0) rectangle (%s,%s);" % (f(k * u), f(L), f(H))]
    for i in range(1, n):
        s.append(r"\draw[otNavy!55,line width=.5pt] (%s,0) -- (%s,%s);" % (f(i * u), f(i * u), f(H)))
    s += [r"\draw[otNavy,line width=.8pt] (0,0) rectangle (%s,%s);" % (f(L), f(H)),
          r"\draw[otGreenDark,line width=1.1pt] (%s,0) -- (%s,%s);" % (f(k * u), f(k * u), f(H)),
          r"\draw[accol] (0,%s) -- (%s,%s);" % (f(H + .12), f(L), f(H + .12)),
          r"\node[anchor=south] at (%s,%s) {%s};" % (f(L / 2), f(H + .42),
                                                     "$100\\,\\%$ : " + total + " \\quad (10 cases de " + part + " " + unite + ")"),
          r"\draw[accolV] (%s,-.12) -- (0,-.12);" % f(k * u),
          r"\node[text=otGreenDark,anchor=north west] at (0,-.45) {%s};" % titre_part]
    # valeur de chaque case (10 %), écrite au milieu de la case
    for i in range(n):
        col = "otGreenDark" if i < k else "otNavy"
        s.append(r"\node[text=%s,font=\otMedium\fontsize{8.5}{10}\selectfont,inner sep=0pt] at (%s,%s) {%s};"
                 % (col, f((i + .5) * u), f(H / 2), part))
    if reste:
        s += [r"\draw[accolN] (%s,-1.1) -- (%s,-1.1);" % (f(L), f(k * u)),
              r"\node[text=otNavy,anchor=north east] at (%s,-1.43) {%s};" % (f(L), reste)]
    return figure(s)


FIGURES["cours_pourcentage"] = barre("$60$ €", "$6$", 3, "€", "$30\\,\\%$ de $60$ € $= 3 \\times 6 = 18$ €")
FIGURES["ex2917_corrige"] = barre("$40$ adhérents", "$4$", 3, "adhérents",
                                  "$30\\,\\%$ de $40 = 3 \\times 4 = 12$ adhérents")
FIGURES["ex2927_corrige"] = barre("$80$ €", "$8$", 3, "€", "remise de $30\\,\\%$ : $3 \\times 8 = 24$ €",
                                  reste="prix payé : $80 - 24 = 56$ €")


# ================================================================== GRAPHIQUES
LAB = (r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-15pt,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},"
       r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}")


def carre(x, y, col):
    return r"\fill[%s] (axis cs:%s,%s) ++(-2.4pt,-2.4pt) rectangle ++(4.8pt,4.8pt);" % (col, x, y)


def graphe_2920(corr):
    A = [(1, 2.5), (2, 5), (4, 10), (5, 12.5)]
    B = [(1, 5), (2, 8), (3, 11), (5, 17)]
    c = []
    if corr:
        c += [r"\addplot[otGreenDark,line width=1.3pt,domain=0:6] {2.5*x};",
              r"\addplot[otOrange!85!black,line width=1.1pt,dash pattern=on 4pt off 2.5pt,domain=0:6] {3*x+2};",
              r"\fill[otGreenDark] (axis cs:0,0) circle (2.6pt);",
              r"\draw[otOrange!85!black,fill=white,line width=1pt] (axis cs:0,2) circle (2.6pt);"]
    for x, y in A:
        c.append(r"\fill[otNavy] (axis cs:%s,%s) circle (2.5pt);" % (x, y))
    for x, y in B:
        c.append(carre(x, y, "otOrange!85!black"))
    if corr:
        c += [r"\node[text=otGreenDark,anchor=west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:6.25,15) {A : passe\\par l'origine};",
              r"\node[text=otOrange!80!black,anchor=west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:6.25,20.5) {B : ne passe pas\\par l'origine};"]
    else:
        c += [r"\node[text=otNavy,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:5.35,12.5) {tableau A};",
              r"\node[text=otOrange!80!black,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:5.35,17) {tableau B};"]
    return "\n".join([r"\begin{tikzpicture}",
                      r"\begin{axis}[otWeb, width=%s, height=5.2cm, xmin=0, xmax=6.3, ymin=0, ymax=21.5," % ("4.25cm" if corr else "5.0cm")
                      + r" xtick={1,...,6}, ytick={2,4,...,20}, xlabel={masse (kg)}, ylabel={prix (€)}," + LAB + "]"]
                     + c + [r"\end{axis}", r"\end{tikzpicture}"])


FIGURES["ex2920_enonce"] = graphe_2920(False)
FIGURES["ex2920_corrige"] = graphe_2920(True)


def graphe_cours():
    """Tissu (6 €/m, proportionnel) et taxi (4 € + 2 €/km, non proportionnel) côte à côte."""
    tissu = [(1, 6), (2, 12), (3.5, 21), (5, 30)]
    taxi = [(1, 6), (2, 8), (3, 10), (5, 14)]
    g1 = [r"\begin{axis}[otWeb, name=g1, width=2.75cm, height=3.6cm, xmin=0, xmax=5.6, ymin=0, ymax=33,"
          r" xtick={1,...,5}, ytick={6,12,...,30}, xlabel={longueur (m)}, ylabel={prix (€)}," + LAB
          + r", title={tissu}, title style={font=\otMedium\fontsize{9}{11}\selectfont,text=otNavy,yshift=11pt}]",
          r"\addplot[courbe,domain=0:5.4] {6*x};",
          r"\fill[otNavy] (axis cs:0,0) circle (2.6pt);"]
    g1 += [r"\fill[otNavy] (axis cs:%s,%s) circle (2.3pt);" % p for p in tissu]
    g1 += [r"\end{axis}"]
    g2 = [r"\begin{axis}[otWeb, at={(g1.east)}, anchor=west, xshift=1.35cm, width=2.75cm, height=3.6cm, xmin=0, xmax=5.6, ymin=0, ymax=16.5,"
          r" xtick={1,...,5}, ytick={2,4,...,16}, xlabel={distance (km)}, ylabel={prix (€)}," + LAB
          + r", title={taxi}, title style={font=\otMedium\fontsize{9}{11}\selectfont,text=otOrange!80!black,yshift=11pt}]",
          r"\addplot[otOrange!85!black,line width=1.35pt,domain=0:5.4] {2*x+4};",
          r"\draw[otOrange!85!black,fill=white,line width=1pt] (axis cs:0,4) circle (2.6pt);"]
    g2 += [carre(x, y, "otOrange!85!black") for x, y in taxi]
    g2 += [r"\end{axis}"]
    return "\n".join([r"\begin{tikzpicture}"] + g1 + g2 + [r"\end{tikzpicture}"])


FIGURES["cours_graphique"] = graphe_cours()


# ================================================================== ÉCHELLE : TERRAIN (cours)
def terrain():
    k = 1.25          # 1 cm du plan -> 1,25 cm de figure
    L, l = 4 * k, 2 * k
    s = [r"\fill[otGreen!14] (0,0) rectangle (%s,%s);" % (f(L), f(l)),
         r"\draw[otNavy,line width=1pt] (0,0) rectangle (%s,%s);" % (f(L), f(l)),
         r"\draw[otNavy,line width=.6pt] (%s,0) -- (%s,%s);" % (f(L / 2), f(L / 2), f(l)),
         r"\draw[otNavy,line width=.6pt] (0,%s) arc[start angle=-90,end angle=90,radius=%s];" % (f(l / 2 - .6 * k), f(.6 * k)),
         r"\draw[otNavy,line width=.6pt] (%s,%s) arc[start angle=270,end angle=90,radius=%s];" % (f(L), f(l / 2 - .6 * k), f(.6 * k)),
         # cotes mesurées sur le plan
         r"\draw[cote] (0,-.38) -- (%s,-.38);" % f(L),
         r"\draw[otMuted!70,line width=.4pt] (0,-.08) -- (0,-.5) (%s,-.08) -- (%s,-.5);" % (f(L), f(L)),
         r"\node[anchor=north] at (%s,-.48) {$4$ cm};" % f(L / 2),
         r"\draw[cote] (-.38,0) -- (-.38,%s);" % f(l),
         r"\draw[otMuted!70,line width=.4pt] (-.08,0) -- (-.5,0) (-.08,%s) -- (-.5,%s);" % (f(l), f(l)),
         r"\node[anchor=east] at (-.48,%s) {$2$ cm};" % f(l / 2)]
    # échelle graphique (sous le plan) : 1 cm du plan = 10 m
    ex, ey = 0, -1.75
    for i in range(2):
        col = "otInk" if i == 0 else "white"
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (col, f(ex + i * k), f(ey), f(ex + (i + 1) * k), f(ey + .14)))
    s += [r"\draw[otInk,line width=.5pt] (%s,%s) rectangle (%s,%s);" % (f(ex), f(ey), f(ex + 2 * k), f(ey + .14)),
          r"\node[petit,anchor=north] at (%s,%s) {0};" % (f(ex), f(ey - .1)),
          r"\node[petit,anchor=north] at (%s,%s) {10 m};" % (f(ex + k), f(ey - .1)),
          r"\node[petit,anchor=north] at (%s,%s) {20 m};" % (f(ex + 2 * k), f(ey - .1)),
          r"\node[txt,anchor=west] at (%s,%s) {échelle $\dfrac{1}{1\,000}$};" % (f(ex + 2 * k + .9), f(ey + .07))]
    return figure(s)


FIGURES["cours_echelle"] = terrain()


# ================================================================== PLAN DE LA CHAMBRE (2924, 1/50)
def chambre(corr):
    k = .62
    L, l = 8 * k, 6 * k
    bl, bw = 4 * k, 1.8 * k
    tc, st = ("otGreenDark", "coteV") if corr else ("otInk", "cote")
    v = (r"4\ \text{m}", r"3\ \text{m}", r"2\ \text{m}", r"90\ \text{cm}") if corr else \
        (r"8\ \text{cm}", r"6\ \text{cm}", r"4\ \text{cm}", r"1{,}8\ \text{cm}")
    s = [r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(L), f(l)),
         r"\draw[otNavy,line width=1.6pt] (0,0) rectangle (%s,%s);" % (f(L), f(l)),
         # fenêtre sur le mur du haut
         r"\fill[white] (%s,%s) rectangle (%s,%s);" % (f(L * .55), f(l - .05), f(L * .85), f(l + .05)),
         r"\draw[otNavy,line width=.6pt] (%s,%s) rectangle (%s,%s);" % (f(L * .55), f(l - .05), f(L * .85), f(l + .05)),
         # lit dans le coin en bas à gauche
         r"\fill[white] (0,0) rectangle (%s,%s);" % (f(bl), f(bw)),
         r"\draw[otNavy,line width=.8pt] (0,0) rectangle (%s,%s);" % (f(bl), f(bw)),
         r"\fill[otMuted!18] (.1,.12) rectangle (.5,%s);" % f(bw - .12),
         r"\draw[otMuted,line width=.5pt] (.1,.12) rectangle (.5,%s);" % f(bw - .12),
         r"\node[txt,text=otNavy] at (%s,%s) {lit};" % (f((bl + .5) / 2), f(bw / 2)),
         r"\node[txt,text=otNavy] at (%s,%s) {chambre};" % (f(L * .62), f(l * .62)),
         # cotes de la chambre (extérieur)
         r"\draw[%s] (0,-.4) -- (%s,-.4);" % (st, f(L)),
         r"\draw[otMuted!70,line width=.4pt] (0,-.1) -- (0,-.52) (%s,-.1) -- (%s,-.52);" % (f(L), f(L)),
         r"\node[text=%s,anchor=north] at (%s,-.5) {$%s$};" % (tc, f(L / 2), v[0]),
         r"\draw[%s] (-.4,0) -- (-.4,%s);" % (st, f(l)),
         r"\draw[otMuted!70,line width=.4pt] (-.1,0) -- (-.52,0) (-.1,%s) -- (-.52,%s);" % (f(l), f(l)),
         r"\node[text=%s,anchor=east] at (-.5,%s) {$%s$};" % (tc, f(l / 2), v[1]),
         # cotes du lit (dans la chambre, dans l'espace libre)
         r"\draw[%s] (0,%s) -- (%s,%s);" % (st, f(bw + .32), f(bl), f(bw + .32)),
         r"\node[text=%s,anchor=south] at (%s,%s) {$%s$};" % (tc, f(bl / 2), f(bw + .4), v[2]),
         r"\draw[%s] (%s,0) -- (%s,%s);" % (st, f(bl + .32), f(bl + .32), f(bw)),
         r"\node[text=%s,anchor=west] at (%s,%s) {$%s$};" % (tc, f(bl + .42), f(bw / 2), v[3])]
    if not corr:
        s.append(r"\node[txt,anchor=north east] at (%s,-.55) {échelle $\dfrac{1}{50}$};" % f(L + .1))
    return figure(s)


FIGURES["ex2924_enonce"] = chambre(False)
FIGURES["ex2924_corrige"] = chambre(True)


# ================================================================== CARTE DE RANDONNÉE (2918, 1/25 000)
def triangle(a, b, c):
    """P = (0,0), L = (c, 0), C tel que PC = a et CL = b."""
    xC = (a * a - b * b + c * c) / (2 * c)
    yC = math.sqrt(a * a - xC * xC)
    return (0, 0), (xC, yC), (c, 0)


def carte(corr):
    u = .72
    P, C, Lc = triangle(4 * u, 6.4 * u, 5.6 * u)
    th = math.radians(8)

    def rot(p):
        return (p[0] * math.cos(th) - p[1] * math.sin(th), p[0] * math.sin(th) + p[1] * math.cos(th))
    P, C, Lc = rot(P), rot(C), rot(Lc)
    G = ((P[0] + C[0] + Lc[0]) / 3, (P[1] + C[1] + Lc[1]) / 3)
    xs, ys = [P[0], C[0], Lc[0]], [P[1], C[1], Lc[1]]
    x0, x1, y0, y1 = min(xs) - 1.75, max(xs) + .9, min(ys) - .85, max(ys) + .75
    s = [r"\fill[otGreen!9] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x1), f(y1)),
         r"\draw[otMuted,line width=.6pt] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x1), f(y1)),
         # le lac
         r"\fill[otSky] (%s,%s) ellipse (.62 and .34);" % (f(Lc[0] + .2), f(Lc[1] - .3)),
         r"\draw[otNavy!45,line width=.5pt] (%s,%s) ellipse (.62 and .34);" % (f(Lc[0] + .2), f(Lc[1] - .3)),
         r"\draw[otOrange!85!black,line width=1.5pt,line join=round] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
         % (f(P[0]), f(P[1]), f(C[0]), f(C[1]), f(Lc[0]), f(Lc[1]))]
    for p in (P, C, Lc):
        s.append(r"\fill[otNavy] (%s,%s) circle (2.6pt);" % (f(p[0]), f(p[1])))
    s += [r"\node[txt,text=otNavy,anchor=north east] at (%s,%s) {parking};" % (f(P[0] - .08), f(P[1] - .1)),
          r"\node[txt,text=otNavy,anchor=south] at (%s,%s) {cascade};" % (f(C[0]), f(C[1] + .14)),
          r"\node[txt,text=otNavy,anchor=north] at (%s,%s) {lac};" % (f(Lc[0] + .25), f(Lc[1] - .7))]
    if corr:
        vals = (r"$1$ km", r"$1{,}6$ km", r"$1{,}4$ km")
        col = "otGreenDark"
    else:
        vals = (r"$4$ cm", r"$6{,}4$ cm", r"$5{,}6$ cm")
        col = "otInk"
    for (A, B), t in zip(((P, C), (C, Lc), (Lc, P)), vals):
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        dx, dy = mx - G[0], my - G[1]
        nrm = math.hypot(dx, dy)
        dx, dy = dx / nrm, dy / nrm
        ang = math.degrees(math.atan2(dy, dx))
        anc = {0: "west", 1: "south west", 2: "south", 3: "south east", 4: "east", 5: "north east",
               6: "north", 7: "north west"}[int(((ang + 22.5) % 360) // 45)]
        s.append(r"\node[text=%s,anchor=%s] at (%s,%s) {%s};" % (col, anc, f(mx + .16 * dx), f(my + .16 * dy), t))
    if corr:
        s.append(r"\node[text=otGreenDark,anchor=north west] at (%s,%s) {boucle : $1 + 1{,}6 + 1{,}4 = 4$ km};" % (f(x0), f(y0 - .15)))
    else:
        s.append(r"\node[txt,anchor=north west] at (%s,%s) {carte à l'échelle $\dfrac{1}{25\,000}$};" % (f(x0), f(y0 - .15)))
    return figure(s)


FIGURES["ex2918_enonce"] = carte(False)
FIGURES["ex2918_corrige"] = carte(True)


# ================================================================== RECETTE (2921)
def recette():
    W, H = 5.6, 3.3
    s = [r"\fill[otSky!60] (0,0) rectangle (%s,%s);" % (f(W), f(H)),
         r"\draw[otNavy,line width=.9pt,rounded corners=4pt] (0,0) rectangle (%s,%s);" % (f(W), f(H)),
         r"\node[txt,text=otNavy,anchor=north] at (%s,%s) {Pâte à crêpes};" % (f(W / 2), f(H - .22)),
         r"\node[petit,anchor=north] at (%s,%s) {pour 4 personnes};" % (f(W / 2), f(H - .62)),
         r"\draw[otNavy!40,line width=.5pt] (.4,%s) -- (%s,%s);" % (f(H - 1.07), f(W - .4), f(H - 1.07))]
    lignes = [(r"$250$ g", "de farine"), (r"$3$", "œufs"), (r"$50$ cl", "de lait"), (r"$40$ g", "de beurre fondu")]
    for i, (q, nom) in enumerate(lignes):
        y = H - 1.42 - i * .47
        s += [r"\fill[otNavy] (.6,%s) circle (1.6pt);" % f(y),
              r"\node[anchor=east] at (2.0,%s) {%s};" % (f(y), q),
              r"\node[anchor=west] at (2.15,%s) {%s};" % (f(y), nom)]
    return figure(s)


FIGURES["ex2921_recette"] = recette()


# ================================================================== LOTS DE CAHIERS (2934)
def cahier(x, y, col):
    """Petit cahier vu de face : couverture colorée, étiquette blanche avec deux lignes."""
    w, h = .4, .54
    return [r"\fill[%s!30,rounded corners=1.2pt] (%s,%s) rectangle (%s,%s);" % (col, f(x), f(y), f(x + w), f(y + h)),
            r"\draw[%s,line width=.6pt,rounded corners=1.2pt] (%s,%s) rectangle (%s,%s);" % (col, f(x), f(y), f(x + w), f(y + h)),
            r"\fill[white] (%s,%s) rectangle (%s,%s);" % (f(x + .08), f(y + .26), f(x + .32), f(y + .43)),
            r"\draw[%s!70,line width=.35pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
            % (col, f(x + .12), f(y + .38), f(x + .28), f(y + .38), f(x + .12), f(y + .31), f(x + .28), f(y + .31))]


def lots():
    s = []
    for j, (nom, nb, prix, col) in enumerate((("Magasin A", 3, r"$4{,}50$ €", "otNavy"),
                                              ("Magasin B", 5, r"$7$ €", "otOrange!80!black"))):
        x = j * 3.55
        s += [r"\draw[%s,line width=.9pt,rounded corners=4pt] (%s,0) rectangle (%s,2.55);" % (col, f(x), f(x + 3.2)),
              r"\node[txt,text=%s,anchor=north] at (%s,2.38) {%s};" % (col, f(x + 1.6), nom)]
        x0 = x + 1.6 - (nb * .52 - .12) / 2
        for i in range(nb):
            s += cahier(x0 + i * .52, 1.08, "otNavy" if j == 0 else "otOrange!85!black")
        s += [r"\node[petit,anchor=north] at (%s,.98) {lot de %d cahiers};" % (f(x + 1.6), nb),
              r"\node[anchor=north,font=\large] at (%s,.58) {%s};" % (f(x + 1.6), prix)]
    return figure(s)


FIGURES["ex2934_enonce"] = lots()


def barres_h(lignes, k=.11, Lnom=1.9):
    """Barres horizontales : (nom, valeur, texte, couleur_remplissage, couleur_trait, couleur_texte)."""
    s = []
    h, pas = .5, .78
    for i, (nom, v, t, cf, cd, ct) in enumerate(lignes):
        y = -i * pas
        s += [r"\fill[%s] (0,%s) rectangle (%s,%s);" % (cf, f(y), f(v * k), f(y + h)),
              r"\draw[%s,line width=.7pt] (0,%s) rectangle (%s,%s);" % (cd, f(y), f(v * k), f(y + h)),
              r"\node[txt,text=%s,anchor=east] at (-.15,%s) {%s};" % (ct, f(y + h / 2), nom),
              r"\node[text=%s,anchor=west] at (%s,%s) {%s};" % (ct, f(v * k + .12), f(y + h / 2), t)]
    n = len(lignes)
    s.append(r"\draw[otMuted,line width=.6pt] (0,%s) -- (0,%s);" % (f(-(n - 1) * pas - .15), f(h + .15)))
    return figure(s)


FIGURES["ex2934_corrige"] = barres_h([
    ("magasin A", 45, r"$45$ €", "otNavy!25", "otNavy", "otNavy"),
    ("magasin B", 42, r"$42$ €", "otOrange!30", "otOrange!85!black", "otOrange!80!black"),
    ("A avec remise", 40.5, r"$40{,}50$ €", "otGreen!40", "otGreenDark", "otGreenDark")], k=.075)


# ================================================================== ENQUÊTE (2931)
def proportions():
    L, h, pas = 5.2, .55, .8
    s = []
    for i, (nom, p, t) in enumerate((("5e A", 75, r"$75\,\%$"), ("5e B", 70, r"$70\,\%$"))):
        y = -i * (pas + .35)
        s += [r"\fill[otGreen!40] (0,%s) rectangle (%s,%s);" % (f(y), f(L * p / 100), f(y + h)),
              r"\fill[otSky] (%s,%s) rectangle (%s,%s);" % (f(L * p / 100), f(y), f(L), f(y + h)),
              r"\draw[otNavy,line width=.7pt] (0,%s) rectangle (%s,%s);" % (f(y), f(L), f(y + h)),
              r"\draw[otGreenDark,line width=1.1pt] (%s,%s) -- (%s,%s);" % (f(L * p / 100), f(y), f(L * p / 100), f(y + h)),
              r"\node[txt,text=otNavy,anchor=east] at (-.15,%s) {%s};" % (f(y + h / 2), nom),
              r"\node[text=otGreenDark,anchor=west] at (%s,%s) {%s};" % (f(L + .15), f(y + h / 2), t)]
    yb = -(pas + .35) - .2
    s += [r"\draw[otMuted,line width=.5pt] (0,%s) -- (%s,%s);" % (f(yb), f(L), f(yb))]
    for q in (0, 50, 100):
        s += [r"\draw[otMuted,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(L * q / 100), f(yb), f(L * q / 100), f(yb - .1)),
              r"\node[petit,anchor=north] at (%s,%s) {%s};" % (f(L * q / 100), f(yb - .14), "$%d\\,\\%%$" % q)]
    return figure(s)


FIGURES["ex2931_corrige"] = proportions()
