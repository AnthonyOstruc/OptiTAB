# -*- coding: utf-8 -*-
"""Figures de la notion 130 (6e : repérer, comparer et arrondir), style des livres.

Compilées par outils/figures_livre.py. Demi-droites graduées en dixièmes et en
centièmes, agrandissements (zoom), encadrements et arrondis illustrés.
Énoncé : figure sans la réponse ; corrigé : éléments de réponse en vert foncé
(otGreenDark). Toutes les positions sont calculées en fractions exactes.
"""
from decimal import Decimal
from fractions import Fraction as Fr

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  axeSans/.style={otMuted,line width=.6pt},
  grad/.style={otMuted,line width=.5pt},
  gradF/.style={otMuted,line width=.8pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont},
  zoom/.style={otMuted!80,line width=.5pt,dash pattern=on 2.5pt off 2pt},
  accol/.style={line width=.75pt,decorate,decoration={brace,amplitude=4pt}},
}
"""

VERT = "otGreenDark"
NAVY = "otNavy"
ORANGE = "otOrange!90!black"


def F(s):
    """'2,64' -> Fraction exacte (accepte aussi un entier ou une Fraction)."""
    if isinstance(s, str):
        return Fr(s.replace(",", "."))
    return Fr(s)


def f(v):
    return ("%.4f" % float(v)).rstrip("0").rstrip(".")


def nb(v):
    """Nombre décimal en LaTeX (virgule décimale)."""
    v = F(v)
    d = Decimal(v.numerator) / Decimal(v.denominator)
    s = format(d.normalize(), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def droite(a, b, U, pas, y=0.0, labels=(), moyens=(), origine=False, fleche=True, ext_g=.3, ext_d=.5):
    """Portion de demi-droite graduée de a à b (Fractions), U cm par unité, un trait tous les « pas ».

    labels : valeurs écrites sous la droite ; moyens : traits un peu plus longs (sans texte).
    origine=True : la demi-droite commence à 0 (pas de prolongement à gauche).
    Renvoie (code, X) où X(v) donne l'abscisse en cm.
    """
    a, b, pas = F(a), F(b), F(pas)
    X = lambda v: float(U * (F(v) - a))
    g = 0 if origine else ext_g
    style = "axe" if fleche else "axeSans"
    s = [r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(X(a) - g), f(y), f(X(b) + ext_d), f(y))]
    n = int((b - a) / pas)
    labels = [F(x) for x in labels]
    moyens = [F(x) for x in moyens]
    for i in range(n + 1):
        v = a + i * pas
        if v in labels:
            h, st = .13, "gradF"
        elif v in moyens:
            h, st = .1, "grad"
        else:
            h, st = .065, "grad"
        s.append(r"\draw[%s] (%s,%s) -- (%s,%s);" % (st, f(X(v)), f(y - h), f(X(v)), f(y + h)))
        if v in labels:
            s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X(v)), f(y - .17), nb(v)))
    return "\n".join(s), X


def point(x, y=0.0, coul=NAVY, r=2.6):
    return r"\fill[%s] (%s,%s) circle (%spt);" % (coul, f(x), f(y), f(r))


def dessus(x, y, texte, coul=NAVY, h=.17):
    return r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y + h), texte)


def dessus_haut(x, y, texte, coul=NAVY, h=.62):
    """Étiquette surélevée, reliée au point par un fin trait de rappel."""
    return (r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y + .14), f(x), f(y + h - .03))
            + "\n" + r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y + h), texte))


def accolade(x1, x2, y, texte, coul=VERT, haut=True, petit=False):
    """Accolade horizontale au-dessus (haut=True) ou au-dessous d'un segment, avec son texte."""
    police = ",petit" if petit else ""
    if haut:
        return (r"\draw[accol,%s] (%s,%s) -- (%s,%s);" % (coul, f(x1), f(y), f(x2), f(y))
                + "\n" + r"\node[anchor=south,text=%s,inner sep=1.5pt%s] at (%s,%s) {%s};"
                % (coul, police, f((x1 + x2) / 2), f(y + .2), texte))
    return (r"\draw[accol,%s] (%s,%s) -- (%s,%s);" % (coul, f(x2), f(y), f(x1), f(y))
            + "\n" + r"\node[anchor=north,text=%s,inner sep=1.5pt%s] at (%s,%s) {%s};"
            % (coul, police, f((x1 + x2) / 2), f(y - .2), texte))


