# -*- coding: utf-8 -*-
"""Figures de la notion « Symétries et demi-tour » (5e), style des livres.

Compilées par outils/figures_livre.py. Machinerie reprise de la notion 288 (4e,
translations) : constructions sur quadrillage pâle ou sur papier blanc.
Bleu marine = figure de départ, axe, centre et éléments donnés ; vert foncé =
image et traits de construction (corrigés) ; orange = figure à reconnaître (3008).
Les énoncés montrent la figure de départ et l'axe ou le centre, SANS l'image ;
les corrigés ajoutent l'image en vert avec les traits de construction.
Les étiquettes des points sont placées automatiquement dans la direction la
plus éloignée des traits qui partent du point (on peut imposer l'angle).

DONNEES rassemble les coordonnées utilisées : verif_275.py les relit et
recalcule chaque image avec sympy.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  grille/.style={otRule,line width=.4pt,step=1},
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  num/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,inner sep=0pt},
  depart/.style={otNavy,line width=1pt,line join=round,fill=otSky},
  departv/.style={otNavy,line width=1pt,line join=round},
  image/.style={otGreenDark,line width=1pt,line join=round,fill=otGreen!16},
  imagev/.style={otGreenDark,line width=1pt,line join=round},
  repere/.style={otOrange!90!black,line width=1pt,line join=round,fill=otOrange!22},
  constr/.style={otGreenDark,line width=.7pt,dash pattern=on 3pt off 2pt},
  constrb/.style={otNavy!70,line width=.7pt,dash pattern=on 3pt off 2pt},
  axe/.style={otNavy,line width=1.1pt},
  axev/.style={otGreenDark,line width=1.1pt,dash pattern=on 5pt off 2.5pt},
  mat/.style={otNavy,line width=1.8pt},
  matv/.style={otGreenDark,line width=1.8pt},
  lettre/.style={otNavy,line width=3.2pt,line cap=round,line join=round},
  pas/.style={otNavy,line width=.9pt,-{Stealth[length=2.2mm]}},
  pasv/.style={otGreenDark,line width=.9pt,-{Stealth[length=2.2mm]}},
  vect/.style={otGreenDark,line width=1pt,-{Stealth[length=2.4mm]}},
  arc/.style={otGreenDark,line width=.7pt},
}
"""

V = "otGreenDark"
N = "otNavy"
O_ = "otOrange!80!black"


