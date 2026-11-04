# -*- coding: utf-8 -*-
"""Figures de la notion 249 (4e : calculer avec les nombres relatifs), style des livres.

Compilées par outils/figures_livre.py. Droites graduées et déplacements,
thermomètres, schémas d'altitudes, carré magique, pyramides, programme de calcul.
Éléments de réponse en vert foncé (otGreenDark) dans les corrigés.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  axeV/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  gradTexteG/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=east,inner sep=1pt},
  gradTexteD/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=west,inner sep=1pt},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont},
  deplV/.style={otGreenDark,line width=1.1pt,-{Stealth[length=2.4mm]}},
  deplO/.style={otOrange!85!black,line width=1.1pt,-{Stealth[length=2.4mm]}},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=4.6cm,minimum height=.8cm,inner sep=3pt,text=otInk,align=center},
  boiteP/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=3.6cm,minimum height=.62cm,inner sep=3pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  case/.style={draw=otNavy,line width=.8pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  accolV/.style={otGreenDark,line width=.7pt,decorate,decoration={brace,amplitude=4pt}},
}
"""

VERT = "otGreenDark"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def nb(v):
    """Nombre relatif écrit en LaTeX (virgule décimale, signe moins)."""
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


# ===================================================================== outils communs
def droite(a, b, U, y=0.0, x0=0.0, labels=None, pas_label=1):
    """Droite graduée horizontale de a à b (entiers), U cm par unité. Renvoie (code, X)."""
    X = lambda v: x0 + U * (v - a)
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(X(a) - .3), f(y), f(X(b) + .45), f(y))]
    for k in range(a, b + 1):
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(k)), f(y - .08), f(X(k)), f(y + .08)))
        if (labels is None and (k - a) % pas_label == 0) or (labels is not None and k in labels):
            s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X(k)), f(y - .16), nb(k)))
    return "\n".join(s), X


def point(x, y, coul="otNavy", r=2.4):
    return r"\fill[%s] (%s,%s) circle (%spt);" % (coul, f(x), f(y), f(r))


def arc_dessus(x1, x2, y, h, style, texte, coul, dessous=False):
    """Flèche courbe de x1 vers x2 au-dessus (ou au-dessous) de la droite, texte au sommet."""
    sg = -1 if dessous else 1
    xm = (x1 + x2) / 2
    s = [r"\draw[%s] (%s,%s) .. controls (%s,%s) and (%s,%s) .. (%s,%s);"
         % (style, f(x1), f(y + sg * .12), f(x1), f(y + sg * h * 1.33), f(x2), f(y + sg * h * 1.33), f(x2), f(y + sg * .12))]
    anc = "north" if dessous else "south"
    s.append(r"\node[anchor=%s,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (anc, coul, f(xm), f(y + sg * (h + .08)), texte))
    return "\n".join(s)


FIGURES = {}

# ===================================================================== cours 1 : opposés
_c, X = droite(-5, 5, .62)
_s = [r"\begin{tikzpicture}", _c]
for v in (-4, 4):
    _s.append(point(X(v), 0, "otOrange!90!black", 2.8))
for v1, v2 in ((0, -4), (0, 4)):
    _s.append(r"\draw[cote] (%s,.42) -- (%s,.42);" % (f(X(v1)), f(X(v2))))
    _s.append(r"\node[anchor=south,text=otInk,inner sep=1.5pt] at (%s,.5) {$4$};" % f((X(v1) + X(v2)) / 2))
_s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.12) -- (%s,.52);" % (f(X(0)), f(X(0))))
_s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.12) -- (%s,.52);" % (f(X(-4)), f(X(-4))))
_s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.12) -- (%s,.52);" % (f(X(4)), f(X(4))))
_s.append(r"\node[anchor=north,text=otInk,align=center] at (%s,-.62) {$-4$ et $4$ sont opposés :\\même distance à zéro $4$, signes contraires.};" % f(X(0)))
_s.append(r"\end{tikzpicture}")
FIGURES["opposes"] = "\n".join(_s)


