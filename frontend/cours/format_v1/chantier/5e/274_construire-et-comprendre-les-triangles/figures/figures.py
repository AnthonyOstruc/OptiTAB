# -*- coding: utf-8 -*-
r"""Figures de la notion « Construire et comprendre les triangles » (5e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = construction
et éléments de réponse (corrigés), orange = angles donnés. Les figures « à main levée »
des énoncés sont tracées d'un trait légèrement irrégulier et portent seulement les données.

Toutes les constructions sont calculées en vraie grandeur (cm réels, ou m pour les
situations concrètes), puis réduites d'un facteur k : DONNEES garde les coordonnées
réelles, contrôlées par verif_274.py (sympy). Outils géométriques et classe Fig repris
de la notion 282 (4e).
"""
import math

PREAMBULE_EXTRA = r"""
\usetikzlibrary{decorations.pathmorphing}
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  compas/.style={otGreenDark,line width=.7pt},
  constr/.style={otGreenDark,line width=.75pt},
  pointille/.style={otMuted,line width=.6pt,dash pattern=on 3pt off 2pt},
  rep/.style={otGreenDark,line width=1.1pt,line join=round},
  repTir/.style={otGreenDark,line width=.9pt,dash pattern=on 4pt off 2.5pt},
  main/.style={otNavy,line width=.9pt,line join=round,decorate,
    decoration={random steps,segment length=5pt,amplitude=.45pt}},
  rayon/.style={otOrange!90!black,line width=.75pt,dash pattern=on 3.5pt off 2pt},
}
"""

OR = "otOrange!90!black"
VE = "otGreenDark"
NA = "otNavy"
RG = "otRed!85!black"

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


def tri_ccc(AB, AC, BC, A=(0.0, 0.0), rot=0.0, haut=True):
    """A, B, C avec B à AB de A dans la direction rot, C du côté gauche (haut) de A→B."""
    x = (AB ** 2 + AC ** 2 - BC ** 2) / (2 * AB)
    y = math.sqrt(AC ** 2 - x ** 2) * (1 if haut else -1)
    r = math.radians(rot)
    B = (A[0] + AB * math.cos(r), A[1] + AB * math.sin(r))
    C = (A[0] + x * math.cos(r) - y * math.sin(r), A[1] + x * math.sin(r) + y * math.cos(r))
    return A, B, C


def tri_aca(B, L, angB, angC):
    """Côté [BC] horizontal de longueur L ; angles angB en B et angC en C ; renvoie (A, B, C)."""
    C = (B[0] + L, B[1])
    a = 180 - angB - angC
    BA = L * math.sin(math.radians(angC)) / math.sin(math.radians(a))
    return pol(B, BA, angB), B, C


def inter_droites(p1, d1, p2, d2):
    """Intersection des droites (p1, direction d1 en degrés) et (p2, direction d2)."""
    u = (math.cos(math.radians(d1)), math.sin(math.radians(d1)))
    v = (math.cos(math.radians(d2)), math.sin(math.radians(d2)))
    det = u[0] * (-v[1]) - u[1] * (-v[0])
    t = ((p2[0] - p1[0]) * (-v[1]) - (p2[1] - p1[1]) * (-v[0])) / det
    return (p1[0] + t * u[0], p1[1] + t * u[1])


def pied(p, a, b):
    ux, uy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / (ux * ux + uy * uy)
    return (a[0] + t * ux, a[1] + t * uy)


def centre_circ(A, B, C):
    ax, ay = A
    bx, by = B
    cx, cy = C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax - cx) + (cx ** 2 + cy ** 2) * (bx - ax)) / d
    return (ux, uy)


def orthocentre(A, B, C):
    return inter_droites(A, direc(B, C) + 90, B, direc(A, C) + 90)


def isometrie(pts, rot=0.0, miroir=False, dx=0.0, dy=0.0, ech=1.0):
    """Image de points : miroir (x → −x), rotation, homothétie ech, translation."""
    r = math.radians(rot)
    out = []
    for (x, y) in pts:
        if miroir:
            x = -x
        x, y = ech * x, ech * y
        out.append((x * math.cos(r) - y * math.sin(r) + dx, x * math.sin(r) + y * math.cos(r) + dy))
    return out


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

    def droite(self, p, q, t0=-0.2, t1=1.2, style="geoTrait"):
        self.seg(lerp(p, q, t0), lerp(p, q, t1), style)

    def cercle(self, c, r, style="compas"):
        self.add(r"\draw[%s] %s circle (%s);" % (style, self.P(c), f(r * self.k)))

    def compas(self, c, r, a_mil, demi=12, style="compas"):
        """Arc de compas de centre c, rayon r (réel), centré sur la direction a_mil (degrés)."""
        a1, a2 = a_mil - demi, a_mil + demi
        dep = pol(self.T(c), r * self.k, a1)
        self.add(r"\draw[%s] %s arc (%s:%s:%s);" % (style, self.Q(dep), f(a1), f(a2), f(r * self.k)))

    def compas_vers(self, c, p, demi=12, style="compas"):
        """Arc de compas de centre c passant par p."""
        self.compas(c, dist(c, p), direc(c, p), demi, style)

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
    def angle(self, o, p, q, r=0.42, txt=None, n=1, coul=OR, lr=None, plein=False, am=None):
        """Arc de l'angle saillant (o ; p, q), rayon r en cm ; texte sur la bissectrice (ou direction am)."""
        a1, a2 = direc(o, p), direc(o, q)
        sw = (a2 - a1) % 360
        if sw > 180:
            a1, a2 = a2, a1
            sw = 360 - sw
        a2 = a1 + sw
        O_ = self.T(o)
        if plein:
            self.add(r"\fill[%s,opacity=.18] %s -- %s arc (%s:%s:%s) -- cycle;"
                     % (coul, self.Q(O_), self.Q(pol(O_, r, a1)), f(a1), f(a2), f(r)))
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
            self.add(r"\node[lab,text=%s,anchor=center] at %s {%s};" % (coul, self.Q(q2), txt))

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


def cm(v):
    return "%s cm" % v


def vert(t):
    return r"\textcolor{otGreenDark}{%s}" % t


def legende(F, p, txt, coul="otMuted"):
    F.texte(p, txt, "north", "txt", coul, reel=False)



TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


