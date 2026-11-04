# -*- coding: utf-8 -*-
"""Figures de la notion 270 (5e : inconnues et équations simples), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Balances de Roberval (chaque étape = la même opération sur les deux plateaux),
schémas en barres (données dans l'énoncé, valeur trouvée en vert dans le corrigé),
programme de calcul « à l'endroit » puis « à l'envers ».
Bleu marine = données, orange = nombres connus, vert foncé = éléments de réponse.
Machinerie des balances reprise de la notion 256 (4e).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=1pt},
  masse/.style={draw=otOrange!80!black,fill=otOrange!25,line width=.8pt},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
  accolv/.style={decorate,decoration={brace,amplitude=5pt},otGreenDark,line width=.7pt},
  barre/.style={draw=otNavy,line width=.8pt},
  fleche/.style={otOrange!90!black,line width=1pt,-{Stealth[length=2.4mm]}},
  flecheP/.style={otNavy,line width=.9pt,-{Stealth[length=2.3mm]}},
  flecheV/.style={otGreenDark,line width=.9pt,-{Stealth[length=2.3mm]}},
  case/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=2pt,minimum height=.62cm,minimum width=1.25cm,inner sep=3pt},
  caseV/.style={draw=otGreenDark,fill=otGreen!15,line width=.8pt,rounded corners=2pt,minimum height=.62cm,minimum width=1.25cm,inner sep=3pt,text=otGreenDark},
}
"""

FIGURES = {}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait
V = "otGreenDark"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def vert(s):
    return r"\textcolor{otGreenDark}{%s}" % s


def visible(m):
    return m.replace("{,}", ",").replace("\\,", "")


# ================================================================== BALANCES DE ROBERVAL
E, PW = 1.9, 1.6           # demi-fléau, demi-largeur d'un plateau
LB, GAP, HM = .44, .07, .42


def larg_masse(m):
    return max(.66, .17 * len(visible(m)) + .4)


def plateau(cx, y0, n, m, final=False):
    """n boîtes x puis une masse m (texte) posées sur un plateau centré en cx."""
    s = []
    lm = larg_masse(m) if m else 0
    larg = n * LB + max(n - 1, 0) * GAP + ((GAP if n else 0) + lm if m else 0)
    x = cx - larg / 2
    bord, fond, enc = ("otGreenDark", "otGreen!18", "otGreenDark") if final else ("otNavy", "otSky", "otInk")
    for _ in range(n):
        s.append(r"\draw[boite,draw=%s,fill=%s] (%s,%s) rectangle (%s,%s);" % (bord, fond, f(x), f(y0), f(x + LB), f(y0 + LB)))
        s.append(r"\node[text=%s] at (%s,%s) {$x$};" % (enc, f(x + LB / 2), f(y0 + LB / 2)))
        x += LB + GAP
    if m:
        s.append(r"\draw[masse] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
                 % (f(x), f(y0), f(x + lm), f(y0), f(x + lm - .1), f(y0 + HM), f(x + .1), f(y0 + HM)))
        s.append(r"\node[text=otInk] at (%s,%s) {$%s$};" % (f(x + lm / 2), f(y0 + HM / 2), m))
    return s


def balance(g, d, oy=0.0, eg=None, ed=None, final=False, nom=None):
    """g, d : (nombre de boîtes, masse ou None) ; eg, ed : membres écrits sous les plateaux."""
    s = [
        r"\fill[otMuted!25] (-1,%s) -- (1,%s) -- (.6,%s) -- (-.6,%s) -- cycle;" % (f(oy), f(oy), f(oy + .25), f(oy + .25)),
        r"\draw[otMuted,line width=.8pt] (-1,%s) -- (1,%s) -- (.6,%s) -- (-.6,%s) -- cycle;" % (f(oy), f(oy), f(oy + .25), f(oy + .25)),
        r"\draw[otMuted,line width=2.2pt] (0,%s) -- (0,%s);" % (f(oy + .25), f(oy + 1.1)),
        r"\draw[otNavy,line width=1.6pt] (%s,%s) -- (%s,%s);" % (f(-E), f(oy + 1.1), f(E), f(oy + 1.1)),
        r"\fill[otMuted] (0,%s) circle (2.4pt);" % f(oy + 1.1),
    ]
    for cx in (-E, E):
        s += [r"\draw[otNavy,line width=1.6pt] (%s,%s) -- (%s,%s);" % (f(cx), f(oy + 1.1), f(cx), f(oy + 1.45)),
              r"\draw[otNavy,line width=1.8pt] (%s,%s) -- (%s,%s);" % (f(cx - PW), f(oy + 1.5), f(cx + PW), f(oy + 1.5))]
    s += plateau(-E, oy + 1.6, *g, final=final)
    s += plateau(E, oy + 1.6, *d, final=final)
    c = V if final else "otInk"
    if eg:
        s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(-E), f(oy + .62), eg))
    if ed:
        s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(E), f(oy + .62), ed))
    if nom:
        s.append(r"\node[txt,anchor=west,text=otNavy] at (%s,%s) {%s};" % (f(-E - PW), f(oy + 2.45), nom))
    return s


