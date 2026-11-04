# -*- coding: utf-8 -*-
"""Figures de la notion 267 (5e : carrés et cubes), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Carrés en quadrillage (aire et côté), cubes empilés en perspective cavalière
(volume), motifs de points qui grandissent, pavage d'une terrasse, boîte remplie
de petits cubes, agrandissements, programmes de calcul.
Convention : énoncé = figure sans la réponse ; corrigé = éléments comptés en
vert (otGreen / otGreenDark).
Fonction de quadrillage reprise de la notion 4e 254 (carrés et racines carrées).
"""
from math import cos, sin, radians

PREAMBULE_EXTRA = r"""
\tikzset{
  titre/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,text=otNavy,inner sep=1pt,align=center},
  leg/.style={text=otInk,align=center,inner sep=1pt},
  legV/.style={text=otGreenDark,align=center,inner sep=1pt},
  fleche/.style={otMuted,line width=.7pt,-{Stealth[length=2mm]}},
  boite/.style={draw=otNavy,line width=.8pt,rounded corners=2pt,inner sep=4pt,minimum height=6mm,fill=otSky},
  boiteV/.style={draw=otGreenDark,line width=.8pt,rounded corners=2pt,inner sep=4pt,minimum height=6mm,fill=otGreen!14,text=otGreenDark},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
}
"""

VERTF = "otGreenDark"
FIGURES = {}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


def cote_h(x0, x1, y, texte, coul="otInk", dessous=True):
    """Cote horizontale de x0 à x1 à la hauteur y ; texte sous (ou sur) la flèche, jamais dessus."""
    a = "north" if dessous else "south"
    dy = -.06 if dessous else .06
    return [r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x0), f(y), f(x1), f(y)),
            r"\node[anchor=%s,text=%s,inner sep=1pt] at (%s,%s) {%s};" % (a, coul, f((x0 + x1) / 2), f(y + dy), texte)]


def cote_v(x, y0, y1, texte, coul="otInk", gauche=True):
    """Cote verticale ; texte à gauche (ou à droite) de la flèche."""
    a = "east" if gauche else "west"
    dx = -.06 if gauche else .06
    return [r"\draw[cote] (%s,%s) -- (%s,%s);" % (f(x), f(y0), f(x), f(y1)),
            r"\node[anchor=%s,text=%s,inner sep=1pt,align=center] at (%s,%s) {%s};" % (a, coul, f(x + dx), f((y0 + y1) / 2), texte)]


