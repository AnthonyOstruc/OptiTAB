# -*- coding: utf-8 -*-
"""Figures de la notion 265 (5e : fractions, quotients et comparaisons), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Barres et disques partagés, droites graduées. Convention : énoncé = figure seule
(parts à colorier laissées blanches) ; corrigé = parts et points de la réponse en
vert (otGreenDark / otGreen).
Outils repris de la notion 4e 251 (fractions).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradF/.style={otMuted,line width=.8pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  part/.style={draw=otNavy,line width=.7pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  accolV/.style={otGreenDark,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
}
"""


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


BLEU = "otNavy!28"
VERT = "otGreen!55"
ORANGE = "otOrange!55"
VERTF = "otGreenDark"
ORF = "otOrange!85!black"


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


# ================================================================== outils
def disque(cx, cy, r, couleurs):
    """Disque partagé en len(couleurs) secteurs égaux (sens horaire depuis le haut)."""
    n = len(couleurs)
    s = []
    for i, c in enumerate(couleurs):
        a0 = 90 - 360 * i / n
        a1 = 90 - 360 * (i + 1) / n
        s.append(r"\filldraw[fill=%s,part] (%s,%s) -- ++(%s:%s) arc[start angle=%s,end angle=%s,radius=%s] -- cycle;"
                 % (c or "white", f(cx), f(cy), f(a0), f(r), f(a0), f(a1), f(r)))
    return "\n".join(s)


def barre(x, y, w, h, n, couleurs, trait="part"):
    """Barre de n parts égales ; couleurs : liste (None = blanc)."""
    s = []
    d = w / n
    for i in range(n):
        c = couleurs[i] if i < len(couleurs) and couleurs[i] else "white"
        s.append(r"\filldraw[fill=%s,%s] (%s,%s) rectangle (%s,%s);" % (c, trait, f(x + i * d), f(y), f(x + (i + 1) * d), f(y + h)))
    return "\n".join(s)


def accolade_dessous(x0, x1, y, texte, coul="otInk", dy=.12, style="accol"):
    return (r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x1), f(y - dy), f(x0), f(y - dy))
            + "\n" + r"\node[anchor=north,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y - dy - .2), texte))


def accolade_dessus(x0, x1, y, texte, coul="otInk", dy=.12, style="accol"):
    return (r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x0), f(y + dy), f(x1), f(y + dy))
            + "\n" + r"\node[anchor=south,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y + dy + .2), texte))


def point(x, y=0, coul="otNavy"):
    return r"\fill[%s] (%s,%s) circle (2.4pt);" % (coul, f(x), f(y))


def droite(den, kmax, U, pts, entiers, y=0.0, prolonge=.5):
    """Droite graduée de 0 à kmax/den, unité U cm partagée en den.

    pts = [(k, texte_dessus, texte_dessous, couleur, hauteur)] : point d'abscisse k/den.
    entiers = valeurs entières à écrire sous l'axe.
    """
    X = lambda k: U * k / den
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(-.3), f(y), f(X(kmax) + prolonge), f(y))]
    for k in range(kmax + 1):
        if k % den == 0:
            s.append(r"\draw[gradF] (%s,%s) -- (%s,%s);" % (f(X(k)), f(y - .13), f(X(k)), f(y + .13)))
        else:
            s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(k)), f(y - .08), f(X(k)), f(y + .08)))
    for e in entiers:
        s.append(r"\node[gradTexte] at (%s,%s) {$%d$};" % (f(X(e * den)), f(y - .2), e))
    for k, haut_txt, bas_txt, c, h in pts:
        s.append(point(X(k), y, c))
        if haut_txt:
            if h > .3:
                s.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (c, f(X(k)), f(y + .1), f(X(k)), f(y + h - .05)))
            s.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (c, f(X(k)), f(y + h), haut_txt))
        if bas_txt:
            s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (c, f(X(k)), f(y - .2), bas_txt))
    return "\n".join(s)


def fr(a, b):
    return r"$\dfrac{%d}{%d}$" % (a, b)


FIGURES = {}

# ================================================================== COURS
# 1. Une fraction de l'unité ; une fraction supérieure à 1
_s = [barre(0, 0, 3.4, .65, 5, [BLEU] * 3)]
_s.append(r"\node[anchor=west,text=otInk] at (3.65,.325) {%s de la barre};" % fr(3, 5))
_s.append(disque(.62, -1.3, .62, [BLEU] * 4))
_s.append(disque(2.1, -1.3, .62, [BLEU] * 3 + [None]))
_s.append(r"\node[anchor=west,text=otInk] at (2.95,-1.3) {%s d'un disque};" % fr(7, 4))
FIGURES["cours_unite"] = tikz(_s)