# ====================================================================== COURS
# --- I. inégalité triangulaire : base fixe, deux arcs
def inegalite(cas, k, haut_ligne=None, noms=("A", "B")):
    """cas : (base, rayon depuis A, rayon depuis B, texte1, texte2, statut ok/plat/non)."""
    F = Fig(k)
    Lmax = max(c[0] for c in cas)
    y = 0.0
    for (L, a, b, t1, t2, st) in cas:
        A, B = (0.0, y), (L, y)
        if st == "ok":
            _, _, C = tri_ccc(L, a, b, A)
            F.fill([A, B, C], "otGreen!14")
            F.compas_vers(A, C, 14)
            F.compas_vers(B, C, 14)
            F.seg(A, C, "rep")
            F.seg(B, C, "rep")
            F.pt(C, None, coul=VE)
            coul = VE
        elif st == "plat":
            C = (a, y)
            F.compas(A, a, 0, 22)
            F.compas(B, b, 180, 22 if b > 3 else 30)
            F.pt(C, None, coul=OR)
            coul = OR
        else:
            F.compas(A, a, 38, 34, "otRed!80!black,line width=.7pt")
            F.compas(B, b, 142, 34, "otRed!80!black,line width=.7pt")
            coul = RG
        F.seg(A, B, "geoTrait,line width=1.1pt")
        F.pt(A, noms[0], 200)
        F.pt(B, noms[1], 340)
        xl = a / 2 if st == "plat" else L / 2
        F.add(r"\node[lab,anchor=north] at %s {%s};" % (F.Q((xl * k, y * k - 0.09)), cm(str(L).replace(".", ","))))
        F.add(r"\coordinate (t) at (%s,%s);" % (f(Lmax * k + 0.75), f(y * k + 0.42)))
        F.add(r"\node[lab,anchor=west] at (t) {%s};" % t1)
        F.add(r"\node[txt,text=%s,anchor=north west] at ($(t)+(0,-.28)$) {%s};" % (coul, t2))
        y -= haut_ligne
    return F


F = inegalite([(5, 3.5, 2.5, r"$3{,}5 + 2{,}5 > 5$", "triangle possible", "ok"),
               (5, 3, 2, r"$3 + 2 = 5$", "triangle aplati", "plat"),
               (5, 2.5, 2, r"$2{,}5 + 2 < 5$", "aucun triangle", "non")], 0.62, haut_ligne=3.9)
FIGURES["cours_inegalite"] = F.code()
DONNEES["cours_inegalite"] = {"A": (0, 0), "B": (5, 0), "C": tri_ccc(5, 3.5, 2.5)[2]}


# --- II. somme des angles (démonstration par la parallèle)
def somme_angles():
    F = Fig(1.0)
    B, C, A = (0, 0), (4.6, 0), (1.6, 2.8)
    G, D = (-0.8, 2.8), (5.4, 2.8)
    F.fill([A, B, C])
    F.seg(G, D, "geoTrait")
    F.poly([A, B, C])
    F.angle(B, C, A, 0.5, n=1, coul=OR, plein=True)
    F.angle(C, A, B, 0.5, n=2, coul=VE, plein=True)
    F.angle(A, B, C, 0.42, n=3, coul=NA)
    F.angle(A, G, B, 0.5, n=1, coul=OR, plein=True)
    F.angle(A, C, D, 0.5, n=2, coul=VE, plein=True)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.nom(D, "(d)", 0, 0.1)
    return F.code()


FIGURES["cours_somme_angles"] = somme_angles()


# --- II. triangles particuliers
def particuliers():
    F = Fig(1.0)
    B, C = (0, 0), (2.4, 0)
    A = (1.2, 2.2)
    F.fill([A, B, C])
    F.poly([A, B, C])
    F.tick(A, B, 2)
    F.tick(A, C, 2)
    F.angle(B, C, A, 0.4)
    F.angle(C, A, B, 0.4)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    legende(F, (1.2, -0.42), "isocèle en $A$")
    dx = 4.3
    B2, C2 = (dx, 0), (dx + 2.4, 0)
    A2 = (dx + 1.2, 2.4 * math.sqrt(3) / 2)
    F.fill([A2, B2, C2])
    F.poly([A2, B2, C2])
    for p, q in ((A2, B2), (B2, C2), (C2, A2)):
        F.tick(p, q, 1)
    F.angle(B2, C2, A2, 0.42, deg(60), lr=0.78)
    F.angle(C2, A2, B2, 0.42, deg(60), lr=0.78)
    F.angle(A2, B2, C2, 0.42, deg(60), lr=0.78)
    F.pts({"D": A2, "E": B2, "F": C2}, {"D": 90, "E": 200, "F": 340})
    legende(F, (dx + 1.2, -0.42), "équilatéral")
    dy = -3.6
    A3, B3, C3 = (0.2, dy), (2.6, dy), (0.2, dy + 1.7)
    F.fill([A3, B3, C3])
    F.poly([A3, B3, C3])
    F.droit(A3, B3, C3)
    F.pts({"R": A3, "S": B3, "T": C3}, {"R": 225, "S": 340, "T": 90})
    legende(F, (1.4, dy - 0.42), "rectangle en $R$")
    A4, B4, C4 = (dx + 0.3, dy), (dx + 2.3, dy), (dx + 0.3, dy + 2.0)
    F.fill([A4, B4, C4])
    F.poly([A4, B4, C4])
    F.droit(A4, B4, C4)
    F.tick(A4, B4, 1)
    F.tick(A4, C4, 1)
    F.angle(B4, A4, C4, 0.45, deg(45), lr=1.05)
    F.angle(C4, A4, B4, 0.45, deg(45), lr=1.05)
    F.pts({"K": A4, "L": B4, "M": C4}, {"K": 225, "L": 340, "M": 90})
    legende(F, (dx + 1.3, dy - 0.42), "rectangle isocèle en $K$")
    return F.code()


FIGURES["cours_particuliers"] = particuliers()


# --- III. les trois constructions
def construction_ccc(AB, AC, BC, k, noms="ABC", txt=None, second=False):
    A, B, C = tri_ccc(AB, AC, BC)
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.compas_vers(A, C, 9)
    F.compas_vers(B, C, 9)
    if second:
        C2 = (C[0], -C[1])
        F.compas_vers(A, C2, 9)
        F.compas_vers(B, C2, 9)
        F.seg(A, C2, "repTir")
        F.seg(B, C2, "repTir")
        F.pt(C2, noms[2] + "'", 270, coul=VE, d=0.2)
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.seg(A, C, "rep")
    F.seg(B, C, "rep")
    a, b, c = noms
    t = txt or (cm(AB), cm(AC), cm(BC))
    F.lcote(A, B, t[0], C if not second else (C[0], C[1] * 3), d=0.13)
    F.lcote(A, C, vert(t[1]), B, t=0.42)
    F.lcote(B, C, vert(t[2]), A, t=0.42)
    F.pt(A, a, 200)
    F.pt(B, b, 340)
    F.pt(C, c, 90, coul=VE, d=0.26)
    return F, (A, B, C)


