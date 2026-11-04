# -*- coding: utf-8 -*-
"""Figures de la notion « Théorème de Thalès et triangles semblables » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = angles. Longueurs en cotes (flèches grises) : les
morceaux depuis A au premier niveau, les côtés entiers au second niveau.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  aide/.style={otMuted,line width=.65pt,dash pattern=on 3pt off 2pt},
  rayon/.style={otOrange!90!black,line width=.75pt,dash pattern=on 3.5pt off 2pt},
}
"""

V = r"\textcolor{otGreenDark}{%s}"


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def pt(p, nom, ang, coul="otNavy", d=.13, texte=None):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};"
                 % (texte or ("otInk" if coul == "otNavy" else coul), (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, coul="otInk", maths=True):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    t = ("$%s$" % txt) if maths else txt
    return [r"\node[lab,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(q), t)]


def lseg(p, q, txt, cote=1, t=.5, d=.14, coul="otInk", maths=False):
    """Étiquette d'un segment [pq], à gauche (cote=1) ou à droite (cote=-1) de p→q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    tt = ("$%s$" % txt) if maths else txt
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, P(m), tt)]


def coord(**pts):
    return [" ".join(r"\coordinate (%s) at %s;" % (k, P(v)) for k, v in pts.items())]


def arc(c, a1, a2, r, txt=None, rl=None, coul="otOrange!90!black", n=1):
    s = []
    for k in range(n):
        rr = r + .07 * k
        dep = (c[0] + rr * math.cos(math.radians(a1)), c[1] + rr * math.sin(math.radians(a1)))
        s.append(r"\draw[%s,line width=.75pt] %s arc (%s:%s:%s);" % (coul, P(dep), f(a1), f(a2), f(rr)))
    if txt:
        am = (a1 + a2) / 2
        s += lab(c, txt, am, d=rl or r + .14, coul=coul)
    return s


def direc(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def figure(corps, U=1.0):
    return "\n".join([r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round]" % (f(U), f(U))]
                     + corps + [r"\end{tikzpicture}"])


def lerp(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def coul_txt(txt, vert):
    return (V % txt) if vert else txt


FIGURES = {}


# ================================================================== configurations de Thalès
def emboitee(r=.45, L=None, vert=(), noms="AMBNC", petit=False, A=(1.9, 4.4), B=(0, 0), C=(6.2, 0),
             pnoms=None):
    """Configuration emboîtée : M sur [AB], N sur [AC], (MN) // (BC).

    L : étiquettes de longueur (clés AM, MB, AB, AN, NC, AC, MN, BC) ; vert : clés en vert.
    """
    L = L or {}
    a, m, b, n, c_ = noms
    M, N = lerp(A, B, r), lerp(A, C, r)
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if petit:
        s += [r"\fill[otGreen!18] (A) -- (M) -- (N) -- cycle;"]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;"]
    s += [r"\draw[%s] (M) -- (N);" % ("geoReponse,line width=1.2pt" if "MN" in vert else "geoTrait")]
    # cotes : côté gauche (à gauche de B→A) et côté droit (à gauche de A→C)
    def cote(p, q, cle, off):
        if cle in L:
            return [r"\cote[%s]{%s}{%s}{%s}" % (off, p, q, coul_txt(L[cle], cle in vert))]
        return []
    deux_g = any(k in L for k in ("AM", "MB")) and "AB" in L
    deux_d = any(k in L for k in ("AN", "NC")) and "AC" in L
    s += cote("M", "A", "AM", .42) + cote("B", "M", "MB", .42) + cote("B", "A", "AB", 1.05 if deux_g else .42)
    s += cote("A", "N", "AN", .42) + cote("N", "C", "NC", .42) + cote("A", "C", "AC", 1.05 if deux_d else .42)
    s += cote("C", "B", "BC", .42)
    if "MN" in L:
        s += lseg(M, N, coul_txt(L["MN"], "MN" in vert), cote=-1, d=.12)
    pn = pnoms or {}
    s += pt(A, a, pn.get("A", 90)) + pt(B, b, pn.get("B", 200)) + pt(C, c_, pn.get("C", 340))
    s += pt(M, m, pn.get("M", 208), d=.16) + pt(N, n, pn.get("N", 352), d=.16)
    return figure(s)


def papillon(r=.6, L=None, vert=(), noms="AMBNC", petit=False, B=(-2.1, -2.7), C=(2.9, -2.7)):
    """Configuration papillon : M, A, B alignés dans cet ordre ; N, A, C aussi ; (MN) // (BC)."""
    L = L or {}
    a, m, b, n, c_ = noms
    A = (0, 0)
    M, N = (-r * B[0], -r * B[1]), (-r * C[0], -r * C[1])
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    s += [r"\fill[%s] (A) -- (M) -- (N) -- cycle;" % ("otGreen!18" if petit else "otSky")]
    s += [r"\draw[geoTrait] (M) -- (B) (N) -- (C) (B) -- (C);"]
    s += [r"\draw[%s] (M) -- (N);" % ("geoReponse,line width=1.2pt" if "MN" in vert else "geoTrait")]

    def cote(p, q, cle):
        if cle in L:
            return [r"\cote[.42]{%s}{%s}{%s}" % (p, q, coul_txt(L[cle], cle in vert))]
        return []
    s += cote("B", "A", "AB") + cote("A", "C", "AC") + cote("M", "A", "AM") + cote("A", "N", "AN")
    if "MN" in L:
        s += lseg(N, M, coul_txt(L["MN"], "MN" in vert), cote=-1, d=.12)
    if "BC" in L:
        s += lseg(B, C, coul_txt(L["BC"], "BC" in vert), cote=-1, d=.12)
    s += pt(A, a, 180, d=.2) + pt(B, b, 200) + pt(C, c_, 340) + pt(M, m, 20) + pt(N, n, 160)
    return figure(s)


# ================================================================== COURS
FIGURES["cours_emboitee"] = emboitee(.45, petit=True)
FIGURES["cours_papillon"] = papillon(.6, petit=True)

# réciproque : rapports égaux (exemple du cours 4/10 = 6/15)
FIGURES["cours_reciproque"] = emboitee(.4, {"AM": "4 cm", "AB": "10 cm", "AN": "6 cm", "AC": "15 cm"},
                                       vert=("MN",), petit=False)


# triangles semblables
def tri_angles(B, L, beta, gamma):
    t = L * math.sin(math.radians(gamma)) / math.sin(math.radians(beta + gamma))
    A = (B[0] + t * math.cos(math.radians(beta)), B[1] + t * math.sin(math.radians(beta)))
    return A, B, (B[0] + L, B[1])


def marque_angles(A, B, C, specs):
    """specs : liste (sommet, texte, nb d'arcs, couleur) ; sommet parmi 'A','B','C'."""
    pts_ = {"A": (A, B, C), "B": (B, C, A), "C": (C, A, B)}
    s = []
    for som, txt, nb, coul in specs:
        o, p, q = pts_[som]
        a1, a2 = direc(o, p), direc(o, q)
        if (a2 - a1) % 360 > 180:
            a1, a2 = a2, a1
        if a2 < a1:
            a2 += 360
        s += arc(o, a1, a2, .5, txt, rl=.82, coul=coul, n=nb)
    return s


def semblables_cours():
    A, B, C = tri_angles((0, 0), 2.8, 62, 44)
    D, E, F = tri_angles((3.9, 0), 4.2, 62, 44)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(D), P(E), P(F)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(D), P(E), P(F))]
    o, g, n_ = "otOrange!90!black", "otGreenDark", "otNavy"
    s += marque_angles(A, B, C, [("B", None, 1, o), ("C", None, 2, g), ("A", None, 3, n_)])
    s += marque_angles(D, E, F, [("B", None, 1, o), ("C", None, 2, g), ("A", None, 3, n_)])
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", 315)
    s += pt(D, "D", 90) + pt(E, "E", 225) + pt(F, "F", 315)
    s += [r"\draw[otMuted,line width=.6pt,-{Stealth[length=2mm]}] (1.6,-.5) to[bend right=18] (5.6,-.5);"]
    s += [r"\node[lab,text=otMuted,anchor=north] at (3.6,-.98) {longueurs $\times\,k$};"]
    return figure(s)