# 2. Deux crêpes partagées entre cinq personnes
_s = [disque(.8, 0, .75, [VERT] + [None] * 4), disque(2.7, 0, .75, [VERT] + [None] * 4)]
_s.append(r"\node[anchor=north,text=%s,align=center] at (1.75,-.95) {part d'une personne :\\$2$ cinquièmes, soit %s de crêpe};"
          % (VERTF, fr(2, 5)))
FIGURES["cours_crepes"] = tikz(_s)

# 3. Fractions égales : 2/3 = 4/6 = 8/12
_s = []
for i, (n, k, lab) in enumerate([(3, 2, fr(2, 3)), (6, 4, fr(4, 6)), (12, 8, fr(8, 12))]):
    y = -1.05 * i
    _s.append(barre(0, y, 5.4, .6, n, [BLEU] * k))
    _s.append(r"\node[anchor=east,text=otInk] at (-.2,%s) {%s};" % (f(y + .3), lab))
_s.append(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt] (3.6,-2.35) -- (3.6,.85);")
FIGURES["cours_egales"] = tikz(_s)

# 4. Droite graduée en tiers : 2/3, 5/3, 7/3
FIGURES["cours_droite"] = tikz([droite(3, 9, 2.0,
                                       [(2, fr(2, 3), "", "otNavy", .2),
                                        (5, fr(5, 3), "", "otNavy", .2),
                                        (7, fr(7, 3), "", "otNavy", .2)],
                                       [0, 1, 2, 3])])

# 5. Prendre 3/5 de 40 €
_s = []
w = 1.2
_s.append(barre(0, 0, 5 * w, .7, 5, [VERT] * 3))
for i in range(5):
    _s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.1) {$8$ €};" % f(w * i + w / 2))
_s.append(accolade_dessus(0, 5 * w, .7, r"la somme : $40$ €"))
_s.append(accolade_dessous(0, 3 * w, -.55, r"%s de $40$ € : $3 \times 8 = 24$ €" % fr(3, 5), VERTF, style="accolV"))
FIGURES["cours_quantite"] = tikz(_s)


# ================================================================== 2789 : fraction, partage et quotient
_s = []
_s.append(r"\node[anchor=south,text=otNavy,font=\bfseries] at (.62,.8) {a)};")
_s.append(disque(.62, 0, .62, [BLEU] * 3 + [None] * 5))
_s.append(r"\node[anchor=south,text=otNavy,font=\bfseries] at (2.55,.8) {b)};")
_s.append(barre(1.6, -.27, 1.9, .54, 5, [BLEU] * 4))
_s.append(r"\node[anchor=south,text=otNavy,font=\bfseries] at (5.06,.8) {c)};")
_s.append(disque(4.34, 0, .6, [BLEU] * 4))
_s.append(disque(5.78, 0, .6, [BLEU] + [None] * 3))
FIGURES["lire_enonce"] = tikz(_s)


def tablettes(corrige):
    s = []
    for i in range(2):
        y = -1.0 * i
        cols = [VERT] if corrige else []
        s.append(barre(0, y, 3.9, .65, 3, cols))
        s.append(r"\node[anchor=east,text=otInk] at (-.2,%s) {tablette %d};" % (f(y + .325), i + 1))
    if corrige:
        s.append(r"\node[anchor=north west,text=%s,align=left] at (0,-1.25) {part d'un enfant : $2$ tiers,\\soit %s de tablette};"
                 % (VERTF, fr(2, 3)))
    return tikz(s)


FIGURES["tablettes_enonce"] = tablettes(False)
FIGURES["tablettes_corrige"] = tablettes(True)


# ================================================================== 2803 : la réserve de jus (24 L)
def jus(corrige):
    s = []
    w = 1.4
    s.append(barre(0, 0, 4 * w, .7, 4, [VERT] * 3 if corrige else []))
    s.append(accolade_dessus(0, 4 * w, .7, r"la réserve : $24$ L"))
    if corrige:
        for i in range(4):
            s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.1) {$6$ L};" % f(w * i + w / 2))
        s.append(accolade_dessous(0, 3 * w, -.55, r"%s de $24$ L : $3 \times 6 = 18$ L" % fr(3, 4), VERTF, style="accolV"))
    return tikz(s)


