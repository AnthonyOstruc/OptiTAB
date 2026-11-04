# -*- coding: utf-8 -*-
r"""Figures de la notion « Construire et comparer des triangles » (4e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = construction
et éléments de réponse (corrigés), orange = angles donnés. Les figures « à main levée »
des énoncés sont tracées d'un trait légèrement irrégulier.

Toutes les constructions sont calculées en vraie grandeur (cm réels, ou m pour les
situations concrètes), puis réduites d'un facteur k : DONNEES garde les coordonnées
réelles, contrôlées par verif_282.py (sympy).
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


# ====================================================================== COURS
# --- I. inégalité triangulaire : base fixe, deux arcs
def inegalite(cas, k, haut_ligne=None):
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
            h = C[1] - y
            coul = VE
        elif st == "plat":
            C = (a, y)
            F.compas(A, a, 0, 22)
            F.compas(B, b, 180, 22 if b > 3 else 30)
            F.pt(C, None, coul=OR)
            h = 0.6 / k
            coul = OR
        else:
            F.compas(A, a, 38, 34, "otRed!80!black,line width=.7pt")
            F.compas(B, b, 142, 34, "otRed!80!black,line width=.7pt")
            h = max(a, b) * math.sin(math.radians(72)) * 0.9
            coul = RG
        F.seg(A, B, "geoTrait,line width=1.1pt")
        F.pt(A, "A", 200)
        F.pt(B, "B", 340)
        xl = a / 2 if st == "plat" else L / 2
        F.add(r"\node[lab,anchor=north] at %s {%s};" % (F.Q((xl * k, y * k - 0.09)), cm(str(L).replace(".", ","))))
        F.add(r"\coordinate (t) at (%s,%s);" % (f(Lmax * k + 0.75), f(y * k + 0.42)))
        F.add(r"\node[lab,anchor=west] at (t) {%s};" % t1)
        F.add(r"\node[txt,text=%s,anchor=north west] at ($(t)+(0,-.28)$) {%s};" % (coul, t2))
        y -= (haut_ligne or (h + 0.9 / k + 0.25 / k))
    return F


F = inegalite([(6, 4, 3.5, r"$4 + 3{,}5 > 6$", "triangle possible", "ok"),
               (6, 4, 2, r"$4 + 2 = 6$", "triangle aplati", "plat"),
               (6, 3.5, 2, r"$3{,}5 + 2 < 6$", "aucun triangle", "non")], 0.55, haut_ligne=4.3)
FIGURES["cours_inegalite"] = F.code()


# --- II. somme des angles
def somme_angles():
    F = Fig(1.0)
    B, C, A = (0, 0), (4.6, 0), (1.6, 2.8)
    F.fill([A, B, C])
    F.seg((-0.7, 2.8), (5.3, 2.8), "geoTrait")
    F.poly([A, B, C])
    F.angle(B, C, A, 0.5, n=1, coul=OR, plein=True)
    F.angle(C, A, B, 0.5, n=2, coul=VE, plein=True)
    F.angle(A, B, C, 0.42, n=3, coul=NA)
    F.angle(A, (-0.7, 2.8), B, 0.5, n=1, coul=OR, plein=True)
    F.angle(A, C, (5.3, 2.8), 0.5, n=2, coul=VE, plein=True)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.nom((5.3, 2.8), "(d)", 0, 0.1)
    return F.code()


FIGURES["cours_somme_angles"] = somme_angles()


# --- II. triangles particuliers
def particuliers():
    F = Fig(1.0)
    # isocèle en A
    o = (0, 0)
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
    # équilatéral
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
    F.pts({"A": A2, "B": B2, "C": C2}, {"A": 90, "B": 200, "C": 340})
    legende(F, (dx + 1.2, -0.42), "équilatéral")
    # rectangle en A
    dy = -3.6
    A3, B3, C3 = (0.2, dy), (2.6, dy), (0.2, dy + 1.7)
    F.fill([A3, B3, C3])
    F.poly([A3, B3, C3])
    F.droit(A3, B3, C3)
    F.pts({"A": A3, "B": B3, "C": C3}, {"A": 225, "B": 340, "C": 90})
    legende(F, (1.4, dy - 0.42), "rectangle en $A$")
    # rectangle isocèle en A
    A4, B4, C4 = (dx + 0.3, dy), (dx + 2.3, dy), (dx + 0.3, dy + 2.0)
    F.fill([A4, B4, C4])
    F.poly([A4, B4, C4])
    F.droit(A4, B4, C4)
    F.tick(A4, B4, 1)
    F.tick(A4, C4, 1)
    F.angle(B4, A4, C4, 0.45, deg(45), lr=1.05)
    F.angle(C4, A4, B4, 0.45, deg(45), lr=1.05)
    F.pts({"A": A4, "B": B4, "C": C4}, {"A": 225, "B": 340, "C": 90})
    legende(F, (dx + 1.3, dy - 0.42), "rectangle isocèle en $A$")
    return F.code()


FIGURES["cours_particuliers"] = particuliers()


# --- III. constructions du cours
def construction_ccc(AB, AC, BC, k, noms="ABC", txt=None, second=False, mesures=None):
    A, B, C = tri_ccc(AB, AC, BC)
    F = Fig(k)
    g = centre(A, B, C)
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


F, (A, B, C) = construction_ccc(5, 4, 3.5, 0.85, txt=("5 cm", "4 cm", "3,5 cm"))
DONNEES["cours_ccc"] = {"A": A, "B": B, "C": C}
FIGURES["cours_ccc"] = F.code()


def construction_cac(AB, AC, ang, k, noms="ABC", txt=None, mesure=None):
    a, b, c = noms
    A, B = (0.0, 0.0), (AB, 0.0)
    C = pol(A, AC, ang)
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.seg(A, pol(A, AC * 1.32, ang), "constr")
    F.compas_vers(A, C, 8)
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.seg(B, C, "rep")
    F.angle(A, B, C, 0.5, deg(ang), coul=OR)
    t = txt or (cm(AB), cm(AC))
    F.lcote(A, B, t[0], C)
    F.lcote(A, C, vert(t[1]), B, t=0.45)
    if mesure:
        F.lcote(B, C, vert(mesure), A, t=0.5)
    F.pt(A, a, 200)
    F.pt(B, b, 340)
    F.pt(C, c, ang + 45, coul=VE, d=0.26)
    return F, (A, B, C)


F, (D_, E_, F_) = construction_cac(5, 3.5, 45, 0.85, noms="DEF", txt=("5 cm", "3,5 cm"))
DONNEES["cours_cac"] = {"D": D_, "E": E_, "F": F_}
FIGURES["cours_cac"] = F.code()


def construction_aca(BC, angB, angC, k, noms="ABC", txt=None, mesures=None, angle_sommet=None):
    """Côté [BC] horizontal ; noms = (sommet construit, extrémité gauche, extrémité droite)."""
    A, B, C = tri_aca((0.0, 0.0), BC, angB, angC)
    a, b, c = noms
    F = Fig(k)
    F.fill([A, B, C], "otGreen!12")
    F.seg(B, lerp(B, A, 1.28), "constr")
    F.seg(C, lerp(C, A, 1.28), "constr")
    F.seg(B, C, "geoTrait,line width=1.1pt")
    F.angle(B, C, A, 0.55, deg(angB), coul=OR)
    F.angle(C, A, B, 0.55, deg(angC), coul=OR)
    if angle_sommet:
        F.angle(A, B, C, 0.4, vert(deg(angle_sommet)), coul=VE)
    F.lcote(B, C, txt or cm(BC), A)
    if mesures:
        F.lcote(B, A, vert(mesures[0]), C, t=0.42)
        F.lcote(C, A, vert(mesures[1]), B, t=0.42)
    F.pt(B, b, 200)
    F.pt(C, c, 340)
    F.pt(A, a, (angB + 180 - angC) / 2, coul=VE, d=0.22)
    return F, (A, B, C)


F, (T_, R_, S_) = construction_aca(5, 35, 65, 0.85, noms="TRS", txt="5 cm")
DONNEES["cours_aca"] = {"R": R_, "S": S_, "T": T_}
FIGURES["cours_aca"] = F.code()


# --- IV. médiatrice
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
def cercle_circonscrit(A, B, C, k, noms="ABC", arcs=None, d3_tir=False, extra=None, lab_d=None, ret=False):
    F = Fig(k)
    O = centre_circ(A, B, C)
    R = dist(O, A)
    F.fill([A, B, C])
    F.cercle(O, R, "otGreenDark,line width=.95pt")
    mil = {}
    for (p, q, nm) in ((A, B, "AB"), (B, C, "BC"), (C, A, "CA")):
        m = lerp(p, q, 0.5)
        mil[nm] = m
        d = direc(p, q) + 90
        L = R + 0.55 / k
        u = pol(O, 1, d)
        # segment de la médiatrice : de part et d'autre de O, jusqu'au cercle + marge
        t = [((m[0] - O[0]) * math.cos(math.radians(d)) + (m[1] - O[1]) * math.sin(math.radians(d)))]
        e1 = pol(O, L, d)
        e2 = pol(O, -L, d)
        sty = "repTir" if (d3_tir and nm == "CA") else "rep"
        F.seg(e1, e2, sty + ",line width=.8pt")
    for (p, q, nm) in ((A, B, "AB"), (B, C, "BC"), (C, A, "CA")):
        m = mil[nm]
        F.tick(p, m, 1 if nm == "AB" else (2 if nm == "BC" else 3), NA)
        F.tick(m, q, 1 if nm == "AB" else (2 if nm == "BC" else 3), NA)
        F.droit(m, q, O if dist(m, O) > 0.3 / k else pol(m, 1, direc(p, q) + 90), 0.17, VE)
    if arcs:
        for (p, q, r) in arcs:
            m = lerp(p, q, 0.5)
            h = math.sqrt(r * r - (dist(p, q) / 2) ** 2)
            d = direc(p, q) + 90
            for P_ in (pol(m, h, d), pol(m, -h, d)):
                F.compas_vers(p, P_, 8)
                F.compas_vers(q, P_, 8)
    F.poly([A, B, C])
    g = centre(A, B, C)
    a, b, c = noms
    F.pts({a: A, b: B, c: C}, None, g)
    dirs = []
    for (p, q) in ((A, B), (B, C), (C, A)):
        dirs += [direc(p, q) + 90, direc(p, q) - 90]
    F.pt(O, "O", angle_libre(dirs), coul=VE, d=0.2)
    if lab_d:
        for nm, v in lab_d.items():
            if nm != "O":
                F.nom(v[0], v[1], v[2], 0.1, VE)
    if ret:
        return F, O, R
    return F.code()


A, B, C = (0.0, 0.0), (5.0, 0.0), (1.6, 3.4)
FIGURES["cours_cercle"] = cercle_circonscrit(A, B, C, 0.8)
DONNEES["cours_cercle"] = {"A": A, "B": B, "C": C, "O": centre_circ(A, B, C)}


# --- IV. hauteurs
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
    legende(F, (1.8, -0.45), "hauteurs concourantes")
    # triangle obtus en E
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
    legende(F, (dx + 0.6, dy - 0.58), "hauteur issue de $D$ extérieure")
    return F.code()


FIGURES["cours_hauteurs"] = hauteurs_cours()


# --- V. cas d'égalité
T0 = [(0.0, 0.0), (2.4, 0.0), (0.75, 1.55)]


def paire(F, dy, codes, dx2=3.5, rot=200, miroir=True, ech=1.0, tri=None, coul_codes=None):
    """Deux triangles : T0 en (0, dy) et son image (isométrie, ou similitude si ech ≠ 1)."""
    t1 = [(x, y + dy) for (x, y) in (tri or T0)]
    t2 = isometrie(tri or T0, rot, miroir, 0, 0, ech)
    gx = min(p[0] for p in t2)
    gy = min(p[1] for p in t2)
    t2 = [(x - gx + dx2, y - gy + dy) for (x, y) in t2]
    for t in (t1, t2):
        F.fill(t)
        F.poly(t)
        for c in codes:
            typ = c[0]
            if typ == "c":
                _, i, j, n = c
                F.tick(t[i], t[j], n)
            else:
                _, i, n, cl = c
                j, l = (i + 1) % 3, (i + 2) % 3
                F.angle(t[i], t[j], t[l], 0.32, n=n, coul=cl)
    return t1, t2


def cas_egalite():
    F = Fig(1.0)
    paire(F, 0.0, [("c", 0, 1, 1), ("c", 1, 2, 2), ("c", 2, 0, 3)])
    legende(F, (3.0, -0.3), "trois côtés égaux deux à deux")
    paire(F, -2.75, [("c", 0, 1, 1), ("c", 0, 2, 2), ("a", 0, 1, OR)])
    legende(F, (3.0, -3.05), "deux côtés et l'angle compris")
    paire(F, -5.5, [("c", 0, 1, 1), ("a", 0, 1, OR), ("a", 1, 2, VE)])
    legende(F, (3.0, -5.8), "un côté et les deux angles adjacents")
    return F.code()


FIGURES["cours_egalite"] = cas_egalite()


# --- VI. triangles semblables (côtés 4, 5, 6 et × 1,5)
def semblables_cours():
    F = Fig(0.45)
    B, C = (0.0, 0.0), (5.0, 0.0)
    _, _, A = tri_ccc(5, 4, 6, B)  # BA = 4, CA = 6
    E, Fp = (8.2, 0.0), (8.2 + 7.5, 0.0)
    _, _, D = tri_ccc(7.5, 6, 9, E)
    DONNEES["cours_semblables"] = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}
    F.fill([A, B, C])
    F.fill([D, E, Fp], "otGreen!14")
    F.poly([A, B, C])
    F.poly([D, E, Fp])
    for (s, p, q, n, cl) in ((A, B, C, 1, OR), (B, C, A, 2, VE), (C, A, B, 3, NA)):
        F.angle(s, p, q, 0.34, n=n, coul=cl)
    for (s, p, q, n, cl) in ((D, E, Fp, 1, OR), (E, Fp, D, 2, VE), (Fp, D, E, 3, NA)):
        F.angle(s, p, q, 0.34, n=n, coul=cl)
    gA = centre(A, B, C)
    gD = centre(D, E, Fp)
    F.lcote(A, B, "4", C)
    F.lcote(B, C, "5", A)
    F.lcote(A, C, "6", B)
    F.lcote(D, E, "6", Fp)
    F.lcote(E, Fp, vert("7,5"), D)
    F.lcote(D, Fp, "9", E)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 220, "C": 330})
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 90, "E": 220, "F": 330})
    F.add(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2mm]}] %s to[bend left=25] %s;"
          % (F.P((3.6, 2.6)), F.P((7.6, 2.6))))
    F.texte((5.6, 3.25), r"$\times\,1{,}5$", "south", "lab", "otMuted")
    return F.code()


FIGURES["cours_semblables"] = semblables_cours()


# --- VII. rédaction
def redaction():
    F = Fig(0.9)
    A, B = (0.0, 0.0), (4.4, 0.0)
    C = pol(A, 2.8, 40)
    D = pol(A, 2.8, -40)
    F.fill([A, B, C])
    F.fill([A, B, D], "otGreen!14")
    F.poly([A, B, C])
    F.poly([A, B, D])
    F.seg(A, B, "geoTrait,line width=1.2pt")
    F.tick(A, C, 1)
    F.tick(A, D, 1)
    F.angle(A, B, C, 0.5, coul=OR)
    F.angle(A, D, B, 0.5, coul=OR)
    F.seg(B, C, "rep")
    F.seg(B, D, "rep")
    F.tick(B, C, 2, VE)
    F.tick(B, D, 2, VE)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 180, "B": 0, "C": 90, "D": 270})
    return F.code()


FIGURES["cours_redaction"] = redaction()


# ====================================================================== EXERCICES
# --- 3146 : trois cas
F = inegalite([(8, 3, 4, r"$3 + 4 < 8$", "aucun triangle", "non"),
               (6, 4, 5, r"$4 + 5 > 6$", "triangle possible", "ok"),
               (12, 5, 7, r"$5 + 7 = 12$", "triangle aplati", "plat")], 0.35, haut_ligne=6.6)
FIGURES["ex3146_corrige"] = F.code()


# --- esquisses à main levée
def esquisse(pts, cotes, angles=(), noms_ang=None, k=1.0, seed=7, droits=(), ticks=(), legende_y=None):
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


# 3147
FIGURES["ex3147_enonce"] = esquisse({"A": (0, 0), "B": (4.6, 0), "C": (3.4, 2.2)},
                                    [("A", "B", "6 cm"), ("A", "C", "5 cm"), ("B", "C", "4 cm")],
                                    noms_ang={"A": 200, "B": 340, "C": 90})
F, (A, B, C) = construction_ccc(6, 5, 4, 0.75, second=True)
F.angle(A, B, C, 0.6, vert(r"$\approx 41^{\circ}$"), coul=VE, lr=1.25)
DONNEES["ex3147"] = {"A": A, "B": B, "C": C}
FIGURES["ex3147_corrige"] = F.code()


# --- 3148 : trois triangles
def ex3148(corr):
    F = Fig(0.92)
    # ABC : A = 52, B = 71
    A, B, C = tri_aca((0, 0), 2.5, 52, 71)
    # tri_aca renvoie (sommet, B, C) avec angles en B et C : on renomme
    S, P, Q = A, B, C  # S = sommet ; P (angle 52) ; Q (angle 71)
    A_, B_, C_ = P, Q, S
    F.fill([A_, B_, C_])
    F.poly([A_, B_, C_])
    F.angle(A_, B_, C_, 0.42, deg(52))
    F.angle(B_, C_, A_, 0.42, deg(71))
    if corr:
        F.angle(C_, A_, B_, 0.35, vert(deg(57)), coul=VE)
    F.pts({"A": A_, "B": B_, "C": C_}, {"A": 200, "B": 340, "C": 90})
    # EFG isocèle en E, E = 40
    dx = 3.35
    E = (dx + 1.0, 2.75)
    Fp = pol(E, 2.9, 250)
    G = pol(E, 2.9, 290)
    F.fill([E, Fp, G])
    F.poly([E, Fp, G])
    F.tick(E, Fp, 2)
    F.tick(E, G, 2)
    F.angle(E, Fp, G, 0.5, deg(40), lr=1.05)
    if corr:
        F.angle(Fp, G, E, 0.38, vert(deg(70)), coul=VE, lr=0.8)
        F.angle(G, E, Fp, 0.38, vert(deg(70)), coul=VE, lr=0.8)
    F.pts({"E": E, "F": Fp, "G": G}, {"E": 90, "F": 200, "G": 340})
    # RST rectangle en R, S = 35
    rx = 6.25
    R = (rx, 0.0)
    S_ = (rx + 2.6, 0.0)
    T = (rx, 2.6 * math.tan(math.radians(35)))
    F.fill([R, S_, T])
    F.poly([R, S_, T])
    F.droit(R, S_, T)
    F.angle(S_, T, R, 0.55, deg(35), lr=1.15)
    if corr:
        F.angle(T, R, S_, 0.38, vert(deg(55)), coul=VE)
    F.pts({"R": R, "S": S_, "T": T}, {"R": 225, "S": 340, "T": 90})
    DONNEES["ex3148" + ("c" if corr else "")] = {"A": A_, "B": B_, "C": C_, "E": E, "F": Fp, "G": G,
                                                  "R": R, "S": S_, "T": T}
    return F.code()


FIGURES["ex3148_enonce"] = ex3148(False)
FIGURES["ex3148_corrige"] = ex3148(True)


# --- 3149 : quatre paires
TP = [(0.0, 0.0), (2.2, 0.0), (0.7, 1.4)]


def ex3149(corr):
    F = Fig(1.0)
    rangs = [
        ([("c", 0, 1, 1), ("c", 1, 2, 2), ("c", 2, 0, 3)], 1.0, "trois côtés : égaux"),
        ([("c", 0, 1, 1), ("c", 0, 2, 2), ("a", 0, 1, OR)], 1.0, "deux côtés et l'angle compris : égaux"),
        ([("c", 0, 1, 1), ("a", 0, 1, OR), ("a", 1, 2, VE)], 1.0, "un côté et les deux angles adjacents : égaux"),
        ([("a", 0, 1, OR), ("a", 1, 2, VE), ("a", 2, 3, NA)], 1.45, "trois angles seulement : non égaux"),
    ]
    y_haut = 0.0
    for i, (codes, ech, txt) in enumerate(rangs):
        t2 = isometrie(TP, 165, True, 0, 0, ech)
        h = max(max(p[1] for p in TP), max(p[1] for p in t2) - min(p[1] for p in t2))
        dy = y_haut - h
        F.texte((-0.35, dy + 0.6), r"Paire %d" % (i + 1), "east", "txt", NA, reel=False)
        paire(F, dy, codes, dx2=3.0, rot=165, miroir=True, ech=ech, tri=TP)
        if corr:
            legende(F, (2.6, dy - 0.25), txt, VE)
            y_haut = dy - 0.95
        else:
            y_haut = dy - 0.6
    return F.code()


FIGURES["ex3149_enonce"] = ex3149(False)
FIGURES["ex3149_corrige"] = ex3149(True)


# --- 3150 : ABC (AB 5, BC 6, CA 4) et EFD
def ex3150(corr):
    F = Fig(0.5)
    B, C, A = tri_ccc(6, 5, 4)  # B origine, C à 6, A : BA = 5, CA = 4
    # image : A → E, B → F, C → D (miroir + rotation)
    E, Fp, D = isometrie([A, B, C], rot=-100, miroir=True)
    gx = min(p[0] for p in (E, Fp, D))
    gy = min(p[1] for p in (E, Fp, D))
    E, Fp, D = [(x - gx + 8.6, y - gy - 0.6) for (x, y) in (E, Fp, D)]
    DONNEES["ex3150"] = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}
    for t in ((A, B, C), (E, Fp, D)):
        F.fill(list(t), "otSky" if t[0] is A or not corr else "otGreen!12")
        F.poly(list(t))
    g1, g2 = centre(A, B, C), centre(D, E, Fp)
    F.lcote(A, B, "5", C)
    F.lcote(B, C, "6", A)
    F.lcote(C, A, "4", B)
    F.lcote(E, Fp, "5", D)
    F.lcote(Fp, D, "6", E)
    F.lcote(D, E, "4", Fp)
    if corr:
        for (p, q, n) in ((A, B, 1), (B, C, 2), (C, A, 3), (E, Fp, 1), (Fp, D, 2), (D, E, 3)):
            F.tick(p, q, n, VE, t=0.68)
        F.angle(A, B, C, 0.42, vert(r"$83^{\circ}$"), coul=VE)
        F.angle(B, C, A, 0.5, vert(r"$41^{\circ}$"), coul=VE)
        F.angle(C, A, B, 0.45, vert(r"$56^{\circ}$"), coul=VE)
        F.angle(E, Fp, D, 0.42, vert(r"$83^{\circ}$"), coul=VE)
        F.angle(Fp, D, E, 0.5, vert(r"$41^{\circ}$"), coul=VE)
        F.angle(D, E, Fp, 0.45, vert(r"$56^{\circ}$"), coul=VE)
    F.pts({"A": A, "B": B, "C": C}, None, g1)
    F.pts({"D": D, "E": E, "F": Fp}, None, g2)
    return F.code()


FIGURES["ex3150_enonce"] = ex3150(False)
FIGURES["ex3150_corrige"] = ex3150(True)

# --- 3151
FIGURES["ex3151_enonce"] = esquisse({"A": (0, 0), "B": (4.0, 0), "C": (2.0, 2.4)},
                                    [("A", "B", "5 cm"), ("A", "C", "4 cm")],
                                    angles=[("A", "B", "C", deg(50))],
                                    noms_ang={"A": 200, "B": 340, "C": 90})
F, (A, B, C) = construction_cac(5, 4, 50, 0.8, mesure=r"$\approx 3{,}9$ cm")
DONNEES["ex3151"] = {"A": A, "B": B, "C": C}
FIGURES["ex3151_corrige"] = F.code()

# --- 3152
FIGURES["ex3152_enonce"] = esquisse({"B": (0, 0), "C": (4.4, 0), "A": (3.0, 2.4)},
                                    [("B", "C", "6 cm")],
                                    angles=[("B", "C", "A", deg(40)), ("C", "A", "B", deg(60))],
                                    noms_ang={"A": 90, "B": 200, "C": 340})
F, (A, B, C) = construction_aca(6, 40, 60, 0.75, noms="ABC", mesures=(r"$\approx 5{,}3$ cm", r"$\approx 3{,}9$ cm"),
                                angle_sommet=80)
DONNEES["ex3152"] = {"A": A, "B": B, "C": C}
FIGURES["ex3152_corrige"] = F.code()


# --- 3153 : parallélogramme
def ex3153(corr):
    F = Fig(0.55)
    A, B = (0.0, 0.0), (7.0, 0.0)
    C = pol(B, 4, 110)
    D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
    DONNEES["ex3153"] = {"A": A, "B": B, "C": C, "D": D}
    if corr:
        F.fill([A, B, C])
        F.fill([C, D, A], "otGreen!14")
    else:
        F.fill([A, B, C, D])
    F.poly([A, B, C, D])
    F.seg(A, C, "geoTrait")
    F.angle(B, C, A, 0.42, deg(70))
    if corr:
        F.tick(A, B, 1, t=0.7)
        F.tick(C, D, 1, t=0.7)
        F.tick(B, C, 2, t=0.72)
        F.tick(D, A, 2, t=0.72)
        F.angle(D, A, C, 0.42, vert(deg(70)), coul=VE, lr=0.78)
        aAC = direc(A, C)
        F.angle(A, B, D, 0.38, vert(deg(110)), coul=VE, am=(aAC + 110) / 2, lr=0.95)
        F.angle(C, D, B, 0.38, vert(deg(110)), coul=VE, am=(aAC + 180 + 290) / 2, lr=0.95)
    F.lcote(A, B, "7 cm", C)
    F.lcote(B, C, "4 cm", A)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    return F.code()


FIGURES["ex3153_enonce"] = ex3153(False)
FIGURES["ex3153_corrige"] = ex3153(True)


# --- 3154 : isocèle en A, sommet 40°
def ex3154(corr):
    F = Fig(0.82)
    A = (0.0, 4.5 * math.cos(math.radians(20)))
    B = (-4.5 * math.sin(math.radians(20)), 0.0)
    C = (4.5 * math.sin(math.radians(20)), 0.0)
    H = (0.0, 0.0)
    DONNEES["ex3154"] = {"A": A, "B": B, "C": C, "H": H}
    if corr:
        F.fill([A, B, H])
        F.fill([A, H, C], "otGreen!14")
    else:
        F.fill([A, B, C])
    F.poly([A, B, C])
    F.seg(A, H, "geoTrait")
    F.tick(A, B, 2)
    F.tick(A, C, 2)
    F.tick(B, H, 1)
    F.tick(H, C, 1)
    if corr:
        F.droit(H, C, A, 0.2, VE)
        F.angle(B, C, A, 0.42, vert(deg(70)), coul=VE)
        F.angle(C, A, B, 0.42, vert(deg(70)), coul=VE)
        F.angle(A, B, H, 0.75, coul=VE)
        F.angle(A, H, C, 0.85, n=1, coul=VE)
    F.pts({"A": A, "B": B, "C": C, "H": H}, {"A": 90, "B": 200, "C": 340, "H": 270})
    return F.code()


FIGURES["ex3154_enonce"] = ex3154(False)
FIGURES["ex3154_corrige"] = ex3154(True)

# --- 3155 : médiatrices et cercle circonscrit (AB 7, BC 6, AC 5)
FIGURES["ex3155_enonce"] = esquisse({"A": (0, 0), "B": (4.6, 0), "C": (1.7, 2.6)},
                                    [("A", "B", "7 cm"), ("B", "C", "6 cm"), ("A", "C", "5 cm")],
                                    noms_ang={"A": 200, "B": 340, "C": 90})
A, B, C = tri_ccc(7, 5, 6)
F, O, R = cercle_circonscrit(A, B, C, 0.6, arcs=[(A, B, 4.5), (B, C, 5.0)], d3_tir=True, ret=True,
                             lab_d={"O": 186})
DONNEES["ex3155"] = {"A": A, "B": B, "C": C, "O": O}
F.nom(pol(O, R + 0.55 / 0.6, 90), "(d_1)", 0, 0.1, VE)
F.nom(pol(O, R + 0.55 / 0.6, direc(B, C) + 90), "(d_2)", direc(B, C) + 90, 0.1, VE)
FIGURES["ex3155_corrige"] = F.code()


# --- 3156 : diagonales de même milieu
def ex3156(corr):
    F = Fig(0.45)
    O = (0.0, 0.0)
    A = pol(O, 4, 200)
    C = pol(A, 6, 20 + 47)
    B = (-A[0], -A[1])
    D = (-C[0], -C[1])
    DONNEES["ex3156"] = {"A": A, "B": B, "C": C, "D": D, "O": O}
    if corr:
        F.fill([A, O, C])
        F.fill([B, O, D], "otGreen!14")
        F.seg(A, C, "geoTrait")
        F.seg(B, D, "rep")
    F.seg(A, B)
    F.seg(C, D)
    F.tick(A, O, 1)
    F.tick(O, B, 1)
    F.tick(C, O, 2)
    F.tick(O, D, 2)
    if corr:
        F.angle(O, A, C, 0.38, coul=NA)
        F.angle(O, B, D, 0.38, coul=NA)
        F.angle(A, O, C, 0.5, deg(47), coul=OR)
        F.angle(B, O, D, 0.5, vert(deg(47)), coul=VE)
        F.lcote(A, C, "6 cm", O)
        F.lcote(B, D, vert("6 cm"), O)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 200, "B": 20, "C": 90, "D": 270})
    F.pt(O, "O", 160 if not corr else 64, d=0.2)
    return F.code()


FIGURES["ex3156_enonce"] = ex3156(False)
FIGURES["ex3156_corrige"] = ex3156(True)


# --- 3157 : contre-exemples
def ex3157():
    F = Fig(0.4)
    A, B = (0.0, 0.0), (4.0, 0.0)
    C1 = pol(A, 6, 40)
    C2 = pol(A, 6, 100)
    F.fill([A, B, C1])
    F.fill([A, B, C2], "otGreen!14")
    F.poly([A, B, C1])
    F.poly([A, B, C2], "repTir")
    F.seg(A, B, "geoTrait,line width=1.1pt")
    F.lcote(A, B, "4", C1)
    F.lcote(A, C1, "6", B, t=0.62)
    F.lcote(A, C2, vert("6"), B, t=0.62)
    F.pts({"A": A, "B": B}, {"A": 225, "B": 315})
    F.pt(C1, "C", 30)
    F.pt(C2, "C'", 90, coul=VE)
    legende(F, (0.8, -0.62), "question 2")
    # question 3 : deux triangles 50-60-70
    dx = 7.4
    P1, Q1 = (dx, 0.0), (dx + 4.0, 0.0)
    R1 = tri_aca(P1, 4.0, 50, 60)[0]
    P2, Q2 = (dx + 5.0, 0.0), (dx + 12.0, 0.0)
    R2 = tri_aca(P2, 7.0, 50, 60)[0]
    for t, fl in (((P1, Q1, R1), "otSky"), ((P2, Q2, R2), "otGreen!14")):
        F.fill(list(t), fl)
        F.poly(list(t))
        F.angle(t[0], t[1], t[2], 0.3, n=1, coul=OR)
        F.angle(t[1], t[2], t[0], 0.3, n=2, coul=VE)
        F.angle(t[2], t[0], t[1], 0.3, n=3, coul=NA)
    legende(F, ((dx + 6.0) * 0.4, -0.62), "question 3")
    DONNEES["ex3157"] = {"A": A, "B": B, "C1": C1, "C2": C2, "P1": P1, "Q1": Q1, "R1": R1, "P2": P2, "Q2": Q2, "R2": R2}
    return F.code()


FIGURES["ex3157_corrige"] = ex3157()


# --- 3158 : hauteurs
A58, B58, C58 = (2.0, 4.5), (0.0, 0.0), (8.0, 0.0)
H58 = (2.0, 0.0)
E58, F58, G58 = (-1.5, 2.5), (0.0, 0.0), (4.5, 0.0)


def ex3158_enonce():
    F = Fig(0.52)
    A, B, C, H = A58, B58, C58, H58
    F.fill([A, B, C])
    F.poly([A, B, C])
    F.seg(A, H)
    F.droit(H, C, A)
    F.cote(B, H, "2 cm", -0.42)
    F.cote(B, C, "8 cm", -1.05)
    F.lcote(A, H, "4,5 cm", B, t=0.5)
    F.lcote(A, C, "7,5 cm", B)
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 180, "C": 0})
    F.pt(H, "H", 300, d=0.16)
    dx = 11.0
    E, Fp, G = [(x + dx, y) for (x, y) in (E58, F58, G58)]
    F.fill([E, Fp, G])
    F.poly([E, Fp, G])
    F.angle(Fp, G, E, 0.35, coul=OR)
    F.pts({"E": E, "F": Fp, "G": G}, {"E": 90, "F": 270, "G": 0})
    return F.code()


def ex3158_corrige1():
    F = Fig(0.6)
    A, B, C, H = A58, B58, C58, H58
    K = pied(B, A, C)
    L = pied(C, A, B)
    O = orthocentre(A, B, C)
    DONNEES["ex3158"] = {"A": A, "B": B, "C": C, "H": H, "K": K, "L": L, "Orth": O}
    F.fill([A, B, C])
    F.seg(A, H, "rep")
    F.seg(B, K, "rep")
    F.seg(C, L, "rep")
    F.droit(H, C, A, 0.2, VE)
    F.droit(K, C, B, 0.2, VE)
    F.droit(L, B, C, 0.2, VE)
    F.poly([A, B, C])
    F.pts({"A": A, "B": B, "C": C}, {"A": 90, "B": 200, "C": 340})
    F.pt(H, "H", 270, coul=VE, d=0.16)
    F.pt(K, "K", 40, coul=VE, d=0.16)
    F.pt(L, None, coul=VE)
    F.pt(O, None, coul=VE)
    return F.code()


def ex3158_corrige2():
    F = Fig(0.7)
    E, Fp, G = E58, F58, G58
    Ep = (E[0], 0.0)
    Fh = pied(Fp, E, G)
    DONNEES["ex3158b"] = {"E": E, "F": Fp, "G": G, "E'": Ep, "Fh": Fh}
    F.fill([E, Fp, G])
    F.seg(Ep, Fp, "pointille")
    F.seg(E, Ep, "rep")
    F.seg(Fp, Fh, "rep")
    F.droit(Ep, Fp, E, 0.2, VE)
    F.droit(Fh, G, Fp, 0.2, VE)
    F.poly([E, Fp, G])
    F.pts({"E": E, "F": Fp, "G": G}, {"E": 90, "F": 285, "G": 340})
    F.pt(Ep, None, coul=VE)
    legende(F, ((Ep[0] + 0.4) * 0.7, -0.5), "pied hors de $[FG]$", VE)
    return F.code()


FIGURES["ex3158_enonce"] = ex3158_enonce()
FIGURES["ex3158_corrige1"] = ex3158_corrige1()
FIGURES["ex3158_corrige2"] = ex3158_corrige2()


# --- 3159 : triangles semblables
def ex3159(corr):
    F = Fig(0.75)
    A, B, C = None, None, None
    C_, A_, B_ = tri_aca((0.0, 0.0), 3.2, 50, 60)  # A_ à gauche (50°), B_ à droite (60°)
    A, B, C = A_, B_, C_
    # DEF : D en bas à gauche (70°), E en bas à droite (50°)
    F_, D, E = tri_aca((4.4, 0.0), 4.4, 70, 50)
    DONNEES["ex3159"] = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F_}
    F.fill([A, B, C])
    F.fill([D, E, F_], "otGreen!12" if corr else "otSky")
    F.poly([A, B, C])
    F.poly([D, E, F_])
    F.angle(A, B, C, 0.42, deg(50), coul=OR)
    F.angle(B, C, A, 0.42, deg(60), n=2, coul=OR)
    F.angle(D, E, F_, 0.42, deg(70), n=3, coul=OR)
    F.angle(E, F_, D, 0.42, deg(50), coul=OR)
    if corr:
        F.angle(C, A, B, 0.36, vert(deg(70)), n=3, coul=VE)
        F.angle(F_, D, E, 0.36, vert(deg(60)), n=2, coul=VE)
    F.pts({"A": A, "B": B, "C": C}, {"A": 200, "B": 340, "C": 90})
    F.pts({"D": D, "E": E, "F": F_}, {"D": 200, "E": 340, "F": 90})
    return F.code()


def ex3159_corrige2():
    F = Fig(0.42)
    P, Q, R = tri_ccc(6, 4, 3)
    dx = 7.4
    P2, Q2, R2 = tri_ccc(9, 6, 4.5, (dx, 0.0))
    DONNEES["ex3159b"] = {"P": P, "Q": Q, "R": R, "P2": P2, "Q2": Q2, "R2": R2}
    F.fill([P, Q, R])
    F.fill([P2, Q2, R2], "otGreen!14")
    F.poly([P, Q, R])
    F.poly([P2, Q2, R2])
    F.lcote(P, Q, "6", R)
    F.lcote(P, R, "4", Q)
    F.lcote(Q, R, "3", P)
    F.lcote(P2, Q2, vert("9"), R2)
    F.lcote(P2, R2, vert("6"), Q2)
    F.lcote(Q2, R2, vert("4,5"), P2)
    F.texte((3.0, -1.6), "$T_1$", "north", "lab", NA)
    F.texte((dx + 4.5, -1.6), "$T_3$", "north", "lab", VE)
    F.add(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2mm]}] %s to[bend left=25] %s;"
          % (F.P((4.6, 2.4)), F.P((9.6, 3.4))))
    F.texte((7.0, 4.25), r"$\times\,1{,}5$", "south", "lab", "otMuted")
    return F.code()


FIGURES["ex3159_enonce"] = ex3159(False)
FIGURES["ex3159_corrige"] = ex3159(True)
FIGURES["ex3159_corrige2"] = ex3159_corrige2()


# --- 3160 : rivière (mètres)
def ex3160(corr):
    F = Fig(0.055)
    B, C, D = (0.0, 0.0), (40.0, 0.0), (80.0, 0.0)
    A, E = (0.0, -28.0), (80.0, 28.0)
    DONNEES["ex3160"] = {"A": A, "B": B, "C": C, "D": D, "E": E}
    F.fill([(-10, 0), (92, 0), (92, -40), (-10, -40)], "otSky")
    F.seg((-10, 0), (92, 0), "otMuted,line width=.6pt")
    F.seg((-10, -40), (92, -40), "otMuted,line width=.6pt")
    F.texte((70, -27), "rivière", "center", "txt", NA)
    if corr:
        F.fill([A, B, C], "otNavy!12")
        F.fill([E, D, C], "otGreen!18")
    F.seg(A, E)
    F.seg(B, D)
    F.seg(D, E)
    F.seg(A, B, "rep" if corr else "repTir")
    F.droit(B, C, A)
    F.droit(D, C, E)
    F.tick(B, C, 1)
    F.tick(C, D, 1)
    F.add(r"\node[lab,anchor=south] at %s {40 m};" % F.Q((9.5 * 0.055, 0.1)))
    F.add(r"\node[lab,anchor=north] at %s {40 m};" % F.Q((52 * 0.055, -0.1)))
    if corr:
        F.angle(C, B, A, 0.38, coul=OR)
        F.angle(C, D, E, 0.38, coul=OR)
        F.lcote(A, B, vert("28 m"), C)
        F.lcote(D, E, "28 m", C)
    else:
        F.lcote(A, B, "?", C)
    F.pts({"A": A, "B": B, "C": C, "D": D, "E": E}, {"A": 270, "B": 160, "C": 258, "D": 315, "E": 45})
    return F.code()


FIGURES["ex3160_enonce"] = ex3160(False)
FIGURES["ex3160_corrige"] = ex3160(True)


# --- 3161 : ombres (mètres)
def ex3161(corr):
    F = Fig(0.6)
    O, B, S = (0.0, 0.0), (1.8, 0.0), (1.8, 1.2)
    P, A, T = (3.4, 0.0), (12.4, 0.0), (12.4, 6.0)
    DONNEES["ex3161"] = {"O": O, "B": B, "S": S, "P": P, "A": A, "T": T}
    F.seg((-0.5, 0), (13.3, 0), "otMuted,line width=.7pt")
    F.fill([O, B, S], "otSky" if not corr else "otNavy!12")
    F.fill([P, A, T], "otSky" if not corr else "otGreen!16")
    F.seg(O, S, "rayon")
    F.seg(P, T, "rayon")
    F.seg(B, S, "otNavy,line width=2pt")
    F.seg(A, T, ("otGreenDark" if corr else "otNavy") + ",line width=2.4pt")
    F.seg(O, B, "otInk,line width=1.3pt")
    F.seg(P, A, "otInk,line width=1.3pt")
    F.droit(B, O, S, 0.2)
    F.droit(A, P, T, 0.25)
    if corr:
        F.angle(O, B, S, 0.55, coul=OR)
        F.angle(P, A, T, 0.55, coul=OR)
    F.cote(B, O, "1,8 m", 0.62)
    F.cote(A, P, "9 m", 0.62)
    F.add(r"\node[lab,anchor=west] at %s {1,2 m};" % F.Q((1.8 * 0.6 + 0.1, 0.6 * 0.6)))
    F.add(r"\node[lab,anchor=west] at %s {%s};" % (F.Q((12.4 * 0.6 + 0.12, 3.0 * 0.6)), vert("6 m") if corr else "?"))
    F.texte((7.3, 4.6), "rayons du soleil", "south east", "txt", "otOrange!80!black")
    F.pts({"O": O, "B": B, "S": S, "P": P, "A": A, "T": T},
          {"O": 215, "B": 325, "S": 90, "P": 215, "A": 325, "T": 90})
    return F.code()


FIGURES["ex3161_enonce"] = ex3161(False)
FIGURES["ex3161_corrige"] = ex3161(True)


# --- 3162 : équilatéral dans un équilatéral
def ex3162(corr):
    F = Fig(0.72)
    A, B = (0.0, 0.0), (6.0, 0.0)
    C = (3.0, 3 * math.sqrt(3))
    D = lerp(A, B, 2 / 6)
    E = lerp(B, C, 2 / 6)
    Fp = lerp(C, A, 2 / 6)
    DONNEES["ex3162"] = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}
    F.fill([A, B, C])
    if corr:
        F.fill([A, D, Fp], "otGreen!16")
        F.fill([B, E, D], "otGreen!16")
        F.fill([C, Fp, E], "otGreen!16")
    F.poly([A, B, C])
    F.poly([D, E, Fp], "rep" if corr else "geoTrait")
    for (p, q) in ((A, D), (B, E), (C, Fp)):
        F.tick(p, q, 1)
    for (p, q) in ((D, B), (E, C), (Fp, A)):
        F.tick(p, q, 2)
    if corr:
        for (p, q) in ((D, E), (E, Fp), (Fp, D)):
            F.tick(p, q, 3, VE)
        F.angle(A, B, C, 0.36, deg(60), lr=0.78)
        F.angle(B, C, A, 0.36, deg(60), lr=0.78)
        F.angle(C, A, B, 0.36, deg(60), lr=0.78)
    g = centre(A, B, C)
    F.pts({"A": A, "B": B, "C": C}, {"A": 210, "B": 330, "C": 90})
    F.pts({"D": D, "E": E, "F": Fp}, {"D": 270, "E": 30, "F": 150})
    return F.code()


FIGURES["ex3162_enonce"] = ex3162(False)
FIGURES["ex3162_corrige"] = ex3162(True)


# --- 3163 : antenne (quadrillage, 1 carreau = 1 km)
A63, B63, C63, D63, O63 = (1, 2), (9, 2), (8, 9), (12, 5), (5, 5)


def ex3163(corr):
    F = Fig(0.55)
    DONNEES["ex3163"] = {"A": A63, "B": B63, "C": C63, "D": D63, "O": O63}
    F.add(r"\draw[otRule,line width=.4pt] (0,0) grid[step=%s] %s;" % (f(0.55), F.P((13, 11))))
    if corr:
        F.cercle(O63, 5, "otGreenDark,line width=.9pt")
        F.seg((5, 0), (5, 11), "rep,line width=.85pt")
        F.seg((0, 5 - 5 / 7), (13, 5 + 8 / 7), "rep,line width=.85pt")
        F.tick(A63, (5, 2), 1)
        F.tick((5, 2), B63, 1)
        F.tick(B63, (8.5, 5.5), 2)
        F.tick((8.5, 5.5), C63, 2)
        F.seg(O63, D63, "repTir")
        F.droit((5, 2), B63, (5, 5), 0.18, VE)
        F.droit((8.5, 5.5), C63, (12, 6), 0.18, VE)
        F.pt(O63, "O", 229, coul=VE, d=0.2)
    F.poly([A63, B63, C63], "geoTrait,line width=.8pt,dash pattern=on 3pt off 2pt")
    F.pts({"A": A63, "B": B63, "C": C63, "D": D63}, {"A": 225, "B": 315, "C": 60, "D": 0})
    if corr:
        legende(F, (6.5 * 0.55, -0.15), "$OA = OB = OC = 5$ km ; $OD = 7$ km", VE)
        return F.code()
    F.add(r"\draw[otNavy,line width=1pt] %s -- %s;" % (F.P((0, -0.6)), F.P((1, -0.6))))
    F.add(r"\node[txt,text=otMuted,anchor=west] at %s {1 km};" % F.Q((1 * 0.55 + 0.12, -0.6 * 0.55)))
    return F.code()


FIGURES["ex3163_enonce"] = ex3163(False)
FIGURES["ex3163_corrige"] = ex3163(True)


# --- 3164 : deux côtés et un angle non compris
def ex3164_c1():
    F = Fig(0.75)
    B, A = (0.0, 0.0), (6.0, 0.0)
    d = 6 * math.cos(math.radians(40))
    h = math.sqrt(4.5 ** 2 - (6 * math.sin(math.radians(40))) ** 2)
    C1, C2 = pol(B, d + h, 40), pol(B, d - h, 40)
    DONNEES["ex3164"] = {"A": A, "B": B, "C1": C1, "C2": C2}
    F.fill([A, B, C1], "otNavy!10")
    F.fill([A, B, C2], "otGreen!20")
    F.seg(B, pol(B, 8.2, 40), "geoTrait")
    a1, a2 = direc(A, C1), direc(A, C2)
    F.add(r"\draw[compas] %s arc (%s:%s:%s);" % (F.Q(pol(F.T(A), 4.5 * 0.75, a1 - 9)), f(a1 - 9), f(a2 + 9), f(4.5 * 0.75)))
    F.seg(A, C1, "rep")
    F.seg(A, C2, "rep")
    F.seg(B, A, "geoTrait,line width=1.1pt")
    F.angle(B, A, C1, 0.6, deg(40))
    F.lcote(B, A, "6 cm", C1)
    F.lcote(A, C1, vert("4,5 cm"), B, t=0.5)
    F.lcote(A, C2, vert("4,5 cm"), C1, t=0.55)
    F.pt(B, "B", 200)
    F.pt(A, "A", 340)
    F.pt(C1, "C_1", 112, coul=VE, d=0.2)
    F.pt(C2, "C_2", 148, coul=VE, d=0.2)
    F.nom(pol(B, 8.2, 40), "x", 40, 0.1)
    return F.code()


def ex3164_c2():
    F = Fig(0.5)
    B, A = (0.0, 0.0), (6.0, 0.0)
    d = 6 * math.cos(math.radians(40))
    h7 = math.sqrt(49 - (6 * math.sin(math.radians(40))) ** 2)
    C, Cx = pol(B, d + h7, 40), pol(B, d - h7, 40)
    H = pol(B, d, 40)
    DONNEES["ex3164b"] = {"A": A, "B": B, "C": C, "Cx": Cx, "H": H}
    F.seg(B, pol(B, 12.2, 40), "geoTrait")
    F.seg(B, pol(B, -1.7, 40), "pointille")
    F.seg(B, A, "geoTrait,line width=1.1pt")
    F.seg(A, H, "pointille")
    F.droit(H, B, A, 0.17)
    F.cercle(A, 3, "otRed!80!black,line width=.75pt")
    a1 = direc(A, C)
    a2 = direc(A, Cx)
    if a2 < a1:
        a2 += 360
    F.add(r"\draw[compas] %s arc (%s:%s:%s);" % (F.Q(pol(F.T(A), 3.5, a1 - 12)), f(a1 - 12), f(a2 + 4), f(3.5)))
    F.seg(A, C, "rep")
    F.pt(B, "B", 300, d=0.17)
    F.pt(A, "A", 330)
    F.pt(C, "C", 100, coul=VE, d=0.2)
    F.pt(Cx, None, coul=RG)
    F.nom(pol(B, 12.2, 40), "x", 40, 0.1)
    F.lcote(A, C, vert("7 cm"), B, t=0.55)
    F.texte((A[0] + 3.0 * math.cos(math.radians(300)), A[1] + 3.0 * math.sin(math.radians(300))),
            r"\textcolor{otRed!85!black}{rayon 3 cm}", "north west", "lab", reel=True)
    cx = F.T(Cx)
    F.texte((cx[0] - 0.22, cx[1] + 0.12), r"hors de $[Bx)$", "south east", "txt", "otRed!85!black", reel=False)
    return F.code()


FIGURES["ex3164_corrige"] = ex3164_c1()
FIGURES["ex3164_corrige2"] = ex3164_c2()


# --- 3165 : cerf-volant (cm réels)
def ex3165(corr):
    k = 0.055
    F = Fig(k)
    H, A, C, B, D = (0.0, 0.0), (0.0, 20.0), (0.0, -60.0), (-25.0, 0.0), (25.0, 0.0)
    DONNEES["ex3165"] = {"A": A, "B": B, "C": C, "D": D, "H": H}
    if corr:
        F.fill([A, B, H], "otNavy!12")
        F.fill([A, H, D], "otGreen!18")
        F.fill([B, C, D], "otSky")
    else:
        F.fill([A, B, C, D])
    F.poly([A, B, C, D])
    F.seg(A, C, "rep" if corr else "geoTrait")
    F.seg(B, D)
    F.droit(H, D, A, 0.2, VE if corr else NA)
    F.tick(B, H, 1)
    F.tick(H, D, 1)
    F.cote(A, H, "20 cm", 2.0)
    F.cote(H, C, "60 cm", 2.0)
    F.cote(B, D, "50 cm", 1.8)
    if corr:
        F.tick(A, B, 2, VE)
        F.tick(A, D, 2, VE)
        F.tick(C, B, 3, VE)
        F.tick(C, D, 3, VE)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 150, "B": 180, "C": 270, "D": 315})
    F.pt(H, "H", 225 if not corr else 225, d=0.17)
    if corr:
        legende(F, (0.0, -60 * k - 0.45), "$(AC)$ : médiatrice de $[BD]$", VE)
    return F.code()


FIGURES["ex3165_enonce"] = ex3165(False)
FIGURES["ex3165_corrige"] = ex3165(True)


# --- 3166 : rectangle
def ex3166(corr):
    F = Fig(0.68)
    A, B, C, D, M = (0.0, 0.0), (8.0, 0.0), (8.0, 3.0), (0.0, 3.0), (4.0, 0.0)
    DONNEES["ex3166"] = {"A": A, "B": B, "C": C, "D": D, "M": M}
    if corr:
        F.fill([M, A, D], "otNavy!12")
        F.fill([M, B, C], "otGreen!18")
        F.seg((4.0, 3.75), (4.0, 0.0), "repTir")
    else:
        F.fill([A, B, C, D])
    F.poly([A, B, C, D])
    F.seg(M, D)
    F.seg(M, C)
    for (s, p, q) in ((A, B, D), (B, C, A), (C, D, B), (D, A, C)):
        F.droit(s, p, q)
    F.tick(A, M, 1)
    F.tick(M, B, 1)
    F.cote(B, A, "8 cm", 0.85)
    F.lcote(A, D, "3 cm", B)
    if corr:
        F.tick(M, D, 2, VE)
        F.tick(M, C, 2, VE)
        F.angle(M, A, D, 0.55, deg(37))
        F.angle(M, C, B, 0.55, vert(deg(37)), coul=VE)
        F.angle(M, D, C, 0.42, vert(deg(106)), coul=VE, am=112, lr=1.0)
        F.angle(D, M, C, 0.55, vert(deg(37)), coul=VE)
        F.angle(C, D, M, 0.55, vert(deg(37)), coul=VE)
    F.pts({"A": A, "B": B, "C": C, "D": D}, {"A": 225, "B": 315, "C": 45, "D": 135})
    F.pt(M, "M", 270, d=0.16)
    return F.code()


FIGURES["ex3166_enonce"] = ex3166(False)
FIGURES["ex3166_corrige"] = ex3166(True)