F, (L_, M_, N_) = construction_ccc(5.5, 4.5, 3, 0.85, noms="LMN", txt=("5,5 cm", "4,5 cm", "3 cm"))
DONNEES["cours_ccc"] = {"L": L_, "M": M_, "N": N_}
FIGURES["cours_ccc"] = F.code()


def construction_cac(AB, AC, ang, k, noms="ABC", txt=None, mesure=None, droit=False):
    a, b, c = noms
    A, B = (0.0, 0.0), (AB, 0.0)
    C = pol(A, AC, ang)
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.seg(A, pol(A, AC * 1.3, ang), "constr")
    F.compas_vers(A, C, 8)
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.seg(B, C, "rep")
    if droit:
        F.droit(A, B, C, 0.24, OR)
    else:
        F.angle(A, B, C, 0.5, deg(ang), coul=OR)
    t = txt or (cm(AB), cm(AC))
    F.lcote(A, B, t[0], C)
    F.lcote(A, C, vert(t[1]), B, t=0.45)
    if mesure:
        F.lcote(B, C, vert(mesure), A, t=0.5)
    F.pt(A, a, 200 if ang < 80 else 225)
    F.pt(B, b, 340)
    F.pt(C, c, ang + 45 if ang < 80 else 45, coul=VE, d=0.26)
    return F, (A, B, C)


F, (R_, S_, T_) = construction_cac(5, 3.5, 40, 0.85, noms="RST", txt=("5 cm", "3,5 cm"))
DONNEES["cours_cac"] = {"R": R_, "S": S_, "T": T_}
FIGURES["cours_cac"] = F.code()


def construction_aca(BC, angB, angC, k, noms="ABC", txt=None, mesures=None, angle_sommet=None,
                     coul_angles=(OR, OR)):
    """Côté [BC] horizontal ; noms = (sommet construit, extrémité gauche, extrémité droite)."""
    A, B, C = tri_aca((0.0, 0.0), BC, angB, angC)
    a, b, c = noms
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.seg(B, lerp(B, A, 1.28), "constr")
    F.seg(C, lerp(C, A, 1.28), "constr")
    F.seg(B, C, "geoTrait,line width=1.1pt")
    tB = deg(angB) if coul_angles[0] == OR else vert(deg(angB))
    tC = deg(angC) if coul_angles[1] == OR else vert(deg(angC))
    F.angle(B, C, A, 0.55, tB, coul=coul_angles[0])
    F.angle(C, A, B, 0.55, tC, coul=coul_angles[1])
    if angle_sommet:
        F.angle(A, B, C, 0.4, angle_sommet[0], coul=angle_sommet[1])
    F.lcote(B, C, txt or cm(BC), A)
    if mesures:
        F.lcote(B, A, vert(mesures[0]), C, t=0.42)
        F.lcote(C, A, vert(mesures[1]), B, t=0.42)
    F.pt(B, b, 200)
    F.pt(C, c, 340)
    F.pt(A, a, (angB + 180 - angC) / 2, coul=VE, d=0.22)
    return F, (A, B, C)


F, (K_, I_, J_) = construction_aca(5, 35, 70, 0.85, noms="KIJ", txt="5 cm")
DONNEES["cours_aca"] = {"I": I_, "J": J_, "K": K_}
FIGURES["cours_aca"] = F.code()


# --- IV. médiatrice au compas
def mediatrice_cours():
    F = Fig(1.0)
    A, B = (0.0, 0.0), (4.4, 0.0)
    r = 3.0
    I = (2.2, 0.0)
    h = math.sqrt(r * r - 2.2 ** 2)
    P1, P2 = (2.2, h), (2.2, -h)
    M = (2.2, 1.25)
    for c in (A, B):
        F.compas_vers(c, P1, 9)
        F.compas_vers(c, P2, 9)
    F.seg((2.2, -h - 0.45), (2.2, h + 0.55), "rep")
    F.seg(M, A, "repTir")
    F.seg(M, B, "repTir")
    F.tick(M, A, 2, VE)
    F.tick(M, B, 2, VE)
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.tick(A, I, 1)
    F.tick(I, B, 1)
    F.droit(I, B, P1, 0.2, VE)
    F.pt(A, "A", 180)
    F.pt(B, "B", 0)
    F.pt(I, "I", 225, d=0.17)
    F.pt(M, "M", 15, coul=VE, d=0.16)
    F.pt(P1, None, coul=VE)
    F.pt(P2, None, coul=VE)
    F.nom((2.2, -h - 0.45), r"\text{médiatrice de } [AB]", 0, 0.12, VE)
    return F.code()


FIGURES["cours_mediatrice"] = mediatrice_cours()


# --- IV. cercle circonscrit
def cercle_circonscrit(A, B, C, k, noms="ABC", ret=False, codes=True):
    F = Fig(k)
    O = centre_circ(A, B, C)
    R = dist(O, A)
    F.fill([A, B, C])
    F.cercle(O, R, "otGreenDark,line width=.95pt")
    for (p, q) in ((A, B), (B, C), (C, A)):
        d = direc(p, q) + 90
        L = R + 0.55 / k
        F.seg(pol(O, L, d), pol(O, -L, d), "rep,line width=.8pt")
    if codes:
        for (p, q, n) in ((A, B, 1), (B, C, 2), (C, A, 3)):
            m = lerp(p, q, 0.5)
            F.tick(p, m, n, NA)
            F.tick(m, q, n, NA)
            F.droit(m, q, O if dist(m, O) > 0.3 / k else pol(m, 1, direc(p, q) + 90), 0.17, VE)
    F.poly([A, B, C])
    g = centre(A, B, C)
    a, b, c = noms
    F.pts({a: A, b: B, c: C}, None, g)
    dirs = []
    for (p, q) in ((A, B), (B, C), (C, A)):
        dirs += [direc(p, q) + 90, direc(p, q) - 90]
    if dist(O, lerp(B, C, 0.5)) > 0.2 / k:
        F.pt(O, "O", angle_libre(dirs), coul=VE, d=0.2)
    if ret:
        return F, O, R
    return F.code()


A, B, C = (0.0, 0.0), (5.0, 0.0), (1.6, 3.4)
FIGURES["cours_cercle"] = cercle_circonscrit(A, B, C, 0.8)
DONNEES["cours_cercle"] = {"A": A, "B": B, "C": C, "O": centre_circ(A, B, C)}


