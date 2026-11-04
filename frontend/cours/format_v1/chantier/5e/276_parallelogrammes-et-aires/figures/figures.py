# -*- coding: utf-8 -*-
r"""Figures de la notion « Parallélogrammes et aires » (5e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
trouvés (corrigés) et constructions, orange = angles. Les hauteurs sont en pointillés :
bleu marine quand elles sont données, vert quand elles sont trouvées.

Toutes les figures sont calculées en vraie grandeur (cm, ou m pour les terrains), puis
réduites d'un facteur k : DONNEES garde les coordonnées réelles, contrôlées par
verif_276.py (sympy). Outils géométriques et classe Fig repris de la notion 274 (5e).
"""
import math

PREAMBULE_EXTRA = r"""
\usetikzlibrary{decorations.pathmorphing}
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  compas/.style={otGreenDark,line width=.7pt},
  constr/.style={otGreenDark,line width=.75pt},
  rep/.style={otGreenDark,line width=1.1pt,line join=round},
  repTir/.style={otGreenDark,line width=.9pt,dash pattern=on 4pt off 2.5pt},
  haut/.style={otNavy,line width=.85pt,dash pattern=on 3.5pt off 2pt},
  hautV/.style={otGreenDark,line width=1.1pt,dash pattern=on 3.5pt off 2pt},
  prolong/.style={otMuted,line width=.6pt,dash pattern=on 1.6pt off 1.6pt},
  diag/.style={otNavy!80,line width=.7pt},
  main/.style={otNavy,line width=.9pt,line join=round,decorate,
    decoration={random steps,segment length=5pt,amplitude=.45pt}},
}
"""

OR = "otOrange!90!black"
VE = "otGreenDark"
NA = "otNavy"
MU = "otMuted"

DONNEES = {}
FIGURES = {}


# ====================================================================== outils
def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def pol(p, L, deg):
    a = math.radians(deg)
    return (p[0] + L * math.cos(a), p[1] + L * math.sin(a))