def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def ecart(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


# ------------------------------------------------------------ transformations
def sym_v(p, a):
    """Symétrie d'axe vertical x = a."""
    return (2 * a - p[0], p[1])


def sym_h(p, b):
    """Symétrie d'axe horizontal y = b."""
    return (p[0], 2 * b - p[1])


def sym_diag(p):
    """Symétrie d'axe la diagonale y = x."""
    return (p[1], p[0])


def sym_droite(p, a, b):
    """Symétrie d'axe la droite (ab) quelconque."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    L2 = ux * ux + uy * uy
    t = ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / L2
    h = (a[0] + t * ux, a[1] + t * uy)
    return (2 * h[0] - p[0], 2 * h[1] - p[1])


def pied(p, a, b):
    ux, uy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / (ux * ux + uy * uy)
    return (a[0] + t * ux, a[1] + t * uy)


def demi_tour(p, o):
    return (2 * o[0] - p[0], 2 * o[1] - p[1])


def milieu(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def pol(c, r, ang):
    return (c[0] + r * math.cos(math.radians(ang)), c[1] + r * math.sin(math.radians(ang)))


def inter(a, b, c, d):
    """Intersection des droites (ab) et (cd)."""
    x1, y1 = a
    x2, y2 = b
    x3, y3 = c
    x4, y4 = d
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def tr(pts, v):
    return [(x + v[0], y + v[1]) for x, y in pts]


class Fig:
    """Figure sur quadrillage ou papier blanc : segments mémorisés pour placer les étiquettes."""

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

    def poly(self, pts, style="depart", ferme=True):
        self.corps.append(r"\draw[%s] %s%s;" % (style, " -- ".join(P(p) for p in pts), " -- cycle" if ferme else ""))
        n = len(pts) if ferme else len(pts) - 1
        for i in range(n):
            self.segs.append((pts[i], pts[(i + 1) % len(pts)]))

    def fleche(self, p, q, style="pas"):
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


def angle_droit(F, s, p, q, taille=.3, coul=V):
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


def arc_angle(F, s, p, q, r=.5, coul=N, txt=None, rt=None, n=1):
    """Arc marquant l'angle de sommet s entre [sp) et [sq) (sens direct de p vers q)."""
    a1 = math.degrees(math.atan2(p[1] - s[1], p[0] - s[0]))
    a2 = math.degrees(math.atan2(q[1] - s[1], q[0] - s[0]))
    while a2 < a1:
        a2 += 360
    for k in range(n):
        rr = r + k * .09
        F.brut(r"\draw[%s,line width=.7pt] %s ++(%s:%s) arc (%s:%s:%s);" % (
            coul, P(s), f(a1), f(rr), f(a1), f(a2), f(rr)))
    if txt:
        am = math.radians((a1 + a2) / 2)
        rr = rt if rt is not None else r + .28
        q2 = (s[0] + rr * math.cos(am), s[1] + rr * math.sin(am))
        anc = (math.degrees(am) + 180) % 360
        F.brut(r"\node[txt,text=%s,anchor=%d] at %s {%s};" % (coul, anc, P(q2), txt), haut=True)


def arc_autour(F, c, r, a_mil, ouv=13):
    F.brut(r"\draw[arc] %s ++(%s:%s) arc (%s:%s:%s);" % (P(c), f(a_mil - ouv), f(r), f(a_mil - ouv), f(a_mil + ouv), f(r)))


def direction(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def primes(noms):
    return [n + "'" for n in noms]


def polygone(F, pts, noms, style="depart", coul=N, angs=None):
    F.poly(pts, style)
    for i, p in enumerate(pts):
        n = noms[i] if noms else None
        F.point(p, n, coul, ang=None if angs is None else angs[i])


FIGURES = {}
TOLERE = {}
DONNEES = {}

# =================================================================== cours
# I. symétrie axiale sur quadrillage (axe vertical)
AX_C = {"A": (2, 2), "B": (5, 1), "C": (3, 5)}
AXE_C = 7
AX_C_IM = {k + "'": sym_v(p, AXE_C) for k, p in AX_C.items()}
DONNEES["cours_axiale"] = {"axe x": AXE_C, "depart": AX_C, "image": AX_C_IM}


def cours_axiale():
    F = Fig(.55)
    F.grille(0, 0, 14, 6)
    F.seg((AXE_C, -.35), (AXE_C, 6.35), "axe", memo=False)
    F.texte((AXE_C + .2, 6.25), r"$(d)$", "north west", N)
    A, A2 = AX_C["A"], AX_C_IM["A'"]
    H = (AXE_C, A[1])
    F.seg(A, A2, "constr")
    angle_droit(F, H, A2, (AXE_C, A[1] + 1))
    codage(F, A, H, 2)
    codage(F, H, A2, 2)
    pts = [AX_C[k] for k in "ABC"]
    polygone(F, [AX_C_IM[k + "'"] for k in "ABC"], primes("ABC"), "image", V)
    polygone(F, pts, list("ABC"))
    return F.code()


FIGURES["cours_axiale"] = cours_axiale()

# I. axe en diagonale
DG_C = {"K": (5, 1), "L": (7, 3), "M": (6, 5)}
DG_C_IM = {k + "'": sym_diag(p) for k, p in DG_C.items()}
DONNEES["cours_axiale_diagonale"] = {"axe": "y = x", "depart": DG_C, "image": DG_C_IM}


def cours_axiale_diagonale():
    F = Fig(.55)
    F.grille(0, 0, 8, 8)
    F.seg((-.3, -.3), (8.3, 8.3), "axe", memo=False)
    F.texte((7.6, 8.1), r"$(d)$", "east", N)
    K, K2 = DG_C["K"], DG_C_IM["K'"]
    H = milieu(K, K2)
    F.seg(K, K2, "constr")
    angle_droit(F, H, K2, (H[0] + 1, H[1] + 1))
    codage(F, K, H, 2)
    codage(F, H, K2, 2)
    polygone(F, [DG_C_IM[k + "'"] for k in "KLM"], primes("KLM"), "image", V)
    polygone(F, [DG_C[k] for k in "KLM"], list("KLM"))
    return F.code()


FIGURES["cours_axiale_diagonale"] = cours_axiale_diagonale()

# I. papier blanc : au compas
CMP = {"d1": (0, .4), "d2": (7.4, 3.6), "A": (2.2, 3.6)}
CMP["R"] = (1.05, .4 + 1.05 * 3.2 / 7.4)
CMP["S"] = (5.4, .4 + 5.4 * 3.2 / 7.4)
CMP["A'"] = sym_droite(CMP["A"], CMP["d1"], CMP["d2"])
DONNEES["cours_axiale_compas"] = CMP


def cours_axiale_compas():
    F = Fig(.75)
    a, b = CMP["d1"], CMP["d2"]
    F.seg(a, b, "axe", memo=False)
    F.texte((b[0] + .1, b[1] - .05), r"$(d)$", "west", N)
    A, A2, R, S = CMP["A"], CMP["A'"], CMP["R"], CMP["S"]
    for c in (R, S):
        r = dist(c, A)
        arc_autour(F, c, r, direction(c, A2), 9 if c is R else 7)
        arc_autour(F, c, r, direction(c, A), 6 if c is R else 5)
    F.seg(R, A, "constrb,dash pattern=on 1.5pt off 2pt")
    F.seg(S, A, "constrb,dash pattern=on 1.5pt off 2pt")
    F.seg(R, A2, "constr,dash pattern=on 1.5pt off 2pt")
    F.seg(S, A2, "constr,dash pattern=on 1.5pt off 2pt")
    F.point(R, "R", ang=290)
    F.point(S, "S", ang=290)
    F.point(A, "A", ang=110)
    F.point(A2, "A'", V, ang=280)
    return F.code()


FIGURES["cours_axiale_compas"] = cours_axiale_compas()

# II. demi-tour : définition
DT_C = {"A": (0, 0), "O": (2.6, 1.3)}
DT_C["A'"] = demi_tour(DT_C["A"], DT_C["O"])
DONNEES["cours_demitour_point"] = DT_C


def cours_demitour_point():
    F = Fig(.8)
    A, O, A2 = DT_C["A"], DT_C["O"], DT_C["A'"]
    r = dist(O, A)
    a0 = direction(O, A)
    # demi-cercle parcouru par A autour de O
    F.brut(r"\draw[otGreenDark,line width=.8pt,dash pattern=on 3pt off 2pt,-{Stealth[length=2.4mm]}] %s ++(%s:%s) arc (%s:%s:%s);" % (
        P(O), f(a0), f(r), f(a0), f(a0 - 180 + 4), f(r)))
    F.seg(A, A2, "geoTrait")
    codage(F, A, O, 1, N)
    codage(F, O, A2, 1, N)
    F.texte((O[0], O[1] + r + .2), r"demi-tour", "south", V, "txt")
    F.point(A, "A", ang=200)
    F.point(O, "O", ang=120)
    F.point(A2, "A'", V, ang=20)
    return F.code()


FIGURES["cours_demitour_point"] = cours_demitour_point()

# II. demi-tour sur quadrillage
DQ_C = {"A": (1, 5), "B": (4, 6), "C": (2, 8)}
O_DQ = (6, 4)
DQ_C_IM = {k + "'": demi_tour(p, O_DQ) for k, p in DQ_C.items()}
DONNEES["cours_demitour_quadrillage"] = {"O": O_DQ, "depart": DQ_C, "image": DQ_C_IM}


def cours_demitour_quadrillage():
    F = Fig(.55)
    F.grille(0, 0, 12, 8)
    A, A2 = DQ_C["A"], DQ_C_IM["A'"]
    # chemin de A à O, puis le même chemin à partir de O
    c1 = (O_DQ[0], A[1])
    c2 = (A2[0], O_DQ[1])
    F.fleche(A, c1, "pas")
    F.fleche(c1, O_DQ, "pas")
    F.fleche(O_DQ, c2, "pasv")
    F.fleche(c2, A2, "pasv")
    F.texte((milieu(A, c1)[0], A[1] - .15), r"5", "north", N, "num")
    F.texte((c1[0] + .15, (c1[1] + O_DQ[1]) / 2), r"1", "west", N, "num")
    F.texte(milieu(O_DQ, c2), r"5", "north", V, "num")
    F.texte((c2[0] + .15, (c2[1] + A2[1]) / 2), r"1", "west", V, "num")
    polygone(F, [DQ_C_IM[k + "'"] for k in "ABC"], primes("ABC"), "image", V,
             angs=[0, None, 270])
    polygone(F, [DQ_C[k] for k in "ABC"], list("ABC"), angs=[180, 0, 90])
    F.point(O_DQ, "O", ang=225)
    return F.code()


FIGURES["cours_demitour_quadrillage"] = cours_demitour_quadrillage()

# II. papier blanc : règle et compas
DC_C = {"A": (0, 2.2), "O": (3, 1.2)}
DC_C["A'"] = demi_tour(DC_C["A"], DC_C["O"])
DONNEES["cours_demitour_compas"] = DC_C


def cours_demitour_compas():
    F = Fig(.8)
    A, O, A2 = DC_C["A"], DC_C["O"], DC_C["A'"]
    u = ((A2[0] - A[0]) / dist(A, A2), (A2[1] - A[1]) / dist(A, A2))
    F.seg((A[0] - .5 * u[0], A[1] - .5 * u[1]), (A2[0] + .9 * u[0], A2[1] + .9 * u[1]), "geoTrait,line width=.7pt")
    arc_autour(F, O, dist(O, A), direction(O, A2), 9)
    arc_autour(F, O, dist(O, A), direction(O, A), 7)
    codage(F, A, O, 1, N)
    codage(F, O, A2, 1, V)
    F.point(A, "A", ang=110)
    F.point(O, "O", ang=105)
    F.point(A2, "A'", V, ang=297)
    return F.code()


FIGURES["cours_demitour_compas"] = cours_demitour_compas()

# III. image d'une droite par demi-tour
DR_C = {"A": (0, 3.2), "B": (3.2, 4.4), "O": (4, 2.2)}
DR_C["A'"] = demi_tour(DR_C["A"], DR_C["O"])
DR_C["B'"] = demi_tour(DR_C["B"], DR_C["O"])
DONNEES["cours_droites"] = DR_C


def cours_droites():
    F = Fig(.66)
    A, B, O, A2, B2 = (DR_C[k] for k in ("A", "B", "O", "A'", "B'"))
    u = ((B[0] - A[0]) / dist(A, B), (B[1] - A[1]) / dist(A, B))
    F.seg((A[0] - 1.2 * u[0], A[1] - 1.2 * u[1]), (B[0] + 1.6 * u[0], B[1] + 1.6 * u[1]), "geoTrait", memo=False)
    F.seg((B2[0] - 1.6 * u[0], B2[1] - 1.6 * u[1]), (A2[0] + 1.2 * u[0], A2[1] + 1.2 * u[1]), "geoReponse", memo=False)
    e = (B[0] + 1.6 * u[0], B[1] + 1.6 * u[1])
    F.texte((e[0] - .05, e[1] + .25), r"$(\Delta)$", "south east", N)
    e2 = (A2[0] + 1.2 * u[0], A2[1] + 1.2 * u[1])
    F.texte((e2[0] + .05, e2[1] - .25), r"$(\Delta')$", "north west", V)
    F.seg(A, A2, "constr")
    F.seg(B, B2, "constr")
    codage(F, A, O, 1)
    codage(F, O, A2, 1)
    codage(F, B, O, 2)
    codage(F, O, B2, 2)
    F.point(A, "A", ang=120)
    F.point(B, "B", ang=110)
    F.point(O, "O", ang=228)
    F.point(A2, "A'", V, ang=300)
    F.point(B2, "B'", V, ang=290)
    return F.code()


FIGURES["cours_droites"] = cours_droites()


# IV. axes et centres de figures usuelles
def cours_centres():
    U = .6
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    W, H = 4.4, 3.9
    cell = {}

    def centre_pt(c):
        s.append(r"\fill[otGreenDark] %s circle (2.6pt);" % P(c))

    def ax(p, q):
        s.append(r"\draw[axev] %s -- %s;" % (P(p), P(q)))

    def nom(c, t, l2=None):
        s.append(r"\node[txt,text=otNavy,anchor=north,align=center] at %s {%s};" % (P((c[0], c[1] - 1.45)), t.replace(" ", r"\\")))

    for i, n in enumerate(["rectangle", "carré", "losange", "parallélogramme", "triangle équilatéral", "cercle"]):
        cell[n] = ((i % 3) * W, (1 - i // 3) * H + .3)
    # rectangle
    c = cell["rectangle"]
    w, h = 1.6, .9
    s.append(r"\draw[depart] %s rectangle %s;" % (P((c[0] - w, c[1] - h)), P((c[0] + w, c[1] + h))))
    ax((c[0], c[1] - h - .35), (c[0], c[1] + h + .35))
    ax((c[0] - w - .35, c[1]), (c[0] + w + .35, c[1]))
    centre_pt(c)
    nom(c, "rectangle")
    # carré
    c = cell["carré"]
    a = 1.0
    s.append(r"\draw[depart] %s rectangle %s;" % (P((c[0] - a, c[1] - a)), P((c[0] + a, c[1] + a))))
    ax((c[0], c[1] - a - .3), (c[0], c[1] + a + .3))
    ax((c[0] - a - .3, c[1]), (c[0] + a + .3, c[1]))
    ax((c[0] - a - .25, c[1] - a - .25), (c[0] + a + .25, c[1] + a + .25))
    ax((c[0] - a - .25, c[1] + a + .25), (c[0] + a + .25, c[1] - a - .25))
    centre_pt(c)
    nom(c, "carré")
    # losange
    c = cell["losange"]
    dx, dy = 1.6, 1.0
    s.append(r"\draw[depart] %s -- %s -- %s -- %s -- cycle;" % (
        P((c[0] - dx, c[1])), P((c[0], c[1] - dy)), P((c[0] + dx, c[1])), P((c[0], c[1] + dy))))
    ax((c[0] - dx - .35, c[1]), (c[0] + dx + .35, c[1]))
    ax((c[0], c[1] - dy - .35), (c[0], c[1] + dy + .35))
    centre_pt(c)
    nom(c, "losange")
    # parallélogramme
    c = cell["parallélogramme"]
    pts = [(c[0] - 1.65, c[1] - .9), (c[0] + .9, c[1] - .9), (c[0] + 1.65, c[1] + .9), (c[0] - .9, c[1] + .9)]
    s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(p) for p in pts))
    s.append(r"\draw[constr] %s -- %s %s -- %s;" % (P(pts[0]), P(pts[2]), P(pts[1]), P(pts[3])))
    centre_pt(c)
    nom(c, "parallélogramme")
    # triangle équilatéral
    c = cell["triangle équilatéral"]
    r = 1.15
    cc = (c[0], c[1] - .1)
    tri = [pol(cc, r, 90), pol(cc, r, 210), pol(cc, r, 330)]
    s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(p) for p in tri))
    for k in range(3):
        p = tri[k]
        m = milieu(tri[(k + 1) % 3], tri[(k + 2) % 3])
        L = dist(p, m)
        u = ((m[0] - p[0]) / L, (m[1] - p[1]) / L)
        ax((p[0] - .3 * u[0], p[1] - .3 * u[1]), (m[0] + .3 * u[0], m[1] + .3 * u[1]))
    nom(c, "triangle équilatéral")
    # cercle
    c = cell["cercle"]
    r = 1.0
    s.append(r"\draw[depart] %s circle (%s);" % (P(c), f(r)))
    for ang in (90, 30, 150):
        ax(pol(c, r + .3, ang), pol(c, r + .3, ang + 180))
    centre_pt(c)
    nom(c, "cercle")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_centres"] = cours_centres()