def cercle_rectangle():
    """Triangle EFG rectangle en E : le centre du cercle circonscrit est le milieu de l'hypoténuse."""
    F = Fig(0.9)
    E, Fp, G = (0.0, 0.0), (5.0, 0.0), None
    # E sur le cercle de diamètre [FG] : F(0,0), G(5,0), E au-dessus
    Fp, G = (0.0, 0.0), (5.0, 0.0)
    O = (2.5, 0.0)
    E = pol(O, 2.5, 118)
    F.fill([E, Fp, G])
    F.cercle(O, 2.5, "otGreenDark,line width=.95pt")
    F.poly([E, Fp, G])
    F.seg(Fp, G, "geoTrait,line width=1.1pt")
    F.droit(E, Fp, G)
    F.tick(Fp, O, 1, VE)
    F.tick(O, G, 1, VE)
    F.seg(O, E, "repTir")
    F.tick(O, E, 1, VE, t=0.45)
    F.pts({"E": E, "F": Fp, "G": G}, {"E": 118, "F": 180, "G": 0})
    F.pt(O, "O", 270, coul=VE, d=0.18)
    DONNEES["cours_cercle_rect"] = {"E": E, "F": Fp, "G": G, "O": O}
    return F.code()


FIGURES["cours_cercle_rect"] = cercle_rectangle()


# --- V. hauteurs
def hauteurs_cours():
    F = Fig(1.0)
    A, B, C = (1.1, 2.7), (0.0, 0.0), (3.6, 0.0)
    H = orthocentre(A, B, C)
    F.fill([A, B, C])
    for (s, p, q) in ((A, B, C), (B, C, A), (C, A, B)):
        K = pied(s, p, q)
        F.seg(s, K, "rep,line width=.85pt")
        F.droit(K, q if dist(K, q) > 0.3 else p, s, 0.17, VE)
    F.poly([A, B, C])
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, None, coul=VE)
    legende(F, (1.8, -0.45), "les trois hauteurs sont concourantes")
    dx, dy = 1.4, -3.3
    D, E, Fp = (dx - 1.0, dy + 1.9), (dx, dy), (dx + 2.6, dy)
    K = (D[0], dy)
    F.fill([D, E, Fp])
    F.seg(K, E, "pointille")
    F.seg(D, K, "rep,line width=.85pt")
    F.droit(K, E, D, 0.17, VE)
    F.poly([D, E, Fp])
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 300, "F": 340})
    F.pt(K, "K", 225, coul=VE, d=0.16)
    legende(F, (dx + 0.6, dy - 0.58), "hauteur issue de $D$ à l'extérieur")
    DONNEES["cours_hauteurs"] = {"A": A, "B": B, "C": C, "H": H, "D": D, "E": E, "F": Fp, "K": K}
    return F.code()


FIGURES["cours_hauteurs"] = hauteurs_cours()


# --- V. aire : le triangle est la moitié d'un rectangle
def aire_cours():
    F = Fig(0.75)
    B, C, A = (0.0, 0.0), (6.0, 0.0), (2.0, 3.5)
    H = (2.0, 0.0)
    P, Q = (0.0, 3.5), (6.0, 3.5)
    F.fill([B, H, A], "otSky")
    F.fill([H, C, A], "otGreen!16")
    F.poly([B, C, Q, P], "pointille")
    F.seg(B, A, "otNavy!45,line width=.6pt")
    F.poly([A, B, C])
    F.seg(A, H, "rep")
    F.droit(H, C, A, 0.2, VE)
    F.cote(B, C, "base", -0.5)
    F.lcote(A, H, vert("hauteur"), B, t=0.5, d=0.1)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 300, coul=VE, d=0.17)
    DONNEES["cours_aire"] = {"A": A, "B": B, "C": C, "H": H}
    return F.code()


FIGURES["cours_aire"] = aire_cours()


# --- VI. médianes
def medianes_cours():
    F = Fig(0.8)
    B, C, A = (0.0, 0.0), (6.0, 0.0), (2.2, 3.6)
    M = (3.0, 0.0)
    H = (2.2, 0.0)
    F.fill([A, B, M], "otSky")
    F.fill([A, M, C], "otGreen!16")
    F.seg(A, H, "pointille")
    F.droit(H, C, A, 0.18, NA)
    F.poly([A, B, C])
    F.seg(A, M, "rep")
    F.tick(B, M, 1)
    F.tick(M, C, 1)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(M, "M", 270, coul=VE, d=0.17)
    F.pt(H, "H", 270, d=0.17)
    DONNEES["cours_mediane_aire"] = {"A": A, "B": B, "C": C, "M": M, "H": H}
    return F.code()


def medianes_G():
    F = Fig(0.8)
    dx = 0.0
    D, E, Fp = (dx + 1.2, 3.6), (dx, 0.0), (dx + 5.6, 0.0)
    G = centre(D, E, Fp)
    F.fill([D, E, Fp])
    for (s, p, q, n) in ((D, E, Fp, 1), (E, Fp, D, 2), (Fp, D, E, 3)):
        m = lerp(p, q, 0.5)
        F.seg(s, m, "rep,line width=.85pt")
        F.tick(p, m, n)
        F.tick(m, q, n)
    F.poly([D, E, Fp])
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 200, "F": 340})
    F.pt(G, "G", 0, coul=VE, d=0.2)
    DONNEES["cours_medianes_G"] = {"D": D, "E": E, "F": Fp, "G": G}
    return F.code()


FIGURES["cours_mediane_aire"] = medianes_cours()
FIGURES["cours_medianes_G"] = medianes_G()


# ====================================================================== EXERCICES
def esquisse(pts, cotes, angles=(), noms_ang=None, k=1.0, seed=7, droits=(), ticks=(), legende_y=None):
    """Figure à main levée : seulement les données (côtés, angles, codages)."""
    F = Fig(k, seed)
    g = centre(*pts.values())
    F.poly(list(pts.values()), "main")
    for (n1, n2, txt) in cotes:
        F.lcote(pts[n1], pts[n2], txt, g)
    for (s, p, q, txt) in angles:
        F.angle(pts[s], pts[p], pts[q], 0.45, txt, coul=OR)
    for (s, p, q) in droits:
        F.droit(pts[s], pts[p], pts[q])
    for (p, q, n) in ticks:
        F.tick(pts[p], pts[q], n)
    for n, p in pts.items():
        a = (noms_ang or {}).get(n)
        F.pt(p, n, a if a is not None else direc(g, p))
    ymin = min(p[1] for p in pts.values()) * k
    xm = (min(p[0] for p in pts.values()) + max(p[0] for p in pts.values())) / 2 * k
    legende(F, (xm, ymin - 0.55 if legende_y is None else legende_y), "figure à main levée")
    return F.code()