FIGURES["jus_enonce"] = jus(False)
FIGURES["jus_corrige"] = jus(True)


# ================================================================== 2794 : 3/4 = 6/8
def egales(corrige):
    s = []
    W = 4.8
    s.append(barre(0, 0, W, .6, 4, [BLEU] * 3))
    s.append(barre(0, -1.05, W, .6, 8, [VERT] * 6 if corrige else []))
    if corrige:
        s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {%s};" % fr(3, 4))
        s.append(r"\node[anchor=east,text=%s] at (-.2,-.75) {%s};" % (VERTF, fr(6, 8)))
        s.append(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt] (%s,-1.3) -- (%s,.85);" % (f(W * 3 / 4), f(W * 3 / 4)))
    else:
        s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {barre A};")
        s.append(r"\node[anchor=east,text=otInk] at (-.2,-.75) {barre B};")
    return tikz(s)


FIGURES["egales_enonce"] = egales(False)
FIGURES["egales_corrige"] = egales(True)


# ================================================================== 2790 : rubans 3/8 et 5/16
def rubans(corrige):
    s = []
    W = 5.2
    s.append(barre(0, 0, W, .6, 8, [VERT] * 3 if corrige else []))
    if corrige:
        for i in range(8):
            x = W / 8 * (i + .5)
            s.append(r"\draw[otNavy!45,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (%s,.06) -- (%s,.54);" % (f(x), f(x)))
    s.append(barre(0, -1.0, W, .6, 16, [VERT] * 5 if corrige else []))
    s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {Alice};")
    s.append(r"\node[anchor=east,text=otInk] at (-.2,-.7) {Bilal};")
    if corrige:
        s.append(r"\node[anchor=south,text=%s] at (%s,.68) {%s};" % (VERTF, f(W * 3 / 16), r"$\dfrac{3}{8} = \dfrac{6}{16}$"))
        s.append(accolade_dessous(0, W * 5 / 16, -1.0, fr(5, 16), VERTF, style="accolV"))
    return tikz(s)


FIGURES["rubans_enonce"] = rubans(False)
FIGURES["rubans_corrige"] = rubans(True)


# ================================================================== 2800 : ranger sur une droite en seizièmes
FIGURES["ranger_corrige"] = tikz([droite(16, 20, 4.8,
                                         [(7, fr(7, 16), "", VERTF, .2),
                                          (8, fr(1, 2), "", VERTF, 1.15),
                                          (10, fr(5, 8), "", VERTF, .2),
                                          (12, fr(3, 4), "", VERTF, .2),
                                          (18, fr(9, 8), "", VERTF, .2)],
                                         [0, 1], prolonge=.45)])


# ================================================================== 2801 : droite en quarts de 0 à 3
def droite_quarts(corrige):
    pts = [(3, "$A$", fr(3, 4) if corrige else "", "otNavy", .2),
           (6, "$B$", fr(6, 4) if corrige else "", "otNavy", .2),
           (9, "$C$", fr(9, 4) if corrige else "", "otNavy", .2)]
    if corrige:
        # lettres A, B, C en bleu (données, redessinées ci-dessous), abscisses lues en vert
        pts = [(3, "", fr(3, 4), VERTF, .2), (6, "", fr(6, 4), VERTF, .2), (9, "", fr(9, 4), VERTF, .2),
               (5, "$D$", fr(5, 4), VERTF, .2), (11, "$E$", fr(11, 4), VERTF, .2), (2, "$F$", fr(2, 4), VERTF, .2)]
    U = 2.0
    s = [droite(4, 12, U, pts, [0, 1, 2, 3])]
    if corrige:
        for k, lettre in ((3, "A"), (6, "B"), (9, "C")):
            s.append(point(U * k / 4, 0, "otNavy"))
            s.append(r"\node[anchor=south,text=otNavy,inner sep=1.5pt] at (%s,.2) {$%s$};" % (f(U * k / 4), lettre))
    return tikz(s)


FIGURES["droite_enonce"] = droite_quarts(False)
FIGURES["droite_corrige"] = droite_quarts(True)


