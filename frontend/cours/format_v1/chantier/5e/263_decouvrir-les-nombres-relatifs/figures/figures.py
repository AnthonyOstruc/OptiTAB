# -*- coding: utf-8 -*-
"""Figures de la notion 263 (5e : découvrir les nombres relatifs), style des livres.

Compilées par outils/figures_livre.py. Droites graduées, thermomètres, repères du
plan, schéma d'altitudes, coupe d'immeuble (ascenseur). Éléments de réponse en
vert foncé (otGreenDark) dans les corrigés ; l'énoncé ne donne jamais la réponse.
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
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  accolV/.style={otGreenDark,line width=.7pt,decorate,decoration={brace,amplitude=4pt}},
}
\pgfplotsset{repere/.style={otWeb, xlabel={}, ylabel={},
  yticklabel style={anchor=east,xshift=-2.5pt,yshift=0pt}}}
"""

VERT = "otGreenDark"
NAVY = "otNavy"
ORANGE = "otOrange!90!black"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def nb(v):
    """Nombre relatif écrit en LaTeX (virgule décimale)."""
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s.replace(".", "{,}")


# ===================================================================== outils communs
def droite(a, b, U, y=0.0, pas=1.0, labels="tout", lab_pas=1.0):
    """Droite graduée horizontale de a à b, U cm par unité, graduations tous les « pas ».

    labels = "tout" (toutes les graduations multiples de lab_pas) ou liste de valeurs.
    Renvoie (code, X).
    """
    X = lambda v: U * (v - a)
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(X(a) - .3), f(y), f(X(b) + .45), f(y))]
    n = int(round((b - a) / pas))
    for i in range(n + 1):
        v = round(a + i * pas, 6)
        entier = abs(v / lab_pas - round(v / lab_pas)) < 1e-9
        h = .1 if entier else .065
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(v)), f(y - h), f(X(v)), f(y + h)))
        mettre = (labels == "tout" and entier) or (labels != "tout" and any(abs(v - w) < 1e-9 for w in labels))
        if mettre:
            s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X(v)), f(y - .16), nb(v)))
    return "\n".join(s), X


def point(x, y, coul=NAVY, r=2.5):
    return r"\fill[%s] (%s,%s) circle (%spt);" % (coul, f(x), f(y), f(r))


def nom_dessus(x, y, texte, coul=NAVY, h=.16):
    return r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y + h), texte)


def nom_dessus_haut(x, y, texte, coul=NAVY, h=.62):
    """Étiquette surélevée, reliée au point par un fin trait de rappel."""
    return (r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y + .13), f(x), f(y + h - .02))
            + "\n" + r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y + h), texte))


FIGURES = {}