def direc(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def dist(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def lerp(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def quatrieme(A, B, C):
    """D tel que ABCD soit un parallélogramme."""
    return (A[0] + C[0] - B[0], A[1] + C[1] - B[1])


def pied(p, a, b):
    ux, uy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / (ux * ux + uy * uy)
    return (a[0] + t * ux, a[1] + t * uy)


def angle_libre(dirs):
    """Milieu du plus grand secteur libre entre les directions données (degrés)."""
    d = sorted(x % 360 for x in dirs)
    best, mil = -1, 0
    for i, a in enumerate(d):
        b = d[(i + 1) % len(d)] + (360 if i == len(d) - 1 else 0)
        if b - a > best:
            best, mil = b - a, (a + b) / 2
    return mil % 360


def centre(*pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


class Fig:
    """Figure TikZ : coordonnées réelles multipliées par k ; décalages des textes en cm."""

    def __init__(self, k=1.0, seed=None):
        self.k = k
        self.s = []
        if seed is not None:
            self.s.append(r"\pgfmathsetseed{%d}" % seed)

    def T(self, p):
        return (p[0] * self.k, p[1] * self.k)

    def P(self, p):
        q = self.T(p)
        return "(%s,%s)" % (f(q[0]), f(q[1]))

    def Q(self, q):  # coordonnées déjà en cm
        return "(%s,%s)" % (f(q[0]), f(q[1]))

    def add(self, *l):
        self.s += list(l)

    def code(self):
        return "\n".join([r"\begin{tikzpicture}[line cap=round,line join=round]"] + self.s + [r"\end{tikzpicture}"])

    # ---------------------------------------------------------------- tracés
    def fill(self, pts, coul="otSky"):
        self.add(r"\fill[%s] %s -- cycle;" % (coul, " -- ".join(self.P(p) for p in pts)))

    def poly(self, pts, style="geoTrait", ferme=True):
        self.add(r"\draw[%s] %s%s;" % (style, " -- ".join(self.P(p) for p in pts), " -- cycle" if ferme else ""))

    def seg(self, p, q, style="geoTrait"):
        self.add(r"\draw[%s] %s -- %s;" % (style, self.P(p), self.P(q)))

    def cercle(self, c, r, style="compas"):
        self.add(r"\draw[%s] %s circle (%s);" % (style, self.P(c), f(r * self.k)))

    def compas(self, c, r, a_mil, demi=12, style="compas"):
        """Arc de compas de centre c, rayon r (réel), centré sur la direction a_mil (degrés)."""
        a1, a2 = a_mil - demi, a_mil + demi
        dep = pol(self.T(c), r * self.k, a1)
        self.add(r"\draw[%s] %s arc (%s:%s:%s);" % (style, self.Q(dep), f(a1), f(a2), f(r * self.k)))

    # ---------------------------------------------------------------- textes
    def texte(self, p, txt, anchor="center", style="lab", coul=None, reel=True):
        q = self.P(p) if reel else self.Q(p)
        c = (",text=%s" % coul) if coul else ""
        self.add(r"\node[%s%s,anchor=%s] at %s {%s};" % (style, c, anchor, q, txt))

    def nom(self, p, txt, ang, d=0.14, coul="otInk", maths=True):
        q = pol(self.T(p), d, ang)
        t = ("$%s$" % txt) if maths else txt
        self.add(r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, f((ang + 180) % 360), self.Q(q), t))

    def pt(self, p, txt=None, ang=90, coul=NA, tc=None, d=0.14):
        self.add(r"\fill[%s] %s circle (1.9pt);" % (coul, self.P(p)))
        if txt:
            self.nom(p, txt, ang, d, tc or ("otInk" if coul == NA else coul))

    def pts(self, dico, angs, g=None, **kw):
        """Points nommés ; angs : {nom: angle} ou None pour l'orientation automatique (depuis g)."""
        for n, p in dico.items():
            a = angs.get(n) if angs else None
            if a is None:
                a = direc(g, p)
            self.pt(p, n, a, **kw)

    def lcote(self, p, q, txt, loin, d=0.13, coul="otInk", t=0.5):
        """Texte le long de [pq], du côté opposé au point « loin » (réel)."""
        P_, Q_, L_ = self.T(p), self.T(q), self.T(loin)
        dx, dy = Q_[0] - P_[0], Q_[1] - P_[1]
        n = math.hypot(dx, dy)
        nx, ny = -dy / n, dx / n
        m = (P_[0] + t * dx, P_[1] + t * dy)
        if (L_[0] - m[0]) * nx + (L_[1] - m[1]) * ny > 0:
            nx, ny = -nx, -ny
        ang = math.degrees(math.atan2(ny, nx))
        q2 = (m[0] + d * nx, m[1] + d * ny)
        noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
        anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
        self.add(r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, self.Q(q2), txt))

    # ---------------------------------------------------------------- codages
    def angle(self, o, p, q, r=0.42, txt=None, n=1, coul=OR, lr=None, am=None, tc=None):
        """Arc de l'angle saillant (o ; p, q), rayon r en cm ; texte sur la bissectrice (ou direction am)."""
        a1, a2 = direc(o, p), direc(o, q)
        sw = (a2 - a1) % 360
        if sw > 180:
            a1, a2 = a2, a1
            sw = 360 - sw
        a2 = a1 + sw
        O_ = self.T(o)
        for i in range(n):
            rr = r + 0.07 * i
            self.add(r"\draw[%s,line width=.75pt] %s arc (%s:%s:%s);" % (coul, self.Q(pol(O_, rr, a1)), f(a1), f(a2), f(rr)))
        if txt:
            if am is None:
                am = a1 + sw / 2
            if lr is None:
                lr = max(r + 0.07 * (n - 1) + 0.26, 0.34 / math.sin(math.radians(max(sw, 8) / 2)))
                lr = min(lr, r + 1.1)
            q2 = pol(O_, lr, am)
            self.add(r"\node[lab,text=%s,anchor=center] at %s {%s};" % (tc or coul, self.Q(q2), txt))

    def droit(self, o, p, q, s=0.2, coul=NA):
        O_ = self.T(o)
        u = pol(O_, s, direc(o, p))
        v = pol(O_, s, direc(o, q))
        w = (u[0] + v[0] - O_[0], u[1] + v[1] - O_[1])
        self.add(r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, self.Q(u), self.Q(w), self.Q(v)))

    def tick(self, p, q, n=1, coul=NA, t=0.5):
        P_, Q_ = self.T(p), self.T(q)
        dx, dy = Q_[0] - P_[0], Q_[1] - P_[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        vx, vy = -uy, ux
        m = (P_[0] + t * dx, P_[1] + t * dy)
        for i in range(n):
            o = (i - (n - 1) / 2) * 0.075
            c = (m[0] + o * ux, m[1] + o * uy)
            self.add(r"\draw[%s,line width=.7pt] %s -- %s;" % (coul, self.Q((c[0] - .11 * vx, c[1] - .11 * vy)),
                                                              self.Q((c[0] + .11 * vx, c[1] + .11 * vy))))

    def cote(self, p, q, txt, off=0.4, coul="otInk"):
        r"""Cote grise parallèle à [pq], décalée vers la gauche de p→q (macro \cote du préambule)."""
        self.add(r"\coordinate (cA) at %s; \coordinate (cB) at %s;" % (self.P(p), self.P(q)))
        self.add(r"\cote[%s]{cA}{cB}{\textcolor{%s}{%s}}" % (f(off), coul, txt))


def deg(v):
    return r"$%s^{\circ}$" % v


def vert(t):
    return r"\textcolor{otGreenDark}{%s}" % t


def legende(F, p, txt, coul="otMuted"):
    """Légende (coordonnées en cm, déjà réduites)."""
    F.texte(p, txt, "north", "txt", coul, reel=False)


TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


# ====================================================================== COURS
def cours_parallelogramme():
    """RSTU (RS = 10, ST = 6, angle R = 60°, à l'échelle) : côtés et angles, puis diagonales."""
    k = 0.24
    R = (0.0, 0.0)
    S = (10.0, 0.0)
    U = pol(R, 6, 60)
    T = quatrieme(S, R, U)  # T = S + U - R
    O = lerp(R, T, 0.5)
    DONNEES["cours_parallelogramme"] = {"R": R, "S": S, "T": T, "U": U, "O": O}
    F = Fig(k)
    dx = 15.5
    # panneau 1 : côtés et angles opposés
    F.fill([R, S, T, U])
    F.poly([R, S, T, U])
    F.tick(R, S, 2)
    F.tick(U, T, 2)
    F.tick(S, T, 1)
    F.tick(R, U, 1)
    F.angle(R, S, U, 0.42, n=1)
    F.angle(T, U, S, 0.42, n=1)
    F.angle(S, T, R, 0.3, n=2)
    F.angle(U, R, T, 0.3, n=2)
    F.pts({"R": R, "S": S, "T": T, "U": U}, {"R": 225, "S": 315, "T": 45, "U": 135})
    legende(F, (F.T(lerp(R, S, 0.5))[0] + 0.35, -0.5), "côtés et angles")
    # panneau 2 : diagonales
    R2, S2, T2, U2, O2 = [add(p, (dx, 0)) for p in (R, S, T, U, O)]
    F.fill([R2, S2, T2, U2])
    F.poly([R2, S2, T2, U2])
    F.seg(R2, T2, "diag")
    F.seg(S2, U2, "diag")
    F.tick(R2, O2, 1, VE)
    F.tick(O2, T2, 1, VE)
    F.tick(S2, O2, 2, VE)
    F.tick(O2, U2, 2, VE)
    F.pts({"R": R2, "S": S2, "T": T2, "U": U2}, {"R": 225, "S": 315, "T": 45, "U": 135})
    F.pt(O2, "O", angle_libre([direc(O2, p) for p in (R2, S2, T2, U2)]), coul=VE, d=0.17)
    legende(F, (F.T(lerp(R2, S2, 0.5))[0] + 0.35, -0.5), "diagonales")
    return F.code()


def cours_construction():
    """Quatrième sommet au compas : arcs de rayons BC (centre A) et AB (centre C)."""
    A = (0.0, 0.0)
    B = (4.0, 0.0)
    C = pol(B, 2.6, 115)
    D = quatrieme(A, B, C)
    DONNEES["cours_construction"] = {"A": A, "B": B, "C": C, "D": D}
    F = Fig(1.15)
    F.seg(A, B)
    F.seg(B, C)
    F.seg(A, C, "prolong")
    F.compas(A, dist(B, C), direc(A, D), 16)
    F.compas(C, dist(A, B), direc(C, D), 12)
    F.seg(A, D, "rep")
    F.seg(C, D, "rep")
    F.pts({"A": A, "B": B, "C": C}, {"A": 225, "B": 315, "C": 45})
    F.pt(D, "D", 135, coul=VE, d=0.18)
    F.lcote(A, D, vert("rayon $BC$"), C, d=0.18, t=0.45)
    F.lcote(D, C, vert("rayon $AB$"), A, d=0.16, t=0.55)
    return F.code()


def cours_particuliers():
    k = 0.72
    F = Fig(k)
    # rectangle
    a, b = 3.2, 2.0
    R1 = [(0, 0), (a, 0), (a, b), (0, b)]
    O1 = (a / 2, b / 2)
    F.fill(R1)
    F.poly(R1)
    for p in R1:
        F.seg(p, O1, "diag")
    for i in range(4):
        F.tick(R1[i], O1, 1, VE)
    F.droit(R1[0], R1[1], R1[3], 0.17)
    F.droit(R1[1], R1[2], R1[0], 0.17)
    F.droit(R1[2], R1[3], R1[1], 0.17)
    F.droit(R1[3], R1[0], R1[2], 0.17)
    legende(F, (k * a / 2, -0.25), "rectangle")
    # losange
    x0 = a + 0.9
    O2 = (x0 + 1.5, 1.0)
    L2 = [(x0, 1.0), (x0 + 1.5, 0.0), (x0 + 3.0, 1.0), (x0 + 1.5, 2.0)]
    F.fill(L2)
    F.poly(L2)
    F.seg(L2[0], L2[2], "diag")
    F.seg(L2[1], L2[3], "diag")
    for i in range(4):
        F.tick(L2[i], L2[(i + 1) % 4], 1)
    F.droit(O2, L2[2], L2[3], 0.17, VE)
    legende(F, (k * O2[0], -0.25), "losange")
    # carré
    x1 = x0 + 3.0 + 0.9
    c = 2.0
    C3 = [(x1, 0), (x1 + c, 0), (x1 + c, c), (x1, c)]
    O3 = (x1 + c / 2, c / 2)
    F.fill(C3)
    F.poly(C3)
    F.seg(C3[0], C3[2], "diag")
    F.seg(C3[1], C3[3], "diag")
    for i in range(4):
        F.tick(C3[i], C3[(i + 1) % 4], 1)
    F.droit(C3[0], C3[1], C3[3], 0.17)
    F.droit(O3, C3[2], C3[3], 0.15, VE)
    legende(F, (k * O3[0], -0.25), "carré")
    DONNEES["cours_particuliers"] = {"rectangle": R1, "losange": L2, "carre": C3}
    return F.code()


def cours_aire_para():
    """Le triangle ADH, découpé, est recollé en BCH' : rectangle HH'CD de même aire."""
    A, B = (0.0, 0.0), (5.0, 0.0)
    D = (1.4, 2.4)
    C = add(B, D)
    H = (D[0], 0.0)
    H2 = (C[0], 0.0)
    DONNEES["cours_aire_para"] = {"A": A, "B": B, "C": C, "D": D, "H": H, "H2": H2}
    F = Fig(1.1)
    F.fill([H, B, C, D], "otSky")
    F.fill([A, H, D], "otOrange!22")
    F.fill([B, H2, C], "otGreen!22")
    F.poly([A, B, C, D])
    F.poly([B, H2, C], "repTir", ferme=False)
    F.seg(D, H, "haut")
    F.droit(H, B, D, 0.18)
    F.droit(H2, C, B, 0.18, VE)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    F.pt(H, "H", 270, d=0.16)
    F.nom(H2, r"H'", 300, 0.16, VE)
    F.lcote(D, H, "$h$", B, d=0.12, t=0.5)
    F.cote(A, B, "$b$", -0.75)
    return F.code()


def cours_aire_triangle():
    k = 0.7
    F = Fig(k)
    # triangle = moitié d'un parallélogramme
    A, B, C = (0.0, 0.0), (4.0, 0.0), (1.3, 2.2)
    D = add(B, C)
    H = (C[0], 0.0)
    F.fill([B, D, C], "otGreen!14")
    F.fill([A, B, C], "otSky")
    F.poly([B, D, C], "repTir", ferme=False)
    F.poly([A, B, C])
    F.seg(C, H, "haut")
    F.droit(H, B, C, 0.17)
    F.lcote(C, H, "$h$", A, d=0.11, t=0.45)
    F.cote(A, B, "$b$", -0.55)
    for n, p, a in (("A", A, 225), ("B", B, 315), ("C", C, 110)):
        F.pt(p, n, a)
    # triangle obtus : pied sur le prolongement
    dx = 6.2
    E, G2, Hh = (dx, 0.0), (dx + 3.6, 2.2), (dx + 3.6, 0.0)
    Fp = (dx + 2.3, 0.0)
    F.fill([E, Fp, G2], "otSky")
    F.seg(Fp, add(Hh, (0.45, 0)), "prolong")
    F.poly([E, Fp, G2])
    F.seg(G2, Hh, "haut")
    F.droit(Hh, Fp, G2, 0.17)
    F.lcote(G2, Hh, "$h$", Fp, d=0.11, t=0.45)
    F.cote(E, Fp, "$b$", -0.55)
    for n, p, a in (("E", E, 225), ("F", Fp, 290), ("G", G2, 60)):
        F.pt(p, n, a)
    DONNEES["cours_aire_triangle"] = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp, "G": G2, "H": Hh}
    return F.code()


def cours_disque():
    r = 1.0
    n = 8                      # 8 parts « en bas » + 8 parts « en haut » = 16 parts
    th = 360.0 / (2 * n)
    w = 2 * r * math.sin(math.radians(th / 2))
    y0 = r * (1 - math.cos(math.radians(th / 2)))
    F = Fig(1.0)
    # disque : moitié haute bleue, moitié basse verte
    Oc = (0.0, r)
    F.add(r"\fill[otSky] %s ++(%s,0) arc (0:180:%s) -- cycle;" % (F.P(Oc), f(r), f(r)))
    F.add(r"\fill[otGreen!22] %s ++(%s,0) arc (0:-180:%s) -- cycle;" % (F.P(Oc), f(r), f(r)))
    F.cercle(Oc, r, "geoTrait")
    F.seg(Oc, pol(Oc, r, 50))
    F.pt(Oc, "O", 230, d=0.14)
    F.lcote(Oc, pol(Oc, r, 50), "$r$", pol(Oc, r, 0), d=0.1, t=0.55)
    # flèche
    x_a = r + 0.35
    F.add(r"\draw[otMuted,line width=.8pt,-{Stealth[length=2mm]}] (%s,%s) -- (%s,%s);" % (f(x_a), f(r), f(x_a + 0.7), f(r)))
    # parts disposées tête-bêche
    x0 = x_a + 1.05
    for i in range(n):
        P = (x0 + i * w + w / 2, r)               # sommet en haut, arc en bas
        a1, a2 = 270 - th / 2, 270 + th / 2
        p1 = pol(P, r, a1)
        F.add(r"\filldraw[fill=otSky,draw=otNavy,line width=.6pt] %s -- %s arc (%s:%s:%s) -- cycle;"
              % (F.P(P), F.P(p1), f(a1), f(a2), f(r)))
        Q = (x0 + (i + 1) * w, y0)                 # sommet en bas, arc en haut
        b1, b2 = 90 - th / 2, 90 + th / 2
        q1 = pol(Q, r, b1)
        F.add(r"\filldraw[fill=otGreen!22,draw=otNavy,line width=.6pt] %s -- %s arc (%s:%s:%s) -- cycle;"
              % (F.P(Q), F.P(q1), f(b1), f(b2), f(r)))
    base = n * w
    F.cote((x0, 0.0), (x0 + base, 0.0), r"$\pi \times r$", -0.45)
    xr = x0 + base + w / 2
    F.cote((xr, y0), (xr, r), "$r$", -0.42)
    DONNEES["cours_disque"] = {"r": r, "n": n, "w": w, "base": base}
    return F.code()


FIGURES["cours_parallelogramme"] = cours_parallelogramme()
FIGURES["cours_construction"] = cours_construction()
FIGURES["cours_particuliers"] = cours_particuliers()
FIGURES["cours_aire_para"] = cours_aire_para()
FIGURES["cours_aire_triangle"] = cours_aire_triangle()
FIGURES["cours_disque"] = cours_disque()


# ====================================================================== 3020 : propriétés
def ex3020(corr):
    A, B = (0.0, 0.0), (8.0, 0.0)
    D = pol(A, 5, 60)
    C = add(B, D)
    O = lerp(A, C, 0.5)
    DONNEES["ex3020"] = {"A": A, "B": B, "C": C, "D": D, "O": O}
    F = Fig(0.64)
    F.fill([A, B, C, D])
    F.seg(A, C, "diag")
    F.seg(B, D, "diag")
    F.poly([A, B, C, D])
    F.angle(A, B, D, 0.55, deg(60), am=11, lr=1.42)
    F.lcote(A, B, "8 cm", D, t=0.5, d=0.12)
    F.lcote(A, D, "5 cm", B, t=0.5, d=0.12)
    F.lcote(O, D, "3,5 cm", A, t=0.45, d=0.1)
    if corr:
        F.tick(A, O, 1, VE, t=0.35)
        F.tick(O, C, 1, VE, t=0.65)
        F.tick(O, B, 2, VE, t=0.45)
        F.tick(O, D, 2, VE, t=0.55)
        F.lcote(D, C, vert("8 cm"), A, t=0.5, d=0.12)
        F.lcote(B, C, vert("5 cm"), A, t=0.5, d=0.12)
        F.angle(C, D, B, 0.55, vert(deg(60)), coul=VE, am=191, lr=1.42)
        F.angle(B, C, A, 0.42, vert(deg(120)), coul=VE, am=100, lr=0.85)
        F.angle(D, A, C, 0.42, vert(deg(120)), coul=VE, am=280, lr=0.85)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    F.pt(O, "O", angle_libre([direc(O, p) for p in (A, B, C, D)]), d=0.16)
    return F.code()


FIGURES["ex3020_enonce"] = ex3020(False)
FIGURES["ex3020_corrige"] = ex3020(True)


# ====================================================================== 3026 : construire
def pts3026():
    A, B = (0.0, 0.0), (5.0, 0.0)
    C = pol(B, 3.5, 180 - 70)
    D = quatrieme(A, B, C)
    O = lerp(A, C, 0.5)
    DONNEES["ex3026"] = {"A": A, "B": B, "C": C, "D": D, "O": O}
    return A, B, C, D, O


def ex3026_croquis():
    A, B, C, D, O = pts3026()
    F = Fig(0.85, seed=11)
    F.poly([A, B, C, D], "main")
    F.angle(B, A, C, 0.45, deg(70))
    F.lcote(A, B, "5 cm", D, t=0.5, d=0.12)
    F.lcote(B, C, "3,5 cm", A, t=0.5, d=0.12)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    return F.code()


def ex3026_compas():
    A, B, C, D, O = pts3026()
    F = Fig(0.85)
    F.seg(A, B)
    F.seg(B, C)
    F.angle(B, A, C, 0.45, deg(70))
    F.compas(A, 3.5, direc(A, D), 15)
    F.compas(C, 5.0, direc(C, D), 11)
    F.seg(A, D, "rep")
    F.seg(C, D, "rep")
    F.lcote(A, B, "5 cm", D, t=0.5, d=0.12)
    F.lcote(B, C, "3,5 cm", A, t=0.5, d=0.12)
    F.lcote(A, D, vert("3,5 cm"), B, t=0.42, d=0.14)
    F.lcote(D, C, vert("5 cm"), A, t=0.5, d=0.14)
    F.pts({"A": A, "B": B, "C": C}, {"A": 225, "B": 315, "C": 45})
    F.pt(D, "D", 135, coul=VE, d=0.18)
    return F.code()


def ex3026_diagonales():
    A, B, C, D, O = pts3026()
    F = Fig(0.85)
    F.seg(A, B)
    F.seg(B, C)
    F.seg(A, C, "diag")
    F.seg(B, D, "repTir")
    F.seg(A, D, "rep")
    F.seg(C, D, "rep")
    F.tick(A, O, 1)
    F.tick(O, C, 1)
    F.tick(B, O, 2, VE)
    F.tick(O, D, 2, VE)
    F.pts({"A": A, "B": B, "C": C}, {"A": 225, "B": 315, "C": 45})
    F.pt(D, "D", 135, coul=VE, d=0.18)
    F.pt(O, "O", angle_libre([direc(O, p) for p in (A, B, C, D)]), d=0.16)
    return F.code()


FIGURES["ex3026_croquis"] = ex3026_croquis()
FIGURES["ex3026_compas"] = ex3026_compas()
FIGURES["ex3026_diagonales"] = ex3026_diagonales()


# ====================================================================== 3024 : diagonales
def panneaux3024():
    """(noms, angles des sommets depuis O, demi-diagonales, codages, droit, titre)."""
    return [
        ("ABCD", (195, 315, 15, 135), (2.0, 1.25, 2.0, 1.25), (1, 2, 1, 2), False, "parallélogramme"),
        ("EFGH", (200, 320, 20, 140), (1.9, 1.9, 1.9, 1.9), (1, 1, 1, 1), False, "rectangle"),
        ("IJKL", (180, 270, 0, 90), (2.0, 1.15, 2.0, 1.15), (1, 2, 1, 2), True, "losange"),
        ("MNPQ", (225, 315, 45, 135), (1.6, 1.6, 1.6, 1.6), (1, 1, 1, 1), True, "carré"),
    ]


def ex3024(corr):
    F = Fig(0.72)
    pos = [(0.0, 0.0), (4.9, 0.0), (0.0, -4.05), (4.9, -4.05)]
    don = {}
    for (noms, angs, demi, cod, droit, titre), (cx, cy) in zip(panneaux3024(), pos):
        O = (cx + 2.15, cy)
        S = [pol(O, l, a) for a, l in zip(angs, demi)]
        don[noms] = S
        if corr:
            F.fill(S, "otGreen!12")
            F.poly(S, "rep")
        F.seg(S[0], S[2], "geoTrait")
        F.seg(S[1], S[3], "geoTrait")
        for i in range(4):
            F.tick(O, S[i], cod[i], t=0.55)
        if droit:
            F.droit(O, S[2], S[3], 0.2)
        for i in range(4):
            F.pt(S[i], noms[i], angs[i], d=0.15)
        F.pt(O, "O", {"IJKL": 225, "MNPQ": 270}.get(noms, angle_libre(list(angs))), d=0.17)
        yb = cy - 1.25
        if corr:
            legende(F, (F.T(O)[0], F.T((0, yb))[1] - 0.5), titre, VE)
        else:
            legende(F, (F.T(O)[0], F.T((0, yb))[1] - 0.5), "Figure %d" % (len(don)))
    DONNEES["ex3024"] = don
    return F.code()


FIGURES["ex3024_enonce"] = ex3024(False)
FIGURES["ex3024_corrige"] = ex3024(True)


# ====================================================================== 3031 : démontrer
def pts3031():
    R = (0.0, 0.0)
    D, O = (-3.0, 0.0), (0.0, 2.0)
    L, E = (3.0, 0.0), (0.0, -2.0)
    DONNEES["ex3031"] = {"R": R, "D": D, "O": O, "L": L, "E": E}
    return R, D, O, L, E


def ex3031_enonce():
    R, D, O, L, E = pts3031()
    F = Fig(0.9)
    F.fill([D, R, O])
    F.seg(R, L, "prolong")
    F.seg(R, E, "prolong")
    F.poly([D, R, O])
    F.droit(R, D, O, 0.22)
    F.lcote(D, R, "3 cm", O, t=0.5, d=0.12)
    F.lcote(R, O, "2 cm", D, t=0.5, d=0.12)
    F.pts({"D": D, "O": O, "L": L, "E": E}, {"D": 180, "O": 90, "L": 0, "E": 270})
    F.pt(R, "R", 225, d=0.16)
    return F.code()


def ex3031_trapeze():
    I, J, K, L = (0.0, 0.0), (2.4, 3.2), (4.6, 3.2), (7.0, 0.0)
    S = (3.5, 3.2 * 3.5 / 2.4)          # intersection de (IJ) et (LK)
    DONNEES["ex3031_trapeze"] = {"I": I, "J": J, "K": K, "L": L, "S": S}
    F = Fig(0.78)
    F.fill([I, J, K, L])
    F.seg(J, S, "prolong")
    F.seg(K, S, "prolong")
    F.poly([I, J, K, L])
    F.tick(I, J, 1)
    F.tick(L, K, 1)
    F.lcote(I, J, "4 cm", L, t=0.68, d=0.13)
    F.lcote(L, K, "4 cm", I, t=0.68, d=0.13)
    F.pts({"I": I, "J": J, "K": K, "L": L}, {"I": 225, "J": 160, "K": 20, "L": 315})
    legende(F, (F.T(lerp(I, L, 0.5))[0], -0.2), r"$(IJ)$ et $(KL)$ ne sont pas parallèles", OR)
    return F.code()


def ex3031_corrige():
    R, D, O, L, E = pts3031()
    F = Fig(0.9)
    F.fill([D, O, L, E], "otGreen!12")
    F.seg(D, L, "geoTrait")
    F.seg(O, E, "geoTrait")
    F.poly([D, O, L, E], "rep")
    F.droit(R, L, O, 0.22)
    F.tick(D, R, 1)
    F.tick(R, L, 1)
    F.tick(R, O, 2)
    F.tick(R, E, 2)
    F.pts({"D": D, "O": O, "L": L, "E": E}, {"D": 180, "O": 90, "L": 0, "E": 270})
    F.pt(R, "R", 225, d=0.16)
    return F.code()


FIGURES["ex3031_enonce"] = ex3031_enonce()
FIGURES["ex3031_trapeze"] = ex3031_trapeze()
FIGURES["ex3031_corrige"] = ex3031_corrige()


# ====================================================================== 3021 : aire et hauteurs
def pts3021():
    A, B, D = (0.0, 0.0), (6.0, 0.0), (3.0, 4.0)
    C = add(B, D)
    H = (3.0, 0.0)
    K = pied(B, A, D)
    E, Fp, Hh = (0.0, 0.0), (3.0, 0.0), (5.0, 4.0)
    G = add(Fp, Hh)
    P = (5.0, 0.0)
    DONNEES["ex3021"] = {"A": A, "B": B, "C": C, "D": D, "H": H, "K": K,
                         "E": E, "F": Fp, "G": G, "Hh": Hh, "P": P}
    return A, B, C, D, H, K, E, Fp, G, Hh, P


def ex3021_abcd(corr):
    A, B, C, D, H, K, *_ = pts3021()
    F = Fig(0.72)
    F.fill([A, B, C, D])
    F.poly([A, B, C, D])
    F.seg(D, H, "haut")
    F.droit(H, B, D, 0.2)
    F.lcote(A, B, "6 cm", D, t=0.74, d=0.12)
    F.lcote(A, D, "5 cm", B, t=0.5, d=0.12)
    F.lcote(D, H, "4 cm", A, t=0.8, d=0.1)
    if corr:
        F.seg(B, K, "hautV")
        F.droit(K, A, B, 0.2, VE)
        F.lcote(B, K, vert("4,8 cm"), A, t=0.36, d=0.12)
        F.pt(K, "K", 160, coul=VE, d=0.16)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 90})
    F.pt(H, "H", 270, d=0.16)
    return F.code()