def lettre_val(lettre, val, coul_val=VERT):
    """« A(0,4) » : la lettre en bleu, l'abscisse en vert."""
    return r"$%s$\textcolor{%s}{$(%s)$}" % (lettre, coul_val, nb(F(val)))


FIGURES = {}


# ===================================================================== COURS
# 1. demi-droite graduée en dixièmes : origine, unité, abscisses
def cours_droite():
    c, X = droite(0, 2, 2.9, Fr(1, 10), labels=[0, 1, 2], moyens=[Fr(1, 2), Fr(3, 2)], origine=True)
    s = [r"\begin{tikzpicture}", c]
    for v, nm in (("0,7", "A"), ("1,2", "B")):
        s.append(point(X(F(v)), 0, ORANGE, 2.8))
        s.append(dessus(X(F(v)), 0, r"$%s(%s)$" % (nm, nb(F(v))), "otInk"))
    s.append(r"\node[anchor=north,petit,text=otMuted] at (%s,-.55) {origine};" % f(X(0)))
    s.append(accolade(X(1), X(2), -.62, r"$1$ unité $=$ $10$ intervalles", "otNavy", haut=False, petit=True))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_droite"] = cours_droite()


# 2. zoom : placer 2,64
def zoom(a, b, za, U1, U2, pts_haut, pts_bas, lab_haut, lab_bas, moy_bas=(), ecart=2.5, extra_haut="", extra_bas=""):
    """Portion [a ; b] en dixièmes (en haut) et agrandissement [za ; za + 0,1] en centièmes (en bas)."""
    za = F(za)
    zb = za + Fr(1, 10)
    ch, Xh = droite(a, b, U1, Fr(1, 10), y=ecart, labels=lab_haut)
    cb, Xb = droite(za, zb, U2, Fr(1, 100), y=0, labels=lab_bas, moyens=moy_bas)
    s = [ch, cb]
    # traits de l'agrandissement : des extrémités de [za ; zb] (haut) aux extrémités de la droite du bas
    s.append(r"\draw[zoom] (%s,%s) -- (%s,%s);" % (f(Xh(za)), f(ecart - .58), f(Xb(za)), f(.2)))
    s.append(r"\draw[zoom] (%s,%s) -- (%s,%s);" % (f(Xh(zb)), f(ecart - .58), f(Xb(zb)), f(.2)))
    s.append(r"\fill[otSky,opacity=.9] (%s,%s) rectangle (%s,%s);" % (f(Xh(za)), f(ecart - .045), f(Xh(zb)), f(ecart + .045)))
    s.append(r"\draw[otNavy!70,line width=1.4pt] (%s,%s) -- (%s,%s);" % (f(Xh(za)), f(ecart), f(Xh(zb)), f(ecart)))
    for v, txt, coul in pts_haut:
        s.append(point(Xh(F(v)), ecart, coul))
        if txt:
            s.append(dessus(Xh(F(v)), ecart, txt, coul))
    for v, txt, coul, haut in pts_bas:
        s.append(point(Xb(F(v)), 0, coul))
        if txt:
            s.append((dessus_haut if haut else dessus)(Xb(F(v)), 0, txt, coul))
    s.append(extra_haut)
    s.append(extra_bas)
    return "\n".join(s), Xh, Xb


def cours_zoom():
    c, Xh, Xb = zoom(2, 3, "2,6", 5.8, 58, [("2,64", r"$C$", ORANGE)], [("2,64", r"$C(2{,}64)$", ORANGE, False)],
                     [Fr(20 + k, 10) for k in range(11)], [F("2,6"), F("2,65"), F("2,7")])
    s = [r"\begin{tikzpicture}", c,
         r"\end{tikzpicture}"]
    return "\n".join(s)


FIGURES["cours_zoom"] = cours_zoom()