FIGURES["cours_semblables"] = semblables_cours()


# ombres (cours et exercice 2094)
def ombres(bh, bo, ah, ao, txt, vert=False, echelle=.32):
    """Bâton (hauteur bh, ombre bo) et arbre (hauteur ah, ombre ao) ; txt : étiquettes."""
    u = echelle
    s = []
    x0 = 0
    Bp, Bs, Bo = (x0 + bo * u, 0), (x0 + bo * u, bh * u), (x0, 0)
    x1 = x0 + bo * u + 1.4
    Ap, As, Ao = (x1 + ao * u, 0), (x1 + ao * u, ah * u), (x1, 0)
    s += [r"\draw[otMuted,line width=.7pt] (-.4,0) -- %s;" % P((Ap[0] + .6, 0))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(Bo), P(Bp), P(Bs)),
          r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!18" if vert else "otSky", P(Ao), P(Ap), P(As))]
    s += [r"\draw[rayon] %s -- %s;" % (P(Bs), P(Bo)), r"\draw[rayon] %s -- %s;" % (P(As), P(Ao))]
    s += [r"\draw[otNavy,line width=2pt] %s -- %s;" % (P(Bp), P(Bs))]
    s += [r"\draw[%s,line width=2.4pt] %s -- %s;" % ("otGreenDark" if vert else "otNavy", P(Ap), P(As))]
    s += [r"\draw[otInk,line width=1.6pt] %s -- %s;" % (P(Bo), P(Bp)), r"\draw[otInk,line width=1.6pt] %s -- %s;" % (P(Ao), P(Ap))]
    s += [r"\draw[otNavy,line width=.6pt] %s -- ++(-.2,0) -- ++(0,.2) -- ++(.2,0);" % P(Bp),
          r"\draw[otNavy,line width=.6pt] %s -- ++(-.2,0) -- ++(0,.2) -- ++(.2,0);" % P(Ap)]
    s += lab(((Bp[0] + Bo[0]) / 2, 0), txt["bo"], 270, d=.16, maths=False)
    s += lab(((Ap[0] + Ao[0]) / 2, 0), txt["ao"], 270, d=.16, maths=False)
    s += lab((Bp[0], Bs[1] / 2), txt["bh"], 0, d=.14, maths=False)
    s += lab((Ap[0], As[1] / 2), coul_txt(txt["ah"], vert), 0, d=.16, maths=False)
    s += [r"\node[txt,text=otMuted,anchor=south] at %s {bâton};" % P((Bp[0], Bs[1] + .12)),
          r"\node[txt,text=otMuted,anchor=south] at %s {arbre};" % P((Ap[0], As[1] + .12)),
          r"\node[txt,text=otOrange!80!black,anchor=south east] at %s {rayons du soleil};" % P(((Ao[0] + As[0]) / 2 - .15, As[1] / 2 + .25))]
    return figure(s)


