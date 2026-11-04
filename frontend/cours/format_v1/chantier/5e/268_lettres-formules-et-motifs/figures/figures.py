# -*- coding: utf-8 -*-
"""Figures de la notion 268 (5e : lettres, formules et motifs), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Motifs qui grandissent (allumettes, carreaux, tables et chaises), rectangles et
figures à côtés littéraux, programmes de calcul en schéma, feuilles de tableur.
L'énoncé ne donne jamais la réponse ; dans les corrigés, le comptage et les
éléments de réponse sont en vert foncé (otGreenDark), les parties fixes en orange.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum height=.66cm,inner sep=3.5pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  titreP/.style={text=otNavy,font=\bfseries},
  allum/.style={otOrange!65!black,line width=2.6pt,line cap=round},
  allumO/.style={otOrange,line width=2.6pt,line cap=round},
  allumV/.style={otGreenDark,line width=2.6pt,line cap=round},
  allumV2/.style={otGreen,line width=2.6pt,line cap=round},
  tete/.style={fill=otRed},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  etape/.style={font=\otMedium\fontsize{9}{11}\selectfont,text=otNavy},
  cellule/.style={font=\otRegular\fontsize{9}{11}\selectfont,text=otNavy},
  table/.style={fill=otSky,draw=otNavy,line width=.8pt},
  chaise/.style={fill=otMuted!22,draw=otMuted,line width=.6pt,rounded corners=1.2pt},
  chaiseO/.style={fill=otOrange!35,draw=otOrange!85!black,line width=.6pt,rounded corners=1.2pt},
  chaiseV/.style={fill=otGreen!35,draw=otGreenDark,line width=.6pt,rounded corners=1.2pt},
  carreau/.style={fill=otMuted!38,draw=otMuted,line width=.5pt},
  carreauO/.style={fill=otOrange!40,draw=otOrange!85!black,line width=.5pt},
  carreauV/.style={fill=otGreen!40,draw=otGreenDark,line width=.5pt},
  vide/.style={fill=white,draw=otNavy!45,line width=.5pt},
}
"""

VERT = "otGreenDark"
ORANGE_T = "otOrange!85!black"


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


FIGURES = {}


# ===================================================================== allumettes
def allumette(x1, y1, x2, y2, style="allum", g=.12, r=2.3):
    """Allumette de (x1,y1) vers (x2,y2), raccourcie de g à chaque bout ; tête rouge à l'arrivée."""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    a = (x1 + g * ux, y1 + g * uy)
    b = (x2 - g * ux, y2 - g * uy)
    return [r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(a[0]), f(a[1]), f(b[0]), f(b[1])),
            r"\fill[tete] (%s,%s) circle (%spt);" % (f(b[0]), f(b[1]), f(r))]


# ---------------------------------------------------------------- carrés accolés (cours)
def carres(nb, s, x0, styles=None):
    """nb carrés accolés de côté s. styles = (style de la 1re verticale, fonction k -> style du carré k)."""
    L = []
    st0 = styles[0] if styles else "allum"
    L += allumette(x0, 0, x0, s, st0)
    for k in range(nb):
        st = styles[1](k) if styles else "allum"
        a, b = x0 + k * s, x0 + (k + 1) * s
        L += allumette(a, s, b, s, st)
        L += allumette(a, 0, b, 0, st)
        L += allumette(b, 0, b, s, st)
    return L


def cours_motif():
    """Étapes 1, 2, 3 l'une sous l'autre (lisible sur téléphone), comptage à droite."""
    s = .72
    L = []
    x0 = 1.55
    for i in range(3):
        n = i + 1
        y = -i * 1.25
        bloc = carres(n, s, x0, ("allumO", lambda k: "allumV" if k % 2 == 0 else "allumV2"))
        L += [decaler(lg, 0, y) for lg in bloc]
        L.append(r"\node[etape,anchor=east] at (%s,%s) {Étape %d};" % (f(x0 - .32), f(y + s / 2), n))
        calc = "1 + 3 = 4" if n == 1 else r"1 + 3 \times %d = %d" % (n, 3 * n + 1)
        L.append(r"\node[text=%s,anchor=west] at (%s,%s) {$%s$};" % (VERT, f(x0 + 3 * s + .45), f(y + s / 2), calc))
    L.append(r"\node[petit,anchor=north west,text=otOrange!85!black] at (0,%s) {en orange : la première allumette};" % f(-2.5 - .3))
    L.append(r"\node[petit,anchor=north west,text=otGreenDark] at (0,%s) {en vert : 3 allumettes par carré};" % f(-2.5 - .72))
    return tikz(L)


