# -*- coding: utf-8 -*-
"""Figures de la notion « Manipuler les nombres réels » (Seconde), style des livres.

Compilées par outils/figures_livre.py. Droites graduées : axe gris à flèche,
graduations en Montserrat, intervalles en vert foncé avec crochets.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  bande/.style={line width=3.2pt,line cap=butt},
  crochet/.style={line width=1.3pt,line join=miter},
}
"""


def f(v):
    """Nombre TikZ (point décimal)."""
    return ("%.4f" % v).rstrip("0").rstrip(".")


def axe(x0, x1, y=0.0, ticks=(), labels=None, depart=None):
    """Axe horizontal de x0 à x1 (flèche), graduations, étiquettes sous l'axe."""
    d = x0 if depart is None else depart
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(d), f(y), f(x1), f(y))]
    for t in ticks:
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(t), f(y - .07), f(t), f(y + .07)))
    for t, txt in (labels or {}).items():
        s.append(r"\node[gradTexte] at (%s,%s) {%s};" % (f(t), f(y - .3), txt))
    return "\n".join(s)


def crochet(x, y, sens, couleur="otGreenDark", h=.2, l=.11):
    """Crochet en x : sens=+1 ouvert vers la droite « [ », -1 « ] »."""
    return r"\draw[crochet,%s] ([xshift=%scm]%s,%s) -- (%s,%s) -- (%s,%s) -- ([xshift=%scm]%s,%s);" % (
        couleur, f(sens * l), f(x), f(y + h), f(x), f(y + h), f(x), f(y - h), f(sens * l), f(x), f(y - h))


def intervalle(a, b, y, ga, gb, couleur="otGreenDark", opac="otGreen!85"):
    """Bande [a;b] sur la ligne y ; ga/gb : 'f' fermé, 'o' ouvert, None (infini)."""
    s = [r"\draw[bande,%s] (%s,%s) -- (%s,%s);" % (opac, f(a), f(y), f(b), f(y))]
    if ga:
        s.append(crochet(a, y, +1 if ga == "f" else -1, couleur))
    if gb:
        s.append(crochet(b, y, -1 if gb == "f" else +1, couleur))
    return "\n".join(s)


def num(v):
    """Graduation au format français."""
    t = ("%g" % v).replace(".", "{,}")
    return "$%s$" % t.replace("-", "-")


FIGURES = {}

# ------------------------------------------------------------------ cours 1
# Ensembles emboîtés N ⊂ Z ⊂ D ⊂ Q ⊂ R
_ens = [
    (r"\mathbb{R}", r"$\sqrt{2}$\quad $\pi$\quad $-\sqrt{5}$"),
    (r"\mathbb{Q}", r"$\dfrac{1}{3}$\quad $-\dfrac{5}{7}$"),
    (r"\mathbb{D}", r"$0{,}25$\quad $-3{,}4$"),
    (r"\mathbb{Z}", r"$-5$\quad $-1$"),
    (r"\mathbb{N}", r"$0$\quad $3$\quad $17$"),
]
_teintes = ["otSky!55", "otSky!85", "otSky", "otNavy!12", "otNavy!18"]
_s = [r"\begin{tikzpicture}"]
L, R, B, T = 0.0, 8.6, 0.0, 6.6
for k, ((sym, ex), teinte) in enumerate(zip(_ens, _teintes)):
    l, r, b, t = L + .5 * k, R - .5 * k, B + .32 * k, T - 1.02 * k
    _s.append(r"\filldraw[fill=%s,draw=otNavy,line width=.8pt,rounded corners=6pt] (%s,%s) rectangle (%s,%s);"
              % (teinte, f(l), f(b), f(r), f(t)))
    yl = t - .5
    _s.append(r"\node[anchor=west,text=otNavy,font=\large] at (%s,%s) {$%s$};" % (f(l + .2), f(yl), sym))
    _s.append(r"\node[anchor=west,text=otInk] at (%s,%s) {%s};" % (f(l + 1.05), f(yl), ex))
_s.append(r"\end{tikzpicture}")
FIGURES["ensembles"] = "\n".join(_s)

