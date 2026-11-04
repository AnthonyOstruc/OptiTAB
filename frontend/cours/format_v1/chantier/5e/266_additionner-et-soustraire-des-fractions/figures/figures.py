# -*- coding: utf-8 -*-
"""Figures de la notion 266 (5e : additionner et soustraire des fractions), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Barres et disques partagés, schémas en barres des problèmes, pyramide.
Convention : énoncé = données seules (parts vides ou parts données) ; corrigé =
parts additionnées en vert (otGreen / otGreenDark), part restante en blanc.
Outils repris de la notion 5e 265 (même style).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  part/.style={draw=otNavy,line width=.7pt},
  groupe/.style={draw=otNavy,line width=1.6pt},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  accolV/.style={otGreenDark,line width=.6pt,decorate,decoration={brace,amplitude=4pt}},
  brique/.style={draw=otNavy,line width=.7pt,minimum width=2.2cm,minimum height=1.05cm,inner sep=0pt},
}
"""


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


BLEU = "otNavy!28"
ORANGE = "otOrange!50"
ROSE = "otRed!28"
VERT = "otGreen!60"
VERT2 = "otGreen!30"
VERTF = "otGreenDark"
VERTS = "otGreen!85"
VERTC = "otGreen!15"
SAUT = r"\\"
ORF = "otOrange!85!black"


def tikz(lignes):
    return "\n".join([r"\begin{tikzpicture}"] + lignes + [r"\end{tikzpicture}"])


def fr(a, b):
    return r"$\dfrac{%d}{%d}$" % (a, b)


# ================================================================== outils
def barre(x, y, w, h, n, couleurs):
    """Barre de n parts égales ; couleurs : liste (None = blanc)."""
    s = []
    d = w / n
    for i in range(n):
        c = couleurs[i] if i < len(couleurs) and couleurs[i] else "white"
        s.append(r"\filldraw[fill=%s,part] (%s,%s) rectangle (%s,%s);" % (c, f(x + i * d), f(y), f(x + (i + 1) * d), f(y + h)))
    return "\n".join(s)


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


def accolade_dessous(x0, x1, y, texte, coul="otInk", dy=.12, style="accol"):
    texte = texte.replace(SAUT, SAUT + "[5pt]")
    return (r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x1), f(y - dy), f(x0), f(y - dy))
            + "\n" + r"\node[anchor=north,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y - dy - .2), texte))


def accolade_dessus(x0, x1, y, texte, coul="otInk", dy=.12, style="accol"):
    texte = texte.replace(SAUT, SAUT + "[5pt]")
    return (r"\draw[%s] (%s,%s) -- (%s,%s);" % (style, f(x0), f(y + dy), f(x1), f(y + dy))
            + "\n" + r"\node[anchor=south,text=%s,align=center] at (%s,%s) {%s};" % (coul, f((x0 + x1) / 2), f(y + dy + .2), texte))


def legende(x, y, coul, texte, couleur_texte="otInk"):
    """Petit carré de couleur suivi d'un texte (légende)."""
    return (r"\filldraw[fill=%s,part] (%s,%s) rectangle (%s,%s);" % (coul, f(x), f(y - .17), f(x + .34), f(y + .17))
            + "\n" + r"\node[anchor=west,text=%s] at (%s,%s) {%s};" % (couleur_texte, f(x + .5), f(y), texte))


FIGURES = {}

# ================================================================== COURS
# 1. 3/8 + 2/8 = 5/8
_W = 6.4
_d = _W / 8
_s = [barre(0, 0, _W, .7, 8, [BLEU] * 3 + [VERT] * 2)]
_s.append(accolade_dessus(0, 3 * _d, .7, fr(3, 8), "otNavy"))
_s.append(accolade_dessus(3 * _d, 5 * _d, .7, fr(2, 8), VERTF))
_s.append(accolade_dessous(0, 5 * _d, 0, r"$\dfrac{3}{8} + \dfrac{2}{8} = \dfrac{5}{8}$", VERTF, style="accolV"))
FIGURES["cours_meme_den"] = tikz(_s)

