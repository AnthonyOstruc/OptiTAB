# -*- coding: utf-8 -*-
"""Figures de la notion « Translations, agrandissements et réductions » (4e), style des livres.

Compilées par outils/figures_livre.py. Constructions sur quadrillage pâle :
bleu marine = figure de départ et éléments donnés, vert foncé = image et traits
de construction (corrigés), orange = figure transformée à reconnaître (3671),
motif repère (frise, pavage) ou rayon lumineux.
Les étiquettes des points sont placées automatiquement dans la direction la
plus éloignée des traits qui partent du point (on peut imposer l'angle).

DONNEES rassemble les coordonnées utilisées : verif_288.py les relit.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  grille/.style={otRule,line width=.4pt,step=1},
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  num/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,inner sep=0pt},
  depart/.style={otNavy,line width=1pt,line join=round,fill=otSky},
  image/.style={otGreenDark,line width=1pt,line join=round,fill=otGreen!16},
  repere/.style={otOrange!90!black,line width=1pt,line join=round,fill=otOrange!22},
  constr/.style={otGreenDark,line width=.7pt,dash pattern=on 3pt off 2pt},
  axe/.style={otNavy,line width=1.1pt},
  vect/.style={otNavy,line width=1.1pt,-{Stealth[length=2.6mm]}},
  vectv/.style={otGreenDark,line width=1.1pt,-{Stealth[length=2.6mm]}},
  fl/.style={otGreenDark,line width=.7pt,dash pattern=on 3pt off 2pt,-{Stealth[length=2.2mm]}},
  arc/.style={otGreenDark,line width=.7pt},
}
"""

V = "otGreenDark"
N = "otNavy"
O_ = "otOrange!80!black"


def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def ecart(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def tr(pts, v):
    return [(x + v[0], y + v[1]) for x, y in pts]


def homo(pts, k, o=(0, 0), dest=(0, 0)):
    """Agrandissement / réduction de coefficient k : o est envoyé sur dest."""
    return [(dest[0] + k * (x - o[0]), dest[1] + k * (y - o[1])) for x, y in pts]


class Fig:
    """Figure sur quadrillage : segments mémorisés pour placer les étiquettes."""

    def __init__(self, U=.6):
        self.U = U
        self.fond, self.corps, self.haut = [], [], []
        self.segs = []
        self.etiq = []
        self.pts = []

    def grille(self, x0, y0, x1, y1):
        self.fond.append(r"\draw[grille] %s grid %s;" % (P((x0, y0)), P((x1, y1))))

    def seg(self, p, q, style="constr", memo=True):
        self.corps.append(r"\draw[%s] %s -- %s;" % (style, P(p), P(q)))
        if memo:
            self.segs.append((p, q))

    def poly(self, pts, style="depart"):
        self.corps.append(r"\draw[%s] %s -- cycle;" % (style, " -- ".join(P(p) for p in pts)))
        for i in range(len(pts)):
            self.segs.append((pts[i], pts[(i + 1) % len(pts)]))

    def fleche(self, p, q, style="vect"):
        self.corps.append(r"\draw[%s] %s -- %s;" % (style, P(p), P(q)))
        self.segs.append((p, q))

    def brut(self, code, haut=False):
        (self.haut if haut else self.corps).append(code)

    def point(self, p, nom=None, coul=N, ang=None, d=.15, evite=()):
        self.pts.append(p)
        self.haut.append(r"\fill[%s] %s circle (2.2pt);" % (coul, P(p)))
        if nom:
            self.etiq.append((p, nom, coul, ang, d, evite))

    def texte(self, p, txt, anchor="center", coul="otInk", style="lab"):
        self.haut.append(r"\node[%s,text=%s,anchor=%s] at %s {%s};" % (style, coul, anchor, P(p), txt))

    def directions(self, p):
        dirs = []
        for a, b in self.segs:
            for u, v in ((a, b), (b, a)):
                if math.hypot(u[0] - p[0], u[1] - p[1]) < 1e-9 and math.hypot(v[0] - p[0], v[1] - p[1]) > 1e-9:
                    dirs.append(math.degrees(math.atan2(v[1] - p[1], v[0] - p[0])))
            ab = (b[0] - a[0], b[1] - a[1])
            ap = (p[0] - a[0], p[1] - a[1])
            L2 = ab[0] ** 2 + ab[1] ** 2
            if L2 > 0:
                t = (ap[0] * ab[0] + ap[1] * ab[1]) / L2
                cr = ab[0] * ap[1] - ab[1] * ap[0]
                if 1e-6 < t < 1 - 1e-6 and abs(cr) / math.sqrt(L2) < 1e-6:
                    a1 = math.degrees(math.atan2(ab[1], ab[0]))
                    dirs += [a1, a1 + 180]
        for q in self.pts:
            dd = math.hypot(q[0] - p[0], q[1] - p[1])
            if 1e-9 < dd < 1.6:
                dirs.append(math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])))
        return dirs

    def rendu_etiq(self):
        out = []
        for p, nom, coul, ang, d, evite in self.etiq:
            if ang is None:
                dirs = self.directions(p) + list(evite)
                best, val = 45, -1
                for c in range(0, 360, 5):
                    m = min([ecart(c, x) for x in dirs] or [180])
                    m2 = m + (2 if c % 90 == 45 else 0)
                    if m2 > val:
                        best, val = c, m2
                ang = best
            a = math.radians(ang)
            dd = d / self.U * .6 + .12
            q = (p[0] + dd * math.cos(a), p[1] + dd * math.sin(a))
            out.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};" % (coul, (ang + 180) % 360, P(q), nom))
        return out

    def code(self):
        return "\n".join([r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round]" % (f(self.U), f(self.U))]
                         + self.fond + self.corps + self.haut + self.rendu_etiq() + [r"\end{tikzpicture}"])


def angle_droit(F, s, p, q, taille=.32, coul=V):
    def u(a):
        L = math.hypot(a[0] - s[0], a[1] - s[1])
        return ((a[0] - s[0]) / L * taille, (a[1] - s[1]) / L * taille)
    a, b = u(p), u(q)
    F.brut(r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (
        coul, P((s[0] + a[0], s[1] + a[1])), P((s[0] + a[0] + b[0], s[1] + a[1] + b[1])), P((s[0] + b[0], s[1] + b[1]))))