PAS = 3.05   # écart vertical entre deux étapes


def operation(oy, texte):
    """Flèches orange et texte de l'opération, sous la balance dont le socle est en oy."""
    return [r"\draw[fleche] (%s,%s) -- (%s,%s);" % (f(xx), f(oy - .12), f(xx), f(oy - .8)) for xx in (-3.35, 3.35)] \
        + [r"\node[txt] at (0,%s) {%s};" % (f(oy - .46), texte)]


def etapes(liste, ops, conclusion=None, nom=None):
    """liste : [(g, d, eg, ed)] ; ops : textes entre les étapes ; la dernière étape est en vert."""
    s = []
    for k, (g, d, eg, ed) in enumerate(liste):
        oy = -k * PAS
        s += balance(g, d, oy, eg, ed, final=(k == len(liste) - 1), nom=nom if k == 0 else None)
        if k < len(liste) - 1:
            s += operation(oy, ops[k])
    if conclusion:
        oy = -(len(liste) - 1) * PAS
        s.append(r"\node[txt,text=otGreenDark] at (0,%s) {%s};" % (f(oy - .5), conclusion))
    return figure(s)


# cours : x + 5 = 12 puis 3x = 12
FIGURES["cours_balance_add"] = etapes(
    [((1, "5"), (0, "12"), "x + 5", "12"),
     ((1, None), (0, "7"), "x", "7")],
    ["on enlève $5$ g sur chaque plateau"])
FIGURES["cours_balance_mul"] = etapes(
    [((3, None), (0, "12"), "3x", "12"),
     ((1, None), (0, "4"), "x", "4")],
    ["on garde le tiers de chaque plateau"])

# 2896 : balances A (x + 8 = 23) et B (x + 4,5 = 12)
FIGURES["ex2896_A"] = figure(balance((1, "8"), (0, "23"), nom="Balance A"))
FIGURES["ex2896_B"] = figure(balance((1, "4{,}5"), (0, "12"), nom="Balance B"))
FIGURES["ex2896_A_corrige"] = etapes(
    [((1, "8"), (0, "23"), "x + 8", "23"),
     ((1, None), (0, "15"), "x", "15")],
    ["on enlève $8$ g sur chaque plateau"], nom="Balance A")
FIGURES["ex2896_B_corrige"] = etapes(
    [((1, "4{,}5"), (0, "12"), "x + 4{,}5", "12"),
     ((1, None), (0, "7{,}5"), "x", "7{,}5")],
    ["on enlève $4{,}5$ g sur chaque plateau"], nom="Balance B")

# 2898 : 4x = 18
FIGURES["ex2898_balance"] = figure(balance((4, None), (0, "18")))
FIGURES["ex2898_balance_corrige"] = etapes(
    [((4, None), (0, "18"), "4x", "18"),
     ((1, None), (0, "4{,}5"), "x", "4{,}5")],
    ["on garde le quart de chaque plateau"])


# ================================================================== SCHÉMAS EN BARRES
H = .62


def bande(blocs, u, total=None, sous=None, y=0.0, sous_couleur="otMuted"):
    """Une barre horizontale.
    blocs : [(largeur, texte, style)] avec style 'x' (inconnue), 'n' (nombre connu), 'v' (valeur trouvée, vert).
    total : texte d'une accolade au-dessus de toute la barre.
    sous : [(i0, i1, texte)] accolades sous les blocs i0..i1 (vertes)."""
    s, x, bords = [], 0.0, [0.0]
    for (w, t, st) in blocs:
        w *= u
        if st == "v":
            dessin, fond, coul = "otGreenDark", "otGreen!15", "otGreenDark"
        elif st == "x":
            dessin, fond, coul = "otNavy", "otSky", "otInk"
        else:
            dessin, fond, coul = "otOrange!80!black", "otOrange!18", "otInk"
        s.append(r"\draw[line width=.8pt,draw=%s,fill=%s] (%s,%s) rectangle (%s,%s);" % (dessin, fond, f(x), f(y), f(x + w), f(y + H)))
        if t:
            s.append(r"\node[text=%s] at (%s,%s) {%s};" % (coul, f(x + w / 2), f(y + H / 2), t))
        x += w
        bords.append(x)
    if total:
        s.append(r"\draw[accol] (0,%s) -- (%s,%s) node[midway,above=7pt,inner sep=1pt,text=otInk] {%s};" % (f(y + H + .12), f(x), f(y + H + .12), total))
    for (i0, i1, t) in (sous or []):
        a, b = bords[i0], bords[i1 + 1]
        s.append(r"\draw[accolv] (%s,%s) -- (%s,%s) node[midway,below=7pt,inner sep=1pt,text=otGreenDark] {%s};" % (f(b - .03), f(y - .12), f(a + .03), f(y - .12), t))
    return s


