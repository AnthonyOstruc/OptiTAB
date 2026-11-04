# -*- coding: utf-8 -*-
"""Figures de la notion « Transformations du plan » (3e), style des livres.

Compilées par outils/figures_livre.py. Constructions sur quadrillage pâle :
bleu marine = figure de départ et éléments donnés (axe, centre, vecteur),
vert foncé = image et traits de construction (corrigés), orange = motif repère
(frise, rosace, pavage). Les étiquettes des points sont placées automatiquement
dans la direction la plus éloignée des traits qui partent du point
(on peut imposer l'angle).
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
  cache/.style={otMuted,line width=.8pt,dash pattern=on 3pt off 2pt},
}
"""

V = "otGreenDark"
N = "otNavy"


def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def ecart(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


class Fig:
    """Figure sur quadrillage : segments mémorisés pour placer les étiquettes."""

    def __init__(self, U=.6):
        self.U = U
        self.fond, self.corps, self.haut = [], [], []
        self.segs = []
        self.etiq = []
        self.pts = []

    # ------------------------------------------------------------ tracés
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

    # ------------------------------------------------------------ étiquettes
    def directions(self, p):
        dirs = []
        for a, b in self.segs:
            for u, v in ((a, b), (b, a)):
                if math.hypot(u[0] - p[0], u[1] - p[1]) < 1e-9 and math.hypot(v[0] - p[0], v[1] - p[1]) > 1e-9:
                    dirs.append(math.degrees(math.atan2(v[1] - p[1], v[0] - p[0])))
            # p strictement à l'intérieur de [ab]
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
                    # légère préférence pour les diagonales (étiquette hors des lignes du quadrillage)
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
    """Marque d'angle droit au sommet s entre les directions s→p et s→q (taille en unités)."""
    def u(a):
        L = math.hypot(a[0] - s[0], a[1] - s[1])
        return ((a[0] - s[0]) / L * taille, (a[1] - s[1]) / L * taille)
    a, b = u(p), u(q)
    F.brut(r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (
        coul, P((s[0] + a[0], s[1] + a[1])), P((s[0] + a[0] + b[0], s[1] + a[1] + b[1])), P((s[0] + b[0], s[1] + b[1]))))


def codage(F, p, q, n=1, coul=V):
    """n petits traits au milieu de [pq]."""
    m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    h = .2
    for k in range(n):
        o = (k - (n - 1) / 2) * .13
        c = (m[0] + o * ux, m[1] + o * uy)
        F.brut(r"\draw[%s,line width=.75pt] %s -- %s;" % (
            coul, P((c[0] - h * uy, c[1] + h * ux)), P((c[0] + h * uy, c[1] - h * ux))))


def primes(noms):
    return [n + "'" for n in noms]


def triangle(F, pts, noms, style="depart", coul=N, angs=None):
    F.poly(pts, style)
    for i, (p, n) in enumerate(zip(pts, noms)):
        F.point(p, n, coul, ang=None if angs is None else angs[i])


FIGURES = {}
TOLERE = {}

# =================================================================== exercices : isométries
def ex_axiale(corrige):
    F = Fig(.62)
    F.grille(0, 0, 12, 6)
    F.seg((6, -.4), (6, 6.4), "axe")
    F.texte((6.2, 6.25), r"$(d)$", "west", "otNavy")
    A, B, C = (1, 1), (4, 1), (2, 4)
    img = [(12 - x, y) for x, y in (A, B, C)]
    if corrige:
        F.seg(C, img[2], "constr")
        H = (6, 4)
        angle_droit(F, H, (10, 4), (6, 6))
        codage(F, C, H, 2)
        codage(F, H, img[2], 2)
        triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    return F.code()


FIGURES["ex2401_enonce"] = ex_axiale(False)
FIGURES["ex2401_corrige"] = ex_axiale(True)


def ex_centrale(corrige):
    F = Fig(.62)
    F.grille(0, 0, 12, 8)
    O = (6, 4)
    A, B, C = (2, 5), (5, 5), (2, 7)
    img = [(12 - x, 8 - y) for x, y in (A, B, C)]
    if corrige:
        for p, q in zip((A, B, C), img):
            F.seg(p, q, "constr")
        codage(F, A, O, 1)
        codage(F, O, img[0], 1)
        codage(F, C, O, 2)
        codage(F, O, img[2], 2)
        triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    F.point(O, "O")
    return F.code()


FIGURES["ex2402_enonce"] = ex_centrale(False)
FIGURES["ex2402_corrige"] = ex_centrale(True)


def ex_translation(corrige):
    F = Fig(.62)
    F.grille(0, 0, 10, 8)
    Pp, Q = (1, 5), (5, 7)
    F.fleche(Pp, Q, "vect")
    F.point(Pp, "P")
    F.point(Q, "Q")
    A, B, C = (1, 1), (4, 1), (2, 3)
    img = [(x + 4, y + 2) for x, y in (A, B, C)]
    if corrige:
        for p, q in zip((A, B, C), img):
            F.fleche(p, q, "constr,-{Stealth[length=2.2mm]}")
        triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    return F.code()


FIGURES["ex2403_enonce"] = ex_translation(False)
FIGURES["ex2403_corrige"] = ex_translation(True)


def ex_rotation(corrige):
    F = Fig(.62)
    F.grille(1, 2, 10, 9)
    O = (5, 4)
    A, B, C = (7, 4), (9, 4), (8, 6)
    img = [(5 - (y - 4), 4 + (x - 5)) for x, y in (A, B, C)]
    if corrige:
        F.seg(O, A, "constr")
        F.seg(O, img[0], "constr")
        angle_droit(F, O, A, img[0])
        F.brut(r"\draw[otGreenDark,line width=.8pt,-{Stealth[length=2.2mm]}] (%s,4) arc (0:86:2);" % f(7 - 0))
        triangle(F, img, primes("ABC"), "image", V, angs=[205, None, None])
    triangle(F, [A, B, C], "ABC", angs=[300, 330, 90] if corrige else None)
    F.point(O, "O")
    return F.code()


FIGURES["ex2404_enonce"] = ex_rotation(False)
FIGURES["ex2404_corrige"] = ex_rotation(True)


# -------------------------------------------------- reconnaître une transformation
GAMMA = [(1, 4), (2, 4), (2, 6), (3, 6), (3, 7), (1, 7)]


def ex_reconnaitre(corrige):
    F = Fig(.55)
    F.grille(0, 0, 15, 8)
    F1 = [(x, y - 4) for x, y in GAMMA]
    F2 = [(9 - x, y) for x, y in GAMMA]
    F3 = [(10 - x, 7 - y) for x, y in GAMMA]
    F4 = [(y + 7, 6 - x) for x, y in GAMMA]
    F5 = [(.5 * x + 10.5, .5 * y - 1.5) for x, y in GAMMA]
    if corrige:
        F.seg((4.5, -.4), (4.5, 8.4), "constr")
        F.texte((4.65, 8.25), r"axe", "west", V, "txt")
        F.seg((1, 4), (9, 3), "constr")
        F.fleche((.45, 6.5), (.45, 2.5), "vectv")
    F.poly(GAMMA, "repere")
    for pts, st in ((F1, "depart"), (F2, "depart"), (F3, "depart"), (F4, "depart"), (F5, "depart")):
        F.poly(pts, st)
    F.texte((1.5, 5), r"$F$", "center", "otOrange!80!black")
    F.texte((1.5, 1), r"$F_1$", "center", N)
    F.texte((7.5, 5), r"$F_2$", "center", N)
    F.texte((8.5, 1.5), r"$F_3$", "center", N)
    F.texte((12, 4.5), r"$F_4$", "center", N)
    F.texte((12.25, 1.25), r"$F_5$", "west", N)
    if corrige:
        F.point((5, 3.5), "I", V, ang=270)
    return F.code()


FIGURES["ex2406_enonce"] = ex_reconnaitre(False)
FIGURES["ex2406_corrige"] = ex_reconnaitre(True)


# =================================================================== homothéties
def ex_homot(O, pts, k, grille, corrige, U=.6, angs=None, angO=None):
    F = Fig(U)
    F.grille(*grille)
    img = [(O[0] + k * (x - O[0]), O[1] + k * (y - O[1])) for x, y in pts]
    if corrige:
        for p, q in zip(pts, img):
            if k > 0:
                F.seg(O, q if abs(k) > 1 else p, "constr")
            else:
                F.seg(p, q, "constr")
        triangle(F, img, primes("ABC"), "image", V, angs=None if angs is None else angs[3:])
    triangle(F, pts, "ABC", angs=None if angs is None else angs[:3])
    F.point(O, "O", ang=angO)
    return F.code()


A08 = [165, None, None, None, None, None]
FIGURES["ex2408_enonce"] = ex_homot((1, 1), [(4, 2), (6, 2), (5, 4)], 2, (0, 0, 12, 8), False, angs=A08)
FIGURES["ex2408_corrige"] = ex_homot((1, 1), [(4, 2), (6, 2), (5, 4)], 2, (0, 0, 12, 8), True, angs=A08)
FIGURES["ex2409_enonce"] = ex_homot((7, 4), [(1, 2), (5, 2), (3, 6)], -.5, (0, 1, 11, 7), False, angO=270)
FIGURES["ex2409_corrige"] = ex_homot((7, 4), [(1, 2), (5, 2), (3, 6)], -.5, (0, 1, 11, 7), True, angO=270)


def ex_centre(corrige):
    """Homothétie de centre caché Ω(1 ; 1) et de rapport 2."""
    F = Fig(.62)
    F.grille(0, 0, 10, 8)
    W = (1, 1)
    pts = [(3, 3), (5, 3), (3, 4)]
    img = [(1 + 2 * (x - 1), 1 + 2 * (y - 1)) for x, y in pts]
    if corrige:
        for q in img:
            F.seg(W, q, "constr")
        F.point(W, r"\Omega", V)
    triangle(F, img, primes("ABC"), "depart")
    triangle(F, pts, "ABC", angs=[270, None, None])
    return F.code()


FIGURES["ex2415_enonce"] = ex_centre(False)
FIGURES["ex2415_corrige"] = ex_centre(True)


def ex_rapport():
    """Deux cas : A' du même côté que A, ou de l'autre côté de O (OA = 4, OA' = 10)."""
    U = .55
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round]" % (U, U)]

    def ligne(y, xo, xa, xap, titre):
        xs = [xo, xa, xap]
        s.append(r"\draw[otMuted,line width=.6pt] (%s,%s) -- (%s,%s);" % (f(min(xs) - .8), f(y), f(max(xs) + .8), f(y)))
        for x, nom, c in ((xo, "O", N), (xa, "A", N), (xap, "A'", V)):
            s.append(r"\fill[%s] (%s,%s) circle (2.2pt);" % (c, f(x), f(y)))
            s.append(r"\node[lab,text=%s,anchor=south] at (%s,%s) {$%s$};" % ("otInk" if c == N else c, f(x), f(y + .3), nom))
        s.append(r"\draw[cote] (%s,%s) -- (%s,%s) node[midway,coteTexte]{4 cm};" % (f(xo), f(y - .75), f(xa), f(y - .75)))
        s.append(r"\draw[cote] (%s,%s) -- (%s,%s) node[midway,coteTexte]{10 cm};" % (f(xo), f(y - 1.75), f(xap), f(y - 1.75)))
        for x in (xo, xa):
            s.append(r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y - .2), f(x), f(y - .95)))
        for x in (xo, xap):
            s.append(r"\draw[otMuted!70,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y - .2), f(x), f(y - 1.95)))
        s.append(r"\node[txt,text=otGreenDark,anchor=west] at (%s,%s) {%s};" % (f(min(xs) - .8), f(y + 1.2), titre))

    ligne(5.2, 0, 4, 10, r"Cas 1 : même côté, $k = 2{,}5$")
    ligne(0, 10, 14, 0, r"Cas 2 : de part et d'autre de $O$, $k = -2{,}5$")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2410_corrige"] = ex_rapport()


# =================================================================== frise, rosace, pavage
CHEVRON = [(.5, .5), (2.5, .5), (3.5, 1.5), (2.5, 2.5), (.5, 2.5), (1.5, 1.5)]


def ex_frise(corrige, n=6, U=.34):
    F = Fig(U)
    F.grille(0, 0, 4 * n, 3)
    for i in range(n):
        F.poly([(x + 4 * i, y) for x, y in CHEVRON], "repere" if i == 0 else "depart")
        F.texte((4 * i + 2, -.45), str(i + 1), "north", "otOrange!80!black" if i == 0 else N, "num")
    if corrige:
        for x in (3.5, 7.5, 19.5):
            F.seg((x, 1.5), (x, 3.3 if x == 3.5 else 4.6), "constr", memo=False)
        F.seg((7.5, 3.3), (7.5, 4.6), "constr", memo=False)
        F.fleche((3.5, 3.6), (7.5, 3.6), "vectv")
        F.texte((5.5, 3.8), "4 cm", "south", V, "txt")
        F.fleche((7.5, 4.9), (19.5, 4.9), "vectv")
        F.texte((13.5, 5.1), "12 cm", "south", V, "txt")
    return F.code()


FIGURES["ex2413_enonce"] = ex_frise(False)
FIGURES["ex2413_corrige"] = ex_frise(True)


def petale(t, R=3.0):
    return (r"(0,0) .. controls (%s:%s) and (%s:%s) .. (%s:%s) .. controls (%s:%s) and (%s:%s) .. (0,0)"
            % (f(t - 22), f(R * .45), f(t - 14), f(R * .85), f(t), f(R), f(t + 14), f(R * .85), f(t + 22), f(R * .45)))


def rosace(n, corrige, numeros=True, U=.8):
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round]" % (U, U)]
    for i in range(n):
        t = 360 / n * i
        st = "repere" if i == 0 else "depart"
        s.append(r"\draw[%s] %s;" % (st, petale(t)))
        if numeros:
            s.append(r"\node[num,text=%s] at (%s:3.55) {%d};" % ("otOrange!80!black" if i == 0 else N, f(t), i + 1))
    if corrige:
        a = 360 / n
        s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.2mm]}] (0:2.45) arc (0:%s:2.45);" % f(a - 2))
        s.append(r"\node[txt,text=otGreenDark] at (%s:3.55) {%s\,°};" % (f(a / 2), f(a).replace(".", "{,}")))
    s.append(r"\fill[otNavy] (0,0) circle (2.2pt);")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2414_enonce"] = rosace(8, False)