# --- 2980 : trois longueurs
FIGURES["ex2980_enonce"] = esquisse({"A": (0, 0), "B": (4.6, 0), "C": (1.9, 2.5)},
                                    [("A", "B", "6 cm"), ("A", "C", "4 cm"), ("B", "C", "5 cm")],
                                    noms_ang={"A": 200, "B": 340, "C": 90})
F = inegalite([(7, 4, 5, r"a) $4 + 5 > 7$", "triangle possible", "ok"),
               (8, 3, 4, r"b) $3 + 4 < 8$", "aucun triangle", "non"),
               (6, 2.5, 3.5, r"c) $2{,}5 + 3{,}5 = 6$", "triangle aplati", "plat")], 0.42, haut_ligne=6.4)
FIGURES["ex2980_corrige1"] = F.code()
DONNEES["ex2980_corrige1"] = {"C_a": tri_ccc(7, 4, 5)[2]}
F, (A, B, C) = construction_ccc(6, 4, 5, 0.75, second=True)
DONNEES["ex2980"] = {"A": A, "B": B, "C": C, "C'": (C[0], -C[1])}
FIGURES["ex2980_corrige2"] = F.code()


# --- 2984 : somme des angles et triangles particuliers
def ex2984(corr):
    F = Fig(0.82)
    rep = {}

    def val(v):
        return vert(deg(v)) if corr else r"$?$"

    # a) ABC : A = 47, B = 68 -> C = 65 ([BC] horizontal)
    A, B, C = tri_aca((0.0, 0.0), 2.9, 68, 65)
    F.fill([A, B, C])
    F.poly([A, B, C])
    F.angle(B, C, A, 0.42, deg(68))
    F.angle(A, B, C, 0.42, deg(47))
    F.angle(C, A, B, 0.42, val(65), coul=VE if corr else OR)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    legende(F, (1.45 * 0.82, -0.42), "a)")
    rep["a"] = (A, B, C)
    # b) DEF rectangle en D : E = 34 -> F = 56 ([EF] horizontal)
    dx = 4.3
    D, E, Fp = tri_aca((dx, 0.0), 3.4, 34, 56)
    F.fill([D, E, Fp])
    F.poly([D, E, Fp])
    F.droit(D, E, Fp, 0.2)
    F.angle(E, Fp, D, 0.55, deg(34))
    F.angle(Fp, D, E, 0.42, val(56), coul=VE if corr else OR)
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 200, "F": 340})
    legende(F, ((dx + 1.7) * 0.82, -0.42), "b)")
    rep["b"] = (D, E, Fp)
    # c) GHI isocèle en G : G = 40 -> H = I = 70
    dy = -5.0
    G, H, I = tri_aca((0.3, dy), 2.3, 70, 70)
    F.fill([G, H, I])
    F.poly([G, H, I])
    F.tick(G, H, 2)
    F.tick(G, I, 2)
    F.angle(G, H, I, 0.42, deg(40))
    F.angle(H, I, G, 0.42, val(70), coul=VE if corr else OR)
    F.angle(I, G, H, 0.42, val(70), coul=VE if corr else OR)
    F.pts({"G": G, "H": H, "I": I}, {"G": 90, "H": 200, "I": 340})
    legende(F, (1.45 * 0.82, (dy - 0.5) * 0.82), "c)")
    rep["c"] = (G, H, I)
    # d) JKL isocèle en J : K = 52 -> L = 52, J = 76
    J, K, L = tri_aca((dx, dy), 3.4, 52, 52)
    F.fill([J, K, L])
    F.poly([J, K, L])
    F.tick(J, K, 2)
    F.tick(J, L, 2)
    F.angle(K, L, J, 0.42, deg(52))
    F.angle(L, J, K, 0.42, val(52), coul=VE if corr else OR)
    F.angle(J, K, L, 0.42, val(76), coul=VE if corr else OR)
    F.pts({"J": J, "K": K, "L": L}, {"J": 90, "K": 200, "L": 340})
    legende(F, ((dx + 1.7) * 0.82, (dy - 0.5) * 0.82), "d)")
    rep["d"] = (J, K, L)
    DONNEES["ex2984"] = rep
    return F.code()


FIGURES["ex2984_enonce"] = ex2984(False)
FIGURES["ex2984_corrige"] = ex2984(True)


# --- 2981 : deux côtés et l'angle compris
FIGURES["ex2981_enonce"] = esquisse({"D": (0, 0), "E": (4.4, 0), "F": (2.0, 2.5)},
                                    [("D", "E", "5,5 cm"), ("D", "F", "4 cm")],
                                    angles=[("D", "E", "F", deg(50))],
                                    noms_ang={"D": 200, "E": 340, "F": 90})
F, (D_, E_, F_) = construction_cac(5.5, 4, 50, 0.8, noms="DEF", txt=("5,5 cm", "4 cm"),
                                   mesure=r"$\approx 4{,}2$ cm")
DONNEES["ex2981"] = {"D": D_, "E": E_, "F": F_}
FIGURES["ex2981_corrige1"] = F.code()


def ex2981_iso():
    F = Fig(1.15)
    A, B = (0.0, 0.0), (4.0, 0.0)
    C = pol(A, 4.0, 30)
    F.fill([A, B, C], "otGreen!12")
    F.seg(A, pol(A, 5.0, 30), "constr")
    F.compas_vers(A, C, 8)
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.seg(B, C, "rep")
    F.angle(A, B, C, 0.8, deg(30), coul=OR)
    F.angle(B, C, A, 0.45, vert(deg(75)), coul=VE)
    F.angle(C, A, B, 0.45, vert(deg(75)), coul=VE)
    F.tick(A, B, 2)
    F.tick(A, C, 2, VE)
    F.lcote(A, B, "4 cm", C, t=0.32)
    F.lcote(A, C, vert("4 cm"), B, t=0.32)
    F.pt(A, "A", 200)
    F.pt(B, "B", 300)
    F.pt(C, "C", 75, coul=VE, d=0.2)
    DONNEES["ex2981_iso"] = {"A": A, "B": B, "C": C}
    return F.code()


FIGURES["ex2981_corrige2"] = ex2981_iso()


