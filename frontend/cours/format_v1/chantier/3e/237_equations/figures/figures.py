# -*- coding: utf-8 -*-
"""Figures de la notion « Équations » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = repères d'aide.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=1pt},
  masse/.style={draw=otOrange!80!black,fill=otOrange!25,line width=.8pt},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
}
\newcommand{\coteV}[4][0.35]{\draw[cote] ($(#2)!#1cm!90:(#3)$) -- ($(#3)!#1cm!-90:(#2)$) node[midway,coteTexte,text=otGreenDark]{#4};
  \draw[otMuted!70,line width=.4pt] (#2) -- ($(#2)!#1cm+2pt!90:(#3)$) (#3) -- ($(#3)!#1cm+2pt!-90:(#2)$);}
"""

V = r"\textcolor{otGreenDark}{%s}"


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


# ================================================================== BALANCE
def plateau(cx, y0, n, m, vert=False):
    """Objets posés sur un plateau centré en cx (haut du plateau en y0) : n boîtes x et une masse m."""
    s = []
    lb, gap, lm = .56, .1, .78
    larg = n * lb + max(n - 1, 0) * gap + (gap + lm if (m and n) else (lm if m else 0))
    x = cx - larg / 2
    bord = "otGreenDark" if vert else "otNavy"
    fond = "otGreen!18" if vert else "otSky"
    for _ in range(n):
        s.append(r"\draw[boite,draw=%s,fill=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
                 % (bord, fond, x, y0, x + lb, y0 + lb))
        s.append(r"\node[text=%s] at (%.3f,%.3f) {$x$};" % ("otGreenDark" if vert else "otInk", x + lb / 2, y0 + lb / 2))
        x += lb + gap
    if m:
        h = .5
        s.append(r"\draw[masse] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;"
                 % (x, y0, x + lm, y0, x + lm - .1, y0 + h, x + .1, y0 + h))
        s.append(r"\node[text=otInk] at (%.3f,%.3f) {$%s$};" % (x + lm / 2, y0 + h / 2, m))
    return s


