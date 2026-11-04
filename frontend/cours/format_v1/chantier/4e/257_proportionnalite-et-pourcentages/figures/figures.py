# -*- coding: utf-8 -*-
"""Figures de la notion « Proportionnalité et pourcentages » (4e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = contre-exemple ou élément d'alerte.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  valeur/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=2pt,minimum height=.8cm,minimum width=1.75cm,text=otInk},
  valeurV/.style={valeur,draw=otGreenDark,fill=otGreen!15,text=otGreenDark},
  fl/.style={otNavy,line width=.9pt,-{Stealth[length=2.3mm]}},
  flV/.style={otGreenDark,line width=.9pt,-{Stealth[length=2.3mm]}},
  flO/.style={otOrange!85!black,line width=.9pt,-{Stealth[length=2.3mm]}},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
  accolV/.style={decorate,decoration={brace,amplitude=5pt},otGreenDark,line width=.8pt},
  coteV/.style={otGreenDark,line width=.6pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}},
}
"""


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def axe(opts, corps):
    return "\n".join([r"\begin{tikzpicture}", r"\begin{axis}[otWeb, %s]" % opts] + corps
                     + [r"\end{axis}", r"\end{tikzpicture}"])


LAB = (r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-15pt,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},"
       r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}")

FIGURES = {}


# ================================================================== TABLEAU DE PROPORTIONNALITÉ
def tableau(entetes, l1, l2, coef, vert=False, w0=2.6, w=1.25, vertes=()):
    h = .75
    s = []
    for r, (ent, ligne) in enumerate(((entetes[0], l1), (entetes[1], l2))):
        y = -r * h
        s.append(r"\fill[otSky] (0,%.2f) rectangle (%.2f,%.2f);" % (y, w0, y - h))
        s.append(r"\node[txt,text=otNavy] at (%.2f,%.2f) {%s};" % (w0 / 2, y - h / 2, ent))
        for k, v in enumerate(ligne):
            c = "otGreenDark" if (r, k) in vertes else "otInk"
            s.append(r"\node[text=%s] at (%.2f,%.2f) {$%s$};" % (c, w0 + (k + .5) * w, y - h / 2, v))
    n = len(l1)
    W = w0 + n * w
    s += [r"\draw[otNavy,line width=.7pt] (0,0) rectangle (%.2f,%.2f);" % (W, -2 * h),
          r"\draw[otNavy,line width=.7pt] (0,%.2f) -- (%.2f,%.2f);" % (-h, W, -h)]
    for k in range(n):
        s.append(r"\draw[otNavy,line width=.7pt] (%.2f,0) -- (%.2f,%.2f);" % (w0 + k * w, w0 + k * w, -2 * h))
    st = "flV" if vert else "fl"
    c = "otGreenDark" if vert else "otNavy"
    s += [r"\draw[%s] (%.2f,%.2f) to[out=0,in=0,looseness=1.6] (%.2f,%.2f);" % (st, W + .1, -h / 2, W + .1, -1.5 * h),
          r"\node[text=%s,anchor=west] at (%.2f,%.2f) {$\times %s$};" % (c, W + .62, -h, coef)]
    return figure(s)


FIGURES["cours_tableau"] = tableau(("masse (kg)", "prix (€)"), ("2", "5", "8"), ("7", "17{,}5", "28"), "3{,}5")
FIGURES["ex2621_corrige"] = tableau(("masse (kg)", "prix (€)"), ("2", "5", "8", "12", "14"),
                                    ("7", "17{,}5", "28", "42", "49"), "3{,}5", vert=True, w0=2.2, w=1.0,
                                    vertes={(1, 3), (0, 4)})
FIGURES["ex2633_corrige"] = tableau(("prix HT (€)", "prix TTC (€)"), ("100", "150", "80"),
                                    ("120", "180", "96"), "1{,}2", vert=True, w0=2.7,
                                    vertes={(1, 1), (0, 2)})