# --- 2978 : calculer un angle avant de construire
# AUG : AU = 5, A = 40, G = 75 -> U = 65 ; EFG isocèle en E : FG = 5, E = 70 -> F = G = 55
G0, A0, U0 = tri_aca((0.0, 0.0), 5, 40, 65)
FIGURES["ex2978_enonce1"] = esquisse({"A": (0, 0), "U": (3.9, 0), "G": (2.9, 2.35)},
                                     [("A", "U", "5 cm")],
                                     angles=[("A", "U", "G", deg(40)), ("G", "A", "U", deg(75))],
                                     noms_ang={"A": 200, "U": 340, "G": 80})
FIGURES["ex2978_enonce2"] = esquisse({"F": (0, 0), "G": (3.8, 0), "E": (1.9, 2.6)},
                                     [("F", "G", "5 cm")],
                                     angles=[("E", "F", "G", deg(70))],
                                     ticks=[("E", "F", 2), ("E", "G", 2)],
                                     noms_ang={"F": 200, "G": 340, "E": 90})
F, (G_, A_, U_) = construction_aca(5, 40, 65, 0.85, noms="GAU", txt="5 cm",
                                   mesures=(r"$\approx 4{,}7$ cm", r"$\approx 3{,}3$ cm"),
                                   angle_sommet=(vert(deg(75)), VE), coul_angles=(OR, VE))
DONNEES["ex2978_AUG"] = {"A": A_, "U": U_, "G": G_}
FIGURES["ex2978_corrige1"] = F.code()
F, (E_, F2_, G2_) = construction_aca(5, 55, 55, 0.85, noms="EFG", txt="5 cm",
                                     angle_sommet=(deg(70), OR), coul_angles=(VE, VE))
F.tick(E_, F2_, 2, VE)
F.tick(E_, G2_, 2, VE)
DONNEES["ex2978_EFG"] = {"E": E_, "F": F2_, "G": G2_}
FIGURES["ex2978_corrige2"] = F.code()


# --- 2991 : hauteurs et aire
A91, B91, C91 = (4.0, 4.0), (0.0, 0.0), (7.0, 0.0)
D91, E91, F91 = (-1.5, 3.0), (0.0, 0.0), (4.0, 0.0)


def ex2991_enonce():
    F = Fig(0.85)
    A, B, C = A91, B91, C91
    F.fill([A, B, C])
    F.poly([A, B, C])
    F.lcote(B, C, "7 cm", A)
    F.lcote(A, C, "5 cm", B)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    return F.code()


def ex2991_enonce2():
    F = Fig(0.85)
    D, E, Fp = D91, E91, F91
    F.fill([D, E, Fp])
    F.poly([D, E, Fp])
    F.lcote(E, Fp, "4 cm", D)
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 270, "F": 340})
    return F.code()


def ex2991_corrige1():
    F = Fig(0.85)
    A, B, C = A91, B91, C91
    H = pied(A, B, C)
    K = pied(B, A, C)
    L = pied(C, A, B)
    O = orthocentre(A, B, C)
    DONNEES["ex2991"] = {"A": A, "B": B, "C": C, "H": H, "K": K, "L": L, "Orth": O}
    F.fill([A, B, C])
    F.seg(A, H, "rep")
    F.seg(B, K, "rep")
    F.seg(C, L, "rep")
    F.droit(H, C, A, 0.2, VE)
    F.droit(K, C, B, 0.2, VE)
    F.droit(L, B, C, 0.2, VE)
    F.poly([A, B, C])
    F.lcote(A, H, vert("4 cm"), B, t=0.72, d=0.1)
    F.lcote(B, K, vert("5,6 cm"), A, t=0.36, d=0.1)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 270, coul=VE, d=0.16)
    F.pt(K, "K", 40, coul=VE, d=0.16)
    F.pt(L, "L", 135, coul=VE, d=0.16)
    F.pt(O, None, coul=VE)
    return F.code()


def ex2991_corrige2():
    F = Fig(0.85)
    D, E, Fp = D91, E91, F91
    K = (D[0], 0.0)
    DONNEES["ex2991b"] = {"D": D, "E": E, "F": Fp, "K": K}
    F.fill([D, E, Fp])
    F.seg(K, E, "pointille")
    F.seg(D, K, "rep")
    F.droit(K, E, D, 0.2, VE)
    F.poly([D, E, Fp])
    F.lcote(D, K, vert("3 cm"), E, t=0.5, d=0.1)
    F.lcote(E, Fp, "4 cm", D)
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 300, "F": 340})
    F.pt(K, "K", 225, coul=VE, d=0.16)
    return F.code()


FIGURES["ex2991_enonce1"] = ex2991_enonce()
FIGURES["ex2991_enonce2"] = ex2991_enonce2()
FIGURES["ex2991_corrige1"] = ex2991_corrige1()
FIGURES["ex2991_corrige2"] = ex2991_corrige2()


# --- 2987 : médiatrices et cercle circonscrit
FIGURES["ex2987_enonce1"] = esquisse({"A": (0, 0), "B": (4.8, 0), "C": (1.9, 2.8)},
                                     [("A", "B", "7 cm"), ("A", "C", "5 cm"), ("B", "C", "6 cm")],
                                     noms_ang={"A": 200, "B": 340, "C": 90})
FIGURES["ex2987_enonce2"] = esquisse({"R": (0, 0), "S": (2.6, 0), "T": (0, 3.2)},
                                     [("R", "S", "3 cm"), ("R", "T", "4 cm")],
                                     droits=[("R", "S", "T")],
                                     noms_ang={"R": 225, "S": 340, "T": 90})


def mediatrice_arcs(F, p, q, r):
    """Arcs de compas (rayon r) de la médiatrice de [pq], de part et d'autre."""
    m = lerp(p, q, 0.5)
    h = math.sqrt(r * r - (dist(p, q) / 2) ** 2)
    d = direc(p, q) + 90
    for P_ in (pol(m, h, d), pol(m, -h, d)):
        F.compas_vers(p, P_, 7)
        F.compas_vers(q, P_, 7)
        F.pt(P_, None, coul=VE)
    return pol(m, h, d), pol(m, -h, d)