# ===================================================================== cours 2 / fiche 1 : déplacements
def deplacements():
    s = [r"\begin{tikzpicture}"]
    c1, X = droite(-5, 5, .6, y=0)
    s.append(c1)
    s.append(arc_dessus(X(-2), X(3), 0, .55, "deplV", r"$+5$", VERT))
    s.append(point(X(-2), 0, "otNavy", 2.6))
    s.append(point(X(3), 0, VERT, 2.8))
    s.append(r"\node[anchor=south west,text=otInk] at (%s,1.0) {$(-2) + 5 = 3$};" % f(X(-5) - .3))
    y2 = -2.0
    c2, _ = droite(-5, 5, .6, y=y2)
    s.append(c2)
    s.append(arc_dessus(X(3), X(-4), y2, .55, "deplO", r"$-7$", "otOrange!85!black"))
    s.append(point(X(3), y2, "otNavy", 2.6))
    s.append(point(X(-4), y2, "otOrange!85!black", 2.8))
    s.append(r"\node[anchor=south west,text=otInk] at (%s,%s) {$3 - 7 = -4$};" % (f(X(-5) - .3), f(y2 + 1.0)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["deplacements"] = deplacements()


# ===================================================================== cours 3 / fiche 2 : priorités
def priorites():
    s = [r"\begin{tikzpicture}"]
    etapes = [r"\textbf{1.} Parenthèses, crochets\\{\otRegular\fontsize{8.5}{10}\selectfont les plus intérieurs d'abord}",
              r"\textbf{2.} Multiplications, divisions\\{\otRegular\fontsize{8.5}{10}\selectfont de gauche à droite}",
              r"\textbf{3.} Additions, soustractions\\{\otRegular\fontsize{8.5}{10}\selectfont de gauche à droite}"]
    dy = 1.3
    for k, e in enumerate(etapes):
        y = -k * dy
        s.append(r"\node[boite,minimum width=0pt,text width=4.1cm] (p%d) at (2.1,%s) {%s};" % (k, f(y), e))
        if k:
            s.append(r"\draw[fleche] (p%d.south) -- (p%d.north);" % (k - 1, k))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["priorites"] = priorites()


# ===================================================================== thermomètres
def thermometre(tmin, tmax, U, marques, pas_label=2, x=0.0, largeur=.42, extra=None):
    """Thermomètre vertical. marques : [(t, texte_gauche, couleur)]. Graduations à droite."""
    Y = lambda t: U * (t - tmin)
    w = largeur
    s = []
    # tube et réservoir
    s.append(r"\draw[otNavy,line width=.9pt,fill=white,rounded corners=%scm] (%s,%s) rectangle (%s,%s);"
             % (f(w / 2), f(x - w / 2), f(Y(tmin) - .35), f(x + w / 2), f(Y(tmax) + .3)))
    s.append(r"\filldraw[draw=otNavy,line width=.9pt,fill=otRed!75] (%s,%s) circle (.36);" % (f(x), f(Y(tmin) - .55)))
    s.append(r"\fill[otRed!75] (%s,%s) rectangle (%s,%s);" % (f(x - .09), f(Y(tmin) - .4), f(x + .09), f(Y(tmin) - .2)))
    for t in range(tmin, tmax + 1):
        lg = .16 if (t - tmin) % pas_label == 0 else .09
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(x + w / 2), f(Y(t)), f(x + w / 2 + lg), f(Y(t))))
        if (t - tmin) % pas_label == 0:
            s.append(r"\node[gradTexteD] at (%s,%s) {$%s$};" % (f(x + w / 2 + .2), f(Y(t)), nb(t)))
    s.append(r"\node[anchor=south,petit,text=otMuted] at (%s,%s) {°C};" % (f(x + w / 2 + .45), f(Y(tmax) + .32)))
    for t, txt, c in marques:
        s.append(r"\draw[%s,line width=1.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 + .05), f(Y(t)), f(x + w / 2 - .05), f(Y(t))))
        s.append(r"\draw[%s,line width=.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 - .12), f(Y(t)), f(x - w / 2 - .42), f(Y(t))))
        s.append(r"\node[anchor=east,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (c, f(x - w / 2 - .45), f(Y(t)), txt))
    if extra:
        s.append(extra(Y))
    return "\n".join(s)


def thermo_cours():
    s = [r"\begin{tikzpicture}"]
    xd = 1.75

    def fleche(Y):
        return (r"\draw[deplV] (%s,%s) -- (%s,%s);" % (f(xd), f(Y(3)), f(xd), f(Y(-5)))
                + "\n" + r"\draw[%s,line width=.5pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
                % (VERT, f(xd - .1), f(Y(3)), f(xd + .1), f(Y(3)), f(xd - .1), f(Y(-5)), f(xd + .1), f(Y(-5)))
                + "\n" + r"\node[anchor=west,text=%s,align=left] at (%s,%s) {$5 \times (-1{,}6)$\\$= -8$ °C};"
                % (VERT, f(xd + .15), f((Y(3) + Y(-5)) / 2)))
    s.append(thermometre(-8, 6, .3, [(3, r"midi : $3$ °C", "otNavy"), (-5, r"17 h : $-5$ °C", VERT)], extra=fleche))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["thermometre_cours"] = thermo_cours()


def thermo_villes(corrige):
    s = [r"\begin{tikzpicture}"]
    marques = [(3, "Brest", "otNavy"), (-4, "Lille", "otNavy"), (-7, "Strasbourg", "otNavy")]
    xd = 1.6

    def ecart(Y):
        if not corrige:
            return ""
        return (r"\draw[accolV] (%s,%s) -- (%s,%s);" % (f(xd), f(Y(3)), f(xd), f(Y(-7)))
                + "\n" + r"\node[anchor=west,text=%s,align=left] at (%s,%s) {écart :\\$3 - (-7) = 10$ °C};"
                % (VERT, f(xd + .25), f((Y(3) + Y(-7)) / 2)))
    s.append(thermometre(-10, 10, .26, marques, extra=ecart))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_thermo_enonce"] = thermo_villes(False)
FIGURES["ex_thermo_corrige"] = thermo_villes(True)


# ===================================================================== cours 5 : altitudes
def altitudes(points, amin, amax, pas, U, ecart=None, coul_ecart=VERT, titre=r"altitude (m)", mer_x=2.3,
              etiquettes_x=2.6, extra=None):
    """Axe vertical des altitudes, mer sous 0. points : [(alt, icône, texte, couleur, x_icone)]."""
    Y = lambda a: U * (a - amin)
    s = []
    s.append(r"\fill[otSky] (.12,%s) rectangle (%s,%s);" % (f(Y(amin)), f(mer_x), f(Y(0))))
    s.append(r"\draw[otNavy!55,line width=.9pt] (.12,%s) -- (%s,%s);" % (f(Y(0)), f(mer_x), f(Y(0))))
    s.append(r"\draw[axeV] (0,%s) -- (0,%s);" % (f(Y(amin) - .1), f(Y(amax) + .45)))
    s.append(r"\node[anchor=south,petit,text=otMuted] at (0,%s) {%s};" % (f(Y(amax) + .5), titre))
    a = amin
    while a <= amax:
        s.append(r"\draw[grad] (-.08,%s) -- (.08,%s);" % (f(Y(a)), f(Y(a))))
        s.append(r"\node[gradTexteG] at (-.14,%s) {$%s$};" % (f(Y(a)), nb(a).replace("000", r"\,000") if abs(a) >= 1000 else nb(a)))
        a += pas
    for alt, icone, txt, c, xi in points:
        s.append(icone(xi, Y(alt), c))
        if txt:
            s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (c, f(etiquettes_x), f(Y(alt)), txt))
    if ecart:
        a1, a2, xe, txt = ecart
        s.append(r"\draw[cote,%s] (%s,%s) -- (%s,%s);" % (coul_ecart, f(xe), f(Y(a1)), f(xe), f(Y(a2))))
        s.append(r"\node[anchor=west,text=%s,align=left] at (%s,%s) {%s};" % (coul_ecart, f(xe + .12), f((Y(a1) + Y(a2)) / 2), txt))
    if extra:
        s.append(extra(Y))
    return "\n".join(s)


def ic_point(x, y, c):
    return point(x, y, c, 2.8)


def ic_oiseau(x, y, c):
    return (r"\draw[%s,line width=1pt,line cap=round] (%s,%s) .. controls (%s,%s) .. (%s,%s) .. controls (%s,%s) .. (%s,%s);"
            % (c, f(x - .28), f(y + .06), f(x - .14), f(y + .16), f(x), f(y - .02), f(x + .14), f(y + .16), f(x + .28), f(y + .06)))


def ic_plongeur(x, y, c):
    return (r"\fill[%s] (%s,%s) circle (2.6pt);" % (c, f(x - .2), f(y))
            + "\n" + r"\draw[%s,line width=1.6pt,line cap=round] (%s,%s) -- (%s,%s);" % (c, f(x - .12), f(y), f(x + .22), f(y))
            + "\n" + r"\draw[%s,line width=1pt,line cap=round] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
            % (c, f(x + .22), f(y), f(x + .36), f(y + .07), f(x + .22), f(y), f(x + .36), f(y - .07)))


def ic_drone(x, y, c):
    return (r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (c, f(x - .16), f(y - .06), f(x + .16), f(y + .06))
            + "\n" + r"\draw[%s,line width=.8pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
            % (c, f(x - .16), f(y + .03), f(x - .3), f(y + .1), f(x + .16), f(y + .03), f(x + .3), f(y + .1))
            + "\n" + r"\draw[%s,line width=1.1pt] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
            % (c, f(x - .42), f(y + .12), f(x - .18), f(y + .12), f(x + .18), f(y + .12), f(x + .42), f(y + .12)))


def ic_sousmarin(x, y, c):
    return (r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) ellipse (.45 and .13);" % (c, c, f(x), f(y))
            + "\n" + r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) rectangle (%s,%s);"
            % (c, c, f(x - .08), f(y + .1), f(x + .1), f(y + .24)))


