# -*- coding: utf-8 -*-
"""Figures de la notion « Théorème de Pythagore » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = constructions d'aide. Les étiquettes de côtés sont
placées automatiquement du côté extérieur du triangle.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  aide/.style={otOrange!90!black,line width=.8pt,dash pattern=on 3.5pt off 2pt},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  grille/.style={otRule!75,line width=.35pt},
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
}
"""

V = r"\textcolor{otGreenDark}{%s}"


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def pt(p, nom, ang, coul="otNavy", d=.14):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};"
                 % ("otInk" if coul == "otNavy" else coul, (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, coul="otInk"):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    return [r"\node[lab,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(q), txt)]


def lseg(p, q, txt, cote=1, t=.5, d=.14):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,anchor=%s] at %s {%s};" % (anc, P(m), txt)]


def ext(p, q, r):
    """cote (1 ou -1) qui place une étiquette de [pq] du côté opposé à r."""
    cr = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return -1 if cr > 0 else 1


def figure(corps):
    return "\n".join([r"\begin{tikzpicture}[line cap=round]"] + corps + [r"\end{tikzpicture}"])


def angle_droit(p, sommet, q, coul="otNavy", r=.22):
    """Petit carré d'angle droit en « sommet »."""
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L * r, (b[1] - a[1]) / L * r)
    a, b = u(sommet, p), u(sommet, q)
    p1 = (sommet[0] + a[0], sommet[1] + a[1])
    p2 = (sommet[0] + a[0] + b[0], sommet[1] + a[1] + b[1])
    p3 = (sommet[0] + b[0], sommet[1] + b[1])
    return [r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, P(p1), P(p2), P(p3))]


def triangle(pts, noms, droit=None, droit_vert=False, cotes=None, vert=(), remplir="otSky",
             traits_verts=(), t=None, d=.14, noms_ang=None):
    """pts : trois points (cm) ; noms : trois lettres ; droit : indice du sommet de l'angle droit.

    cotes : {(i, j): texte} ; vert : clés (i, j) écrites en vert ; traits_verts : côtés tracés en vert.
    """
    cotes = cotes or {}
    t = t or {}
    G = (sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3)
    s = [r"\fill[%s] %s -- %s -- %s -- cycle;" % (remplir, P(pts[0]), P(pts[1]), P(pts[2])),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(pts[0]), P(pts[1]), P(pts[2]))]
    for (i, j) in traits_verts:
        s.append(r"\draw[geoReponse,line width=1.4pt] %s -- %s;" % (P(pts[i]), P(pts[j])))
    if droit is not None:
        o = [k for k in range(3) if k != droit]
        s += angle_droit(pts[o[0]], pts[droit], pts[o[1]], "otGreenDark" if droit_vert else "otNavy")
    for (i, j), txt in cotes.items():
        k = 3 - i - j
        c = ext(pts[i], pts[j], pts[k])
        s += lseg(pts[i], pts[j], (V % txt) if (i, j) in vert else txt, c, t=t.get((i, j), .5), d=d)
    for k in range(3):
        ang = noms_ang[k] if noms_ang else math.degrees(math.atan2(pts[k][1] - G[1], pts[k][0] - G[0]))
        s += pt(pts[k], noms[k], ang)
    return s


def rect_tri(a, b, U, noms="ABC", cotes=None, vert=(), droit=True, droit_vert=False, rot=0, traits_verts=(),
             remplir="otSky", noms_ang=None, origine=(0, 0)):
    """Triangle rectangle en noms[0] : côté a horizontal (vers noms[1]), côté b vertical (vers noms[2])."""
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def R(x, y):
        return (origine[0] + x * c - y * s_, origine[1] + x * s_ + y * c)
    pts = [R(0, 0), R(a * U, 0), R(0, b * U)]
    return triangle(pts, noms, 0 if droit else None, droit_vert, cotes, vert, remplir, traits_verts,
                    noms_ang=noms_ang)


FIGURES = {}