def decaler(ligne, dx, dy):
    """Décale toutes les coordonnées (x,y) d'une ligne TikZ."""
    import re as _re
    return _re.sub(r"\((-?[\d.]+),(-?[\d.]+)\)",
                   lambda m: "(%s,%s)" % (f(float(m.group(1)) + dx), f(float(m.group(2)) + dy)), ligne)


FIGURES["cours_motif"] = cours_motif()


# ---------------------------------------------------------------- triangles (exercice 2852)
def triangles(nb, s, x0, styles=None):
    """Bande de nb triangles équilatéraux alternés (pointe en haut, puis en bas…).
    styles = (style de la 1re allumette, fonction k -> style des 2 allumettes du triangle k)."""
    h = s * math.sqrt(3) / 2
    L = []
    st0 = styles[0] if styles else "allum"
    G, R = .21, 2.1   # écart aux sommets (plusieurs allumettes s'y rejoignent), rayon des têtes
    L += allumette(x0, 0, x0 + s / 2, h, st0, G, R)    # côté gauche du 1er triangle
    for k in range(nb):
        st = styles[1](k) if styles else "allum"
        if k % 2 == 0:   # pointe en haut : base en bas + côté droit
            a = x0 + (k // 2) * s
            L += allumette(a, 0, a + s, 0, st, G, R)
            L += allumette(a + s, 0, a + s / 2, h, st, G, R)
        else:            # pointe en bas : base en haut + côté droit
            a = x0 + (k // 2) * s + s / 2
            L += allumette(a, h, a + s, h, st, G, R)
            L += allumette(a + s / 2, 0, a + s, h, st, G, R)
    return L, h


def largeur_tri(nb, s):
    return (nb + 1) / 2 * s


def ex2852_enonce():
    s = 1.0
    L = []
    x = 0.0
    for n in (1, 2, 3):
        T, h = triangles(n, s, x)
        L += T
        L.append(r"\node[etape,anchor=north] at (%s,-.3) {Étape %d};" % (f(x + largeur_tri(n, s) / 2), n))
        x += largeur_tri(n, s) + .95
    return tikz(L)


def ex2852_corrige():
    s = 1.45
    styles = ("allumO", lambda k: "allumV" if k % 2 == 0 else "allumV2")
    T, h = triangles(3, s, 0.0, styles)
    L = list(T)
    # « 2 » au centre de chaque triangle
    for k in range(3):
        if k % 2 == 0:
            cx, cy = (k // 2) * s + s / 2, h / 3
        else:
            cx, cy = (k // 2) * s + s, 2 * h / 3
        L.append(r"\node[text=%s] at (%s,%s) {$2$};" % (VERT, f(cx), f(cy)))
    L.append(r"\node[text=%s,anchor=east] at (%s,%s) {$1$};" % (ORANGE_T, f(s / 4 - .2), f(h / 2 + .05)))
    L.append(r"\node[etape,anchor=south] at (%s,%s) {Étape 3};" % (f(largeur_tri(3, s) / 2), f(h + .25)))
    L.append(r"\node[text=%s,anchor=north] at (%s,-.3) {$1 + 2 \times 3 = 7$ allumettes};" % (VERT, f(largeur_tri(3, s) / 2)))
    return tikz(L)


FIGURES["ex2852_enonce"] = ex2852_enonce()
FIGURES["ex2852_corrige"] = ex2852_corrige()


# ===================================================================== bordure de carreaux (2866)
def bordure(n, u, x0, mode="enonce"):
    """Carré blanc de n × n entouré d'une bordure d'un carreau. mode = enonce | corrige."""
    L = []
    N = n + 2
    for i in range(N):
        for j in range(N):
            bord = i in (0, N - 1) or j in (0, N - 1)
            coin = i in (0, N - 1) and j in (0, N - 1)
            if not bord:
                st = "vide"
            elif mode == "corrige":
                st = "carreauO" if coin else "carreauV"
            else:
                st = "carreau"
            L.append(r"\filldraw[%s] (%s,%s) rectangle (%s,%s);"
                     % (st, f(x0 + i * u), f(j * u), f(x0 + (i + 1) * u), f((j + 1) * u)))
    L.append(r"\draw[otNavy,line width=.9pt] (%s,0) rectangle (%s,%s);" % (f(x0), f(x0 + N * u), f(N * u)))
    return L


def ex2866_enonce():
    u = .4
    L = []
    x = 0.0
    for n in (1, 2, 3):
        L += bordure(n, u, x)
        L.append(r"\node[etape,anchor=north] at (%s,-.22) {Étape %d};" % (f(x + (n + 2) * u / 2), n))
        x += (n + 2) * u + .75
    return tikz(L)


def ex2866_corrige():
    u = .62
    n = 3
    N = n + 2
    L = bordure(n, u, 0.0, "corrige")
    W = N * u
    # nombre de carreaux verts de chaque côté (hors coins)
    L.append(r"\node[text=%s,anchor=south] at (%s,%s) {$3$};" % (VERT, f(W / 2), f(W + .08)))
    L.append(r"\node[text=%s,anchor=north] at (%s,%s) {$3$};" % (VERT, f(W / 2), f(-.08)))
    L.append(r"\node[text=%s,anchor=east] at (%s,%s) {$3$};" % (VERT, f(-.1), f(W / 2)))
    L.append(r"\node[text=%s,anchor=west] at (%s,%s) {$3$};" % (VERT, f(W + .1), f(W / 2)))
    L.append(r"\node[petit,anchor=north,text=otGreenDark] at (%s,-.6) {en vert : 4 côtés de 3 carreaux};" % f(W / 2))
    L.append(r"\node[petit,anchor=north,text=otOrange!85!black] at (%s,-1.02) {en orange : 4 coins};" % f(W / 2))
    L.append(r"\node[text=%s,anchor=north] at (%s,-1.5) {$4 \times 3 + 4 = 16$ carreaux gris};" % (VERT, f(W / 2)))
    return tikz(L)


FIGURES["ex2866_enonce"] = ex2866_enonce()
FIGURES["ex2866_corrige"] = ex2866_corrige()


# ===================================================================== tables et chaises (2867)
def tables(n, t, x0, mode="enonce"):
    """n tables carrées accolées de côté t, une chaise par côté libre."""
    L = []
    cw, ch, e = .34, .2, .09   # chaise : largeur, épaisseur, écart à la table
    for k in range(n):
        L.append(r"\filldraw[table] (%s,0) rectangle (%s,%s);" % (f(x0 + k * t), f(x0 + (k + 1) * t), f(t)))
    st_lg = "chaiseV" if mode == "corrige" else "chaise"
    st_bout = "chaiseO" if mode == "corrige" else "chaise"
    for k in range(n):
        cx = x0 + (k + .5) * t
        L.append(r"\filldraw[%s] (%s,%s) rectangle (%s,%s);" % (st_lg, f(cx - cw / 2), f(t + e), f(cx + cw / 2), f(t + e + ch)))
        L.append(r"\filldraw[%s] (%s,%s) rectangle (%s,%s);" % (st_lg, f(cx - cw / 2), f(-e - ch), f(cx + cw / 2), f(-e)))
    L.append(r"\filldraw[%s] (%s,%s) rectangle (%s,%s);" % (st_bout, f(x0 - e - ch), f(t / 2 - cw / 2), f(x0 - e), f(t / 2 + cw / 2)))
    xr = x0 + n * t
    L.append(r"\filldraw[%s] (%s,%s) rectangle (%s,%s);" % (st_bout, f(xr + e), f(t / 2 - cw / 2), f(xr + e + ch), f(t / 2 + cw / 2)))
    return L


def ex2867_enonce():
    t = .62
    L = []
    x = 0.0
    for n, lab in ((1, "1 table"), (2, "2 tables"), (3, "3 tables")):
        L += tables(n, t, x)
        L.append(r"\node[etape,anchor=north] at (%s,-.42) {%s};" % (f(x + n * t / 2), lab))
        x += n * t + 1.0
    return tikz(L)


def ex2867_corrige():
    t = 1.0
    L = tables(3, t, 0.0, "corrige")
    L.append(r"\node[petit,anchor=south,text=otGreenDark] at (1.5,1.42) {en haut : 3 chaises};")
    L.append(r"\node[petit,anchor=north,text=otGreenDark] at (1.5,-.42) {en bas : 3 chaises};")
    L.append(r"\node[anchor=east,text=otOrange!85!black] at (-.42,.5) {$1$};")
    L.append(r"\node[anchor=west,text=otOrange!85!black] at (3.42,.5) {$1$};")
    L.append(r"\node[text=%s,anchor=north] at (1.5,-.95) {$2 \times 3 + 2 = 8$ chaises};" % VERT)
    return tikz(L)


FIGURES["ex2867_enonce"] = ex2867_enonce()
FIGURES["ex2867_corrige"] = ex2867_corrige()


# ===================================================================== programmes de calcul
def programme(etapes, expressions=None, titre=None, x0=0.0, largeur=3.4, nom="p", ecart=.42):
    """Programme vertical : boîtes reliées par des flèches ; expressions (en vert) à droite."""
    L = []
    for k, e in enumerate(etapes):
        if k == 0:
            L.append(r"\node[boite,minimum width=%scm] (%s0) at (%s,0) {%s};" % (f(largeur), nom, f(x0), e))
        else:
            L.append(r"\node[boite,minimum width=%scm,below=%scm of %s%d] (%s%d) {%s};"
                     % (f(largeur), f(ecart), nom, k - 1, nom, k, e))
            L.append(r"\draw[fleche] (%s%d.south) -- (%s%d.north);" % (nom, k - 1, nom, k))
        if expressions and expressions[k]:
            L.append(r"\node[anchor=west,text=%s] at ($(%s%d.east)+(.3,0)$) {%s};" % (VERT, nom, k, expressions[k]))
    if titre:
        L.append(r"\node[titreP,anchor=south] at ($(%s0.north)+(0,.12)$) {%s};" % (nom, titre))
    return L


FIGURES["cours_programme"] = tikz(programme(
    ["Choisir un nombre", "Ajouter $4$", "Multiplier par $5$"],
    ["$x$", "$x + 4$", r"$5(x + 4)$"], largeur=3.2))

ETAPES_A = ["Choisir un nombre", "Multiplier par $4$", "Ajouter $3$"]
ETAPES_B = ["Choisir un nombre", "Ajouter $3$", "Multiplier par $4$"]
FIGURES["ex2853_enonce"] = tikz(programme(ETAPES_A, titre="Programme A", nom="a", largeur=3.0)
                                + programme(ETAPES_B, titre="Programme B", nom="b", x0=3.45, largeur=3.0))
FIGURES["ex2853_A"] = tikz(programme(ETAPES_A, ["$x$", r"$4x$", r"$4x + 3$"], titre="Programme A", nom="a", largeur=3.3))
FIGURES["ex2853_B"] = tikz(programme(ETAPES_B, ["$x$", r"$x + 3$", r"$4(x + 3)$"], titre="Programme B", nom="b", largeur=3.3))

ETAPES_CUI = [r"Choisir le nombre\\de tables", "Ajouter $2$", "Multiplier par $2$"]
FIGURES["ex2867_programme"] = tikz(programme(ETAPES_CUI, largeur=3.4))
FIGURES["ex2867_programme_corrige"] = tikz(programme(ETAPES_CUI, ["$n$", "$n + 2$", r"$2(n + 2)$"], largeur=3.4))


# ===================================================================== feuilles de tableur
def tableur(colonnes, lignes, largeurs, active=None, barre=None, vert=None, surligne=None, h=.52):
    """Feuille de tableur.
    colonnes : lettres (A, B…) ; lignes : liste de lignes (textes), la 1re = en-têtes (ligne 1).
    largeurs : largeurs des colonnes (la colonne des numéros est ajoutée).
    active = (ligne, colonne) cellule sélectionnée (indices 1.. / 0..) ; barre = (nom, formule).
    vert = ensemble de (ligne, colonne) écrits en vert ; surligne = numéro de ligne surlignée en vert."""
    L = []
    wn = .55
    xs = [0.0, wn]
    for w in largeurs:
        xs.append(xs[-1] + w)
    R = len(lignes) + 1          # + ligne des lettres
    top = 0.0
    if barre:
        nomc, formule = barre
        yb = .2 + h
        L.append(r"\filldraw[fill=white,draw=otMuted!70,line width=.5pt] (0,%s) rectangle (%s,%s);" % (f(.2), f(xs[-1]), f(yb)))
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(1.05), f(.2), f(1.05), f(yb)))
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f(.525), f(.2 + h / 2), nomc))
        L.append(r"\node[petit,text=otMuted,font=\itshape] at (%s,%s) {fx};" % (f(1.35), f(.2 + h / 2)))
        if formule:
            coul = "otGreenDark" if vert and "barre" in vert else "otInk"
            L.append(r"\node[anchor=west,font=\otRegular\fontsize{9.5}{11}\selectfont,text=%s] at (%s,%s) {%s};"
                     % (coul, f(1.62), f(.2 + h / 2), formule))
    # fonds
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[-1]), f(top - h)))
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[1]), f(top - R * h)))
    if surligne:
        y0 = top - surligne * h
        L.append(r"\fill[otGreen!18] (%s,%s) rectangle (%s,%s);" % (f(xs[1]), f(y0), f(xs[-1]), f(y0 - h)))
    for k, c in enumerate(colonnes):
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f((xs[k + 1] + xs[k + 2]) / 2), f(top - h / 2), c))
    for r, ligne in enumerate(lignes):
        y = top - (r + 1) * h - h / 2
        L.append(r"\node[cellule] at (%s,%s) {%d};" % (f(wn / 2), f(y), r + 1))
        for k, v in enumerate(ligne):
            if not v:
                continue
            coul = "otGreenDark" if vert and (r + 1, k) in vert else "otInk"
            L.append(r"\node[text=%s] at (%s,%s) {%s};" % (coul, f((xs[k + 1] + xs[k + 2]) / 2), f(y), v))
    for r in range(R + 1):
        L.append(r"\draw[otMuted!70,line width=.5pt] (0,%s) -- (%s,%s);" % (f(top - r * h), f(xs[-1]), f(top - r * h)))
    for x in xs:
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x), f(top), f(x), f(top - R * h)))
    if active:
        r, k = active
        L.append(r"\draw[otNavy,line width=1.4pt] (%s,%s) rectangle (%s,%s);"
                 % (f(xs[k + 1]), f(top - r * h), f(xs[k + 2]), f(top - (r + 1) * h)))
    return L