def ex3021_efgh(corr):
    *_, E, Fp, G, Hh, P = pts3021()
    F = Fig(0.72)
    F.fill([E, Fp, G, Hh])
    F.seg(Fp, add(P, (0.8, 0)), "prolong")
    F.poly([E, Fp, G, Hh])
    F.seg(Hh, P, "hautV" if corr else "haut")
    F.droit(P, Fp, Hh, 0.2, VE if corr else NA)
    F.lcote(E, Fp, "3 cm", Hh, t=0.5, d=0.12)
    F.lcote(P, Hh, vert("4 cm") if corr else "4 cm", Fp, t=0.7, d=0.1)
    F.pts({"E": E, "F": Fp, "G": G, "H": Hh}, {"E": 225, "F": 270, "G": 45, "H": 135})
    F.pt(P, "P", 270, coul=VE if corr else NA, d=0.16)
    return F.code()


FIGURES["ex3021_abcd"] = ex3021_abcd(False)
FIGURES["ex3021_efgh"] = ex3021_efgh(False)
FIGURES["ex3021_abcd_corrige"] = ex3021_abcd(True)
FIGURES["ex3021_efgh_corrige"] = ex3021_efgh(True)


# ====================================================================== 3033 : triangles, parcelle
def pts3033():
    R, S, T = (0.0, 0.0), (6.0, 0.0), (2.0, 4.0)
    H = (2.0, 0.0)
    dx = 8.4
    U, V, W = (dx, 0.0), (dx + 3.0, 0.0), (dx + 5.0, 4.0)
    P = (dx + 5.0, 0.0)
    A, B, D = (0.0, 0.0), (6.0, 0.0), (1.5, 2.5)
    C = add(B, D)
    E = (3.5, 4.5)
    K = (3.5, 2.5)
    Hp = (1.5, 0.0)
    DONNEES["ex3033"] = {"R": R, "S": S, "T": T, "H": H, "U": U, "V": V, "W": W, "P": P,
                         "A": A, "B": B, "C": C, "D": D, "E": E, "K": K, "Hp": Hp}
    return R, S, T, H, U, V, W, P, A, B, C, D, E, K, Hp


