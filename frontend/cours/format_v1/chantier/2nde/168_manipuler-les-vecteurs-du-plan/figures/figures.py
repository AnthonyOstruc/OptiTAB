# -*- coding: utf-8 -*-
"""Figures de la notion « Manipuler les vecteurs du plan » (Seconde), style des livres.

Compilées par outils/figures_livre.py. Vecteurs : traits épais à pointe
Stealth (bleu marine = données, orange = vecteur recopié, vert foncé = réponse) ;
repères : quadrillage pâle, axes gris, graduations Montserrat.
Les étiquettes sont posées perpendiculairement au vecteur, dans l'espace libre
(ancre numérique = direction opposée au décalage).
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grille/.style={otRule!75,line width=.35pt},
  grad/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  vec/.style={line width=1.2pt,line cap=round,-{Stealth[length=2.7mm,width=2.1mm]}},
  lab/.style={text=otInk,inner sep=0pt},
  aide/.style={otMuted,line width=.65pt,dash pattern=on 3pt off 2pt},
  aideV/.style={otGreenDark,line width=.8pt,dash pattern=on 3.5pt off 2pt},
  cot/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
}
"""


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def num(k):
    return ("$%d$" % k)


def repere(x0, x1, y0, y1, xt=(), yt=(), axes=True, origine=True, noms=True):
    """Quadrillage [x0;x1]×[y0;y1], axes, graduations étiquetées xt / yt."""
    # step=1 (sans unité) : un carreau = une unité du repère, quel que soit x=U cm
    # (le pas par défaut de « grid » est 1 cm, décalé du repère dès que U ≠ 1).
    s = [r"\draw[grille,step=1] (%s,%s) grid (%s,%s);" % (f(x0), f(y0), f(x1), f(y1))]
    if not axes:
        return s
    s.append(r"\draw[axe] (%s,0) -- (%s,0);" % (f(x0), f(x1 + .5)))
    s.append(r"\draw[axe] (0,%s) -- (0,%s);" % (f(y0), f(y1 + .5)))
    # pas de graduation sur l'extrémité de départ d'un axe
    for k in range(int(math.ceil(x0)), int(x1) + 1):
        if k and k != x0:
            s.append(r"\draw[otMuted,line width=.5pt] (%d,-.07) -- (%d,.07);" % (k, k))
    for k in range(int(math.ceil(y0)), int(y1) + 1):
        if k and k != y0:
            s.append(r"\draw[otMuted,line width=.5pt] (-.07,%d) -- (.07,%d);" % (k, k))
    for k in xt:
        s.append(r"\node[grad,anchor=north] at (%d,-.12) {%s};" % (k, num(k)))
    for k in yt:
        s.append(r"\node[grad,anchor=east] at (-.12,%d) {%s};" % (k, num(k)))
    if origine:
        s.append(r"\node[grad,anchor=north east] at (-.08,-.08) {$0$};")
    if noms:
        s.append(r"\node[text=otMuted,anchor=west,inner sep=2pt] at (%s,0) {$x$};" % f(x1 + .5))
        s.append(r"\node[text=otMuted,anchor=south,inner sep=2pt] at (0,%s) {$y$};" % f(y1 + .5))
    return s


def pt(p, nom, ang, coul="otNavy", d=.13, U=1.0):
    """Point plein + nom placé dans la direction ang (degrés)."""
    a = math.radians(ang)
    q = (p[0] + d / U * math.cos(a), p[1] + d / U * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,anchor=%d] at %s {$%s$};" % ((ang + 180) % 360, P(q), nom))
    return s


def vect(p, q, coul="otNavy", style="vec"):
    return [r"\draw[%s,%s] %s -- %s;" % (style, coul, P(p), P(q))]