# ---------------------------------------------------------------- cours : carrés d'allumettes
_cours_lignes = [["Étape", "Allumettes"]] + [["$%d$" % n, "$%d$" % (3 * n + 1)] for n in range(1, 6)]
FIGURES["cours_tableur"] = tikz(tableur(["A", "B"], _cours_lignes, [2.0, 2.4], active=(2, 1),
                                        barre=("B2", "=3*A2+1")))

# ---------------------------------------------------------------- 2859 : 3x + 4 et x²
_x = list(range(0, 6))
_l_en = [["$x$", "$3x + 4$", "$x^2$"]] + [["$%d$" % v, "", ""] for v in _x]
FIGURES["ex2859_enonce"] = tikz(tableur(["A", "B", "C"], _l_en, [1.5, 2.0, 2.0], active=(2, 1), barre=("B2", "")))
_l_co = [["$x$", "$3x + 4$", "$x^2$"]] + [["$%d$" % v, "$%d$" % (3 * v + 4), "$%d$" % (v * v)] for v in _x]
_vert = {(r, k) for r in range(2, 8) for k in (1, 2)} | {"barre"}
FIGURES["ex2859_corrige"] = tikz(tableur(["A", "B", "C"], _l_co, [1.5, 2.0, 2.0], active=(2, 1),
                                         barre=("B2", "=3*A2+4"), vert=_vert, surligne=6))