# ================================================================== 2793 : pizzas des tables A et B
def pizzas(corrige):
    s = []
    r = .55
    s.append(r"\node[anchor=west,text=otNavy,font=\bfseries] at (0,.9) {Table A : $3$ pizzas pour $4$ enfants};")
    for i in range(3):
        s.append(disque(.6 + 1.25 * i, 0, r, ([VERT] if corrige else []) + [None] * (4 - (1 if corrige else 0))))
    s.append(r"\node[anchor=west,text=otNavy,font=\bfseries] at (0,-1.1) {Table B : $5$ pizzas pour $8$ enfants};")
    for i in range(5):
        s.append(disque(.6 + 1.25 * i, -2.0, r, ([VERT] if corrige else []) + [None] * (8 - (1 if corrige else 0))))
    if corrige:
        s.append(r"\node[anchor=west,text=%s,align=left] at (3.95,0) {un enfant :\\$3$ quarts $=$ %s};" % (VERTF, fr(3, 4)))
        s.append(r"\node[anchor=north west,text=%s] at (0,-2.7) {un enfant : $5$ huitièmes $=$ %s de pizza};" % (VERTF, fr(5, 8)))
    return tikz(s)


FIGURES["pizzas_enonce"] = pizzas(False)
FIGURES["pizzas_corrige"] = pizzas(True)


# ================================================================== 2808 : deux gourdes (50 cL et 100 cL)
def gourdes(corrige):
    s = []
    u = .052  # cm par cL
    s.append(barre(0, 0, 50 * u, .6, 5, [VERT] * 4 if corrige else []))
    yb = -2.5 if corrige else -1.55   # place de l'accolade d'Alice dans le corrigé
    s.append(barre(0, yb, 100 * u, .6, 10, [VERT] * 7 if corrige else []))
    s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {Alice};")
    s.append(r"\node[anchor=east,text=otInk] at (-.2,%s) {Bilal};" % f(yb + .3))
    s.append(r"\node[anchor=west,text=otMuted] at (%s,.3) {gourde de $50$ cL};" % f(50 * u + .2))
    s.append(r"\node[anchor=south east,text=otMuted,inner sep=1pt] at (%s,%s) {gourde de $100$ cL};" % (f(100 * u), f(yb + .7)))
    if corrige:
        s.append(accolade_dessous(0, 40 * u, 0, r"%s de $50$ cL $= 40$ cL" % fr(4, 5), VERTF, style="accolV"))
        s.append(accolade_dessous(0, 70 * u, yb, r"%s de $100$ cL $= 70$ cL" % fr(7, 10), VERTF, style="accolV"))
    return tikz(s)


FIGURES["gourdes_enonce"] = gourdes(False)
FIGURES["gourdes_corrige"] = gourdes(True)


# ================================================================== 2807 : la réserve de 150 L
def reserve(corrige):
    s = []
    w = 1.25
    cols = [VERT, VERT, ORANGE] if corrige else []
    s.append(barre(0, 0, 5 * w, .7, 5, cols))
    s.append(accolade_dessus(0, 5 * w, .7, r"la réserve : $150$ L"))
    if corrige:
        for i in range(5):
            s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.1) {$30$ L};" % f(w * i + w / 2))
        s.append(accolade_dessous(0, 2 * w, -.55, r"jour 1\\$60$ L", VERTF, style="accolV"))
        s.append(accolade_dessous(2 * w, 3 * w, -.55, r"jour 2\\$30$ L", ORF))
        s.append(accolade_dessous(3 * w, 5 * w, -.55, r"reste\\$60$ L", "otNavy"))
    return tikz(s)


FIGURES["reserve_enonce"] = reserve(False)
FIGURES["reserve_corrige"] = reserve(True)


# ================================================================== 2809 : parcours du cross (0 à 2 km)
def cross(corrige):
    U = 2.6
    pts = []
    if corrige:
        pts = [(5, "$R$", fr(5, 4), VERTF, .2), (6, "$P$", fr(6, 4), VERTF, .2)]
    s = [droite(4, 8, U, pts, [0, 1, 2], prolonge=.55)]
    s.append(r"\node[anchor=south,text=otNavy,inner sep=1.5pt] at (0,.2) {départ};")
    s.append(r"\node[anchor=south,text=otNavy,inner sep=1.5pt] at (%s,.2) {arrivée};" % f(2 * U))
    s.append(r"\node[anchor=north west,text=otMuted,font=\otRegular\fontsize{9}{10}\selectfont] at (%s,-.2) {km};" % f(2 * U + .3))
    return tikz(s)


FIGURES["cross_enonce"] = cross(False)
FIGURES["cross_corrige"] = cross(True)