def balance(g, d, oy=0, eg=None, ed=None, vert=False):
    """g, d : (n boîtes, masse) ; eg, ed : expressions écrites sous les plateaux."""
    E = 2.05
    s = [
        # socle et colonne
        r"\fill[otMuted!30] (-1,%.2f) -- (1,%.2f) -- (.6,%.2f) -- (-.6,%.2f) -- cycle;" % (oy, oy, oy + .25, oy + .25),
        r"\draw[otMuted,line width=.8pt] (-1,%.2f) -- (1,%.2f) -- (.6,%.2f) -- (-.6,%.2f) -- cycle;" % (oy, oy, oy + .25, oy + .25),
        r"\draw[otMuted,line width=2.2pt] (0,%.2f) -- (0,%.2f);" % (oy + .25, oy + 1.1),
        r"\fill[otMuted] (0,%.2f) circle (2.4pt);" % (oy + 1.1),
        # fléau
        r"\draw[otNavy,line width=1.6pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (-E, oy + 1.1, E, oy + 1.1),
    ]
    for cx in (-E, E):
        s += [r"\draw[otNavy,line width=1.6pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (cx, oy + 1.1, cx, oy + 1.45),
              r"\draw[otNavy,line width=1.8pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (cx - 1.75, oy + 1.5, cx + 1.75, oy + 1.5)]
    s += plateau(-E, oy + 1.6, *g, vert=vert)
    s += plateau(E, oy + 1.6, *d, vert=vert)
    c = "otGreenDark" if vert else "otInk"
    if eg:
        s.append(r"\node[text=%s] at (%.2f,%.2f) {$%s$};" % (c, -E, oy + .6, eg))
    if ed:
        s.append(r"\node[text=%s] at (%.2f,%.2f) {$%s$};" % (c, E, oy + .6, ed))
    return s


def fleche(t):
    return [r"\draw[otOrange!90!black,line width=1pt,-{Stealth[length=2.4mm]}] (%s,2.9) -- (%s,2.4);" % (x, x) for x in (-3.15, 3.15)] \
        + [r"\node[txt] at (0,2.65) {%s};" % t]


FIGURES = {}

# cours et fiche : 3x + 2 = x + 8, puis 2x = 6
FIGURES["cours_balance"] = figure(
    balance((3, "2"), (1, "8"), oy=3.1, eg="3x + 2", ed="x + 8")
    + fleche("on enlève $x$ et $2$ sur chaque plateau")
    + balance((2, None), (0, "6"), oy=0, eg="2x", ed="6", vert=True)
    + [r"\node[txt,text=otGreenDark,anchor=west] at (-3.8,-.45) {donc $x = 6 \div 2 = 3$};"])

# exercice 2201 : 4x + 3 = x + 12
FIGURES["ex2201_enonce"] = figure(balance((4, "3"), (1, "12")))
FIGURES["ex2201_corrige"] = figure(
    balance((4, "3"), (1, "12"), oy=3.1, eg="4x + 3", ed="x + 12")
    + fleche("on enlève $x$ et $3$ sur chaque plateau")
    + balance((3, None), (0, "9"), oy=0, eg="3x", ed="9", vert=True)
    + [r"\node[txt,text=otGreenDark,anchor=west] at (-3.8,-.45) {donc $x = 9 \div 3 = 3$};"])


# ================================================================== COURBES
def axe(opts, corps):
    return "\n".join([r"\begin{tikzpicture}", r"\begin{axis}[otWeb, %s]" % opts] + corps
                     + [r"\end{axis}", r"\end{tikzpicture}"])


def produit_cours():
    return axe(
        r"width=7.4cm, height=6.4cm, xmin=-4.4, xmax=3.6, ymin=-7, ymax=8.4,"
        r"xtick={-4,-2,-1,1,3}, ytick={-4,-2,2,4,6}",
        [r"\addplot[courbe,domain=-4.2:3.2] {(x-2)*(x+3)};",
         r"\fill[otGreenDark] (axis cs:-3,0) circle (2.6pt);",
         r"\fill[otGreenDark] (axis cs:2,0) circle (2.6pt);",
         r"\node[text=otGreenDark,anchor=north east,inner sep=1pt] at (axis cs:-3.1,-.35) {$-3$};",
         r"\node[text=otGreenDark,anchor=north west,inner sep=1pt] at (axis cs:2.1,-.35) {$2$};",
])


FIGURES["cours_produit"] = produit_cours()


def tarifs_cours():
    return axe(
        r"width=6.6cm, height=5.6cm, xmin=0, xmax=10.6, ymin=0, ymax=56,"
        r"xtick={1,2,3,4,5,7,8,9,10}, ytick={10,20,40,50}, xlabel={séances}, ylabel={prix en €},"
        r"every axis x label/.style={at={(axis cs:10.6,0)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},"
        r"every axis y label/.style={at={(axis cs:0,56)},anchor=south west,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}",
        [r"\addplot[courbe,domain=0:10] {5*x};",
         r"\addplot[courbe2,domain=0:10] {3*x+12};",
         r"\draw[guide] (axis cs:6,0) -- (axis cs:6,30) -- (axis cs:0,30);",
         r"\fill[otGreenDark] (axis cs:6,30) circle (2.6pt);",
         r"\node[text=otGreenDark,anchor=north,inner sep=1pt,yshift=-2.5pt] at (axis cs:6,0) {$6$};",
         r"\node[text=otGreenDark,anchor=east,inner sep=1pt,xshift=-2pt] at (axis cs:0,30) {$30$};",
         r"\node[text=otNavy,anchor=west] at (axis cs:10.1,50) {$y = 5x$};",
         r"\node[text=otGreenDark,anchor=west] at (axis cs:10.1,42) {$y = 3x + 12$};"])


FIGURES["cours_tarifs"] = tarifs_cours()


def graphe_2214(corr):
    c = [r"\addplot[courbe,domain=-2.2:4.2] {(x+1)*(x-3)};",
         r"\draw[seuil] (axis cs:-2.6,-3) -- (axis cs:4.6,-3);",
         r"\node[text=otOrange!80!black,anchor=west] at (axis cs:4.65,-3) {$y = -3$};",
         r"\node[text=otNavy,anchor=west] at (axis cs:3.3,6.3) {$\mathcal{C}_f$};"]
    if corr:
        c += [r"\fill[otGreenDark] (axis cs:-1,0) circle (2.6pt);",
              r"\fill[otGreenDark] (axis cs:3,0) circle (2.6pt);",
              r"\fill[otGreenDark] (axis cs:0,-3) circle (2.6pt);",
              r"\fill[otGreenDark] (axis cs:2,-3) circle (2.6pt);"]
    return axe(
        r"width=6.6cm, height=6.2cm, xmin=-2.6, xmax=4.6, ymin=-4.8, ymax=7,"
        r"xtick={-2,-1,1,2,3,4}, xticklabels={}, ytick={-4,-2,2,4,6}",
        c)


FIGURES["ex2214_enonce"] = graphe_2214(False)
FIGURES["ex2214_corrige"] = graphe_2214(True)

XLAB = {
    "ex2214_enonce": [(-2, "c", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "c", "4")],
    "ex2214_corrige": [(-2, "c", "-2"), (-1, "g", "-1"), (1, "c", "1"), (2, "c", "2"), (3, "d", "3"), (4, "c", "4")],
}


def graphe_2220(corr):
    c = [r"\addplot[courbe,domain=0:14] {9*x};",
         r"\addplot[courbe2,domain=0:14] {40+4*x};",
         r"\node[text=otNavy,anchor=west] at (axis cs:14.2,126) {tarif A};",
         r"\node[text=otGreenDark,anchor=west] at (axis cs:14.2,96) {tarif B};"]
    if corr:
        c += [r"\draw[guide] (axis cs:8,0) -- (axis cs:8,72) -- (axis cs:0,72);",
              r"\fill[otGreenDark] (axis cs:8,72) circle (2.6pt);",
              r"\node[text=otGreenDark,anchor=north,inner sep=1pt,yshift=-2.5pt] at (axis cs:8,0) {$8$};",
              r"\node[text=otGreenDark,anchor=east,inner sep=1pt,xshift=-2pt] at (axis cs:0,72) {$72$};"]
    xt = "{2,4,6,10,12,14}" if corr else "{2,4,6,8,10,12,14}"
    return axe(
        r"width=7.2cm, height=6cm, xmin=0, xmax=15, ymin=0, ymax=136,"
        r"xtick=%s, ytick={20,40,60,80,100,120}, minor xtick={1,3,...,15}, minor ytick={10,30,...,130},"
        r"grid=both, minor grid style={otRule!45,line width=.3pt},"
        r"xlabel={séances}, ylabel={prix en €},"
        r"every axis x label/.style={at={(axis cs:15,0)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},"
        r"every axis y label/.style={at={(axis cs:0,136)},anchor=south west,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}" % xt,
        c)


FIGURES["ex2220_enonce"] = graphe_2220(False)
FIGURES["ex2220_corrige"] = graphe_2220(True)


# ================================================================== SCHÉMAS DE SITUATION
def billets(corr):
    L, H = 8.0, .9
    a = L * 12 / 28
    s = [r"\fill[otSky] (0,0) rectangle (%.2f,%.2f);" % (a, H),
         r"\fill[otOrange!18] (%.2f,0) rectangle (%.2f,%.2f);" % (a, L, H),
         r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%.2f,%.2f);" % (L, H),
         r"\draw[otNavy,line width=.9pt] (%.2f,0) -- (%.2f,%.2f);" % (a, a, H),
         r"\node[txt] at (%.2f,%.2f) {billets jeunes};" % (a / 2, H / 2),
         r"\node[txt] at (%.2f,%.2f) {autres billets};" % ((a + L) / 2, H / 2),
         r"\draw[accol] (0,%.2f) -- (%.2f,%.2f);" % (H + .12, a, H + .12),
         r"\draw[accol] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, H + .12, L, H + .12),
         r"\draw[accol] (%.2f,-.12) -- (0,-.12);" % L]
    if corr:
        s += [r"\node[text=otGreenDark,anchor=south] at (%.2f,%.2f) {$12$ billets à $6$ € : $72$ €};" % (a / 2, H + .38),
              r"\node[text=otGreenDark,anchor=south] at (%.2f,%.2f) {$16$ billets à $10$ € : $160$ €};" % ((a + L) / 2, H + .38),
              r"\node[text=otGreenDark,anchor=north] at (%.2f,-.4) {$28$ billets, $72 + 160 = 232$ €};" % (L / 2)]
    else:
        s += [r"\node[anchor=south] at (%.2f,%.2f) {$x$ billets à $6$ €};" % (a / 2, H + .38),
              r"\node[anchor=south] at (%.2f,%.2f) {$28 - x$ billets à $10$ €};" % ((a + L) / 2, H + .38),
              r"\node[anchor=north] at (%.2f,-.4) {$28$ billets en tout, $232$ €};" % (L / 2)]
    return figure(s)