# ---------------------------------------------------------------- 2868 : le potager
_xp = [3, 4, 5, 6]
_p_en = [["$x$", "Périmètre", "Aire"]] + [["$%d$" % v, "", ""] for v in _xp]
FIGURES["ex2868_tableur_enonce"] = tikz(tableur(["A", "B", "C"], _p_en, [1.2, 2.25, 2.25], active=(2, 1),
                                                barre=("B2", "=2*A2+2*(A2+5)")))
_p_co = [["$x$", "Périmètre", "Aire"]] + [["$%d$" % v, "$%d$" % (2 * v + 2 * (v + 5)), "$%d$" % (v * (v + 5))] for v in _xp]
_vertp = {(r, k) for r in range(2, 6) for k in (1, 2)} | {"barre"}
FIGURES["ex2868_tableur_corrige"] = tikz(tableur(["A", "B", "C"], _p_co, [1.2, 2.25, 2.25], active=(2, 2),
                                                 barre=("C2", "=A2*(A2+5)"), vert=_vertp, surligne=5))


# ===================================================================== rectangles et figures
def rect_cotes(x0, y0, W, H, haut, gauche, fond="otSky", coul_txt="otInk", nom=None):
    """Rectangle avec une cote au-dessus et une cote à gauche (texte hors des traits)."""
    L = [r"\filldraw[fill=%s,draw=otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (fond, f(x0), f(y0), f(x0 + W), f(y0 + H)),
         r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 + .03), f(y0 + H + .3), f(x0 + W - .03), f(y0 + H + .3)),
         r"\node[anchor=south,text=%s] at (%s,%s) {%s};" % (coul_txt, f(x0 + W / 2), f(y0 + H + .36), haut),
         r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0 - .3), f(y0 + H - .03), f(x0 - .3), f(y0 + .03)),
         r"\node[anchor=east,text=%s] at (%s,%s) {%s};" % (coul_txt, f(x0 - .38), f(y0 + H / 2), gauche)]
    # angles droits
    a = .2
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x0 + W, y0, -1, 1), (x0 + W, y0 + H, -1, -1), (x0, y0 + H, 1, -1)):
        L.append(r"\draw[otNavy,line width=.55pt] (%s,%s) -- (%s,%s) -- (%s,%s);"
                 % (f(cx + dx * a), f(cy), f(cx + dx * a), f(cy + dy * a), f(cx), f(cy + dy * a)))
    if nom:
        L.append(r"\node[text=otNavy] at (%s,%s) {%s};" % (f(x0 + W / 2), f(y0 + H / 2), nom))
    return L