# ================================================================== PRODUIT EN CROIX
def croix(ent, a, b, c, d, vert=False):
    """Tableau 2 x 2 : a | b sur la 1re ligne, c | d sur la 2de ; on cherche d.
    Les cases en croix sont colorées : (a, d) en orange pâle, (b, c) en bleu."""
    w0, w, h = 2.6, 1.6, .8
    s = []
    cells = {(0, 0): ("otOrange!22", a), (0, 1): ("otGreen!22", b), (1, 0): ("otGreen!22", c), (1, 1): ("otOrange!22", d)}
    for r in range(2):
        y = -r * h
        s.append(r"\fill[otSky] (0,%.2f) rectangle (%.2f,%.2f);" % (y, w0, y - h))
        s.append(r"\node[txt,text=otNavy] at (%.2f,%.2f) {%s};" % (w0 / 2, y - h / 2, ent[r]))
        for k in range(2):
            f, v = cells[(r, k)]
            x0 = w0 + k * w
            s.append(r"\fill[%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (f, x0, y, x0 + w, y - h))
            col = "otGreenDark" if (vert and (r, k) == (1, 1)) else "otInk"
            s.append(r"\node[text=%s] at (%.2f,%.2f) {$%s$};" % (col, x0 + w / 2, y - h / 2, v))
    W = w0 + 2 * w
    s += [r"\draw[otNavy,line width=.7pt] (0,0) rectangle (%.2f,%.2f);" % (W, -2 * h),
          r"\draw[otNavy,line width=.7pt] (0,%.2f) -- (%.2f,%.2f);" % (-h, W, -h),
          r"\draw[otNavy,line width=.7pt] (%.2f,0) -- (%.2f,%.2f);" % (w0, w0, -2 * h),
          r"\draw[otNavy,line width=.7pt] (%.2f,0) -- (%.2f,%.2f);" % (w0 + w, w0 + w, -2 * h)]
    return s, W, h


def fig_croix(vert):
    s, W, h = croix(("cahiers", "prix (€)"), "6", "9", r"9{,}60", r"14{,}40" if vert else "?", vert)
    if vert:
        s += [r"\node[text=otGreenDark,anchor=north west] at (0,%.2f) {$6 \times ? = 9 \times 9{,}60$, donc $? = \dfrac{9 \times 9{,}60}{6} = 14{,}40$};" % (-2 * h - .3)]
    else:
        s += [r"\node[anchor=north west] at (0,%.2f) {produits en croix égaux : $6 \times ? = 9 \times 9{,}60$};" % (-2 * h - .3)]
    return figure(s)


FIGURES["cours_croix"] = fig_croix(False)
FIGURES["ex2622_corrige"] = fig_croix(True)


# ================================================================== BARRE DE POURCENTAGE
def barre_pourcentage():
    L, H, n = 8.0, .8, 10
    u = L / n
    s = [r"\fill[otGreen!35] (0,0) rectangle (%.2f,%.2f);" % (1.5 * u, H),
         r"\fill[otSky] (%.2f,0) rectangle (%.2f,%.2f);" % (1.5 * u, L, H),
         r"\draw[otNavy,line width=.8pt] (0,0) rectangle (%.2f,%.2f);" % (L, H)]
    for k in range(1, n):
        s.append(r"\draw[otNavy!60,line width=.5pt] (%.2f,0) -- (%.2f,%.2f);" % (k * u, k * u, H))
    s.append(r"\draw[otGreenDark,line width=1pt,dash pattern=on 2pt off 1.5pt] (%.2f,0) -- (%.2f,%.2f);" % (1.5 * u, 1.5 * u, H))
    s += [r"\draw[accol] (0,%.2f) -- (%.2f,%.2f);" % (H + .12, L, H + .12),
          r"\node[anchor=south] at (%.2f,%.2f) {$100\ \%%$ : $240$ €};" % (L / 2, H + .45),
          r"\draw[accol] (%.2f,-.12) -- (%.2f,-.12);" % (u, 0),
          r"\node[petit,anchor=north] at (%.2f,-.45) {$10\ \%%$ : $24$ €};" % (u / 2),
          r"\draw[accolV] (%.2f,-.9) -- (0,-.9);" % (1.5 * u),
          r"\node[text=otGreenDark,anchor=north west] at (0,-1.22) {$15\ \%$ de $240$ € $= 0{,}15 \times 240 = 36$ €};"]
    return figure(s)


FIGURES["cours_pourcentage"] = barre_pourcentage()


# ================================================================== CHAÎNES DE COEFFICIENTS
def chaine(vals, coefs, vert_fin=False, y=0, dx=3.2, t="a"):
    s = []
    for i, v in enumerate(vals):
        st = "valeurV" if (vert_fin and i == len(vals) - 1) else "valeur"
        s.append(r"\node[%s] (v%d%s) at (%.2f,%.2f) {%s};" % (st, i, t, i * dx, y, v))
    for i, c in enumerate(coefs):
        col, st = (("otGreenDark", "flV") if c.startswith("!") else ("otNavy", "fl"))
        c = c.lstrip("!")
        s.append(r"\draw[%s] (v%d%s.north) to[bend left=38] node[midway,above=2pt,text=%s] {%s} (v%d%s.north);"
                 % (st, i, t, col, c, i + 1, t))
    return s


FIGURES["cours_coef"] = figure(
    chaine(("$60$ €", "$42$ €"), ("baisse de $30\\ \\%$ : $\\times 0{,}7$",), dx=4.6)
    + chaine(("$250$ €", "$270$ €"), ("hausse de $8\\ \\%$ : $\\times 1{,}08$",), dx=4.6, y=-2.7, t="b"))
FIGURES["ex2625_corrige"] = figure(
    chaine(("$60$ €", "$42$ €"), ("!$-30\\ \\%$ : $\\times 0{,}7$",), vert_fin=True, dx=4.2)
    + chaine(("$100$ €", "$110$ €", "$99$ €"), ("$+10\\ \\%$ : $\\times 1{,}1$", "!$-10\\ \\%$ : $\\times 0{,}9$"),
             vert_fin=True, dx=3.4, y=-2.3, t="b"))


# ================================================================== GRAPHIQUES
def graphe_cours():
    return axe(
        r"width=5.4cm, height=4.8cm, xmin=0, xmax=8.6, ymin=0, ymax=13.4, xtick={1,...,8}, ytick={2,4,...,12},"
        r"xlabel={}, ylabel={}",
        [r"\addplot[courbe,domain=0:8] {1.5*x};",
         r"\addplot[otOrange!85!black,line width=1.35pt,domain=0:8] {.75*x+4};",
         r"\fill[otNavy] (axis cs:0,0) circle (2.4pt);",
         r"\fill[otOrange!85!black] (axis cs:0,4) circle (2.4pt);",
         r"\node[text=otNavy,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:8.2,12) {proportionnel};",
         r"\node[text=otOrange!80!black,anchor=west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:8.2,9.2) {non\\proportionnel};"])


FIGURES["cours_graphique"] = graphe_cours()


def graphe_vitesse():
    return axe(
        r"width=6.2cm, height=4.6cm, xmin=0, xmax=3.4, ymin=0, ymax=300, xtick={1,2,3}, ytick={90,180,270},"
        r"xlabel={durée (h)}, ylabel={distance (km)}," + LAB,
        [r"\addplot[courbe,domain=0:3.2] {90*x};",
         r"\guides{1}{90}", r"\guides{2}{180}",
         r"\pnt{1}{90}", r"\pnt{2}{180}", r"\pnt{3}{270}", r"\fill[otNavy] (axis cs:0,0) circle (2.1pt);",
         r"\node[text=otGreenDark,anchor=north west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:2.12,82) {$d = 90 \times t$\\vitesse : $90$ km/h};"])


FIGURES["cours_vitesse"] = graphe_vitesse()


def graphe_2624(corr):
    c = [r"\addplot[%s,domain=0:8] {2.4*x};" % ("otGreenDark,line width=1.35pt" if corr else "courbe"),
         r"\addplot[otOrange!85!black,line width=1.35pt,domain=0:8] {1.5*x+6};",
         r"\addplot[otMuted,line width=1.35pt,domain=0:7.5] {0.35*x^2};",
         r"\fill[%s] (axis cs:5,12) circle (2.6pt);" % ("otGreenDark" if corr else "otNavy"),
         r"\node[text=%s,anchor=west] at (axis cs:5.25,11.75) {$A$};" % ("otGreenDark" if corr else "otNavy"),
         r"\node[text=%s,anchor=north west] at (axis cs:2.7,5.4) {$\mathcal{G}_1$};" % ("otGreenDark" if corr else "otNavy"),
         r"\node[text=otOrange!80!black,anchor=south east] at (axis cs:1.6,9.4) {$\mathcal{G}_2$};",
         r"\node[text=otMuted,anchor=north west] at (axis cs:5.6,8.6) {$\mathcal{G}_3$};"]
    if corr:
        c += [r"\guides{4}{9.6}", r"\guides{7.5}{18}",
              r"\fill[otGreenDark] (axis cs:4,9.6) circle (2.4pt);",
              r"\fill[otGreenDark] (axis cs:7.5,18) circle (2.4pt);",
              r"\node[text=otGreenDark,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:0.12,9.75) {$9{,}6$ €};",
              r"\node[text=otGreenDark,anchor=south west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:7.62,0.9) {$7{,}5$ kg};"]
    return axe(
        r"width=6.8cm, height=6.6cm, xmin=0, xmax=8.6, ymin=0, ymax=21, xtick={1,...,8}, ytick={2,4,...,20},"
        r"xlabel={masse (kg)}, ylabel={prix (€)}," + LAB,
        c)


FIGURES["ex2624_enonce"] = graphe_2624(False)
FIGURES["ex2624_corrige"] = graphe_2624(True)


def graphe_2627():
    pts = [(0.5, 45, "$45$ km"), (5 / 3, 150, "$150$ km"), (7 / 3, 210, "$210$ km"), (3, 270, "$270$ km")]
    c = [r"\addplot[courbe,domain=0:3.2] {90*x};", r"\fill[otNavy] (axis cs:0,0) circle (2.1pt);"]
    for x, y, t in pts:
        c += [r"\draw[guide] (axis cs:%.4f,0) -- (axis cs:%.4f,%d) -- (axis cs:0,%d);" % (x, x, y, y),
              r"\fill[otGreenDark] (axis cs:%.4f,%d) circle (2.4pt);" % (x, y),
              r"\node[text=otGreenDark,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:%.4f,%d) {%s};" % (x + .07, y - 6, t)]
    return axe(
        r"width=7cm, height=5.2cm, xmin=0, xmax=3.5, ymin=0, ymax=310, xtick={0.5,1,1.5,2,2.5,3}, ytick={50,100,...,300},"
        r"xlabel={durée (h)}, ylabel={distance (km)}," + LAB,
        c)


FIGURES["ex2627_corrige"] = graphe_2627()


def graphe_2628():
    return axe(
        r"width=7cm, height=5.2cm, xmin=0, xmax=64, ymin=0, ymax=118, xtick={10,20,...,60}, ytick={20,40,...,100},"
        r"xlabel={volume (L)}, ylabel={prix (€)}," + LAB,
        [r"\addplot[courbe,domain=0:60] {1.85*x};", r"\fill[otNavy] (axis cs:0,0) circle (2.1pt);",
         r"\guides{40}{74}", r"\guides{55}{101.75}", r"\guides{27.03}{50}",
         r"\fill[otGreenDark] (axis cs:40,74) circle (2.4pt);",
         r"\fill[otGreenDark] (axis cs:55,101.75) circle (2.4pt);",
         r"\fill[otGreenDark] (axis cs:27.03,50) circle (2.4pt);",
         r"\node[text=otGreenDark,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:41,71) {$(40\,;74)$};",
         r"\node[text=otGreenDark,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:56,98.5) {$(55\,;101{,}75)$};",
         r"\node[text=otGreenDark,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:28,47) {$50$ € : $\approx 27$ L};"])


FIGURES["ex2628_corrige"] = graphe_2628()


def graphe_2634():
    return axe(
        r"width=6.2cm, height=5.4cm, xmin=0, xmax=5.6, ymin=0, ymax=27, xtick={1,...,5}, ytick={4,8,...,24},"
        r"xlabel={côté (cm)}, ylabel={}," + LAB,
        [r"\addplot[courbe,domain=0:5.2] {4*x};",
         r"\addplot[otOrange!85!black,line width=1.35pt,domain=0:5.2] {x^2};",
         r"\pnt{1}{4}", r"\pnt{2}{8}",
         r"\fill[otOrange!85!black] (axis cs:1,1) circle (2.1pt);",
         r"\fill[otOrange!85!black] (axis cs:2,4) circle (2.1pt);",
         r"\node[text=otNavy,anchor=north west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:0.25,25.5) {périmètre (cm) : droite};",
         r"\node[text=otOrange!80!black,anchor=north west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:3.05,6.4) {aire (cm²) :\\pas une droite};"])


FIGURES["ex2634_corrige"] = graphe_2634()


def graphe_2638(corr):
    c = [r"\addplot[courbe,domain=0:3.2] {18*x};",
         r"\addplot[otOrange!85!black,line width=1.35pt] coordinates {(0,0) (1,24) (1.5,24) (3,54)};",
         r"\node[text=otNavy,anchor=south east] at (axis cs:2.45,46) {Léa};",
         r"\node[text=otOrange!80!black,anchor=north west] at (axis cs:2.15,30) {Tom};"]
    if corr:
        c += [r"\guides{1}{24}", r"\draw[guide] (axis cs:1,18) -- (axis cs:0,18);",
              r"\draw[guide] (axis cs:1.3333,0) -- (axis cs:1.3333,24);",
              r"\fill[otGreenDark] (axis cs:1,18) circle (2.4pt);",
              r"\fill[otGreenDark] (axis cs:1,24) circle (2.4pt);",
              r"\fill[otGreenDark] (axis cs:1.3333,24) circle (2.4pt);",
              r"\fill[otGreenDark] (axis cs:3,54) circle (2.4pt);",
              r"\node[text=otGreenDark,anchor=south,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:1.3333,26.5) {1 h 20};",
              r"\node[text=otGreenDark,anchor=south east,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:2.95,55.5) {$(3\,;54)$};"]
    return axe(
        r"width=7cm, height=5.4cm, xmin=0, xmax=3.4, ymin=0, ymax=60, xtick={0.5,1,1.5,2,2.5,3}, ytick={6,12,...,54},"
        r"xlabel={durée (h)}, ylabel={distance (km)}," + LAB,
        c)


FIGURES["ex2638_enonce"] = graphe_2638(False)
FIGURES["ex2638_corrige"] = graphe_2638(True)


# ================================================================== DIAGRAMMES EN BARRES
def barres(labels, vals, ymax, ytick, ylabel, fmt, couleur="fill=otGreen!70,draw=otGreenDark"):
    coords = " ".join("(%s,%s)" % (l, v) for l, v in zip(labels, vals))
    return "\n".join([
        r"\begin{tikzpicture}",
        r"\begin{axis}[otBarres, width=%s, height=4.4cm, symbolic x coords={%s}, xtick=data, ymax=%s, ytick={%s},"
        % ("%.1fcm" % (1.7 * len(labels) + .6), ",".join(labels), ymax, ytick)
        + r" ylabel={%s}, nodes near coords={%s}, bar width=24pt, enlarge x limits=%s,"
        % (ylabel, fmt, "0.45" if len(labels) == 2 else "0.18")
        + r" every node near coord/.append style={text=otGreenDark,font=\otMedium\fontsize{8.5}{10}\selectfont}]",
        r"\addplot[%s] coordinates {%s};" % (couleur, coords),
        r"\end{axis}", r"\end{tikzpicture}"])


FIGURES["ex2636_corrige"] = barres(["Collège A", "Collège B"], [85, 82], 100, "0,20,40,60,80,100",
                                   r"taux de réussite (\%)", r"$\pgfmathprintnumber{\pgfplotspointmeta}\ \%$")
FIGURES["ex2641_corrige"] = barres(["1 jour", "2 jours", "3 jours", "6 jours"], [45, 42.5, 40, 35], 50,
                                   "0,10,20,30,40,50", r"prix d'une journée (€)",
                                   r"$\pgfmathprintnumber[fixed,precision=2]{\pgfplotspointmeta}$ €")


# ================================================================== PLAN DE L'APPARTEMENT (1/100)
def plan(corr):
    k = .55  # 1 cm du plan -> 0,62 cm de figure
    A, B, H1, H2, h1 = 6.2 * k, 4.2 * k, 4.5 * k, 3.5 * k, 6.2 * k
    W, Ht = A + B, h1
    s = [r"\fill[otSky] (0,0) rectangle (%.3f,%.3f);" % (A, H1),
         r"\fill[otMuted!12] (0,%.3f) rectangle (%.3f,%.3f);" % (H1, A, Ht),
         r"\fill[otOrange!14] (%.3f,0) rectangle (%.3f,%.3f);" % (A, W, H2),
         r"\fill[otGreen!14] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (A, H2, W, Ht),
         r"\draw[otNavy,line width=1pt] (0,0) rectangle (%.3f,%.3f);" % (W, Ht),
         r"\draw[otNavy,line width=1pt] (%.3f,0) -- (%.3f,%.3f);" % (A, A, Ht),
         r"\draw[otNavy,line width=1pt] (0,%.3f) -- (%.3f,%.3f);" % (H1, A, H1),
         r"\draw[otNavy,line width=1pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (A, H2, W, H2),
         r"\node[txt,text=otNavy] at (%.3f,%.3f) {séjour};" % (A / 2, H1 / 2),
         r"\node[txt,text=otMuted] at (%.3f,%.3f) {entrée};" % (A / 2, (H1 + Ht) / 2),
         r"\node[txt,text=otOrange!80!black] at (%.3f,%.3f) {chambre};" % (A + B / 2, H2 / 2),
         r"\node[txt,text=otGreenDark] at (%.3f,%.3f) {cuisine};" % (A + B / 2, (H2 + Ht) / 2)]
    if corr:
        vals = ("6{,}2 m", "4{,}2 m", "4{,}5 m", "1{,}7 m", "3{,}5 m", "2{,}7 m")
        st, tc = "coteV", "otGreenDark"
    else:
        vals = ("6{,}2 cm", "4{,}2 cm", "4{,}5 cm", "1{,}7 cm", "3{,}5 cm", "2{,}7 cm")
        st, tc = "cote", "otInk"
    d = .42
    cotes = [((0, -d), (A, -d), vals[0], "h"), ((A, -d), (W, -d), vals[1], "h"),
             ((-d, 0), (-d, H1), vals[2], "g"), ((-d, H1), (-d, Ht), vals[3], "g"),
             ((W + d, 0), (W + d, H2), vals[4], "d"), ((W + d, H2), (W + d, Ht), vals[5], "d")]
    for (x1, y1), (x2, y2), v, pos in cotes:
        s.append(r"\draw[%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (st, x1, y1, x2, y2))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if pos == "h":
            s.append(r"\node[text=%s,anchor=north] at (%.3f,%.3f) {$%s$};" % (tc, mx, my - .1, v.replace(" ", r"\ \text{") + "}"))
        elif pos == "g":
            s.append(r"\node[text=%s,anchor=east] at (%.3f,%.3f) {$%s$};" % (tc, mx - .1, my, v.replace(" ", r"\ \text{") + "}"))
        else:
            s.append(r"\node[text=%s,anchor=west] at (%.3f,%.3f) {$%s$};" % (tc, mx + .1, my, v.replace(" ", r"\ \text{") + "}"))
    for x in (0, A, W):
        s.append(r"\draw[otMuted!70,line width=.4pt] (%.3f,-.08) -- (%.3f,%.3f);" % (x, x, -d - .08))
    for y in (0, H1, Ht):
        s.append(r"\draw[otMuted!70,line width=.4pt] (-.08,%.3f) -- (%.3f,%.3f);" % (y, -d - .08, y))
    for y in (0, H2, Ht):
        s.append(r"\draw[otMuted!70,line width=.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (W + .08, y, W + d + .08, y))
    return figure(s)


FIGURES["ex2629_enonce"] = plan(False)
FIGURES["ex2629_corrige"] = plan(True)


# ================================================================== CARTE DE RANDONNÉE (1/25 000)
def _sentier():
    """Ligne brisée de longueur 18 (unités « cm sur la carte ») entre P et R distants de 11."""
    forme = [(0, 0), (1.4, .9), (2.9, -.5), (4.4, .8), (5.9, -.6), (7.4, .7), (8.9, -.5), (10.1, .4), (11, 0)]

    def longueur(a):
        pts = [(x, a * y) for x, y in forme]
        return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    lo, hi = 0.1, 10.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if longueur(m) < 18 else (lo, m)
    a = (lo + hi) / 2
    th = math.radians(24)
    return [(x * math.cos(th) - a * y * math.sin(th), x * math.sin(th) + a * y * math.cos(th)) for x, y in forme]


def carte(corr):
    u = .5
    pts = [(x * u, y * u) for x, y in _sentier()]
    P, R = pts[0], pts[-1]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs) - .6, max(xs) + .6, min(ys) - .9, max(ys) + .8
    s = [r"\fill[otGreen!8] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, y0, x1, y1),
         r"\draw[otMuted,line width=.6pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, y0, x1, y1),
         r"\draw[%s,line width=.9pt,dash pattern=on 3pt off 2pt] (%.3f,%.3f) -- (%.3f,%.3f);"
         % ("otGreenDark" if corr else "otMuted", P[0], P[1], R[0], R[1]),
         r"\draw[otOrange!85!black,line width=1.5pt,line join=round] plot[smooth,tension=.55] coordinates {" + " ".join("(%.3f,%.3f)" % p for p in pts) + "};",
         r"\fill[otNavy] (%.3f,%.3f) circle (2.6pt);" % P,
         r"\fill[otNavy] (%.3f,%.3f) circle (2.6pt);" % R,
         r"\node[txt,text=otNavy,anchor=north] at (%.3f,%.3f) {parking};" % (P[0] + .1, P[1] - .2),
         r"\node[txt,text=otNavy,anchor=south] at (%.3f,%.3f) {refuge};" % (R[0] - .2, R[1] + .2)]
    # légende (sous la carte) : sentier et vol d'oiseau
    ly = y0 - 1.45
    s += [r"\draw[otOrange!85!black,line width=1.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, ly, x0 + .7, ly),
          r"\draw[%s,line width=.9pt,dash pattern=on 3pt off 2pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % ("otGreenDark" if corr else "otMuted", x0, ly - .55, x0 + .7, ly - .55)]
    if corr:
        s += [r"\node[text=otGreenDark,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (%.3f,%.3f) {sentier : $18$ cm, soit $4{,}5$ km};" % (x0 + .9, ly),
              r"\node[text=otGreenDark,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (%.3f,%.3f) {vol d'oiseau : $11$ cm, soit $2{,}75$ km};" % (x0 + .9, ly - .55)]
    else:
        s += [r"\node[txt,anchor=west] at (%.3f,%.3f) {sentier};" % (x0 + .9, ly),
              r"\node[txt,anchor=west] at (%.3f,%.3f) {à vol d'oiseau};" % (x0 + .9, ly - .55)]
    # échelle graphique : 4 cm de carte = 1 km
    ex, ey = x0, y0 - .55
    s += [r"\fill[otInk] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (ex, ey, ex + 2 * u, ey + .12),
          r"\draw[otInk,line width=.5pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (ex, ey, ex + 4 * u, ey + .12),
          r"\node[petit,anchor=north] at (%.3f,%.3f) {0};" % (ex, ey - .12),
          r"\node[petit,anchor=north] at (%.3f,%.3f) {1 km};" % (ex + 4 * u, ey - .12),
          r"\node[txt,anchor=west] at (%.3f,%.3f) {Échelle $\dfrac{1}{25\,000}$};" % (ex + 4 * u + .9, ey + .02)]
    return figure(s)


FIGURES["ex2637_enonce"] = carte(False)
FIGURES["ex2637_corrige"] = carte(True)


# ================================================================== PHOTOS (2640)
def photos(corr):
    k = .092
    s = []
    # photo 10 x 15
    s += [r"\fill[otSky] (0,0) rectangle (%.3f,%.3f);" % (10 * k, 15 * k),
          r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%.3f,%.3f);" % (10 * k, 15 * k),
          r"\node[petit,anchor=north] at (%.3f,-.15) {$10$ cm};" % (5 * k),
          r"\node[petit,anchor=east] at (-.12,%.3f) {$15$ cm};" % (7.5 * k),
          r"\node[txt,text=otNavy,anchor=south] at (%.3f,%.3f) {photo};" % (5 * k, 15 * k + .15)]
    # agrandissement 25 x 37,5
    x = 10 * k + 1.5
    col = "otGreenDark" if corr else "otNavy"
    s += [r"\fill[otGreen!12] (%.3f,0) rectangle (%.3f,%.3f);" % (x, x + 25 * k, 37.5 * k),
          r"\draw[%s,line width=.9pt] (%.3f,0) rectangle (%.3f,%.3f);" % (col, x, x + 25 * k, 37.5 * k),
          r"\node[petit,anchor=north] at (%.3f,-.15) {$25$ cm};" % (x + 12.5 * k),
          r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,%.3f) {agrandissement};" % (x + 12.5 * k, 37.5 * k + .15)]
    if corr:
        s.append(r"\node[text=otGreenDark,anchor=east] at (%.3f,%.3f) {$37{,}5$ cm};" % (x - .12, 18.75 * k))
    else:
        s.append(r"\node[text=otInk,anchor=east] at (%.3f,%.3f) {?};" % (x - .12, 18.75 * k))
    if corr:
        # impression sur un papier 13 x 18 : photo de 13 x 19,5 qui dépasse
        x2 = x + 25 * k + 1.6
        s += [r"\fill[otGreen!12] (%.3f,0) rectangle (%.3f,%.3f);" % (x2, x2 + 13 * k, 18 * k),
              r"\fill[otOrange!35] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x2, 18 * k, x2 + 13 * k, 19.5 * k),
              r"\draw[otNavy,line width=.9pt] (%.3f,0) rectangle (%.3f,%.3f);" % (x2, x2 + 13 * k, 18 * k),
              r"\draw[otOrange!85!black,line width=.8pt,dash pattern=on 2.5pt off 1.5pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
              % (x2, 18 * k, x2, 19.5 * k, x2 + 13 * k, 19.5 * k, x2 + 13 * k, 18 * k),
              r"\node[petit,anchor=north] at (%.3f,-.15) {$13$ cm};" % (x2 + 6.5 * k),
              r"\node[petit,anchor=west] at (%.3f,%.3f) {$18$ cm};" % (x2 + 13 * k + .12, 9 * k),
              r"\node[text=otOrange!80!black,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (%.3f,%.3f) {$1{,}5$ cm};" % (x2 + 13 * k + .12, 18.75 * k + .12),
              r"\node[txt,text=otNavy,anchor=south,align=center] at (%.3f,%.3f) {papier\\$13 \times 18$};" % (x2 + 6.5 * k, 19.5 * k + .45)]
    return figure(s)


FIGURES["ex2640_enonce"] = photos(False)
FIGURES["ex2640_corrige"] = photos(True)


# ================================================================== MÉLANGE (2639)
def melange():
    k = 2.4  # 1 L -> 2,4 cm
    w = 1.3
    cols = [("boisson A", 1, .3, "$0{,}3$ L"), ("jus B", .5, .4, "$0{,}4$ L"), ("mélange", 1.5, .7, "$0{,}7$ L")]
    s = []
    for i, (nom, v, j, t) in enumerate(cols):
        x = i * 2.4
        s += [r"\fill[otGreen!45] (%.3f,0) rectangle (%.3f,%.3f);" % (x, x + w, j * k),
              r"\fill[otSky] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x, j * k, x + w, v * k),
              r"\draw[otNavy,line width=.8pt] (%.3f,0) rectangle (%.3f,%.3f);" % (x, x + w, v * k),
              r"\draw[otNavy!60,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, j * k, x + w, j * k),
              r"\node[text=otGreenDark,font=\otMedium\fontsize{8.5}{10}\selectfont] at (%.3f,%.3f) {%s};" % (x + w / 2, j * k / 2, t),
              r"\node[txt,text=otNavy,anchor=north] at (%.3f,-.15) {%s};" % (x + w / 2, nom),
              r"\node[petit,anchor=south] at (%.3f,%.3f) {$%s$ L};" % (x + w / 2, v * k + .12, ("%g" % v).replace(".", "{,}"))]
    s += [r"\node[text=otNavy] at (%.3f,%.3f) {$+$};" % (1.85, .6),
          r"\node[text=otNavy] at (%.3f,%.3f) {$=$};" % (4.25, .6),
          r"\node[text=otGreenDark,anchor=west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (%.3f,%.3f) {$\dfrac{0{,}7}{1{,}5} \approx 46{,}7\ \%%$\\de jus de fruits};" % (2 * 2.4 + w + .2, 1.6),
          r"\fill[otGreen!45] (0,%.3f) rectangle (.3,%.3f);" % (-1.05, -.8),
          r"\node[petit,anchor=west] at (.4,%.3f) {jus de fruits};" % (-.925),
          r"\fill[otSky] (3,%.3f) rectangle (3.3,%.3f);" % (-1.05, -.8),
          r"\draw[otNavy!60,line width=.4pt] (3,%.3f) rectangle (3.3,%.3f);" % (-1.05, -.8),
          r"\node[petit,anchor=west] at (3.4,%.3f) {reste de la boisson};" % (-.925)]
    return figure(s)


FIGURES["ex2639_corrige"] = melange()


# ================================================================== ÉCHELLE (cours)
def echelle_cours():
    u = 1.0
    s = []
    for i in range(4):
        f = "otInk" if i % 2 == 0 else "white"
        s.append(r"\fill[%s] (%.2f,0) rectangle (%.2f,.16);" % (f, i * u, (i + 1) * u))
    s += [r"\draw[otInk,line width=.5pt] (0,0) rectangle (%.2f,.16);" % (4 * u),
          r"\node[petit,anchor=north] at (0,-.12) {0};",
          r"\node[petit,anchor=north] at (%.2f,-.12) {1 km};" % (4 * u),
          r"\draw[cote] (0,.5) -- (%.2f,.5);" % (4 * u),
          r"\node[anchor=south] at (%.2f,.62) {$4$ cm sur la carte};" % (2 * u),
          r"\node[anchor=north,align=center,text=otGreenDark] at (%.2f,-.75) {$4 \times 25\,000 = 100\,000$ cm\\soit $1$ km dans la réalité};" % (2 * u)]
    return figure(s)


FIGURES["cours_echelle"] = echelle_cours()