# ================================================================== carrés en quadrillage
def carre_quadrille(x, y, n, u, fond="otSky", grille="otNavy!35", bord="otNavy", blocs=None):
    """Carré de n × n carreaux de u cm, coin inférieur gauche (x, y).

    blocs = (b, couleurs) : partage en blocs b × b remplis de couleurs alternées, traits épais entre blocs.
    """
    c = n * u
    L = []
    if blocs:
        b, coul = blocs
        for i in range(n // b):
            for j in range(n // b):
                L.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);"
                         % (coul[(i + j) % len(coul)], f(x + i * b * u), f(y + j * b * u), f(x + (i + 1) * b * u), f(y + (j + 1) * b * u)))
    else:
        L.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (fond, f(x), f(y), f(x + c), f(y + c)))
    for k in range(1, n):
        L.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (grille, f(x + k * u), f(y), f(x + k * u), f(y + c)))
        L.append(r"\draw[%s,line width=.4pt] (%s,%s) -- (%s,%s);" % (grille, f(x), f(y + k * u), f(x + c), f(y + k * u)))
    if blocs:
        b = blocs[0]
        for k in range(b, n, b):
            L.append(r"\draw[%s,line width=1pt] (%s,%s) -- (%s,%s);" % (bord, f(x + k * u), f(y), f(x + k * u), f(y + c)))
            L.append(r"\draw[%s,line width=1pt] (%s,%s) -- (%s,%s);" % (bord, f(x), f(y + k * u), f(x + c), f(y + k * u)))
    L.append(r"\draw[%s,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (bord, f(x), f(y), f(x + c), f(y + c)))
    return L


def rangee_carres(cotes, u, gap, etiquettes, coul="otInk", fond="otSky", grille="otNavy!35"):
    """Carrés de côtés donnés (en carreaux), alignés en bas ; étiquette sous chacun."""
    L, x = [], 0.0
    for n, e in zip(cotes, etiquettes):
        L += carre_quadrille(x, 0, n, u, fond=fond, grille=grille)
        L.append(r"\node[anchor=north,text=%s,align=center] at (%s,-.14) {%s};" % (coul, f(x + n * u / 2), e))
        x += n * u + gap
    return L


# ================================================================== cubes empilés (perspective cavalière)
K, ANG = .5, 40   # coefficient et angle de fuite


def proj(x0, y0, u, X, Y, Z):
    return (x0 + u * (X + K * Y * cos(radians(ANG))), y0 + u * (Z + K * Y * sin(radians(ANG))))


COUL = {  # (face avant, dessus, côté droit)
    "bleu": ("otNavy!20", "otNavy!8", "otNavy!36"),
    "vert": ("otGreen!50", "otGreen!25", "otGreen!72"),
    "vertc": ("otGreen!28", "otGreen!12", "otGreen!45"),
}


def empilement(x0, y0, nx, ny, nz, u, vert=None, bloc=None, grille=True):
    """Pavé de nx × ny × nz petits cubes d'arête u (coin avant bas gauche en (x0, y0)).

    vert(face, a, b) -> None / "vert" / "vertc" : couleur d'un petit carré visible
    (face 'av' : a = colonne, b = rangée ; 'de' : a = colonne, b = profondeur ;
    'dr' : a = profondeur, b = rangée). bloc = b : traits épais tous les b cubes.
    """
    P = lambda X, Y, Z: "(%s,%s)" % tuple(f(v) for v in proj(x0, y0, u, X, Y, Z))
    L = []

    def face(nom, a, b, pts):
        c = (vert(nom, a, b) if vert else None) or "bleu"
        idx = {"av": 0, "de": 1, "dr": 2}[nom]
        trait = "otNavy!70" if grille else COUL[c][idx]
        L.append(r"\filldraw[fill=%s,draw=%s,line width=.4pt,line join=round] %s -- cycle;"
                 % (COUL[c][idx], trait, " -- ".join(P(*p) for p in pts)))

    for i in range(nx):
        for k in range(nz):
            face("av", i, k, [(i, 0, k), (i + 1, 0, k), (i + 1, 0, k + 1), (i, 0, k + 1)])
    for i in range(nx):
        for j in range(ny):
            face("de", i, j, [(i, j, nz), (i + 1, j, nz), (i + 1, j + 1, nz), (i, j + 1, nz)])
    for j in range(ny):
        for k in range(nz):
            face("dr", j, k, [(nx, j, k), (nx, j + 1, k), (nx, j + 1, k + 1), (nx, j, k + 1)])
    if bloc:
        ep = r"\draw[otNavy,line width=.95pt] %s -- %s;"
        for i in range(bloc, nx, bloc):
            L.append(ep % (P(i, 0, 0), P(i, 0, nz)))
            L.append(ep % (P(i, 0, nz), P(i, ny, nz)))
        for k in range(bloc, nz, bloc):
            L.append(ep % (P(0, 0, k), P(nx, 0, k)))
            L.append(ep % (P(nx, 0, k), P(nx, ny, k)))
        for j in range(bloc, ny, bloc):
            L.append(ep % (P(0, j, nz), P(nx, j, nz)))
            L.append(ep % (P(nx, j, 0), P(nx, j, nz)))
    # contour extérieur
    L.append(r"\draw[otNavy,line width=.9pt,line join=round] %s -- %s -- %s -- %s -- %s -- %s -- cycle;"
             % (P(0, 0, 0), P(nx, 0, 0), P(nx, ny, 0), P(nx, ny, nz), P(0, ny, nz), P(0, 0, nz)))
    L.append(r"\draw[otNavy,line width=.9pt,line join=round] %s -- %s -- %s %s -- %s;"
             % (P(0, 0, nz), P(nx, 0, nz), P(nx, ny, nz), P(nx, 0, nz), P(nx, 0, 0)))
    return L


def haut(x0, y0, n, u):
    """Ordonnée du sommet d'un empilement n × n × n."""
    return proj(x0, y0, u, 0, n, n)[1]


def largeur(n, u):
    return proj(0, 0, u, n, n, 0)[0]


def couche_haut(n):
    return lambda face, a, b: "vert" if (face == "de" or b == n - 1) else None


# ================================================================== COURS
# 1. Carré de 5 carreaux de côté
_u = .5
FIGURES["cours_carre5"] = tikz(
    carre_quadrille(0, 0, 5, _u)
    + cote_h(0, 5 * _u, -.3, r"côté : $5$ carreaux")
    + [r"\node[anchor=west,leg] at (%s,%s) {$5 \times 5 = 5^2$\\$= 25$ carreaux};" % (f(5 * _u + .45), f(5 * _u / 2))])

# 2. Cube de 4 petits cubes d'arête : une couche en vert
_u = .55
_s = empilement(0, 0, 4, 4, 4, _u, vert=couche_haut(4))
_s += cote_h(0, 4 * _u, -.3, r"arête : $4$ petits cubes")
_xd = largeur(4, _u) + .35
_s.append(r"\node[anchor=west,legV] at (%s,%s) {une couche :\\$4 \times 4 = 16$ cubes};" % (f(_xd), f(haut(0, 0, 4, _u) - .25)))
_s.append(r"\node[anchor=west,leg] at (%s,%s) {$4$ couches :\\$4 \times 4 \times 4 = 4^3$\\$= 64$ petits cubes};" % (f(_xd), f(.75)))
FIGURES["cours_cube4"] = tikz(_s)

# 3. Un cube de 1 dm d'arête rempli de cubes de 1 cm
_u = .3
_s = empilement(0, 0, 10, 10, 10, _u)
_s += cote_h(0, 10 * _u, -.3, r"$1$ dm $= 10$ cm")
_s += cote_v(-.3, 0, 10 * _u, r"$10$\\cm")
_s.append(r"\node[anchor=north,leg] at (%s,-.95) {$10 \times 10 \times 10 = 10^3 = 1\,000$ cubes de $1$ cm³};"
          % f(largeur(10, _u) / 2))
FIGURES["cours_dm3"] = tikz(_s)

# 4. Schéma général : carré de côté c, cube d'arête c (cours et fiche)
_c = 2.0
_s = [r"\draw[otNavy,line width=.9pt,fill=otSky] (0,0) rectangle (%s,%s);" % (f(_c), f(_c)),
      r"\node[text=otNavy] at (%s,%s) {aire $c^2$};" % (f(_c / 2), f(_c / 2))]
_s += cote_h(0, _c, -.3, r"$c$")
_x = _c + 1.3
_s += empilement(_x, 0, 1, 1, 1, _c, grille=False)
_s += cote_h(_x, _x + _c, -.3, r"$c$")
_s.append(r"\node[text=otNavy] at (%s,%s) {volume $c^3$};" % (f(_x + _c / 2), f(_c / 2)))
FIGURES["schema_carre_cube"] = tikz(_s)


# ================================================================== 2831 : carreaux et petits cubes
_u = .45
FIGURES["ex2831_carres_enonce"] = tikz(rangee_carres(
    [1, 2, 3, 4], _u, .9, [r"côté $1$", r"côté $2$", r"côté $3$", r"côté $4$"], coul="otMuted"))
FIGURES["ex2831_carres_corrige"] = tikz(rangee_carres(
    [1, 2, 3, 4], _u, .9, [r"$1^2 = 1$", r"$2^2 = 4$", r"$3^2 = 9$", r"$4^2 = 16$"],
    coul=VERTF, fond="otGreen!28", grille="otGreenDark!45"))


def cubes_2831(corrige):
    u, gap, x, s = .5, .85, 0.0, []
    for n in (1, 2, 3):
        s += empilement(x, 0, n, n, n, u, vert=couche_haut(n) if corrige else None)
        if corrige:
            txt = [r"$1^3 = 1$", r"$2 \times 2 \times 2$\\$= 2^3 = 8$", r"$3 \times 3 \times 3$\\$= 3^3 = 27$"][n - 1]
            s.append(r"\node[anchor=north,legV] at (%s,-.14) {%s};" % (f(x + n * u / 2), txt))
        else:
            s.append(r"\node[anchor=north,text=otMuted] at (%s,-.14) {arête $%d$};" % (f(x + n * u / 2), n))
        x += largeur(n, u) + gap
    return tikz(s)


FIGURES["ex2831_cubes_enonce"] = cubes_2831(False)
FIGURES["ex2831_cubes_corrige"] = cubes_2831(True)


# ================================================================== 2835 : motif de points
def motif(n, x0, s=.34, vert_ajout=False, r="2.3pt"):
    L = []
    for i in range(n):
        for j in range(n):
            c = "otGreenDark" if (vert_ajout and (i == n - 1 or j == n - 1)) else "otNavy"
            L.append(r"\fill[%s] (%s,%s) circle (%s);" % (c, f(x0 + i * s), f(j * s), r))
    return L


_s, _x = [], 0.0
for _n in (1, 2, 3, 4):
    _s += motif(_n, _x)
    _s.append(r"\node[anchor=north,text=otMuted] at (%s,-.3) {étape $%d$};" % (f(_x + (_n - 1) * .34 / 2), _n))
    _x += (_n - 1) * .34 + 1.15
FIGURES["ex2835_enonce"] = tikz(_s)

_s = motif(4, 0)
_s.append(r"\node[anchor=north,leg] at (%s,-.3) {étape $4$ :\\$4^2 = 16$ points};" % f(3 * .34 / 2))
_x5 = 3 * .34 + 2.4
_s.append(r"\draw[fleche] (%s,%s) -- (%s,%s);" % (f(3 * .34 + .45), f(1.5 * .34), f(_x5 - .45), f(1.5 * .34)))
_s += motif(5, _x5, vert_ajout=True)
_s.append(r"\node[anchor=north,legV] at (%s,-.3) {étape $5$ : $16 + 9$\\$= 25 = 5^2$ points};" % f(_x5 + 4 * .34 / 2))
_s.append(r"\node[anchor=west,legV] at (%s,%s) {$9$ points\\ajoutés};" % (f(_x5 + 4 * .34 + .4), f(2 * .34)))
FIGURES["ex2835_corrige"] = tikz(_s)


# ================================================================== 2845 : la terrasse
_u = .4   # 0,5 m -> 0,4 cm de dessin
_c = 9 * _u
_s = [r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(_c), f(_c)),
      r"\filldraw[fill=otNavy!30,draw=otNavy,line width=.6pt] (0,0) rectangle (%s,%s);" % (f(_u), f(_u)),
      r"\draw[otNavy,line width=.9pt] (0,0) rectangle (%s,%s);" % (f(_c), f(_c)),
      r"\node[anchor=west,leg] (d) at (%s,%s) {une dalle :\\$0{,}5$ m de côté};" % (f(_c + .45), f(.75)),
      r"\draw[otMuted,line width=.5pt,-{Stealth[length=1.6mm]}] (d.west) -- (%s,%s);" % (f(_u + .06), f(_u / 2 + .03)),
      r"\node[text=otNavy] at (%s,%s) {terrasse};" % (f(_c / 2), f(_c / 2 + .2))]