FIGURES["cours_ombre"] = ombres(1, 1.5, 6, 9, {"bo": "1,5 m", "ao": "9 m", "bh": "1 m", "ah": "$h$"}, echelle=.5)

# ================================================================== EXERCICES
# 2087 : rapports (sans valeurs)
FIGURES["ex2087_enonce"] = emboitee(.45)
FIGURES["ex2087_corrige"] = emboitee(.45, {"AM": "$AM$", "AB": "$AB$", "AN": "$AN$", "AC": "$AC$"},
                                     vert=("MN",), petit=True)

# 2088
FIGURES["ex2088_enonce"] = emboitee(.6, {"AM": "3 cm", "AB": "5 cm", "AC": "10 cm", "BC": "7,5 cm"})
FIGURES["ex2088_corrige"] = emboitee(.6, {"AM": "3 cm", "AB": "5 cm", "AN": "6 cm", "AC": "10 cm", "BC": "7,5 cm",
                                          "MN": "4,5 cm"}, vert=("AN", "MN"), petit=True)


# 2089 : trois figures, reconnaître une configuration
def trois_configs(corrige):
    s = []
    # (a) emboîtée R U S / V T
    R, S_, T = (.9, 2.9), (0, 0), (2.3, 0)
    U_, Vv = lerp(R, S_, .45), lerp(R, T, .45)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(R), P(S_), P(T)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle %s -- %s;" % (P(R), P(S_), P(T), P(U_), P(Vv))]
    s += pt(R, "R", 90) + pt(S_, "S", 200) + pt(T, "T", 340) + pt(U_, "U", 180) + pt(Vv, "V", 0)
    s += [r"\node[txt,text=otNavy,anchor=north] at (1.15,-.45) {(a)};",
          r"\node[lab,anchor=north] at (1.15,-.9) {$(UV) \parallel (ST)$};"]
    # (b) papillon E O G / F O H
    ox = 4.3
    O = (ox, 1.45)
    G, H = (ox - 1.0, 0), (ox + 1.1, 0)
    E, F = (ox + .4 * 1.0, 1.45 + .4 * 1.45), (ox - .4 * 1.1, 1.45 + .4 * 1.45)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(G), P(H)),
          r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(E), P(F)),
          r"\draw[geoTrait] %s -- %s %s -- %s %s -- %s %s -- %s;" % (P(E), P(G), P(F), P(H), P(G), P(H), P(E), P(F))]
    s += pt(O, "O", 180, d=.18) + pt(G, "G", 200) + pt(H, "H", 340) + pt(E, "E", 20) + pt(F, "F", 160)
    s += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.45) {(b)};" % f(ox),
          r"\node[lab,anchor=north] at (%s,-.9) {$(EF) \parallel (GH)$};" % f(ox)]
    # (c) aucune information de parallélisme
    cx = 6.35
    I, J, K = (cx + .9, 2.9), (cx, 0), (cx + 2.3, 0)
    Pp, Q = lerp(I, J, .45), lerp(I, K, .47)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(I), P(J), P(K)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle %s -- %s;" % (P(I), P(J), P(K), P(Pp), P(Q))]
    s += pt(I, "I", 90) + pt(J, "J", 200) + pt(K, "K", 340) + pt(Pp, "P", 180) + pt(Q, "Q", 0)
    s += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.45) {(c)};" % f(cx + 1.15),
          r"\node[txt,text=otMuted,anchor=north,align=center] at (%s,-.95) {parallélisme\\non donné};" % f(cx + 1.15)]
    return figure(s)