def codage(F, p, q, n=1, coul=V, h=.2):
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    for k in range(n):
        o = (k - (n - 1) / 2) * .13
        c = (m[0] + o * ux, m[1] + o * uy)
        F.brut(r"\draw[%s,line width=.75pt] %s -- %s;" % (
            coul, P((c[0] - h * uy, c[1] + h * ux)), P((c[0] + h * uy, c[1] - h * ux))))


def etiq_cote(F, p, q, txt, d=.45, coul="otInk", cote_gauche=True, t=.5):
    """Texte posé le long de [pq] (à la fraction t), décalé de d du côté gauche (sens p→q) ou droit."""
    m = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    nx, ny = -(q[1] - p[1]) / L, (q[0] - p[0]) / L
    if not cote_gauche:
        nx, ny = -nx, -ny
    a = math.degrees(math.atan2(ny, nx))
    F.brut(r"\node[txt,text=%s,anchor=%d] at %s {%s};" % (coul, (a + 180) % 360, P((m[0] + d * nx, m[1] + d * ny)), txt), haut=True)


def primes(noms):
    return [n + "'" for n in noms]


def triangle(F, pts, noms, style="depart", coul=N, angs=None):
    F.poly(pts, style)
    for i, (p, n) in enumerate(zip(pts, noms)):
        F.point(p, n, coul, ang=None if angs is None else angs[i])


FIGURES = {}
TOLERE = {}
DONNEES = {}

# =================================================================== cours
TRI_C = [(1, 1), (4, 1), (2, 4)]
VEC_C = (7, 2)
DONNEES["cours_translation"] = {"ABC": TRI_C, "vecteur": VEC_C, "A'B'C'": tr(TRI_C, VEC_C)}


def cours_translation():
    F = Fig(.62)
    F.grille(0, 0, 12, 7)
    img = tr(TRI_C, VEC_C)
    F.fleche(TRI_C[0], img[0], "vect")
    for p, q in zip(TRI_C[1:], img[1:]):
        F.fleche(p, q, "fl")
    triangle(F, img, primes("ABC"), "image", V)
    triangle(F, TRI_C, "ABC")
    return F.code()


FIGURES["cours_translation"] = cours_translation()

PARA = {"A": (0, 0), "A'": (5, 1.4), "M": (1.2, 3), "M'": (6.2, 4.4)}
DONNEES["cours_parallelogramme"] = PARA


def cours_parallelogramme():
    F = Fig(.8)
    A, A2, M, M2 = PARA["A"], PARA["A'"], PARA["M"], PARA["M'"]
    F.brut(r"\fill[otGreen!12] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(A2), P(M2), P(M)))
    F.seg(A, M, "constr")
    F.seg(A2, M2, "constr")
    F.fleche(A, A2, "vect")
    F.fleche(M, M2, "vectv")
    codage(F, A, A2, 2, N)
    codage(F, M, M2, 2, V)
    codage(F, A, M, 1, V)
    codage(F, A2, M2, 1, V)
    F.point(A, "A")
    F.point(A2, "A'")
    F.point(M, "M")
    F.point(M2, "M'", V)
    return F.code()


FIGURES["cours_parallelogramme"] = cours_parallelogramme()


def arc_autour(F, c, r, a_mil, ouv=13):
    F.brut(r"\draw[arc] %s ++(%s:%s) arc (%s:%s:%s);" % (P(c), f(a_mil - ouv), f(r), f(a_mil - ouv), f(a_mil + ouv), f(r)))


def cours_compas():
    F = Fig(.8)
    A, A2, M, M2 = PARA["A"], PARA["A'"], PARA["M"], PARA["M'"]
    rAA = math.hypot(A2[0] - A[0], A2[1] - A[1])
    rAM = math.hypot(M[0] - A[0], M[1] - A[1])
    arc_autour(F, M, rAA, math.degrees(math.atan2(M2[1] - M[1], M2[0] - M[0])), 6)
    arc_autour(F, A2, rAM, math.degrees(math.atan2(M2[1] - A2[1], M2[0] - A2[0])), 10)
    F.seg(A, M, "geoTrait")
    F.seg(M, M2, "constr")
    F.seg(A2, M2, "constr")
    F.fleche(A, A2, "vect")
    F.point(A, "A")
    F.point(A2, "A'")
    F.point(M, "M")
    F.point(M2, "M'", V, ang=30, d=.3)
    etiq_cote(F, M, M2, r"rayon $AA'$", .3, V, True)
    etiq_cote(F, A2, M2, r"rayon $AM$", .55, V, False, .4)
    return F.code()


FIGURES["cours_compas"] = cours_compas()

DRAP = [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)]
DONNEES["cours_trois"] = {
    "depart": DRAP,
    "axiale (x=4)": [(8 - x, y) for x, y in DRAP],
    "centrale (3,5 ; 2,5)": [(7 - x, 5 - y) for x, y in DRAP],
    "translation (+4 ; 0)": tr(DRAP, (4, 0)),
}


def cours_trois():
    U = .4
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]

    def pan(ox, oy, titre, img, extra):
        s.append(r"\begin{scope}[shift={(%s,%s)}]" % (f(ox), f(oy)))
        s.append(r"\draw[grille] (0,0) grid (8,5);")
        s.extend(extra)
        s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(p) for p in DRAP))
        s.append(r"\draw[image] %s -- cycle;" % " -- ".join(P(p) for p in img))
        s.append(r"\node[txt,text=otNavy,anchor=north] at (4,-.4) {%s};" % titre)
        s.append(r"\end{scope}")

    pan(0, 7.4, "symétrie axiale", [(8 - x, y) for x, y in DRAP], [r"\draw[axe] (4,-.3) -- (4,5.3);"])
    pan(10, 7.4, "symétrie centrale", [(7 - x, 5 - y) for x, y in DRAP],
        [r"\draw[constr] (1,4) -- (6,1);", r"\fill[otNavy] (3.5,2.5) circle (2.4pt);"])
    pan(5, 0, "translation", tr(DRAP, (4, 0)), [r"\draw[vect] (1,.45) -- (5,.45);"])
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_trois"] = cours_trois()

CHEVRON = [(.5, .5), (2.5, .5), (3.5, 1.5), (2.5, 2.5), (.5, 2.5), (1.5, 1.5)]


