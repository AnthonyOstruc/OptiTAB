# -*- coding: utf-8 -*-
"""Figures de la notion « Raisonner et démontrer » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
utilisés ou obtenus dans la démonstration (corrigés), orange = angles et contre-exemples.
Les figures d'énoncé ne portent que les données (aucun angle droit à démontrer, aucune
longueur à calculer).
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  aide/.style={otGreenDark,line width=.8pt,dash pattern=on 3.5pt off 2pt},
  boite/.style={rounded corners=3pt,line width=.8pt,minimum height=1.25cm,text width=2.2cm,align=center,inner sep=4pt},
}
"""

V = r"\textcolor{otGreenDark}{%s}"
ORANGE = "otOrange!90!black"


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def figure(corps):
    return "\n".join([r"\begin{tikzpicture}[line cap=round]"] + corps + [r"\end{tikzpicture}"])


def lerp(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def direc(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def pt(p, nom, ang, coul="otNavy", d=.14, texte=None):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};"
                 % (texte or ("otInk" if coul == "otNavy" else coul), (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, coul="otInk"):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    return [r"\node[lab,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(q), txt)]


def lseg(p, q, txt, cote=1, t=.5, d=.14, coul="otInk"):
    """Étiquette du segment [pq], à gauche (cote=1) ou à droite (cote=-1) de p→q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, P(m), txt)]


def ext(p, q, r):
    """cote (1 ou -1) qui place une étiquette de [pq] du côté opposé à r."""
    cr = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return -1 if cr > 0 else 1


def angle_droit(p, sommet, q, coul="otNavy", r=.22):
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L * r, (b[1] - a[1]) / L * r)
    a, b = u(sommet, p), u(sommet, q)
    p1 = (sommet[0] + a[0], sommet[1] + a[1])
    p2 = (sommet[0] + a[0] + b[0], sommet[1] + a[1] + b[1])
    p3 = (sommet[0] + b[0], sommet[1] + b[1])
    return [r"\draw[%s,line width=.65pt] %s -- %s -- %s;" % (coul, P(p1), P(p2), P(p3))]


def arc_angle(o, p, q, r=.45, coul=ORANGE, n=1, txt=None, rl=None, lw=.75, coche=False):
    """Arc de l'angle saillant (p, o, q) ; n arcs concentriques ; texte facultatif sur la bissectrice ;
    coche : petit trait radial au milieu de l'arc (codage d'angles égaux)."""
    a1, a2 = direc(o, p), direc(o, q)
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    if a2 < a1:
        a2 += 360
    s = []
    for k in range(n):
        rr = r + .07 * k
        dep = (o[0] + rr * math.cos(math.radians(a1)), o[1] + rr * math.sin(math.radians(a1)))
        s.append(r"\draw[%s,line width=%spt] %s arc (%s:%s:%s);" % (coul, f(lw), P(dep), f(a1), f(a2), f(rr)))
    if coche:
        am = math.radians((a1 + a2) / 2)
        c1 = (o[0] + (r - .09) * math.cos(am), o[1] + (r - .09) * math.sin(am))
        c2 = (o[0] + (r + .09) * math.cos(am), o[1] + (r + .09) * math.sin(am))
        s.append(r"\draw[%s,line width=%spt] %s -- %s;" % (coul, f(lw), P(c1), P(c2)))
    if txt:
        am = math.radians((a1 + a2) / 2)
        R = rl or r + .32
        c = (o[0] + R * math.cos(am), o[1] + R * math.sin(am))
        s.append(r"\node[lab,text=%s] at %s {%s};" % (coul, P(c), txt))
    return s


def traits(p, q, n=1, coul="otNavy", L=.12, ecart=.055):
    """n petits traits de codage au milieu de [pq] (longueurs égales)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    Lg = math.hypot(dx, dy)
    ux, uy = dx / Lg, dy / Lg
    nx, ny = -uy, ux
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    s = []
    for k in range(n):
        c = (m[0] + (k - (n - 1) / 2) * ecart * ux, m[1] + (k - (n - 1) / 2) * ecart * uy)
        a = (c[0] - L / 2 * nx, c[1] - L / 2 * ny)
        b = (c[0] + L / 2 * nx, c[1] + L / 2 * ny)
        s.append(r"\draw[%s,line width=.75pt] %s -- %s;" % (coul, P(a), P(b)))
    return s


def coord(**pts):
    return [" ".join(r"\coordinate (%s) at %s;" % (k, P(v)) for k, v in pts.items())]


def cote(p, q, txt, off=.42, vert=False):
    """Cote de [pq] (noms de coordonnées), décalée vers la gauche de p→q."""
    return [r"\cote[%s]{%s}{%s}{%s}" % (f(off), p, q, (V % txt) if vert else txt)]


def poly(pts, remplir="otSky", trait="geoTrait"):
    ch = " -- ".join(P(p) for p in pts) + " -- cycle"
    s = []
    if remplir:
        s.append(r"\fill[%s] %s;" % (remplir, ch))
    s.append(r"\draw[%s] %s;" % (trait, ch))
    return s


FIGURES = {}
TOLERE = {}


# ================================================================== COURS
def losange(cote_txt=True):
    """Losange ABCD de côté 3 (cm), angle 65° en A : contre-exemple « 4 côtés égaux => carré »."""
    L, al = 3.0, 65
    A = (0, 0)
    B = (L, 0)
    u = (L * math.cos(math.radians(al)), L * math.sin(math.radians(al)))
    D = (u[0], u[1])
    C = (B[0] + u[0], B[1] + u[1])
    s = poly([A, B, C, D], remplir="otOrange!10", trait="geoTrait")
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        s += traits(p, q, 1)
    s += arc_angle(A, B, D, r=.5, txt=r"$65^\circ$", rl=.9)
    if cote_txt:
        s += lseg(A, B, "3 cm", -1, d=.16)
    s += pt(A, "A", 225) + pt(B, "B", 300) + pt(C, "C", 45) + pt(D, "D", 135)
    return figure(s)


FIGURES["cours_losange"] = losange()


def trapeze():
    """Trapèze isocèle ABCD : diagonales de même longueur, ce n'est pas un rectangle."""
    A, B, C, D = (0, 0), (5, 0), (3.8, 2.3), (1.2, 2.3)
    s = poly([A, B, C, D])
    s += [r"\draw[otGreenDark,line width=1.1pt] %s -- %s;" % (P(A), P(C)),
          r"\draw[otGreenDark,line width=1.1pt] %s -- %s;" % (P(B), P(D))]
    s += traits(A, lerp(A, C, .62), 2, "otGreenDark")
    s += traits(B, lerp(B, D, .62), 2, "otGreenDark")
    s += traits(A, D, 1) + traits(B, C, 1)
    s += pt(A, "A", 225) + pt(B, "B", 315) + pt(C, "C", 45) + pt(D, "D", 135)
    s += [r"\node[lab,text=otGreenDark,anchor=north] at (2.5,-.42) {$AC = BD$};"]
    return figure(s)


FIGURES["cours_trapeze"] = trapeze()


def demarche():
    """Schéma vertical d'une étape de démonstration : On sait que -> Or -> Donc (lisible sur téléphone)."""
    st = r"rounded corners=3pt,line width=.8pt,minimum height=1.05cm,text width=3.6cm,align=center,inner sep=4pt"
    s = [r"\node[%s,draw=otNavy,fill=otSky] (a) at (0,0) {{\bfseries On sait que…}\\[1pt]les données};" % st,
         r"\node[%s,draw=otOrange!90!black,fill=otOrange!10] (b) at (0,-1.75) {{\bfseries Or…}\\[1pt]une propriété du cours};" % st,
         r"\node[%s,draw=otGreenDark,fill=otGreen!14] (c) at (0,-3.5) {{\bfseries Donc…}\\[1pt]la conclusion};" % st,
         r"\draw[otMuted,line width=.8pt,-{Stealth[length=2.2mm]}] (a.south) -- (b.north);",
         r"\draw[otMuted,line width=.8pt,-{Stealth[length=2.2mm]}] (b.south) -- (c.north);",
         r"\draw[otGreenDark,line width=.8pt,-{Stealth[length=2.2mm]},rounded corners=8pt] (c.east) -- ++(.55,0) |- (a.east);",
         r"\node[lab,text=otGreenDark,anchor=west,align=left] at (2.55,-1.75) {la conclusion\\devient une\\donnée de l'étape\\suivante};"]
    return figure(s)


FIGURES["cours_demarche"] = demarche()


def rect_tri_513(vert=True):
    U = .45
    A, C, B = (0, 0), (12 * U, 0), (0, 5 * U)
    s = poly([A, C, B], remplir="otGreen!14" if vert else "otSky")
    s += angle_droit(C, A, B, "otGreenDark" if vert else "otNavy")
    s += lseg(A, C, "12 cm", -1, d=.16) + lseg(B, A, "5 cm", -1, d=.16) + lseg(C, B, "13 cm", -1, d=.14)
    s += pt(A, "A", 225) + pt(C, "C", 315) + pt(B, "B", 135)
    return figure(s)


FIGURES["cours_pythagore"] = rect_tri_513()


def somme_angles():
    B, C, A = (0, 0), (5, 0), (1.8, 2.8)
    E, F = (-.9, 2.8), (6.4, 2.8)
    s = poly([A, B, C])
    s += [r"\draw[geoTrait] %s -- %s;" % (P(E), P(F))]
    o, g = ORANGE, "otGreenDark"
    s += arc_angle(B, C, A, r=.5, coul=o, n=1)
    s += arc_angle(A, E, B, r=.5, coul=o, n=1)
    s += arc_angle(C, A, B, r=.5, coul=g, n=2)
    s += arc_angle(A, C, F, r=.5, coul=g, n=2)
    s += arc_angle(A, B, C, r=.42, coul="otNavy", n=1, lw=.6)
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", 315) + pt(E, "E", 270, d=.16) + pt(F, "F", 270, d=.16)
    s += [r"\node[lab,text=otNavy,anchor=south] at %s {$(d)$};" % P((5.6, 2.92))]
    return figure(s)


FIGURES["cours_somme_angles"] = somme_angles()


def points_pair_impair():
    """2n : deux rangées de n points ; 2n + 1 : un point de plus."""
    e = .42
    s = []

    def groupe(x0, nb, extra, coul_extra=ORANGE):
        out = []
        for k in range(nb):
            for y in (0, e):
                out.append(r"\fill[otNavy] %s circle (2.6pt);" % P((x0 + k * e, y)))
        if extra:
            out.append(r"\fill[%s] %s circle (2.6pt);" % (coul_extra, P((x0 + nb * e, 0))))
        return out
    s += groupe(0, 5, False)
    s += groupe(3.6, 5, True)
    s += [r"\draw[otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}] (-.1,.62) -- (%s,.62);" % f(4 * e + .1),
          r"\node[lab,text=otMuted,anchor=south] at (%s,.82) {$n$ colonnes};" % f(2 * e),
          r"\draw[otMuted,line width=.6pt,decorate,decoration={brace,amplitude=4pt}] (3.5,.62) -- (%s,.62);" % f(3.6 + 4 * e + .1),
          r"\node[lab,text=otMuted,anchor=south] at (%s,.82) {$n$ colonnes};" % f(3.6 + 2 * e)]
    s += [r"\node[lab,anchor=north] at (%s,-.32) {pair : $2n$};" % f(2 * e),
          r"\node[lab,anchor=north] at (%s,-.32) {impair : $2n + 1$};" % f(3.6 + 2.5 * e)]
    return figure(s)


FIGURES["cours_pair_impair"] = points_pair_impair()


# ================================================================== EXERCICES
# 2485 : deux rectangles de même périmètre (contre-exemple)
def deux_rectangles():
    U = .5
    s = poly([(0, 0), (9 * U, 0), (9 * U, U), (0, U)], remplir="otOrange!10")
    x0 = 9 * U + 1.2
    s += poly([(x0, 0), (x0 + 5 * U, 0), (x0 + 5 * U, 5 * U), (x0, 5 * U)], remplir="otOrange!10")
    s += lseg((0, U), (9 * U, U), "9 cm", 1, d=.14) + lseg((0, 0), (0, U), "1 cm", 1, d=.14)
    s += lseg((x0, 5 * U), (x0 + 5 * U, 5 * U), "5 cm", 1, d=.14) + lseg((x0, 0), (x0, 5 * U), "5 cm", 1, d=.14)
    s += [r"\node[lab,anchor=north,align=center] at (%s,-.25) {périmètre $20$ cm\\\textcolor{otGreenDark}{aire $9$ cm²}};" % f(4.5 * U),
          r"\node[lab,anchor=north,align=center] at (%s,-.25) {périmètre $20$ cm\\\textcolor{otGreenDark}{aire $25$ cm²}};" % f(x0 + 2.5 * U)]
    return figure(s)


FIGURES["ex2485_corrige"] = deux_rectangles()


# 2486 : impair + impair = pair (points)
def impair_plus_impair():
    e = .4
    s = []

    def colonnes(x0, nb, extra_haut=None, extra_bas=None, coul_dern=None):
        out = []
        for k in range(nb):
            c = coul_dern if (coul_dern and k == nb - 1) else "otNavy"
            for y in (0, e):
                out.append(r"\fill[%s] %s circle (2.6pt);" % (c, P((x0 + k * e, y))))
        if extra_bas:
            out.append(r"\fill[%s] %s circle (2.6pt);" % (extra_bas, P((x0 + nb * e, 0))))
        return out
    s += colonnes(0, 3, extra_bas=ORANGE)
    s += [r"\node[lab] at (1.85,.2) {$+$};"]
    s += colonnes(2.35, 2, extra_bas=ORANGE)
    s += [r"\node[lab] at (3.75,.2) {$=$};"]
    s += colonnes(4.25, 6, coul_dern="otGreenDark")
    s += [r"\node[lab,anchor=north] at (%s,-.3) {$7$};" % f(1.5 * e),
          r"\node[lab,anchor=north] at (%s,-.3) {$5$};" % f(2.35 + e),
          r"\node[lab,anchor=north] at (%s,-.3) {\textcolor{otGreenDark}{$12$ : pair}};" % f(4.25 + 2.5 * e)]
    return figure(s)


FIGURES["ex2486_corrige"] = impair_plus_impair()


# 2489 : contre-exemples géométriques
def cerf_volant():
    O = (0, 0)
    E, G, F, H = (0, 1.25), (0, -2.6), (-1.6, 0), (1.6, 0)
    s = poly([E, F, G, H], remplir="otOrange!10")
    s += [r"\draw[otGreenDark,line width=1pt] %s -- %s;" % (P(E), P(G)),
          r"\draw[otGreenDark,line width=1pt] %s -- %s;" % (P(F), P(H))]
    s += angle_droit(H, O, E, "otGreenDark")
    s += traits(E, F, 1) + traits(E, H, 1) + traits(F, G, 2) + traits(H, G, 2)
    s += pt(E, "E", 90) + pt(F, "F", 180) + pt(G, "G", 270) + pt(H, "H", 0)
    s += [r"\fill[otGreenDark] (0,0) circle (1.8pt);", r"\node[lab,text=otGreenDark,anchor=north east] at (-.08,-.08) {$O$};"]
    return figure(s)


FIGURES["ex2489_cerf_volant"] = cerf_volant()


def deux_equilateraux():
    def tri(x0, L, noms):
        A, B = (x0, 0), (x0 + L, 0)
        C = (x0 + L / 2, L * math.sqrt(3) / 2)
        s = poly([A, B, C], remplir="otOrange!10")
        for o, p, q in ((A, B, C), (B, C, A), (C, A, B)):
            s += arc_angle(o, p, q, r=.32, coul=ORANGE)
        s += arc_angle(A, B, C, r=.32, coul=ORANGE, txt=r"$60^\circ$", rl=.78 if L > 2 else .7)[-1:]
        s += lseg(A, B, "%s cm" % ("2" if L < 2.5 else "4"), -1, d=.15)
        s += pt(A, noms[0], 225) + pt(B, noms[1], 315) + pt(C, noms[2], 90)
        return s
    s = tri(0, 1.8, "ABC") + tri(2.7, 3.6, "DEF")
    return figure(s)


FIGURES["ex2489_equilateraux"] = deux_equilateraux()


# 2490 : triangle isocèle non équilatéral
def isocele():
    U = .75
    S, T = (0, 0), (3 * U, 0)
    R = (1.5 * U, math.sqrt(16 - 2.25) * U)
    s = poly([R, S, T], remplir="otOrange!10")
    s += traits(R, S, 1) + traits(R, T, 1)
    s += lseg(S, R, "4 cm", 1, d=.16) + lseg(R, T, "4 cm", 1, d=.16) + lseg(S, T, "3 cm", -1, d=.15)
    s += pt(R, "R", 90) + pt(S, "S", 225) + pt(T, "T", 315)
    return figure(s)


FIGURES["ex2490_isocele"] = isocele()


# 2491 : AB = 3, AC = 4, angle en A non précisé
def ex2491_enonce():
    U = .8
    A, C = (0, 0), (4 * U, 0)
    B = (3 * U * math.cos(math.radians(105)), 3 * U * math.sin(math.radians(105)))
    s = poly([A, C, B])
    s += lseg(A, C, "4 cm", -1, d=.16) + lseg(B, A, "3 cm", -1, d=.16)
    s += lseg(C, B, "?", -1, d=.14)
    s += pt(A, "A", 250) + pt(C, "C", 315) + pt(B, "B", 120)
    return figure(s)


FIGURES["ex2491_enonce"] = ex2491_enonce()


def ex2491_corrige():
    U = .75
    # cas 1 : rectangle en A (AC horizontal 4, AB vertical 3)
    A, C, B = (0, 0), (4 * U, 0), (0, 3 * U)
    s = poly([A, C, B], remplir="otSky")
    s += angle_droit(C, A, B, "otGreenDark")
    s += [r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(C), P(B))]
    s += lseg(A, C, "4 cm", -1, d=.15) + lseg(B, A, "3 cm", -1, d=.15) + lseg(C, B, V % "5 cm", -1, d=.13)
    s += pt(A, "A", 225) + pt(C, "C", 315) + pt(B, "B", 135)
    s += [r"\node[lab,anchor=north] at %s {rectangle en $A$};" % P((2 * U, -.62))]
    # cas 2 : rectangle en B (BA vertical 3, BC horizontal racine 7, AC = 4)
    x0 = 4 * U + 1.5
    B2, A2, C2 = (x0, 0), (x0, 3 * U), (x0 + math.sqrt(7) * U, 0)
    s += poly([B2, C2, A2], remplir="otSky")
    s += angle_droit(C2, B2, A2, "otGreenDark")
    s += [r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(B2), P(C2))]
    s += lseg(B2, C2, V % r"$\sqrt{7}$ cm", -1, d=.15) + lseg(A2, B2, "3 cm", -1, d=.15)
    s += lseg(C2, A2, "4 cm", -1, d=.13)
    s += pt(B2, "B", 225) + pt(C2, "C", 315) + pt(A2, "A", 135)
    s += [r"\node[lab,anchor=north] at %s {rectangle en $B$};" % P((x0 + math.sqrt(7) * U / 2, -.62))]
    return figure(s)