# ================================================================== COURS
# carrés construits sur les côtés (3, 4, 5)
def carres():
    U = .62
    A, B, C = (0, 0), (4 * U, 0), (0, 3 * U)
    s = [r"\fill[otSky] (0,0) rectangle %s;" % P((4 * U, -4 * U)),
         r"\fill[otSky] (0,0) rectangle %s;" % P((-3 * U, 3 * U))]
    # carré sur l'hypoténuse : B -> C, puis vers l'extérieur
    dx, dy = C[0] - B[0], C[1] - B[1]
    D = (C[0] + dy, C[1] - dx)
    E = (B[0] + dy, B[1] - dx)
    # (dx, dy) = C - B ; (dy, -dx) pointe vers l'extérieur
    s += [r"\fill[otGreen!16] %s -- %s -- %s -- %s -- cycle;" % (P(B), P(C), P(D), P(E))]
    s += [r"\draw[geoTrait] (0,0) rectangle %s;" % P((4 * U, -4 * U)),
          r"\draw[geoTrait] (0,0) rectangle %s;" % P((-3 * U, 3 * U)),
          r"\draw[otGreenDark,line width=.9pt] %s -- %s -- %s -- %s -- cycle;" % (P(B), P(C), P(D), P(E))]
    s += [r"\fill[white] (0,0) -- %s -- %s -- cycle;" % (P(B), P(C)),
          r"\draw[geoTrait,line width=1.3pt] (0,0) -- %s -- %s -- cycle;" % (P(B), P(C))]
    s += angle_droit(B, A, C)
    s += [r"\node[lab] at %s {$AB^2$};" % P((2 * U, -2 * U)),
          r"\node[lab] at %s {$AC^2$};" % P((-1.5 * U, 1.5 * U)),
          r"\node[lab,text=otGreenDark] at %s {$BC^2$};" % P(((B[0] + D[0]) / 2, (B[1] + D[1]) / 2))]
    s += pt(A, "A", 225, d=.16) + pt(B, "B", 300) + pt(C, "C", 150)
    return figure(s)


FIGURES["cours_carres"] = carres()


# démonstration par les aires : carré de côté a + b
def demo():
    a, b, U = 3.0, 1.6, 1.0
    L = a + b
    P1, P2, P3, P4 = (a, 0), (L, a), (b, L), (0, b)
    s = [r"\fill[otGreen!16] %s -- %s -- %s -- %s -- cycle;" % (P(P1), P(P2), P(P3), P(P4))]
    for (q, r_) in (((0, 0), None),):
        pass
    tris = [((0, 0), P1, P4), ((L, 0), P2, P1), ((L, L), P3, P2), ((0, L), P4, P3)]
    for o, p, q in tris:
        s.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(o), P(p), P(q)))
    s += [r"\draw[geoTrait] (0,0) rectangle %s;" % P((L, L)),
          r"\draw[otGreenDark,line width=1pt] %s -- %s -- %s -- %s -- cycle;" % (P(P1), P(P2), P(P3), P(P4))]
    s += [r"\node[lab] at %s {$a$};" % P((a / 2, -.25)), r"\node[lab] at %s {$b$};" % P((a + b / 2, -.25)),
          r"\node[lab] at %s {$a$};" % P((L + .25, a / 2)), r"\node[lab] at %s {$b$};" % P((L + .25, a + b / 2)),
          r"\node[lab] at %s {$a$};" % P((L - a / 2, L + .25)), r"\node[lab] at %s {$b$};" % P((b / 2, L + .25)),
          r"\node[lab] at %s {$a$};" % P((-.25, L - a / 2)), r"\node[lab] at %s {$b$};" % P((-.25, b / 2))]
    s += lseg(P1, P2, V % "$c$", -1, d=.12)
    s += [r"\node[lab,text=otGreenDark] at %s {$c^2$};" % P((L / 2, L / 2))]
    return figure(s)


FIGURES["cours_demo"] = demo()