def ex3033_triangles(corr):
    R, S, T, H, U, V, W, P, *_ = pts3033()
    F = Fig(0.5)
    if corr:
        T2 = add(S, T)
        X = add(U, sub(W, V))
        F.fill([S, T2, T], "otGreen!14")
        F.poly([S, T2, T], "repTir", ferme=False)
        F.fill([U, X, W], "otGreen!14")
        F.poly([U, X, W], "repTir", ferme=False)
    F.fill([R, S, T])
    F.fill([U, V, W])
    F.seg(V, add(P, (0.7, 0)), "prolong")
    F.poly([R, S, T])
    F.poly([U, V, W])
    F.seg(T, H, "haut")
    F.seg(W, P, "haut")
    F.droit(H, S, T, 0.18)
    F.droit(P, V, W, 0.18)
    F.lcote(R, S, "6 cm", T, t=0.66, d=0.12)
    F.lcote(T, H, "4 cm", R, t=0.5, d=0.1)
    F.lcote(U, V, "3 cm", W, t=0.5, d=0.12)
    F.lcote(W, P, "4 cm", U, t=0.5, d=0.1)
    F.pts({"R": R, "S": S, "T": T, "U": U, "V": V, "W": W},
          {"R": 225, "S": 315, "T": 90, "U": 225, "V": 270, "W": 45})
    F.pt(H, "H", 270, d=0.16)
    F.pt(P, "P", 270, d=0.16)
    if corr:
        legende(F, (F.T(lerp(R, S, 0.5))[0] + 0.3, -0.62), r"aire : $\dfrac{6 \times 4}{2} = 12\ \text{cm}^2$", VE)
        legende(F, (F.T(lerp(U, P, 0.5))[0], -0.62), r"aire : $\dfrac{3 \times 4}{2} = 6\ \text{cm}^2$", VE)
    return F.code()