# V. comparer les deux symétries (drapeau)
DRAP = {"A": (1, 1), "B": (1, 5), "C": (3, 4), "D": (1, 3)}
AXE_CMP = 4
O_CMP = (4, 3)
DONNEES["cours_comparer"] = {
    "depart": DRAP, "axe x": AXE_CMP, "O": O_CMP,
    "axiale": {k: sym_v(p, AXE_CMP) for k, p in DRAP.items()},
    "demi-tour": {k: demi_tour(p, O_CMP) for k, p in DRAP.items()},
}


def drapeau(s, d, mat, fanion):
    s.append(r"\draw[%s] %s -- cycle;" % (fanion, " -- ".join(P(d[k]) for k in "BCD")))
    s.append(r"\draw[%s] %s -- %s;" % (mat, P(d["A"]), P(d["B"])))


def cours_comparer():
    U = .42
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    for ox, titre, l2, img, extra in (
            (0, "symétrie d'axe $(d)$", "la figure est retournée",
             {k: sym_v(p, AXE_CMP) for k, p in DRAP.items()},
             [r"\draw[axe] (4,-.35) -- (4,6.35);", r"\node[lab,text=otNavy,anchor=north west] at (4.15,6.3) {$(d)$};"]),
            (9.6, "demi-tour de centre $O$", "la figure a tourné de 180°",
             {k: demi_tour(p, O_CMP) for k, p in DRAP.items()},
             [r"\fill[otNavy] (4,3) circle (2.4pt);", r"\node[lab,text=otNavy,anchor=north] at (4,2.75) {$O$};"])):
        s.append(r"\begin{scope}[shift={(%s,0)}]" % f(ox))
        s.append(r"\draw[grille] (0,0) grid (8,6);")
        s.extend(extra[:1])
        drapeau(s, DRAP, "mat", "depart")
        drapeau(s, img, "matv", "image")
        s.extend(extra[1:])
        s.append(r"\node[txt,text=otNavy,anchor=north] at (4,-.55) {%s};" % titre)
        s.append(r"\node[txt,text=otMuted,anchor=north] at (4,-1.45) {%s};" % l2)
        s.append(r"\end{scope}")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_comparer"] = cours_comparer()