# 2. 2/3 + 1/6 = 4/6 + 1/6 = 5/6
_W = 5.2
_s = []
_s.append(barre(0, 0, _W, .6, 3, [BLEU] * 2))
_s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {%s};" % fr(2, 3))
_s.append(barre(0, -1.1, _W, .6, 6, [ORANGE]))
_s.append(r"\node[anchor=east,text=otInk] at (-.2,-.8) {%s};" % fr(1, 6))
_s.append(barre(0, -2.4, _W, .6, 6, [VERT] * 4 + [VERT2]))
_s.append(r"\node[anchor=east,text=%s] at (-.2,-2.1) {somme};" % VERTF)
_s.append(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt] (%s,-1.8) -- (%s,0);" % (f(_W * 2 / 3), f(_W * 2 / 3)))
_s.append(accolade_dessous(0, _W * 2 / 3, -2.4, r"$\dfrac{2}{3} = \dfrac{4}{6}$", VERTF, style="accolV"))
_s.append(accolade_dessous(_W * 2 / 3, _W * 5 / 6, -2.4, fr(1, 6), VERTF, style="accolV"))
_s.append(r"\node[anchor=north,text=%s] at (%s,-3.75) {$\dfrac{4}{6} + \dfrac{1}{6} = \dfrac{5}{6}$};" % (VERTF, f(_W / 2)))
FIGURES["cours_multiple"] = tikz(_s)

# 3. Le gâteau : Léa 1/6, Hugo 1/3 = 2/6, reste 1/2
_s = [disque(1.1, 0, 1.1, [VERT2, VERT, VERT, None, None, None])]
_s.append(legende(2.75, .75, VERT2, r"Léa : %s" % fr(1, 6)))
_s.append(legende(2.75, 0, VERT, r"Hugo : $\dfrac{1}{3} = \dfrac{2}{6}$"))
_s.append(legende(2.75, -.75, "white", r"reste : $\dfrac{3}{6} = \dfrac{1}{2}$"))
FIGURES["cours_gateau"] = tikz(_s)

# 4. Le terrain de 300 m² : potager 2/5 = 4/10, pelouse 3/10, fleurs 3/10
_W = 6.6
_d = _W / 10
_s = [barre(0, 0, _W, .7, 10, [VERT] * 4 + [VERT2] * 3)]
_s.append(accolade_dessus(0, _W, .7, r"le terrain : $300$ m²"))
_s.append(accolade_dessous(0, 4 * _d, 0, r"potager\\%s\\$120$ m²" % fr(4, 10), VERTF, style="accolV"))
_s.append(accolade_dessous(4 * _d, 7 * _d, 0, r"pelouse\\%s\\$90$ m²" % fr(3, 10), VERTF, style="accolV"))
_s.append(accolade_dessous(7 * _d, _W, 0, r"fleurs\\%s\\$90$ m²" % fr(3, 10), "otNavy"))
FIGURES["cours_terrain"] = tikz(_s)


# ================================================================== 2812 : barre en neuvièmes
def neuviemes(corrige):
    W = 6.3
    d = W / 9
    s = []
    if corrige:
        s.append(barre(0, 0, W, .7, 9, [VERT] * 6))
        s.append(r"\draw[groupe] (%s,0) -- (%s,.7);" % (f(3 * d), f(3 * d)))
        s.append(r"\draw[groupe] (%s,0) -- (%s,.7);" % (f(6 * d), f(6 * d)))
        s.append(r"\draw[groupe] (0,0) rectangle (%s,.7);" % f(W))
        s.append(accolade_dessus(0, 2 * d, .7, fr(2, 9), VERTF))
        s.append(accolade_dessus(2 * d, 6 * d, .7, fr(4, 9), VERTF))
        s.append(accolade_dessous(0, 6 * d, 0, r"$\dfrac{2}{9} + \dfrac{4}{9} = \dfrac{6}{9} = \dfrac{2}{3}$", VERTF, style="accolV"))
    else:
        s.append(barre(0, 0, W, .7, 9, [BLEU] * 2 + [ORANGE] * 4))
    return tikz(s)


FIGURES["neuviemes_enonce"] = neuviemes(False)
FIGURES["neuviemes_corrige"] = neuviemes(True)