def ex3033_parcelle(corr):
    *_, A, B, C, D, E, K, Hp = pts3033()
    F = Fig(0.9)
    F.fill([A, B, C, D], "otSky")
    F.fill([D, C, E], "otGreen!16" if corr else "otSky")
    F.poly([A, B, C, D])
    F.poly([D, E, C], ferme=False)
    F.seg(D, Hp, "haut")
    F.seg(E, K, "haut")
    F.droit(Hp, B, D, 0.18)
    F.droit(K, C, E, 0.18)
    F.lcote(A, B, "6 m", D, t=0.6, d=0.12)
    F.lcote(D, Hp, "2,5 m", A, t=0.5, d=0.1)
    F.lcote(E, K, "2 m", D, t=0.5, d=0.1)
    if corr:
        F.texte((4.3, 1.15), vert(r"$15\ \text{m}^2$"))
        F.texte((5.0, 3.15), vert(r"$6\ \text{m}^2$"))
        F.lcote(D, C, vert("6 m"), A, t=0.78, d=0.1)
    F.pts({"A": A, "B": B, "C": C, "D": D, "E": E}, {"A": 225, "B": 315, "C": 0, "D": 180, "E": 90})
    F.pt(Hp, "H", 270, d=0.16)
    F.pt(K, "K", 290, d=0.16)
    return F.code()