# =================================================================== 3000 axial sur quadrillage
E3000a = {"A": (1, 1), "B": (3, 1), "C": (3, 4), "D": (1, 5)}
AXE3000a = 4
E3000b = {"E": (1, 5), "F": (6, 6), "G": (3, 7)}
AXE3000b = 4
E3000c = {"K": (5, 1), "L": (7, 3), "M": (4, 4)}
DONNEES["ex3000"] = {
    "a": {"axe x": AXE3000a, "depart": E3000a, "image": {k: sym_v(p, AXE3000a) for k, p in E3000a.items()}},
    "b": {"axe y": AXE3000b, "depart": E3000b, "image": {k: sym_h(p, AXE3000b) for k, p in E3000b.items()}},
    "c": {"axe": "y = x", "depart": E3000c, "image": {k: sym_diag(p) for k, p in E3000c.items()}},
}


def ex3000a(corrige):
    F = Fig(.55)
    F.grille(0, 0, 8, 6)
    F.seg((AXE3000a, -.35), (AXE3000a, 6.35), "axe", memo=False)
    F.texte((AXE3000a + .2, 6.25), r"$(d_1)$", "north west", N)
    noms = "ABCD"
    if corrige:
        D, D2 = E3000a["D"], sym_v(E3000a["D"], AXE3000a)
        H = (AXE3000a, D[1])
        F.seg(D, D2, "constr")
        angle_droit(F, H, D2, (AXE3000a, D[1] - 1))
        codage(F, D, H, 3)
        codage(F, H, D2, 3)
        polygone(F, [sym_v(E3000a[k], AXE3000a) for k in noms], primes(noms), "image", V)
    polygone(F, [E3000a[k] for k in noms], list(noms))
    return F.code()