FIGURES["ex2215_enonce"] = billets(False)
FIGURES["ex2215_corrige"] = billets(True)


def rectangle(corr):
    L, l = 5.4, 3.3
    s = [r"\fill[otSky] (0,0) rectangle (%.2f,%.2f);" % (L, l),
         r"\draw[geoTrait] (0,0) rectangle (%.2f,%.2f);" % (L, l),
         r"\coordinate (A) at (0,0); \coordinate (B) at (%.2f,0); \coordinate (C) at (%.2f,%.2f); \coordinate (D) at (0,%.2f);" % (L, L, l, l),
         r"\angledroit{B}{A}{D} \angledroit{A}{B}{C} \angledroit{B}{C}{D} \angledroit{C}{D}{A}"]
    s += [r"\cote[.45]{B}{A}{$x + 7$}", r"\cote[.45]{A}{D}{$x$}"]
    if corr:
        s += [r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {largeur : $x = 11$ cm};" % (L / 2, l * .64),
              r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {longueur : $x + 7 = 18$ cm};" % (L / 2, l * .36)]
    else:
        s += [r"\node[txt] at (%.2f,%.2f) {périmètre : $58$ cm};" % (L / 2, l / 2)]
    return figure(s)


FIGURES["ex2216_enonce"] = rectangle(False)
FIGURES["ex2216_corrige"] = rectangle(True)


def aires(corr):
    u = .42
    c, a, b = 6 * u, 4 * u, 9 * u
    ox = c + 1.6
    s = [r"\fill[otSky] (0,0) rectangle (%.2f,%.2f);" % (c, c),
         r"\draw[geoTrait] (0,0) rectangle (%.2f,%.2f);" % (c, c),
         r"\fill[otOrange!18] (%.2f,0) rectangle (%.2f,%.2f);" % (ox, ox + b, a),
         r"\draw[geoTrait] (%.2f,0) rectangle (%.2f,%.2f);" % (ox, ox + b, a),
         r"\coordinate (A) at (0,0); \coordinate (B) at (%.2f,0); \coordinate (C) at (%.2f,%.2f); \coordinate (D) at (0,%.2f);" % (c, c, c, c),
         r"\coordinate (E) at (%.2f,0); \coordinate (F) at (%.2f,0); \coordinate (G) at (%.2f,%.2f); \coordinate (H) at (%.2f,%.2f);" % (ox, ox + b, ox + b, a, ox, a),
         r"\angledroit{B}{A}{D} \angledroit{F}{E}{H}"]
    s += [r"\cote[.45]{B}{A}{$x + 2$}", r"\cote[.45]{A}{D}{$x + 2$}",
          r"\cote[.45]{F}{E}{$x + 5$}", r"\cote[.45]{E}{H}{$x$}"]
    if corr:
        s += [r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {côté $6$ cm};" % (c / 2, c * .62),
              r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {aire $36$ cm²};" % (c / 2, c * .38),
              r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {$4$ cm sur $9$ cm};" % (ox + b / 2, a * .66),
              r"\node[txt,text=otGreenDark] at (%.2f,%.2f) {aire $36$ cm²};" % (ox + b / 2, a * .34)]
    else:
        s += [r"\node[txt] at (%.2f,%.2f) {carré};" % (c / 2, c / 2),
              r"\node[txt] at (%.2f,%.2f) {rectangle};" % (ox + b / 2, a / 2)]
    return figure(s)


FIGURES["ex2219_enonce"] = aires(False)
FIGURES["ex2219_corrige"] = aires(True)


def ages(corr):
    xs = (0, 3.8, 6.3)
    s = [r"\draw[otMuted,line width=.8pt,-{Stealth[length=2.4mm]}] (-.6,0) -- (7.2,0);",
         r"\node[petit,anchor=west] at (7.3,0) {temps};"]
    quand = ("il y a $7$ ans", "aujourd'hui", "dans $5$ ans")
    if corr:
        age = (V % "$12$ ans", V % "$19$ ans", V % "$24$ ans")
    else:
        age = ("$x - 7$", "$x$", "$x + 5$")
    for x, q, g in zip(xs, quand, age):
        s += [r"\draw[otNavy,line width=1pt] (%.2f,-.12) -- (%.2f,.12);" % (x, x),
              r"\fill[otNavy] (%.2f,0) circle (2.2pt);" % x,
              r"\node[petit,anchor=south] at (%.2f,.3) {%s};" % (x, q),
              r"\node[anchor=north] at (%.2f,-.3) {%s};" % (x, g)]
    s += [r"\draw[accol] (%.2f,.85) -- (%.2f,.85) node[midway,above=5pt,petit] {$7$ ans};" % (xs[0], xs[1]),
          r"\draw[accol] (%.2f,.85) -- (%.2f,.85) node[midway,above=5pt,petit] {$5$ ans};" % (xs[1], xs[2])]
    if corr:
        s.append(r"\node[txt,text=otGreenDark] at (3.15,-1.45) {$24 = 2 \times 12$ : l'âge dans $5$ ans est le double};")
    else:
        s.append(r"\node[txt] at (3.15,-1.45) {âge dans $5$ ans $=$ double de l'âge d'il y a $7$ ans};")
    return figure(s)


FIGURES["ex2221_enonce"] = ages(False)
FIGURES["ex2221_corrige"] = ages(True)