# repère : distance entre A(1 ; 2) et B(7 ; 10) — sert au cours et à l'exercice 2368
def repere_ab(corrige, cours=False):
    U = .5
    s = [r"\begin{scope}[x=%scm,y=%scm]" % (f(U), f(U)),
         r"\draw[grille,step=1] (-.5,-.5) grid (8.5,11.5);",
         r"\draw[axe] (-.5,0) -- (9,0);", r"\draw[axe] (0,-.5) -- (0,12);"]
    for k in range(1, 9):
        s.append(r"\draw[otMuted,line width=.5pt] (%d,-.1) -- (%d,.1);" % (k, k))
    for k in range(1, 12):
        s.append(r"\draw[otMuted,line width=.5pt] (-.1,%d) -- (.1,%d);" % (k, k))
    for k in (1, 7):
        s.append(r"\node[grad,anchor=north] at (%d,-.15) {$%d$};" % (k, k))
    for k in (2, 10):
        s.append(r"\node[grad,anchor=east] at (-.15,%d) {$%d$};" % (k, k))
    s.append(r"\node[grad,anchor=north east] at (-.1,-.1) {$0$};")
    s.append(r"\fill[%s] (1,2) -- (7,2) -- (7,10) -- cycle;" % ("otGreen!16" if corrige else "otSky"))
    s.append(r"\draw[aide] (1,2) -- (7,2) -- (7,10);")
    s.append(r"\draw[%s] (1,2) -- (7,10);" % ("geoReponse,line width=1.3pt" if corrige else "geoTrait"))
    s.append(r"\draw[otOrange!90!black,line width=.6pt] (6.55,2) -- (6.55,2.45) -- (7,2.45);")
    s.append(r"\node[lab,text=otOrange!80!black,anchor=north] at (4,1.8) {$6$};")
    s.append(r"\node[lab,text=otOrange!80!black,anchor=west] at (7.2,6) {$8$};")
    if corrige:
        s.append(r"\node[lab,text=otGreenDark,anchor=south east] at (3.85,6.1) {$AB = 10$};")
    s.append(r"\end{scope}")
    s += pt((.5, 1), "A", 150) + pt((3.5, 5), "B", 90) + pt((3.5, 1), "" if cours else "C", 315)
    return figure(s)


FIGURES["cours_repere"] = repere_ab(True, cours=True)

# ================================================================== EXERCICES
# 2359 : repérer l'hypoténuse
def deux_triangles(corrige):
    s = rect_tri(3.2, 2.2, 1.0, "ABC", traits_verts=[(1, 2)] if corrige else [],
                 noms_ang=[225, 315, 90])
    D, E, F = (4.6, 2.4), (5.5, 0), (8.2, 1.3)
    s += triangle([D, E, F], "DEF", droit=1, traits_verts=[(0, 2)] if corrige else [], noms_ang=[135, 270, 0])
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=south west] at (1.75,1.25) {hypoténuse};",
              r"\node[txt,text=otGreenDark,anchor=south west] at (6.75,2.15) {hypoténuse};"]
    return figure(s)


FIGURES["ex2359_enonce"] = deux_triangles(False)
FIGURES["ex2359_corrige"] = deux_triangles(True)

# 2360 : 6, 8, hypoténuse 10
FIGURES["ex2360_enonce"] = figure(rect_tri(8, 6, .55, "ABC", {(0, 1): "8 cm", (0, 2): "6 cm"}))
FIGURES["ex2360_corrige"] = figure(rect_tri(8, 6, .55, "ABC", {(0, 1): "8 cm", (0, 2): "6 cm", (1, 2): "10 cm"},
                                            vert=[(1, 2)], traits_verts=[(1, 2)]))
# 2361 : BC = 13, AB = 5 -> AC = 12
FIGURES["ex2361_enonce"] = figure(rect_tri(12, 5, .45, "ACB", {(0, 2): "5 cm", (1, 2): "13 cm"}))
FIGURES["ex2361_corrige"] = figure(rect_tri(12, 5, .45, "ACB", {(0, 2): "5 cm", (1, 2): "13 cm", (0, 1): "12 cm"},
                                            vert=[(0, 1)], traits_verts=[(0, 1)]))
# 2362 : 4 et 7 -> racine de 65
FIGURES["ex2362_enonce"] = figure(rect_tri(7, 4, .65, "ACB", {(0, 1): "7 cm", (0, 2): "4 cm"}))
FIGURES["ex2362_corrige"] = figure(rect_tri(7, 4, .65, "ACB", {(0, 1): "7 cm", (0, 2): "4 cm",
                                                              (1, 2): r"$\sqrt{65} \approx 8{,}1$ cm"},
                                            vert=[(1, 2)], traits_verts=[(1, 2)]))


# 2363 : 9, 12, 15 (sans angle droit dans l'énoncé)
def tri_cotes(a, b, c, U, rot=0):
    """Triangle de base c (de B à C), côté a = AB, côté b = AC ; renvoie A, B, C."""
    xa = (a * a - b * b + c * c) / (2 * c)
    ya = math.sqrt(max(a * a - xa * xa, 0))
    pts = [(xa, ya), (0, 0), (c, 0)]
    cs, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [((x * cs - y * sn) * U, (x * sn + y * cs) * U) for x, y in pts]