def ex3000b(corrige):
    F = Fig(.55)
    F.grille(0, 0, 8, 8)
    F.seg((-.35, AXE3000b), (8.35, AXE3000b), "axe", memo=False)
    F.texte((8.45, AXE3000b), r"$(d_2)$", "west", N)
    noms = "EFG"
    if corrige:
        Fp, F2 = E3000b["F"], sym_h(E3000b["F"], AXE3000b)
        H = (Fp[0], AXE3000b)
        F.seg(Fp, F2, "constr")
        angle_droit(F, H, F2, (Fp[0] + 1, AXE3000b))
        codage(F, Fp, H, 2)
        codage(F, H, F2, 2)
        polygone(F, [sym_h(E3000b[k], AXE3000b) for k in noms], primes(noms), "image", V)
    polygone(F, [E3000b[k] for k in noms], list(noms))
    return F.code()


def ex3000c(corrige):
    F = Fig(.55)
    F.grille(0, 0, 8, 8)
    F.seg((-.3, -.3), (8.3, 8.3), "axe", memo=False)
    F.texte((7.6, 8.1), r"$(d_3)$", "east", N)
    noms = "KLM"
    if corrige:
        K, K2 = E3000c["K"], sym_diag(E3000c["K"])
        H = milieu(K, K2)
        F.seg(K, K2, "constr")
        angle_droit(F, H, K2, (H[0] + 1, H[1] + 1))
        codage(F, K, H, 2)
        codage(F, H, K2, 2)
        img = [sym_diag(E3000c[k]) for k in noms]
        F.poly(img, "image")
        F.point(img[0], "K'", V)
        F.point(img[1], "L'", V)
    polygone(F, [E3000c[k] for k in noms], list(noms), angs=[None, None, 257])
    return F.code()


for _c in (False, True):
    _s = "corrige" if _c else "enonce"
    FIGURES["ex3000a_" + _s] = ex3000a(_c)
    FIGURES["ex3000b_" + _s] = ex3000b(_c)
    FIGURES["ex3000c_" + _s] = ex3000c(_c)

# =================================================================== 2999 symétrique d'un point par demi-tour
O2999 = (5, 4)
P2999 = {"A": (1, 6), "B": (7, 7), "C": (2, 7)}
G2999 = (9, 5)
H2999 = demi_tour(G2999, O2999)
DONNEES["ex2999"] = {"O": O2999, "depart": P2999,
                     "image": {k + "'": demi_tour(p, O2999) for k, p in P2999.items()},
                     "G": G2999, "H": H2999}


def ex2999(corrige):
    F = Fig(.6)
    F.grille(0, 0, 10, 8)
    if corrige:
        A, A2 = P2999["A"], demi_tour(P2999["A"], O2999)
        c1 = (O2999[0], A[1])
        c2 = (A2[0], O2999[1])
        F.fleche(A, c1, "pas")
        F.fleche(c1, O2999, "pas")
        F.fleche(O2999, c2, "pasv")
        F.fleche(c2, A2, "pasv")
        F.texte((4.1, A[1] + .15), r"4", "south", N, "num")
        F.texte((c1[0] - .15, (c1[1] + O2999[1]) / 2), r"2", "east", N, "num")
        F.texte((7, O2999[1] - .15), r"4", "north", V, "num")
        F.texte((c2[0] - .15, (c2[1] + A2[1]) / 2), r"2", "east", V, "num")
        for k in "BC":
            F.seg(P2999[k], demi_tour(P2999[k], O2999), "constr")
        F.seg(G2999, H2999, "constr")
        for k in "ABC":
            F.point(demi_tour(P2999[k], O2999), k + "'", V)
        F.point(H2999, "H", V)
    for k in "ABC":
        F.point(P2999[k], k)
    F.point(G2999, "G")
    F.point(O2999, "O", ang=None if corrige else 270)
    return F.code()


FIGURES["ex2999_enonce"] = ex2999(False)
FIGURES["ex2999_corrige"] = ex2999(True)

# =================================================================== 3006 drapeau par demi-tour
O3006 = (6, 4)
D3006 = {"A": (2, 2), "B": (2, 7), "C": (5, 6), "D": (2, 5)}
D3006_IM = {k + "'": demi_tour(p, O3006) for k, p in D3006.items()}
DONNEES["ex3006"] = {"O": O3006, "depart": D3006, "image": D3006_IM}


def ex3006(corrige):
    F = Fig(.55)
    F.grille(0, 0, 12, 8)
    d = D3006
    if corrige:
        for k, n in (("A", 1), ("C", 2)):
            p, q = d[k], D3006_IM[k + "'"]
            F.seg(p, q, "constr")
            codage(F, p, O3006, n)
            codage(F, O3006, q, n)
        im = D3006_IM
        F.poly([im["B'"], im["C'"], im["D'"]], "image")
        F.seg(im["A'"], im["B'"], "matv")
        for k in "ABCD":
            F.point(im[k + "'"], k + "'", V)
    F.poly([d["B"], d["C"], d["D"]], "depart")
    F.seg(d["A"], d["B"], "mat")
    for k in "ABCD":
        F.point(d[k], k)
    F.point(O3006, "O")
    return F.code()


FIGURES["ex3006_enonce"] = ex3006(False)
FIGURES["ex3006_corrige"] = ex3006(True)

# =================================================================== 3003 axiale sur papier blanc
B3003 = (0.0, 0.0)
A3003 = pol(B3003, 4, 100)
C3003 = pol(B3003, 3, 40)
D1_3003 = (3.7, -1.0)
D2_3003 = (5.0, 5.6)
R3003 = (D1_3003[0] + .2 * (D2_3003[0] - D1_3003[0]), D1_3003[1] + .2 * (D2_3003[1] - D1_3003[1]))
S3003 = (D1_3003[0] + .92 * (D2_3003[0] - D1_3003[0]), D1_3003[1] + .92 * (D2_3003[1] - D1_3003[1]))
I3003 = inter(B3003, C3003, D1_3003, D2_3003)
IM3003 = {k + "'": sym_droite(p, D1_3003, D2_3003) for k, p in (("A", A3003), ("B", B3003), ("C", C3003))}
DONNEES["ex3003"] = {"A": A3003, "B": B3003, "C": C3003, "axe": (D1_3003, D2_3003), "R": R3003, "S": S3003,
                     "I": I3003, "image": IM3003}


