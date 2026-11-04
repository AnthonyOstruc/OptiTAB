# -*- coding: utf-8 -*-
"""Figures de la notion 252 (4e : puissances et notation scientifique), style des livres.

Compilées par outils/figures_livre.py : déplacement de la virgule, échelle des
préfixes de nano à giga, échelles des tailles graduées en puissances de 10,
feuille pliée, plage (pavé droit), satellite géostationnaire.
Éléments de réponse en vert foncé (otGreenDark) dans les corrigés.
"""
from math import cos, log10, pi, sin

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexteG/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=east,inner sep=1pt},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont},
  saut/.style={line width=.9pt,-{Stealth[length=1.9mm]}},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  pref/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=2.7cm,minimum height=.62cm,inner sep=2pt,text=otInk},
  prefU/.style={draw=otMuted,fill=white,line width=.7pt,rounded corners=3pt,dash pattern=on 2pt off 1.5pt,
    minimum width=2.7cm,minimum height=.62cm,inner sep=2pt,text=otMuted},
  couche/.style={draw=otNavy,fill=otSky,line width=.5pt},
  coucheV/.style={draw=otGreenDark,fill=otGreen!25,line width=.5pt},
}
"""

VERT = "otGreenDark"
ORANGE = "otOrange!85!black"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


FIGURES = {}


# ===================================================================== virgule
def virgule(lignes):
    """lignes : [(operation, chiffres, i_depart, i_arrivee, resultat, couleur, texte_saut, ajoutes)].

    chiffres : liste de chiffres affichés ; la virgule « après l'indice i » ;
    i_arrivee = dernier indice → nombre entier (pas de virgule finale affichée) ;
    ajoutes : indices des zéros ajoutés (gris).
    """
    w = .56
    s = [r"\begin{tikzpicture}"]
    for k, (op, ch, i0, i1, res, coul, txt, ajoutes) in enumerate(lignes):
        y = -k * 1.75
        x0 = 0.0
        s.append(r"\node[anchor=east,text=otInk] at (%s,%s) {%s};" % (f(x0 - .45), f(y), op))
        for j, c in enumerate(ch):
            col = "otMuted!70" if j in ajoutes else "otInk"
            s.append(r"\node[text=%s,font=\large,inner sep=0pt] at (%s,%s) {$%s$};" % (col, f(x0 + j * w), f(y), c))
        xv = lambda i: x0 + (i + .5) * w
        # ancienne virgule (grise)
        s.append(r"\node[text=otMuted!70,font=\large,inner sep=0pt,anchor=north] at (%s,%s) {$,$};" % (f(xv(i0) - .05), f(y - .02)))
        # nouvelle virgule (sauf nombre entier)
        if i1 != len(ch) - 1:
            s.append(r"\node[text=%s,font=\large\bfseries,inner sep=0pt,anchor=north] at (%s,%s) {$\boldsymbol{,}$};" % (coul, f(xv(i1) - .05), f(y - .02)))
        pas = 1 if i1 > i0 else -1
        bend = "bend left=55" if pas > 0 else "bend right=55"
        for i in range(i0, i1, pas):
            s.append(r"\draw[saut,%s] (%s,%s) to[%s] (%s,%s);" % (coul, f(xv(i) + .05 * pas), f(y + .3), bend, f(xv(i + pas) - .05 * pas), f(y + .3)))
        xm = (xv(i0) + xv(i1)) / 2
        s.append(r"\node[anchor=south,text=%s,petit,inner sep=1pt] at (%s,%s) {%s};" % (coul, f(xm), f(y + .62), txt))
        s.append(r"\node[anchor=west,text=%s] at (%s,%s) {%s};" % (coul, f(x0 + (len(ch) - 1) * w + .45), f(y), res))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["virgule_cours"] = virgule([
    (r"$5{,}8 \times 10^{3}$", ["5", "8", "0", "0"], 0, 3, r"$= 5\,800$", "otNavy", r"$3$ rangs vers la droite", {2, 3}),
    (r"$5{,}8 \times 10^{-2}$", ["0", "0", "5", "8"], 2, 0, r"$= 0{,}058$", ORANGE, r"$2$ rangs vers la gauche", {0, 1}),
])

FIGURES["ex_virgule_corrige"] = virgule([
    (r"$3{,}45 \times 10^{2}$", ["3", "4", "5"], 0, 2, r"$= 345$", VERT, r"$2$ rangs vers la droite", set()),
    (r"$3{,}45 \times 10^{-2}$", ["0", "0", "3", "4", "5"], 2, 0, r"$= 0{,}034\,5$", VERT, r"$2$ rangs vers la gauche", {0, 1}),
])


# ===================================================================== préfixes
PREFIXES = [("giga", "G", 9), ("méga", "M", 6), ("kilo", "k", 3), ("unité", "", 0),
            ("milli", "m", -3), ("micro", "µ", -6), ("nano", "n", -9)]


def prefixes(verts=()):
    dy = .82
    s = [r"\begin{tikzpicture}"]
    for k, (nom, sym, n) in enumerate(PREFIXES):
        y = -k * dy
        if nom == "unité":
            s.append(r"\node[prefU] at (0,%s) {sans préfixe};" % f(y))
        else:
            s.append(r"\node[pref] at (0,%s) {%s\enspace(%s)};" % (f(y), nom, sym))
        coul = VERT if n in verts else ("otMuted" if n == 0 else "otNavy")
        s.append(r"\node[anchor=west,text=%s] at (1.6,%s) {$10^{%d}$};" % (coul, f(y), n))
        if k > 0:
            ya, yb = y + .12, y + dy - .12
            s.append(r"\draw[fleche] (3.05,%s) to[bend right=55] (3.05,%s);" % (f(ya), f(yb)))
            s.append(r"\node[anchor=west,text=otMuted,petit] at (3.32,%s) {$\times 1\,000$};" % f(y + dy / 2))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["prefixes"] = prefixes()
FIGURES["ex_prefixes_corrige"] = prefixes(verts=(9, 3, -3, -6))


# ===================================================================== échelles en puissances de 10
def echelle(n0, n1, pas, objets, coul="otNavy", labels=None, unites=None, titre="longueurs en mètres",
            majeures=None):
    """Axe vertical de 10^n0 (bas) à 10^n1 (haut).

    objets : [(log10 de la taille, texte)] ; labels : exposants écrits à gauche ;
    unites : {exposant: texte gris à gauche des puissances} ; majeures : exposants à grand trait.
    """
    Y = lambda v: (v - n0) * pas
    labels = range(n0, n1 + 1) if labels is None else labels
    majeures = set(labels) if majeures is None else set(majeures)
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[axe] (0,-.25) -- (0,%s);" % f(Y(n1) + .45))
    for n in range(n0, n1 + 1):
        h = .11 if n in majeures else .06
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(-h), f(Y(n)), f(h), f(Y(n))))
    for n in labels:
        s.append(r"\node[gradTexteG] at (-.18,%s) {$10^{%d}$};" % (f(Y(n)), n))
        if unites and n in unites:
            s.append(r"\node[anchor=east,text=otMuted!80,petit,inner sep=1pt] at (-1.05,%s) {%s};" % (f(Y(n)), unites[n]))
    for v, nom in objets:
        s.append(r"\fill[%s] (0,%s) circle (2.3pt);" % (coul, f(Y(v))))
        s.append(r"\draw[%s,line width=.45pt] (.12,%s) -- (.42,%s);" % (coul, f(Y(v)), f(Y(v))))
        s.append(r"\node[anchor=west,text=%s,inner sep=1pt] at (.47,%s) {%s};" % (coul, f(Y(v)), nom))
    if titre:
        s.append(r"\node[anchor=south,text=otMuted,petit] at (0,%s) {%s};" % (f(Y(n1) + .55), titre))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["echelle_cours"] = echelle(-10, 21, .3, [
    (-10, "atome"), (-7, "virus"), (-5, "cellule"), (-3, "fourmi"), (0, "être humain"),
    (2, "tour Eiffel"), (7, "diamètre de la Terre"), (11, "distance Terre – Soleil"),
    (16, "année-lumière"), (21, "diamètre de la Voie lactée")],
    labels=range(-9, 22, 3), unites={-9: "1 nm", -6: "1 µm", -3: "1 mm", 0: "1 m", 3: "1 km"})

# exercice 2536 : tailles microscopiques (positions réelles sur l'échelle)
MICRO = [(log10(1e-10), r"atome : $1 \times 10^{-10}$ m"), (log10(1.2e-7), r"virus : $1{,}2 \times 10^{-7}$ m"),
         (log10(7e-6), r"globule rouge : $7 \times 10^{-6}$ m"), (log10(8e-5), r"cheveu : $8 \times 10^{-5}$ m")]
FIGURES["ex_micro_enonce"] = echelle(-11, -3, .62, [])
FIGURES["ex_micro_corrige"] = echelle(-11, -3, .62, MICRO, coul=VERT)

# exercice 2542 : de la bactérie à la galaxie d'Andromède (ordres de grandeur)
GRANDS = [(-6, "bactérie"), (-2, "grain de riz"), (1, "girafe"), (4, "mont Everest"),
          (8, "diamètre de Jupiter"), (12, "distance Soleil – Jupiter"), (21, "galaxie d'Andromède")]
FIGURES["ex_echelle_enonce"] = echelle(-6, 21, .3, [], labels=range(-6, 22, 3))
FIGURES["ex_echelle_corrige"] = echelle(-6, 21, .3, GRANDS, coul=VERT, labels=range(-6, 22, 3))


# ===================================================================== feuille pliée (2528)
def pliage(corrige):
    lw, h, gap = 1.55, .13, .62
    s = [r"\begin{tikzpicture}"]
    for k in range(4):
        x = k * (lw + gap)
        n = 2 ** k
        cache = (k == 3 and not corrige)
        if cache:
            s.append(r"\draw[otMuted,line width=.6pt,dash pattern=on 2pt off 1.5pt] (%s,0) rectangle (%s,%s);"
                     % (f(x), f(x + lw), f(8 * h)))
            s.append(r"\node[text=otOrange!85!black,font=\Large] at (%s,%s) {?};" % (f(x + lw / 2), f(4 * h)))
            haut, txt, coul = 8 * h, r"? couches", ORANGE
            txt = r"$?$ couches"
        else:
            st = "coucheV" if (k == 3 and corrige) else "couche"
            for j in range(n):
                s.append(r"\draw[%s] (%s,%s) rectangle (%s,%s);" % (st, f(x), f(j * h), f(x + lw), f((j + 1) * h)))
            haut = n * h
            if k == 3:
                txt, coul = r"$2^3 = 8$ couches", VERT
            else:
                txt, coul = (r"$1$ couche" if n == 1 else r"$%d$ couches" % n), "otNavy"
        s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (coul, f(x + lw / 2), f(haut + .1), txt))
        s.append(r"\node[anchor=north,text=otMuted,petit,inner sep=1pt] at (%s,-.12) {%s};"
                 % (f(x + lw / 2), "0 pli" if k == 0 else ("1 pli" if k == 1 else "%d plis" % k)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_pliage_enonce"] = pliage(False)
FIGURES["ex_pliage_corrige"] = pliage(True)


# ===================================================================== plage (2545)
def plage():
    L, H, dx, dy = 4.6, .85, 1.2, .6
    s = [r"\begin{tikzpicture}"]
    s.append(r"\coordinate (A) at (0,0); \coordinate (B) at (%s,0); \coordinate (C) at (%s,%s); \coordinate (D) at (0,%s);"
             % (f(L), f(L), f(H), f(H)))
    s.append(r"\coordinate (E) at (%s,%s); \coordinate (F) at (%s,%s); \coordinate (G) at (%s,%s); \coordinate (Hh) at (%s,%s);"
             % (f(dx), f(dy), f(L + dx), f(dy), f(L + dx), f(H + dy), f(dx), f(H + dy)))
    s.append(r"\fill[otOrange!22] (A) -- (B) -- (F) -- (G) -- (Hh) -- (D) -- cycle;")
    s.append(r"\fill[otOrange!35] (B) -- (F) -- (G) -- (C) -- cycle;")
    s.append(r"\draw[otMuted,line width=.55pt,dash pattern=on 2.5pt off 1.8pt] (A) -- (E) -- (F) (E) -- (Hh);")
    s.append(r"\draw[otOrange!70!black,line width=.85pt,line join=round] (A) -- (B) -- (C) -- (D) -- cycle (B) -- (F) -- (G) -- (C) (D) -- (Hh) -- (G);")
    # cotes
    s.append(r"\draw[cote] (0,-.38) -- (%s,-.38);" % f(L))
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,-.05) -- (0,-.5) (%s,-.05) -- (%s,-.5);" % (f(L), f(L)))
    s.append(r"\node[coteTexte] at (%s,-.38) {$3$ km};" % f(L / 2))
    s.append(r"\draw[cote] (-.38,0) -- (-.38,%s);" % f(H))
    s.append(r"\draw[otMuted!70,line width=.4pt] (-.05,0) -- (-.5,0) (-.05,%s) -- (-.5,%s);" % (f(H), f(H)))
    s.append(r"\node[anchor=east,text=otInk,inner sep=1pt] at (-.5,%s) {$2$ m};" % f(H / 2))
    s.append(r"\node[anchor=north west,text=otInk,inner sep=1pt] at (%s,%s) {$50$ m};" % (f(L + dx / 2 + .12), f(dy / 2 - .02)))
    # grain de sable
    c, x0 = .62, L + dx + 1.0
    s.append(r"\fill[otOrange!35] (%s,0) rectangle (%s,%s);" % (f(x0), f(x0 + c), f(c)))
    s.append(r"\fill[otOrange!22] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
             % (f(x0), f(c), f(x0 + .25), f(c + .2), f(x0 + c + .25), f(c + .2), f(x0 + c), f(c)))
    s.append(r"\fill[otOrange!45] (%s,0) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
             % (f(x0 + c), f(x0 + c + .25), f(.2), f(x0 + c + .25), f(c + .2), f(x0 + c), f(c)))
    s.append(r"\draw[otOrange!70!black,line width=.7pt,line join=round] (%s,0) rectangle (%s,%s) (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) (%s,0) -- (%s,%s) -- (%s,%s);"
             % (f(x0), f(x0 + c), f(c), f(x0), f(c), f(x0 + .25), f(c + .2), f(x0 + c + .25), f(c + .2), f(x0 + c), f(c),
                f(x0 + c), f(x0 + c + .25), f(.2), f(x0 + c + .25), f(c + .2)))
    s.append(r"\draw[cote] (%s,-.38) -- (%s,-.38);" % (f(x0), f(x0 + c)))
    s.append(r"\draw[otMuted!70,line width=.4pt] (%s,-.05) -- (%s,-.5) (%s,-.05) -- (%s,-.5);" % (f(x0), f(x0), f(x0 + c), f(x0 + c)))
    s.append(r"\node[anchor=north,text=otInk,inner sep=1pt] at (%s,-.52) {$1$ mm};" % f(x0 + c / 2))
    s.append(r"\node[anchor=south,text=otMuted,petit,inner sep=1pt] at (%s,%s) {un grain};" % (f(x0 + c / 2 + .12), f(c + .32)))
    s.append(r"\node[anchor=south,text=otMuted,petit,inner sep=1pt] at (%s,%s) {la couche de sable (pas à l'échelle)};" % (f((L + dx) / 2), f(H + dy + .15)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_plage_enonce"] = plage()


# ===================================================================== satellite (2546)
def satellite(corrige):
    """Orbite à l'échelle : rayon de la Terre 6,4 et rayon de l'orbite 42,4 (milliers de km)."""
    Ro = 3.8
    rT = Ro * 6.4 / 42.4
    deg = 38
    a = deg * pi / 180
    ux, uy = cos(a), sin(a)
    nx, ny = -uy, ux                      # normale à gauche du rayon [OS]
    S = (Ro * ux, Ro * uy)
    E = (rT * ux, rT * uy)
    orange = "otOrange!85!black"
    s = [r"\begin{tikzpicture}"]
    s.append(r"\draw[%s,line width=.7pt,dash pattern=on 3pt off 2pt] (0,0) circle (%s);" % (orange, f(Ro)))
    s.append(r"\draw[otNavy,line width=.8pt,fill=otSky] (0,0) circle (%s);" % f(rT))
    s.append(r"\draw[otNavy,line width=.9pt] (0,0) -- (%s,%s);" % (f(E[0]), f(E[1])))
    s.append(r"\draw[%s,line width=.9pt] (%s,%s) -- (%s,%s);" % (orange, f(E[0]), f(E[1]), f(S[0]), f(S[1])))
    s.append(r"\fill[otNavy] (0,0) circle (1.6pt);")
    s.append(r"\node[anchor=south east,text=otInk,inner sep=1pt] at (-.02,.02) {$O$};")
    s.append(r"\node[anchor=north,text=otNavy,align=center,inner sep=1pt] at (0,%s) {Terre\\{\otRegular\fontsize{8.5}{10}\selectfont rayon : $6{,}4 \times 10^{3}$ km}};"
             % f(-rT - .1))
    # satellite : corps et panneaux solaires
    s.append(r"\begin{scope}[shift={(%s,%s)},rotate=%s]" % (f(S[0]), f(S[1]), f(deg - 90)))
    s.append(r"\fill[otNavy] (-.11,-.09) rectangle (.11,.09);")
    s.append(r"\fill[otNavy!55] (-.34,-.05) rectangle (-.15,.05) (.15,-.05) rectangle (.34,.05);")
    s.append(r"\end{scope}")
    s.append(r"\node[anchor=south west,text=otInk,inner sep=1.5pt] at (%s,%s) {$S$};" % (f(S[0] + .22), f(S[1] + .12)))
    m = ((E[0] + S[0]) / 2, (E[1] + S[1]) / 2)
    s.append(r"\node[anchor=south east,text=%s,petit,align=right,inner sep=1pt] at (%s,%s) {altitude\\$3{,}6 \times 10^{4}$ km};"
             % (orange, f(m[0] + .22 * nx - .05), f(m[1] + .22 * ny)))
    s.append(r"\node[anchor=north east,text=%s,petit,inner sep=1pt] at (%s,%s) {orbite};"
             % (orange, f(Ro * cos(-2.4) - .05), f(Ro * sin(-2.4) - .05)))
    if corrige:
        d = .5
        P = (-d * nx, -d * ny)            # cote parallèle à [OS], décalée vers la droite
        Q = (S[0] + P[0] - .1 * ux, S[1] + P[1] - .1 * uy)
        s.append(r"\draw[%s,line width=.75pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (%s,%s) -- (%s,%s);"
                 % (VERT, f(P[0]), f(P[1]), f(Q[0]), f(Q[1])))
        t = (rT + Ro) / 2 - .05           # texte centré sur la partie de la cote hors de la Terre
        s.append(r"\node[coteTexte,text=%s,rotate=%s,font=\small] at (%s,%s) {$OS = 4{,}24 \times 10^{4}$ km};"
                 % (VERT, f(deg), f(P[0] + t * ux), f(P[1] + t * uy)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_satellite_enonce"] = satellite(False)
FIGURES["ex_satellite_corrige"] = satellite(True)

TOLERE = {
    "ex_satellite_corrige": "cote verte inclinée le long de [OS] : son texte est posé sur la cote avec un fond blanc "
                            "(comme toute cote) ; le cadre horizontal du texte incliné englobe le rayon orange parallèle, "
                            "qui reste à 0,5 cm du texte : aucun trait sous le texte (vérifié à l'œil)",
}