FIGURES["ex2089_enonce"] = trois_configs(False)
FIGURES["ex2089_corrige"] = papillon(.4, {"AM": "2 cm", "AB": "5 cm", "AN": "3 cm", "AC": "7,5 cm"},
                                     vert=("AC",), noms="OEGFH", petit=True, B=(-2.7, -3.4), C=(3.7, -3.4))

# 2090
FIGURES["ex2090_enonce"] = emboitee(.6, {"AM": "3 cm", "MB": "2 cm", "AC": "12 cm"})
FIGURES["ex2090_corrige"] = emboitee(.6, {"AM": "3 cm", "MB": "2 cm", "AB": "5 cm", "AN": "7,2 cm", "NC": "4,8 cm",
                                          "AC": "12 cm"}, vert=("AB", "AN", "NC"), petit=True)

# 2222
FIGURES["ex2222_enonce"] = emboitee(.4, {"AM": "6 cm", "AB": "?", "AN": "4 cm", "AC": "10 cm"})
FIGURES["ex2222_corrige"] = emboitee(.4, {"AM": "6 cm", "MB": "9 cm", "AB": "15 cm", "AN": "4 cm", "AC": "10 cm"},
                                     vert=("AB", "MB"), petit=True)


# 2223 : triangles semblables reconnus par les angles
def deux_triangles_angles(t1, t2, angles1, angles2, noms1, noms2, vert2=(), corr=None, L1=3.0, L2=4.1,
                          decal=4.1, cotes1=(), cotes2=()):
    """t1, t2 : (angle en B, angle en C) ; angles : textes {sommet: texte}."""
    A, B, C = tri_angles((0, 0), L1, *t1)
    D, E, F = tri_angles((decal, 0), L2, *t2)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corr else "otSky", P(D), P(E), P(F)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(D), P(E), P(F))]
    o = "otOrange!90!black"
    s += marque_angles(A, B, C, [(k, v, 1, "otGreenDark" if k in (corr or {}) else o) for k, v in angles1.items()])
    s += marque_angles(D, E, F, [(k, v, 1, "otGreenDark" if k in vert2 else o) for k, v in angles2.items()])
    for (p, q, t, cc, vv) in cotes1:
        s += lseg({"A": A, "B": B, "C": C}[p], {"A": A, "B": B, "C": C}[q], coul_txt(t, vv), cote=cc, d=.12)
    for (p, q, t, cc, vv) in cotes2:
        s += lseg({"A": D, "B": E, "C": F}[p], {"A": D, "B": E, "C": F}[q], coul_txt(t, vv), cote=cc, d=.12)
    s += pt(A, noms1[0], 90) + pt(B, noms1[1], 225) + pt(C, noms1[2], 315)
    s += pt(D, noms2[0], 90) + pt(E, noms2[1], 225) + pt(F, noms2[2], 315)
    return figure(s)