def ex3003(corrige):
    F = Fig(.62)
    A, B, C = A3003, B3003, C3003
    a, b = D1_3003, D2_3003
    F.seg(a, b, "axe", memo=False)
    F.texte((b[0] - .05, b[1] + .1), r"$(d)$", "south", N)
    if corrige:
        A2, B2, C2 = IM3003["A'"], IM3003["B'"], IM3003["C'"]
        # A' : équerre
        H = pied(A, a, b)
        F.seg(A, A2, "constr")
        angle_droit(F, H, A2, b)
        codage(F, A, H, 1)
        codage(F, H, A2, 1)
        # B' : compas (centres R et S sur l'axe)
        for c, o1, o2 in ((R3003, 7, 5), (S3003, 4, 3)):
            r = dist(c, B)
            arc_autour(F, c, r, direction(c, B2), o1)
            arc_autour(F, c, r, direction(c, B), o2)
        F.point(R3003, "R", ang=170)
        F.point(S3003, "S", ang=170)
        # C' : équerre
        H2 = pied(C, a, b)
        F.seg(C, C2, "constr")
        angle_droit(F, H2, C2, b)
        codage(F, C, H2, 2)
        codage(F, H2, C2, 2)
        # droites (BC) et (B'C') jusqu'à I
        F.seg(C, I3003, "constrb", memo=True)
        F.seg(C2, I3003, "constr", memo=True)
        F.poly([A2, B2, C2], "imagev")
        for n, p, an in (("A'", A2, None), ("B'", B2, 0), ("C'", C2, 270)):
            F.point(p, n, V, ang=an)
        F.point(I3003, "I", ang=145)
    F.poly([A, B, C], "departv")
    arc_angle(F, B, C, A, .55, N, r"$60^\circ$", .95)
    F.point(A, "A")
    F.point(B, "B", ang=200)
    F.point(C, "C")
    return F.code()


FIGURES["ex3003_enonce"] = ex3003(False)
FIGURES["ex3003_corrige"] = ex3003(True)

# =================================================================== 3001 demi-tour sur papier blanc
F3001 = (1.0, 0.6)
E3001 = pol(F3001, 3.5, 110)
G3001 = pol(F3001, 2.5, 40)
O3001 = (0.35, -1.8)
K3001 = (-3.0, 1.0)
R3001 = 1.5
IM3001 = {k + "'": demi_tour(p, O3001) for k, p in (("E", E3001), ("F", F3001), ("G", G3001), ("K", K3001))}
DONNEES["ex3001"] = {"E": E3001, "F": F3001, "G": G3001, "O": O3001, "K": K3001, "rayon": R3001, "image": IM3001}


def ex3001(corrige):
    F = Fig(.5)
    E, Fp, G, O, K = E3001, F3001, G3001, O3001, K3001
    if corrige:
        im = IM3001
        for k, n in (("E", 1), ("F", 2), ("G", 0), ("K", 0)):
            p = {"E": E, "F": Fp, "G": G, "K": K}[k]
            q = im[k + "'"]
            F.seg(p, q, "constr")
            if n:
                codage(F, p, O, n)
                codage(F, O, q, n)
        arc_autour(F, O, dist(O, E), direction(O, im["E'"]), 6)
        F.brut(r"\draw[otGreenDark,line width=1pt] %s circle (%s);" % (P(im["K'"]), f(R3001)))
        F.poly([im["E'"], im["F'"], im["G'"]], "imagev")
        for k, an in (("E", None), ("F", 110), ("G", None)):
            F.point(im[k + "'"], k + "'", V, ang=an)
        F.point(im["K'"], "K'", V)
    F.brut(r"\draw[otNavy,line width=1pt] %s circle (%s);" % (P(K), f(R3001)))
    F.poly([E, Fp, G], "departv")
    arc_angle(F, Fp, G, E, .7, N, r"$70^\circ$", 1.15)
    F.point(E, "E")
    F.point(Fp, "F", ang=182)
    F.point(G, "G")
    F.point(K, "K", ang=None)
    F.texte(pol(K, R3001 + .15, 225), r"$(\mathscr{C})$", "north east", N)
    F.point(O, "O")
    return F.code()


FIGURES["ex3001_enonce"] = ex3001(False)
FIGURES["ex3001_corrige"] = ex3001(True)

# =================================================================== 3008 axiale ou demi-tour ?
L0 = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 3), (0, 3)]
PAN3008 = {
    1: {"type": "axiale", "axe x": 4, "bleu": tr(L0, (1, 2))},
    2: {"type": "demi-tour", "O": (4, 3), "bleu": tr(L0, (1, 1))},
    3: {"type": "axiale", "axe": "y = x", "bleu": tr(L0, (4, 0))},
    4: {"type": "aucune", "vecteur": (4, 2), "bleu": tr(L0, (1, 1))},
}
for _k, _p in PAN3008.items():
    if _k == 1:
        _p["orange"] = [sym_v(q, 4) for q in _p["bleu"]]
    elif _k == 2:
        _p["orange"] = [demi_tour(q, _p["O"]) for q in _p["bleu"]]
    elif _k == 3:
        _p["orange"] = [sym_diag(q) for q in _p["bleu"]]
    else:
        _p["orange"] = tr(_p["bleu"], _p["vecteur"])
DONNEES["ex3008"] = PAN3008


def ex3008(corrige):
    U = .42
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    pos = {1: (0, 10.4), 2: (9.4, 10.4), 3: (0, 0), 4: (9.4, 0)}
    for k in (1, 2, 3, 4):
        p = PAN3008[k]
        s.append(r"\begin{scope}[shift={%s}]" % P(pos[k]))
        s.append(r"\draw[grille] (0,0) grid (7,7);")
        s.append(r"\draw[depart] %s -- cycle;" % " -- ".join(P(q) for q in p["bleu"]))
        s.append(r"\draw[%s] %s -- cycle;" % ("image" if corrige else "repere", " -- ".join(P(q) for q in p["orange"])))
        if corrige:
            if k == 1:
                s.append(r"\draw[axev] (4,-.35) -- (4,7.35);")
            elif k == 3:
                s.append(r"\draw[axev] (-.3,-.3) -- (7.3,7.3);")
            elif k == 2:
                O = p["O"]
                for i in (0, 4):
                    a, b = p["bleu"][i], p["orange"][i]
                    s.append(r"\draw[constr] %s -- %s;" % (P(a), P(b)))
                s.append(r"\fill[otGreenDark] %s circle (2.6pt);" % P(O))
                s.append(r"\node[lab,text=otGreenDark,anchor=south] at %s {$O$};" % P((O[0] + .1, O[1] + .35)))
            else:
                for i in (0, 4):
                    a, b = p["bleu"][i], p["orange"][i]
                    s.append(r"\draw[vect] %s -- %s;" % (P(a), P(b)))
        s.append(r"\node[txt,text=otNavy,anchor=north] at (3.5,-.45) {figure %d};" % k)
        if corrige:
            l2 = {1: "symétrie axiale", 2: "demi-tour", 3: "symétrie axiale", 4: "ni l'une ni l'autre"}[k]
            s.append(r"\node[txt,text=otGreenDark,anchor=north] at (3.5,-1.45) {%s};" % l2)
        s.append(r"\end{scope}")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3008_enonce"] = ex3008(False)