def lignes_barres(lignes, u, pas=.95, xlab=-.25, droite=None, total=None, bas=None, ecart=2.0):
    """Plusieurs barres nommées : lignes = [(nom, blocs)] ; total = accolade verticale à droite."""
    s, xmax = [], 0.0
    for i, (nom, blocs) in enumerate(lignes):
        y = -i * pas
        s.append(r"\node[txt,anchor=east] at (%s,%s) {%s};" % (f(xlab), f(y + H / 2), nom))
        s += bande(blocs, u, y=y)
        xmax = max(xmax, sum(b[0] for b in blocs) * u)
    n = len(lignes)
    if droite:
        for i, t in enumerate(droite):
            if t:
                s.append(r"\node[anchor=west] at (%s,%s) {%s};" % (f(xmax + .35), f(-i * pas + H / 2), t))
    if total:
        haut, bas_ = H + .05, -(n - 1) * pas - .05
        xa = xmax + (ecart if droite else .25)
        s.append(r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(xa), f(haut), f(xa), f(bas_)))
        s.append(r"\node[anchor=west] at (%s,%s) {%s};" % (f(xa + .3), f((haut + bas_) / 2), total))
    if bas:
        for j, ligne in enumerate([bas] if isinstance(bas, str) else bas):
            s.append(r"\node[anchor=north] at (%s,%s) {%s};" % (f(xmax / 2), f(-(n - 1) * pas - .45 - .5 * j), ligne))
    return s


# ---- cours
FIGURES["cours_barres_livre"] = figure(bande(
    [(2.4, r"livre : $x$", "x"), (2.0, r"reste : $12{,}50$ €", "n")], 1.25, total=r"$40$ €"))
FIGURES["cours_barres_etageres"] = figure(bande(
    [(1, r"$n$", "x")] * 7, .95, total=r"$168$ livres"))
FIGURES["cours_remonter"] = figure(bande(
    [(1, r"$x$", "x")] * 3 + [(.6, r"$2$", "n")], 1.35, total=r"$11$ €",
    sous=[(0, 2, r"$11 - 2 = 9$ €, puis $9 \div 3 = 3$ €")]))

# ---- 2901 : randonnée et ruban
FIGURES["ex2901_rando"] = figure(bande(
    [(7.8, r"parcourus : $7{,}8$ km", "n"), (4.7, r"$d$", "x")], .5, total=r"$12{,}5$ km"))
FIGURES["ex2901_rando_corrige"] = figure(bande(
    [(7.8, r"parcourus : $7{,}8$ km", "n"), (4.7, r"$d$", "v")], .5, total=r"$12{,}5$ km",
    sous=[(1, 1, r"$12{,}5 - 7{,}8 = 4{,}7$ km")]))
FIGURES["ex2901_ruban"] = figure(bande(
    [(1, r"$\ell$", "x")] * 8, .8, total=r"$18$ m"))
FIGURES["ex2901_ruban_corrige"] = figure(bande(
    [(1, r"$2{,}25$", "v")] * 8, .85, total=r"$18$ m")
    + [r"\node[anchor=north,text=otGreenDark] at (%s,-.3) {$\ell = 18 \div 8 = 2{,}25$ m};" % f(4 * .85)])

# ---- 2914 : bidon et flacons
FIGURES["ex2914_enonce"] = figure(bande(
    [(1.2, r"$1{,}2$ kg", "n"), (3.6, r"contenu : $m$", "x")], 1.45, total=r"bidon rempli : $4{,}8$ kg")
    + [r"\node[petit,anchor=north] at (%s,-.2) {bidon vide};" % f(.6 * 1.45)])