# 3. comparer 6,25 et 6,3
def cours_comparer():
    c, X = droite("6,2", "6,4", 29, Fr(1, 100), labels=[F("6,2"), F("6,3"), F("6,4")], moyens=[F("6,25"), F("6,35")])
    s = [r"\begin{tikzpicture}", c]
    for v in ("6,25", "6,3"):
        s.append(point(X(F(v)), 0, ORANGE, 2.8))
    s.append(dessus(X(F("6,25")), 0, r"$6{,}25$", "otInk"))
    s.append(dessus(X(F("6,3")), 0, r"$6{,}3 = 6{,}30$", "otInk"))
    s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.4mm]}] (%s,1.05) -- (%s,1.05);" % (f(X(F("6,2"))), f(X(F("6,4")))))
    s.append(r"\node[anchor=south,petit,text=otGreenDark] at (%s,1.1) {les nombres augmentent vers la droite};" % f(X(F("6,3"))))
    s.append(r"\node[anchor=north,text=otInk] at (%s,-.62) {donc $6{,}25 < 6{,}3$};" % f(X(F("6,3"))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_comparer"] = cours_comparer()


# 4. encadrer 8,463 au dixième et au centième
def cours_encadrer():
    c, X = droite("8,4", "8,5", 58, Fr(1, 100), labels=[F("8,4"), F("8,5")],
                 moyens=[F("8,4") + Fr(k, 100) for k in range(11)])
    x = X(F("8,463"))
    s = [r"\begin{tikzpicture}", c]
    s.append(r"\draw[otGreenDark,line width=2.2pt,opacity=.85] (%s,0) -- (%s,0);" % (f(X(F("8,46"))), f(X(F("8,47")))))
    s.append(point(x, 0, ORANGE, 2.8))
    s.append(r"\node[anchor=north,text=otInk,inner sep=1.5pt] at (%s,-.17) {$8{,}46$};" % f(X(F("8,46")) - .15))
    s.append(r"\node[anchor=north,text=otInk,inner sep=1.5pt] at (%s,-.17) {$8{,}47$};" % f(X(F("8,47")) + .15))
    s.append(dessus_haut(x, 0, r"$8{,}463$", "otOrange!85!black", h=.5))
    s.append(accolade(X(F("8,4")), X(F("8,5")), 1.25, r"au dixième : $8{,}4 < 8{,}463 < 8{,}5$", "otNavy"))
    s.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.75) {au centième : $8{,}46 < 8{,}463 < 8{,}47$};" % f(X(F("8,45"))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_encadrer"] = cours_encadrer()


# 5. arrondi au dixième de 3,47
def figure_arrondi(a, v, U=58, lab_point=None, conclusion=None, d_gauche=None, d_droite=None):
    a = F(a)
    b = a + Fr(1, 10)
    m = a + Fr(5, 100)
    c, X = droite(a, b, U, Fr(1, 100), labels=[a, b])
    xv, xm = X(F(v)), X(m)
    s = [r"\begin{tikzpicture}", c]
    # milieu
    s.append(r"\draw[otOrange,line width=.9pt,dash pattern=on 3pt off 2pt] (%s,-.15) -- (%s,1.55);" % (f(xm), f(xm)))
    s.append(r"\node[anchor=south,petit,text=otOrange!85!black,inner sep=1.5pt] at (%s,1.55) {milieu : $%s$};" % (f(xm), nb(m)))
    s.append(point(xv, 0, VERT, 2.9))
    s.append(r"\node[anchor=north,text=otGreenDark,inner sep=1.5pt] at (%s,-.17) {%s};" % (f(xv), lab_point or "$%s$" % nb(F(v))))
    if d_gauche:
        s.append(r"\draw[cote] (%s,.5) -- (%s,.5);" % (f(X(a)), f(xv)))
        s.append(r"\node[anchor=south west,petit,text=otInk,inner sep=1.2pt] at (%s,.57) {%s};" % (f(X(a) + .08), d_gauche))
        s.append(r"\draw[cote,otGreenDark] (%s,1.05) -- (%s,1.05);" % (f(xv), f(X(b))))
        s.append(r"\node[anchor=south,petit,text=otGreenDark,inner sep=1.2pt] at (%s,1.22) {%s};" % (f((X(b) + xv) / 2), d_droite))
        for xx, hh in ((X(a), .62), (xv, 1.17), (X(b), 1.17)):
            s.append(r"\draw[otMuted!70,line width=.4pt] (%s,.14) -- (%s,%s);" % (f(xx), f(xx), f(hh)))
    if conclusion:
        s.append(r"\node[anchor=north,text=otInk,align=center] at (%s,-.75) {%s};" % (f(xm), conclusion))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_arrondi"] = figure_arrondi(
    "3,4", "3,47", d_gauche=r"$7$ centièmes", d_droite=r"$3$ centièmes",
    conclusion=r"$3{,}47$ est plus proche de $3{,}5$ :\\son arrondi au dixième est $3{,}5$.")