FIGURES["ex3008_corrige"] = ex3008(True)

# =================================================================== 3005 propriétés du demi-tour
A3005 = (0.0, 0.0)
B3005 = pol(A3005, 6, 15)
C3005 = pol(A3005, 4, 105)
M3005 = pol(A3005, 2, 15)
O3005 = (7.0, 4.2)
IM3005 = {k + "'": demi_tour(p, O3005) for k, p in (("A", A3005), ("B", B3005), ("C", C3005), ("M", M3005))}
DONNEES["ex3005"] = {"A": A3005, "B": B3005, "C": C3005, "M": M3005, "O": O3005, "image": IM3005}


def cote_ext(F, p, q, txt, d=.6, coul=N, gauche=False):
    """Flèche de cote parallèle à [pq], décalée de d (côté gauche ou droit du sens p→q)."""
    L = dist(p, q)
    nx, ny = -(q[1] - p[1]) / L, (q[0] - p[0]) / L
    if not gauche:
        nx, ny = -nx, -ny
    a = (p[0] + d * nx, p[1] + d * ny)
    b = (q[0] + d * nx, q[1] + d * ny)
    F.brut(r"\draw[%s,line width=.55pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] %s -- %s;" % (coul, P(a), P(b)))
    m = ((a[0] + b[0]) / 2 + .22 * nx, (a[1] + b[1]) / 2 + .22 * ny)
    ang = math.degrees(math.atan2(ny, nx))
    F.brut(r"\node[txt,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(m), txt), haut=True)
    F.brut(r"\draw[%s!60,line width=.4pt] %s -- %s %s -- %s;" % (
        coul, P(p), P((p[0] + (d + .15) * nx, p[1] + (d + .15) * ny)), P(q), P((q[0] + (d + .15) * nx, q[1] + (d + .15) * ny))))


def ex3005(corrige):
    F = Fig(.4)
    A, B, C, M, O = A3005, B3005, C3005, M3005, O3005
    if corrige:
        im = IM3005
        A2, B2, C2, M2 = im["A'"], im["B'"], im["C'"], im["M'"]
        F.seg(B, B2, "constr")
        codage(F, B, O, 1)
        codage(F, O, B2, 1)
        F.poly([A2, B2, C2], "imagev")
        angle_droit(F, A2, B2, C2, .45)
        cote_ext(F, A2, B2, r"6 cm", .75, V, False)
        etiq_cote(F, A2, C2, r"4 cm", .3, V, True)
        F.point(A2, "A'", V, ang=15)
        F.point(B2, "B'", V, ang=175)
        F.point(C2, "C'", V)
        F.point(M2, "M'", V, ang=285)
    F.poly([A, B, C], "departv")
    angle_droit(F, A, B, C, .45, N)
    cote_ext(F, A, B, r"6 cm", .75, N, False)
    etiq_cote(F, A, C, r"4 cm", .3, N, True)
    F.point(A, "A", ang=195)
    F.point(B, "B", ang=355)
    F.point(C, "C")
    F.point(M, "M", ang=105)
    F.point(O, "O")
    return F.code()


FIGURES["ex3005_enonce"] = ex3005(False)
FIGURES["ex3005_corrige"] = ex3005(True)

# =================================================================== 3015 axes et centres de symétrie
LW, LH = 1.6, 2.2
LETTRES = {
    "H": [[(0, 0), (0, LH)], [(LW, 0), (LW, LH)], [(0, LH / 2), (LW, LH / 2)]],
    "N": [[(0, 0), (0, LH), (LW, 0), (LW, LH)]],
    "E": [[(LW, 0), (0, 0), (0, LH), (LW, LH)], [(0, LH / 2), (LW * .8, LH / 2)]],
    "X": [[(0, 0), (LW, LH)], [(0, LH), (LW, 0)]],
    "T": [[(0, LH), (LW, LH)], [(LW / 2, LH), (LW / 2, 0)]],
    "Z": [[(0, LH), (LW, LH), (0, 0), (LW, 0)]],
}
# axes de chaque lettre ("v" vertical, "h" horizontal) et centre (True/False)
SYM_LETTRES = {"H": ("vh", True), "N": ("", True), "E": ("h", False), "X": ("vh", True),
               "T": ("v", False), "Z": ("", True)}
DONNEES["ex3015_lettres"] = {"lettres": LETTRES, "symetries": SYM_LETTRES}


def ex3015_lettres(corrige):
    U = .62
    s = [r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round,line join=round]" % (U, U)]
    ordre = "HNEXTZ"
    for i, l in enumerate(ordre):
        ox, oy = (i % 3) * 3.6, (1 - i // 3) * 4.0
        s.append(r"\begin{scope}[shift={(%s,%s)}]" % (f(ox), f(oy)))
        for tr_ in LETTRES[l]:
            s.append(r"\draw[lettre] %s;" % " -- ".join(P(p) for p in tr_))
        if corrige:
            axes, centre = SYM_LETTRES[l]
            if "v" in axes:
                s.append(r"\draw[axev] (%s,-.5) -- (%s,%s);" % (f(LW / 2), f(LW / 2), f(LH + .5)))
            if "h" in axes:
                s.append(r"\draw[axev] (-.5,%s) -- (%s,%s);" % (f(LH / 2), f(LW + .5), f(LH / 2)))
            if centre:
                s.append(r"\draw[otGreenDark,fill=white,line width=1.2pt] (%s,%s) circle (3.4pt);" % (f(LW / 2), f(LH / 2)))
                s.append(r"\fill[otGreenDark] (%s,%s) circle (1.6pt);" % (f(LW / 2), f(LH / 2)))
        s.append(r"\end{scope}")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3015_lettres_enonce"] = ex3015_lettres(False)
FIGURES["ex3015_lettres_corrige"] = ex3015_lettres(True)

O3015 = (5, 4)
Q3015 = [(1, 1), (5, 1), (5, 2), (2, 2), (2, 6), (1, 6)]
T3015 = [(3, 3), (4, 3), (3, 4)]
DONNEES["ex3015_completer"] = {"O": O3015, "bleu": [Q3015, T3015],
                               "image": [[demi_tour(p, O3015) for p in Q3015], [demi_tour(p, O3015) for p in T3015]]}


def ex3015_completer(corrige):
    F = Fig(.55)
    F.grille(0, 0, 10, 8)
    if corrige:
        img = [demi_tour(p, O3015) for p in Q3015]
        imt = [demi_tour(p, O3015) for p in T3015]
        F.seg(Q3015[4], img[4], "constr")
        codage(F, Q3015[4], O3015, 2)
        codage(F, O3015, img[4], 2)
        F.poly(img, "image")
        F.poly(imt, "image")
    F.poly(Q3015, "depart")
    F.poly(T3015, "depart")
    F.point(O3015, "O", ang=None if corrige else 30)
    return F.code()


FIGURES["ex3015_completer_enonce"] = ex3015_completer(False)
FIGURES["ex3015_completer_corrige"] = ex3015_completer(True)

# =================================================================== 3012 comparer les deux symétries
F3012 = {"A": (1, 6), "B": (4, 6), "C": (4, 7), "D": (2, 9), "E": (1, 9)}
AXE3012 = 6
O3012 = (7, 5)
F1_3012 = {k: sym_v(p, AXE3012) for k, p in F3012.items()}
F2_3012 = {k: demi_tour(p, O3012) for k, p in F3012.items()}
DONNEES["ex3012"] = {"F": F3012, "axe x": AXE3012, "O": O3012, "F1": F1_3012, "F2": F2_3012}


def ex3012(corrige):
    F = Fig(.5)
    F.grille(0, 0, 14, 10)
    F.seg((AXE3012, -.35), (AXE3012, 10.35), "axe", memo=False)
    F.texte((AXE3012 - .2, 10.25), r"$(d)$", "north east", N)
    noms = "ABCDE"
    if corrige:
        C, C1, C2 = F3012["C"], F1_3012["C"], F2_3012["C"]
        Hc = (AXE3012, C[1])
        F.seg(C, C1, "constr")
        angle_droit(F, Hc, C1, (AXE3012, C[1] + 1))
        codage(F, C, Hc, 2)
        codage(F, Hc, C1, 2)
        F.seg(C, C2, "constr")
        codage(F, C, O3012, 1)
        codage(F, O3012, C2, 1)
        F.poly([F1_3012[k] for k in noms], "image")
        F.poly([F2_3012[k] for k in noms], "image")
        F.seg(F1_3012["C"], F1_3012["D"], "otGreenDark,line width=2pt")
        F.seg(F2_3012["C"], F2_3012["D"], "otGreenDark,line width=2pt")
        F.point(C1, "C_1", V)
        F.point(F1_3012["D"], "D_1", V)
        F.point(C2, "C_2", V)
        F.point(F2_3012["D"], "D_2", V)
        F.texte((10.5, 7.5), r"$F_1$", "center", V)
        F.texte((11.5, 2.5), r"$F_2$", "center", V)
    F.poly([F3012[k] for k in noms], "depart")
    F.seg(F3012["C"], F3012["D"], "otNavy,line width=2pt")
    for k in noms:
        F.point(F3012[k], k)
    F.texte((2.2, 7.1), r"$F$", "center", N)
    F.point(O3012, "O", ang=None if corrige else 270)
    return F.code()


FIGURES["ex3012_enonce"] = ex3012(False)
FIGURES["ex3012_corrige"] = ex3012(True)

# =================================================================== 3019 carreau de la terrasse
T3019_TRI = [(1, 5), (3, 5), (1, 7)]
T3019_CAR = [(2, 7), (3, 7), (3, 8), (2, 8)]
AXE3019 = 4
O3019 = (4, 4)


def etape1(pts):
    return [sym_v(p, AXE3019) for p in pts]


def etape2(pts):
    return [demi_tour(p, O3019) for p in pts]


T3019_HAUT = [T3019_TRI, T3019_CAR, etape1(T3019_TRI), etape1(T3019_CAR)]
T3019_BAS = [etape2(m) for m in T3019_HAUT]
DONNEES["ex3019"] = {"axe x": AXE3019, "O": O3019, "motif": [T3019_TRI, T3019_CAR],
                     "etape 1": T3019_HAUT[2:], "etape 2": T3019_BAS}


def ex3019(corrige):
    F = Fig(.6)
    F.grille(0, 0, 8, 8)
    F.brut(r"\draw[otNavy,line width=1.4pt] (0,0) rectangle (8,8);")
    F.seg((AXE3019, -.4), (AXE3019, 8.4), "axe", memo=False)
    F.texte((AXE3019 + .15, 8.5), r"$(d)$", "south west", N)
    if corrige:
        F.seg(T3019_TRI[0], T3019_BAS[0][0], "constr")
        codage(F, T3019_TRI[0], O3019, 1)
        codage(F, O3019, T3019_BAS[0][0], 1)
        for m in T3019_HAUT[2:] + T3019_BAS:
            F.poly(m, "image")
    F.poly(T3019_TRI, "depart")
    F.poly(T3019_CAR, "depart")
    F.point(O3019, "O", ang=None if corrige else 315)
    return F.code()


FIGURES["ex3019_enonce"] = ex3019(False)
FIGURES["ex3019_corrige"] = ex3019(True)