# ABC : B = 60°, C = 70° (A = 50°) ; DEF : base [EF], E = 50°, F = 60° (D = 70°)
FIGURES["ex2223_enonce"] = deux_triangles_angles((60, 70), (50, 60), {"A": r"50^\circ", "B": r"60^\circ"},
                                                 {"A": r"70^\circ", "B": r"50^\circ"}, "ABC", "DEF")
FIGURES["ex2223_corrige"] = deux_triangles_angles((60, 70), (50, 60),
                                                  {"A": r"50^\circ", "B": r"60^\circ", "C": r"70^\circ"},
                                                  {"A": r"70^\circ", "B": r"50^\circ", "C": r"60^\circ"}, "ABC", "DEF",
                                                  vert2=("C",), corr={"C": 1})


# 2224 : contre-exemple « même ordre »
def contre_exemple():
    A, B, C = (2.2, 3.0), (0, 0), (5.2, 0)
    M = lerp(A, B, .5)
    N = lerp(A, C, -.5)  # N du côté opposé : A entre N et C
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
          r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
          r"\draw[geoTrait] (A) -- (N);",
          r"\draw[otOrange!90!black,line width=1.1pt] (M) -- (N);"]
    s += [r"\cote[.42]{M}{A}{$2$}", r"\cote[1.0]{B}{A}{$4$}", r"\cote[.42]{N}{A}{$3$}", r"\cote[.42]{A}{C}{$6$}"]
    s += pt(A, "A", 0, d=.18) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 180) + pt(N, "N", 120)
    s += [r"\node[txt,text=otOrange!80!black,anchor=north west] at (5.4,4.3) {$(MN)$ coupe $(BC)$};"]
    return figure(s)


FIGURES["ex2224_corrige"] = contre_exemple()

# 2091 : réciproque
FIGURES["ex2091_enonce"] = emboitee(.4, {"AM": "4 cm", "AB": "10 cm", "AN": "6 cm", "AC": "15 cm", "BC": "10 cm"})
FIGURES["ex2091_corrige"] = emboitee(.4, {"AM": "4 cm", "AB": "10 cm", "AN": "6 cm", "AC": "15 cm", "BC": "10 cm",
                                          "MN": "4 cm"}, vert=("MN",), petit=True)


# 2092 : non parallèles (N placé selon les vraies longueurs : 5/12)
def non_paralleles(corrige):
    A, B, C = (1.9, 4.4), (0, 0), (6.2, 0)
    M, N = lerp(A, B, 3 / 8), lerp(A, C, 5 / 12)
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;", r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
          r"\draw[%s] (M) -- (N);" % ("otOrange!90!black,line width=1.1pt" if corrige else "geoTrait")]
    s += [r"\cote[.42]{M}{A}{$3$ cm}", r"\cote[1.05]{B}{A}{$8$ cm}", r"\cote[.42]{A}{N}{$5$ cm}",
          r"\cote[1.05]{A}{C}{$12$ cm}"]
    if corrige:
        N2 = lerp(A, C, 3 / 8)
        s += [r"\draw[geoReponse,dash pattern=on 3.5pt off 2pt] (M) -- %s;" % P(N2)]
        s += pt(N2, "N'", 262, "otGreenDark", d=.2)
        s += [r"\node[txt,text=otGreenDark,anchor=north] at (3.1,-.75) {$(MN') \parallel (BC)$ si $AN' = 4{,}5$ cm};"]
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 180) + pt(N, "N", 0)
    return figure(s)


FIGURES["ex2092_enonce"] = non_paralleles(False)
FIGURES["ex2092_corrige"] = non_paralleles(True)

# 2093 : papillon
FIGURES["ex2093_enonce"] = papillon(.6, {"AM": "3 cm", "AB": "5 cm", "AC": "8 cm", "BC": "6 cm"})
FIGURES["ex2093_corrige"] = papillon(.6, {"AM": "3 cm", "AB": "5 cm", "AN": "4,8 cm", "AC": "8 cm", "BC": "6 cm",
                                          "MN": "3,6 cm"}, vert=("AN", "MN"), petit=True)