_y2 = -2.75
FIGURES["ex2914_corrige"] = figure(
    bande([(1.2, r"$1{,}2$ kg", "n"), (3.6, r"$m$", "v")], 1.45, total=r"bidon rempli : $4{,}8$ kg",
          sous=[(1, 1, r"$m = 4{,}8 - 1{,}2 = 3{,}6$ kg")])
    + bande([(1, r"$0{,}45$", "v")] * 8, .87, y=_y2, total=r"contenu ($3{,}6$ kg) partagé en $8$ flacons")
    + [r"\node[petit,anchor=north] at (%s,-.2) {bidon vide};" % f(.6 * 1.45),
       r"\node[anchor=north,text=otGreenDark] at (%s,%s) {$x = 3{,}6 \div 8 = 0{,}45$ kg par flacon};" % (f(4 * .87), f(_y2 - .3))])

# ---- 2904 : billes (4t = 64) et ruban coupé en deux (2x + 0,6 = 2,4)
L_BILLES = [("Tom", [(1, r"$t$", "x")]),
            ("Inès", [(1, r"$t$", "x")] * 3)]
FIGURES["ex2904_billes"] = figure(lignes_barres(L_BILLES, 1.1, total=r"$64$ billes"))
FIGURES["ex2904_billes_corrige"] = figure(lignes_barres(
    [("Tom", [(1, r"$16$", "v")]), ("Inès", [(1, r"$16$", "v")] * 3)], 1.1,
    total=r"$64$ billes",
    bas=[vert(r"$4t = 64$, donc $t = 64 \div 4 = 16$"),
         vert(r"Tom : $16$ billes ; Inès : $3 \times 16 = 48$ billes")]))
L_RUBAN = [("petit", [(1, r"$x$", "x")]),
           ("grand", [(1, r"$x$", "x"), (.6, r"$0{,}6$", "n")])]
FIGURES["ex2904_ruban"] = figure(lignes_barres(L_RUBAN, 1.6, total=r"$2{,}4$ m"))
FIGURES["ex2904_ruban_corrige"] = figure(lignes_barres(
    [("petit", [(1, r"$0{,}9$", "v")]), ("grand", [(1, r"$0{,}9$", "v"), (.6, r"$0{,}6$", "n")])], 1.6,
    total=r"$2{,}4$ m",
    bas=[vert(r"$2{,}4 - 0{,}6 = 1{,}8$ m, puis $x = 1{,}8 \div 2 = 0{,}9$ m"),
         vert(r"petit : $0{,}9$ m ; grand : $0{,}9 + 0{,}6 = 1{,}5$ m")]))


# ================================================================== PROGRAMME DE CALCUL (2900)
def programme(cases, ops, retour=None):
    """cases : textes des cases ; ops : opérations écrites au-dessus des flèches (à l'endroit).
    retour : (cases vertes, opérations inverses) écrites sur une ligne en dessous, flèches vers la gauche."""
    dx = 2.3
    s = []
    for i, t in enumerate(cases):
        s.append(r"\node[case] (c%d) at (%s,0) {%s};" % (i, f(i * dx), t))
    for i, op in enumerate(ops):
        s.append(r"\draw[flecheP] (c%d.east) -- (c%d.west) node[midway,above=4pt,inner sep=1pt,text=otNavy] {%s};" % (i, i + 1, op))
    if retour:
        rc, rops = retour
        y = -2.1
        for i, t in enumerate(rc):
            s.append(r"\node[caseV] (r%d) at (%s,%s) {%s};" % (i, f(i * dx), f(y), t))
        for i, op in enumerate(rops):
            s.append(r"\draw[flecheV] (r%d.west) -- (r%d.east) node[midway,below=4pt,inner sep=1pt,text=otGreenDark] {%s};" % (i + 1, i, op))
        s.append(r"\node[txt,text=otGreenDark,anchor=south west] at (%s,%s) {à l'envers (opérations inverses) :};" % (f(-.65), f(y + .55)))
        s.append(r"\node[txt,text=otNavy,anchor=south west] at (%s,%s) {à l'endroit :};" % (f(-.65), f(.85)))
    return figure(s)


FIGURES["ex2900_programme"] = programme(["nombre", "", "résultat"], [r"$\times 4$", r"$+ 7$"])
FIGURES["ex2900_corrige"] = programme([r"$9$", r"$36$", r"$43$"], [r"$\times 4$", r"$+ 7$"],
                                      retour=([r"$9$", r"$36$", r"$43$"], [r"$\div 4$", r"$- 7$"]))