# ===================================================================== thermomètre
def thermometre(tmin, tmax, U, marques, pas_label=2, x=0.0, largeur=.42):
    """Thermomètre vertical. marques : [(t, texte_gauche, couleur)]. Graduations à droite."""
    Y = lambda t: U * (t - tmin)
    w = largeur
    s = []
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
    # repère du zéro
    s.append(r"\draw[otNavy!60,line width=.9pt] (%s,%s) -- (%s,%s);" % (f(x + w / 2), f(Y(0)), f(x + w / 2 + .2), f(Y(0))))
    for t, txt, c in marques:
        s.append(r"\draw[%s,line width=1.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 + .05), f(Y(t)), f(x + w / 2 - .05), f(Y(t))))
        s.append(r"\draw[%s,line width=.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 - .12), f(Y(t)), f(x - w / 2 - .42), f(Y(t))))
        s.append(r"\node[anchor=east,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (c, f(x - w / 2 - .45), f(Y(t)), txt))
    return "\n".join(s)


# ===================================================================== COURS
# 1. thermomètre : sous zéro / au-dessus de zéro
FIGURES["cours_thermometre"] = "\n".join([
    r"\begin{tikzpicture}",
    thermometre(-8, 8, .26, [(6, r"après-midi : $6$ °C", NAVY), (-4, r"nuit : $-4$ °C", ORANGE)]),
    r"\node[anchor=west,petit,text=otNavy,align=left] at (1.35,%s) {au-dessus de zéro :\\nombres positifs};" % f(.26 * (4 + 8)),
    r"\node[anchor=west,petit,text=otOrange!85!black,align=left] at (1.35,%s) {sous zéro :\\nombres négatifs};" % f(.26 * (-4 + 8)),
    r"\end{tikzpicture}"])


# 2. droite graduée : origine, sens, unité, abscisses
def cours_droite():
    c, X = droite(-5, 4, .66, pas=.5, lab_pas=1)
    s = [r"\begin{tikzpicture}", c]
    for v, nm in ((-4, "E"), (-1.5, "F"), (2.5, "G")):
        s.append(point(X(v), 0, ORANGE, 2.8))
        s.append(nom_dessus(X(v), 0, r"$%s(%s)$" % (nm, nb(v)), "otInk"))
    # unité
    s.append(r"\draw[cote] (%s,.95) -- (%s,.95);" % (f(X(0)), f(X(1))))
    s.append(r"\node[anchor=south,petit,text=otMuted,inner sep=1pt] at (%s,1.0) {unité};" % f(X(.5)))
    s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.14) -- (%s,1.02) (%s,.14) -- (%s,1.02);" % (f(X(0)), f(X(0)), f(X(1)), f(X(1))))
    s.append(r"\node[anchor=north,petit,text=otMuted] at (%s,-.55) {origine $O$};" % f(X(0)))
    s.append(r"\node[anchor=north east,petit,text=otMuted] at (%s,-.55) {sens positif $\rightarrow$};" % f(X(4) + .5))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_droite"] = cours_droite()


# 3. opposés et distance à zéro
def cours_opposes():
    c, X = droite(-5, 5, .56)
    s = [r"\begin{tikzpicture}", c]
    for v in (-3.5, 3.5):
        s.append(point(X(v), 0, ORANGE, 2.8))
    for v1, v2 in ((-3.5, 0), (0, 3.5)):
        s.append(r"\draw[cote] (%s,.5) -- (%s,.5);" % (f(X(v1)), f(X(v2))))
        s.append(r"\node[anchor=south,text=otInk,inner sep=1.5pt] at (%s,.56) {$3{,}5$};" % f((X(v1) + X(v2)) / 2))
    for v in (-3.5, 0, 3.5):
        s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.13) -- (%s,.6);" % (f(X(v)), f(X(v))))
    s.append(r"\node[anchor=north,text=otInk,align=center] at (%s,-.62) {$-3{,}5$ et $3{,}5$ sont opposés :\\même distance à zéro, de part et d'autre de $0$.};" % f(X(0)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_opposes"] = cours_opposes()


# 4. repère du plan
def repere(points, xmin=-5, xmax=5, ymin=-4, ymax=4, w=6.6, h=None, extra=""):
    """Repère orthogonal quadrillé. points : [(x, y, texte, ancre, couleur)]."""
    ux = w / (xmax - xmin + 1)
    h = h or ux * (ymax - ymin + 1)
    xt = ",".join(str(k) for k in range(xmin, xmax + 1) if k)
    yt = ",".join(str(k) for k in range(ymin, ymax + 1) if k)
    s = [r"\begin{axis}[repere, width=%scm, height=%scm, xmin=%s, xmax=%s, ymin=%s, ymax=%s, xtick={%s}, ytick={%s}]"
         % (f(w), f(h), f(xmin - .5), f(xmax + .5), f(ymin - .5), f(ymax + .5), xt, yt)]
    s.append(r"\node[anchor=north east,text=otMuted,inner sep=2pt] at (axis cs:0,0) {$O$};")
    s.append(extra)
    for x, y, txt, anc, c in points:
        s.append(r"\fill[%s] (axis cs:%s,%s) circle (2.6pt);" % (c, f(x), f(y)))
        if txt:
            s.append(r"\node[anchor=%s,text=%s,inner sep=2.5pt] at (axis cs:%s,%s) {%s};" % (anc, c, f(x), f(y), txt))
    s.append(r"\end{axis}")
    return "\n".join(s)


def cours_repere():
    guides = (r"\draw[otGreenDark,line width=.7pt,dash pattern=on 2.5pt off 1.8pt] (axis cs:2,3) -- (axis cs:2,0);" "\n"
              r"\draw[otGreenDark,line width=.7pt,dash pattern=on 2.5pt off 1.8pt] (axis cs:2,3) -- (axis cs:0,3);")
    pts = [(2, 3, r"$P(2\,;\,3)$", "south west", NAVY),
           (-4, 1, r"$Q(-4\,;\,1)$", "south", NAVY),
           (-3, -2, r"$R(-3\,;\,-2)$", "north", NAVY),
           (4, -2, r"$S(4\,;\,-2)$", "north", NAVY)]
    s = [r"\begin{tikzpicture}", repere(pts, extra=guides), r"\end{tikzpicture}"]
    return "\n".join(s)


FIGURES["cours_repere"] = cours_repere()


# 5. comparer deux nombres négatifs
def cours_comparer():
    c, X = droite(-9, 2, .54)
    s = [r"\begin{tikzpicture}", c]
    for v in (-8, -3):
        s.append(point(X(v), 0, ORANGE, 2.8))
        s.append(nom_dessus(X(v), 0, r"$%s$" % nb(v), "otInk"))
    s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.4mm]}] (%s,.95) -- (%s,.95);" % (f(X(-9)), f(X(2))))
    s.append(r"\node[anchor=south,petit,text=otGreenDark] at (%s,1.0) {les nombres augmentent vers la droite};" % f(X(-3.5)))
    s.append(r"\node[anchor=north,text=otInk] at (%s,-.6) {$-8$ est à gauche de $-3$, donc $-8 < -3$.};" % f(X(-3.5)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_comparer"] = cours_comparer()


# ===================================================================== 2747 : thermomètre de Gap
def thermo_gap(corrige):
    if corrige:
        m = [(5, r"14 h : $5$ °C", VERT), (-3, r"7 h : $-3$ °C", VERT)]
    else:
        m = [(5, r"14 h", NAVY), (-3, r"7 h", NAVY)]
    return "\n".join([r"\begin{tikzpicture}", thermometre(-10, 10, .23, m), r"\end{tikzpicture}"])


FIGURES["ex2747_thermo_enonce"] = thermo_gap(False)
FIGURES["ex2747_thermo_corrige"] = thermo_gap(True)


# ===================================================================== 2752 : lire et placer (pas 0,5)
def droite_demi(corrige):
    c, X = droite(-4, 3, .86, pas=.5, labels=[0, 1])
    s = [r"\begin{tikzpicture}", c]
    lus = [(-2.5, "A"), (-.5, "B"), (1.5, "C")]
    for v, nm in lus:
        s.append(point(X(v), 0, NAVY, 2.8))
        txt = r"$%s(%s)$" % (nm, nb(v)) if corrige else r"$%s$" % nm
        s.append(r"\node[anchor=south,inner sep=1.5pt] at (%s,.16) {%s};" % (f(X(v)), (r"\textcolor{otGreenDark}{%s}" % txt) if corrige else txt))
    if corrige:
        for v, nm in ((-3, "E"), (2, "F"), (-1.5, "G")):
            s.append(point(X(v), 0, VERT, 2.8))
            s.append(r"\node[anchor=north,text=%s,inner sep=1.5pt] at (%s,-.62) {$%s(%s)$};" % (VERT, f(X(v)), nm, nb(v)))
            s.append(r"\draw[%s!60,line width=.4pt] (%s,-.13) -- (%s,-.6);" % (VERT, f(X(v)), f(X(v))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2752_droite_enonce"] = droite_demi(False)
FIGURES["ex2752_droite_corrige"] = droite_demi(True)


# ===================================================================== 2748 : opposés sur la droite
def droite_opposes(corrige):
    c, X = droite(-6, 6, .52)
    s = [r"\begin{tikzpicture}", c]
    for v, nm in ((-5, "M"), (2, "N")):
        s.append(point(X(v), 0, NAVY, 2.8))
        s.append(nom_dessus(X(v), 0, r"$%s$" % nm, NAVY))
    if corrige:
        for v, nm in ((5, "P"), (-2, "Q")):
            s.append(point(X(v), 0, VERT, 2.8))
            s.append(nom_dessus(X(v), 0, r"$%s$" % nm, VERT))
        # distances égales, sous la droite
        for v1, v2, t, yy in ((-5, 0, "5", -.75), (0, 5, "5", -.75), (-2, 0, "2", -1.35), (0, 2, "2", -1.35)):
            s.append(r"\draw[cote,%s] (%s,%s) -- (%s,%s);" % (VERT, f(X(v1)), f(yy), f(X(v2)), f(yy)))
            s.append(r"\node[anchor=north,text=%s,inner sep=1.5pt] at (%s,%s) {$%s$};" % (VERT, f((X(v1) + X(v2)) / 2), f(yy - .04), t))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2748_opposes_enonce"] = droite_opposes(False)
FIGURES["ex2748_opposes_corrige"] = droite_opposes(True)


# ===================================================================== 2749 : repère, lire et placer
def repere_2749(corrige):
    c = VERT if corrige else NAVY
    if corrige:
        lus = [(3, 2, r"$A(3\,;\,2)$", "south west"), (-4, 3, r"$B(-4\,;\,3)$", "south"),
               (-2, -3, r"$C(-2\,;\,-3)$", "north"), (4, -1, r"$D(4\,;\,-1)$", "north"),
               (0, 3, r"$E(0\,;\,3)$", "south west"), (-3, 0, r"$F(-3\,;\,0)$", "south")]
    else:
        lus = [(3, 2, r"$A$", "south west"), (-4, 3, r"$B$", "south east"), (-2, -3, r"$C$", "north east"),
               (4, -1, r"$D$", "north west"), (0, 3, r"$E$", "south west"), (-3, 0, r"$F$", "south")]
    pts = [(x, y, t, a, c) for x, y, t, a in lus]
    if corrige:
        pts += [(-1, 4, r"$G$", "south east", VERT), (2, -4, r"$H$", "north west", VERT),
                (-5, -2, r"$K$", "east", VERT), (-3, 2, r"$M$", "north east", VERT)]
        # pts lus en bleu, réponses (coordonnées) en vert
        pts = [(x, y, t, a, VERT if t else NAVY) for x, y, t, a, _ in pts]
    return "\n".join([r"\begin{tikzpicture}", repere(pts, h=5.4), r"\end{tikzpicture}"])


FIGURES["ex2749_repere_enonce"] = repere_2749(False)
FIGURES["ex2749_repere_corrige"] = repere_2749(True)


# ===================================================================== 2751 : températures des villes
def villes():
    data = [(5, "Rome"), (2.5, "Paris"), (-1, "Berlin"), (-4.5, "Oslo"), (-7, "Helsinki"),
            (-9.5, "Moscou"), (-12, "Montréal")]
    m = [(v, r"%s : $%s$ °C" % (nm, nb(v)), VERT) for v, nm in data]
    return "\n".join([r"\begin{tikzpicture}", thermometre(-14, 6, .27, m), r"\end{tikzpicture}"])


FIGURES["ex2751_villes_corrige"] = villes()


# ===================================================================== 2759 : quatre points placés
def placement_2759():
    c, X = droite(-5, 4, .7, pas=.5, lab_pas=1)
    s = [r"\begin{tikzpicture}", c]
    for v, nm, haut in ((-4.5, "A", False), (-3.2, "C", True), (-.7, "E", True), (.7, "D", False), (3.2, "B", False)):
        s.append(point(X(v), 0, VERT, 2.8))
        if haut:
            s.append(nom_dessus_haut(X(v), 0, r"$%s(%s)$" % (nm, nb(v)), VERT, .62))
        else:
            s.append(nom_dessus(X(v), 0, r"$%s(%s)$" % (nm, nb(v)), VERT))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2759_droite_corrige"] = placement_2759()


# ===================================================================== 2750 : l'ascenseur de la tour
def immeuble(corrige):
    h, W = .42, 1.7
    s = [r"\begin{tikzpicture}"]
    for k in range(-3, 9):
        y0 = k * h
        fill = "otMuted!14" if k < 0 else "otSky"
        s.append(r"\filldraw[fill=%s,draw=otNavy,line width=.7pt] (0,%s) rectangle (%s,%s);" % (fill, f(y0), f(W), f(y0 + h)))
        s.append(r"\node[gradTexteG] at (-.12,%s) {$%s$};" % (f(y0 + h / 2), nb(k)))
        # fenêtres
        if k >= 0:
            for xw in (.3, .75, 1.2):
                s.append(r"\fill[otNavy!35] (%s,%s) rectangle (%s,%s);" % (f(xw), f(y0 + .12), f(xw + .2), f(y0 + .3)))
    # cage d'ascenseur (pointillés) et toit
    s.append(r"\draw[otNavy,line width=.9pt] (-.1,%s) -- (%s,%s);" % (f(9 * h), f(W + .1), f(9 * h)))
    # sol
    s.append(r"\draw[otGreenDark!70!black,line width=1.6pt] (%s,0) -- (%s,0);" % (f(-.05), f(W + .42)))
    s.append(r"\node[anchor=south,petit,text=otMuted] at (-.3,%s) {étage};" % f(9 * h + .1))
    if corrige:
        xa = W + .25
        for k in (-3, -2, 0, 3, 5, 7):
            s.append(point(xa, k * h + h / 2, VERT, 2.8))
        s.append(r"\draw[accolV] (%s,%s) -- (%s,%s);" % (f(xa + .25), f(3 * h + h / 2), f(xa + .25), f(-2 * h + h / 2)))
        s.append(r"\node[anchor=west,text=%s,align=left] at (%s,%s) {de $-2$ à $3$ :\\$5$ étages};" % (VERT, f(xa + .45), f(h)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2750_immeuble_enonce"] = immeuble(False)
FIGURES["ex2750_immeuble_corrige"] = immeuble(True)


# ===================================================================== 2753 : altitudes et profondeurs
def ic_oiseau(x, y, c):
    return (r"\draw[%s,line width=1pt,line cap=round] (%s,%s) .. controls (%s,%s) .. (%s,%s) .. controls (%s,%s) .. (%s,%s);"
            % (c, f(x - .28), f(y + .06), f(x - .14), f(y + .16), f(x), f(y - .02), f(x + .14), f(y + .16), f(x + .28), f(y + .06)))


def ic_plongeur(x, y, c):
    return (r"\fill[%s] (%s,%s) circle (2.6pt);" % (c, f(x - .2), f(y))
            + "\n" + r"\draw[%s,line width=1.6pt,line cap=round] (%s,%s) -- (%s,%s);" % (c, f(x - .12), f(y), f(x + .22), f(y))
            + "\n" + r"\draw[%s,line width=1pt,line cap=round] (%s,%s) -- (%s,%s) (%s,%s) -- (%s,%s);"
            % (c, f(x + .22), f(y), f(x + .36), f(y + .07), f(x + .22), f(y), f(x + .36), f(y - .07)))


def ic_sousmarin(x, y, c):
    return (r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) ellipse (.42 and .12);" % (c, c, f(x), f(y))
            + "\n" + r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) rectangle (%s,%s);"
            % (c, c, f(x - .08), f(y + .09), f(x + .1), f(y + .22)))


def ic_bateau(x, y, c):
    return (r"\filldraw[fill=%s!85,draw=%s,line width=.6pt] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
            % (c, c, f(x - .38), f(y + .12), f(x + .38), f(y + .12), f(x + .26), f(y - .02), f(x - .26), f(y - .02))
            + "\n" + r"\draw[%s,line width=.8pt] (%s,%s) -- (%s,%s);" % (c, f(x), f(y + .12), f(x), f(y + .5))
            + "\n" + r"\fill[%s!60] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;" % (c, f(x + .04), f(y + .48), f(x + .04), f(y + .17), f(x + .3), f(y + .17)))


def ic_epave(x, y, c):
    return (r"\filldraw[fill=%s!55,draw=%s,line width=.6pt,rotate around={-14:(%s,%s)}] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
            % (c, c, f(x), f(y), f(x - .36), f(y + .1), f(x + .36), f(y + .1), f(x + .24), f(y - .06), f(x - .24), f(y - .06)))


def ic_falaise(x, y, c, y0):
    """Falaise posée sur le niveau de la mer (y0), sommet en (x, y)."""
    return (r"\filldraw[fill=otMuted!30,draw=otMuted,line width=.6pt] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
            % (f(x - .55), f(y0), f(x - .5), f(y - .25), f(x - .2), f(y), f(x), f(y), f(x + .08), f(y0))
            + "\n" + point(x, y, c, 2.6))


def altitudes_2753(corrige):
    U = .047 if corrige else .034
    amin, amax = -80, 80
    Y = lambda a: U * (a - amin)
    mer_x = 2.2
    lab_x = 2.45
    s = [r"\begin{tikzpicture}"]
    s.append(r"\fill[otSky] (.12,%s) rectangle (%s,%s);" % (f(Y(amin)), f(mer_x), f(Y(0))))
    s.append(r"\draw[otNavy!55,line width=.9pt] (.12,%s) -- (%s,%s);" % (f(Y(0)), f(mer_x), f(Y(0))))
    s.append(r"\draw[axeV] (0,%s) -- (0,%s);" % (f(Y(amin) - .1), f(Y(amax) + .45)))
    s.append(r"\node[anchor=south,petit,text=otMuted] at (0,%s) {altitude (m)};" % f(Y(amax) + .5))
    for a in range(amin, amax + 1, 10):
        lg = .1 if a % 20 == 0 else .06
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(-lg), f(Y(a)), f(lg), f(Y(a))))
        if a % 20 == 0:
            s.append(r"\node[gradTexteG] at (-.14,%s) {$%s$};" % (f(Y(a)), nb(a)))
    items = [(70, "falaise", "sommet de la falaise", NAVY),
             (40, "oiseau", "mouette", NAVY),
             (0, "bateau", "bateau", NAVY),
             (-30, "plongeur", "plongeuse", NAVY),
             (-50, "epave", "épave", ORANGE),
             (-70, "sousmarin", "sous-marin", ORANGE)]
    xi = .95
    for a, ic, nom, c in items:
        y = Y(a)
        if ic == "falaise":
            s.append(ic_falaise(2.0, y, c, Y(0)))
            s.append(r"\draw[guide] (.14,%s) -- (1.74,%s);" % (f(y), f(y)))
        elif ic == "oiseau":
            s.append(ic_oiseau(xi, y, c))
        elif ic == "bateau":
            s.append(ic_bateau(xi, y, c))
        elif ic == "plongeur":
            s.append(ic_plongeur(xi, y, c))
        elif ic == "epave":
            s.append(ic_epave(xi, y, c))
        else:
            s.append(ic_sousmarin(xi, y, c))
        # guide horizontal vers l'axe
        if ic != "falaise":
            s.append(r"\draw[guide] (.14,%s) -- (%s,%s);" % (f(y), f(xi - .45), f(y)))
        if corrige:
            txt = r"%s\\\textcolor{otGreenDark}{$%s$ m}" % (nom, nb(a))
        else:
            txt = nom
        if ic == "bateau":
            anc, yy = "south west", y + (.02 if corrige else .06)
        else:
            anc, yy = "west", y
        s.append(r"\node[anchor=%s,text=otInk,inner sep=1.5pt,align=left] at (%s,%s) {%s};" % (anc, f(lab_x), f(yy), txt))
    if not corrige:
        s.append(r"\node[anchor=west,petit,text=otNavy!80,inner sep=1.5pt] at (%s,%s) {(niveau de la mer)};" % (f(lab_x), f(Y(0) - .2)))
    if corrige:
        xe = 4.75
        s.append(r"\draw[cote,%s] (%s,%s) -- (%s,%s);" % (VERT, f(xe), f(Y(40)), f(xe), f(Y(-30))))
        s.append(r"\node[anchor=west,text=%s,align=left] at (%s,%s) {écart :\\$40 + 30$\\$= 70$ m};" % (VERT, f(xe + .1), f(Y(5))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2753_altitudes_enonce"] = altitudes_2753(False)
FIGURES["ex2753_altitudes_corrige"] = altitudes_2753(True)


# ===================================================================== 2765 : zoom entre -2,7 et -2,3
def zoom_2765():
    a, b, U = -2.7, -2.3, 14.5
    X = lambda v: U * (v - a)
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[axe] (%s,0) -- (%s,0);" % (f(-.4), f(X(b) + .5)))
    for i in range(0, 41):
        v = round(a + i * .01, 4)
        dix = i % 10 == 0
        cinq = i % 5 == 0
        hh = .12 if dix else (.08 if cinq else .045)
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(v)), f(-hh), f(X(v)), f(hh)))
        if dix:
            s.append(r"\node[gradTexte] at (%s,-.18) {$%s$};" % (f(X(v)), nb(v)))
    # zone solution (bornes exclues)
    s.append(r"\draw[otGreen,line width=3.2pt,opacity=.9] (%s,0) -- (%s,0);" % (f(X(-2.5)), f(X(-2.4))))
    for v in (-2.5, -2.4):
        s.append(r"\draw[otGreenDark,fill=white,line width=1pt] (%s,0) circle (2.6pt);" % f(X(v)))
    s.append(point(X(-2.45), 0, VERT, 3))
    s.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,.2) {$x = -2{,}45$};" % (VERT, f(X(-2.45))))
    # encadrement des indices 1 et 2, au-dessus
    s.append(r"\draw[cote] (%s,.95) -- (%s,.95);" % (f(X(-2.6)), f(X(-2.4))))
    s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.15) -- (%s,1.02) (%s,.15) -- (%s,1.02);" % (f(X(-2.6)), f(X(-2.6)), f(X(-2.4)), f(X(-2.4))))
    s.append(r"\node[anchor=south,petit,text=otMuted,inner sep=1pt] at (%s,1.0) {indices 1 et 2};" % f(X(-2.5)))
    s.append(r"\node[anchor=north,petit,text=%s] at (%s,-.58) {indices 1 à 3 : $-2{,}5 < x < -2{,}4$};" % (VERT, f(X(-2.45))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2765_zoom_corrige"] = zoom_2765()


# ===================================================================== 2754 : sortie au ski
def temperatures_2754():
    data = [(-7, "6 h"), (-5.5, "21 h"), (-4.5, "9 h"), (-2, "18 h"), (1.5, "12 h"), (3, "15 h")]
    m = [(v, r"%s : $%s$ °C" % (hh, nb(v)), VERT) for v, hh in data]
    return "\n".join([r"\begin{tikzpicture}", thermometre(-8, 4, .46, m), r"\end{tikzpicture}"])


FIGURES["ex2754_temperatures_corrige"] = temperatures_2754()


def plan_2754(corrige):
    pts = [(-3, 2, r"$C$", "south east", NAVY), (2, 4, r"$T$", "south west", NAVY),
           (4, -1, r"$R$", "south west", NAVY), (-4, -3, r"$P$", "north east", NAVY)]
    if corrige:
        pts = [(-3, 2, r"$C(-3\,;\,2)$", "south", VERT), (2, 4, r"$T(2\,;\,4)$", "south west", VERT),
               (4, -1, r"$R(4\,;\,-1)$", "north", VERT), (-4, -3, r"$P(-4\,;\,-3)$", "north", VERT),
               (-2, -1, r"$S$", "north", VERT), (-4, -1, r"$F$", "east", VERT)]
    return "\n".join([r"\begin{tikzpicture}", repere(pts, h=5.4), r"\end{tikzpicture}"])


FIGURES["ex2754_plan_enonce"] = plan_2754(False)
FIGURES["ex2754_plan_corrige"] = plan_2754(True)