def cours_frise():
    F = Fig(.42)
    F.grille(0, 0, 16, 3)
    for i in range(4):
        F.poly(tr(CHEVRON, (4 * i, 0)), "repere" if i == 0 else "depart")
        F.texte((4 * i + 2, -.45), str(i + 1), "north", O_ if i == 0 else N, "num")
    F.seg((.5, .5), (.5, 3.4), "constr", memo=False)
    F.seg((4.5, .5), (4.5, 3.4), "constr", memo=False)
    F.fleche((.5, 3.6), (4.5, 3.6), "vectv")
    return F.code()


FIGURES["cours_frise"] = cours_frise()


def cours_pavage():
    """Chevrons emboîtés : translations de 2 carreaux vers la droite et de 2 carreaux vers le haut."""
    U = .5
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[grille] (0,0) grid (14,7);")
    base = [(x, y) for x, y in CHEVRON]
    for j in range(3):
        for i in range(5):
            pts = tr(base, (2 * i, 2 * j))
            st = "repere" if (i, j) == (0, 0) else "depart"
            s.append(r"\draw[%s] %s -- cycle;" % (st, " -- ".join(P(p) for p in pts)))
    # flèches des deux translations, au-dessus du pavage
    s.append(r"\draw[vectv] (2,1.5) -- (4,1.5);")
    s.append(r"\draw[vectv] (2,1.5) -- (2,3.5);")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_pavage"] = cours_pavage()

TRI_K = [(0, 0), (4, 0), (0, 2)]
DONNEES["cours_agrandissement"] = {"depart": TRI_K, "k=0,5": homo(TRI_K, .5), "k=2": homo(TRI_K, 2)}


def cours_agrandissement():
    """Deux rangées : départ et réduction en haut, agrandissement en bas (lisible sur téléphone)."""
    F = Fig(.55)
    F.grille(-1, -1, 11, 10)
    agr = homo(TRI_K, 2, dest=(0, 0))
    dep = homo(TRI_K, 1, dest=(0, 6))
    red = homo(TRI_K, .5, dest=(6, 6))
    F.poly(red, "image")
    F.poly(dep, "depart")
    F.poly(agr, "image")
    for t, c in ((red, V), (dep, N), (agr, V)):
        angle_droit(F, t[0], t[1], t[2], .3, c)
    etiq_cote(F, red[0], red[1], "2", .3, V, False)
    etiq_cote(F, red[0], red[2], "1", .3, V, True)
    etiq_cote(F, dep[0], dep[1], "4", .3, N, False)
    etiq_cote(F, dep[0], dep[2], "2", .3, N, True)
    etiq_cote(F, agr[0], agr[1], "8", .3, V, False)
    etiq_cote(F, agr[0], agr[2], "4", .3, V, True)
    F.texte((2.4, 7.6), r"départ", "south west", N, "txt")
    F.texte((6.3, 7.4), r"réduction, $k = 0{,}5$", "south west", V, "txt")
    F.texte((4.3, 2.6), r"agrandissement, $k = 2$", "south west", V, "txt")
    return F.code()


FIGURES["cours_agrandissement"] = cours_agrandissement()


def cours_aires():
    U = .5
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[depart] (0,0) rectangle (2,1);")
    s.append(r"\draw[image] (3.2,0) rectangle (7.2,2);")
    s.append(r"\draw[otGreenDark,line width=.5pt] (5.2,0) -- (5.2,2) (3.2,1) -- (7.2,1);")
    s.append(r"\draw[image] (8.4,0) rectangle (14.4,3);")
    s.append(r"\draw[otGreenDark,line width=.5pt] (10.4,0) -- (10.4,3) (12.4,0) -- (12.4,3) (8.4,1) -- (14.4,1) (8.4,2) -- (14.4,2);")
    s.append(r"\node[txt,text=otNavy,anchor=north,align=center] at (1,-.4) {départ};")
    s.append(r"\node[txt,text=otGreenDark,anchor=north,align=center] at (5.2,-.4) {coefficient 2\\aire × 4};")
    s.append(r"\node[txt,text=otGreenDark,anchor=north,align=center] at (11.4,-.4) {coefficient 3\\aire × 9};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_aires"] = cours_aires()

# =================================================================== 3671 reconnaître
S71 = [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)]
IMG71 = {
    "a": tr(S71, (5, 1)),
    "b": [(10 - x, y) for x, y in S71],
    "c": [(10 - x, 5 - y) for x, y in S71],
    "d": homo(S71, 2, o=(1, 1), dest=(5, 1)),
}
DONNEES["ex3671"] = {"S": S71, **IMG71}


def ex3671(corrige):
    U = .36
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    pos = {"a": (0, 10), "b": (11.5, 10), "c": (0, 0), "d": (11.5, 0)}
    for cle in "abcd":
        ox, oy = pos[cle]
        s.append(r"\begin{scope}[shift={(%s,%s)}]" % (f(ox), f(oy)))
        s.append(r"\draw[grille] (0,0) grid (10,8);")
        if corrige and cle == "b":
            s.append(r"\draw[otGreenDark,line width=1.1pt,dash pattern=on 4pt off 2.5pt] (5,-.3) -- (5,8.3);")
        if corrige and cle == "c":
            s.append(r"\draw[constr] (1,4) -- (9,1);")
        s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(p) for p in S71))
        s.append(r"\draw[repere] %s -- cycle;" % " -- ".join(P(p) for p in IMG71[cle]))
        if corrige and cle == "a":
            s.append(r"\draw[vectv] (1,1) -- (6,2);")
        if corrige and cle == "c":
            s.append(r"\fill[otGreenDark] (5,2.5) circle (2.6pt);")
        if corrige and cle == "d":
            s.append(r"\node[lab,text=otGreenDark] at (2.5,6.5) {$\times 2$};")
        s.append(r"\node[txt,text=otNavy,anchor=north] at (5,-.45) {figure %s};" % cle)
        s.append(r"\end{scope}")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3671_enonce"] = ex3671(False)
FIGURES["ex3671_corrige"] = ex3671(True)

# =================================================================== 3672 repère
P72 = {"A": (1, 1), "A'": (4, 3), "B": (2, 4), "C": (-2, 3), "D": (-1, -2)}
V72 = (3, 2)
I72 = {"B'": tr([P72["B"]], V72)[0], "C'": tr([P72["C"]], V72)[0], "D'": tr([P72["D"]], V72)[0],
       "E": tr([P72["A"]], (-3, -2))[0]}
DONNEES["ex3672"] = {**P72, **I72}