# 2225 : ABC (A 40, B 65, C 75) ; DEF (D 65, E 75, F 40)
FIGURES["ex2225_enonce"] = deux_triangles_angles(
    (65, 75), (40, 65), {"A": r"40^\circ", "B": r"65^\circ", "C": r"75^\circ"},
    {"A": r"75^\circ", "B": r"40^\circ", "C": r"65^\circ"}, "ABC", "EFD", L1=2.9, L2=4.35, decal=3.75,
    cotes1=[("A", "B", "6 cm", -1, False), ("B", "C", "8 cm", -1, False)],
    cotes2=[("B", "C", "9 cm", -1, False), ("A", "B", "10,5 cm", -1, False)])
FIGURES["ex2225_corrige"] = deux_triangles_angles(
    (65, 75), (40, 65), {"A": r"40^\circ", "B": r"65^\circ", "C": r"75^\circ"},
    {"A": r"75^\circ", "B": r"40^\circ", "C": r"65^\circ"}, "ABC", "EFD", L1=2.9, L2=4.35, decal=3.75,
    cotes1=[("A", "B", "6 cm", -1, False), ("B", "C", "8 cm", -1, False), ("C", "A", "7 cm", -1, True)],
    cotes2=[("B", "C", "9 cm", -1, False), ("A", "B", "10,5 cm", -1, False), ("C", "A", "12 cm", -1, True)])


# 2226 : deux triangles semblables, côtés 4 cm et 10 cm
def deux_semblables(k_txt, vert):
    A, B, C = tri_angles((0, 0), 2.0, 70, 45)
    D, E, F = tri_angles((3.0, 0), 5.0, 70, 45)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if vert else "otSky", P(D), P(E), P(F)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(D), P(E), P(F))]
    s += lseg(B, C, "4 cm", -1, d=.12) + lseg(E, F, "10 cm", -1, d=.12)
    s += [r"\node[lab,anchor=north] at %s {$\mathcal{P} = 15$ cm}; " % P((1.0, -.62)),
          r"\node[lab,anchor=north] at %s {$\mathcal{A} = 12$ cm²};" % P((1.0, -1.12))]
    if vert:
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P((5.5, -.62)), V % r"$\mathcal{P} = 37{,}5$ cm"),
              r"\node[lab,anchor=north] at %s {%s};" % (P((5.5, -1.12)), V % r"$\mathcal{A} = 75$ cm²"),
              r"\node[txt,text=otGreenDark,anchor=south] at %s {$k = 2{,}5$};" % P((2.55, 1.0))]
    return figure(s)


FIGURES["ex2226_enonce"] = deux_semblables("", False)
FIGURES["ex2226_corrige"] = deux_semblables("", True)


# 2227 : triangles par leurs côtés (4, 6, 8), (6, 9, 12), (5 ; 7,5 ; 9)
def tri_cotes(a, b, c, x0, U):
    """Triangle de base c (horizontale), côtés a (gauche) et b (droite)."""
    xa = (a * a - b * b + c * c) / (2 * c)
    ya = math.sqrt(a * a - xa * xa)
    return (x0 + xa * U, ya * U), (x0, 0), (x0 + c * U, 0)


def trois_triangles(corrige):
    U = .28
    s = []
    data = [("T_1", (4, 6, 8), ("4", "6", "8"), 0),
            ("T_2", (6, 9, 12), ("6", "9", "12"), 2.75),
            ("T_3", (5, 7.5, 9), ("5", "7,5", "9"), 6.55)]
    for nom, (a, b, c), (ta, tb, tc), x0 in data:
        A, B, C = tri_cotes(a, b, c, x0, U)
        vert = corrige and nom in ("T_1", "T_2")
        s += [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!16" if vert else "otSky", P(A), P(B), P(C)),
              r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
        s += lseg(B, A, ta, 1, d=.1) + lseg(A, C, tb, 1, d=.1) + lseg(B, C, tc, -1, d=.1)
        s += [r"\node[txt,text=otNavy,anchor=north] at %s {$%s$};" % (P(((B[0] + C[0]) / 2, -.5)), nom)]
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=north] at (2.9,-1.0) {$T_2$ : côtés de $T_1$ multipliés par $1{,}5$};"]
    return figure(s)


FIGURES["ex2227_enonce"] = trois_triangles(False)
FIGURES["ex2227_corrige"] = trois_triangles(True)

# 2228 : réciproque en papillon (2,4 / 4 et 3 / 5)
FIGURES["ex2228_enonce"] = papillon(.6, {"AM": "2,4 cm", "AB": "4 cm", "AN": "3 cm", "AC": "5 cm", "BC": "6,5 cm"},
                                    B=(-2.4, -2.9), C=(2.8, -2.9))