FIGURES["ex2414_corrige"] = rosace(8, True)


def pavage(numeros, corrige, U=.95, nx=4, ny=2):
    """Carrés de 2 carreaux coupés par leur diagonale montante."""
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    W, H = 2 * nx, 2 * ny
    s.append(r"\draw[grille] (0,0) grid (%d,%d);" % (W, H))
    marques = {}
    if numeros:
        marques = {(0, 0, "b"): "1", (0, 0, "h"): "2", (2, 0, "b"): "3", (1, 1, "b"): "4", (1, 0, "h"): "5"}
    for i in range(nx):
        for j in range(ny):
            x, y = 2 * i, 2 * j
            for part, pts, g in (("b", [(x, y), (x + 2, y), (x + 2, y + 2)], (x + 4 / 3, y + 2 / 3)),
                                 ("h", [(x, y), (x + 2, y + 2), (x, y + 2)], (x + 2 / 3, y + 4 / 3))):
                lab = marques.get((i, j, part))
                st = "repere" if lab == "1" else "depart"
                s.append(r"\draw[%s] %s -- cycle;" % (st, " -- ".join(P(p) for p in pts)))
                if lab:
                    s.append(r"\node[num,text=%s] at %s {%s};" % ("otOrange!80!black" if lab == "1" else N, P(g), lab))
    if corrige:
        # translations 1 → 3 et 1 → 4, axe de 1 ↔ 2, centres de 1 ↔ 2 et de 1 ↔ 5
        s.append(r"\draw[otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt] (-.4,-.4) -- (2.45,2.45);")
        s.append(r"\fill[otGreenDark] (1,1) circle (2.6pt);")
        s.append(r"\fill[otGreenDark] (2,1) circle (2.6pt);")
        s.append(r"\draw[vectv] (.9,.3) -- (4.9,.3);")
        s.append(r"\draw[vectv] (1.6,1.3) -- (3.6,3.3);")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2417_enonce"] = pavage(True, False)