# ===================================================================== EXERCICES
# 3209 : lire et placer en dixièmes (0 à 2)
def ex3209(corrige):
    c, X = droite(0, 2, 2.9, Fr(1, 10), labels=[0, 1, 2], moyens=[Fr(1, 2), Fr(3, 2)], origine=True)
    s = [r"\begin{tikzpicture}", c]
    lus = (("A", "0,4"), ("B", "1,3"), ("C", "1,8"))
    for nm, v in lus:
        s.append(point(X(F(v)), 0, NAVY))
        s.append(dessus(X(F(v)), 0, r"$%s$" % nm, NAVY))
        if corrige:
            s.append(r"\node[anchor=north,text=otGreenDark,inner sep=1.5pt] at (%s,-.17) {$%s$};" % (f(X(F(v))), nb(F(v))))
    s.append(r"\node[anchor=north,petit,text=otMuted] at (%s,-.55) {$O$};" % f(X(0)))
    if corrige:
        for nm, v in (("D", "0,9"), ("E", "1,5"), ("F", "1,05")):
            s.append(point(X(F(v)), 0, VERT, 2.9))
            s.append(dessus(X(F(v)), 0, r"$%s$" % nm, VERT))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3209_enonce"] = ex3209(False)
FIGURES["ex3209_corrige"] = ex3209(True)


# 3210 : placer 2,15 et 2,5 (demi-droite de 2 à 3 en dixièmes)
def ex3210(corrige):
    c, X = droite(2, 3, 5.8, Fr(1, 10), labels=[2, 3], moyens=[F("2,5")])
    s = [r"\begin{tikzpicture}", c]
    if corrige:
        for v in ("2,15", "2,5"):
            s.append(point(X(F(v)), 0, VERT, 2.9))
            s.append(dessus(X(F(v)), 0, r"$%s$" % nb(F(v)), VERT))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3210_enonce"] = ex3210(False)
FIGURES["ex3210_corrige"] = ex3210(True)


# 3213 : arrondi au dixième de 4,738
FIGURES["ex3213_corrige"] = figure_arrondi(
    "4,7", "4,738", d_gauche=r"$38$ millièmes", d_droite=r"$62$ millièmes",
    conclusion=r"$4{,}738$ est à gauche du milieu :\\il est plus proche de $4{,}7$.")


