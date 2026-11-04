# -*- coding: utf-8 -*-
"""Figures de la notion 158 (Première, produit scalaire), style des livres OptiTAB.

Compilées par outils/figures_livre.py :
    python figures_livre.py ../chantier/1ere/158_calcul-vectoriel-et-produit-scalaire [nom …]

Toutes les figures sont construites par la petite classe Fig : coordonnées en
unités de la figure (x = y = u cm), points en \\fill … circle, étiquettes posées
à une distance fixe (en cm) dans une direction choisie, ancrées du côté opposé :
le texte part du point vers l'extérieur et ne recouvre jamais un trait.
Éléments de réponse (corrigés) en vert otGreenDark.
"""
import math

RAC = math.sqrt


def n(v):
    return f"{v:.3f}"


class Fig:
    def __init__(self, u=1.0):
        self.u = u
        self.s = []

    def add(self, x):
        self.s.append(x)
        return self

    def c(self, P):
        return "(" + n(P[0]) + "," + n(P[1]) + ")"

    def tikz(self):
        tete = r"\begin{tikzpicture}[x=" + n(self.u) + "cm,y=" + n(self.u) + "cm,line cap=round,line join=round]"
        return tete + "\n" + "\n".join(self.s) + "\n" + r"\end{tikzpicture}"

    # -------------------------------------------------------------- tracés
    def seg(self, P, Q, style="geoTrait"):
        return self.add(r"\draw[" + style + "] " + self.c(P) + " -- " + self.c(Q) + ";")

    def poly(self, pts, style="geoTrait", fill=None):
        chemin = " -- ".join(self.c(p) for p in pts) + " -- cycle;"
        if fill:
            self.add(r"\fill[" + fill + "] " + chemin)
        return self.add(r"\draw[" + style + "] " + chemin)

    def vect(self, P, Q, col="otNavy", w="0.95pt"):
        return self.add(r"\draw[" + col + ",line width=" + w + r",-{Stealth[length=2.4mm]}] " + self.c(P) + " -- " + self.c(Q) + ";")

    def cercle(self, O, r, style="geoTrait"):
        return self.add(r"\draw[" + style + "] " + self.c(O) + " circle (" + n(r * self.u) + "cm);")

    def pt(self, P, col="otNavy"):
        return self.add(r"\fill[" + col + "] " + self.c(P) + " circle (1.9pt);")

    def lab(self, P, txt, ang, d=0.13, col="otInk"):
        """Étiquette dans la direction ang (degrés), à d cm du point P."""
        k = d / self.u
        Q = (P[0] + k * math.cos(math.radians(ang)), P[1] + k * math.sin(math.radians(ang)))
        anc = (ang + 180) % 360
        return self.add(r"\node[anchor=" + f"{anc:.0f}" + ",inner sep=1.2pt,text=" + col + "] at " + self.c(Q) + " {" + txt + "};")

    def texte(self, P, txt, anchor="center", col="otInk", style=""):
        return self.add(r"\node[anchor=" + anchor + ",inner sep=1.2pt,text=" + col + ("," + style if style else "") + "] at " + self.c(P) + " {" + txt + "};")

    def note(self, P, txt, anchor="center"):
        return self.add(r"\node[anchor=" + anchor + r",inner sep=1.2pt,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted] at " + self.c(P) + " {" + txt + "};")

    def droit(self, V, P, Q, col="otNavy", s=0.24):
        """Angle droit en V (côtés vers P et Q)."""
        k = s / self.u
        a = _unit(V, P)
        b = _unit(V, Q)
        p1 = (V[0] + k * a[0], V[1] + k * a[1])
        p2 = (p1[0] + k * b[0], p1[1] + k * b[1])
        p3 = (V[0] + k * b[0], V[1] + k * b[1])
        return self.add(r"\draw[" + col + ",line width=.65pt] " + self.c(p1) + " -- " + self.c(p2) + " -- " + self.c(p3) + ";")

    def arc(self, V, P, Q, r=0.55, col="otGreenDark", lab=None, dl=0.32):
        """Arc d'angle en V, de la direction VP à la direction VQ (sens direct)."""
        a1 = math.degrees(math.atan2(P[1] - V[1], P[0] - V[0]))
        a2 = math.degrees(math.atan2(Q[1] - V[1], Q[0] - V[0]))
        while a2 < a1:
            a2 += 360
        k = r / self.u
        S = (V[0] + k * math.cos(math.radians(a1)), V[1] + k * math.sin(math.radians(a1)))
        self.add(r"\draw[" + col + ",line width=.75pt] " + self.c(S) + " arc[start angle=" + f"{a1:.2f}" + ",end angle=" + f"{a2:.2f}" + ",radius=" + n(r) + "cm];")
        if lab:
            m = math.radians((a1 + a2) / 2)
            kk = (r + dl) / self.u
            self.add(r"\node[inner sep=1pt,text=" + col + "] at " + self.c((V[0] + kk * math.cos(m), V[1] + kk * math.sin(m))) + " {" + lab + "};")
        return self

    def codage(self, P, Q, nb=1, col="otNavy"):
        """nb petits traits perpendiculaires au milieu de [PQ]."""
        M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
        t = _unit(P, Q)
        nn = (-t[1], t[0])
        h = 0.11 / self.u
        e = 0.07 / self.u
        for i in range(nb):
            o = (i - (nb - 1) / 2) * e
            C = (M[0] + o * t[0], M[1] + o * t[1])
            self.add(r"\draw[" + col + ",line width=.7pt] " + self.c((C[0] - h * nn[0], C[1] - h * nn[1])) + " -- " + self.c((C[0] + h * nn[0], C[1] + h * nn[1])) + ";")
        return self

    def cote_seg(self, P, Q, txt, cote=1, d=0.14, col="otInk"):
        """Longueur écrite au milieu de [PQ], décalée perpendiculairement (cote=1 : à gauche de P→Q)."""
        M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
        t = _unit(P, Q)
        ang = math.degrees(math.atan2(t[0], -t[1])) if cote == 1 else math.degrees(math.atan2(-t[0], t[1]))
        return self.lab(M, txt, ang, d, col)

    def repere(self, xmin, xmax, ymin, ymax, gx=None, gy=None, grille=True, O=True):
        """Quadrillage, axes et graduations (gx, gy : valeurs graduées)."""
        if grille:
            self.add(r"\draw[otRule!80,line width=.35pt] " + self.c((xmin, ymin)) + " grid " + self.c((xmax, ymax)) + ";")
        e = 0.35 / self.u
        self.add(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2.3mm]}] " + self.c((xmin, 0)) + " -- " + self.c((xmax + e, 0)) + ";")
        self.add(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2.3mm]}] " + self.c((0, ymin)) + " -- " + self.c((0, ymax + e)) + ";")
        f = r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt"
        for x in (gx or []):
            self.add(r"\node[" + f + ",anchor=north] at " + self.c((x, -0.06 / self.u)) + " {" + _fr(x) + "};")
        for y in (gy or []):
            self.add(r"\node[" + f + ",anchor=east] at " + self.c((-0.06 / self.u, y)) + " {" + _fr(y) + "};")
        if O:
            self.add(r"\node[" + f + ",anchor=north east] at " + self.c((-0.04 / self.u, -0.04 / self.u)) + " {0};")
        return self