FIGURES["ex2491_corrige"] = ex2491_corrige()


# 2496 : AB = 4,8 ; AC = 6,4 ; BC = 8 (base [BC])
def ex2496(corrige):
    U = .62
    B, C = (0, 0), (8 * U, 0)
    A = (4.8 * .6 * U, 4.8 * .8 * U)
    H = (A[0], 0)
    s = poly([A, B, C], remplir="otGreen!14" if corrige else "otSky")
    s += lseg(B, A, "4,8 cm", 1, d=.16) + lseg(A, C, "6,4 cm", 1, d=.16) + lseg(B, C, "8 cm", -1, d=.15, t=.75)
    if corrige:
        s += angle_droit(B, A, C, "otGreenDark")
        s += [r"\draw[aide] %s -- %s;" % (P(A), P(H))]
        s += angle_droit(C, H, A, "otGreenDark", r=.18)
        s += lseg(H, A, V % "3,84 cm", -1, d=.12, t=.45)
        s += pt(H, "H", 270, coul="otGreenDark")
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340)
    return figure(s)


FIGURES["ex2496_enonce"] = ex2496(False)
FIGURES["ex2496_corrige"] = ex2496(True)


# Thalès : triangle ABC donné par ses côtés, M sur [AB], N sur [AC]
def tri_cotes(ab, ac, bc, U):
    """B = (0,0), C = (bc,0), A au-dessus, à ab de B et ac de C (échelle U)."""
    x = (ab ** 2 - ac ** 2 + bc ** 2) / (2 * bc)
    y = math.sqrt(ab ** 2 - x ** 2)
    return (x * U, y * U), (0, 0), (bc * U, 0)