# 3216 : zoom de [5 ; 6] sur [5,3 ; 5,4]
def ex3216(corrige):
    lab_h = [Fr(50 + k, 10) for k in range(11)]
    lab_b = [F("5,3"), F("5,4")]
    if corrige:
        haut = [("5,37", r"$M$", NAVY)]
        bas = [("5,37", r"$M$", NAVY, False), ("5,31", r"$K$", NAVY, False),
               ("5,35", r"$N$", VERT, True), ("5,325", r"$R$", VERT, True)]
    else:
        haut = [("5,37", r"$M$", NAVY)]
        bas = [("5,37", r"$M$", NAVY, False), ("5,31", r"$K$", NAVY, False)]
    c, Xh, Xb = zoom(5, 6, "5,3", 5.8, 58, haut, bas, lab_h, lab_b, moy_bas=[F("5,35")])
    s = [r"\begin{tikzpicture}", c]
    if corrige:
        for v in ("5,31", "5,37"):
            s.append(r"\node[anchor=north,text=otGreenDark,inner sep=1.5pt] at (%s,-.17) {$%s$};" % (f(Xb(F(v))), nb(F(v))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3216_enonce"] = ex3216(False)
FIGURES["ex3216_corrige"] = ex3216(True)


# 3211 : encadrements de 23,186 (zoom de [23 ; 24] sur [23,1 ; 23,2])
def ex3211():
    lab_h = [Fr(230 + k, 10) for k in range(0, 11, 2)]
    lab_b = [F("23,1"), F("23,15"), F("23,2")]
    c, Xh, Xb = zoom(23, 24, "23,1", 5.8, 58, [("23,186", "", ORANGE)], [("23,186", "", ORANGE, False)], lab_h, lab_b)
    s = [r"\begin{tikzpicture}", c]
    s.append(r"\draw[otGreenDark,line width=2.2pt,opacity=.85] (%s,0) -- (%s,0);" % (f(Xb(F("23,18"))), f(Xb(F("23,19")))))
    s.append(point(Xb(F("23,186")), 0, ORANGE, 2.8))
    s.append(r"\node[anchor=south east,text=otOrange!85!black,inner sep=1.5pt] at (%s,.1) {$23{,}186$};" % f(Xb(F("23,186")) - .05))
    s.append(r"\node[anchor=north,text=otGreenDark,align=center] at (%s,-.62) {au centième :\\$23{,}18 < 23{,}186 < 23{,}19$};" % f(Xb(F("23,15"))))
    s.append(r"\draw[accol,%s] (%s,2.82) -- (%s,2.82);" % (VERT, f(Xh(F("23,1"))), f(Xh(F("23,2")))))
    s.append(r"\node[anchor=south west,text=%s,inner sep=1.5pt] at (%s,3.02) {au dixième : $23{,}1 < 23{,}186 < 23{,}2$};" % (VERT, f(Xh(23) - .1)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3211_corrige"] = ex3211()


# 3212 : le nombre mystère, entre 6,4 et 6,6
def ex3212():
    c, X = droite("6,4", "6,6", 29, Fr(1, 100), labels=[F("6,4"), F("6,45"), F("6,5"), F("6,55"), F("6,6")])
    s = [r"\begin{tikzpicture}", c]
    # indice 2 : arrondi au dixième 6,5 -> de 6,45 (compris) à 6,55 (exclu)
    y2, y3 = 1.0, .55
    s.append(r"\draw[otOrange,line width=2.4pt] (%s,%s) -- (%s,%s);" % (f(X(F("6,45"))), f(y2), f(X(F("6,54"))), f(y2)))
    s.append(r"\node[anchor=south,petit,text=otOrange!85!black,inner sep=1.5pt] at (%s,%s) {indice 2 : de $6{,}45$ à $6{,}54$};" % (f(X(F("6,495"))), f(y2 + .08)))
    # indice 3 : en plus, inférieur à 6,5
    s.append(r"\draw[otGreenDark,line width=2.4pt] (%s,%s) -- (%s,%s);" % (f(X(F("6,45"))), f(y3), f(X(F("6,49"))), f(y3)))
    s.append(r"\node[anchor=west,petit,text=otGreenDark,inner sep=1.5pt] at (%s,%s) {indice 3 : jusqu'à $6{,}49$};" % (f(X(F("6,49")) + .25), f(y3)))
    for v in ("6,46", "6,48"):
        s.append(point(X(F(v)), 0, VERT if v == "6,48" else "otMuted", 2.9 if v == "6,48" else 2.3))
    s.append(r"\node[anchor=north,text=otGreenDark,inner sep=1.5pt] at (%s,-.62) {$6{,}48$};" % f(X(F("6,48"))))
    s.append(r"\draw[otGreenDark!70,line width=.4pt] (%s,-.14) -- (%s,-.62);" % (f(X(F("6,48"))), f(X(F("6,48")))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3212_corrige"] = ex3212()


# 3229 : le ruban du saut en longueur, de 3,30 m à 3,50 m en centièmes
def ex3229(corrige):
    c, X = droite("3,3", "3,5", 29, Fr(1, 100), labels=[F("3,3"), F("3,4"), F("3,5")], moyens=[F("3,35"), F("3,45")])
    s = [r"\begin{tikzpicture}", c]
    for nm, v in (("L", "3,36"), ("N", "3,47")):
        s.append(point(X(F(v)), 0, NAVY))
        if corrige:
            s.append(dessus(X(F(v)), 0, r"$%s$ : \textcolor{otGreenDark}{$%s$ m}" % (nm, nb(F(v))), NAVY))
        else:
            s.append(dessus(X(F(v)), 0, r"$%s$" % nm, NAVY))
    s.append(r"\node[anchor=west,petit,text=otMuted] at (%s,0) {m};" % f(X(F("3,5")) + .55))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3229_enonce"] = ex3229(False)
FIGURES["ex3229_corrige"] = ex3229(True)