def codage_segment(x1, y1, x2, y2, n=1):
    """n petits traits perpendiculaires au milieu du segment (longueurs égales)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    vx, vy = -uy, ux
    out = []
    for i in range(n):
        d = (i - (n - 1) / 2) * .085
        cx, cy = mx + d * ux, my + d * uy
        out.append(r"\draw[otNavy,line width=.7pt] (%s,%s) -- (%s,%s);"
                   % (f(cx - .1 * vx), f(cy - .1 * vy), f(cx + .1 * vx), f(cy + .1 * vy)))
    return out


def polygone_regulier(cx, cy, r, n, rot, fond="otSky"):
    pts = [(cx + r * math.cos(math.radians(rot + 360 * k / n)), cy + r * math.sin(math.radians(rot + 360 * k / n)))
           for k in range(n)]
    L = [r"\filldraw[fill=%s,draw=otNavy,line width=.9pt,line join=round] %s -- cycle;"
         % (fond, " -- ".join("(%s,%s)" % (f(x), f(y)) for x, y in pts))]
    for k in range(n):
        x1, y1 = pts[k]
        x2, y2 = pts[(k + 1) % n]
        L += codage_segment(x1, y1, x2, y2)
    return L, pts


def carre_code(x0, y0, c, lettre, coul_txt="otInk"):
    L = [r"\filldraw[fill=otSky,draw=otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x0 + c), f(y0 + c))]
    for (x1, y1, x2, y2) in ((x0, y0, x0 + c, y0), (x0 + c, y0, x0 + c, y0 + c), (x0 + c, y0 + c, x0, y0 + c), (x0, y0 + c, x0, y0)):
        L += codage_segment(x1, y1, x2, y2)
    a = .2
    L.append(r"\draw[otNavy,line width=.55pt] (%s,%s) -- (%s,%s) -- (%s,%s);" % (f(x0 + a), f(y0), f(x0 + a), f(y0 + a), f(x0), f(y0 + a)))
    L.append(r"\node[anchor=north,text=%s] at (%s,%s) {%s};" % (coul_txt, f(x0 + c / 2), f(y0 - .14), lettre))
    return L


# ---------------------------------------------------------------- cours : rectangle et carré
def cours_rectangle():
    L = rect_cotes(0, 0, 3.0, 1.6, r"$L$", r"$\ell$")
    L.append(r"\node[petit,anchor=north] at (1.5,-.2) {rectangle};")
    L += carre_code(3.85, 0, 1.6, "$c$")
    L.append(r"\node[petit,anchor=north] at (4.65,-.62) {carré};")
    return tikz(L)


FIGURES["cours_rectangle"] = cours_rectangle()


# ---------------------------------------------------------------- 2856 : quatre figures
def ex2856(corrige):
    L = []
    Y = 3.5            # bas de la rangée du haut
    CG, CD = 1.2, 4.95  # centres des colonnes gauche et droite
    # carré (en haut à gauche)
    L += carre_code(CG - .75, Y, 1.5, "$c$")
    # rectangle (en haut à droite)
    L += rect_cotes(CD - 1.4, Y, 2.8, 1.5, "$L$", r"$\ell$")
    # triangle équilatéral (en bas à gauche)
    s = 1.9
    h = s * math.sqrt(3) / 2
    tx, ty = CG - s / 2, .0
    pts = [(tx, ty), (tx + s, ty), (tx + s / 2, ty + h)]
    L.append(r"\filldraw[fill=otSky,draw=otNavy,line width=.9pt,line join=round] (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
             % tuple(f(v) for p in pts for v in p))
    for k in range(3):
        x1, y1 = pts[k]
        x2, y2 = pts[(k + 1) % 3]
        L += codage_segment(x1, y1, x2, y2)
    L.append(r"\node[anchor=north] at (%s,%s) {$a$};" % (f(tx + s / 2), f(ty - .14)))
    # hexagone régulier (en bas à droite) : côté b, un côté horizontal en bas
    r = .95
    P, pts6 = polygone_regulier(CD, ty + r * math.sqrt(3) / 2, r, 6, 0)
    L += P
    L.append(r"\node[anchor=north] at (%s,%s) {$b$};" % (f(CD), f(ty - .14)))
    noms = [(CG, Y - .62, "carré"), (CD, Y - .57, "rectangle"),
            (CG, ty - .72, "triangle équilatéral"), (CD, ty - .72, "hexagone régulier")]
    if not corrige:
        for x, y, t in noms:
            L.append(r"\node[petit,anchor=north] at (%s,%s) {%s};" % (f(x), f(y), t))
        return tikz(L)
    form = [(CG, Y - .62, r"$P = 4c$\\$A = c^2$"),
            (CD, Y - .57, r"$P = 2L + 2\ell$\\$A = L\ell$"),
            (CG, ty - .72, r"$P = 3a$"),
            (CD, ty - .72, r"$P = 6b$")]
    for x, y, t in form:
        L.append(r"\node[anchor=north,align=center,text=%s] at (%s,%s) {%s};" % (VERT, f(x), f(y), t))
    return tikz(L)


FIGURES["ex2856_enonce"] = ex2856(False)
FIGURES["ex2856_corrige"] = ex2856(True)


# ---------------------------------------------------------------- 2868 : le potager
def ex2868_enonce():
    L = rect_cotes(0, 0, 4.4, 2.0, "$x + 5$", "$x$", fond="otGreen!14")
    L.append(r"\node[text=otGreenDark!80!black] at (2.2,1.0) {potager};")
    L.append(r"\node[petit,anchor=north] at (2.2,-.18) {(longueurs en mètres)};")
    return tikz(L)


def ex2868_corrige():
    L = rect_cotes(0, 0, 4.4, 2.0, r"$4 + 5 = 9$ m", "$4$ m", fond="otGreen!14", coul_txt=VERT)
    L.append(r"\node[text=otGreenDark!80!black] at (2.2,1.0) {potager pour $x = 4$};")
    L.append(r"\node[text=%s,anchor=north] at (2.2,-.2) {$P = 2 \times 4 + 2 \times 9 = 26$ m};" % VERT)
    L.append(r"\node[text=%s,anchor=north] at (2.2,-.78) {$A = 4 \times 9 = 36$ m$^2$};" % VERT)
    return tikz(L)


FIGURES["ex2868_enonce"] = ex2868_enonce()
FIGURES["ex2868_corrige"] = ex2868_corrige()