_s += cote_h(0, _c, -.3, r"$4{,}5$ m")
_s += cote_v(-.3, 0, _c, r"$4{,}5$ m")
FIGURES["ex2845_enonce"] = tikz(_s)

_s = carre_quadrille(0, 0, 9, _u, fond="otGreen!30", grille="otGreenDark!60")
_s += cote_h(0, _c, -.3, r"$9$ dalles", coul=VERTF)
_s += cote_v(-.3, 0, _c, r"$9$\\dalles", coul=VERTF)
_s.append(r"\node[anchor=west,legV] at (%s,%s) {$9$ rangées\\de $9$ dalles :\\$9 \times 9 = 9^2$\\$= 81$ dalles};" % (f(_c + .4), f(_c / 2)))
FIGURES["ex2845_corrige"] = tikz(_s)


# ================================================================== 2851 : la boîte cubique
def boite_fil(x0, y0, n, u):
    """Cube vide (arêtes cachées en pointillés)."""
    P = lambda X, Y, Z: "(%s,%s)" % tuple(f(v) for v in proj(x0, y0, u, X, Y, Z))
    a = n
    return [
        r"\fill[otSky] %s -- %s -- %s -- %s -- %s -- %s -- cycle;" % (P(0, 0, 0), P(a, 0, 0), P(a, a, 0), P(a, a, a), P(0, a, a), P(0, 0, a)),
        r"\draw[cache] %s -- %s -- %s %s -- %s;" % (P(0, 0, 0), P(0, a, 0), P(a, a, 0), P(0, a, 0), P(0, a, a)),
        r"\draw[otNavy,line width=.9pt,line join=round] %s -- %s -- %s -- %s -- %s -- %s -- cycle;"
        % (P(0, 0, 0), P(a, 0, 0), P(a, a, 0), P(a, a, a), P(0, a, a), P(0, 0, a)),
        r"\draw[otNavy,line width=.9pt,line join=round] %s -- %s -- %s %s -- %s;" % (P(0, 0, a), P(a, 0, a), P(a, a, a), P(a, 0, a), P(a, 0, 0)),
    ]