FIGURES["ex2417_corrige"] = pavage(True, True)


# =================================================================== problèmes
def logo(corrige):
    U = .9
    A, B, C = (0, 0), (4, 0), (0, 3)
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[depart] (0,0) -- (4,0) -- (0,3) -- cycle;")
    if corrige:
        s.append(r"\draw[otGreenDark,line width=.7pt] (.35,0) -- (.35,.35) -- (0,.35);")
    s.append(r"\draw[cote] (0,-.45) -- (4,-.45) node[midway,coteTexte]{4 cm};")
    s.append(r"\draw[cote] (-.45,0) -- (-.45,3) node[midway,coteTexte]{3 cm};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (0,-.1) -- (0,-.6) (4,-.1) -- (4,-.6) (-.1,0) -- (-.6,0) (-.1,3) -- (-.6,3);")
    s.append(r"\draw[cote] ($(4,0)!.45cm!-90:(0,3)$) -- ($(0,3)!.45cm!90:(4,0)$) node[midway,coteTexte]{5 cm};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2418_enonce"] = logo(False)
FIGURES["ex2418_corrige"] = logo(True)


def projecteur(corrige):
    U = .92
    O = (0, 0)
    Pd, Qd = (-1.4, .5), (-1.4, -.5)
    k = -5.6 / 1.4
    Pe, Qe = (Pd[0] * k, Pd[1] * k), (Qd[0] * k, Qd[1] * k)
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[otOrange!90!black,line width=.7pt,dash pattern=on 3.5pt off 2pt] %s -- %s %s -- %s;" % (P(Pd), P(Pe), P(Qd), P(Qe)))
    s.append(r"\draw[otNavy,line width=2pt] %s -- %s;" % (P(Pd), P(Qd)))
    s.append(r"\draw[%s,line width=2pt] %s -- %s;" % ("otGreenDark" if corrige else "otNavy", P(Pe), P(Qe)))
    s.append(r"\draw[otMuted,line width=.8pt] (5.6,-2.7) -- (5.6,2.7);")
    s.append(r"\fill[otNavy] (0,0) circle (2.2pt);")
    s.append(r"\node[lab,anchor=north] at (0,-.32) {$O$};")
    s.append(r"\node[txt,text=otNavy,anchor=south] at (-1.4,.7) {diapositive};")
    s.append(r"\node[txt,text=otMuted,anchor=south] at (5.6,2.85) {écran};")
    s.append(r"\node[txt,text=otNavy,anchor=east] at (-1.6,0) {3,6 cm};")
    s.append(r"\node[txt,text=%s,anchor=west] at (5.8,0) {%s};" % (("otGreenDark", "2,88 m") if corrige else ("otNavy", "?")))
    s.append(r"\draw[cote] (-1.4,-2.2) -- (0,-2.2) node[midway,coteTexte]{5 cm};")
    s.append(r"\draw[cote] (0,-3.1) -- (5.6,-3.1) node[midway,coteTexte]{4 m};")
    s.append(r"\draw[otMuted!70,line width=.4pt] (-1.4,-.65) -- (-1.4,-2.35) (0,-.75) -- (0,-3.25) (5.6,-2.75) -- (5.6,-3.25);")
    s.append(r"\node[txt,text=otMuted,anchor=north] at (2.8,-3.45) {(schéma, pas à l'échelle)};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2419_enonce"] = projecteur(False)