def thales(A, B, C, rM, rN, L, vert=(), mn_style="geoTrait", extra=None, petit=False):
    M, N = lerp(A, B, rM), lerp(A, C, rN)
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if petit:
        s += [r"\fill[otGreen!18] (A) -- (M) -- (N) -- cycle;"]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;"]
    if mn_style:
        s += [r"\draw[%s] (M) -- (N);" % mn_style]
    deux_g = "AM" in L and "AB" in L
    deux_d = any(k in L for k in ("AN", "AP")) and "AC" in L
    if "AM" in L:
        s += cote("M", "A", L["AM"], .42, "AM" in vert)
    if "AB" in L:
        s += cote("B", "A", L["AB"], 1.05 if deux_g else .42, "AB" in vert)
    if "AN" in L:
        s += cote("A", "N", L["AN"], .42, "AN" in vert)
    if "AC" in L:
        s += cote("A", "C", L["AC"], 1.05 if deux_d else .42, "AC" in vert)
    if "BC" in L:
        s += cote("C", "B", L["BC"], .42, "BC" in vert)
    if "MN" in L:
        s += lseg(M, N, (V % L["MN"]) if "MN" in vert else L["MN"], cote=-1, d=.12)
    if extra:
        s += extra(A, B, C, M, N)
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340)
    s += pt(M, "M", 195, d=.16) + pt(N, "N", 345, d=.16)
    return figure(s)


