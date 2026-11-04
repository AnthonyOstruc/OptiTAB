# -*- coding: utf-8 -*-
"""Figures de la notion « Théorème de Pythagore » (4e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés : hypoténuse repérée, longueur trouvée), orange = constructions
d'aide. Les étiquettes de côtés sont placées automatiquement du côté extérieur du
triangle. Outils repris de la notion 244 (3e).
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
ORANGE = "otOrange!80!black"


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
        s.append(r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(pts[i]), P(pts[j])))
    if droit is not None:
        o = [k for k in range(3) if k != droit]
        s += angle_droit(pts[o[0]], pts[droit], pts[o[1]], "otGreenDark" if droit_vert else "otNavy")
    for (i, j), txt in cotes.items():
        k = 3 - i - j
        c = ext(pts[i], pts[j], pts[k])
        s += lseg(pts[i], pts[j], (V % txt) if (i, j) in vert else txt, c, t=t.get((i, j), .5), d=d)
    for k in range(3):
        if noms[k]:
            ang = noms_ang[k] if noms_ang else math.degrees(math.atan2(pts[k][1] - G[1], pts[k][0] - G[0]))
            s += pt(pts[k], noms[k], ang)
    return s


def rect_pts(a, b, U, rot=0, origine=(0, 0)):
    c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def R(x, y):
        return (origine[0] + x * c - y * s_, origine[1] + x * s_ + y * c)
    return [R(0, 0), R(a * U, 0), R(0, b * U)]


def rect_tri(a, b, U, noms="ABC", cotes=None, vert=(), droit=True, droit_vert=False, rot=0, traits_verts=(),
             remplir="otSky", noms_ang=None, origine=(0, 0), t=None):
    """Triangle rectangle en noms[0] : côté a « horizontal » (vers noms[1]), côté b « vertical » (vers noms[2])."""
    pts = rect_pts(a, b, U, rot, origine)
    return triangle(pts, noms, 0 if droit else None, droit_vert, cotes, vert, remplir, traits_verts,
                    noms_ang=noms_ang, t=t)


def tri_cotes(a, b, c, U, rot=0, origine=(0, 0)):
    """Triangle de base c (de B à C), côté a = AB, côté b = AC ; renvoie A, B, C."""
    xa = (a * a - b * b + c * c) / (2 * c)
    ya = math.sqrt(max(a * a - xa * xa, 0))
    pts = [(xa, ya), (0, 0), (c, 0)]
    cs, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(origine[0] + (x * cs - y * sn) * U, origine[1] + (x * sn + y * cs) * U) for x, y in pts]


def legende(x, y, txt, coul="otNavy", anc="north"):
    return [r"\node[txt,text=%s,anchor=%s] at %s {%s};" % (coul, anc, P((x, y)), txt)]


FIGURES = {}

# ================================================================== COURS
# vocabulaire du triangle rectangle
def vocabulaire():
    s = rect_tri(4.2, 2.6, 1.0, "ABC", traits_verts=[(1, 2)], noms_ang=[225, 315, 90])
    s += lseg((4.2, 0), (0, 2.6), V % "hypoténuse", -1, t=.45, d=.16)
    s += [r"\node[txt,text=otNavy,anchor=north] at (2.1,-.2) {côté de l'angle droit};"]
    s += [r"\node[txt,text=otNavy,anchor=east,align=center] at (-.25,1.4) {côté de\\l'angle droit};"]
    s += [r"\node[txt,text=otNavy,anchor=south west] at (.33,.3) {angle droit};"]
    return figure(s)


FIGURES["cours_vocabulaire"] = vocabulaire()


# carrés construits sur les côtés (3, 4, 5)
def carres():
    U = .62
    A, B, C = (0, 0), (4 * U, 0), (0, 3 * U)
    s = [r"\fill[otSky] (0,0) rectangle %s;" % P((4 * U, -4 * U)),
         r"\fill[otSky] (0,0) rectangle %s;" % P((-3 * U, 3 * U))]
    dx, dy = C[0] - B[0], C[1] - B[1]
    D = (C[0] + dy, C[1] - dx)
    E = (B[0] + dy, B[1] - dx)
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


# preuve par découpage : deux rangements des quatre mêmes triangles dans le même carré
def demo():
    a, b = 2.1, 1.15
    L = a + b
    g = .95
    s = []
    # à gauche : carré central c²
    P1, P2, P3, P4 = (a, 0), (L, a), (b, L), (0, b)
    s += [r"\fill[otGreen!18] %s -- %s -- %s -- %s -- cycle;" % (P(P1), P(P2), P(P3), P(P4))]
    for o, p, q in [((0, 0), P1, P4), ((L, 0), P2, P1), ((L, L), P3, P2), ((0, L), P4, P3)]:
        s.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(o), P(p), P(q)))
    s += [r"\draw[geoTrait] (0,0) rectangle %s;" % P((L, L)),
          r"\draw[otGreenDark,line width=1pt] %s -- %s -- %s -- %s -- cycle;" % (P(P1), P(P2), P(P3), P(P4))]
    s += [r"\node[lab] at %s {$a$};" % P((a / 2, -.22)), r"\node[lab] at %s {$b$};" % P((a + b / 2, -.22)),
          r"\node[lab] at %s {$b$};" % P((-.22, b / 2)), r"\node[lab] at %s {$a$};" % P((-.22, b + a / 2))]
    s += [r"\node[lab,text=otGreenDark] at %s {$c^2$};" % P((L / 2, L / 2))]
    s += legende(L / 2, -.5, r"partie verte : $c^2$", "otGreenDark")
    # à droite : carrés a² et b²
    o = L + g
    s += [r"\fill[otGreen!18] %s rectangle %s;" % (P((o, 0)), P((o + a, a))),
          r"\fill[otGreen!18] %s rectangle %s;" % (P((o + a, a)), P((o + L, L)))]
    s += [r"\fill[otSky] %s rectangle %s;" % (P((o + a, 0)), P((o + L, a))),
          r"\fill[otSky] %s rectangle %s;" % (P((o, a)), P((o + a, L)))]
    s += [r"\draw[geoTrait] %s -- %s;" % (P((o + a, 0)), P((o + L, a))),
          r"\draw[geoTrait] %s -- %s;" % (P((o, a)), P((o + a, L)))]
    s += [r"\draw[geoTrait] %s rectangle %s;" % (P((o, 0)), P((o + L, L))),
          r"\draw[otGreenDark,line width=1pt] %s rectangle %s;" % (P((o, 0)), P((o + a, a))),
          r"\draw[otGreenDark,line width=1pt] %s rectangle %s;" % (P((o + a, a)), P((o + L, L)))]
    s += [r"\node[lab] at %s {$a$};" % P((o + a / 2, -.22)), r"\node[lab] at %s {$b$};" % P((o + a + b / 2, -.22)),
          r"\node[lab] at %s {$a$};" % P((o + L + .22, a / 2)), r"\node[lab] at %s {$b$};" % P((o + L + .22, a + b / 2))]
    s += [r"\node[lab,text=otGreenDark] at %s {$a^2$};" % P((o + a / 2, a / 2)),
          r"\node[lab,text=otGreenDark] at %s {$b^2$};" % P((o + a + b / 2, a + b / 2))]
    s += legende(o + L / 2, -.5, r"partie verte : $a^2 + b^2$", "otGreenDark")
    return figure(s)


FIGURES["cours_demo"] = demo()

# exemple du cours : AB = 12, AC = 16 -> BC = 20
FIGURES["cours_ex_hyp"] = figure(rect_tri(16, 12, .22, "ACB", {(0, 1): "16 cm", (0, 2): "12 cm", (1, 2): "20 cm"},
                                          vert=[(1, 2)], traits_verts=[(1, 2)], noms_ang=[225, 315, 90]))
# exemple du cours : EF = 25, DE = 7 -> DF = 24
FIGURES["cours_ex_cote"] = figure(rect_tri(24, 7, .17, "DFE", {(0, 2): "7 cm", (1, 2): "25 cm", (0, 1): "24 cm"},
                                           vert=[(0, 1)], traits_verts=[(0, 1)], noms_ang=[225, 315, 90]))


# réciproque : MN = 4,5 ; MP = 6 ; NP = 7,5 -> rectangle en M
def reciproque():
    M, N, Pp = tri_cotes(4.5, 6, 7.5, .62)
    s = triangle([M, N, Pp], "MNP", droit=0, droit_vert=True,
                 cotes={(0, 1): "4,5 cm", (0, 2): "6 cm", (1, 2): "7,5 cm"})
    return figure(s)


FIGURES["cours_reciproque"] = reciproque()


# où trouver un triangle rectangle : quatre situations
def situations():
    s = []
    W = 3.9   # largeur d'une case
    # (1) échelle contre un mur
    o = (0, 3.0)
    s += [r"\fill[otMuted!25] %s rectangle %s;" % (P((o[0] + .2, o[1])), P((o[0] + .45, o[1] + 2.1))),
          r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((o[0] + .45, o[1])), P((o[0] + .45, o[1] + 2.1))),
          r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((o[0] + .2, o[1])), P((o[0] + 2.6, o[1])))]
    A, B, C = (o[0] + .45, o[1]), (o[0] + 1.45, o[1]), (o[0] + .45, o[1] + 1.85)
    s += [r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[otOrange!90!black,line width=2pt] %s -- %s;" % (P(B), P(C))]
    s += angle_droit(B, A, C, "otGreenDark", r=.18)
    s += legende(o[0] + 1.4, o[1] - .25, "mur et sol")
    # (2) diagonale d'un rectangle
    o = (W + .3, 3.0)
    w, h = 3.0, 1.7
    s += [r"\fill[otSky] %s rectangle %s;" % (P(o), P((o[0] + w, o[1] + h))),
          r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(o), P((o[0] + w, o[1])), P((o[0] + w, o[1] + h))),
          r"\draw[geoTrait] %s rectangle %s;" % (P(o), P((o[0] + w, o[1] + h))),
          r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(o), P((o[0] + w, o[1] + h)))]
    s += angle_droit(o, (o[0] + w, o[1]), (o[0] + w, o[1] + h), "otGreenDark", r=.18)
    s += legende(o[0] + w / 2, o[1] - .25, "coin d'un rectangle")
    # (3) hauteur d'un triangle isocèle
    o = (.15, 0)
    A, B, C, H = o, (o[0] + 3.0, o[1]), (o[0] + 1.5, o[1] + 1.9), (o[0] + 1.5, o[1])
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(A), P(H), P(C)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoReponse,line width=1.1pt] %s -- %s;" % (P(C), P(H))]
    s += [r"\coordinate (i1) at %s; \coordinate (i2) at %s; \coordinate (i3) at %s; \coordinate (i4) at %s;"
          % (P(A), P(C), P(C), P(B)), r"\codage{i1}{i2}", r"\codage{i3}{i4}"]
    s += angle_droit(B, H, C, "otGreenDark", r=.18)
    s += legende(o[0] + 1.5, o[1] - .25, "triangle isocèle")
    # (4) losange
    o = (W + 1.8, 0.95)
    A, B, C, D = (o[0] - 1.5, o[1]), (o[0], o[1] - .95), (o[0] + 1.5, o[1]), (o[0], o[1] + .95)
    s += [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D)),
          r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(A), P(o), P(D)),
          r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D)),
          r"\draw[otNavy,line width=.6pt] %s -- %s %s -- %s;" % (P(A), P(C), P(B), P(D))]
    s += angle_droit(A, o, D, "otGreenDark", r=.16)
    s += legende(o[0], -.25, "diagonales d'un losange")
    return figure(s)


FIGURES["cours_situations"] = situations()

# ================================================================== EXERCICES
# 3188 : repérer l'hypoténuse dans trois triangles
def trois_hyp(corrige):
    s = []
    # triangle 1 : ABC rectangle en A
    s += rect_tri(2.4, 1.8, 1.0, "ABC", traits_verts=[(1, 2)] if corrige else [], noms_ang=[225, 315, 90])
    s += legende(1.2, -.5, "triangle 1")
    # triangle 2 : DEF rectangle en F (angle droit en haut à droite)
    s += rect_tri(2.2, 1.8, 1.0, "FDE", rot=180, origine=(5.2, 1.8),
                  traits_verts=[(1, 2)] if corrige else [], noms_ang=[45, 135, 270])
    s += legende(4.1, -.5, "triangle 2")
    # triangle 3 : GHK rectangle en H, penché
    cot = {(0, 1): "5 cm", (0, 2): "12 cm"}
    if corrige:
        cot[(1, 2)] = "13 cm"
    s += rect_tri(5, 12, .19, "HGK", cot, vert=[(1, 2)], rot=24, origine=(7.3, 0),
                  traits_verts=[(1, 2)] if corrige else [], noms_ang=[270, 0, 90])
    s += legende(7.3, -.5, "triangle 3")
    return figure(s)


FIGURES["ex3188_enonce"] = trois_hyp(False)
FIGURES["ex3188_corrige"] = trois_hyp(True)


# 3189 : AB = 9, AC = 12 -> BC = 15 ; hauteur AH = 7,2
def ex3189(etape):
    U = .3
    pts = rect_pts(12, 9, U)          # A, C, B
    cot = {(0, 1): "12 cm", (0, 2): "9 cm"}
    if etape >= 1:
        cot[(1, 2)] = "15 cm"
    s = triangle(pts, "ACB", 0, False, cot, vert=[(1, 2)] if etape == 1 else [],
                 traits_verts=[(1, 2)] if etape == 1 else [], noms_ang=[225, 315, 90])
    if etape == 2:
        A, C, B = pts
        dx, dy = B[0] - C[0], B[1] - C[1]
        tt = ((A[0] - C[0]) * dx + (A[1] - C[1]) * dy) / (dx * dx + dy * dy)
        H = (C[0] + tt * dx, C[1] + tt * dy)
        s += [r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(A), P(H))]
        s += angle_droit(C, H, A, "otGreenDark", r=.18)
        s += lseg(A, H, V % "7,2 cm", -1, t=.5, d=.12)
        s += pt(H, "H", 45, "otGreenDark", d=.16)
    return figure(s)


FIGURES["ex3189_enonce"] = ex3189(0)
FIGURES["ex3189_corrige"] = ex3189(1)
FIGURES["ex3189_hauteur"] = ex3189(2)

# 3190 : DF = 17, DE = 8 -> EF = 15 (rectangle en E)
FIGURES["ex3190_enonce"] = figure(rect_tri(15, 8, .28, "EFD", {(0, 2): "8 cm", (1, 2): "17 cm"}, noms_ang=[225, 315, 90]))
FIGURES["ex3190_corrige"] = figure(rect_tri(15, 8, .28, "EFD", {(0, 2): "8 cm", (1, 2): "17 cm", (0, 1): "15 cm"},
                                            vert=[(0, 1)], traits_verts=[(0, 1)], noms_ang=[225, 315, 90]))


# 3191 : GHK rectangle en G (7 et 5 -> racine de 74) ; LMN rectangle en M (LN = 9, LM = 4 -> racine de 65)
def ex3191(corrige):
    U = .42
    cot = {(0, 1): "7 cm", (0, 2): "5 cm"}
    if corrige:
        cot[(1, 2)] = r"$\sqrt{74} \approx 8{,}6$ cm"
    s = rect_tri(7, 5, U, "GHK", cot, vert=[(1, 2)], traits_verts=[(1, 2)] if corrige else [], noms_ang=[225, 315, 90])
    o = (4.3, 0)
    cot = {(0, 2): "4 cm", (1, 2): "9 cm"}
    if corrige:
        cot[(0, 1)] = r"$\sqrt{65} \approx 8{,}1$ cm"
    s += rect_tri(65 ** .5, 4, U, "MNL", cot, vert=[(0, 1)], traits_verts=[(0, 1)] if corrige else [],
                  noms_ang=[225, 315, 90], origine=o)
    return figure(s)


FIGURES["ex3191_enonce"] = ex3191(False)
FIGURES["ex3191_corrige"] = ex3191(True)


# 3192 : ABC (20, 21, 29) et RST (1,6 ; 3 ; 3,4)
def ex3192(corrige):
    A, B, C = tri_cotes(20, 21, 29, .135)
    s = triangle([A, B, C], "ABC", droit=0 if corrige else None, droit_vert=True,
                 cotes={(0, 1): "20 cm", (0, 2): "21 cm", (1, 2): "29 cm"})
    R, S_, T = tri_cotes(1.6, 3, 3.4, .95, origine=(5.0, 0))
    s += triangle([R, S_, T], "RST", droit=0 if corrige else None, droit_vert=True,
                  cotes={(0, 1): "1,6 cm", (0, 2): "3 cm", (1, 2): "3,4 cm"})
    return figure(s)


FIGURES["ex3192_enonce"] = ex3192(False)
FIGURES["ex3192_corrige"] = ex3192(True)


# 3193 : EFG (EF = 6, FG = 7, EG = 9) : non rectangle
def ex3193(corrige):
    F, E, G = tri_cotes(6, 7, 9, .48)
    s = triangle([F, E, G], "FEG", cotes={(0, 1): "6 cm", (0, 2): "7 cm", (1, 2): "9 cm"})
    if corrige:
        s += legende((E[0] + G[0]) / 2, -.62, r"$9^2 = 81$ et $6^2 + 7^2 = 85$ : $81 \neq 85$", "otGreenDark")
    return figure(s)


FIGURES["ex3193_enonce"] = ex3193(False)
FIGURES["ex3193_corrige"] = ex3193(True)


# 3194 : choisir la propriété — (a) ABC rectangle en B ; (b) DEF 10-24-26 ; (c) GHI 4-7-8
def ex3194(corrige):
    s = []
    cot = {(0, 1): "12", (0, 2): "5"}
    if corrige:
        cot[(1, 2)] = "13"
    s += rect_tri(12, 5, .19, "BCA", cot, vert=[(1, 2)], traits_verts=[(1, 2)] if corrige else [],
                  noms_ang=[225, 290, 90])
    s += legende(1.14, -.55, "(a)")
    E, D, F = tri_cotes(10, 24, 26, .088, origine=(3.05, 0))
    s += triangle([E, D, F], "EDF", droit=0 if corrige else None, droit_vert=True,
                  cotes={(0, 1): "10", (0, 2): "24", (1, 2): "26"}, noms_ang=[90, 250, 290])
    s += legende(4.2, -.55, "(b)")
    H, G, I = tri_cotes(4, 7, 8, .26, origine=(6.09, 0))
    s += triangle([H, G, I], "HGI", cotes={(0, 1): "4", (0, 2): "7", (1, 2): "8"}, noms_ang=[90, 250, 290])
    s += legende(7.13, -.55, "(c)")
    y = -.55
    if corrige:
        y = -.95
        s += legende(7.13, y, "non rectangle", ORANGE)
        s += legende(4.2, y, r"rectangle en $E$", "otGreenDark")
        s += legende(1.14, y, r"$AC = 13$", "otGreenDark")
    s += [r"\node[txt,text=otMuted,anchor=north west] at (-.4,%s) {longueurs en cm};" % f(y - .45)]
    return figure(s)


FIGURES["ex3194_enonce"] = ex3194(False)
FIGURES["ex3194_corrige"] = ex3194(True)


# 3195 : échelle de 4,5 m, pied à 1,2 m -> hauteur 4,34 m
def echelle(corrige):
    U = .8
    A, B, C = (0, 0), (1.2 * U, 0), (0, 4.337 * U)
    s = [r"\fill[otMuted!25] (-.35,0) rectangle (0,%s);" % f(C[1] + .6),
         r"\draw[otMuted,line width=.8pt] (0,0) -- (0,%s);" % f(C[1] + .6),
         r"\draw[otMuted,line width=.8pt] (-.35,0) -- (2.4,0);"]
    s += [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corrige else "otSky", P(A), P(B), P(C))]
    s += [r"\draw[otOrange!90!black,line width=2.2pt] %s -- %s;" % (P(B), P(C))]
    s += angle_droit(B, A, C, "otNavy")
    s += [r"\node[lab,anchor=north] at %s {1,2 m};" % P((.48, -.2))] + lseg(B, C, "4,5 m", -1, d=.14)
    if corrige:
        s += [r"\draw[geoReponse,line width=1.8pt] %s -- %s;" % (P(A), P(C))]
        s += [r"\node[lab,anchor=east] at (-.45,2.0) {%s};" % (V % r"$\approx 4{,}34$ m")]
    s += pt(A, "A", 215, d=.16) + pt(B, "B", 330) + pt(C, "C", 30, d=.16)
    s += [r"\node[txt,text=otMuted,anchor=east] at (-.45,.75) {mur};",
          r"\node[txt,text=otMuted,anchor=north] at (2.0,-.12) {sol};"]
    return figure(s)


FIGURES["ex3195_enonce"] = echelle(False)
FIGURES["ex3195_corrige"] = echelle(True)


# 3196 : additionner ou soustraire ?
def ex3196(corrige):
    s = []
    U = .34
    cot = {(0, 1): "6", (0, 2): "4"}
    if corrige:
        cot[(1, 2)] = r"$\approx 7{,}2$"
    s += rect_tri(6, 4, U, "RTS", cot, vert=[(1, 2)], traits_verts=[(1, 2)] if corrige else [], noms_ang=[225, 315, 90])
    s += legende(1.02, -.55, "(a)")
    o = (2.95, 0)
    cot = {(0, 2): "7", (1, 2): "10"}
    if corrige:
        cot[(0, 1)] = r"$\approx 7{,}1$"
    s += rect_tri(51 ** .5, 7, U, "LMK", cot, vert=[(0, 1)], traits_verts=[(0, 1)] if corrige else [],
                  noms_ang=[225, 315, 90], origine=o)
    s += legende(o[0] + 1.21, -.55, "(b)")
    o = (6.3, 0)
    cot = {(0, 2): "2,5", (1, 2): "6,5"}
    if corrige:
        cot[(0, 1)] = "6"
    s += rect_tri(6, 2.5, U, "VUW", cot, vert=[(0, 1)], traits_verts=[(0, 1)] if corrige else [],
                  noms_ang=[225, 315, 90], origine=o)
    s += legende(o[0] + 1.02, -.55, "(c)")
    s += [r"\node[txt,text=otMuted,anchor=north west] at (-.4,-1.0) {longueurs en cm};"]
    return figure(s)


FIGURES["ex3196_enonce"] = ex3196(False)
FIGURES["ex3196_corrige"] = ex3196(True)


# 3197 : isocèle AB = AC = 10, BC = 12, H milieu de [BC] -> AH = 8
def isocele(corrige):
    U = .32
    B, C, A, H = (0, 0), (12 * U, 0), (6 * U, 8 * U), (6 * U, 0)
    s = [r"\coordinate (hB) at %s; \coordinate (hH) at %s; \coordinate (hC) at %s;" % (P(B), P(H), P(C))]
    s += triangle([B, C, A], "BCA", cotes={(0, 2): "10 cm", (1, 2): "10 cm"}, noms_ang=[225, 315, 90])
    if corrige:
        s += [r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(B), P(H), P(A)),
              r"\draw[geoTrait] %s -- %s -- %s;" % (P(H), P(B), P(A))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.6pt" if corrige else "aide", P(A), P(H))]
    s += angle_droit(C, H, A, "otGreenDark" if corrige else "otOrange!90!black")
    s += [r"\codage{hB}{hH}", r"\codage{hH}{hC}"]
    if corrige:
        s += [r"\node[lab,anchor=north] at %s {6 cm};" % P((3 * U, -.2))]
        s += lab((H[0], A[1] * .45), V % "8 cm", 0, d=.12)
    else:
        s += [r"\node[lab,anchor=north] at %s {$BC = 12$ cm};" % P((6 * U, -.55))]
    s += pt(H, "H", 270, "otGreenDark" if corrige else "otNavy", d=.18)
    return figure(s)


FIGURES["ex3197_enonce"] = isocele(False)
FIGURES["ex3197_corrige"] = isocele(True)


# 3198 : repère A(1 ; 1), B(7 ; 1), C(7 ; 9), D(-2 ; 5)
def repere(etape):
    U = .5
    s = [r"\begin{scope}[x=%scm,y=%scm]" % (f(U), f(U)),
         r"\draw[grille,step=1] (-3.5,-.5) grid (8.5,10.5);",
         r"\draw[axe] (-3.5,0) -- (9,0);", r"\draw[axe] (0,-.5) -- (0,11);"]
    for k in range(-3, 9):
        if k:
            s.append(r"\draw[otMuted,line width=.5pt] (%d,-.1) -- (%d,.1);" % (k, k))
    for k in range(1, 11):
        s.append(r"\draw[otMuted,line width=.5pt] (-.1,%d) -- (.1,%d);" % (k, k))
    for k in (-2, 1, 7):
        s.append(r"\node[grad,anchor=north] at (%d,-.15) {$%d$};" % (k, k))
    for k in ((9,) if etape == 2 else (5, 9)):
        s.append(r"\node[grad,anchor=east] at (-.15,%d) {$%d$};" % (k, k))
    s.append(r"\node[grad,anchor=north east] at (-.1,-.1) {$0$};")
    if etape == 0:
        s.append(r"\fill[otSky] (1,1) -- (7,1) -- (7,9) -- cycle;")
        s.append(r"\draw[geoTrait] (1,1) -- (7,1) -- (7,9) -- cycle;")
    elif etape == 1:
        s.append(r"\fill[otGreen!16] (1,1) -- (7,1) -- (7,9) -- cycle;")
        s.append(r"\draw[geoTrait] (1,1) -- (7,1) -- (7,9);")
        s.append(r"\draw[geoReponse,line width=1.5pt] (1,1) -- (7,9);")
        s.append(r"\draw[otGreenDark,line width=.6pt] (6.55,1) -- (6.55,1.45) -- (7,1.45);")
        s.append(r"\node[lab,anchor=south] at (4,1.1) {$6$};")
        s.append(r"\node[lab,anchor=west] at (7.2,5) {$8$};")
        s.append(r"\node[lab,text=otGreenDark,anchor=south east] at (3.85,5.2) {$AC = 10$};")
    else:
        s.append(r"\fill[otGreen!16] (1,1) -- (-2,1) -- (-2,5) -- cycle;")
        s.append(r"\fill[otGreen!16] (-2,5) -- (7,5) -- (7,9) -- cycle;")
        s.append(r"\draw[aide] (1,1) -- (-2,1) -- (-2,5);")
        s.append(r"\draw[aide] (-2,5) -- (7,5) -- (7,9);")
        s.append(r"\draw[otOrange!90!black,line width=.6pt] (-1.55,1) -- (-1.55,1.45) -- (-2,1.45);")
        s.append(r"\draw[otOrange!90!black,line width=.6pt] (6.55,5) -- (6.55,5.45) -- (7,5.45);")
        s.append(r"\draw[geoReponse,line width=1.5pt] (1,1) -- (-2,5);")
        s.append(r"\draw[geoReponse,line width=1.5pt] (-2,5) -- (7,9);")
        s.append(r"\draw[geoTrait,dash pattern=on 2.5pt off 2pt] (1,1) -- (7,9);")
        s.append(r"\node[lab,text=%s,anchor=north] at (-.5,.9) {$3$};" % ORANGE)
        s.append(r"\node[lab,text=%s,anchor=east] at (-2.2,3) {$4$};" % ORANGE)
        s.append(r"\node[lab,text=%s,anchor=north] at (4.6,4.9) {$9$};" % ORANGE)
        s.append(r"\node[lab,text=%s,anchor=west] at (7.2,7) {$4$};" % ORANGE)
        s.append(r"\node[lab,text=otGreenDark,anchor=north east] at (-.86,2.73) {$5$};")
        s.append(r"\node[lab,text=otGreenDark,anchor=north west] at (2.66,6.64) {$\approx 9{,}85$};")
    s.append(r"\end{scope}")
    pts = {"A": ((.5, .5), 225), "B": ((3.5, .5), 315), "C": ((3.5, 4.5), 45), "D": ((-1, 2.5), 135)}
    for nom, (p, ang) in pts.items():
        if etape == 2 and nom == "B":
            continue
        if nom == "D" and etape == 1:
            continue
        s += pt(p, nom, ang)
    if etape == 0:
        pass
    return figure(s)


FIGURES["ex3198_enonce"] = repere(0)
FIGURES["ex3198_corrige"] = repere(1)
FIGURES["ex3198_corrige2"] = repere(2)


# 3199 : losange de diagonales 16 et 12 -> côté 10
def losange(corrige):
    U = .27
    A, B, C, D, O = (-8 * U, 0), (0, -6 * U), (8 * U, 0), (0, 6 * U), (0, 0)
    s = [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D))]
    if corrige:
        s += [r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(A), P(O), P(D))]
    s += [r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D)),
          r"\draw[otNavy,line width=.7pt] %s -- %s %s -- %s;" % (P(A), P(C), P(B), P(D))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(D))]
        s += angle_droit(A, O, D, "otGreenDark", r=.2)
        s += lseg(A, D, V % "10 cm", 1, d=.14)
        s += [r"\node[lab,anchor=north] at %s {8 cm};" % P((-4 * U, -.12))]
        s += [r"\node[lab,anchor=west] at %s {6 cm};" % P((.12, 3 * U - .25))]
    else:
        s += angle_droit(A, O, D, "otNavy", r=.2)
        s += [r"\node[lab,anchor=north] at %s {$AC = 16$ cm et $BD = 12$ cm};" % P((0, -6 * U - .45))]
    s += pt(A, "A", 180) + pt(B, "B", 270) + pt(C, "C", 0) + pt(D, "D", 90) + pt(O, "O", 315, d=.16)
    return figure(s)


FIGURES["ex3199_enonce"] = losange(False)
FIGURES["ex3199_corrige"] = losange(True)


# 3200 : corde à 13 nœuds tendue en triangle 3-4-5
def corde(corrige):
    U = .75
    A, B, C = (0, 0), (4 * U, 0), (0, 3 * U)
    s = [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corrige else "otSky", P(A), P(B), P(C)),
         r"\draw[otOrange!85!black,line width=1.6pt] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    noeuds = [(k * U, 0) for k in range(5)] + [(4 * U - k * .8 * U, k * .6 * U) for k in range(1, 6)] + \
             [(0, (3 - k) * U) for k in range(1, 3)]
    for q in noeuds:
        s.append(r"\fill[otNavy] %s circle (2.4pt);" % P(q))
    if corrige:
        s += angle_droit(B, A, C, "otGreenDark", r=.26)
    s += [r"\node[lab,anchor=north] at %s {4 intervalles};" % P((2 * U, -.18))]
    s += [r"\node[lab,anchor=east] at %s {3 intervalles};" % P((-.18, 1.5 * U))]
    s += lseg(B, C, "5 intervalles", -1, d=.16)
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=south west] at %s {angle droit};" % P((.38, .3))]
    return figure(s)


FIGURES["ex3200_enonce"] = corde(False)
FIGURES["ex3200_corrige"] = corde(True)

# 3201 : erreur 3 corrigée (rectangle en B, AC = 10, AB = 6 -> BC = 8)
FIGURES["ex3201_corrige"] = figure(rect_tri(8, 6, .3, "BCA", {(0, 2): "6", (1, 2): "10", (0, 1): "8"},
                                            vert=[(0, 1)], traits_verts=[(0, 1)], noms_ang=[225, 315, 90]))


# 3202 : rampe (hauteur 0,5 m, avancée 6 m) — schéma, hauteur exagérée
def rampe(corrige):
    D, H, S = (0, 0), (5.6, 0), (5.6, 1.3)
    s = [r"\fill[otMuted!25] %s rectangle %s;" % (P((5.6, 0)), P((6.6, 2.6))),
         r"\draw[otMuted,line width=.8pt] %s -- %s -- %s;" % (P((6.6, 1.3)), P((5.6, 1.3)), P((5.6, 0))),
         r"\draw[otMuted,line width=.8pt] (-.4,0) -- (6.6,0);",
         r"\fill[white] %s rectangle %s;" % (P((5.95, 1.3)), P((6.45, 2.4))),
         r"\draw[otMuted,line width=.6pt] %s rectangle %s;" % (P((5.95, 1.3)), P((6.45, 2.4)))]
    s += [r"\node[txt,text=otMuted,anchor=south] at %s {porte};" % P((6.2, 2.45))]
    cot = {(0, 1): "6 m", (1, 2): "0,5 m"}
    if corrige:
        cot[(0, 2)] = r"$\approx 6{,}02$ m"
    else:
        cot[(0, 2)] = "rampe"
    s += triangle([D, H, S], "DHS", droit=1, cotes=cot, vert=[(0, 2)] if corrige else [],
                  traits_verts=[(0, 2)] if corrige else [], noms_ang=[120, 300, 120])
    s += [r"\node[txt,text=otMuted,anchor=north west] at (-.4,-.55) {schéma : la hauteur est exagérée};"]
    return figure(s)


FIGURES["ex3202_enonce"] = rampe(False)
FIGURES["ex3202_corrige"] = rampe(True)


# 3203 : terrain de football 105 x 68
def terrain(corrige):
    U = .05
    A, B, C, D = (0, 0), (105 * U, 0), (105 * U, 68 * U), (0, 68 * U)
    M = (40 * U, 68 * U)
    O = (52.5 * U, 34 * U)
    s = [r"\fill[otGreen!10] %s rectangle %s;" % (P(A), P(C)),
         r"\draw[geoTrait] %s rectangle %s;" % (P(A), P(C))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(A), P(C)),
              r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(A), P(M))]
        s += angle_droit(A, D, M, "otGreenDark")
        s += angle_droit(A, B, C, "otGreenDark")
        s += lseg(A, C, V % r"$\approx 125{,}1$ m", -1, t=.45, d=.12)
        s += lseg(A, M, V % r"$\approx 78{,}9$ m", -1, t=.8, d=.12)
        s += pt(O, "O", 120, "otGreenDark", d=.16)
    else:
        s += angle_droit(A, B, C)
        s += [r"\draw[aide] %s -- %s;" % (P(A), P(M))]
    s += lab((52.5 * U, 0), "105 m", 270, d=.18) + lab((105 * U, 34 * U), "68 m", 0, d=.16)
    s += lab((20 * U, 68 * U), "40 m", 90, d=.18)
    s += pt(A, "A", 225) + pt(B, "B", 315) + pt(C, "C", 45) + pt(D, "D", 135) + pt(M, "M", 90, d=.5)
    return figure(s)


FIGURES["ex3203_enonce"] = terrain(False)
FIGURES["ex3203_corrige"] = terrain(True)


# 3204 : tente canadienne (prisme) et sa section ASB
def tente():
    U = 1.6
    A, B, S = (0, 0), (1.8 * U, 0), (.9 * U, 1.2 * U)
    k = (1.9, 1.3)   # fuite (longueur 2,2 m, raccourcie)
    A2, B2, S2 = [(p[0] + k[0], p[1] + k[1]) for p in (A, B, S)]
    s = [r"\fill[otSky!70] %s -- %s -- %s -- %s -- cycle;" % (P(B), P(B2), P(S2), P(S)),
         r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(S))]
    s += [r"\draw[cache] %s -- %s -- %s %s -- %s;" % (P(A), P(A2), P(B2), P(A2), P(S2))]
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(S)),
          r"\draw[geoTrait] %s -- %s -- %s -- %s;" % (P(B), P(B2), P(S2), P(S))]
    s += [r"\coordinate (eA) at %s; \coordinate (eS) at %s; \coordinate (eB) at %s;" % (P(A), P(S), P(B)),
          r"\codage[2]{eA}{eS}", r"\codage[2]{eS}{eB}"]
    s += lseg(A, S, "1,5 m", 1, t=.3, d=.14)
    s += [r"\node[lab,anchor=north] at %s {1,8 m};" % P((.9 * U, -.15))]
    s += lseg(B, B2, "2,2 m", -1, d=.16)
    s += pt(A, "A", 210) + pt(B, "B", 270) + pt(S, "S", 120)
    return figure(s)


def section(corrige):
    U = 2.2
    A, B, S, H = (0, 0), (1.8 * U, 0), (.9 * U, 1.2 * U), (.9 * U, 0)
    s = [r"\coordinate (tA) at %s; \coordinate (tH) at %s; \coordinate (tB) at %s;" % (P(A), P(H), P(B))]
    s += triangle([A, B, S], "ABS", cotes={(0, 2): "1,5 m", (1, 2): "1,5 m"}, noms_ang=[225, 315, 90])
    s += [r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(A), P(H), P(S)),
          r"\draw[geoTrait] %s -- %s -- %s;" % (P(H), P(A), P(S))]
    s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(S), P(H))]
    s += angle_droit(B, H, S, "otGreenDark")
    s += [r"\codage{tA}{tH}", r"\codage{tH}{tB}"]
    s += [r"\node[lab,anchor=north] at %s {0,9 m};" % P((.45 * U, -.2))]
    s += lab((H[0], S[1] * .45), V % "1,2 m", 0, d=.12)
    s += pt(H, "H", 270, "otGreenDark", d=.18)
    return figure(s)


FIGURES["ex3204_enonce"] = tente()
FIGURES["ex3204_corrige"] = section(True)


# 3205 : boîte 24 x 18 x 16 ; AC = 30 ; AG = 34
def boite(corrige):
    lx, ly, lz = 24 * .19, 18 * .19, 16 * .19
    k = .5
    dx, dy = ly * k * math.cos(math.radians(45)), ly * k * math.sin(math.radians(45))
    A, B, C, D = (0, 0), (lx, 0), (lx + dx, dy), (dx, dy)
    E, F, G, H = [(x, y + lz) for x, y in (A, B, C, D)]
    s = [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(F), P(E)),
         r"\fill[otSky!60] %s -- %s -- %s -- %s -- cycle;" % (P(B), P(C), P(G), P(F)),
         r"\fill[otSky!35] %s -- %s -- %s -- %s -- cycle;" % (P(E), P(F), P(G), P(H))]
    s += [r"\draw[cache] %s -- %s -- %s %s -- %s;" % (P(A), P(D), P(C), P(D), P(H))]
    if corrige:
        s += [r"\fill[otGreen!22] %s -- %s -- %s -- cycle;" % (P(A), P(C), P(G)),
              r"\draw[otGreenDark,line width=1.2pt,dash pattern=on 3pt off 2pt] %s -- %s;" % (P(A), P(C)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(G))]
        s += angle_droit(A, C, G, "otGreenDark", r=.18)
    s += [r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle %s -- %s -- %s -- %s %s -- %s -- %s;"
          % (P(A), P(B), P(F), P(E), P(B), P(C), P(G), P(F), P(E), P(H), P(G))]
    s += lab(((A[0] + B[0]) / 2, 0), "24 cm", 270, d=.16)
    s += lab(((B[0] + C[0]) / 2, (B[1] + C[1]) / 2), "18 cm", 315, d=.16)
    s += lab((0, lz / 2), "16 cm", 180, d=.16)
    if corrige:
        s += [r"\node[lab,text=otGreenDark,anchor=north] at %s {$AC = 30$ cm \quad et \quad $AG = 34$ cm};"
              % P(((lx + dx) / 2, -.62))]
    s += pt(A, "A", 225) + pt(B, "B", 300) + pt(C, "C", 330, d=.16) + pt(D, "D", 160, d=.18)
    s += pt(E, "E", 150) + pt(F, "F", 235, d=.16) + pt(G, "G", 45) + pt(H, "H", 90)
    return figure(s)


FIGURES["ex3205_enonce"] = boite(False)
FIGURES["ex3205_corrige"] = boite(True)


# 3206 : spirale de Théodore
def spirale(corrige, n=8):
    U = 1.35
    pts = [(1.0, 0.0)]
    for _ in range(n - 1):
        x, y = pts[-1]
        r = math.hypot(x, y)
        pts.append((x - y / r, y + x / r))
    pts = [(x * U, y * U) for x, y in pts]
    O = (0, 0)
    s = []
    for i in range(n - 1):
        coul = "otGreen!16" if (corrige and i < 3) else ("otSky" if i % 2 == 0 else "otSky!55")
        s.append(r"\fill[%s] %s -- %s -- %s -- cycle;" % (coul, P(O), P(pts[i]), P(pts[i + 1])))
    for i in range(n):
        s.append(r"\draw[otNavy,line width=.6pt] %s -- %s;" % (P(O), P(pts[i])))
    s.append(r"\draw[geoTrait] %s -- %s;" % (P(O), P(pts[0])))
    s.append(r"\draw[geoTrait] " + " -- ".join(P(p) for p in pts) + ";")
    if corrige:
        for i in (1, 2, 3):
            s.append(r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(O), P(pts[i])))
    for i in range(n - 1):
        s += angle_droit(O, pts[i], pts[i + 1], "otNavy", r=.14)
    # étiquettes des sommets, vers l'extérieur
    for i, p in enumerate(pts):
        ang = math.degrees(math.atan2(p[1], p[0]))
        s += pt(p, "A_{%d}" % (i + 1), ang, d=.14)
    s += pt(O, "O", 270, d=.16)
    # « 1 » sur [A1A2] (à l'extérieur) et sur [OA1]
    s += [r"\node[lab,anchor=north] at %s {$1$};" % P((U / 2, -.1))]
    s += lab(((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2), "$1$", 0, d=.12)
    if corrige:
        vals = [r"$\sqrt{2}$", r"$\sqrt{3}$", r"$2$"]
        for i, v in zip((1, 2, 3), vals):
            p = pts[i]
            m = (p[0] * .62, p[1] * .62)
            # étiquette à côté du rayon, dans le triangle suivant (sens trigonométrique)
            ang = math.degrees(math.atan2(p[1], p[0])) - 90
            s += lab(m, V % v, ang + 180, d=.1)
    return figure(s)


FIGURES["ex3206_enonce"] = spirale(False)
FIGURES["ex3206_corrige"] = spirale(True)


# 3207 : voilier P -> N (15 km nord) -> E (8 km est) -> F (9 km sud)
def voilier(corrige):
    U = .25
    Pp, N, E, F, L = (0, 0), (0, 15 * U), (8 * U, 15 * U), (8 * U, 6 * U), (0, 6 * U)
    s = []
    if corrige:
        s += [r"\fill[otGreen!16] %s -- %s -- %s -- cycle;" % (P(Pp), P(L), P(F))]
        s += [r"\draw[aide] %s -- %s;" % (P(L), P(F))]
        s += angle_droit(Pp, L, F, "otOrange!90!black", r=.18)
        s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(Pp), P(F))]
    arr = r"\draw[otNavy,line width=1.3pt,-{Stealth[length=2.6mm]}] %s -- %s;"
    s += [arr % (P(Pp), P((N[0], N[1] - .04))), arr % (P(N), P((E[0] - .04, E[1]))), arr % (P(E), P((F[0], F[1] + .04)))]
    s += angle_droit(Pp, N, E)
    s += lab((0, 12 * U), "15 km", 180, d=.16) + lab((4 * U, 15 * U), "8 km", 90, d=.16)
    s += lab((8 * U, 10.5 * U), "9 km", 0, d=.16)
    if corrige:
        s += [r"\node[lab,text=%s,anchor=north] at %s {8 km};" % (ORANGE, P((4 * U, 6 * U - .08)))]
        s += lab((0, 3 * U), "6 km", 180, d=.16)
        s += lseg(Pp, F, V % "10 km", -1, t=.42, d=.1)
    s += pt(Pp, "P", 225) + pt(N, "N", 135) + pt(E, "E", 45) + pt(F, "F", 0)
    if corrige:
        s += pt(L, "L", 180)
    s += [r"\node[txt,text=otMuted,anchor=west] at %s {port};" % P((.25, -.12))]
    s += [r"\draw[otMuted,line width=.7pt,-{Stealth[length=2mm]}] (3.4,.2) -- (3.4,1.0);",
          r"\node[txt,text=otMuted,anchor=south] at (3.4,1.05) {N};"]
    return figure(s)


FIGURES["ex3207_enonce"] = voilier(False)
FIGURES["ex3207_corrige"] = voilier(True)


# 3208 : écran 110,7 x 62,3 -> diagonale 127,0 cm
def ecran(corrige):
    U = .047
    w, h = 110.7 * U, 62.3 * U
    s = [r"\fill[otInk!85] (-.15,-.15) rectangle %s;" % P((w + .15, h + .15)),
         r"\fill[otSky] (0,0) rectangle %s;" % P((w, h)),
         r"\fill[otInk!85] %s rectangle %s;" % (P((w / 2 - .35, -.15)), P((w / 2 + .35, -.45))),
         r"\fill[otInk!85] %s rectangle %s;" % (P((w / 2 - 1.0, -.45)), P((w / 2 + 1.0, -.55)))]
    s += [r"\draw[%s] (0,0) -- %s;" % ("geoReponse,line width=1.6pt" if corrige else "aide", P((w, h)))]
    s += angle_droit((0, 0), (w, 0), (w, h), r=.2)
    s += lab((w / 2, -.55), "110,7 cm", 270, d=.12) + lab((w + .15, h / 2), "62,3 cm", 0, d=.16)
    if corrige:
        s += lseg((0, 0), (w, h), V % r"$\approx 127{,}0$ cm", 1, t=.4, d=.14)
    return figure(s)


FIGURES["ex3208_enonce"] = ecran(False)
FIGURES["ex3208_corrige"] = ecran(True)