# ------------------------------------------------------------------ cours 2
# Quelques réels placés sur la droite graduée
_s = [r"\begin{tikzpicture}[x=1.1cm]"]
_s.append(axe(-3.5, 4.6, ticks=range(-3, 5), labels={k: num(k) for k in range(-3, 5)}))
for x, txt in [(-2, r"$-2$"), (-0.75, r"$-0{,}75$"), (1 / 3, r"$\dfrac{1}{3}$"),
               (2 ** .5, r"$\sqrt{2}$"), (3.14159265, r"$\pi$")]:
    _s.append(r"\fill[otNavy] (%s,0) circle (2.3pt);" % f(x))
    _s.append(r"\node[anchor=south,text=otNavy] at (%s,.17) {%s};" % (f(x), txt))
_s.append(r"\end{tikzpicture}")
FIGURES["droite_reels"] = "\n".join(_s)

# ------------------------------------------------------------------ cours 3
# Quatre intervalles et leurs inégalités
_rows = [
    (r"$[2\,;5]$", 2, 5, "f", "f", r"$2\le x\le 5$"),
    (r"$]2\,;5[$", 2, 5, "o", "o", r"$2<x<5$"),
    (r"$[2\,;+\infty[$", 2, 7.45, "f", None, r"$x\ge 2$"),
    (r"$]{-\infty}\,;1]$", -1.45, 1, None, "f", r"$x\le 1$"),
]
_s = [r"\begin{tikzpicture}[x=.61cm]"]
for i, (nom, a, b, ga, gb, ineg) in enumerate(_rows):
    y = -1.15 * i
    _s.append(axe(-1.5, 7.6, y=y, ticks=range(-1, 8), labels={k: num(k) for k in range(-1, 8)}))
    _s.append(intervalle(a, b, y, ga, gb))
    _s.append(r"\node[anchor=east,text=otNavy] at (-1.8,%s) {%s};" % (f(y), nom))
    _s.append(r"\node[anchor=west,text=otInk] at (7.9,%s) {%s};" % (f(y), ineg))
_s.append(r"\end{tikzpicture}")
FIGURES["intervalles"] = "\n".join(_s)

# ------------------------------------------------------------------ cours 4
# Valeur absolue et distance
_s = [r"\begin{tikzpicture}[x=.8cm]"]
_s.append(axe(-4.5, 6.6, ticks=range(-4, 7), labels={k: num(k) for k in range(-4, 7)}))
_s.append(r"\draw[guide] (-3,.12) -- (-3,1.55);")
_s.append(r"\draw[guide] (5,.12) -- (5,1.55);")
_s.append(r"\draw[guide] (0,.12) -- (0,.75);")
_s.append(r"\draw[cote,otOrange] (-3,.75) -- (0,.75);")
_s.append(r"\node[anchor=south,text=otOrange!80!black] at (-1.5,.8) {$|{-3}|=3$};")
_s.append(r"\draw[cote,otGreenDark] (-3,1.55) -- (5,1.55);")
_s.append(r"\node[anchor=south,text=otGreenDark] at (1,1.6) {distance entre $-3$ et $5$ : $|5-(-3)|=8$};")
for x in (-3, 0, 5):
    _s.append(r"\fill[otNavy] (%s,0) circle (2.3pt);" % x)
_s.append(r"\end{tikzpicture}")
FIGURES["distance"] = "\n".join(_s)

# ------------------------------------------------------------------ cours 5
# Intervalle centré |x - 3| <= 2
_s = [r"\begin{tikzpicture}[x=1.1cm]"]
_s.append(axe(-.5, 6.6, ticks=range(0, 7), labels={k: num(k) for k in range(0, 7)}))
_s.append(intervalle(1, 5, 0, "f", "f"))
_s.append(r"\fill[otNavy] (3,0) circle (2.4pt);")
_s.append(r"\draw[guide] (3,.12) -- (3,.75);")
_s.append(r"\draw[cote,otNavy] (1,.75) -- (3,.75);")
_s.append(r"\draw[cote,otNavy] (3,.75) -- (5,.75);")
_s.append(r"\node[anchor=south,text=otNavy] at (2,.8) {$r=2$};")
_s.append(r"\node[anchor=south,text=otNavy] at (4,.8) {$r=2$};")
_s.append(r"\node[anchor=north,text=otNavy] at (3,-.72) {centre $a=3$};")
_s.append(r"\node[anchor=south,text=otGreenDark] at (3,1.45) {$|x-3|\le 2 \iff x\in[1\,;5]$};")
_s.append(r"\end{tikzpicture}")
FIGURES["intervalle_centre"] = "\n".join(_s)