# ================================================================== 2814 : quarts et huitièmes
def quarts_huitiemes(corrige):
    W = 5.4
    d = W / 8
    s = []
    s.append(barre(0, 0, W, .6, 4, [BLEU]))
    s.append(r"\node[anchor=east,text=otInk] at (-.2,.3) {barre A};")
    s.append(barre(0, -1.1, W, .6, 8, [BLEU] * 3))
    s.append(r"\node[anchor=east,text=otInk] at (-.2,-.8) {barre B};")
    if corrige:
        s.append(barre(0, -2.4, W, .6, 8, [VERT] * 2 + [VERT2] * 3))
        s.append(r"\node[anchor=east,text=%s] at (-.2,-2.1) {somme};" % VERTF)
        s.append(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt] (%s,-1.8) -- (%s,0);" % (f(2 * d), f(2 * d)))
        s.append(accolade_dessous(0, 5 * d, -2.4, r"$\dfrac{2}{8} + \dfrac{3}{8} = \dfrac{5}{8}$", VERTF, style="accolV"))
    return tikz(s)


FIGURES["quarts_enonce"] = quarts_huitiemes(False)
FIGURES["quarts_corrige"] = quarts_huitiemes(True)


# ================================================================== 2810 : réservoir de 60 L en douzièmes
def reservoir(corrige):
    W = 6.8
    d = W / 12
    s = []
    if corrige:
        s.append(barre(0, 0, W, .7, 12, [VERT] * 3 + [VERT2] * 5))
        s.append(accolade_dessus(0, 8 * d, .7, r"utilisé : $\dfrac{8}{12} = \dfrac{2}{3}$, soit $40$ L", VERTF, style="accolV"))
        s.append(accolade_dessous(0, 3 * d, 0, r"matin\\%s\\$15$ L" % fr(3, 12), VERTF, style="accolV"))
        s.append(accolade_dessous(3 * d, 8 * d, 0, r"après-midi\\%s\\$25$ L" % fr(5, 12), VERTF, style="accolV"))
        s.append(accolade_dessous(8 * d, W, 0, r"reste\\$\dfrac{4}{12} = \dfrac{1}{3}$\\$20$ L", "otNavy"))
    else:
        s.append(barre(0, 0, W, .7, 12, []))
        s.append(accolade_dessus(0, W, .7, r"la réserve : $60$ L"))
    return tikz(s)


FIGURES["reservoir_enonce"] = reservoir(False)
FIGURES["reservoir_corrige"] = reservoir(True)


# ================================================================== 2818 : pyramide
def pyramide(corrige):
    L, H = 2.2, 1.05
    base = [fr(1, 6), fr(1, 3), fr(5, 12)]
    milieu = [fr(1, 2), fr(3, 4)] if corrige else ["", ""]
    sommet = [fr(5, 4)] if corrige else [""]
    s = []
    for j, (ligne, coul) in enumerate([(base, "otInk"), (milieu, VERTF), (sommet, VERTF)]):
        n = len(ligne)
        x0 = j * L / 2
        for i, t in enumerate(ligne):
            x = x0 + i * L + L / 2
            y = j * H + H / 2
            fill = "otGreen!14" if (corrige and j > 0) else "white"
            s.append(r"\node[brique,fill=%s,text=%s] at (%s,%s) {%s};" % (fill, coul, f(x), f(y), t))
    return tikz(s)


FIGURES["pyramide_enonce"] = pyramide(False)
FIGURES["pyramide_corrige"] = pyramide(True)


# ================================================================== 2830 : bouteille de 3/2 L en huitièmes
def bouteille(corrige):
    W = 6.8
    d = W / 12
    s = []
    if corrige:
        s.append(barre(0, 0, W, .7, 12, [VERT] * 4 + [VERT2] * 3))
        s.append(accolade_dessus(0, 7 * d, .7, r"servi : $\dfrac{4}{8} + \dfrac{3}{8} = \dfrac{7}{8}$ L", VERTF, style="accolV"))
        s.append(accolade_dessous(0, 4 * d, 0, r"Léo\\$\dfrac{1}{2} = \dfrac{4}{8}$ L", VERTF, style="accolV"))
        s.append(accolade_dessous(4 * d, 7 * d, 0, r"Mia\\%s L" % fr(3, 8), VERTF, style="accolV"))
        s.append(accolade_dessous(7 * d, W, 0, r"reste\\$\dfrac{12}{8} - \dfrac{7}{8} = \dfrac{5}{8}$ L", "otNavy"))
    else:
        s.append(barre(0, 0, W, .7, 12, []))
        s.append(accolade_dessus(0, W, .7, r"la bouteille : %s L" % fr(3, 2)))
        s.append(r"\draw[accol] (%s,-.12) -- (0,-.12);" % f(d))
        s.append(r"\node[anchor=north west,text=otMuted,inner sep=0pt] at (0,-.4) {$1$ case : %s L};" % fr(1, 8))
    return tikz(s)