A, B, C = tri_cotes(9, 12, 15, .4)
FIGURES["ex2363_enonce"] = figure(triangle([A, B, C], "ABC", cotes={(0, 1): "9 cm", (0, 2): "12 cm", (1, 2): "15 cm"}))
FIGURES["ex2363_corrige"] = figure(triangle([A, B, C], "ABC", droit=0, droit_vert=True,
                                            cotes={(0, 1): "9 cm", (0, 2): "12 cm", (1, 2): "15 cm"}))
A, B, C = tri_cotes(5, 7, 9, .55)
FIGURES["ex2364_enonce"] = figure(triangle([A, B, C], "ABC", cotes={(0, 1): "5 cm", (0, 2): "7 cm", (1, 2): "9 cm"}))
FIGURES["ex2364_corrige"] = figure(
    triangle([A, B, C], "ABC", cotes={(0, 1): "5 cm", (0, 2): "7 cm", (1, 2): "9 cm"})
    + [r"\node[lab,text=otGreenDark,anchor=north] at %s {$9^2 = 81$ et $5^2 + 7^2 = 74$ : $81 \neq 74$};" % P((C[0] / 2, -.55))])


# 2365 : additionner ou soustraire ?
def trois_rect(corrige):
    s = []
    s += rect_tri(3, 4, .42, "RST", {(0, 1): "9 cm", (0, 2): "12 cm"} if not corrige else
                  {(0, 1): "9 cm", (0, 2): "12 cm", (1, 2): "15 cm"}, vert=[(1, 2)],
                  traits_verts=[(1, 2)] if corrige else [], noms_ang=[225, 315, 90])
    s += [r"\node[txt,text=otNavy,anchor=north] at (.65,-.55) {(a)};"]
    # (b) KLM rectangle en L : KM = 17, KL = 8, LM = 15
    U = .17
    o = (2.75, 0)
    s += rect_tri(15, 8, U, "LMK", {(0, 2): "8 cm", (1, 2): "17 cm"} if not corrige else
                  {(0, 2): "8 cm", (1, 2): "17 cm", (0, 1): "15 cm"}, vert=[(0, 1)],
                  traits_verts=[(0, 1)] if corrige else [], noms_ang=[225, 315, 90], origine=o)
    s += [r"\node[txt,text=otNavy,anchor=north] at (4.05,-.55) {(b)};"]
    # (c) UVW rectangle en W : UV = 2,5, UW = 1,5, VW = 2
    o = (6.35, 0)
    s += rect_tri(2, 1.5, .95, "WVU", {(0, 2): "1,5 cm", (1, 2): "2,5 cm"} if not corrige else
                  {(0, 2): "1,5 cm", (1, 2): "2,5 cm", (0, 1): "2 cm"}, vert=[(0, 1)],
                  traits_verts=[(0, 1)] if corrige else [], noms_ang=[225, 315, 90], origine=o)
    s += [r"\node[txt,text=otNavy,anchor=north] at (7.3,-.55) {(c)};"]
    return figure(s)


FIGURES["ex2365_enonce"] = trois_rect(False)
FIGURES["ex2365_corrige"] = trois_rect(True)


# 2366 : échelle de 5 m, pied à 1,4 m
def echelle(corrige):
    U = .8
    A, B, C = (0, 0), (1.4 * U, 0), (0, 4.8 * U)
    s = [r"\fill[otMuted!25] (-.35,-.0) rectangle (0,%s);" % f(4.8 * U + .6),
         r"\draw[otMuted,line width=.8pt] (0,0) -- (0,%s);" % f(4.8 * U + .6),
         r"\draw[otMuted,line width=.8pt] (-.35,0) -- (2.6,0);"]
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;".replace("(A)", P(A)).replace("(B)", P(B)).replace("(C)", P(C))]
    s += [r"\draw[otOrange!90!black,line width=2.2pt] %s -- %s;" % (P(B), P(C))]
    s += angle_droit(B, A, C, "otGreenDark" if corrige else "otNavy")
    s += [r"\node[lab,anchor=north] at %s {1,4 m};" % P((.56, -.2))] + lseg(B, C, "5 m", -1, d=.14)
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(C))]
        s += [r"\node[lab,anchor=east] at (-.45,2.6) {%s};" % (V % "4,8 m")]
    s += pt(A, "A", 215, d=.16) + pt(B, "B", 330) + pt(C, "C", 30, d=.16)
    s += [r"\node[txt,text=otMuted,anchor=east] at (-.45,.9) {mur};",
          r"\node[txt,text=otMuted,anchor=north] at (2.1,-.12) {sol};"]
    return figure(s)