def repere(xmin, xmax, ymin, ymax, U, corps):
    s = [r"\begin{tikzpicture}",
         r"\begin{axis}[otWeb, x=%scm, y=%scm, xmin=%s, xmax=%s, ymin=%s, ymax=%s," % (f(U), f(U), f(xmin), f(xmax), f(ymin), f(ymax)),
         r"  xtick={%s}, ytick={%s}," % (",".join(str(i) for i in range(int(math.ceil(xmin)), int(xmax) + 1) if i != 0),
                                         ",".join(str(i) for i in range(int(math.ceil(ymin)), int(ymax) + 1) if i != 0)),
         r"  extra x ticks={0}, extra x tick labels={}, yticklabel style={anchor=east,xshift=-2pt,yshift=0pt}, ]"]
    s += corps
    s += [r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(s)


def pt_axis(p, nom, coul=N, anchor="south west", dx=.12, dy=.12):
    lab = r"\node[lab,text=%s,anchor=%s,fill=white,inner sep=1pt] at (axis cs:%s,%s) {$%s$};" % (
        coul, anchor, f(p[0] + dx), f(p[1] + dy), nom)
    return [r"\fill[%s] (axis cs:%s,%s) circle (2.2pt);" % (coul, f(p[0]), f(p[1])), lab]


def fl_axis(p, q, style):
    return r"\draw[%s] (axis cs:%s,%s) -- (axis cs:%s,%s);" % (style, f(p[0]), f(p[1]), f(q[0]), f(q[1]))


def ex3672(corrige):
    c = [fl_axis(P72["A"], P72["A'"], "vect")]
    if corrige:
        for a, b in (("B", "B'"), ("C", "C'"), ("D", "D'")):
            c.append(fl_axis(P72[a], I72[b], "fl"))
        c.append(fl_axis(I72["E"], P72["A"], "fl"))
    c += pt_axis(P72["A"], "A", anchor="north west", dx=.15, dy=-.1)
    c += pt_axis(P72["A'"], "A'", anchor="north west", dx=.15, dy=-.1)
    c += pt_axis(P72["B"], "B", anchor="south east", dx=-.1, dy=.12)
    c += pt_axis(P72["C"], "C", anchor="south east", dx=-.1, dy=.12)
    c += pt_axis(P72["D"], "D", anchor="north east", dx=-.1, dy=-.1)
    if corrige:
        c += pt_axis(I72["B'"], "B'", V, anchor="south east", dx=-.1, dy=.12)
        c += pt_axis(I72["C'"], "C'", V, anchor="south east", dx=-.1, dy=.12)
        c += pt_axis(I72["D'"], "D'", V, anchor="south west", dx=.12, dy=.15)
        c += pt_axis(I72["E"], "E", V, anchor="north east", dx=-.1, dy=-.1)
    return repere(-3.5, 7.5, -3.5, 7.5, .55, c)


FIGURES["ex3672_enonce"] = ex3672(False)
FIGURES["ex3672_corrige"] = ex3672(True)

# =================================================================== 3673 triangle sur quadrillage
T73 = [(1, 1), (5, 1), (2, 4)]
V73 = (5, 2)
DONNEES["ex3673"] = {"ABC": T73, "vecteur": V73, "A'B'C'": tr(T73, V73)}


def ex3673(corrige):
    F = Fig(.62)
    F.grille(0, 0, 11, 7)
    img = tr(T73, V73)
    F.fleche(T73[0], img[0], "vect")
    if corrige:
        for p, q in zip(T73[1:], img[1:]):
            F.fleche(p, q, "fl")
        triangle(F, img, primes("ABC"), "image", V)
    else:
        F.point(img[0], "A'")
    triangle(F, T73, "ABC")
    return F.code()


FIGURES["ex3673_enonce"] = ex3673(False)
FIGURES["ex3673_corrige"] = ex3673(True)

# =================================================================== 3674 parallélogramme
P74 = {"A": (0, 0), "B": (4.8, 1.4), "M": (1.8, 2.4)}
P74["M'"] = (P74["M"][0] + 4.8, P74["M"][1] + 1.4)
P74["C"] = (9.6, 2.8)
DONNEES["ex3674"] = P74


def ex3674(corrige):
    F = Fig(.8)
    A, B, M, M2, C = P74["A"], P74["B"], P74["M"], P74["M'"], P74["C"]
    if corrige:
        F.brut(r"\fill[otGreen!12] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(M2), P(M)))
        F.fleche(B, C, "fl")
        F.fleche(M, M2, "vectv")
        F.seg(B, M2, "constr")
        codage(F, A, M, 1, V)
        codage(F, B, M2, 1, V)
    F.seg(A, M, "geoTrait")
    F.fleche(A, B, "vect")
    if corrige:
        codage(F, A, B, 2, V)
        codage(F, M, M2, 2, V)
    etiq_cote(F, A, B, "5 cm", .45, "otInk", False)
    etiq_cote(F, A, M, "3 cm", .45, "otInk", True)
    if corrige:
        etiq_cote(F, M, M2, "5 cm", .45, V, True)
        etiq_cote(F, B, M2, "3 cm", .45, V, False)
        F.point(M2, "M'", V)
        F.point(C, "C", V)
    F.point(A, "A")
    F.point(B, "B")
    F.point(M, "M")
    return F.code()


FIGURES["ex3674_enonce"] = ex3674(False)
FIGURES["ex3674_corrige"] = ex3674(True)

# =================================================================== 3675 rectangle
def ex3675(corrige):
    F = Fig(.55)
    F.grille(0, 0, 13, 6)
    F.poly([(1, 1), (4, 1), (4, 3), (1, 3)], "depart")
    F.texte((2.5, .75), "3 cm", "north", N, "txt")
    F.texte((.75, 2), "2 cm", "east", N, "txt")
    if corrige:
        F.poly([(6, 1), (12, 1), (12, 5), (6, 5)], "image")
        F.seg((9, 1), (9, 5), "otGreenDark,line width=.6pt")
        F.seg((6, 3), (12, 3), "otGreenDark,line width=.6pt")
        F.texte((9, .75), "6 cm", "north", V, "txt")
        F.texte((12.25, 3), "4 cm", "west", V, "txt")
    return F.code()


FIGURES["ex3675_enonce"] = ex3675(False)
FIGURES["ex3675_corrige"] = ex3675(True)

# =================================================================== 3676 triangle réduit
T76 = {"T": (0, 0), "S": (8, 0), "R": (0, 6)}
T76r = {k + "'": (10 + .5 * x, .5 * y) for k, (x, y) in T76.items()}
DONNEES["ex3676"] = {**T76, **T76r}


def ex3676(corrige):
    F = Fig(.45)
    T, S, R = T76["T"], T76["S"], T76["R"]
    triangle(F, [T, S, R], "TSR", angs=[225, 315, 135])
    angle_droit(F, T, S, R, .7, N)
    etiq_cote(F, T, S, "8 cm", .55, "otInk", False)
    etiq_cote(F, R, T, "6 cm", .55, "otInk", False)
    etiq_cote(F, S, R, "10 cm", .75, "otInk", False)
    if corrige:
        T2, S2, R2 = T76r["T'"], T76r["S'"], T76r["R'"]
        triangle(F, [T2, S2, R2], ["T'", "S'", "R'"], "image", V, angs=[225, 315, 135])
        angle_droit(F, T2, S2, R2, .5, V)
        etiq_cote(F, T2, S2, "4 cm", .55, V, False)
        etiq_cote(F, R2, T2, "3 cm", .55, V, False)
        etiq_cote(F, S2, R2, "5 cm", .75, V, False)
    return F.code()


FIGURES["ex3676_enonce"] = ex3676(False)
FIGURES["ex3676_corrige"] = ex3676(True)

# =================================================================== 3678 frise
MOTIF78 = [(0, 0), (1.8, 0), (2.4, 1), (1.8, 2), (0, 2), (.6, 1)]


def ex3678(corrige):
    U = .345
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[otMuted,line width=.6pt] (0,2.8) -- (24,2.8);")
    for x in range(25):
        h = .45 if x % 3 == 0 else .22
        s.append(r"\draw[otMuted,line width=.5pt] (%d,2.8) -- (%d,%s);" % (x, x, f(2.8 + h)))
        if x % 3 == 0:
            s.append(r"\node[font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,anchor=south,inner sep=1pt] at (%d,3.35) {%d};" % (x, x))
    s.append(r"\node[font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,anchor=west,inner sep=1pt] at (24.4,2.8) {cm};")
    for i in range(8):
        st = "repere" if i == 0 else "depart"
        s.append(r"\draw[%s] %s -- cycle;" % (st, " -- ".join(P(p) for p in tr(MOTIF78, (3 * i, 0)))))
        s.append(r"\node[num,text=%s,anchor=north] at (%s,-.4) {%d};" % (O_ if i == 0 else N, f(3 * i + 1.2), i + 1))
    if corrige:
        s.append(r"\draw[vectv] (0,-1.75) -- (3,-1.75);")
        s.append(r"\node[txt,text=otGreenDark,anchor=west] at (3.3,-1.75) {3 cm};")
        s.append(r"\draw[vectv] (0,-2.75) -- (9,-2.75);")
        s.append(r"\node[txt,text=otGreenDark,anchor=west] at (9.3,-2.75) {9 cm : du motif 1 au motif 4};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3678_enonce"] = ex3678(False)
FIGURES["ex3678_corrige"] = ex3678(True)

# =================================================================== 3679 translation ou symétrie
F79 = {"A": (1, 6), "B": (1, 10), "C": (4, 9), "D": (1, 8)}
AXE79 = 6
O79 = (3, 6)
E79 = (9, 1)
V79 = (E79[0] - F79["A"][0], E79[1] - F79["A"][1])
F79_1 = {k: (2 * AXE79 - x, y) for k, (x, y) in F79.items()}
F79_2 = {k: (2 * O79[0] - x, 2 * O79[1] - y) for k, (x, y) in F79.items()}
F79_3 = {k: (x + V79[0], y + V79[1]) for k, (x, y) in F79.items()}
DONNEES["ex3679"] = {"F": F79, "axe x": AXE79, "O": O79, "E": E79, "F1": F79_1, "F2": F79_2, "F3": F79_3}


def drapeau(F, d, style, coul):
    F.seg(d["A"], d["B"], "%s,line width=1.6pt" % coul)
    F.poly([d["B"], d["C"], d["D"]], style)


def ex3679(corrige):
    F = Fig(.58)
    F.grille(0, 0, 13, 11)
    F.seg((AXE79, -.3), (AXE79, 11.3), "axe")
    F.texte((AXE79 + .2, 11.1), r"$(d)$", "north west", N)
    if corrige:
        C, C1, C2 = F79["C"], F79_1["C"], F79_2["C"]
        F.seg(C, C1, "constr", memo=False)
        angle_droit(F, (AXE79, C[1]), C1, (AXE79, C[1] + 2), .3)
        codage(F, C, (AXE79, C[1]), 2)
        codage(F, (AXE79, C[1]), C1, 2)
        F.seg(C, C2, "constr", memo=False)
        codage(F, C, O79, 1)
        codage(F, O79, C2, 1)
        F.fleche(F79["A"], E79, "fl")
        for d, nom, p, anc in ((F79_1, "F_1", (12, 9.4), "west"), (F79_2, "F_2", (5.35, 2.4), "west"),
                               (F79_3, "F_3", (12.3, 2.4), "west")):
            drapeau(F, d, "image", V)
            F.texte(p, r"$%s$" % nom, anc, V)
    drapeau(F, F79, "depart", N)
    F.texte((2, 9), r"$F$", "center", N)
    for k, ang in (("A", 225), ("B", 135), ("C", 30), ("D", 180)):
        F.point(F79[k], k, ang=ang)
    F.point(O79, "O", ang=270)
    F.point(E79, "E", ang=225 if not corrige else 200)
    return F.code()


FIGURES["ex3679_enonce"] = ex3679(False)
FIGURES["ex3679_corrige"] = ex3679(True)

# =================================================================== 3680 règle et compas
P80 = {"E": (0, 0), "F": (4, 0), "G": (0, 3), "E'": (5.5, -2)}
V80 = (5.5, -2)
P80["F'"] = (P80["F"][0] + V80[0], P80["F"][1] + V80[1])
P80["G'"] = (P80["G"][0] + V80[0], P80["G"][1] + V80[1])
DONNEES["ex3680"] = P80


def ex3680(corrige):
    F = Fig(.75)
    E, Fp, G, E2, F2, G2 = (P80[k] for k in ("E", "F", "G", "E'", "F'", "G'"))
    rEE = math.hypot(*V80)
    if corrige:
        F.brut(r"\fill[otGreen!10] %s -- %s -- %s -- %s -- cycle;" % (P(E), P(E2), P(G2), P(G)))
        arc_autour(F, Fp, rEE, math.degrees(math.atan2(V80[1], V80[0])), 7)
        arc_autour(F, E2, 4, 0, 11)
        arc_autour(F, G, rEE, math.degrees(math.atan2(V80[1], V80[0])), 7)
        arc_autour(F, E2, 3, 90, 13)
        F.seg(Fp, F2, "constr")
        F.seg(G, G2, "constr")
        triangle(F, [E2, F2, G2], ["E'", "F'", "G'"], "image", V, angs=[270, 0, 45])
        angle_droit(F, E2, F2, G2, .32, V)
    else:
        F.point(E2, "E'", ang=270)
    F.fleche(E, E2, "vect")
    triangle(F, [E, Fp, G], "EFG", angs=[200, 300, 135])
    angle_droit(F, E, Fp, G, .32, N)
    etiq_cote(F, E, Fp, "4 cm", .35, "otInk", True, .6)
    etiq_cote(F, G, E, "3 cm", .4, "otInk", False)
    etiq_cote(F, Fp, G, "5 cm", .3, "otInk", True, .55)
    return F.code()


FIGURES["ex3680_enonce"] = ex3680(False)
FIGURES["ex3680_corrige"] = ex3680(True)

# =================================================================== 3681 plan de la chambre
def ex3681():
    U = .7
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=butt,line join=round]" % (U, U)]
    s.append(r"\fill[otSky] (0,0) rectangle (9,7);")
    s.append(r"\draw[otNavy,line width=2.2pt] (1,0) -- (0,0) -- (0,7) -- (9,7) -- (9,0) -- (2.8,0);")
    s.append(r"\draw[otNavy,line width=1pt] (1,0) -- (1,1.8);")
    s.append(r"\draw[otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt] (1,1.8) arc (90:0:1.8);")
    s.append(r"\node[txt,text=otInk] at (4.5,4) {chambre};")
    s.append(r"\draw[cote] (0,7.6) -- (9,7.6) node[midway,coteTexte]{9 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,7.15) -- (0,7.8) (9,7.15) -- (9,7.8);")
    s.append(r"\draw[cote] (9.6,0) -- (9.6,7) node[midway,coteTexte]{7 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (9.15,0) -- (9.8,0) (9.15,7) -- (9.8,7);")
    s.append(r"\draw[cote] (1,-.6) -- (2.8,-.6);")
    s.append(r"\draw[otMuted!70,line width=.4pt] (1,-.15) -- (1,-.8) (2.8,-.15) -- (2.8,-.8);")
    s.append(r"\node[txt,text=otInk,anchor=west] at (3.1,-.6) {porte : 1,8 cm};")
    s.append(r"\node[txt,text=otMuted,anchor=north] at (4.5,-1.3) {plan à l'échelle 1/50};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3681_enonce"] = ex3681()

# =================================================================== 3682 formats de photos
def ex3682(corrige):
    U = .2
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[otGreenDark,line width=1pt] (0,0) rectangle (20,30);")
    s.append(r"\draw[otOrange!90!black,line width=1pt] (0,0) rectangle (13,18);")
    s.append(r"\draw[otNavy,line width=1pt,fill=otSky] (0,0) rectangle (10,15);")
    s.append(r"\node[txt,text=otNavy,anchor=north west] at (.7,14.3) {10 × 15};")
    s.append(r"\node[txt,text=otOrange!80!black,anchor=north west] at (.7,17.3) {13 × 18};")
    s.append(r"\node[txt,text=otGreenDark,anchor=north west] at (.7,29.3) {20 × 30};")
    if corrige:
        s.append(r"\draw[otGreenDark,line width=.9pt,dash pattern=on 4pt off 2.5pt] (0,0) -- (20,30);")
        s.append(r"\draw[otOrange!90!black,line width=.9pt,dash pattern=on 1.5pt off 2pt] (0,0) -- (13,18);")
    s.append(r"\node[txt,text=otMuted,anchor=north] at (10,-.8) {dimensions en cm};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3682_enonce"] = ex3682(False)
FIGURES["ex3682_corrige"] = ex3682(True)

# =================================================================== 3683 maison
MAISON = [(0, 0), (4, 0), (4, 4), (2, 6), (0, 4)]
M83 = tr(MAISON, (1, 1))
M83_1 = homo(MAISON, .5, dest=(7, 1))
M83_2 = homo(MAISON, 1.5, dest=(11, 1))
DONNEES["ex3683"] = {"M": M83, "M1": M83_1, "M2": M83_2}


def ex3683(corrige):
    F = Fig(.46)
    F.grille(0, 0, 18, 11)
    F.poly(M83, "depart")
    F.texte((3, 3), r"$M$", "center", N)
    if corrige:
        F.poly(M83_1, "image")
        F.poly(M83_2, "image")
        F.texte((8, 2), r"$M_1$", "center", V)
        F.texte((14, 4), r"$M_2$", "center", V)
        angle_droit(F, (3, 7), (1, 5), (5, 5), .35, N)
        angle_droit(F, (8, 4), (7, 3), (9, 3), .3, V)
        angle_droit(F, (14, 10), (11, 7), (17, 7), .4, V)
    return F.code()


FIGURES["ex3683_enonce"] = ex3683(False)
FIGURES["ex3683_corrige"] = ex3683(True)

# =================================================================== 3684 compléter un agrandissement
cosE = 75 / 96
D84 = (6 * cosE, 6 * math.sqrt(1 - cosE ** 2))
T84 = {"E": (0, 0), "F": (8, 0), "D": D84}
OX84 = 10.4
T84b = {k + "'": (OX84 + 1.5 * x, 1.5 * y) for k, (x, y) in T84.items()}
DONNEES["ex3684"] = {**T84, **T84b}


def ex3684(corrige):
    F = Fig(.37)
    E, Fp, D = T84["E"], T84["F"], T84["D"]
    E2, F2, D2 = T84b["E'"], T84b["F'"], T84b["D'"]
    triangle(F, [E, Fp, D], "EFD", angs=[225, 315, 90])
    st = "image" if corrige else "depart"
    co = V if corrige else N
    triangle(F, [E2, F2, D2], ["E'", "F'", "D'"], st, co, angs=[225, 315, 90])
    aE = math.degrees(math.atan2(D[1], D[0]))
    for c, r, col in ((E, 1.4, N), (E2, 1.6, co)):
        F.brut(r"\draw[%s,line width=.7pt] %s ++(0:%s) arc (0:%s:%s);" % (col, P(c), f(r), f(aE), f(r)))
        F.brut(r"\node[txt,text=%s,anchor=west] at %s {39°};" % (col, P((c[0] + r + .25, c[1] + .55))), haut=True)
    etiq_cote(F, E, Fp, "8 cm", .55, "otInk", False)
    etiq_cote(F, D, E, "6 cm", .55, "otInk", False)
    etiq_cote(F, Fp, D, "5 cm", .55, "otInk", False)
    etiq_cote(F, D2, E2, "9 cm", .55, co, False)
    etiq_cote(F, E2, F2, "12 cm" if corrige else "?", .55, V if corrige else co, False)
    etiq_cote(F, F2, D2, "7,5 cm" if corrige else "?", .55, V if corrige else co, False)
    return F.code()


FIGURES["ex3684_enonce"] = ex3684(False)
FIGURES["ex3684_corrige"] = ex3684(True)

# =================================================================== 3685 carrelage
CARREAU = [(0, 0), (3, 0), (4, 2), (1, 2)]
DEC85 = (1, 1)


def carreau(c, r):
    return tr(CARREAU, (3 * c + r + DEC85[0], 2 * r + DEC85[1]))


NUM85 = {(0, 0): "1", (1, 0): "2", (0, 1): "3", (1, 1): "4", (3, 2): "5"}
DONNEES["ex3685"] = {n: carreau(*cr) for cr, n in NUM85.items()}


def centre(pts):
    return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts))