FIGURES["ex2419_corrige"] = projecteur(True)


def parallelogramme(corrige):
    F = Fig(.8)
    F.grille(0, 0, 7, 6)
    A, B, C, D = (1, 1), (5, 2), (6, 5), (2, 4)
    I = (3.5, 3)
    if corrige:
        F.seg(A, C, "constr")
        F.seg(B, D, "constr")
        F.fleche(B, A, "vectv")
        F.fleche(C, D, "vectv")
        F.seg(A, D, "image")
        F.point(D, "D", V)
        F.point(I, "I", V, ang=90, d=.2)
    else:
        F.fleche(B, A, "vect")
    F.seg(B, C, "geoTrait")
    F.point(A, "A")
    F.point(B, "B")
    F.point(C, "C")
    return F.code()


FIGURES["ex2420_enonce"] = parallelogramme(False)
FIGURES["ex2420_corrige"] = parallelogramme(True)


def pyramide(section_verte=False, U=.62, cotes=True):
    A, B, C, D = (0, 0), (6, 0), (8.4, 2.2), (2.4, 2.2)
    H = (4.2, 1.1)
    S = (4.2, 8.4)
    sec = [((S[0] + (p[0] - S[0]) / 3), (S[1] + (p[1] - S[1]) / 3)) for p in (A, B, C, D)]
    Hs = ((S[0] + (H[0] - S[0]) / 3), (S[1] + (H[1] - S[1]) / 3))
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(S)))
    s.append(r"\fill[%s] %s -- cycle;" % ("otGreen!25" if section_verte else "otOrange!25", " -- ".join(P(p) for p in sec)))
    s.append(r"\draw[cache] %s -- %s -- %s %s -- %s %s -- %s;" % (P(A), P(D), P(C), P(S), P(D), P(S), P(H)))
    cs = "otGreenDark" if section_verte else "otOrange!90!black"
    s.append(r"\draw[%s,line width=1pt] %s -- %s -- %s;" % (cs, P(sec[0]), P(sec[1]), P(sec[2])))
    s.append(r"\draw[%s,line width=.8pt,dash pattern=on 3pt off 2pt] %s -- %s -- %s;" % (cs, P(sec[2]), P(sec[3]), P(sec[0])))
    s.append(r"\draw[geoTrait] %s -- %s -- %s -- %s -- %s %s -- %s;" % (P(A), P(B), P(C), P(S), P(A), P(S), P(B)))
    for p in (S, A, B, C, D, H):
        s.append(r"\fill[otNavy] %s circle (1.9pt);" % P(p))
    s.append(r"\node[lab,anchor=south] at %s {$S$};" % P((S[0], S[1] + .2)))
    s.append(r"\node[lab,anchor=north east] at %s {$A$};" % P((A[0] - .1, A[1] - .1)))
    s.append(r"\node[lab,anchor=north west] at %s {$B$};" % P((B[0] + .1, B[1] - .1)))
    s.append(r"\node[lab,anchor=west] at %s {$C$};" % P((C[0] + .18, C[1])))
    s.append(r"\node[lab,anchor=east] at %s {$D$};" % P((D[0] - .2, D[1] + .05)))
    s.append(r"\node[lab,anchor=north] at %s {$H$};" % P((H[0] + .25, H[1] - .12)))
    if cotes:
        s.append(r"\node[txt,text=%s,anchor=west] at %s {section};" % (cs, P((sec[2][0] + .5, sec[2][1]))))
        s.append(r"\draw[otMuted!70,line width=.4pt] %s -- %s;" % (P((sec[2][0] + .1, sec[2][1])), P((sec[2][0] + .45, sec[2][1]))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2421_enonce"] = pyramide()

# =================================================================== cours et fiche
def cours_axiale():
    F = Fig(.62)
    F.grille(0, 0, 8, 7)
    F.seg((-.3, -.3), (7.3, 7.3), "axe")
    F.texte((6.85, 7.3), r"$(d)$", "south east", "otNavy")
    A, B, C = (1, 3), (2, 6), (4, 6)
    img = [(y, x) for x, y in (A, B, C)]
    for p, q in zip((A, B, C), img):
        F.seg(p, q, "constr")
    Hm = (2, 2)
    angle_droit(F, Hm, A, (5, 5), .3)
    codage(F, A, Hm, 2)
    codage(F, Hm, img[0], 2)
    triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    return F.code()


FIGURES["cours_axiale"] = cours_axiale()


def cours_centrale():
    F = Fig(.62)
    F.grille(0, 0, 10, 7)
    O = (5, 3)
    A, B, C = (1, 4), (4, 4), (3, 6)
    img = [(10 - x, 6 - y) for x, y in (A, B, C)]
    for p, q in zip((A, B, C), img):
        F.seg(p, q, "constr")
    codage(F, A, O, 1)
    codage(F, O, img[0], 1)
    codage(F, B, O, 2)
    codage(F, O, img[1], 2)
    triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    F.point(O, "O")
    return F.code()


FIGURES["cours_centrale"] = cours_centrale()


def cours_translation():
    F = Fig(.62)
    F.grille(0, 0, 11, 6)
    F.fleche((7, 1), (10, 3), "vect")
    F.texte((8.75, 1.8), r"$\vec{u}$", "north west", "otNavy")
    A, B, C = (1, 1), (4, 2), (2, 3)
    img = [(x + 3, y + 2) for x, y in (A, B, C)]
    for p, q in zip((A, B, C), img):
        F.fleche(p, q, "constr,-{Stealth[length=2.2mm]}")
    triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    return F.code()


FIGURES["cours_translation"] = cours_translation()


def cours_rotation():
    F = Fig(.62)
    F.grille(0, 0, 9, 7)
    O = (4, 2)
    A, B, C = (2, 3), (1, 5), (3, 5)
    rot = lambda p: (O[0] + (p[1] - O[1]), O[1] - (p[0] - O[0]))   # quart de tour, sens des aiguilles
    img = [rot(p) for p in (A, B, C)]
    F.seg(O, B, "constr")
    F.seg(O, img[1], "constr")
    angle_droit(F, O, B, img[1], .3)
    rB = math.hypot(B[0] - O[0], B[1] - O[1])
    a0 = math.degrees(math.atan2(B[1] - O[1], B[0] - O[0]))
    F.brut(r"\draw[otGreenDark,line width=.8pt,-{Stealth[length=2.2mm]}] %s arc (%s:%s:%s);"
           % (P(B), f(a0), f(a0 - 86), f(rB)))
    triangle(F, img, primes("ABC"), "image", V)
    triangle(F, [A, B, C], "ABC")
    F.point(O, "O", ang=225)
    return F.code()


FIGURES["cours_rotation"] = cours_rotation()

FIGURES["cours_homot_pos"] = ex_homot((0, 1), [(2, 2), (3, 2), (2, 3)], 3, (-1, 0, 10, 7), True, U=.62)
FIGURES["cours_homot_neg"] = ex_homot((5, 4), [(7, 3), (8, 5), (6, 6)], -2, (-2, -1, 9, 7), True, U=.62, angO=None)


def cours_k():
    """Côtés × 2 : aire × 4, volume × 8."""
    U = .64
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s.append(r"\draw[depart] (0,0) rectangle (1,1);")
    s.append(r"\draw[image] (1.8,0) rectangle (3.8,2);")
    s.append(r"\draw[otGreenDark,line width=.5pt] (2.8,0) -- (2.8,2) (1.8,1) -- (3.8,1);")
    s.append(r"\node[txt,text=otInk,anchor=north,align=center] at (1.9,-.35) {côtés $\times 2$\\aire $\times 4$};")
    ox = 5.6
    dx, dy = .55, .4

    def cube(x, y, a, st, sub):
        pts = lambda u, v, w: (x + u + w * dx, y + v + w * dy)
        av = [pts(0, 0, 0), pts(a, 0, 0), pts(a, a, 0), pts(0, a, 0)]
        dessus = [pts(0, a, 0), pts(a, a, 0), pts(a, a, a), pts(0, a, a)]
        cote = [pts(a, 0, 0), pts(a, 0, a), pts(a, a, a), pts(a, a, 0)]
        for face in (av, dessus, cote):
            s.append(r"\draw[%s] %s -- cycle;" % (st, " -- ".join(P(p) for p in face)))
        if sub:
            c = "otGreenDark,line width=.5pt"
            h = a / 2
            s.append(r"\draw[%s] %s -- %s %s -- %s;" % (c, P(pts(h, 0, 0)), P(pts(h, a, 0)), P(pts(0, h, 0)), P(pts(a, h, 0))))
            s.append(r"\draw[%s] %s -- %s %s -- %s;" % (c, P(pts(h, a, 0)), P(pts(h, a, a)), P(pts(0, a, h)), P(pts(a, a, h))))
            s.append(r"\draw[%s] %s -- %s %s -- %s;" % (c, P(pts(a, 0, h)), P(pts(a, a, h)), P(pts(a, h, 0)), P(pts(a, h, a))))

    cube(ox, 0, 1, "depart", False)
    cube(ox + 1.9, 0, 2, "image", True)
    s.append(r"\node[txt,text=otInk,anchor=north,align=center] at (%s,-.35) {arêtes $\times 2$\\volume $\times 8$};" % f(ox + 2.0))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_k"] = cours_k()


def cours_frise():
    F = Fig(.42)
    F.grille(0, 0, 16, 3)
    for i in range(4):
        F.poly([(x + 4 * i, y) for x, y in CHEVRON], "repere" if i == 0 else "depart")
    F.fleche((3.5, 3.5), (7.5, 3.5), "vectv")
    F.seg((3.5, 1.5), (3.5, 3.3), "constr", memo=False)
    F.seg((7.5, 1.5), (7.5, 3.3), "constr", memo=False)
    F.texte((5.5, 3.75), r"$\vec{u}$", "south", V)
    return F.code()


FIGURES["cours_frise"] = cours_frise()
FIGURES["cours_rosace"] = rosace(6, True, numeros=False, U=.62)
FIGURES["cours_pavage"] = pavage(False, False, U=.75, nx=5, ny=2)


def fiche_isometries():
    U = .42
    G = [(1, 1), (2, 1), (2, 3), (3, 3), (3, 4), (1, 4)]
    panneaux = []
    # (titre, image, extras)
    def pan(ox, oy, titre, img, extra):
        s = [r"\begin{scope}[shift={(%s,%s)}]" % (f(ox), f(oy)), r"\draw[grille] (0,0) grid (8,5);"]
        s += extra
        s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(p) for p in G))
        s.append(r"\draw[image] %s -- cycle;" % " -- ".join(P(p) for p in img))
        s.append(r"\node[txt,text=otNavy,anchor=north] at (4,-.35) {%s};" % titre)
        s.append(r"\end{scope}")
        return s

    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    s += pan(0, 7.2, "symétrie axiale", [(8 - x, y) for x, y in G],
             [r"\draw[axe] (4,-.3) -- (4,5.3);"])
    s += pan(10, 7.2, "symétrie centrale", [(7 - x, 5 - y) for x, y in G],
             [r"\fill[otNavy] (3.5,2.5) circle (2.2pt);"])
    s += pan(0, 0, "translation", [(x + 4, y) for x, y in G],
             [r"\draw[vect] (1,.5) -- (5,.5);"])
    rot = [(y + 3, 5 - x) for x, y in G]
    s += pan(10, 0, "rotation (quart de tour)", rot,
             [r"\draw[constr] (4,1) -- (2,1) (4,1) -- (4,3);",
              r"\draw[otGreenDark,line width=.6pt] (3.6,1) -- (3.6,1.4) -- (4,1.4);",
              r"\fill[otNavy] (4,1) circle (2.2pt);"])
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["fiche_isometries"] = fiche_isometries()