FIGURES["ex2366_enonce"] = echelle(False)
FIGURES["ex2366_corrige"] = echelle(True)


# 2367 : rectangle 20 x 15 et diagonale
def rectangle_diag(corrige):
    U = .26
    A, B, C, D = (0, 0), (20 * U, 0), (20 * U, 15 * U), (0, 15 * U)
    s = [r"\fill[otSky] %s rectangle %s;" % (P(A), P(C)),
         r"\draw[geoTrait] %s rectangle %s;" % (P(A), P(C))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.4pt" if corrige else "geoTrait", P(A), P(C))]
    s += angle_droit(A, B, C, "otGreenDark" if corrige else "otNavy")
    s += lab(((A[0] + B[0]) / 2, 0), "20 cm", 270, d=.16) + lab((C[0], C[1] / 2), "15 cm", 0, d=.16)
    if corrige:
        s += lseg(A, C, V % "25 cm", 1, t=.42, d=.14)
    s += pt(A, "A", 225) + pt(B, "B", 315) + pt(C, "C", 45) + pt(D, "D", 135)
    return figure(s)


FIGURES["ex2367_enonce"] = rectangle_diag(False)
FIGURES["ex2367_corrige"] = rectangle_diag(True)
FIGURES["ex2368_enonce"] = repere_ab(False)
FIGURES["ex2368_corrige"] = repere_ab(True)

# 2369 : AB = 7,5 ; AC = 4,5 ; BC = 6 -> rectangle en C, hauteur CH = 3,6
A_, B_, C_ = (0, 0), (7.5, 0), None
U = .75
# C tel que AC = 4,5 et BC = 6
xc = (4.5 ** 2 - 6 ** 2 + 7.5 ** 2) / (2 * 7.5)
yc = math.sqrt(4.5 ** 2 - xc ** 2)
A_, B_, C_ = (0, 0), (7.5 * U, 0), (xc * U, yc * U)
H_ = (xc * U, 0)


def hauteur(corrige):
    s = triangle([A_, B_, C_], "ABC", droit=2 if corrige else None, droit_vert=True,
                 cotes={(0, 2): "4,5 cm", (1, 2): "6 cm"})
    s += lab(((A_[0] + B_[0]) / 2 + 1.0, 0), "7,5 cm", 270, d=.16)
    if corrige:
        s += [r"\draw[geoReponse,line width=1.2pt] %s -- %s;" % (P(C_), P(H_))]
        s += angle_droit(B_, H_, C_, "otGreenDark")
        s += lab((H_[0], C_[1] * .3), V % "3,6 cm", 180, d=.12)
        s += pt(H_, "H", 270, "otGreenDark", d=.16)
    return figure(s)


FIGURES["ex2369_enonce"] = hauteur(False)
FIGURES["ex2369_corrige"] = hauteur(True)


# 2370 : voile rectangle en A, AB = 2,4 (horizontal, bôme), BC = 4
def voile(corrige):
    U = 1.0
    A, B, C = (0, 0), (2.4 * U, 0), (0, 3.2 * U)
    s = [r"\draw[otMuted,line width=2pt] (0,-.25) -- (0,%s);" % f(3.2 * U + .3)]
    s += triangle([A, B, C], "ABC", droit=0, cotes={(0, 1): "2,4 m", (1, 2): "4 m"} if not corrige else
                  {(0, 1): "2,4 m", (1, 2): "4 m", (0, 2): "3,2 m"}, vert=[(0, 2)],
                  traits_verts=[(0, 2)] if corrige else [], noms_ang=[200, 315, 135])
    s += [r"\node[txt,text=otMuted,anchor=east] at (-.25,1.0) {mât};"]
    return figure(s)


FIGURES["ex2370_enonce"] = voile(False)
FIGURES["ex2370_corrige"] = voile(True)


# 2371 : ouverture 0,9 x 1,2 et tige
def ouverture(corrige):
    U = 2.6
    s = [r"\fill[otSky] (0,0) rectangle %s;" % P((1.2 * U, .9 * U)),
         r"\draw[geoTrait] (0,0) rectangle %s;" % P((1.2 * U, .9 * U))]
    s += [r"\draw[%s] (0,0) -- %s;" % ("geoReponse,line width=1.6pt" if corrige else "aide", P((1.2 * U, .9 * U)))]
    s += angle_droit((0, 0), (1.2 * U, 0), (1.2 * U, .9 * U))
    s += lab((.6 * U, 0), "1,2 m", 270, d=.16) + lab((1.2 * U, .45 * U), "0,9 m", 0, d=.16)
    if corrige:
        s += lseg((0, 0), (1.2 * U, .9 * U), V % "1,5 m", 1, t=.42)
    return figure(s)


FIGURES["ex2371_enonce"] = ouverture(False)
FIGURES["ex2371_corrige"] = ouverture(True)


# 2372 : EFG (2,8 ; 4,5 ; 5,3) et RST (4 ; 5,5 ; 6,8)
def deux_presque(corrige):
    U = .56
    E, F, G = tri_cotes(2.8, 4.5, 5.3, U)  # E en haut, côtés EF = 2,8, EG = 4,5, FG = 5,3
    s = triangle([E, F, G], "EFG", droit=0 if corrige else None, droit_vert=True,
                 cotes={(0, 1): "2,8", (0, 2): "4,5", (1, 2): "5,3"})
    R_, S_, T_ = tri_cotes(4, 5.5, 6.8, U)
    R_, S_, T_ = [(x + 3.9, y) for x, y in (R_, S_, T_)]
    s += triangle([R_, S_, T_], "RST", cotes={(0, 1): "4", (0, 2): "5,5", (1, 2): "6,8"})
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=north] at %s {rectangle en $E$};" % P((F[0] + 1.6, -.55)),
              r"\node[txt,text=otOrange!80!black,anchor=north] at %s {non rectangle};" % P((S_[0] + 2.1, -.55))]
    s += [r"\node[txt,text=otMuted,anchor=north west] at (-.1,%s) {longueurs en cm};" % f(-1.05 if corrige else -.55)]
    return figure(s)