FIGURES["ex3033_triangles"] = ex3033_triangles(False)
FIGURES["ex3033_parcelle"] = ex3033_parcelle(False)
FIGURES["ex3033_triangles_corrige"] = ex3033_triangles(True)
FIGURES["ex3033_parcelle_corrige"] = ex3033_parcelle(True)


# ====================================================================== 3040 : terrasse
def pts3040():
    T = [(0.0, 0.0), (6.0, 0.0), (6.0, 4.0), (0.0, 4.0)]
    M, N, P, Q = (1.5, 1.0), (4.5, 1.0), (5.0, 3.0), (2.0, 3.0)
    Hq = (2.0, 1.0)
    DONNEES["ex3040"] = {"terrasse": T, "M": M, "N": N, "P": P, "Q": Q, "Hq": Hq}
    return T, M, N, P, Q, Hq


def ex3040(corr):
    T, M, N, P, Q, Hq = pts3040()
    F = Fig(1.05)
    if corr:
        F.fill(T, "otGreen!22")
        for i in range(1, 12):
            F.seg((i * 0.5, 0), (i * 0.5, 4), "otGreenDark!35,line width=.35pt")
        for j in range(1, 8):
            F.seg((0, j * 0.5), (6, j * 0.5), "otGreenDark!35,line width=.35pt")
        F.fill([M, N, P, Q], "otOrange!30")
        F.poly([M, N, P, Q], "otOrange!90!black,line width=.9pt")
        F.poly(T)
        F.cote(T[0], T[1], "6 m", -0.4)
        F.cote(T[1], T[2], "4 m", -0.4)
        legende(F, (3.6, -0.95), r"\textcolor{otGreenDark}{surface à daller : $24 - 6 = 18\ \text{m}^2$}")
        legende(F, (3.6, -1.45), r"\textcolor{otOrange!90!black}{massif : $3 \times 2 = 6\ \text{m}^2$} \quad un carreau = une dalle")
    else:
        F.fill(T, "otSky")
        F.fill([M, N, P, Q], "otOrange!30")
        F.poly(T)
        F.poly([M, N, P, Q], "otOrange!90!black,line width=.9pt")
        F.seg(Q, Hq, "haut")
        F.droit(Hq, N, Q, 0.17)
        F.lcote(M, N, "3 m", Q, t=0.6, d=0.1)
        F.lcote(Q, Hq, "2 m", M, t=0.5, d=0.1)
        F.texte((3.8, 1.9), r"\textcolor{otOrange!70!black}{massif}", "center", "txt")
        F.cote(T[0], T[1], "6 m", -0.4)
        F.cote(T[1], T[2], "4 m", -0.4)
    return F.code()