_u = .5   # 5 cm -> 0,5 cm de dessin
_s = boite_fil(0, 0, 6, _u)
_s += cote_h(0, 6 * _u, -.3, r"$30$ cm")
_xp = largeur(6, _u) + .9
_s += empilement(_xp, 0, 1, 1, 1, _u)
_s += cote_h(_xp, _xp + _u, -.3, r"$5$ cm")
_s.append(r"\node[anchor=south,leg] at (%s,%s) {un petit\\cube};" % (f(_xp + largeur(1, _u) / 2), f(haut(0, 0, 1, _u) + .15)))
_s.append(r"\node[anchor=south,leg] at (%s,%s) {la boîte (vide)};" % (f(largeur(6, _u) / 2), f(haut(0, 0, 6, _u) + .12)))
FIGURES["ex2851_enonce"] = tikz(_s)

_s = empilement(0, 0, 6, 6, 6, _u, vert=couche_haut(6))
_s += cote_h(0, 6 * _u, -.3, r"$6$ petits cubes", coul=VERTF)
_xd = largeur(6, _u) + .35
_s.append(r"\node[anchor=west,legV] at (%s,%s) {couche du haut :\\$6 \times 6 = 6^2 = 36$};" % (f(_xd), f(haut(0, 0, 6, _u) - .3)))
_s.append(r"\node[anchor=west,leg] at (%s,%s) {$6$ couches :\\$6 \times 6 \times 6 = 6^3$\\$= 216$ petits cubes};" % (f(_xd), f(1.0)))
FIGURES["ex2851_corrige"] = tikz(_s)