FIGURES["ex2372_enonce"] = deux_presque(False)
FIGURES["ex2372_corrige"] = deux_presque(True)


# 2373 : rampe (hauteur 0,75 m, avancée 10 m) — schéma non à l'échelle (hauteur exagérée)
def rampe(corrige):
    A, B, C = (5.8, 0), (0, 0), (5.8, 1.6)
    s = [r"\draw[otMuted,line width=.7pt] (-.4,0) -- (6.6,0);"]
    s += triangle([A, B, C], "ABC", droit=0, cotes={(0, 1): "10 m", (0, 2): "0,75 m"}
                  if not corrige else {(0, 1): "10 m", (0, 2): "0,75 m", (1, 2): r"$\approx 10{,}03$ m"},
                  vert=[(1, 2)], traits_verts=[(1, 2)] if corrige else [], noms_ang=[315, 225, 45])
    s += [r"\node[txt,text=otMuted,anchor=north west] at (-.4,-.55) {schéma : la hauteur est exagérée};"]
    return figure(s)


FIGURES["ex2373_enonce"] = rampe(False)
FIGURES["ex2373_corrige"] = rampe(True)


# 2374 : parc 160 x 120
def parc(corrige):
    U = .034
    D, E, F, G = (0, 0), (160 * U, 0), (160 * U, 120 * U), (0, 120 * U)
    s = [r"\fill[otGreen!10] %s rectangle %s;" % (P(D), P(F)),
         r"\draw[geoTrait] %s rectangle %s;" % (P(D), P(F))]
    s += [r"\draw[otOrange!90!black,line width=1.6pt,-{Stealth[length=2.4mm]}] %s -- %s -- %s;" % (P((0, .08)), P((160 * U - .08, .08)), P((160 * U - .08, 120 * U - .1)))]
    s += [r"\draw[%s,-{Stealth[length=2.4mm]}] %s -- %s;" % ("geoReponse,line width=1.6pt" if corrige else "aide", P(D), P((F[0] - .1, F[1] - .075)))]
    s += angle_droit(D, E, F)
    s += lab((80 * U, 0), "160 m", 270, d=.18) + lab((160 * U, 60 * U), "120 m", 0, d=.18)
    if corrige:
        s += lseg(D, F, V % "200 m", 1, t=.4, d=.16)
    s += pt(D, "D", 225) + pt(E, "E", 315) + pt(F, "F", 45)
    return figure(s)