def ex2987_corrige1():
    A, B, C = tri_ccc(7, 5, 6)
    O = centre_circ(A, B, C)
    R = dist(O, A)
    k = 0.7
    F = Fig(k)
    F.fill([A, B, C])
    F.cercle(O, R, "otGreenDark,line width=.95pt")
    # médiatrices de [AB] et [AC] construites au compas, la troisième en tirets
    for (p, q, r) in ((A, B, 5.3), (B, C, 4.84)):
        P1, P2 = mediatrice_arcs(F, p, q, r)
        F.seg(lerp(P1, P2, -0.08), lerp(P1, P2, 1.08), "rep,line width=.8pt")
    d = direc(A, C) + 90
    F.seg(pol(O, R + 0.6, d), pol(O, -(R + 0.6), d), "repTir,line width=.8pt")
    for (p, q, n) in ((A, B, 1), (A, C, 2), (B, C, 3)):
        m = lerp(p, q, 0.5)
        F.tick(p, m, n, NA)
        F.tick(m, q, n, NA)
    F.poly([A, B, C])
    F.pts({"A": A, "B": B, "C": C}, {"A": 200, "B": 340, "C": 100})
    dirs = []
    for (p, q) in ((A, B), (B, C), (C, A)):
        dirs += [direc(p, q) + 90, direc(p, q) - 90]
    F.pt(O, "O", angle_libre(dirs), coul=VE, d=0.2)
    DONNEES["ex2987"] = {"A": A, "B": B, "C": C, "O": O, "R": R}
    return F.code()


def ex2987_corrige2():
    R_, S_, T_ = (0.0, 0.0), (3.0, 0.0), (0.0, 4.0)
    O = lerp(S_, T_, 0.5)
    k = 0.75
    F = Fig(k)
    F.fill([R_, S_, T_])
    F.cercle(O, 2.5, "otGreenDark,line width=.95pt")
    for (p, q) in ((R_, S_), (R_, T_)):
        m = lerp(p, q, 0.5)
        d = direc(p, q) + 90
        F.seg(pol(m, -0.6, d), pol(m, dist(m, O) + 1.0, d), "rep,line width=.8pt")
        F.tick(p, m, 1 if p == R_ and q == S_ else 2, NA)
        F.tick(m, q, 1 if p == R_ and q == S_ else 2, NA)
    F.poly([R_, S_, T_])
    F.droit(R_, S_, T_, 0.22)
    F.tick(S_, O, 3, VE)
    F.tick(O, T_, 3, VE)
    F.pts({"R": R_, "S": S_, "T": T_}, {"R": 225, "S": 300, "T": 135})
    F.pt(O, "O", 30, coul=VE, d=0.2)
    DONNEES["ex2987_RST"] = {"R": R_, "S": S_, "T": T_, "O": O}
    return F.code()


FIGURES["ex2987_corrige1"] = ex2987_corrige1()
FIGURES["ex2987_corrige2"] = ex2987_corrige2()


# --- 2982 : partager un champ (mètres, k petit)
A82, B82, C82 = (30.0, 40.0), (0.0, 0.0), (90.0, 0.0)
H82, M82 = (30.0, 0.0), (45.0, 0.0)
K82 = 0.07


def ex2982_enonce():
    F = Fig(K82)
    A, B, C, H, M = A82, B82, C82, H82, M82
    F.fill([A, B, C])
    F.seg(A, H, "pointille")
    F.droit(H, C, A, 0.18)
    F.poly([A, B, C])
    F.seg(A, M)
    F.tick(B, M, 1)
    F.tick(M, C, 1)
    F.cote(B, C, "90 m", -0.62)
    F.lcote(A, H, "40 m", C, t=0.5, d=0.1)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 290, d=0.16)
    F.pt(M, "M", 290, d=0.16)
    return F.code()


def ex2982_hauteur():
    F = Fig(K82)
    A, B, C, H = A82, B82, C82, H82
    F.fill([A, B, H], "otSky")
    F.fill([A, H, C], "otOrange!18")
    F.poly([A, B, C])
    F.seg(A, H, "geoTrait")
    F.droit(H, C, A, 0.18)
    F.texte((19, 12), r"$600\ \text{m}^2$", "center")
    F.texte((55, 13), r"$1\,200\ \text{m}^2$", "center")
    F.lcote(B, H, "30 m", A)
    F.lcote(H, C, "60 m", A)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, None)
    F.nom(H, "H", 300, 0.16)
    return F.code()


def ex2982_mediane():
    F = Fig(K82)
    A, B, C, H, M = A82, B82, C82, H82, M82
    F.fill([A, B, M], "otSky")
    F.fill([A, M, C], "otGreen!16")
    F.seg(A, H, "pointille")
    F.droit(H, C, A, 0.18)
    F.poly([A, B, C])
    F.seg(A, M, "rep")
    F.tick(B, M, 1)
    F.tick(M, C, 1)
    F.texte((58, 12), vert(r"$900\ \text{m}^2$"), "center")
    F.texte((15, 9), r"$900\ \text{m}^2$", "center")
    F.lcote(B, M, "45 m", A, t=0.62)
    F.lcote(M, C, "45 m", A)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 120, d=0.16)
    F.pt(M, "M", 290, coul=VE, d=0.16)
    return F.code()


def ex2982_trois():
    F = Fig(K82)
    A, B, C = A82, B82, C82
    P, Q = (30.0, 0.0), (60.0, 0.0)
    F.fill([A, B, P], "otSky")
    F.fill([A, P, Q], "otGreen!16")
    F.fill([A, Q, C], "otSky")
    F.poly([A, B, C])
    F.seg(A, P, "rep")
    F.seg(A, Q, "rep")
    for (p, q) in ((B, P), (P, Q), (Q, C)):
        F.tick(p, q, 1)
    F.texte((19, 12), r"$600\ \text{m}^2$", "center")
    F.texte((40, 10), vert(r"$600\ \text{m}^2$"), "center")
    F.texte((65, 9), r"$600\ \text{m}^2$", "center")
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(P, "P", 270, coul=VE, d=0.16)
    F.pt(Q, "Q", 270, coul=VE, d=0.16)
    return F.code()


def ex2982_medianes():
    F = Fig(K82)
    A, B, C = A82, B82, C82
    G = centre(A, B, C)
    DONNEES["ex2982"] = {"A": A, "B": B, "C": C, "H": H82, "M": M82, "G": G}
    F.fill([A, B, C])
    for (s, p, q, n) in ((A, B, C, 1), (B, C, A, 2), (C, A, B, 3)):
        m = lerp(p, q, 0.5)
        F.seg(s, m, "rep,line width=.85pt")
        F.tick(p, m, n)
        F.tick(m, q, n)
    F.poly([A, B, C])
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    dirs = [direc(G, A), direc(G, B), direc(G, C)] + [direc(G, lerp(p, q, 0.5)) for (p, q) in ((A, B), (B, C), (C, A))]
    F.pt(G, "G", angle_libre(dirs), coul=VE, d=0.2)
    return F.code()


FIGURES["ex2982_enonce"] = ex2982_enonce()
FIGURES["ex2982_hauteur"] = ex2982_hauteur()
FIGURES["ex2982_mediane"] = ex2982_mediane()
FIGURES["ex2982_trois"] = ex2982_trois()
FIGURES["ex2982_medianes"] = ex2982_medianes()