FIGURES["altitudes_cours"] = "\n".join([r"\begin{tikzpicture}", altitudes(
    [(18, ic_oiseau, r"goéland : $18$ m", "otNavy", 1.2), (-35, ic_plongeur, r"plongeuse : $-35$ m", "otNavy", 1.2)],
    -40, 30, 10, .075, ecart=(18, -35, 5.65, r"écart :\\$53$ m"), coul_ecart="otGreenDark", etiquettes_x=2.45),
    r"\node[anchor=west,petit,text=otNavy!80] at (2.45,%s) {niveau de la mer};" % f(.075 * 40),
    r"\end{tikzpicture}"])


# ===================================================================== 2478 : sous-marin et drone
def sousmarin(corrige):
    pts = [(85, ic_drone, r"drone : $85$ m", "otNavy", 1.2),
           (-240, ic_sousmarin, r"sous-marin : $-240$ m", "otOrange!85!black", 1.2)]
    ecart = None
    if corrige:
        pts += [(45, ic_point, r"après $8$ min : $45$ m", VERT, 1.2),
                (-144, ic_point, r"après $8$ min : $-144$ m", VERT, 1.2)]
        ecart = (45, -144, 6.1, r"écart :\\$189$ m")

    def fl(Y):
        if not corrige:
            return ""
        return (r"\draw[deplV] (1.2,%s) -- (1.2,%s);" % (f(Y(85) - .14), f(Y(45) + .12))
                + "\n" + r"\draw[deplV] (1.2,%s) -- (1.2,%s);" % (f(Y(-240) + .3), f(Y(-144) - .12)))
    s = [r"\begin{tikzpicture}",
         altitudes(pts, -300, 100, 50, .0135, ecart=ecart, extra=fl),
         r"\node[anchor=west,petit,text=otNavy!80] at (2.6,%s) {niveau de la mer};" % f(.0135 * 300),
         r"\end{tikzpicture}"]
    return "\n".join(s)