FIGURES["ex2228_corrige"] = papillon(.6, {"AM": "2,4 cm", "AB": "4 cm", "AN": "3 cm", "AC": "5 cm", "BC": "6,5 cm",
                                          "MN": "3,9 cm"}, vert=("MN",), petit=True, B=(-2.4, -2.9), C=(2.8, -2.9))

# 2094 : ombre de l'arbre
FIGURES["ex2094_enonce"] = ombres(1.5, 2, 9, 12, {"bo": "2 m", "ao": "12 m", "bh": "1,5 m", "ah": "$h$"}, echelle=.42)
FIGURES["ex2094_corrige"] = ombres(1.5, 2, 9, 12, {"bo": "2 m", "ao": "12 m", "bh": "1,5 m", "ah": "$h = 9$ m"},
                                   vert=True, echelle=.42)

# 2095 : équation
FIGURES["ex2095_enonce"] = emboitee(2 / 3, {"AM": "4 cm", "MB": "$x$", "AN": "6 cm", "NC": "3 cm", "BC": "7,5 cm"})
FIGURES["ex2095_corrige"] = emboitee(2 / 3, {"AM": "4 cm", "MB": "$x = 2$ cm", "AN": "6 cm", "NC": "3 cm",
                                             "BC": "7,5 cm", "MN": "5 cm"}, vert=("MB", "MN"), petit=True)

# 2096 : corriger l'erreur
FIGURES["ex2096_enonce"] = emboitee(3 / 8, {"AM": "3 cm", "AB": "8 cm", "AC": "16 cm", "BC": "12 cm"})
FIGURES["ex2096_corrige"] = emboitee(3 / 8, {"AM": "3 cm", "AB": "8 cm", "AN": "6 cm", "NC": "10 cm", "AC": "16 cm",
                                             "BC": "12 cm", "MN": "4,5 cm"}, vert=("AN", "NC", "MN"), petit=True)


# 2229 : largeur d'une rivière
def riviere(corrige):
    A = (3.2, 6.4)
    M, N = (.8, 2.4), (5.6, 2.4)
    k = 30 / 24
    B = (A[0] + k * (M[0] - A[0]), A[1] + k * (M[1] - A[1]))
    C = (A[0] + k * (N[0] - A[0]), A[1] + k * (N[1] - A[1]))
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky!70!otNavy!14] (-.9,2.4) rectangle (7.3,5.9);",
          r"\draw[otNavy!45,line width=.6pt] (-.9,2.4) -- (7.3,2.4) (-.9,5.9) -- (7.3,5.9);",
          r"\node[txt,text=otNavy!75,anchor=west] at (-.8,4.15) {rivière};"]
    s += [r"\draw[geoTrait] (A) -- (B) (A) -- (C) (B) -- (C);",
          r"\draw[%s] (M) -- (N);" % ("geoTrait")]
    if corrige:
        s += lseg(A, M, V % "24 m", -1, t=.5, d=.14)
    s += lseg(M, B, "6 m", -1, t=.5, d=.14)
    s += lseg(M, N, "12 m", 1, t=.5, d=.12)
    s += lseg(B, C, "15 m", -1, d=.12)
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 112, d=.16) + pt(N, "N", 68, d=.16)
    s += [r"\node[txt,text=otMuted,anchor=west] at (3.5,6.45) {arbre};"]
    return figure(s)


FIGURES["ex2229_enonce"] = riviere(False)
FIGURES["ex2229_corrige"] = riviere(True)