FIGURES["ex2374_enonce"] = parc(False)
FIGURES["ex2374_corrige"] = parc(True)


# 2375 : isocèle CA = CB = 13, AB = 10, H milieu de [AB]
def isocele(corrige):
    U = .36
    A, B, C, H = (0, 0), (10 * U, 0), (5 * U, 12 * U), (5 * U, 0)
    s = triangle([A, B, C], "ABC", cotes={(0, 2): "13 cm", (1, 2): "13 cm"}, noms_ang=[225, 315, 90])
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.3pt" if corrige else "aide", P(C), P(H))]
    s += angle_droit(B, H, C, "otGreenDark" if corrige else "otOrange!90!black")
    s += [r"\codage{%s}{%s}" % ("hA", "hH"), r"\codage{%s}{%s}" % ("hH", "hB")]
    s = [r"\coordinate (hA) at %s; \coordinate (hH) at %s; \coordinate (hB) at %s;" % (P(A), P(H), P(B))] + s
    s += [r"\node[lab,anchor=north] at %s {$AB = 10$ cm};" % P((5 * U, -.55))] if not corrige else \
        [r"\node[lab,anchor=north] at %s {%s};" % (P((2.5 * U, -.55)), V % "$AH = 5$ cm")]
    if corrige:
        s += lab((H[0], C[1] * .42), V % "12 cm", 180, d=.1)
    s += pt(H, "H", 270, "otGreenDark" if corrige else "otNavy", d=.18)
    return figure(s)


FIGURES["ex2375_enonce"] = isocele(False)
FIGURES["ex2375_corrige"] = isocele(True)


# 2376 : pavé 3 x 4 x 12 (perspective cavalière)
def pave(corrige):
    lx, ly, lz = 4 * .5, 3 * .5, 12 * .32
    k = .5
    dx, dy = ly * k * math.cos(math.radians(35)), ly * k * math.sin(math.radians(35))
    E, F, G, H = (0, 0), (lx, 0), (lx + dx, dy), (dx, dy)
    A, B, C, D = [(x, y + lz) for x, y in (E, F, G, H)]
    s = [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(E), P(F), P(B), P(A)),
         r"\fill[otSky!60] %s -- %s -- %s -- %s -- cycle;" % (P(F), P(G), P(C), P(B))]
    s += [r"\draw[cache] %s -- %s -- %s %s -- %s;" % (P(E), P(H), P(G), P(H), P(D))]
    if corrige:
        s += [r"\fill[otGreen!22] %s -- %s -- %s -- cycle;" % (P(E), P(G), P(C)),
              r"\draw[otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt] %s -- %s;" % (P(E), P(G)),
              r"\draw[geoReponse,line width=1.4pt] %s -- %s;" % (P(E), P(C))]
        s += angle_droit(E, G, C, "otGreenDark", r=.18)
    s += [r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle %s -- %s -- %s -- %s -- %s %s -- %s;"
          % (P(E), P(F), P(B), P(A), P(F), P(G), P(C), P(B), P(A), P(A), P(D))]
    s += [r"\draw[geoTrait] %s -- %s;" % (P(D), P(C))]
    s += lab(((E[0] + F[0]) / 2, 0), "4 cm", 270, d=.16)
    s += lab(((F[0] + G[0]) / 2, (F[1] + G[1]) / 2), "3 cm", 315, d=.16)
    s += lab((G[0], (G[1] + C[1]) / 2), "12 cm", 0, d=.16)
    if corrige:
        s += [r"\node[lab,text=otGreenDark,anchor=north] at %s {$EG = 5$ cm};" % P((lx / 2, -.62)),
              r"\node[lab,text=otGreenDark,anchor=east] at %s {$EC = 13$ cm};" % P((-.15, lz * .55))]
    s += pt(E, "E", 225) + pt(G, "G", 0, d=.16) + pt(C, "C", 45)
    return figure(s)


FIGURES["ex2376_enonce"] = pave(False)
FIGURES["ex2376_corrige"] = pave(True)