FIGURES["ex_sousmarin_enonce"] = sousmarin(False)
FIGURES["ex_sousmarin_corrige"] = sousmarin(True)


# ===================================================================== 2465 : tableau de la règle des signes
def tableau_signes():
    W0, w, h = 2.0, .95, .62
    vals_a = [3, 2, 1, 0, -1, -2, -3]
    s = [r"\begin{tikzpicture}"]
    n = len(vals_a)
    s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(W0), f(2 * h)))
    s.append(r"\draw[case] (0,0) rectangle (%s,%s);" % (f(W0 + n * w), f(2 * h)))
    s.append(r"\draw[case] (0,%s) -- (%s,%s);" % (f(h), f(W0 + n * w), f(h)))
    for i in range(n + 1):
        s.append(r"\draw[case] (%s,0) -- (%s,%s);" % (f(W0 + i * w), f(W0 + i * w), f(2 * h)))
    s.append(r"\node[text=otInk] at (%s,%s) {$a$};" % (f(W0 / 2), f(1.5 * h)))
    s.append(r"\node[text=otInk] at (%s,%s) {$a \times (-2)$};" % (f(W0 / 2), f(.5 * h)))
    for i, a in enumerate(vals_a):
        xc = W0 + (i + .5) * w
        s.append(r"\node[text=otInk] at (%s,%s) {$%s$};" % (f(xc), f(1.5 * h), nb(a)))
        c = "otInk" if i == 0 else VERT
        s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(xc), f(.5 * h), nb(-2 * a)))
        if i:
            s.append(arc_dessus(xc - w + .1, xc - .1, 0, .32, "deplV", r"$+2$", VERT, dessous=True))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_signes_corrige"] = tableau_signes()