def ex3685(corrige):
    U = .5
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[grille] (0,0) grid (17,8);")
    for r in range(3):
        for c in range(4):
            st = "repere" if (c, r) == (0, 0) else "depart"
            s.append(r"\draw[%s] %s -- cycle;" % (st, " -- ".join(P(p) for p in carreau(c, r))))
    # numéro et départ des flèches au même endroit de chaque carreau (repère : coin en bas à gauche) ;
    # décalages choisis pour qu'aucune flèche ne passe sur un numéro
    for (c, r), n in NUM85.items():
        o = carreau(c, r)[0]
        s.append(r"\node[num,text=%s] at %s {%s};" % (O_ if n == "1" else N, P((o[0] + 1.4, o[1] + .5)), n))
    if corrige:
        o1 = carreau(0, 0)[0]
        dep = (o1[0] + 1.0, o1[1] + 1.1)
        for cr in ((1, 0), (0, 1), (1, 1)):
            o = carreau(*cr)[0]
            s.append(r"\draw[vectv] %s -- %s;" % (P(dep), P((o[0] + 1.0, o[1] + 1.1))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3685_enonce"] = ex3685(False)
FIGURES["ex3685_corrige"] = ex3685(True)

# =================================================================== 3686 robot
R86 = {"R": (1, 1), "R_1": (4, 3), "R_2": (6, -1), "P": (3, -3)}
DONNEES["ex3686"] = R86


def ex3686(corrige):
    c = []
    if corrige:
        c.append(fl_axis(R86["R"], R86["P"], "otMuted,line width=.8pt,dash pattern=on 2pt off 2pt,-{Stealth[length=2.2mm]}"))
        c.append(fl_axis(R86["P"], R86["R_2"], "otMuted,line width=.8pt,dash pattern=on 2pt off 2pt,-{Stealth[length=2.2mm]}"))
        c.append(fl_axis(R86["R"], R86["R_2"], "otOrange!90!black,line width=1.1pt,-{Stealth[length=2.6mm]}"))
        c.append(fl_axis(R86["R"], R86["R_1"], "vectv"))
        c.append(fl_axis(R86["R_1"], R86["R_2"], "vectv"))
    c += pt_axis(R86["R"], "R", anchor="south east", dx=-.12, dy=.12)
    if corrige:
        c += pt_axis(R86["R_1"], "R_1", V, anchor="south", dx=0, dy=.2)
        c += pt_axis(R86["R_2"], "R_2", V, anchor="west", dx=.2, dy=0)
        c += pt_axis(R86["P"], r"(3 ; -3)", "otMuted", anchor="north", dx=0, dy=-.2)
    return repere(-1.5, 8.5, -4.5, 5.5, .6, c)


FIGURES["ex3686_enonce"] = ex3686(False)
FIGURES["ex3686_corrige"] = ex3686(True)

# =================================================================== 3687 logo
LOGO = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
L87 = tr(LOGO, (1, 1))
L87g = homo(LOGO, 1.5, dest=(7, 1))
DONNEES["ex3687"] = {"depart": L87, "agrandi": L87g}


def cotes_logo(F, pts, vals, coul, d=.4):
    ts = [.5, .5, .3, .7, .5, .5]   # côtés intérieurs : étiquettes écartées du coin rentrant
    for i, v in enumerate(vals):
        p, q = pts[i], pts[(i + 1) % len(pts)]
        etiq_cote(F, p, q, v, d, coul, False, ts[i])


def ex3687(corrige):
    F = Fig(.58)
    F.grille(0, 0, 14, 8)
    F.poly(L87, "depart")
    cotes_logo(F, L87, ["4", "2", "2", "2", "2", "4"], N)
    if corrige:
        F.poly(L87g, "image")
        cotes_logo(F, L87g, ["6", "3", "3", "3", "3", "6"], V)
    return F.code()


FIGURES["ex3687_enonce"] = ex3687(False)
FIGURES["ex3687_corrige"] = ex3687(True)

# =================================================================== 3688 jardin
def ex3688():
    U = .55
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[otGreenDark,line width=1.2pt,fill=otGreen!14] (0,0) rectangle (15,8);")
    s.append(r"\draw[otNavy,line width=1pt,fill=otSky] (11,5) circle (1);")
    s.append(r"\node[txt,text=otGreenDark] at (5.5,4) {pelouse};")
    s.append(r"\node[txt,text=otNavy,anchor=north] at (11,3.65) {bassin};")
    s.append(r"\draw[cote] (10,6.5) -- (12,6.5) node[midway,above=2pt,txt,text=otInk]{2 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (10,5) -- (10,6.7) (12,5) -- (12,6.7);")
    s.append(r"\draw[cote] (0,-.7) -- (15,-.7) node[midway,coteTexte]{15 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,-.2) -- (0,-.9) (15,-.2) -- (15,-.9);")
    s.append(r"\draw[cote] (-.7,0) -- (-.7,8) node[midway,coteTexte]{8 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (-.2,0) -- (-.9,0) (-.2,8) -- (-.9,8);")
    s.append(r"\node[txt,text=otMuted,anchor=north] at (7.5,-1.4) {plan à l'échelle 1/200};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3688_enonce"] = ex3688()

# =================================================================== 3689 tour
def ex3689():
    U = .5
    H = 10.0
    h2 = H * 115 / 330
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    gauche = [(0, 0), (1.25, 1.7), (2.0, h2), (2.75, 8.4), (2.9, 9.6)]
    droite = [(5.8 - x, y) for x, y in gauche]
    s.append(r"\fill[otSky] %s -- %s -- (2.9,1.05) arc (90:180:1.45 and 1.05) -- cycle;" % (
        " -- ".join(P(p) for p in gauche + list(reversed(droite))), P((4.35, 0))))
    s.append(r"\draw[otNavy,line width=1pt] %s;" % " -- ".join(P(p) for p in gauche))
    s.append(r"\draw[otNavy,line width=1pt] %s;" % " -- ".join(P(p) for p in droite))
    s.append(r"\draw[otNavy,line width=1pt] (2.9,9.6) -- (2.9,%s);" % f(H))
    s.append(r"\draw[otNavy,line width=1pt] (1.45,0) arc (180:0:1.45 and 1.05);")
    s.append(r"\draw[otNavy,line width=1pt] (.95,1.7) -- (4.85,1.7);")
    s.append(r"\draw[otNavy,line width=1pt] (1.75,%s) -- (4.05,%s);" % (f(h2), f(h2)))
    s.append(r"\draw[otMuted,line width=.8pt] (-1.6,0) -- (8.8,0);")
    s.append(r"\draw[cote] (8.3,0) -- (8.3,%s) node[midway,coteTexte]{330 m};" % f(H))
    s.append(r"\draw[otMuted!70,line width=.4pt] (3.1,%s) -- (8.5,%s);" % (f(H), f(H)))
    s.append(r"\draw[cote] (-1.1,0) -- (-1.1,%s) node[midway,coteTexte]{115 m};" % f(h2))
    s.append(r"\draw[otMuted!70,line width=.4pt] (1.55,%s) -- (-1.3,%s);" % (f(h2), f(h2)))
    s.append(r"\node[txt,text=otNavy,anchor=west] at (4.4,%s) {2\textsuperscript{e} étage};" % f(h2 + .45))
    s.append(r"\draw[cote] (0,-.8) -- (5.8,-.8) node[midway,coteTexte]{125 m};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,-.2) -- (0,-1) (5.8,-.2) -- (5.8,-1);")
    s.append(r"\node[txt,text=otMuted,anchor=north] at (2.9,-1.5) {(schéma, pas à l'échelle)};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3689_enonce"] = ex3689()

# =================================================================== 3690 formats de papier
FORMATS = {"A5": (14.85, 21), "A4": (21, 29.7), "A3": (29.7, 42)}
DONNEES["ex3690"] = FORMATS


def ex3690(corrige):
    U = .15
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    coul = {"A3": "otGreenDark", "A4": "otNavy", "A5": "otOrange!90!black"}
    for n in ("A3", "A4", "A5"):
        w, h = FORMATS[n]
        fill = ",fill=otSky" if n == "A4" else (",fill=otOrange!14" if n == "A5" else "")
        s.append(r"\draw[%s,line width=1pt%s] (0,0) rectangle (%s,%s);" % (coul[n], fill, f(w), f(h)))
    for n in ("A3", "A4", "A5"):
        w, h = FORMATS[n]
        s.append(r"\node[txt,text=%s,anchor=north west] at (1,%s) {%s};" % (coul[n].replace("!90!black", "!80!black"), f(h - 1), n))
    if corrige:
        s.append(r"\draw[otGreenDark,line width=.9pt,dash pattern=on 4pt off 2.5pt] (0,0) -- (29.7,42);")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3690_enonce"] = ex3690(False)
FIGURES["ex3690_corrige"] = ex3690(True)

# =================================================================== 3691 théâtre d'ombres
O91 = {"L": (0, 0), "A": (5, 0), "B": (5, 1), "A'": (20, 0), "B'": (20, 4)}   # unité : 10 cm
DONNEES["ex3691"] = O91


def ex3691(corrige):
    U = .39
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[otMuted,line width=.8pt] (-.8,0) -- (21.5,0);")
    s.append(r"\draw[otMuted!60,line width=3pt] (20.35,-.1) -- (20.35,5);")
    s.append(r"\draw[otOrange!90!black,line width=.8pt,dash pattern=on 3.5pt off 2pt] (0,0) -- (20,4);")
    s.append(r"\draw[otNavy,line width=2pt] (5,0) -- (5,1);")
    s.append(r"\draw[%s,line width=2pt] (20,0) -- (20,4);" % ("otGreenDark" if corrige else "otNavy"))
    s.append(r"\fill[otOrange] (0,0) circle (4pt);")
    for k, anc, d in (("A", "north", (0, -.25)), ("A'", "north east", (-.15, -.2)), ("B", "south east", (-.12, .15)),
                      ("B'", "south east", (-.15, .1)), ("L", "north", (0, -.35))):
        p = O91[k]
        s.append(r"\fill[otNavy] %s circle (2pt);" % P(p))
        s.append(r"\node[lab,anchor=%s] at %s {$%s$};" % (anc, P((p[0] + d[0], p[1] + d[1])), k))
    s.append(r"\node[txt,text=otOrange!80!black,anchor=south] at (0,.5) {lampe};")
    s.append(r"\node[txt,text=otMuted,anchor=south] at (20.35,5.2) {écran};")
    s.append(r"\node[txt,text=otNavy,anchor=west] at (5.35,.5) {10 cm};")
    s.append(r"\node[txt,text=%s,anchor=east] at (19.6,1.9) {%s};" % (("otGreenDark", "40 cm") if corrige else ("otNavy", "?")))
    s.append(r"\draw[cote] (0,-1.5) -- (5,-1.5) node[midway,coteTexte]{50 cm};")
    s.append(r"\draw[cote] (0,-2.6) -- (20,-2.6) node[midway,coteTexte]{200 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,-.9) -- (0,-2.8) (5,-.9) -- (5,-1.7) (20,-.9) -- (20,-2.8);")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3691_enonce"] = ex3691(False)
FIGURES["ex3691_corrige"] = ex3691(True)