# ================================================================== 2849 : agrandir un carré et un cube
_u = .5
_s = carre_quadrille(0, 0, 3, _u)
_s += cote_h(0, 3 * _u, -.3, r"$3$ cm")
_s.append(r"\node[anchor=south,leg] at (%s,%s) {le carré};" % (f(1.5 * _u), f(3 * _u + .12)))
_x = 3 * _u + 1.4
_s += empilement(_x, 0, 2, 2, 2, _u)
_s += cote_h(_x, _x + 2 * _u, -.3, r"$2$ cm")
_s.append(r"\node[anchor=south,leg] at (%s,%s) {le cube};" % (f(_x + largeur(2, _u) / 2), f(haut(0, 0, 2, _u) + .12)))
FIGURES["ex2849_enonce"] = tikz(_s)

_s = carre_quadrille(0, 0, 6, _u, blocs=(3, ["otGreen!45", "otGreen!20"]), grille="otGreenDark!45")
_s += cote_h(0, 6 * _u, -.3, r"$6$ cm")
_s.append(r"\node[anchor=west,legV] at (%s,%s) {$4$ carrés de $9$ cm²\\$36$ cm² $= 4 \times 9$ cm²};" % (f(6 * _u + .4), f(3 * _u)))
FIGURES["ex2849_carre_corrige"] = tikz(_s)


def bloc_alterne(face, a, b):
    """Gros cubes de 2 cm (empilement 2 × 2 × 2) : deux verts alternés."""
    if face == "av":
        i, j, k = a, 0, b
    elif face == "de":
        i, j, k = a, b, 1
    else:
        i, j, k = 1, a, b
    return "vert" if (i + j + k) % 2 == 0 else "vertc"


_s = empilement(0, 0, 2, 2, 2, 2 * _u, vert=bloc_alterne)
_s += cote_h(0, 4 * _u, -.3, r"$4$ cm")
_s.append(r"\node[anchor=west,legV] at (%s,%s) {$8$ cubes de $2$ cm d'arête\\(un est caché derrière),\\chacun de $8$ cm³ :\\$8 \times 8 = 64$ cm³};"
          % (f(largeur(4, _u) + .4), f(haut(0, 0, 4, _u) / 2)))
FIGURES["ex2849_cube_corrige"] = tikz(_s)


# ================================================================== 2847 : deux programmes de calcul
def chaine(y, depart, ops, valeurs, titre):
    """Programme de calcul en ligne : depart -> op -> valeur ... (valeurs en vert)."""
    s = [r"\node[anchor=west,titre] at (0,%s) {%s};" % (f(y + .75), titre)]
    x = 0.0
    s.append(r"\node[boite,anchor=west] (n0) at (%s,%s) {$%s$};" % (f(x), f(y), depart))
    for k, (op, v) in enumerate(zip(ops, valeurs), start=1):
        s.append(r"\node[boiteV,anchor=west] (n%d) at ($(n%d.east)+(1.55,0)$) {$%s$};" % (k, k - 1, v))
        s.append(r"\draw[fleche] ($(n%d.east)+(.08,0)$) -- ($(n%d.west)+(-.08,0)$);" % (k - 1, k))
        s.append(r"\node[anchor=south,text=otNavy,inner sep=1pt] at ($(n%d.east)!.5!(n%d.west)+(0,.1)$) {%s};" % (k - 1, k, op))
    return s


_s = chaine(0, "5", [r"au carré", r"$\times 3$", r"$- 7$"], ["25", "75", "68"], r"Programme A")
_s += chaine(-1.9, "5", [r"$\times 3$", r"au carré", r"$- 7$"], ["15", "225", "218"], r"Programme B")
FIGURES["ex2847_corrige"] = tikz(_s)