# ===================================================================== 2468 : deux déplacements depuis -8
def deux_deplacements():
    s = [r"\begin{tikzpicture}"]
    c1, X = droite(-12, 0, .66, y=0)
    s.append(c1)
    s.append(arc_dessus(X(-8), X(-5), 0, .5, "deplV", r"$+3$", VERT))
    s.append(point(X(-8), 0, "otNavy", 2.6))
    s.append(point(X(-5), 0, VERT, 2.8))
    s.append(r"\node[anchor=south west,text=%s] at (%s,.2) {$-8 - (-3) = -8 + 3 = -5$};" % (VERT, f(X(-4.6))))
    c2, _ = droite(-12, 0, .66, y=-1.7)
    s.append(c2)
    s.append(arc_dessus(X(-8), X(-11), -1.7, .5, "deplV", r"$-3$", VERT))
    s.append(point(X(-8), -1.7, "otNavy", 2.6))
    s.append(point(X(-11), -1.7, VERT, 2.8))
    s.append(r"\node[anchor=south west,text=%s] at (%s,-1.5) {$-8 - 3 = -8 + (-3) = -11$};" % (VERT, f(X(-7.6))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_droite_corrige"] = deux_deplacements()


# ===================================================================== 2476 : semaine de températures
def semaine():
    s = [r"\begin{tikzpicture}"]
    c, X = droite(-7, 4, .72, y=0)
    s.append(c)
    jours = [(-6, "lun.", .3), (-5, "dim.", .85), (-4, "jeu.", .3), (-2, "mar.", .3), (-1, "sam.", .85),
             (1, "mer.", .3), (3, "ven.", .3)]
    for v, j, h in jours:
        coul = VERT if v in (-6, 3) else "otNavy"
        s.append(point(X(v), 0, coul, 2.7))
        if h > .5:
            s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.12) -- (%s,%s);" % (f(X(v)), f(X(v)), f(h - .04)))
        s.append(r"\node[anchor=south,petit,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (coul, f(X(v)), f(h - .1 if h < .5 else h), j))
    s.append(r"\draw[cote,%s] (%s,-.78) -- (%s,-.78);" % (VERT, f(X(-6)), f(X(3))))
    s.append(r"\draw[otMuted!70,line width=.4pt] (%s,-.5) -- (%s,-.86) (%s,-.5) -- (%s,-.86);" % (f(X(-6)), f(X(-6)), f(X(3)), f(X(3))))
    s.append(r"\node[anchor=north,text=%s] at (%s,-.86) {amplitude : $3 - (-6) = 9$ °C};" % (VERT, f((X(-6) + X(3)) / 2)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_semaine_corrige"] = semaine()


# ===================================================================== 2474 : température en montagne
def montagne(corrige):
    U = .00135
    Y = lambda a: U * a
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[axeV] (0,0) -- (0,%s);" % f(Y(3500) + .45))
    s.append(r"\node[anchor=south,petit,text=otMuted] at (0,%s) {altitude (m)};" % f(Y(3500) + .5))
    for a in range(0, 3501, 500):
        s.append(r"\draw[grad] (-.08,%s) -- (.08,%s);" % (f(Y(a)), f(Y(a))))
        s.append(r"\node[gradTexteG] at (-.14,%s) {$%s$};" % (f(Y(a)), ("%d" % a).replace("000", r"\,000").replace("500", "500") if a < 1000 else (r"%d\,%03d" % (a // 1000, a % 1000))))
    V, Rf, Sm = (1.0, 400), (4.3, 2900), (5.3, 3200)
    prof = [(.45, 150), V, (2.2, 1300), (3.2, 2250), Rf, Sm, (6.4, 2300), (7.0, 1700)]
    s.append(r"\draw[otNavy,line width=1.3pt,line join=round] %s;" % " -- ".join("(%s,%s)" % (f(px), f(Y(pa))) for px, pa in prof))
    for (px, pa) in (V, Rf, Sm):
        s.append(point(px, Y(pa), "otOrange!90!black", 2.8))
    s.append(r"\draw[guide] (0,%s) -- (%s,%s);" % (f(Y(400)), f(V[0]), f(Y(400))))
    s.append(r"\node[anchor=north west,text=otInk,align=left] at (%s,%s) {village : $400$ m\\$12$ °C};" % (f(V[0] + .1), f(Y(400) - .08)))
    t_ref = r" ; \textcolor{otGreenDark}{$-3$ °C}" if corrige else ""
    t_som = r" ; \textcolor{otGreenDark}{$-4{,}8$ °C}" if corrige else ""
    s.append(r"\node[anchor=south east,text=otInk] at (%s,%s) {refuge : $2\,900$ m%s};" % (f(Rf[0] - .1), f(Y(2900) + .12), t_ref))
    s.append(r"\node[anchor=south,text=otInk] at (%s,%s) {sommet : $3\,200$ m%s};" % (f(Sm[0] + (.55 if corrige else .3)), f(Y(3200) + .24), t_som))
    if corrige:
        # 0 °C vers 2 400 m
        xi = 3.2 + (2400 - 2250) / (2900 - 2250) * (4.3 - 3.2)
        s.append(r"\draw[%s,line width=.8pt,dash pattern=on 3pt off 2pt] (0,%s) -- (%s,%s);" % (VERT, f(Y(2400)), f(xi), f(Y(2400))))
        s.append(point(xi, Y(2400), VERT, 2.8))
        s.append(r"\node[anchor=south west,text=%s] at (.12,%s) {$0$ °C vers $2\,400$ m};" % (VERT, f(Y(2400) + .04)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_montagne_enonce"] = montagne(False)
FIGURES["ex_montagne_corrige"] = montagne(True)

# ===================================================================== 2475 : évolution du solde
FIGURES["ex_compte_corrige"] = r"""\begin{tikzpicture}
\begin{axis}[otBarres, ymajorgrids=false, width=6.3cm, height=4.2cm, ymin=-80, ymax=260,
  enlarge x limits=0.1, bar width=15pt, xtick={1,2,3,4,5,6},
  xticklabels={1\textsuperscript{er},3,7,12,15,20}, xlabel={jour de mars}, ylabel={solde (€)},
  ytick={-50,0,50,100,150,200,250},
  nodes near coords, point meta=explicit symbolic,
  every node near coord/.append style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otInk}]
\addplot[fill=otNavy!55,draw=otNavy,bar shift=0pt] coordinates {(1,125)[$125$] (2,76.5)[$76{,}5$] (3,21)[$21$] (5,211)[$211$]};
\addplot[fill=otOrange!75,draw=otOrange!80!black,bar shift=0pt,
  every node near coord/.append style={anchor=north,yshift=-2pt,text=otOrange!70!black}]
  coordinates {(4,-39)[$-39$] (6,-19)[$-19$]};
\draw[otInk,line width=.7pt] (axis cs:0.4,0) -- (axis cs:6.6,0);
\end{axis}
\end{tikzpicture}"""


# ===================================================================== 2479 : échelles Celsius / Fahrenheit
def echelles():
    U = .036
    Y = lambda c: U * (c + 50)
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[otNavy,line width=.9pt] (-.2,%s) rectangle (.2,%s);" % (f(Y(-50)), f(Y(110))))
    s.append(r"\node[anchor=south,text=otNavy] at (-.75,%s) {°C};" % f(Y(110) + .1))
    s.append(r"\node[anchor=south,text=otNavy] at (.75,%s) {°F};" % f(Y(110) + .1))
    for c in range(-40, 101, 20):
        s.append(r"\draw[grad] (-.2,%s) -- (-.36,%s);" % (f(Y(c)), f(Y(c))))
        s.append(r"\node[gradTexteG] at (-.4,%s) {$%s$};" % (f(Y(c)), nb(c)))
    for c, F in ((-40, -40), (-20, -4), (0, 32), (100, 212)):
        s.append(r"\draw[grad] (.2,%s) -- (.36,%s);" % (f(Y(c)), f(Y(c))))
        coul = VERT if c == -40 else "otMuted"
        s.append(r"\node[gradTexteD,text=%s] at (.4,%s) {$%s$};" % (coul, f(Y(c)), nb(F)))
    s.append(r"\draw[%s,line width=1.6pt] (-.18,%s) -- (.18,%s);" % (VERT, f(Y(-40)), f(Y(-40))))
    s.append(r"\node[anchor=west,text=%s] at (1.2,%s) {$-40$ °C $= -40$ °F};" % (VERT, f(Y(-40))))
    s.append(r"\node[anchor=west,petit,text=otMuted] at (1.2,%s) {l'eau bout};" % f(Y(100)))
    s.append(r"\node[anchor=west,petit,text=otMuted] at (1.2,%s) {l'eau gèle};" % f(Y(0)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_echelles_corrige"] = echelles()


# ===================================================================== 2480 : carré magique
def carre(corrige):
    c = 1.3
    M = [["a", "-4", "b"], ["-2", "0", "2"], ["c", "4", "-3"]]
    sol = {"a": "3", "b": "1", "c": "-1"}
    s = [r"\begin{tikzpicture}"]
    for i in range(4):
        s.append(r"\draw[case] (%s,0) -- (%s,%s);" % (f(i * c), f(i * c), f(3 * c)))
        s.append(r"\draw[case] (0,%s) -- (%s,%s);" % (f(i * c), f(3 * c), f(i * c)))
    for i, ligne in enumerate(M):
        for j, v in enumerate(ligne):
            xc, yc = (j + .5) * c, (2.5 - i) * c
            if v in sol:
                if corrige:
                    s.append(r"\node[text=%s,font=\Large] at (%s,%s) {$%s$};" % (VERT, f(xc), f(yc), sol[v]))
                else:
                    s.append(r"\node[text=otOrange!85!black,font=\Large] at (%s,%s) {$%s$};" % (f(xc), f(yc), v))
            else:
                s.append(r"\node[text=otInk,font=\Large] at (%s,%s) {$%s$};" % (f(xc), f(yc), v))
    if corrige:
        s.append(r"\node[anchor=north,text=%s] at (%s,-.15) {somme magique : $0$};" % (VERT, f(1.5 * c)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_carre_enonce"] = carre(False)
FIGURES["ex_carre_corrige"] = carre(True)


# ===================================================================== 2481 : pyramides de produits
def pyramide(titre, etages, w=1.25, h=.62):
    """etages : liste de la base au sommet ; chaque case = (texte, couleur) ou None (vide)."""
    s = [r"\begin{tikzpicture}"]
    nbase = len(etages[0])
    for k, et in enumerate(etages):
        x0 = k * w / 2
        y0 = k * h
        for i, case in enumerate(et):
            x = x0 + i * w
            s.append(r"\draw[case,fill=white] (%s,%s) rectangle (%s,%s);" % (f(x), f(y0), f(x + w), f(y0 + h)))
            if case:
                t, col = case
                s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (col, f(x + w / 2), f(y0 + h / 2), t))
    s.append(r"\node[anchor=south,text=otNavy,font=\bfseries] at (%s,%s) {%s};" % (f(nbase * w / 2), f(len(etages) * h + .1), titre))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


I = "otInk"
FIGURES["ex_pyr1_enonce"] = pyramide("Pyramide 1", [[("-2", I), ("3", I), ("-1", I), ("4", I)], [None] * 3, [None] * 2, [None]])
FIGURES["ex_pyr2_enonce"] = pyramide("Pyramide 2", [[("5", I), None, ("-2", I)], [("-15", I), None], [None]], w=1.45)
FIGURES["ex_pyr1_corrige"] = pyramide("Pyramide 1", [[("-2", I), ("3", I), ("-1", I), ("4", I)],
                                                     [("-6", VERT), ("-3", VERT), ("-4", VERT)],
                                                     [("18", VERT), ("12", VERT)], [("216", VERT)]])
FIGURES["ex_pyr1bis_corrige"] = pyramide("Pyramide 1 modifiée", [[("-2", I), ("3", I), ("-1", I), ("-4", "otOrange!85!black")],
                                                                 [("-6", VERT), ("-3", VERT), ("4", VERT)],
                                                                 [("18", VERT), ("-12", VERT)], [("-216", VERT)]])
FIGURES["ex_pyr2_corrige"] = pyramide("Pyramide 2", [[("5", I), ("-3", VERT), ("-2", I)], [("-15", I), ("6", VERT)],
                                                     [("-90", VERT)]], w=1.45)


# ===================================================================== 2482 : programme de calcul
def programme(corrige):
    etapes = ["Choisir un nombre", r"Le multiplier par $-4$", r"Ajouter $6$", r"Diviser le résultat par $-2$"]
    expr = [r"$x$", r"$-4x$", r"$-4x + 6$", r"$2x - 3$"]
    s = [r"\begin{tikzpicture}"]
    dy = 1.05
    for k, e in enumerate(etapes):
        s.append(r"\node[boiteP,minimum width=4.4cm] (b%d) at (0,%s) {%s};" % (k, f(-k * dy), e))
        if k:
            s.append(r"\draw[fleche] (b%d.south) -- (b%d.north);" % (k - 1, k))
        if corrige:
            s.append(r"\node[anchor=west,text=%s] at ($(b%d.east)+(.3,0)$) {%s};" % (VERT, k, expr[k]))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_programme_enonce"] = programme(False)
FIGURES["ex_programme_corrige"] = programme(True)


# ===================================================================== 2483 : profil de randonnée
def profil(corrige):
    alts = [850, 1170, 1020, 1430, 1155, 850]
    noms = ["D", "A", "B", "C", "E", "F"]
    var = ["+320", "-150", "+410", "-275", "-305"]
    dx = 1.55
    Y = lambda a: (a - 700) * .0068
    P = [(i * dx, Y(a)) for i, a in enumerate(alts)]
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[otNavy,line width=1.3pt,line join=round] %s;" % " -- ".join("(%s,%s)" % (f(x), f(y)) for x, y in P))
    for (x, y), nm in zip(P, noms):
        s.append(point(x, y, "otOrange!90!black", 2.8))
    # noms des points : au-dessus des sommets, au-dessous des creux
    pos = ["below", "above", "below", "above", "above right", "below"]
    for (x, y), nm, p in zip(P, noms, pos):
        s.append(r"\node[%s=3pt,text=otInk] at (%s,%s) {$%s$};" % (p, f(x), f(y), nm))
    # variations : au milieu de chaque segment, décalées hors du tracé
    for i, v in enumerate(var):
        (x1, y1), (x2, y2) = P[i], P[i + 1]
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        monte = y2 > y1
        anc = "south east" if monte else "south west"
        s.append(r"\node[anchor=%s,text=otOrange!85!black,inner sep=1.5pt] at (%s,%s) {$%s$ m};"
                 % (anc, f(xm - .08 if monte else xm + .08), f(ym + .1), nb(int(v)) if v.startswith("-") else v))
    if corrige:
        offs = {0: ("below", "D"), 1: ("above", "A"), 2: ("below", "B"), 3: ("above", "C"), 4: ("above right", "E"), 5: ("below", "F")}
        for i, ((x, y), a) in enumerate(zip(P, alts)):
            p = offs[i][0]
            if p == "below":
                s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,%s) {$%s$ m};" % (VERT, f(x), f(y - .52), nb(a).replace("1", "1", 1) if a < 1000 else r"1\,%03d" % (a - 1000)))
            elif p == "above":
                s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,%s) {$%s$ m};" % (VERT, f(x), f(y + .52), r"1\,%03d" % (a - 1000)))
            else:
                s.append(r"\node[anchor=south west,text=%s,inner sep=1pt] at (%s,%s) {$%s$ m};" % (VERT, f(x + .2), f(y + .42), r"1\,%03d" % (a - 1000)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_profil_enonce"] = profil(False)
FIGURES["ex_profil_corrige"] = profil(True)


# ===================================================================== 2484 : fuseaux horaires
def fuseaux(corrige):
    s = [r"\begin{tikzpicture}"]
    c, X = droite(-9, 10, .42, y=0)
    s.append(c)
    villes = [(-8, "Los Angeles", 1.0), (-5, "New York", .35), (1, "Paris", .35), (9, "Tokyo", .35)]
    for v, nom, h in villes:
        coul = "otNavy" if v == 1 else "otOrange!90!black"
        s.append(point(X(v), 0, coul, 2.8))
        if h > .5:
            s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.12) -- (%s,%s);" % (f(X(v)), f(X(v)), f(h - .02)))
        s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (coul, f(X(v)), f(h - .2 if h < .5 else h), nom))
    s.append(r"\node[anchor=north,petit,text=otMuted] at (%s,%s) {décalage par rapport à l'heure universelle (en heures)};"
             % (f(X(.5)), f(-.6 if not corrige else -1.75)))
    if corrige:
        s.append(arc_dessus(X(1), X(-5), -.55, .55, "deplV", r"$-6$ h", VERT, dessous=True))
        s.append(arc_dessus(X(1), X(9), -.55, .55, "deplV", r"$+8$ h", VERT, dessous=True))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_fuseaux_enonce"] = fuseaux(False)
FIGURES["ex_fuseaux_corrige"] = fuseaux(True)