# ------------------------------------------------------------------ cours 6
# Encadrements successifs de racine de 2 (zooms)
_s = [r"\begin{tikzpicture}"]
W = 6.0
niveaux = [
    (1.0, 2.0, 0.1, r"$1$", r"$2$", r"amplitude $1$", 1.4, 1.5),
    (1.4, 1.5, 0.01, r"$1{,}4$", r"$1{,}5$", r"amplitude $0{,}1$", 1.41, 1.42),
    (1.41, 1.42, 0.001, r"$1{,}41$", r"$1{,}42$", r"amplitude $0{,}01$", None, None),
]
r2 = 2 ** .5
for i, (a, b, pas, ta, tb, amp, za, zb) in enumerate(niveaux):
    y = -1.75 * i
    X = lambda v, a=a, b=b: W * (v - a) / (b - a)
    _s.append(r"\draw[otMuted,line width=.6pt] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
    for k in range(11):
        h = .12 if k in (0, 10) else .07
        _s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(W * k / 10), f(y - h), f(W * k / 10), f(y + h)))
    _s.append(r"\node[gradTexte] at (0,%s) {%s};" % (f(y - .3), ta))
    _s.append(r"\node[gradTexte] at (%s,%s) {%s};" % (f(W), f(y - .3), tb))
    _s.append(r"\node[anchor=west,text=otMuted] at (%s,%s) {%s};"
              % (f(W + .35), f(y), amp))
    if za is not None:
        _s.append(r"\draw[bande,otOrange] (%s,%s) -- (%s,%s);" % (f(X(za)), f(y), f(X(zb)), f(y)))
        yn = -1.75 * (i + 1)
        _s.append(r"\draw[otOrange,line width=.5pt,dash pattern=on 2.5pt off 1.8pt] (%s,%s) -- (0,%s);"
                  % (f(X(za)), f(y - .14), f(yn + .14)))
        _s.append(r"\draw[otOrange,line width=.5pt,dash pattern=on 2.5pt off 1.8pt] (%s,%s) -- (%s,%s);"
                  % (f(X(zb)), f(y - .14), f(W), f(yn + .14)))
    else:
        _s.append(r"\draw[bande,otGreen!85] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
    _s.append(r"\fill[otNavy] (%s,%s) circle (2.3pt);" % (f(X(r2)), f(y)))
    _s.append(r"\node[anchor=south,text=otNavy] at (%s,%s) {$\sqrt{2}$};" % (f(X(r2)), f(y + .15)))
_s.append(r"\node[anchor=north,text=otGreenDark] at (%s,%s) {$1{,}41\le\sqrt{2}\le 1{,}42$ : encadrement à $10^{-2}$ près};"
          % (f(W / 2), f(-1.75 * 2 - .75)))
_s.append(r"\end{tikzpicture}")
FIGURES["encadrement_racine2"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1929 (Q1)
# Intersection [-1;4] ∩ ]2;6[ = ]2;4]
_s = [r"\begin{tikzpicture}[x=.86cm]"]
_s.append(axe(-2.5, 7.6, ticks=range(-2, 8), labels={k: num(k) for k in range(-2, 8)}))
_s.append(intervalle(-1, 4, 1.35, "f", "f", "otNavy", "otNavy!55"))
_s.append(r"\node[anchor=east,text=otNavy] at (-1.25,1.35) {$[-1\,;4]$};")
_s.append(intervalle(2, 6, .75, "o", "o", "otOrange!85!black", "otOrange!80"))
_s.append(r"\node[anchor=west,text=otOrange!80!black] at (6.25,.75) {$]2\,;6[$};")
_s.append(intervalle(2, 4, 0, "o", "f"))
_s.append(r"\node[anchor=north,text=otGreenDark] at (3,-.75) {partie commune : $]2\,;4]$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_intersection"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1930 (Q5)
# Les deux réels à distance 2 de 3
_s = [r"\begin{tikzpicture}[x=1.1cm]"]
_s.append(axe(-.5, 6.6, ticks=range(0, 7), labels={k: num(k) for k in range(0, 7)}))
_s.append(r"\fill[otNavy] (3,0) circle (2.3pt);")
_s.append(r"\draw[guide] (3,.12) -- (3,.75);")
_s.append(r"\draw[guide] (1,.12) -- (1,.75);")
_s.append(r"\draw[guide] (5,.12) -- (5,.75);")
_s.append(r"\draw[cote,otNavy] (1,.75) -- (3,.75);")
_s.append(r"\draw[cote,otNavy] (3,.75) -- (5,.75);")
_s.append(r"\node[anchor=south,text=otNavy] at (2,.8) {$2$};")
_s.append(r"\node[anchor=south,text=otNavy] at (4,.8) {$2$};")
_s.append(r"\fill[otGreenDark] (1,0) circle (2.6pt);")
_s.append(r"\fill[otGreenDark] (5,0) circle (2.6pt);")
_s.append(r"\node[anchor=north,text=otGreenDark] at (3,-.72) {$x=1$ ou $x=5$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_distance_deux"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1931 (Q4)
# |x + 2| < 3  <=>  x ∈ ]-5 ; 1[
_s = [r"\begin{tikzpicture}[x=.95cm]"]
_s.append(axe(-6.5, 2.6, ticks=range(-6, 3), labels={k: num(k) for k in range(-6, 3)}))
_s.append(intervalle(-5, 1, 0, "o", "o"))
_s.append(r"\fill[otNavy] (-2,0) circle (2.4pt);")
_s.append(r"\draw[guide] (-2,.12) -- (-2,.75);")
_s.append(r"\draw[cote,otNavy] (-5,.75) -- (-2,.75);")
_s.append(r"\draw[cote,otNavy] (-2,.75) -- (1,.75);")
_s.append(r"\node[anchor=south,text=otNavy] at (-3.5,.8) {$r=3$};")
_s.append(r"\node[anchor=south,text=otNavy] at (-.5,.8) {$r=3$};")
_s.append(r"\node[anchor=north,text=otNavy] at (-2,-.72) {centre $a=-2$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_centre_ouvert"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1935 (Q2)
# Tolérance : |L - 30| <= 0,3
_s = [r"\begin{tikzpicture}[x=8.5cm]"]
_tk = [29.6 + .1 * k for k in range(9)]
_s.append(axe(29.55, 30.48, ticks=_tk, labels={t: num(round(t, 1)) for t in _tk}))
_s.append(intervalle(29.7, 30.3, 0, "f", "f"))
_s.append(r"\fill[otNavy] (30,0) circle (2.4pt);")
_s.append(r"\draw[guide] (30,.12) -- (30,.75);")
_s.append(r"\draw[cote,otNavy] (29.7,.75) -- (30,.75);")
_s.append(r"\draw[cote,otNavy] (30,.75) -- (30.3,.75);")
_s.append(r"\node[anchor=south,text=otNavy] at (29.85,.8) {$r=0{,}3$};")
_s.append(r"\node[anchor=south,text=otNavy] at (30.15,.8) {$r=0{,}3$};")
_s.append(r"\node[anchor=north,text=otGreenDark] at (30,-.72) {longueurs acceptées (en cm)};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_tolerance"] = "\n".join(_s)


# =================================================================== finition 2026-11-02

# ------------------------------------------------------- exercice 1934 (Q4)
# Balayage de centième en centième : 1,41 accepté, 1,42 refusé
_s = [r"\begin{tikzpicture}[x=100cm]"]
_tk = [1.37 + .01 * k for k in range(8)]
_s.append(axe(1.365, 1.448, ticks=_tk, labels={t: ("$%.2f$" % t).replace(".", "{,}") for t in _tk}))
for a in (1.38, 1.39, 1.40):
    _s.append(r"\draw[otGreenDark,line width=.8pt,-{Stealth[length=1.8mm]}] (%s,.1) to[out=70,in=110] (%s,.1);"
              % (f(a), f(a + .01)))
_s.append(r"\draw[otOrange!85!black,line width=.8pt,dash pattern=on 2.5pt off 1.8pt,-{Stealth[length=1.8mm]}] "
          r"(1.41,.1) to[out=70,in=110] (1.42,.1);")
_s.append(r"\fill[otGreenDark] (1.41,0) circle (2.6pt);")
_s.append(r"\fill[otOrange!85!black] (1.42,0) circle (2.6pt);")
_s.append(r"\node[anchor=south east,text=otGreenDark] at (1.412,.62) {$1{,}41^2=1{,}9881\le 2$};")
_s.append(r"\node[anchor=south west,text=otOrange!80!black] at (1.418,.62) {$1{,}42^2=2{,}0164>2$};")
_s.append(r"\draw[otNavy,line width=.9pt] (1.41421,-.12) -- (1.41421,-.95);")
_s.append(r"\fill[otNavy] (1.41421,0) circle (1.9pt);")
_s.append(r"\node[anchor=north,text=otNavy] at (1.41421,-.95) {$\sqrt{2}\approx 1{,}4142$};")
_s.append(r"\node[anchor=west,text=otMuted,font=\otRegular\fontsize{9}{10}\selectfont] at (1.365,.62) {pas $h=0{,}01$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_balayage"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1926 (Q5)
# ]3,5 ; 4] : seul 4 appartient à l'intervalle
_s = [r"\begin{tikzpicture}[x=6.5cm]"]
_tk = [3.3 + .1 * k for k in range(11)]
_s.append(axe(3.25, 4.38, ticks=_tk, labels={t: num(round(t, 1)) for t in _tk}))
_s.append(intervalle(3.5, 4, 0, "o", "f"))
for x, c, sym in [(3.5, "otOrange!85!black", r"\notin"), (4, "otGreenDark", r"\in"),
                  (4.1, "otOrange!85!black", r"\notin")]:
    _s.append(r"\fill[%s] (%s,0) circle (2.5pt);" % (c, f(x)))
    _s.append(r"\node[anchor=south,text=%s,font=\large] at (%s,.36) {$%s$};" % (c, f(x), sym))
_s.append(r"\node[anchor=north,text=otGreenDark] at (3.75,-.72) {intervalle $]3{,}5\,;4]$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_appartenance"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1928 (Q3 à Q5)
# Trois inégalités représentées sur la droite
_rows = [
    (r"$-2\le x<4$", -2, 4, "f", "o"),
    (r"$x\ge 7$", 7, 9.45, "f", None),
    (r"$x<-3$", -5.45, -3, None, "o"),
]
_s = [r"\begin{tikzpicture}[x=.47cm]"]
for i, (ineg, a, b, ga, gb) in enumerate(_rows):
    y = -1.2 * i
    _s.append(axe(-5.5, 9.6, y=y, ticks=range(-5, 10), labels={k: num(k) for k in range(-5, 10)}))
    _s.append(intervalle(a, b, y, ga, gb))
    _s.append(r"\node[anchor=east,text=otInk] at (-5.8,%s) {%s};" % (f(y), ineg))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_traduire"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1932 (Q5)
# Classement des cinq nombres dans D, Q \ D, R \ Q
_ens = [
    (r"\mathbb{R}", r"$\sqrt{2}$\qquad $\pi$"),
    (r"\mathbb{Q}", r"$\dfrac{1}{3}$"),
    (r"\mathbb{D}", r"$-2{,}5$\qquad $\dfrac{5}{2}$"),
]
_teintes = ["otSky!55", "otSky!85", "otSky"]
_s = [r"\begin{tikzpicture}"]
L, R, B, T = 0.0, 6.0, 0.0, 4.5
for k, ((sym, ex), teinte) in enumerate(zip(_ens, _teintes)):
    l, r, b, t = L + .6 * k, R - .6 * k, B + .45 * k, T - 1.25 * k
    _s.append(r"\filldraw[fill=%s,draw=otNavy,line width=.8pt,rounded corners=6pt] (%s,%s) rectangle (%s,%s);"
              % (teinte, f(l), f(b), f(r), f(t)))
    yl = t - .6
    _s.append(r"\node[anchor=west,text=otNavy,font=\large] at (%s,%s) {$%s$};" % (f(l + .2), f(yl), sym))
    _s.append(r"\node[anchor=west,text=otGreenDark] at (%s,%s) {%s};" % (f(l + 1.2), f(yl), ex))
_s.append(r"\end{tikzpicture}")
FIGURES["ex_classer"] = "\n".join(_s)

# ------------------------------------------------------- exercice 1933 (Q3)
# 5/7 ≈ 0,714 entre 0,7 et 0,8
_s = [r"\begin{tikzpicture}[x=20cm]"]
_tk = [.6 + .01 * k for k in range(31)]
_s.append(axe(.585, .925, ticks=[], labels={}))
for k, t in enumerate(_tk):
    h = .12 if k % 10 == 0 else .06
    _s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(t), f(-h), f(t), f(h)))
for t in (.6, .7, .8, .9):
    _s.append(r"\node[gradTexte] at (%s,-.3) {%s};" % (f(t), num(round(t, 1))))
_s.append(r"\draw[bande,otGreen!85] (.7,0) -- (.8,0);")
_s.append(crochet(.7, 0, +1))
_s.append(crochet(.8, 0, -1))
_s.append(r"\fill[otNavy] (%s,0) circle (2.4pt);" % f(5 / 7))
_s.append(r"\node[anchor=south,text=otNavy] at (%s,.25) {$\dfrac{5}{7}\approx 0{,}714$};" % f(5 / 7))
_s.append(r"\draw[cote,otGreenDark] (.7,-.85) -- (.8,-.85);")
_s.append(r"\node[anchor=north,text=otGreenDark] at (.75,-.9) {amplitude $0{,}1$};")
_s.append(r"\end{tikzpicture}")
FIGURES["ex_cinq_septiemes"] = "\n".join(_s)


# ------------------------------------------------------- nouveau-1 : droite graduée
def droite_points(corrige):
    pts = [("A", -1.5, "otNavy"), ("B", -.25, "otNavy"), ("C", .75, "otNavy"), ("D", 1.75, "otNavy")]
    if corrige:
        pts += [("E", -.75, "otGreenDark"), ("F", 2.5, "otGreenDark"), ("G", 2 ** .5, "otGreenDark")]
    s = [r"\begin{tikzpicture}[x=1.55cm]"]
    if corrige:
        s.append(r"\draw[bande,otGreen!60] (-1,0) -- (1,0);")
    s.append(axe(-2.3, 3.25, ticks=[], labels={}))
    for k in range(-8, 13):
        t = k / 4
        h = .13 if k % 4 == 0 else .07
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(t), f(-h), f(t), f(h)))
    for k in range(-2, 4):
        s.append(r"\node[gradTexte] at (%s,-.3) {%s};" % (f(k), num(k)))
    if corrige:
        s.append(crochet(-1, 0, +1))
        s.append(crochet(1, 0, -1))
        s.append(r"\node[anchor=north,text=otGreenDark] at (0,-.75) {intervalle $[-1\,;1]$};")
    for nom, x, c in pts:
        s.append(r"\fill[%s] (%s,0) circle (2.4pt);" % (c, f(x)))
        s.append(r"\node[anchor=south,text=%s] at (%s,.2) {$%s$};" % (c, f(x), nom))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["n1_droite_enonce"] = droite_points(False)
FIGURES["n1_droite_corrige"] = droite_points(True)

# ------------------------------------------------------- nouveau-2 : terrain rectangulaire
_s = [r"\begin{tikzpicture}"]
_s.append(r"\coordinate (P) at (0,0); \coordinate (Q) at (6.24,0); \coordinate (R) at (6.24,4.19); \coordinate (S) at (0,4.19);")
_s.append(r"\fill[otGreen!14] (P) rectangle (R);")
_s.append(r"\draw[geoTrait] (P) -- (Q) -- (R) -- (S) -- cycle;")
_s.append(r"\draw[otOrange!85!black,line width=.9pt,dash pattern=on 4pt off 2.5pt] (P) -- (R);")
_s.append(r"\angledroit{S}{P}{Q}")
_s.append(r"\node[text=otOrange!80!black,anchor=south east] at (3.0,2.15) {diagonale $d$};")
_s.append(r"\cote[0.45]{Q}{P}{$23{,}4$ m}")
_s.append(r"\draw[otMuted!70,line width=.4pt] (6.3,0) -- (6.78,0) (6.3,4.19) -- (6.78,4.19);")
_s.append(r"\draw[cote] (6.7,0) -- (6.7,4.19);")
_s.append(r"\node[anchor=west,text=otInk] at (6.8,2.1) {$15{,}7$ m};")
_s.append(r"\end{tikzpicture}")
FIGURES["n2_terrain"] = "\n".join(_s)

TOLERE = {"n2_terrain": "longueur 23,4 m posée sur sa flèche de cote, fond blanc (usage normal d une cote)"}