FIGURES["bouteille_enonce"] = bouteille(False)
FIGURES["bouteille_corrige"] = bouteille(True)


# ================================================================== 2824 : roman de 240 pages en douzièmes
def livre(corrige):
    W = 6.8
    d = W / 12
    s = []
    if corrige:
        s.append(barre(0, 0, W, .7, 12, [VERT] * 4 + [VERT2] * 5 + [VERT] * 2))
        s.append(r"\draw[accol] (%s,.82) -- (%s,.82);" % (f(11 * d), f(W)))
        s.append(r"\node[anchor=south east,text=otNavy] at (%s,1.1) {reste : %s, soit $20$ pages};" % (f(W), fr(1, 12)))
        s.append(accolade_dessous(0, 4 * d, 0, r"lundi\\%s" % fr(4, 12), VERTF, style="accolV"))
        s.append(accolade_dessous(4 * d, 9 * d, 0, r"mardi\\%s" % fr(5, 12), VERTF, style="accolV"))
        s.append(accolade_dessous(9 * d, 11 * d, 0, r"mercredi\\%s" % fr(2, 12), VERTF, style="accolV"))
    else:
        s.append(barre(0, 0, W, .7, 12, []))
        s.append(accolade_dessus(0, W, .7, r"le livre : $240$ pages"))
    return tikz(s)


FIGURES["livre_enonce"] = livre(False)
FIGURES["livre_corrige"] = livre(True)


# ================================================================== 2815 : activités du club (disque en huitièmes)
def club(corrige):
    s = []
    if corrige:
        cols = [VERTS] * 4 + [VERT2] * 2 + [VERTC] + [None]
        s.append(disque(1.15, 0, 1.15, cols))
        s.append(legende(2.7, 1.05, VERTS, r"sport : $\dfrac{1}{2} = \dfrac{4}{8}$"))
        s.append(legende(2.7, .35, VERT2, r"théâtre : $\dfrac{1}{4} = \dfrac{2}{8}$"))
        s.append(legende(2.7, -.35, VERTC, r"musique : %s" % fr(1, 8)))
        s.append(legende(2.7, -1.05, "white", r"échecs : %s ($5$ élèves)" % fr(1, 8)))
    else:
        cols = [BLEU] * 4 + [ORANGE] * 2 + [ROSE] + [None]
        s.append(disque(1.15, 0, 1.15, cols))
        s.append(legende(2.7, 1.05, BLEU, "sport"))
        s.append(legende(2.7, .35, ORANGE, "théâtre"))
        s.append(legende(2.7, -.35, ROSE, "musique"))
        s.append(legende(2.7, -1.05, "white", "échecs"))
    return tikz(s)


FIGURES["club_enonce"] = club(False)
FIGURES["club_corrige"] = club(True)


# ================================================================== 2811 : randonnée de 18 km en neuvièmes
def rando(corrige):
    W = 6.6
    d = W / 9
    s = []
    if corrige:
        s.append(barre(0, 0, W, .7, 9, [VERT] * 4 + [VERT2] * 3))
        s.append(accolade_dessus(0, 7 * d, .7, r"avant le goûter : $\dfrac{4}{9} + \dfrac{3}{9} = \dfrac{7}{9}$", VERTF, style="accolV"))
        s.append(accolade_dessous(0, 4 * d, 0, r"matin\\%s\\$8$ km" % fr(4, 9), VERTF, style="accolV"))
        s.append(accolade_dessous(4 * d, 7 * d, 0, r"après-midi\\%s\\$6$ km" % fr(3, 9), VERTF, style="accolV"))
        s.append(accolade_dessous(7 * d, W, 0, r"reste\\%s\\$4$ km" % fr(2, 9), "otNavy"))
    else:
        s.append(barre(0, 0, W, .7, 9, []))
        s.append(accolade_dessus(0, W, .7, r"le parcours : $18$ km"))
    return tikz(s)


FIGURES["rando_enonce"] = rando(False)
FIGURES["rando_corrige"] = rando(True)