# 2230 : hauteur du phare
def phare(corrige):
    u = .17
    A = (0, 0)
    e = 2.8
    Bp, Bs = (3 * u * e, 0), (3 * u * e, 2 * u * e)
    Pp, Ps = (39 * u, 0), (39 * u, 26 * u)
    s = [r"\draw[otMuted,line width=.7pt] (-.5,0) -- %s;" % P((Pp[0] + .7, 0))]
    s += [r"\fill[%s] %s -- %s -- %s -- cycle;" % ("otGreen!14" if corrige else "otSky", P(A), P(Pp), P(Ps))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse" if corrige else "rayon", P(A), P(Ps))]
    s += [r"\draw[otNavy,line width=2pt] %s -- %s;" % (P(Bp), P(Bs)),
          r"\draw[%s,line width=2.6pt] %s -- %s;" % ("otGreenDark" if corrige else "otNavy", P(Pp), P(Ps))]
    s += [r"\draw[otNavy,line width=.6pt] %s -- ++(-.2,0) -- ++(0,.2) -- ++(.2,0);" % P(Pp)]
    s += [r"\coordinate (oeil) at (0,0); \coordinate (pb) at %s; \coordinate (pp) at %s;" % (P(Bp), P(Pp)),
          r"\cote[.45]{pb}{oeil}{$3$ m}", r"\cote[1.05]{pp}{oeil}{$39$ m}"]
    s += lab((Bp[0], Bs[1] * .45), "2 m", 0, d=.14, maths=False)
    s += lab((Pp[0], Ps[1] / 2), V % "$h = 26$ m" if corrige else "$h$", 0, d=.18, maths=False)
    if corrige:
        s += lseg(A, Ps, V % r"$AS = \sqrt{2\,197} \approx 46{,}9$ m", 1, t=.45, d=.14)
    s += pt(A, "A", 135, d=.15)
    if corrige:
        s += pt(Ps, "S", 90, "otGreenDark", d=.15)
    s += [r"\node[txt,text=otMuted,anchor=west] at %s {phare};" % P((Pp[0] + .2, Ps[1] - .25))]
    if not corrige:
        s += [r"\node[txt,text=otOrange!80!black,anchor=south east] at %s {ligne de visée};" % P((3.0, 2.35))]
    return figure(s)


FIGURES["ex2230_enonce"] = phare(False)
FIGURES["ex2230_corrige"] = phare(True)


# 2231 : photo et agrandissement
def photos(corrige):
    u = .15
    s = [r"\fill[otSky] (0,0) rectangle %s;" % P((10 * u, 15 * u)),
         r"\draw[geoTrait] (0,0) rectangle %s;" % P((10 * u, 15 * u))]
    x0 = 10 * u + 1.3
    s += [r"\fill[%s] %s rectangle %s;" % ("otGreen!14" if corrige else "otSky", P((x0, 0)), P((x0 + 30 * u, 45 * u))),
          r"\draw[geoTrait] %s rectangle %s;" % (P((x0, 0)), P((x0 + 30 * u, 45 * u)))]
    s += lab((5 * u, 0), "10 cm", 270, d=.14, maths=False) + lab((10 * u, 7.5 * u), "15 cm", 0, d=.12, maths=False)
    s += lab((x0 + 15 * u, 0), V % "30 cm" if corrige else "?", 270, d=.14, maths=False)
    s += lab((x0 + 30 * u, 22.5 * u), "45 cm", 0, d=.12, maths=False)
    s += [r"\node[txt,text=otMuted,anchor=south] at %s {photo};" % P((5 * u, 15 * u + .12)),
          r"\node[txt,text=otMuted,anchor=south] at %s {agrandissement};" % P((x0 + 15 * u, 45 * u + .12))]
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=south] at %s {$\times\,3$};" % P((10 * u + .65, 15 * u + .5))]
    return figure(s)


FIGURES["ex2231_enonce"] = photos(False)
FIGURES["ex2231_corrige"] = photos(True)


# 2232 : type brevet (A en haut, [AB] vertical, M sur [AB], N sur [AC])
def brevet(corrige):
    u = .6
    A, B, C = (0, 6 * u), (0, 0), (8 * u, 0)
    M, N = (0, 1.5 * u), (6 * u, 1.5 * u)
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if corrige:
        s += [r"\fill[otGreen!18] (A) -- (M) -- (N) -- cycle;"]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;"]
    s += [r"\draw[%s] (M) -- (N);" % ("geoReponse,line width=1.2pt" if corrige else "geoTrait")]
    if corrige:
        s += [r"\angledroit{A}{M}{N}", r"\angledroit{A}{B}{C}"]
    s += [r"\cote[.42]{M}{A}{$4{,}5$ cm}", r"\cote[1.35]{B}{A}{$6$ cm}"]
    s += [r"\cote[.42]{A}{C}{$10$ cm}"]
    s += lseg(A, N, "7,5 cm", -1, t=.45, d=.1)
    s += lseg(M, N, "6 cm", -1, t=.6, d=.1)
    if corrige:
        s += lseg(B, C, V % "8 cm", -1, d=.12)
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", 315) + pt(M, "M", 235, d=.18) + pt(N, "N", 20, d=.16)
    return figure(s)


FIGURES["ex2232_enonce"] = brevet(False)
FIGURES["ex2232_corrige"] = brevet(True)