FIGURES["ex3040_enonce"] = ex3040(False)
FIGURES["ex3040_corrige"] = ex3040(True)


# ====================================================================== 3038 : stade
def ex3038(corr):
    k = 0.04
    L, l = 90.0, 60.0
    r = l / 2
    F = Fig(k)
    DONNEES["ex3038"] = {"L": L, "l": l, "r": r}
    if not corr:
        # pelouse : rectangle + deux demi-disques
        F.add(r"\fill[otGreen!22] %s -- %s arc (-90:90:%s) -- %s arc (90:270:%s) -- cycle;"
              % (F.P((0, 0)), F.P((L, 0)), f(r * k), F.P((0, l)), f(r * k)))
        F.add(r"\draw[geoTrait] %s -- %s arc (-90:90:%s) -- %s arc (90:270:%s) -- cycle;"
              % (F.P((0, 0)), F.P((L, 0)), f(r * k), F.P((0, l)), f(r * k)))
        F.seg((0, 0), (0, l), "prolong")
        F.seg((L, 0), (L, l), "prolong")
        F.cote((0, l), (L, l), "90 m", 0.45)
        F.lcote((0, 0), (0, l), "60 m", (-10, l / 2), t=0.5, d=0.1)
    else:
        F.fill([(0, 0), (L, 0), (L, l), (0, l)], "otSky")
        F.poly([(0, 0), (L, 0), (L, l), (0, l)])
        cx = L + 22 + r
        F.add(r"\fill[otGreen!22] %s circle (%s);" % (F.P((cx, r)), f(r * k)))
        F.cercle((cx, r), r, "geoTrait")
        F.seg((cx, 0), (cx, l), "prolong")
        F.seg((cx, r), (cx + r, r), "rep")
        F.pt((cx, r), None)
        F.texte((cx + r / 2, r + 3), vert("30 m"), "south", "lab")
        F.texte((L + 11, r), r"$+$", "center", "lab")
        F.cote((0, 0), (L, 0), "90 m", -0.4)
        F.lcote((0, 0), (0, l), "60 m", (L, l / 2), t=0.5, d=0.1)
        legende(F, (F.T((L / 2, 0))[0], -0.85), r"$90 \times 60 = 5\,400\ \text{m}^2$", NA)
        legende(F, (F.T((cx, 0))[0], -0.85), r"$\pi \times 30^2 \approx 2\,827{,}4\ \text{m}^2$", VE)
    return F.code()