# 2377 : mât de 6 m, fixation à 4,5 m
def mat(corrige):
    U = .5
    P_, S, F1, F2 = (0, 0), (0, 6 * U), (4.5 * U, 0), (-4.5 * U, 0)
    s = [r"\draw[otMuted,line width=.7pt] (-3,0) -- (3,0);"]
    s += [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corrige else "otSky", P(P_), P(F1), P(S))]
    s += [r"\draw[otNavy,line width=2.4pt] %s -- %s;" % (P(P_), P(S))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.3pt" if corrige else "otOrange!90!black,line width=1.1pt", P(S), P(F1)),
          r"\draw[otOrange!90!black,line width=1.1pt,dash pattern=on 3pt off 2pt] %s -- %s;" % (P(S), P(F2))]
    s += angle_droit(F1, P_, S)
    s += lab((0, 3 * U), "6 m", 180, d=.16) + lab((2.25 * U, 0), "4,5 m", 270, d=.16)
    if corrige:
        s += lseg(F1, S, V % "7,5 m", 1, d=.14)
    else:
        s += lseg(F1, S, "câble", 1, d=.14)
    s += pt(P_, "P", 225) + pt(S, "S", 90) + pt(F1, "F", 300)
    return figure(s)


FIGURES["ex2377_enonce"] = mat(False)
FIGURES["ex2377_corrige"] = mat(True)


# 2378 : écran 120 x 67,5
def ecran(corrige):
    U = .045
    w, h = 120 * U, 67.5 * U
    s = [r"\fill[otInk!85] (-.15,-.15) rectangle %s;" % P((w + .15, h + .15)),
         r"\fill[otSky] (0,0) rectangle %s;" % P((w, h)),
         r"\fill[otInk!85] %s rectangle %s;" % (P((w / 2 - .35, -.15)), P((w / 2 + .35, -.45))),
         r"\fill[otInk!85] %s rectangle %s;" % (P((w / 2 - 1.0, -.45)), P((w / 2 + 1.0, -.55)))]
    s += [r"\draw[%s] (0,0) -- %s;" % ("geoReponse,line width=1.4pt" if corrige else "aide", P((w, h)))]
    s += angle_droit((0, 0), (w, 0), (w, h), r=.2)
    s += lab((w / 2, -.55), "120 cm", 270, d=.12) + lab((w + .15, h / 2), "67,5 cm", 0, d=.16)
    if corrige:
        s += lseg((0, 0), (w, h), V % r"$\approx 137{,}7$ cm", 1, t=.4, d=.14)
    return figure(s)


FIGURES["ex2378_enonce"] = ecran(False)
FIGURES["ex2378_corrige"] = ecran(True)


# 2379 : bateau 12 km est puis 5 km nord
def bateau(corrige):
    U = .45
    Pt, E, N = (0, 0), (12 * U, 0), (12 * U, 5 * U)
    s = [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corrige else "otSky", P(Pt), P(E), P(N))]
    s += [r"\draw[otNavy,line width=1.3pt,-{Stealth[length=2.6mm]}] %s -- %s;" % (P(Pt), P((E[0] - .05, 0))),
          r"\draw[otNavy,line width=1.3pt,-{Stealth[length=2.6mm]}] %s -- %s;" % (P(E), P((E[0], N[1] - .05)))]
    s += [r"\draw[%s,-{Stealth[length=2.6mm]}] %s -- %s;" % ("geoReponse,line width=1.3pt" if corrige else "aide", P(N), P((.1, .045)))]
    s += angle_droit(Pt, E, N)
    s += lab((6 * U, 0), "12 km", 270, d=.16) + lab((12 * U, 2.5 * U), "5 km", 0, d=.16)
    if corrige:
        s += lseg(Pt, N, V % "13 km", 1, t=.45, d=.14)
    s += pt(Pt, "P", 180, d=.16) + pt(E, "E", 315) + pt(N, "B", 45)
    s += [r"\node[txt,text=otMuted,anchor=north east] at (-.1,-.15) {port};",
          r"\draw[otMuted,line width=.7pt,-{Stealth[length=2mm]}] (6.6,.8) -- (6.6,1.6);",
          r"\node[txt,text=otMuted,anchor=south] at (6.6,1.65) {N};"]
    return figure(s)


FIGURES["ex2379_enonce"] = bateau(False)
FIGURES["ex2379_corrige"] = bateau(True)