def lvec(p, q, txt, cote=1, t=.5, d=.15, U=1.0, coul="otInk"):
    """Étiquette d'un vecteur p→q, à gauche (cote=1) ou à droite (cote=-1)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d / U * nx, p[1] + t * dy + d / U * ny)
    ang = math.degrees(math.atan2(ny, nx))
    return [r"\node[lab,text=%s,anchor=%d] at %s {$%s$};" % (coul, round(ang + 180) % 360, P(m), txt)]


def figure(U, corps):
    return "\n".join([r"\begin{tikzpicture}[x=%scm,y=%scm]" % (f(U), f(U))] + corps + [r"\end{tikzpicture}"])


FIGURES = {}

# ------------------------------------------------------------------ cours 1 : égalité de vecteurs
A, B, C, D = (0, 0), (4, 1), (1, 2.2), (5, 3.2)
c = [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(D), P(C))]
c += [r"\draw[aide] %s -- %s %s -- %s;" % (P(A), P(C), P(B), P(D))]
c += vect(A, B) + vect(C, D)
c += lvec(A, B, r"\vec{u}", -1) + lvec(C, D, r"\vec{u}", 1)
c += pt(A, "A", 225) + pt(B, "B", 330) + pt(C, "C", 150) + pt(D, "D", 30)
FIGURES["egalite"] = figure(1.0, c)

# ------------------------------------------------------------------ cours 2 : Chasles et parallélogramme
A, B, C = (0, 0), (2, 1.9), (3.6, 0.4)
c = vect(A, B) + vect(B, C, "otOrange") + vect(A, C, "otGreenDark")
c += lvec(A, B, r"\overrightarrow{AB}", 1) + lvec(B, C, r"\overrightarrow{BC}", 1)
c += lvec(A, C, r"\overrightarrow{AC}", -1, coul="otGreenDark")
c += pt(A, "A", 200) + pt(B, "B", 90) + pt(C, "C", 340)
O = (4.8, 0)
Uu, Vv = (O[0] + 2.3, .5), (O[0] + .5, 1.7)
M = (O[0] + 2.8, 2.2)
c += [r"\draw[aide] %s -- %s -- %s;" % (P(Uu), P(M), P(Vv))]
c += vect(O, Uu) + vect(O, Vv, "otOrange") + vect(O, M, "otGreenDark")
c += lvec(O, Uu, r"\vec{u}", -1) + lvec(O, Vv, r"\vec{v}", 1)
c += [r"\node[lab,text=otGreenDark,anchor=225] at %s {$\vec{u} + \vec{v}$};" % P((M[0] + .1, M[1] + .1))]
c += pt(O, "O", 225)
FIGURES["chasles"] = figure(1.0, c)

# ------------------------------------------------------------------ cours 3 : produit par un réel
U = .7
c = repere(0, 12, 0, 3, axes=False)
c += vect((1, 1), (3, 2)) + vect((4, 0), (8, 2), "otGreenDark") + vect((12, 2), (9, .5), "otOrange")
c += lvec((1, 1), (3, 2), r"\vec{u}", 1, U=U)
c += lvec((4, 0), (8, 2), r"2\vec{u}", 1, U=U, coul="otGreenDark")
c += lvec((12, 2), (9, .5), r"-1{,}5\,\vec{u}", -1, U=U, coul="otOrange!80!black")
FIGURES["produit"] = figure(U, c)

# ------------------------------------------------------------------ cours 4 : base orthonormée
U = .95
c = repere(-1, 6, -1, 3, axes=False)
c += vect((0, 0), (1, 0), "otGreenDark") + vect((0, 0), (0, 1), "otGreenDark")
c += lvec((0, 0), (1, 0), r"\vec{i}", -1, U=U, coul="otGreenDark")
c += lvec((0, 0), (0, 1), r"\vec{j}", 1, U=U, coul="otGreenDark")
c += pt((0, 0), "O", 225, U=U)
A, H, B = (2, 0), (5, 0), (5, 2)
c += [r"\draw[aide,otOrange!90!black] %s -- %s -- %s;" % (P(A), P(H), P(B))]
c += [r"\node[lab,text=otOrange!80!black,anchor=north] at (3.5,-.15) {$3\vec{i}$};"]
c += [r"\node[lab,text=otOrange!80!black,anchor=west] at (5.17,1) {$2\vec{j}$};"]
c += vect(A, B)
c += [r"\node[lab,anchor=south] at (5,2.22) {$\vec{u} = 3\vec{i} + 2\vec{j}$};"]
FIGURES["base"] = figure(U, c)

# ------------------------------------------------------------------ cours 5 : coordonnées, distance, milieu
U = .85
A, B, I = (1, 1), (5, 4), (3, 2.5)
c = repere(-1, 7, -1, 5, xt=range(1, 7), yt=range(1, 5))
c += [r"\draw[aide,otOrange!90!black] %s -- (5,1) -- %s;" % (P(A), P(B))]
c += [r"\node[cot,text=otOrange!80!black,anchor=north] at (3,.86) {$x_B - x_A = 4$};"]
c += [r"\node[cot,text=otOrange!80!black,anchor=west] at (5.16,2.5) {$y_B - y_A = 3$};"]
c += vect(A, B)
c += [r"\node[lab,anchor=south east] at (2.5,2.65) {$\overrightarrow{AB}\,(4\,;3)$};"]
c += pt(A, "A", 200, U=U) + pt(B, "B", 70, U=U) + pt(I, "I", 300, "otGreenDark", U=U)
FIGURES["coordonnees"] = figure(U, c)

# ------------------------------------------------------------------ cours 6 : points alignés
U = .8
A, B, C = (1, 1), (3, 2), (7, 4)
c = repere(-1, 8, -1, 5, xt=range(1, 8), yt=range(1, 5))
# droite (AC) en pointillés ; AB sur la droite ; AC tracé juste en dessous, parallèlement
# (sinon la flèche verte semble partir de B et représenter BC)
c += [r"\draw[aide] (.3,.65) -- (7.5,4.25);"]
_d = (.13, -.26)
A2, C2 = (A[0] + _d[0], A[1] + _d[1]), (C[0] + _d[0], C[1] + _d[1])
c += vect(A2, C2, "otGreenDark") + vect(A, B)
c += [r"\node[lab,anchor=south east] at (2,1.8) {$\overrightarrow{AB}\,(2\,;1)$};"]
c += lvec(A2, C2, r"\overrightarrow{AC}\,(6\,;3)", -1, t=.6, d=.32, U=U, coul="otGreenDark")
c += pt(A, "A", 150, U=U) + pt(B, "B", 120, U=U) + pt(C, "C", 110, U=U)
FIGURES["alignes"] = figure(U, c)

# ------------------------------------------------------------------ ex 1956 : translation
U = .6
A, B, C, D = (1, -2), (4, 1), (-2, 3), (1, 6)
c = repere(-3, 5, -3, 7, xt=(-2, -1, 1, 2, 4), yt=(-2, 2, 4, 6), origine=False)
c += [r"\draw[aide] %s -- %s %s -- %s;" % (P(A), P(C), P(B), P(D))]
c += vect(A, B) + vect(C, D, "otGreenDark")
c += pt(A, "A", 270, U=U) + pt(B, "B", 0, U=U) + pt(C, "C", 180, U=U) + pt(D, "D", 90, "otGreenDark", U=U)
FIGURES["ex_translation"] = figure(U, c)

# ------------------------------------------------------------------ ex 1963 : triangle isocèle
U = .8
A, B, C, M = (0, 1), (4, 3), (2, -1), (1, 0)
c = repere(-1, 5, -2, 4, xt=(2, 3, 4), yt=(-1, 2, 3), origine=False)
c += [r"\coordinate (A) at %s; \coordinate (B) at %s; \coordinate (C) at %s; \coordinate (M) at %s;"
      % (P(A), P(B), P(C), P(M))]
c += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\draw[geoReponse] (B) -- (M);",
      r"\codage{A}{B}", r"\codage{B}{C}", r"\codage[2]{A}{M}", r"\codage[2]{M}{C}"]
c += pt(A, "A", 180, U=U) + pt(B, "B", 45, U=U) + pt(C, "C", 270, U=U) + pt(M, "M", 235, "otGreenDark", U=U)
FIGURES["ex_isocele"] = figure(U, c)

# ------------------------------------------------------------------ ex 1964 : parallélogramme
U = .65
A, B, C, D, I = (2, 1), (6, 3), (4, -1), (0, -3), (3, 0)
c = repere(-1, 7, -4, 4, xt=(1, 2, 4, 5, 6), yt=(-2, -1, 1, 2, 3), origine=False)
c += [r"\draw[aide] %s -- %s %s -- %s;" % (P(A), P(C), P(B), P(D))]
c += [r"\draw[geoTrait] %s -- %s -- %s;" % (P(C), P(B), P(A))]
c += [r"\draw[geoReponse] %s -- %s -- %s;" % (P(A), P(D), P(C))]
c += pt(A, "A", 135, U=U) + pt(B, "B", 30, U=U) + pt(C, "C", 315, U=U)
c += pt(D, "D", 215, "otGreenDark", U=U) + pt(I, "I", 90, "otGreenDark", U=U)
FIGURES["ex_parallelogramme"] = figure(U, c)

# ------------------------------------------------------------------ ex 1962 : alignement et parallélisme
U = .62
A, B, C, D, Pp = (-1, 1), (2, 3), (4, 0), (1, -2), (-7, -3)
c = repere(-8, 5, -4, 4, xt=(1,), yt=(1,))
c += [r"\draw[geoTrait] (-8,-3.667) -- (3.2,3.8);", r"\draw[geoTrait] (-2,-4) -- (4.9,.6);"]
c += [r"\node[lab,text=otNavy,anchor=east] at (2.95,3.85) {$(AB)$};",
      r"\node[lab,text=otNavy,anchor=south west] at (5,.7) {$(CD)$};"]
c += pt(A, "A", 120, U=U) + pt(B, "B", 300, U=U) + pt(C, "C", 300, U=U) + pt(D, "D", 300, U=U)
c += pt(Pp, "P", 300, "otGreenDark", U=U)
FIGURES["ex_alignement"] = figure(U, c)

# ------------------------------------------------------------------ ex 1960 : triangle et droite parallèle
A, B, C = (0, 0), (6, .6), (1.8, 4.2)
M = (.4 * B[0], .4 * B[1])
N = (.4 * C[0], .4 * C[1])
c = [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
c += [r"\draw[geoReponse] %s -- %s;" % (P(M), P(N))]
c += pt(A, "A", 225) + pt(B, "B", 330) + pt(C, "C", 90)
c += pt(M, "M", 280, "otGreenDark") + pt(N, "N", 180, "otGreenDark")
FIGURES["ex_triangle_mn"] = figure(1.0, c)

# ------------------------------------------------------------------ ex 1959 : drone
U = .9
S, A, B, T = (-3, 2), (2, 1), (0, 5), (1, 2)
c = repere(-4, 3, -1, 6, xt=(1,), yt=(1,))
c += vect(S, A) + vect(A, B) + vect(B, T) + vect(S, T, "otGreenDark")
c += lvec(S, A, r"\vec{u}", -1, t=.35, U=U) + lvec(A, B, r"\vec{v}", -1, U=U)  # u loin de la graduation 1
c += lvec(B, T, r"\vec{w}", -1, t=.78, d=.1, U=U)
c += lvec(S, T, r"\overrightarrow{ST}", 1, U=U, coul="otGreenDark")
c += pt(S, "S", 180, U=U) + pt(A, "A", 330, U=U) + pt(B, "B", 150, U=U) + pt(T, "T", 290, "otGreenDark", U=U)
FIGURES["ex_drone"] = figure(U, c)

# ------------------------------------------------------------------ ex 1958 : D milieu de [AE]
A, B, C = (0, 0), (5, 1), (1, 5)
D = (11 / 3, 7 / 3)
D2 = (7 / 3, 11 / 3)
E = (22 / 3, 14 / 3)
c = [r"\coordinate (A) at %s; \coordinate (B) at %s; \coordinate (C) at %s; \coordinate (D) at %s; "
     r"\coordinate (D2) at %s; \coordinate (E) at %s;" % (P(A), P(B), P(C), P(D), P(D2), P(E))]
c += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\draw[geoReponse] (A) -- (E);",
      r"\codage{B}{D}", r"\codage{D}{D2}", r"\codage{D2}{C}", r"\codage[2]{A}{D}", r"\codage[2]{D}{E}"]
c += pt(A, "A", 225) + pt(B, "B", 300) + pt(C, "C", 90)
c += pt(D, "D", 84, "otGreenDark") + pt(E, "E", 45, "otGreenDark")
FIGURES["ex_triangle_ade"] = figure(1.0, c)


# ------------------------------------------------------------------ nouveau-1 : lecture graphique
def _n1(corrige):
    U = .7
    A, B, C, D, E, F = (-4, 1), (-1, 3), (2, -1), (5, 1), (1, -3), (-2, -5)
    c = repere(-5, 6, -6, 4, xt=(1,), yt=(1,))
    if corrige:
        g = r"\node[cot,text=otGreenDark,anchor=%s] at (%s,%s) {$%s$};"
        c += [r"\draw[aideV] %s -- (-1,1) -- %s;" % (P(A), P(B)),
              g % ("north", "-2.5", ".85", "+3"), g % ("west", "-.86", "2", "+2")]
        c += [r"\draw[aideV] %s -- (5,-1) -- %s;" % (P(C), P(D)),
              g % ("north", "3.5", "-1.15", "+3"), g % ("west", "5.14", ".5", "+2")]
        c += [r"\draw[aideV] %s -- (-2,-3) -- %s;" % (P(E), P(F)),
              g % ("south", "-.5", "-2.85", "-3"), g % ("east", "-2.14", "-4", "-2")]
    c += vect(A, B) + vect(C, D) + vect(E, F)
    c += pt(A, "A", 180, U=U) + pt(B, "B", 90, U=U) + pt(C, "C", 270, U=U)
    c += pt(D, "D", 0, U=U) + pt(E, "E", 0, U=U) + pt(F, "F", 180, U=U)
    return figure(U, c)


FIGURES["n1_enonce"] = _n1(False)
FIGURES["n1_corrige"] = _n1(True)


# ------------------------------------------------------------------ nouveau-2 : construire u + v et u − v
def _n2(corrige):
    U = .9
    O, Uu, Vv = (0, 0), (3, 1), (-1, 2)
    c = repere(-2, 5, -2, 4, xt=() if corrige else (1,), yt=(1,), origine=False)
    if corrige:
        M, Q = (2, 3), (4, -1)
        c += [r"\draw[aide] %s -- %s;" % (P(Vv), P(M))]
        c += vect(Uu, M, "otOrange") + vect(Uu, Q, "otOrange")
        c += lvec(Uu, M, r"\vec{v}", -1, U=U, coul="otOrange!80!black")
        c += lvec(Uu, Q, r"-\vec{v}", 1, U=U, coul="otOrange!80!black")
        c += vect(O, M, "otGreenDark") + vect(O, Q, "otGreenDark")
        c += lvec(O, M, r"\vec{u} + \vec{v}", -1, t=.42, U=U, coul="otGreenDark")
        c += lvec(O, Q, r"\vec{u} - \vec{v}", -1, t=.45, U=U, coul="otGreenDark")
        c += pt(M, "M", 90, "otGreenDark", U=U) + pt(Q, "P", 300, "otGreenDark", U=U)
    c += vect(O, Uu) + vect(O, Vv)
    c += lvec(O, Uu, r"\vec{u}", 1 if corrige else -1, t=.8 if corrige else .5, U=U)
    c += lvec(O, Vv, r"\vec{v}", 1, t=.75, U=U)  # loin de la graduation 1 de l'axe des ordonnées
    c += pt(O, "O", 235, U=U)
    return figure(U, c)


FIGURES["n2_enonce"] = _n2(False)
FIGURES["n2_corrige"] = _n2(True)


# ================================================================== finition 2026-11-02
# Figures d'énoncé (données seules) et figures de corrigé ajoutées.

# ------------------------------------------------------------------ ex 1966 (corrigé) : u + v et w = 2u
U = .62
O, Uu, Vv, S = (0, 0), (3, -1), (-2, 4), (1, 3)
W0, W1 = (0, -2.5), (6, -4.5)
c = repere(-3, 7, -5, 5, xt=(1, 3, 6), yt=(-4, -2, 1, 3), origine=False)
c += [r"\draw[aide] %s -- %s -- %s;" % (P(Uu), P(S), P(Vv))]
c += vect(O, Uu) + vect(O, Vv) + vect(O, S, "otGreenDark") + vect(W0, W1, "otGreenDark")
c += lvec(O, Uu, r"\vec{u}", 1, t=.62, U=U) + lvec(O, Vv, r"\vec{v}", -1, t=.6, U=U)
c += lvec(O, S, r"\vec{u} + \vec{v}", -1, t=.62, U=U, coul="otGreenDark")
c += lvec(W0, W1, r"\vec{w} = 2\vec{u}", -1, t=.55, U=U, coul="otGreenDark")
c += pt(O, "O", 225, U=U)
FIGURES["ex_somme_colineaire"] = figure(U, c)

# ------------------------------------------------------------------ ex 1967 (corrigé) : chemin A → D → C → B
A, D, C, B = (0, 0), (1.4, 2.6), (4.4, 3.0), (5.6, .5)
c = vect(A, D) + vect(D, C) + vect(C, B) + vect(A, B, "otGreenDark")
c += lvec(A, D, r"\overrightarrow{AD}", 1) + lvec(D, C, r"\overrightarrow{DC}", 1)
c += lvec(C, B, r"\overrightarrow{CB}", 1)
c += lvec(A, B, r"\overrightarrow{AB}", -1, coul="otGreenDark")
c += pt(A, "A", 200) + pt(D, "D", 120) + pt(C, "C", 60) + pt(B, "B", 340)
FIGURES["ex_chasles_chemin"] = figure(1.0, c)

# ------------------------------------------------------------------ ex 1965 (corrigé) : milieu de [AB]
U = .75
A, B, M = (1, -3), (7, 1), (4, -1)
c = repere(-1, 8, -4, 2, xt=(1, 4), yt=(-3, -1, 1))
c += [r"\draw[aide,otOrange!90!black] %s -- (7,-3) -- %s;" % (P(A), P(B))]
c += [r"\node[cot,text=otOrange!80!black,anchor=north] at (4,-3.16) {$6$};"]
c += [r"\node[cot,text=otOrange!80!black,anchor=west] at (7.16,-1) {$4$};"]
c += vect(A, M, "otGreenDark") + vect(M, B, "otGreenDark")
c += lvec(A, M, r"\overrightarrow{AM}", 1, U=U, coul="otGreenDark")
c += lvec(M, B, r"\overrightarrow{MB}", 1, U=U, coul="otGreenDark")
c += pt(A, "A", 180, U=U) + pt(B, "B", 90, U=U) + pt(M, "M", 300, "otGreenDark", U=U)
FIGURES["ex_milieu"] = figure(U, c)


# ------------------------------------------------------------------ ex 1961 : D(t ; −1) tel que (CD) // (AB)
def _ex1961(corrige):
    U = .7
    A, B, C, D = (-2, 0), (1, 3), (4, 2), (1, -1)
    c = repere(-3, 5, -3, 4, xt=(1, 4), yt=(2, 3))
    c += [r"\draw[aide] (-3,-1) -- (5.3,-1);"]
    c += [r"\node[lab,text=otMuted,anchor=west] at (5.4,-1) {$y = -1$};"]
    c += [r"\draw[geoTrait] (-3,-1) -- (2,4);"]
    c += [r"\node[lab,text=otNavy,anchor=south] at (2,4.1) {$(AB)$};"]
    if corrige:
        c += [r"\draw[geoReponse] (-1,-3) -- (5.5,3.5);"]
        c += [r"\node[lab,text=otGreenDark,anchor=west] at (5.58,3.5) {$(CD)$};"]
        c += pt(D, "D", 315, "otGreenDark", U=U)
    c += pt(A, "A", 120, U=U) + pt(B, "B", 330, U=U) + pt(C, "C", 120, U=U)
    return figure(U, c)


FIGURES["ex_parallele_t_enonce"] = _ex1961(False)
FIGURES["ex_parallele_t_corrige"] = _ex1961(True)

# ------------------------------------------------------------------ ex 1957 (corrigé) : coordonnées proportionnelles
k = 2.2
O1, V1 = (0, 0), (2, 1)
O2 = (3.2, 0)
U2 = (O2[0] + k * 2, O2[1] + k * 1)
c = [r"\draw[aide] %s -- (%s,0) -- %s;" % (P(O1), f(V1[0]), P(V1))]
c += [r"\draw[aideV] %s -- (%s,%s) -- %s;" % (P(O2), f(U2[0]), f(O2[1]), P(U2))]
c += vect(O1, V1) + vect(O2, U2, "otGreenDark")
c += lvec(O1, V1, r"\vec{v}", 1, t=.4)
c += lvec(O2, U2, r"\vec{u} = k\vec{v}", 1, t=.45, coul="otGreenDark")
c += [r"\node[cot,text=otMuted,anchor=north] at (1,-.14) {$x'$};",
      r"\node[cot,text=otMuted,anchor=west] at (2.14,.5) {$y'$};"]
c += [r"\node[cot,text=otGreenDark,anchor=north] at (%s,-.14) {$x = kx'$};" % f(O2[0] + k),
      r"\node[cot,text=otGreenDark,anchor=west] at (%s,%s) {$y = ky'$};" % (f(U2[0] + .14), f(k / 2))]
FIGURES["ex_colineaires"] = figure(1.0, c)

# ------------------------------------------------------------------ énoncés : données seules (sans la réponse)
# 1956 : A, B, C et le vecteur AB (D à construire)
U = .6
A, B, C = (1, -2), (4, 1), (-2, 3)
c = repere(-3, 5, -3, 7, xt=(-2, -1, 1, 2, 4), yt=(-2, 2, 4, 6), origine=False)
c += vect(A, B)
c += pt(A, "A", 270, U=U) + pt(B, "B", 0, U=U) + pt(C, "C", 180, U=U)
FIGURES["ex_translation_enonce"] = figure(U, c)

# 1963 : triangle ABC (sans codage ni milieu)
U = .8
A, B, C = (0, 1), (4, 3), (2, -1)
c = repere(-1, 5, -2, 4, xt=(2, 3, 4), yt=(-1, 2, 3), origine=False)
c += [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
c += pt(A, "A", 180, U=U) + pt(B, "B", 45, U=U) + pt(C, "C", 270, U=U)
FIGURES["ex_isocele_enonce"] = figure(U, c)

# 1964 : A, B, C et les côtés [AB], [BC] (D à trouver)
U = .65
A, B, C = (2, 1), (6, 3), (4, -1)
c = repere(-1, 7, -4, 4, xt=(1, 2, 4, 5, 6), yt=(-2, -1, 1, 2, 3), origine=False)
c += [r"\draw[geoTrait] %s -- %s -- %s;" % (P(C), P(B), P(A))]
c += pt(A, "A", 135, U=U) + pt(B, "B", 30, U=U) + pt(C, "C", 315, U=U)
FIGURES["ex_parallelogramme_enonce"] = figure(U, c)

# 1962 : les quatre points A, B, C, D
U = .75
A, B, C, D = (-1, 1), (2, 3), (4, 0), (1, -2)
c = repere(-3, 5, -3, 4, xt=(-1, 1, 2, 4), yt=(-2, 1, 3))
c += pt(A, "A", 120, U=U) + pt(B, "B", 90, U=U) + pt(C, "C", 90, U=U) + pt(D, "D", 0, U=U)
FIGURES["ex_alignement_enonce"] = figure(U, c)

# 1960 : triangle ABC, M et N placés (sans [MN])
A, B, C = (0, 0), (6, .6), (1.8, 4.2)
M = (.4 * B[0], .4 * B[1])
N = (.4 * C[0], .4 * C[1])
c = [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
c += pt(A, "A", 225) + pt(B, "B", 330) + pt(C, "C", 90)
c += pt(M, "M", 280) + pt(N, "N", 180)
FIGURES["ex_triangle_mn_enonce"] = figure(1.0, c)

# 1958 : triangle ABC et D sur [BC] au tiers (E à construire)
A, B, C = (0, 0), (5, 1), (1, 5)
D = (11 / 3, 7 / 3)
D2 = (7 / 3, 11 / 3)
c = [r"\coordinate (A) at %s; \coordinate (B) at %s; \coordinate (C) at %s; \coordinate (D) at %s; "
     r"\coordinate (D2) at %s;" % (P(A), P(B), P(C), P(D), P(D2))]
c += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
      r"\codage{B}{D}", r"\codage{D}{D2}", r"\codage{D2}{C}"]
c += pt(A, "A", 225) + pt(B, "B", 300) + pt(C, "C", 90) + pt(D, "D", 30)
FIGURES["ex_triangle_ade_enonce"] = figure(1.0, c)