FIGURES["ex3038_enonce"] = ex3038(False)
FIGURES["ex3038_corrige"] = ex3038(True)


# ====================================================================== 3022 : partage du terrain
def pts3022():
    A, B, D = (0.0, 0.0), (12.0, 0.0), (3.0, 7.0)
    C = add(B, D)
    O = lerp(A, C, 0.5)
    H = (3.0, 0.0)
    Fa = pied(A, B, D)
    DONNEES["ex3022"] = {"A": A, "B": B, "C": C, "D": D, "O": O, "H": H, "F": Fa}
    return A, B, C, D, O, H, Fa


def ex3022(corr):
    A, B, C, D, O, H, Fa = pts3022()
    F = Fig(0.44)
    if corr:
        F.fill([A, O, B], "otSky")
        F.fill([B, O, C], "otGreen!16")
        F.fill([C, O, D], "otSky")
        F.fill([D, O, A], "otGreen!16")
    else:
        F.fill([A, B, C, D])
    F.seg(A, C, "diag")
    F.seg(B, D, "diag")
    F.poly([A, B, C, D])
    F.tick(A, O, 1, t=0.5)
    F.tick(O, C, 1, t=0.5)
    F.tick(B, O, 2, t=0.5)
    F.tick(O, D, 2, t=0.3)
    if corr:
        F.seg(A, Fa, "hautV")
        F.droit(Fa, D, A, 0.18, VE)
        F.pt(Fa, None, coul=VE)
        F.texte((6.5, 1.15), vert(r"$21\ \text{m}^2$"))
        F.texte((5.0, 3.35), vert(r"$21\ \text{m}^2$"))
        F.texte((11.2, 3.5), vert(r"$21\ \text{m}^2$"))
        F.texte((8.6, 5.75), vert(r"$21\ \text{m}^2$"))
    else:
        F.seg(D, H, "haut")
        F.droit(H, B, D, 0.18)
        F.lcote(D, H, "7 m", A, t=0.3, d=0.1)
        F.pt(H, "H", 270, d=0.16)
    F.lcote(A, B, "12 m", D, t=0.62, d=0.12)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    F.pt(O, "O", 270 if not corr else 300, d=0.18)
    return F.code()


FIGURES["ex3022_enonce"] = ex3022(False)
FIGURES["ex3022_corrige"] = ex3022(True)


# ====================================================================== 3023 : massif en losange
def pts3023():
    A, B, C, D = (-3.0, 0.0), (0.0, -2.0), (3.0, 0.0), (0.0, 2.0)
    O = (0.0, 0.0)
    DONNEES["ex3023"] = {"A": A, "B": B, "C": C, "D": D, "O": O, "r": 1.0}
    return A, B, C, D, O


def ex3023(corr):
    A, B, C, D, O = pts3023()
    F = Fig(0.95)
    if corr:
        F.fill([A, B, C], "otSky")
        F.fill([A, C, D], "otGreen!16")
    else:
        F.fill([A, B, C, D], "otGreen!16")
    F.add(r"\fill[otNavy!14] %s circle (%s);" % (F.P(O), f(1.0 * F.k)))
    F.cercle(O, 1.0, "otNavy,line width=.8pt")
    F.seg(A, C, "geoTrait")
    if corr:
        F.seg(O, B, "otGreenDark,line width=1.4pt")
        F.seg(O, D, "otGreenDark,line width=1.4pt")
        legende(F, (0.0, -3.75), r"hauteurs des triangles $ABC$ et $ADC$ : $OB = OD = 2$ m", VE)
    else:
        F.seg(B, D, "geoTrait")
        F.seg(O, pol(O, 1.0, 45), "geoTrait")
        F.texte(pol(O, 1.12, 45), "1 m", "south west", "lab")
    F.poly([A, B, C, D])
    F.tick(A, O, 1, t=0.4)
    F.tick(O, C, 1, t=0.6)
    F.tick(B, O, 2, t=0.38)
    F.tick(O, D, 2, t=0.62)
    F.droit(O, C, D, 0.2)
    F.cote(A, C, "6 m", -2.95)
    if not corr:
        F.cote(B, D, "4 m", -4.5)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 180, "B": 270, "C": 0, "D": 90})
    F.pt(O, "O", 225, d=0.16)
    return F.code()


FIGURES["ex3023_enonce"] = ex3023(False)
FIGURES["ex3023_corrige"] = ex3023(True)

# FIN