# --- 2994 : jardin rectangulaire (mètres)
A94, B94, C94, D94 = (0.0, 0.0), (12.0, 0.0), (12.0, 8.0), (0.0, 8.0)
M94, M2_94, K94, N94 = (4.0, 8.0), (9.0, 8.0), (4.0, 0.0), (12.0, 3.0)
K94F = 0.48


def ex2994(cas):
    F = Fig(K94F)
    A, B, C, D, M = A94, B94, C94, D94, M94
    if cas == "enonce":
        F.fill([A, B, M], "otSky")
    elif cas == "c1":
        F.fill([A, B, M], "otSky")
    else:
        F.fill([A, B, N94], "otGreen!16")
    F.poly([A, B, C, D])
    if cas in ("enonce", "c1"):
        F.seg(A, M)
        F.seg(B, M)
    if cas == "c1":
        F.seg(A, M2_94, "repTir")
        F.seg(B, M2_94, "repTir")
        F.seg(M, K94, "rep")
        F.droit(K94, B, M, 0.2, VE)
        F.lcote(M, K94, vert("8 m"), A, t=0.62, d=0.1)
        F.pt(K94, "K", 270, coul=VE, d=0.16)
        F.pt(M2_94, "M'", 90, coul=VE, d=0.16)
    if cas == "c2":
        F.seg(A, N94, "rep")
        F.lcote(B, N94, vert("3 m"), A, t=0.5)
        F.pt(N94, "N", 0, coul=VE, d=0.16)
    for (s, p, q) in ((A, B, D), (B, C, A), (C, D, B), (D, A, C)):
        F.droit(s, p, q, 0.2)
    F.cote(A, B, "12 m", -0.55)
    F.lcote(B, C, "8 m", A, t=0.75 if cas == "c2" else 0.5)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 200, "B": 340, "C": 20, "D": 160})
    if cas != "c2":
        F.pt(M, "M", 90, d=0.14)
    if cas == "enonce":
        F.cote(D, M, "4 m", 0.8)
    return F.code()


FIGURES["ex2994_enonce"] = ex2994("enonce")
FIGURES["ex2994_corrige1"] = ex2994("c1")
FIGURES["ex2994_corrige2"] = ex2994("c2")
DONNEES["ex2994"] = {"A": A94, "B": B94, "C": C94, "D": D94, "M": M94, "M'": M2_94, "K": K94, "N": N94}


# --- 2998 : angle extérieur, isocèle en A
B98, C98 = (0.0, 0.0), (4.0, 0.0)
A98 = (2.0, 2.0 * math.tan(math.radians(56)))
D98 = (6.4, 0.0)


def ex2998(corr):
    F = Fig(0.9)
    A, B, C, D = A98, B98, C98, D98
    F.fill([A, B, C])
    F.seg(C, D, "geoTrait")
    F.poly([A, B, C])
    F.tick(A, B, 2)
    F.tick(A, C, 2)
    F.angle(C, D, A, 0.45, deg(124), coul=OR)
    if corr:
        F.angle(C, A, B, 0.45, vert(deg(56)), coul=VE)
        F.angle(B, C, A, 0.45, vert(deg(56)), coul=VE)
        F.angle(A, B, C, 0.45, vert(deg(68)), coul=VE)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 90, "B": 200, "C": 270, "D": 340})
    DONNEES["ex2998"] = {"A": A, "B": B, "C": C, "D": D}
    return F.code()


FIGURES["ex2998_enonce"] = ex2998(False)
FIGURES["ex2998_corrige"] = ex2998(True)


# --- 2996 : synthèse, triangle rectangle en A (AB = 4,5 ; AC = 6)
FIGURES["ex2996_enonce"] = esquisse({"A": (0, 0), "B": (2.9, 0), "C": (0, 3.6)},
                                    [("A", "B", "4,5 cm"), ("A", "C", "6 cm")],
                                    droits=[("A", "B", "C")],
                                    noms_ang={"A": 225, "B": 340, "C": 90})


def ex2996_construction():
    A, B, C = (0.0, 0.0), (4.5, 0.0), (0.0, 6.0)
    O = lerp(B, C, 0.5)
    k = 0.6
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.cercle(O, 3.75, "otGreenDark,line width=.95pt")
    F.seg(A, (0.0, 6.9), "constr")           # perpendiculaire tracée à l'équerre
    F.compas_vers(A, C, 7)                    # report de 6 cm au compas
    P1, P2 = mediatrice_arcs(F, B, C, 4.93)
    F.seg(lerp(P1, P2, -0.1), lerp(P1, P2, 1.1), "rep,line width=.8pt")
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.seg(A, C, "rep")
    F.seg(B, C, "rep")
    F.droit(A, B, C, 0.24, NA)
    F.tick(B, O, 1, NA)
    F.tick(O, C, 1, NA)
    F.lcote(A, B, "4,5 cm", C)
    F.lcote(A, C, vert("6 cm"), (-1.0, 3.0), t=0.55)
    F.pts({"A": A, "B": B}, {"A": 225, "B": 300})
    F.pt(C, "C", 135, coul=VE, d=0.2)
    F.pt(O, "O", -8, coul=VE, d=0.2)
    DONNEES["ex2996_constr"] = {"A": A, "B": B, "C": C, "O": O, "P1": P1, "P2": P2}
    return F.code()


def ex2996_aires():
    B, C = (0.0, 0.0), (7.5, 0.0)
    _, _, A = tri_ccc(7.5, 4.5, 6, B)        # BA = 4,5 ; CA = 6
    H = pied(A, B, C)
    O = lerp(B, C, 0.5)
    DONNEES["ex2996_aires"] = {"A": A, "B": B, "C": C, "H": H, "O": O}
    F = Fig(0.75)
    F.fill([A, B, O], "otSky")
    F.fill([A, O, C], "otGreen!16")
    F.poly([A, B, C])
    F.seg(A, H, "rep")
    F.seg(A, O, "geoTrait")
    F.droit(H, B, A, 0.2, VE)
    F.droit(A, B, C, 0.22, NA)
    F.tick(B, O, 1)
    F.tick(O, C, 1)
    F.lcote(A, H, vert("3,6 cm"), C, t=0.55, d=0.1)
    F.cote(B, C, "7,5 cm", -0.55)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 290, coul=VE, d=0.16)
    F.pt(O, "O", 290, coul=VE, d=0.16)
    return F.code()


FIGURES["ex2996_corrige1"] = ex2996_construction()
FIGURES["ex2996_corrige2"] = ex2996_aires()

# FIN