A97, B97, C97 = tri_cotes(7.5, 10, 12, .44)
FIGURES["ex2497_enonce"] = thales(A97, B97, C97, .4, .4,
                                  {"AM": "3 cm", "AB": "7,5 cm", "AN": "4 cm", "AC": "10 cm", "BC": "12 cm"})
FIGURES["ex2497_corrige"] = thales(A97, B97, C97, .4, .4,
                                   {"AM": "3 cm", "AB": "7,5 cm", "AN": "4 cm", "AC": "10 cm", "BC": "12 cm",
                                    "MN": "4,8 cm"}, vert=("MN",), mn_style="geoReponse,line width=1.3pt", petit=True)


def ex2497_corrige_p():
    """(MN) parallèle (pointillés verts) et (MP) qui ne l'est pas : AP = 5 cm."""
    A, B, C = A97, B97, C97
    M, N, Pp = lerp(A, B, .4), lerp(A, C, .4), lerp(A, C, .5)
    s = coord(A=A, B=B, C=C, M=M, N=N, Q=Pp)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;", r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
          r"\draw[aide] (M) -- (N);", r"\draw[otOrange!90!black,line width=1.1pt] (M) -- (Q);"]
    s += cote("M", "A", "3 cm", .42) + cote("B", "A", "7,5 cm", 1.05)
    s += cote("A", "Q", "5 cm", .66) + cote("A", "C", "10 cm", 1.3)
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 195, d=.16)
    s += pt(N, "N", 60, coul="otGreenDark", d=.16)
    s += pt(Pp, "P", 235, coul=ORANGE, d=.18, texte="otOrange!80!black")
    return figure(s)