def _unit(P, Q):
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    L = math.hypot(dx, dy)
    return (dx / L, dy / L)


def _fr(v):
    return ("$" + str(v).replace("-", "-") + "$") if v < 0 else str(v)


def ext(V, G):
    """Direction (degrés) de G vers V : pour poser l'étiquette de V à l'extérieur."""
    return math.degrees(math.atan2(V[1] - G[1], V[0] - G[0]))


def centre(*pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def triangle(f, pts, noms, style="geoTrait", fill=None, d=0.14):
    G = centre(*pts)
    f.poly(pts, style, fill)
    for p, nom in zip(pts, noms):
        f.pt(p)
        if nom:
            f.lab(p, nom, ext(p, G), d)
    return G


FIGURES = {}

# =================================================================== COURS
# --- projection : angle aigu / angle obtus
f = Fig(1.0)
# panneau 1 (aigu)
A, B, C, H = (0, 0), (3.3, 0), (2.1, 1.75), (2.1, 0)
f.seg((-0.35, 0), (3.95, 0), "otMuted,line width=.5pt,dash pattern=on 2pt off 1.6pt")
f.seg(A, (2.1, 0), "otGreenDark,line width=2.6pt,line cap=butt")
f.seg(C, H, "guide")
f.droit(H, C, A, "otMuted", 0.2)
f.vect(A, B, "otNavy")
f.vect(A, C, "otOrange!90!black")
for p in (A, H, C):
    f.pt(p)
f.lab(A, "$A$", 235); f.lab(H, "$H$", -60, 0.17); f.lab(B, "$B$", -90, 0.17); f.lab(C, "$C$", 90)
f.texte((1.65, -0.85), r"$\overrightarrow{AB} \cdot \overrightarrow{AC} = AB \times AH$")
f.note((1.65, -1.38), "angle aigu : produit positif")
# panneau 2 (obtus), décalé de 4,75
dx = -0.15  # panneau 2 placé sous le panneau 1 (lisible sur téléphone)
f.add(r"\begin{scope}[yshift=-4.05cm]")
A2, B2, C2, H2 = (dx + 1.0, 0), (dx + 3.9, 0), (dx + 0.15, 1.75), (dx + 0.15, 0)
f.seg((dx - 0.3, 0), (dx + 4.25, 0), "otMuted,line width=.5pt,dash pattern=on 2pt off 1.6pt")
f.seg(H2, A2, "otGreenDark,line width=2.6pt,line cap=butt")
f.seg(C2, H2, "guide")
f.droit(H2, C2, B2, "otMuted", 0.2)
f.vect(A2, B2, "otNavy")
f.vect(A2, C2, "otOrange!90!black")
for p in (A2, H2, C2):
    f.pt(p)
f.lab(A2, "$A$", -60, 0.17); f.lab(H2, "$H$", 235); f.lab(B2, "$B$", -90, 0.17); f.lab(C2, "$C$", 90)
f.texte((dx + 2.0, -0.85), r"$\overrightarrow{AB} \cdot \overrightarrow{AC} = -AB \times AH$")
f.note((dx + 2.0, -1.38), "angle obtus : produit négatif")
f.add(r"\end{scope}")
FIGURES["cours_projection"] = f.tikz()

# --- Al-Kashi
f = Fig(0.95)
A, B, C = (0, 0), (5.4, 0), (1.9, 3.1)
f.poly([A, B, C], "geoTrait", "otSky")
G = centre(A, B, C)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.cote_seg(A, B, "$c$", -1)
f.cote_seg(A, C, "$b$", 1)
f.cote_seg(B, C, "$a$", -1)
f.arc(A, B, C, 0.6, "otGreenDark", r"$\widehat{A}$", 0.33)
f.texte((2.7, -0.95), r"$a^2 = b^2 + c^2 - 2bc\cos\widehat{A}$")
FIGURES["cours_alkashi"] = f.tikz()

# --- cercle de diamètre [AB]
f = Fig(1.0)
I, R = (0, 0), 2.0
A, B = (-R, 0), (R, 0)
M = (R * math.cos(math.radians(62)), R * math.sin(math.radians(62)))
M2 = (R * math.cos(math.radians(228)), R * math.sin(math.radians(228)))
f.cercle(I, R, "otGreenDark,line width=1.1pt")
f.seg(A, B, "geoTrait")
f.seg(A, M); f.seg(M, B)
f.seg(A, M2, "otNavy!55,line width=.8pt"); f.seg(M2, B, "otNavy!55,line width=.8pt")
f.droit(M, A, B, "otNavy", 0.24)
f.droit(M2, A, B, "otNavy!55", 0.24)
for p in (A, B, I, M, M2):
    f.pt(p)
f.lab(A, "$A$", 180); f.lab(B, "$B$", 0); f.lab(I, "$I$", -90, 0.16)
f.lab(M, "$M$", 62); f.lab(M2, "$M'$", 228)
f.texte((0, -2.55), r"$\overrightarrow{MA} \cdot \overrightarrow{MB} = 0 \iff M$ sur le cercle de diamètre $[AB]$")
FIGURES["cours_cercle"] = f.tikz()

# --- formule de la médiane
f = Fig(0.95)
A, B, M = (0, 0), (5.2, 0), (1.5, 2.9)
I = (2.6, 0)
f.poly([A, B, M])
f.seg(M, I, "otGreenDark,line width=1.1pt")
f.codage(A, I, 1); f.codage(I, B, 1)
G = centre(A, B, M)
for p, nm in ((A, "$A$"), (B, "$B$"), (M, "$M$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(I, "otGreenDark"); f.lab(I, "$I$", -90, 0.16)
f.texte((2.6, -0.95), r"$MA^2 + MB^2 = 2MI^2 + \frac{AB^2}{2}$")
FIGURES["cours_mediane"] = f.tikz()

# =================================================================== EXERCICES
# --- 1397 : triangle rectangle en A
f = Fig(0.8)
f.repere(-1, 6, -1, 5, gx=[1, 2, 3, 4, 5], gy=[1, 2, 3])
A, B, C = (2, 1), (5, 3), (0, 4)
G = centre(A, B, C)
f.poly([A, B, C])
f.droit(A, B, C, "otGreenDark", 0.26)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
FIGURES["ex1397_rectangle"] = f.tikz()

# --- 1397 : médiane
f = Fig(0.6)
f.repere(-1, 5, -1, 9, gx=[1, 2, 3, 4], gy=[2, 4, 6, 8])
A, B, C = (1, 2), (4, 6), (2, 8)
I = (3, 7)
G = centre(A, B, C)
f.poly([A, B, C])
f.seg(A, I, "otGreenDark,line width=1.1pt")
f.codage(B, I, 1); f.codage(I, C, 1)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(I, "otGreenDark"); f.lab(I, "$I$", 45, 0.14, "otGreenDark")
FIGURES["ex1397_mediane"] = f.tikz()

# --- 1398 : triangle 4, 5, 6
f = Fig(0.85)
cA = 1 / 8
A, B, C = (0, 0), (4, 0), (5 * cA, 5 * RAC(1 - cA ** 2))
G = triangle(f, [A, B, C], ["$A$", "$B$", "$C$"])
f.cote_seg(A, B, "$4$", -1)
f.cote_seg(A, C, "$5$", 1)
f.cote_seg(B, C, "$6$", -1)
f.arc(A, B, C, 0.55, "otGreenDark", r"$\widehat{A}$", 0.36)
FIGURES["ex1398_triangle"] = f.tikz()

# --- 1399 : décomposition MA, MB avec I
f = Fig(1.0)
A, B, I, M = (0, 0), (4.4, 0), (2.2, 0), (1.3, 2.3)
f.seg(A, B, "geoTrait")
f.vect(M, A, "otNavy")
f.vect(M, B, "otNavy")
f.vect(M, I, "otGreenDark")
f.codage(A, I, 1); f.codage(I, B, 1)
for p in (A, B, M):
    f.pt(p)
f.pt(I, "otGreenDark")
f.lab(A, "$A$", 200); f.lab(B, "$B$", -20); f.lab(M, "$M$", 90); f.lab(I, "$I$", -90, 0.16)
FIGURES["ex1399_decomposition"] = f.tikz()


def lieu(u, xr, yr, gx, gy, A, B, cercles, noms=None, O=True):
    """Repère, points A, B, I et cercles (centre, rayon, style, étiquette, angle)."""
    f = Fig(u)
    f.repere(xr[0], xr[1], yr[0], yr[1], gx=gx, gy=gy, O=O)
    I = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    for (O, r, st, lb, ang) in cercles:
        f.cercle(O, r, st)
        if lb:
            P = (O[0] + r * math.cos(math.radians(ang)), O[1] + r * math.sin(math.radians(ang)))
            f.lab(P, lb, ang, 0.1, "otGreenDark" if "Green" in st else "otNavy")
    f.seg(A, B, "geoTrait")
    noms = noms or ("$A$", "$B$", "$I$")
    for p in (A, B):
        f.pt(p)
    f.pt(I, "otGreenDark")
    return f, I


# --- 1399 q2 : A(0;0), B(4;0)
f, I = lieu(0.75, (-1, 5), (-3, 3), [1, 2, 3], [-2, -1, 1, 2], (0, 0), (4, 0),
            [((2, 0), 2, "otGreenDark,line width=1.1pt", None, 0)])
f.lab((0, 0), "$A$", 135, 0.16); f.lab((4, 0), "$B$", 45, 0.16); f.lab(I, "$I$", 90, 0.14, "otGreenDark")
FIGURES["ex1399_q2"] = f.tikz()

# --- 1399 q4 : A(2;1), B(6;3), I(4;2), rayon √5
f, I = lieu(0.7, (-1, 7), (-1, 5), [1, 2, 6], [1, 2, 3, 4], (2, 1), (6, 3),
            [((4, 2), RAC(5), "otGreenDark,line width=1.1pt", None, 0)])
f.lab((2, 1), "$A$", 206.6, 0.16); f.lab((6, 3), "$B$", 26.6, 0.16); f.lab(I, "$I$", 115, 0.15, "otGreenDark")
FIGURES["ex1399_q4"] = f.tikz()

# --- 1399 q5 : A(0;0), B(6;0), rayon 3√2 (et cercle de diamètre [AB] en pointillés)
f, I = lieu(0.5, (-2, 8), (-5, 5), [2, 4], [-4, 4], (0, 0), (6, 0),
            [((3, 0), 3, "otNavy!60,line width=.8pt,dash pattern=on 3pt off 2pt", None, 0),
             ((3, 0), 3 * RAC(2), "otGreenDark,line width=1.1pt", None, 0)])
f.lab((0, 0), "$A$", 125, 0.16); f.lab((6, 0), "$B$", 55, 0.16); f.lab(I, "$I$", 90, 0.14, "otGreenDark")
FIGURES["ex1399_q5"] = f.tikz()

# --- 1400 q1 : A(1;2), B(5;4), C(3;6)
f = Fig(0.7)
f.repere(-1, 6, -1, 7, gx=[1, 2, 3, 4, 5], gy=[1, 2, 3, 4, 5, 6])
A, B, C = (1, 2), (5, 4), (3, 6)
G = triangle(f, [A, B, C], ["$A$", "$B$", "$C$"])
f.codage(A, B, 2); f.codage(A, C, 2)
f.arc(A, B, C, 0.6, "otGreenDark")
FIGURES["ex1400_triangle"] = f.tikz()

# --- 1400 q3 : triangle 5, 6, 7
f = Fig(0.75)
A, B = (0, 0), (5, 0)
C = (6 * 0.2, 6 * RAC(1 - 0.04))
G = triangle(f, [A, B, C], ["$A$", "$B$", "$C$"])
f.cote_seg(A, B, "$5$", -1); f.cote_seg(A, C, "$6$", 1); f.cote_seg(B, C, "$7$", -1)
FIGURES["ex1400_triangle567"] = f.tikz()

# --- 1400 q4 : A(0;0), B(8;0), rayon 2√7
f, I = lieu(0.42, (-2, 10), (-6, 6), [2, 4, 6, 8], [-4, 4], (0, 0), (8, 0),
            [((4, 0), 2 * RAC(7), "otGreenDark,line width=1.1pt", None, 0)])
f.lab((0, 0), "$A$", 125, 0.16); f.lab((8, 0), "$B$", 55, 0.16); f.lab(I, "$I$", 90, 0.14, "otGreenDark")
FIGURES["ex1400_cercle"] = f.tikz()

# --- 1401 : rectangle (énoncé)
f = Fig(0.85)
A, B, C, D = (0, 0), (6, 0), (6, 4), (0, 4)
I = (3, 4)
f.poly([A, B, C, D])
f.seg(A, I, "otNavy!60,line width=.8pt")
f.codage(D, I, 1); f.codage(I, C, 1)
for p in (A, B, C, D, I):
    f.pt(p)
f.lab(A, "$A$", 225); f.lab(B, "$B$", -45); f.lab(C, "$C$", 45); f.lab(D, "$D$", 135); f.lab(I, "$I$", 90)
f.cote_seg(A, B, "$6$", -1, 0.16)
f.cote_seg(B, C, "$4$", -1, 0.16)
f.droit(A, B, D, "otNavy", 0.24); f.droit(B, C, A, "otNavy", 0.24)
FIGURES["ex1401_rectangle"] = f.tikz()

# --- 1401 : projection de I (corrigé)
f = Fig(0.85)
J = (3, 0)
f.poly([A, B, C, D])
f.seg(A, I, "otNavy!60,line width=.8pt")
f.seg(A, J, "otGreenDark,line width=2.4pt,line cap=butt")
f.seg(I, J, "guide")
f.droit(J, I, B, "otMuted", 0.22)
for p in (A, B, C, D, I):
    f.pt(p)
f.pt(J, "otGreenDark")
f.lab(A, "$A$", 225); f.lab(B, "$B$", -45); f.lab(C, "$C$", 45); f.lab(D, "$D$", 135); f.lab(I, "$I$", 90)
f.lab(J, "$J$", -90, 0.17, "otGreenDark")
FIGURES["ex1401_projection"] = f.tikz()

# --- 1401 : carré (énoncé et corrigé)
for nom, corrige in (("ex1401_carre", False), ("ex1401_carre_corrige", True)):
    f = Fig(0.95)
    A, B, C, D = (0, 0), (4, 0), (4, 4), (0, 4)
    I, J = (2, 0), (4, 2)
    K = (1.6, 0.8)
    f.poly([A, B, C, D])
    f.seg(D, I, "otOrange!90!black,line width=1pt")
    f.seg(A, J, "otOrange!90!black,line width=1pt")
    f.codage(A, I, 1); f.codage(I, B, 1); f.codage(B, J, 2); f.codage(J, C, 2)
    if corrige:
        f.droit(K, J, I, "otGreenDark", 0.24)
    for p in (A, B, C, D, I, J):
        f.pt(p)
    f.lab(A, "$A$", 225); f.lab(B, "$B$", -45); f.lab(C, "$C$", 45); f.lab(D, "$D$", 135)
    f.lab(I, "$I$", -90, 0.16); f.lab(J, "$J$", 0, 0.16)
    FIGURES[nom] = f.tikz()

# --- 1402 : triangle A(0;0), B(6;0), C(3;4) et hauteur
for nom, haut in (("ex1402_triangle", False), ("ex1402_hauteur", True)):
    f = Fig(0.75)
    f.repere(-1, 7, -1, 5, gx=[1, 2, 3, 4, 5, 6], gy=[1, 2, 3, 4], O=False)
    A, B, C = (0, 0), (6, 0), (3, 4)
    f.poly([A, B, C])
    if haut:
        H = (3.84, 2.88)
        f.seg(A, H, "otGreenDark,line width=1.1pt")
        f.droit(H, A, C, "otGreenDark", 0.22)
        f.pt(H, "otGreenDark"); f.lab(H, "$H$", 37, 0.15, "otGreenDark")
    f.codage(A, C, 2); f.codage(B, C, 2)
    for p in (A, B, C):
        f.pt(p)
    f.lab(A, "$A$", 135, 0.16); f.lab(B, "$B$", 45, 0.16); f.lab(C, "$C$", 90)
    FIGURES[nom] = f.tikz()

# --- 1402 : deux cercles de centre O, rayons 2 et 2√2
f, I = lieu(0.62, (-4, 4), (-4, 4), [], [], (-2, 0), (2, 0), O=False, cercles=
            [((0, 0), 2, "otNavy,line width=1.1pt", None, 0),
             ((0, 0), 2 * RAC(2), "otGreenDark,line width=1.1pt", r"$\mathcal{E}_2$", 52)])
f.lab((-2, 0), "$A$", 135, 0.16); f.lab((2, 0), "$B$", 45, 0.16); f.lab(I, "$I$", -60, 0.16, "otGreenDark")
f.lab((2 * math.cos(math.radians(128)), 2 * math.sin(math.radians(128))), r"$\mathcal{E}_1$", 308, 0.1, "otNavy")
FIGURES["ex1402_cercles"] = f.tikz()

# --- 1403 : A(2;1), B(6;5), C(4;7), rectangle en B, médiane [AI]
f = Fig(0.6)
f.repere(-1, 8, -1, 8, gx=[2, 4, 6], gy=[2, 4, 6])
A, B, C = (2, 1), (6, 5), (4, 7)
I = (5, 6)
G = centre(A, B, C)
f.poly([A, B, C])
f.seg(A, I, "otGreenDark,line width=1.1pt")
f.droit(B, A, C, "otGreenDark", 0.24)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(I, "otGreenDark"); f.lab(I, "$I$", 187, 0.15, "otGreenDark")
FIGURES["ex1403_triangle"] = f.tikz()

# --- 1404 : A(-1;2), B(3;4), C(1;8), rectangle isocèle en B
f = Fig(0.6)
f.repere(-2, 5, -1, 9, gx=[-1, 1, 2, 3, 4], gy=[6, 8])
A, B, C = (-1, 2), (3, 4), (1, 8)
G = centre(A, B, C)
f.poly([A, B, C])
f.droit(B, A, C, "otGreenDark", 0.24)
f.codage(A, B, 1); f.codage(B, C, 1)
f.arc(A, B, C, 0.6, "otGreenDark")
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
FIGURES["ex1404_triangle"] = f.tikz()

# --- 1404 : cercles de centre O, rayons 3 et 3√2
f, I = lieu(0.45, (-5, 5), (-5, 5), [], [], (-3, 0), (3, 0), O=False, cercles=
            [((0, 0), 3, "otNavy,line width=1.1pt", None, 0),
             ((0, 0), 3 * RAC(2), "otGreenDark,line width=1.1pt", r"$\mathcal{E}_2$", 52)])
f.lab((-3, 0), "$A$", 135, 0.16); f.lab((3, 0), "$B$", 45, 0.16); f.lab(I, "$I$", -60, 0.16, "otGreenDark")
f.lab((3 * math.cos(math.radians(128)), 3 * math.sin(math.radians(128))), r"$\mathcal{E}_1$", 308, 0.1, "otNavy")
FIGURES["ex1404_cercles"] = f.tikz()

# --- 1405 : triangle A(0;0), B(8;0), C(4;6)
f = Fig(0.6)
f.repere(-1, 9, -1, 7, gx=[2, 4, 6, 8], gy=[2, 4, 6], O=False)
A, B, C = (0, 0), (8, 0), (4, 6)
f.poly([A, B, C])
f.codage(A, C, 2); f.codage(B, C, 2)
for p in (A, B, C):
    f.pt(p)
f.lab(A, "$A$", 135, 0.16); f.lab(B, "$B$", 45, 0.16); f.lab(C, "$C$", 90)
FIGURES["ex1405_triangle"] = f.tikz()

# --- 1405 : cercles C1, C2, C3 de centre I(4;0)
f, I = lieu(0.42, (-3, 11), (-7, 7), [], [], (0, 0), (8, 0),
            [((4, 0), 2, "otGreenDark,line width=1.1pt", r"$\mathcal{C}_2$", 60),
             ((4, 0), 4, "otNavy,line width=1.1pt", r"$\mathcal{C}_1$", 60),
             ((4, 0), 6, "otOrange!90!black,line width=1.1pt", r"$\mathcal{C}_3$", 60)])
f.lab((0, 0), "$A$", 135, 0.16); f.lab((8, 0), "$B$", 45, 0.16); f.lab(I, "$I$", -90, 0.16, "otGreenDark")
FIGURES["ex1405_cercles"] = f.tikz()

# --- nouveau-1 : quadrillage, projection sur (AB)
for nom, corrige in (("n1_quadrillage", False), ("n1_quadrillage_corrige", True)):
    f = Fig(0.75)
    f.add(r"\draw[otRule!80,line width=.35pt] (-3,-4) grid (6,4);")
    f.seg((-3, 0), (6, 0), "otMuted,line width=.5pt,dash pattern=on 2pt off 1.6pt")
    A, B = (0, 0), (4, 0)
    pts = {"C": (3, 2), "D": (-2, 3), "E": (2, -3), "F": (0, 3)}
    if corrige:
        f.seg(A, (3, 0), "otGreenDark,line width=2.4pt,line cap=butt")
        f.seg((-2, 0), A, "otRed,line width=2.4pt,line cap=butt")
        for p in ("C", "D", "E"):
            P = pts[p]
            f.seg(P, (P[0], 0), "guide")
        f.seg(pts["F"], A, "guide")
    f.vect(A, B, "otNavy", "1.1pt")
    for nm, P in pts.items():
        f.pt(P)
    f.pt(A)
    f.lab(A, "$A$", 225, 0.15); f.lab(B, "$B$", -60, 0.16)
    f.lab(pts["C"], "$C$", 45); f.lab(pts["D"], "$D$", 135); f.lab(pts["E"], "$E$", -45); f.lab(pts["F"], "$F$", 45)
    if corrige:
        for P, nm, ang in (((3, 0), "$H$", -60), ((-2, 0), "$K$", -120), ((2, 0), "$L$", 60)):
            f.pt(P, "otGreenDark")
            f.lab(P, nm, ang, 0.15, "otGreenDark")
    FIGURES[nom] = f.tikz()

# --- nouveau-1 : triangle équilatéral, pied de la hauteur
f = Fig(0.75)
A, B = (0, 0), (6, 0)
C = (3, 3 * RAC(3))
H = (3, 0)
f.poly([A, B, C])
f.seg(A, H, "otGreenDark,line width=2.4pt,line cap=butt")
f.seg(C, H, "guide")
f.droit(H, C, B, "otMuted", 0.22)
f.codage(A, C, 2); f.codage(B, C, 2); f.codage(A, B, 2)
G = centre(A, B, C)
for p, nm in ((A, "$R$"), (B, "$S$"), (C, "$T$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(H, "otGreenDark"); f.lab(H, "$K$", -90, 0.17, "otGreenDark")
FIGURES["n1_equilateral"] = f.tikz()

# --- nouveau-2 : triangle AB = 6, AC = 4, BC = 5, médiane [AI]
f = Fig(0.9)
cA = 9 / 16
A, B, C = (0, 0), (6, 0), (4 * cA, 4 * RAC(1 - cA ** 2))
I = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
G = centre(A, B, C)
f.poly([A, B, C])
f.seg(A, I, "otGreenDark,line width=1.1pt")
f.codage(B, I, 1); f.codage(I, C, 1)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(I, "otGreenDark"); f.lab(I, "$I$", math.degrees(math.atan2(I[1], I[0])) + 90 - 90 + 15, 0.15, "otGreenDark")
f.cote_seg(A, B, "$6$", -1); f.cote_seg(A, C, "$4$", 1)
FIGURES["n2_triangle"] = f.tikz()

# --- nouveau-3 : randonneur (énoncé et corrigé)
for nom, corrige in (("n3_schema", False), ("n3_corrige", True)):
    f = Fig(0.8)
    A, C = (0, 0), (5, 0)
    B = (3 * math.cos(math.radians(120)), 3 * math.sin(math.radians(120)))
    H = (B[0], 0)
    if corrige:
        f.seg(H, A, "otGreenDark,line width=2.4pt,line cap=butt")
        f.seg(B, H, "otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt")
        f.droit(H, B, C, "otGreenDark", 0.22)
        f.seg((B[0] - 0.6, 0), A, "otMuted,line width=.5pt,dash pattern=on 2pt off 1.6pt")
    f.seg(A, B); f.seg(A, C)
    f.seg(B, C, "otNavy,line width=.9pt,dash pattern=on 4pt off 2.5pt")
    f.arc(A, C, B, 0.5, "otOrange!90!black", r"$120°$", 0.38)
    for p in (A, B, C):
        f.pt(p)
    f.lab(A, "$A$", -60, 0.16); f.lab(B, "$B$", 110); f.lab(C, "$C$", 0)
    if not corrige:
        f.cote_seg(A, B, r"$3$ km", 1)
    f.cote_seg(A, C, r"$5$ km", -1, 0.16)
    if corrige:
        f.pt(H, "otGreenDark"); f.lab(H, "$H$", -90, 0.17, "otGreenDark")
    FIGURES[nom] = f.tikz()


# =================================================================== COMPLÉMENTS
# Figures d'énoncé (sans réponse) et figures de corrigé (réponses en vert)
# ajoutées pour que chaque énoncé et chaque corrigé de géométrie montre sa figure.

def tri_repere(u, xr, yr, gx, gy, pts, noms=("$A$", "$B$", "$C$"), O=True, angles=None):
    """Triangle dans un repère ; étiquettes vers l'extérieur."""
    f = Fig(u)
    f.repere(xr[0], xr[1], yr[0], yr[1], gx=gx, gy=gy, O=O)
    G = centre(*pts)
    f.poly(list(pts))
    for p, nm in zip(pts, noms):
        f.pt(p)
        f.lab(p, nm, (angles or {}).get(nm, ext(p, G)))
    return f


# --- 1405 : hauteur issue de C (corrigé, aire)
f = Fig(0.6)
f.repere(-1, 9, -1, 7, gx=[2, 6, 8], gy=[2, 4, 6], O=False)
A, B, C, H = (0, 0), (8, 0), (4, 6), (4, 0)
f.poly([A, B, C])
f.seg(C, H, "otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt")
f.droit(H, C, B, "otGreenDark", 0.22)
for p in (A, B, C):
    f.pt(p)
f.pt(H, "otGreenDark")
f.lab(A, "$A$", 135, 0.16); f.lab(B, "$B$", 45, 0.16); f.lab(C, "$C$", 90); f.lab(H, "$H$", -60, 0.17, "otGreenDark")
FIGURES["ex1405_triangle_corrige"] = f.tikz()

# --- 1405 partie C : triangle DEF (énoncé et corrigé)
for nom, corrige in (("ex1405_def", False), ("ex1405_def_corrige", True)):
    f = Fig(0.5)
    D, E = (0, 0), (10, 0)
    F = (8 * 0.5, 8 * math.sin(math.radians(60)))
    f.seg(D, E); f.seg(D, F)
    f.seg(E, F, "otGreenDark,line width=1.2pt" if corrige else "otNavy,line width=.9pt,dash pattern=on 4pt off 2.5pt")
    f.arc(D, E, F, 0.5, "otOrange!90!black", r"$60°$", 0.38)
    if corrige:
        f.arc(E, F, D, 0.5, "otGreenDark")
        f.arc(F, D, E, 0.45, "otGreenDark")
    G = centre(D, E, F)
    for p, nm in ((D, "$D$"), (E, "$E$"), (F, "$F$")):
        f.pt(p); f.lab(p, nm, ext(p, G))
    f.cote_seg(D, E, "$10$", -1, 0.16)
    f.cote_seg(D, F, "$8$", 1)
    if corrige:
        f.cote_seg(F, E, r"$2\sqrt{21}$", 1, 0.14, "otGreenDark")
    FIGURES[nom] = f.tikz()

# --- 1401 : projection de C sur (AB) (corrigé A1)
f = Fig(0.85)
A, B, C, D = (0, 0), (6, 0), (6, 4), (0, 4)
f.poly([A, B, C, D])
f.seg(A, B, "otGreenDark,line width=2.4pt,line cap=butt")
f.vect(A, C, "otOrange!90!black")
f.droit(B, C, A, "otNavy", 0.24)
for p in (A, B, C, D):
    f.pt(p)
f.lab(A, "$A$", 225); f.lab(B, "$B$", -45); f.lab(C, "$C$", 45); f.lab(D, "$D$", 135)
f.cote_seg(A, B, "$6$", -1, 0.16, "otGreenDark")
FIGURES["ex1401_rect_corrige"] = f.tikz()

# --- 1403 : triangle (énoncé), triangle d'Al-Kashi (énoncé et corrigé)
f = tri_repere(0.6, (-1, 8), (-1, 8), [2, 4, 6], [2, 4, 6], [(2, 1), (6, 5), (4, 7)])
FIGURES["ex1403_triangle_enonce"] = f.tikz()

for nom, corrige in (("ex1403_alkashi", False), ("ex1403_alkashi_corrige", True)):
    f = Fig(0.6)
    A, B = (0, 0), (7, 0)
    C = (5 * math.cos(math.radians(120)), 5 * math.sin(math.radians(120)))
    f.seg(A, B); f.seg(A, C)
    f.seg(B, C, "otGreenDark,line width=1.2pt" if corrige else "otNavy,line width=.9pt,dash pattern=on 4pt off 2.5pt")
    f.arc(A, B, C, 0.5, "otOrange!90!black", r"$\frac{2\pi}{3}$", 0.4)
    G = centre(A, B, C)
    for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
        f.pt(p); f.lab(p, nm, ext(p, G))
    f.cote_seg(A, B, "$7$", -1, 0.16)
    f.cote_seg(A, C, "$5$", 1)
    if corrige:
        f.cote_seg(B, C, r"$\sqrt{109}$", -1, 0.14, "otGreenDark")
    FIGURES[nom] = f.tikz()

# --- 1397 : corrigés des questions 1, 2, 3
f = tri_repere(0.7, (-1, 5), (-1, 7), [1, 2, 3, 4], [1, 2, 3, 4, 5, 6], [(1, 2), (4, 6), (2, 5)])
f.arc((2, 5), (1, 2), (4, 6), 0.4, "otGreenDark")
FIGURES["ex1397_q1"] = f.tikz()

f = Fig(0.6)
f.repere(-1, 6, -1, 8, gx=[2, 3, 4, 5], gy=[2, 6], O=True)
A, B, C, D = (1, 3), (5, 7), (0, 4), (3, 1)
f.seg(A, B); f.seg(C, D)
f.droit(A, B, D, "otGreenDark", 0.24)
for p in (A, B, C, D):
    f.pt(p)
f.lab(A, "$A$", 225, 0.16); f.lab(B, "$B$", 0); f.lab(C, "$C$", 135, 0.16); f.lab(D, "$D$", 0)
FIGURES["ex1397_q2"] = f.tikz()

f = Fig(0.7)
f.repere(-1, 4, -1, 6, gx=[1, 2, 3], gy=[1, 2, 3, 4, 5], O=False)
A, B, C = (0, 0), (3, 4), (1, 5)
f.vect(A, B, "otNavy"); f.vect(A, C, "otNavy")
f.arc(A, B, C, 0.75, "otGreenDark")
f.pt(A)
f.lab(A, "$A$", 225, 0.16); f.lab(B, "$B$", 0); f.lab(C, "$C$", 90)
FIGURES["ex1397_q3"] = f.tikz()

# --- 1398 : corrigés des questions 1, 2, 5
f = Fig(0.55)
A, B = (0, 0), (5, 0)
C = (3.5, 7 * math.sin(math.radians(60)))
f.seg(A, B); f.seg(A, C); f.seg(B, C, "otGreenDark,line width=1.2pt")
f.arc(A, B, C, 0.5, "otOrange!90!black", r"$60°$", 0.38)
G = centre(A, B, C)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.cote_seg(A, B, "$5$", -1, 0.16); f.cote_seg(A, C, "$7$", 1)
f.cote_seg(B, C, r"$\sqrt{39}$", -1, 0.14, "otGreenDark")
FIGURES["ex1398_q1"] = f.tikz()

f = Fig(0.5)
B, A, C = (0, 0), (0, 6), (8, 0)
f.poly([A, B, C])
f.droit(B, A, C, "otGreenDark", 0.26)
G = centre(A, B, C)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.cote_seg(B, A, "$6$", -1, 0.16); f.cote_seg(B, C, "$8$", 1, 0.16); f.cote_seg(A, C, "$10$", -1)
FIGURES["ex1398_q2"] = f.tikz()

f = Fig(0.55)
A, B = (0, 0), (4, 0)
aa = math.acos(-0.25)
C = (6 * math.cos(aa), 6 * math.sin(aa))
f.poly([A, B, C])
f.arc(A, B, C, 0.45, "otGreenDark")
G = centre(A, B, C)
for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.cote_seg(A, B, "$4$", -1, 0.16); f.cote_seg(A, C, "$6$", 1); f.cote_seg(B, C, "$8$", -1)
FIGURES["ex1398_q5"] = f.tikz()

# --- 1400 : triangle (énoncé) et triangle 5, 6, 7 corrigé
f = tri_repere(0.7, (-1, 6), (-1, 7), [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [(1, 2), (5, 4), (3, 6)])
FIGURES["ex1400_triangle_enonce"] = f.tikz()

f = Fig(0.75)
A, B = (0, 0), (5, 0)
C = (6 * 0.2, 6 * RAC(1 - 0.04))
G = triangle(f, [A, B, C], ["$A$", "$B$", "$C$"])
f.cote_seg(A, B, "$5$", -1); f.cote_seg(A, C, "$6$", 1); f.cote_seg(B, C, "$7$", -1)
f.arc(A, B, C, 0.5, "otGreenDark")
f.arc(B, C, A, 0.5, "otGreenDark")
f.arc(C, A, B, 0.6, "otGreenDark")
FIGURES["ex1400_triangle567_corrige"] = f.tikz()

# --- 1404 : triangle (énoncé)
f = tri_repere(0.6, (-2, 5), (-1, 9), [-1, 1, 2, 3, 4], [6, 8], [(-1, 2), (3, 4), (1, 8)])
FIGURES["ex1404_triangle_enonce"] = f.tikz()

# --- nouveau-1 : triangle équilatéral (énoncé)
f = Fig(0.75)
A, B = (0, 0), (6, 0)
C = (3, 3 * RAC(3))
H = (3, 0)
f.poly([A, B, C])
f.codage(A, C, 2); f.codage(B, C, 2); f.codage(A, H, 1); f.codage(H, B, 1)
G = centre(A, B, C)
for p, nm in ((A, "$R$"), (B, "$S$"), (C, "$T$")):
    f.pt(p); f.lab(p, nm, ext(p, G))
f.pt(H); f.lab(H, "$K$", -90, 0.17)
FIGURES["n1_equilateral_enonce"] = f.tikz()

# --- nouveau-2 : énoncé (médiane en bleu) et corrigé (médiane et angle en vert)
for nom, corrige in (("n2_triangle", False), ("n2_corrige", True)):
    f = Fig(0.9)
    cA = 9 / 16
    A, B, C = (0, 0), (6, 0), (4 * cA, 4 * RAC(1 - cA ** 2))
    I = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    G = centre(A, B, C)
    f.poly([A, B, C])
    col = "otGreenDark" if corrige else "otNavy"
    f.seg(A, I, col + ",line width=1.1pt" if corrige else "otNavy,line width=.9pt,dash pattern=on 4pt off 2.5pt")
    if corrige:
        f.arc(A, B, C, 0.75, "otGreenDark")
    f.codage(B, I, 1); f.codage(I, C, 1)
    for p, nm in ((A, "$A$"), (B, "$B$"), (C, "$C$")):
        f.pt(p); f.lab(p, nm, ext(p, G))
    f.pt(I, col); f.lab(I, "$I$", 37, 0.15, col)
    f.cote_seg(A, B, "$6$", -1); f.cote_seg(A, C, "$4$", 1)
    FIGURES[nom] = f.tikz()
