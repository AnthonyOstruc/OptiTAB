# -*- coding: utf-8 -*-
"""Figures de la notion 264 (5e : additionner et soustraire des relatifs), style des livres.

Compilées par outils/figures_livre.py. Droites graduées et déplacements, thermomètres,
altitudes, pyramides additives, piste de jeu. Énoncé : le départ seulement ; corrigé :
déplacements et arrivée en vert foncé (otGreenDark). Outils repris de la notion 249 (4e).
Toutes les valeurs dessinées sont calculées ici et revérifiées par verif_264.py.
"""
from fractions import Fraction as Fr

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
  liaison/.style={otGreenDark!70,line width=.6pt,dash pattern=on 2pt off 1.6pt},
  case/.style={draw=otNavy,line width=.8pt},
  accolV/.style={otGreenDark,line width=.7pt,decorate,decoration={brace,amplitude=4pt}},
}
"""

VERT = "otGreenDark"
ORANGE = "otOrange!85!black"
BLEU = "otNavy"


def f(v):
    return ("%.4f" % float(v)).rstrip("0").rstrip(".")


def nb(v):
    """Nombre relatif écrit en LaTeX (virgule décimale, signe moins)."""
    s = ("%.2f" % float(v)).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s.replace(".", "{,}")


def sg(v):
    """Nombre relatif avec son signe : +5, -3."""
    return ("+" + nb(v)) if v > 0 else nb(v)


# ===================================================================== outils communs
def droite(a, b, U, y=0.0, x0=0.0):
    """Droite graduée horizontale de a à b (entiers), U cm par unité. Renvoie (code, X)."""
    X = lambda v: x0 + U * (v - a)
    s = [r"\draw[axe] (%s,%s) -- (%s,%s);" % (f(X(a) - .3), f(y), f(X(b) + .45), f(y))]
    for k in range(a, b + 1):
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(k)), f(y - .08), f(X(k)), f(y + .08)))
        s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X(k)), f(y - .16), nb(k)))
    return "\n".join(s), X


def point(x, y, coul=BLEU, r=2.6):
    return r"\fill[%s] (%s,%s) circle (%spt);" % (coul, f(x), f(y), f(r))


def arc(x1, x2, y, h, style, texte, coul):
    """Flèche courbe de x1 vers x2 au-dessus de la droite, texte au sommet."""
    xm = (x1 + x2) / 2
    s = [r"\draw[%s] (%s,%s) .. controls (%s,%s) and (%s,%s) .. (%s,%s);"
         % (style, f(x1), f(y + .12), f(x1), f(y + h * 1.33), f(x2), f(y + h * 1.33), f(x2), f(y + .12))]
    s.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(xm), f(y + h + .08), texte))
    return "\n".join(s)


FIGURES = {}

# ===================================================================== cours 1 / fiche 1 : additions
def cours_addition():
    s = [r"\begin{tikzpicture}"]
    c1, X = droite(-5, 5, .6, y=0)
    s.append(c1)
    s.append(arc(X(-2), X(3), 0, .55, "deplV", r"$+5$", VERT))
    s.append(point(X(-2), 0, BLEU))
    s.append(point(X(3), 0, VERT, 2.8))
    s.append(r"\node[anchor=south west,text=otInk] at (%s,1.0) {$(-2) + (+5) = 3$};" % f(X(-5) - .3))
    y2 = -2.2
    c2, _ = droite(-5, 5, .6, y=y2)
    s.append(c2)
    s.append(arc(X(1), X(-3), y2, .55, "deplO", r"$-4$", ORANGE))
    s.append(point(X(1), y2, BLEU))
    s.append(point(X(-3), y2, ORANGE, 2.8))
    s.append(r"\node[anchor=south east,text=otInk] at (%s,%s) {$(+1) + (-4) = -3$};" % (f(X(5) + .45), f(y2 + 1.0)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_addition"] = cours_addition()


# ===================================================================== cours 2 : soustractions
def cours_soustraction():
    s = [r"\begin{tikzpicture}"]
    c1, X = droite(-6, 6, .52, y=0)
    s.append(c1)
    s.append(arc(X(2), X(5), 0, .5, "deplV", r"$+3$", VERT))
    s.append(point(X(2), 0, BLEU))
    s.append(point(X(5), 0, VERT, 2.8))
    s.append(r"\node[anchor=south west,text=otInk] at (%s,.95) {$2 - (-3) = 2 + (+3) = 5$};" % f(X(-6) - .3))
    y2 = -2.2
    c2, _ = droite(-6, 6, .52, y=y2)
    s.append(c2)
    s.append(arc(X(-1), X(-5), y2, .5, "deplO", r"$-4$", ORANGE))
    s.append(point(X(-1), y2, BLEU))
    s.append(point(X(-5), y2, ORANGE, 2.8))
    s.append(r"\node[anchor=south east,text=otInk] at (%s,%s) {$-1 - (+4) = -1 + (-4) = -5$};" % (f(X(6) + .45), f(y2 + .95)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_soustraction"] = cours_soustraction()


# ===================================================================== thermomètres
def thermometre(tmin, tmax, U, marques, pas_label=2, x=0.0, largeur=.42, extra=None):
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
    for t, txt, c in marques:
        s.append(r"\draw[%s,line width=1.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 + .05), f(Y(t)), f(x + w / 2 - .05), f(Y(t))))
        if txt:
            s.append(r"\draw[%s,line width=.6pt] (%s,%s) -- (%s,%s);" % (c, f(x - w / 2 - .12), f(Y(t)), f(x - w / 2 - .42), f(Y(t))))
            s.append(r"\node[anchor=east,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (c, f(x - w / 2 - .45), f(Y(t)), txt))
    if extra:
        s.append(extra(Y))
    return "\n".join(s)


def fleche_v(x, y1, y2, style="deplV"):
    """Flèche verticale de y1 vers y2, avec deux petits traits aux extrémités."""
    coul = VERT if style == "deplV" else ORANGE
    return (r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x), f(y1), f(x), f(y2))
            + "\n" + r"\draw[%s,line width=.5pt] (%s,%s) -- (%s,%s);" % (coul, f(x - .1), f(y1), f(x + .1), f(y1)))


# cours : de -7 °C (7 h) à 5 °C (14 h), puis -1 °C (22 h)
COURS_THERMO = [(-7, "7 h"), (5, "14 h"), (-1, "22 h")]


def cours_thermometre():
    s = [r"\begin{tikzpicture}"]
    (t0, h0), (t1, h1), (t2, h2) = COURS_THERMO

    def fl(Y):
        out = [fleche_v(1.55, Y(t0), Y(t1)),
               r"\node[anchor=west,text=%s] at (1.68,%s) {$%s$ °C};" % (VERT, f((Y(t0) + Y(t1)) / 2), sg(t1 - t0)),
               fleche_v(2.95, Y(t1), Y(t2), "deplO"),
               r"\node[anchor=west,text=%s] at (3.08,%s) {$%s$ °C};" % (ORANGE, f((Y(t1) + Y(t2)) / 2), sg(t2 - t1))]
        return "\n".join(out)

    marques = [(t0, r"%s : $%s$ °C" % (h0, nb(t0)), BLEU), (t1, r"%s : $%s$ °C" % (h1, nb(t1)), VERT),
               (t2, r"%s : $%s$ °C" % (h2, nb(t2)), ORANGE)]
    s.append(thermometre(-8, 8, .26, marques, extra=fl))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_thermometre"] = cours_thermometre()


# ===================================================================== altitudes
def ic_oiseau(x, y, c):
    return (r"\draw[%s,line width=1pt,line cap=round] (%s,%s) .. controls (%s,%s) .. (%s,%s) .. controls (%s,%s) .. (%s,%s);"
            % (c, f(x - .28), f(y + .06), f(x - .14), f(y + .16), f(x), f(y - .02), f(x + .14), f(y + .16), f(x + .28), f(y + .06)))


def ic_poisson(x, y, c):
    return (r"\fill[%s] (%s,%s) ellipse (.24 and .1);" % (c, f(x), f(y))
            + "\n" + r"\fill[%s] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
            % (c, f(x + .2), f(y), f(x + .4), f(y + .11), f(x + .4), f(y - .11)))


def ic_sousmarin(x, y, c):
    return (r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) ellipse (.42 and .12);" % (c, c, f(x), f(y))
            + "\n" + r"\filldraw[fill=%s!80,draw=%s,line width=.6pt] (%s,%s) rectangle (%s,%s);"
            % (c, c, f(x - .08), f(y + .09), f(x + .1), f(y + .23)))


def axe_altitudes(amin, amax, pas, U, mer_x, titre=r"altitude (m)"):
    Y = lambda a: U * (a - amin)
    s = [r"\fill[otSky] (.12,%s) rectangle (%s,%s);" % (f(Y(amin)), f(mer_x), f(Y(0))),
         r"\draw[otNavy!55,line width=.9pt] (.12,%s) -- (%s,%s);" % (f(Y(0)), f(mer_x), f(Y(0))),
         r"\draw[axeV] (0,%s) -- (0,%s);" % (f(Y(amin) - .1), f(Y(amax) + .45)),
         r"\node[anchor=south,petit,text=otMuted] at (0,%s) {%s};" % (f(Y(amax) + .5), titre)]
    a = amin
    while a <= amax:
        s.append(r"\draw[grad] (-.08,%s) -- (.08,%s);" % (f(Y(a)), f(Y(a))))
        s.append(r"\node[gradTexteG] at (-.14,%s) {$%s$};" % (f(Y(a)), nb(a)))
        a += pas
    s.append(r"\node[anchor=north east,petit,text=otNavy!80,inner sep=2pt] at (%s,%s) {niveau de la mer};" % (f(mer_x - .05), f(Y(0) - .04)))
    return "\n".join(s), Y


COURS_MOUETTE, COURS_POISSON = 12, -9


def cours_altitudes():
    s = [r"\begin{tikzpicture}"]
    code, Y = axe_altitudes(-15, 15, 5, .12, 3.7)
    s.append(code)
    s.append(ic_oiseau(.9, Y(COURS_MOUETTE), BLEU))
    s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (1.35,%s) {mouette : $%s$ m};" % (BLEU, f(Y(COURS_MOUETTE)), nb(COURS_MOUETTE)))
    s.append(ic_poisson(.8, Y(COURS_POISSON), BLEU))
    s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (1.35,%s) {poisson : $%s$ m};" % (BLEU, f(Y(COURS_POISSON)), nb(COURS_POISSON)))
    xe = 4.4
    s.append(r"\draw[cote,%s] (%s,%s) -- (%s,%s);" % (VERT, f(xe), f(Y(COURS_MOUETTE)), f(xe), f(Y(COURS_POISSON))))
    s.append(r"\draw[otMuted!60,line width=.4pt,dash pattern=on 2pt off 1.6pt] (3.75,%s) -- (%s,%s) (3.75,%s) -- (%s,%s);"
             % (f(Y(COURS_MOUETTE)), f(xe + .1), f(Y(COURS_MOUETTE)), f(Y(COURS_POISSON)), f(xe + .1), f(Y(COURS_POISSON))))
    s.append(r"\node[anchor=west,text=%s,align=left] at (%s,%s) {écart :\\$%s - (%s)$\\$= %s$ m};"
             % (VERT, f(xe + .15), f((Y(COURS_MOUETTE) + Y(COURS_POISSON)) / 2), nb(COURS_MOUETTE), nb(COURS_POISSON),
                nb(COURS_MOUETTE - COURS_POISSON)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_altitudes"] = cours_altitudes()


# ===================================================================== 2772 : trois additions
EX_ADD = [("a", -3, 5), ("b", 2, -6), ("c", -1, -4)]


def ex_addition(corrige):
    s = [r"\begin{tikzpicture}"]
    dy = 1.95
    for k, (lettre, a, b) in enumerate(EX_ADD):
        y = -k * dy
        c, X = droite(-6, 5, .6, y=y)
        s.append(c)
        if corrige:
            s.append(arc(X(a), X(a + b), y, .45, "deplV", r"$%s$" % sg(b), VERT))
            s.append(point(X(a + b), y, VERT, 2.8))
            s.append(r"\node[anchor=south west,text=%s] at (%s,%s) {%s) $(%s) + (%s) = %s$};"
                     % (VERT, f(X(-6) - .3), f(y + .78), lettre, sg(a), sg(b), nb(a + b)))
        else:
            s.append(r"\node[anchor=south west,text=otInk] at (%s,%s) {%s) $(%s) + (%s)$};"
                     % (f(X(-6) - .3), f(y + .78), lettre, sg(a), sg(b)))
        s.append(point(X(a), y, BLEU))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_addition_enonce"] = ex_addition(False)
FIGURES["ex_addition_corrige"] = ex_addition(True)


# ===================================================================== 2773 : 1 - (-4) et 1 - (+4)
EX_SOUS = [("a", 1, -4), ("b", 1, 4)]


def ex_soustraction(corrige):
    s = [r"\begin{tikzpicture}"]
    dy = 2.0
    for k, (lettre, a, b) in enumerate(EX_SOUS):
        y = -k * dy
        c, X = droite(-5, 7, .55, y=y)
        s.append(c)
        if corrige:
            s.append(arc(X(a), X(a - b), y, .45, "deplV", r"$%s$" % sg(-b), VERT))
            s.append(point(X(a - b), y, VERT, 2.8))
            s.append(r"\node[anchor=south west,text=%s] at (%s,%s) {%s) $%s - (%s) = %s + (%s) = %s$};"
                     % (VERT, f(X(-5) - .3), f(y + .78), lettre, nb(a), sg(b), nb(a), sg(-b), nb(a - b)))
        else:
            s.append(r"\node[anchor=south west,text=otInk] at (%s,%s) {%s) $%s - (%s)$};"
                     % (f(X(-5) - .3), f(y + .78), lettre, nb(a), sg(b)))
        s.append(point(X(a), y, BLEU))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_soustraction_enonce"] = ex_soustraction(False)
FIGURES["ex_soustraction_corrige"] = ex_soustraction(True)


# ===================================================================== 2768 : la journée
J_6H, J_HAUSSE, J_BAISSE, J_NUIT = -4, 7, -5, -6
J_MIDI = J_6H + J_HAUSSE
J_18H = J_MIDI + J_BAISSE


def ex_journee(corrige):
    s = [r"\begin{tikzpicture}"]
    if not corrige:
        s.append(thermometre(-8, 6, .3, [(J_6H, "6 h", BLEU)]))
    else:
        marques = [(J_6H, r"6 h : $%s$ °C" % nb(J_6H), BLEU), (J_MIDI, r"midi : $%s$ °C" % nb(J_MIDI), VERT),
                   (J_18H, r"18 h : $%s$ °C" % nb(J_18H), VERT), (J_NUIT, r"nuit : $%s$ °C" % nb(J_NUIT), VERT)]

        def fl(Y):
            out = []
            for x, t1, t2 in ((1.5, J_6H, J_MIDI), (2.45, J_MIDI, J_18H), (3.4, J_18H, J_NUIT)):
                out.append(fleche_v(x, Y(t1), Y(t2)))
                out.append(r"\node[anchor=west,text=%s] at (%s,%s) {$%s$};" % (VERT, f(x + .1), f((Y(t1) + Y(t2)) / 2), sg(t2 - t1)))
            return "\n".join(out)
        s.append(thermometre(-8, 6, .3, marques, extra=fl))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_journee_enonce"] = ex_journee(False)
FIGURES["ex_journee_corrige"] = ex_journee(True)


# ===================================================================== 2769 : pyramides additives
P1_BASE = [-3, 5, -8, 2]
P2_BASE = [4, None, -7]
P2_DONNE = -2          # case gauche du 2e étage de la pyramide 2


def etages(base):
    rangs = [list(base)]
    while len(rangs[-1]) > 1:
        r = rangs[-1]
        rangs.append([r[i] + r[i + 1] for i in range(len(r) - 1)])
    return rangs


def p2_complete():
    b = P2_DONNE - P2_BASE[0]
    return etages([P2_BASE[0], b, P2_BASE[2]])


def pyramide(x0, titre, cases, w=.92, h=.58):
    """cases : liste de la base au sommet ; chaque case = (texte, couleur) ou None (vide)."""
    s = []
    nbase = len(cases[0])
    for k, et in enumerate(cases):
        for i, case in enumerate(et):
            x = x0 + k * w / 2 + i * w
            y = k * h
            s.append(r"\draw[case,fill=white] (%s,%s) rectangle (%s,%s);" % (f(x), f(y), f(x + w), f(y + h)))
            if case:
                t, col = case
                s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (col, f(x + w / 2), f(y + h / 2), t))
    s.append(r"\node[anchor=south,text=otNavy,font=\bfseries] at (%s,%s) {%s};" % (f(x0 + nbase * w / 2), f(len(cases) * h + .1), titre))
    return "\n".join(s)


def ex_pyramides(corrige):
    I = "otInk"
    r1 = etages(P1_BASE)
    r2 = p2_complete()
    if corrige:
        c1 = [[(nb(v), I) for v in r1[0]]] + [[(nb(v), VERT) for v in r] for r in r1[1:]]
        c2 = [[(nb(r2[0][0]), I), (nb(r2[0][1]), VERT), (nb(r2[0][2]), I)],
              [(nb(r2[1][0]), I), (nb(r2[1][1]), VERT)], [(nb(r2[2][0]), VERT)]]
    else:
        c1 = [[(nb(v), I) for v in r1[0]], [None] * 3, [None] * 2, [None]]
        c2 = [[(nb(P2_BASE[0]), I), None, (nb(P2_BASE[2]), I)], [(nb(P2_DONNE), I), None], [None]]
    return "\n".join([r"\begin{tikzpicture}", pyramide(0, "Pyramide 1", c1), pyramide(4.25, "Pyramide 2", c2),
                      r"\end{tikzpicture}"])


FIGURES["ex_pyramides_enonce"] = ex_pyramides(False)
FIGURES["ex_pyramides_corrige"] = ex_pyramides(True)

P1_MODIF = [-3, 5, -8, -2]


def ex_pyramide_modifiee():
    I = "otInk"
    avant, apres = etages(P1_BASE), etages(P1_MODIF)
    cases = []
    for k, (ra, rb) in enumerate(zip(avant, apres)):
        ligne = []
        for va, vb in zip(ra, rb):
            if k == 0:
                ligne.append((nb(vb), ORANGE if va != vb else I))
            else:
                ligne.append((nb(vb), VERT if va != vb else I))
        cases.append(ligne)
    return "\n".join([r"\begin{tikzpicture}", pyramide(0, "Pyramide 1 modifiée", cases), r"\end{tikzpicture}"])


FIGURES["ex_pyramide_modifiee_corrige"] = ex_pyramide_modifiee()


# ===================================================================== 2787 : le sous-marin
SM_DEPART, SM_DEPL, SM_GOELAND = -15, [-12, 7, -18], 8


def sm_altitudes():
    a = [SM_DEPART]
    for d in SM_DEPL:
        a.append(a[-1] + d)
    return a


def ex_sousmarin(corrige):
    s = [r"\begin{tikzpicture}"]
    code, Y = axe_altitudes(-40, 10, 10, .11, 3.7)
    s.append(code)
    xs = .9
    s.append(ic_oiseau(xs, Y(SM_GOELAND), BLEU))
    s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (1.4,%s) {goéland : $%s$ m};" % (BLEU, f(Y(SM_GOELAND)), nb(SM_GOELAND)))
    s.append(ic_sousmarin(xs, Y(SM_DEPART), BLEU))
    lab = "départ" if corrige else "sous-marin"
    s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (1.45,%s) {%s : $%s$ m};" % (BLEU, f(Y(SM_DEPART) + .06), lab, nb(SM_DEPART)))
    if corrige:
        alt = sm_altitudes()
        xk = [xs, 2.0, 3.1]
        for k, d in enumerate(SM_DEPL):
            x = xk[k]
            y1 = Y(alt[k]) - (.14 if k == 0 else 0)
            s.append(r"\draw[deplV] (%s,%s) -- (%s,%s);" % (f(x), f(y1), f(x), f(Y(alt[k + 1]))))
            anc, dx = ("east", -.08) if k == 0 else ("west", .06)
            s.append(r"\node[anchor=%s,text=%s,inner sep=1.5pt] at (%s,%s) {$%s$};"
                     % (anc, VERT, f(x + dx), f((Y(alt[k]) + Y(alt[k + 1])) / 2), sg(d)))
            if k < 2:
                s.append(r"\draw[liaison] (%s,%s) -- (%s,%s);" % (f(x), f(Y(alt[k + 1])), f(xk[k + 1]), f(Y(alt[k + 1]))))
            s.append(point(x, Y(alt[k + 1]), VERT, 2.6))
        # altitudes atteintes
        s.append(r"\node[anchor=north,text=%s,inner sep=2pt] at (%s,%s) {$%s$};" % (VERT, f(xk[0]), f(Y(alt[1]) - .06), nb(alt[1])))
        s.append(r"\node[anchor=east,text=%s,inner sep=2pt] at (%s,%s) {$%s$};" % (VERT, f(xk[1] - .08), f(Y(alt[2])), nb(alt[2])))
        s.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (%s,%s) {$%s$ m};" % (VERT, f(xk[2] + .12), f(Y(alt[3])), nb(alt[3])))
        # écart goéland / sous-marin
        xe = 4.45
        s.append(r"\draw[cote,%s] (%s,%s) -- (%s,%s);" % (VERT, f(xe), f(Y(SM_GOELAND)), f(xe), f(Y(alt[3]))))
        s.append(r"\draw[otMuted!60,line width=.4pt,dash pattern=on 2pt off 1.6pt] (3.75,%s) -- (%s,%s);"
                 % (f(Y(SM_GOELAND)), f(xe + .1), f(Y(SM_GOELAND))))
        s.append(r"\node[anchor=west,text=%s,align=left] at (%s,%s) {écart :\\$%s$ m};"
                 % (VERT, f(xe + .12), f((Y(SM_GOELAND) + Y(alt[3])) / 2), nb(SM_GOELAND - alt[3])))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_sousmarin_enonce"] = ex_sousmarin(False)
FIGURES["ex_sousmarin_corrige"] = ex_sousmarin(True)


# ===================================================================== 2770 : station de ski (vendredi)
V_MIN, V_MAX = -6, 2


def ex_station(corrige):
    s = [r"\begin{tikzpicture}"]
    if not corrige:
        s.append(thermometre(-10, 6, .27, [(V_MIN, "vendredi, minimale", BLEU)]))
    else:
        marques = [(V_MAX, r"maximale : $%s$ °C" % nb(V_MAX), BLEU), (V_MIN, r"minimale : $%s$ °C" % nb(V_MIN), VERT)]

        def ec(Y):
            xd = 1.45
            return (r"\draw[accolV] (%s,%s) -- (%s,%s);" % (f(xd), f(Y(V_MAX)), f(xd), f(Y(V_MIN)))
                    + "\n" + r"\node[anchor=west,text=%s,align=left] at (%s,%s) {amplitude :\\$%s - (%s) = %s$ °C};"
                    % (VERT, f(xd + .25), f((Y(V_MAX) + Y(V_MIN)) / 2), nb(V_MAX), nb(V_MIN), nb(V_MAX - V_MIN)))
        s.append(thermometre(-10, 6, .27, marques, extra=ec))
        s.append(r"\node[anchor=south west,text=otNavy,font=\bfseries] at (-3.2,%s) {Vendredi};" % f(.27 * 16 + .25))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_station_enonce"] = ex_station(False)
FIGURES["ex_station_corrige"] = ex_station(True)


# ===================================================================== 2771 : la piste graduée
CARTES_A = [4, -7, -2, 6]
CARTES_B3 = [-3, 5, -8]
B_ARRIVEE = -2
CARTE_B4 = B_ARRIVEE - sum(CARTES_B3)


def cases(cartes):
    c = [0]
    for v in cartes:
        c.append(c[-1] + v)
    return c


def piste(y, nom, cartes, couleurs, U=.47, pas=.55, decal=None):
    """Piste graduée et parcours en escalier : une flèche horizontale par carte."""
    code, X = droite(-7, 7, U, y=y)
    s = [code]
    c = cases(cartes)
    decal = decal or {}
    s.append(r"\node[anchor=south west,text=otInk] at (%s,%s) {%s};" % (f(X(-7) - .3), f(y + pas * len(cartes) + .3), nom))
    s.append(r"\draw[liaison] (%s,%s) -- (%s,%s);" % (f(X(0)), f(y + .12), f(X(0)), f(y + pas)))
    for k, v in enumerate(cartes):
        yk = y + pas * (k + 1)
        s.append(r"\draw[deplV] (%s,%s) -- (%s,%s);" % (f(X(c[k])), f(yk), f(X(c[k + 1])), f(yk)))
        xm = (X(c[k]) + X(c[k + 1])) / 2 + decal.get(k, 0)
        s.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {$%s$};" % (couleurs[k], f(xm), f(yk + .02), sg(v)))
        if k + 1 < len(cartes):
            s.append(r"\draw[liaison] (%s,%s) -- (%s,%s);" % (f(X(c[k + 1])), f(yk), f(X(c[k + 1])), f(yk + pas)))
    yl = y + pas * len(cartes)
    s.append(r"\draw[liaison] (%s,%s) -- (%s,%s);" % (f(X(c[-1])), f(yl), f(X(c[-1])), f(y + .12)))
    s.append(point(X(0), y, BLEU))
    s.append(point(X(c[-1]), y, VERT, 2.9))
    return "\n".join(s)


def ex_piste(corrige):
    s = [r"\begin{tikzpicture}"]
    if not corrige:
        code, X = droite(-7, 7, .47, y=0)
        s.append(code)
        s.append(point(X(0), 0, BLEU))
        s.append(r"\node[anchor=south,text=%s,inner sep=2pt] at (%s,.12) {départ};" % (BLEU, f(X(0))))
    else:
        s.append(piste(0, "Anaïs", CARTES_A, [VERT] * 4, decal={1: -.6}))
        s.append(piste(-3.7, "Bastien", CARTES_B3 + [CARTE_B4], [VERT] * 4, decal={0: .22, 2: .8}))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_piste_enonce"] = ex_piste(False)
FIGURES["ex_piste_corrige"] = ex_piste(True)