FIGURES["ex2497_corrige_p"] = ex2497_corrige_p()


# 2498 : parallélogramme ABCD (en fait un rectangle) de côtés 6 et 8, diagonale 10
def ex2498(corrige):
    U = .5
    A, B, C, D = (0, 6 * U), (0, 0), (8 * U, 0), (8 * U, 6 * U)
    O = (4 * U, 3 * U)
    s = poly([A, B, C, D])
    s += [r"\draw[geoTrait] %s -- %s;" % (P(A), P(C))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.3pt" if corrige else "otNavy!55,line width=.7pt,dash pattern=on 3pt off 2pt", P(B), P(D))]
    s += lseg(A, B, "6 cm", -1, d=.16) + lseg(B, C, "8 cm", -1, d=.15)
    s += lseg(A, C, "10 cm", 1, d=.12, t=.74)
    if corrige:
        s += angle_droit(A, B, C, "otGreenDark", r=.26)
        s += lseg(D, B, V % "10 cm", -1, d=.12, t=.24)
    s += pt(A, "A", 135) + pt(B, "B", 225) + pt(C, "C", 315) + pt(D, "D", 45)
    s += pt(O, "O", 90, d=.17)
    return figure(s)


FIGURES["ex2498_enonce"] = ex2498(False)
FIGURES["ex2498_corrige"] = ex2498(True)


# 2499 : démonstration de Pythagore par les aires
def carre_pythagore(corrige):
    a, b = 3.0, 1.6
    L = a + b
    P1, P2, P3, P4 = (a, 0), (L, a), (b, L), (0, b)
    s = [r"\fill[%s] %s -- %s -- %s -- %s -- cycle;" % ("otGreen!16" if corrige else "otOrange!10", P(P1), P(P2), P(P3), P(P4))]
    tris = [((0, 0), P1, P4), ((L, 0), P2, P1), ((L, L), P3, P2), ((0, L), P4, P3)]
    for o, p, q in tris:
        s.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(o), P(p), P(q)))
    s += [r"\draw[geoTrait] (0,0) rectangle %s;" % P((L, L)),
          r"\draw[%s] %s -- %s -- %s -- %s -- cycle;" % ("otGreenDark,line width=1.1pt" if corrige else "geoTrait",
                                                         P(P1), P(P2), P(P3), P(P4))]
    s += [r"\node[lab] at %s {$a$};" % P((a / 2, -.27)), r"\node[lab] at %s {$b$};" % P((a + b / 2, -.27)),
          r"\node[lab] at %s {$a$};" % P((L + .27, a / 2)), r"\node[lab] at %s {$b$};" % P((L + .27, a + b / 2)),
          r"\node[lab] at %s {$a$};" % P((L - a / 2, L + .27)), r"\node[lab] at %s {$b$};" % P((b / 2, L + .27)),
          r"\node[lab] at %s {$a$};" % P((-.27, L - a / 2)), r"\node[lab] at %s {$b$};" % P((-.27, b / 2))]
    cc = "otGreenDark" if corrige else "otInk"
    for p, q in ((P1, P2), (P2, P3), (P3, P4), (P4, P1)):
        s += lseg(p, q, "$c$", 1, d=.2, coul=cc)
    if corrige:
        s += arc_angle(P1, (0, 0), P4, r=.62, coul=ORANGE, txt=r"$\alpha$", rl=1.0)
        s += arc_angle(P1, (L, 0), P2, r=.42, coul="otNavy", txt=r"$\beta$", rl=.72)
        s += angle_droit(P4, P1, P2, "otGreenDark", r=.28)
        s += [r"\node[lab,text=otGreenDark] at %s {$c^2$};" % P((L / 2, L / 2))]
    return figure(s)


FIGURES["ex2499_enonce"] = carre_pythagore(False)
FIGURES["ex2499_corrige"] = carre_pythagore(True)


# 2501 : rectangle de périmètre 40 cm, puis courbe de l'aire
def ex2501_enonce():
    s = poly([(0, 0), (4.2, 0), (4.2, 2.1), (0, 2.1)])
    s += [r"\node[lab,anchor=north] at (2.1,-.15) {$x$};",
          r"\node[lab,align=center] at (2.1,1.05) {périmètre : $40$ cm};"]
    return figure(s)


FIGURES["ex2501_enonce"] = ex2501_enonce()

FIGURES["ex2501_corrige"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.6cm, xmin=-1, xmax=22, ymin=-8, ymax=118,
  xtick={5,10,15,20}, ytick={20,40,60,80,100}, xlabel={$x$}, ylabel={$A(x)$}]
\addplot[courbe,domain=0:20] {x*(20-x)};
\guides{10}{100}
\guides{7}{91}
\pnt{7}{91}
\pnt[otGreenDark]{10}{100}
\node[lab,text=otGreenDark,anchor=south west] at (axis cs:10.4,101) {maximum : $100$};
\end{axis}
\end{tikzpicture}
"""


# 2502 : le triangle d'or
def triangle_or(corrige):
    U = .95
    AB, BC = 5.0, 2 * 5 * math.sin(math.radians(18))
    B, C = (0, 0), (BC * U, 0)
    h = math.sqrt(AB ** 2 - (BC / 2) ** 2) * U
    A = (BC * U / 2, h)
    D = lerp(A, C, BC / AB)
    s = poly([A, B, C], remplir="otSky")
    if corrige:
        s = [r"\fill[otGreen!14] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(D))] + \
            [r"\fill[otOrange!12] %s -- %s -- %s -- cycle;" % (P(B), P(C), P(D))] + \
            [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    s += [r"\draw[geoTrait] %s -- %s;" % (P(B), P(D))]
    if not corrige:
        s += traits(A, B, 1) + traits(A, C, 1)
    s += arc_angle(A, B, C, r=.75, coul=ORANGE, txt=r"$36^\circ$", rl=1.12)
    if corrige:
        g = "otGreenDark"
        s += arc_angle(B, C, D, r=.55, coul=g, txt=r"$36^\circ$", rl=1.22)
        s += arc_angle(B, D, A, r=.62, coul=g, txt=r"$36^\circ$", rl=1.22)
        s += arc_angle(C, A, B, r=.42, coul=g, txt=r"$72^\circ$", rl=.78)
        s += arc_angle(D, B, C, r=.32, coul=g, txt=r"$72^\circ$", rl=.66)
        s += traits(A, D, 2, g) + traits(D, B, 2, g) + traits(B, C, 2, g)
    else:
        s += arc_angle(B, C, D, r=.6, coul="otNavy", n=1, lw=.65, coche=True)
        s += arc_angle(B, D, A, r=.6, coul="otNavy", n=1, lw=.65, coche=True)
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", 315) + pt(D, "D", 0, d=.16)
    return figure(s)


FIGURES["ex2502_enonce"] = triangle_or(False)
FIGURES["ex2502_corrige"] = triangle_or(True)


# 2504 : M sur [AB], N sur [AC] : AM = 2, AB = 5, AN = 3, AC = 6 (non parallèles)
A04, B04, C04 = tri_cotes(5, 6, 6.2, .62)
FIGURES["ex2504_enonce"] = thales(A04, B04, C04, 2 / 5, 3 / 6,
                                  {"AM": "2 cm", "AB": "5 cm", "AN": "3 cm", "AC": "6 cm"})


def ex2504_corrige():
    A, B, C = A04, B04, C04
    M, N = lerp(A, B, .4), lerp(A, C, .5)
    Pp = lerp(A, C, .4)
    s = coord(A=A, B=B, C=C, M=M, N=N, Q=Pp)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;", r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
          r"\draw[otOrange!90!black,line width=1.1pt] (M) -- (N);", r"\draw[aide] (M) -- (Q);"]
    s += cote("M", "A", "2 cm", .42) + cote("B", "A", "5 cm", 1.05)
    s += cote("A", "Q", "2,4 cm", .42, vert=True) + cote("A", "C", "6 cm", 1.05)
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 195, d=.16)
    s += pt(Pp, "P", 20, coul="otGreenDark", d=.16)
    s += pt(N, "N", 330, coul=ORANGE, d=.16, texte="otOrange!80!black")
    return figure(s)


FIGURES["ex2504_corrige"] = ex2504_corrige()


# 2505 : ABC rectangle en B (AB = 9, BC = 12, AC = 15), E sur [AB] (AE = 6), F sur [AC] (AF = 10)
def ex2505(corrige):
    U = .37
    B, C, A = (0, 0), (12 * U, 0), (0, 9 * U)
    E, F = lerp(A, B, 6 / 9), lerp(A, C, 10 / 15)
    s = coord(A=A, B=B, C=C, E=E, F=F)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if corrige:
        s += [r"\fill[otGreen!18] (A) -- (E) -- (F) -- cycle;"]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;"]
    s += [r"\draw[%s] (E) -- (F);" % ("geoReponse,line width=1.3pt" if corrige else "geoTrait")]
    s += cote("E", "A", "6 cm", .42) + cote("B", "A", "9 cm", 1.05)
    s += cote("A", "F", "10 cm", .42) + cote("A", "C", "15 cm", 1.05) + cote("C", "B", "12 cm", .42)
    if corrige:
        s += angle_droit(A, B, C, "otGreenDark", r=.24)
        s += angle_droit(A, E, F, "otGreenDark", r=.22)
        s += lseg(E, F, V % "8 cm", -1, d=.12, t=.55)
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", 315)
    s += pt(E, "E", 180, d=.16) + pt(F, "F", 35, d=.16)
    return figure(s)


FIGURES["ex2505_enonce"] = ex2505(False)
FIGURES["ex2505_corrige"] = ex2505(True)
